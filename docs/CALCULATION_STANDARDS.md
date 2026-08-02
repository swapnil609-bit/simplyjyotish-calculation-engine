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

