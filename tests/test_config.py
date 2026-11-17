"""Tests for YAML configuration loading and SPEC alignment."""

from __future__ import annotations

from imsfe.config import (
    SPEC_FACTORS,
    load_experiments,
    load_settings,
    load_variables,
)


def test_settings_load() -> None:
    settings = load_settings()
    assert "COL" in settings.origins
    assert settings.n_destinations == 60
    assert settings.hs_chapters.primary == "64"
    assert settings.years.start == 2012
    assert settings.years.end == 2023
    assert settings.horizons == [1, 3]
    assert settings.entry_threshold_usd == 50_000
    assert settings.seed == 42


def test_variables_load_and_factor_list_matches_spec() -> None:
    cfg = load_variables()
    assert tuple(cfg.factors) == SPEC_FACTORS
    assert list(cfg.factors) == [
        "demand",
        "cost_access",
        "logistics",
        "competition",
        "product_fit",
        "macro_risk",
        "institutional",
        "openness_legacy",
    ]


def test_every_variable_has_valid_factor_and_direction() -> None:
    cfg = load_variables()
    valid_directions = {"benefit", "cost"}
    ids = {v.id for v in cfg.variables}
    expected_ids = {
        "IMPV",
        "IMPC",
        "GRW",
        "GDPPC",
        "DIST",
        "TARIF",
        "FTA",
        "LPI",
        "ASIASH",
        "HHI",
        "UVGAP",
        "CULT",
        "LANG",
        "INFL",
        "UNEMP",
        "GOV",
        "EOC",
        "REEXP",
    }
    assert ids == expected_ids
    for var in cfg.variables:
        assert var.factor in SPEC_FACTORS
        assert var.direction in valid_directions
        assert var.transform in {"none", "log", "log1p"}


def test_experiments_load_and_default_in_grid() -> None:
    exp = load_experiments()
    assert "minmax" in exp.normalizations
    assert "wsm" in exp.mcdm_methods
    assert "expert_mean" in exp.weight_schemes
    assert exp.default.normalization == "minmax"
    assert exp.default.mcdm == "wsm"
    assert exp.default.weights == "expert_mean"
