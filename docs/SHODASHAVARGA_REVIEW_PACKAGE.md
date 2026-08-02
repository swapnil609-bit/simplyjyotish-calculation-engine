# Shodashavarga review package

Package version: `parashara_bphs_chapter_6_v1`  
Scope: calculation rules only; no interpretations, predictions, or remedies.

## Selected convention

The engine uses the BPHS Chapter 6 Parashari Shodashavarga baseline: D1, D2,
D3, D4, D7, D9, D10, D12, D16, D20, D24, D27, D30, D40, D45, and D60. The
source-verses and plain-language formulas are in [VARGA_CONVENTIONS.md](VARGA_CONVENTIONS.md).

## Source and comparison basis

- Primary source: *Brihat Parashara Hora Shastra*, Chapter 6, verses 2-41;
  the implemented verse ranges are emitted in every `DivisionalChart` result.
- Independent comparison oracle: PyJHora 4.8.7, configured to its named
  traditional Parashari method and Lahiri setting. It is AGPL-3.0 and is never
  copied into the engine.
- Future manual oracle: Jagannatha Hora 8.0 with Lahiri ayanamsa.

## Boundary policy

All normal vargas use start-inclusive, end-exclusive Decimal intervals. D30
uses its five unequal BPHS segments with the same policy. Tests cover every
source sign and each boundary at epsilon below, exact, and epsilon above.

## Evidence

[varga_pyjhora_4_8_7.json](../tests/fixtures/varga_pyjhora_4_8_7.json)
contains 25 fixed non-boundary comparison cases per varga. Each group records
the pinned oracle method; the shared metadata records source, version, licence,
ayanamsa, node type, scheme ID, inputs, and expected sign. The cases represent
Lagna plus all nine Vedic grahas. The automated suite adds all-sign and
all-boundary coverage.

## D60 review detail

D60 exposes two intentionally separate values:

1. `varga_sign`: determined from the within-sign half-degree part, independent
   of the source sign.
2. `amsha_name`: forward through the list below for odd signs and reverse for
   even signs.

The source-transcribed D60 names are: Ghora, Rakshasa, Deva, Kubera, Yaksha,
Kindara, Bhrashta, Kulaghna, Garala, Vahni, Maya, Purishaka, Apampati,
Marutvan, Kala, Sarpa, Amrita, Indu, Mridu, Komala, Heramba, Brahma, Vishnu,
Maheshwara, Deva, Ardra, Kalinasa, Kshiteesha, Kamalakara, Gulika, Mrityu,
Kala, Davagni, Ghora, Yama, Kantaka, Shuddha, Amrita, Purnachandra,
Vishadagdha, Kulanas, Vamshakshaya, Utpata, Kala, Saumya, Komala, Sheetala,
Karaladamshtra, Chandramukhi, Praveena, Kalapavaka, Dhanayudha, Nirmala,
Saumya, Krura, Atisheeta, Amrita, Payodhi, Brahmana, and Chandrarekha.

No deity, auspiciousness, or interpretation attribute is emitted unless it is
separately transcribed, cited, and validated.

## Recorded discrepancy

PyJHora 4.8.7's D30 implementation uses inclusive upper comparisons. At an
exact segment edge, it can retain the preceding segment; this engine assigns
the edge to the next segment under its global start-inclusive/end-exclusive
contract. Non-boundary comparison fixtures agree. This is an explicit policy
difference, not a hidden mismatch.

## Review status and unresolved questions

All sixteen divisions are source-verified, cross-implementation-verified, and
fully tested. `expert_reviewed` is false for all outputs because no practicing
Parashari Jyotishi has yet reviewed this package. No source contradiction
requires a second default scheme at present. A future reviewer should confirm
the selected BPHS edition/transliteration and the D30 boundary policy.
