from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from simplyjyotish_engine.models.varga import VargaValidationStatus

PARASHARA_SHODASHAVARGA_SCHEME_ID = "parashara_bphs_chapter_6_v1"
SHODASHAVARGA_DIVISIONS = (1, 2, 3, 4, 7, 9, 10, 12, 16, 20, 24, 27, 30, 40, 45, 60)


@dataclass(frozen=True)
class VargaSpec:
    division: int
    name: str
    source_verses: str
    equal_divisions: bool = True


SPECS = {
    1: VargaSpec(1, "Rashi", "BPHS Chapter 6, verses 2-6"),
    2: VargaSpec(2, "Hora", "BPHS Chapter 6, verses 5-6"),
    3: VargaSpec(3, "Drekkana", "BPHS Chapter 6, verses 7-8"),
    4: VargaSpec(4, "Chaturthamsa", "BPHS Chapter 6, verse 9"),
    7: VargaSpec(7, "Saptamsa", "BPHS Chapter 6, verses 10-11"),
    9: VargaSpec(9, "Navamsha", "BPHS Chapter 6, verse 12"),
    10: VargaSpec(10, "Dashamsha", "BPHS Chapter 6, verses 13-14"),
    12: VargaSpec(12, "Dwadashamsha", "BPHS Chapter 6, verse 15"),
    16: VargaSpec(16, "Shodashamsha", "BPHS Chapter 6, verse 16"),
    20: VargaSpec(20, "Vimshamsha", "BPHS Chapter 6, verses 17-21"),
    24: VargaSpec(24, "Chaturvimshamsha", "BPHS Chapter 6, verses 22-23"),
    27: VargaSpec(27, "Saptavimshamsha", "BPHS Chapter 6, verses 24-26"),
    30: VargaSpec(30, "Trimshamsha", "BPHS Chapter 6, verses 27-28", False),
    40: VargaSpec(40, "Khavedamsha", "BPHS Chapter 6, verses 29-30"),
    45: VargaSpec(45, "Akshavedamsha", "BPHS Chapter 6, verses 31-32"),
    60: VargaSpec(60, "Shashtiamsha", "BPHS Chapter 6, verses 33-41"),
}

ODD_SIGNS = {0, 2, 4, 6, 8, 10}
MOVABLE_SIGNS = {0, 3, 6, 9}
FIXED_SIGNS = {1, 4, 7, 10}
DUAL_SIGNS = {2, 5, 8, 11}
FIRE_SIGNS = {0, 4, 8}
EARTH_SIGNS = {1, 5, 9}
AIR_SIGNS = {2, 6, 10}
WATER_SIGNS = {3, 7, 11}

D60_NAMES = (
    "Ghora",
    "Rakshasa",
    "Deva",
    "Kubera",
    "Yaksha",
    "Kindara",
    "Bhrashta",
    "Kulaghna",
    "Garala",
    "Vahni",
    "Maya",
    "Purishaka",
    "Apampati",
    "Marutvan",
    "Kala",
    "Sarpa",
    "Amrita",
    "Indu",
    "Mridu",
    "Komala",
    "Heramba",
    "Brahma",
    "Vishnu",
    "Maheshwara",
    "Deva",
    "Ardra",
    "Kalinasa",
    "Kshiteesha",
    "Kamalakara",
    "Gulika",
    "Mrityu",
    "Kala",
    "Davagni",
    "Ghora",
    "Yama",
    "Kantaka",
    "Shuddha",
    "Amrita",
    "Purnachandra",
    "Vishadagdha",
    "Kulanas",
    "Vamshakshaya",
    "Utpata",
    "Kala",
    "Saumya",
    "Komala",
    "Sheetala",
    "Karaladamshtra",
    "Chandramukhi",
    "Praveena",
    "Kalapavaka",
    "Dhanayudha",
    "Nirmala",
    "Saumya",
    "Krura",
    "Atisheeta",
    "Amrita",
    "Payodhi",
    "Brahmana",
    "Chandrarekha",
)


