from __future__ import annotations

from zoneinfo import ZoneInfo

from simplyjyotish_engine.aspects.relationships import calculate_relationships
from simplyjyotish_engine.models.advanced import (
    BhavaStrength,
    PlanetStrength,
    ShadbalaResult,
    StrengthComponent,
)
from simplyjyotish_engine.models.chart import BirthChart
from simplyjyotish_engine.models.validation import ReleaseStatus, ValidationStatus
from simplyjyotish_engine.vargas.framework import calculate_varga
from simplyjyotish_engine.vedic.dignity import EXALTATION, OWN_SIGNS

EXALTATION_DEGREES = {
    "sun": 10.0,
    "moon": 33.0,
    "mars": 298.0,
    "mercury": 165.0,
    "jupiter": 95.0,
    "venus": 357.0,
    "saturn": 200.0,
}
NAISARGIKA = {
    "sun": 60.0,
    "moon": 51.43,
    "mars": 17.14,
    "mercury": 25.71,
    "jupiter": 34.29,
    "venus": 42.86,
    "saturn": 8.57,
}
DIG_BEST_HOUSES = {
    "sun": 10,
    "mars": 10,
    "moon": 4,
    "venus": 4,
    "mercury": 1,
    "jupiter": 1,
    "saturn": 7,
}
BENEFICS = {"moon", "mercury", "jupiter", "venus"}


def _component(name: str, total: float, **subcomponents: float) -> StrengthComponent:
    return StrengthComponent(
        name=name,
        total_virupas=round(total, 6),
        subcomponents={key: round(value, 6) for key, value in subcomponents.items()},
    )


def _uchcha(planet: str, longitude: float) -> float:
    if planet not in EXALTATION_DEGREES:
        return 0.0
    distance = (longitude - (EXALTATION_DEGREES[planet] + 180.0)) % 360.0
    return min(distance, 360.0 - distance) / 180.0 * 60.0


def _sthana(chart: BirthChart, planet_name: str) -> StrengthComponent:
    planet = next(item for item in chart.planets if item.position.planet == planet_name)
    uchcha = _uchcha(planet_name, planet.position.longitude.decimal_degrees)
    varga_scores = []
    for division in (1, 2, 3, 7, 9, 12, 30):
        varga = calculate_varga(chart, division)
        placement = next(item for item in varga.planets if item.planet == planet_name)
        varga_scores.append(
            20.0 if placement.varga_sign.index in OWN_SIGNS.get(planet_name, set()) else 5.0
        )
    saptavargaja = sum(varga_scores) / len(varga_scores)
    ojayugma = (
        15.0
        if (planet_name in {"sun", "mars", "jupiter"} and planet.sign.index % 2 == 0)
        or (planet_name in {"moon", "venus"} and planet.sign.index % 2 == 1)
        else 7.5
    )
    kendradi = (
        60.0 if planet.house in {1, 4, 7, 10} else 30.0 if planet.house in {2, 5, 8, 11} else 15.0
    )
    drekkana = 15.0 if planet.house in {1, 5, 9} else 7.5
    return _component(
        "sthana_bala",
        uchcha + saptavargaja + ojayugma + kendradi + drekkana,
        uchcha_bala=uchcha,
        saptavargaja_bala=saptavargaja,
        ojayugma=ojayugma,
        kendradi=kendradi,
        drekkana=drekkana,
    )


def _dig(planet_name: str, house: int) -> StrengthComponent:
    best = DIG_BEST_HOUSES.get(planet_name, 1)
    distance = min((house - best) % 12, (best - house) % 12)
    return _component(
        "dig_bala",
        max(0.0, 60.0 * (1.0 - distance / 6.0)),
        distance_from_best_house=float(distance),
    )


def _kaala(chart: BirthChart, planet_name: str) -> StrengthComponent:
    local_hour = chart.provenance.resolved_utc.astimezone(
        ZoneInfo(chart.provenance.source_input_timezone)
    ).hour
    diurnal = 6 <= local_hour < 18
    day_strength = (
        20.0
        if (planet_name in {"sun", "jupiter", "venus"} and diurnal)
        or (planet_name in {"moon", "mars", "saturn"} and not diurnal)
        else 10.0
    )
    moon = next(item for item in chart.planets if item.position.planet == "moon")
    sun = next(item for item in chart.planets if item.position.planet == "sun")
    phase = (
        moon.position.longitude.decimal_degrees - sun.position.longitude.decimal_degrees
    ) % 360.0
    paksha = 30.0 * (1.0 - abs(phase - 180.0) / 180.0)
    return _component(
        "kaala_bala",
        day_strength + paksha + 10.0,
        natonnata=day_strength,
        paksha=paksha,
        tribhaga=10.0,
    )


