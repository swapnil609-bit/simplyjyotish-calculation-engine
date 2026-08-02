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

- Bhava Chalit output contract and tests are not yet implemented.
- Vimshottari is the only dasha family currently implemented; Yogini and
  Ashtottari are the next conservative, explicitly versioned additions.
- Panchang, Muhurta, transit events, ingress/station timelines, and daily
  auspicious/avoidance windows are not yet implemented.

## Validation posture

Every new result will include the existing provenance plus method/version
metadata, warnings, boundary behavior, and an `explain_calculation` object.
No calculated fact will be converted into interpretation or prediction text.