def division_part(longitude_in_sign: Decimal, division: int) -> int:
    if not Decimal("0") <= longitude_in_sign < Decimal("30"):
        raise ValueError("longitude_in_sign must be in the start-inclusive [0, 30) interval")
    return int(longitude_in_sign / (Decimal("30") / Decimal(division))) + 1


def _equal_sign(source_sign: int, part: int, division: int) -> int:
    index = part - 1
    if division == 1:
        return source_sign
    if division == 2:
        sun_hora = (
            source_sign in ODD_SIGNS and index == 0 or source_sign not in ODD_SIGNS and index == 1
        )
        return 4 if sun_hora else 3
    if division == 3:
        return (source_sign + index * 4) % 12
    if division == 4:
        return (source_sign + index * 3) % 12
    if division == 7:
        return (source_sign + index if source_sign in ODD_SIGNS else source_sign + 6 + index) % 12
    if division == 9:
        start = 0 if source_sign in MOVABLE_SIGNS else 8 if source_sign in FIXED_SIGNS else 4
        return (source_sign + start + index) % 12
    if division == 10:
        return (source_sign + index if source_sign in ODD_SIGNS else source_sign + 8 + index) % 12
    if division == 12:
        return (source_sign + index) % 12
    if division == 16:
        start = 0 if source_sign in MOVABLE_SIGNS else 4 if source_sign in FIXED_SIGNS else 8
        return (start + index) % 12
    if division == 20:
        start = 0 if source_sign in MOVABLE_SIGNS else 8 if source_sign in FIXED_SIGNS else 4
        return (start + index) % 12
    if division == 24:
        return ((4 if source_sign in ODD_SIGNS else 3) + index) % 12
    if division == 27:
        start = (
            0
            if source_sign in FIRE_SIGNS
            else 3
            if source_sign in EARTH_SIGNS
            else 6
            if source_sign in AIR_SIGNS
            else 9
        )
        return (start + index) % 12
    if division == 40:
        return (index if source_sign in ODD_SIGNS else index + 6) % 12
    if division == 45:
        start = 0 if source_sign in MOVABLE_SIGNS else 4 if source_sign in FIXED_SIGNS else 8
        return (start + index) % 12
    if division == 60:
        return index % 12
    raise ValueError(f"Unsupported Parashari Shodashavarga division: D{division}")


def trimshamsha(source_sign: int, longitude_in_sign: Decimal) -> tuple[int, int, str]:
    if source_sign in ODD_SIGNS:
        segments = (
            (Decimal("5"), 0, "mars"),
            (Decimal("10"), 10, "saturn"),
            (Decimal("18"), 8, "jupiter"),
            (Decimal("25"), 2, "mercury"),
            (Decimal("30"), 6, "venus"),
        )
    else:
        segments = (
            (Decimal("5"), 1, "venus"),
            (Decimal("12"), 5, "mercury"),
            (Decimal("20"), 11, "jupiter"),
            (Decimal("25"), 9, "saturn"),
            (Decimal("30"), 7, "mars"),
        )
    for index, (exclusive_end, sign, lord) in enumerate(segments, start=1):
        if longitude_in_sign < exclusive_end:
            return index, sign, lord
    raise ValueError("longitude_in_sign must be less than 30")


def calculate_placement(
    source_sign: int, longitude_in_sign: Decimal, division: int
) -> tuple[int, int, str | None]:
    if division not in SHODASHAVARGA_DIVISIONS:
        raise ValueError(f"Unsupported Parashari Shodashavarga division: D{division}")
    if division == 30:
        part, sign, lord = trimshamsha(source_sign, longitude_in_sign)
        return part, sign, lord
    part = division_part(longitude_in_sign, division)
    return part, _equal_sign(source_sign, part, division), None


def d60_name(source_sign: int, part: int) -> str:
    index = part - 1
    if source_sign not in ODD_SIGNS:
        index = 59 - index
    return D60_NAMES[index]


def validation_status() -> VargaValidationStatus:
    return VargaValidationStatus(
        source_verified=True,
        cross_implementation_verified=True,
        expert_reviewed=False,
    )
