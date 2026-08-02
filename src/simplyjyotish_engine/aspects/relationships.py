from __future__ import annotations

from itertools import combinations

from simplyjyotish_engine.models.advanced import (
    AspectFact,
    ConjunctionFact,
    DispositorChain,
    ExchangeFact,
    GrahaYuddhaFact,
    PapakartariFact,
    RelationshipResult,
)
from simplyjyotish_engine.models.chart import BirthChart, PlanetChartFact
from simplyjyotish_engine.vargas.parashara_bphs import DUAL_SIGNS, FIXED_SIGNS, MOVABLE_SIGNS

GRAHA_METHOD = "parashari_graha_drishti_v1"
JAIMINI_METHOD = "jaimini_rashi_drishti_v1"
YUDDHA_METHOD = "graha_yuddha_longitude_with_latitude_tiebreak_v1"
SPECIAL_ASPECTS = {"mars": (4, 8), "jupiter": (5, 9), "saturn": (3, 10)}
NATURAL_MALEFICS = {"sun", "mars", "saturn", "rahu", "ketu"}


def _planet_map(chart: BirthChart) -> dict[str, PlanetChartFact]:
    return {planet.position.planet: planet for planet in chart.planets}


def _graha_drishti(chart: BirthChart) -> list[AspectFact]:
    facts: list[AspectFact] = []
    for source in chart.planets:
        source_sign = source.sign.index
        distances = {7, *SPECIAL_ASPECTS.get(source.position.planet, ())}
        for target in chart.planets:
            if target.position.planet == source.position.planet:
                continue
            sign_distance = (target.sign.index - source_sign) % 12 + 1
            if sign_distance in distances:
                aspect_type = "seventh" if sign_distance == 7 else f"special_{sign_distance}"
                facts.append(
                    AspectFact(
                        source=source.position.planet,
                        target=target.position.planet,
                        method_id=GRAHA_METHOD,
                        aspect_type=aspect_type,
                        orb_degrees=0.0,
                        from_sign_index=source.sign.index,
                        to_sign_index=target.sign.index,
                        from_house=source.house,
                        to_house=target.house,
                    )
                )
    return facts


def _jaimini(chart: BirthChart) -> list[AspectFact]:
    facts: list[AspectFact] = []
    for source in chart.planets:
        for target in chart.planets:
            if source.position.planet == target.position.planet:
                continue
            source_sign, target_sign = source.sign.index, target.sign.index
            if source_sign in MOVABLE_SIGNS:
                applies = target_sign in FIXED_SIGNS and target_sign not in {
                    (source_sign + 3) % 12,
                    (source_sign - 3) % 12,
                }
            elif source_sign in FIXED_SIGNS:
                applies = target_sign in MOVABLE_SIGNS and target_sign not in {
                    (source_sign + 3) % 12,
                    (source_sign - 3) % 12,
                }
            else:
                applies = (
                    source_sign in DUAL_SIGNS
                    and target_sign in DUAL_SIGNS
                    and target_sign != source_sign
                )
            if applies:
                facts.append(
                    AspectFact(
                        source=source.position.planet,
                        target=target.position.planet,
                        method_id=JAIMINI_METHOD,
                        aspect_type="rashi",
                        orb_degrees=0.0,
                        from_sign_index=source_sign,
                        to_sign_index=target_sign,
                        from_house=source.house,
                        to_house=target.house,
                    )
                )
    return facts


