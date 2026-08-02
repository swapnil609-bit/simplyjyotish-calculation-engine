from __future__ import annotations

from datetime import datetime, timedelta
from decimal import ROUND_HALF_EVEN, Decimal

from simplyjyotish_engine.models.chart import BirthChart
from simplyjyotish_engine.models.dasha import DashaDepth, DashaPeriod, DashaTimeline
from simplyjyotish_engine.vedic.reference import NAKSHATRA_SIZE, NAKSHATRAS

VIMSHOTTARI_YEARS = {
    "ketu": Decimal("7"),
    "venus": Decimal("20"),
    "sun": Decimal("6"),
    "moon": Decimal("10"),
    "mars": Decimal("7"),
    "rahu": Decimal("18"),
    "jupiter": Decimal("16"),
    "saturn": Decimal("19"),
    "mercury": Decimal("17"),
}
VIMSHOTTARI_SEQUENCE = tuple(VIMSHOTTARI_YEARS)
VIMSHOTTARI_TOTAL_YEARS = Decimal("120")
YEAR_LENGTH_DAYS = Decimal("365.25")
LEVELS = tuple(DashaDepth)
MICROSECONDS_PER_DAY = Decimal("86400000000")


def _period_days(years: Decimal) -> Decimal:
    return years * YEAR_LENGTH_DAYS


def _timedelta_microseconds(value: timedelta) -> Decimal:
    return (
        Decimal(value.days) * MICROSECONDS_PER_DAY
        + Decimal(value.seconds) * Decimal("1000000")
        + Decimal(value.microseconds)
    )


def _duration_days(start: datetime, end: datetime) -> float:
    return float(_timedelta_microseconds(end - start) / MICROSECONDS_PER_DAY)


def _offset_end(start: datetime, total: timedelta, fraction: Decimal) -> datetime:
    microseconds = (_timedelta_microseconds(total) * fraction).to_integral_value(ROUND_HALF_EVEN)
    return start + timedelta(microseconds=int(microseconds))


def _child_periods(parent: DashaPeriod, child_level: DashaDepth) -> list[DashaPeriod]:
    start_index = VIMSHOTTARI_SEQUENCE.index(parent.lord)
    total_duration = parent.end - parent.start
    periods: list[DashaPeriod] = []
    cursor = parent.start
    elapsed_fraction = Decimal("0")
    for offset in range(9):
        lord = VIMSHOTTARI_SEQUENCE[(start_index + offset) % 9]
        if offset == 8:
            end = parent.end
        else:
            fraction = VIMSHOTTARI_YEARS[lord] / VIMSHOTTARI_TOTAL_YEARS
            elapsed_fraction += fraction
            end = _offset_end(parent.start, total_duration, elapsed_fraction)
        periods.append(
            DashaPeriod(
                level=child_level.value,
                lord=lord,
                start=cursor,
                end=end,
                duration_days=_duration_days(cursor, end),
                parent_lord=parent.lord,
                lord_chain=(*parent.lord_chain, lord),
            )
        )
        cursor = end
    return periods


def _expand_period(parent: DashaPeriod, max_depth: DashaDepth) -> list[DashaPeriod]:
    parent_level = DashaDepth(parent.level)
    next_index = LEVELS.index(parent_level) + 1
    if next_index > LEVELS.index(max_depth):
        return []
    children = _child_periods(parent, LEVELS[next_index])
    result: list[DashaPeriod] = []
    for child in children:
        result.append(child)
        result.extend(_expand_period(child, max_depth))
    return result


def calculate_vimshottari_dasha(
    chart: BirthChart,
    max_depth: DashaDepth = DashaDepth.ANTARDASHA,
    mahadasha_count: int = 18,
) -> DashaTimeline:
    """Return a deterministic future Vimshottari timeline from the birth instant.

    The first Mahadasha is the remaining proportional balance of the Moon's
    nakshatra lord. Every final child closes exactly on its parent endpoint to
    prevent rounding gaps at Antardasha through Prana boundaries.
    """
    if mahadasha_count < 1:
        raise ValueError("mahadasha_count must be at least one")
    moon = next(planet for planet in chart.planets if planet.position.planet == "moon")
    nakshatra_index = moon.nakshatra.index
    nakshatra_start = Decimal(nakshatra_index) * Decimal(str(NAKSHATRA_SIZE))
    moon_longitude = Decimal(str(moon.position.longitude.decimal_degrees))
    elapsed_fraction = (moon_longitude - nakshatra_start) / Decimal(str(NAKSHATRA_SIZE))
    first_lord = NAKSHATRAS[nakshatra_index][1]
    first_balance_years = VIMSHOTTARI_YEARS[first_lord] * (Decimal("1") - elapsed_fraction)
    cursor = chart.provenance.resolved_utc
    periods: list[DashaPeriod] = []
    lord_index = VIMSHOTTARI_SEQUENCE.index(first_lord)
    for offset in range(mahadasha_count):
        lord = VIMSHOTTARI_SEQUENCE[(lord_index + offset) % 9]
        years = first_balance_years if offset == 0 else VIMSHOTTARI_YEARS[lord]
        end = cursor + timedelta(days=float(_period_days(years)))
        mahadasha = DashaPeriod(
            level=DashaDepth.MAHADASHA.value,
            lord=lord,
            start=cursor,
            end=end,
            duration_days=_duration_days(cursor, end),
            lord_chain=(lord,),
        )
        periods.append(mahadasha)
        periods.extend(_expand_period(mahadasha, max_depth))
        cursor = end
    return DashaTimeline(
        system="vimshottari",
        convention=(
            "Moon nakshatra lord; 365.25-day dasha year; proportional balance "
            "at birth; nested periods close exactly on parent endpoints"
        ),
        provenance=chart.provenance,
        periods=periods,
        warnings=(["prana_timeline_can_be_large"] if max_depth == DashaDepth.PRANA else []),
    )
