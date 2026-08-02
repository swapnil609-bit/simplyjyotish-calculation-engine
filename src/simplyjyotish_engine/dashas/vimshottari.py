from __future__ import annotations

from datetime import datetime, timedelta

from simplyjyotish_engine.models.chart import BirthChart
from simplyjyotish_engine.models.dasha import DashaPeriod, DashaTimeline
from simplyjyotish_engine.vedic.reference import NAKSHATRA_SIZE, NAKSHATRAS

VIMSHOTTARI_YEARS = {
    "ketu": 7.0,
    "venus": 20.0,
    "sun": 6.0,
    "moon": 10.0,
    "mars": 7.0,
    "rahu": 18.0,
    "jupiter": 16.0,
    "saturn": 19.0,
    "mercury": 17.0,
}
VIMSHOTTARI_SEQUENCE = tuple(VIMSHOTTARI_YEARS)
VIMSHOTTARI_TOTAL_YEARS = 120.0
YEAR_LENGTH_DAYS = 365.25


def _period_days(years: float) -> float:
    return years * YEAR_LENGTH_DAYS


def _nested_periods(lord: str, start: datetime, duration_days: float) -> list[DashaPeriod]:
    start_index = VIMSHOTTARI_SEQUENCE.index(lord)
    periods: list[DashaPeriod] = []
    cursor = start
    for offset in range(9):
        sub_lord = VIMSHOTTARI_SEQUENCE[(start_index + offset) % 9]
        sub_days = duration_days * VIMSHOTTARI_YEARS[sub_lord] / VIMSHOTTARI_TOTAL_YEARS
        end = cursor + timedelta(days=sub_days)
        periods.append(
            DashaPeriod(
                level="antardasha",
                lord=sub_lord,
                start=cursor,
                end=end,
                duration_days=sub_days,
                parent_lord=lord,
            )
        )
        cursor = end
    return periods


def calculate_vimshottari_dasha(chart: BirthChart) -> DashaTimeline:
    moon = next(planet for planet in chart.planets if planet.position.planet == "moon")
    nakshatra_index = moon.nakshatra.index
    nakshatra_start = nakshatra_index * NAKSHATRA_SIZE
    elapsed_fraction = (moon.position.longitude.decimal_degrees - nakshatra_start) / NAKSHATRA_SIZE
    first_lord = NAKSHATRAS[nakshatra_index][1]
    first_balance_years = VIMSHOTTARI_YEARS[first_lord] * (1.0 - elapsed_fraction)
    cursor = chart.provenance.resolved_utc
    periods: list[DashaPeriod] = []
    lord_index = VIMSHOTTARI_SEQUENCE.index(first_lord)
    for offset in range(18):
        lord = VIMSHOTTARI_SEQUENCE[(lord_index + offset) % 9]
        years = first_balance_years if offset == 0 else VIMSHOTTARI_YEARS[lord]
        duration_days = _period_days(years)
        end = cursor + timedelta(days=duration_days)
        periods.append(
            DashaPeriod(
                level="mahadasha", lord=lord, start=cursor, end=end, duration_days=duration_days
            )
        )
        periods.extend(_nested_periods(lord, cursor, duration_days))
        cursor = end
    return DashaTimeline(
        system="vimshottari",
        convention=(
            "Moon nakshatra lord; 365.25-day dasha year; first period begins "
            "at birth with proportional balance"
        ),
        provenance=chart.provenance,
        periods=periods,
    )
