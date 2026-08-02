# Parashari Shodashavarga conventions

Default scheme: `parashara_bphs_chapter_6_v1`.

This engine implements the sixteen divisions named in BPHS Chapter 6: D1, D2,
D3, D4, D7, D9, D10, D12, D16, D20, D24, D27, D30, D40, D45, and D60. It does
not silently substitute Jaimini, KP, Raman, Kashinatha, PVR-specific, or other
methods. All equal divisions use start-inclusive, end-exclusive Decimal
intervals; D30 uses the explicit unequal BPHS segments.

| Division | Default calculation rule |
|---|---|
| D1 | Source sign. |
| D2 | Odd: Sun/Leo then Moon/Cancer; even: Moon/Cancer then Sun/Leo. |
| D3 | First, fifth, and ninth from the source sign. |
| D4 | The four kendras from the source sign. |
| D7 | Odd signs count from themselves; even signs from the seventh, forward. |
| D9 | Movable/self, fixed/ninth, dual/fifth starting signs. |
| D10 | Odd/self; even/ninth starting signs. |
| D12 | Count from the source sign. |
| D16 | Movable/Aries, fixed/Leo, dual/Sagittarius starts. |
| D20 | Movable/Aries, fixed/Sagittarius, dual/Leo starts. |
| D24 | Odd/Leo and even/Cancer starts. |
| D27 | Fire/Aries, earth/Cancer, air/Libra, water/Capricorn starts. |
| D30 | BPHS unequal five-segment odd/even tables. |
| D40 | Odd/Aries and even/Libra starts. |
| D45 | Movable/Aries, fixed/Leo, dual/Sagittarius starts. |
| D60 | Sign is derived only from the within-sign half-degree part; the named-amsha order separately reverses for even source signs. |

## D60 separation

D60 returns both `varga_sign` and `amsha_name`. The sign follows the BPHS
within-sign calculation and does not depend on whether the source sign is odd
or even. The 60-name sequence is forward in odd signs and reversed in even
signs. The engine intentionally does not attach interpretation or prediction
text to the names.

## Validation state

Every default varga result contains `source_verified`,
`cross_implementation_verified`, and `expert_reviewed`. The first two are true
for this scheme after source-based tests and the pinned PyJHora comparison
fixtures; `expert_reviewed` remains false until a practicing Parashari Jyotishi
reviews it. This does not block public calculation-library release.

## Recorded discrepancy

PyJHora 4.8.7 uses inclusive upper bounds in its D30 table implementation.
This engine deliberately uses the documented start-inclusive, end-exclusive
interval policy, so an exact D30 segment boundary belongs to the following
segment. Non-boundary PyJHora fixture cases agree; the explicit boundary tests
record this policy difference.
