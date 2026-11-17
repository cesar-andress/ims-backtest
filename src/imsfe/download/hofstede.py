"""Load manually provided Hofstede cultural-dimension scores."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from imsfe.io import manual_dir, raw_dir, record_artifact, sha256_file, should_skip

HOFSTEDE_PARQUET_REL = "hofstede/hofstede.parquet"
REQUIRED_DIMS = ["pdi", "idv", "mas", "uai", "ltowvs", "ivr"]


def _candidate_csvs() -> list[Path]:
    folder = manual_dir() / "hofstede"
    return sorted(folder.glob("*.csv"))


def load_hofstede_csv(path: Path | None = None) -> pd.DataFrame:
    """Load Hofstede 6-dimension CSV. No download; manual file required."""
    if path is None:
        candidates = _candidate_csvs()
        if not candidates:
            raise FileNotFoundError(
                f"No Hofstede CSV in {manual_dir() / 'hofstede'}/. "
                "See data/manual/hofstede/README.md."
            )
        path = candidates[0]
    df = pd.read_csv(path)
    cols = {c.lower().strip(): c for c in df.columns}
    if "iso3" not in cols and "ctr" in cols:
        # geerthofstede.com often uses `ctr` for country abbreviation.
        df = df.rename(columns={cols["ctr"]: "iso3"})
        cols = {c.lower().strip(): c for c in df.columns}
    if "iso3" not in cols:
        raise ValueError(
            f"{path.name} must contain an iso3 (or ctr) column; got {list(df.columns)}"
        )
    rename = {cols["iso3"]: "iso3"}
    for dim in REQUIRED_DIMS:
        if dim not in cols:
            raise ValueError(
                f"{path.name} missing Hofstede dimension {dim!r}; got {list(df.columns)}"
            )
        rename[cols[dim]] = dim
    out = df.rename(columns=rename)[["iso3", *REQUIRED_DIMS]].copy()
    out["iso3"] = out["iso3"].astype(str).str.upper().str.strip()
    for dim in REQUIRED_DIMS:
        out[dim] = pd.to_numeric(out[dim], errors="coerce")
    # Do not impute; keep NaNs as missing.
    return out


def fetch_hofstede(*, force: bool = False) -> dict[str, Any]:
    """Copy/normalize the manual Hofstede CSV into data/raw/."""
    version = "manual"
    rel = HOFSTEDE_PARQUET_REL
    if should_skip("hofstede", version, [rel], force=force):
        return {"skipped": True, "parquet": str(raw_dir() / rel)}

    candidates = _candidate_csvs()
    if not candidates:
        raise FileNotFoundError(
            "Hofstede has no automatic download. Place a 6-dimension CSV in "
            f"{manual_dir() / 'hofstede'}/ (see README there)."
        )
    src = candidates[0]
    df = load_hofstede_csv(src)
    path = raw_dir() / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
    record_artifact(
        "hofstede",
        url=f"manual:{src.name}",
        version=version,
        relative_paths=[rel],
        sha256=sha256_file(path),
        extra={"n_rows": int(len(df)), "source_file": src.name},
    )
    return {"skipped": False, "parquet": str(path), "source_file": str(src)}
