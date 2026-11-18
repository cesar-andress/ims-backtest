"""Build panel, features, and predictive outcomes from cleaned sources."""

from __future__ import annotations

from typing import Any

import pandas as pd

from imsfe.build.descriptives import (
    variable_coverage,
    write_correlation_and_vif,
    write_data_dictionary,
    write_descriptives,
)
from imsfe.build.features import compute_features
from imsfe.build.outcomes import add_outcomes
from imsfe.build.panel import build_panel_skeleton, processed_dir
from imsfe.config import load_settings, load_variables


def run_build(
    *,
    chapter: str | None = None,
    base_year: int | None = None,
) -> dict[str, Any]:
    """Build panel_ijt.parquet, data dictionary, and descriptives."""
    settings = load_settings()
    variables = load_variables()
    panel, flows, dest_map = build_panel_skeleton(
        settings, chapter=chapter, base_year=base_year
    )
    featured = compute_features(panel, flows, settings, variables)
    full = add_outcomes(featured, settings)

    out_path = processed_dir() / "panel_ijt.parquet"
    full.to_parquet(out_path, index=False)

    t1 = write_data_dictionary(full, variables)
    t3 = write_descriptives(full, variables)
    corr, vif = write_correlation_and_vif(full, variables)
    cov = variable_coverage(full, variables)

    return {
        "panel_path": out_path,
        "n_rows": int(len(full)),
        "n_cols": int(full.shape[1]),
        "shape": tuple(full.shape),
        "destinations_by_origin": dest_map,
        "coverage": cov,
        "t1_path": t1,
        "t3_path": t3,
        "corr_path": corr,
        "vif_path": vif,
        "years": (settings.years.start, settings.years.end),
        "chapter": str(chapter or settings.hs_chapters.primary).zfill(2),
        "base_year": int(base_year if base_year is not None else settings.years.end),
    }


def top_destinations_by_impv(
    panel: pd.DataFrame,
    origin: str,
    year: int,
    n: int = 10,
) -> pd.DataFrame:
    """Top-n destinations for an origin-year ranked by IMPV_raw (or IMPV)."""
    sub = panel.loc[(panel["iso3_o"] == origin) & (panel["year"] == year)].copy()
    col = "IMPV_raw" if "IMPV_raw" in sub.columns else "IMPV"
    return sub.sort_values(col, ascending=False).head(n)[
        ["iso3_o", "iso3_d", "year", col, "X_ijt"]
    ]
