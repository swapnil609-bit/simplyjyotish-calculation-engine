from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from simplyjyotish_engine.models.outputs import Provenance


class EventTime(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    event: str
    instant_utc: datetime
    local_time: datetime
    validation_status: str = "implemented_requires_expert_review"


class PanchangaElement(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    element: str
    index: int = Field(ge=1)
    name: str
    start: EventTime
    end: EventTime
    fraction_complete_at_local_midnight: float = Field(ge=0, lt=1)


class TimeWindow(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    event: str
    start: EventTime
    end: EventTime
    validation_status: str = "implemented_requires_expert_review"


class DailyWindows(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    sunrise: EventTime
    sunset: EventTime
    moonrise: EventTime | None = None
    moonset: EventTime | None = None
    rahu_kaal: TimeWindow
    yamaganda: TimeWindow
    gulika_kaal: TimeWindow
    abhijit_muhurta: TimeWindow
    hora: list[TimeWindow]
    choghadiya: list[TimeWindow]


class PanchangaResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    provenance: Provenance
    local_date: date
    tithi: PanchangaElement
    nakshatra: PanchangaElement
    yoga: PanchangaElement
    karana: PanchangaElement
    windows: DailyWindows
    warnings: list[str] = Field(default_factory=list)
    explain_calculation: dict[str, str]


class TransitPoint(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    planet: str
    longitude_degrees: float = Field(ge=0, lt=360)
    sign_index: int = Field(ge=0, le=11)
    retrograde: bool
    speed_longitude_degrees_per_day: float


class TransitSnapshot(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    instant_utc: datetime
    local_time: datetime
    points: list[TransitPoint]
    validation_status: str = "implemented_requires_expert_review"


class TransitEvent(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    event: str
    planet: str
    instant_utc: datetime
    local_time: datetime
    from_sign_index: int | None = Field(default=None, ge=0, le=11)
    to_sign_index: int | None = Field(default=None, ge=0, le=11)
    direction: str | None = None
    validation_status: str = "implemented_requires_expert_review"


class TransitTimeline(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    provenance: Provenance
    snapshots: list[TransitSnapshot]
    events: list[TransitEvent]
    warnings: list[str] = Field(default_factory=list)
    explain_calculation: dict[str, str]


class SadeSatiCondition(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    instant_utc: datetime
    local_time: datetime
    saturn_sign_index: int = Field(ge=0, le=11)
    natal_moon_sign_index: int = Field(ge=0, le=11)
    active: bool
    phase: str
    relative_sign_offset: int = Field(ge=0, le=11)
    validation_status: str = "deterministic_condition_requires_expert_review"


class SadeSatiTimeline(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    provenance: Provenance
    conditions: list[SadeSatiCondition]
    warnings: list[str] = Field(default_factory=list)
    explain_calculation: dict[str, str]
