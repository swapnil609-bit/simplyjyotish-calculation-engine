from __future__ import annotations

from simplyjyotish_engine.models.events import DailyWindows
from simplyjyotish_engine.models.inputs import LocationDate
from simplyjyotish_engine.panchanga.daily import calculate_panchanga


def calculate_muhurta_primitives(location: LocationDate) -> DailyWindows:
    """Return deterministic daily time windows without an auspiciousness judgment."""
    return calculate_panchanga(location).windows
