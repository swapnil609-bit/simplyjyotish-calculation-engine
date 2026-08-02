# Panchanga and Muhurta conventions

The engine uses Swiss Ephemeris sidereal longitudes with the selected engine
ayanamsa. The default output is a calculation record, not an auspiciousness
judgment.

- Tithi is the Moon-minus-Sun phase in 30 equal 12-degree segments.
- Nakshatra is sidereal Moon longitude in 27 equal segments of 13°20′.
- Yoga is the Sun-plus-Moon phase in 27 equal 13°20′ segments.
- Karana is each six-degree half-tithi. The seven repeating movable names and
  the four fixed positions follow the conventional 60-half-tithi sequence.
- Endpoints are found by deterministic bracketed bisection of Swiss
  Ephemeris longitudes around local midnight.
- Sunrise, sunset, moonrise, and moonset use Swiss Ephemeris `rise_trans` with
  the requested geographic coordinates and standard refraction behavior.
- Rahu Kaal, Yamaganda, Gulika Kaal, Abhijit, Hora, and day/night Choghadiya
  use the versioned weekday tables in `panchanga/daily.py`. The default
  `gauri_choghadiya_pyjhora_1` tables are comparison-aligned with PyJHora.
- `LocationDate.muhurta` accepts explicit seven-row regional day/night tables;
  the table shape is validated and the convention identifier is returned in
  the result warnings.

The weekday tables and naming conventions remain marked for practicing
Jyotishi review because regional almanacs differ. Extreme-latitude missing
rise/set events return `windows: null` with a warning rather than fabricated
times.
