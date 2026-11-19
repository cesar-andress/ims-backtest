"""Download applied preferential tariffs from the WITS TRN SDMX API.

Endpoint pattern (World Bank WITS)::

    /API/V1/SDMX/V21/datasource/TRN/reporter/{rep}/partner/{origin}/product/all/year/{y}/datatype/{reported|aveestimated}

Reporters are the destination set (EU members → reporter 918). Partners are the
configured origins. HS6 lines in configured chapters are aggregated to a simple
average AHS per (destination, origin, chapter, year). When a product has
non-ad-valorem lines (``NBR_NA_LINES`` > 0), the ``aveestimated`` observation is
preferred when available. Missing years can be filled by LOCF with an explicit
``tarif_locf`` flag.
"""

from __future__ import annotations

import time
import xml.etree.ElementTree as ET
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import requests

from imsfe.config import Settings, load_settings
from imsfe.download.iso_codes import (
    EU27_ISO3,
    wits_partner_code,
    wits_reporter_code,
)
from imsfe.io import raw_dir, record_artifact, sha256_file, should_skip

WITS_PARQUET_REL = "wits/ahs_tariffs.parquet"
TRN_DEFAULT_BASE = "https://wits.worldbank.org/API/V1/SDMX/V21/datasource/TRN"


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def trn_url(
    reporter: str,
    partner: str,
    year: int,
    datatype: str,
    *,
    base_url: str = TRN_DEFAULT_BASE,
) -> str:
    """Build a WITS TRN StructureSpecific SDMX URL."""
    base = base_url.rstrip("/")
    return (
        f"{base}/reporter/{reporter}/partner/{partner}/product/all/"
        f"year/{int(year)}/datatype/{datatype}"
    )


def cache_path_for_url(url: str, *, cache_dir: Path | None = None) -> Path:
    """Deterministic cache path under ``data/raw/wits/`` for a TRN URL."""
    root = cache_dir or (raw_dir() / "wits")
    # reporter/partner/year/datatype from URL tail
    parts = url.rstrip("/").split("/")
    try:
        rep = parts[parts.index("reporter") + 1]
        partner = parts[parts.index("partner") + 1]
        year = parts[parts.index("year") + 1]
        dtype = parts[parts.index("datatype") + 1]
    except (ValueError, IndexError) as exc:
        raise ValueError(f"Cannot derive cache path from URL: {url}") from exc
    return root / f"trn_r{rep}_p{partner}_y{year}_{dtype}.xml"


def parse_trn_xml(xml_text: str | bytes) -> pd.DataFrame:
    """Parse StructureSpecific TRN XML into one row per HS6 product series."""
    if isinstance(xml_text, bytes):
        xml_text = xml_text.decode("utf-8", errors="replace")
    if not xml_text.strip():
        return pd.DataFrame(
            columns=[
                "product_code",
                "reporter",
                "partner",
                "year",
                "ahs",
                "nbr_na_lines",
                "datatype",
                "tariff_type",
            ]
        )
    root = ET.fromstring(xml_text)
    rows: list[dict[str, Any]] = []
    for el in root.iter():
        if _local(el.tag) != "Series":
            continue
        sattrs = {_local(k): v for k, v in el.attrib.items()}
        product = str(sattrs.get("PRODUCTCODE", "")).strip()
        if not product:
            continue
        reporter = str(sattrs.get("REPORTER", "")).strip()
        partner = str(sattrs.get("PARTNER", "")).strip()
        datatype = str(sattrs.get("DATATYPE", "")).strip()
        for obs in list(el):
            if _local(obs.tag) != "Obs":
                continue
            oattrs = {_local(k): v for k, v in obs.attrib.items()}
            year_raw = oattrs.get("TIME_PERIOD")
            val_raw = oattrs.get("OBS_VALUE")
            if year_raw is None or val_raw is None:
                continue
            try:
                year = int(str(year_raw)[:4])
                ahs = float(val_raw)
            except (TypeError, ValueError):
                continue
            try:
                nbr_na = int(float(oattrs.get("NBR_NA_LINES") or 0))
            except (TypeError, ValueError):
                nbr_na = 0
            rows.append(
                {
                    "product_code": product,
                    "reporter": reporter,
                    "partner": partner,
                    "year": year,
                    "ahs": ahs,
                    "nbr_na_lines": nbr_na,
                    "datatype": datatype,
                    "tariff_type": oattrs.get("TARIFFTYPE", ""),
                }
            )
    return pd.DataFrame.from_records(rows)


