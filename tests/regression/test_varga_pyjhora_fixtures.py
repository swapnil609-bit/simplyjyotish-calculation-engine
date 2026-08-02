import json
from decimal import Decimal
from pathlib import Path

import pytest

from simplyjyotish_engine.vargas.parashara_bphs import calculate_placement

FIXTURE_PATH = Path("tests/fixtures/varga_pyjhora_4_8_7.json")
FIXTURE = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


@pytest.mark.parametrize("division", sorted(int(value) for value in FIXTURE["vargas"]))
def test_pinned_pyjhora_regression_fixtures(division: int) -> None:
    group = FIXTURE["vargas"][str(division)]
    longitudes = FIXTURE["longitude_in_sign_degrees"]
    expected_signs = group["expected_varga_signs"]
    assert len(expected_signs) >= 25
    assert set(FIXTURE["entities"]) == {
        "lagna",
        "sun",
        "moon",
        "mars",
        "mercury",
        "jupiter",
        "venus",
        "saturn",
        "rahu",
        "ketu",
    }
    for source_sign, longitude, expected_sign in zip(
        group["source_signs"], longitudes, expected_signs, strict=True
    ):
        assert calculate_placement(source_sign, Decimal(longitude), division)[1] == expected_sign
