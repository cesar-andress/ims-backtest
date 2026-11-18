"""Determinism and leakage guards for the ML benchmark."""

from __future__ import annotations

import numpy as np
import pandas as pd

from imsfe.validation.backtest import make_split
from imsfe.validation.ml import (
    _ts_cv_folds,
    compare_factor_importances,
    detect_backend,
    feature_matrix,
    run_ml_walkforward,
)
from imsfe.weights import Weights


def _toy_panel(n_years: int = 8, n_dest: int = 12) -> pd.DataFrame:
    rng = np.random.default_rng(0)
    rows = []
    years = list(range(2012, 2012 + n_years))
    dests = [f"D{i:02d}" for i in range(n_dest)]
    for origin in ("COL", "PER"):
        for year in years:
            for j, dest in enumerate(dests):
                # Features known at t; outcome uses a lagged signal + noise
                base = j + 0.1 * (year - 2012)
                rows.append(
                    {
                        "iso3_o": origin,
                        "iso3_d": dest,
                        "year": year,
                        "IMPV": base + rng.normal(0, 0.2),
                        "IMPC": base / 10 + rng.normal(0, 0.05),
                        "GRW": rng.normal(0, 0.1),
                        "GDPPC": 9.0 + rng.normal(0, 0.1),
                        "DIST": 8.0 + 0.01 * j,
                        "TARIF": np.nan,
                        "FTA": float(j % 2),
                        "LPI": 3.0 + rng.normal(0, 0.1),
                        "ASIASH": 0.2 + 0.01 * j,
                        "HHI": 0.1,
                        "UVGAP": abs(rng.normal(0.5, 0.2)),
                        "CULT": np.nan,
                        "LANG": float(j % 3 == 0),
                        "INFL": abs(rng.normal(1.0, 0.5)),
                        "UNEMP": 5.0 + rng.normal(0, 0.5),
                        "GOV": rng.normal(0, 1),
                        "EOC": 50 + rng.normal(0, 5),
                        "REEXP": 0.2,
                        "y_int_k1": base + rng.normal(0, 0.5),
                        "y_ext_k1": float(j < 3),
                        "y_level_k1": max(0.0, 1000 * (base + 1)),
                    }
                )
    return pd.DataFrame.from_records(rows)


def test_ts_cv_folds_expanding() -> None:
    folds = _ts_cv_folds([2012, 2013, 2014, 2015, 2016])
    assert folds[0] == ([2012, 2013, 2014], [2015])
    assert all(max(tr) < va[0] for tr, va in folds)


def test_ml_seed_reproducible() -> None:
    panel = _toy_panel()
    split = make_split(panel["year"].unique(), first_test_year=2017, horizon=1)
    # Force CPU LightGBM for CI portability
    r1 = run_ml_walkforward(panel, split, seed=42, backend="lightgbm_cpu")
    r2 = run_ml_walkforward(panel, split, seed=42, backend="lightgbm_cpu")
    pd.testing.assert_frame_equal(
        r1.predictions.sort_values(["iso3_o", "year", "iso3_d"]).reset_index(drop=True),
        r2.predictions.sort_values(["iso3_o", "year", "iso3_d"]).reset_index(drop=True),
    )
    assert r1.runtime_sec >= 0


def test_ml_no_test_year_in_training_log() -> None:
    panel = _toy_panel()
    split = make_split(panel["year"].unique(), first_test_year=2017, horizon=1)
    r = run_ml_walkforward(panel, split, seed=0, backend="lightgbm_cpu")
    assert max(r.log["train_years"]) + 1 < 2017
    assert min(r.log["test_years"]) >= 2017
    assert set(r.block_metrics["year"]) <= set(split.test_feature_years)


def test_compare_factor_importances_shares() -> None:
    shap = pd.Series({"demand": 0.6, "logistics": 0.4})
    expert = Weights(
        factors=pd.Series({"demand": 0.5, "logistics": 0.5}),
        variables_within={
            "demand": pd.Series({"IMPV": 1.0}),
            "logistics": pd.Series({"LPI": 1.0}),
        },
        scheme="test",
    )
    df = compare_factor_importances(shap, expert, None)
    assert set(df["factor"]) >= {"demand", "logistics"}
    assert df.loc[df.factor == "demand", "shap_share"].iloc[0] == 0.6


def test_feature_matrix_maps_factors() -> None:
    panel = _toy_panel(n_years=3, n_dest=4)
    feats, cols, factor_of = feature_matrix(panel)
    assert "IMPV" in cols
    assert factor_of["IMPV"] == "demand"
    assert feats.shape[0] == len(panel)


def test_detect_backend_returns_known() -> None:
    assert detect_backend(0) in {"xgboost_cuda", "lightgbm_cpu"}
