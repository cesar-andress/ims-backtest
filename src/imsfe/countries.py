"""ISO3 country code mapping and English display names."""

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

# Canonical English short names for manuscript tables (ISO3 -> name).
ISO3_TO_NAME: dict[str, str] = {
    "ARE": "United Arab Emirates",
    "ARG": "Argentina",
    "AUS": "Australia",
    "AUT": "Austria",
    "BEL": "Belgium",
    "BGD": "Bangladesh",
    "BGR": "Bulgaria",
    "BRA": "Brazil",
    "CAN": "Canada",
    "CHE": "Switzerland",
    "CHL": "Chile",
    "CHN": "China",
    "COL": "Colombia",
    "CZE": "Czechia",
    "DEU": "Germany",
    "DNK": "Denmark",
    "DZA": "Algeria",
    "ECU": "Ecuador",
    "ESP": "Spain",
    "FIN": "Finland",
    "FRA": "France",
    "GBR": "United Kingdom",
    "GRC": "Greece",
    "HKG": "Hong Kong SAR",
    "HRV": "Croatia",
    "HUN": "Hungary",
    "IDN": "Indonesia",
    "IND": "India",
    "IRL": "Ireland",
    "IRQ": "Iraq",
    "ISR": "Israel",
    "ITA": "Italy",
    "JPN": "Japan",
    "KAZ": "Kazakhstan",
    "KGZ": "Kyrgyzstan",
    "KOR": "Korea, Rep.",
    "KWT": "Kuwait",
    "MAR": "Morocco",
    "MEX": "Mexico",
    "MYS": "Malaysia",
    "NLD": "Netherlands",
    "NOR": "Norway",
    "NZL": "New Zealand",
    "PER": "Peru",
    "PHL": "Philippines",
    "POL": "Poland",
    "PRT": "Portugal",
    "QAT": "Qatar",
    "ROU": "Romania",
    "RUS": "Russian Federation",
    "SAU": "Saudi Arabia",
    "SGP": "Singapore",
    "SVK": "Slovak Republic",
    "SVN": "Slovenia",
    "SWE": "Sweden",
    "THA": "Thailand",
    "TUR": "Türkiye",
    "UKR": "Ukraine",
    "USA": "United States",
    "VNM": "Viet Nam",
    "ZAF": "South Africa",
}


def to_iso3(name: str) -> str:
    """Map a country name to ISO3; raise if unknown."""
    key = name.strip()
    if key not in LEGACY_NAME_TO_ISO3:
        raise KeyError(f"Unknown country name for ISO3 mapping: {name!r}")
    return LEGACY_NAME_TO_ISO3[key]


def country_name(iso3: str) -> str:
    """English display name for an ISO3 code; falls back to the code itself."""
    code = str(iso3).strip().upper()
    return ISO3_TO_NAME.get(code, code)


def with_country_name(df, iso_col: str = "iso3", name_col: str = "country"):
    """Return a copy with a canonical English ``name_col`` beside ``iso_col``."""
    out = df.copy()
    if iso_col not in out.columns:
        return out
    out[name_col] = out[iso_col].map(lambda x: country_name(str(x)))
    return out
