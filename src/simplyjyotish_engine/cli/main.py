from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from simplyjyotish_engine.models.inputs import BirthDetails
from simplyjyotish_engine.vedic.chart import calculate_birth_chart

app = typer.Typer(help="Developer CLI for deterministic Jyotish calculations.")


@app.command()
def chart(
    input: Annotated[Path, typer.Option("--input", exists=True, readable=True)],
) -> None:
    """Calculate Milestone 1 planetary positions from a JSON birth input."""
    birth = BirthDetails.model_validate_json(input.read_text(encoding="utf-8"))
    typer.echo(calculate_birth_chart(birth).model_dump_json(indent=2))


@app.command()
def verify() -> None:
    """Run the local Python test suite."""
    import pytest

    raise typer.Exit(pytest.main(["-q"]))


if __name__ == "__main__":
    app()
