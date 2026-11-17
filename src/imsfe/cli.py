"""Typer CLI entry points for download, build, run, report, and legacy."""

from __future__ import annotations

import typer

app = typer.Typer(
    name="imsfe",
    help="IMSFE 2.0: reproducible international market selection.",
    no_args_is_help=True,
)


@app.command()
def download() -> None:
    """Download official data sources into data/raw/ (stub)."""
    typer.echo("download: not implemented yet (Phase 2)")
    raise typer.Exit(code=1)


@app.command()
def build() -> None:
    """Build the origin×destination×year panel and features (stub)."""
    typer.echo("build: not implemented yet (Phase 3)")
    raise typer.Exit(code=1)


@app.command()
def run(
    experiment: str = typer.Option("default", "--experiment", "-e", help="Experiment name"),
) -> None:
    """Run normalisation / MCDM / weight experiment grid (stub)."""
    typer.echo(f"run: not implemented yet (Phase 4); experiment={experiment}")
    raise typer.Exit(code=1)


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
