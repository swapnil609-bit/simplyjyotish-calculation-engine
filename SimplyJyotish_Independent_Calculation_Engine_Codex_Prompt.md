# SimplyJyotish — Independent Astrology Calculation Engine

## Development brief and master prompt for Codex

**Project name:** `simplyjyotish-calculation-engine`  
**Project type:** Deterministic Vedic/Jyotish calculation library and command-line toolkit  
**Repository visibility:** Public GitHub repository  
**Licence approach:** AGPL-3.0-compatible public repository while Swiss Ephemeris is used under its free AGPL option  
**Scope:** Calculation engine only. This project must have **no website, mobile app, dashboard, chatbot, AI interpretation, prediction copy, payments, authentication system, SaaS API server, or external astrology API dependency.**

---

## 1. Product decision and non-negotiable boundaries

SimplyJyotish will be built as separate independent projects:

1. **Astrology Calculation Engine** — this project
2. Prediction Rules Engine — separate future project
3. AI Interpretation/Translation service — separate future project
4. Website — separate future project
5. Flutter mobile apps — separate future project
6. Admin Dashboard — separate future project
7. Final integration project — separate future project

This repository owns only deterministic, reproducible astrological calculations. It should act like a powerful internal mathematical library that later projects can import or call through a thin adapter created in the integration project.

It must **not** decide whether a person will have a good career, marriage, health, wealth, or bad day. It may return objective astrological facts such as planetary positions, dashas, yogas, dosha flags, strengths, transit events, Panchang values, and calculation explanations. A later rules engine will convert those facts into scores and predictions.

Do not build an HTTP/REST/GraphQL API in this repository. Create:

- a clean Python package;
- typed Python functions/classes;
- a CLI for calculation and regression testing;
- serialisable JSON output schemas;
- adapter interfaces only, so a future private backend can wrap this engine without changing its calculation code.

---

## 2. Swiss Ephemeris and public-AGPL rules

Use Swiss Ephemeris as the primary astronomical calculation foundation because it is the established high-precision engine for planetary positions, houses, eclipses and related astrological calculations.

Use the free **AGPL** option for this public repository. The whole repository, including modifications and any code that directly uses Swiss Ephemeris, must be published under a compatible AGPL-3.0-or-later licence. Include all required copyright and licence notices.

Create these files before writing any implementation:

- `LICENSE` — AGPL-3.0-or-later
- `THIRD_PARTY_NOTICES.md`
- `LICENSING_STRATEGY.md`
- `NOTICE`

`LICENSING_STRATEGY.md` must clearly state:

- Swiss Ephemeris is dual-licensed: AGPL or Swiss Ephemeris Professional Licence.
- This repository deliberately uses the AGPL option and is therefore public source code.
- Before SimplyJyotish puts Swiss Ephemeris into a proprietary/closed-source commercial website, app, server, or distributed software, the owner must obtain and comply with the Swiss Ephemeris Professional Licence or keep all relevant source code publicly available under AGPL.
- This is an engineering note, not legal advice; verify the current terms directly with Astrodienst before commercial launch.

Do not commit any confidential keys, user data, proprietary content, paid ephemeris files, or secrets.

---

## 3. Technical stack

Use:

- Python 3.12+
- `pyswisseph` or a carefully documented maintained binding to Swiss Ephemeris
- Pydantic v2 for strict, serialisable input/output models
- `pytest`, `pytest-cov`, `hypothesis` where useful
- Ruff, mypy, pre-commit
- Typer for a high-quality command-line interface
- `uv` or Poetry for reproducible dependency management; choose one and document it
- Docker only for reproducible development/testing; do not add database services because this engine should not store user data
- GitHub Actions for formatting, linting, type checks, tests, package build and licence-notice verification

Use `Decimal` or integer arc-seconds internally where it protects classification boundaries. Never use fuzzy rounding that could change a sign, nakshatra, pada, tithi, house, or dasha boundary.

---

## 4. Calculation standards — versioned and explicit

Create `docs/CALCULATION_STANDARDS.md`. No output may silently rely on hidden defaults.

Default standards:

