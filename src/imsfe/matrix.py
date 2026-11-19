"""Attractiveness × product-market fit strategic matrix (SPEC §3.5).

Main configuration: hierarchical WSM + minmax + expert weights, scores on 0–10.
Missing criteria use the shared block missing-data policy (exclude if >20% missing,
median-impute the rest); candidate destinations are never dropped. No
silent imputation. Time-invariant dyadic gaps in late BACI years are reported
in the coverage table.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from adjustText import adjust_text

from imsfe.build.descriptives import outputs_tables_dir
from imsfe.build.panel import processed_dir
from imsfe.config import VariablesConfig, load_settings, load_variables, project_root
from imsfe.legacy import LEGACY_EXCEL_REL
from imsfe.mcdm import hierarchical_wsm
from imsfe.normalize import normalize_matrix
from imsfe.report.figures import figures_dir
from imsfe.run_experiments import _directions, score_origin_year
from imsfe.weights import Weights, weights_expert_mean

CutoffMode = Literal["median", "fixed5"]

# Attractiveness factors (SPEC §3.5 / Phase-8 prompt).
ATTRACTIVENESS_FACTORS: tuple[str, ...] = (
    "demand",
    "logistics",
    "institutional",
    "macro_risk",
)

# Fit variables: product-market fit + cost/access (prompt; LANG included).
FIT_VARIABLES: tuple[str, ...] = ("UVGAP", "CULT", "LANG", "DIST", "TARIF", "FTA")

# Dyadic traits treated as time-invariant for the case year when CEPII ends
# earlier than BACI. Fill is last observation with year <= case year; logged.
TIME_INVARIANT_FIT: tuple[str, ...] = ("DIST", "LANG", "FTA", "CULT")

QUADRANT_ORDER: tuple[str, ...] = (
    "Global Leaders",
    "Niche Markets",
    "Emerging Opportunities",
    "Challenging Markets",
)


@dataclass(frozen=True)
class QuadrantCopy:
    """Legacy Figure-3 strategy texts with axes adapted to Attractiveness × Fit."""

    name: str
    description: str
    strategy: str


def _legacy_excel_path() -> Path:
    return (project_root() / LEGACY_EXCEL_REL).resolve()


def load_quadrant_strategy_texts(
    excel_path: Path | None = None,
) -> dict[str, QuadrantCopy]:
    """Read Cruce Inglés quadrant prose; adapt IMSFE/EOC wording to Attract/Fit."""
    from openpyxl import load_workbook

    path = excel_path or _legacy_excel_path()
    if not path.is_file():
        raise FileNotFoundError(f"Legacy Excel not found (read-only): {path}")
    wb = load_workbook(path, data_only=True, read_only=True)
    if "Cruce Inglés" not in wb.sheetnames:
        raise ValueError("Sheet 'Cruce Inglés' missing from legacy Excel")
    ws = wb["Cruce Inglés"]

    def cell(coord: str) -> str:
        v = ws[coord].value
        return "" if v is None else str(v).strip()

    # Layout: B/C × rows 2–9 (HIGH/LOW IMSFE × LOW/HIGH EOC).
    raw = {
        "Niche Markets": (cell("B3"), cell("B5")),
        "Global Leaders": (cell("C3"), cell("C5")),
        "Challenging Markets": (cell("B7"), cell("B9")),
        "Emerging Opportunities": (cell("C7"), cell("C9")),
    }
    wb.close()

    def adapt(text: str) -> str:
        """Replace legacy axis names; keep strategy substance unchanged."""
        repl = (
            ("high economic openness", "high product-market fit"),
            ("High economic openness", "High product-market fit"),
            ("low economic openness", "low product-market fit"),
            ("Low economic openness", "Low product-market fit"),
            ("economic openness", "product-market fit"),
            ("Economic openness", "Product-market fit"),
            ("trade openness", "product-market fit"),
            ("Trade openness", "Product-market fit"),
            ("less economically open", "lower product-market fit"),
            ("Less economically open", "Lower product-market fit"),
            ("HIGH EOC", "HIGH FIT"),
            ("LOW EOC", "LOW FIT"),
            ("HIGH IMSFE", "HIGH ATTRACTIVENESS"),
            ("LOW IMSFE", "LOW ATTRACTIVENESS"),
            ("IMSFE", "market attractiveness"),
            ("EOC", "product-market fit"),
        )
        out = text
        for a, b in repl:
            out = out.replace(a, b)
        return out

    return {
        name: QuadrantCopy(
            name=name,
            description=adapt(desc),
            strategy=adapt(strat),
        )
        for name, (desc, strat) in raw.items()
    }


def _variable_ids_for_factors(
    variables: VariablesConfig, factors: tuple[str, ...]
) -> list[str]:
    wanted = set(factors)
    return [v.id for v in variables.variables if v.factor in wanted]


def _axis_score(
    group: pd.DataFrame,
    variable_ids: list[str],
    *,
    variables: VariablesConfig,
    weights: Weights,
    normalization: str = "minmax",
) -> tuple[pd.Series, list[str], list[str]]:
    """Hierarchical WSM on a variable subset; returns scores in ~[0, 10]."""
    from imsfe.block_prep import prepare_block

    directions = _directions(variables)
    present = [v for v in variable_ids if v in group.columns]
    prep = prepare_block(group, present)
    complete = prep.matrix
    usable = prep.used_variables
    dropped = [v for v in variable_ids if v not in usable]
    if complete.empty or len(complete) < 2 or not usable:
        return pd.Series(dtype=float), usable, dropped
    dirs = {c: directions[c] for c in usable}
    w = weights.restrict(usable)
    normalized = normalize_matrix(complete, dirs, normalization)  # type: ignore[arg-type]
    scores = hierarchical_wsm(normalized, w)
    scores.name = "score"
    return scores, usable, dropped


def assign_quadrant(
    attractiveness: float,
    fit: float,
    *,
    attr_cut: float,
    fit_cut: float,
) -> str:
    """2×2 labels: high/low Attractiveness × high/low Fit."""
    high_a = attractiveness >= attr_cut
    high_f = fit >= fit_cut
    if high_a and high_f:
        return "Global Leaders"
    if high_a and not high_f:
        return "Niche Markets"
    if (not high_a) and high_f:
        return "Emerging Opportunities"
    return "Challenging Markets"


def fill_time_invariant_fit(
    group: pd.DataFrame,
    history: pd.DataFrame,
    year: int,
    *,
    variables: tuple[str, ...] = TIME_INVARIANT_FIT,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Last-observation fill for static dyadic fit vars (year <= case year).

    Does not invent values: only copies an earlier observed (origin, dest) cell.
    Returns the filled group and a coverage dict (n_filled / source years).
    """
    out = group.copy()
    report: dict[str, Any] = {}
    hist = history.loc[history["year"] <= int(year)].sort_values("year")
    for vid in variables:
        if vid not in out.columns:
            report[vid] = {"n_filled": 0, "reason": "column_absent"}
            continue
        missing = out[vid].isna()
        n_miss = int(missing.sum())
        if n_miss == 0 or vid not in hist.columns:
            report[vid] = {"n_filled": 0, "n_missing": n_miss}
            continue
        filled = 0
        src_years: list[int] = []
        for idx, row in out.loc[missing].iterrows():
            d = row["iso3_d"]
            past = hist.loc[
                (hist["iso3_d"] == d) & hist[vid].notna(), ["year", vid]
            ]
            if past.empty:
                continue
            last = past.iloc[-1]
            out.at[idx, vid] = float(last[vid])
            filled += 1
            src_years.append(int(last["year"]))
        report[vid] = {
            "n_filled": filled,
            "n_missing_before": n_miss,
            "source_year_min": int(min(src_years)) if src_years else None,
            "source_year_max": int(max(src_years)) if src_years else None,
        }
    return out, report


