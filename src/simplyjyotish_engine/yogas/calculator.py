from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from simplyjyotish_engine.models.chart import BirthChart, PlanetChartFact
from simplyjyotish_engine.models.conditions import YogaDetectionResult, YogaFact
from simplyjyotish_engine.models.validation import ValidationStatus

YOGA_CONVENTION = "classical_objective_yogas_parashari_v1"
SOURCE = ("BPHS yoga chapters; Jataka Parijata yoga definitions; source review pending",)
BENEFICS = {"mercury", "jupiter", "venus"}
NATURAL_MALEFICS = {"sun", "mars", "saturn", "rahu", "ketu"}
MAHAPURUSHA = {
    "mars": "ruchaka",
    "mercury": "bhadra",
    "jupiter": "hamsa",
    "venus": "malavya",
    "saturn": "shasha",
}
EXALTATION = {"sun": 0, "moon": 1, "mars": 9, "mercury": 5, "jupiter": 3, "venus": 11, "saturn": 6}


def _facts(chart: BirthChart) -> dict[str, PlanetChartFact]:
    return {item.position.planet: item for item in chart.planets}


def _from_house(first: int, second: int) -> int:
    return (second - first) % 12 + 1


def _in(items: Iterable[str], value: str) -> bool:
    return value in set(items)


def _status() -> ValidationStatus:
    return ValidationStatus(
        source_verified=True,
        cross_implementation_verified=False,
        expert_reviewed=False,
        source_reference_ids=("bphs_yoga_definitions_v1",),
        notes=("Objective condition only; no outcome or interpretation is emitted.",),
    )


def _fact(
    yoga_id: str,
    detected: bool,
    *,
    planets: Iterable[str] = (),
    houses: Iterable[int] = (),
    facts: dict[str, Any],
    satisfied: Iterable[str] = (),
    not_satisfied: Iterable[str] = (),
    cancellation: Iterable[str] = (),
    version: str = YOGA_CONVENTION,
) -> YogaFact:
    return YogaFact(
        yoga_id=yoga_id,
        convention_version=version,
        detected=detected,
        planets_involved=tuple(planets),
        houses_involved=tuple(sorted(set(houses))),
        exact_calculation_facts=facts,
        conditions_satisfied=tuple(satisfied),
        conditions_not_satisfied=tuple(not_satisfied),
        cancellation_or_weakening_factors=tuple(cancellation),
        source_citation=SOURCE,
        validation_status=_status(),
    )


