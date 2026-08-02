from simplyjyotish_engine.vedic.reference import nakshatra_fact, sign_index


def test_sign_boundaries() -> None:
    assert sign_index(0.0) == 0
    assert sign_index(29.999999) == 0
    assert sign_index(30.0) == 1
    assert sign_index(359.999999) == 11


def test_nakshatra_and_pada_boundaries() -> None:
    assert nakshatra_fact(0.0).name == "Ashwini"
    assert nakshatra_fact(0.0).pada == 1
    assert nakshatra_fact(3 + 20 / 60).pada == 2
    assert nakshatra_fact(13 + 20 / 60).name == "Bharani"
