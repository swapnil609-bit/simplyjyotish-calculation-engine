from __future__ import annotations

from simplyjyotish_engine.models.chart import BirthChart
from simplyjyotish_engine.models.varga import DivisionalChart, VargaPlanet
from simplyjyotish_engine.vedic.reference import sign_fact, sign_index

DIVISION_NAMES = {1: "Rashi", 9: "Navamsha", 10: "Dashamsha", 60: "Shashtiamsha"}


def _varga_sign(source_sign: int, part: int, division: int) -> int:
    if division == 1:
        return source_sign
    if division == 9:
        # Movable signs begin at themselves, fixed signs at the 9th sign,
        # and dual signs at the 5th sign.
        modality = ("movable", "fixed", "dual")[source_sign % 3]
        start_offset = {"movable": 0, "fixed": 8, "dual": 4}[modality]
        return (source_sign + start_offset + part - 1) % 12
    if division == 10:
        # Parashara Dashamsha: odd signs count from themselves; even signs
        # count from the 9th sign.
        start_offset = 0 if source_sign % 2 == 0 else 8
        return (source_sign + start_offset + part - 1) % 12
    if division == 60:
        # Common Parashari Shashtiamsha sign convention: forward for odd
        # signs and reverse for even signs. Names are intentionally deferred.
        direction = 1 if source_sign % 2 == 0 else -1
        return (source_sign + direction * (part - 1)) % 12
    raise ValueError(f"Unsupported validated varga division: D{division}")


def calculate_varga(chart: BirthChart, division: int) -> DivisionalChart:
    if division not in DIVISION_NAMES:
        raise ValueError("Milestone 3 supports divisions D1, D9, D10, and D60")
    planets: list[VargaPlanet] = []
    for planet in chart.planets:
        longitude = planet.position.longitude.decimal_degrees
        source_sign = sign_index(longitude)
        part = min(division, int((longitude % 30.0) / (30.0 / division)) + 1)
        planets.append(
            VargaPlanet(
                planet=planet.position.planet,
                source_longitude_degrees=longitude,
                source_sign=sign_fact(source_sign),
                division_part=part,
                varga_sign=sign_fact(_varga_sign(source_sign, part, division)),
            )
        )
    return DivisionalChart(
        division=division,
        name=DIVISION_NAMES[division],
        convention="Parashari sign-based mapping; D60 uses forward odd/reverse even convention",
        provenance=chart.provenance,
        planets=planets,
    )
