# Varga validation and convention register

Vargas are not a single universal algorithm. The engine will only mark a
division complete after it has an explicit mapping, a source reference,
boundary tests, and a documented selected convention.

## Implemented baseline

| Varga | Current convention | Validation status |
|---|---|---|
| D1 Rashi | Sign placement | implemented and tested |
| D9 Navamsha | Movable/self, fixed/9th, dual/5th start mapping | implemented and tested; expert regression sign-off still useful |
| D10 Dashamsha | Odd/self, even/9th start mapping | implemented and tested; expert regression sign-off still useful |
| D60 Shashtiamsha | Forward count for odd signs, reverse for even signs | implemented and tested; expert sign-off required before a stable public release |

## Requires a selected tradition before implementation

| Varga family | Why expert convention is needed |
|---|---|
| D2 Hora | Parashara and alternate Hora conventions differ, especially sign handling. |
| D3 Drekkana, D4 Chaturthamsa, D5 Panchamsa, D6 Shashtamsa, D7 Saptamsa, D8 Ashtamsa | Start-sign/counting rules vary by text and school. |
| D11, D16, D20, D24, D27 | Published mappings and deity/sign tables vary; a source edition must be selected. |
| D30 Trimshamsha | Unequal divisions and gender/sign rules are convention-sensitive. |
| D40 Khavedamsha, D45 Akshavedamsha | Odd/even and directional conventions vary. |
| D60 names and interpretations | The sign-placement convention is implemented, but the 60 named amshas and any attributes need an authoritative source table. |
| General D1-D60 framework | Only divisions with a source-backed mapping will be exposed; no fabricated generic mapping. |

## Expert sign-off package

For each new varga, provide or approve:

1. The primary source edition or school (for example, a specified Parashara
   translation and commentator).
2. The exact start-sign and counting-direction rule, including odd/even,
   movable/fixed/dual, gender, or deity exceptions.
3. At least 10 trusted longitude-to-varga-sign regression cases, including
   exact and near-boundary longitudes.
4. Whether named amshas, lords, or only sign placement are required.

The engine team can implement, test, document, and version these decisions end
to end. An astrologer is only needed to choose or approve the tradition where
classical authorities legitimately differ.
