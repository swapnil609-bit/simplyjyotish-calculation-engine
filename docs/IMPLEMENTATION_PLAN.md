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

4. Panchang, Muhurta, and transit primitives: complete. This includes Bhava
   Chalit, Yogini, Ashtottari, Panchanga elements and endpoints, daily time
   windows, ingress/station/event timelines, Sade Sati conditions, and
   structured validation fixtures.

## Post-release hardening

5. Post-release hardening: continue independent reference reconciliation,
   optional-reference test isolation, boundary/regression coverage, and
   documentation maintenance. No new calculation family is promoted without
   independent source evidence and an explicit validation status.
6. Future release: only after the discrepancy register, expert-review items,
   and reproducible release checks are reassessed. The alpha tag is immutable;
   fixes use a new versioned tag.

No phase adds a website, mobile app, REST/API server, AI, interpretation,
prediction prose, authentication, payments, persistence, or external
astrology API dependency.
