from pathlib import Path

from simplyjyotish_engine.dashas.vimshottari import calculate_vimshottari_dasha
from simplyjyotish_engine.models.dasha import DashaDepth
from simplyjyotish_engine.models.inputs import BirthDetails
from simplyjyotish_engine.vedic.chart import calculate_birth_chart


def test_vimshottari_timeline_has_nested_periods() -> None:
    birth = BirthDetails.model_validate_json(Path("tests/fixtures/sample_birth.json").read_text())
    timeline = calculate_vimshottari_dasha(calculate_birth_chart(birth))
    assert timeline.system == "vimshottari"
    assert len([period for period in timeline.periods if period.level == "mahadasha"]) == 18
    assert len([period for period in timeline.periods if period.level == "antardasha"]) == 162
    assert all(period.start < period.end for period in timeline.periods)


def test_pratyantardasha_closes_exactly_on_parent_boundaries() -> None:
    birth = BirthDetails.model_validate_json(Path("tests/fixtures/sample_birth.json").read_text())
    timeline = calculate_vimshottari_dasha(
        calculate_birth_chart(birth), max_depth=DashaDepth.PRATYANTARDASHA, mahadasha_count=1
    )
    antardashas = [period for period in timeline.periods if period.level == "antardasha"]
    assert len(antardashas) == 9
    for parent in antardashas:
        children = [
            period
            for period in timeline.periods
            if period.level == "pratyantardasha" and period.lord_chain[:-1] == parent.lord_chain
        ]
        assert len(children) == 9
        assert children[0].start == parent.start
        assert children[-1].end == parent.end


def test_active_at_birth_contains_every_requested_level() -> None:
    birth = BirthDetails.model_validate_json(Path("tests/fixtures/sample_birth.json").read_text())
    chart = calculate_birth_chart(birth)
    timeline = calculate_vimshottari_dasha(chart, max_depth=DashaDepth.PRANA, mahadasha_count=1)
    assert [period.level for period in timeline.active_at(chart.provenance.resolved_utc)] == [
        "mahadasha",
        "antardasha",
        "pratyantardasha",
        "sookshma",
        "prana",
    ]
