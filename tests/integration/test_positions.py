from pathlib import Path

from simplyjyotish_engine.astronomy.positions import calculate_planetary_positions
from simplyjyotish_engine.models.inputs import BirthDetails


def test_sample_positions_have_provenance_and_node_invariant() -> None:
    fixture = Path("tests/fixtures/sample_birth.json")
    result = calculate_planetary_positions(BirthDetails.model_validate_json(fixture.read_text()))
    by_name = {position.planet: position for position in result.positions}
    assert len(by_name) == 12
    assert result.provenance.calculation_standard_version == "1.0.0"
    separation = (
        by_name["ketu"].longitude.decimal_degrees - by_name["rahu"].longitude.decimal_degrees
    ) % 360
    assert abs(separation - 180.0) < 1e-12
    assert all(0 <= position.longitude.decimal_degrees < 360 for position in result.positions)
