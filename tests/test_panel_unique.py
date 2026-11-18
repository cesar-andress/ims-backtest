"""Panel key uniqueness and new outcome columns."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from imsfe.build.outcomes import add_outcomes
from imsfe.validation.run import assert_panel_unique


def test_assert_panel_unique_passes() -> None:
    panel = pd.DataFrame(
        {
            "iso3_o": ["COL", "COL"],
            "iso3_d": ["USA", "DEU"],
            "year": [2020, 2020],
            "hs_chapter": ["64", "64"],
            "X_ijt": [1.0, 2.0],
        }
    )
    assert_panel_unique(panel)


def test_assert_panel_unique_fails_on_dupes() -> None:
    panel = pd.DataFrame(
        {
            "iso3_o": ["COL", "COL"],
            "iso3_d": ["USA", "USA"],
            "year": [2020, 2020],
            "hs_chapter": ["64", "64"],
            "X_ijt": [1.0, 2.0],
        }
    )
    with pytest.raises(AssertionError, match="duplicate"):
        assert_panel_unique(panel)


def test_outcomes_growth_and_new_markets() -> None:
    rows = []
    for year in (2018, 2019, 2020, 2021):
        for i, dest in enumerate(["USA", "DEU", "CHN", "BRA"]):
            rows.append(
                {
                    "iso3_o": "COL",
                    "iso3_d": dest,
                    "year": year,
                    "hs_chapter": "64",
                    "X_ijt": float((i + 1) * 1000 * (year - 2017)),
                }
            )
    panel = pd.DataFrame(rows)
    out = add_outcomes(panel)
    assert "y_growth_k1" in out.columns
    assert "y_newmarket_k1" in out.columns
    assert "new_market_at_t" in out.columns
    # Growth defined whenever future year exists
    sub = out.loc[out["year"] == 2019]
    assert sub["y_growth_k1"].notna().all()
    # New-market relevance is NaN for above-median share destinations
    assert sub["y_newmarket_k1"].isna().any()
    assert np.isfinite(sub["y_newmarket_k1"].to_numpy(dtype=float)).sum() >= 1
