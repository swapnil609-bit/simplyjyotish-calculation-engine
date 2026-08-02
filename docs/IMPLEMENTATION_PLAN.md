# Implementation plan

This plan is calculation-engine-only. Every feature requires typed output,
explicit standards, deterministic tests, regression evidence, and a feature
matrix entry before it is marked complete.

## Completed

1. Foundation: packaging, AGPL notices, Swiss Ephemeris, time conversion,
   planetary positions, CLI, CI.
2. Birth chart core: ascendant, whole-sign houses, signs, nakshatra/pada,
   dignity, retrograde, combustion.
3. Charts and Dashas: BPHS Parashari Shodashavarga, D60 separation, and
   Vimshottari through Prana.

## Current phase

4. Panchang, Muhurta, and transit primitives: Bhava Chalit completion,
   remaining conservative dasha systems, Panchang elements and endpoints,
   daily time windows, ingress/station/event timelines, Sade Sati conditions,
   and structured validation fixtures.

## Next phases

5. Advanced calculations: aspects, Shadbala, Ashtakavarga, objective yoga and
   dosha detectors, matching facts, and birth-time sensitivity.
6. Release readiness: documentation review, reproducible Docker build, CI,
   licence audit, examples, and release notes.

No phase adds a website, mobile app, REST/API server, AI, interpretation,
prediction prose, authentication, payments, persistence, or external
astrology API dependency.

