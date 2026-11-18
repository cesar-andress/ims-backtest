"""Leakage guards and walk-forward split tests."""

from __future__ import annotations

import pytest

from imsfe.validation.backtest import make_split


def test_walk_forward_no_leakage() -> None:
    split = make_split(range(2012, 2024), first_test_year=2019, horizon=1)
    assert max(split.train_feature_years) + 1 < 2019
    assert min(split.test_feature_years) >= 2019
    split.assert_no_leakage()


def test_walk_forward_k3() -> None:
    split = make_split(range(2012, 2024), first_test_year=2019, horizon=3)
    assert all(y + 3 < 2019 for y in split.train_feature_years)
    assert 2020 in split.test_feature_years  # 2020+3=2023
    assert 2021 not in split.test_feature_years  # 2021+3=2024 out of sample


def test_leakage_assertion_fires_on_bad_manual_split() -> None:
    from imsfe.validation.backtest import WalkForwardSplit

    bad = WalkForwardSplit(
        first_test_year=2019,
        horizon=1,
        feature_years_all=(2018, 2019, 2020),
    )
    # train would include 2018 because 2018+1=2019 is NOT < 2019 → empty train
    assert bad.train_feature_years == []
    # Construct an illegal state and assert
    with pytest.raises(AssertionError, match="leakage"):
        # Bypass property by calling assert with corrupted logic via monkeypatch
        # Directly invoke the check with a forged train year by subclassing
        class Evil(WalkForwardSplit):
            @property
            def train_feature_years(self):  # type: ignore[override]
                return [2018]  # outcome 2019 >= first_test_year

        Evil(2019, 1, (2018, 2019)).assert_no_leakage()
