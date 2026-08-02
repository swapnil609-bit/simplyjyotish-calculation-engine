# Validation discrepancy register

This register is part of the Reference Reconciliation and Release Candidate
Milestone. Expected values are independent of this engine. Every entry has a
classification:

- A — confirmed implementation defect
- B — legitimate convention difference
- C — reference configuration or fixture mismatch
- D — reference-data uncertainty
- E — independent reference unavailable

A mismatch is not resolved by changing a formula unless a separately
identified convention is adopted and tested.

| ID | Family | Reference | Affected fields | Resolution/status |
|---|---|---|---|---|
| ID | Family | Class | Resolution/action | Release state |
|---|---|---|---|---|
| `DISC-SHADBALA-VPJAIN-001` | Shadbala, Bhava Bala, Ishta/Kashta, Vimsopaka | D | PyJHora output is independently pinned, but the available source does not establish identical formula/configuration parity for the engine’s explicitly provisional model. Source verification was downgraded to pending; no formula imitation was performed. | experimental |
| `DISC-BHAVA-CHALIT-001` | Bhava Chalit | B | Retained as `equal_from_ascendant_v1`; PyJHora Bhava-Madhya method remains a separately identified reference convention. | provisional |
| `DISC-YOGINI-ANCHOR-001` | Yogini Dasha | B | Retained `birth_anchored_v1` and documented PyJHora `elapsed_balance_before_birth_v1` as separate anchoring conventions. | provisional |
| `DISC-ASHTOTTARI-ELIGIBILITY-001` | Ashtottari Dasha | B | Conservative eligibility, seed and birth-balance rules remain versioned as `ashtottari_default_rule_v1`; eligible reference rows remain pinned. | provisional |
| `DISC-ASHTAKAVARGA-SP-001` | Ashtakavarga | D | PyJHora calculator output is retained; conflicting printed-book Pinda values are recorded as reference-data uncertainty. | provisional |
| `DISC-EXTENDED-VARGA-METHODS-001` | D5/D6/D8/D11 | B | Existing explicit `*_parashari_alt_v1` methods remain opt-in and outside the default BPHS Shodashavarga baseline. | experimental / excluded from default |
| `DISC-SPECIAL-POINTS-CONVENTION-001` | Special Lagnas, Avasthas, Upagrahas | B | Explicit convention identifiers remain; Avastha and regional Gulika/Mandi variants are not promoted to stable defaults. | experimental |
| `DISC-SPECIAL-POINTS-NAME-001` | Solar Upagrahas | C | Corrected the catalog key `indrachaapa` to the engine’s stable `indrachapa` identifier; added exact-ID regression coverage. | provisional |
| `DISC-JHORA-UNAVAILABLE-001` | All closure families | E | Official publisher package was downloaded and launch attempted. The Windows installer hung under headless execution and exposed no CLI/export path; temporary files were removed. No JHora values are claimed. | validation-pending |

## Release interpretation

The reconciliation process is complete for this local alpha candidate. The
engine is technically testable and reproducible, but the alpha is not a
parity-complete or expert-reviewed release. Advanced discrepancy-registered
families are not stable defaults.
