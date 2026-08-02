# Project status

Status date: 2026-08-02  
Runtime: Python 3.12.10  
Repository state at phase start: clean  
Last completed milestone commit: `5c9f076`

## Completed and green

- Swiss Ephemeris Python 3.12 build through Visual Studio Build Tools 2022.
- BPHS Parashari Shodashavarga default scheme:
  `parashara_bphs_chapter_6_v1`.
- Vimshottari Mahadasha through Prana.
- 437-test suite, Ruff, and mypy passing after the current implementation pass.

## Gaps identified for this phase

- Bhava Chalit, Yogini, and Ashtottari are implemented in the current phase.
- These features carry explicit expert-review status because house-boundary,
  dasha applicability, and tradition-specific subperiod conventions vary.
- Panchanga elements and start/end endpoints are implemented.
- Sunrise/sunset/moonrise/moonset, Rahu Kaal, Yamaganda, Gulika Kaal,
  Abhijit, Hora, and day/night Choghadiya are implemented.
- Transit snapshots, ingress/station timelines, and deterministic Sade Sati
  condition flags are implemented.
- Nighttime Choghadiya and validated regional Muhurta table overrides are
  implemented.
- Transit events now use coarse brackets plus tolerance-controlled bisection;
  event outputs include configured tolerance and achieved precision.
- Advanced relationships, Shadbala, Ashtakavarga, and explicit extended
  D5/D6/D8/D11 methods are implemented in the current milestone.

## Validation posture

Every new result will include the existing provenance plus method/version
metadata, warnings, boundary behavior, and an `explain_calculation` object.
No calculated fact will be converted into interpretation or prediction text.
