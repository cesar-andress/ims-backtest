"""Learned weights: absent vars → 0; two consecutive fits bit-identical."""

from __future__ import annotations

import numpy as np
import pandas as pd

from imsfe.config import load_variables
from imsfe.validation.learned import fit_learned_weights, variables_with_train_data


def _tiny_panel() -> pd.DataFrame:
    """Minimal panel with some variables present and CULT absent."""
    variables = load_variables()
    ids = [v.id for v in variables.variables]
    rows = []
    rng = np.random.default_rng(0)
    for origin in ("COL", "PER"):
        for year in (2015, 2016, 2017):
            dests = [f"D{i:02d}" for i in range(25)]
            for i, dest in enumerate(dests):
                row = {
                    "iso3_o": origin,
                    "iso3_d": dest,
                    "year": year,
                    "hs_chapter": "64",
                    "X_ijt": float(1000 * (i + 1)),
                    "y_int_k1": float(rng.normal(0, 0.2)),
                }
                for vid in ids:
                    if vid == "CULT":
                        row[vid] = np.nan
                    else:
                        row[vid] = float(rng.random())
                rows.append(row)
    return pd.DataFrame(rows)


def test_absent_variables_get_zero_weight() -> None:
    panel = _tiny_panel()
    present, absent = variables_with_train_data(panel, [2015, 2016], load_variables())
    assert "CULT" in absent
    assert "IMPV" in present
    w, info = fit_learned_weights(
        panel,
        [2015, 2016],
        horizon=1,
        n_restarts=3,
        maxiter=15,
        force_cpu=True,
    )
    flat = w.flat()
    assert "CULT" in info["absent_variables"]
    # CULT may be dropped from hierarchy entirely; flat() then omits it → treat as 0
    cult_w = float(flat.get("CULT", 0.0)) if hasattr(flat, "get") else (
        float(flat["CULT"]) if "CULT" in flat.index else 0.0
    )
    assert cult_w == 0.0
    cmp = info["comparison"]
    assert float(cmp.loc[cmp["variable"] == "CULT", "learned"].iloc[0]) == 0.0


def test_two_consecutive_fits_bit_identical() -> None:
    panel = _tiny_panel()
    years = [2015, 2016]
    _, info1 = fit_learned_weights(
        panel, years, horizon=1, n_restarts=3, maxiter=20, force_cpu=True
    )
    _, info2 = fit_learned_weights(
        panel, years, horizon=1, n_restarts=3, maxiter=20, force_cpu=True
    )
    a = info1["comparison"]["learned"].to_numpy(dtype=float)
    b = info2["comparison"]["learned"].to_numpy(dtype=float)
    assert np.array_equal(a, b)