def compute_strategic_matrix(
    panel: pd.DataFrame,
    *,
    origin: str = "COL",
    year: int | None = None,
    normalization: str = "minmax",
    weight_scheme: str = "expert_mean",
    variables: VariablesConfig | None = None,
    fill_invariant_fit: bool = True,
) -> pd.DataFrame:
    """Attractiveness and fit scores (0–10) plus both cutoff quadrant labels."""
    variables = variables or load_variables()
    if weight_scheme != "expert_mean":
        raise ValueError("Case study uses expert_mean weights only")
    weights = weights_expert_mean(variables)
    sub = panel.loc[panel["iso3_o"] == origin]
    if sub.empty:
        raise ValueError(f"No panel rows for origin {origin}")
    if year is None:
        year = int(sub["year"].max())
    group = sub.loc[sub["year"] == int(year)].copy()
    if group.empty:
        raise ValueError(f"No panel rows for {origin}/{year}")

    locf_report: dict[str, Any] = {}
    if fill_invariant_fit:
        group, locf_report = fill_time_invariant_fit(group, sub, int(year))

    attr_ids = _variable_ids_for_factors(variables, ATTRACTIVENESS_FACTORS)
    fit_ids = list(FIT_VARIABLES)

    attr_sc, attr_used, attr_dropped = _axis_score(
        group, attr_ids, variables=variables, weights=weights, normalization=normalization
    )
    fit_sc, fit_used, fit_dropped = _axis_score(
        group, fit_ids, variables=variables, weights=weights, normalization=normalization
    )
    common = attr_sc.index.intersection(fit_sc.index)
    if len(common) < 2:
        raise RuntimeError(
            f"Insufficient destinations with both axis scores for {origin}/{year} "
            f"(attr_used={attr_used}, fit_used={fit_used})"
        )

    # Overall main-config ranking (full variable set, same prep as experiments).
    overall = score_origin_year(
        group,
        variables=variables,
        normalization=normalization,
        method="wsm",
        weight_scheme="expert_mean",
    ).set_index("dest")

    dest = group.set_index("iso3_d")
    rows = []
    for d in common:
        a = float(attr_sc.loc[d])
        f = float(fit_sc.loc[d])
        impv = float(dest.loc[d, "IMPV_raw"]) if "IMPV_raw" in dest.columns else np.nan
        if pd.isna(impv) and "IMPV" in dest.columns:
            impv = float(dest.loc[d, "IMPV"])
        x = float(dest.loc[d, "X_ijt"]) if "X_ijt" in dest.columns else np.nan
        grw = float(dest.loc[d, "GRW_raw"]) if "GRW_raw" in dest.columns else np.nan
        ow = float(overall.loc[d, "score"]) if d in overall.index else np.nan
        orank = int(overall.loc[d, "rank"]) if d in overall.index else np.nan
        rows.append(
            {
                "origin": origin,
                "year": int(year),
                "dest": str(d),
                "attractiveness": a,
                "fit": f,
                "composite": (a + f) / 2.0,
                "overall_score": ow,
                "overall_rank": orank,
                "IMPV_raw": impv,
                "X_ijt": x,
                "GRW_raw": grw,
                "quadrant_median": assign_quadrant(
                    a,
                    f,
                    attr_cut=float(np.median(attr_sc.loc[common])),
                    fit_cut=float(np.median(fit_sc.loc[common])),
                ),
                "quadrant_fixed5": assign_quadrant(a, f, attr_cut=5.0, fit_cut=5.0),
            }
        )
    out = pd.DataFrame.from_records(rows).sort_values(
        ["overall_rank", "composite"], ascending=[True, False]
    )
    out.attrs["attr_used"] = list(attr_used)
    out.attrs["attr_dropped"] = list(attr_dropped)
    out.attrs["fit_used"] = list(fit_used)
    out.attrs["fit_dropped"] = list(fit_dropped)
    out.attrs["attr_cut_median"] = float(np.median(attr_sc.loc[common]))
    out.attrs["fit_cut_median"] = float(np.median(fit_sc.loc[common]))
    out.attrs["locf_fit"] = locf_report
    return out


