"""Typer CLI entry points for download, build, run, report, and legacy."""

from __future__ import annotations

import typer

app = typer.Typer(
    name="imsfe",
    help="IMSFE 2.0: reproducible international market selection.",
    no_args_is_help=True,
)


@app.command()
def download(
    force: bool = typer.Option(False, "--force", help="Re-download even if manifest matches"),
    report: bool = typer.Option(
        False, "--report", help="Only write coverage.md from existing data/raw"
    ),
) -> None:
    """Download official data sources into data/raw/ and update the manifest."""
    from imsfe.download import run_download

    result = run_download(force=force, report_only=report)
    typer.echo(f"coverage -> {result['coverage_path']}")
    for source, info in result["status"].items():
        if not info:
            continue
        if info.get("error"):
            typer.echo(f"  {source}: ERROR {info['error']}")
        elif info.get("skipped"):
            typer.echo(f"  {source}: skipped")
        else:
            typer.echo(f"  {source}: ok")


@app.command()
def build(
    chapter: str | None = typer.Option(
        None, "--chapter", help="HS chapter (default: settings primary)"
    ),
) -> None:
    """Build the origin×destination×year panel, features, and outcomes."""
    import pandas as pd

    from imsfe.build import run_build, top_destinations_by_impv

    result = run_build(chapter=chapter)
    typer.echo(f"panel -> {result['panel_path']}")
    typer.echo(f"shape -> {result['shape']}")
    typer.echo(f"T1    -> {result['t1_path']}")
    typer.echo(f"T3    -> {result['t3_path']}")
    typer.echo("coverage %:")
    for _, row in result["coverage"].iterrows():
        typer.echo(f"  {row['variable']}: {row['coverage_pct']:.1f}")
    panel = pd.read_parquet(result["panel_path"])
    last_year = int(panel["year"].max())
    top = top_destinations_by_impv(panel, "COL", last_year, n=10)
    typer.echo(f"Top-10 destinations for COL in {last_year} by IMPV:")
    for _, row in top.iterrows():
        typer.echo(
            f"  {row['iso3_d']}: IMPV={row['IMPV_raw']:.0f}  X_ijt={row['X_ijt']:.0f}"
        )


@app.command()
def run(
    experiment: str = typer.Option(
        "default",
        "--experiment",
        "-e",
        help="default | grid | method+normalization+weights",
    ),
) -> None:
    """Run normalisation × MCDM × weights grid; write scores and T7."""
    from imsfe.run_experiments import run_experiments

    result = run_experiments(experiment=experiment)
    typer.echo(f"scores -> {result['scores_path']} ({result['n_rows']} rows)")
    typer.echo(f"combos -> {result['n_combos']}")
    typer.echo(f"T7     -> {result['t7_path']}")
    typer.echo(
        f"Top-10 {result['origin']} {result['year']} "
        f"{result['primary_method']}+{result['primary_normalization']}+{result['primary_weights']}:"
    )
    for _, row in result["top10"].iterrows():
        typer.echo(f"  {int(row['rank']):2d}. {row['dest']}: {row['score']:.4f}")


@app.command()
def smaa(
    origin: str = typer.Option("COL", "--origin", "-o"),
    year: int | None = typer.Option(None, "--year", "-y"),
    samples: int | None = typer.Option(None, "--samples", help="Override smaa.n_samples"),
    mode: str = typer.Option("dirichlet", "--mode", help="dirichlet | box"),
) -> None:
    """SMAA weight uncertainty: T8 table and F2 rank-acceptability heatmap."""
    from imsfe.smaa import run_smaa_case

    result = run_smaa_case(
        origin=origin,
        year=year,
        mode=mode,  # type: ignore[arg-type]
        n_samples=samples,
    )
    typer.echo(f"SMAA {result['origin']} {result['year']}: n={result['summary']['n_samples']}")
    typer.echo(f"T8 -> {result['t8_path']}")
    for kind, path in result["figure_paths"].items():
        typer.echo(f"F2 ({kind}) -> {path}")
    typer.echo(result["t8"].to_string(index=False))


@app.command()
def validate(
    first_test_year: int = typer.Option(2019, "--first-test-year"),
    horizon: int = typer.Option(1, "--horizon", "-k"),
    boot: int | None = typer.Option(None, "--boot", help="Bootstrap reps (default settings)"),
) -> None:
    """Walk-forward predictive validation: T4/T5/T6 and F4."""
    from imsfe.validation import run_validation

    result = run_validation(
        first_test_year=first_test_year,
        horizon=horizon,
        n_boot=boot,
    )
    typer.echo(f"T4 -> {result['t4_path']}")
    typer.echo(f"T5 -> {result['t5_path']}")
    typer.echo(f"T6 -> {result['t6_path']}")
    typer.echo(f"F4 -> {result['f4_path']}")
    typer.echo(result["summary"])


