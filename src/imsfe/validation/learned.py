"""Fit simplex-constrained weights maximizing mean NDCG@10 on training years.

Determinism
-----------
- Fixed seed and a fixed list of multi-start offsets (no RNG during starts).
- L-BFGS-B with fixed solver options.
- Among successful starts, pick the lowest objective; ties broken by
  lexicographically smaller parameter vector.
- Variables with no finite data in the training window receive weight exactly 0
  and are listed in the returned info / comparison table.
- Published fits force the CPU path (no CUDA dependency).
"""

from __future__ import annotations

import os
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

# Deterministic offset patterns (broadcast / tiled to theta length).
_START_PATTERNS: tuple[np.ndarray, ...] = (
    np.array([0.0]),
    np.array([0.35, -0.35]),
    np.array([-0.5, 0.25, 0.25]),
    np.array([0.6, -0.2, -0.2, -0.2]),
    np.array([-0.4, 0.4, -0.15, 0.15, 0.0]),
)


def _force_cpu() -> None:
    """Ensure published learned-weight fits do not depend on CUDA."""
    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")


def variables_with_train_data(
    panel: pd.DataFrame,
    train_years: list[int],
    variables: VariablesConfig,
) -> tuple[list[str], list[str]]:
    """Return (present_ids, absent_ids) based on any finite value in train years."""
    train = panel.loc[panel["year"].isin(train_years)]
    present: list[str] = []
    absent: list[str] = []
    for v in variables.variables:
        if v.id in train.columns and train[v.id].notna().any():
            present.append(v.id)
        else:
            absent.append(v.id)
    return present, absent


def _pack_params(weights: Weights) -> tuple[np.ndarray, list[str], dict[str, list[str]]]:
    """Free logits: factor logits + within each factor; softmax at unpack."""
    factor_names = list(weights.factors.index)
    structure = {f: list(weights.variables_within[f].index) for f in factor_names}
    parts: list[float] = []
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


def _expand_start(pattern: np.ndarray, n: int) -> np.ndarray:
    if pattern.size == 1 and float(pattern[0]) == 0.0:
        return np.zeros(n, dtype=float)
    reps = int(np.ceil(n / pattern.size))
    return np.tile(pattern, reps)[:n].astype(float)


def _zero_absent(weights: Weights, absent: list[str], all_ids: list[str]) -> Weights:
    """Set absent variables to weight 0 and renormalise over present ones."""
    if not absent:
        return weights
    present = [v for v in all_ids if v not in absent]
    if not present:
        raise RuntimeError("No variables with training-window data for learned weights")
    return weights.restrict(present)


def fit_learned_weights(
    panel: pd.DataFrame,
    train_years: list[int],
    *,
    horizon: int = 1,
    normalization: str = "minmax",
    method: str = "wsm",
    n_restarts: int = 5,
    seed: int = 42,  # retained for API compatibility; starts are fixed
    variables: VariablesConfig | None = None,
    maxiter: int = 80,
    force_cpu: bool = True,
) -> tuple[Weights, dict[str, Any]]:
    """Maximise mean NDCG@10 over training origin-years (softmax + L-BFGS-B)."""
    del seed  # fixed starts; seed kept so callers need not change
    if force_cpu:
        _force_cpu()

    variables = variables or load_variables()
    all_ids = [v.id for v in variables.variables]
    present, absent = variables_with_train_data(panel, train_years, variables)

    init_full = weights_expert_mean(variables)
    init = _zero_absent(init_full, absent, all_ids)
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

    n_starts = max(1, int(n_restarts))
    starts: list[np.ndarray] = []
    for i in range(n_starts):
        pattern = _START_PATTERNS[i % len(_START_PATTERNS)]
        starts.append(theta0 + _expand_start(pattern, theta0.size))

    best_theta = starts[0].copy()
    best_val = float(objective(best_theta))
    for th in starts:
        res = minimize(
            objective,
            th,
            method="L-BFGS-B",
            options={
                "maxiter": maxiter,
                "ftol": 1e-6,
                "gtol": 1e-6,
                "maxfun": maxiter * 20,
            },
        )
        cand_val = float(res.fun) if np.isfinite(res.fun) else float("inf")
        cand_theta = np.asarray(res.x, dtype=float)
        if cand_val < best_val - 1e-15:
            best_val = cand_val
            best_theta = cand_theta
        elif abs(cand_val - best_val) <= 1e-15:
            # Deterministic tie-break: lexicographically smaller theta
            if tuple(cand_theta.tolist()) < tuple(best_theta.tolist()):
                best_theta = cand_theta
                best_val = cand_val

    learned_present = _unpack_params(best_theta, factor_names, structure)
    # Rebuild full flat vector with exact zeros for absent variables
    flat_present = learned_present.flat()
    flat_full = pd.Series(0.0, index=all_ids, dtype=float)
    for vid, w in flat_present.items():
        if vid in flat_full.index:
            flat_full.loc[vid] = float(w)
    # Hierarchical form via restrict-inverse: put absent at 0 within factors
    fw_parts: dict[str, float] = {}
    within: dict[str, pd.Series] = {}
    for factor in {v.factor for v in variables.variables}:
        vids = [v.id for v in variables.variables if v.factor == factor]
        masses = []
        for vid in vids:
            masses.append(float(flat_full.get(vid, 0.0)))
        s = pd.Series(masses, index=vids, dtype=float)
        factor_mass = float(s.sum())
        if factor_mass <= 0:
            # Keep factor with uniform-zero-within (all absent) — drop factor
            continue
        fw_parts[factor] = factor_mass
        within[factor] = s / factor_mass
    fw = pd.Series(fw_parts, dtype=float)
    fw = fw / fw.sum()
    learned = Weights(factors=fw, variables_within=within, scheme="learned")
    set_learned_weights(learned)

    expert = weights_expert_mean(variables)
    equal = weights_equal(variables)
    compare = pd.DataFrame(
        {
            "variable": all_ids,
            "learned": [float(flat_full.get(v, 0.0)) for v in all_ids],
            "expert_mean": expert.flat().reindex(all_ids).to_numpy(),
            "equal": equal.flat().reindex(all_ids).to_numpy(),
            "has_train_data": [v in present for v in all_ids],
        }
    )
    info = {
        "train_ndcg@10": -best_val,
        "n_train_groups": len(groups),
        "n_restarts": n_starts,
        "comparison": compare,
        "factor_years": list(train_years),
        "horizon": horizon,
        "absent_variables": list(absent),
        "present_variables": list(present),
        "force_cpu": force_cpu,
    }
    return learned, info
