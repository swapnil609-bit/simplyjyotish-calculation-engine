from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from simplyjyotish_engine.models.chart import SignFact
from simplyjyotish_engine.models.outputs import Provenance
from simplyjyotish_engine.models.validation import ReleaseStatus


class VargaValidationStatus(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    release_status: ReleaseStatus = ReleaseStatus.PROVISIONAL
    implemented: bool = True
    unit_tested: bool = True
    source_verified: bool
    cross_implementation_verified: bool
    expert_reviewed: bool = False


class VargaPlanet(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    planet: str
    source_longitude_degrees: float
    source_sign: SignFact
    division_part: int = Field(ge=1)
    varga_sign: SignFact
    amsha_name: str | None = None
    amsha_deity: str | None = None
    amsha_lord: str | None = None
    amsha_classification: str | None = None


class DivisionalChart(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    division: int = Field(ge=1, le=60)
    name: str
    varga_scheme_id: str
    source_verses: str
    boundary_convention: str
    convention: str
    validation_status: VargaValidationStatus
    provenance: Provenance
    ascendant: VargaPlanet
    planets: list[VargaPlanet]
    warnings: list[str] = Field(default_factory=list)
