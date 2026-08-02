from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, date, datetime, time, timedelta
from itertools import pairwise

from simplyjyotish_engine.astronomy.positions import calculate_planetary_positions
from simplyjyotish_engine.core.time import resolve_timezone
from simplyjyotish_engine.models.chart import BirthChart
from simplyjyotish_engine.models.events import (
    SadeSatiCondition,
    SadeSatiTimeline,
    TransitEvent,
    TransitPoint,
    TransitSnapshot,
    TransitTimeline,
)
from simplyjyotish_engine.models.inputs import BirthDetails, LocationDate, TransitRequest
from simplyjyotish_engine.vedic.reference import sign_index


def _birth_at(request: TransitRequest, local: datetime) -> BirthDetails:
    return BirthDetails(
        date_of_birth=local.date(),
        local_time_of_birth=local.replace(tzinfo=None),
        timezone_name=request.timezone_name,
        latitude=request.latitude,
        longitude=request.longitude,
        settings=request.settings,
    )


def _sample(request: TransitRequest, local: datetime) -> tuple[datetime, dict[str, TransitPoint]]:
    result = calculate_planetary_positions(_birth_at(request, local))
    points = {
        position.planet: TransitPoint(
            planet=position.planet,
            longitude_degrees=position.longitude.decimal_degrees,
            sign_index=sign_index(position.longitude.decimal_degrees),
            retrograde=position.retrograde,
            speed_longitude_degrees_per_day=position.speed_longitude_degrees_per_day,
        )
        for position in result.positions
        if position.planet in request.planets
    }
    return result.provenance.resolved_utc, points


def _event_time(request: TransitRequest, local: datetime) -> tuple[datetime, datetime]:
    utc = local.replace(tzinfo=resolve_timezone(request.timezone_name)).astimezone(UTC)
    return utc, utc.astimezone(resolve_timezone(request.timezone_name))


def _refine_root(
    left: datetime,
    right: datetime,
    function: Callable[[datetime], float],
    tolerance_seconds: float,
) -> tuple[datetime, float]:
    left_value = function(left)
    right_value = function(right)
    if abs(left_value) <= 1e-12:
        return left, tolerance_seconds
    if abs(right_value) <= 1e-12:
        return right, tolerance_seconds
    if left_value * right_value > 0:
        raise ValueError("root refinement requires a bracket with opposite signs")
    while (right - left).total_seconds() > tolerance_seconds:
        middle = left + (right - left) / 2
        middle_value = function(middle)
        if left_value * middle_value <= 0:
            right, right_value = middle, middle_value
        else:
            left, left_value = middle, middle_value
    return left + (right - left) / 2, (right - left).total_seconds()


