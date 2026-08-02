# Feature matrix

| Feature | Status |
|---|---|
| Packaging, licensing, CI scaffold | implemented and tested |
| Strict birth/settings/provenance models | implemented and tested |
| IANA local time to UTC and Julian Day | implemented and tested |
| Swiss Ephemeris planetary positions | implemented and tested when dependency is installed |
| Sidereal/tropical and true/mean node settings | implemented and tested when dependency is installed |
| CLI chart smoke command | implemented and tested when dependency is installed |
| Ascendant, whole-sign houses, signs, nakshatras, padas | implemented and tested when dependency is installed |
| Planetary dignity, retrograde and combustion facts | implemented and tested when dependency is installed |
| BPHS Chapter 6 Parashari Shodashavarga (D1/D2/D3/D4/D7/D9/D10/D12/D16/D20/D24/D27/D30/D40/D45/D60) | implemented and tested |
| D60 sign placement and named-amsha sequence | implemented and tested; not yet reviewed by a practicing Jyotishi |
| Vimshottari through Prana (depth-selectable) | implemented and tested when dependency is installed |
| Extended vargas D5/D6/D8/D11 | implemented as explicit non-default methods; source/expert review pending |
| Equal-from-Ascendant Bhava Chalit chart | implemented and boundary-tested; expert convention review required |
| Yogini dasha through selectable nested depth | implemented and regression-tested; expert convention review required |
| Ashtottari dasha through selectable nested depth | implemented with conservative eligibility gate; expert convention review required |
| Panchanga tithi/nakshatra/yoga/karana with start/end boundaries | implemented and regression-tested; tradition review required |
| Sunrise, sunset, moonrise, moonset | implemented through Swiss Ephemeris; polar no-event cases are explicit |
| Muhurta primitives: Rahu Kaal, Yamaganda, Gulika Kaal, Abhijit, Hora, day/night Choghadiya | implemented with configurable regional tables; expert convention review required |
| Transit snapshots, ingress and retrograde station events | coarse bracket plus tolerance-controlled numerical refinement; endpoint/regression-tested |
| Sade Sati three-sign Saturn condition | implemented as deterministic condition flags; no interpretation |
| Vedic aspects and relationships | implemented: Graha Drishti, Jaimini Rashi Drishti, conjunctions, dispositorship, exchanges, Yuddha, Papakartari |
| Shadbala and Bhava Bala | implemented with six component outputs, Ishta/Kashta, and Vimsopaka fields; expert review pending |
| Ashtakavarga | implemented: BAV, PAV, SAV, Trikona/Ekadhipatya Shodhana, Shodhya Pinda; expert review pending |
| Independent validation catalog | validation-closure catalog implemented with complete priority-family fixtures, component/period comparisons, five status flags, and discrepancy register; 453 tests, Ruff, and mypy pass; JHora parity and expert review remain pending |
| Objective Yoga detectors | implemented as fact-only versioned detections; cross-implementation and expert review pending |
| Objective Dosha and condition detectors | implemented with raw conditions separated from exceptions/weakening factors; Mrityu Bhaga intentionally unavailable |
| Birth-time sensitivity analysis | implemented for configured sampled ranges, Lagna/house/Nakshatra-Pada/D9/D10/D60 and birth-start Vimshottari boundary changes |
| Arudha, Bhava Padas, Upapada, Hora/Ghati/Bhava Lagna | implemented with explicit convention identifiers; expert review pending |
| Chara Karakas, Gulika/Mandi, Upagrahas, Pushkara/Vargottama/Vaiseshikamsa, Avasthas | implemented with explicit conventions; expert/source review pending |
| Interpretation, prediction, UI, REST/API server, persistence, accounts | intentionally excluded |
