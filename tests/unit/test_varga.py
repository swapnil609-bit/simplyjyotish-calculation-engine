from simplyjyotish_engine.vargas.framework import _varga_sign
from simplyjyotish_engine.vedic.reference import sign_fact, sign_index


def test_navamsa_mapping_boundaries() -> None:
    assert _varga_sign(0, 1, 9) == 0
    assert _varga_sign(1, 1, 9) == 9
    assert _varga_sign(2, 1, 9) == 6


def test_division_part_is_sign_local() -> None:
    assert sign_index(29.999) == 0
    assert sign_fact(0).name == "Aries"
