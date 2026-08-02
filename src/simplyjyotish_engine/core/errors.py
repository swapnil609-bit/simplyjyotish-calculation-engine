class CalculationError(Exception):
    """Base error for unsupported or invalid deterministic calculations."""


class DependencyUnavailableError(CalculationError):
    """Raised when Swiss Ephemeris is not installed."""
