"""Load applied preferential tariffs from WITS/TRAINS or manual CSV exports."""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

import pandas as pd
import requests

from imsfe.config import Settings, load_settings
from imsfe.io import manual_dir, raw_dir, record_artifact, sha256_file, should_skip

WITS_PARQUET_REL = "wits/ahs_tariffs.parquet"


def _manual_csv_paths() -> list[Path]:
    folder = manual_dir() / "wits"
    return sorted(folder.glob("*.csv"))


def load_manual_wits_csvs(paths: list[Path] | None = None) -> pd.DataFrame:
    """Load human WITS exports. Required columns documented in data/manual/README.md."""
    files = paths if paths is not None else _manual_csv_paths()
    if not files:
        raise FileNotFoundError(
            f"No WITS CSV exports in {manual_dir() / 'wits'}/. "
            "See data/manual/wits/README.md for export settings."
        )
    frames: list[pd.DataFrame] = []
    required = {"reporter_iso3", "partner_iso3", "year", "hs_chapter", "ahs_simple_avg"}
    for path in files:
        df = pd.read_csv(path)
        cols = {c.lower(): c for c in df.columns}
        # Accept a few aliases.
        rename = {}
        aliases = {
            "reporter_iso3": ["reporter_iso3", "reporter", "reportercode"],
            "partner_iso3": ["partner_iso3", "partner", "partnercode"],
            "year": ["year", "period", "time"],
            "hs_chapter": ["hs_chapter", "chapter", "productcode", "product"],
            "ahs_simple_avg": [
                "ahs_simple_avg",
                "ahs",
                "dutyvalue",
                "simpleaverage",
                "value",
            ],
        }
        # Stricter mapping for documented schema.
        lower_set = set(cols)
        if not required.issubset(lower_set):
            # try alias map
            mapped: dict[str, str] = {}
            for canon, alist in aliases.items():
                for a in alist:
                    if a in cols:
                        mapped[canon] = cols[a]
                        break
            if set(mapped) >= required:
                rename = {mapped[k]: k for k in required}
                df = df.rename(columns=rename)
            else:
                raise ValueError(
                    f"{path.name} must contain columns {sorted(required)} "
                    f"(or documented aliases); got {list(df.columns)}"
                )
        else:
            df = df.rename(columns={cols[c]: c for c in required})
        frames.append(df[list(required)].copy())
    out = pd.concat(frames, ignore_index=True)
    out["year"] = pd.to_numeric(out["year"], errors="coerce").astype("Int64")
    out["ahs_simple_avg"] = pd.to_numeric(out["ahs_simple_avg"], errors="coerce")
    out["hs_chapter"] = out["hs_chapter"].astype(str).str.zfill(2)
    out = out.dropna(subset=["year", "ahs_simple_avg"])
    out["year"] = out["year"].astype(int)
    return out


def _parse_sdmx_obs_values(xml_text: str) -> list[dict[str, Any]]:
    """Parse WITS SDMX-ML GenericData observations into dict rows."""
    # Namespaces vary; match by localname.
    root = ET.fromstring(xml_text)
    rows: list[dict[str, Any]] = []

    def local(tag: str) -> str:
        return tag.rsplit("}", 1)[-1]

    for obs in root.iter():
        if local(obs.tag) != "Obs":
            continue
        dims: dict[str, str] = {}
        value = None
        for child in list(obs):
            lname = local(child.tag)
            if lname == "ObsKey":
                for value_el in child:
                    if local(value_el.tag) == "Value":
                        dims[value_el.attrib.get("id", "")] = value_el.attrib.get(
                            "value", ""
                        )
            elif lname == "ObsValue":
                value = child.attrib.get("value")
            elif lname == "Value" and "id" in child.attrib:
                dims[child.attrib["id"]] = child.attrib.get("value", "")
        if value is None:
            continue
        try:
            num = float(value)
        except ValueError:
            continue
        rows.append({"dims": dims, "value": num})
    return rows


def try_wits_api_probe(settings: Settings, session: requests.Session | None = None) -> pd.DataFrame:
    """Probe the WITS SDMX API for origin partners (product from settings).

    Chapter-level HS keys are not reliably exposed; this probe uses the configured
    product (default Total) for each origin against a small reporter set to verify
    connectivity. Full HS-chapter series must come from manual CSVs.
    """
    sess = session or requests.Session()
    reporters = ["USA", "DEU", "CHN"]
    rows: list[dict[str, Any]] = []
    base = settings.wits.base_url.rstrip("/")
    indicator = settings.wits.indicator
    product = settings.wits.product
    for partner in settings.origins:
        for reporter in reporters:
            key = f"A.{reporter}.{partner}.{product}.{indicator}"
            url = (
                f"{base}/{key}"
                f"?startPeriod={settings.years.start}&endPeriod={settings.years.end}"
            )
            resp = sess.get(url, timeout=60)
            if resp.status_code != 200:
                continue
            if "Invalid" in resp.text or "error" in resp.text.lower()[:200]:
                continue
            for obs in _parse_sdmx_obs_values(resp.text):
                year = obs["dims"].get("TIME_PERIOD") or obs["dims"].get("TIME")
                if year is None:
                    continue
                if not re.fullmatch(r"\d{4}", str(year)):
                    continue
                rows.append(
                    {
                        "reporter_iso3": reporter,
                        "partner_iso3": partner,
                        "year": int(year),
                        "hs_chapter": "ALL",
                        "ahs_simple_avg": obs["value"],
                        "product_code": product,
                        "source": "wits_api_probe",
                    }
                )
    if not rows:
        raise RuntimeError(
            "WITS API probe returned no observations; use manual CSV exports "
            f"in {manual_dir() / 'wits'}/"
        )
    return pd.DataFrame.from_records(rows)


def fetch_wits(settings: Settings | None = None, *, force: bool = False) -> dict[str, Any]:
    """Prefer manual HS-chapter CSVs; fall back to a limited WITS API probe."""
    settings = settings or load_settings()
    version = settings.wits.version
    rel = WITS_PARQUET_REL
    if should_skip("wits", version, [rel], force=force):
        return {"skipped": True, "parquet": str(raw_dir() / rel)}

    source_note = ""
    try:
        df = load_manual_wits_csvs()
        source_note = "manual:data/manual/wits"
    except FileNotFoundError:
        try:
            df = try_wits_api_probe(settings)
            source_note = settings.wits.base_url
            # API probe is not chapter-complete — do not pretend it is.
            print(
                "WITS: no manual CSVs found; stored API probe rows with hs_chapter=ALL. "
                "For HS-chapter AHS averages required by SPEC, export CSVs into "
                "data/manual/wits/ (see README)."
            )
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(
                "WITS unavailable via API and no manual CSVs present. "
                f"Place exports in data/manual/wits/. Detail: {exc}"
            ) from exc

    path = raw_dir() / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
    record_artifact(
        "wits",
        url=source_note,
        version=version,
        relative_paths=[rel],
        sha256=sha256_file(path),
        extra={"n_rows": int(len(df)), "columns": list(df.columns)},
    )
    return {"skipped": False, "parquet": str(path), "url": source_note, "n_rows": len(df)}
