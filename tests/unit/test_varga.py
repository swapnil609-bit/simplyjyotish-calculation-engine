from decimal import Decimal

import pytest

from simplyjyotish_engine.vargas.parashara_bphs import (
    D60_NAMES,
    SHODASHAVARGA_DIVISIONS,
    calculate_placement,
    d60_name,
    division_part,
)


def test_shodashavarga_scope_is_exactly_the_selected_sixteen() -> None:
    assert SHODASHAVARGA_DIVISIONS == (1, 2, 3, 4, 7, 9, 10, 12, 16, 20, 24, 27, 30, 40, 45, 60)


@pytest.mark.parametrize("division", SHODASHAVARGA_DIVISIONS)
def test_start_and_end_boundaries_are_start_inclusive_end_exclusive(division: int) -> None:
    if division == 30:
        assert calculate_placement(0, Decimal("0"), division)[0] == 1
        assert calculate_placement(0, Decimal("29.999999"), division)[0] == 5
    else:
        assert division_part(Decimal("0"), division) == 1
        assert division_part(Decimal("29.999999"), division) == division


def test_d60_sign_and_name_are_separate_calculations() -> None:
    part, odd_sign, _ = calculate_placement(0, Decimal("0"), 60)
    _, even_sign, _ = calculate_placement(1, Decimal("0"), 60)
    assert part == 1
    assert odd_sign == even_sign == 0
    assert d60_name(0, 1) == D60_NAMES[0]
    assert d60_name(1, 1) == D60_NAMES[-1]


def test_trimshamsha_boundaries_are_start_inclusive() -> None:
    assert calculate_placement(0, Decimal("4.999999"), 30)[2] == "mars"
    assert calculate_placement(0, Decimal("5"), 30)[2] == "saturn"
    assert calculate_placement(1, Decimal("11.999999"), 30)[2] == "mercury"
    assert calculate_placement(1, Decimal("12"), 30)[2] == "jupiter"
