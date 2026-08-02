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
    assert result.windows is not None
    assert len(result.windows.choghadiya_day) == 8
    assert len(result.windows.choghadiya_night) == 8
    assert len(result.windows.choghadiya) == 16
    assert (
        result.windows.choghadiya_day[-1].end.instant_utc
        == result.windows.choghadiya_night[0].start.instant_utc
    )


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


def test_panchanga_handles_polar_sunrise_unavailability_and_midnight_crossing() -> None:
    polar = calculate_panchanga(
        LocationDate(date=date(2024, 1, 1), timezone_name="UTC", latitude=69.0, longitude=0.0)
    )
    assert polar.windows is None
    assert "sunrise_or_sunset_unavailable_returns_windows_null" in polar.warnings
    location = LocationDate(
        date=date(2024, 1, 1), timezone_name="Asia/Kolkata", latitude=17.385, longitude=78.4867
    )
    result = calculate_panchanga(location)
    assert result.windows is not None
    assert result.windows.choghadiya_night[0].start.local_time.date() == location.date
    assert result.windows.choghadiya_night[-1].end.local_time.date() == date(2024, 1, 2)


def test_transit_refines_endpoint_and_timezone_crossing_events() -> None:
    utc_request = TransitRequest(
        start_date=date(2024, 1, 14),
        end_date=date(2024, 1, 15),
        timezone_name="UTC",
        latitude=0,
        longitude=0,
        planets=("sun",),
        coarse_step_hours=168,
        event_tolerance_seconds=0.5,
    )
    local_request = utc_request.model_copy(update={"timezone_name": "Asia/Kolkata"})
    utc_events = calculate_transit_timeline(utc_request).events
    local_events = calculate_transit_timeline(local_request).events
    assert utc_events and local_events
    assert utc_events[0].local_time.date() != local_events[0].local_time.date()
    assert utc_events[0].achieved_precision_seconds <= 0.5
    assert utc_events[0].search_window_start_utc <= utc_events[0].instant_utc
    assert utc_events[0].instant_utc <= utc_events[0].search_window_end_utc


def test_transit_detects_a_retrograde_loop_with_coarse_brackets() -> None:
    request = TransitRequest(
        start_date=date(2024, 4, 1),
        end_date=date(2024, 4, 26),
        timezone_name="UTC",
        latitude=0,
        longitude=0,
        planets=("mercury",),
        coarse_step_hours=168,
        event_tolerance_seconds=2.0,
    )
    events = calculate_transit_timeline(request).events
    assert [event.event for event in events if event.event.startswith("station_")] == [
        "station_retrograde",
        "station_direct",
    ]
