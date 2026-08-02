# Calculation standards

Standard version: `1.0.0`.

Defaults are explicit and serialized: sidereal zodiac; Lahiri/Chitrapaksha
ayanamsa; true lunar nodes; WGS84 coordinates; IANA timezone converted to UTC;
Swiss Ephemeris files when configured, otherwise the documented Moshier
fallback. Tropical zodiac, mean nodes, other ayanamsas, and house systems are
settings, not hidden behavior. Rashi houses default to whole sign; house cusp
systems will be added only with validation.

Milestone 1 exposes astronomical longitude, latitude, distance, speed, and
retrograde status. Boundary-sensitive classifications must use precise values
and must not apply presentation rounding before classification.

Milestone 2 uses 27 equal nakshatras of 13°20' and four equal padas. Whole-sign
planet houses are assigned from the sidereal ascendant sign; Swiss Ephemeris
house cusps are retained as provenance data. Initial combustion thresholds are
Moon 12°, Mars 17°, Mercury 14°, Jupiter 11°, Venus 10°, and Saturn 15° from
the Sun; these are calculation defaults and require tradition-specific review.
Cazimi is flagged at an absolute separation of 1° or less.

Milestone 3 uses the documented Parashari mappings for D1, D9, D10, and D60.
Vimshottari uses the Moon's sidereal nakshatra lord, proportional first-period
balance, nested Antardasha periods, and a fixed 365.25-day dasha year. These
conventions are versioned and must not be changed silently.
