"""Tests for legacy Excel reproduction and audit outputs."""

from __future__ import annotations

from pathlib import Path

import pytest

from imsfe.legacy import (
    default_excel_path,
    load_eoc,
    load_preferential_tariffs,
    load_raw_criteria,
    normalize_eoc,
    run_legacy,
    score_pipeline,
)


@pytest.fixture(scope="module")
def legacy_result() -> dict:
    path = default_excel_path()
    if not path.is_file():
        pytest.skip(f"Legacy Excel not available: {path}")
    return run_legacy(path)


def test_imsfe_scores_match_paper_to_2_decimals(legacy_result: dict) -> None:
    scores = legacy_result["scores"]["ratio_legacy"]
    expected = {
        "CHE": 6.12,
        "SGP": 5.81,
        "DNK": 5.10,
        "NLD": 4.85,
        "CAN": 4.80,
        "VNM": 2.96,
    }
    for iso, value in expected.items():
        assert round(float(scores.loc[iso]), 2) == value, (
            f"{iso}: got {scores.loc[iso]:.4f}, expected {value}"
        )


def test_normalized_eoc_are_sgp(legacy_result: dict) -> None:
    neoc = legacy_result["neoc"]
    assert round(float(neoc.loc["ARE"]), 2) == 10.00
    assert round(float(neoc.loc["SGP"]), 2) == 9.48


def test_cptr_austria_equals_australia(legacy_result: dict) -> None:
    raw = legacy_result["raw"]
    assert raw.loc["AUT", "CPTR"] == raw.loc["AUS", "CPTR"] == 9_375_992


def test_preferential_tariffs_refuse_when_empty(tmp_path: Path) -> None:
    empty = tmp_path / "tariffs.csv"
    empty.write_text("iso3,tariff_pct,source\nUSA,,\nCHE,,\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Preferential tariffs are incomplete"):
        load_preferential_tariffs(empty)


def test_preferential_tariffs_file_complete() -> None:
    tariffs = load_preferential_tariffs()
    assert len(tariffs) == 30
    assert tariffs.notna().all()
    assert (tariffs >= 0).all()


def test_audit_and_comparison_written(legacy_result: dict) -> None:
    audit = Path(legacy_result["audit_path"])
    comparison = Path(legacy_result["comparison_path"])
    assert audit.is_file()
    assert comparison.is_file()
    text = audit.read_text(encoding="utf-8")
    assert "MANUAL CHECK" in text
    assert "CPTR" in text
    assert "9375992" in text or "9.37599e+06" in text or "9375992" in text
    df_head = comparison.read_text(encoding="utf-8").splitlines()[0]
    assert "rank_ratio_legacy" in df_head
    assert "rank_minmax" in df_head
    assert "rank_rank" in df_head


def test_weights_yaml_exported(legacy_result: dict) -> None:
    path = Path(legacy_result["weights_yaml"])
    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    assert "kendall_w_factors" in text
    assert "COST" in text
    assert "PPAD" in text


def test_raw_loader_has_30_countries() -> None:
    if not default_excel_path().is_file():
        pytest.skip("Legacy Excel not available")
    raw = load_raw_criteria()
    assert len(raw) == 30
    assert set(raw.columns) >= {"country", "PPAD", "CUDI"}


def test_eoc_loader_covers_preselection() -> None:
    if not default_excel_path().is_file():
        pytest.skip("Legacy Excel not available")
    raw = load_raw_criteria()
    eoc = load_eoc()
    neoc = normalize_eoc(eoc.reindex(raw.index)["eoc"])
    assert round(float(neoc.loc["ARE"]), 2) == 10.00


def test_minmax_runs(legacy_result: dict) -> None:
    raw = legacy_result["raw"]
    var_w = legacy_result["experts"].variable_summary["mean"]
    scores = score_pipeline(raw, var_w, "minmax")
    assert len(scores) == 30
    assert scores.max() > scores.min()
