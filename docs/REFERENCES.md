# References

- Astrodienst, Swiss Ephemeris documentation and licence: <https://www.astro.com/swisseph/>
- Python `zoneinfo` documentation: <https://docs.python.org/3/library/zoneinfo.html>
- IERS conventions for time-scale terminology: <https://www.iers.org/IERS/EN/Publications/TechnicalNotes/technicalNotes.html>
- Brihat Parashara Hora Shastra, Chapter 6, *The Sixteen Divisions of a Rashi*,
  verses 2-41. The current engine convention follows the R. Santhanam English
  edition's chapter/verse structure; see `docs/VARGA_CONVENTIONS.md` for the
  implemented formulas and source-verse references.
- PyJHora 4.8.7, AGPL-3.0, `naturalstupid/PyJHora`, used only as a pinned
  independent development/test oracle with Lahiri ayanamsa. Its source code is
  not copied into this project.
- Jagannatha Hora 8.0 by P.V.R. Narasimha Rao, attempted as an external
  validation reference from the official publisher page during the alpha
  release pass. Its installer did not expose an automated report path in this
  environment, so no JHora values are claimed or copied. Publisher page:
  <https://www.vedicastrologer.org/jh/>.
- B.V. Raman, *How to Judge a Horoscope*, is reserved as a secondary
  comparison source for dasha and bhava conventions.
- PyJHora 4.8.7 `horoscope/dhasa/graha/yogini.py` and `ashtottari.py` are the
  current comparison sources for sequence, duration, and eligibility mechanics.
- PyJHora 4.8.7 `panchanga/drik.py` is a comparison source for Panchanga,
  rise/set, and daily time-window naming; source code is not copied.
- Swiss Ephemeris `rise_trans`, `calc_ut`, and planetary-event documentation
  are the primary astronomical calculation references for daily and transit
  event timing.
- Brihat Parashara Hora Shastra, Chapter 26, *Shadbaladhyaya*, is the primary
  convention reference for the six strength components; PyJHora
  `horoscope/chart/strength.py` is a pinned comparison source.
- Brihat Parashara Hora Shastra, Chapter 12, *Ashtakavarga*, is the primary
  convention reference; PyJHora `horoscope/chart/ashtakavarga.py` is the
  pinned comparison source for tables and shodhana mechanics.
- Classical Graha Drishti, Jaimini Rashi Drishti, and Parivartana conventions
  are represented by explicit method identifiers in
  `docs/ADVANCED_CALCULATIONS_CONVENTIONS.md`; conflicting traditions are not
  silently merged.
- Classical yoga and condition definitions are represented as source-reference
  identifiers in the fact detectors. The current independent comparison
  catalog is `tests/fixtures/validation_reference_catalog.json`; edition,
  settings, tolerance, and verification flags are stored with each record.
- Validation-closure expected values, source locations, settings, tolerances,
  and independent-status flags are catalogued in
  `tests/fixtures/validation_reference_catalog.json`; known mismatches and
  their resolutions are recorded in `docs/VALIDATION_DISCREPANCIES.md` and
  `tests/fixtures/validation_discrepancies.json`.

Classical Jyotish conventions will be added beside the relevant module only
when the exact tradition and implementation rule are specified.
