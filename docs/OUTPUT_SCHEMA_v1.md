# Output schema v1

All public Pydantic results serialize to JSON. Results containing astronomical
provenance include:

- `provenance.engine_version`
- `provenance.calculation_standard_version`
- `provenance.output_schema_version` (`1.0.0`)
- ephemeris mode and known ephemeris version
- ayanamsa, node type, zodiac and source timezone
- resolved UTC, latitude and longitude

Calculation families additionally expose their `method_id`, `convention`, or
`convention_version`, warnings and `explain_calculation` fields. Validation
objects expose `release_status`, implementation/test/source/cross-implementation/
expert-review flags, references and notes.

## Compatibility policy

Adding optional fields is compatible within schema major version 1. Removing
or renaming fields, changing units, changing enum values, or changing the
meaning of an existing field requires a new schema major version. A formula or
tradition change requires a new calculation/convention identifier even when
the JSON shape remains unchanged.
