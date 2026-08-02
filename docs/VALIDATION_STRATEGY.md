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
node method, house method where applicable, expected result, permitted
tolerance, and the five separate status flags `implemented`, `unit_tested`,
`source_verified`, `cross_implementation_verified`, and `expert_reviewed`.
Published examples and pinned PyJHora 4.8.7 results are evidence records only;
they are never generated from the engine under test. Mismatches remain visible
and are not silently used to tune formulas.

The validation-closure catalog covers all six VP Jain Shadbala components and
totals, Bhava Bala, Ishta/Kashta, all pinned Vimsopaka variants, Bhava Chalit,
Yogini and Ashtottari periods/eligibility, BAV/PAV/SAV, both Shodhana methods,
Shodhya Pinda, D5/D6/D8/D11, and convention-sensitive special Lagnas,
Upagrahas, Arudha, Pushkara and Avastha availability. Executable regression
tests compare every directly comparable numeric field and assert that known
mismatches are present in `docs/VALIDATION_DISCREPANCIES.md` and
`tests/fixtures/validation_discrepancies.json`. A reference-unavailable field
is recorded as such; it is never replaced with an engine-generated expected
value.

The discrepancy register is normative for this milestone. A mismatch is
closed only by identical settings and independent evidence, or by a separately
versioned convention. Jagannatha Hora comparison remains open because its
executable or exported reports are not present in this workspace.
