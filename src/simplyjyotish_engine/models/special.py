from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from simplyjyotish_engine.models.outputs import Provenance
from simplyjyotish_engine.models.validation import ValidationStatus


class SpecialPoint(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    point_id: str
    longitude_degrees: float = Field(ge=0, lt=360)
    sign_index: int = Field(ge=0, le=11)
    house: int | None = Field(default=None, ge=1, le=12)
    source_facts: dict[str, Any]


class SpecialPointsResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    provenance: Provenance
    convention_version: str
    points: list[SpecialPoint]
    validation_status: ValidationStatus
    warnings: list[str] = Field(default_factory=list)


class CharaKarakaFact(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    karaka: str
    planet: str
    degrees_in_sign: float
    rank: int = Field(ge=1, le=8)
    source_facts: dict[str, Any]


class CharaKarakaResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    provenance: Provenance
    convention_version: str
    karakas: list[CharaKarakaFact]
    validation_status: ValidationStatus


class AvasthaFact(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    planet: str
    convention_version: str
    bala_avastha: str
    jagradadi_avastha: str
    deeptadi_avastha: str
    source_facts: dict[str, Any]


class AvasthaResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    provenance: Provenance
    avasthas: list[AvasthaFact]
    validation_status: ValidationStatus


class VargaClassificationFact(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    planet: str
    pushkara_navamsha: bool
    pushkara_bhaga: bool
    vargottama: bool
    vaiseshikamsa: bool
    source_facts: dict[str, Any]


class VargaClassificationResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    provenance: Provenance
    convention_version: str
    classifications: list[VargaClassificationFact]
    validation_status: ValidationStatus


class SensitivityChange(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    feature: str
    first_changed_offset_seconds: float
    before_value: Any
    after_value: Any
    details: dict[str, Any]


class BirthTimeSensitivityResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    provenance: Provenance
    convention_version: str
    range_start_offset_seconds: float
    range_end_offset_seconds: float
    sample_step_seconds: float
    changes: list[SensitivityChange]
    sampled_timeline: list[dict[str, Any]]
    confidence_warnings: list[str]
    validation_status: ValidationStatus