def bilateral_export_growth(
    panel: pd.DataFrame,
    origin: str,
    dests: list[str],
    year: int,
    *,
    lag: int = 3,
) -> pd.Series:
    """log(X_t+1)−log(X_{t−lag}+1) for origin→dest when both years exist."""
    cur = panel.loc[
        (panel["iso3_o"] == origin) & (panel["year"] == year) & (panel["iso3_d"].isin(dests))
    ].set_index("iso3_d")["X_ijt"]
    past = panel.loc[
        (panel["iso3_o"] == origin)
        & (panel["year"] == year - lag)
        & (panel["iso3_d"].isin(dests))
    ].set_index("iso3_d")["X_ijt"]
    out = {}
    for d in dests:
        if d not in cur.index or d not in past.index:
            out[d] = np.nan
            continue
        x1 = float(cur.loc[d])
        x0 = float(past.loc[d])
        if not np.isfinite(x1) or not np.isfinite(x0):
            out[d] = np.nan
        else:
            out[d] = float(np.log(x1 + 1.0) - np.log(x0 + 1.0))
    return pd.Series(out, dtype=float, name="export_growth_log")


def build_recommendation_table(
    matrix: pd.DataFrame,
    panel: pd.DataFrame,
    *,
    top_n: int = 10,
    quadrant_col: str = "quadrant_median",
) -> pd.DataFrame:
    """Side-by-side recommended (overall WSM top-n) vs actual (X_ijt top-n)."""
    origin = str(matrix["origin"].iloc[0])
    year = int(matrix["year"].iloc[0])
    ranked = matrix.sort_values("overall_rank", ascending=True)
    recommended = ranked.head(top_n)["dest"].tolist()
    actual = (
        matrix.sort_values("X_ijt", ascending=False).head(top_n)["dest"].tolist()
    )
    growth = bilateral_export_growth(panel, origin, list(set(recommended + actual)), year)

    def rows_for(kind: str, dests: list[str]) -> list[dict[str, Any]]:
        rows = []
        for i, d in enumerate(dests, start=1):
            m = matrix.loc[matrix["dest"] == d].iloc[0]
            rows.append(
                {
                    "origin": origin,
                    "year": year,
                    "list": kind,
                    "list_rank": i,
                    "dest": d,
                    "overall_rank": int(m["overall_rank"])
                    if pd.notna(m["overall_rank"])
                    else np.nan,
                    "overall_score": float(m["overall_score"])
                    if pd.notna(m["overall_score"])
                    else np.nan,
                    "attractiveness": float(m["attractiveness"]),
                    "fit": float(m["fit"]),
                    "quadrant": str(m[quadrant_col]),
                    "export_value_usd": float(m["X_ijt"]) if pd.notna(m["X_ijt"]) else np.nan,
                    "export_growth_log_3y": float(growth.get(d, np.nan))
                    if d in growth.index
                    else np.nan,
                    "dest_import_cagr_3y": float(m["GRW_raw"])
                    if pd.notna(m["GRW_raw"])
                    else np.nan,
                    "in_other_list": d in (actual if kind == "recommended" else recommended),
                }
            )
        return rows

    return pd.DataFrame.from_records(
        rows_for("recommended", recommended) + rows_for("actual", actual)
    )


