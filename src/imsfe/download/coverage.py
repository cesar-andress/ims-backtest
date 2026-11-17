"""Coverage report for downloaded raw sources."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from imsfe.config import Settings, load_settings
from imsfe.io import outputs_logs_dir, raw_dir


def _year_span(settings: Settings) -> list[int]:
    return list(range(settings.years.start, settings.years.end + 1))


def _missing_share(observed: set[int] | set[str], expected: set[int] | set[str]) -> float:
    if not expected:
        return 0.0
    missing = expected - observed
    return len(missing) / len(expected)


def _section(title: str, lines: list[str]) -> list[str]:
    return [f"## {title}", ""] + lines + [""]


def coverage_worldbank(settings: Settings) -> list[str]:
    lines: list[str] = []
    expected_years = set(_year_span(settings))
    for label, rel in [
        ("WDI", "worldbank/wdi_indicators.parquet"),
        ("WGI", "worldbank/wgi_indicators.parquet"),
    ]:
        path = raw_dir() / rel
        if not path.is_file():
            lines.append(f"- **{label}**: missing (`{rel}`)")
            continue
        df = pd.read_parquet(path)
        countries = df["iso3"].nunique()
        years = set(df["year"].dropna().astype(int))
        inds = sorted(df["indicator"].unique())
        lines.append(
            f"- **{label}**: countries={countries}, years={min(years)}–{max(years)} "
            f"(n_years={len(years)}), indicators={len(inds)}, "
            f"missing_year_share={_missing_share(years, expected_years):.3f}, "
            f"rows={len(df)}"
        )
        lines.append(f"  - indicators: {', '.join(inds)}")
    return _section("World Bank", lines)


def coverage_baci(settings: Settings) -> list[str]:
    trade_dir = raw_dir() / "baci/trade_by_year"
    lines: list[str] = []
    if not trade_dir.exists():
        return _section("BACI", ["- **BACI**: missing (`baci/trade_by_year`)"])
    parts = sorted(trade_dir.glob("year=*/part.parquet"))
    if not parts:
        return _section("BACI", ["- **BACI**: directory present but no year partitions"])
    years = []
    n_rows = 0
    exporters: set[str] = set()
    importers: set[str] = set()
    for part in parts:
        year = int(part.parent.name.split("=")[1])
        years.append(year)
        df = pd.read_parquet(part, columns=["i", "j"])
        n_rows += len(df)
        exporters.update(df["i"].astype(str))
        importers.update(df["j"].astype(str))
    expected = set(_year_span(settings))
    lines.append(
        f"- **BACI trade**: partitions={len(parts)}, years={min(years)}–{max(years)}, "
        f"exporters={len(exporters)}, importers={len(importers)}, rows={n_rows}, "
        f"missing_year_share={_missing_share(set(years), expected):.3f}"
    )
    for meta in ["baci/country_codes.parquet", "baci/product_codes.parquet"]:
        p = raw_dir() / meta
        if p.is_file():
            lines.append(f"- **{meta}**: rows={len(pd.read_parquet(p))}")
        else:
            lines.append(f"- **{meta}**: missing")
    return _section("BACI", lines)


def coverage_gravity(settings: Settings) -> list[str]:
    path = raw_dir() / "cepii_gravity/gravity.parquet"
    if not path.is_file():
        return _section("CEPII Gravity", ["- **Gravity**: missing"])
    df = pd.read_parquet(path)
    years = set(df["year"].astype(int))
    expected = set(_year_span(settings))
    origins = df["iso3_o"].nunique()
    dests = df["iso3_d"].nunique()
    lines = [
        f"- **Gravity**: rows={len(df)}, iso3_o={origins}, iso3_d={dests}, "
        f"years={min(years)}–{max(years)}, "
        f"missing_year_share={_missing_share(years, expected):.3f}"
    ]
    for col in ["distw_harmonic", "distw", "contig", "comlang_off", "fta_wto"]:
        if col in df.columns:
            miss = float(df[col].isna().mean())
            lines.append(f"  - {col}: missing_share={miss:.3f}")
    return _section("CEPII Gravity", lines)


def coverage_wits(settings: Settings) -> list[str]:
    path = raw_dir() / "wits/ahs_tariffs.parquet"
    if not path.is_file():
        return _section(
            "WITS",
            [
                "- **WITS**: missing — place HS-chapter AHS CSVs in `data/manual/wits/` "
                "(see README)."
            ],
        )
    df = pd.read_parquet(path)
    years = set(df["year"].astype(int))
    expected = set(_year_span(settings))
    lines = [
        f"- **WITS**: rows={len(df)}, reporters={df['reporter_iso3'].nunique()}, "
        f"partners={df['partner_iso3'].nunique()}, "
        f"years={min(years)}–{max(years)}, "
        f"missing_year_share={_missing_share(years, expected):.3f}"
    ]
    if "hs_chapter" in df.columns:
        chapters = sorted(df["hs_chapter"].astype(str).unique())
        lines.append(f"  - hs_chapter values: {chapters}")
        expected_ch = set(settings.hs_chapter_codes())
        observed_ch = {c for c in chapters if c != "ALL"}
        lines.append(
            f"  - missing_chapter_share_vs_settings="
            f"{_missing_share(observed_ch, expected_ch):.3f}"
        )
    return _section("WITS", lines)


def coverage_hofstede() -> list[str]:
    path = raw_dir() / "hofstede/hofstede.parquet"
    if not path.is_file():
        return _section(
            "Hofstede",
            ["- **Hofstede**: missing — place CSV in `data/manual/hofstede/`."],
        )
    df = pd.read_parquet(path)
    dims = [c for c in df.columns if c != "iso3"]
    lines = [f"- **Hofstede**: countries={df['iso3'].nunique()}, rows={len(df)}"]
    for dim in dims:
        lines.append(f"  - {dim}: missing_share={float(df[dim].isna().mean()):.3f}")
    return _section("Hofstede", lines)


def write_coverage_report(
    settings: Settings | None = None,
    *,
    status: dict[str, Any] | None = None,
) -> Path:
    """Write outputs/logs/coverage.md and return its path."""
    settings = settings or load_settings()
    lines = [
        "# Data download coverage",
        "",
        f"Years in settings: {settings.years.start}–{settings.years.end}",
        f"HS chapters: {', '.join(settings.hs_chapter_codes())}",
        f"Origins: {', '.join(settings.origins)}",
        "",
    ]
    if status:
        lines.append("## Run status")
        lines.append("")
        for source, info in status.items():
            if isinstance(info, dict) and info.get("error"):
                lines.append(f"- **{source}**: ERROR — {info['error']}")
            elif isinstance(info, dict) and info.get("skipped"):
                lines.append(f"- **{source}**: skipped (idempotent)")
            else:
                lines.append(f"- **{source}**: ok")
        lines.append("")

    lines.extend(coverage_worldbank(settings))
    lines.extend(coverage_baci(settings))
    lines.extend(coverage_gravity(settings))
    lines.extend(coverage_wits(settings))
    lines.extend(coverage_hofstede())

    out = outputs_logs_dir() / "coverage.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out
