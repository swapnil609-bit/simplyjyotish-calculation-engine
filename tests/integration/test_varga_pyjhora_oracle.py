"""Independent development-time comparison against the pinned PyJHora release."""

from decimal import Decimal

import pytest
from jhora.horoscope.chart import charts

from simplyjyotish_engine.vargas.parashara_bphs import (
    SHODASHAVARGA_DIVISIONS,
    calculate_placement,
)

ORACLE_FUNCTIONS = {
    2: (charts.hora_chart, 2),
    3: (charts.drekkana_chart, 1),
    4: (charts.chaturthamsa_chart, 1),
    7: (charts.saptamsa_chart, 1),
    9: (charts.navamsa_chart, 1),
    10: (charts.dasamsa_chart, 1),
    12: (charts.dwadasamsa_chart, 1),
    16: (charts.shodasamsa_chart, 1),
    20: (charts.vimsamsa_chart, 1),
    24: (charts.chaturvimsamsa_chart, 1),
    27: (charts.nakshatramsa_chart, 1),
    30: (charts.trimsamsa_chart, 1),
    40: (charts.khavedamsa_chart, 1),
    45: (charts.akshavedamsa_chart, 1),
    # Method 2 implements the BPHS degree-within-sign D60 sign mapping.
    60: (charts.shashtyamsa_chart, 2),
}
FIXED_NON_BOUNDARY_LONGITUDES = tuple(
    Decimal("0.123456") + Decimal(index) * Decimal("1.137") for index in range(25)
)


@pytest.mark.parametrize("division", SHODASHAVARGA_DIVISIONS[1:])
@pytest.mark.parametrize("case_index", range(25))
def test_parashari_shodashavarga_matches_pyjhora_4_8_7_on_fixed_cases(
    division: int, case_index: int
) -> None:
    source_sign = (case_index * 5 + division) % 12
    longitude = FIXED_NON_BOUNDARY_LONGITUDES[case_index]
    _, expected_sign, _ = calculate_placement(source_sign, longitude, division)
    function, method = ORACLE_FUNCTIONS[division]
    oracle_sign = function([["L", [source_sign, float(longitude)]]], chart_method=method)[0][1][0]
    assert expected_sign == oracle_sign
