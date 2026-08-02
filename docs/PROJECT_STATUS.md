# Project status

Status date: 2026-08-02  
Runtime: Python 3.12.10  
Repository state at phase start: clean  
Last completed milestone commit: `831a5e9`

## Completed and green

- Swiss Ephemeris Python 3.12 build through Visual Studio Build Tools 2022.
- BPHS Parashari Shodashavarga default scheme:
  `parashara_bphs_chapter_6_v1`.
- Vimshottari Mahadasha through Prana.
- 437-test suite, Ruff, and mypy passing after the current implementation pass.

## Gaps identified for this phase

- Bhava Chalit, Yogini, and Ashtottari are implemented in the current phase.
- These features carry explicit expert-review status because house-boundary,
  dasha applicability, and tradition-specific subperiod conventions vary.
- Panchanga elements and start/end endpoints are implemented.
- Sunrise/sunset/moonrise/moonset, Rahu Kaal, Yamaganda, Gulika Kaal,
  Abhijit, Hora, and day/night Choghadiya are implemented.
- Transit snapshots, ingress/station timelines, and deterministic Sade Sati
  condition flags are implemented.
- Nighttime Choghadiya and validated regional Muhurta table overrides are
  implemented.
- Transit events now use coarse brackets plus tolerance-controlled bisection;
  event outputs include configured tolerance and achieved precision.
- Advanced relationships, Shadbala, Ashtakavarga, and explicit extended
  D5/D6/D8/D11 methods are implemented in the current milestone.
- Independent validation metadata is pinned in
  `tests/fixtures/validation_reference_catalog.json`; flags are explicit and
  mismatches are not silently tuned away.
- Fact-only yoga and dosha/condition detectors are implemented with raw facts,
  exceptions/cancellations, source citations, and structured validation state.
- Birth-time sensitivity and versioned special-point primitives are implemented
  for sampled boundary analysis, including Pushkara Navamsha, Pushkara Bhaga,
  Vargottama, and Vaiseshikamsa classifications. Source and expert review
  remain pending for those school-specific conventions.

## Current milestone completion

- Objective yoga and dosha/condition contracts, sensitivity analysis, special
  points, and auxiliary classifications are implemented and tested.
- Full validation completed: 444 tests passed, Ruff passed, mypy passed.
- Independent expected-value catalog includes the VP Jain Shadbala arrays,
  Bhava Bala, Ishta Phala, Vimsopaka reference values, and Ashtakavarga
  regression metadata. Engine parity remains honestly flagged where formulas
  are provisional.

## Validation posture

Every new result will include the existing provenance plus method/version
metadata, warnings, boundary behavior, and an `explain_calculation` object.
No calculated fact will be converted into interpretation or prediction text.
