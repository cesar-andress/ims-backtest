"""Unit tests for panel construction and feature transforms (no network)."""

from __future__ import annotations

import numpy as np
import pandas as pd

from imsfe.build.features import apply_transform, kogut_singh
from imsfe.build.panel import select_destinations_for_origin


def test_select_destinations_excludes_origin() -> None:
    totals = pd.DataFrame(
        {
            "iso3": ["USA", "DEU", "COL", "FRA", "CHN"],
            "import_usd": [5e9, 4e9, 3e9, 2e9, 1e9],
        }
    )
    dests = select_destinations_for_origin(totals, "COL", n=3)
    assert dests == ["USA", "DEU", "FRA"]
    assert "COL" not in dests


def test_apply_transform_log() -> None:
    s = pd.Series([1.0, 0.0, np.e, -1.0])
    out = apply_transform(s, "log")
    assert abs(out[0] - 0.0) < 1e-12
    assert np.isnan(out[1])
    assert abs(out[2] - 1.0) < 1e-12
    assert np.isnan(out[3])


def test_kogut_singh_basic() -> None:
    a = pd.Series({"pdi": 10, "idv": 20, "mas": 30, "uai": 40, "ltowvs": 50, "ivr": 60})
    b = pd.Series({"pdi": 10, "idv": 20, "mas": 30, "uai": 40, "ltowvs": 50, "ivr": 60})
    var = pd.Series({"pdi": 1.0, "idv": 1.0, "mas": 1.0, "uai": 1.0, "ltowvs": 1.0, "ivr": 1.0})
    assert kogut_singh(a, b, var) == 0.0
    c = b.copy()
    c["pdi"] = 12
    assert abs(kogut_singh(a, c, var) - (4.0 / 6.0)) < 1e-12
