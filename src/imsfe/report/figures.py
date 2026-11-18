"""Generate manuscript figures F1–F5 (PNG + PDF)."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

from imsfe.config import project_root

if TYPE_CHECKING:
    from imsfe.smaa import SMAAResult

# Wong / IBM colorblind-safe sequential (light → dark blue-teal).
_CB_COLORS = ["#f7fbff", "#c6dbef", "#6baed6", "#2171b5", "#08306b"]
_CB_CMAP = LinearSegmentedColormap.from_list("imsfe_cb", _CB_COLORS)


def figures_dir() -> Path:
    path = project_root() / "outputs" / "figures"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _save_fig(fig: plt.Figure, stem: str) -> dict[str, Path]:
    png = figures_dir() / f"{stem}.png"
    pdf = figures_dir() / f"{stem}.pdf"
    fig.savefig(png, dpi=300, bbox_inches="tight")
    fig.savefig(pdf, format="pdf", bbox_inches="tight")
    plt.close(fig)
    return {"png": png, "pdf": pdf}


def plot_framework_diagram(stem: str = "F1_framework") -> dict[str, Path]:
    """F1: screening → criteria → weights → normalisation/MCDM → backtest → matrix."""
    stages = [
        ("Screening", "Origins, HS chapter,\ntop-N destinations"),
        ("Criteria", "Demand, logistics,\nfit, risk, …"),
        ("Weights", "Expert / learned\n/ SMAA"),
        ("Norm + MCDM", "Min-max + WSM\n(TOPSIS/VIKOR/…)"),
        ("Backtest", "Walk-forward\nNDCG / PPML"),
        ("Strategic matrix", "Attractiveness\n× fit (F3)"),
    ]
    fig, ax = plt.subplots(figsize=(11.5, 3.2))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3)
    ax.axis("off")
    ax.set_title("IMSFE 2.0 analytical framework", fontsize=12, pad=8)
    box_w, box_h = 1.7, 1.6
    y = 0.7
    for i, (title, body) in enumerate(stages):
        x = 0.35 + i * 1.95
        rect = mpatches.FancyBboxPatch(
            (x, y),
            box_w,
            box_h,
            boxstyle="round,pad=0.04,rounding_size=0.15",
            facecolor="#DDEEFF",
            edgecolor="#0072B2",
            linewidth=1.2,
        )
        ax.add_patch(rect)
        ax.text(
            x + box_w / 2,
            y + box_h * 0.72,
            title,
            ha="center",
            va="center",
            fontsize=9,
            fontweight="bold",
        )
        ax.text(
            x + box_w / 2,
            y + box_h * 0.32,
            body,
            ha="center",
            va="center",
            fontsize=7.5,
            color="#333333",
        )
        if i < len(stages) - 1:
            ax.annotate(
                "",
                xy=(x + box_w + 0.18, y + box_h / 2),
                xytext=(x + box_w + 0.02, y + box_h / 2),
                arrowprops=dict(arrowstyle="->", color="#333333", lw=1.2),
            )
    return _save_fig(fig, stem)


def plot_smaa_rank_heatmap(
    result: SMAAResult,
    *,
    top_n: int = 15,
    stem: str = "F2_smaa_rank_acceptability",
    max_rank_cols: int = 15,
) -> dict[str, Path]:
    """F2: rank-acceptability heatmap for the top-n deterministic destinations."""
    order = result.deterministic_ranks.sort_values().index.tolist()[:top_n]
    idx = [result.alternatives.index(a) for a in order]
    n_ranks = min(max_rank_cols, result.acceptability.shape[1])
    mat = result.acceptability[np.ix_(idx, list(range(n_ranks)))]

    fig_h = max(4.0, 0.35 * len(order) + 1.5)
    fig, ax = plt.subplots(figsize=(8.5, fig_h))
    im = ax.imshow(mat, aspect="auto", cmap=_CB_CMAP, vmin=0.0, vmax=1.0)
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels(order)
    ax.set_xticks(range(n_ranks))
    ax.set_xticklabels([str(r) for r in range(1, n_ranks + 1)])
    ax.set_xlabel("Rank r")
    ax.set_ylabel("Destination")
    ax.set_title("SMAA rank acceptability $b_j^r$ (top destinations)")
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label(r"$b_j^r = P(\mathrm{rank}=r)$")
    fig.tight_layout()
    return _save_fig(fig, stem)


def plot_f4_from_blocks(
    blocks: pd.DataFrame,
    *,
    stem: str = "F4_ndcg_by_year",
) -> dict[str, Path]:
    """F4: mean NDCG@10 by year for selected methods."""
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
    return _save_fig(fig, stem)


def plot_f5_from_shap_csv(
    comparison: pd.DataFrame,
    *,
    stem: str = "F5_shap_vs_weights",
) -> dict[str, Path]:
    """F5 grouped bars from T4_shap_factor_importance.csv schema."""
    df = comparison.sort_values("factor")
    factors = df["factor"].tolist()
    x = np.arange(len(factors), dtype=float)
    width = 0.25
    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.bar(x - width, df["shap_share"], width, label="SHAP mean|φ|", color="#0072B2")
    ax.bar(x, df["expert_share"], width, label="Expert factor w", color="#E69F00")
    if "learned_share" in df.columns and df["learned_share"].notna().any():
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
    cols = [c for c in ("shap_share", "expert_share", "learned_share") if c in df.columns]
    ymax = float(np.nanmax(df[cols].to_numpy(dtype=float)))
    ax.set_ylim(0, max(0.01, ymax * 1.15))
    fig.tight_layout()
    return _save_fig(fig, stem)


def save_placeholder(*_args: Any, **_kwargs: Any) -> None:
    """Reserved."""
    return None
