# Supported features

## Stable default profile

The default release profile enables only sufficiently validated foundations:

- Python 3.12+ input validation and IANA timezone conversion.
- Swiss Ephemeris planetary positions, ascendant, signs, nakshatras and
  sidereal chart provenance.
- `parashara_bphs_chapter_6_v1` BPHS Shodashavarga divisions.
- Deterministic JSON serialization with output schema `1.0.0`.

## Provisional opt-in profile

These APIs are available for development and explicit consumer opt-in, with
validation status exposed in each result:

Panchanga, sunrise/set and moonrise/set, Muhurta primitives, transit events,
Sade Sati conditions, Vimshottari/Yogini/Ashtottari Dashas, Bhava Chalit,
Vedic relationships, Ashtakavarga, objective Yoga/Dosha facts, and birth-time
sensitivity.

## Experimental opt-in profile

Shadbala and Bhava Bala, Ishta/Kashta, Vimsopaka, D5/D6/D8/D11, special
Lagnas, Upagrahas, Avasthas, Pushkara/Vargottama/Vaiseshikamsa and related
convention-sensitive primitives.

## Excluded from default

Alternative divisional methods and non-default Bhava/Muhurta conventions are
available only through explicit versioned method or settings identifiers.
