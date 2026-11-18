"""Construct the origin × destination × year trade panel from BACI."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from imsfe.config import Settings, load_settings, project_root
from imsfe.io import raw_dir

# CEPII BACI stores ``v`` in thousands of current USD.
BACI_VALUE_SCALE = 1_000.0


def processed_dir() -> Path:
    """Return data/processed/."""
    path = project_root() / "data" / "processed"
    path.mkdir(parents=True, exist_ok=True)
    return path


def baci_trade_dir() -> Path:
    return raw_dir() / "baci" / "trade_by_year"


def load_baci_country_map() -> dict[str, str]:
    """Map BACI numeric country codes (as str) to ISO3."""
    path = raw_dir() / "baci" / "country_codes.parquet"
    if not path.is_file():
        raise FileNotFoundError(f"Missing BACI country codes: {path}")
    cc = pd.read_parquet(path)
    code = cc["country_code"].astype(str)
    iso3 = cc["country_iso3"].astype(str).str.upper()
    return dict(zip(code, iso3, strict=False))


def _chapter_mask(k: pd.Series, chapter: str) -> pd.Series:
    ch = str(chapter).zfill(2)
    ks = k.astype(str).str.zfill(6)
    return ks.str.startswith(ch)


def load_baci_chapter_flows(
    settings: Settings | None = None,
    *,
    chapter: str | None = None,
    trade_frames: dict[int, pd.DataFrame] | None = None,
    country_map: dict[str, str] | None = None,
) -> pd.DataFrame:
    """Aggregate BACI 6-digit flows to chapter level.

    Returns columns: year, iso3_o, iso3_d, value_usd, qty_tons, hs_chapter.
    ``value_usd`` is converted from BACI thousands-USD to USD.
    """
    settings = settings or load_settings()
    chapter = str(chapter or settings.hs_chapters.primary).zfill(2)
    cmap = country_map or load_baci_country_map()
    years = range(settings.years.start, settings.years.end + 1)
    frames: list[pd.DataFrame] = []

    for year in years:
        if trade_frames is not None:
            if year not in trade_frames:
                continue
            raw = trade_frames[year].copy()
        else:
            part = baci_trade_dir() / f"year={year}"
            if not part.exists():
                continue
            raw = pd.read_parquet(part)
        if raw.empty:
            continue
        mask = _chapter_mask(raw["k"], chapter)
        sub = raw.loc[mask, ["t", "i", "j", "v", "q"]].copy()
        if sub.empty:
            continue
        sub["iso3_o"] = sub["i"].astype(str).map(cmap)
        sub["iso3_d"] = sub["j"].astype(str).map(cmap)
        sub = sub.dropna(subset=["iso3_o", "iso3_d"])
        agg = (
            sub.groupby(["iso3_o", "iso3_d"], as_index=False)
            .agg(value_thousands=("v", "sum"), qty_tons=("q", "sum"))
        )
        agg["year"] = int(year)
        agg["hs_chapter"] = chapter
        agg["value_usd"] = agg["value_thousands"] * BACI_VALUE_SCALE
        frames.append(agg[["year", "iso3_o", "iso3_d", "value_usd", "qty_tons", "hs_chapter"]])

    if not frames:
        raise FileNotFoundError(
            f"No BACI chapter-{chapter} flows found for years "
            f"{settings.years.start}-{settings.years.end}"
        )
    out = pd.concat(frames, ignore_index=True)
    return out


def destination_import_totals(flows: pd.DataFrame, year: int) -> pd.DataFrame:
    """Total chapter imports by destination in ``year`` (USD)."""
    sub = flows.loc[flows["year"] == year]
    totals = (
        sub.groupby("iso3_d", as_index=False)["value_usd"]
        .sum()
        .rename(columns={"iso3_d": "iso3", "value_usd": "import_usd"})
        .sort_values("import_usd", ascending=False)
        .reset_index(drop=True)
    )
    return totals


def select_destinations_for_origin(
    import_totals: pd.DataFrame,
    origin: str,
    n: int,
) -> list[str]:
    """Top-N importers excluding the origin itself."""
    ranked = import_totals.loc[import_totals["iso3"] != origin, "iso3"].tolist()
    return ranked[:n]


def build_panel_skeleton(
    settings: Settings | None = None,
    *,
    chapter: str | None = None,
    flows: pd.DataFrame | None = None,
    base_year: int | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, list[str]]]:
    """Build origin×destination×year skeleton with bilateral export flows.

    Returns
    -------
    panel
        Columns: iso3_o, iso3_d, year, hs_chapter, X_ijt, Q_ijt
    flows
        Full chapter-level BACI aggregates (all pairs).
    destinations_by_origin
        Top-N destination lists used for each origin.
    """
    settings = settings or load_settings()
    chapter = str(chapter or settings.hs_chapters.primary).zfill(2)
    flows = flows if flows is not None else load_baci_chapter_flows(settings, chapter=chapter)
    base = int(base_year if base_year is not None else settings.years.end)
    totals = destination_import_totals(flows, base)
    if totals.empty:
        raise RuntimeError(f"No destination imports for chapter {chapter} in base year {base}")

    dest_map: dict[str, list[str]] = {}
    rows: list[dict] = []
    years = list(range(settings.years.start, settings.years.end + 1))

    # Bilateral lookup for X_ijt
    bilat = flows.set_index(["iso3_o", "iso3_d", "year"])[["value_usd", "qty_tons"]]

    for origin in settings.origins:
        dests = select_destinations_for_origin(totals, origin, settings.n_destinations)
        dest_map[origin] = dests
        for dest in dests:
            for year in years:
                key = (origin, dest, year)
                if key in bilat.index:
                    x = float(bilat.loc[key, "value_usd"])
                    q = float(bilat.loc[key, "qty_tons"])
                    # MultiIndex may return Series if duplicates
                    if isinstance(x, pd.Series):
                        x = float(x.iloc[0])
                        q = float(q.iloc[0])
                else:
                    x, q = 0.0, float("nan")
                rows.append(
                    {
                        "iso3_o": origin,
                        "iso3_d": dest,
                        "year": year,
                        "hs_chapter": chapter,
                        "X_ijt": x,
                        "Q_ijt": q,
                    }
                )

    panel = pd.DataFrame.from_records(rows)
    panel.attrs["base_year"] = base
    panel.attrs["destinations_by_origin"] = dest_map
    return panel, flows, dest_map


def build_panel(
    settings: Settings | None = None,
    *,
    chapter: str | None = None,
    flows: pd.DataFrame | None = None,
    base_year: int | None = None,
) -> pd.DataFrame:
    """Public helper returning only the skeleton panel."""
    panel, _, _ = build_panel_skeleton(
        settings, chapter=chapter, flows=flows, base_year=base_year
    )
    return panel
