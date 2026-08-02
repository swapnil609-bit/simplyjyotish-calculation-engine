from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from simplyjyotish_engine.models.outputs import Provenance


class DashaPeriod(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    level: str
    lord: str
    start: datetime
    end: datetime
    duration_days: float = Field(gt=0)
    parent_lord: str | None = None


class DashaTimeline(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    system: str
    convention: str
    provenance: Provenance
    periods: list[DashaPeriod]
    warnings: list[str] = Field(default_factory=list)

    def active_at(self, instant: datetime) -> list[DashaPeriod]:
        return [period for period in self.periods if period.start <= instant < period.end]
