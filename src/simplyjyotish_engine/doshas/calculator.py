from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from simplyjyotish_engine.models.chart import BirthChart
from simplyjyotish_engine.models.conditions import DoshaDetectionResult, DoshaFact
from simplyjyotish_engine.models.validation import ValidationStatus

MALEFICS = {"sun", "mars", "saturn", "rahu", "ketu"}
SOURCE = (
    "BPHS condition chapters; classical Jyotisha convention catalogue; source review pending",
)


def _status(*notes: str) -> ValidationStatus:
    return ValidationStatus(
        source_verified=True,
        cross_implementation_verified=False,
        expert_reviewed=False,
        source_reference_ids=("bphs_condition_definitions_v1",),
        notes=notes,
    )


def _distance(a: float, b: float) -> float:
    return abs((a - b + 180.0) % 360.0 - 180.0)


def _house_distance(first: int, second: int) -> int:
    return (second - first) % 12 + 1


def _condition(
    condition_id: str,
    detected: bool,
    *,
    version: str,
    raw: dict[str, Any],
    planets: Iterable[str] = (),
    houses: Iterable[int] = (),
    exceptions: Iterable[str] = (),
    severity: Iterable[str] = (),
    notes: tuple[str, ...] = (),
) -> DoshaFact:
    return DoshaFact(
        condition_id=condition_id,
        convention_version=version,
        detected=detected,
        raw_condition=raw,
        exceptions_and_cancellations=tuple(exceptions),
        severity_factors=tuple(severity),
        planets_involved=tuple(planets),
        houses_involved=tuple(sorted(set(houses))),
        source_citation=SOURCE,
        validation_status=_status(*notes),
    )


