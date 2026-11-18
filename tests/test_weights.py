"""Tests for weight schemes and validation."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from imsfe.config import load_variables
from imsfe.weights import (
    get_weights,
    weights_entropy,
    weights_equal,
    weights_expert_mean,
    weights_learned,
)


def test_equal_sums_to_one() -> None:
    w = weights_equal()
    assert np.isclose(w.factors.sum(), 1.0)
    for vw in w.variables_within.values():
        assert np.isclose(vw.sum(), 1.0)
    assert np.isclose(w.flat().sum(), 1.0)


def test_expert_mean_logs_unmapped_and_validates() -> None:
    w = weights_expert_mean()
    assert w.scheme == "expert_mean"
    assert np.isclose(w.factors.sum(), 1.0)
    assert (w.factors >= 0).all()
    # New variable ids are not in the legacy Excel → notes must mention them
    assert any("IMPV" in n for n in w.notes)
    flat = w.flat()
    assert np.isclose(flat.sum(), 1.0)
    assert (flat >= 0).all()


def test_entropy_and_critic_flat() -> None:
    matrix = pd.DataFrame(
        {"a": [1.0, 2.0, 3.0], "b": [3.0, 2.0, 1.0], "c": [1.0, 1.0, 2.0]}
    )
    e = weights_entropy(matrix)
    assert np.isclose(e.sum(), 1.0)
    c = get_weights(
        "critic",
        load_variables(),
        matrix=matrix.rename(columns={"a": "IMPV", "b": "DIST", "c": "LPI"}),
        directions={"IMPV": "benefit", "DIST": "cost", "LPI": "benefit"},
    )
    assert np.isclose(c.flat().sum(), 1.0)


def test_learned_requires_fit() -> None:
    from imsfe.weights import clear_learned_weights

    clear_learned_weights()
    with pytest.raises(RuntimeError, match="not fitted"):
        weights_learned()


def test_restrict_drops_missing() -> None:
    w = weights_equal()
    # Keep only demand variables that exist
    demand_vars = list(w.variables_within["demand"].index)[:1]
    other = list(w.variables_within["logistics"].index)[:1]
    rw = w.restrict(demand_vars + other)
    assert set(rw.factors.index) <= {"demand", "logistics"}
    assert np.isclose(rw.factors.sum(), 1.0)
