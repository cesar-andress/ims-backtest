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


@app.command()
def legacy() -> None:
    """Reproduce and audit the original Excel ranking (stub)."""
    typer.echo("legacy: not implemented yet (Phase 1)")
    raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
