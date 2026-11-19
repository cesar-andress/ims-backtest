"""Run normalisation × MCDM × weights grid and write scores/ranks."""

from __future__ import annotations

import logging
from itertools import product
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import kendalltau

from imsfe.build.descriptives import outputs_tables_dir
from imsfe.build.panel import processed_dir
from imsfe.config import (
    ExperimentsConfig,
    Settings,
    VariablesConfig,
    load_experiments,
    load_settings,
    load_variables,
)
from imsfe.mcdm import score
from imsfe.normalize import normalize_matrix
from imsfe.weights import get_weights

logger = logging.getLogger(__name__)


def _feature_columns(variables: VariablesConfig) -> list[str]:
    return [v.id for v in variables.variables]


def _directions(variables: VariablesConfig) -> dict[str, str]:
    return {v.id: v.direction for v in variables.variables}


def _prepare_slice(
    raw: pd.DataFrame,
    columns: list[str],
) -> tuple[pd.DataFrame, list[str]]:
    """Legacy helper retained for descriptives; prefer ``prepare_block``.

    Builds a temporary frame with ``iso3_d`` from the index and applies the
    fixed-candidate missing-data policy.
    """
    from imsfe.block_prep import prepare_block

    if raw.empty:
        return pd.DataFrame(index=raw.index), []
    tmp = raw.copy()
    tmp = tmp.reset_index()
    # Index name may already be iso3_d
    if "iso3_d" not in tmp.columns:
        tmp = tmp.rename(columns={tmp.columns[0]: "iso3_d"})
    prep = prepare_block(tmp, columns)
    return prep.matrix, prep.used_variables


def score_origin_year(
    group: pd.DataFrame,
    *,
    variables: VariablesConfig,
    normalization: str,
    method: str,
    weight_scheme: str,
    cached_weights: dict[str, Any] | None = None,
) -> pd.DataFrame:
    """Score one (origin, year) cross-section; returns dest/score/rank rows."""
    from imsfe.block_prep import prepare_block

    directions = _directions(variables)
    cols = _feature_columns(variables)
    prep = prepare_block(group, cols)
    complete = prep.matrix
    usable = prep.used_variables
    if complete.empty or len(complete) < 2:
        return pd.DataFrame(
            columns=["dest", "score", "rank", "n_alternatives", "n_criteria"]
        )

    dirs = {c: directions[c] for c in usable}
    # Objective weights from the prepared matrix
    if weight_scheme in ("entropy", "critic"):
        weights = get_weights(
            weight_scheme, variables, matrix=complete, directions=dirs
        )
    elif cached_weights and weight_scheme in cached_weights:
        weights = cached_weights[weight_scheme]
    else:
        weights = get_weights(weight_scheme, variables)
    weights = weights.restrict(usable)

    normalized = normalize_matrix(complete, dirs, normalization)  # type: ignore[arg-type]
    sc = score(
        complete,
        weights,
        dirs,  # type: ignore[arg-type]
        method,  # type: ignore[arg-type]
        normalized=normalized,
    )
    sc = sc.replace([np.inf, -np.inf], np.nan)
    if sc.isna().any():
        # Should not happen with prepared matrix; drop only non-finite scores.
        sc = sc.dropna()
    if sc.empty or len(sc) < 2:
        return pd.DataFrame(
            columns=["dest", "score", "rank", "n_alternatives", "n_criteria"]
        )
    ranks = sc.rank(ascending=False, method="min").astype(int)
    out = pd.DataFrame(
        {
            "dest": sc.index.astype(str),
            "score": sc.to_numpy(dtype=float),
            "rank": ranks.to_numpy(dtype=int),
            "n_alternatives": len(sc),
            "n_criteria": len(usable),
        }
    )
    return out


