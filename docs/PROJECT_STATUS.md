# Project status

Status date: 2026-08-02  
Runtime: Python 3.12.10  
Accepted baseline commit: `5d64904`
Current milestone: Reference Reconciliation and v0.1.0-alpha release candidate

## Scope completed in this milestone

- Added independent reference records for Shadbala and all six components,
  Bhava Bala, Ishta/Kashta, Vimsopaka variants, Bhava Chalit, Yogini,
  Ashtottari and eligibility, Ashtakavarga tables and Shodhana/Pinda, extended
  D5/D6/D8/D11, and convention-sensitive special points.
- Preserved exact source locations, editions/software versions, settings,
  ayanamsa, node and house methods, expected values, tolerances, and the five
  independent validation statuses.
- Added executable component-level comparisons and negative/schema tests.
- Added a discrepancy register for formula, anchoring, house-method,
  book-versus-calculator, convention, and unavailable-JHora differences.
- Kept the SimplyJyotish defaults unchanged; no formula was tuned solely for
  parity.

## Validation status

Full verification run: 455 pytest tests passed, Ruff passed, and mypy passed.

The local release candidate uses package version `0.1.0a0`, engine version
`0.1.0-alpha`, and output schema version `1.0.0`. Release classifications are
documented in `SUPPORTED_FEATURES.md`; advanced discrepancy-registered
families are not stable defaults.

`implemented`, `unit_tested`, `source_verified`,
`cross_implementation_verified`, and `expert_reviewed` are tracked separately
in the catalog and output contracts. Expert review remains pending for
strength conventions, dasha conventions, Bhava Chalit, extended Vargas, and
special-point conventions. Jagannatha Hora parity remains pending because no
executable or exported report is available in the workspace.

The independent catalog is
`tests/fixtures/validation_reference_catalog.json`. The discrepancy register
is `docs/VALIDATION_DISCREPANCIES.md` with machine-readable entries in
`tests/fixtures/validation_discrepancies.json`.

## Boundaries preserved

This repository remains a deterministic Python calculation library with CLI,
tests, structured JSON-compatible outputs, Swiss Ephemeris, and no website,
mobile app, REST/API server, interpretation, prediction, remedies, AI/LLM,
accounts, payments, or external astrology API dependency.

## Release assessment

The local alpha release candidate is technically testable and reproducible but
not parity-complete or expert-reviewed for the discrepancy-registered families.
It is ready for local/public GitHub review only after owner approval; it has
not been tagged, published or pushed.