def plot_f3_matrix(
    matrix: pd.DataFrame,
    *,
    cutoff: CutoffMode = "median",
    stem: str = "F3_attractiveness_fit_matrix",
    actual_top_n: int = 10,
) -> dict[str, Path]:
    """Scatter: fit (X) × attractiveness (Y); bubble = IMPV; mark actual top-n."""
    df = matrix.copy()
    if cutoff == "median":
        attr_cut = float(df["attractiveness"].median())
        fit_cut = float(df["fit"].median())
        qcol = "quadrant_median"
    else:
        attr_cut = 5.0
        fit_cut = 5.0
        qcol = "quadrant_fixed5"

    actual = set(
        df.sort_values("X_ijt", ascending=False).head(actual_top_n)["dest"].tolist()
    )
    sizes = df["IMPV_raw"].to_numpy(dtype=float)
    sizes = np.where(np.isfinite(sizes) & (sizes > 0), sizes, np.nan)
    if np.isfinite(sizes).any():
        s_plot = 40.0 + 200.0 * (sizes / np.nanmax(sizes))
        s_plot = np.where(np.isfinite(s_plot), s_plot, 40.0)
    else:
        s_plot = np.full(len(df), 60.0)

    fig, ax = plt.subplots(figsize=(9.5, 7.2))
    is_act = df["dest"].isin(actual)
    ax.scatter(
        df.loc[~is_act, "fit"],
        df.loc[~is_act, "attractiveness"],
        s=s_plot[~is_act.to_numpy()],
        c="#56B4E9",
        alpha=0.75,
        edgecolors="#0072B2",
        linewidths=0.6,
        label="Other destinations",
        zorder=2,
    )
    ax.scatter(
        df.loc[is_act, "fit"],
        df.loc[is_act, "attractiveness"],
        s=s_plot[is_act.to_numpy()],
        c="#E69F00",
        marker="D",
        alpha=0.9,
        edgecolors="#000000",
        linewidths=0.8,
        label=f"Actual top-{actual_top_n} by X_ijt",
        zorder=3,
    )
    ax.axvline(fit_cut, color="#333333", ls="--", lw=1.0, zorder=1)
    ax.axhline(attr_cut, color="#333333", ls="--", lw=1.0, zorder=1)

    # Corner labels (adapted legacy names)
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    # Expand a bit for labels
    ax.set_xlim(min(0.0, xlim[0] - 0.2), max(10.0, xlim[1] + 0.2))
    ax.set_ylim(min(0.0, ylim[0] - 0.2), max(10.0, ylim[1] + 0.2))
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    label_style = dict(fontsize=8, fontweight="bold", ha="center", va="center", alpha=0.85)
    ax.text((fit_cut + x1) / 2, (attr_cut + y1) / 2, "Global Leaders", **label_style)
    ax.text((x0 + fit_cut) / 2, (attr_cut + y1) / 2, "Niche Markets", **label_style)
    ax.text(
        (fit_cut + x1) / 2,
        (y0 + attr_cut) / 2,
        "Emerging Opportunities",
        **label_style,
    )
    ax.text(
        (x0 + fit_cut) / 2,
        (y0 + attr_cut) / 2,
        "Challenging Markets",
        **label_style,
    )

    texts = []
    for _, row in df.iterrows():
        texts.append(
            ax.text(
                float(row["fit"]),
                float(row["attractiveness"]),
                str(row["dest"]),
                fontsize=7,
                ha="center",
                va="center",
            )
        )
    adjust_text(
        texts,
        ax=ax,
        arrowprops=dict(arrowstyle="-", color="gray", lw=0.4),
        expand=(1.15, 1.25),
        force_text=(0.4, 0.6),
    )

    origin = str(df["origin"].iloc[0])
    year = int(df["year"].iloc[0])
    ax.set_xlabel("Product-market fit (0–10)")
    ax.set_ylabel("Market attractiveness (0–10)")
    ax.set_title(
        f"{origin} HS64 {year}: attractiveness × fit "
        f"(cut-offs: attract={attr_cut:.2f}, fit={fit_cut:.2f}; {cutoff})"
    )
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()

    _ = qcol  # selected quadrant rule (median vs fixed5) encoded in stem/title
    png = figures_dir() / f"{stem}.png"
    pdf = figures_dir() / f"{stem}.pdf"
    fig.savefig(png, dpi=300, bbox_inches="tight")
    fig.savefig(pdf, format="pdf", bbox_inches="tight")
    plt.close(fig)
    return {"png": png, "pdf": pdf}


