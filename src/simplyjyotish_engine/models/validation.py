from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ValidationStatus(BaseModel):
    """Machine-readable validation state attached to calculation results."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    implemented: bool = True
    unit_tested: bool = True
    source_verified: bool = False
    cross_implementation_verified: bool = False
    expert_reviewed: bool = False
    source_reference_ids: tuple[str, ...] = Field(default_factory=tuple)
    notes: tuple[str, ...] = Field(default_factory=tuple)
