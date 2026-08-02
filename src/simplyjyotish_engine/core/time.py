from __future__ import annotations

from datetime import UTC, datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from simplyjyotish_engine.core.errors import CalculationError

JULIAN_DAY_UNIX_EPOCH = 2440587.5


def resolve_timezone(name: str) -> ZoneInfo:
    try:
        return ZoneInfo(name)
    except ZoneInfoNotFoundError as exc:
        raise CalculationError(f"Unknown IANA timezone: {name}") from exc


def to_utc(local_datetime: datetime, timezone_name: str) -> datetime:
    if local_datetime.tzinfo is not None:
        raise CalculationError("Birth local_datetime must be timezone-naive")
    return local_datetime.replace(tzinfo=resolve_timezone(timezone_name)).astimezone(UTC)


def julian_day(instant_utc: datetime) -> float:
    if instant_utc.tzinfo is None:
        raise CalculationError("Julian Day input must be timezone-aware")
    value = instant_utc.astimezone(UTC)
    return JULIAN_DAY_UNIX_EPOCH + value.timestamp() / 86400.0
