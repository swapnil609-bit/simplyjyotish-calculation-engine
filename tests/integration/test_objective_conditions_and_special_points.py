from datetime import UTC, datetime
from pathlib import Path

import pytest

from simplyjyotish_engine import (
    calculate_avasthas,
    calculate_birth_time_sensitivity,
    calculate_chara_karakas,
    calculate_doshas,
    calculate_lagna_points,
    calculate_special_points,
    calculate_upagrahas,
    calculate_varga_classifications,
    calculate_yogas,
)
from simplyjyotish_engine.models.inputs import BirthDetails
from simplyjyotish_engine.vedic.chart import calculate_birth_chart


@pytest.fixture
def sample_birth() -> BirthDetails:
    return BirthDetails.model_validate_json(Path("tests/fixtures/sample_birth.json").read_text())


def test_yoga_and_dosha_results_are_fact_only_and_versioned(sample_birth: BirthDetails) -> None:
    chart = calculate_birth_chart(sample_birth)
    yogas = calculate_yogas(chart)
    doshas = calculate_doshas(chart)

    assert yogas.yogas
    assert doshas.conditions
    assert all(item.convention_version for item in yogas.yogas)
    assert all(item.validation_status.source_verified for item in yogas.yogas)
    assert all("prediction" not in item.model_dump_json().lower() for item in doshas.conditions)
    kemadruma = next(item for item in yogas.yogas if item.yoga_id == "kemadruma")
    assert "second_from_moon" in kemadruma.exact_calculation_facts
    assert kemadruma.cancellation_or_weakening_factors is not None


def test_special_points_and_avasthas_have_structured_outputs(sample_birth: BirthDetails) -> None:
    chart = calculate_birth_chart(sample_birth)
    arudhas = calculate_special_points(chart)
    karakas = calculate_chara_karakas(chart)
    avasthas = calculate_avasthas(chart)
    classifications = calculate_varga_classifications(chart)
    lagna_points = calculate_lagna_points(chart, sample_birth)
    upagrahas = calculate_upagrahas(chart, sample_birth)

    assert {"arudha_lagna", "upapada_lagna"} <= {point.point_id for point in arudhas.points}
    assert (
        len([point for point in arudhas.points if point.point_id.startswith("bhava_pada_")]) == 12
    )
    assert len(karakas.karakas) == 8
    assert len(avasthas.avasthas) == 12
    assert len(classifications.classifications) == 12
    assert all(
        item.source_facts["vaiseshikamsa_threshold"] == 10
        for item in classifications.classifications
    )
    assert {"hora_lagna", "ghati_lagna", "bhava_lagna"} <= {
        point.point_id for point in lagna_points.points
    }
    assert {"gulika", "mandi", "dhuma", "upaketu"} <= {point.point_id for point in upagrahas.points}


def test_birth_time_sensitivity_records_discrete_timeline(sample_birth: BirthDetails) -> None:
    result = calculate_birth_time_sensitivity(
        sample_birth, range_minutes=5, sample_step_seconds=300
    )

    assert result.range_start_offset_seconds == -300
    assert result.range_end_offset_seconds == 300
    assert len(result.sampled_timeline) == 3
    assert "vimshottari_first_lord" in result.sampled_timeline[0]
    assert "rectification" in result.confidence_warnings[0].lower()


def test_sensitivity_rejects_nonpositive_parameters(sample_birth: BirthDetails) -> None:
    with pytest.raises(ValueError, match="must be positive"):
        calculate_birth_time_sensitivity(sample_birth, range_minutes=0)


def test_sensitivity_requires_aware_evaluation_time(sample_birth: BirthDetails) -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        calculate_birth_time_sensitivity(
            sample_birth,
            range_minutes=1,
            sample_step_seconds=60,
            evaluation_utc=datetime(2020, 1, 1),
        )
    result = calculate_birth_time_sensitivity(
        sample_birth,
        range_minutes=1,
        sample_step_seconds=60,
        evaluation_utc=datetime(2020, 1, 1, tzinfo=UTC),
    )
    assert "active_vimshottari_chain" in result.sampled_timeline[0]
