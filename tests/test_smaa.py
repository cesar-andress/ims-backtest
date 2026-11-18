"""SMAA sampling, reproducibility, and zero-dispersion collapse."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from imsfe.smaa import (
    build_expert_stats,
    dirichlet_concentration,
    ranks_from_scores,
    run_smaa_wsm,
    sample_dirichlet,
)
from imsfe.weights import Weights, weights_equal


def test_dirichlet_mom_formula() -> None:
    mu = np.array([0.5, 0.3, 0.2])
    # Choose sigma so each κ_i equals 99: σ² = μ(1-μ)/(κ+1)
    kappa_target = 99.0
    sigma = np.sqrt(mu * (1 - mu) / (kappa_target + 1))
    kappa = dirichlet_concentration(mu, sigma)
    assert kappa == pytest.approx(kappa_target, rel=1e-6)


def test_zero_dispersion_collapses_to_deterministic() -> None:
    """dispersion_scale=0 ⇒ every sample equals the expert-mean ranking."""
    norm = pd.DataFrame(
        {
            "v1": [10.0, 8.0, 6.0, 4.0],
            "v2": [1.0, 3.0, 5.0, 7.0],
            "v3": [9.0, 7.0, 5.0, 3.0],
        },
        index=["A", "B", "C", "D"],
    )
    center = Weights(
        factors=pd.Series({"f1": 0.6, "f2": 0.4}),
        variables_within={
            "f1": pd.Series({"v1": 0.5, "v2": 0.5}),
            "f2": pd.Series({"v3": 1.0}),
        },
        scheme="test",
    )
    stats = build_expert_stats(center, default_cv=0.3)
    res = run_smaa_wsm(
        norm,
        center,
        stats,
        n_samples=500,
        seed=7,
        dispersion_scale=0.0,
    )
    # All samples identical ranks
    assert np.all(res.ranks == res.ranks[:, :1])
    for alt in res.alternatives:
        assert int(res.ranks[res.alternatives.index(alt), 0]) == int(
            res.deterministic_ranks.loc[alt]
        )
    assert (res.p_top_k(1) == (res.deterministic_ranks == 1).astype(float)).all()


def test_smaa_seed_reproducible() -> None:
    norm = pd.DataFrame(
        {"a": [1.0, 2.0, 3.0], "b": [3.0, 2.0, 1.0]},
        index=["x", "y", "z"],
    )
    center = Weights(
        factors=pd.Series({"f": 1.0}),
        variables_within={"f": pd.Series({"a": 0.4, "b": 0.6})},
        scheme="test",
    )
    stats = build_expert_stats(center, default_cv=0.2)
    r1 = run_smaa_wsm(norm, center, stats, n_samples=200, seed=42, dispersion_scale=1.0)
    r2 = run_smaa_wsm(norm, center, stats, n_samples=200, seed=42, dispersion_scale=1.0)
    r3 = run_smaa_wsm(norm, center, stats, n_samples=200, seed=99, dispersion_scale=1.0)
    np.testing.assert_array_equal(r1.ranks, r2.ranks)
    assert not np.array_equal(r1.ranks, r3.ranks)


def test_sample_dirichlet_means_near_mu() -> None:
    mu = np.array([0.5, 0.25, 0.25])
    sigma = np.array([0.05, 0.04, 0.04])
    rng = np.random.default_rng(0)
    draws = sample_dirichlet(mu, sigma, 20_000, rng)
    np.testing.assert_allclose(draws.mean(axis=0), mu, atol=0.01)
    assert np.allclose(draws.sum(axis=1), 1.0)


def test_ranks_from_scores_basic() -> None:
    scores = np.array([[3.0, 1.0], [2.0, 4.0], [1.0, 2.0]])
    ranks = ranks_from_scores(scores)
    # sample 0: alt0 best, sample 1: alt1 best
    assert list(ranks[:, 0]) == [1, 2, 3]
    assert list(ranks[:, 1]) == [3, 1, 2]


def test_build_expert_stats_with_equal_weights() -> None:
    w = weights_equal()
    stats = build_expert_stats(w)
    assert len(stats.factor_names) == len(w.factors)
    assert stats.factor_mu.sum() == pytest.approx(1.0)
