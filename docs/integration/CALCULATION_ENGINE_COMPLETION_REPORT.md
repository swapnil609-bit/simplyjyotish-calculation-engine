# Calculation Engine Completion Report

Status: complete for the `v0.1.0-alpha` calculation-engine scope.

## Release identity

- Engine version: `0.1.0-alpha`
- Output schema version: `1.0.0`
- Calculation standard version: `1.0.0`
- Current Git commit at handoff: `ef47227`
- Published tag: `v0.1.0-alpha` (annotated and immutable)
- Repository: `https://github.com/swapnil609-bit/simplyjyotish-calculation-engine`
- License: AGPL-3.0-or-later, with Swiss Ephemeris free-AGPL terms documented in `THIRD_PARTY_NOTICES.md`

## Supported modules

The public engine contains deterministic, structured calculations for:

- Birth charts, planetary positions, ascendant, houses, signs, nakshatras,
  padas, dignity, combustion, and retrograde facts.
- BPHS Chapter 6 Shodashavarga D1/D2/D3/D4/D7/D9/D10/D12/D16/D20/D24/D27/D30/
  D40/D45/D60 using `parashara_bphs_chapter_6_v1`.
- Vimshottari through Prana, Yogini and Ashtottari with explicit status fields.
- Panchanga, sunrise/set, moonrise/set, Muhurta windows, day/night
  Choghadiya, transits, ingress/station refinement, and Sade Sati conditions.
- Parashari and Jaimini relationships, conjunctions, dispositorship,
  exchanges, Graha Yuddha and Papakartari.
- Shadbala-family fields, Ashtakavarga, objective Yoga/Dosha facts, special
  Lagnas, Upagrahas, Avasthas, classifications, and birth-time sensitivity.

## Disabled or experimental modules

Experimental and convention-sensitive calculations are not enabled silently.
They require explicit consumer selection and retain their method/convention
identifier and validation status. This includes Shadbala-family values,
Vimsopaka, extended D5/D6/D8/D11 methods, special-point conventions,
Avasthas, non-Vimshottari dasha conventions, and unresolved regional or
traditional alternatives.

The engine does not contain interpretation, prediction, remedies, scoring,
accounts, a website, a mobile application, an API server, or Prediction Rules
Engine logic.

## Verification and packaging

- Python 3.12.10 release environment: 458 pytest tests passed.
- Ruff: passed.
- Mypy: passed for 57 source files.
- Wheel and source distribution: built successfully.
- Clean-environment installation and test run: passed.
- Secret, private-path, tracked-build-output, and credential-pattern scans:
  passed.
- Package version: `0.1.0a0` (PEP 440 representation of the alpha).

## External validation requirements

Jagannatha Hora 8.0 parity remains pending because its Windows executable did
not expose a usable automated report/export path in this environment. Jyotishi
expert review remains pending. The discrepancy register in
`docs/VALIDATION_DISCREPANCIES.md` records all remaining A/B/C/D/E cases.

## Production-readiness limitations

This is a public alpha, not production-certified software. Consumers must
check `release_status`, `source_verified`, `cross_implementation_verified`,
and `expert_reviewed` before using any result. No result should be marketed as
expert-validated or as a prediction. The separate Rule Engine must consume
facts and statuses, not recalculate astrology independently.
