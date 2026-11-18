"""Stochastic multicriteria acceptability analysis over weight uncertainty.

Dirichlet concentration (method of moments)
------------------------------------------
Sample ``w ~ Dir(κ μ)`` with mean vector ``μ`` (``∑ μ_i = 1``, ``μ_i > 0``).
Marginal variances are

    Var(w_i) = μ_i (1 − μ_i) / (κ + 1).

Given an observed expert SD ``σ_i`` for component ``i``,

    κ_i = μ_i (1 − μ_i) / σ_i² − 1.

We take ``κ = median{κ_i : κ_i > 0}`` (scaled by ``dispersion_scale``) and set
``α = κ μ``. When every ``σ_i → 0`` or ``dispersion_scale = 0``, sampling
collapses to the point mass at ``μ`` (deterministic ranking).

Alternative mode ``box``: draw each weight independently from Uniform[min, max]
using the expert ranges, then renormalise to the simplex.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

import numpy as np
import pandas as pd

from imsfe.build.descriptives import outputs_tables_dir
from imsfe.build.panel import processed_dir
from imsfe.config import Settings, VariablesConfig, load_settings, load_variables
from imsfe.mcdm import score
from imsfe.normalize import normalize_matrix
from imsfe.run_experiments import _directions, _feature_columns, _prepare_slice
from imsfe.weights import (
    LEGACY_FACTOR_MAP,
    Weights,
    load_expert_yaml,
    weights_expert_mean,
)

SamplingMode = Literal["dirichlet", "box"]


def dirichlet_concentration(
    mu: np.ndarray,
    sigma: np.ndarray,
    *,
    dispersion_scale: float = 1.0,
    min_kappa: float = 1.0,
    max_kappa: float = 1e8,
) -> float:
    """MoM concentration ``κ`` for ``Dir(κ μ)`` given component SDs ``sigma``.

    ``dispersion_scale`` multiplies all ``σ`` (0 ⇒ infinite concentration).
    """
    mu = np.asarray(mu, dtype=float)
    sigma = np.asarray(sigma, dtype=float) * float(dispersion_scale)
    if dispersion_scale <= 0 or not np.isfinite(sigma).any() or np.nanmax(sigma) <= 0:
        return float(max_kappa)
    kappas = []
    for m, s in zip(mu, sigma, strict=False):
        if not np.isfinite(s) or s <= 0 or m <= 0 or m >= 1:
            continue
        k = m * (1.0 - m) / (s**2) - 1.0
        if np.isfinite(k) and k > 0:
            kappas.append(k)
    if not kappas:
        return float(max_kappa)
    kappa = float(np.median(kappas))
    return float(np.clip(kappa, min_kappa, max_kappa))


def sample_dirichlet(
    mu: np.ndarray,
    sigma: np.ndarray,
    n: int,
    rng: np.random.Generator,
    *,
    dispersion_scale: float = 1.0,
) -> np.ndarray:
    """Draw ``n`` weight vectors from ``Dir(κ μ)``; shape ``(n, len(mu))``."""
    mu = np.asarray(mu, dtype=float)
    mu = mu / mu.sum()
    kappa = dirichlet_concentration(mu, sigma, dispersion_scale=dispersion_scale)
    if kappa >= 1e7 or dispersion_scale <= 0:
        return np.repeat(mu.reshape(1, -1), n, axis=0)
    alpha = np.clip(kappa * mu, 1e-12, None)
    return rng.dirichlet(alpha, size=n)


def sample_box(
    lows: np.ndarray,
    highs: np.ndarray,
    n: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """Uniform draws in ``[low, high]`` per component, then row-renormalise."""
    lows = np.asarray(lows, dtype=float)
    highs = np.asarray(highs, dtype=float)
    u = rng.uniform(lows, highs, size=(n, len(lows)))
    u = np.clip(u, 1e-12, None)
    return u / u.sum(axis=1, keepdims=True)


@dataclass
class ExpertWeightStats:
    """Means / SDs / bounds aligned with a ``Weights`` hierarchy."""

    factor_names: list[str]
    factor_mu: np.ndarray
    factor_sigma: np.ndarray
    factor_min: np.ndarray
    factor_max: np.ndarray
    within: dict[str, dict[str, np.ndarray]]  # factor -> {names, mu, sigma, min, max}
    notes: tuple[str, ...] = field(default_factory=tuple)


def build_expert_stats(
    center: Weights,
    *,
    expert_path: Path | None = None,
    default_cv: float = 0.25,
) -> ExpertWeightStats:
    """Attach expert SD/min/max to the centre weights (legacy map when possible)."""
    expert = load_expert_yaml(expert_path)
    leg_f = expert.get("factors", {})
    leg_v = expert.get("variables", {})
    notes: list[str] = []

    factor_names = list(center.factors.index)
    mu = center.factors.reindex(factor_names).to_numpy(dtype=float)
    sigma = np.zeros(len(factor_names), dtype=float)
    mins = np.zeros(len(factor_names), dtype=float)
    maxs = np.zeros(len(factor_names), dtype=float)
    for i, f in enumerate(factor_names):
        legacy = LEGACY_FACTOR_MAP.get(f)
        if legacy and legacy in leg_f:
            sigma[i] = float(leg_f[legacy]["sd"])
            mins[i] = float(leg_f[legacy]["min"])
            maxs[i] = float(leg_f[legacy]["max"])
        else:
            notes.append(f"factor {f}: no legacy SD; using default_cv={default_cv}")
    for i, _f in enumerate(factor_names):
        if sigma[i] > 0:
            continue
        sigma[i] = default_cv * float(mu[i])
        mins[i] = max(1e-6, float(mu[i]) - 2 * sigma[i])
        maxs[i] = min(1.0, float(mu[i]) + 2 * sigma[i])
        if maxs[i] <= mins[i]:
            maxs[i] = mins[i] + 1e-6

    within: dict[str, dict[str, np.ndarray]] = {}
    for factor, vw in center.variables_within.items():
        names = list(vw.index)
        vmu = vw.reindex(names).to_numpy(dtype=float)
        vsig = np.zeros(len(names), dtype=float)
        vmin = np.zeros(len(names), dtype=float)
        vmax = np.zeros(len(names), dtype=float)
        for j, vid in enumerate(names):
            if vid in leg_v:
                vsig[j] = float(leg_v[vid]["sd"])
                vmin[j] = float(leg_v[vid]["min"])
                vmax[j] = float(leg_v[vid]["max"])
            else:
                vsig[j] = default_cv * vmu[j]
                vmin[j] = max(1e-6, vmu[j] - 2 * vsig[j])
                vmax[j] = min(1.0, vmu[j] + 2 * vsig[j])
                notes.append(
                    f"{vid}: no legacy SD; default_cv={default_cv} inside {factor}"
                )
            if vmax[j] <= vmin[j]:
                vmax[j] = vmin[j] + 1e-6
        within[str(factor)] = {
            "names": np.array(names, dtype=object),
            "mu": vmu,
            "sigma": vsig,
            "min": vmin,
            "max": vmax,
        }

    return ExpertWeightStats(
        factor_names=factor_names,
        factor_mu=mu,
        factor_sigma=sigma,
        factor_min=mins,
        factor_max=maxs,
        within=within,
        notes=tuple(notes),
    )


def sample_hierarchical_weights(
    stats: ExpertWeightStats,
    n_samples: int,
    rng: np.random.Generator,
    *,
    mode: SamplingMode = "dirichlet",
    dispersion_scale: float = 1.0,
    columns: list[str] | None = None,
) -> tuple[np.ndarray, list[str]]:
    """Sample flat variable weights; returns ``(n_samples, n_vars)`` and names."""
    if mode == "dirichlet":
        f_w = sample_dirichlet(
            stats.factor_mu,
            stats.factor_sigma,
            n_samples,
            rng,
            dispersion_scale=dispersion_scale,
        )
    else:
        f_w = sample_box(stats.factor_min, stats.factor_max, n_samples, rng)

    # Within-factor samples
    pieces: list[np.ndarray] = []
    names: list[str] = []
    for i, factor in enumerate(stats.factor_names):
        block = stats.within[factor]
        vnames = [str(x) for x in block["names"]]
        if mode == "dirichlet":
            v_w = sample_dirichlet(
                block["mu"],
                block["sigma"],
                n_samples,
                rng,
                dispersion_scale=dispersion_scale,
            )
        else:
            v_w = sample_box(block["min"], block["max"], n_samples, rng)
        # flat contribution: factor_w * within_w
        pieces.append(f_w[:, i : i + 1] * v_w)
        names.extend(vnames)

    flat = np.concatenate(pieces, axis=1)
    if columns is not None:
        idx = {n: j for j, n in enumerate(names)}
        keep = [c for c in columns if c in idx]
        flat = flat[:, [idx[c] for c in keep]]
        # renormalise
        flat = flat / np.clip(flat.sum(axis=1, keepdims=True), 1e-15, None)
        names = keep
    else:
        flat = flat / np.clip(flat.sum(axis=1, keepdims=True), 1e-15, None)
    return flat, names


def ranks_from_scores(scores: np.ndarray) -> np.ndarray:
    """Ranks (1=best) for score matrix ``(n_alt, n_samples)``; higher score better."""
    n_alt, n_samples = scores.shape
    order = np.argsort(-scores, axis=0, kind="mergesort")
    ranks = np.empty((n_alt, n_samples), dtype=int)
    rank_vals = np.arange(1, n_alt + 1, dtype=int).reshape(-1, 1)
    sample_idx = np.broadcast_to(np.arange(n_samples, dtype=int), order.shape)
    ranks[order, sample_idx] = rank_vals
    return ranks


def rank_acceptability(ranks: np.ndarray) -> np.ndarray:
    """``b[j, r-1] = P(alt j has rank r)``; ``ranks`` shape ``(n_alt, n_samples)``."""
    n_alt, n_samples = ranks.shape
    b = np.zeros((n_alt, n_alt), dtype=float)
    for r in range(1, n_alt + 1):
        b[:, r - 1] = (ranks == r).sum(axis=1) / n_samples
    return b


@dataclass
class SMAAResult:
    alternatives: list[str]
    criteria: list[str]
    ranks: np.ndarray  # (n_alt, n_samples)
    scores: np.ndarray  # (n_alt, n_samples)
    acceptability: np.ndarray  # (n_alt, n_alt)
    weight_samples: np.ndarray  # (n_samples, n_crit)
    central_weights: pd.Series
    deterministic_scores: pd.Series
    deterministic_ranks: pd.Series
    mode: str
    n_samples: int
    seed: int
    dispersion_scale: float
    notes: tuple[str, ...] = ()

    def p_top_k(self, k: int) -> pd.Series:
        p = (self.ranks <= k).mean(axis=1)
        return pd.Series(p, index=self.alternatives, name=f"p_top_{k}")

    def rank_interval(self, q_low: float = 0.05, q_high: float = 0.95) -> pd.DataFrame:
        low = np.quantile(self.ranks, q_low, axis=1)
        high = np.quantile(self.ranks, q_high, axis=1)
        return pd.DataFrame(
            {
                "rank_q05": low,
                "rank_q95": high,
            },
            index=self.alternatives,
        )


def run_smaa_wsm(
    normalized: pd.DataFrame,
    center: Weights,
    stats: ExpertWeightStats,
    *,
    n_samples: int = 10_000,
    seed: int = 42,
    mode: SamplingMode = "dirichlet",
    dispersion_scale: float = 1.0,
) -> SMAAResult:
    """Vectorised SMAA for hierarchical WSM on a pre-normalised matrix."""
    rng = np.random.default_rng(seed)
    center_r = center.restrict(list(normalized.columns))
    # Rebuild stats restricted to available columns via sampling filter
    cols = list(normalized.columns)
    W, crit = sample_hierarchical_weights(
        stats,
        n_samples,
        rng,
        mode=mode,
        dispersion_scale=dispersion_scale,
        columns=cols,
    )
    # Align normalized columns to crit order
    N = normalized.loc[:, crit].to_numpy(dtype=float)  # (n_alt, n_crit)
    scores = N @ W.T  # (n_alt, n_samples)
    ranks = ranks_from_scores(scores)
    b = rank_acceptability(ranks)

    det = score(normalized, center_r, {}, "wsm", normalized=normalized)
    det_ranks = det.rank(ascending=False, method="min").astype(int)

    central = pd.Series(W.mean(axis=0), index=crit, dtype=float)
    central = central / central.sum()

    return SMAAResult(
        alternatives=list(normalized.index.astype(str)),
        criteria=crit,
        ranks=ranks,
        scores=scores,
        acceptability=b,
        weight_samples=W,
        central_weights=central,
        deterministic_scores=det,
        deterministic_ranks=det_ranks,
        mode=mode,
        n_samples=n_samples,
        seed=seed,
        dispersion_scale=dispersion_scale,
        notes=stats.notes,
    )


def run_smaa_generic(
    raw: pd.DataFrame,
    normalized: pd.DataFrame,
    directions: dict[str, str],
    center: Weights,
    stats: ExpertWeightStats,
    method: str,
    *,
    n_samples: int = 10_000,
    seed: int = 42,
    mode: SamplingMode = "dirichlet",
    dispersion_scale: float = 1.0,
) -> SMAAResult:
    """SMAA for non-WSM methods (loop over samples; still seeded)."""
    if method == "wsm":
        return run_smaa_wsm(
            normalized,
            center,
            stats,
            n_samples=n_samples,
            seed=seed,
            mode=mode,
            dispersion_scale=dispersion_scale,
        )
    rng = np.random.default_rng(seed)
    center_r = center.restrict(list(normalized.columns))
    cols = list(normalized.columns)
    W, crit = sample_hierarchical_weights(
        stats,
        n_samples,
        rng,
        mode=mode,
        dispersion_scale=dispersion_scale,
        columns=cols,
    )
    alts = list(normalized.index.astype(str))
    score_mat = np.zeros((len(alts), n_samples), dtype=float)
    raw_m = raw.loc[:, crit]
    norm_m = normalized.loc[:, crit]
    dirs = {c: directions[c] for c in crit}
    for s in range(n_samples):
        # Build Weights from flat sample via single dummy factor
        flat = pd.Series(W[s], index=crit, dtype=float)
        # Collapse to hierarchical by original factors in center_r
        within: dict[str, pd.Series] = {}
        fmass: dict[str, float] = {}
        for factor, vw in center_r.variables_within.items():
            ids = [v for v in vw.index if v in flat.index]
            if not ids:
                continue
            sub = flat.loc[ids].clip(lower=0)
            mass = float(sub.sum())
            if mass <= 0:
                continue
            within[factor] = sub / mass
            fmass[factor] = mass
        fw = pd.Series(fmass, dtype=float)
        fw = fw / fw.sum()
        wobj = Weights(factors=fw, variables_within=within, scheme="smaa_sample")
        sc = score(raw_m, wobj, dirs, method, normalized=norm_m)  # type: ignore[arg-type]
        score_mat[:, s] = sc.reindex(normalized.index).to_numpy(dtype=float)

    ranks = ranks_from_scores(score_mat)
    b = rank_acceptability(ranks)
    det = score(raw_m, center_r, dirs, method, normalized=norm_m)  # type: ignore[arg-type]
    det_ranks = det.rank(ascending=False, method="min").astype(int)
    central = pd.Series(W.mean(axis=0), index=crit, dtype=float)
    central = central / central.sum()
    return SMAAResult(
        alternatives=alts,
        criteria=crit,
        ranks=ranks,
        scores=score_mat,
        acceptability=b,
        weight_samples=W,
        central_weights=central,
        deterministic_scores=det,
        deterministic_ranks=det_ranks,
        mode=mode,
        n_samples=n_samples,
        seed=seed,
        dispersion_scale=dispersion_scale,
        notes=stats.notes,
    )


def prepare_origin_year_matrices(
    panel: pd.DataFrame,
    origin: str,
    year: int,
    *,
    normalization: str = "minmax",
    variables: VariablesConfig | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, str], Weights]:
    """Raw complete matrix, normalised matrix, directions, restricted expert weights."""
    variables = variables or load_variables()
    group = panel.loc[(panel["iso3_o"] == origin) & (panel["year"] == year)]
    if group.empty:
        raise ValueError(f"No panel rows for {origin}/{year}")
    cols = _feature_columns(variables)
    directions = _directions(variables)
    dest = group.set_index("iso3_d")
    complete, usable = _prepare_slice(dest[cols], cols)
    if complete.empty or len(complete) < 2:
        raise ValueError(f"Insufficient complete destinations for {origin}/{year}")
    dirs = {c: directions[c] for c in usable}
    normalized = normalize_matrix(complete, dirs, normalization)  # type: ignore[arg-type]
    center = weights_expert_mean(variables).restrict(usable)
    return complete, normalized, dirs, center


def build_t8(result: SMAAResult, top_n: int = 10) -> pd.DataFrame:
    """COL-style table: score, rank, P(top-1), P(top-5), 90% rank interval."""
    order = result.deterministic_ranks.sort_values().index.tolist()[:top_n]
    interval = result.rank_interval(0.05, 0.95)
    rows = []
    p1 = result.p_top_k(1)
    p5 = result.p_top_k(5)
    for dest in order:
        rows.append(
            {
                "dest": dest,
                "score": float(result.deterministic_scores.loc[dest]),
                "rank": int(result.deterministic_ranks.loc[dest]),
                "p_top1": float(p1.loc[dest]),
                "p_top5": float(p5.loc[dest]),
                "rank_q05": float(interval.loc[dest, "rank_q05"]),
                "rank_q95": float(interval.loc[dest, "rank_q95"]),
            }
        )
    return pd.DataFrame.from_records(rows)


def run_smaa_case(
    *,
    origin: str = "COL",
    year: int | None = None,
    normalization: str = "minmax",
    method: str = "wsm",
    mode: SamplingMode = "dirichlet",
    dispersion_scale: float = 1.0,
    n_samples: int | None = None,
    seed: int | None = None,
    panel_path: Path | None = None,
    settings: Settings | None = None,
) -> dict[str, Any]:
    """Run SMAA for one origin-year; write T8 and F2."""
    from imsfe.report.figures import plot_smaa_rank_heatmap

    settings = settings or load_settings()
    n_samples = int(settings.smaa.n_samples if n_samples is None else n_samples)
    seed = int(settings.smaa.seed if seed is None else seed)
    path = panel_path or (processed_dir() / "panel_ijt.parquet")
    panel = pd.read_parquet(path)
    if year is None:
        year = int(panel.loc[panel["iso3_o"] == origin, "year"].max())

    raw, normalized, dirs, center = prepare_origin_year_matrices(
        panel, origin, int(year), normalization=normalization
    )
    stats = build_expert_stats(center)
    if method == "wsm":
        result = run_smaa_wsm(
            normalized,
            center,
            stats,
            n_samples=n_samples,
            seed=seed,
            mode=mode,
            dispersion_scale=dispersion_scale,
        )
    else:
        result = run_smaa_generic(
            raw,
            normalized,
            dirs,
            center,
            stats,
            method,
            n_samples=n_samples,
            seed=seed,
            mode=mode,
            dispersion_scale=dispersion_scale,
        )

    t8 = build_t8(result, top_n=10)
    t8_path = outputs_tables_dir() / "T8_smaa_col.csv"
    t8.to_csv(t8_path, index=False)

    fig_paths = plot_smaa_rank_heatmap(result, top_n=15, stem="F2_smaa_rank_acceptability")

    # Persist compact SMAA summary under processed (gitignored parquet OK)
    summary = {
        "origin": origin,
        "year": int(year),
        "method": method,
        "normalization": normalization,
        "mode": mode,
        "n_samples": n_samples,
        "seed": seed,
        "central_weights": result.central_weights.to_dict(),
    }
    return {
        "result": result,
        "t8": t8,
        "t8_path": t8_path,
        "figure_paths": fig_paths,
        "summary": summary,
        "year": int(year),
        "origin": origin,
    }