@app.command()
def ml(
    first_test_year: int = typer.Option(2019, "--first-test-year"),
    horizon: int = typer.Option(1, "--horizon", "-k"),
    boot: int | None = typer.Option(None, "--boot"),
) -> None:
    """GBM walk-forward benchmark + SHAP factor chart (F5); merges into T4."""
    from imsfe.validation.ml import run_ml_benchmark

    result = run_ml_benchmark(
        first_test_year=first_test_year,
        horizon=horizon,
        n_boot=boot,
    )
    typer.echo(
        f"ML backend={result['backend']} runtime_s={result['runtime_sec']:.2f}"
    )
    typer.echo(f"T4 -> {result['t4_path']}")
    typer.echo(f"SHAP CSV -> {result['shap_csv']}")
    for kind, path in result["figure_paths"].items():
        typer.echo(f"F5 ({kind}) -> {path}")
    typer.echo(result["comparison"].to_string(index=False))


@app.command("matrix")
def matrix_cmd(
    origin: str = typer.Option("COL", "--origin", "-o"),
    year: int | None = typer.Option(None, "--year", "-y", help="Default: latest year"),
    top_n: int = typer.Option(10, "--top-n"),
) -> None:
    """Attractiveness × fit strategic matrix (F3) and recommended vs actual table."""
    from imsfe.matrix import run_case_study

    result = run_case_study(origin=origin, year=year, top_n=top_n)
    cov = result["coverage"]
    typer.echo(f"Case {result['origin']} HS{cov['hs_chapter']} {result['year']}")
    typer.echo(f"attr used={cov['attr_used']} dropped={cov['attr_dropped']}")
    typer.echo(f"fit  used={cov['fit_used']} dropped={cov['fit_dropped']}")
    typer.echo(f"matrix  -> {result['matrix_path']}")
    typer.echo(f"compare -> {result['compare_path']}")
    typer.echo(f"guide   -> {result['guide_path']}")
    for kind, path in result["figure_paths"].items():
        typer.echo(f"F3 ({kind}) -> {path}")
    cmp_ = result["compare"]
    typer.echo("Recommended vs actual (export value / 3y log growth):")
    typer.echo(cmp_.to_string(index=False))


@app.command()
def report(
    refresh: bool = typer.Option(
        False,
        "--refresh",
        help="Re-run SMAA + case matrix while regenerating F2/F3",
    ),
    robustness: bool = typer.Option(
        True,
        "--robustness/--no-robustness",
        help="Extra origin/horizon/threshold/chapter appendix sweep",
    ),
) -> None:
    """Regenerate T1–T9 (CSV+Markdown), F1–F5, and outputs/logs/build.json."""
    from imsfe.report import run_report

    result = run_report(refresh_pipelines=refresh, run_robustness=robustness)
    typer.echo(f"manifest -> {result['manifest']}")
    for key in ("T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "A1"):
        if key in result["tables"] and result["tables"][key]:
            typer.echo(f"  table {key} ok")
    for key, val in result["figures"].items():
        if isinstance(val, dict) and "png" in val:
            typer.echo(f"  figure {key} -> {val['png']}")



@app.command("legacy")
def legacy_cmd() -> None:
    """Reproduce and audit the original Excel ranking."""
    from imsfe.legacy import run_legacy

    result = run_legacy()
    typer.echo(f"weights -> {result['weights_yaml']}")
    typer.echo(f"audit   -> {result['audit_path']}")
    typer.echo(f"compare -> {result['comparison_path']}")
    typer.echo(f"tau     -> {result['tau_path']}")
    typer.echo(f"unified -> {result['unified_path']}")
    if result["pref_tariff_error"]:
        typer.echo(
            "minmax_pref_tariff skipped (fill data/manual/legacy_preferential_tariffs.csv):"
        )
        typer.echo(f"  {result['pref_tariff_error']}")
    top = result["scores"]["ratio_legacy"].sort_values(ascending=False).head(5)
    typer.echo("Top-5 ratio_legacy:")
    for iso, score in top.items():
        typer.echo(f"  {iso}: {score:.2f}")


if __name__ == "__main__":
    app()