def calculate_yogas(chart: BirthChart) -> YogaDetectionResult:
    """Return objective yoga condition facts under a conservative v1 convention."""
    by = _facts(chart)
    moon = by["moon"]
    lagna = chart.ascendant.sign.index
    result: list[YogaFact] = []

    for planet, yoga_name in MAHAPURUSHA.items():
        item = by[planet]
        kendra = item.house in {1, 4, 7, 10}
        dignity = item.dignity.status in {"own_sign", "exalted"}
        result.append(
            _fact(
                f"panch_mahapurusha_{yoga_name}",
                kendra and dignity,
                planets=(planet,),
                houses=(item.house,),
                facts={
                    "planet_house": item.house,
                    "sign_index": item.sign.index,
                    "dignity": item.dignity.status,
                    "kendra_houses": [1, 4, 7, 10],
                },
                satisfied=("planet_in_kendra", "planet_in_own_or_exaltation_sign")
                if kendra and dignity
                else (),
                not_satisfied=tuple(
                    x
                    for x, ok in (
                        ("planet_in_kendra", kendra),
                        ("planet_in_own_or_exaltation_sign", dignity),
                    )
                    if not ok
                ),
            )
        )

    def same_house(identifier: str, names: tuple[str, ...]) -> YogaFact:
        houses = tuple(by[name].house for name in names)
        detected = len(set(houses)) == 1
        return _fact(
            identifier,
            detected,
            planets=names,
            houses=houses,
            facts={"planet_houses": dict(zip(names, houses, strict=True))},
            satisfied=("same_house",) if detected else (),
            not_satisfied=() if detected else ("same_house",),
        )

    result.extend(
        (
            same_house("gaja_kesari", ("moon", "jupiter")),
            same_house("budhaditya", ("sun", "mercury")),
            same_house("chandra_mangala", ("moon", "mars")),
        )
    )

    benefic_from_moon = tuple(
        name for name in BENEFICS if _from_house(moon.house, by[name].house) in {6, 7, 8}
    )
    result.append(
        _fact(
            "adhi",
            bool(benefic_from_moon),
            planets=("moon",) + benefic_from_moon,
            houses=(moon.house,) + tuple(by[name].house for name in benefic_from_moon),
            facts={
                "benefics_in_6_7_8_from_moon": list(benefic_from_moon),
                "required_rule": "at_least_one",
            },
            satisfied=("benefic_in_6_7_8_from_moon",) if benefic_from_moon else (),
            not_satisfied=() if benefic_from_moon else ("benefic_in_6_7_8_from_moon",),
            version="adhi_any_benefic_from_moon_v1",
        )
    )

    amala_candidates = tuple(
        name
        for name in BENEFICS
        if by[name].house == 10 or _from_house(moon.house, by[name].house) == 10
    )
    result.append(
        _fact(
            "amala",
            bool(amala_candidates),
            planets=amala_candidates,
            houses=tuple(by[name].house for name in amala_candidates),
            facts={"benefics_tenth_from_lagna_or_moon": list(amala_candidates)},
            satisfied=("benefic_in_tenth_from_lagna_or_moon",) if amala_candidates else (),
            not_satisfied=() if amala_candidates else ("benefic_in_tenth_from_lagna_or_moon",),
        )
    )

    second = tuple(
        name
        for name, item in by.items()
        if name != "sun" and _from_house(moon.house, item.house) == 2
    )
    twelfth = tuple(
        name
        for name, item in by.items()
        if name != "sun" and _from_house(moon.house, item.house) == 12
    )
    for identifier, names, rule in (
        ("sunapha", second, "planet_in_second_from_moon"),
        ("anapha", twelfth, "planet_in_twelfth_from_moon"),
        ("durudhara", second + twelfth, "planets_on_both_sides_of_moon"),
    ):
        detected = bool(second and twelfth) if identifier == "durudhara" else bool(names)
        result.append(
            _fact(
                identifier,
                detected,
                planets=("moon",) + tuple(names),
                houses=(moon.house,) + tuple(by[name].house for name in names),
                facts={"second_from_moon": list(second), "twelfth_from_moon": list(twelfth)},
                satisfied=(rule,) if detected else (),
                not_satisfied=() if detected else (rule,),
            )
        )

    occupied = {item.house for name, item in by.items() if name not in {"sun", "moon"}}
    kemadruma_cancel = []
    if moon.house in {1, 4, 7, 10}:
        kemadruma_cancel.append("moon_in_kendra_from_lagna")
    if any(
        _from_house(moon.house, item.house) in {1, 4, 7, 10}
        for name, item in by.items()
        if name not in {"sun", "moon"}
    ):
        kemadruma_cancel.append("planet_in_kendra_from_moon")
    kemadruma_raw = not second and not twelfth
    result.append(
        _fact(
            "kemadruma",
            kemadruma_raw and not kemadruma_cancel,
            planets=("moon",),
            houses=(moon.house,),
            facts={
                "second_from_moon": list(second),
                "twelfth_from_moon": list(twelfth),
                "occupied_houses_excluding_sun_moon": sorted(occupied),
            },
            satisfied=("no_planet_second_or_twelfth_from_moon",) if kemadruma_raw else (),
            not_satisfied=() if kemadruma_raw else ("no_planet_second_or_twelfth_from_moon",),
            cancellation=kemadruma_cancel,
            version="kemadruma_with_explicit_cancellations_v1",
        )
    )

    # Sign-lord exchanges and their house classification.
    exchanges: list[tuple[str, str, int, int]] = []
    for first, first_item in by.items():
        if first in {"rahu", "ketu"}:
            continue
        for second_name, second_item in by.items():
            if first >= second_name or second_name in {"rahu", "ketu"}:
                continue
            if first_item.sign.lord == second_name and second_item.sign.lord == first:
                exchanges.append((first, second_name, first_item.house, second_item.house))
    for first, second_name, first_house, second_house in exchanges:
        if {first_house, second_house} & {6, 8, 12}:
            kind = "dainya"
        elif {first_house, second_house} & {3, 11}:
            kind = "khala"
        else:
            kind = "maha"
        result.append(
            _fact(
                "parivartana",
                True,
                planets=(first, second_name),
                houses=(first_house, second_house),
                facts={
                    "exchange_type": kind,
                    "first_lord_house": first_house,
                    "second_lord_house": second_house,
                },
                satisfied=("mutual_sign_lord_exchange",),
                version="parivartana_house_classification_v1",
            )
        )
    if not exchanges:
        result.append(
            _fact(
                "parivartana",
                False,
                facts={"exchange_count": 0},
                not_satisfied=("mutual_sign_lord_exchange",),
                version="parivartana_house_classification_v1",
            )
        )

    exchange_pairs = {(first, second) for first, second, _, _ in exchanges}

    # Generic lord connection families are intentionally fact-level, not outcome claims.
    house_lord = {
        house: next(
            (name for name, item in by.items() if item.sign.index == (lagna + house - 1) % 12), None
        )
        for house in range(1, 13)
    }

    def connected(first_house: int, second_house: int) -> tuple[bool, tuple[str, ...]]:
        first_lord, second_lord = house_lord[first_house], house_lord[second_house]
        if first_lord is None or second_lord is None:
            return False, ()
        connected_value = (
            by[first_lord].house == by[second_lord].house
            or (
                first_lord,
                second_lord,
            )
            in exchange_pairs
        )
        return connected_value, (first_lord, second_lord)

    for identifier, pairs, version in (
        (
            "raja_yoga",
            ((1, 5), (1, 9), (4, 5), (4, 9), (7, 5), (7, 9), (10, 5), (10, 9)),
            "raja_yoga_kendra_trikona_connection_v1",
        ),
        (
            "dhana_yoga",
            ((2, 5), (2, 9), (11, 5), (11, 9), (2, 11)),
            "dhana_yoga_lord_connection_v1",
        ),
        (
            "vipareeta_raja_yoga",
            ((6, 8), (6, 12), (8, 12)),
            "vipareeta_raja_yoga_dusthana_lord_connection_v1",
        ),
        ("dharma_karmadhipati", ((9, 10),), "dharma_karmadhipati_lord_connection_v1"),
    ):
        matches = [(a, b, connected(a, b)[1]) for a, b in pairs if connected(a, b)[0]]
        result.append(
            _fact(
                identifier,
                bool(matches),
                planets=tuple(name for _, _, names in matches for name in names),
                houses=tuple(h for match in matches for h in match[:2]),
                facts={
                    "matching_house_lord_pairs": [[a, b, list(names)] for a, b, names in matches]
                },
                satisfied=("configured_lord_connection",) if matches else (),
                not_satisfied=() if matches else ("configured_lord_connection",),
                version=version,
            )
        )

    debilitation_facts = []
    for name, item in by.items():
        if item.dignity.status == "debilitated":
            cancellation = []
            deb_lord = item.sign.lord
            if by.get(deb_lord) and by[deb_lord].house in {1, 4, 7, 10}:
                cancellation.append("lord_of_debilitation_sign_in_kendra")
            debilitation_facts.append((name, item.house, cancellation))
    result.append(
        _fact(
            "neecha_bhanga",
            bool(debilitation_facts and any(c for _, _, c in debilitation_facts)),
            planets=tuple(n for n, _, _ in debilitation_facts),
            houses=tuple(h for _, h, _ in debilitation_facts),
            facts={
                "debilitated_planets": [
                    {"planet": n, "house": h, "cancellations": c} for n, h, c in debilitation_facts
                ]
            },
            satisfied=("debilitated_planet_has_configured_cancellation",)
            if any(c for _, _, c in debilitation_facts)
            else (),
            not_satisfied=()
            if any(c for _, _, c in debilitation_facts)
            else ("debilitated_planet_has_configured_cancellation",),
            cancellation=tuple(
                f"{n}:{item}" for n, _, factors in debilitation_facts for item in factors
            ),
            version="neecha_bhanga_minimal_kendra_rule_v1",
        )
    )

    all_houses = [item.house for item in by.values()]
    result.append(
        _fact(
            "nabhassa_chatussagara",
            set(all_houses) <= {1, 4, 7, 10} and len(all_houses) == len(by),
            planets=tuple(by),
            houses=tuple(
                sorted(set(all_houses)),
            ),
            facts={"planet_houses": all_houses, "required_houses": [1, 4, 7, 10]},
            satisfied=("all_recorded_planets_in_kendras",)
            if set(all_houses) <= {1, 4, 7, 10}
            else (),
            not_satisfied=()
            if set(all_houses) <= {1, 4, 7, 10}
            else ("all_recorded_planets_in_kendras",),
            version="nabhassa_chatussagara_whole_sign_v1",
        )
    )
    return YogaDetectionResult(
        provenance=chart.provenance,
        convention_version=YOGA_CONVENTION,
        yogas=result,
        warnings=["Cross-implementation validation is pending for yoga detector families."],
    )