def run_grid(
    panel: pd.DataFrame,
    experiments: ExperimentsConfig | None = None,
    variables: VariablesConfig | None = None,
    *,
    skip_learned: bool = True,
) -> pd.DataFrame:
    """Cartesian product of normalisation × MCDM × weights over the panel."""
    experiments = experiments or load_experiments()
    variables = variables or load_variables()
    weight_schemes = [
        w
        for w in experiments.weight_schemes
        if not (skip_learned and w == "learned")
    ]
    # Cache origin-independent schemes once.
    cached_weights = {
        "equal": get_weights("equal", variables),
        "expert_mean": get_weights("expert_mean", variables),
    }
    rows: list[dict[str, Any]] = []
    n_skip = 0
    groups = panel.groupby(["iso3_o", "year"], sort=True)
    combos = list(
        product(experiments.normalizations, experiments.mcdm_methods, weight_schemes)
    )
    print(
        f"Running {len(combos)} combinations over {groups.ngroups} origin-year groups",
        flush=True,
    )
    for (origin, year), group in groups:
        for norm, method, wscheme in combos:
            try:
                scored = score_origin_year(
                    group,
                    variables=variables,
                    normalization=norm,
                    method=method,
                    weight_scheme=wscheme,
                    cached_weights=cached_weights,
                )
            except Exception as exc:  # noqa: BLE001
                n_skip += 1
                if n_skip <= 5:
                    print(
                        f"skip {origin}/{year} {method}+{norm}+{wscheme}: {exc}",
                        flush=True,
                    )
                continue
            for rec in scored.to_dict(orient="records"):
                rows.append(
                    {
                        "origin": origin,
                        "year": int(year),
                        "dest": rec["dest"],
                        "method": method,
                        "normalization": norm,
                        "weights": wscheme,
                        "score": rec["score"],
                        "rank": rec["rank"],
                    }
                )
    if n_skip:
        print(f"skipped {n_skip} origin-year×combo cells (see first 5 above)", flush=True)
    if not rows:
        return pd.DataFrame(
            columns=[
                "origin",
                "year",
                "dest",
                "method",
                "normalization",
                "weights",
                "score",
                "rank",
            ]
        )
    return pd.DataFrame.from_records(rows)


def kendall_tau_matrix(
    scores: pd.DataFrame,
    *,
    origin: str,
    year: int,
) -> pd.DataFrame:
    """Pairwise Kendall tau of ranks across method combinations for one origin-year."""
    sub = scores.loc[(scores["origin"] == origin) & (scores["year"] == year)].copy()
    if sub.empty:
        return pd.DataFrame()
    sub["combo"] = (
        sub["method"] + "|" + sub["normalization"] + "|" + sub["weights"]
    )
    # Pivot rank by dest × combo; require shared destinations
    pivot = sub.pivot_table(index="dest", columns="combo", values="rank", aggfunc="first")
    combos = list(pivot.columns)
    mat = pd.DataFrame(index=combos, columns=combos, dtype=float)
    for a in combos:
        for b in combos:
            pair = pivot[[a, b]].dropna()
            if len(pair) < 3:
                mat.loc[a, b] = np.nan
                continue
            tau, _ = kendalltau(pair[a], pair[b])
            mat.loc[a, b] = float(tau) if tau == tau else np.nan
    return mat


def run_experiments(
    *,
    experiment: str = "default",
    panel_path: Path | None = None,
    settings: Settings | None = None,
) -> dict[str, Any]:
    """Execute the experiment grid, write scores.parquet and T7_robustness.csv."""
    settings = settings or load_settings()
    experiments = load_experiments()
    variables = load_variables()
    path = panel_path or (processed_dir() / "panel_ijt.parquet")
    if not path.is_file():
        raise FileNotFoundError(
            f"Missing panel at {path}; run `imsfe build` first"
        )
    panel = pd.read_parquet(path)

    # Always compute the full grid (learned skipped) for robustness table.
    scores = run_grid(panel, experiments, variables, skip_learned=True)
    out_scores = processed_dir() / "scores.parquet"
    scores.to_parquet(out_scores, index=False)

    last_year = int(panel["year"].max())
    origin = settings.origins[0]
    # Primary combo for printing
    if experiment == "default":
        norm = experiments.default.normalization
        method = experiments.default.mcdm
        wscheme = experiments.default.weights
    elif experiment == "grid":
        norm = experiments.default.normalization
        method = experiments.default.mcdm
        wscheme = experiments.default.weights
    else:
        # Allow "wsm+minmax+expert_mean" shorthand
        parts = experiment.replace(" ", "").split("+")
        if len(parts) == 3:
            method, norm, wscheme = parts
        else:
            raise ValueError(
                f"Unknown experiment {experiment!r}; use 'default', 'grid', "
                "or 'method+normalization+weights'"
            )

    primary = scores.loc[
        (scores["origin"] == origin)
        & (scores["year"] == last_year)
        & (scores["method"] == method)
        & (scores["normalization"] == norm)
        & (scores["weights"] == wscheme)
    ].sort_values("rank")

    tau = kendall_tau_matrix(scores, origin=origin, year=last_year)
    t7 = outputs_tables_dir() / "T7_robustness.csv"
    tau.to_csv(t7)

    return {
        "scores_path": out_scores,
        "t7_path": t7,
        "n_rows": int(len(scores)),
        "n_combos": int(
            scores[["method", "normalization", "weights"]].drop_duplicates().shape[0]
        ),
        "origin": origin,
        "year": last_year,
        "primary_method": method,
        "primary_normalization": norm,
        "primary_weights": wscheme,
        "top10": primary.head(10),
        "tau": tau,
    }
