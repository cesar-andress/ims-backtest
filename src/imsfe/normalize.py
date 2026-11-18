"""Cross-section normalisation methods for destination scores (SPEC §3.4)."""

from __future__ import annotations

from typing import Literal

import numpy as np
import pandas as pd
from scipy.stats import rankdata

NormalizationId = Literal["ratio_legacy", "minmax", "zscore", "rank", "log_minmax"]
Direction = Literal["benefit", "cost"]

# Midpoint used when a column is constant under a [0, 10] scale.
_CONSTANT_MID_10 = 5.0


def _as_float(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").astype(float)


def normalize_ratio_legacy(series: pd.Series, direction: Direction) -> pd.Series:
    """Legacy ratio formula (7): benefit ``y/max*10``, cost ``min/y*10``.

    Reproduces ``legacy.ratio_normalize`` when all cost values are strictly
    positive. Non-positive cost values are left as NaN (cannot apply min/y).
    If a benefit column has max == 0, returns zeros. If a cost column has no
    positive values, returns all-NaN.
    """
    s = _as_float(series)
    if direction == "benefit":
        vmax = float(s.max(skipna=True)) if s.notna().any() else float("nan")
        if not np.isfinite(vmax) or vmax == 0.0:
            return pd.Series(0.0, index=s.index, dtype=float)
        return s / vmax * 10.0
    # cost
    pos = s > 0
    if not bool(pos.any()):
        return pd.Series(np.nan, index=s.index, dtype=float)
    vmin = float(s.loc[pos].min())
    out = pd.Series(np.nan, index=s.index, dtype=float)
    out.loc[pos] = vmin / s.loc[pos] * 10.0
    return out


def normalize_minmax(series: pd.Series, direction: Direction) -> pd.Series:
    """Min-max to [0, 10]; constant columns map to 5."""
    s = _as_float(series)
    vmin = float(s.min(skipna=True)) if s.notna().any() else float("nan")
    vmax = float(s.max(skipna=True)) if s.notna().any() else float("nan")
    if not np.isfinite(vmin) or not np.isfinite(vmax):
        return pd.Series(np.nan, index=s.index, dtype=float)
    span = vmax - vmin
    if span == 0.0:
        return pd.Series(_CONSTANT_MID_10, index=s.index, dtype=float)
    if direction == "benefit":
        return (s - vmin) / span * 10.0
    return (vmax - s) / span * 10.0


def normalize_zscore(series: pd.Series, direction: Direction) -> pd.Series:
    """Z-score; cost criteria are sign-flipped so higher is always better."""
    s = _as_float(series)
    mu = float(s.mean(skipna=True)) if s.notna().any() else float("nan")
    sigma = float(s.std(skipna=True, ddof=1)) if s.notna().sum() > 1 else 0.0
    if not np.isfinite(mu):
        return pd.Series(np.nan, index=s.index, dtype=float)
    if sigma == 0.0 or not np.isfinite(sigma):
        z = pd.Series(0.0, index=s.index, dtype=float)
    else:
        z = (s - mu) / sigma
    return z if direction == "benefit" else -z


def normalize_rank(series: pd.Series, direction: Direction) -> pd.Series:
    """Average ranks scaled to (0, 10]; higher is better."""
    s = _as_float(series)
    n = int(s.notna().sum())
    if n == 0:
        return pd.Series(np.nan, index=s.index, dtype=float)
    values = s.to_numpy(dtype=float)
    # rankdata puts NaN last with nan_policy; mask manually
    out = np.full(len(s), np.nan, dtype=float)
    mask = np.isfinite(values)
    if direction == "benefit":
        ranks = rankdata(values[mask], method="average")
    else:
        ranks = rankdata(-values[mask], method="average")
    out[mask] = ranks / n * 10.0
    return pd.Series(out, index=s.index, dtype=float)


def normalize_log_minmax(series: pd.Series, direction: Direction) -> pd.Series:
    """Shift to positive, log, then min-max to [0, 10] with direction."""
    s = _as_float(series)
    if not s.notna().any():
        return pd.Series(np.nan, index=s.index, dtype=float)
    vmin = float(s.min(skipna=True))
    shifted = s - vmin + 1e-12
    logged = np.log(shifted)
    return normalize_minmax(pd.Series(logged, index=s.index), direction)


_DISPATCH = {
    "ratio_legacy": normalize_ratio_legacy,
    "minmax": normalize_minmax,
    "zscore": normalize_zscore,
    "rank": normalize_rank,
    "log_minmax": normalize_log_minmax,
}


def normalize_column(
    series: pd.Series,
    direction: Direction,
    method: NormalizationId,
) -> pd.Series:
    """Normalise one criterion column."""
    if method not in _DISPATCH:
        raise ValueError(f"Unknown normalisation method: {method}")
    return _DISPATCH[method](series, direction)


def normalize_matrix(
    raw: pd.DataFrame,
    directions: dict[str, Direction],
    method: NormalizationId,
) -> pd.DataFrame:
    """Normalise every column of a destination cross-section."""
    out = pd.DataFrame(index=raw.index)
    for col in raw.columns:
        if col not in directions:
            raise KeyError(f"Missing direction for column {col}")
        out[col] = normalize_column(raw[col], directions[col], method)
    return out


def normalize_panel_group(
    group: pd.DataFrame,
    columns: list[str],
    directions: dict[str, Direction],
    method: NormalizationId,
) -> pd.DataFrame:
    """Normalise a single (origin, year) destination cross-section."""
    return normalize_matrix(group[columns], directions, method)
