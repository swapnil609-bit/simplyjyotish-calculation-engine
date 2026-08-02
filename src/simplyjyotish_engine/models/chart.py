from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from simplyjyotish_engine.models.outputs import LongitudeValue, PlanetaryPosition, Provenance


class SignFact(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    index: int = Field(ge=0, le=11)
    name: str
    lord: str
    element: str
    modality: str


class NakshatraFact(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    index: int = Field(ge=0, le=26)
    name: str
    lord: str
    pada: int = Field(ge=1, le=4)
    navamsha_sign: SignFact


class DignityFact(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: str
    reference_sign: str | None = None


class PlanetChartFact(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    position: PlanetaryPosition
    sign: SignFact
    house: int = Field(ge=1, le=12)
    nakshatra: NakshatraFact
    dignity: DignityFact
    retrograde: bool
    combust: bool
    cazimi: bool


class AscendantFact(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    longitude: LongitudeValue
    sign: SignFact


class HouseFact(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    number: int = Field(ge=1, le=12)
    cusp_longitude: LongitudeValue
    sign: SignFact


class BirthChart(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    provenance: Provenance
    julian_day_ut: float
    ascendant: AscendantFact
    houses: list[HouseFact]
    planets: list[PlanetChartFact]
    warnings: list[str] = Field(default_factory=list)
    explain_calculation: dict[str, str]


class BhavaChalitPlacement(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    object_name: str
    longitude: LongitudeValue
    house: int = Field(ge=1, le=12)
    cusp_house: int = Field(ge=1, le=12)
    boundary_distance_degrees: float = Field(ge=0, lt=30)


class BhavaChalitChart(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    provenance: Provenance
    method_id: str
    method: str
    ascendant: LongitudeValue
    cusps: list[HouseFact]
    placements: list[BhavaChalitPlacement]
    warnings: list[str] = Field(default_factory=list)
    explain_calculation: dict[str, str]