| Setting | Default | Alternatives to support |
|---|---|---|
| Zodiac | Sidereal | Tropical only as optional astronomy/Western compatibility mode |
| Ayanamsa | Lahiri / Chitrapaksha | Raman, Krishnamurti/KP, Yukteshwar, Fagan-Bradley, user-defined offset |
| Node calculation | True nodes | Mean nodes |
| Rashi houses | Whole sign | Sripati, Equal, Placidus only where technically appropriate |
| Bhava Chalit | Separate chart mode | KP/Porphyry-style mode only after documented validation |
| Geographic coordinates | WGS84 decimal degrees | Manual coordinate input only; no mandatory geocoding provider |
| Time | IANA timezone and local civil time converted to UTC | Explicit fixed-offset mode for historical/manual cases |
| Ephemeris | Swiss Ephemeris planetary files | JPL file when locally installed; Moshier only as documented fallback |

Every result must include `engine_version`, `calculation_standard_version`, `ephemeris_mode`, `ephemeris_file_version_when_known`, `ayanamsa`, `node_type`, source input timezone, resolved UTC instant, latitude and longitude.

---

## 5. Repository structure

Create this structure. Keep modules small and independently testable.

```text
simplyjyotish-calculation-engine/
├── LICENSE
├── NOTICE
├── README.md
├── THIRD_PARTY_NOTICES.md
├── LICENSING_STRATEGY.md
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── .github/workflows/ci.yml
├── docs/
│   ├── ARCHITECTURE.md
│   ├── CALCULATION_STANDARDS.md
│   ├── FEATURE_MATRIX.md
│   ├── INPUT_CONVENTIONS.md
│   ├── OUTPUT_CONTRACTS.md
│   ├── VALIDATION_STRATEGY.md
│   ├── EXTENSION_GUIDE.md
│   └── REFERENCES.md
├── src/simplyjyotish_engine/
│   ├── core/
│   ├── models/
│   ├── astronomy/
│   ├── vedic/
│   ├── panchang/
│   ├── dashas/
│   ├── vargas/
│   ├── strengths/
│   ├── aspects/
│   ├── yogas/
│   ├── doshas/
│   ├── matchmaking/
│   ├── transits/
│   ├── muhurta/
│   ├── charts/
│   ├── reports/
│   ├── adapters/
│   └── cli/
├── tests/
│   ├── fixtures/
│   ├── unit/
│   ├── integration/
│   ├── regression/
│   └── property/
└── scripts/
```

---

## 6. Input and output principles

### Required birth input model

Create a strict `BirthDetails` model with:

- date of birth;
- local time of birth including seconds when known;
- `timezone_name` as IANA timezone, for example `Asia/Kolkata`;
- latitude and longitude;
- optional place label only for display;
- birth-time accuracy enum: `exact`, `approximate_5_minutes`, `approximate_15_minutes`, `unknown`;
- optional calculation settings override;
- original values preserved without mutation.

The engine must never call a web geocoding, timezone or astrology service. The integration project can resolve a city to coordinates/timezone and pass the final values to this library.

### Output principles

- Return typed Pydantic models that can be exported to JSON.
- Return numeric longitudes in both decimal degrees and a formatted DMS representation.
- Return machine-readable codes plus English display labels. Do not embed interpretation paragraphs.
- Include warnings: uncertain birth time, unavailable high-precision ephemeris file, extreme latitude, historical timezone ambiguity, unsupported date range, boundary sensitivity.
- Add an `explain_calculation` object showing formula/method identifiers and inputs, not chain-of-thought.

---

## 7. Maximum calculation feature matrix

Implement this engine in tested stages. Build as many features as possible, but do not leave fake/stub methods that claim a result. A feature is complete only when it has documented standards, typed output and regression tests.

### A. Foundation astronomy

- Gregorian and Julian calendar input; Julian Day conversion
- UTC conversion with IANA timezone support
- Delta-T handling through Swiss Ephemeris
- Geocentric and topocentric calculations
- Sidereal and tropical positions
- Planetary positions: Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto
- Vedic grahas: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu
- True and mean node options
- Speed, longitude, latitude, distance, declination, right ascension
- Retrograde/direct/stationary status
- Combustion and cazimi thresholds as documented configurable definitions
- Ascendant, MC, ARMC and house cusps
- Sunrise, sunset, moonrise, moonset
- Lunar phase, exact tithi endpoints, new/full moon times
- Solar/lunar eclipses and planetary ingresses where Swiss Ephemeris supports them

### B. Core Jyotish chart facts

