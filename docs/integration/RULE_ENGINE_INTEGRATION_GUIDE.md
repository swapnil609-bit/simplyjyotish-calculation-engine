# Rule Engine Integration Guide

The Rule Engine should treat this package as the sole calculation authority.
It should consume structured facts and validation metadata and must never
reimplement chart, dasha, Panchanga, transit, Varga, or strength formulas.

## Public entry points

Library entry points include:

- `calculate_birth_chart(BirthDetails)`
- `calculate_varga(BirthChart, division, scheme_id=...)`
- `calculate_vimshottari_dasha(BirthChart, max_depth=...)`
- `calculate_yogini_dasha(...)` and `calculate_ashtottari_dasha(...)`
- `calculate_panchanga(LocationDate)`
- `calculate_transit_timeline(TransitRequest)` and `calculate_sade_sati(...)`
- `calculate_relationships(BirthChart, conjunction_orb_degrees=...)`
- `calculate_shadbala(BirthChart)` and `calculate_ashtakavarga(BirthChart)`
- objective Yoga/Dosha and special-point functions documented in the feature
  matrix.

The CLI exposes the same families as JSON commands. There is no REST server.

## Inputs and errors

Birth inputs require date, naive local birth time, IANA timezone, latitude,
longitude, and explicit or defaulted calculation settings. Settings include
zodiac, ayanamsha, node type, and ephemeris mode. Transit and daily Panchanga
inputs additionally require a date range/location and may configure event
tolerance or regional Muhurta tables.

Pydantic validation errors are structured field errors. Unsupported methods,
invalid ranges, missing Swiss Ephemeris, unavailable rise/set events, and
unresolvable event brackets must be handled as typed validation or calculation
errors. Do not convert an unavailable astronomical event to a fabricated time.

## Output and manifest

Every Rule Engine-compatible adapter response must include this manifest,
directly or as a referenced immutable object:

```json
{
  "methodology_id": "simplyjyotish_engine_v1",
  "zodiac": "sidereal",
  "ayanamsha_id": "lahiri",
  "house_assignment": "whole_sign_from_ascendant_v1",
  "node_type": "true",
  "vimshottari_year_basis": "365.25_days",
  "divisional_chart_conventions": {
    "D1": "rashi_whole_sign_v1",
    "D9": "parashara_bphs_chapter_6_v1",
    "D10": "parashara_bphs_chapter_6_v1"
  },
  "engine_version": "0.1.0-alpha",
  "contract_version": "1.0.0",
  "ephemeris_version": "2.10.03"
}
```

The raw engine models expose the same critical information through
`provenance`, method/convention fields, and validation fields. The adapter
should normalize them into the manifest above and reject any result whose
node type is absent or ambiguous.

## Fields for direct Rule Engine use

Suitable direct facts include normalized longitudes, signs, houses,
nakshatras/padas, retrograde/combustion/dignity flags, house lords,
dispositor chains, conjunctions, explicit aspect facts, dasha period
boundaries, Panchanga event times, transit event times, and raw Yoga/Dosha
conditions.

The adapter may normalize datetime serialization to UTC, enum strings to a
single internal representation, tuple values to arrays, and decimal-degree
units to the engine's documented degree units. It must preserve the original
value, unit, convention identifier, provenance, warnings, and validation
status when normalization is performed.

## Fields requiring caution

Strength totals, Ashtakavarga Shodhana/Pinda, non-Vimshottari dasha outputs,
Bhava Chalit, extended Vargas, special points, Avasthas, and regional Muhurta
results are not stable expert-certified facts. The Rule Engine must gate them
on `release_status` and the five validation flags.

## Prohibited recalculation

The Rule Engine must never independently calculate planetary positions,
ayanamsha, houses, Vargas, aspects, combustion, dignity, dashas, Panchanga,
Muhurta, transits, Sade Sati, Shadbala, Ashtakavarga, or condition facts. It
must not add prediction prose, scoring, remedies, or interpretations to this
repository's output contract.
