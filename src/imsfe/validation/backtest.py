"""Walk-forward predictive evaluation of IMS rankings against export outcomes."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from imsfe.config import VariablesConfig, load_experiments, load_settings, load_variables
from imsfe.mcdm import hierarchical_wsm, score
from imsfe.normalize import normalize_matrix
from imsfe.run_experiments import _directions, _feature_columns
from imsfe.validation.metrics import evaluate_ranking
from imsfe.weights import Weights, get_weights


@dataclass(frozen=True)
class WalkForwardSplit:
    """Temporal split with an explicit leakage rule on outcome years."""

    first_test_year: int
    horizon: int
    feature_years_all: tuple[int, ...]

    @property
    def train_feature_years(self) -> list[int]:
        # Outcome year for feature year t is t+k; must be < first_test_year.
        return [y for y in self.feature_years_all if y + self.horizon < self.first_test_year]

    @property
    def test_feature_years(self) -> list[int]:
        ymax = max(self.feature_years_all)
        return [
            y
            for y in self.feature_years_all
            if y >= self.first_test_year and y + self.horizon <= ymax
        ]

    def assert_no_leakage(self) -> None:
        for y in self.train_feature_years:
            if y + self.horizon >= self.first_test_year:
                raise AssertionError(
                    f"leakage: train feature year {y} has outcome year "
                    f"{y + self.horizon} >= first_test_year {self.first_test_year}"
                )
        for y in self.test_feature_years:
            if y < self.first_test_year:
                raise AssertionError(f"test year {y} < first_test_year")


def make_split(
    years: Iterable[int],
    *,
    first_test_year: int,
    horizon: int,
) -> WalkForwardSplit:
    split = WalkForwardSplit(
        first_test_year=int(first_test_year),
        horizon=int(horizon),
        feature_years_all=tuple(sorted(set(int(y) for y in years))),
    )
    split.assert_no_leakage()
    return split


def score_slice(
    group: pd.DataFrame,
    *,
    variables: VariablesConfig,
    normalization: str,
    method: str,
    weights: Weights,
    return_meta: bool = False,
) -> pd.Series | tuple[pd.Series, dict[str, object]]:
    """Score destinations for one origin-year group; index = iso3_d.

    Candidate set is fixed (all destinations in ``group``); missing-data policy
    from ``settings.missing_data``.
    """
    from imsfe.block_prep import block_meta_dict, prepare_block

    cols = _feature_columns(variables)
    directions = _directions(variables)
    prep = prepare_block(group, cols)
    complete = prep.matrix
    usable = prep.used_variables
    meta = block_meta_dict(prep)
    if complete.empty or len(complete) < 2:
        empty = pd.Series(dtype=float)
        return (empty, meta) if return_meta else empty
    dirs = {c: directions[c] for c in usable}
    w = weights.restrict(usable)
    normalized = normalize_matrix(complete, dirs, normalization)  # type: ignore[arg-type]
    sc = score(
        complete,
        w,
        dirs,  # type: ignore[arg-type]
        method,  # type: ignore[arg-type]
        normalized=normalized,
    )
    sc = sc.replace([np.inf, -np.inf], np.nan)
    # Keep all candidates; non-finite scores are rare after preparation.
    if return_meta:
        return sc, meta
    return sc


def factor_scores_slice(
    group: pd.DataFrame,
    *,
    variables: VariablesConfig,
    normalization: str,
    weights: Weights,
) -> pd.DataFrame:
    """Hierarchical factor scores for one origin-year (before factor aggregation)."""
    from imsfe.block_prep import prepare_block

    cols = _feature_columns(variables)
    directions = _directions(variables)
    prep = prepare_block(group, cols)
    complete = prep.matrix
    usable = prep.used_variables
    if complete.empty:
        return pd.DataFrame()
    dirs = {c: directions[c] for c in usable}
    w = weights.restrict(usable)
    normalized = normalize_matrix(complete, dirs, normalization)  # type: ignore[arg-type]
    factor_mat = pd.DataFrame(index=normalized.index, dtype=float)
    for factor, vw in w.variables_within.items():
        ids = [c for c in vw.index if c in normalized.columns]
        if not ids:
            continue
        ww = vw.loc[ids]
        ww = ww / ww.sum()
        factor_mat[factor] = normalized[ids].mul(ww, axis=1).sum(axis=1)
    return factor_mat


ABLATION_SETS: dict[str, list[str]] = {
    # Macro attractiveness: demand + logistics + institutions + macro risk
    "base_macro": [
        "IMPV",
        "IMPC",
        "GRW",
        "GDPPC",
        "LPI",
        "GOV",
        "INFL",
        "UNEMP",
        "EOC",
    ],
    "plus_fit": [
        "IMPV",
        "IMPC",
        "GRW",
        "GDPPC",
        "LPI",
        "GOV",
        "INFL",
        "UNEMP",
        "EOC",
        "UVGAP",
        "CULT",
        "LANG",
        "DIST",
        "TARIF",
        "FTA",
    ],
    "plus_fit_comp": [
        "IMPV",
        "IMPC",
        "GRW",
        "GDPPC",
        "LPI",
        "GOV",
        "INFL",
        "UNEMP",
        "EOC",
        "UVGAP",
        "CULT",
        "LANG",
        "DIST",
        "TARIF",
        "FTA",
        "ASIASH",
        "HHI",
    ],
}


def score_with_variable_subset(
    group: pd.DataFrame,
    variable_ids: list[str],
    *,
    variables: VariablesConfig,
    normalization: str = "minmax",
) -> pd.Series:
    """Equal-within-available-factor WSM on a variable subset (ablation)."""
    from imsfe.block_prep import prepare_block

    directions = _directions(variables)
    present = [v for v in variable_ids if v in group.columns]
    prep = prepare_block(group, present)
    complete = prep.matrix
    usable = prep.used_variables
    if complete.empty or len(complete) < 2:
        return pd.Series(dtype=float)
    # Equal hierarchical weights over factors that still have variables
    by_factor: dict[str, list[str]] = {}
    for v in variables.variables:
        if v.id in usable:
            by_factor.setdefault(v.factor, []).append(v.id)
    if not by_factor:
        return pd.Series(dtype=float)
    fw = pd.Series({f: 1.0 / len(by_factor) for f in by_factor}, dtype=float)
    within = {
        f: pd.Series(1.0 / len(vs), index=vs, dtype=float) for f, vs in by_factor.items()
    }
    w = Weights(factors=fw, variables_within=within, scheme="ablation_equal")
    dirs = {c: directions[c] for c in usable}
    normalized = normalize_matrix(complete, dirs, normalization)  # type: ignore[arg-type]
    return hierarchical_wsm(normalized, w)


def baseline_scores(
    group: pd.DataFrame,
    name: str,
    *,
    rng: np.random.Generator | None = None,
) -> pd.Series:
    """Build a baseline score series indexed by destination."""
    g = group.set_index("iso3_d")
    if name == "import_volume":
        col = "IMPV_raw" if "IMPV_raw" in g.columns else "IMPV"
        return pd.to_numeric(g[col], errors="coerce")
    if name == "eoc":
        col = "EOC_raw" if "EOC_raw" in g.columns else "EOC"
        return pd.to_numeric(g[col], errors="coerce")
    if name == "random":
        if rng is None:
            rng = np.random.default_rng(0)
        return pd.Series(rng.random(len(g)), index=g.index, dtype=float)
    raise ValueError(f"Unknown baseline {name}")


TARGET_Y_COLUMNS = {
    "intensive": "y_int_k{k}",
    "growth": "y_growth_k{k}",
    "new_markets": "y_newmarket_k{k}",
}


def metrics_for_scores(
    scores: pd.Series,
    group: pd.DataFrame,
    *,
    horizon: int,
    target: str = "intensive",
) -> dict[str, float]:
    g = group.drop_duplicates("iso3_d", keep="first").set_index("iso3_d")
    scores = scores[~scores.index.duplicated(keep="first")]
    y_tmpl = TARGET_Y_COLUMNS.get(target, TARGET_Y_COLUMNS["intensive"])
    y_col = y_tmpl.format(k=horizon)
    y_int = g[y_col] if y_col in g.columns else None
    y_ext = g[f"y_ext_k{horizon}"] if f"y_ext_k{horizon}" in g.columns else None
    # For new_markets / growth, AUC on y_ext is still informative but secondary.
    return evaluate_ranking(scores, y_int=y_int, y_ext=y_ext if target == "intensive" else None)


def collect_method_metrics(
    panel: pd.DataFrame,
    split: WalkForwardSplit,
    *,
    method_specs: list[dict[str, Any]],
    baselines: list[str] | None = None,
    random_seeds: int = 100,
    gravity_score_table: pd.DataFrame | None = None,
    learned_weights: Weights | None = None,
    target: str = "intensive",
) -> pd.DataFrame:
    """Evaluate methods/baselines on every test origin-year; one row per block."""
    settings = load_settings()
    variables = load_variables()
    experiments = load_experiments()
    baselines = baselines or list(experiments.baselines)
    rows: list[dict[str, Any]] = []

    cached: dict[str, Weights] = {
        "equal": get_weights("equal", variables),
        "expert_mean": get_weights("expert_mean", variables),
    }
    if learned_weights is not None:
        cached["learned"] = learned_weights

    from imsfe.block_prep import block_meta_dict, prepare_block

    test = panel.loc[panel["year"].isin(split.test_feature_years)]
    for (origin, year), group in test.groupby(["iso3_o", "year"], sort=True):
        # Fixed candidate set for this block (identical across methods).
        cols = _feature_columns(variables)
        prep = prepare_block(group, cols)
        block_meta = block_meta_dict(prep)
        cand = list(prep.candidates)

        def _restrict(sc: pd.Series, _cand: list[str] = cand) -> pd.Series:
            return sc.reindex(_cand)

        # Method configs
        for spec in method_specs:
            name = spec["name"]
            wscheme = spec["weights"]
            if wscheme == "learned" and learned_weights is None:
                continue
            if wscheme in ("entropy", "critic"):
                dirs = {c: _directions(variables)[c] for c in prep.used_variables}
                weights = get_weights(
                    wscheme,
                    variables,
                    matrix=prep.matrix,
                    directions=dirs,
                )
            else:
                weights = cached.get(wscheme) or get_weights(wscheme, variables)
            sc, meta = score_slice(
                group,
                variables=variables,
                normalization=spec["normalization"],
                method=spec["method"],
                weights=weights,
                return_meta=True,
            )
            if sc.empty:
                continue
            sc = _restrict(sc)
            mets = metrics_for_scores(
                sc, group, horizon=split.horizon, target=target
            )
            rows.append(
                {
                    "origin": origin,
                    "year": int(year),
                    "method": name,
                    "family": "ims",
                    "target": target,
                    "horizon": int(split.horizon),
                    **block_meta,
                    **mets,
                }
            )

        # Baselines — same candidate index as IMS methods
        for b in baselines:
            if b == "equal_weights":
                sc, _meta = score_slice(
                    group,
                    variables=variables,
                    normalization="minmax",
                    method="wsm",
                    weights=cached["equal"],
                    return_meta=True,
                )
            elif b == "gravity_ppml":
                if gravity_score_table is None:
                    continue
                sub = gravity_score_table.loc[
                    (gravity_score_table["iso3_o"] == origin)
                    & (gravity_score_table["year"] == year)
                ].drop_duplicates("iso3_d", keep="first")
                sc = sub.set_index("iso3_d")["score"]
            elif b == "random":
                acc: list[dict[str, float]] = []
                for s in range(random_seeds):
                    rng = np.random.default_rng(settings.seed + s)
                    sc_r = _restrict(baseline_scores(group, "random", rng=rng))
                    acc.append(
                        metrics_for_scores(
                            sc_r, group, horizon=split.horizon, target=target
                        )
                    )
                if not acc:
                    continue
                avg = pd.DataFrame(acc).mean(numeric_only=True).to_dict()
                rows.append(
                    {
                        "origin": origin,
                        "year": int(year),
                        "method": "random",
                        "family": "baseline",
                        "target": target,
                        "horizon": int(split.horizon),
                        **block_meta,
                        **avg,
                    }
                )
                continue
            else:
                sc = baseline_scores(group, b)
            if sc is None or sc.empty:
                continue
            sc = _restrict(sc)
            mets = metrics_for_scores(
                sc, group, horizon=split.horizon, target=target
            )
            rows.append(
                {
                    "origin": origin,
                    "year": int(year),
                    "method": b,
                    "family": "baseline",
                    "target": target,
                    "horizon": int(split.horizon),
                    **block_meta,
                    **mets,
                }
            )

        # Ablation variants
        for abl_name, var_ids in ABLATION_SETS.items():
            sc = score_with_variable_subset(
                group, var_ids, variables=variables, normalization="minmax"
            )
            if sc.empty:
                continue
            sc = _restrict(sc)
            mets = metrics_for_scores(
                sc, group, horizon=split.horizon, target=target
            )
            rows.append(
                {
                    "origin": origin,
                    "year": int(year),
                    "method": abl_name,
                    "family": "ablation",
                    "target": target,
                    "horizon": int(split.horizon),
                    **block_meta,
                    **mets,
                }
            )

    return pd.DataFrame.from_records(rows)


def bootstrap_method_summary(
    block_metrics: pd.DataFrame,
    *,
    metric: str = "ndcg@10",
    n_reps: int = 2000,
    seed: int = 42,
    alpha: float = 0.05,
) -> pd.DataFrame:
    """Mean metric by method with percentile CI; blocks = origin-year rows."""
    rng = np.random.default_rng(seed)
    methods = sorted(block_metrics["method"].unique())
    # Each block key
    blocks = block_metrics[["origin", "year"]].drop_duplicates().reset_index(drop=True)
    n_blocks = len(blocks)
    rows = []
    for method in methods:
        sub = block_metrics.loc[block_metrics["method"] == method]
        # map block -> metric
        merged = blocks.merge(sub[["origin", "year", metric]], on=["origin", "year"], how="left")
        vals = merged[metric].to_numpy(dtype=float)
        observed = float(np.nanmean(vals))
        boots = np.empty(n_reps, dtype=float)
        for r in range(n_reps):
            idx = rng.integers(0, n_blocks, size=n_blocks)
            boots[r] = float(np.nanmean(vals[idx]))
        lo, hi = np.nanpercentile(boots, [100 * alpha / 2, 100 * (1 - alpha / 2)])
        rows.append(
            {
                "method": method,
                "metric": metric,
                "mean": observed,
                "ci95_low": float(lo),
                "ci95_high": float(hi),
                "n_blocks": int(np.isfinite(vals).sum()),
            }
        )
    return pd.DataFrame.from_records(rows)


def bootstrap_paired_deltas(
    block_metrics: pd.DataFrame,
    *,
    methods: list[str] | None = None,
    baselines: tuple[str, ...] = ("import_volume", "gravity_ppml", "random"),
    metric: str = "ndcg@10",
    n_reps: int = 2000,
    seed: int = 42,
) -> pd.DataFrame:
    """Paired bootstrap Δ(method − baseline) with 95% CIs over origin-year blocks.

    Also reports lift over random when ``random`` is among baselines.
    """
    rng = np.random.default_rng(seed)
    present = set(block_metrics["method"])
    if methods is None:
        methods = sorted(
            m
            for m in present
            if m not in baselines and not str(m).startswith("base_")
            and m not in ABLATION_SETS
        )
    blocks = block_metrics[["origin", "year"]].drop_duplicates().reset_index(drop=True)
    pivot = block_metrics.pivot_table(
        index=["origin", "year"], columns="method", values=metric, aggfunc="first"
    )
    target = (
        str(block_metrics["target"].iloc[0]) if "target" in block_metrics.columns else ""
    )
    horizon = (
        int(block_metrics["horizon"].iloc[0])
        if "horizon" in block_metrics.columns
        else -1
    )
    rows: list[dict[str, Any]] = []
    for method in methods:
        if method not in pivot.columns:
            continue
        for baseline in baselines:
            if baseline not in pivot.columns:
                continue
            aligned = blocks.merge(
                (pivot[method] - pivot[baseline]).rename("delta").reset_index(),
                on=["origin", "year"],
                how="left",
            )["delta"].to_numpy(dtype=float)
            obs = float(np.nanmean(aligned))
            n_blocks = len(aligned)
            boots = np.empty(n_reps, dtype=float)
            for r in range(n_reps):
                idx = rng.integers(0, n_blocks, size=n_blocks)
                boots[r] = float(np.nanmean(aligned[idx]))
            lo, hi = np.nanpercentile(boots, [2.5, 97.5])
            rows.append(
                {
                    "contrast": f"{method} - {baseline}",
                    "method": method,
                    "baseline": baseline,
                    "metric": metric,
                    "target": target,
                    "horizon": horizon,
                    "delta_mean": obs,
                    "ci95_low": float(lo),
                    "ci95_high": float(hi),
                    "n_blocks": int(np.isfinite(aligned).sum()),
                }
            )
    return pd.DataFrame.from_records(rows)


def bootstrap_ablation_deltas(
    block_metrics: pd.DataFrame,
    *,
    metric: str = "ndcg@10",
    baseline: str = "base_macro",
    n_reps: int = 2000,
    seed: int = 42,
) -> pd.DataFrame:
    """Δ(method − base_macro) with bootstrap CI over origin-year blocks."""
    rng = np.random.default_rng(seed)
    abl = [m for m in ABLATION_SETS if m in set(block_metrics["method"])]
    blocks = block_metrics[["origin", "year"]].drop_duplicates().reset_index(drop=True)
    pivot = block_metrics.pivot_table(
        index=["origin", "year"], columns="method", values=metric, aggfunc="first"
    )
    rows = []
    for method in abl:
        if method == baseline or method not in pivot.columns or baseline not in pivot.columns:
            continue
        # align to blocks order
        aligned = blocks.merge(
            (pivot[method] - pivot[baseline]).rename("delta").reset_index(),
            on=["origin", "year"],
            how="left",
        )["delta"].to_numpy(dtype=float)
        obs = float(np.nanmean(aligned))
        boots = np.empty(n_reps, dtype=float)
        n_blocks = len(aligned)
        for r in range(n_reps):
            idx = rng.integers(0, n_blocks, size=n_blocks)
            boots[r] = float(np.nanmean(aligned[idx]))
        lo, hi = np.nanpercentile(boots, [2.5, 97.5])
        rows.append(
            {
                "contrast": f"{method} - {baseline}",
                "metric": metric,
                "delta_mean": obs,
                "ci95_low": float(lo),
                "ci95_high": float(hi),
                "n_blocks": int(np.isfinite(aligned).sum()),
            }
        )
    return pd.DataFrame.from_records(rows)
