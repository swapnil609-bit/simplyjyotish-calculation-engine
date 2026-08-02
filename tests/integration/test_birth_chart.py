from pathlib import Path

from simplyjyotish_engine.models.inputs import BirthDetails
from simplyjyotish_engine.vedic.chart import calculate_birth_chart
from simplyjyotish_engine.vargas.framework import calculate_varga
from simplyjyotish_engine.vargas.parashara_bphs import SHODASHAVARGA_DIVISIONS


def test_birth_chart_has_ascendant_houses_and_facts() -> None:
    birth = BirthDetails.model_validate_json(Path("tests/fixtures/sample_birth.json").read_text())
    chart = calculate_birth_chart(birth)
    assert 0 <= chart.ascendant.longitude.decimal_degrees < 360
    assert len(chart.houses) == 12
    assert len(chart.planets) == 12
    assert all(1 <= planet.house <= 12 for planet in chart.planets)


def test_all_default_shodashavargas_include_lagna_and_vedic_grahas() -> None:
    birth = BirthDetails.model_validate_json(Path("tests/fixtures/sample_birth.json").read_text())
    chart = calculate_birth_chart(birth)
    for division in SHODASHAVARGA_DIVISIONS:
        varga = calculate_varga(chart, division)
        assert varga.varga_scheme_id == "parashara_bphs_chapter_6_v1"
        assert varga.ascendant.planet == "lagna"
        assert {"sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn", "rahu", "ketu"} <= {
            planet.planet for planet in varga.planets
        }