- Rashi/sign, sign lord and degree
- Nakshatra, nakshatra lord, pada, navamsha sign
- Lagna, Arudha Lagna and special lagnas where definitions are documented
- House placement from Lagna, Moon and Sun
- House lords, house ownership and placements
- Chara/sthira/dwisvabhava classification
- gender, element, modality, varna and other traditional sign attributes stored as structured reference data
- planetary friendships: natural, temporary and compound
- dignity: exaltation, debilitation, own sign, mooltrikona, friend, enemy, neutral
- directional strength eligibility and digbala components
- Maraka and Badhaka identification with the selected convention stated in output
- Pushkara Navamsha and Pushkara Bhaga flags, with source convention documented

### C. Chart formats and chart rendering data

- D1 Rashi chart
- Bhava Chalit chart
- North Indian chart coordinate/data layout
- South Indian chart coordinate/data layout
- East Indian/Bengali chart coordinate/data layout
- Wheel-chart-neutral data layout for future UI use
- Printable tabular chart data
- Do not create UI images/SVGs in this repository unless they are purely optional data renderers with no web UI dependency.

### D. Divisional / varga charts

Implement exact calculation logic and test boundary values for:

- D1 Rashi
- D2 Hora
- D3 Drekkana
- D4 Chaturthamsa
- D5 Panchamsa
- D6 Shashtamsa
- D7 Saptamsa
- D8 Ashtamsa
- D9 Navamsha
- D10 Dashamsha
- D11 Rudramsa
- D12 Dwadashamsha
- D16 Shodashamsha
- D20 Vimshamsha
- D24 Chaturvimshamsha
- D27 Bhamsa/Nakshatramsa
- D30 Trimshamsha
- D40 Khavedamsha
- D45 Akshavedamsha
- D60 Shashtiamsha
- general `D1..D60` division framework where a classical, documented mapping is supported

Make the varying traditions explicit rather than pretending there is only one universal mapping.

### E. Aspects, conjunctions and relationships

- Standard Vedic graha drishti: all 7th aspects; special Mars, Jupiter and Saturn aspects
- Optional Jaimini rashi drishti
- Optional Western geometric aspects for future interoperability
- Configurable orb calculation and exactness
- Conjunction clusters
- Planetary war / graha yuddha with documented eligibility and decision method
- Mutual reception / parivartana classification
- Sign exchange, house exchange and dispositorship chains
- Papakartari and other objectively detectable enclosure patterns

### F. Dasha systems

Build generic infrastructure for nested dasha periods, exact start/end timestamps, active-period lookup and timeline export.

Implement:

- Vimshottari Dasha: Mahadasha, Antardasha, Pratyantardasha, Sookshma and Prana where calculation precision is validated
- Yogini Dasha
- Ashtottari Dasha with documented eligibility conventions
- Chara Dasha
- Narayana Dasha
- Kala Chakra Dasha only after rigorous validation

Every dasha result must state the starting basis, nakshatra/pada assumption, year-length convention and implementation version.

### G. Strength calculations

- Shadbala with component-level values and total Rupas
- Sthana Bala
- Dig Bala
- Kala Bala
- Cheshta Bala
- Naisargika Bala
- Drik Bala
- Bhava Bala, if all inputs are validated
- Ishta Phala and Kashta Phala
- Vimsopaka Bala
- Avasthas: Baladi, Deeptadi and Jagratadi/Sayanadi only with explicit convention

Do not turn strength into life predictions; return calculated components only.

### H. Ashtakavarga

- Bhinna Ashtakavarga for the seven planets plus Lagna as appropriate
- Sarvashtakavarga
- Rekha/bindu tables by sign and house
- Kakshya support data if definitions are implemented and tested
- Transit score helpers based only on bindu placement, not prediction prose

### I. Yogas and objectively calculable combinations

Create a versioned registry. Each yoga must return:

- `yoga_id`, name, definition version, involved planets/houses, facts supporting the result, status and any caveat.

Prioritise:

- Gaja Kesari Yoga
- Budhaditya Yoga
- Panch Mahapurusha Yogas
- Dhana Yoga patterns
- Raja Yoga patterns
- Vipareeta Raja Yoga patterns
- Neecha Bhanga Raja Yoga patterns
- Dharma Karmadhipati Yoga
- Adhi Yoga
- Chandra-Mangala Yoga
- Parivartana Yogas
- Kemadruma flags, including mitigating factors
- Kala Sarpa pattern variants — fact detection only; do not present it as guaranteed negative destiny
- Nabhasa Yogas where reliable definitions are documented

Place each definition in data/configuration or a dedicated clear evaluator. Add references and tests. Do not copy interpretation wording from commercial astrology sites.

