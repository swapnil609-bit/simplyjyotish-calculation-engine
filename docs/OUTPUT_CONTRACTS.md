# Output contracts

Public results are Pydantic models and serialize to stable JSON. Longitudes
are returned in decimal degrees and DMS. Results include engine version,
calculation standard version, ephemeris mode, known ephemeris file version,
ayanamsa, node type, source timezone, resolved UTC, latitude, and longitude.
Warnings are machine-readable. `explain_calculation` contains method and
input identifiers, never hidden reasoning.

