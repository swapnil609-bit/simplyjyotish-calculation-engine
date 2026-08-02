from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from simplyjyotish_engine.models.chart import SignFact
from simplyjyotish_engine.models.outputs import Provenance


class VargaPlanet(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    planet: str
    source_longitude_degrees: float
    source_sign: SignFact
    division_part: int = Field(ge=1)
    varga_sign: SignFact


class DivisionalChart(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    division: int = Field(ge=1, le=60)
    name: str
    convention: str
    provenance: Provenance
    planets: list[VargaPlanet]
    warnings: list[str] = Field(default_factory=list)
