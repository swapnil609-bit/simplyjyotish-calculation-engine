from pathlib import Path

from simplyjyotish_engine.dashas.ashtottari import (
    ashtottari_eligibility,
    calculate_ashtottari_dasha,
)
from simplyjyotish_engine.dashas.vimshottari import calculate_vimshottari_dasha
from simplyjyotish_engine.dashas.yogini import YOGINI_SEQUENCE, calculate_yogini_dasha
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


def test_yogini_sequence_and_nested_boundaries_are_deterministic() -> None:
    birth = BirthDetails.model_validate_json(Path("tests/fixtures/sample_birth.json").read_text())
    chart = calculate_birth_chart(birth)
    timeline = calculate_yogini_dasha(chart, max_depth=DashaDepth.PRATYANTARDASHA, cycle_count=1)
    maha = [period for period in timeline.periods if period.level == "mahadasha"]
    assert len(maha) == 8
    first_index = YOGINI_SEQUENCE.index(maha[0].lord)
    assert [period.lord for period in maha] == [
        YOGINI_SEQUENCE[(first_index + index) % len(YOGINI_SEQUENCE)] for index in range(8)
    ]
    for parent in [period for period in timeline.periods if period.level == "antardasha"]:
        children = [
            period
            for period in timeline.periods
            if period.level == "pratyantardasha" and period.lord_chain[:-1] == parent.lord_chain
        ]
        assert children[0].start == parent.start
        assert children[-1].end == parent.end


def test_ashtottari_has_explicit_eligibility_and_optional_override() -> None:
    birth = BirthDetails.model_validate_json(Path("tests/fixtures/sample_birth.json").read_text())
    chart = calculate_birth_chart(birth)
    applicable, reason = ashtottari_eligibility(chart)
    assert isinstance(applicable, bool)
    assert reason
    timeline = calculate_ashtottari_dasha(chart, cycle_count=1, require_eligibility=False)
    assert timeline.system == "ashtottari"
    assert timeline.eligibility in {"applicable", "not_applicable"}
    assert len([period for period in timeline.periods if period.level == "mahadasha"]) == 8
