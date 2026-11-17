"""Fetch CEPII Gravity bilateral covariates (distance, FTA, language)."""

from __future__ import annotations

import zipfile
from pathlib import Path
from typing import Any

import pandas as pd

from imsfe.config import Settings, load_settings
from imsfe.download.http_util import download_file
from imsfe.io import manual_dir, raw_dir, record_artifact, sha256_file, should_skip

GRAVITY_ZIP_REL = "cepii_gravity/gravity_download.zip"
GRAVITY_PARQUET_REL = "cepii_gravity/gravity.parquet"

KEEP_CANDIDATES = {
    "iso3_o": ["iso3_o", "iso3o", "iso_o"],
    "iso3_d": ["iso3_d", "iso3d", "iso_d"],
    "year": ["year", "year_id"],
    "distw_harmonic": ["distw_harmonic", "distw_harm"],
    "distw": ["distw", "distw_pop"],
    "contig": ["contig"],
    "comlang_off": ["comlang_off", "comlang"],
    "fta_wto": ["fta_wto", "fta"],
}


def _manual_candidates(settings: Settings) -> list[Path]:
    manual = manual_dir() / "cepii_gravity"
    names = []
    if settings.cepii_gravity.version:
        names.append(f"Gravity_csv_V{settings.cepii_gravity.version}.zip")
        names.append(f"Gravity_V{settings.cepii_gravity.version}.csv")
    names.extend(["gravity.zip", "Gravity.csv"])
    return [manual / n for n in names] + sorted(manual.glob("Gravity*"))


def resolve_gravity_archive(
    settings: Settings, *, force: bool = False
) -> tuple[Path, str, str]:
    """Return (archive_or_csv path, url_note, version)."""
    version = settings.cepii_gravity.version or "unknown"
    rel = GRAVITY_ZIP_REL
    dest = raw_dir() / rel
    url = settings.cepii_gravity.url or ""

    if should_skip("cepii_gravity_zip", version, [rel], force=force) and dest.is_file():
        return dest, url or "manifest", version

    if url:
        try:
            download_file(url, dest)
            return dest, url, version
        except Exception as exc:  # noqa: BLE001
            print(
                f"CEPII Gravity download failed ({exc}).\n"
                "Manual fallback: download Gravity CSV zip from CEPII and place it in "
                f"{manual_dir() / 'cepii_gravity'}/."
            )

    for candidate in _manual_candidates(settings):
        if candidate.is_file():
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(candidate.read_bytes())
            return dest, f"manual:{candidate.name}", version

    raise FileNotFoundError(
        "CEPII Gravity file not available. Set cepii_gravity.url in "
        "config/settings.yaml, or place the CSV zip under data/manual/cepii_gravity/ "
        f"(see {manual_dir() / 'cepii_gravity' / 'README.md'})."
    )


def _pick_column(columns: list[str], aliases: list[str]) -> str | None:
    lower = {c.lower(): c for c in columns}
    for alias in aliases:
        if alias.lower() in lower:
            return lower[alias.lower()]
    return None


def _load_gravity_frame(archive: Path) -> pd.DataFrame:
    if archive.suffix.lower() == ".csv":
        return pd.read_csv(archive, low_memory=False)
    with zipfile.ZipFile(archive) as zf:
        csv_members = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        if not csv_members:
            raise RuntimeError(f"No CSV inside Gravity archive: {archive}")
        # Prefer the largest CSV (main table).
        member = max(csv_members, key=lambda n: zf.getinfo(n).file_size)
        with zf.open(member) as fh:
            return pd.read_csv(fh, low_memory=False)


def convert_gravity(archive: Path, settings: Settings) -> Path:
    """Keep required bilateral columns and filter to settings years."""
    raw = _load_gravity_frame(archive)
    mapping: dict[str, str] = {}
    for canonical, aliases in KEEP_CANDIDATES.items():
        found = _pick_column(list(raw.columns), aliases)
        if found:
            mapping[canonical] = found

    required = ["iso3_o", "iso3_d", "year"]
    missing_req = [c for c in required if c not in mapping]
    if missing_req:
        raise RuntimeError(
            f"Gravity file missing required columns {missing_req}; "
            f"available={list(raw.columns)[:30]}"
        )
    if "distw_harmonic" not in mapping and "distw" not in mapping:
        raise RuntimeError(
            "Gravity file has neither distw_harmonic nor distw; "
            f"available={list(raw.columns)[:30]}"
        )

    out = pd.DataFrame()
    for canonical, source_col in mapping.items():
        out[canonical] = raw[source_col]
    out["year"] = pd.to_numeric(out["year"], errors="coerce").astype("Int64")
    out = out.dropna(subset=["year"])
    out["year"] = out["year"].astype(int)
    out = out.loc[
        (out["year"] >= settings.years.start) & (out["year"] <= settings.years.end)
    ].copy()

    # Prefer harmonic distance when present; always keep distw if available.
    path = raw_dir() / GRAVITY_PARQUET_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    out.to_parquet(path, index=False)
    return path


def fetch_cepii_gravity(
    settings: Settings | None = None, *, force: bool = False
) -> dict[str, Any]:
    """Download/convert CEPII Gravity."""
    settings = settings or load_settings()
    version = settings.cepii_gravity.version or "unknown"
    paths = [GRAVITY_ZIP_REL, GRAVITY_PARQUET_REL]
    if should_skip("cepii_gravity", version, paths, force=force):
        return {
            "skipped": True,
            "parquet": str(raw_dir() / GRAVITY_PARQUET_REL),
        }

    archive, url_note, version = resolve_gravity_archive(settings, force=force)
    record_artifact(
        "cepii_gravity_zip",
        url=url_note,
        version=version,
        relative_paths=[GRAVITY_ZIP_REL],
        sha256=sha256_file(archive),
    )
    parquet = convert_gravity(archive, settings)
    record_artifact(
        "cepii_gravity",
        url=url_note,
        version=version,
        relative_paths=paths,
        sha256=sha256_file(parquet),
        extra={"n_rows": int(pd.read_parquet(parquet).shape[0])},
    )
    return {"skipped": False, "url": url_note, "parquet": str(parquet)}
