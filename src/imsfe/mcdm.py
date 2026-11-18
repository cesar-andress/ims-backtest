"""Multi-criteria decision methods (WSM, TOPSIS, VIKOR, PROMETHEE II)."""

from __future__ import annotations

from typing import Literal

import numpy as np
import pandas as pd
from pymcdm.methods import PROMETHEE_II, TOPSIS, VIKOR

from imsfe.weights import Weights

McdmId = Literal["wsm", "topsis", "vikor", "promethee_ii"]
Direction = Literal["benefit", "cost"]


def _types_vector(columns: list[str], directions: dict[str, Direction]) -> np.ndarray:
    return np.array(
        [1 if directions[c] == "benefit" else -1 for c in columns],
        dtype=int,
    )


def hierarchical_wsm(
    normalized: pd.DataFrame,
    weights: Weights,
) -> pd.Series:
    """Hierarchical WSM: variables → factors → score (legacy IMSFE aggregation).

    Expects ``normalized`` columns to already respect direction (higher = better),
    as produced by ``normalize_matrix``.
    """
    factor_scores = pd.DataFrame(index=normalized.index, dtype=float)
    for factor, fw_vars in weights.variables_within.items():
        cols = [c for c in fw_vars.index if c in normalized.columns]
        if not cols:
            continue
        w = fw_vars.loc[cols].astype(float)
        w = w / w.sum()
        factor_scores[factor] = normalized[cols].mul(w, axis=1).sum(axis=1)
    fw = weights.factors.reindex(factor_scores.columns).astype(float).fillna(0.0)
    if float(fw.sum()) <= 0:
        raise ValueError("No overlapping factors between weights and matrix")
    fw = fw / fw.sum()
    scores = factor_scores.mul(fw, axis=1).sum(axis=1)
    scores.name = "score"
    return scores


def _flat_weights_array(weights: Weights, columns: list[str]) -> np.ndarray:
    flat = weights.flat(columns)
    arr = flat.reindex(columns).fillna(0.0).to_numpy(dtype=float)
    total = arr.sum()
    if total <= 0:
        raise ValueError("flat weights sum to zero")
    return arr / total


def score_topsis(
    matrix: pd.DataFrame,
    weights: Weights,
    directions: dict[str, Direction],
) -> pd.Series:
    """TOPSIS via pymcdm (higher score = better). Matrix is raw values."""
    cols = list(matrix.columns)
    w = _flat_weights_array(weights, cols)
    types = _types_vector(cols, directions)
    pref = TOPSIS()(matrix.to_numpy(dtype=float), w, types)
    return pd.Series(pref, index=matrix.index, name="score", dtype=float)


def score_vikor(
    matrix: pd.DataFrame,
    weights: Weights,
    directions: dict[str, Direction],
    *,
    v: float = 0.5,
) -> pd.Series:
    """VIKOR via pymcdm. Returns ``-Q`` so that higher is better."""
    cols = list(matrix.columns)
    w = _flat_weights_array(weights, cols)
    types = _types_vector(cols, directions)
    q = VIKOR(v=v)(matrix.to_numpy(dtype=float), w, types)
    return pd.Series(-np.asarray(q, dtype=float), index=matrix.index, name="score")


def score_promethee_ii(
    matrix: pd.DataFrame,
    weights: Weights,
    directions: dict[str, Direction],
) -> pd.Series:
    """PROMETHEE II with the usual preference function (pymcdm)."""
    cols = list(matrix.columns)
    w = _flat_weights_array(weights, cols)
    types = _types_vector(cols, directions)
    phi = PROMETHEE_II("usual")(matrix.to_numpy(dtype=float), w, types)
    return pd.Series(np.asarray(phi, dtype=float), index=matrix.index, name="score")


def score(
    matrix: pd.DataFrame,
    weights: Weights,
    directions: dict[str, Direction],
    method: McdmId,
    *,
    normalized: pd.DataFrame | None = None,
) -> pd.Series:
    """Common interface: return a score Series (higher = better).

    - ``wsm`` uses ``normalized`` (direction already applied).
    - ``topsis`` / ``vikor`` / ``promethee_ii`` use the raw ``matrix`` plus
      benefit/cost ``directions`` (pymcdm applies its own internal scaling).
    """
    if method == "wsm":
        if normalized is None:
            raise ValueError("WSM requires a pre-normalised matrix")
        return hierarchical_wsm(normalized, weights)
    if method == "topsis":
        return score_topsis(matrix, weights, directions)
    if method == "vikor":
        return score_vikor(matrix, weights, directions)
    if method == "promethee_ii":
        return score_promethee_ii(matrix, weights, directions)
    raise ValueError(f"Unknown MCDM method: {method}")