def filter_chapters(lines: pd.DataFrame, chapters: Iterable[str]) -> pd.DataFrame:
    """Keep HS6 rows whose product code starts with a configured chapter."""
    if lines.empty:
        return lines.copy()
    prefixes = {str(c).zfill(2) for c in chapters}
    out = lines.copy()
    out["hs_chapter"] = out["product_code"].astype(str).str[:2]
    return out.loc[out["hs_chapter"].isin(prefixes)].copy()


def merge_reported_aveestimated(
    reported: pd.DataFrame,
    aveestimated: pd.DataFrame,
) -> pd.DataFrame:
    """Prefer aveestimated AHS when reported lines have non-ad-valorem rates."""
    if reported.empty and aveestimated.empty:
        return reported.copy()
    if aveestimated.empty:
        return reported.copy()
    if reported.empty:
        return aveestimated.copy()

    key = ["product_code", "reporter", "partner", "year"]
    ave = aveestimated.drop_duplicates(key, keep="first").set_index(key)["ahs"]
    rows: list[dict[str, Any]] = []
    for _, row in reported.iterrows():
        rec = row.to_dict()
        k = tuple(row[c] for c in key)
        if int(row.get("nbr_na_lines") or 0) > 0 and k in ave.index:
            rec["ahs"] = float(ave.loc[k])
            rec["datatype"] = "AveEstimated"
            rec["ahs_source"] = "aveestimated"
        else:
            rec["ahs_source"] = "reported"
        rows.append(rec)
    return pd.DataFrame.from_records(rows)


def aggregate_chapter_ahs(lines: pd.DataFrame) -> pd.DataFrame:
    """Simple average of HS6 AHS rates by reporter/partner/chapter/year."""
    if lines.empty:
        return pd.DataFrame(
            columns=[
                "reporter",
                "partner",
                "year",
                "hs_chapter",
                "ahs_simple_avg",
                "n_hs6",
                "n_na_products",
            ]
        )
    df = lines.copy()
    if "hs_chapter" not in df.columns:
        df["hs_chapter"] = df["product_code"].astype(str).str[:2]
    g = (
        df.groupby(["reporter", "partner", "year", "hs_chapter"], as_index=False)
        .agg(
            ahs_simple_avg=("ahs", "mean"),
            n_hs6=("product_code", "nunique"),
            n_na_products=(
                "nbr_na_lines",
                lambda s: int((pd.to_numeric(s, errors="coerce").fillna(0) > 0).sum()),
            ),
        )
    )
    return g


