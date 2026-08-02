from __future__ import annotations

from typing import Any

from simplyjyotish_engine.astronomy.ephemeris import require_swiss_ephemeris
from simplyjyotish_engine.astronomy.positions import _dms, _flags, calculate_planetary_positions
from simplyjyotish_engine.core.time import julian_day, to_utc
from simplyjyotish_engine.models.chart import (
    AscendantFact,
    BirthChart,
    HouseFact,
    PlanetChartFact,
)
from simplyjyotish_engine.models.inputs import BirthDetails
from simplyjyotish_engine.models.outputs import LongitudeValue
from simplyjyotish_engine.vedic.dignity import dignity
from simplyjyotish_engine.vedic.reference import nakshatra_fact, sign_fact, sign_index

COMBUSTION_LIMITS = {
    "moon": 12.0,
    "mars": 17.0,
    "mercury": 14.0,
    "jupiter": 11.0,
    "venus": 10.0,
    "saturn": 15.0,
}


def _longitude_value(value: float) -> LongitudeValue:
    normalized = value % 360.0
    return LongitudeValue(decimal_degrees=normalized, dms=_dms(normalized))


def _angular_distance(first: float, second: float) -> float:
    return abs((first - second + 180.0) % 360.0 - 180.0)


def calculate_birth_chart(birth: BirthDetails) -> BirthChart:
    swe: Any = require_swiss_ephemeris()
    utc = to_utc(birth.local_datetime(), birth.timezone_name)
    jd = julian_day(utc)
    settings = birth.settings
    flags = _flags(settings, swe)
    position_result = calculate_planetary_positions(birth)
    by_name = {position.planet: position for position in position_result.positions}
    cusps, ascmc = swe.houses_ex(jd, birth.latitude, birth.longitude, b"W", flags)
    ascendant = ascmc[0] % 360.0
    houses = [
        HouseFact(
            number=index + 1,
            cusp_longitude=_longitude_value(cusps[index]),
            sign=sign_fact(sign_index(cusps[index])),
        )
        for index in range(12)
    ]
    sun_longitude = by_name["sun"].longitude.decimal_degrees
    planet_facts: list[PlanetChartFact] = []
    for name, position in by_name.items():
        sign = sign_index(position.longitude.decimal_degrees)
        distance_from_sun = _angular_distance(position.longitude.decimal_degrees, sun_longitude)
        limit = COMBUSTION_LIMITS.get(name, 0.0)
        planet_facts.append(
            PlanetChartFact(
                position=position,
                sign=sign_fact(sign),
                house=((sign - sign_index(ascendant)) % 12) + 1,
                nakshatra=nakshatra_fact(position.longitude.decimal_degrees),
                dignity=dignity(name, sign),
                retrograde=position.retrograde,
                combust=name != "sun" and limit > 0 and distance_from_sun <= limit,
                cazimi=name != "sun" and distance_from_sun <= 1.0,
            )
        )
    return BirthChart(
        provenance=position_result.provenance,
        julian_day_ut=jd,
        ascendant=AscendantFact(
            longitude=_longitude_value(ascendant), sign=sign_fact(sign_index(ascendant))
        ),
        houses=houses,
        planets=planet_facts,
        warnings=position_result.warnings,
        explain_calculation={
            "houses": "Swiss Ephemeris houses_ex with whole-sign planet house assignment",
            "nakshatra": "27 equal nakshatras of 13°20' with four padas",
            "combustion": "configurable angular distance thresholds from Sun",
        },
    )
