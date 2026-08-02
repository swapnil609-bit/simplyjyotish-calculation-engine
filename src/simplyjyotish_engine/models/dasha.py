from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from simplyjyotish_engine.models.outputs import Provenance


class DashaDepth(StrEnum):
    MAHADASHA = "mahadasha"
    ANTARDASHA = "antardasha"
    PRATYANTARDASHA = "pratyantardasha"
    SOOKSHMA = "sookshma"
    PRANA = "prana"


class DashaPeriod(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    level: str
    lord: str
    start: datetime
    end: datetime
    duration_days: float = Field(gt=0)
    parent_lord: str | None = None
    lord_chain: tuple[str, ...] = Field(min_length=1)


class DashaTimeline(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    system: str
    convention: str
    provenance: Provenance
    periods: list[DashaPeriod]
    warnings: list[str] = Field(default_factory=list)

    def active_at(self, instant: datetime) -> list[DashaPeriod]:
        return sorted(
            (period for period in self.periods if period.start <= instant < period.end),
            key=lambda period: len(period.lord_chain),
        )