def _cheshta(chart: BirthChart, planet_name: str) -> StrengthComponent:
    planet = next(item for item in chart.planets if item.position.planet == planet_name)
    value = 30.0 if planet_name in {"sun", "moon"} else 60.0 if planet.retrograde else 30.0
    return _component("cheshta_bala", value, motion=value)


def _drik(chart: BirthChart, planet_name: str) -> StrengthComponent:
    relationships = calculate_relationships(chart)
    value = sum(
        15.0 if aspect.source in BENEFICS else -15.0
        for aspect in relationships.graha_drishti
        if aspect.target == planet_name
    )
    return _component("drik_bala", value, aspect_contribution=value)


def _vimsopaka(chart: BirthChart, planet_name: str) -> float:
    scores = []
    for division in (1, 2, 3, 7, 9, 10, 12, 16, 30, 60):
        placement = next(
            item for item in calculate_varga(chart, division).planets if item.planet == planet_name
        )
        scores.append(
            20.0
            if placement.varga_sign.index in OWN_SIGNS.get(planet_name, set())
            or (planet_name in EXALTATION and placement.varga_sign.index == EXALTATION[planet_name])
            else 5.0
        )
    return sum(scores) / len(scores)


def calculate_shadbala(chart: BirthChart) -> ShadbalaResult:
    strengths: list[PlanetStrength] = []
    for planet in chart.planets:
        name = planet.position.planet
        if name not in NAISARGIKA:
            continue
        components = [
            _sthana(chart, name),
            _dig(name, planet.house),
            _kaala(chart, name),
            _cheshta(chart, name),
            _component("naisargika_bala", NAISARGIKA[name], fixed=NAISARGIKA[name]),
            _drik(chart, name),
        ]
        total = sum(component.total_virupas for component in components)
        ishta = max(
            0.0,
            min(
                100.0,
                components[0].subcomponents["uchcha_bala"] * components[3].total_virupas / 36.0,
            ),
        )
        strengths.append(
            PlanetStrength(
                planet=name,
                components=components,
                shadbala_total_virupas=total,
                shadbala_total_rupas=total / 60.0,
                ishta_phala=ishta,
                kashta_phala=100.0 - ishta,
                vimsopaka_bala=_vimsopaka(chart, name),
            )
        )
    by_planet = {item.planet: item.shadbala_total_virupas for item in strengths}
    houses = []
    for house in range(1, 13):
        house_fact = chart.houses[house - 1]
        occupied = sum(
            by_planet.get(item.position.planet, 0.0)
            for item in chart.planets
            if item.house == house
        )
        houses.append(
            BhavaStrength(
                house=house,
                bala_virupas=by_planet.get(house_fact.sign.lord, 0.0) + occupied / 4.0,
                lord=house_fact.sign.lord,
            )
        )
    return ShadbalaResult(
        provenance=chart.provenance,
        method_id="parashara_shadbala_v1",
        planets=strengths,
        bhava_bala=houses,
        warnings=[
            "component formulas are deterministic and source-documented; expert "
            "convention review pending"
        ],
        explain_calculation={
            "sthana_bala": "uchcha, saptavargaja, ojayugma, kendradi, and drekkana subcomponents",
            "dig_bala": "distance from planet-specific directional-strength house",
            "kaala_bala": "diurnal, paksha, and tribhaga default components",
            "cheshta_bala": "retrograde motion receives the configured maximum default",
            "drik_bala": "net graha-drishti contribution",
            "ishta_kashta": "normalized uccha × cheshta derived pair",
            "vimsopaka": "equal weighted dignity score across ten configured vargas",
        },
        validation_status=ValidationStatus(
            release_status=ReleaseStatus.EXPERIMENTAL,
            source_verified=False,
            cross_implementation_verified=False,
            source_reference_ids=("bphs_chapter_26", "pyjhora_4_8_7_vp_jain"),
            notes=(
                "Provisional component formulas are retained without parity tuning; "
                "source verification is pending identical formula/configuration mapping.",
            ),
        ),
    )
