from __future__ import annotations

from simplyjyotish_engine.models.chart import DignityFact
from simplyjyotish_engine.vedic.reference import SIGNS

EXALTATION = {"sun": 0, "moon": 1, "mars": 9, "mercury": 5, "jupiter": 3, "venus": 11, "saturn": 6}
DEBILITATION = {planet: (sign + 6) % 12 for planet, sign in EXALTATION.items()}
OWN_SIGNS = {
    "sun": {4},
    "moon": {3},
    "mars": {0, 7},
    "mercury": {2, 5},
    "jupiter": {8, 11},
    "venus": {1, 6},
    "saturn": {9, 10},
}


def dignity(planet: str, sign_index: int) -> DignityFact:
    reference_sign = SIGNS[sign_index][0]
    if planet in EXALTATION and sign_index == EXALTATION[planet]:
        return DignityFact(status="exalted", reference_sign=reference_sign)
    if planet in DEBILITATION and sign_index == DEBILITATION[planet]:
        return DignityFact(status="debilitated", reference_sign=reference_sign)
    if sign_index in OWN_SIGNS.get(planet, set()):
        return DignityFact(status="own_sign", reference_sign=reference_sign)
    return DignityFact(status="other")
