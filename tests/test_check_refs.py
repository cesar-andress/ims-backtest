"""Unit tests for scripts/check_refs.py (bib-only; no network)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_refs.py"


def _load_mod():
    spec = importlib.util.spec_from_file_location("check_refs", SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_parse_bib_entries_extracts_fields() -> None:
    mod = _load_mod()
    text = """
@article{foo2020,
  title = {Hello World},
  year = {2020},
  doi = {10.1000/xyz},
}
@book{bar,
  title = {No DOI Here},
  year = {2019},
}
"""
    entries = mod.parse_bib_entries(text)
    assert len(entries) == 2
    assert entries[0]["key"] == "foo2020"
    assert entries[0]["doi"] == "10.1000/xyz"
    assert entries[1]["doi"] is None


def test_check_entry_no_doi() -> None:
    mod = _load_mod()
    row = mod.check_entry({"key": "x", "doi": None, "title": "T", "year": "2020"})
    assert row["status"] == "no_doi"


def test_check_entry_lookup_failed() -> None:
    mod = _load_mod()

    def boom(_doi: str):
        return {"_error": "HTTP 404"}

    row = mod.check_entry(
        {"key": "x", "doi": "10.0/x", "title": "T", "year": "2020"},
        crossref_fn=boom,
    )
    assert row["status"] == "doi_lookup_failed"


def test_check_entry_metadata_mismatch() -> None:
    mod = _load_mod()

    def cr(_doi: str):
        return {
            "title": ["Completely Different Title"],
            "published-print": {"date-parts": [[2020]]},
        }

    row = mod.check_entry(
        {"key": "x", "doi": "10.0/x", "title": "Original Unique Phrase", "year": "2020"},
        crossref_fn=cr,
    )
    assert row["status"] == "metadata_mismatch"


def test_check_entry_year_mismatch() -> None:
    mod = _load_mod()

    def cr(_doi: str):
        return {
            "title": ["Hello World Paper"],
            "published-print": {"date-parts": [[2019]]},
        }

    row = mod.check_entry(
        {"key": "x", "doi": "10.0/x", "title": "Hello World Paper", "year": "2020"},
        crossref_fn=cr,
    )
    assert row["status"] == "year_mismatch"


def test_check_entry_ok() -> None:
    mod = _load_mod()

    def cr(_doi: str):
        return {
            "title": ["Hello World Paper"],
            "published-print": {"date-parts": [[2020]]},
        }

    row = mod.check_entry(
        {"key": "x", "doi": "10.0/x", "title": "Hello World Paper", "year": "2020"},
        crossref_fn=cr,
    )
    assert row["status"] == "ok"


def test_main_nonzero_on_mismatch(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    mod = _load_mod()
    bib = tmp_path / "refs.bib"
    bib.write_text("@misc{a,\n  title = {X},\n}\n", encoding="utf-8")
    out_md = tmp_path / "refs_check.md"
    out_json = tmp_path / "refs_check.json"
    monkeypatch.setattr(mod, "BIB", bib)
    monkeypatch.setattr(mod, "OUT_MD", out_md)
    monkeypatch.setattr(mod, "OUT_JSON", out_json)
    rc = mod.main([])
    assert rc == 1
    assert out_md.is_file()


def test_load_entries_bib_only(tmp_path: Path) -> None:
    mod = _load_mod()
    bib = tmp_path / "refs.bib"
    bib.write_text(
        "@article{k,\n  title = {T},\n  year = {2021},\n  doi = {10.1/x},\n}\n",
        encoding="utf-8",
    )
    # A JSON sidecar must be ignored
    (tmp_path / "refs_extracted.json").write_text("[]", encoding="utf-8")
    entries = mod.load_entries(bib)
    assert len(entries) == 1
    assert entries[0]["key"] == "k"
