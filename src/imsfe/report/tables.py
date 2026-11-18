"""Regenerate manuscript tables T1–T9 as CSV + Markdown (no .tex files)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from imsfe.build.descriptives import (
    outputs_tables_dir,
    variable_coverage,
    write_correlation_and_vif,
    write_descriptives,
)
from imsfe.config import config_dir, load_variables
from imsfe.countries import country_name
from imsfe.expert_mapping import load_expert_mapping, unmapped_criteria
from imsfe.report.format_util import write_table_bundle
from imsfe.weights import LEGACY_FACTOR_MAP, weights_expert_mean


def _read_csv(name: str) -> pd.DataFrame | None:
    path = outputs_tables_dir() / name
    if not path.is_file():
        return None
    return pd.read_csv(path)


def build_t1(panel: pd.DataFrame) -> dict[str, Path]:
    variables = load_variables()
    cov = variable_coverage(panel, variables)
    # Enrich with names/notes from YAML
    meta = {v.id: v for v in variables.variables}
    cov["name"] = cov["variable"].map(lambda x: meta[x].name if x in meta else "")
    cov["transform"] = cov["variable"].map(lambda x: meta[x].transform if x in meta else "")
    order = ["variable", "name", "factor", "direction", "source", "transform", "coverage_pct"]
    cov = cov[order]
    return write_table_bundle(
        cov,
        "T1_variables",
        title="T1. Variables, sources, direction, and coverage",
        notes="Coverage is the non-null share of the transformed feature column in the panel.",
        float_cols={"coverage_pct"},
    )


def build_t2() -> dict[str, Path]:
    """Expert weights: mean, SD, CV + Kendall W from weights_expert.yaml."""
    path = config_dir() / "weights_expert.yaml"
    with path.open(encoding="utf-8") as fh:
        expert = yaml.safe_load(fh)
    rows = []
    for factor, stats in expert.get("factors", {}).items():
        mean = float(stats["mean"])
        sd = float(stats["sd"])
        rows.append(
            {
                "level": "factor",
                "id": factor,
                "parent": "",
                "mean": mean,
                "sd": sd,
                "cv": (sd / mean) if mean else float("nan"),
                "min": float(stats["min"]),
                "max": float(stats["max"]),
            }
        )
    for vid, stats in expert.get("variables", {}).items():
        mean = float(stats["mean"])
        sd = float(stats["sd"])
        rows.append(
            {
                "level": "variable",
                "id": vid,
                "parent": str(stats.get("factor", "")),
                "mean": mean,
                "sd": sd,
                "cv": (sd / mean) if mean else float("nan"),
                "min": float(stats["min"]),
                "max": float(stats["max"]),
            }
        )
    df = pd.DataFrame(rows)
    # Mapped IMSFE 2.0 factor weights used in scoring
    w = weights_expert_mean()
    mapped = pd.DataFrame(
        {
            "imsfe_factor": list(w.factors.index),
            "weight": w.factors.to_numpy(),
            "legacy_map": [
                LEGACY_FACTOR_MAP.get(str(f), "(equal residual)") for f in w.factors.index
            ],
        }
    )
    kw = float(expert.get("kendall_w_factors", float("nan")))
    emap = load_expert_mapping()
    unmapped = unmapped_criteria(emap)
    notes = (
        f"Legacy expert panel (n={expert.get('n_experts', '?')}); "
        f"Kendall W on factor ratings = {kw:.4f}. "
        "IMSFE 2.0 factors inherit mapped legacy means; unmapped factors share residual mass. "
        f"Unmapped criteria (expert_mapping.yaml): {', '.join(unmapped) if unmapped else 'none'}."
    )
    paths = write_table_bundle(
        df,
        "T2_expert_weights",
        title="T2. Expert weights (mean, SD, CV) and Kendall W",
        notes=notes,
        float_digits=4,
    )
    # Companion mapping table
    write_table_bundle(
        mapped,
        "T2_expert_weights_mapped",
        title="T2b. IMSFE 2.0 factor weights derived from expert means",
        float_digits=4,
    )
    # Explicit criterion → legacy Excel map (including unmapped)
    crit_rows = []
    meta = {v.id: v for v in load_variables().variables}
    for vid, raw in sorted(emap.items()):
        crit_rows.append(
            {
                "criterion": vid,
                "factor": meta[vid].factor if vid in meta else "",
                "legacy_variables": (
                    "unmapped" if raw == "unmapped" else ", ".join(raw)
                ),
                "mapped": raw != "unmapped",
            }
        )
    write_table_bundle(
        pd.DataFrame(crit_rows),
        "T2_expert_mapping",
        title="T2c. Criterion → legacy Excel variable mapping",
        notes=(
            "Unmapped criteria are listed explicitly. SMAA dispersion for unmapped "
            "uses the empirical SD of mapped experts within the same factor."
        ),
    )
    # Also store Kendall W as a one-row CSV for provenance
    pd.DataFrame(
        [{"statistic": "kendall_w_factors", "value": kw, "n_experts": expert.get("n_experts")}]
    ).to_csv(outputs_tables_dir() / "T2_kendall_w.csv", index=False)
    return paths


def build_t3(panel: pd.DataFrame) -> dict[str, Path]:
    write_descriptives(panel)
    write_correlation_and_vif(panel)
    desc = _read_csv("T3_descriptives.csv")
    paths = {}
    if desc is not None:
        paths.update(
            write_table_bundle(
                desc,
                "T3_descriptives",
                title="T3. Descriptive statistics of transformed features",
                float_digits=3,
            )
        )
    corr = _read_csv("T3_correlation.csv")
    if corr is not None:
        # First column may be index name from to_csv
        paths["T3_correlation_csv"] = outputs_tables_dir() / "T3_correlation.csv"
        write_table_bundle(
            corr,
            "T3_correlation",
            title="T3b. Pearson correlation matrix",
            float_digits=3,
        )
    vif = _read_csv("T3_vif.csv")
    if vif is not None:
        write_table_bundle(
            vif,
            "T3_vif",
            title="T3c. Variance inflation factors",
            float_digits=3,
        )
    return paths


def build_t4() -> dict[str, Path]:
    paths: dict[str, Path] = {}
    t4 = _read_csv("T4_predictive_metrics.csv")
    if t4 is not None:
        paths.update(
            write_table_bundle(
                t4,
                "T4_predictive_metrics",
                title="T4. Predictive validation metrics (bootstrap means and 95% CIs)",
                float_digits=3,
            )
        )
    for stem, title in (
        ("T4_learned_vs_expert_weights", "T4b. Learned vs expert variable weights"),
        ("T4_shap_factor_importance", "T4c. SHAP vs expert vs learned factor shares"),
        ("T4_paired_lift", "T4d. Paired bootstrap lift vs import_volume / gravity / random"),
        ("T4_learned_absent_variables", "T4e. Variables with no training-window data (weight 0)"),
    ):
        df = _read_csv(f"{stem}.csv")
        if df is not None:
            paths.update(write_table_bundle(df, stem, title=title, float_digits=4))
    return paths


def build_t5() -> dict[str, Path]:
    t5 = _read_csv("T5_ppml.csv")
    if t5 is None:
        return {}
    return write_table_bundle(
        t5,
        "T5_ppml",
        title="T5. PPML: scores / factors and exports",
        float_digits=4,
    )


def build_t6() -> dict[str, Path]:
    paths: dict[str, Path] = {}
    for stem, title in (
        ("T6_ablation", "T6. Ablation deltas (fit / competition) with bootstrap CIs"),
        ("T6_ablation_levels", "T6b. Ablation level metrics"),
    ):
        df = _read_csv(f"{stem}.csv")
        if df is not None:
            paths.update(write_table_bundle(df, stem, title=title, float_digits=4))
    return paths


def build_t7() -> dict[str, Path]:
    t7 = _read_csv("T7_robustness.csv")
    if t7 is None:
        return {}
    return write_table_bundle(
        t7,
        "T7_robustness",
        title="T7. Ranking robustness (Kendall τ across normalisation × MCDM × weights)",
        float_digits=3,
    )


def build_t8() -> dict[str, Path]:
    paths: dict[str, Path] = {}
    t8 = _read_csv("T8_smaa_col.csv")
    if t8 is not None:
        if "dest" in t8.columns and "country" not in t8.columns:
            t8 = t8.copy()
            t8.insert(1, "country", t8["dest"].map(lambda x: country_name(str(x))))
        paths.update(
            write_table_bundle(
                t8,
                "T8_smaa_col",
                title="T8. Colombia case: top destinations with SMAA probabilities",
                float_digits=4,
                iso_cols=(),
            )
        )
    sens = _read_csv("T8_smaa_unmapped_dispersion_sensitivity.csv")
    if sens is not None:
        paths.update(
            write_table_bundle(
                sens,
                "T8_smaa_unmapped_dispersion_sensitivity",
                title="T8b. SMAA sensitivity: mapped-factor SD vs fixed CV for unmapped criteria",
                float_digits=4,
            )
        )
    return paths


def build_t9() -> dict[str, Path]:
    """Legacy appendix: original vs corrected rankings."""
    legacy = _read_csv("legacy_comparison.csv")
    if legacy is None:
        # unified scores as fallback
        legacy = _read_csv("legacy_unified_scores.csv")
    if legacy is None:
        return {}
    if "iso3" in legacy.columns and "country" not in legacy.columns:
        legacy = legacy.copy()
        legacy.insert(1, "country", legacy["iso3"].map(lambda x: country_name(str(x))))
    paths = write_table_bundle(
        legacy,
        "T9_legacy_comparison",
        title="T9. Legacy IMSFE ranking: original ratio vs corrected normalisations",
        float_digits=3,
    )
    tau = _read_csv("legacy_kendall_tau.csv")
    if tau is not None:
        write_table_bundle(
            tau,
            "T9_legacy_kendall_tau",
            title="T9b. Kendall τ of corrected rankings vs ratio_legacy",
            float_digits=4,
        )
    return paths


def build_appendix_robustness(df: pd.DataFrame) -> dict[str, Path]:
    return write_table_bundle(
        df,
        "A1_extra_robustness",
        title="A1. Extra robustness: origins, horizons, thresholds, chapters",
        notes=(
            "WSM + minmax + expert_mean. Chapter rows with status=skipped_no_panel "
            "require a separate `imsfe build --chapter` run."
        ),
        float_digits=4,
    )


def regenerate_all_tables(
    panel: pd.DataFrame,
    *,
    robustness: pd.DataFrame | None = None,
) -> dict[str, Any]:
    """Rebuild T1–T9 bundles from panel + existing analysis CSVs."""
    results: dict[str, Any] = {}
    results["T1"] = build_t1(panel)
    results["T2"] = build_t2()
    results["T3"] = build_t3(panel)
    results["T4"] = build_t4()
    results["T5"] = build_t5()
    results["T6"] = build_t6()
    results["T7"] = build_t7()
    results["T8"] = build_t8()
    results["T9"] = build_t9()
    if robustness is not None and not robustness.empty:
        results["A1"] = build_appendix_robustness(robustness)
    return results
