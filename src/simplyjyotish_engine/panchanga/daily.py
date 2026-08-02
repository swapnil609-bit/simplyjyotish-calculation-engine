from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, date, datetime, time, timedelta
from math import floor
from typing import Any

from simplyjyotish_engine.astronomy.ephemeris import require_swiss_ephemeris
from simplyjyotish_engine.astronomy.positions import _flags
from simplyjyotish_engine.core.time import (
    datetime_from_julian_day,
    julian_day,
    resolve_timezone,
    to_utc,
)
from simplyjyotish_engine.models.events import (
    DailyWindows,
    EventTime,
    PanchangaElement,
    PanchangaResult,
    TimeWindow,
)
from simplyjyotish_engine.models.inputs import BirthDetails, LocationDate
from simplyjyotish_engine.vedic.reference import NAKSHATRAS

TITHIS = (
    "Pratipada",
    "Dvitiya",
    "Tritiya",
    "Chaturthi",
    "Panchami",
    "Shashthi",
    "Saptami",
    "Ashtami",
    "Navami",
    "Dashami",
    "Ekadashi",
    "Dwadashi",
    "Trayodashi",
    "Chaturdashi",
    "Purnima",
)
YOGAS = (
    "Vishkambha",
    "Priti",
    "Ayushman",
    "Saubhagya",
    "Shobhana",
    "Atiganda",
    "Sukarma",
    "Dhriti",
    "Shula",
    "Ganda",
    "Vriddhi",
    "Dhruva",
    "Vyaghata",
    "Harshana",
    "Vajra",
    "Siddhi",
    "Vyatipata",
    "Variyana",
    "Parigha",
    "Shiva",
    "Siddha",
    "Sadhya",
    "Shubha",
    "Shukla",
    "Brahma",
    "Indra",
    "Vaidhriti",
)
KARANA_MOVABLE = ("Bava", "Balava", "Kaulava", "Taitila", "Gara", "Vanija", "Vishti")
RAHU_PART = (1, 6, 4, 5, 3, 2, 7)  # Monday through Sunday, zero based
YAMAGANDA_PART = (3, 2, 1, 0, 5, 4, 4)
GULIKA_PART = (5, 4, 3, 2, 1, 0, 6)
HORA_LORDS = ("sun", "venus", "mercury", "moon", "saturn", "jupiter", "mars")
DAY_LORDS = ("moon", "mars", "mercury", "jupiter", "venus", "saturn", "sun")
CHOGHADIYA = (
    ("Amrit", "Kaal", "Shubh", "Rog", "Udveg", "Char", "Labh", "Amrit"),
    ("Rog", "Udveg", "Char", "Labh", "Amrit", "Kaal", "Shubh", "Rog"),
    ("Labh", "Amrit", "Kaal", "Shubh", "Rog", "Udveg", "Char", "Labh"),
    ("Shubh", "Rog", "Udveg", "Char", "Labh", "Amrit", "Kaal", "Shubh"),
    ("Char", "Labh", "Amrit", "Kaal", "Shubh", "Rog", "Udveg", "Char"),
    ("Kaal", "Shubh", "Rog", "Udveg", "Char", "Labh", "Amrit", "Kaal"),
    ("Udveg", "Char", "Labh", "Amrit", "Kaal", "Shubh", "Rog", "Udveg"),
)


def _birth_at_midnight(location: LocationDate) -> BirthDetails:
    return BirthDetails(
        date_of_birth=location.date,
        local_time_of_birth=datetime.combine(location.date, time()),
        timezone_name=location.timezone_name,
        latitude=location.latitude,
        longitude=location.longitude,
        settings=location.settings,
    )


def _phase(swe: Any, jd: float, location: LocationDate, kind: str) -> float:
    flags = _flags(location.settings, swe)
    sun = swe.calc_ut(jd, swe.SUN, flags)[0][0]
    moon = swe.calc_ut(jd, swe.MOON, flags)[0][0]
    if kind == "tithi":
        return float((moon - sun) % 360.0)
    if kind == "nakshatra":
        return float(moon % 360.0)
    if kind == "yoga":
        return float((moon + sun) % 360.0)
    if kind == "karana":
        return float((moon - sun) % 360.0)
    raise ValueError(f"Unknown Panchanga phase: {kind}")


