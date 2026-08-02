# Validation strategy

Core time conversion has deterministic unit tests, including DST and
coordinate-sign cases. Swiss Ephemeris integration tests verify provenance,
planet identity, longitude ranges, and the Rahu/Ketu opposition invariant.
Regression fixtures will be added as each domain becomes stable. Values must
be cross-checked against Swiss Ephemeris documentation and an independent
established calculator in development-only fixtures; no commercial report
text is copied. Unsupported precision or date ranges must raise a clear
error or warning rather than invent a value.

Boundary tests for signs, nakshatras, padas, tithis, houses, and dasha periods
are required before those modules are marked complete. CI runs formatting,
linting, type checks, tests, package build, and a licence-notice check.

