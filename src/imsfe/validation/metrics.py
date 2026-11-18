"""Ranking and classification metrics for predictive validation.

NDCG gain
---------
For intensive-margin validation we set the relevance gain of destination ``j`` to
a **rank-transformed** ``y_int`` within the origin-year cross-section:

1. Keep destinations with non-null ``y_int`` (SPEC: defined only when
   ``X_ijt`` exceeds the entry threshold).
2. Rank ``y_int`` ascending (average ties); convert to gain
   ``g = rank / n`` so the best growth gets gain 1 and the worst gets ``1/n``.
   (Equivalently a positive monotone transform of export growth; we do **not**
   use raw ``y_int`` as gain because it can be negative.)

An alternative clip-based gain ``max(y_int, 0)`` is available via
``ndcg_gain="clipped"`` for sensitivity checks.
"""

from __future__ import annotations

from typing import Literal

import numpy as np
import pandas as pd
from scipy.stats import kendalltau, spearmanr
from sklearn.metrics import roc_auc_score

GainMode = Literal["rank", "clipped"]


def spearman_corr(score: pd.Series, y: pd.Series) -> float:
    """Spearman ρ between score and outcome (pairwise complete)."""
    a, b = _align(score, y)
    if len(a) < 3:
        return float("nan")
    rho, _ = spearmanr(a, b)
    return float(rho)


def kendall_corr(score: pd.Series, y: pd.Series) -> float:
    """Kendall τ between score and outcome (pairwise complete)."""
    a, b = _align(score, y)
    if len(a) < 3:
        return float("nan")
    tau, _ = kendalltau(a, b)
    return float(tau)


def _align(a: pd.Series, b: pd.Series) -> tuple[np.ndarray, np.ndarray]:
    aa = a[~a.index.duplicated(keep="first")].rename("a")
    bb = b[~b.index.duplicated(keep="first")].rename("b")
    df = pd.concat([aa, bb], axis=1).dropna()
    return df["a"].to_numpy(dtype=float), df["b"].to_numpy(dtype=float)


def _dcg(relevances: np.ndarray, k: int) -> float:
    rel = np.asarray(relevances[:k], dtype=float)
    if rel.size == 0:
        return 0.0
    discounts = 1.0 / np.log2(np.arange(2, rel.size + 2))
    return float(np.sum(rel * discounts))


def relevance_gains(y_int: pd.Series, *, mode: GainMode = "rank") -> pd.Series:
    """Non-negative gains from ``y_int`` for NDCG (see module docstring)."""
    s = pd.to_numeric(y_int, errors="coerce").dropna()
    if s.empty:
        return s
    if mode == "clipped":
        g = s.clip(lower=0.0)
        return g
    # rank-transform to (0, 1]
    ranks = s.rank(method="average", ascending=True)
    return ranks / float(len(ranks))


def ndcg_at_k(
    score: pd.Series,
    y_int: pd.Series,
    k: int = 10,
    *,
    gain: GainMode = "rank",
) -> float:
    """NDCG@k with gains from ``y_int`` (rank-transformed by default)."""
    gains = relevance_gains(y_int, mode=gain)
    df = pd.concat([score.rename("score"), gains.rename("gain")], axis=1).dropna()
    if df.empty:
        return float("nan")
    k_eff = min(k, len(df))
    ordered = df.sort_values("score", ascending=False)["gain"].to_numpy(dtype=float)
    ideal = np.sort(df["gain"].to_numpy(dtype=float))[::-1]
    idcg = _dcg(ideal, k_eff)
    if idcg <= 0:
        return float("nan")
    return _dcg(ordered, k_eff) / idcg


def precision_at_k(
    score: pd.Series,
    y_int: pd.Series,
    k: int = 10,
) -> float:
    """Precision@k for 'top growth': fraction of top-k scores in top-k y_int."""
    df = pd.concat([score.rename("score"), y_int.rename("y")], axis=1).dropna()
    if df.empty:
        return float("nan")
    k_eff = min(k, len(df))
    top_score = set(df.sort_values("score", ascending=False).head(k_eff).index)
    top_y = set(df.sort_values("y", ascending=False).head(k_eff).index)
    return float(len(top_score & top_y) / k_eff)


def auc_ext(score: pd.Series, y_ext: pd.Series) -> float:
    """ROC AUC treating ``score`` as entry propensity vs binary ``y_ext``."""
    df = pd.concat([score.rename("score"), y_ext.rename("y")], axis=1).dropna()
    if df.empty or df["y"].nunique() < 2:
        return float("nan")
    return float(roc_auc_score(df["y"].to_numpy(dtype=float), df["score"].to_numpy(dtype=float)))


def evaluate_ranking(
    score: pd.Series,
    *,
    y_int: pd.Series | None = None,
    y_ext: pd.Series | None = None,
    k_ndcg: tuple[int, ...] = (5, 10),
    k_precision: int = 10,
    gain: GainMode = "rank",
) -> dict[str, float]:
    """Bundle of ranking/classification metrics for one origin-year slice."""
    out: dict[str, float] = {}
    if y_int is not None:
        out["spearman"] = spearman_corr(score, y_int)
        out["kendall"] = kendall_corr(score, y_int)
        for k in k_ndcg:
            out[f"ndcg@{k}"] = ndcg_at_k(score, y_int, k=k, gain=gain)
        out[f"precision@{k_precision}"] = precision_at_k(score, y_int, k=k_precision)
    if y_ext is not None:
        out["auc"] = auc_ext(score, y_ext)
    return out
