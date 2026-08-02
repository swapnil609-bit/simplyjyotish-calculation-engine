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

For the default Shodashavarga scheme, tests cover every source sign, every
division start/middle/end, every boundary at epsilon below/exact/epsilon above,
and deterministic fixed non-boundary comparisons. `tests/fixtures/
varga_pyjhora_4_8_7.json` stores 25 PyJHora 4.8.7 comparison cases per varga,
with source/settings metadata and Lagna plus all nine Vedic grahas represented.
The engine policy is start-inclusive/end-exclusive; any oracle difference at a
boundary is recorded as a convention discrepancy rather than hidden.
