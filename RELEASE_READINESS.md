# v0.1.0-alpha release readiness

Status: local release candidate prepared; not published or pushed.

## Classification

- Stable default surface: deterministic input/time conversion, Swiss Ephemeris
  planetary positions, sidereal chart facts, and the BPHS Chapter 6
  `parashara_bphs_chapter_6_v1` Shodashavarga baseline.
- Provisional: Panchanga/Muhurta, transit timelines, Vimshottari/Yogini/
  Ashtottari, Bhava Chalit, relationships, Ashtakavarga, and objective
  yoga/dosha facts.
- Experimental: Shadbala/Bhava Bala/Ishta/Vimsopaka, D5/D6/D8/D11, special
  Lagnas, Upagrahas, Avasthas, and birth-time sensitivity.
- Excluded from default: alternative Varga methods and non-default Bhava
  Madhya/region-specific conventions. They require explicit method IDs or
  settings.

Advanced functions remain importable for development and explicit opt-in
validation, but their `ValidationStatus.release_status` is not stable.

## Gates

- Full pytest, Ruff, mypy, package build, clean-environment installation,
  CLI, deterministic repeatability, notice and secret checks must pass.
- No public release, tag, or push is performed by this milestone.
- Expert review and Jagannatha Hora comparison remain open items.

## Decision

Suitable for local technical review and a public GitHub review branch after
the owner’s approval. Not a claim of expert-reviewed or parity-complete
astrological software.
