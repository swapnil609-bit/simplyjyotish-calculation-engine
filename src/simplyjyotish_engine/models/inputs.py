from __future__ import annotations

from datetime import date, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator

from simplyjyotish_engine.core.time import resolve_timezone


class BirthTimeAccuracy(StrEnum):
    EXACT = "exact"
    APPROXIMATE_5_MINUTES = "approximate_5_minutes"
    APPROXIMATE_15_MINUTES = "approximate_15_minutes"
    UNKNOWN = "unknown"


class Zodiac(StrEnum):
    SIDEREAL = "sidereal"
    TROPICAL = "tropical"


class Ayanamsa(StrEnum):
    LAHIRI = "lahiri"
    RAMAN = "raman"
    KRISHNAMURTI = "krishnamurti"
    YUKTESHWAR = "yukteshwar"
    FAGAN_BRADLEY = "fagan_bradley"


class NodeType(StrEnum):
    TRUE = "true"
    MEAN = "mean"


class CalculationSettings(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    zodiac: Zodiac = Zodiac.SIDEREAL
    ayanamsa: Ayanamsa = Ayanamsa.LAHIRI
    node_type: NodeType = NodeType.TRUE
    ephemeris_mode: str = "swiss_ephemeris"


class BirthDetails(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    date_of_birth: date
    local_time_of_birth: datetime
    timezone_name: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    place_label: str | None = None
    birth_time_accuracy: BirthTimeAccuracy = BirthTimeAccuracy.UNKNOWN
    settings: CalculationSettings = Field(default_factory=CalculationSettings)

    @field_validator("local_time_of_birth")
    @classmethod
    def require_naive_time(cls, value: datetime) -> datetime:
        if value.tzinfo is not None:
            raise ValueError("local_time_of_birth must not contain a timezone")
        return value

    @field_validator("timezone_name")
    @classmethod
    def validate_timezone(cls, value: str) -> str:
        resolve_timezone(value)
        return value

    def local_datetime(self) -> datetime:
        return datetime.combine(self.date_of_birth, self.local_time_of_birth.time())
