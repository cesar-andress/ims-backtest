"""Fit simplex-constrained weights maximizing mean NDCG@10 on training years."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import softmax

from imsfe.config import VariablesConfig, load_variables
from imsfe.validation.backtest import metrics_for_scores, score_slice
from imsfe.weights import (
    Weights,
    set_learned_weights,
    weights_equal,
    weights_expert_mean,
)


def _pack_params(weights: Weights) -> tuple[np.ndarray, list[str], dict[str, list[str]]]:
    """Free logits: factor logits (K-1 free via softmax) + within each factor."""
    # We optimise all factor logits and all within-factor logits, then softmax.
    factor_names = list(weights.factors.index)
    structure = {f: list(weights.variables_within[f].index) for f in factor_names}
    parts: list[float] = []
    # factor logits initialised from log(mean)
    parts.extend(np.log(np.clip(weights.factors.reindex(factor_names).to_numpy(), 1e-12, None)))
    for f in factor_names:
        vw = weights.variables_within[f].reindex(structure[f]).to_numpy(dtype=float)
        parts.extend(np.log(np.clip(vw, 1e-12, None)))
    return np.asarray(parts, dtype=float), factor_names, structure


def _unpack_params(
    theta: np.ndarray,
    factor_names: list[str],
    structure: dict[str, list[str]],
) -> Weights:
    k = len(factor_names)
    f_logits = theta[:k]
    fw = pd.Series(softmax(f_logits), index=factor_names, dtype=float)
    within: dict[str, pd.Series] = {}
    cursor = k
    for f in factor_names:
        n = len(structure[f])
        logits = theta[cursor : cursor + n]
        cursor += n
        within[f] = pd.Series(softmax(logits), index=structure[f], dtype=float)
    return Weights(factors=fw, variables_within=within, scheme="learned")


def fit_learned_weights(
    panel: pd.DataFrame,
    train_years: list[int],
    *,
    horizon: int = 1,
    normalization: str = "minmax",
    method: str = "wsm",
    n_restarts: int = 5,
    seed: int = 42,
    variables: VariablesConfig | None = None,
    maxiter: int = 80,
) -> tuple[Weights, dict[str, Any]]:
    """Maximise mean NDCG@10 over training origin-years (softmax + L-BFGS-B)."""
    variables = variables or load_variables()
    init = weights_expert_mean(variables)
    theta0, factor_names, structure = _pack_params(init)
    train = panel.loc[panel["year"].isin(train_years)]
    groups = list(train.groupby(["iso3_o", "year"], sort=True))
    if not groups:
        raise RuntimeError("No training origin-year groups for learned weights")

    def objective(theta: np.ndarray) -> float:
        w = _unpack_params(theta, factor_names, structure)
        vals = []
        for (_, _), group in groups:
            sc = score_slice(
                group,
                variables=variables,
                normalization=normalization,
                method=method,
                weights=w,
            )
            if sc.empty:
                continue
            mets = metrics_for_scores(sc, group, horizon=horizon)
            v = mets.get("ndcg@10", float("nan"))
            if np.isfinite(v):
                vals.append(v)
        if not vals:
            return 0.0
        return -float(np.mean(vals))

    rng = np.random.default_rng(seed)
    best_theta = theta0.copy()
    best_val = objective(theta0)
    restarts = [theta0]
    for _ in range(max(0, n_restarts - 1)):
        restarts.append(theta0 + rng.normal(0.0, 0.5, size=theta0.shape))

    for th in restarts:
        res = minimize(
            objective,
            th,
            method="L-BFGS-B",
            options={"maxiter": maxiter, "ftol": 1e-6},
        )
        if res.success or np.isfinite(res.fun):
            if res.fun < best_val:
                best_val = float(res.fun)
                best_theta = np.asarray(res.x, dtype=float)

    learned = _unpack_params(best_theta, factor_names, structure)
    set_learned_weights(learned)
    expert = weights_expert_mean(variables)
    equal = weights_equal(variables)
    compare = pd.DataFrame(
        {
            "variable": list(learned.flat().index),
            "learned": learned.flat().to_numpy(),
            "expert_mean": expert.flat().reindex(learned.flat().index).to_numpy(),
            "equal": equal.flat().reindex(learned.flat().index).to_numpy(),
        }
    )
    info = {
        "train_ndcg@10": -best_val,
        "n_train_groups": len(groups),
        "n_restarts": n_restarts,
        "comparison": compare,
        "factor_years": list(train_years),
        "horizon": horizon,
    }
    return learned, info
