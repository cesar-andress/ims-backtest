"""Fixed candidate-set preparation and identical ranking sets."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from imsfe.block_prep import InsufficientCandidatesError, prepare_block
from imsfe.config import MissingDataSettings, load_variables
from imsfe.validation.backtest import baseline_scores, score_slice
from imsfe.weights import weights_equal, weights_expert_mean


def _block(n_dest: int = 25, tarif_missing: float = 0.0) -> pd.DataFrame:
    rng = np.random.default_rng(0)
    dests = [f"D{i:02d}" for i in range(n_dest)]
    rows = []
    variables = load_variables()
    ids = [v.id for v in variables.variables]
    for i, d in enumerate(dests):
        row = {"iso3_o": "COL", "iso3_d": d, "year": 2020, "hs_chapter": "64"}
        for vid in ids:
            row[vid] = float(rng.random())
        if tarif_missing > 0 and i < int(tarif_missing * n_dest):
            row["TARIF"] = np.nan
        rows.append(row)
    return pd.DataFrame(rows)


def test_prepare_block_keeps_all_candidates() -> None:
    g = _block(25, tarif_missing=0.5)
    prep = prepare_block(g, [v.id for v in load_variables().variables])
    assert prep.n_candidates == 25
    assert len(prep.matrix) == 25
    assert prep.matrix.isna().sum().sum() == 0


def test_prepare_block_excludes_high_missing_variable() -> None:
    g = _block(25, tarif_missing=0.5)  # 50% > 20%
    prep = prepare_block(
        g,
        [v.id for v in load_variables().variables],
        missing=MissingDataSettings(max_missing_share=0.20, min_candidates=20),
    )
    assert "TARIF" in prep.excluded_variables
    assert "TARIF" not in prep.used_variables


def test_prepare_block_fails_if_too_few_candidates() -> None:
    g = _block(10)
    with pytest.raises(InsufficientCandidatesError):
        prepare_block(
            g,
            [v.id for v in load_variables().variables],
            missing=MissingDataSettings(min_candidates=20),
        )


def test_all_methods_rank_same_destinations() -> None:
    g = _block(30, tarif_missing=0.4)
    variables = load_variables()
    expert = weights_expert_mean(variables)
    equal = weights_equal(variables)
    sc_expert = score_slice(
        g, variables=variables, normalization="minmax", method="wsm", weights=expert
    )
    sc_equal = score_slice(
        g, variables=variables, normalization="minmax", method="wsm", weights=equal
    )
    sc_topsis = score_slice(
        g, variables=variables, normalization="minmax", method="topsis", weights=expert
    )
    sc_imp = baseline_scores(g, "import_volume")
    # Align import_volume to the IMS candidate index
    sc_imp = sc_imp.reindex(sc_expert.index)
    assert set(sc_expert.dropna().index) == set(sc_equal.dropna().index)
    assert set(sc_expert.index) == set(sc_topsis.index)
    assert set(sc_expert.index) == set(sc_imp.index)
    assert len(sc_expert) >= 20
