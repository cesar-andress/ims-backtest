"""Fetch and convert CEPII BACI trade data for configured HS chapters."""

from __future__ import annotations

import io
import zipfile
from pathlib import Path
from typing import Any

import pandas as pd

from imsfe.config import Settings, load_settings
from imsfe.download.http_util import download_file
from imsfe.io import manual_dir, raw_dir, record_artifact, sha256_file, should_skip

BACI_ZIP_REL = "baci/baci_download.zip"
BACI_PARQUET_DIR_REL = "baci/trade_by_year"
COUNTRY_REL = "baci/country_codes.parquet"
PRODUCT_REL = "baci/product_codes.parquet"


def _manual_zip_candidates(settings: Settings) -> list[Path]:
    manual = manual_dir() / "baci"
    names = []
    if settings.baci.version and settings.baci.nomenclature:
        names.append(
            f"BACI_{settings.baci.nomenclature}_V{settings.baci.version}.zip"
        )
    names.extend(["baci.zip", "BACI.zip"])
    return [manual / n for n in names] + sorted(manual.glob("BACI_*.zip"))


def resolve_baci_zip(settings: Settings, *, force: bool = False) -> tuple[Path, str, str]:
    """Return (zip_path, url_or_note, version). Downloads or uses manual fallback."""
    version = settings.baci.version or "unknown"
    rel = BACI_ZIP_REL
    dest = raw_dir() / rel
    url = settings.baci.url or ""

    if should_skip("baci_zip", version, [rel], force=force) and dest.is_file():
        return dest, url or "manifest", version

    if url:
        try:
            download_file(url, dest)
            return dest, url, version
        except Exception as exc:  # noqa: BLE001
            print(
                f"BACI download failed ({exc}).\n"
                "Manual fallback: download the BACI zip from CEPII and place it in "
                f"{manual_dir() / 'baci'}/ "
                f"(expected name BACI_{settings.baci.nomenclature}_V{version}.zip)."
            )

    for candidate in _manual_zip_candidates(settings):
        if candidate.is_file():
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(candidate.read_bytes())
            return dest, f"manual:{candidate.name}", version

    raise FileNotFoundError(
        "BACI zip not available. Set baci.url in config/settings.yaml to a working "
        "CEPII URL, or place the zip under data/manual/baci/ "
        f"(see {manual_dir() / 'baci' / 'README.md'})."
    )


def _read_member_csv(zf: zipfile.ZipFile, name: str, **kwargs: Any) -> pd.DataFrame:
    with zf.open(name) as fh:
        return pd.read_csv(fh, dtype=str, **kwargs)


def _find_member(names: list[str], prefix: str) -> str:
    matches = [n for n in names if Path(n).name.lower().startswith(prefix.lower())]
    if not matches:
        raise FileNotFoundError(f"No zip member starting with {prefix!r}")
    return sorted(matches)[0]


def convert_baci_zip(
    zip_path: Path,
    settings: Settings,
) -> dict[str, Path]:
    """Filter BACI zip to configured HS chapters; write parquet partitioned by year."""
    chapters = settings.hs_chapter_codes()
    year_min, year_max = settings.years.start, settings.years.end
    out_dir = raw_dir() / BACI_PARQUET_DIR_REL
    if out_dir.exists():
        for old in out_dir.glob("year=*"):
            for f in old.glob("*.parquet"):
                f.unlink()
            old.rmdir()
    out_dir.mkdir(parents=True, exist_ok=True)

    country_path = raw_dir() / COUNTRY_REL
    product_path = raw_dir() / PRODUCT_REL
    country_path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        country_member = _find_member(names, "country_codes")
        product_member = _find_member(names, "product_codes")
        countries = _read_member_csv(zf, country_member)
        products = _read_member_csv(zf, product_member)
        countries.to_parquet(country_path, index=False)
        products.to_parquet(product_path, index=False)

        trade_members = [
            n
            for n in names
            if Path(n).name.upper().startswith("BACI_") and n.lower().endswith(".csv")
        ]
        if not trade_members:
            raise RuntimeError("No BACI trade CSV members found in zip")

        written: list[Path] = []
        for member in sorted(trade_members):
            # Filenames like BACI_HS12_Y2017_V202601.csv
            year = None
            for part in Path(member).stem.split("_"):
                if part.startswith("Y") and part[1:].isdigit():
                    year = int(part[1:])
                    break
            if year is None:
                continue
            if year < year_min or year > year_max:
                continue

            chunks: list[pd.DataFrame] = []
            with zf.open(member) as fh:
                # Read in chunks; keep product codes as strings.
                text = io.TextIOWrapper(fh, encoding="utf-8")
                reader = pd.read_csv(
                    text,
                    dtype={"k": str, "i": str, "j": str},
                    chunksize=500_000,
                )
                for chunk in reader:
                    chunk["k"] = chunk["k"].astype(str).str.zfill(6)
                    mask = chunk["k"].str[:2].isin(chapters)
                    filtered = chunk.loc[mask].copy()
                    if filtered.empty:
                        continue
                    filtered["t"] = filtered["t"].astype(int)
                    filtered["v"] = pd.to_numeric(filtered["v"], errors="coerce")
                    filtered["q"] = pd.to_numeric(filtered["q"], errors="coerce")
                    chunks.append(filtered)
            if not chunks:
                continue
            year_df = pd.concat(chunks, ignore_index=True)
            part_dir = out_dir / f"year={year}"
            part_dir.mkdir(parents=True, exist_ok=True)
            part_path = part_dir / "part.parquet"
            year_df.to_parquet(part_path, index=False)
            written.append(part_path)

    if not written:
        raise RuntimeError(
            "BACI conversion produced no rows for the configured years/chapters"
        )
    return {
        "trade_dir": out_dir,
        "countries": country_path,
        "products": product_path,
    }


def fetch_baci(settings: Settings | None = None, *, force: bool = False) -> dict[str, Any]:
    """Download (or load manual) BACI and convert to parquet."""
    settings = settings or load_settings()
    version = settings.baci.version or "unknown"
    paths = [BACI_ZIP_REL, COUNTRY_REL, PRODUCT_REL, BACI_PARQUET_DIR_REL]
    if should_skip("baci", version, paths, force=force):
        return {
            "skipped": True,
            "zip": str(raw_dir() / BACI_ZIP_REL),
            "trade_dir": str(raw_dir() / BACI_PARQUET_DIR_REL),
        }

    zip_path, url_note, version = resolve_baci_zip(settings, force=force)
    record_artifact(
        "baci_zip",
        url=url_note,
        version=version,
        relative_paths=[BACI_ZIP_REL],
        sha256=sha256_file(zip_path),
    )
    converted = convert_baci_zip(zip_path, settings)
    # Hash the country file as a stable fingerprint of the converted release.
    record_artifact(
        "baci",
        url=url_note,
        version=version,
        relative_paths=paths,
        sha256=sha256_file(converted["countries"]),
        extra={
            "nomenclature": settings.baci.nomenclature,
            "chapters": settings.hs_chapter_codes(),
            "years": [settings.years.start, settings.years.end],
        },
    )
    return {
        "skipped": False,
        "zip": str(zip_path),
        "url": url_note,
        "trade_dir": str(converted["trade_dir"]),
        "countries": str(converted["countries"]),
        "products": str(converted["products"]),
    }
