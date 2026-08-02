import json
from pathlib import Path


def test_validation_catalog_contains_independent_source_metadata() -> None:
    path = Path("tests/fixtures/validation_reference_catalog.json")
    catalog = json.loads(path.read_text())
    assert catalog["schema_version"] == "reference_validation_catalog_v1"
    assert len(catalog["records"]) >= 5
    for record in catalog["records"]:
        assert record["source"]
        assert record["edition_or_software"]
        assert "settings" in record
        assert "expected_result" in record
        assert "permitted_tolerance" in record
        assert isinstance(record["source_verified"], bool)
        assert isinstance(record["cross_implementation_verified"], bool)


def test_shadbala_reference_contains_all_six_components_and_totals() -> None:
    catalog = json.loads(Path("tests/fixtures/validation_reference_catalog.json").read_text())
    record = next(item for item in catalog["records"] if item["domain"] == "shadbala")
    expected = record["expected_result"]
    assert {"positional", "temporal", "directional", "motional", "natural", "aspectual"} <= set(
        expected
    )
    assert all(
        len(expected[name]) == 7
        for name in ("positional", "temporal", "directional", "motional", "natural", "aspectual")
    )
    assert len(expected["total_virupas"]) == len(expected["total_rupas"]) == 7
