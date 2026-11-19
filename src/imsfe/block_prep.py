"""Fixed candidate-set preparation for origin-year scoring blocks.

Rules
-----
1. The candidate set is every destination present in the (origin, year) panel
   slice — never drop destinations because a criterion is missing.
2. A variable with missing share strictly greater than ``max_missing_share`` in
   the block is excluded for that block (weights renormalised).
3. Remaining NaNs are imputed with the block median; imputed cells are flagged.
4. Fail loudly if ``n_candidates < min_candidates``.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from imsfe.config import MissingDataSettings, Settings, load_settings


@dataclass
class PreparedBlock:
    """Prepared feature matrix for one origin-year block."""

    matrix: pd.DataFrame
    candidates: list[str]
    used_variables: list[str]
    excluded_variables: list[str]
    n_candidates: int
    n_imputed_cells: int
    imputed_mask: pd.DataFrame
    notes: tuple[str, ...] = field(default_factory=tuple)


class InsufficientCandidatesError(RuntimeError):
    """Raised when a scoring block has fewer destinations than required."""


def prepare_block(
    group: pd.DataFrame,
    columns: list[str],
    *,
    settings: Settings | None = None,
    missing: MissingDataSettings | None = None,
) -> PreparedBlock:
    """Prepare a fixed candidate set with variable exclusion and median impute.

    Parameters
    ----------
    group
        Origin-year slice with column ``iso3_d`` and feature columns.
    columns
        Candidate feature ids (typically all IMS variables).
    """
    settings = settings or load_settings()
    policy = missing or settings.missing_data
    dest = group.drop_duplicates("iso3_d", keep="first").set_index("iso3_d")
    candidates = [str(i) for i in dest.index.tolist()]
    n_cand = len(candidates)
    if n_cand < int(policy.min_candidates):
        raise InsufficientCandidatesError(
            f"n_candidates={n_cand} < min_candidates={policy.min_candidates} "
            f"for block with destinations={candidates[:5]}…"
        )

    present_cols = [c for c in columns if c in dest.columns]
    raw = dest[present_cols].apply(pd.to_numeric, errors="coerce")

    excluded: list[str] = []
    used: list[str] = []
    notes: list[str] = []
    for c in present_cols:
        miss = float(raw[c].isna().mean()) if len(raw) else 1.0
        if miss > float(policy.max_missing_share):
            excluded.append(c)
            notes.append(
                f"exclude {c}: missing_share={miss:.3f} > {policy.max_missing_share}"
            )
        elif not raw[c].notna().any():
            excluded.append(c)
            notes.append(f"exclude {c}: all missing")
        else:
            used.append(c)

    if not used:
        raise RuntimeError(
            f"No usable variables after missing-share filter "
            f"(excluded={excluded})"
        )

    mat = raw[used].copy()
    imputed_mask = pd.DataFrame(False, index=mat.index, columns=used)
    n_imputed = 0
    if policy.impute == "median":
        for c in used:
            col = mat[c]
            miss = col.isna()
            if not miss.any():
                continue
            med = float(col.median())
            if not np.isfinite(med):
                # All-NaN should have been excluded; defensive zero.
                med = 0.0
            mat.loc[miss, c] = med
            imputed_mask.loc[miss, c] = True
            n_imputed += int(miss.sum())
            notes.append(f"impute {c}: n={int(miss.sum())} median={med:.6g}")
    else:
        raise ValueError(f"Unknown impute policy: {policy.impute}")

    # All candidates retained; no row drops.
    assert len(mat) == n_cand
    assert mat.isna().sum().sum() == 0

    return PreparedBlock(
        matrix=mat,
        candidates=candidates,
        used_variables=used,
        excluded_variables=excluded,
        n_candidates=n_cand,
        n_imputed_cells=n_imputed,
        imputed_mask=imputed_mask,
        notes=tuple(notes),
    )


def block_meta_dict(prep: PreparedBlock) -> dict[str, object]:
    """Compact metadata for validation block logs."""
    return {
        "n_candidates": prep.n_candidates,
        "n_imputed_cells": prep.n_imputed_cells,
        "excluded_variables": ",".join(prep.excluded_variables),
        "used_variables": ",".join(prep.used_variables),
        "n_excluded_variables": len(prep.excluded_variables),
    }
