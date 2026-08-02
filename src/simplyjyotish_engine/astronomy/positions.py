from __future__ import annotations

from simplyjyotish_engine.astronomy.ephemeris import PLANETS, require_swiss_ephemeris
from simplyjyotish_engine.core.time import julian_day, to_utc
from simplyjyotish_engine.models.inputs import Ayanamsa, BirthDetails, CalculationSettings, NodeType
from simplyjyotish_engine.models.outputs import (
    LongitudeValue,
    PlanetaryPosition,
    PlanetaryPositionsResult,
    Provenance,
)


def _dms(degrees: float) -> str:
    whole = int(degrees)
    minutes_float = (degrees - whole) * 60
    minutes = int(minutes_float)
    seconds = round((minutes_float - minutes) * 60, 3)
    if seconds >= 60:
        seconds = 0.0
        minutes += 1
    if minutes >= 60:
        minutes = 0
        whole = (whole + 1) % 360
    return f"{whole:03d}°{minutes:02d}'{seconds:06.3f}\""


def _flags(settings: CalculationSettings, swe: object) -> int:
    flags = swe.FLG_SWIEPH | swe.FLG_SPEED
    if settings.zodiac.value == "sidereal":
        flags |= swe.FLG_SIDEREAL
        sidereal_modes = {
            Ayanamsa.LAHIRI: swe.SIDM_LAHIRI,
            Ayanamsa.RAMAN: swe.SIDM_RAMAN,
            Ayanamsa.KRISHNAMURTI: swe.SIDM_KRISHNAMURTI,
            Ayanamsa.YUKTESHWAR: swe.SIDM_YUKTESHWAR,
            Ayanamsa.FAGAN_BRADLEY: swe.SIDM_FAGAN_BRADLEY,
        }
        swe.set_sid_mode(sidereal_modes[settings.ayanamsa])
    return flags


def calculate_planetary_positions(birth: BirthDetails) -> PlanetaryPositionsResult:
    swe = require_swiss_ephemeris()
    settings = birth.settings
    utc = to_utc(birth.local_datetime(), birth.timezone_name)
    jd = julian_day(utc)
    flags = _flags(settings, swe)
    values: list[PlanetaryPosition] = []
    for name, planet in PLANETS.items():
        if name == "ketu":
            rahu = next(item for item in values if item.planet == "rahu")
            longitude = (rahu.longitude.decimal_degrees + 180.0) % 360.0
            values.append(
                PlanetaryPosition(
                    planet=name,
                    longitude=LongitudeValue(decimal_degrees=longitude, dms=_dms(longitude)),
                    latitude_degrees=-rahu.latitude_degrees,
                    distance_au=rahu.distance_au,
                    speed_longitude_degrees_per_day=rahu.speed_longitude_degrees_per_day,
                    right_ascension_degrees=rahu.right_ascension_degrees,
                    declination_degrees=-rahu.declination_degrees,
                    retrograde=rahu.retrograde,
                )
            )
            continue
        calc_planet = (
            swe.TRUE_NODE if name == "rahu" and settings.node_type == NodeType.TRUE else planet
        )
        if name == "rahu" and settings.node_type == NodeType.MEAN:
            calc_planet = swe.MEAN_NODE
        xx, _ = swe.calc_ut(jd, calc_planet, flags)
        longitude = xx[0] % 360.0
        values.append(
            PlanetaryPosition(
                planet=name,
                longitude=LongitudeValue(decimal_degrees=longitude, dms=_dms(longitude)),
                latitude_degrees=xx[1],
                distance_au=xx[2],
                speed_longitude_degrees_per_day=xx[3],
                right_ascension_degrees=xx[4],
                declination_degrees=xx[5],
                retrograde=xx[3] < 0,
            )
        )
    return PlanetaryPositionsResult(
        provenance=Provenance(
            ephemeris_mode="swiss_ephemeris",
            ephemeris_file_version_when_known=getattr(swe, "version", None),
            ayanamsa=settings.ayanamsa,
            node_type=settings.node_type,
            zodiac=settings.zodiac,
            source_input_timezone=birth.timezone_name,
            resolved_utc=utc,
            latitude=birth.latitude,
            longitude=birth.longitude,
        ),
        julian_day_ut=jd,
        positions=values,
        warnings=(
            [] if birth.birth_time_accuracy.value == "exact" else ["birth_time_accuracy_uncertain"]
        ),
        explain_calculation={
            "julian_day": "UTC instant converted from Unix epoch",
            "positions": "Swiss Ephemeris calc_ut",
        },
    )
