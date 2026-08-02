from pathlib import Path

from simplyjyotish_engine.charts.bhava import calculate_bhava_chalit
from simplyjyotish_engine.models.inputs import BirthDetails
from simplyjyotish_engine.vedic.chart import calculate_birth_chart


def test_equal_bhava_chalit_has_twelve_cusps_and_all_objects() -> None:
    birth = BirthDetails.model_validate_json(Path("tests/fixtures/sample_birth.json").read_text())
    chart = calculate_birth_chart(birth)
    result = calculate_bhava_chalit(chart)
    assert result.method_id == "equal_from_ascendant_v1"
    assert len(result.cusps) == 12
    assert len(result.placements) == len(chart.planets) + 1
    assert result.placements[0].object_name == "ascendant"
    assert result.placements[0].house == 1


def test_equal_bhava_chalit_wraps_at_zero_degrees() -> None:
    birth = BirthDetails.model_validate_json(Path("tests/fixtures/sample_birth.json").read_text())
    result = calculate_bhava_chalit(calculate_birth_chart(birth))
    cusp_degrees = [cusp.cusp_longitude.decimal_degrees for cusp in result.cusps]
    assert all(0 <= value < 360 for value in cusp_degrees)
    assert all(result.cusps[index].number == index + 1 for index in range(12))
