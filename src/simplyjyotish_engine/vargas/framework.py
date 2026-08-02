from __future__ import annotations

from decimal import Decimal

from simplyjyotish_engine.models.chart import BirthChart
from simplyjyotish_engine.models.varga import DivisionalChart, VargaPlanet
from simplyjyotish_engine.vargas.extended import EXTENDED_VARGA_METHODS, calculate_extended_varga
from simplyjyotish_engine.vargas.parashara_bphs import (
    PARASHARA_SHODASHAVARGA_SCHEME_ID,
    SPECS,
    calculate_placement,
    d60_name,
    validation_status,
)
from simplyjyotish_engine.vedic.reference import sign_fact


def _source_longitude(longitude: float) -> tuple[int, Decimal]:
    normalized = Decimal(str(longitude)) % Decimal("360")
    source_sign = int(normalized // Decimal("30"))
    return source_sign, normalized % Decimal("30")


def calculate_varga(
    chart: BirthChart,
    division: int,
    scheme_id: str = PARASHARA_SHODASHAVARGA_SCHEME_ID,
) -> DivisionalChart:
    if scheme_id != PARASHARA_SHODASHAVARGA_SCHEME_ID:
        if division in EXTENDED_VARGA_METHODS and scheme_id == EXTENDED_VARGA_METHODS[division][0]:
            return calculate_extended_varga(chart, division, scheme_id)
        raise ValueError(f"Unsupported varga scheme: {scheme_id}")
    if division not in SPECS:
        if division in EXTENDED_VARGA_METHODS and scheme_id == PARASHARA_SHODASHAVARGA_SCHEME_ID:
            raise ValueError(
                f"D{division} is outside the default Shodashavarga baseline; "
                f"pass scheme_id={EXTENDED_VARGA_METHODS[division][0]} explicitly"
            )
        raise ValueError(
            "Default Parashari Shodashavarga supports D1, D2, D3, D4, D7, D9, D10, D12, "
            "D16, D20, D24, D27, D30, D40, D45, and D60"
        )
    spec = SPECS[division]

    def to_varga_planet(planet_name: str, longitude: float) -> VargaPlanet:
        source_sign, longitude_in_sign = _source_longitude(longitude)
        part, varga_sign, amsha_lord = calculate_placement(source_sign, longitude_in_sign, division)
        return VargaPlanet(
            planet=planet_name,
            source_longitude_degrees=longitude,
            source_sign=sign_fact(source_sign),
            division_part=part,
            varga_sign=sign_fact(varga_sign),
            amsha_name=d60_name(source_sign, part) if division == 60 else None,
            amsha_lord=amsha_lord,
        )

    ascendant = to_varga_planet("lagna", chart.ascendant.longitude.decimal_degrees)
    planets = [
        to_varga_planet(planet.position.planet, planet.position.longitude.decimal_degrees)
        for planet in chart.planets
    ]
    return DivisionalChart(
        division=division,
        name=spec.name,
        varga_scheme_id=scheme_id,
        source_verses=spec.source_verses,
        boundary_convention="Start-inclusive, end-exclusive; source longitudes use Decimal.",
        convention=(
            "Direct BPHS Chapter 6 Parashari mapping; named amsha metadata is "
            "separate from varga sign placement."
        ),
        validation_status=validation_status(),
        provenance=chart.provenance,
        ascendant=ascendant,
        planets=planets,
        warnings=["not_yet_reviewed_by_a_practicing_jyotishi"],
    )
