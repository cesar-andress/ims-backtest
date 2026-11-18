"""ISO 3166-1 alpha-3 ↔ numeric helpers for WITS TRN reporters/partners."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml

from imsfe.config import config_dir

# EU customs territory reporter code used by WITS/TRAINS.
WITS_EU_REPORTER = "918"

# EU-27 members (post-2020). All map to WITS reporter 918 for applied tariffs.
EU27_ISO3: frozenset[str] = frozenset(
    {
        "AUT",
        "BEL",
        "BGR",
        "HRV",
        "CYP",
        "CZE",
        "DNK",
        "EST",
        "FIN",
        "FRA",
        "DEU",
        "GRC",
        "HUN",
        "IRL",
        "ITA",
        "LVA",
        "LTU",
        "LUX",
        "MLT",
        "NLD",
        "POL",
        "PRT",
        "ROU",
        "SVK",
        "SVN",
        "ESP",
        "SWE",
    }
)


@lru_cache(maxsize=1)
def iso3_to_numeric(path: Path | None = None) -> dict[str, str]:
    """Load ISO3 → zero-padded numeric codes from config/iso3_numeric.yaml."""
    p = path or (config_dir() / "iso3_numeric.yaml")
    with p.open(encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)
    if not isinstance(raw, dict):
        raise ValueError(f"Invalid ISO numeric map: {p}")
    return {str(k).upper(): str(v).zfill(3) for k, v in raw.items()}


def wits_reporter_code(iso3: str, *, eu_members: frozenset[str] = EU27_ISO3) -> str:
    """Return WITS reporter code (EU members → 918)."""
    code = iso3.upper()
    if code in eu_members:
        return WITS_EU_REPORTER
    mapping = iso3_to_numeric()
    if code not in mapping:
        raise KeyError(f"No ISO numeric code for reporter {code!r}")
    return mapping[code]


def wits_partner_code(iso3: str) -> str:
    """Return WITS partner (origin) numeric code."""
    code = iso3.upper()
    mapping = iso3_to_numeric()
    if code not in mapping:
        raise KeyError(f"No ISO numeric code for partner {code!r}")
    return mapping[code]


def iso3_for_numeric(numeric: str) -> str | None:
    """Reverse lookup; returns None if unknown (e.g. EU 918)."""
    num = str(numeric).zfill(3)
    if num == WITS_EU_REPORTER:
        return None
    inv = {v: k for k, v in iso3_to_numeric().items()}
    return inv.get(num)
