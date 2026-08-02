# Input conventions

`BirthDetails` preserves the supplied local date/time, timezone name,
coordinates, place label, and birth-time accuracy. Coordinates are decimal
degrees in WGS84: latitude is north-positive and longitude is east-positive.
Timezone names must be IANA identifiers. The library never geocodes a place or
guesses a timezone. Fixed offsets are reserved for an explicit future mode.

