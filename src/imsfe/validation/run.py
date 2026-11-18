"""Orchestrate walk-forward validation and write T4/T5/T6/F4."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd

from imsfe.build.descriptives import outputs_tables_dir
from imsfe.build.panel import processed_dir
from imsfe.config import load_settings, load_variables
from imsfe.report.figures import figures_dir
from imsfe.validation.backtest import (
    ABLATION_SETS,
    bootstrap_ablation_deltas,
    bootstrap_method_summary,
    collect_method_metrics,
    factor_scores_slice,
    make_split,
    score_slice,
)
from imsfe.validation.gravity import (
    explanatory_ppml_factors,
    explanatory_ppml_score,
    fit_gravity_ppml,
    predict_gravity_scores,
)
from imsfe.validation.learned import fit_learned_weights
from imsfe.weights import weights_expert_mean


def default_method_specs() -> list[dict[str, str]]:
    """Focused evaluation grid: default MCDM family × key weight schemes."""
    specs = []
    for method in ("wsm", "topsis", "vikor", "promethee_ii"):
        specs.append(
            {
                "name": f"{method}|minmax|expert_mean",
                "method": method,
                "normalization": "minmax",
                "weights": "expert_mean",
            }
        )
    specs.append(
        {
            "name": "wsm|minmax|equal",
            "method": "wsm",
            "normalization": "minmax",
            "weights": "equal",
        }
    )
    specs.append(
        {
            "name": "wsm|minmax|learned",
            "method": "wsm",
            "normalization": "minmax",
            "weights": "learned",
        }
    )
    return specs


def run_validation(
    *,
    first_test_year: int = 2019,
    horizon: int = 1,
    n_boot: int | None = None,
    n_learned_restarts: int = 3,
    panel_path: Path | None = None,
) -> dict[str, Any]:
    """Full predictive-validation pipeline."""
    settings = load_settings()
    n_boot = int(settings.bootstrap.n_reps if n_boot is None else n_boot)
    path = panel_path or (processed_dir() / "panel_ijt.parquet")
    panel = pd.read_parquet(path)
    # Guard against accidental duplicate i×j×t rows from older builds.
    panel = panel.drop_duplicates(["iso3_o", "iso3_d", "year"], keep="first")
    split = make_split(
        panel["year"].unique(),
        first_test_year=first_test_year,
        horizon=horizon,
    )
    print(
        f"split: train_features={split.train_feature_years} "
        f"test_features={split.test_feature_years} k={horizon}",
        flush=True,
    )
    split.assert_no_leakage()

    # --- learned weights on training years only ---
    print("fitting learned weights...", flush=True)
    learned, learned_info = fit_learned_weights(
        panel,
        split.train_feature_years,
        horizon=horizon,
        n_restarts=n_learned_restarts,
        seed=settings.seed,
        maxiter=40,
    )
    learned_path = outputs_tables_dir() / "T4_learned_vs_expert_weights.csv"
    learned_info["comparison"].to_csv(learned_path, index=False)

    # --- gravity predictive baseline ---
    print("fitting gravity PPML...", flush=True)
    grav_est = fit_gravity_ppml(panel, split.train_feature_years, destination_fe=False)
    grav_scores = predict_gravity_scores(panel, grav_est, split.test_feature_years)

    # --- block metrics ---
    print("collecting walk-forward metrics...", flush=True)
    blocks = collect_method_metrics(
        panel,
        split,
        method_specs=default_method_specs(),
        gravity_score_table=grav_scores,
        learned_weights=learned,
        random_seeds=100,
    )
    blocks_path = processed_dir() / "validation_blocks.parquet"
    blocks.to_parquet(blocks_path, index=False)

    # T4: summary with CI for key metrics
    t4_parts = []
    for metric in ("ndcg@10", "spearman", "precision@10", "auc"):
        if metric not in blocks.columns:
            continue
        # Exclude ablation from T4 main table
        sub = blocks.loc[blocks["family"] != "ablation"]
        t4_parts.append(
            bootstrap_method_summary(
                sub, metric=metric, n_reps=n_boot, seed=settings.bootstrap.seed
            )
        )
    t4 = pd.concat(t4_parts, ignore_index=True)
    t4_path = outputs_tables_dir() / "T4_predictive_metrics.csv"
    t4.to_csv(t4_path, index=False)

    # T6: ablation deltas
    abl_blocks = blocks.loc[blocks["method"].isin(ABLATION_SETS.keys())]
    t6 = bootstrap_ablation_deltas(
        abl_blocks,
        metric="ndcg@10",
        baseline="base_macro",
        n_reps=n_boot,
        seed=settings.bootstrap.seed,
    )
    # also raw means
    abl_means = bootstrap_method_summary(
        abl_blocks, metric="ndcg@10", n_reps=n_boot, seed=settings.bootstrap.seed
    )
    t6_path = outputs_tables_dir() / "T6_ablation.csv"
    t6_out = t6.copy()
    t6_out.to_csv(t6_path, index=False)
    abl_means.to_csv(outputs_tables_dir() / "T6_ablation_levels.csv", index=False)

    # T5: explanatory PPML on IMS score + factor scores (test years)
    print("fitting explanatory PPML (T5)...", flush=True)
    expert = weights_expert_mean()
    variables = load_variables()
    score_rows = []
    factor_rows = []
    test_panel = panel.loc[panel["year"].isin(split.test_feature_years)]
    for (origin, year), group in test_panel.groupby(["iso3_o", "year"]):
        sc = score_slice(
            group,
            variables=variables,
            normalization="minmax",
            method="wsm",
            weights=expert,
        )
        if sc.empty:
            continue
        for dest, val in sc.items():
            score_rows.append(
                {
                    "origin": origin,
                    "year": int(year),
                    "dest": dest,
                    "score": float(val),
                }
            )
        fs = factor_scores_slice(
            group,
            variables=variables,
            normalization="minmax",
            weights=expert,
        )
        if not fs.empty:
            tmp = fs.copy()
            tmp.index.name = "iso3_d"
            tmp = tmp.reset_index()
            tmp["iso3_o"] = origin
            tmp["year"] = int(year)
            factor_rows.append(tmp)
    scores_df = pd.DataFrame(score_rows)
    factors_df = pd.concat(factor_rows, ignore_index=True) if factor_rows else pd.DataFrame()

    t5_frames = []
    try:
        r_score = explanatory_ppml_score(
            panel, scores_df, horizon=horizon, label="y_level_on_ims_score"
        )
        t5_frames.append(r_score.to_frame())
    except Exception as exc:  # noqa: BLE001
        print(f"T5 score PPML failed: {exc}", flush=True)
    try:
        if not factors_df.empty:
            # Prefer a non-collinear core of factor scores for T5.
            preferred = [
                "demand",
                "cost_access",
                "competition",
                "product_fit",
                "institutional",
                "macro_risk",
            ]
            fcols = [c for c in preferred if c in factors_df.columns]
            # Drop sparse factor columns (e.g. logistics/LPI) that would wipe rows.
            keep = []
            for c in fcols:
                if float(factors_df[c].notna().mean()) >= 0.5:
                    keep.append(c)
            fcols = keep or fcols
            fac = factors_df[["iso3_o", "iso3_d", "year", *fcols]].copy()
            r_fac = explanatory_ppml_factors(
                panel, fac, horizon=horizon, label="y_level_on_factor_scores"
            )
            t5_frames.append(r_fac.to_frame())
    except Exception as exc:  # noqa: BLE001
        print(f"T5 factors PPML failed: {exc}", flush=True)
    t5 = pd.concat(t5_frames, ignore_index=True) if t5_frames else pd.DataFrame()
    t5_path = outputs_tables_dir() / "T5_ppml.csv"
    t5.to_csv(t5_path, index=False)

    # F4: NDCG@10 by year and method
    f4_path = _plot_f4(blocks.loc[blocks["family"] != "ablation"])

    summary = _plain_summary(t4, t5, t6, learned_info)
    summary_path = outputs_tables_dir() / "validation_summary.txt"
    summary_path.write_text(summary + "\n", encoding="utf-8")

    return {
        "split": split,
        "t4": t4,
        "t4_path": t4_path,
        "t5": t5,
        "t5_path": t5_path,
        "t6": t6,
        "t6_path": t6_path,
        "f4_path": f4_path,
        "learned_path": learned_path,
        "blocks_path": blocks_path,
        "summary": summary,
        "summary_path": summary_path,
        "learned_info": learned_info,
    }


def _plot_f4(blocks: pd.DataFrame) -> Path:
    """NDCG@10 by year and method (selected methods)."""
    keep = [
        "wsm|minmax|expert_mean",
        "wsm|minmax|equal",
        "wsm|minmax|learned",
        "topsis|minmax|expert_mean",
        "import_volume",
        "eoc",
        "gravity_ppml",
        "random",
        "ml_gbm",
    ]
    sub = blocks.loc[blocks["method"].isin(keep) & blocks["ndcg@10"].notna()].copy()
    yearly = (
        sub.groupby(["year", "method"], as_index=False)["ndcg@10"]
        .mean()
        .sort_values(["year", "method"])
    )
    fig, ax = plt.subplots(figsize=(9, 4.5))
    for method, g in yearly.groupby("method"):
        ax.plot(g["year"], g["ndcg@10"], marker="o", label=method)
    ax.set_xlabel("Feature year t")
    ax.set_ylabel("NDCG@10 (mean over origins)")
    ax.set_title("Walk-forward NDCG@10 by year and method")
    ax.legend(fontsize=7, loc="best")
    ax.set_ylim(0, 1.05)
    fig.tight_layout()
    png = figures_dir() / "F4_ndcg_by_year.png"
    pdf = figures_dir() / "F4_ndcg_by_year.pdf"
    fig.savefig(png, dpi=300, bbox_inches="tight")
    fig.savefig(pdf, format="pdf", bbox_inches="tight")
    plt.close(fig)
    return png


def _plain_summary(
    t4: pd.DataFrame,
    t5: pd.DataFrame,
    t6: pd.DataFrame,
    learned_info: dict[str, Any],
) -> str:
    """One paragraph of factual numbers only (no manuscript claims)."""

    def _row(method: str, metric: str) -> str:
        sub = t4.loc[(t4["method"] == method) & (t4["metric"] == metric)]
        if sub.empty:
            return f"{method}/{metric}=NA"
        r = sub.iloc[0]
        return (
            f"{method} {metric}={r['mean']:.3f} "
            f"[{r['ci95_low']:.3f},{r['ci95_high']:.3f}]"
        )

    bits = [
        _row("wsm|minmax|expert_mean", "ndcg@10"),
        _row("wsm|minmax|learned", "ndcg@10"),
        _row("import_volume", "ndcg@10"),
        _row("gravity_ppml", "ndcg@10"),
        _row("random", "ndcg@10"),
        _row("wsm|minmax|expert_mean", "auc"),
    ]
    abl = []
    for _, r in t6.iterrows():
        abl.append(
            f"{r['contrast']} Δndcg@10={r['delta_mean']:.3f} "
            f"[{r['ci95_low']:.3f},{r['ci95_high']:.3f}]"
        )
    t5_bits = []
    if not t5.empty and "ims_score" in set(t5.get("term", [])):
        r = t5.loc[t5["term"] == "ims_score"].iloc[0]
        t5_bits.append(
            f"PPML ims_score coef={r['estimate']:.4f} se={r['std_error']:.4f} "
            f"n={int(r['n_obs'])}"
        )
    return (
        "Walk-forward results (factual): "
        + "; ".join(bits)
        + ". Ablation: "
        + ("; ".join(abl) if abl else "NA")
        + ". "
        + ("; ".join(t5_bits) if t5_bits else "T5 PPML terms recorded in T5_ppml.csv")
        + f". Learned-weight train NDCG@10={learned_info.get('train_ndcg@10', float('nan')):.3f}."
    )
