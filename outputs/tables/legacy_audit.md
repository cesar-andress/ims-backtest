# Legacy IMSFE audit report

Generated from the original Excel (read-only). Numbers below are computed
from the data; manuscript-only issues are marked **MANUAL CHECK**.

## 1. Identical raw values across countries

| Variable | Value | Countries | ISO3 |
|---|---:|---|---|
| INTC | 2192.67 | Austria, Belgium, Italy, Switzerland | AUT, BEL, CHE, ITA |
| INTC | 2242.5 | Denmark, Germany | DEU, DNK |
| INTC | 2441.83 | Romania, Slovakia | ROU, SVK |
| INTC | 3488.33 | Australia, China, Japan, Singapore, South Korea, Viet Nam | AUS, CHN, JPN, KOR, SGP, VNM |
| CIBC | 0.1 | Austria, Belgium, Czech Republic, Denmark, France, Germany, Italy, Netherlands, Poland, Portugal, Romania, Russia, Slovakia, Spain, Sweden, United Kingdom | AUT, BEL, CZE, DEU, DNK, ESP, FRA, GBR, ITA, NLD, POL, PRT, ROU, RUS, SVK, SWE |
| LPIN | 3.3 | Czech Republic, Slovakia, Viet Nam | CZE, SVK, VNM |
| LPIN | 3.4 | Portugal, Saudi Arabia, Turkey | PRT, SAU, TUR |
| LPIN | 3.7 | Australia, China, Italy, United Kingdom | AUS, CHN, GBR, ITA |
| LPIN | 3.8 | South Korea, United States | KOR, USA |
| LPIN | 3.9 | France, Japan, Spain | ESP, FRA, JPN |
| LPIN | 4 | Austria, Belgium, Canada, Sweden, United Arab Emirates | ARE, AUT, BEL, CAN, SWE |
| LPIN | 4.1 | Denmark, Germany, Netherlands, Switzerland | CHE, DEU, DNK, NLD |
| CPTR | 9375992 | Australia, Austria | AUS, AUT |
| ITTT | 18 | Belgium, China, France, Netherlands, Spain | BEL, CHN, ESP, FRA, NLD |
| ITTT | 20 | Denmark, Italy, Sweden | DNK, ITA, SWE |
| ITTT | 21 | Austria, Czech Republic, Poland, Slovakia, Switzerland | AUT, CHE, CZE, POL, SVK |
| CUTA | 0.1 | Singapore, Switzerland | CHE, SGP |
| CUTA | 5 | Australia, Saudi Arabia, United Arab Emirates | ARE, AUS, SAU |
| CUTA | 10 | China, Mexico, Panama | CHN, MEX, PAN |
| CUTA | 16 | Japan, United Kingdom | GBR, JPN |
| CUTA | 17 | Austria, Belgium, Czech Republic, Denmark, France, Germany, Italy, Netherlands, Poland, Portugal, Romania, Slovakia, Spain, Sweden | AUT, BEL, CZE, DEU, DNK, ESP, FRA, ITA, NLD, POL, PRT, ROU, SVK, SWE |
| IOEF | 64.4 | France, Saudi Arabia | FRA, SAU |
| IOEF | 70.2 | Japan, United States | JPN, USA |
| IOEF | 71.6 | Germany, United Arab Emirates | ARE, DEU |
| CLI | 56.5 | Belgium, South Korea | BEL, KOR |
| INRI | 1.9 | Czech Republic, Portugal | CZE, PRT |
| INRI | 2.1 | Japan, South Korea, Sweden, United Arab Emirates, United Kingdom | ARE, GBR, JPN, KOR, SWE |
| INRI | 2.4 | Austria, Saudi Arabia | AUT, SAU |
| INRI | 2.5 | Australia, Netherlands, Poland | AUS, NLD, POL |
| INRI | 2.6 | Belgium, Germany, Spain | BEL, DEU, ESP |
| INRI | 2.7 | Canada, France | CAN, FRA |
| INRI | 3 | China, Italy | CHN, ITA |
| DEIN | 8.08 | Czech Republic, Portugal | CZE, PRT |
| CPIN | 56 | Czech Republic, Spain | CZE, ESP |
| CPIN | 67 | Austria, France | AUT, FRA |
| CPIN | 71 | Japan, United Kingdom | GBR, JPN |
| CPIN | 75 | Canada, Germany | CAN, DEU |
| CUDI | 3 | Turkey, United States | TUR, USA |
| CUDI | 9 | China, Czech Republic, Romania | CHN, CZE, ROU |
| CUDI | 12 | Italy, United Kingdom | GBR, ITA |
| CUDI | 21 | Australia, Poland | AUS, POL |
| CUDI | 57 | Mexico, United Arab Emirates | ARE, MEX |

Expected finding: **CPTR Austria == Australia == 9375992**.

## 2. Ratio normalisation near-binary collapse

For cost variables with a near-zero minimum, `min/y*10` leaves most
countries near 0 and only the minimum near 10.