### J. Dosha and condition detectors

Implement transparent calculations for:

- Manglik/Kuja Dosha with configurable houses and cancellation rules represented separately
- Kala Sarpa variants with documented boundary rules
- Pitra Dosha only if a precisely defined rule-set is supplied; otherwise omit rather than invent
- Guru Chandal, Grahan, Shrapit and Kemadruma pattern flags
- Debilitation, combustion and affliction flags
- Mark results as calculation indicators, not medical, legal, financial or guaranteed-life outcomes.

### K. Panchang and calendar engine

- Vara, Tithi, Nakshatra, Yoga, Karana
- Paksha and lunar month
- Amanta and Purnimanta modes
- Hindu month name, Adhika/Kshaya month indicators where supported
- Samvatsara, Vikram Samvat, Shaka Samvat and Kali year where formulas are documented
- daily Panchang for date/time/location
- tithi/nakshatra/yoga/karana start and end times
- Rahu Kaal, Yamaganda, Gulika Kaal
- Abhijit Muhurat
- Hora, Choghadiya and daytime/nighttime segments
- Brahma Muhurta and Nishita Kala only with documented regional/time conventions
- Sankranti/solar ingress events
- Purnima, Amavasya and Ekadashi detection
- festival-calculation primitives only; no hard-coded religious festival content database in this project

### L. Muhurta primitives

This engine can calculate timing factors, not advise the user that an event is certain to succeed.

- Panchang shuddhi facts
- Tara Bala and Chandra Bala
- weekday, tithi, nakshatra and yoga suitability matrices as versioned reference data
- Lagna availability windows
- Hora and Choghadiya windows
- avoidable time windows: Rahu Kaal/Yamaganda/Gulika
- transit/ingress/eclipses as constraints
- a structured candidate-window ranking input/output interface without subjective recommendation copy

### M. Transit, gochar and event engine

- current/transit planetary positions for any timestamp/location
- natal-to-transit sign and house overlay
- exact ingresses and retrograde stations
- transit aspects to natal planets/angles
- Sade Sati phases based on natal Moon sign
- Ashtama Shani and Kantaka Shani flags
- Jupiter and Saturn sign transit periods
- transit timeline for a date range
- ephemeris event calendar export (JSON/CSV)

### N. Kundli matching facts

Implement calculation-only matching methods with clear convention and transparent component scores:

- Ashtakoota / Guna Milan: Varna, Vashya, Tara, Yoni, Graha Maitri, Gana, Bhakoot, Nadi
- total out of 36
- Manglik comparison facts
- Moon sign/nakshatra compatibility facts
- Dasha overlap timeline facts
- optional Dashakoota/South Indian matching only after a documented specification is available

Never return a final marriage recommendation or claim certainty.

### O. Birth-time sensitivity and rectification support

- Calculate chart changes across a user-selected range around the provided birth time
- identify Lagna, house cusp, navamsha and dasha boundary changes
- return a structured sensitivity report
- include primitives to compare known life-event timestamps with candidate charts
- do not claim automated birth-time rectification is certain; only produce evidence tables for future specialist use.

---

## 8. Public package interface and CLI

Provide typed package-level interfaces such as:

```python
calculate_birth_chart(birth: BirthDetails, settings: CalculationSettings) -> BirthChart
calculate_varga(chart: BirthChart, division: int) -> DivisionalChart
calculate_vimshottari_dasha(chart: BirthChart) -> DashaTimeline
calculate_panchang(moment: GeoMoment, settings: CalculationSettings) -> Panchang
calculate_transits(natal: BirthChart, period: DateRange) -> TransitTimeline
calculate_match(first: BirthDetails, second: BirthDetails) -> AshtakootaMatch
analyse_birth_time_sensitivity(birth: BirthDetails, window_minutes: int) -> SensitivityReport
```

Create CLI commands such as:

```bash
simplyjyotish chart --input tests/fixtures/sample_birth.json --output result.json
simplyjyotish panchang --date 2026-08-02 --time 09:00 --lat 17.385 --lon 78.4867 --timezone Asia/Kolkata
simplyjyotish dasha --input tests/fixtures/sample_birth.json
simplyjyotish varga --input tests/fixtures/sample_birth.json --division 9
simplyjyotish match --first first_birth.json --second second_birth.json
simplyjyotish verify --fixture tests/fixtures/regression_cases.json
```

