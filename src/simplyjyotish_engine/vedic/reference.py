from __future__ import annotations

from simplyjyotish_engine.models.chart import NakshatraFact, SignFact

SIGNS = (
    ("Aries", "mars", "fire", "movable"),
    ("Taurus", "venus", "earth", "fixed"),
    ("Gemini", "mercury", "air", "dual"),
    ("Cancer", "moon", "water", "movable"),
    ("Leo", "sun", "fire", "fixed"),
    ("Virgo", "mercury", "earth", "dual"),
    ("Libra", "venus", "air", "movable"),
    ("Scorpio", "mars", "water", "fixed"),
    ("Sagittarius", "jupiter", "fire", "dual"),
    ("Capricorn", "saturn", "earth", "movable"),
    ("Aquarius", "saturn", "air", "fixed"),
    ("Pisces", "jupiter", "water", "dual"),
)

NAKSHATRAS = (
    ("Ashwini", "ketu"),
    ("Bharani", "venus"),
    ("Krittika", "sun"),
    ("Rohini", "moon"),
    ("Mrigashira", "mars"),
    ("Ardra", "rahu"),
    ("Punarvasu", "jupiter"),
    ("Pushya", "saturn"),
    ("Ashlesha", "mercury"),
    ("Magha", "ketu"),
    ("Purva Phalguni", "venus"),
    ("Uttara Phalguni", "sun"),
    ("Hasta", "moon"),
    ("Chitra", "mars"),
    ("Swati", "rahu"),
    ("Vishakha", "jupiter"),
    ("Anuradha", "saturn"),
    ("Jyeshtha", "mercury"),
    ("Mula", "ketu"),
    ("Purva Ashadha", "venus"),
    ("Uttara Ashadha", "sun"),
    ("Shravana", "moon"),
    ("Dhanishtha", "mars"),
    ("Shatabhisha", "rahu"),
    ("Purva Bhadrapada", "jupiter"),
    ("Uttara Bhadrapada", "saturn"),
    ("Revati", "mercury"),
)

SIGN_SIZE = 30.0
NAKSHATRA_SIZE = 360.0 / 27.0
PADA_SIZE = NAKSHATRA_SIZE / 4.0


def sign_fact(index: int) -> SignFact:
    name, lord, element, modality = SIGNS[index % 12]
    return SignFact(index=index % 12, name=name, lord=lord, element=element, modality=modality)


def sign_index(longitude: float) -> int:
    return int(longitude % 360.0 // SIGN_SIZE)


def nakshatra_fact(longitude: float) -> NakshatraFact:
    normalized = longitude % 360.0
    index = min(26, int(normalized // NAKSHATRA_SIZE))
    within = normalized - index * NAKSHATRA_SIZE
    pada = min(4, int(within // PADA_SIZE) + 1)
    navamsha_index = (index * 4 + pada - 1) % 12
    name, lord = NAKSHATRAS[index]
    return NakshatraFact(
        index=index,
        name=name,
        lord=lord,
        pada=pada,
        navamsha_sign=sign_fact(navamsha_index),
    )
