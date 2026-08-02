from __future__ import annotations

from simplyjyotish_engine.models.advanced import AshtakavargaResult
from simplyjyotish_engine.models.chart import BirthChart

CONTRIBUTORS = ("sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn", "lagna")
TARGETS = CONTRIBUTORS
BENEFIC_TO_HOUSES = (
    (
        (1, 2, 4, 7, 8, 9, 10, 11),
        (3, 6, 10, 11),
        (1, 2, 4, 7, 8, 9, 10, 11),
        (3, 5, 6, 9, 10, 11, 12),
        (5, 6, 9, 11),
        (6, 7, 12),
        (1, 2, 4, 7, 8, 9, 10, 11),
        (3, 4, 6, 10, 11, 12),
    ),
    (
        (3, 6, 7, 8, 10, 11),
        (1, 3, 6, 7, 9, 10, 11),
        (2, 3, 5, 6, 10, 11),
        (1, 3, 4, 5, 7, 8, 10, 11),
        (1, 2, 4, 7, 8, 10, 11),
        (3, 4, 5, 7, 9, 10, 11),
        (3, 5, 6, 11),
        (3, 6, 10, 11),
    ),
    (
        (3, 5, 6, 10, 11),
        (3, 6, 11),
        (1, 2, 4, 7, 8, 10, 11),
        (3, 5, 6, 11),
        (6, 10, 11, 12),
        (6, 8, 11, 12),
        (1, 4, 7, 8, 9, 10, 11),
        (1, 3, 6, 10, 11),
    ),
    (
        (5, 6, 9, 11, 12),
        (2, 4, 6, 8, 10, 11),
        (1, 2, 4, 7, 8, 9, 10, 11),
        (1, 3, 5, 6, 9, 10, 11, 12),
        (6, 8, 11, 12),
        (1, 2, 3, 4, 5, 8, 9, 11),
        (1, 2, 4, 7, 8, 9, 10, 11),
        (1, 2, 4, 6, 8, 10, 11),
    ),
    (
        (1, 2, 3, 4, 7, 8, 9, 10, 11),
        (2, 5, 7, 9, 11),
        (1, 2, 4, 7, 8, 10, 11),
        (1, 2, 4, 5, 6, 9, 10, 11),
        (1, 2, 3, 4, 7, 8, 10, 11),
        (2, 5, 6, 9, 10, 11),
        (3, 5, 6, 12),
        (1, 2, 4, 5, 6, 7, 9, 10, 11),
    ),
    (
        (8, 11, 12),
        (1, 2, 3, 4, 5, 8, 9, 11, 12),
        (3, 4, 6, 9, 11, 12),
        (3, 5, 6, 9, 11),
        (5, 8, 9, 10, 11),
        (1, 2, 3, 4, 5, 8, 9, 10, 11),
        (3, 4, 5, 8, 9, 10, 11),
        (1, 2, 3, 4, 5, 8, 9, 11),
    ),
    (
        (1, 2, 4, 7, 8, 10, 11),
        (3, 6, 11),
        (3, 5, 6, 10, 11, 12),
        (6, 8, 9, 10, 11, 12),
        (5, 6, 11, 12),
        (6, 11, 12),
        (3, 5, 6, 11),
        (1, 3, 4, 6, 10, 11),
    ),
    (
        (3, 4, 6, 10, 11, 12),
        (3, 6, 10, 11, 12),
        (1, 3, 6, 10, 11),
        (1, 2, 4, 6, 8, 10, 11),
        (1, 2, 4, 5, 6, 7, 9, 10, 11),
        (1, 2, 3, 4, 5, 8, 9),
        (1, 3, 4, 6, 10, 11),
        (3, 6, 10, 11),
    ),
)
OWN_SIGNS = ((4,), (3,), (0, 7), (2, 5), (8, 11), (1, 6), (9, 10))
RASI_MULTIPLIERS = (7, 10, 8, 4, 10, 6, 7, 8, 9, 5, 11, 12)
GRAHA_MULTIPLIERS = (5, 5, 8, 5, 10, 7, 5)


def _signs(chart: BirthChart) -> tuple[int, ...]:
    by_name = {planet.position.planet: planet.sign.index for planet in chart.planets}
    return tuple((*[by_name[name] for name in CONTRIBUTORS[:-1]], chart.ascendant.sign.index))