def calculate_transit_timeline(
    request: TransitRequest, sample_hours: int | None = None
) -> TransitTimeline:
    coarse_hours = request.coarse_step_hours if sample_hours is None else sample_hours
    if coarse_hours < 1 or coarse_hours > 168:
        raise ValueError("sample_hours must be between 1 and 168")
    zone = resolve_timezone(request.timezone_name)
    start = datetime.combine(request.start_date, time(0), tzinfo=zone)
    end = datetime.combine(request.end_date + timedelta(days=1), time(0), tzinfo=zone)
    snapshots: list[TransitSnapshot] = []
    samples: list[tuple[datetime, dict[str, TransitPoint]]] = []
    cursor = start
    while cursor <= end:
        utc, points = _sample(request, cursor)
        samples.append((cursor, points))
        snapshots.append(
            TransitSnapshot(instant_utc=utc, local_time=cursor, points=list(points.values()))
        )
        if cursor == end:
            break
        cursor = min(cursor + timedelta(hours=coarse_hours), end)
    events: list[TransitEvent] = []
    for previous, current in pairwise(samples):
        left_local, left_points = previous
        right_local, right_points = current
        for planet in request.planets:
            if planet not in left_points or planet not in right_points:
                continue
            left_point, right_point = left_points[planet], right_points[planet]
            if left_point.sign_index != right_point.sign_index:
                direct = (
                    (right_point.longitude_degrees - left_point.longitude_degrees) % 360
                ) < 180
                if direct:
                    target = (left_point.sign_index + 1) * 30.0
                    target_distance = (target - left_point.longitude_degrees) % 360

                    def ingress_function(
                        moment: datetime,
                        planet_name: str = planet,
                        reference: float = left_point.longitude_degrees,
                        distance: float = target_distance,
                    ) -> float:
                        longitude = _sample(request, moment)[1][planet_name].longitude_degrees
                        return ((longitude - reference) % 360) - distance
                else:
                    target = left_point.sign_index * 30.0
                    target_distance = (left_point.longitude_degrees - target) % 360

                    def ingress_function(
                        moment: datetime,
                        planet_name: str = planet,
                        reference: float = left_point.longitude_degrees,
                        distance: float = target_distance,
                    ) -> float:
                        longitude = _sample(request, moment)[1][planet_name].longitude_degrees
                        return ((reference - longitude) % 360) - distance

                event_local, precision = _refine_root(
                    left_local,
                    right_local,
                    ingress_function,
                    request.event_tolerance_seconds,
                )
                utc, local = _event_time(request, event_local)
                events.append(
                    TransitEvent(
                        event="ingress",
                        planet=planet,
                        instant_utc=utc,
                        local_time=local,
                        from_sign_index=left_point.sign_index,
                        to_sign_index=right_point.sign_index,
                        direction="direct" if direct else "retrograde",
                        configured_tolerance_seconds=request.event_tolerance_seconds,
                        achieved_precision_seconds=precision,
                        refinement_method="bracketed_bisection_on_unwrapped_longitude",
                        search_window_start_utc=left_local.astimezone(UTC),
                        search_window_end_utc=right_local.astimezone(UTC),
                    )
                )
            if left_point.retrograde != right_point.retrograde:

                def station_function(moment: datetime, planet_name: str = planet) -> float:
                    return _sample(request, moment)[1][planet_name].speed_longitude_degrees_per_day

                event_local, precision = _refine_root(
                    left_local,
                    right_local,
                    station_function,
                    request.event_tolerance_seconds,
                )
                utc, local = _event_time(request, event_local)
                events.append(
                    TransitEvent(
                        event="station_retrograde"
                        if not left_point.retrograde
                        else "station_direct",
                        planet=planet,
                        instant_utc=utc,
                        local_time=local,
                        direction="retrograde" if not left_point.retrograde else "direct",
                        configured_tolerance_seconds=request.event_tolerance_seconds,
                        achieved_precision_seconds=precision,
                        refinement_method="bracketed_bisection_on_longitude_speed",
                        search_window_start_utc=left_local.astimezone(UTC),
                        search_window_end_utc=right_local.astimezone(UTC),
                    )
                )
    first_result = calculate_planetary_positions(_birth_at(request, start.replace(tzinfo=None)))
    return TransitTimeline(
        provenance=first_result.provenance,
        snapshots=snapshots,
        events=sorted(events, key=lambda item: item.instant_utc),
        warnings=[
            "coarse sampling locates a bracket; event accuracy is set by event_tolerance_seconds",
            "station and ingress boundaries are refined by numerical bisection",
        ],
        explain_calculation={
            "positions": (
                "Swiss Ephemeris calc_ut with the request zodiac, ayanamsa, and node settings"
            ),
            "ingress": "unwrapped longitude reaches a sign boundary inside a coarse bracket",
            "retrograde": "speed-longitude sign changes exposed as station events",
        },
    )


def calculate_sade_sati(
    chart: BirthChart,
    location: LocationDate,
    end_date: date,
    sample_hours: int = 24,
) -> SadeSatiTimeline:
    request = TransitRequest(
        start_date=location.date,
        end_date=end_date,
        timezone_name=location.timezone_name,
        latitude=location.latitude,
        longitude=location.longitude,
        settings=location.settings,
        planets=("saturn",),
    )
    timeline = calculate_transit_timeline(request, sample_hours=sample_hours)
    natal_moon = next(planet for planet in chart.planets if planet.position.planet == "moon")
    moon_sign = natal_moon.sign.index
    conditions: list[SadeSatiCondition] = []
    for snapshot in timeline.snapshots:
        saturn = next(point for point in snapshot.points if point.planet == "saturn")
        offset = (saturn.sign_index - moon_sign) % 12
        active = offset in {11, 0, 1}
        phase = {11: "rising", 0: "peak", 1: "setting"}.get(offset, "inactive")
        conditions.append(
            SadeSatiCondition(
                instant_utc=snapshot.instant_utc,
                local_time=snapshot.local_time,
                saturn_sign_index=saturn.sign_index,
                natal_moon_sign_index=moon_sign,
                active=active,
                phase=phase,
                relative_sign_offset=offset,
            )
        )
    return SadeSatiTimeline(
        provenance=timeline.provenance,
        conditions=conditions,
        warnings=[
            "Sade Sati is represented only as the Saturn three-sign transit "
            "condition; no interpretation is included"
        ],
        explain_calculation={
            "condition": (
                "Saturn in the sign immediately before, same as, or immediately "
                "after natal Moon sign"
            ),
            "phase_labels": "rising=12th sign offset, peak=Moon sign, setting=2nd sign offset",
        },
    )
