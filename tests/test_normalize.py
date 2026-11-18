"""Property tests for cross-section normalisation methods."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from imsfe.legacy import ratio_normalize as legacy_ratio
from imsfe.normalize import (
    normalize_column,
    normalize_log_minmax,
    normalize_matrix,
    normalize_minmax,
    normalize_rank,
    normalize_ratio_legacy,
    normalize_zscore,
)


def test_ratio_legacy_matches_legacy_module() -> None:
    """Benefit y/max*10 and cost min/y*10 must match legacy.ratio_normalize."""
    raw = pd.DataFrame(
        {
            "PPAD": [10.0, 20.0, 40.0],
            "INTC": [2.0, 4.0, 8.0],
            "CIBC": [1.0, 2.0, 4.0],
            "LPIN": [1.0, 2.0, 3.0],
            "CPTR": [10.0, 20.0, 30.0],
            "ITTT": [3.0, 6.0, 9.0],
            "CUTA": [1.0, 2.0, 3.0],
            "CCTI": [2.0, 4.0, 6.0],
            "IOEF": [5.0, 10.0, 15.0],
            "CLI": [1.0, 2.0, 3.0],
            "INAN": [2.0, 4.0, 8.0],
            "UNRA": [1.0, 2.0, 4.0],
            "FSIN": [1.0, 2.0, 3.0],
            "INRI": [2.0, 3.0, 4.0],
            "DEIN": [1.0, 2.0, 3.0],
            "GLIN": [2.0, 4.0, 6.0],
            "CPIN": [1.0, 3.0, 5.0],
            "CUDI": [1.0, 2.0, 4.0],
        }
    )
    from imsfe.legacy import DIRECTIONS, VARIABLES

    got = normalize_matrix(raw[VARIABLES], DIRECTIONS, "ratio_legacy")
    exp = legacy_ratio(raw[VARIABLES])
    pd.testing.assert_frame_equal(got, exp, rtol=1e-12, atol=1e-12)


def test_minmax_range_and_direction() -> None:
    s = pd.Series([1.0, 3.0, 5.0])
    b = normalize_minmax(s, "benefit")
    c = normalize_minmax(s, "cost")
    assert b.min() == 0.0 and b.max() == 10.0
    assert c.min() == 0.0 and c.max() == 10.0
    assert b.is_monotonic_increasing
    assert c.is_monotonic_decreasing
    # Constant → midpoint
    mid = normalize_minmax(pd.Series([2.0, 2.0, 2.0]), "benefit")
    assert (mid == 5.0).all()


def test_zscore_affine_invariance_benefit() -> None:
    """Positive affine transform ax+b (a>0) leaves benefit z-scores unchanged."""
    s = pd.Series([1.0, 2.0, 4.0, 7.0])
    z1 = normalize_zscore(s, "benefit")
    z2 = normalize_zscore(3.0 * s + 5.0, "benefit")
    pd.testing.assert_series_equal(z1, z2, rtol=1e-12, atol=1e-12)
    # Cost flips sign relative to benefit
    zc = normalize_zscore(s, "cost")
    pd.testing.assert_series_equal(zc, -z1, rtol=1e-12, atol=1e-12)


def test_rank_monotonicity() -> None:
    s = pd.Series([10.0, 30.0, 20.0])
    r = normalize_rank(s, "benefit")
    assert r.iloc[1] == r.max()
    rc = normalize_rank(s, "cost")
    assert rc.iloc[0] == rc.max()
    assert r.max() == 10.0


def test_log_minmax_handles_nonpositive() -> None:
    s = pd.Series([-2.0, 0.0, 5.0])
    out = normalize_log_minmax(s, "benefit")
    assert out.min() == 0.0 and out.max() == 10.0
    assert out.is_monotonic_increasing


def test_ratio_legacy_cost_nonpositive_is_nan() -> None:
    s = pd.Series([0.0, 2.0, 4.0])
    out = normalize_ratio_legacy(s, "cost")
    assert np.isnan(out.iloc[0])
    assert out.iloc[1] == pytest.approx(10.0)  # min(pos)=2 → 2/2*10
    assert out.iloc[2] == pytest.approx(5.0)


def test_normalize_column_dispatch() -> None:
    s = pd.Series([1.0, 2.0, 3.0])
    assert normalize_column(s, "benefit", "minmax").max() == 10.0