| Variable | Direction | Min | Max | Share norm < 1 | Collapses |
|---|---|---:|---:|---:|:---:|
| PPAD | benefit | 30 | 141.37 | 0.00 | no |
| INTC | cost | 697.67 | 3488.33 | 0.00 | no |
| CIBC | cost | 0.1 | 553.333 | 0.47 | yes |
| LPIN | benefit | 2.6 | 4.3 | 0.00 | no |
| CPTR | benefit | 114075 | 2.6899e+08 | 0.87 | yes |
| ITTT | cost | 1 | 44 | 0.87 | no |
| CUTA | cost | 0.1 | 47 | 0.90 | yes |
| CCTI | cost | 31 | 11363 | 0.87 | yes |
| IOEF | benefit | 49 | 84.1 | 0.00 | no |
| CLI | benefit | 22.3 | 98.4 | 0.00 | no |
| INAN | cost | 0.582394 | 68.2339 | 0.47 | yes |
| UNRA | cost | 1.645 | 12.179 | 0.00 | no |
| FSIN | cost | 15.9 | 84 | 0.00 | no |
| INRI | cost | 0.6 | 5.5 | 0.00 | no |
| DEIN | benefit | 2.03 | 9.39 | 0.00 | no |
| GLIN | benefit | 64.61 | 89.72 | 0.00 | no |
| CPIN | benefit | 22 | 90 | 0.00 | no |
| CUDI | cost | 2 | 116 | 0.50 | no |

Variables flagged as collapsing: CIBC, CPTR, CUTA, CCTI, INAN.
Expected: CUTA, CIBC, CCTI, CPTR, INAN.

## 3. Per-variable contribution to Switzerland and Singapore

### Switzerland (`CHE`), IMSFE = 6.1192

| Variable | Contribution | Excess vs mean |
|---|---:|---:|
| CUTA | 0.9472 | +0.8742 |
| PPAD | 0.9232 | +0.3010 |
| CLI | 0.5212 | +0.2528 |
| FSIN | 0.4404 | +0.2125 |
| INAN | 0.3025 | +0.2018 |
| DEIN | 0.3676 | +0.0960 |
| CPIN | 0.3551 | +0.0906 |
| IOEF | 0.4938 | +0.0860 |
| LPIN | 0.7044 | +0.0727 |
| GLIN | 0.3611 | +0.0390 |
| INRI | 0.1626 | +0.0349 |
| UNRA | 0.1954 | -0.0067 |
| CCTI | 0.0277 | -0.0117 |
| INTC | 0.2391 | -0.0118 |
| ITTT | 0.0296 | -0.0232 |
| CUDI | 0.0477 | -0.0363 |
| CPTR | 0.0002 | -0.0376 |
| CIBC | 0.0004 | -0.2516 |

### Singapore (`SGP`), IMSFE = 5.8123

| Variable | Contribution | Excess vs mean |
|---|---:|---:|
| CUTA | 0.9472 | +0.8742 |
| INRI | 0.4879 | +0.3602 |
| PPAD | 0.7837 | +0.1614 |
| CLI | 0.4190 | +0.1505 |
| LPIN | 0.7388 | +0.1071 |
| CPIN | 0.3683 | +0.1038 |
| IOEF | 0.4961 | +0.0884 |
| CCTI | 0.1276 | +0.0882 |
| FSIN | 0.2809 | +0.0530 |
| CPTR | 0.0674 | +0.0297 |
| UNRA | 0.2294 | +0.0273 |
| GLIN | 0.3346 | +0.0125 |
| INAN | 0.1008 | +0.0002 |
| DEIN | 0.2437 | -0.0278 |
| ITTT | 0.0141 | -0.0387 |
| CUDI | 0.0222 | -0.0618 |
| INTC | 0.1503 | -0.1006 |
| CIBC | 0.0002 | -0.2518 |

## 4. Manuscript-only issues (MANUAL CHECK)

- **MANUAL CHECK — Table 8 row misalignment:** several manuscript rows
  appear to show another country's normalised values / unified scores
  (e.g. Vietnam/Switzerland, Poland/Denmark, Korea/Panama,
  Mexico/France, Japan/USA). Verify against `outputs/tables/legacy_comparison.csv`
  and the Excel sheet `3. Standardization of criteria`.
- **MANUAL CHECK — Table 7 Argentina vs Australia:** the manuscript Table 7
  lists Argentina, which is not among the 30 pre-selected markets in the
  Excel; Australia is present in the Excel pre-selection but may be missing
  from the manuscript table.

## 5. Ranking snapshot (ratio_legacy)

| Rank | ISO3 | Country | IMSFE |
|---:|---|---|---:|
| 1 | CHE | Switzerland | 6.1192 |
| 2 | SGP | Singapore | 5.8123 |
| 3 | DNK | Denmark | 5.0986 |
| 4 | NLD | Netherlands | 4.8455 |
| 5 | CAN | Canada | 4.8042 |
| 6 | DEU | Germany | 4.7430 |
| 7 | SWE | Sweden | 4.6327 |
| 8 | PAN | Panama | 4.6277 |
| 9 | AUT | Austria | 4.5776 |
| 10 | PRT | Portugal | 4.5743 |
| 11 | BEL | Belgium | 4.4581 |
| 12 | USA | United States | 4.4176 |
| 13 | FRA | France | 4.3945 |
| 14 | CZE | Czech Republic | 4.2508 |
| 15 | ARE | United Arab Emirates | 4.1671 |
| 16 | GBR | United Kingdom | 4.1607 |
| 17 | KOR | South Korea | 4.1535 |
| 18 | ITA | Italy | 4.1226 |
| 19 | AUS | Australia | 4.0803 |
| 20 | ESP | Spain | 4.0480 |
| 21 | POL | Poland | 4.0152 |
| 22 | JPN | Japan | 3.9175 |
| 23 | SVK | Slovakia | 3.8018 |
| 24 | CHN | China | 3.6762 |
| 25 | ROU | Romania | 3.6073 |
| 26 | MEX | Mexico | 3.5610 |
| 27 | TUR | Turkey | 3.1659 |
| 28 | RUS | Russia | 3.1614 |
| 29 | SAU | Saudi Arabia | 3.1365 |
| 30 | VNM | Viet Nam | 2.9586 |