def apply_locf(
    panel: pd.DataFrame,
    *,
    value_col: str = "ahs_simple_avg",
    flag_col: str = "tarif_locf",
    source_col: str = "tarif_source",
    enabled: bool = True,
) -> pd.DataFrame:
    """Last-observation-carried-forward by (dest, origin, chapter); flag fills.

    Only pairs that already have at least one non-null ``value_col`` observation
    are forward-filled. Pairs that are entirely missing stay missing (MFN fill
    happens later). LOCF cells get ``tarif_source='partner_locf'``.
    """
    if panel.empty:
        out = panel.copy()
        out[flag_col] = pd.Series(dtype=bool)
        if source_col not in out.columns:
            out[source_col] = pd.Series(dtype=object)
        return out
    out = panel.sort_values(
        ["reporter_iso3", "partner_iso3", "hs_chapter", "year"]
    ).copy()
    out[flag_col] = False
    if source_col not in out.columns:
        out[source_col] = pd.NA
    # Observed partner-specific cells
    obs = out[value_col].notna()
    src_missing = out[source_col].isna() | (out[source_col].astype(str) == "<NA>")
    out.loc[obs & src_missing, source_col] = "partner_specific"
    if not enabled:
        return out
    keys = ["reporter_iso3", "partner_iso3", "hs_chapter"]
    filled_parts: list[pd.DataFrame] = []
    for _, g in out.groupby(keys, sort=False):
        gg = g.copy()
        if not gg[value_col].notna().any():
            filled_parts.append(gg)
            continue
        before = gg[value_col].isna()
        gg[value_col] = gg[value_col].ffill()
        locf_mask = before & gg[value_col].notna()
        gg.loc[locf_mask, flag_col] = True
        gg.loc[locf_mask, source_col] = "partner_locf"
        filled_parts.append(gg)
    return pd.concat(filled_parts, ignore_index=True)


def apply_mfn_fallback(
    panel: pd.DataFrame,
    mfn: pd.DataFrame,
    *,
    value_col: str = "ahs_simple_avg",
    source_col: str = "tarif_source",
) -> pd.DataFrame:
    """Fill never-observed partner pairs with reporter-year MFN (partner 000).

    ``mfn`` columns: ``reporter_iso3``, ``year``, ``hs_chapter``, ``mfn_simple_avg``.
    """
    if panel.empty:
        return panel.copy()
    out = panel.copy()
    if source_col not in out.columns:
        out[source_col] = pd.NA
    if mfn.empty:
        return out
    m = mfn.rename(columns={"mfn_simple_avg": "_mfn"}).copy()
    m["hs_chapter"] = m["hs_chapter"].astype(str).str.zfill(2)
    out = out.merge(
        m[["reporter_iso3", "year", "hs_chapter", "_mfn"]],
        on=["reporter_iso3", "year", "hs_chapter"],
        how="left",
    )
    fill = out[value_col].isna() & out["_mfn"].notna()
    out.loc[fill, value_col] = out.loc[fill, "_mfn"]
    out.loc[fill, source_col] = "mfn_no_preference"
    if "tarif_locf" in out.columns:
        out.loc[fill, "tarif_locf"] = False
    return out.drop(columns=["_mfn"])


def _get_with_retries(
    session: requests.Session,
    url: str,
    *,
    retries: int = 5,
    backoff: float = 1.5,
    timeout: int = 90,
) -> tuple[int, bytes]:
    last_exc: Exception | None = None
    for attempt in range(retries):
        try:
            resp = session.get(url, timeout=timeout)
            if resp.status_code in (200, 404):
                return resp.status_code, resp.content
            if resp.status_code in (429, 500, 502, 503, 504):
                time.sleep(backoff * (2**attempt))
                continue
            return resp.status_code, resp.content
        except requests.RequestException as exc:
            last_exc = exc
            time.sleep(backoff * (2**attempt))
    if last_exc is not None:
        raise RuntimeError(f"WITS request failed after retries: {url}") from last_exc
    raise RuntimeError(f"WITS request failed after retries: {url}")


