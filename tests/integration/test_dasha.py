from pathlib import Path

from simplyjyotish_engine.dashas.vimshottari import calculate_vimshottari_dasha
from simplyjyotish_engine.models.inputs import BirthDetails
from simplyjyotish_engine.vedic.chart import calculate_birth_chart


def test_vimshottari_timeline_has_nested_periods() -> None:
    birth = BirthDetails.model_validate_json(Path("tests/fixtures/sample_birth.json").read_text())
    timeline = calculate_vimshottari_dasha(calculate_birth_chart(birth))
    assert timeline.system == "vimshottari"
    assert len([period for period in timeline.periods if period.level == "mahadasha"]) == 18
    assert len([period for period in timeline.periods if period.level == "antardasha"]) == 162
    assert all(period.start < period.end for period in timeline.periods)
