from datetime import date
from pathlib import Path

from simplyjyotish_engine.models.inputs import BirthDetails, LocationDate, TransitRequest
from simplyjyotish_engine.panchanga.daily import calculate_panchanga
from simplyjyotish_engine.transits.timeline import calculate_sade_sati, calculate_transit_timeline
from simplyjyotish_engine.vedic.chart import calculate_birth_chart


def test_panchanga_returns_boundaries_and_daily_windows() -> None:
    location = LocationDate(
        date=date(2024, 1, 1), timezone_name="Asia/Kolkata", latitude=17.385, longitude=78.4867
    )
    result = calculate_panchanga(location)
    assert result.local_date == date(2024, 1, 1)
    for element in (result.tithi, result.nakshatra, result.yoga, result.karana):
        assert element.start.instant_utc < element.end.instant_utc
        assert 0 <= element.fraction_complete_at_local_midnight < 1
    assert result.windows.sunrise.instant_utc < result.windows.sunset.instant_utc
    assert len(result.windows.hora) == 24
    assert len(result.windows.choghadiya) == 8


def test_transit_timeline_and_sade_sati_are_structured_and_deterministic() -> None:
    request = TransitRequest(
        start_date=date(2024, 1, 1),
        end_date=date(2024, 1, 3),
        timezone_name="Asia/Kolkata",
        latitude=17.385,
        longitude=78.4867,
        planets=("sun", "saturn"),
    )
    result = calculate_transit_timeline(request)
    assert len(result.snapshots) == 4
    assert all(point.planet in {"sun", "saturn"} for point in result.snapshots[0].points)
    birth = BirthDetails.model_validate_json(Path("tests/fixtures/sample_birth.json").read_text())
    chart = calculate_birth_chart(birth)
    sade = calculate_sade_sati(
        chart,
        LocationDate(
            date=date(2024, 1, 1), timezone_name="Asia/Kolkata", latitude=17.385, longitude=78.4867
        ),
        date(2024, 1, 3),
    )
    assert len(sade.conditions) == 4
    assert all(condition.relative_sign_offset in range(12) for condition in sade.conditions)
