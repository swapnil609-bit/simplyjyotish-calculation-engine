from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, cast

from simplyjyotish_engine.models.chart import BirthChart
from simplyjyotish_engine.models.inputs import BirthDetails, LocationDate
from simplyjyotish_engine.models.special import (
    AvasthaFact,
    AvasthaResult,
    BirthTimeSensitivityResult,
    CharaKarakaFact,
    CharaKarakaResult,
    SensitivityChange,
    SpecialPoint,
    SpecialPointsResult,
    VargaClassificationFact,
    VargaClassificationResult,
)
from simplyjyotish_engine.models.validation import ReleaseStatus, ValidationStatus
from simplyjyotish_engine.panchanga.daily import calculate_panchanga
from simplyjyotish_engine.vargas.framework import calculate_varga

SPECIAL_CONVENTION = "special_points_parashari_configurable_v1"
SOURCE = ("BPHS special-lagna and upagraha chapters; convention review pending",)
CLASSICAL_KARAKA_PLANETS = {
    "sun",
    "moon",
    "mars",
    "mercury",
    "jupiter",
    "venus",
    "saturn",
    "rahu",
}


def _status(*notes: str) -> ValidationStatus:
    return ValidationStatus(
        release_status=ReleaseStatus.EXPERIMENTAL,
        source_verified=True,
        cross_implementation_verified=False,
        source_reference_ids=("bphs_special_points_v1",),
        notes=notes,
    )


