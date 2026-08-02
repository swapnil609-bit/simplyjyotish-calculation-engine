# Calculation Conventions

This document is the explicit convention manifest for Rule Engine adapters.
It supplements the per-result `provenance`, `method_id`, `convention`, and
`validation_status` fields. A consumer must not infer an undocumented default.

## Core astronomy

- Zodiac: configurable `sidereal` or `tropical`; the default is `sidereal`.
- Ayanamsha: configurable among the supported identifiers; the default is
  `lahiri`. Swiss Ephemeris applies the selected sidereal mode.
- House assignment: Swiss Ephemeris `houses_ex` is used for house cusps with
  the whole-sign-from-Ascendant assignment used for planetary chart houses.
  Bhava Chalit is a separate explicit method: `equal_from_ascendant_v1`.
- Nodes: `true` and `mean` are supported. The current default is `true`.
  `CalculationSettings.node_type` makes the choice configurable per request;
  it is copied into every provenance object.
- Ephemeris: Swiss Ephemeris through `pyswisseph`; the release environment
  reports file/library version `2.10.03` when available.
- Transit reference: local midnight through the exclusive next local midnight
  for daily requests; event times are returned in UTC and request timezone.
  Coarse samples locate a bracket and deterministic bisection refines it.

## Relationships and chart facts

- Planetary aspects: `parashari_graha_drishti_v1`; every planet has the
  seventh-sign aspect, with Mars 4th/8th, Jupiter 5th/9th, and Saturn 3rd/10th
  special aspects.
- Rahu/Ketu aspects: the current default uses only the seventh-sign Graha
  Drishti. Alternative node-aspect traditions are not silently substituted.
- Jaimini aspects: separately configured `jaimini_rashi_drishti_v1`, using
  movable-to-fixed, fixed-to-movable, and dual-to-other-dual sign relations.
- Conjunction: absolute ecliptic longitude separation no greater than the
  configured orb; the relationship API default is 8 degrees.
- Graha Yuddha: classical planets in the same sign within 1 degree; the
  winner uses lower absolute latitude as the configured tie-break, otherwise
  winner is null. Identifier: `graha_yuddha_longitude_with_latitude_tiebreak_v1`.
- Combustion: angular distance from the Sun, with current thresholds in
  `vedic/chart.py`: Moon 12, Mars 17, Mercury 14, Jupiter 11, Venus 10, and
  Saturn 15 degrees. Sun is not marked combust. Cazimi is at most 1 degree.
- Retrograde: Swiss Ephemeris longitude speed below zero. Station events are
  refined from a sampled motion-sign bracket.
- Dignity: sign-based exaltation, debilitation, or own-sign tables in
  `vedic/dignity.py`; otherwise the status is `other`.
- House lord: the lord in the engine's fixed twelve-sign reference table for
  the house cusp sign.
- Dispositor: follow the lord of the occupied sign until a cycle or missing
  planet is reached; cycle index is returned.

## Dasha and Vargas

- Vimshottari year basis: `365.25` days.
- Vimshottari boundary: Moon's nakshatra lord with proportional balance at
  birth; periods are start-inclusive and end-exclusive, and nested endpoints
  close exactly on the parent endpoint.
- D1: Rashi chart with sidereal/tropical and ayanamsha settings from provenance;
  planetary houses use whole-sign-from-Ascendant assignment.
- D2: BPHS Chapter 6 Hora mapping in
  `parashara_bphs_chapter_6_v1`; source- and cross-implementation-verified,
  expert review pending.
- D9: BPHS Chapter 6 Navamsha mapping under the same identifier; source- and
  cross-implementation-verified, expert review pending.
- D10: BPHS Chapter 6 Dashamsha mapping under the same identifier; source- and
  cross-implementation-verified, expert review pending.
- D60: BPHS Chapter 6 degree-within-sign mapping and named-amsha sequence,
  start-inclusive/end-exclusive; source- and cross-implementation-verified,
  expert review pending. Other D60 traditions are not the default.
- D5/D6/D8/D11: explicit opt-in alternative methods only; they are outside the
  default BPHS Shodashavarga set and remain experimental.

## Disputed or pending conventions

The following are deliberately not hidden behind a generic “standard” label:

- Full classical Shadbala component formula parity, Bhava Bala, Ishta/Kashta,
  and Vimsopaka weighting.
- Bhava Chalit tradition and non-Vimshottari dasha anchors/eligibility.
- Ashtakavarga Shodhana and Pinda tabulation variants.
- D5/D6/D8/D11 alternative methods.
- Arudha exceptions, Upagraha/Gulika/Mandi regional rules, Avastha naming and
  segmentation, and regional Muhurta tables.
- Node-aspect alternatives and Graha Yuddha alternative winner rules.

Each disputed choice must remain separately versioned and must retain its
validation status. The engine does not claim that an unresolved convention is
expert-reviewed.
