from datetime import UTC, datetime

import pytest

from simplyjyotish_engine.core.errors import CalculationError
from simplyjyotish_engine.core.time import julian_day, to_utc


def test_utc_conversion_for_india() -> None:
    result = to_utc(datetime(2020, 1, 1, 5, 30), "Asia/Kolkata")
    assert result == datetime(2020, 1, 1, tzinfo=UTC)


def test_dst_conversion() -> None:
    result = to_utc(datetime(2024, 7, 1, 12), "America/New_York")
    assert result.hour == 16


def test_julian_day_epoch() -> None:
    assert julian_day(datetime(1970, 1, 1, tzinfo=UTC)) == 2440587.5


def test_unknown_timezone_is_rejected() -> None:
    with pytest.raises(CalculationError):
        to_utc(datetime(2020, 1, 1), "Mars/Olympus")
