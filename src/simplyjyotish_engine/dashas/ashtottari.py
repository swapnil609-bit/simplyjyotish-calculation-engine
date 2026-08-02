from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

from simplyjyotish_engine.dashas._nested import YEAR_DAYS, duration_days, expand_children
from simplyjyotish_engine.models.chart import BirthChart
from simplyjyotish_engine.models.dasha import DashaDepth, DashaPeriod, DashaTimeline
from simplyjyotish_engine.models.validation import ValidationStatus

ASHTOTTARI_SEQUENCE = ("sun", "moon", "mars", "mercury", "saturn", "jupiter", "rahu", "venus")
ASHTOTTARI_YEARS = dict(
    zip(
        ASHTOTTARI_SEQUENCE,
        map(Decimal, ("6", "15", "8", "17", "10", "19", "12", "21")),
        strict=True,
    )
)
ASHTOTTARI_TOTAL_YEARS = Decimal("108")
ASHTOTTARI_SEGMENTS = (
    ("sun", 6, 9),
    ("moon", 10, 12),
    ("mars", 13, 16),
    ("mercury", 17, 19),
    ("saturn", 20, 22),
    ("jupiter", 23, 25),
    ("rahu", 26, 2),
    ("venus", 3, 5),
)


def ashtottari_eligibility(chart: BirthChart) -> tuple[bool, str]:
    """Return the explicit default applicability rule used by the oracle.

    This is a mechanical house relationship check; it is not an interpretive
    judgment. Traditional eligibility variants remain exposed as review work.
    """
    lagna_lord = chart.ascendant.sign.lord
    lagna_lord_house = next(p.house for p in chart.planets if p.position.planet == lagna_lord)
    rahu_house = next(p.house for p in chart.planets if p.position.planet == "rahu")
    relative = (rahu_house - lagna_lord_house) % 12
    applicable = relative in {3, 4, 6, 8, 9} and rahu_house != 1
    return (
        applicable,
        "rahu_relative_to_lagna_lord_in_trine_or_quadrant_excluding_lagna"
        if applicable
        else "ashtottari_default_rule_not_met",
    )


def _segment_for_longitude(longitude: float) -> tuple[str, float]:
    star = int(longitude // (360.0 / 27.0)) + 1
    within = (longitude % (360.0 / 27.0)) / (360.0 / 27.0)
    for lord, start, end in ASHTOTTARI_SEGMENTS:
        end_norm = end + (27 if end < start else 0)
        probe = star + (27 if star < start else 0)
        if start <= probe <= end_norm:
            span = end_norm - start + 1
            position = ((star - start) % 27 + within) / span
            return lord, position
    raise ValueError("Unable to determine Ashtottari segment")


def calculate_ashtottari_dasha(
    chart: BirthChart,
    max_depth: DashaDepth = DashaDepth.ANTARDASHA,
    cycle_count: int = 2,
    require_eligibility: bool = True,
) -> DashaTimeline:
    applicable, eligibility = ashtottari_eligibility(chart)
    if require_eligibility and not applicable:
        raise ValueError(
            "Ashtottari is not applicable under the configured conservative eligibility rule"
        )
    moon = next(planet for planet in chart.planets if planet.position.planet == "moon")
    first_lord, elapsed = _segment_for_longitude(moon.position.longitude.decimal_degrees)
    first_balance = ASHTOTTARI_YEARS[first_lord] * (Decimal("1") - Decimal(str(elapsed)))
    first_index = ASHTOTTARI_SEQUENCE.index(first_lord)
    cursor = chart.provenance.resolved_utc
    periods: list[DashaPeriod] = []
    for offset in range(cycle_count * len(ASHTOTTARI_SEQUENCE)):
        lord = ASHTOTTARI_SEQUENCE[(first_index + offset) % len(ASHTOTTARI_SEQUENCE)]
        years = first_balance if offset == 0 else ASHTOTTARI_YEARS[lord]
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
        periods.extend(expand_children(parent, ASHTOTTARI_SEQUENCE, ASHTOTTARI_YEARS, max_depth))
        cursor = end
    return DashaTimeline(
        system="ashtottari",
        convention=(
            "108-year 8-lord cycle; nakshatra segment balance; 365.25-day year; "
            "conservative eligibility required by default"
        ),
        provenance=chart.provenance,
        periods=periods,
        warnings=[
            eligibility,
            "ashtottari_eligibility_and_segment_conventions_require_expert_review",
        ],
        eligibility="applicable" if applicable else "not_applicable",
        validation_status="implemented_requires_expert_review",
        validation_detail=ValidationStatus(
            source_verified=True,
            cross_implementation_verified=False,
            source_reference_ids=("bphs_chapter_17_3", "pyjhora_4_8_7_ashtottari_tests"),
            notes=(
                "Eligibility and birth-balance conventions differ across references "
                "and remain versioned.",
            ),
        ),
    )
