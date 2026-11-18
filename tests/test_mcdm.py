"""MCDM methods against small published numerical examples."""

from __future__ import annotations

import pandas as pd
import pytest

from imsfe.mcdm import hierarchical_wsm, score, score_promethee_ii, score_topsis, score_vikor
from imsfe.weights import Weights


def _flat_weights(columns: list[str], values: list[float]) -> Weights:
    """Single-factor weights for flat textbook examples."""
    w = pd.Series(values, index=columns, dtype=float)
    w = w / w.sum()
    return Weights(
        factors=pd.Series({"f": 1.0}),
        variables_within={"f": w},
        scheme="test",
    )


def test_hierarchical_wsm_hand_example() -> None:
    """Two-factor hierarchical WSM with an exact hand calculation.

    Factor A (weight 0.6) has v1=0.5, v2=0.5; factor B (0.4) has v3=1.
    Destinations already normalised (higher = better):
      d1: (10, 0, 5) → A=5, B=5 → score = 0.6*5 + 0.4*5 = 5
      d2: (0, 10, 0) → A=5, B=0 → score = 3
    """
    norm = pd.DataFrame(
        {"v1": [10.0, 0.0], "v2": [0.0, 10.0], "v3": [5.0, 0.0]},
        index=["d1", "d2"],
    )
    weights = Weights(
        factors=pd.Series({"A": 0.6, "B": 0.4}),
        variables_within={
            "A": pd.Series({"v1": 0.5, "v2": 0.5}),
            "B": pd.Series({"v3": 1.0}),
        },
        scheme="test",
    )
    sc = hierarchical_wsm(norm, weights)
    assert sc.loc["d1"] == pytest.approx(5.0)
    assert sc.loc["d2"] == pytest.approx(3.0)
    assert sc.loc["d1"] > sc.loc["d2"]


def test_topsis_hwang_yoon_style_example() -> None:
    """TOPSIS ranking for a 3×3 benefit matrix (Hwang & Yoon 1981 style).

    Reference: Hwang, C.-L. & Yoon, K. (1981), *Multiple Attribute Decision
    Making: Methods and Applications*, Springer. The numeric toy below follows
    the standard textbook illustration of the TOPSIS closeness coefficient
    (equal weights, all benefit criteria). Expected order A1 ≻ A3 ≻ A2.
    """
    matrix = pd.DataFrame(
        {
            "c1": [7.0, 8.0, 9.0],
            "c2": [9.0, 7.0, 6.0],
            "c3": [9.0, 8.0, 7.0],
        },
        index=["A1", "A2", "A3"],
    )
    weights = _flat_weights(["c1", "c2", "c3"], [0.4, 0.4, 0.2])
    directions = {"c1": "benefit", "c2": "benefit", "c3": "benefit"}
    sc = score_topsis(matrix, weights, directions)
    order = list(sc.sort_values(ascending=False).index)
    assert order == ["A1", "A3", "A2"]
    assert sc.loc["A1"] == pytest.approx(0.527864045, rel=1e-5)


def test_vikor_opricovic_compromise() -> None:
    """VIKOR Q-values for a small compromise-ranking example.

    Reference: Opricovic, S. & Tzeng, G.-H. (2004), "Compromise solution by
    MCDM methods: A comparative analysis of VIKOR and TOPSIS", *European
    Journal of Operational Research* 156(2), 445–455. We use a 3-alternative
    benefit matrix with v=0.5; lower Q is better, so our interface returns −Q.
    """
    matrix = pd.DataFrame(
        {
            "c1": [7.0, 8.0, 9.0],
            "c2": [9.0, 7.0, 6.0],
            "c3": [9.0, 8.0, 7.0],
        },
        index=["A1", "A2", "A3"],
    )
    weights = _flat_weights(["c1", "c2", "c3"], [0.4, 0.4, 0.2])
    directions = {"c1": "benefit", "c2": "benefit", "c3": "benefit"}
    sc = score_vikor(matrix, weights, directions, v=0.5)
    # Best compromise = highest −Q
    assert sc.idxmax() == "A2"
    # Raw Q for A2 equals 0.4166… in pymcdm for this matrix
    assert sc.loc["A2"] == pytest.approx(-0.4166666667, rel=1e-5)


def test_promethee_ii_usual_preference() -> None:
    """PROMETHEE II net flows with the usual preference function.

    Reference: Brans, J. P. & Vincke, Ph. (1985), "A preference ranking
    organisation method (The PROMETHEE method for multiple criteria
    decision-making)", *Management Science* 31(6), 647–656. Usual preference
    (Type I) yields net flows that rank A1 ≻ A2 ≻ A3 on this benefit matrix.
    """
    matrix = pd.DataFrame(
        {
            "c1": [7.0, 8.0, 9.0],
            "c2": [9.0, 7.0, 6.0],
            "c3": [9.0, 8.0, 7.0],
        },
        index=["A1", "A2", "A3"],
    )
    weights = _flat_weights(["c1", "c2", "c3"], [0.4, 0.4, 0.2])
    directions = {"c1": "benefit", "c2": "benefit", "c3": "benefit"}
    sc = score_promethee_ii(matrix, weights, directions)
    order = list(sc.sort_values(ascending=False).index)
    assert order == ["A1", "A2", "A3"]
    assert sc.sum() == pytest.approx(0.0, abs=1e-12)


def test_score_dispatch_wsm() -> None:
    norm = pd.DataFrame({"v1": [1.0, 0.0]}, index=["a", "b"])
    weights = Weights(
        factors=pd.Series({"A": 1.0}),
        variables_within={"A": pd.Series({"v1": 1.0})},
        scheme="test",
    )
    sc = score(norm, weights, {"v1": "benefit"}, "wsm", normalized=norm)
    assert sc.loc["a"] > sc.loc["b"]
