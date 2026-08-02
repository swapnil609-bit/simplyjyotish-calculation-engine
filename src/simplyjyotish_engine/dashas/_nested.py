from __future__ import annotations

from datetime import datetime, timedelta
from decimal import ROUND_HALF_EVEN, Decimal

from simplyjyotish_engine.models.dasha import DashaDepth, DashaPeriod

YEAR_DAYS = Decimal("365.25")
MICROSECONDS_PER_DAY = Decimal("86400000000")
LEVELS = tuple(DashaDepth)


def duration_days(start: datetime, end: datetime) -> float:
    delta = end - start
    micros = (
        Decimal(delta.days) * MICROSECONDS_PER_DAY
        + Decimal(delta.seconds) * Decimal("1000000")
        + Decimal(delta.microseconds)
    )
    return float(micros / MICROSECONDS_PER_DAY)


def offset_end(start: datetime, total: timedelta, fraction: Decimal) -> datetime:
    micros = (
        Decimal(total.days) * MICROSECONDS_PER_DAY
        + Decimal(total.seconds) * Decimal("1000000")
        + Decimal(total.microseconds)
    ) * fraction
    return start + timedelta(microseconds=int(micros.to_integral_value(ROUND_HALF_EVEN)))


def expand_children(
    parent: DashaPeriod,
    sequence: tuple[str, ...],
    weights: dict[str, Decimal],
    max_depth: DashaDepth,
) -> list[DashaPeriod]:
    parent_level = DashaDepth(parent.level)
    next_index = LEVELS.index(parent_level) + 1
    if next_index > LEVELS.index(max_depth):
        return []
    total_weight = sum(weights.values(), Decimal("0"))
    start_index = sequence.index(parent.lord)
    children: list[DashaPeriod] = []
    cursor = parent.start
    elapsed = Decimal("0")
    for offset in range(len(sequence)):
        lord = sequence[(start_index + offset) % len(sequence)]
        fraction = weights[lord] / total_weight
        elapsed += fraction
        end = (
            parent.end
            if offset == len(sequence) - 1
            else offset_end(parent.start, parent.end - parent.start, elapsed)
        )
        child = DashaPeriod(
            level=LEVELS[next_index].value,
            lord=lord,
            start=cursor,
            end=end,
            duration_days=duration_days(cursor, end),
            parent_lord=parent.lord,
            lord_chain=(*parent.lord_chain, lord),
        )
        children.append(child)
        cursor = end
    result: list[DashaPeriod] = []
    for child in children:
        result.append(child)
        result.extend(expand_children(child, sequence, weights, max_depth))
    return result