def _find_boundary(
    jd_ref: float, fn: Callable[[float], float], step: float, previous: bool
) -> float:
    reference = fn(jd_ref)
    target = floor(reference / step) * step if previous else (floor(reference / step) + 1) * step
    if previous and abs(reference - target) < 1e-9:
        return jd_ref
    direction = -1.0 if previous else 1.0

    def unwrapped(jd: float) -> float:
        if previous:
            return reference - ((reference - fn(jd)) % 360.0)
        return reference + ((fn(jd) - reference) % 360.0)

    hi = jd_ref
    for _ in range(32):
        lo = hi + direction * 0.25
        lo_value = unwrapped(lo)
        if (previous and lo_value <= target) or (not previous and lo_value >= target):
            left, right = (lo, hi) if previous else (hi, lo)
            for _ in range(48):
                middle = (left + right) / 2
                value = unwrapped(middle)
                if (previous and value <= target) or (not previous and value >= target):
                    if previous:
                        left = middle
                    else:
                        right = middle
                else:
                    if previous:
                        right = middle
                    else:
                        left = middle
            return (left + right) / 2
        hi = lo
    raise ValueError("Panchanga boundary not found in search window")


def _event(name: str, jd: float, location: LocationDate) -> EventTime:
    utc = datetime_from_julian_day(jd)
    local = utc.astimezone(resolve_timezone(location.timezone_name))
    return EventTime(event=name, instant_utc=utc, local_time=local)


def _window(name: str, start: datetime, end: datetime) -> TimeWindow:
    return TimeWindow(
        event=name,
        start=EventTime(event=f"{name}_start", instant_utc=start.astimezone(UTC), local_time=start),
        end=EventTime(event=f"{name}_end", instant_utc=end.astimezone(UTC), local_time=end),
    )


def _rise_set(location: LocationDate, body: int, rise: bool, day: date) -> EventTime | None:
    swe = require_swiss_ephemeris()
    start = to_utc(datetime.combine(day, time()), location.timezone_name)
    flags = swe.FLG_SWIEPH
    mode = swe.CALC_RISE if rise else swe.CALC_SET
    result, times = swe.rise_trans(
        julian_day(start),
        body,
        mode,
        (location.longitude, location.latitude, 0.0),
        0.0,
        10.0,
        flags,
    )
    if result != 0:
        return None
    return _event(
        "sunrise"
        if body == swe.SUN and rise
        else "sunset"
        if body == swe.SUN
        else "moonrise"
        if rise
        else "moonset",
        times[0],
        location,
    )


def _panchanga_element(
    location: LocationDate, kind: str, jd_midnight: float, step: float, index: int, name: str
) -> PanchangaElement:
    swe = require_swiss_ephemeris()

    def fn(jd: float) -> float:
        return _phase(swe, jd, location, kind)

    start = _find_boundary(jd_midnight, fn, step, True)
    end = _find_boundary(jd_midnight, fn, step, False)
    fraction = (fn(jd_midnight) % 360.0 % step) / step
    return PanchangaElement(
        element=kind,
        index=index,
        name=name,
        start=_event(f"{kind}_start", start, location),
        end=_event(f"{kind}_end", end, location),
        fraction_complete_at_local_midnight=fraction,
    )


