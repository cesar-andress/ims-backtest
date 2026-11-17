"""Fetch World Bank and WGI indicators into data/raw/."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import wbgapi as wb

from imsfe.config import Settings, load_settings
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


def _years(settings: Settings) -> range:
    return range(settings.years.start, settings.years.end + 1)


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
        for sid in series_ids:
            meta = wb.series.get(sid)
            if not meta:
                raise RuntimeError(f"World Bank source {source_id} missing series {sid}")
            n_before = len(rows)
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
                rows.append(
                    {
                        "iso3": str(economy),
                        "year": year,
                        "indicator": sid,
                        "value": float(value),
                    }
                )
            if len(rows) == n_before:
                raise RuntimeError(
                    f"World Bank source {source_id} returned no data for {sid}"
                )
    finally:
        wb.db = previous
    return pd.DataFrame.from_records(rows)


def fetch_wdi(settings: Settings | None = None, *, force: bool = False) -> Path:
    """Download WDI indicators to a long parquet."""
    settings = settings or load_settings()
    rel = WDI_REL
    version = f"wdi-{settings.worldbank.wdi_source_id}-{settings.years.start}-{settings.years.end}"
    if should_skip("worldbank_wdi", version, [rel], force=force):
        return raw_dir() / rel

    df = _fetch_long(
        WDI_INDICATORS,
        _years(settings),
        source_id=settings.worldbank.wdi_source_id,
    )
    path = raw_dir() / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
    record_artifact(
        "worldbank_wdi",
        url="https://api.worldbank.org/v2 (wbgapi WDI)",
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
    previous = wb.db
    try:
        wb.db = settings.worldbank.wgi_source_id
        available = {row["id"] for row in wb.series.list()}
        missing = [s for s in api_ids if s not in available]
        if missing:
            raise RuntimeError(
                f"WGI source {settings.worldbank.wgi_source_id} missing series: {missing}"
            )
        # Sanity: at least one non-empty observation for the first series.
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

    df = _fetch_long(api_ids, _years(settings), source_id=settings.worldbank.wgi_source_id)
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
