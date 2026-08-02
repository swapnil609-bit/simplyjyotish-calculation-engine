from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from simplyjyotish_engine.models.outputs import Provenance
from simplyjyotish_engine.models.validation import ValidationStatus


class YogaFact(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    yoga_id: str
    convention_version: str
    detected: bool
    planets_involved: tuple[str, ...] = Field(default_factory=tuple)
    houses_involved: tuple[int, ...] = Field(default_factory=tuple)
    exact_calculation_facts: dict[str, Any]
    conditions_satisfied: tuple[str, ...] = Field(default_factory=tuple)
    conditions_not_satisfied: tuple[str, ...] = Field(default_factory=tuple)
    cancellation_or_weakening_factors: tuple[str, ...] = Field(default_factory=tuple)
    source_citation: tuple[str, ...] = Field(default_factory=tuple)
    validation_status: ValidationStatus


class YogaDetectionResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    provenance: Provenance
    convention_version: str
    yogas: list[YogaFact]
    warnings: list[str] = Field(default_factory=list)


class DoshaFact(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    condition_id: str
    convention_version: str
    detected: bool
    raw_condition: dict[str, Any]
    exceptions_and_cancellations: tuple[str, ...] = Field(default_factory=tuple)
    severity_factors: tuple[str, ...] = Field(default_factory=tuple)
    planets_involved: tuple[str, ...] = Field(default_factory=tuple)
    houses_involved: tuple[int, ...] = Field(default_factory=tuple)
    source_citation: tuple[str, ...] = Field(default_factory=tuple)
    validation_status: ValidationStatus


class DoshaDetectionResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    provenance: Provenance
    convention_version: str
    conditions: list[DoshaFact]
    warnings: list[str] = Field(default_factory=list)
