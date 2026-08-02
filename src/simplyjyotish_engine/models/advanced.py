from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from simplyjyotish_engine.models.outputs import Provenance


class AspectFact(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    source: str
    target: str
    method_id: str
    aspect_type: str
    orb_degrees: float = Field(ge=0, le=180)
    from_sign_index: int = Field(ge=0, le=11)
    to_sign_index: int = Field(ge=0, le=11)
    from_house: int = Field(ge=1, le=12)
    to_house: int = Field(ge=1, le=12)


class ConjunctionFact(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    first: str
    second: str
    orb_degrees: float = Field(ge=0, le=180)
    configured_orb_degrees: float = Field(gt=0, le=30)


class ExchangeFact(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    first: str
    second: str
    first_sign_index: int = Field(ge=0, le=11)
    second_sign_index: int = Field(ge=0, le=11)
    exchange_type: str = "parivartana"


class DispositorChain(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    source: str
    chain: tuple[str, ...] = Field(min_length=1)
    cycle_start_index: int | None = Field(default=None, ge=0)


class GrahaYuddhaFact(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    first: str
    second: str
    longitude_separation_degrees: float = Field(ge=0, le=1)
    winner: str | None = None
    convention_id: str


class PapakartariFact(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    target: str
    target_house: int = Field(ge=1, le=12)
    preceding_house: int = Field(ge=1, le=12)
    following_house: int = Field(ge=1, le=12)
    preceding_malefics: tuple[str, ...]
    following_malefics: tuple[str, ...]
    condition: str


class RelationshipResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    provenance: Provenance
    graha_drishti_method_id: str
    jaimini_rashi_drishti_method_id: str
    conjunction_orb_degrees: float = Field(gt=0, le=30)
    graha_drishti: list[AspectFact]
    jaimini_rashi_drishti: list[AspectFact]
    conjunctions: list[ConjunctionFact]
    parivartana: list[ExchangeFact]
    dispositorship_chains: list[DispositorChain]
    graha_yuddha: list[GrahaYuddhaFact]
    papakartari: list[PapakartariFact]
    warnings: list[str] = Field(default_factory=list)
    explain_calculation: dict[str, str]


class StrengthComponent(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str
    total_virupas: float
    subcomponents: dict[str, float]
    validation_status: str = "implemented_requires_expert_review"


class PlanetStrength(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    planet: str
    components: list[StrengthComponent]
    shadbala_total_virupas: float
    shadbala_total_rupas: float
    ishta_phala: float
    kashta_phala: float
    vimsopaka_bala: float
    validation_status: str = "implemented_requires_expert_review"


class BhavaStrength(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    house: int = Field(ge=1, le=12)
    bala_virupas: float
    lord: str
    validation_status: str = "implemented_requires_expert_review"


class ShadbalaResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    provenance: Provenance
    method_id: str
    planets: list[PlanetStrength]
    bhava_bala: list[BhavaStrength]
    warnings: list[str] = Field(default_factory=list)
    explain_calculation: dict[str, str]


class AshtakavargaResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    provenance: Provenance
    method_id: str
    contributor_order: tuple[str, ...]
    bhinna_ashtakavarga: dict[str, tuple[int, ...]]
    prastara_ashtakavarga: dict[str, tuple[tuple[int, ...], ...]]
    sarvashtakavarga: tuple[int, ...]
    trikona_shodhana: dict[str, tuple[int, ...]]
    ekadhipatya_shodhana: dict[str, tuple[int, ...]]
    shodhya_pinda: dict[str, tuple[int, int, int]]
    validation_status: str = "implemented_requires_expert_review"
    warnings: list[str] = Field(default_factory=list)
    explain_calculation: dict[str, str]
