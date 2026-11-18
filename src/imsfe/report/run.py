"""Orchestrate `imsfe report`: tables, figures, robustness appendix, build.json."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd

from imsfe.build.panel import processed_dir
from imsfe.config import load_settings, project_root
from imsfe.report.figures import (
    figures_dir,
    plot_f4_from_blocks,
    plot_f5_from_shap_csv,
    plot_framework_diagram,
)
from imsfe.report.robustness_extra import run_extra_robustness
from imsfe.report.tables import regenerate_all_tables


def outputs_logs_dir() -> Path:
    path = project_root() / "outputs" / "logs"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _collect_output_files() -> list[Path]:
    root = project_root() / "outputs"
    files: list[Path] = []
    for sub in ("tables", "figures", "logs"):
        d = root / sub
        if not d.is_dir():
            continue
        for p in sorted(d.rglob("*")):
            if p.is_file() and p.name != "build.json":
                files.append(p)
    return files


def write_build_manifest(extra: dict[str, Any] | None = None) -> Path:
    """List output files with SHA-256 hashes -> outputs/logs/build.json."""
    files = _collect_output_files()
    entries = []
    for p in files:
        rel = str(p.relative_to(project_root()))
        entries.append(
            {
                "path": rel,
                "sha256": _sha256(p),
                "bytes": p.stat().st_size,
            }
        )
    payload = {
        "created_utc": datetime.now(UTC).isoformat(),
        "n_files": len(entries),
        "files": entries,
        "extra": extra or {},
    }
    out = outputs_logs_dir() / "build.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out


def _refresh_figures(*, refresh_pipelines: bool) -> dict[str, Any]:
    """Regenerate F1–F5 from artifacts and/or light pipeline calls."""
    fig_out: dict[str, Any] = {}
    fig_out["F1"] = plot_framework_diagram()

    # F2 / F3: optionally re-run SMAA and case matrix
    if refresh_pipelines:
        from imsfe.matrix import run_case_study
        from imsfe.smaa import run_smaa_case

        fig_out["F2"] = run_smaa_case(origin="COL")["figure_paths"]
        fig_out["F3"] = run_case_study(origin="COL")["figure_paths"]
    else:
        # Keep existing F2/F3 if present; still ensure F1/F4/F5 refresh
        for stem in (
            "F2_smaa_rank_acceptability",
            "F3_attractiveness_fit_matrix",
        ):
            png = figures_dir() / f"{stem}.png"
            if png.is_file():
                fig_out[stem] = {"png": png, "pdf": figures_dir() / f"{stem}.pdf"}

    blocks_path = processed_dir() / "validation_blocks.parquet"
    if blocks_path.is_file():
        blocks = pd.read_parquet(blocks_path)
        fig_out["F4"] = plot_f4_from_blocks(blocks)
    shap_path = project_root() / "outputs" / "tables" / "T4_shap_factor_importance.csv"
    if shap_path.is_file():
        shap = pd.read_csv(shap_path)
        fig_out["F5"] = plot_f5_from_shap_csv(shap)
    return fig_out


def run_report(
    *,
    refresh_pipelines: bool = False,
    run_robustness: bool = True,
    first_test_year: int = 2019,
) -> dict[str, Any]:
    """Full Phase-9 report regeneration."""
    settings = load_settings()
    panel_path = processed_dir() / "panel_ijt.parquet"
    if not panel_path.is_file():
        raise FileNotFoundError(
            f"Missing {panel_path}; run `imsfe build` (and ideally validate/smaa/ml/matrix) first"
        )
    panel = pd.read_parquet(panel_path).drop_duplicates(
        ["iso3_o", "iso3_d", "year"], keep="first"
    )

    robustness = None
    if run_robustness:
        print("extra robustness sweeps...", flush=True)
        robustness = run_extra_robustness(panel, settings=settings, first_test_year=first_test_year)
        print(f"  rows={len(robustness)}", flush=True)

    print("regenerating tables T1–T9...", flush=True)
    tables = regenerate_all_tables(panel, robustness=robustness)

    print("regenerating figures F1–F5...", flush=True)
    figures = _refresh_figures(refresh_pipelines=refresh_pipelines)

    manifest = write_build_manifest(
        extra={
            "refresh_pipelines": refresh_pipelines,
            "run_robustness": run_robustness,
            "seed": settings.seed,
            "panel_rows": int(len(panel)),
        }
    )
    print(f"build manifest -> {manifest}", flush=True)
    return {
        "tables": tables,
        "figures": figures,
        "robustness": robustness,
        "manifest": manifest,
        "panel_path": panel_path,
    }
