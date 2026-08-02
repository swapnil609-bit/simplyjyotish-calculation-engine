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
| Extended vargas D5/D6/D8/D11 | planned as separately versioned non-Shodashavarga conventions |
| Equal-from-Ascendant Bhava Chalit chart | implemented and boundary-tested; expert convention review required |
| Yogini dasha through selectable nested depth | implemented and regression-tested; expert convention review required |
| Ashtottari dasha through selectable nested depth | implemented with conservative eligibility gate; expert convention review required |
| Panchanga tithi/nakshatra/yoga/karana with start/end boundaries | implemented and regression-tested; tradition review required |
| Sunrise, sunset, moonrise, moonset | implemented through Swiss Ephemeris; polar no-event cases are explicit |
| Muhurta primitives: Rahu Kaal, Yamaganda, Gulika Kaal, Abhijit, Hora, daytime Choghadiya | implemented with versioned daytime defaults; expert convention review required |
| Transit snapshots, ingress and retrograde station events | implemented with configurable sample grid and boundary bisection |
| Sade Sati three-sign Saturn condition | implemented as deterministic condition flags; no interpretation |
| Interpretation, prediction, UI, REST/API server, persistence, accounts | intentionally excluded |
