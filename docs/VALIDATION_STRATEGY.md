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

The independent validation catalog is `tests/fixtures/validation_reference_catalog.json`.
Each record preserves source, edition/software version, settings, ayanamsa,
node method, expected result, permitted tolerance, and the flags
`source_verified`, `cross_implementation_verified`, and `expert_reviewed`.
Published examples and pinned PyJHora 4.8.7 results are evidence records only;
they are never generated from the engine under test. Mismatches remain visible
and are not silently used to tune formulas.

The current catalog covers all six VP Jain Shadbala component arrays, totals,
Bhava Bala, Ishta Phala, Vimsopaka variants, Ashtakavarga/SAV and Shodhya
Pinda, Yogini/Ashtottari comparison provenance, and explicit extended-varga
status. Current-engine achieved-value comparison is still marked pending where
the implementation is intentionally provisional; the independent expected
values are preserved and are not replaced with engine-generated fixtures.