def calculate_relationships(
    chart: BirthChart, conjunction_orb_degrees: float = 8.0
) -> RelationshipResult:
    if not 0 < conjunction_orb_degrees <= 30:
        raise ValueError("conjunction_orb_degrees must be in (0, 30]")
    planets = _planet_map(chart)
    conjunctions: list[ConjunctionFact] = []
    exchanges: list[ExchangeFact] = []
    yuddha: list[GrahaYuddhaFact] = []
    for first, second in combinations(chart.planets, 2):
        first_longitude = first.position.longitude.decimal_degrees
        second_longitude = second.position.longitude.decimal_degrees
        separation = abs((first_longitude - second_longitude + 180) % 360 - 180)
        if separation <= conjunction_orb_degrees:
            conjunctions.append(
                ConjunctionFact(
                    first=first.position.planet,
                    second=second.position.planet,
                    orb_degrees=separation,
                    configured_orb_degrees=conjunction_orb_degrees,
                )
            )
        if first.sign.lord == second.position.planet and second.sign.lord == first.position.planet:
            exchanges.append(
                ExchangeFact(
                    first=first.position.planet,
                    second=second.position.planet,
                    first_sign_index=first.sign.index,
                    second_sign_index=second.sign.index,
                )
            )
        classical = {"sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn"}
        if (
            first.position.planet in classical
            and second.position.planet in classical
            and first.sign.index == second.sign.index
            and separation <= 1.0
        ):
            latitude_first = abs(first.position.latitude_degrees)
            latitude_second = abs(second.position.latitude_degrees)
            yuddha.append(
                GrahaYuddhaFact(
                    first=first.position.planet,
                    second=second.position.planet,
                    longitude_separation_degrees=separation,
                    winner=first.position.planet
                    if latitude_first < latitude_second
                    else second.position.planet
                    if latitude_second < latitude_first
                    else None,
                    convention_id=YUDDHA_METHOD,
                )
            )
    chains: list[DispositorChain] = []
    for name, _planet in planets.items():
        chain: list[str] = [name]
        seen: dict[str, int] = {name: 0}
        current = name
        while current in planets:
            next_lord = planets[current].sign.lord
            chain.append(next_lord)
            if next_lord in seen:
                cycle_start = seen[next_lord]
                break
            seen[next_lord] = len(chain) - 1
            current = next_lord
        else:
            cycle_start = None
        chains.append(
            DispositorChain(source=name, chain=tuple(chain), cycle_start_index=cycle_start)
        )
    occupied: dict[int, list[str]] = {house: [] for house in range(1, 13)}
    for planet in chart.planets:
        occupied[planet.house].append(planet.position.planet)
    occupied[1].append("lagna")
    papakartari: list[PapakartariFact] = []
    for target, house in [(planet.position.planet, planet.house) for planet in chart.planets] + [
        ("lagna", 1)
    ]:
        previous = ((house - 2) % 12) + 1
        following = (house % 12) + 1
        previous_malefics = tuple(name for name in occupied[previous] if name in NATURAL_MALEFICS)
        following_malefics = tuple(name for name in occupied[following] if name in NATURAL_MALEFICS)
        if previous_malefics and following_malefics:
            papakartari.append(
                PapakartariFact(
                    target=target,
                    target_house=house,
                    preceding_house=previous,
                    following_house=following,
                    preceding_malefics=previous_malefics,
                    following_malefics=following_malefics,
                    condition="natural_malefics_in_2nd_and_12th_houses",
                )
            )
    return RelationshipResult(
        provenance=chart.provenance,
        graha_drishti_method_id=GRAHA_METHOD,
        jaimini_rashi_drishti_method_id=JAIMINI_METHOD,
        conjunction_orb_degrees=conjunction_orb_degrees,
        graha_drishti=_graha_drishti(chart),
        jaimini_rashi_drishti=_jaimini(chart),
        conjunctions=conjunctions,
        parivartana=exchanges,
        dispositorship_chains=chains,
        graha_yuddha=yuddha,
        papakartari=papakartari,
        warnings=[
            "nodes_use_seventh_graha_drishti_only",
            "graha_yuddha_winner_uses_absolute_latitude_tiebreak",
        ],
        explain_calculation={
            "graha_drishti": (
                "all planets aspect the seventh sign; Mars 4th/8th, Jupiter 5th/9th, "
                "Saturn 3rd/10th"
            ),
            "jaimini": (
                "movable-to-fixed, fixed-to-movable excluding adjacent signs; dual "
                "signs aspect other dual signs"
            ),
            "dispositor": (
                "follow the lord of each occupied sign until a cycle or missing planet is reached"
            ),
            "papakartari": (
                "target is flanked by natural malefics in the immediately preceding "
                "and following houses"
            ),
        },
    )
