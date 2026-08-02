# Engine Handoff Checkpoint

## Handoff state

- Files created: all files in `docs/integration/` for the completion report,
  conventions, limitations, guide, samples, and JSON Schema.
- Existing local commit pushed before handoff: `b4bcd2d`.
- Existing tag `v0.1.0-alpha`: unchanged; no new tag created.
- Follow-up handoff content commit: `7f8d244` (`docs: add Rule Engine integration handoff`).
- This checkpoint update is a separate documentation-only commit immediately
  after the handoff content commit.
- Contract version: `1.0.0`.
- Engine version: `0.1.0-alpha`.
- Node convention: configurable `true` or `mean`; current default is `true`,
  and it must be explicit in the Rule Engine manifest.

## Verification required for this checkpoint

- Full pytest suite under Python 3.12: 461 passed.
- Ruff and mypy.
- Wheel and source distribution build.
- Clean-environment verification.
- JSON sample/schema parse and contract-field checks.
- Confirmation that `v0.1.0-alpha` still resolves to the original release
  commit and has not been moved or recreated.

## Missing Rule Engine facts

The adapter must normalize the raw engine results into the documented manifest.
In particular, it must preserve method/convention identifiers, release status,
validation flags, warning arrays, provenance, units, and explicit node type.
The engine does not provide prediction rules or interpretation facts.

## External validation items

JHora parity and Jyotishi expert review remain pending. Strength conventions,
some dasha conventions, Bhava Chalit, Ashtakavarga variants, extended Vargas,
and special-point conventions must remain gated by their statuses.

## Release recommendation

After this handoff commit is reviewed and pushed, the next suitable alpha tag
would be `v0.1.0-alpha.1` or `v0.1.0-beta.1` only after explicit owner
approval. This checkpoint does not create either tag.

The Rule Engine may begin development-only adapter integration against the
version `1.0.0` contract. Production integration is not authorized by this
document because the calculation engine remains an alpha and is not expert-
reviewed or production-certified.
