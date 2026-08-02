# Transit and event timeline conventions

Transit snapshots calculate the configured planets at a local-time sampling
grid. Sign ingress and retrograde/direct station candidates are detected from
successive snapshots and refined by deterministic bisection. `sample_hours`
is part of the calculation contract: callers should use a finer grid around
fast-moving bodies or when they require tighter event capture.

Sade Sati is represented only as Saturn occupying the sign immediately before,
the natal Moon sign, or the sign immediately after it. The phase labels are
mechanical (`rising`, `peak`, `setting`) and contain no prediction or
interpretation.

Validation references are the Swiss Ephemeris documentation and the pinned
PyJHora 4.8.7 Panchanga/transit source for comparison only. No external
astrology API is used by the engine.
