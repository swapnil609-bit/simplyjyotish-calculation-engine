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

Python 3.12+ and `uv` are recommended. Install with `uv sync --extra dev`,
then run `uv run pytest` and `uv run simplyjyotish --help`. Swiss Ephemeris
data can be supplied with `SE_EPHE_PATH`; the engine reports its selected
ephemeris mode in every result.

The project is AGPL-3.0-or-later. Read `LICENSING_STRATEGY.md` before using
Swiss Ephemeris in proprietary software. Astronomical precision does not make
life predictions scientifically certain; this project returns calculations,
not conclusions about a person's life.

