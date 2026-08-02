import json
import math
from datetime import datetime
from pathlib import Path

from simplyjyotish_engine.charts.bhava import calculate_bhava_chalit
from simplyjyotish_engine.models.inputs import BirthDetails
from simplyjyotish_engine.strengths.calculator import calculate_shadbala
from simplyjyotish_engine.vedic.chart import calculate_birth_chart

CATALOG = json.loads(Path("tests/fixtures/validation_reference_catalog.json").read_text())
DISCREPANCIES = json.loads(Path("tests/fixtures/validation_discrepancies.json").read_text())


def _record(record_id: str) -> dict:
    return next(record for record in CATALOG["records"] if record["id"] == record_id)


def _vp_jain_chart():
    birth = BirthDetails(
        date_of_birth=datetime(1981, 9, 13).date(),
        local_time_of_birth=datetime(1981, 9, 13, 1, 30),
        timezone_name="Asia/Kolkata",
        latitude=28.65,
        longitude=77.2166667,
        place_label="VP Jain reference example",
    )
    return calculate_birth_chart(birth)


def _discrepancy_ids() -> set[str]:
    return {item["id"] for item in DISCREPANCIES["entries"]}


def test_vp_jain_shadbala_comparison_executes_all_six_components() -> None:
    reference = _record("pyjhora_shadbala_vp_jain_1981_v1")
    result = calculate_shadbala(_vp_jain_chart())
    by_planet = {item.planet: item for item in result.planets}
    order = ("sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn")
    component_map = {
        "positional": "sthana_bala",
        "temporal": "kaala_bala",
        "directional": "dig_bala",
        "motional": "cheshta_bala",
        "natural": "naisargika_bala",
        "aspectual": "drik_bala",
    }
    comparisons = []
    for reference_name, engine_name in component_map.items():
        expected = reference["expected_result"][reference_name]
        achieved = [
            next(
                component.total_virupas
                for component in by_planet[planet].components
                if component.name == engine_name
            )
            for planet in order
        ]
        comparisons.extend(
            math.isclose(actual, wanted, abs_tol=reference["permitted_tolerance"])
            for actual, wanted in zip(achieved, expected, strict=True)
        )
    achieved_totals = [by_planet[planet].shadbala_total_virupas for planet in order]
    comparisons.extend(
        math.isclose(actual, wanted, abs_tol=reference["permitted_tolerance"])
        for actual, wanted in zip(
            achieved_totals, reference["expected_result"]["total_virupas"], strict=True
        )
    )
    assert len(comparisons) == 49
    assert not all(comparisons)
    assert "DISC-SHADBALA-VPJAIN-001" in _discrepancy_ids()
    assert result.validation_status.source_verified
    assert not result.validation_status.cross_implementation_verified


def test_strength_reference_comparison_covers_bhava_ishta_kashta_and_vimsopaka() -> None:
    reference = _record("pyjhora_vp_jain_bhava_bala_v1")
    strength_reference = _record("pyjhora_vp_jain_ishta_kashta_vimsopaka_v1")
    result = calculate_shadbala(_vp_jain_chart())
    assert len(result.bhava_bala) == 12
    assert len(reference["expected_result"]["bhava_bala_virupas"]) == 12
    assert len(reference["expected_result"]["bhava_bala_rupas"]) == 12
    assert len(strength_reference["expected_result"]["ishta_phala"]) == 7
    assert strength_reference["expected_result"]["kashta_phala"]["expected"] is None
    bhava_achieved = [item.bala_virupas for item in result.bhava_bala]
    bhava_expected = reference["expected_result"]["bhava_bala_virupas"]
    assert any(
        not math.isclose(actual, wanted, abs_tol=reference["permitted_tolerance"])
        for actual, wanted in zip(bhava_achieved, bhava_expected, strict=True)
    )
    ishta_achieved = [item.ishta_phala for item in result.planets]
    ishta_expected = strength_reference["expected_result"]["ishta_phala"]
    assert any(
        not math.isclose(actual, wanted, abs_tol=strength_reference["permitted_tolerance"])
        for actual, wanted in zip(ishta_achieved, ishta_expected, strict=True)
    )
    for planet in result.planets:
        assert {"ishta_phala", "kashta_phala", "vimsopaka_bala"} <= set(planet.model_dump())
    assert "DISC-SHADBALA-VPJAIN-001" in _discrepancy_ids()


def test_bhava_chalit_comparison_keeps_house_methods_separate() -> None:
    record = _record("pyjhora_bhava_madhya_chennai_1996_v1")
    birth = BirthDetails(
        date_of_birth=datetime(1996, 12, 7).date(),
        local_time_of_birth=datetime(1996, 12, 7, 10, 34),
        timezone_name="Asia/Kolkata",
        latitude=13.0878,
        longitude=80.2785,
        place_label="Chennai reference example",
    )
    result = calculate_bhava_chalit(calculate_birth_chart(birth))
    reference_centers = record["expected_result"]["bhava_centers_degrees"]
    achieved_centers = [item.cusp_longitude.decimal_degrees for item in result.cusps]
    assert len(achieved_centers) == len(reference_centers) == 12
    assert result.method_id == "equal_from_ascendant_v1"
    assert record["settings"]["house_method"] == "bhava_madhya_method_1"
    assert "DISC-BHAVA-CHALIT-001" in _discrepancy_ids()
