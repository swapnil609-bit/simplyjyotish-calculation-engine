from datetime import date, datetime

import pytest

from simplyjyotish_engine.models.inputs import BirthDetails


def test_birth_details_preserves_input() -> None:
    birth = BirthDetails(
        date_of_birth=date(1990, 1, 1),
        local_time_of_birth=datetime(1990, 1, 1, 12, 30, 15),
        timezone_name="Asia/Kolkata",
        latitude=17.385,
        longitude=78.4867,
    )
    assert birth.local_time_of_birth.second == 15
    assert birth.model_dump()["timezone_name"] == "Asia/Kolkata"


def test_aware_local_time_is_rejected() -> None:
    with pytest.raises(ValueError):
        BirthDetails(
            date_of_birth=date(1990, 1, 1),
            local_time_of_birth=datetime.fromisoformat("1990-01-01T12:30:00+05:30"),
            timezone_name="Asia/Kolkata",
            latitude=0,
            longitude=0,
        )
