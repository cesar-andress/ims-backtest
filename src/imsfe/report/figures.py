"""Generate manuscript figures (SMAA heatmaps, matrices, metric plots)."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

import matplotlib.pyplot as plt
import numpy as np
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


def plot_smaa_rank_heatmap(
    result: SMAAResult,
    *,
    top_n: int = 15,
    stem: str = "F2_smaa_rank_acceptability",
    max_rank_cols: int = 15,
) -> dict[str, Path]:
    """F2: rank-acceptability heatmap for the top-n deterministic destinations.

    Writes vector PDF and PNG at 300 dpi under ``outputs/figures/``.
    """
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

    out: dict[str, Path] = {}
    png = figures_dir() / f"{stem}.png"
    pdf = figures_dir() / f"{stem}.pdf"
    fig.savefig(png, dpi=300, bbox_inches="tight")
    fig.savefig(pdf, format="pdf", bbox_inches="tight")
    plt.close(fig)
    out["png"] = png
    out["pdf"] = pdf
    return out


def save_placeholder(*_args: Any, **_kwargs: Any) -> None:
    """Reserved for later figure helpers."""
    return None
