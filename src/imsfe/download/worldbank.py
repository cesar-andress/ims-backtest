"""Fetch World Bank and WGI indicators into data/raw/."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import pandas as pd
import requests
import wbgapi as wb

from imsfe.config import Settings, load_settings
from imsfe.download.http_util import download_file
from imsfe.io import raw_dir, record_artifact, sha256_file, should_skip

WDI_INDICATORS: list[str] = [
    "NY.GDP.PCAP.PP.KD",
    "SP.POP.TOTL",
    "NY.GDP.MKTP.CD",
    "NE.TRD.GNFS.ZS",
    "LP.LPI.OVRL.XQ",
    "FP.CPI.TOTL.ZG",
    "SL.UEM.TOTL.ZS",
]

# SPEC uses short WGI codes; WGI API (source 3) exposes GOV_WGI_*.EST.
WGI_API_TO_SPEC: dict[str, str] = {
    "GOV_WGI_VA.EST": "VA.EST",
    "GOV_WGI_PV.EST": "PV.EST",
    "GOV_WGI_GE.EST": "GE.EST",
    "GOV_WGI_RQ.EST": "RQ.EST",
    "GOV_WGI_RL.EST": "RL.EST",
    "GOV_WGI_CC.EST": "CC.EST",
}

WDI_REL = "worldbank/wdi_indicators.parquet"
WGI_REL = "worldbank/wgi_indicators.parquet"
WDI_CSV_ZIP_REL = "worldbank/WDI_CSV.zip"
# Official bulk dump (verified HTTP 200, ~282 MiB, 2026-11-18).
WDI_CSV_ZIP_URL = (
    "https://databankfiles.worldbank.org/public/ddpext_download/WDI_CSV.zip"
)


def _years(settings: Settings) -> range:
    return range(settings.years.start, settings.years.end + 1)


def _with_retries(fn, *, attempts: int = 4, label: str = "worldbank"):
    """Retry transient World Bank API failures (524/502/timeouts)."""
    last_exc: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            wait = min(20, 2**attempt)
            print(f"{label}: attempt {attempt}/{attempts} failed ({exc}); sleep {wait}s")
            time.sleep(wait)
    assert last_exc is not None
    raise last_exc


def _fetch_long(
    series_ids: list[str],
    years: range,
    *,
    source_id: int,
) -> pd.DataFrame:
    """Fetch a long panel via wbgapi.data.fetch: iso3, year, indicator, value."""
    previous = wb.db
    rows: list[dict[str, Any]] = []
    try:
        wb.db = source_id

        def _one(sid: str) -> list[dict[str, Any]]:
            meta = wb.series.get(sid)
            if not meta:
                raise RuntimeError(f"World Bank source {source_id} missing series {sid}")
            local: list[dict[str, Any]] = []
            for obs in wb.data.fetch(sid, "all", time=years, skipBlanks=True):
                economy = obs.get("economy")
                time_key = obs.get("time")
                value = obs.get("value")
                if economy is None or time_key is None or value is None:
                    continue
                year_s = str(time_key).replace("YR", "")
                try:
                    year = int(year_s)
                except ValueError:
                    continue
                local.append(
                    {
                        "iso3": str(economy),
                        "year": year,
                        "indicator": sid,
                        "value": float(value),
                    }
                )
            if not local:
                raise RuntimeError(
                    f"World Bank source {source_id} returned no data for {sid}"
                )
            return local

        for sid in series_ids:
            rows.extend(_with_retries(lambda s=sid: _one(s), label=f"worldbank:{sid}"))
    finally:
        wb.db = previous
    return pd.DataFrame.from_records(rows)


def _fetch_wdi_rest(series_ids: list[str], years: range) -> pd.DataFrame:
    """Fallback WDI/WGI fetch via API v2, one calendar year at a time.

    Bulk multi-year ``country/all`` queries frequently return HTTP 502 from the
    World Bank API; per-year requests with a modest page size are stable.
    """
    rows: list[dict[str, Any]] = []
    session = requests.Session()
    session.trust_env = False  # avoid stuck proxy autodetection in some environments
    for sid in series_ids:
        n_before = len(rows)
        for year in years:
            page = 1
            while True:
                url = (
                    "https://api.worldbank.org/v2/country/all/indicator/"
                    f"{sid}?date={year}:{year}&format=json&per_page=500&page={page}"
                )

                def _get(u=url):
                    resp = session.get(u, timeout=45)
                    if resp.status_code != 200:
                        raise RuntimeError(f"WDI REST HTTP {resp.status_code} for {u}")
                    ctype = resp.headers.get("content-type", "")
                    if "json" not in ctype and not resp.text.lstrip().startswith("["):
                        raise RuntimeError(
                            f"WDI REST non-JSON response for {u} "
                            f"(content-type={ctype!r})"
                        )
                    return resp.json()

                try:
                    payload = _with_retries(
                        _get, attempts=3, label=f"wdi-rest:{sid}:{year}:p{page}"
                    )
                except Exception as exc:  # noqa: BLE001
                    print(f"wdi-rest: skip {sid} {year} page {page} ({exc})")
                    break
                if not isinstance(payload, list) or len(payload) < 2:
                    raise RuntimeError(f"Unexpected WDI payload for {sid}: {payload!r}")
                meta, data = payload[0], payload[1]
                if not data:
                    break
                for obs in data:
                    iso3 = obs.get("countryiso3code") or ""
                    if not iso3 or iso3.strip() == "":
                        continue
                    if obs.get("value") is None:
                        continue
                    rows.append(
                        {
                            "iso3": str(iso3),
                            "year": int(obs["date"]),
                            "indicator": sid,
                            "value": float(obs["value"]),
                        }
                    )
                pages = int(meta.get("pages") or 1)
                if page >= pages:
                    break
                page += 1
        if len(rows) == n_before:
            raise RuntimeError(f"WDI REST returned no data for {sid}")
    return pd.DataFrame.from_records(rows)


def _fetch_wdi_bulk_csv(years: range) -> tuple[pd.DataFrame, str]:
    """Download the official WDI_CSV.zip and filter to required indicators."""
    import zipfile

    zip_path = raw_dir() / WDI_CSV_ZIP_REL
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    download_file(WDI_CSV_ZIP_URL, zip_path, timeout=600)
    with zipfile.ZipFile(zip_path) as zf:
        # File name varies slightly across releases; prefer *Data.csv.
        members = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        data_members = [n for n in members if "data" in Path(n).name.lower()]
        if not data_members:
            raise RuntimeError(f"No *Data.csv in WDI zip; members={members[:10]}")
        member = sorted(data_members, key=lambda n: zf.getinfo(n).file_size)[-1]
        with zf.open(member) as fh:
            wide = pd.read_csv(fh, low_memory=False)
    code_col = "Indicator Code" if "Indicator Code" in wide.columns else "IndicatorCode"
    iso_col = "Country Code" if "Country Code" in wide.columns else "CountryCode"
    if code_col not in wide.columns or iso_col not in wide.columns:
        raise RuntimeError(f"Unexpected WDI CSV columns: {list(wide.columns)[:20]}")
    subset = wide.loc[wide[code_col].isin(WDI_INDICATORS)].copy()
    year_cols = [c for c in subset.columns if str(c).isdigit()]
    year_cols = [c for c in year_cols if years.start <= int(c) <= years.stop - 1]
    if not year_cols:
        raise RuntimeError("WDI CSV has no year columns in the requested range")
    long = subset.melt(
        id_vars=[iso_col, code_col],
        value_vars=year_cols,
        var_name="year",
        value_name="value",
    )
    long = long.rename(columns={iso_col: "iso3", code_col: "indicator"})
    long["year"] = long["year"].astype(int)
    long["value"] = pd.to_numeric(long["value"], errors="coerce")
    long = long.dropna(subset=["value"])
    long = long[["iso3", "year", "indicator", "value"]]
    if long.empty:
        raise RuntimeError("WDI bulk CSV produced no rows after filtering")
    return long, WDI_CSV_ZIP_URL


def fetch_wdi(settings: Settings | None = None, *, force: bool = False) -> Path:
    """Download WDI indicators to a long parquet."""
    settings = settings or load_settings()
    rel = WDI_REL
    version = f"wdi-{settings.worldbank.wdi_source_id}-{settings.years.start}-{settings.years.end}"
    if should_skip("worldbank_wdi", version, [rel], force=force):
        return raw_dir() / rel

    source_url = WDI_CSV_ZIP_URL
    try:
        df, source_url = _fetch_wdi_bulk_csv(_years(settings))
        record_artifact(
            "worldbank_wdi_zip",
            url=WDI_CSV_ZIP_URL,
            version=version,
            relative_paths=[WDI_CSV_ZIP_REL],
            sha256=sha256_file(raw_dir() / WDI_CSV_ZIP_REL),
        )
    except Exception as exc:  # noqa: BLE001
        print(f"worldbank WDI bulk CSV failed ({exc}); trying REST then wbgapi")
        try:
            df = _fetch_wdi_rest(WDI_INDICATORS, _years(settings))
            source_url = "https://api.worldbank.org/v2 (REST per-year)"
        except Exception as exc2:  # noqa: BLE001
            print(f"worldbank WDI REST failed ({exc2}); falling back to wbgapi")
            df = _fetch_long(
                WDI_INDICATORS,
                _years(settings),
                source_id=settings.worldbank.wdi_source_id,
            )
            source_url = "https://api.worldbank.org/v2 (wbgapi WDI)"

    path = raw_dir() / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
    record_artifact(
        "worldbank_wdi",
        url=source_url,
        version=version,
        relative_paths=[rel],
        sha256=sha256_file(path),
        extra={"n_rows": int(len(df)), "indicators": WDI_INDICATORS},
    )
    return path


def fetch_wgi(settings: Settings | None = None, *, force: bool = False) -> Path:
    """Download WGI estimate series and store under SPEC short codes."""
    settings = settings or load_settings()
    rel = WGI_REL
    version = f"wgi-{settings.worldbank.wgi_source_id}-{settings.years.start}-{settings.years.end}"
    if should_skip("worldbank_wgi", version, [rel], force=force):
        return raw_dir() / rel

    api_ids = list(WGI_API_TO_SPEC.keys())
    def _assert_wgi() -> None:
        previous = wb.db
        try:
            wb.db = settings.worldbank.wgi_source_id
            available = {row["id"] for row in wb.series.list()}
            missing = [s for s in api_ids if s not in available]
            if missing:
                raise RuntimeError(
                    f"WGI source {settings.worldbank.wgi_source_id} missing series: {missing}"
                )
            probe = list(
                wb.data.fetch(api_ids[0], ["USA", "COL"], time=2020, skipBlanks=True)
            )
            if not probe:
                raise RuntimeError(
                    f"WGI source {settings.worldbank.wgi_source_id} asserted but returned "
                    f"no probe data for {api_ids[0]}"
                )
        finally:
            wb.db = previous

    # Assert source metadata when the API is up; still allow REST fallback.
    try:
        _with_retries(_assert_wgi, attempts=3, label="wgi-assert")
    except Exception as exc:  # noqa: BLE001
        print(f"worldbank WGI assert skipped ({exc})")
    try:
        df = _fetch_wdi_rest(api_ids, _years(settings))
    except Exception as exc:  # noqa: BLE001
        print(f"worldbank WGI REST failed ({exc}); falling back to wbgapi")
        df = _fetch_long(
            api_ids, _years(settings), source_id=settings.worldbank.wgi_source_id
        )
    df["indicator"] = df["indicator"].map(lambda x: WGI_API_TO_SPEC.get(x, x))
    path = raw_dir() / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
    record_artifact(
        "worldbank_wgi",
        url="https://api.worldbank.org/v2 (wbgapi WGI source 3)",
        version=version,
        relative_paths=[rel],
        sha256=sha256_file(path),
        extra={
            "n_rows": int(len(df)),
            "api_indicators": api_ids,
            "stored_indicators": sorted(WGI_API_TO_SPEC.values()),
            "wgi_source_id": settings.worldbank.wgi_source_id,
        },
    )
    return path


def fetch_worldbank(settings: Settings | None = None, *, force: bool = False) -> dict[str, Any]:
    """Fetch WDI and WGI. Returns paths and any per-source errors."""
    settings = settings or load_settings()
    result: dict[str, Any] = {"paths": {}, "errors": {}}
    try:
        result["paths"]["wdi"] = str(fetch_wdi(settings, force=force))
    except Exception as exc:  # noqa: BLE001 — collect and continue
        result["errors"]["wdi"] = str(exc)
    try:
        result["paths"]["wgi"] = str(fetch_wgi(settings, force=force))
    except Exception as exc:  # noqa: BLE001
        result["errors"]["wgi"] = str(exc)
    return result
