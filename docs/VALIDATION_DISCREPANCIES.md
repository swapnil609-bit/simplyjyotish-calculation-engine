# Validation discrepancy register

This register is part of the Validation Closure Milestone. Expected values are
independent of this engine. A mismatch is not resolved by changing a formula
unless a separately identified convention is adopted and tested.

| ID | Family | Reference | Affected fields | Resolution/status |
|---|---|---|---|---|
| `DISC-SHADBALA-VPJAIN-001` | Shadbala | PyJHora 4.8.7 VP Jain example; BPHS Chapter 26 | All six components, totals, Rupas, Bhava Bala, Ishta, Kashta, Vimsopaka | Documented. Current `parashara_shadbala_v1` is a deterministic provisional component model and does not claim parity with the PyJHora tabulation. No formula was tuned. |
| `DISC-BHAVA-CHALIT-001` | Bhava Chalit | PyJHora `drik._bhaava_madhya_new`, house-method output | Cusp longitudes and placements | Resolved by separate conventions: `equal_from_ascendant_v1` remains the SimplyJyotish default; PyJHora quadrant/Bhava-Madhya output is a separate reference method. |
| `DISC-YOGINI-ANCHOR-001` | Yogini Dasha | PyJHora 4.8.7 `yogini_test` | First-period start and balance | Resolved by separate conventions: engine `birth_anchored_v1` starts the emitted timeline at birth; PyJHora `elapsed_balance_before_birth_v1` preserves the pre-birth balance endpoint. |
| `DISC-ASHTOTTARI-ELIGIBILITY-001` | Ashtottari Dasha | PyJHora Chapter 17.3 tests and JHora comparison notes | Eligibility gate, seed and first-period anchoring | Documented. Engine uses `ashtottari_default_rule_v1` with a conservative eligibility gate; reference outputs are retained for eligible examples. |
| `DISC-ASHTAKAVARGA-SP-001` | Ashtakavarga | PyJHora 4.8.7 Chart 7 and source note | Shodhya Pinda book-vs-calculator values | Documented source discrepancy. PyJHora test output is retained as the pinned calculator oracle; printed-book values are not silently substituted. |
| `DISC-EXTENDED-VARGA-METHODS-001` | D5/D6/D8/D11 | PyJHora Chapter 6 method-comparison tests | Alternative method placement arrays | Resolved by explicit method IDs. Existing `*_parashari_alt_v1` methods remain outside the default Shodashavarga baseline; parity is not claimed until an identical method mapping is selected. |
| `DISC-SPECIAL-POINTS-CONVENTION-001` | Special Lagnas, Avasthas, Upagrahas | PyJHora Chapter 4/5 and `pvr_tests.py` | Hora/Ghati/Bhava Lagna, Gulika/Mandi, Avastha naming, Pushkara classifications | Documented as convention-sensitive. Reference outputs and settings are pinned; cross-implementation status remains false where the current engine intentionally uses a simpler explicit convention. |
| `DISC-JHORA-UNAVAILABLE-001` | All closure families | Jagannatha Hora | Independent JHora executable comparison | Blocked by environment availability only. No JHora executable or exported reports are present in the workspace, so no JHora result is invented. |

## Release interpretation

The engine is technically testable and reproducible, but it is not yet an
expert-reviewed or parity-complete release candidate for strength, dasha,
Bhava Chalit, or convention-sensitive special-point calculations. The
validation-closure milestone therefore closes the evidence and discrepancy
process, not the unresolved expert/parity claims.
