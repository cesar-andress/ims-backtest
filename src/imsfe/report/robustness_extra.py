"""Configurable extra robustness sweeps summarised in an appendix table."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from imsfe.build.outcomes import add_outcomes
from imsfe.config import Settings, load_settings, load_variables
from imsfe.validation.backtest import (
    make_split,
    metrics_for_scores,
    score_slice,
)
from imsfe.weights import weights_expert_mean


def _mean_ndcg(
    panel: pd.DataFrame,
    *,
    origin: str | None,
    horizon: int,
    first_test_year: int = 2019,
) -> dict[str, Any]:
    """Mean NDCG@10 for WSM+minmax+expert over walk-forward test blocks."""
    variables = load_variables()
    weights = weights_expert_mean(variables)
    split = make_split(panel["year"].unique(), first_test_year=first_test_year, horizon=horizon)
    vals: list[float] = []
    n_blocks = 0
    for year in split.test_feature_years:
        sub = panel.loc[panel["year"] == int(year)]
        if origin is not None:
            sub = sub.loc[sub["iso3_o"] == origin]
        if sub.empty:
            continue
        for (_, _), group in sub.groupby(["iso3_o", "year"], sort=True):
            sc = score_slice(
                group,
                variables=variables,
                normalization="minmax",
                method="wsm",
                weights=weights,
            )
            if sc.empty:
                continue
            mets = metrics_for_scores(sc, group, horizon=horizon)
            v = mets.get("ndcg@10", float("nan"))
            if np.isfinite(v):
                vals.append(float(v))
                n_blocks += 1
    return {
        "mean_ndcg@10": float(np.mean(vals)) if vals else float("nan"),
        "n_blocks": n_blocks,
    }


def run_extra_robustness(
    panel: pd.DataFrame,
    *,
    settings: Settings | None = None,
    first_test_year: int = 2019,
    origins: list[str] | None = None,
    horizons: list[int] | None = None,
    thresholds: list[float] | None = None,
    chapters: list[str] | None = None,
) -> pd.DataFrame:
    """Sweep origins / horizons / entry thresholds; chapters if present in panel.

    Same scoring pipeline (WSM + minmax + expert). Does not invent chapter
    panels: missing chapters are reported with status skipped.
    """
    settings = settings or load_settings()
    origins = origins or list(settings.origins)
    horizons = horizons or list(settings.horizons)
    thresholds = thresholds or [10_000.0, 50_000.0, 100_000.0]
    chapters = chapters or [
        str(settings.hs_chapters.primary).zfill(2),
        *[str(c).zfill(2) for c in settings.hs_chapters.robustness],
    ]
    present_chapters = (
        set(panel["hs_chapter"].astype(str).str.zfill(2).unique())
        if "hs_chapter" in panel.columns
        else set()
    )

    rows: list[dict[str, Any]] = []
    # Baseline: all origins, primary chapter, default threshold already in panel
    primary = str(settings.hs_chapters.primary).zfill(2)
    base = panel.copy()
    if "hs_chapter" in base.columns:
        base = base.loc[base["hs_chapter"].astype(str).str.zfill(2) == primary]

    for origin in origins:
        for k in horizons:
            stats = _mean_ndcg(
                base, origin=origin, horizon=int(k), first_test_year=first_test_year
            )
            rows.append(
                {
                    "sweep": "origin_horizon",
                    "origin": origin,
                    "hs_chapter": primary,
                    "horizon_k": int(k),
                    "entry_threshold_usd": float(settings.entry_threshold_usd),
                    "status": "ok" if stats["n_blocks"] else "no_blocks",
                    "mean_ndcg@10": stats["mean_ndcg@10"],
                    "n_blocks": stats["n_blocks"],
                }
            )

    for thr in thresholds:
        # Recompute outcomes under alternative entry thresholds (features unchanged).
        alt = add_outcomes(base.drop(
            columns=[c for c in base.columns if c.startswith("y_")], errors="ignore"
        ), threshold=float(thr), horizons=horizons)
        for k in horizons:
            stats = _mean_ndcg(
                alt, origin=None, horizon=int(k), first_test_year=first_test_year
            )
            rows.append(
                {
                    "sweep": "threshold",
                    "origin": "ALL",
                    "hs_chapter": primary,
                    "horizon_k": int(k),
                    "entry_threshold_usd": float(thr),
                    "status": "ok" if stats["n_blocks"] else "no_blocks",
                    "mean_ndcg@10": stats["mean_ndcg@10"],
                    "n_blocks": stats["n_blocks"],
                }
            )

    for ch in chapters:
        if ch not in present_chapters:
            rows.append(
                {
                    "sweep": "chapter",
                    "origin": "ALL",
                    "hs_chapter": ch,
                    "horizon_k": 1,
                    "entry_threshold_usd": float(settings.entry_threshold_usd),
                    "status": "skipped_no_panel",
                    "mean_ndcg@10": float("nan"),
                    "n_blocks": 0,
                }
            )
            continue
        if ch == primary:
            # Already covered above; still record a chapter-level ALL-origin row.
            stats = _mean_ndcg(
                base, origin=None, horizon=1, first_test_year=first_test_year
            )
            rows.append(
                {
                    "sweep": "chapter",
                    "origin": "ALL",
                    "hs_chapter": ch,
                    "horizon_k": 1,
                    "entry_threshold_usd": float(settings.entry_threshold_usd),
                    "status": "ok",
                    "mean_ndcg@10": stats["mean_ndcg@10"],
                    "n_blocks": stats["n_blocks"],
                }
            )
            continue
        sub = panel.loc[panel["hs_chapter"].astype(str).str.zfill(2) == ch]
        stats = _mean_ndcg(sub, origin=None, horizon=1, first_test_year=first_test_year)
        rows.append(
            {
                "sweep": "chapter",
                "origin": "ALL",
                "hs_chapter": ch,
                "horizon_k": 1,
                "entry_threshold_usd": float(settings.entry_threshold_usd),
                "status": "ok" if stats["n_blocks"] else "no_blocks",
                "mean_ndcg@10": stats["mean_ndcg@10"],
                "n_blocks": stats["n_blocks"],
            }
        )

    return pd.DataFrame.from_records(rows)
