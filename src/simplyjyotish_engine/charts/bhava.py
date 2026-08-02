from __future__ import annotations

from simplyjyotish_engine.models.chart import (
    BhavaChalitChart,
    BhavaChalitPlacement,
    BirthChart,
    HouseFact,
)
from simplyjyotish_engine.models.outputs import LongitudeValue
from simplyjyotish_engine.models.validation import ValidationStatus
from simplyjyotish_engine.vedic.reference import sign_fact, sign_index


def _longitude(value: float) -> LongitudeValue:
    value %= 360.0
    degrees = int(value)
    minutes_float = (value - degrees) * 60
    minutes = int(minutes_float)
    seconds = round((minutes_float - minutes) * 60, 2)
    return LongitudeValue(
        decimal_degrees=value, dms=f"{degrees:03d}°{minutes:02d}'{seconds:05.2f}\""
    )


def calculate_bhava_chalit(
    chart: BirthChart,
    method_id: str = "equal_from_ascendant_v1",
) -> BhavaChalitChart:
    """Calculate the explicitly supported equal-house Bhava Chalit convention.

    Cusps are ascendant + 30° increments. Intervals are start-inclusive and
    end-exclusive, so an object exactly on a cusp belongs to that cusp's house.
    This intentionally does not label Swiss quadrant cusps as Bhava Chalit.
    """
    if method_id != "equal_from_ascendant_v1":
        raise ValueError(f"Unsupported Bhava Chalit method: {method_id}")
    ascendant = chart.ascendant.longitude.decimal_degrees
    cusp_values = [(ascendant + index * 30.0) % 360.0 for index in range(12)]
    cusps = [
        HouseFact(
            number=index + 1, cusp_longitude=_longitude(value), sign=sign_fact(sign_index(value))
        )
        for index, value in enumerate(cusp_values)
    ]
    placements: list[BhavaChalitPlacement] = []
    objects = [("ascendant", ascendant)] + [
        (planet.position.planet, planet.position.longitude.decimal_degrees)
        for planet in chart.planets
    ]
    for object_name, longitude in objects:
        offset = (longitude - ascendant) % 360.0
        house = int(offset // 30.0) + 1
        distance = offset % 30.0
        placements.append(
            BhavaChalitPlacement(
                object_name=object_name,
                longitude=_longitude(longitude),
                house=house,
                cusp_house=house,
                boundary_distance_degrees=distance,
            )
        )
    return BhavaChalitChart(
        provenance=chart.provenance,
        method_id=method_id,
        method="equal houses measured from the sidereal ascendant",
        ascendant=_longitude(ascendant),
        cusps=cusps,
        placements=placements,
        warnings=["equal_house_bhava_chalit_requires_expert_convention_review"],
        explain_calculation={
            "house_boundaries": "ascendant + 30° × (house number - 1), modulo 360°",
            "interval_rule": "start-inclusive, end-exclusive; exact cusp belongs to that house",
            "scope": "No Sripati, quadrant, or unequal-house interpretation is implied",
        },
        validation_status=ValidationStatus(
            source_verified=True,
            cross_implementation_verified=False,
            source_reference_ids=("pyjhora_bhava_madhya_reference",),
            notes=(
                "Equal-from-ascendant is intentionally separate from quadrant "
                "Bhava Madhya methods.",
            ),
        ),
    )
