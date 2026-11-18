"""Load manually provided Hofstede cultural-dimension scores."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from imsfe.io import manual_dir, raw_dir, record_artifact, sha256_file, should_skip

HOFSTEDE_PARQUET_REL = "hofstede/hofstede.parquet"
REQUIRED_DIMS = ["pdi", "idv", "mas", "uai", "ltowvs", "ivr"]

# Official geerthofstede.com ``ctr`` codes → ISO 3166-1 alpha-3.
# Regional aggregates (AFE, AFW, ARA, …) are omitted (no single ISO3).
HOFSTEDE_CTR_TO_ISO3: dict[str, str] = {
    "ALB": "ALB",
    "ALG": "DZA",
    "AND": "AND",
    "ARG": "ARG",
    "ARM": "ARM",
    "AUL": "AUS",
    "AUT": "AUT",
    "AZE": "AZE",
    "BAN": "BGD",
    "BLR": "BLR",
    "BEL": "BEL",
    "BEF": "BEL",
    "BEN": "BEL",
    "BOS": "BIH",
    "BRA": "BRA",
    "BUL": "BGR",
    "BUF": "BFA",
    "CAN": "CAN",
    "CAF": "CAN",
    "CHL": "CHL",
    "CHI": "CHN",
    "COL": "COL",
    "COS": "CRI",
    "CRO": "HRV",
    "CYP": "CYP",
    "CZE": "CZE",
    "DEN": "DNK",
    "DOM": "DOM",
    "ECA": "ECU",
    "EGY": "EGY",
    "ETH": "ETH",
    "SAL": "SLV",
    "EST": "EST",
    "FIN": "FIN",
    "FRA": "FRA",
    "GEO": "GEO",
    "GER": "DEU",
    "GEE": "DEU",
    "GHA": "GHA",
    "GBR": "GBR",
    "GRE": "GRC",
    "GUA": "GTM",
    "HOK": "HKG",
    "HUN": "HUN",
    "ICE": "ISL",
    "IND": "IND",
    "IDO": "IDN",
    "IRA": "IRN",
    "IRQ": "IRQ",
    "IRE": "IRL",
    "ISR": "ISR",
    "ITA": "ITA",
    "JAM": "JAM",
    "JPN": "JPN",
    "JOR": "JOR",
    "KOR": "KOR",
    "KYR": "KGZ",
    "LAT": "LVA",
    "LIT": "LTU",
    "LUX": "LUX",
    "MAC": "MKD",
    "MAL": "MYS",
    "MLI": "MLI",
    "MLT": "MLT",
    "MEX": "MEX",
    "MOL": "MDA",
    "MNG": "MNE",
    "MOR": "MAR",
    "NET": "NLD",
    "NZL": "NZL",
    "NIG": "NGA",
    "NOR": "NOR",
    "PAK": "PAK",
    "PAN": "PAN",
    "PER": "PER",
    "PHI": "PHL",
    "POL": "POL",
    "POR": "PRT",
    "PUE": "PRI",
    "ROM": "ROU",
    "RUS": "RUS",
    "RWA": "RWA",
    "SAU": "SAU",
    "SER": "SRB",
    "SIN": "SGP",
    "SLK": "SVK",
    "SLV": "SVN",
    "SAF": "ZAF",
    "SAW": "ZAF",
    "SPA": "ESP",
    "SUR": "SUR",
    "SWE": "SWE",
    "SWI": "CHE",
    "SWF": "CHE",
    "SWG": "CHE",
    "TAI": "TWN",
    "TAN": "TZA",
    "THA": "THA",
    "TRI": "TTO",
    "TUR": "TUR",
    "USA": "USA",
    "UGA": "UGA",
    "UKR": "UKR",
    "URU": "URY",
    "VEN": "VEN",
    "VIE": "VNM",
    "ZAM": "ZMB",
    "ZIM": "ZWE",
}


def _candidate_csvs() -> list[Path]:
    folder = manual_dir() / "hofstede"
    return sorted(folder.glob("*.csv"))


def load_hofstede_csv(path: Path | None = None) -> pd.DataFrame:
    """Load Hofstede 6-dimension CSV. No download; manual file required.

    Accepts ``;`` or ``,`` separators, ``#NULL!`` missing markers, and maps
    official ``ctr`` codes to ISO3 when needed.
    """
    if path is None:
        candidates = _candidate_csvs()
        if not candidates:
            raise FileNotFoundError(
                f"No Hofstede CSV in {manual_dir() / 'hofstede'}/. "
                "See data/manual/hofstede/README.md."
            )
        path = candidates[0]
    # Detect separator
    sample = path.read_text(encoding="utf-8", errors="replace")[:2048]
    sep = ";" if sample.count(";") > sample.count(",") else ","
    df = pd.read_csv(path, sep=sep, na_values=["#NULL!", "#NULL", "NA", ""])
    cols = {c.lower().strip(): c for c in df.columns}
    if "iso3" not in cols and "ctr" in cols:
        df = df.rename(columns={cols["ctr"]: "ctr"})
        cols = {c.lower().strip(): c for c in df.columns}
        raw_codes = df[cols.get("ctr", "ctr")].astype(str).str.upper().str.strip()
        mapped = raw_codes.map(lambda c: HOFSTEDE_CTR_TO_ISO3.get(c, c if len(c) == 3 else pd.NA))
        df["iso3"] = mapped
        cols = {c.lower().strip(): c for c in df.columns}
        cols["iso3"] = "iso3"
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
    out = out.loc[out["iso3"].notna() & (out["iso3"] != "NAN") & (out["iso3"] != "<NA>")]
    for dim in REQUIRED_DIMS:
        out[dim] = pd.to_numeric(out[dim], errors="coerce")
    # Prefer first complete-ish row per ISO3 (e.g. BEL over BEF/BEN duplicates)
    out = out.drop_duplicates("iso3", keep="first").reset_index(drop=True)
    if out.empty:
        raise ValueError(f"{path.name} produced no ISO3-mapped Hofstede rows")
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
