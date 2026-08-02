# Validation report

## Candidate

- Version: `0.1.0-alpha` (`0.1.0a0` package metadata)
- Output schema: `1.0.0`
- Runtime checked: Python 3.12.10 on Windows
- Primary classical source: BPHS Chapters 6, 12, 17.3 and 26
- Independent implementation: PyJHora 4.8.7, development-only

## Reconciled families

The catalog covers Shadbala components, Bhava Bala, Ishta/Kashta, Vimsopaka,
Bhava Chalit, Yogini, Ashtottari, Ashtakavarga/Shodhana/Pinda, D5/D6/D8/D11,
and special Lagnas/Upagrahas/Avasthas. Each record includes settings, source
location, expected result, tolerance and five validation statuses.

## Classification result

Every discrepancy is classified A/B/C/D/E in
`docs/VALIDATION_DISCREPANCIES.md` and
`tests/fixtures/validation_discrepancies.json`. No confirmed A-class defect
remained after reconciliation. The concrete C-class Upagraha fixture key
mismatch was corrected and regression-tested. B-class differences remain
separately versioned; D/E items remain provisional or pending.

## Independent reference posture

The official Jagannatha Hora 8.0 publisher page was checked and its official
short installer was downloaded and attempted. The installer hung under
headless execution and exposed no machine-readable report path. No JHora
expected value is included or claimed.

## Automated evidence

The final run records the full pytest, Ruff, mypy, build, clean-install, CLI,
repeatability, notice and secret-scan results in the release handoff.
