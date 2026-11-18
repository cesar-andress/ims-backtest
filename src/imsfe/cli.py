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
def report() -> None:
    """Generate tables and figures under outputs/ (stub)."""
    typer.echo("report: not implemented yet (Phase 9)")
    raise typer.Exit(code=1)


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