def write_quadrant_guidebook(path: Path | None = None) -> Path:
    """CSV of adapted legacy quadrant descriptions/strategies."""
    texts = load_quadrant_strategy_texts()
    rows = [
        {
            "quadrant": q,
            "description": texts[q].description,
            "strategy": texts[q].strategy,
        }
        for q in QUADRANT_ORDER
        if q in texts
    ]
    out = path or (outputs_tables_dir() / "case_quadrant_strategies.csv")
    pd.DataFrame(rows).to_csv(out, index=False)
    return out


def run_case_study(
    *,
    origin: str = "COL",
    year: int | None = None,
    panel_path: Path | None = None,
    top_n: int = 10,
) -> dict[str, Any]:
    """Build matrix scores, F3, recommendation table, and coverage log."""
    settings = load_settings()
    path = panel_path or (processed_dir() / "panel_ijt.parquet")
    panel = pd.read_parquet(path).drop_duplicates(["iso3_o", "iso3_d", "year"], keep="first")
    # Chapter filter if present
    primary = str(settings.hs_chapters.primary).zfill(2)
    if "hs_chapter" in panel.columns:
        panel = panel.loc[panel["hs_chapter"].astype(str).str.zfill(2) == primary]

    matrix = compute_strategic_matrix(panel, origin=origin, year=year)
    year_used = int(matrix["year"].iloc[0])
    compare = build_recommendation_table(matrix, panel, top_n=top_n)

    matrix_path = outputs_tables_dir() / "case_matrix_scores.csv"
    matrix.to_csv(matrix_path, index=False)
    # SPEC T9 is the legacy appendix; case contrast uses a dedicated filename.
    compare_path = outputs_tables_dir() / "case_recommended_vs_actual.csv"
    compare.to_csv(compare_path, index=False)

    guide_path = write_quadrant_guidebook()
    fig_paths = plot_f3_matrix(matrix, cutoff="median", stem="F3_attractiveness_fit_matrix")
    # Also emit fixed-5 variant figure
    fig_paths_5 = plot_f3_matrix(
        matrix, cutoff="fixed5", stem="F3_attractiveness_fit_matrix_fixed5"
    )

    coverage = {
        "origin": origin,
        "year": year_used,
        "hs_chapter": primary,
        "n_destinations": int(len(matrix)),
        "attr_used": matrix.attrs.get("attr_used"),
        "attr_dropped": matrix.attrs.get("attr_dropped"),
        "fit_used": matrix.attrs.get("fit_used"),
        "fit_dropped": matrix.attrs.get("fit_dropped"),
        "attr_cut_median": matrix.attrs.get("attr_cut_median"),
        "fit_cut_median": matrix.attrs.get("fit_cut_median"),
        "locf_fit": matrix.attrs.get("locf_fit"),
        "normalization": "minmax",
        "weights": "expert_mean",
        "method": "wsm",
    }
    cov_path = outputs_tables_dir() / "case_matrix_coverage.json"
    cov_path.write_text(json.dumps(coverage, indent=2), encoding="utf-8")

    return {
        "matrix": matrix,
        "compare": compare,
        "matrix_path": matrix_path,
        "compare_path": compare_path,
        "guide_path": guide_path,
        "coverage_path": cov_path,
        "figure_paths": fig_paths,
        "figure_paths_fixed5": fig_paths_5,
        "coverage": coverage,
        "origin": origin,
        "year": year_used,
    }
