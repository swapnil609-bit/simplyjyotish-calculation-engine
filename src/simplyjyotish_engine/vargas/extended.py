from __future__ import annotations

from decimal import Decimal

from simplyjyotish_engine.models.chart import BirthChart
from simplyjyotish_engine.models.varga import DivisionalChart, VargaPlanet, VargaValidationStatus
from simplyjyotish_engine.vedic.reference import sign_fact

EXTENDED_VARGA_METHODS = {
    5: (
        "panchamsha_parashari_alt_v1",
        "Panchamsha",
        "Odd signs count from Aries; even signs count from Libra.",
    ),
    6: (
        "shashtamsha_parashari_alt_v1",
        "Shashtamsha",
        "Odd signs count from the source sign; even signs count from the seventh sign.",
    ),
    8: (
        "ashtamsha_parashari_alt_v1",
        "Ashtamsha",
        "Odd signs count from Aries; even signs count from Scorpio.",
    ),
    11: (
        "ekadashamsha_parashari_alt_v1",
        "Ekadashamsha",
        "Odd signs count from Aries; even signs count from Libra.",
    ),
}


def _extended_sign(source_sign: int, part: int, division: int) -> int:
    index = part - 1
    if division == 5:
        start = 0 if source_sign % 2 == 0 else 6
    elif division == 6:
        start = source_sign if source_sign % 2 == 0 else (source_sign + 6) % 12
    elif division == 8:
        start = 0 if source_sign % 2 == 0 else 7
    elif division == 11:
        start = 0 if source_sign % 2 == 0 else 6
    else:
        raise ValueError(f"Unsupported extended varga D{division}")
    return (start + index) % 12


def calculate_extended_varga(
    chart: BirthChart, division: int, method_id: str | None = None
) -> DivisionalChart:
    if division not in EXTENDED_VARGA_METHODS:
        raise ValueError("Extended methods support only D5, D6, D8, and D11")
    expected_id, name, convention = EXTENDED_VARGA_METHODS[division]
    if method_id is not None and method_id != expected_id:
        raise ValueError(f"Unsupported method for D{division}: {method_id}")

    def placement(planet: str, longitude: float) -> VargaPlanet:
        normalized = Decimal(str(longitude)) % Decimal("360")
        source_sign = int(normalized // Decimal("30"))
        part = int((normalized % Decimal("30")) / (Decimal("30") / division)) + 1
        return VargaPlanet(
            planet=planet,
            source_longitude_degrees=longitude,
            source_sign=sign_fact(source_sign),
            division_part=part,
            varga_sign=sign_fact(_extended_sign(source_sign, part, division)),
        )

    return DivisionalChart(
        division=division,
        name=name,
        varga_scheme_id=expected_id,
        source_verses=(
            "Versioned extended-varga convention; not part of BPHS Chapter 6 Shodashavarga baseline"
        ),
        boundary_convention="Start-inclusive, end-exclusive; Decimal longitude partitioning",
        convention=convention,
        validation_status=VargaValidationStatus(
            source_verified=False, cross_implementation_verified=False, expert_reviewed=False
        ),
        provenance=chart.provenance,
        ascendant=placement("lagna", chart.ascendant.longitude.decimal_degrees),
        planets=[
            placement(planet.position.planet, planet.position.longitude.decimal_degrees)
            for planet in chart.planets
        ],
        warnings=["extended_varga_convention_requires_source_and_expert_review"],
    )