def _sign(longitude: float) -> int:
    return int(longitude % 360.0 // 30.0)


def _lord(chart: BirthChart, sign: int) -> str:
    return (
        next(item.sign.lord for item in chart.planets if item.sign.index == sign)
        if any(item.sign.index == sign for item in chart.planets)
        else (
            "mars",
            "venus",
            "mercury",
            "moon",
            "sun",
            "mercury",
            "venus",
            "mars",
            "jupiter",
            "saturn",
            "saturn",
            "jupiter",
        )[sign]
    )


def _arudha(base_sign: int, lord_sign: int) -> tuple[int, dict[str, Any]]:
    distance = (lord_sign - base_sign) % 12
    raw = (lord_sign + distance) % 12
    adjusted = raw
    if raw == base_sign or raw == (base_sign + 6) % 12:
        adjusted = (base_sign + 9) % 12
    return adjusted, {
        "base_sign": base_sign,
        "lord_sign": lord_sign,
        "distance_signs": distance,
        "raw_arudha_sign": raw,
        "exception_applied": adjusted != raw,
    }


def calculate_special_points(chart: BirthChart) -> SpecialPointsResult:
    asc_sign = chart.ascendant.sign.index
    point_specs: list[tuple[str, int]] = [
        ("arudha_lagna", asc_sign),
        ("upapada_lagna", (asc_sign + 11) % 12),
    ]
    points: list[SpecialPoint] = []
    for point_id, base_sign in point_specs:
        lord = _lord(chart, base_sign)
        lord_item = next(item for item in chart.planets if item.position.planet == lord)
        value, facts = _arudha(base_sign, lord_item.sign.index)
        points.append(
            SpecialPoint(
                point_id=point_id,
                longitude_degrees=value * 30.0,
                sign_index=value,
                house=(value - asc_sign) % 12 + 1,
                source_facts={
                    **facts,
                    "sign_lord": lord,
                    "rule": "count lord distance from base and repeat from lord",
                },
            )
        )
    for house in range(1, 13):
        base_sign = (asc_sign + house - 1) % 12
        lord = _lord(chart, base_sign)
        lord_item = next(item for item in chart.planets if item.position.planet == lord)
        value, facts = _arudha(base_sign, lord_item.sign.index)
        points.append(
            SpecialPoint(
                point_id=f"bhava_pada_{house}",
                longitude_degrees=value * 30.0,
                sign_index=value,
                house=house,
                source_facts={**facts, "sign_lord": lord},
            )
        )
    return SpecialPointsResult(
        provenance=chart.provenance,
        convention_version=SPECIAL_CONVENTION,
        points=points,
        validation_status=_status(
            "Arudha exception rules are versioned and require expert review."
        ),
        warnings=["Arudha results identify geometric placements only."],
    )


def calculate_upagrahas(chart: BirthChart, birth: BirthDetails) -> SpecialPointsResult:
    """Calculate versioned geometric upagraha points.

    Gulika and Mandi use the weekday segment indices of the conservative
    daytime/nighttime division convention. The solar upagrahas use the
    traditional fixed offsets from the sidereal Sun. No interpretation is
    attached to any point.
    """
    weekday = birth.date_of_birth.weekday()
    location = LocationDate(
        date=birth.date_of_birth,
        timezone_name=birth.timezone_name,
        latitude=birth.latitude,
        longitude=birth.longitude,
        settings=birth.settings,
    )
    windows = calculate_panchanga(location).windows
    if windows is None or windows.sunrise is None or windows.sunset is None:
        raise ValueError(
            "Sunrise and sunset are unavailable; Gulika and Mandi cannot be calculated"
        )
    birth_utc = chart.provenance.resolved_utc
    day_fraction = (birth_utc - windows.sunrise.instant_utc).total_seconds() / max(
        1.0, (windows.sunset.instant_utc - windows.sunrise.instant_utc).total_seconds()
    )
    day_segment = max(0, min(7, int(day_fraction * 8)))
    gulika_segment = (weekday + 1) % 8
    mandi_segment = (weekday + 2) % 8
    asc = chart.ascendant.longitude.decimal_degrees
    points = [
        SpecialPoint(
            point_id="gulika",
            longitude_degrees=(asc + gulika_segment * 30.0) % 360.0,
            sign_index=_sign(asc + gulika_segment * 30.0),
            house=(gulika_segment % 12) + 1,
            source_facts={
                "weekday": weekday,
                "birth_day_segment": day_segment,
                "segment_index": gulika_segment,
            },
        ),
        SpecialPoint(
            point_id="mandi",
            longitude_degrees=(asc + mandi_segment * 30.0) % 360.0,
            sign_index=_sign(asc + mandi_segment * 30.0),
            house=(mandi_segment % 12) + 1,
            source_facts={
                "weekday": weekday,
                "birth_day_segment": day_segment,
                "segment_index": mandi_segment,
            },
        ),
    ]
    sun = next(
        item for item in chart.planets if item.position.planet == "sun"
    ).position.longitude.decimal_degrees
    offsets = (
        ("dhuma", 133 + 20 / 60),
        ("vyatipata", 226 + 40 / 60),
        ("parivesha", 46 + 40 / 60),
        ("indrachapa", 313 + 20 / 60),
        ("upaketu", 343 + 20 / 60),
    )
    for point_id, offset in offsets:
        value = (sun + offset) % 360.0
        points.append(
            SpecialPoint(
                point_id=point_id,
                longitude_degrees=value,
                sign_index=_sign(value),
                source_facts={"sun_longitude": sun, "offset_degrees": offset},
            )
        )
    return SpecialPointsResult(
        provenance=chart.provenance,
        convention_version="upagraha_gulika_mandi_solar_offsets_v1",
        points=points,
        validation_status=_status("Gulika/Mandi segment tables require expert convention review."),
        warnings=[
            "Regional Gulika and Mandi segment variants are configurable in a future "
            "convention adapter."
        ],
    )


def calculate_lagna_points(chart: BirthChart, birth: BirthDetails) -> SpecialPointsResult:
    location = LocationDate(
        date=birth.date_of_birth,
        timezone_name=birth.timezone_name,
        latitude=birth.latitude,
        longitude=birth.longitude,
        settings=birth.settings,
    )
    windows = calculate_panchanga(location).windows
    if windows is None or windows.sunrise is None:
        raise ValueError("Sunrise is unavailable; Hora, Ghati and Bhava Lagna cannot be calculated")
    birth_utc = chart.provenance.resolved_utc
    elapsed = (birth_utc - windows.sunrise.instant_utc).total_seconds() / 86400.0
    signs = chart.ascendant.sign.index
    points = []
    for point_id, period_days in (
        ("hora_lagna", 1 / 12),
        ("ghati_lagna", 1 / 60),
        ("bhava_lagna", 1 / 24),
    ):
        count = max(0, int(elapsed / period_days))
        sign = (signs + count) % 12
        points.append(
            SpecialPoint(
                point_id=point_id,
                longitude_degrees=sign * 30.0,
                sign_index=sign,
                house=(sign - signs) % 12 + 1,
                source_facts={
                    "sunrise_utc": windows.sunrise.instant_utc.isoformat(),
                    "elapsed_solar_days": elapsed,
                    "period_days": period_days,
                    "completed_periods": count,
                },
            )
        )
    return SpecialPointsResult(
        provenance=chart.provenance,
        convention_version="special_lagnas_solar_day_period_v1",
        points=points,
        validation_status=_status(
            "Solar-day period convention is explicit; local tradition variants remain pending."
        ),
    )


def calculate_chara_karakas(
    chart: BirthChart, include_rahu: bool = True, rahu_reverse: bool = True
) -> CharaKarakaResult:
    names = [
        item.position.planet
        for item in chart.planets
        if item.position.planet in CLASSICAL_KARAKA_PLANETS
        and (include_rahu or item.position.planet != "rahu")
    ]
    values = []
    for name in names:
        item = next(item for item in chart.planets if item.position.planet == name)
        degrees = item.position.longitude.decimal_degrees % 30.0
        if name == "rahu" and rahu_reverse:
            degrees = 30.0 - degrees
        values.append((degrees, name, item.position.longitude.decimal_degrees % 30.0))
    values.sort(reverse=True)
    labels = (
        "atma_karaka",
        "amatya_karaka",
        "bhratri_karaka",
        "matri_karaka",
        "pitri_karaka",
        "putra_karaka",
        "gnati_karaka",
        "dara_karaka",
    )
    facts = [
        CharaKarakaFact(
            karaka=labels[index],
            planet=name,
            degrees_in_sign=raw,
            rank=index + 1,
            source_facts={"ranking_value": ranking, "rahu_reverse": rahu_reverse},
        )
        for index, (ranking, name, raw) in enumerate(values)
    ]
    return CharaKarakaResult(
        provenance=chart.provenance,
        convention_version="chara_karaka_7_or_8_planets_v1",
        karakas=facts,
        validation_status=_status("Rahu inclusion and reverse-degree handling are configurable."),
    )


def calculate_avasthas(chart: BirthChart) -> AvasthaResult:
    facts = []
    for item in chart.planets:
        degree = item.position.longitude.decimal_degrees % 30.0
        index = min(4, int(degree // 6.0))
        bala = ("bala", "kumara", "yuva", "vriddha", "mrityu")[index]
        jagradadi = ("jagrita", "swapna", "sushupti")[int(degree // 10.0) % 3]
        deeptadi = {"exalted": "deepta", "own_sign": "swastha", "debilitated": "duhkha"}.get(
            item.dignity.status, "mishra"
        )
        facts.append(
            AvasthaFact(
                planet=item.position.planet,
                convention_version="avastha_bala_jagradadi_deeptadi_v1",
                bala_avastha=bala,
                jagradadi_avastha=jagradadi,
                deeptadi_avastha=deeptadi,
                source_facts={"degrees_in_sign": degree, "dignity": item.dignity.status},
            )
        )
    return AvasthaResult(
        provenance=chart.provenance,
        avasthas=facts,
        validation_status=_status("Avastha naming and segment conventions require expert review."),
    )


PUSHKARA_BHAGA_DEGREES = (21.0, 14.0, 24.0, 7.0, 21.0, 14.0, 24.0, 7.0, 21.0, 14.0, 24.0, 7.0)
PUSHKARA_NAVAMSHA_SIGNS = {
    0: {4, 8},
    1: {3, 11},
    2: {5, 9},
    3: {1, 7},
    4: {0, 8},
    5: {1, 7},
    6: {2, 6},
    7: {0, 6},
    8: {1, 5},
    9: {2, 10},
    10: {3, 9},
    11: {4, 8},
}


def calculate_varga_classifications(chart: BirthChart) -> VargaClassificationResult:
    """Return explicit Pushkara, Vargottama, and Vaiseshikamsa facts."""
    vargas = {
        division: calculate_varga(chart, division)
        for division in (1, 2, 3, 4, 7, 9, 10, 12, 16, 20, 24, 27, 30, 40, 45, 60)
    }
    results = []
    for item in chart.planets:
        source_sign = item.sign.index
        degree = item.position.longitude.decimal_degrees % 30.0
        d9_sign = next(
            planet.varga_sign.index
            for planet in vargas[9].planets
            if planet.planet == item.position.planet
        )
        pushkara_nav = d9_sign in PUSHKARA_NAVAMSHA_SIGNS[source_sign]
        pushkara_bhaga = abs(degree - PUSHKARA_BHAGA_DEGREES[source_sign]) <= (1.0 / 60.0)
        own_sign_count = sum(
            1
            for division in vargas.values()
            if next(
                planet.varga_sign.lord
                for planet in division.planets
                if planet.planet == item.position.planet
            )
            == item.position.planet
        )
        results.append(
            VargaClassificationFact(
                planet=item.position.planet,
                pushkara_navamsha=pushkara_nav,
                pushkara_bhaga=pushkara_bhaga,
                vargottama=source_sign == d9_sign,
                vaiseshikamsa=own_sign_count >= 10,
                source_facts={
                    "d9_sign": d9_sign,
                    "pushkara_bhaga_degree": PUSHKARA_BHAGA_DEGREES[source_sign],
                    "varga_own_sign_count": own_sign_count,
                    "vaiseshikamsa_threshold": 10,
                },
            )
        )
    return VargaClassificationResult(
        provenance=chart.provenance,
        convention_version="varga_classifications_pushkara_vargottama_vaiseshikamsa_v1",
        classifications=results,
        validation_status=_status(
            "Pushkara table and Vaiseshikamsa threshold are explicit but require "
            "expert source review."
        ),
    )


def calculate_birth_time_sensitivity(
    birth: BirthDetails,
    range_minutes: float = 60.0,
    sample_step_seconds: float = 60.0,
    evaluation_utc: datetime | None = None,
) -> BirthTimeSensitivityResult:
    if range_minutes <= 0 or sample_step_seconds <= 0:
        raise ValueError("range_minutes and sample_step_seconds must be positive")
    if evaluation_utc is not None and evaluation_utc.tzinfo is None:
        raise ValueError("evaluation_utc must be timezone-aware")
    from simplyjyotish_engine.vedic.chart import calculate_birth_chart

    base = birth.local_datetime()
    offsets = []
    value = -range_minutes * 60.0
    while value <= range_minutes * 60.0 + 1e-9:
        offsets.append(value)
        value += sample_step_seconds
    timeline = []
    charts: list[tuple[float, BirthChart]] = []
    for offset in offsets:
        local = base + timedelta(seconds=offset)
        shifted = birth.model_copy(
            update={"date_of_birth": local.date(), "local_time_of_birth": local}
        )
        chart = calculate_birth_chart(shifted)
        d9 = calculate_varga(chart, 9)
        d10 = calculate_varga(chart, 10)
        d60 = calculate_varga(chart, 60)
        from simplyjyotish_engine.dashas.vimshottari import calculate_vimshottari_dasha

        dasha = calculate_vimshottari_dasha(chart)
        first_dasha = dasha.periods[0]
        query_time = evaluation_utc or chart.provenance.resolved_utc
        active_periods = [
            period for period in dasha.periods if period.start <= query_time < period.end
        ]
        active = max(active_periods, key=lambda period: len(period.lord_chain))
        state = {
            "offset_seconds": offset,
            "lagna_sign": chart.ascendant.sign.index,
            "house_signs": tuple(h.sign.index for h in chart.houses),
            "moon_nakshatra_pada": (
                next(
                    item for item in chart.planets if item.position.planet == "moon"
                ).nakshatra.index,
                next(
                    item for item in chart.planets if item.position.planet == "moon"
                ).nakshatra.pada,
            ),
            "navamsha_lagna": d9.ascendant.varga_sign.index,
            "d10_lagna": d10.ascendant.varga_sign.index,
            "d60_lagna": d60.ascendant.varga_sign.index,
            "vimshottari_first_lord": first_dasha.lord,
            "vimshottari_first_end": first_dasha.end.isoformat(),
            "active_vimshottari_chain": active.lord_chain,
            "active_vimshottari_start": active.start.isoformat(),
            "active_vimshottari_end": active.end.isoformat(),
            "sensitive_boundaries": {"ascendant_degree": chart.ascendant.longitude.decimal_degrees},
        }
        timeline.append(state)
        charts.append((offset, chart))
    changes: list[SensitivityChange] = []
    keys = (
        "lagna_sign",
        "house_signs",
        "moon_nakshatra_pada",
        "navamsha_lagna",
        "d10_lagna",
        "d60_lagna",
        "vimshottari_first_lord",
        "vimshottari_first_end",
        "active_vimshottari_chain",
        "active_vimshottari_start",
        "active_vimshottari_end",
    )
    for key in keys:
        previous = timeline[0][key]
        for state in timeline[1:]:
            if state[key] != previous:
                changes.append(
                    SensitivityChange(
                        feature=key,
                        first_changed_offset_seconds=cast(float, state["offset_seconds"]),
                        before_value=previous,
                        after_value=state[key],
                        details={
                            "sampled": True,
                            "refinement": "not_applicable_for_discrete_boundary",
                        },
                    )
                )
                break
            previous = state[key]
    return BirthTimeSensitivityResult(
        provenance=charts[len(charts) // 2][1].provenance,
        convention_version="birth_time_sensitivity_discrete_sampling_v1",
        range_start_offset_seconds=-range_minutes * 60.0,
        range_end_offset_seconds=range_minutes * 60.0,
        sample_step_seconds=sample_step_seconds,
        changes=changes,
        sampled_timeline=timeline,
        confidence_warnings=[
            "This is sensitivity analysis, not rectification or prediction.",
            "Dasha changes use the configured evaluation UTC instant; no outcome or "
            "rectification is inferred.",
        ],
        validation_status=_status(
            "Boundary changes are sampled deterministically; event-time refinement is not claimed."
        ),
    )
