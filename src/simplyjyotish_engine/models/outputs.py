from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from simplyjyotish_engine.core.constants import CALCULATION_STANDARD_VERSION, ENGINE_VERSION
from simplyjyotish_engine.models.inputs import Ayanamsa, NodeType, Zodiac


class Provenance(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    engine_version: str = ENGINE_VERSION
    calculation_standard_version: str = CALCULATION_STANDARD_VERSION
    ephemeris_mode: str
    ephemeris_file_version_when_known: str | None = None
    ayanamsa: Ayanamsa
    node_type: NodeType
    zodiac: Zodiac
    source_input_timezone: str
    resolved_utc: datetime
    latitude: float
    longitude: float


class LongitudeValue(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    decimal_degrees: float = Field(ge=0, lt=360)
    dms: str


class PlanetaryPosition(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    planet: str
    longitude: LongitudeValue
    latitude_degrees: float
    distance_au: float
    speed_longitude_degrees_per_day: float
    right_ascension_degrees: float
    declination_degrees: float
    retrograde: bool


class PlanetaryPositionsResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    provenance: Provenance
    julian_day_ut: float
    positions: list[PlanetaryPosition]
    warnings: list[str] = Field(default_factory=list)
    explain_calculation: dict[str, str]
