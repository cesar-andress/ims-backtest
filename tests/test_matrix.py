"""Strategic matrix unit tests (synthetic panel; no network)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from imsfe.matrix import (
    ATTRACTIVENESS_FACTORS,
    FIT_VARIABLES,
    assign_quadrant,
    build_recommendation_table,
    compute_strategic_matrix,
    fill_time_invariant_fit,
    plot_f3_matrix,
)


def _toy_panel(n_dest: int = 12, year: int = 2020) -> pd.DataFrame:
    rng = np.random.default_rng(0)
    dests = [f"D{i:02d}" for i in range(n_dest)]
    rows = []
    for i, d in enumerate(dests):
        rows.append(
            {
                "iso3_o": "COL",
                "iso3_d": d,
                "year": year,
                "hs_chapter": "64",
                "X_ijt": float(1000 * (n_dest - i)),
                "IMPV_raw": float(1e6 * (i + 1)),
                "GRW_raw": float(0.05 * (i % 3)),
                # attractiveness-ish
                "IMPV": float(rng.uniform(1, 10)),
                "IMPC": float(rng.uniform(1, 10)),
                "GRW": float(rng.uniform(-1, 1)),
                "GDPPC": float(rng.uniform(1, 10)),
                "LPI": float(rng.uniform(1, 5)),
                "GOV": float(rng.uniform(-1, 1)),
                "INFL": float(rng.uniform(0, 5)),
                "UNEMP": float(rng.uniform(1, 20)),
                # fit
                "UVGAP": float(rng.uniform(0, 2)),
                "CULT": float(rng.uniform(0, 3)),
                "LANG": float(i % 2),
                "DIST": float(rng.uniform(500, 5000)),
                "TARIF": float(rng.uniform(0, 20)),
                "FTA": float(i % 2),
                # fillers required by full WSM
                "ASIASH": float(rng.uniform(0, 1)),
                "HHI": float(rng.uniform(0, 1)),
                "EOC": float(rng.uniform(20, 100)),
                "REEXP": float(rng.uniform(0, 2)),
            }
        )
    # prior year for growth
    for i, d in enumerate(dests):
        rows.append(
            {
                "iso3_o": "COL",
                "iso3_d": d,
                "year": year - 3,
                "hs_chapter": "64",
                "X_ijt": float(500 * (n_dest - i)),
                "IMPV_raw": 1e6,
                "GRW_raw": 0.0,
                "IMPV": 1.0,
                "IMPC": 1.0,
                "GRW": 0.0,
                "GDPPC": 1.0,
                "LPI": 1.0,
                "GOV": 0.0,
                "INFL": 1.0,
                "UNEMP": 5.0,
                "UVGAP": 1.0,
                "CULT": 1.0,
                "LANG": 0.0,
                "DIST": 1000.0,
                "TARIF": 5.0,
                "FTA": 0.0,
                "ASIASH": 0.5,
                "HHI": 0.5,
                "EOC": 50.0,
                "REEXP": 1.0,
            }
        )
    return pd.DataFrame(rows)


def test_assign_quadrant_corners() -> None:
    assert assign_quadrant(8, 8, attr_cut=5, fit_cut=5) == "Global Leaders"
    assert assign_quadrant(8, 2, attr_cut=5, fit_cut=5) == "Niche Markets"
    assert assign_quadrant(2, 8, attr_cut=5, fit_cut=5) == "Emerging Opportunities"
    assert assign_quadrant(2, 2, attr_cut=5, fit_cut=5) == "Challenging Markets"


def test_compute_matrix_scores_bounded() -> None:
    panel = _toy_panel()
    mat = compute_strategic_matrix(panel, origin="COL", year=2020)
    assert len(mat) >= 2
    assert mat["attractiveness"].between(0, 10).all()
    assert mat["fit"].between(0, 10).all()
    assert set(mat["quadrant_fixed5"]).issubset(
        {
            "Global Leaders",
            "Niche Markets",
            "Emerging Opportunities",
            "Challenging Markets",
        }
    )
    # Dropped/used metadata present
    assert any(v in mat.attrs["attr_used"] for v in ("IMPV", "LPI", "GOV"))
    assert any(v in mat.attrs["fit_used"] for v in FIT_VARIABLES)


def test_recommendation_table_two_lists() -> None:
    panel = _toy_panel()
    mat = compute_strategic_matrix(panel, origin="COL", year=2020)
    tab = build_recommendation_table(mat, panel, top_n=5)
    assert set(tab["list"]) == {"recommended", "actual"}
    assert (tab["list"] == "recommended").sum() == 5
    assert (tab["list"] == "actual").sum() == 5
    assert "export_value_usd" in tab.columns
    assert "export_growth_log_3y" in tab.columns


def test_plot_f3_writes_png(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    from imsfe import matrix as matrix_mod

    monkeypatch.setattr(matrix_mod, "figures_dir", lambda: tmp_path)
    panel = _toy_panel()
    mat = compute_strategic_matrix(panel, origin="COL", year=2020)
    paths = plot_f3_matrix(mat, cutoff="median", stem="F3_test")
    assert paths["png"].is_file()
    assert paths["pdf"].is_file()


def test_attractiveness_factor_set_matches_spec() -> None:
    assert "demand" in ATTRACTIVENESS_FACTORS
    assert "logistics" in ATTRACTIVENESS_FACTORS
    assert "institutional" in ATTRACTIVENESS_FACTORS
    assert "macro_risk" in ATTRACTIVENESS_FACTORS
    assert "UVGAP" in FIT_VARIABLES and "DIST" in FIT_VARIABLES


def test_fill_time_invariant_fit_locf() -> None:
    hist = pd.DataFrame(
        {
            "iso3_o": ["COL", "COL"],
            "iso3_d": ["USA", "USA"],
            "year": [2019, 2023],
            "DIST": [1000.0, np.nan],
            "LANG": [1.0, np.nan],
            "FTA": [1.0, np.nan],
            "CULT": [np.nan, np.nan],
        }
    )
    group = hist.loc[hist["year"] == 2023].copy()
    filled, report = fill_time_invariant_fit(group, hist, 2023)
    assert float(filled["DIST"].iloc[0]) == 1000.0
    assert float(filled["LANG"].iloc[0]) == 1.0
    assert report["DIST"]["n_filled"] == 1
    assert report["CULT"]["n_filled"] == 0
