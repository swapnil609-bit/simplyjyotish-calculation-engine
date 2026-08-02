from pathlib import Path

from simplyjyotish_engine.ashtakavarga.calculator import calculate_ashtakavarga
from simplyjyotish_engine.aspects.relationships import calculate_relationships
from simplyjyotish_engine.models.inputs import BirthDetails
from simplyjyotish_engine.strengths.calculator import calculate_shadbala
from simplyjyotish_engine.vargas.extended import EXTENDED_VARGA_METHODS
from simplyjyotish_engine.vargas.framework import calculate_varga
from simplyjyotish_engine.vedic.chart import calculate_birth_chart


def _chart():
    birth = BirthDetails.model_validate_json(Path("tests/fixtures/sample_birth.json").read_text())
    return calculate_birth_chart(birth)


def test_relationships_expose_configured_methods_and_chains() -> None:
    result = calculate_relationships(_chart(), conjunction_orb_degrees=8)
    assert result.graha_drishti_method_id == "parashari_graha_drishti_v1"
    assert result.jaimini_rashi_drishti_method_id == "jaimini_rashi_drishti_v1"
    assert result.dispositorship_chains
    assert all(fact.configured_orb_degrees == 8 for fact in result.conjunctions)


def test_shadbala_has_six_components_and_bhava_outputs() -> None:
    result = calculate_shadbala(_chart())
    assert len(result.planets) == 7
    assert all(len(planet.components) == 6 for planet in result.planets)
    assert all(
        {component.name for component in planet.components}
        == {
            "sthana_bala",
            "dig_bala",
            "kaala_bala",
            "cheshta_bala",
            "naisargika_bala",
            "drik_bala",
        }
        for planet in result.planets
    )
    assert len(result.bhava_bala) == 12


def test_ashtakavarga_tables_and_shodhanas_have_expected_shapes() -> None:
    result = calculate_ashtakavarga(_chart())
    assert len(result.sarvashtakavarga) == 12
    assert all(len(row) == 12 for row in result.bhinna_ashtakavarga.values())
    assert all(len(row) == 8 for row in result.prastara_ashtakavarga.values())
    assert all(len(row) == 12 for row in result.trikona_shodhana.values())
    assert set(result.shodhya_pinda) == {
        "sun",
        "moon",
        "mars",
        "mercury",
        "jupiter",
        "venus",
        "saturn",
    }


def test_extended_vargas_require_explicit_method_and_do_not_change_baseline() -> None:
    chart = _chart()
    for division, (method_id, _, _) in EXTENDED_VARGA_METHODS.items():
        try:
            calculate_varga(chart, division)
        except ValueError as error:
            assert "outside the default Shodashavarga baseline" in str(error)
        else:
            raise AssertionError("extended varga must require an explicit convention identifier")
        result = calculate_varga(chart, division, method_id)
        assert result.varga_scheme_id == method_id
        assert result.validation_status.expert_reviewed is False
    assert calculate_varga(chart, 9).varga_scheme_id == "parashara_bphs_chapter_6_v1"