def calculate_doshas(
    chart: BirthChart,
    manglik_houses: tuple[int, ...] = (1, 2, 4, 7, 8, 12),
    conjunction_orb_degrees: float = 12.0,
) -> DoshaDetectionResult:
    by = {item.position.planet: item for item in chart.planets}
    result: list[DoshaFact] = []
    manglik_houses_found = [
        point
        for point, house in (("lagna", 1), ("moon", by["moon"].house))
        if by["mars"].house in manglik_houses
        if point == "lagna" or _house_distance(house, by["mars"].house) in manglik_houses
    ]
    result.append(
        _condition(
            "manglik_kuja_dosha",
            bool(manglik_houses_found),
            version="manglik_houses_lagna_moon_v1",
            raw={
                "mars_house_from_lagna": by["mars"].house,
                "mars_house_from_moon": _house_distance(by["moon"].house, by["mars"].house),
                "configured_houses": list(manglik_houses),
            },
            planets=("mars",),
            houses=(by["mars"].house,),
            exceptions=("cancellation_rules_not_applied_in_raw_condition",),
            severity=("reference_points_lagna_and_moon",),
        )
    )

    rahu, ketu = by["rahu"], by["ketu"]
    non_nodes = [item for name, item in by.items() if name not in {"rahu", "ketu"}]

    def in_arc(start: int, sign: int) -> bool:
        return (sign - start) % 12 <= 6

    forward = all(in_arc(rahu.sign.index, item.sign.index) for item in non_nodes)
    reverse = all(in_arc(ketu.sign.index, item.sign.index) for item in non_nodes)
    result.append(
        _condition(
            "kala_sarpa_pattern",
            forward or reverse,
            version="kala_sarpa_nodes_inclusive_two_arcs_v1",
            raw={
                "rahu_sign": rahu.sign.index,
                "ketu_sign": ketu.sign.index,
                "forward_arc_contains_all": forward,
                "reverse_arc_contains_all": reverse,
                "planet_signs": {name: item.sign.index for name, item in by.items()},
            },
            planets=tuple(by),
            exceptions=("empty_arc_and_cancellation_traditions_are_not_applied",),
            notes=("Pattern detection is separate from any interpretive claim.",),
        )
    )

    for planet, identifier in (("sun", "grahan_solar"), ("moon", "grahan_lunar")):
        near = [
            node
            for node in ("rahu", "ketu")
            if _distance(
                by[planet].position.longitude.decimal_degrees,
                by[node].position.longitude.decimal_degrees,
            )
            <= conjunction_orb_degrees
        ]
        result.append(
            _condition(
                identifier,
                bool(near),
                version="grahan_conjunction_orb_v1",
                raw={
                    "orb_degrees": conjunction_orb_degrees,
                    "node_distances": {
                        node: _distance(
                            by[planet].position.longitude.decimal_degrees,
                            by[node].position.longitude.decimal_degrees,
                        )
                        for node in ("rahu", "ketu")
                    },
                },
                planets=(planet,) + tuple(near),
                houses=(by[planet].house,),
            )
        )

    for planet, identifier in (("jupiter", "guru_chandal"), ("saturn", "shrapit")):
        near = [
            node
            for node in ("rahu", "ketu")
            if _distance(
                by[planet].position.longitude.decimal_degrees,
                by[node].position.longitude.decimal_degrees,
            )
            <= conjunction_orb_degrees
        ]
        result.append(
            _condition(
                identifier,
                bool(near),
                version="node_conjunction_orb_v1",
                raw={
                    "orb_degrees": conjunction_orb_degrees,
                    "node_distances": {
                        node: _distance(
                            by[planet].position.longitude.decimal_degrees,
                            by[node].position.longitude.decimal_degrees,
                        )
                        for node in ("rahu", "ketu")
                    },
                },
                planets=(planet,) + tuple(near),
                houses=(by[planet].house,),
            )
        )

    second = [
        name
        for name, item in by.items()
        if name != "sun" and _house_distance(by["moon"].house, item.house) == 2
    ]
    twelfth = [
        name
        for name, item in by.items()
        if name != "sun" and _house_distance(by["moon"].house, item.house) == 12
    ]
    result.append(
        _condition(
            "kemadruma",
            not second and not twelfth,
            version="kemadruma_raw_no_planet_sides_v1",
            raw={"second_from_moon": second, "twelfth_from_moon": twelfth},
            planets=("moon",),
            exceptions=("cancellation_factors_are_reported_by_yoga_detector",),
        )
    )

    for name, item in by.items():
        if name == "sun":
            continue
        result.append(
            _condition(
                "combustion",
                item.combust,
                version="combustion_chart_fact_v1",
                raw={"combust": item.combust, "cazimi": item.cazimi},
                planets=(name,),
                houses=(item.house,),
                exceptions=("cazimi_is_reported_as_a_separate_fact",),
            )
        )
    for name, item in by.items():
        result.append(
            _condition(
                "debilitation",
                item.dignity.status == "debilitated",
                version="dignity_reference_table_v1",
                raw={"dignity_status": item.dignity.status, "sign_index": item.sign.index},
                planets=(name,),
                houses=(item.house,),
            )
        )

    for target in (*by, "lagna"):
        target_item = by.get(target)
        if target == "lagna":
            house = 1
        else:
            assert target_item is not None
            house = target_item.house
        preceding = [
            name
            for name, other in by.items()
            if other.house == (house - 2) % 12 + 1 and name in MALEFICS
        ]
        following = [
            name for name, other in by.items() if other.house == house % 12 + 1 and name in MALEFICS
        ]
        result.append(
            _condition(
                "papakartari",
                bool(preceding and following),
                version="papakartari_adjacent_house_malefics_v1",
                raw={
                    "preceding_malefics": preceding,
                    "following_malefics": following,
                    "target": target,
                },
                planets=tuple(preceding + following),
                houses=(house,),
            )
        )

    for target in ("moon", "lagna"):
        target_item = by.get(target)
        if target == "lagna":
            longitude = chart.ascendant.longitude.decimal_degrees
            target_houses: tuple[int, ...] = ()
        else:
            assert target_item is not None
            longitude = target_item.position.longitude.decimal_degrees
            target_houses = (target_item.house,)
        junctions = (0.0, 120.0, 240.0)
        distance = min(
            abs((longitude - junction + 180.0) % 360.0 - 180.0) for junction in junctions
        )
        result.append(
            _condition(
                "gandanta",
                distance <= 0.8,
                version="gandanta_water_fire_junction_48_minutes_v1",
                raw={
                    "longitude": longitude,
                    "nearest_junction_distance": distance,
                    "threshold_degrees": 0.8,
                },
                planets=() if target == "lagna" else (target,),
                houses=target_houses,
            )
        )

    result.append(
        _condition(
            "mrityu_bhaga",
            False,
            version="mrityu_bhaga_unimplemented_v1",
            raw={"available": False},
            notes=(
                "No single reliable source table is bundled; detector intentionally returns "
                "not detected.",
            ),
        )
    )
    return DoshaDetectionResult(
        provenance=chart.provenance,
        convention_version="objective_doshas_and_conditions_v1",
        conditions=result,
        warnings=[
            "Exceptions, cancellations and severity factors are not predictions and require "
            "separate convention review."
        ],
    )
