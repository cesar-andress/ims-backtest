"""Report formatting, F1, and light robustness helpers."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from imsfe.countries import country_name
from imsfe.report.figures import plot_framework_diagram
from imsfe.report.format_util import dataframe_to_booktabs, fmt_number, write_table_bundle
from imsfe.report.robustness_extra import run_extra_robustness
from imsfe.report.run import write_build_manifest


def test_fmt_number_english() -> None:
    assert fmt_number(1234.5, digits=1) == "1,234.5"
    assert fmt_number(0.1234, digits=3) == "0.123"
    assert fmt_number(np.nan) == ""


def test_country_name_known() -> None:
    assert country_name("COL") == "Colombia"
    assert country_name("USA") == "United States"


def test_write_table_bundle_csv_md_no_tex(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from imsfe.report import format_util

    monkeypatch.setattr(format_util, "outputs_tables_dir", lambda: tmp_path)
    df = pd.DataFrame({"iso3": ["COL"], "value": [1.2345]})
    paths = write_table_bundle(df, "T_test", title="Test", float_digits=2)
    assert paths["csv"].is_file()
    assert paths["md"].is_file()
    md = paths["md"].read_text(encoding="utf-8")
    assert "booktabs" in md.lower() or "Booktabs" in md
    assert "1.23" in md or "1,23" not in md  # English dot decimal
    # Must not create .tex
    assert not (tmp_path / "T_test.tex").exists()
    tex = dataframe_to_booktabs(df, caption="c", label="tab:x")
    assert r"\toprule" in tex


def test_plot_f1(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from imsfe.report import figures as figmod

    monkeypatch.setattr(figmod, "figures_dir", lambda: tmp_path)
    paths = plot_framework_diagram(stem="F1_test")
    assert paths["png"].is_file()
    assert paths["pdf"].is_file()


def test_extra_robustness_toy() -> None:
    rng = np.random.default_rng(0)
    rows = []
    for year in range(2016, 2022):
        for o in ("COL", "PER"):
            dests = [f"D{i:02d}" for i in range(25)]
            for i, d in enumerate(dests):
                rows.append(
                    {
                        "iso3_o": o,
                        "iso3_d": d,
                        "year": year,
                        "hs_chapter": "64",
                        "X_ijt": float(1000 * (25 - i) + year),
                        "IMPV": float(rng.uniform(1, 10)),
                        "IMPC": float(rng.uniform(1, 10)),
                        "GRW": float(rng.uniform(-1, 1)),
                        "GDPPC": float(rng.uniform(1, 10)),
                        "DIST": float(rng.uniform(500, 5000)),
                        "TARIF": float(rng.uniform(0, 10)),
                        "FTA": float(i % 2),
                        "LPI": float(rng.uniform(1, 5)),
                        "ASIASH": float(rng.uniform(0, 1)),
                        "HHI": float(rng.uniform(0, 1)),
                        "UVGAP": float(rng.uniform(0, 2)),
                        "CULT": float(rng.uniform(0, 2)),
                        "LANG": float(i % 2),
                        "INFL": float(rng.uniform(0, 5)),
                        "UNEMP": float(rng.uniform(1, 15)),
                        "GOV": float(rng.uniform(-1, 1)),
                        "EOC": float(rng.uniform(20, 80)),
                        "REEXP": float(rng.uniform(0, 2)),
                    }
                )
    panel = pd.DataFrame(rows)
    # outcomes for k=1
    from imsfe.build.outcomes import add_outcomes

    panel = add_outcomes(panel, threshold=50_000.0, horizons=[1, 3])
    out = run_extra_robustness(
        panel,
        origins=["COL"],
        horizons=[1],
        thresholds=[50_000.0],
        chapters=["64", "61"],
        first_test_year=2019,
    )
    assert not out.empty
    assert (out["hs_chapter"] == "61").any()
    skipped = out.loc[out["status"] == "skipped_no_panel"]
    assert not skipped.empty


def test_build_manifest(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from imsfe.report import run as runmod

    monkeypatch.setattr(runmod, "project_root", lambda: tmp_path)
    (tmp_path / "outputs" / "tables").mkdir(parents=True)
    (tmp_path / "outputs" / "figures").mkdir(parents=True)
    (tmp_path / "outputs" / "logs").mkdir(parents=True)
    f = tmp_path / "outputs" / "tables" / "dummy.csv"
    f.write_text("a,b\n1,2\n", encoding="utf-8")
    man = write_build_manifest(extra={"ok": True})
    assert man.is_file()
    data = man.read_text(encoding="utf-8")
    assert "sha256" in data
    assert "dummy.csv" in data
