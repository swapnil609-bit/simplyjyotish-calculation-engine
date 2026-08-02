# SimplyJyotish Calculation Engine v0.1.0-alpha

## Scope

This alpha is a deterministic Python calculation library and CLI. It does not
contain a website, mobile application, REST server, AI, interpretation,
prediction, remedies, accounts, payments, or proprietary prediction logic.

## Included

- Swiss Ephemeris-backed sidereal chart calculations and provenance.
- BPHS Chapter 6 Shodashavarga baseline.
- Panchanga, Muhurta primitives, transits and event timelines.
- Dashas, relationships, strengths, Ashtakavarga, objective conditions and
  explicit special-point primitives.
- Structured JSON outputs with output schema version `1.0.0`, calculation
  standard identifiers, convention identifiers and validation status.

## Validation

The release candidate contains independent PyJHora 4.8.7 fixtures and a
classified discrepancy register. Official Jagannatha Hora 8.0 was attempted,
but no automated report comparison was possible in the available environment.
See `VALIDATION_REPORT.md` and `docs/VALIDATION_DISCREPANCIES.md`.

## Limitations

Strength calculations, convention-sensitive dashas, special points, extended
Vargas and some house/Muhurta conventions are provisional or experimental.
They are not expert-reviewed and must not be treated as prediction output.
