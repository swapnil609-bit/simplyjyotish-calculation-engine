from pathlib import Path

from simplyjyotish_engine.models.inputs import BirthDetails
from simplyjyotish_engine.vedic.chart import calculate_birth_chart


def test_birth_chart_has_ascendant_houses_and_facts() -> None:
    birth = BirthDetails.model_validate_json(Path("tests/fixtures/sample_birth.json").read_text())
    chart = calculate_birth_chart(birth)
    assert 0 <= chart.ascendant.longitude.decimal_degrees < 360
    assert len(chart.houses) == 12
    assert len(chart.planets) == 12
    assert all(1 <= planet.house <= 12 for planet in chart.planets)
