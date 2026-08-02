# Output contracts

Public results are Pydantic models and serialize to stable JSON. Longitudes
are returned in decimal degrees and DMS. Results include engine version,
calculation standard version, ephemeris mode, known ephemeris file version,
ayanamsa, node type, source timezone, resolved UTC, latitude, and longitude.
Warnings are machine-readable. `explain_calculation` contains method and
input identifiers, never hidden reasoning.

Objective yoga and condition results use `YogaFact` and `DoshaFact`. They
include a stable identifier, convention version, detected flag, involved
planets/houses, raw calculation facts, satisfied and unsatisfied conditions,
cancellation/weakening or exception fields, source citations, and structured
`ValidationStatus`. They contain no outcome, prediction, remedy, score, or
interpretation prose.

Special points, avasthas, Chara Karakas, and birth-time sensitivity use the
same provenance and validation model. Sensitivity output is a deterministic
timeline over a configured range and step; it is not automatic rectification.
