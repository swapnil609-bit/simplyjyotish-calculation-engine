# SimplyJyotish Independent Calculation Engine

This repository is a deterministic Python library and CLI for reproducible
Vedic/Jyotish calculation facts. It calculates astronomy and structured
Jyotish data; it does not interpret a chart or provide predictions.

It deliberately contains no website, mobile app, dashboard, chatbot, AI,
prediction rules, accounts, payments, database, external API server, or
external astrology API dependency. Future SimplyJyotish projects should
consume this engine's versioned models instead of reimplementing astrology
math.

## Development

Python 3.12+ is required. On Windows, `pyswisseph` may require MSVC Build
Tools because its current release may not provide a Python 3.12 wheel. A
reproducible pip setup is documented in `examples/README.md` and pinned in
`requirements-lock.txt`. Run `python -m pytest`,
`python -m simplyjyotish --help`, `python -m ruff check src tests`, and
`python -m mypy src`. Swiss Ephemeris data can be supplied with
`SE_EPHE_PATH`; the engine reports its selected ephemeris mode in every
result.

The default divisional-chart scheme is the documented BPHS Chapter 6 Parashari
Shodashavarga baseline. Its conventions, source references, and validation
evidence are in `docs/VARGA_CONVENTIONS.md` and
`docs/SHODASHAVARGA_REVIEW_PACKAGE.md`.

The project is AGPL-3.0-or-later. Read `LICENSING_STRATEGY.md` before using
Swiss Ephemeris in proprietary software. Astronomical precision does not make
life predictions scientifically certain; this project returns calculations,
not conclusions about a person's life.

The local alpha release classification and limitations are in
`RELEASE_READINESS.md`, `SUPPORTED_FEATURES.md`, `KNOWN_LIMITATIONS.md`, and
`VALIDATION_REPORT.md`.