def fetch_cached_xml(
    url: str,
    *,
    session: requests.Session,
    force: bool = False,
    retries: int = 5,
    backoff: float = 1.5,
) -> tuple[Path, int, bool]:
    """Fetch URL into the raw WITS cache. Returns (path, http_status, from_cache)."""
    path = cache_path_for_url(url)
    if path.is_file() and path.stat().st_size > 0 and not force:
        return path, 200, True
    status, content = _get_with_retries(
        session, url, retries=retries, backoff=backoff
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return path, status, False


def destinations_from_baci(settings: Settings) -> list[str]:
    """Union of top-N destinations across origins (same rule as the panel)."""
    from imsfe.build.panel import (
        destination_import_totals,
        load_baci_chapter_flows,
        select_destinations_for_origin,
    )

    chapter = str(settings.hs_chapters.primary).zfill(2)
    flows = load_baci_chapter_flows(settings, chapter=chapter)
    totals = destination_import_totals(flows, settings.years.end)
    dests: set[str] = set()
    for origin in settings.origins:
        dests.update(
            select_destinations_for_origin(totals, origin, settings.n_destinations)
        )
    return sorted(dests)


def fetch_wits(settings: Settings | None = None, *, force: bool = False) -> dict[str, Any]:
    """Download TRN tariffs, aggregate to chapter AHS, optional LOCF, write parquet."""
    settings = settings or load_settings()
    version = settings.wits.version
    rel = WITS_PARQUET_REL
    if should_skip("wits", version, [rel], force=force):
        return {"skipped": True, "parquet": str(raw_dir() / rel)}

    base_url = (settings.wits.base_url or TRN_DEFAULT_BASE).rstrip("/")
    # Prefer TRN datasource path even if legacy TradeStats URL remains in old configs.
    if "datasource/TRN" not in base_url:
        base_url = TRN_DEFAULT_BASE

    locf = bool(getattr(settings.wits, "locf", True))
    max_workers = int(getattr(settings.wits, "max_workers", 8))
    retries = int(getattr(settings.wits, "retries", 5))
    backoff = float(getattr(settings.wits, "backoff_sec", 1.5))
    years = list(range(settings.years.start, settings.years.end + 1))
    chapters = settings.hs_chapter_codes()

    destinations = destinations_from_baci(settings)
    # Unique WITS reporters (EU collapsed to 918). Skip BACI residual codes
    # without ISO numeric identifiers (e.g. S19 "Other Asia, nes").
    seen_rep: set[str] = set()
    skipped_dests: list[str] = []
    eu_dests = [d for d in destinations if d in EU27_ISO3]
    non_eu = [d for d in destinations if d not in EU27_ISO3]
    resolved_non_eu: list[str] = []
    for d in non_eu:
        try:
            seen_rep.add(wits_reporter_code(d))
            resolved_non_eu.append(d)
        except KeyError:
            skipped_dests.append(d)
    non_eu = resolved_non_eu
    if eu_dests:
        seen_rep.add("918")
    if skipped_dests:
        print(
            f"WITS: skipping destinations without ISO numeric codes: {skipped_dests}",
            flush=True,
        )

    partners = [(o, wits_partner_code(o)) for o in settings.origins]

    session = requests.Session()
    session.trust_env = False
    session.headers.update({"User-Agent": "imsfe-wits/2.0 (research; mailto:research@example.com)"})

    # Build fetch list: unique (reporter_code, partner_code, year) × reported
    # (+ aveestimated only when needed after parse — second pass)
    fetch_keys: list[tuple[str, str, int, str]] = []
    unique_reporters = sorted(seen_rep)
    for rep in unique_reporters:
        for _origin, partner in partners:
            for year in years:
                fetch_keys.append((rep, partner, year, "reported"))

    def _one(key: tuple[str, str, int, str]) -> dict[str, Any]:
        rep, partner, year, dtype = key
        url = trn_url(rep, partner, year, dtype, base_url=base_url)
        path, status, cached = fetch_cached_xml(
            url, session=session, force=force, retries=retries, backoff=backoff
        )
        return {
            "reporter": rep,
            "partner": partner,
            "year": year,
            "datatype": dtype,
            "path": str(path),
            "status": status,
            "cached": cached,
            "url": url,
        }

    meta_rows: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futs = {pool.submit(_one, k): k for k in fetch_keys}
        for fut in as_completed(futs):
            meta_rows.append(fut.result())

    # Parse reported, decide which need aveestimated
    line_frames: list[pd.DataFrame] = []
    need_ave: list[tuple[str, str, int]] = []
    for meta in meta_rows:
        if meta["status"] != 200:
            continue
        path = Path(meta["path"])
        if path.stat().st_size < 50:
            continue
        lines = parse_trn_xml(path.read_bytes())
        lines = filter_chapters(lines, chapters)
        if lines.empty:
            continue
        line_frames.append(lines)
        if (lines["nbr_na_lines"].fillna(0) > 0).any():
            need_ave.append((meta["reporter"], meta["partner"], meta["year"]))

    # Second pass: aveestimated for triples with NA lines
    need_ave = sorted(set(need_ave))
    ave_frames: list[pd.DataFrame] = []
    if need_ave:
        ave_keys = [(r, p, y, "aveestimated") for r, p, y in need_ave]

        def _ave(key: tuple[str, str, int, str]) -> dict[str, Any]:
            return _one(key)

        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            for fut in as_completed({pool.submit(_ave, k): k for k in ave_keys}):
                meta = fut.result()
                meta_rows.append(meta)
                if meta["status"] != 200:
                    continue
                path = Path(meta["path"])
                if path.stat().st_size < 50:
                    continue
                lines = filter_chapters(parse_trn_xml(path.read_bytes()), chapters)
                if not lines.empty:
                    ave_frames.append(lines)

    reported_all = (
        pd.concat(line_frames, ignore_index=True) if line_frames else pd.DataFrame()
    )
    ave_all = pd.concat(ave_frames, ignore_index=True) if ave_frames else pd.DataFrame()
    merged = merge_reported_aveestimated(reported_all, ave_all)
    agg = aggregate_chapter_ahs(merged)

    # Map reporter/partner numeric → ISO3 destinations
    partner_inv = {wits_partner_code(o): o for o in settings.origins}
    # Expand EU reporter onto each EU destination present in the destination set
    rows_out: list[dict[str, Any]] = []
    for _, row in agg.iterrows():
        partner_iso = partner_inv.get(str(row["partner"]).zfill(3)) or partner_inv.get(
            str(int(row["partner"]))
        )
        if partner_iso is None:
            # try without zfill variants
            for code, iso in partner_inv.items():
                if str(int(code)) == str(int(row["partner"])):
                    partner_iso = iso
                    break
        if partner_iso is None:
            continue
        rep = str(row["reporter"]).zfill(3)
        if rep == "918" or str(int(rep)) == "918":
            dest_list = [d for d in destinations if d in EU27_ISO3]
        else:
            # reverse numeric → iso3 among non-EU destinations
            dest_list = []
            for d in non_eu:
                try:
                    if wits_reporter_code(d) == rep or int(wits_reporter_code(d)) == int(rep):
                        dest_list.append(d)
                except KeyError:
                    continue
        for dest in dest_list:
            rows_out.append(
                {
                    "reporter_iso3": dest,
                    "partner_iso3": partner_iso,
                    "year": int(row["year"]),
                    "hs_chapter": str(row["hs_chapter"]).zfill(2),
                    "ahs_simple_avg": float(row["ahs_simple_avg"]),
                    "n_hs6": int(row["n_hs6"]),
                    "n_na_products": int(row.get("n_na_products", 0)),
                }
            )

    partner_obs = pd.DataFrame.from_records(rows_out)

    # Full destination × origin × year × chapter grid (includes never-preferred pairs).
    resolved_dests = sorted(set(eu_dests) | set(non_eu))
    grid = (
        pd.MultiIndex.from_product(
            [resolved_dests, settings.origins, years, chapters],
            names=["reporter_iso3", "partner_iso3", "year", "hs_chapter"],
        )
        .to_frame(index=False)
    )
    if partner_obs.empty:
        df = grid.copy()
        df["ahs_simple_avg"] = np.nan
        df["n_hs6"] = pd.NA
        df["n_na_products"] = pd.NA
        df["tarif_source"] = pd.NA
    else:
        df = grid.merge(
            partner_obs,
            on=["reporter_iso3", "partner_iso3", "year", "hs_chapter"],
            how="left",
        )
        df["tarif_source"] = pd.NA
    df = apply_locf(df, enabled=locf)

    # MFN (partner 000) for reporter-years — fill pairs that never had preferences.
    mfn_keys = [(rep, "000", year, "reported") for rep in unique_reporters for year in years]
    mfn_meta: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        for fut in as_completed({pool.submit(_one, k): k for k in mfn_keys}):
            mfn_meta.append(fut.result())
    meta_rows.extend(mfn_meta)

    mfn_frames: list[pd.DataFrame] = []
    for meta in mfn_meta:
        if meta["status"] != 200:
            continue
        path_m = Path(meta["path"])
        if path_m.stat().st_size < 50:
            continue
        lines = filter_chapters(parse_trn_xml(path_m.read_bytes()), chapters)
        if lines.empty:
            continue
        # Prefer aveestimated when NA lines present
        if (lines["nbr_na_lines"].fillna(0) > 0).any():
            ave_url_key = (meta["reporter"], "000", meta["year"], "aveestimated")
            ave_meta = _one(ave_url_key)
            meta_rows.append(ave_meta)
            if ave_meta["status"] == 200 and Path(ave_meta["path"]).stat().st_size >= 50:
                ave_lines = filter_chapters(
                    parse_trn_xml(Path(ave_meta["path"]).read_bytes()), chapters
                )
                lines = merge_reported_aveestimated(lines, ave_lines)
        mfn_frames.append(lines)

    mfn_lines = pd.concat(mfn_frames, ignore_index=True) if mfn_frames else pd.DataFrame()
    mfn_agg = aggregate_chapter_ahs(mfn_lines)
    # Expand MFN reporter codes to destination ISO3
    mfn_rows: list[dict[str, Any]] = []
    for _, row in mfn_agg.iterrows():
        rep = str(row["reporter"]).zfill(3)
        if rep == "918" or str(int(rep)) == "918":
            dest_list = list(eu_dests)
        else:
            dest_list = [
                d
                for d in non_eu
                if int(wits_reporter_code(d)) == int(rep)
            ]
        for dest in dest_list:
            mfn_rows.append(
                {
                    "reporter_iso3": dest,
                    "year": int(row["year"]),
                    "hs_chapter": str(row["hs_chapter"]).zfill(2),
                    "mfn_simple_avg": float(row["ahs_simple_avg"]),
                }
            )
    mfn_df = pd.DataFrame.from_records(mfn_rows)
    df = apply_mfn_fallback(df, mfn_df)

    path = raw_dir() / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)

    n_locf = (
        int(df["tarif_locf"].fillna(False).astype(bool).sum())
        if "tarif_locf" in df.columns
        else 0
    )
    n_mfn = (
        int((df["tarif_source"] == "mfn_no_preference").sum())
        if "tarif_source" in df.columns
        else 0
    )
    n_cached = sum(1 for m in meta_rows if m.get("cached"))
    record_artifact(
        "wits",
        url=base_url,
        version=version,
        relative_paths=[rel],
        sha256=sha256_file(path),
        extra={
            "n_rows": int(len(df)),
            "n_locf": n_locf,
            "n_mfn_no_preference": n_mfn,
            "n_api_calls": len(meta_rows),
            "n_cached": n_cached,
            "n_destinations": len(resolved_dests),
            "chapters": chapters,
            "columns": list(df.columns),
        },
    )
    return {
        "skipped": False,
        "parquet": str(path),
        "url": base_url,
        "n_rows": len(df),
        "n_locf": n_locf,
        "n_mfn_no_preference": n_mfn,
        "n_api_calls": len(meta_rows),
        "n_cached": n_cached,
    }
