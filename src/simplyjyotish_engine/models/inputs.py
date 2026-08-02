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


class MuhurtaSettings(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    convention_id: str = "gauri_choghadiya_pyjhora_1"
    choghadiya_day_table: tuple[tuple[str, ...], ...] | None = None
    choghadiya_night_table: tuple[tuple[str, ...], ...] | None = None

    @field_validator("choghadiya_day_table", "choghadiya_night_table")
    @classmethod
    def validate_choghadiya_table(
        cls, value: tuple[tuple[str, ...], ...] | None
    ) -> tuple[tuple[str, ...], ...] | None:
        if value is not None and (len(value) != 7 or any(len(row) != 8 for row in value)):
            raise ValueError("Choghadiya tables must contain seven weekday rows of eight entries")
        return value


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


class LocationDate(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    date: date
    timezone_name: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    settings: CalculationSettings = Field(default_factory=CalculationSettings)
    muhurta: MuhurtaSettings = Field(default_factory=MuhurtaSettings)

    @field_validator("timezone_name")
    @classmethod
    def validate_timezone(cls, value: str) -> str:
        resolve_timezone(value)
        return value


class TransitRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    start_date: date
    end_date: date
    timezone_name: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    planets: tuple[str, ...] = (
        "sun",
        "moon",
        "mercury",
        "venus",
        "mars",
        "jupiter",
        "saturn",
        "rahu",
        "ketu",
    )
    settings: CalculationSettings = Field(default_factory=CalculationSettings)
    coarse_step_hours: int = Field(default=24, ge=1, le=168)
    event_tolerance_seconds: float = Field(default=1.0, gt=0, le=3600)

    @field_validator("timezone_name")
    @classmethod
    def validate_timezone(cls, value: str) -> str:
        resolve_timezone(value)
        return value

    @field_validator("end_date")
    @classmethod
    def validate_date_order(cls, value: date, info: object) -> date:
        start = getattr(info, "data", {}).get("start_date")
        if start is not None and value < start:
            raise ValueError("end_date must not precede start_date")
        return value
