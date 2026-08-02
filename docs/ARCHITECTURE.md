# Architecture

The engine is a pure calculation library with a thin CLI. Inputs are strict
Pydantic models; calculation modules accept typed models and return typed
models; JSON serialization happens at the boundary. No module performs
network access, geocoding, persistence, interpretation, or prediction.

`core` owns versioned settings, time conversion, errors, and provenance.
`models` owns public contracts. `astronomy` wraps Swiss Ephemeris. Future
`vedic`, `panchang`, `dashas`, and other domains must depend on these layers,
not duplicate astronomical calculations. `adapters` contains interfaces only.

Milestone 1 implements the foundation path: `BirthDetails` -> resolved UTC
moment -> planetary positions -> JSON/CLI output. Every result carries the
calculation standard and ephemeris provenance needed for reproducibility.

