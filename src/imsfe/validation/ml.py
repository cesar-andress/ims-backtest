"""Gradient-boosting walk-forward benchmark with SHAP factor importances.

Uses XGBoost with ``device="cuda"`` when CUDA works, otherwise LightGBM on CPU.
Hyper-parameters are chosen by expanding-window time-series CV on training
feature years only (no test-year leakage).
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from imsfe.build.descriptives import outputs_tables_dir
from imsfe.build.panel import processed_dir
from imsfe.config import VariablesConfig, load_settings, load_variables
from imsfe.report.figures import figures_dir
from imsfe.run_experiments import _feature_columns
from imsfe.validation.backtest import (
    WalkForwardSplit,
    bootstrap_method_summary,
    make_split,
    metrics_for_scores,
)
from imsfe.weights import Weights, flat_to_hierarchical, weights_expert_mean

Backend = Literal["xgboost_cuda", "lightgbm_cpu"]


def _load_learned_weights_for_compare() -> Weights | None:
    """In-process cache first; else rebuild hierarchy from Phase-6 T4 CSV."""
    try:
        from imsfe.weights import weights_learned

        return weights_learned()
    except Exception:  # noqa: BLE001
        pass
    path = outputs_tables_dir() / "T4_learned_vs_expert_weights.csv"
    if not path.is_file():
        return None
    df = pd.read_csv(path)
    if "variable" not in df.columns or "learned" not in df.columns:
        return None
    flat = pd.Series(
        df["learned"].to_numpy(dtype=float),
        index=df["variable"].astype(str),
        dtype=float,
    )
    return flat_to_hierarchical(flat, load_variables(), "learned")


def detect_backend(seed: int = 42) -> Backend:
    """Default to LightGBM CPU for published numbers.

    Set ``IMSFE_ALLOW_CUDA=1`` to optionally try XGBoost+CUDA.
    """
    import os

    if os.environ.get("IMSFE_ALLOW_CUDA", "").strip() not in {"1", "true", "TRUE", "yes"}:
        return "lightgbm_cpu"
    try:
        from xgboost import XGBRegressor

        rng = np.random.default_rng(seed)
        X = rng.normal(size=(32, 4))
        y = rng.normal(size=32)
        m = XGBRegressor(
            n_estimators=4,
            max_depth=2,
            device="cuda",
            tree_method="hist",
            random_state=seed,
            verbosity=0,
        )
        m.fit(X, y)
        return "xgboost_cuda"
    except Exception:  # noqa: BLE001
        return "lightgbm_cpu"


def feature_matrix(
    panel: pd.DataFrame,
    variables: VariablesConfig | None = None,
) -> tuple[pd.DataFrame, list[str], dict[str, str]]:
    """Return feature frame, column order, and variable→factor map."""
    variables = variables or load_variables()
    cols = [c for c in _feature_columns(variables) if c in panel.columns]
    factor_of = {v.id: v.factor for v in variables.variables if v.id in cols}
    feats = panel[cols].apply(pd.to_numeric, errors="coerce")
    return feats, cols, factor_of


@dataclass
class MLFitResult:
    backend: Backend
    best_params: dict[str, Any]
    runtime_sec: float
    model_int: Any
    model_ext: Any | None
    feature_names: list[str]
    factor_of: dict[str, str]
    block_metrics: pd.DataFrame
    predictions: pd.DataFrame
    cv_table: pd.DataFrame
    log: dict[str, Any]


def _make_regressor(backend: Backend, params: dict[str, Any], seed: int) -> Any:
    if backend == "xgboost_cuda":
        from xgboost import XGBRegressor

        return XGBRegressor(
            n_estimators=int(params["n_estimators"]),
            max_depth=int(params["max_depth"]),
            learning_rate=float(params["learning_rate"]),
            subsample=float(params.get("subsample", 0.9)),
            colsample_bytree=float(params.get("colsample_bytree", 0.9)),
            device="cuda",
            tree_method="hist",
            random_state=seed,
            n_jobs=1,
            verbosity=0,
        )
    import lightgbm as lgb

    return lgb.LGBMRegressor(
        n_estimators=int(params["n_estimators"]),
        max_depth=int(params["max_depth"]),
        learning_rate=float(params["learning_rate"]),
        subsample=float(params.get("subsample", 0.9)),
        colsample_bytree=float(params.get("colsample_bytree", 0.9)),
        random_state=seed,
        n_jobs=1,
        verbose=-1,
    )


def _make_classifier(backend: Backend, params: dict[str, Any], seed: int) -> Any:
    if backend == "xgboost_cuda":
        from xgboost import XGBClassifier

        return XGBClassifier(
            n_estimators=int(params["n_estimators"]),
            max_depth=int(params["max_depth"]),
            learning_rate=float(params["learning_rate"]),
            subsample=float(params.get("subsample", 0.9)),
            colsample_bytree=float(params.get("colsample_bytree", 0.9)),
            device="cuda",
            tree_method="hist",
            random_state=seed,
            n_jobs=1,
            verbosity=0,
            eval_metric="logloss",
        )
    import lightgbm as lgb

    return lgb.LGBMClassifier(
        n_estimators=int(params["n_estimators"]),
        max_depth=int(params["max_depth"]),
        learning_rate=float(params["learning_rate"]),
        subsample=float(params.get("subsample", 0.9)),
        colsample_bytree=float(params.get("colsample_bytree", 0.9)),
        random_state=seed,
        n_jobs=1,
        verbose=-1,
    )


def _param_grid() -> list[dict[str, Any]]:
    grid = []
    for n_estimators in (80, 160):
        for max_depth in (3, 5):
            for learning_rate in (0.05, 0.1):
                grid.append(
                    {
                        "n_estimators": n_estimators,
                        "max_depth": max_depth,
                        "learning_rate": learning_rate,
                        "subsample": 0.9,
                        "colsample_bytree": 0.9,
                    }
                )
    return grid


def _ts_cv_folds(train_years: list[int]) -> list[tuple[list[int], list[int]]]:
    """Expanding-window folds; validation = last year of each prefix (≥3 train years)."""
    years = sorted(train_years)
    folds = []
    for i in range(3, len(years)):
        folds.append((years[:i], [years[i]]))
    if not folds and len(years) >= 2:
        folds.append((years[:-1], [years[-1]]))
    return folds


def _fit_predict_int(
    backend: Backend,
    params: dict[str, Any],
    X_tr: np.ndarray,
    y_tr: np.ndarray,
    X_va: np.ndarray,
    seed: int,
) -> np.ndarray:
    model = _make_regressor(backend, params, seed)
    model.fit(X_tr, y_tr)
    return np.asarray(model.predict(X_va), dtype=float)


def time_series_cv_select(
    panel: pd.DataFrame,
    train_years: list[int],
    feature_cols: list[str],
    *,
    horizon: int,
    backend: Backend,
    seed: int,
) -> tuple[dict[str, Any], pd.DataFrame]:
    """Pick hyper-parameters by mean Spearman on expanding validation years."""
    ycol = f"y_int_k{horizon}"
    folds = _ts_cv_folds(train_years)
    rows = []
    best_params = _param_grid()[0]
    best_score = -np.inf
    for params in _param_grid():
        fold_scores = []
        for tr_years, va_years in folds:
            tr = panel.loc[panel["year"].isin(tr_years)].dropna(subset=[ycol])
            va = panel.loc[panel["year"].isin(va_years)].dropna(subset=[ycol])
            if len(tr) < 30 or len(va) < 10:
                continue
            X_tr = tr[feature_cols].to_numpy(dtype=float)
            y_tr = tr[ycol].to_numpy(dtype=float)
            X_va = va[feature_cols].to_numpy(dtype=float)
            pred = _fit_predict_int(backend, params, X_tr, y_tr, X_va, seed)
            # Spearman within each origin-year on validation
            va = va.copy()
            va["_pred"] = pred
            sp = []
            for _, g in va.groupby(["iso3_o", "year"]):
                if g[ycol].nunique() < 2:
                    continue
                from scipy.stats import spearmanr

                rho, _ = spearmanr(g["_pred"], g[ycol])
                if np.isfinite(rho):
                    sp.append(float(rho))
            if sp:
                fold_scores.append(float(np.mean(sp)))
        mean_sp = float(np.mean(fold_scores)) if fold_scores else float("nan")
        rows.append({**params, "cv_spearman": mean_sp, "n_folds": len(fold_scores)})
        if np.isfinite(mean_sp) and mean_sp > best_score:
            best_score = mean_sp
            best_params = params
    return best_params, pd.DataFrame.from_records(rows)


def run_ml_walkforward(
    panel: pd.DataFrame,
    split: WalkForwardSplit,
    *,
    seed: int | None = None,
    backend: Backend | None = None,
) -> MLFitResult:
    """Train on split.train years; score each test origin-year; log runtime."""
    settings = load_settings()
    seed = int(settings.seed if seed is None else seed)
    backend = backend or detect_backend(seed)
    t0 = time.perf_counter()
    variables = load_variables()
    feats, feature_cols, factor_of = feature_matrix(panel, variables)
    work = panel.copy()
    work = work.drop_duplicates(["iso3_o", "iso3_d", "year"], keep="first")
    for c in feature_cols:
        work[c] = feats.loc[work.index, c]

    y_int = f"y_int_k{split.horizon}"
    y_ext = f"y_ext_k{split.horizon}"

    best_params, cv_table = time_series_cv_select(
        work,
        split.train_feature_years,
        feature_cols,
        horizon=split.horizon,
        backend=backend,
        seed=seed,
    )

    train = work.loc[work["year"].isin(split.train_feature_years)]
    tr_int = train.dropna(subset=[y_int])
    model_int = _make_regressor(backend, best_params, seed)
    model_int.fit(
        tr_int[feature_cols].to_numpy(dtype=float),
        tr_int[y_int].to_numpy(dtype=float),
    )

    model_ext = None
    tr_ext = train.dropna(subset=[y_ext])
    if tr_ext[y_ext].nunique() >= 2:
        model_ext = _make_classifier(backend, best_params, seed)
        model_ext.fit(
            tr_ext[feature_cols].to_numpy(dtype=float),
            tr_ext[y_ext].to_numpy(dtype=float),
        )

    pred_rows = []
    metric_rows = []
    test = work.loc[work["year"].isin(split.test_feature_years)]
    for (origin, year), group in test.groupby(["iso3_o", "year"], sort=True):
        X = group[feature_cols].to_numpy(dtype=float)
        score_int = np.asarray(model_int.predict(X), dtype=float)
        if model_ext is not None:
            if hasattr(model_ext, "predict_proba"):
                score_ext = model_ext.predict_proba(X)[:, 1]
            else:
                score_ext = np.asarray(model_ext.predict(X), dtype=float)
        else:
            score_ext = score_int
        for dest, s_int, s_ext in zip(
            group["iso3_d"].tolist(), score_int, score_ext, strict=False
        ):
            pred_rows.append(
                {
                    "iso3_o": origin,
                    "iso3_d": dest,
                    "year": int(year),
                    "score_int": float(s_int),
                    "score_ext": float(s_ext),
                }
            )
        sc = pd.Series(score_int, index=group["iso3_d"].to_numpy())
        # For AUC use classifier scores when available
        mets = metrics_for_scores(sc, group, horizon=split.horizon)
        if model_ext is not None:
            from imsfe.validation.metrics import auc_ext

            g = group.drop_duplicates("iso3_d", keep="first").set_index("iso3_d")
            sc_ext = pd.Series(score_ext, index=group["iso3_d"].to_numpy())
            sc_ext = sc_ext[~sc_ext.index.duplicated(keep="first")]
            if y_ext in g.columns:
                mets["auc"] = auc_ext(sc_ext, g[y_ext])
        metric_rows.append(
            {
                "origin": origin,
                "year": int(year),
                "method": "ml_gbm",
                "family": "ml",
                **mets,
            }
        )

    runtime = time.perf_counter() - t0
    log = {
        "backend": backend,
        "best_params": best_params,
        "runtime_sec": runtime,
        "seed": seed,
        "n_train_int": int(len(tr_int)),
        "n_train_ext": int(len(tr_ext)),
        "n_features": len(feature_cols),
        "train_years": list(split.train_feature_years),
        "test_years": list(split.test_feature_years),
        "horizon": split.horizon,
    }
    return MLFitResult(
        backend=backend,
        best_params=best_params,
        runtime_sec=runtime,
        model_int=model_int,
        model_ext=model_ext,
        feature_names=feature_cols,
        factor_of=factor_of,
        block_metrics=pd.DataFrame.from_records(metric_rows),
        predictions=pd.DataFrame.from_records(pred_rows),
        cv_table=cv_table,
        log=log,
    )


def shap_mean_abs_by_factor(
    model: Any,
    X: pd.DataFrame,
    factor_of: dict[str, str],
    *,
    max_rows: int = 2000,
    seed: int = 42,
) -> pd.Series:
    """Global mean |SHAP| per feature, then sum within factor and renormalise."""
    import shap

    rng = np.random.default_rng(seed)
    if len(X) > max_rows:
        idx = rng.choice(len(X), size=max_rows, replace=False)
        Xs = X.iloc[idx]
    else:
        Xs = X
    explainer = shap.TreeExplainer(model)
    values = explainer.shap_values(Xs.to_numpy(dtype=float))
    if isinstance(values, list):
        # classifier: take positive class
        values = values[1] if len(values) > 1 else values[0]
    values = np.asarray(values, dtype=float)
    mean_abs = np.mean(np.abs(values), axis=0)
    per_feat = pd.Series(mean_abs, index=list(Xs.columns), dtype=float)
    by_factor: dict[str, float] = {}
    for feat, val in per_feat.items():
        fac = factor_of.get(str(feat), "other")
        by_factor[fac] = by_factor.get(fac, 0.0) + float(val)
    s = pd.Series(by_factor, dtype=float)
    if s.sum() > 0:
        s = s / s.sum()
    return s.sort_values(ascending=False)


def compare_factor_importances(
    shap_factors: pd.Series,
    expert: Weights,
    learned: Weights | None = None,
) -> pd.DataFrame:
    """Side-by-side factor shares: SHAP vs expert vs learned."""
    factors = sorted(
        set(shap_factors.index)
        | set(expert.factors.index)
        | (set(learned.factors.index) if learned is not None else set())
    )
    rows = []
    for f in factors:
        rows.append(
            {
                "factor": f,
                "shap_share": float(shap_factors.get(f, 0.0)),
                "expert_share": float(expert.factors.get(f, 0.0)),
                "learned_share": (
                    float(learned.factors.get(f, 0.0)) if learned is not None else np.nan
                ),
            }
        )
    return pd.DataFrame.from_records(rows)


def plot_f5_factor_importance(
    comparison: pd.DataFrame,
    *,
    stem: str = "F5_shap_vs_weights",
) -> dict[str, Path]:
    """Grouped bar chart: SHAP vs expert vs learned factor shares."""
    df = comparison.sort_values("factor")
    factors = df["factor"].tolist()
    x = np.arange(len(factors), dtype=float)
    width = 0.25
    fig, ax = plt.subplots(figsize=(10, 4.8))
    # Colorblind-safe Wong-ish palette
    ax.bar(x - width, df["shap_share"], width, label="SHAP mean|φ|", color="#0072B2")
    ax.bar(x, df["expert_share"], width, label="Expert factor w", color="#E69F00")
    if df["learned_share"].notna().any():
        ax.bar(
            x + width,
            df["learned_share"].fillna(0.0),
            width,
            label="Learned factor w",
            color="#009E73",
        )
    ax.set_xticks(x)
    ax.set_xticklabels(factors, rotation=30, ha="right")
    ax.set_ylabel("Share (sums to 1 within series)")
    ax.set_title("Factor importance: SHAP vs expert vs learned weights")
    ax.legend(loc="best", fontsize=8)
    ymax = float(
        np.nanmax(df[["shap_share", "expert_share", "learned_share"]].to_numpy(dtype=float))
    )
    ax.set_ylim(0, max(0.01, ymax * 1.15))
    fig.tight_layout()
    out = {}
    png = figures_dir() / f"{stem}.png"
    pdf = figures_dir() / f"{stem}.pdf"
    fig.savefig(png, dpi=300, bbox_inches="tight")
    fig.savefig(pdf, format="pdf", bbox_inches="tight")
    plt.close(fig)
    out["png"] = png
    out["pdf"] = pdf
    return out


def run_ml_benchmark(
    *,
    first_test_year: int = 2019,
    horizon: int = 1,
    n_boot: int | None = None,
    panel_path: Path | None = None,
    learned: Weights | None = None,
    update_t4: bool = True,
) -> dict[str, Any]:
    """Full ML phase: walk-forward metrics, merge into T4, SHAP F5 + CSV."""
    settings = load_settings()
    n_boot = int(settings.bootstrap.n_reps if n_boot is None else n_boot)
    path = panel_path or (processed_dir() / "panel_ijt.parquet")
    panel = pd.read_parquet(path).drop_duplicates(["iso3_o", "iso3_d", "year"], keep="first")
    split = make_split(panel["year"].unique(), first_test_year=first_test_year, horizon=horizon)
    split.assert_no_leakage()

    print("ML backend probe...", flush=True)
    result = run_ml_walkforward(panel, split, seed=settings.seed)
    print(
        f"ML done backend={result.backend} runtime_s={result.runtime_sec:.2f} "
        f"params={result.best_params}",
        flush=True,
    )

    # Persist predictions + log
    pred_path = processed_dir() / "ml_predictions.parquet"
    result.predictions.to_parquet(pred_path, index=False)
    log_path = outputs_tables_dir() / "ml_runtime_log.json"
    log_path.write_text(json.dumps(result.log, indent=2), encoding="utf-8")
    cv_path = outputs_tables_dir() / "ml_cv_hyperparams.csv"
    result.cv_table.to_csv(cv_path, index=False)

    # Bootstrap ML rows and merge into T4
    ml_t4_parts = []
    for metric in ("ndcg@10", "spearman", "precision@10", "auc"):
        if metric not in result.block_metrics.columns:
            continue
        ml_t4_parts.append(
            bootstrap_method_summary(
                result.block_metrics,
                metric=metric,
                n_reps=n_boot,
                seed=settings.bootstrap.seed,
            )
        )
    ml_t4 = pd.concat(ml_t4_parts, ignore_index=True) if ml_t4_parts else pd.DataFrame()
    t4_path = outputs_tables_dir() / "T4_predictive_metrics.csv"
    if update_t4 and t4_path.is_file() and not ml_t4.empty:
        old = pd.read_csv(t4_path)
        old = old.loc[old["method"] != "ml_gbm"]
        t4 = pd.concat([old, ml_t4], ignore_index=True)
        t4.to_csv(t4_path, index=False)
    elif not ml_t4.empty:
        ml_t4.to_csv(t4_path, index=False)
        t4 = ml_t4
    else:
        t4 = pd.DataFrame()

    # Append ML blocks to validation_blocks if present
    blocks_path = processed_dir() / "validation_blocks.parquet"
    if blocks_path.is_file():
        blocks = pd.read_parquet(blocks_path)
        blocks = blocks.loc[blocks["method"] != "ml_gbm"]
        blocks = pd.concat([blocks, result.block_metrics], ignore_index=True)
        blocks.to_parquet(blocks_path, index=False)

    # SHAP on training rows with finite y_int
    print("computing SHAP...", flush=True)
    y_int = f"y_int_k{horizon}"
    train = panel.loc[panel["year"].isin(split.train_feature_years)].dropna(subset=[y_int])
    X_train = train[result.feature_names]
    shap_factors = shap_mean_abs_by_factor(
        result.model_int,
        X_train,
        result.factor_of,
        seed=settings.seed,
    )
    expert = weights_expert_mean()
    if learned is None:
        learned = _load_learned_weights_for_compare()
    comparison = compare_factor_importances(shap_factors, expert, learned)
    shap_csv = outputs_tables_dir() / "T4_shap_factor_importance.csv"
    comparison.to_csv(shap_csv, index=False)
    fig_paths = plot_f5_factor_importance(comparison)

    return {
        "result": result,
        "t4": t4,
        "t4_path": t4_path,
        "shap_csv": shap_csv,
        "figure_paths": fig_paths,
        "log_path": log_path,
        "cv_path": cv_path,
        "pred_path": pred_path,
        "backend": result.backend,
        "runtime_sec": result.runtime_sec,
        "comparison": comparison,
    }
