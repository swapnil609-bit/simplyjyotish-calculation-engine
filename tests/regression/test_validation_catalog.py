import json
from pathlib import Path

import pytest

CATALOG_PATH = Path("tests/fixtures/validation_reference_catalog.json")
DISCREPANCY_PATH = Path("tests/fixtures/validation_discrepancies.json")


def _catalog() -> dict:
    return json.loads(CATALOG_PATH.read_text())


def _discrepancies() -> dict:
    return json.loads(DISCREPANCY_PATH.read_text())


def test_validation_catalog_contains_independent_source_metadata() -> None:
    catalog = _catalog()
    assert catalog["schema_version"] == "reference_validation_catalog_v1"
    assert len(catalog["records"]) >= 10
    status_fields = {
        "implemented",
        "unit_tested",
        "source_verified",
        "cross_implementation_verified",
        "expert_reviewed",
    }
    for record in catalog["records"]:
        assert record["source"]
        assert record.get("source_location")
        assert record["edition_or_software"]
        assert "settings" in record
        assert "expected_result" in record
        assert "permitted_tolerance" in record
        assert status_fields <= record.keys()
        assert all(isinstance(record[field], bool) for field in status_fields)
        assert record["release_status"] in {
            "stable", "provisional", "experimental", "excluded_from_default"
        }
        assert record.get("covered_families")


def test_catalog_covers_validation_closure_priority_families() -> None:
    covered = {
        family
        for record in _catalog()["records"]
        for family in record["covered_families"]
    }
    required = {
        "sthana_bala", "dig_bala", "kala_bala", "cheshta_bala", "naisargika_bala", "drik_bala",
        "shadbala_totals", "bhava_bala", "ishta_phala", "kashta_phala", "vimsopaka_bala",
        "bhava_chalit", "yogini_dasha", "ashtottari_dasha", "ashtottari_eligibility",
        "bhinna_ashtakavarga", "prastara_ashtakavarga", "sarvashtakavarga", "trikona_shodhana",
        "ekadhipatya_shodhana", "shodhya_pinda", "D5", "D6", "D8", "D11",
        "special_lagnas", "upagrahas", "arudha_lagna", "avasthas", "pushkara",
    }
    assert required <= covered


def test_shadbala_reference_contains_all_six_components_and_totals() -> None:
    catalog = _catalog()
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


def test_ashtakavarga_fixture_covers_every_table_and_pinda_component() -> None:
    record = next(item for item in _catalog()["records"] if item["domain"] == "ashtakavarga")
    expected = record["expected_result"]
    assert set(expected["bhinna_ashtakavarga"]) == {
        "sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn"
    }
    assert all(len(row) == 12 for row in expected["bhinna_ashtakavarga"].values())
    assert len(expected["sarvashtakavarga"]) == 12
    assert all(len(expected["shodhya_pinda"][key]) == 7 for key in ("rasi", "graha", "total"))
    assert record["expected_result"]["prastara_source_location"]


def test_dasha_fixture_preserves_prebirth_reference_and_engine_anchor_as_distinct() -> None:
    record = next(item for item in _catalog()["records"] if item["domain"] == "dasha")
    first_yogini = record["expected_result"]["yogini_first_cycle"][0]["start_local"]
    first_ashtottari = record["expected_result"]["ashtottari_first_cycle"][0]["start_local"]
    assert tuple(first_yogini[:3]) < (1996, 12, 7)
    assert tuple(first_ashtottari[:3]) < (1996, 12, 7)
    assert "before birth" in record["expected_result"]["reference_start_behavior"]


def test_known_mismatches_are_registered_and_not_silently_tuned() -> None:
    entries = _discrepancies()["entries"]
    discrepancy_ids = {item["id"] for item in entries}
    assert {
        "DISC-SHADBALA-VPJAIN-001",
        "DISC-BHAVA-CHALIT-001",
        "DISC-YOGINI-ANCHOR-001",
        "DISC-ASHTOTTARI-ELIGIBILITY-001",
        "DISC-ASHTAKAVARGA-SP-001",
        "DISC-EXTENDED-VARGA-METHODS-001",
        "DISC-SPECIAL-POINTS-CONVENTION-001",
        "DISC-SPECIAL-POINTS-NAME-001",
        "DISC-JHORA-UNAVAILABLE-001",
    } <= discrepancy_ids
    assert {item["classification"] for item in entries} <= {"A", "B", "C", "D", "E"}
    assert {item["classification"] for item in entries} >= {"B", "C", "D", "E"}


@pytest.mark.parametrize(
    "filename", ["validation_reference_catalog.json", "validation_discrepancies.json"]
)
def test_validation_fixtures_are_strict_json(filename: str) -> None:
    parsed = json.loads((CATALOG_PATH.parent / filename).read_text())
    assert isinstance(parsed, dict)
