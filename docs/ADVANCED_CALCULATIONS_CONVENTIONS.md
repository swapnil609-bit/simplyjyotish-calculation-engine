# Advanced calculation conventions

## Relationships and aspects

`parashari_graha_drishti_v1` gives every configured graha the seventh-sign
aspect and adds Mars 4th/8th, Jupiter 5th/9th, and Saturn 3rd/10th aspects.
`jaimini_rashi_drishti_v1` is separate: movable signs aspect non-adjacent
fixed signs, fixed signs aspect non-adjacent movable signs, and dual signs
aspect other dual signs. Conjunctions use an explicit configurable longitude
orb. Dispositorship follows sign lords until a cycle. Graha Yuddha candidates
use one degree of longitude separation and absolute latitude as the documented
tiebreak; ties remain unresolved. Papakartari reports natural-malefic
occupation of both adjacent houses.

## Shadbala

`parashara_shadbala_v1` returns six component records: Sthana, Dig, Kala,
Cheshta, Naisargika, and Drik Bala, plus Bhava Bala, Ishta/Kashta, and
Vimsopaka fields. The implementation is deterministic and typed; detailed
traditional tabulation review remains pending. No strength value is converted
to interpretation.

## Ashtakavarga

`ashtakavarga_parashari_pinned_oracle_v1` returns Bhinna, Prastara,
Sarvashtakavarga, Trikona Shodhana, Ekadhipatya Shodhana, and Shodhya Pinda.
The fixed benefic-house tables and reduction rules are aligned to the pinned
PyJHora comparison implementation; expert review remains pending.

## Extended Vargas

D5, D6, D8, and D11 require explicit method identifiers and are never selected
by the `parashara_bphs_chapter_6_v1` default. Current identifiers are:

- `panchamsha_parashari_alt_v1`
- `shashtamsha_parashari_alt_v1`
- `ashtamsha_parashari_alt_v1`
- `ekadashamsha_parashari_alt_v1`

These are deliberately marked source-unverified and expert-review pending.
