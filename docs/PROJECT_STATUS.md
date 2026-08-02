# Project status

Status date: 2026-08-02  
Runtime: Python 3.12.10  
Repository state at phase start: clean  
Last approved commit: `7dec915`

## Completed and green

- Swiss Ephemeris Python 3.12 build through Visual Studio Build Tools 2022.
- BPHS Parashari Shodashavarga default scheme:
  `parashara_bphs_chapter_6_v1`.
- Vimshottari Mahadasha through Prana.
- 424-test suite, Ruff, and mypy passing at the last checkpoint.

## Gaps identified for this phase

- Bhava Chalit, Yogini, and Ashtottari are implemented in the current phase.
- These features carry explicit expert-review status because house-boundary,
  dasha applicability, and tradition-specific subperiod conventions vary.
- Panchanga elements and start/end endpoints are implemented.
- Sunrise/sunset/moonrise/moonset, Rahu Kaal, Yamaganda, Gulika Kaal,
  Abhijit, Hora, and daytime Choghadiya are implemented.
- Transit snapshots, ingress/station timelines, and deterministic Sade Sati
  condition flags are implemented.

## Validation posture

Every new result will include the existing provenance plus method/version
metadata, warnings, boundary behavior, and an `explain_calculation` object.
No calculated fact will be converted into interpretation or prediction text.