def _daily_windows(
    location: LocationDate,
    sunrise: EventTime,
    sunset: EventTime,
    moonrise: EventTime | None,
    moonset: EventTime | None,
) -> DailyWindows:
    next_sunrise = _rise_set(
        location, require_swiss_ephemeris().SUN, True, location.date + timedelta(days=1)
    )
    if next_sunrise is None:
        next_sunrise = sunrise
    day_start, day_end = sunrise.local_time, sunset.local_time
    day_part = (day_end - day_start) / 8
    weekday = location.date.weekday()

    def day_part_window(name: str, part: int) -> TimeWindow:
        start = day_start + day_part * part
        return _window(name, start, start + day_part)

    abhijit_center = day_start + (day_end - day_start) / 2
    abhijit_length = (day_end - day_start) / 15
    hora: list[TimeWindow] = []
    night_start, night_end = day_end, next_sunrise.local_time
    for i in range(24):
        if i < 12:
            start = day_start + (day_end - day_start) * i / 12
            lord = HORA_LORDS[(DAY_LORDS.index(DAY_LORDS[weekday]) + i) % 7]
            end = day_start + (day_end - day_start) * (i + 1) / 12
        else:
            j = i - 12
            start = night_start + (night_end - night_start) * j / 12
            lord = HORA_LORDS[(DAY_LORDS.index(DAY_LORDS[weekday]) + i) % 7]
            end = night_start + (night_end - night_start) * (j + 1) / 12
        hora.append(_window(f"hora_{lord}", start, end))
    chog = [
        _window(
            f"choghadiya_{name.lower()}",
            day_start + (day_end - day_start) * i / 8,
            day_start + (day_end - day_start) * (i + 1) / 8,
        )
        for i, name in enumerate(CHOGHADIYA[weekday])
    ]
    return DailyWindows(
        sunrise=sunrise,
        sunset=sunset,
        moonrise=moonrise,
        moonset=moonset,
        rahu_kaal=day_part_window("rahu_kaal", RAHU_PART[weekday]),
        yamaganda=day_part_window("yamaganda", YAMAGANDA_PART[weekday]),
        gulika_kaal=day_part_window("gulika_kaal", GULIKA_PART[weekday]),
        abhijit_muhurta=_window(
            "abhijit_muhurta",
            abhijit_center - abhijit_length / 2,
            abhijit_center + abhijit_length / 2,
        ),
        hora=hora,
        choghadiya=chog,
    )


def calculate_panchanga(location: LocationDate) -> PanchangaResult:
    swe = require_swiss_ephemeris()
    midnight = to_utc(datetime.combine(location.date, time()), location.timezone_name)
    jd = julian_day(midnight)
    phase_values = {
        kind: _phase(swe, jd, location, kind) for kind in ("tithi", "nakshatra", "yoga", "karana")
    }
    tithi_index = int(phase_values["tithi"] // 12) + 1
    paksha = "Shukla" if tithi_index <= 15 else "Krishna"
    tithi_name = f"{paksha} {TITHIS[(tithi_index - 1) % 15]}"
    nak_index = int(phase_values["nakshatra"] // (360 / 27))
    yoga_index = int(phase_values["yoga"] // (360 / 27))
    karana_index = int(phase_values["karana"] // 6) + 1
    if karana_index == 1:
        karana_name = "Kimstughna"
    elif karana_index <= 57:
        karana_name = KARANA_MOVABLE[(karana_index - 2) % 7]
    else:
        karana_name = ("Shakuni", "Chatushpada", "Naga")[karana_index - 58]
    sunrise = _rise_set(location, swe.SUN, True, location.date)
    sunset = _rise_set(location, swe.SUN, False, location.date)
    if sunrise is None or sunset is None:
        raise ValueError("Sunrise or sunset was not found for the requested location/date")
    windows = _daily_windows(
        location,
        sunrise,
        sunset,
        _rise_set(location, swe.MOON, True, location.date),
        _rise_set(location, swe.MOON, False, location.date),
    )
    from simplyjyotish_engine.astronomy.positions import calculate_planetary_positions

    provenance = calculate_planetary_positions(_birth_at_midnight(location)).provenance
    return PanchangaResult(
        provenance=provenance,
        local_date=location.date,
        tithi=_panchanga_element(location, "tithi", jd, 12.0, tithi_index, tithi_name),
        nakshatra=_panchanga_element(
            location, "nakshatra", jd, 360 / 27, nak_index + 1, NAKSHATRAS[nak_index][0]
        ),
        yoga=_panchanga_element(location, "yoga", jd, 360 / 27, yoga_index + 1, YOGAS[yoga_index]),
        karana=_panchanga_element(location, "karana", jd, 6.0, karana_index, karana_name),
        windows=windows,
        warnings=[
            "muhurta_conventions_are_versioned_default_daytime_rules",
            "moonrise_or_moonset_can_be_unavailable_at_extreme_latitudes",
        ],
        explain_calculation={
            "tithi": "sidereal Moon minus Sun phase divided into 30 segments of 12 degrees",
            "nakshatra": "sidereal Moon longitude divided into 27 equal nakshatras",
            "yoga": "sidereal Sun plus Moon phase divided into 27 equal segments",
            "karana": "half-tithi phase divided into 60 six-degree segments",
            "boundary_solver": "deterministic bracketed bisection on Swiss Ephemeris positions",
        },
    )