The CLI is for developers and validation. It must not become a website or service.

---

## 9. Validation and quality bar

Accuracy is the highest priority. Create `docs/VALIDATION_STRATEGY.md` and follow it.

1. Every core function requires unit tests.
2. Store known-good regression fixtures with exact expected values and tolerance rules.
3. Test India-specific locations and `Asia/Kolkata`, plus international timezones and daylight-saving transitions.
4. Test leap years, midnight boundaries, historical dates, extreme latitudes and coordinate signs.
5. Test all sign/nakshatra/pada and tithi boundary transitions.
6. Verify Swiss Ephemeris configuration/path handling and clear fallback warnings.
7. Cross-check a small, documented development-only fixture set against at least one independent established calculator. Record only values and test provenance; do not copy reports or interpretations.
8. Add property-based tests where inputs should preserve invariants such as Ketu being exactly opposite Rahu.
9. Do not hide failures. A calculation that cannot be validated must raise a clear unsupported/validation error rather than return invented numbers.
10. Aim for high test coverage on core calculation modules, with the coverage threshold enforced in CI after initial stable coverage is achieved.

---

## 10. Documentation requirements

The README must explain, in simple language:

- what the engine does;
- what it deliberately does not do;
- how AGPL/public GitHub use works;
- how to install/run tests/use CLI;
- how future projects should integrate without duplicating astrology math;
- why a precise astronomical calculation is not a guarantee of life prediction accuracy.

`docs/FEATURE_MATRIX.md` must list every feature as one of:

- implemented and tested;
- implemented but requires additional validation;
- planned;
- intentionally excluded.

`docs/REFERENCES.md` must list the technical and classical/source references used for each complex convention. Use original explanations and implementation; do not copy content from astrology websites.

---

## 11. Engineering discipline

- Start with `ARCHITECTURE.md`, `CALCULATION_STANDARDS.md`, `FEATURE_MATRIX.md`, `VALIDATION_STRATEGY.md`, and the licence files.
- Implement in vertical slices: foundation → chart → tests → next module.
- Make atomic, meaningful Git commits.
- Keep public source readable and well documented.
- Do not add database, accounts, API keys, network calls, user tracking, analytics or cloud deployment.
- Do not use an LLM anywhere in this repository.
- Do not create personal predictions, daily horoscope prose, remedies, consultations or recommendations.
- Do not copy rules from commercial websites or present any calculated factor as scientific certainty.
- Preserve stable calculation output contracts. Any breaking convention change must increment `calculation_standard_version` and document the migration.

---

## 12. Execution plan for Codex

Work in the following order. Do not skip validation to add more features.

### Milestone 1 — foundation

- repository scaffold, licence docs, packaging and CI;
- strict input/settings/output models;
- Swiss Ephemeris configuration;
- time, Julian Day and planetary position calculations;
- tests and CLI smoke command.

### Milestone 2 — birth chart core

- Lagna/houses, signs, nakshatras, padas, dignity, retrograde, combustion;
- chart data layouts;
- detailed regression suite.

### Milestone 3 — charts and dashas

- Bhava Chalit, varga framework and D1/D9/D10/D60;
- Vimshottari dasha framework and tests;
- expand to the remaining validated vargas/dashas.

### Milestone 4 — Panchang, muhurta and transit primitives

- full Panchang;
- daily time windows;
- events, transits and Sade Sati facts;
- date-range performance tests.

### Milestone 5 — advanced calculation modules

- aspects, Shadbala, Ashtakavarga, yogas/doshas, matching and sensitivity analysis;
- only ship each module once tested/documented.

### Milestone 6 — release readiness

- public documentation review;
- complete feature matrix;
- reproducible Docker build;
- CI green;
- licence/notice review;
- example calculation fixtures and release notes.

At the end of every milestone, provide:

1. what is complete;
2. exact commands to test it;
3. known limitations;
4. feature-matrix update;
5. what needs an expert astrologer to decide later.

---

## 13. Final instruction to Codex

Build this as a serious, public, reusable AGPL Jyotish calculation engine with the maximum practical and testable calculation coverage. Prefer correct, documented, reproducible results over superficial feature count. Keep it fully independent from SimplyJyotish website, Flutter app, dashboard, prediction rules and AI. Future projects must consume this engine’s versioned models rather than independently calculating astrology.

Begin by producing the architecture and calculation standards documents, then scaffold Milestone 1. Do not create an external API server or any user-facing UI.
