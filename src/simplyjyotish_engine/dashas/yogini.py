from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

from simplyjyotish_engine.dashas._nested import YEAR_DAYS, duration_days, expand_children
from simplyjyotish_engine.models.chart import BirthChart
from simplyjyotish_engine.models.dasha import DashaDepth, DashaPeriod, DashaTimeline

YOGINI_SEQUENCE = ("moon", "sun", "jupiter", "mars", "mercury", "saturn", "venus", "rahu")
YOGINI_YEARS = dict(
    zip(
        YOGINI_SEQUENCE,
        map(Decimal, ("1", "2", "3", "4", "5", "6", "7", "8")),
        strict=True,
    )
)
YOGINI_TOTAL_YEARS = Decimal("36")


def calculate_yogini_dasha(
    chart: BirthChart, max_depth: DashaDepth = DashaDepth.ANTARDASHA, cycle_count: int = 3
) -> DashaTimeline:
    if cycle_count < 1:
        raise ValueError("cycle_count must be at least one")
    moon = next(planet for planet in chart.planets if planet.position.planet == "moon")
    star_number = moon.nakshatra.index + 1
    first_index = (star_number - 6) % 8
    first_lord = YOGINI_SEQUENCE[first_index]
    elapsed = Decimal(str((moon.position.longitude.decimal_degrees % (360 / 27)) / (360 / 27)))
    first_balance = YOGINI_YEARS[first_lord] * (Decimal("1") - elapsed)
    cursor = chart.provenance.resolved_utc
    periods: list[DashaPeriod] = []
    for offset in range(cycle_count * len(YOGINI_SEQUENCE)):
        lord = YOGINI_SEQUENCE[(first_index + offset) % len(YOGINI_SEQUENCE)]
        years = first_balance if offset == 0 else YOGINI_YEARS[lord]
        end = cursor + timedelta(days=float(years * YEAR_DAYS))
        parent = DashaPeriod(
            level=DashaDepth.MAHADASHA.value,
            lord=lord,
            start=cursor,
            end=end,
            duration_days=duration_days(cursor, end),
            lord_chain=(lord,),
        )
        periods.append(parent)
        periods.extend(
            expand_children(
                parent, YOGINI_SEQUENCE, {lord: Decimal("1") for lord in YOGINI_SEQUENCE}, max_depth
            )
        )
        cursor = end
    return DashaTimeline(
        system="yogini",
        convention=(
            "PyJHora-compatible 8-lord sequence; 36-year cycle; proportional "
            "birth balance; 365.25-day year"
        ),
        provenance=chart.provenance,
        periods=periods,
        warnings=["yogini_traditions_vary_in_seed_and_subperiod_direction"],
        validation_status="implemented_requires_expert_review",
    )
