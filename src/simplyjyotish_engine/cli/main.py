from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from simplyjyotish_engine.ashtakavarga.calculator import calculate_ashtakavarga
from simplyjyotish_engine.aspects.relationships import calculate_relationships
from simplyjyotish_engine.charts.bhava import calculate_bhava_chalit
from simplyjyotish_engine.dashas.ashtottari import calculate_ashtottari_dasha
from simplyjyotish_engine.dashas.vimshottari import calculate_vimshottari_dasha
from simplyjyotish_engine.dashas.yogini import calculate_yogini_dasha
from simplyjyotish_engine.models.dasha import DashaDepth
from simplyjyotish_engine.models.inputs import BirthDetails, LocationDate, TransitRequest
from simplyjyotish_engine.panchanga.daily import calculate_panchanga
from simplyjyotish_engine.strengths.calculator import calculate_shadbala
from simplyjyotish_engine.transits.timeline import calculate_transit_timeline
from simplyjyotish_engine.vargas.framework import calculate_varga
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


@app.command()
def varga(
    input: Annotated[Path, typer.Option("--input", exists=True, readable=True)],
    division: Annotated[int, typer.Option("--division", min=1, max=60)],
    scheme_id: Annotated[str | None, typer.Option("--scheme-id")] = None,
) -> None:
    """Calculate a supported divisional chart."""
    birth = BirthDetails.model_validate_json(input.read_text(encoding="utf-8"))
    kwargs = {} if scheme_id is None else {"scheme_id": scheme_id}
    result = calculate_varga(calculate_birth_chart(birth), division, **kwargs)
    typer.echo(result.model_dump_json(indent=2))


@app.command()
def dasha(
    input: Annotated[Path, typer.Option("--input", exists=True, readable=True)],
    level: Annotated[DashaDepth, typer.Option("--level")] = DashaDepth.ANTARDASHA,
) -> None:
    """Calculate the validated Vimshottari dasha timeline."""
    birth = BirthDetails.model_validate_json(input.read_text(encoding="utf-8"))
    timeline = calculate_vimshottari_dasha(calculate_birth_chart(birth), max_depth=level)
    typer.echo(timeline.model_dump_json(indent=2))


@app.command()
def bhava(
    input: Annotated[Path, typer.Option("--input", exists=True, readable=True)],
) -> None:
    """Calculate equal-from-Ascendant Bhava Chalit placements."""
    birth = BirthDetails.model_validate_json(input.read_text(encoding="utf-8"))
    typer.echo(calculate_bhava_chalit(calculate_birth_chart(birth)).model_dump_json(indent=2))


@app.command()
def dasha_family(
    input: Annotated[Path, typer.Option("--input", exists=True, readable=True)],
    system: Annotated[str, typer.Option("--system", help="yogini or ashtottari")],
    level: Annotated[DashaDepth, typer.Option("--level")] = DashaDepth.ANTARDASHA,
) -> None:
    """Calculate a supported non-Vimshottari dasha family."""
    birth = BirthDetails.model_validate_json(input.read_text(encoding="utf-8"))
    chart_result = calculate_birth_chart(birth)
    if system == "yogini":
        timeline = calculate_yogini_dasha(chart_result, max_depth=level)
    elif system == "ashtottari":
        timeline = calculate_ashtottari_dasha(chart_result, max_depth=level)
    else:
        raise typer.BadParameter("system must be yogini or ashtottari")
    typer.echo(timeline.model_dump_json(indent=2))


@app.command()
def panchang(
    input: Annotated[Path, typer.Option("--input", exists=True, readable=True)],
) -> None:
    """Calculate deterministic Panchanga and daily Muhurta primitives."""
    request = LocationDate.model_validate_json(input.read_text(encoding="utf-8"))
    typer.echo(calculate_panchanga(request).model_dump_json(indent=2))


@app.command()
def transit(
    input: Annotated[Path, typer.Option("--input", exists=True, readable=True)],
) -> None:
    """Calculate transit snapshots and ingress/station events."""
    request = TransitRequest.model_validate_json(input.read_text(encoding="utf-8"))
    typer.echo(calculate_transit_timeline(request).model_dump_json(indent=2))


@app.command()
def relationships(
    input: Annotated[Path, typer.Option("--input", exists=True, readable=True)],
    conjunction_orb: Annotated[float, typer.Option("--conjunction-orb")] = 8.0,
) -> None:
    """Calculate configured Vedic relationship and aspect facts."""
    birth = BirthDetails.model_validate_json(input.read_text(encoding="utf-8"))
    result = calculate_relationships(calculate_birth_chart(birth), conjunction_orb)
    typer.echo(result.model_dump_json(indent=2))


@app.command()
def shadbala(
    input: Annotated[Path, typer.Option("--input", exists=True, readable=True)],
) -> None:
    """Calculate component-level Shadbala and Bhava Bala."""
    birth = BirthDetails.model_validate_json(input.read_text(encoding="utf-8"))
    typer.echo(calculate_shadbala(calculate_birth_chart(birth)).model_dump_json(indent=2))


@app.command()
def ashtakavarga(
    input: Annotated[Path, typer.Option("--input", exists=True, readable=True)],
) -> None:
    """Calculate BAV, PAV, SAV and Ashtakavarga shodhana facts."""
    birth = BirthDetails.model_validate_json(input.read_text(encoding="utf-8"))
    typer.echo(calculate_ashtakavarga(calculate_birth_chart(birth)).model_dump_json(indent=2))


if __name__ == "__main__":
    app()
