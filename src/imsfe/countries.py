"""ISO3 country code mapping and name normalisation."""

from __future__ import annotations

# Names as they appear in the legacy Excel (and common variants) -> ISO3.
LEGACY_NAME_TO_ISO3: dict[str, str] = {
    "United States": "USA",
    "United States of America": "USA",
    "Germany": "DEU",
    "France": "FRA",
    "Italy": "ITA",
    "China": "CHN",
    "Netherlands": "NLD",
    "United Kingdom": "GBR",
    "Japan": "JPN",
    "Spain": "ESP",
    "Belgium": "BEL",
    "Russia": "RUS",
    "Poland": "POL",
    "South Korea": "KOR",
    "United Arab Emirates": "ARE",
    "Canada": "CAN",
    "Switzerland": "CHE",
    "Austria": "AUT",
    "Australia": "AUS",
    "Mexico": "MEX",
    "Czech Republic": "CZE",
    "Turkey": "TUR",
    "Türkiye": "TUR",
    "Romania": "ROU",
    "Viet Nam": "VNM",
    "Vietnam": "VNM",
    "Sweden": "SWE",
    "Slovakia": "SVK",
    "Denmark": "DNK",
    "Saudi Arabia": "SAU",
    "Panama": "PAN",
    "Portugal": "PRT",
    "Singapore": "SGP",
}


def to_iso3(name: str) -> str:
    """Map a country name to ISO3; raise if unknown."""
    key = name.strip()
    if key not in LEGACY_NAME_TO_ISO3:
        raise KeyError(f"Unknown country name for ISO3 mapping: {name!r}")
    return LEGACY_NAME_TO_ISO3[key]
