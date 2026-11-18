"""Hand-computed examples for ranking metrics."""

from __future__ import annotations

import pandas as pd
import pytest

from imsfe.validation.metrics import (
    auc_ext,
    kendall_corr,
    ndcg_at_k,
    precision_at_k,
    relevance_gains,
    spearman_corr,
)


def test_spearman_perfect() -> None:
    s = pd.Series([1.0, 2.0, 3.0], index=list("abc"))
    y = pd.Series([10.0, 20.0, 30.0], index=list("abc"))
    assert spearman_corr(s, y) == pytest.approx(1.0)


def test_kendall_opposite() -> None:
    s = pd.Series([1.0, 2.0, 3.0], index=list("abc"))
    y = pd.Series([30.0, 20.0, 10.0], index=list("abc"))
    assert kendall_corr(s, y) == pytest.approx(-1.0)


def test_ndcg_rank_gains_hand() -> None:
    """NDCG@2 with rank gains on y=[0.1, 0.5, 0.2] ordered by score.

    Gains (ascending rank / n): a=1/3, b=1, c=2/3.
    Score order b>c>a ⇒ rel=[1, 2/3]; DCG=1 + (2/3)/log2(3).
    Ideal=[1, 2/3]; IDCG same ⇒ NDCG=1.
    """
    score = pd.Series({"a": 1.0, "b": 3.0, "c": 2.0})
    y = pd.Series({"a": 0.1, "b": 0.5, "c": 0.2})
    gains = relevance_gains(y, mode="rank")
    assert gains["b"] == pytest.approx(1.0)
    assert ndcg_at_k(score, y, k=2, gain="rank") == pytest.approx(1.0)


def test_ndcg_clipped_documented() -> None:
    score = pd.Series({"a": 2.0, "b": 1.0})
    y = pd.Series({"a": -1.0, "b": 4.0})
    # clipped gains: a=0, b=4; ranking by score puts a first ⇒ NDCG < 1
    val = ndcg_at_k(score, y, k=2, gain="clipped")
    assert 0.0 <= val < 1.0


def test_precision_at_k_hand() -> None:
    score = pd.Series({"a": 3, "b": 2, "c": 1, "d": 0})
    y = pd.Series({"a": 1, "b": 10, "c": 9, "d": 8})
    # top-2 scores {a,b}; top-2 y {b,c}; intersection {b} ⇒ 0.5
    assert precision_at_k(score, y, k=2) == pytest.approx(0.5)


def test_auc_perfect() -> None:
    score = pd.Series([0.1, 0.4, 0.8, 0.9])
    y = pd.Series([0, 0, 1, 1])
    assert auc_ext(score, y) == pytest.approx(1.0)
