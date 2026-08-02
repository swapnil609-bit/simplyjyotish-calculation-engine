from __future__ import annotations

import importlib
import os
from typing import Any

from simplyjyotish_engine.core.errors import DependencyUnavailableError

swiss: Any = None
try:
    swiss = importlib.import_module("swisseph")
except ImportError:  # pragma: no cover - exercised in environments without optional install
    pass


PLANETS: dict[str, int] = {
    "sun": 0,
    "moon": 1,
    "mercury": 2,
    "venus": 3,
    "mars": 4,
    "jupiter": 5,
    "saturn": 6,
    "uranus": 7,
    "neptune": 8,
    "pluto": 9,
    "rahu": 10,
    "ketu": 11,
}


def require_swiss_ephemeris() -> Any:
    if swiss is None:
        raise DependencyUnavailableError("pyswisseph is required for planetary calculations")
    ephe_path = os.environ.get("SE_EPHE_PATH")
    if ephe_path:
        swiss.set_ephe_path(ephe_path)
    return swiss