def _trikona(rows: list[list[int]]) -> list[list[int]]:
    output = [row[:] for row in rows]
    for row in output[:7]:
        for remainder in range(4):
            indexes = (remainder, remainder + 4, remainder + 8)
            values = [row[index] for index in indexes]
            if 0 in values:
                continue
            minimum = min(values)
            for index in indexes:
                row[index] = 0 if values.count(minimum) == 3 else row[index] - minimum
    return output


def _ekadhipatya(rows: list[list[int]], signs: tuple[int, ...]) -> list[list[int]]:
    output = [row[:] for row in rows]
    occupied = {sign: index for index, sign in enumerate(signs[:7])}
    for row_index, (first, second) in enumerate(OWN_SIGNS[2:], start=2):
        if output[row_index][first] == 0 or output[row_index][second] == 0:
            continue
        if first in occupied and second in occupied:
            continue
        if first not in occupied and second not in occupied:
            if output[row_index][first] == output[row_index][second]:
                output[row_index][first] = output[row_index][second] = 0
            else:
                minimum = min(output[row_index][first], output[row_index][second])
                output[row_index][first] = output[row_index][second] = minimum
            continue
        occupied_sign = first if first in occupied else second
        empty_sign = second if occupied_sign == first else first
        output[row_index][empty_sign] = min(
            output[row_index][empty_sign], output[row_index][occupied_sign]
        )
    return output


def calculate_ashtakavarga(chart: BirthChart) -> AshtakavargaResult:
    signs = _signs(chart)
    bav = [[0 for _ in range(12)] for _ in TARGETS]
    pav = [[[0 for _ in range(12)] for _ in CONTRIBUTORS] for _ in TARGETS]
    for target_index, contributor_houses in enumerate(BENEFIC_TO_HOUSES):
        for contributor_index, houses in enumerate(contributor_houses):
            for house in houses:
                sign = (signs[contributor_index] + house - 1) % 12
                bav[target_index][sign] += 1
                pav[target_index][contributor_index][sign] = 1
    sav = tuple(sum(bav[target][sign] for target in range(7)) for sign in range(12))
    trikona_rows = _trikona(bav)
    ekadhipatya_rows = _ekadhipatya(trikona_rows, signs)
    pindas: dict[str, tuple[int, int, int]] = {}
    for index, planet in enumerate(TARGETS[:7]):
        rasi = sum(
            value * multiplier
            for value, multiplier in zip(ekadhipatya_rows[index], RASI_MULTIPLIERS, strict=True)
        )
        graha = sum(
            GRAHA_MULTIPLIERS[other] * ekadhipatya_rows[index][signs[other]] for other in range(7)
        )
        pindas[planet] = (rasi, graha, rasi + graha)
    return AshtakavargaResult(
        provenance=chart.provenance,
        method_id="ashtakavarga_parashari_pinned_oracle_v1",
        contributor_order=CONTRIBUTORS,
        bhinna_ashtakavarga={planet: tuple(row) for planet, row in zip(TARGETS, bav, strict=True)},
        prastara_ashtakavarga={
            planet: tuple(tuple(values) for values in rows)
            for planet, rows in zip(TARGETS, pav, strict=True)
        },
        sarvashtakavarga=sav,
        trikona_shodhana={
            planet: tuple(row) for planet, row in zip(TARGETS, trikona_rows, strict=True)
        },
        ekadhipatya_shodhana={
            planet: tuple(row) for planet, row in zip(TARGETS, ekadhipatya_rows, strict=True)
        },
        shodhya_pinda=pindas,
        warnings=[
            "ashtakavarga convention cross-checked against pinned PyJHora source; "
            "expert review pending"
        ],
        explain_calculation={
            "bhinna": (
                "seven planetary target rows plus Lagna contributor row using fixed "
                "benefic-house tables"
            ),
            "prastara": "one binary contributor matrix for each target and contributor",
            "trikona_shodhana": (
                "reduce groups of signs at offsets 1, 5, and 9 from each trinal base"
            ),
            "ekadhipatya_shodhana": (
                "apply paired-lord reductions to Mars, Mercury, Jupiter, Venus, and Saturn rows"
            ),
            "shodhya_pinda": (
                "rasi bindus weighted by sign multipliers plus graha bindus weighted by "
                "planetary multipliers"
            ),
        },
    )
