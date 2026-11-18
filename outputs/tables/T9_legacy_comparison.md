# T9. Legacy IMSFE ranking: original ratio vs corrected normalisations

| iso3   | country              |   score_ratio_legacy |   rank_ratio_legacy |   score_minmax |   rank_minmax |   score_rank |   rank_rank |   score_minmax_pref_tariff |   rank_minmax_pref_tariff |
|:-------|:---------------------|---------------------:|--------------------:|---------------:|--------------:|-------------:|------------:|---------------------------:|--------------------------:|
| CHE    | Switzerland          |                6.119 |                   1 |          8.241 |             1 |        7.913 |           1 |                      8.241 |                         1 |
| SGP    | Singapore            |                5.812 |                   2 |          7.078 |             5 |        7.14  |           2 |                      7.078 |                         8 |
| DNK    | Denmark              |                5.099 |                   3 |          7.355 |             2 |        6.947 |           3 |                      7.696 |                         2 |
| NLD    | Netherlands          |                4.846 |                   4 |          7.267 |             3 |        6.885 |           4 |                      7.608 |                         3 |
| CAN    | Canada               |                4.804 |                   5 |          7.148 |             4 |        6.207 |           6 |                      7.55  |                         4 |
| DEU    | Germany              |                4.743 |                   6 |          6.988 |             6 |        6.399 |           5 |                      7.33  |                         5 |
| SWE    | Sweden               |                4.633 |                   7 |          6.841 |             8 |        5.947 |           9 |                      7.182 |                         7 |
| PAN    | Panama               |                4.628 |                   8 |          5.316 |            23 |        4.605 |          21 |                      5.285 |                        23 |
| AUT    | Austria              |                4.578 |                   9 |          6.871 |             7 |        6.059 |           7 |                      7.212 |                         6 |
| PRT    | Portugal             |                4.574 |                  10 |          6.34  |            11 |        5.358 |          15 |                      6.681 |                        12 |
| BEL    | Belgium              |                4.458 |                  11 |          6.567 |             9 |        5.936 |          10 |                      6.908 |                         9 |
| USA    | United States        |                4.418 |                  12 |          6.007 |            17 |        5.771 |          11 |                      6.762 |                        11 |
| FRA    | France               |                4.394 |                  13 |          6.481 |            10 |        5.465 |          14 |                      6.823 |                        10 |
| CZE    | Czech Republic       |                4.251 |                  14 |          6.229 |            12 |        4.996 |          19 |                      6.571 |                        13 |
| ARE    | United Arab Emirates |                4.167 |                  15 |          5.59  |            20 |        5.695 |          12 |                      5.568 |                        21 |
| GBR    | United Kingdom       |                4.161 |                  16 |          6.129 |            14 |        5.27  |          16 |                      6.45  |                        14 |
| KOR    | South Korea          |                4.154 |                  17 |          6.213 |            13 |        6.049 |           8 |                      6.373 |                        16 |
| ITA    | Italy                |                4.123 |                  18 |          6.039 |            16 |        4.693 |          20 |                      6.38  |                        15 |
| AUS    | Australia            |                4.08  |                  19 |          6.1   |            15 |        5.541 |          13 |                      6.112 |                        19 |
| ESP    | Spain                |                4.048 |                  20 |          5.985 |            18 |        5.088 |          18 |                      6.326 |                        17 |
| POL    | Poland               |                4.015 |                  21 |          5.917 |            19 |        4.017 |          23 |                      6.258 |                        18 |
| JPN    | Japan                |                3.918 |                  22 |          5.451 |            22 |        5.221 |          17 |                      5.056 |                        24 |
| SVK    | Slovakia             |                3.802 |                  23 |          5.533 |            21 |        3.586 |          26 |                      5.874 |                        20 |
| CHN    | China                |                3.676 |                  24 |          4.58  |            27 |        3.845 |          25 |                      4.555 |                        27 |
| ROU    | Romania              |                3.607 |                  25 |          5.227 |            24 |        3.194 |          27 |                      5.568 |                        22 |
| MEX    | Mexico               |                3.561 |                  26 |          4.983 |            25 |        4.184 |          22 |                      4.989 |                        25 |
| TUR    | Turkey               |                3.166 |                  27 |          3.404 |            29 |        3.025 |          29 |                      3.404 |                        29 |
| RUS    | Russia               |                3.161 |                  28 |          4.239 |            28 |        3.18  |          28 |                      4.141 |                        28 |
| SAU    | Saudi Arabia         |                3.137 |                  29 |          4.667 |            26 |        3.98  |          24 |                      4.595 |                        26 |
| VNM    | Viet Nam             |                2.959 |                  30 |          3.269 |            30 |        2.807 |          30 |                      3.188 |                        30 |

## Booktabs (copy into manuscript; not a repo .tex file)

```latex
\begin{table}[htbp]
\centering
\caption{T9. Legacy IMSFE ranking: original ratio vs corrected normalisations}
\label{tab:T9_legacy_comparison}
\begin{tabular}{llllllllll}
\toprule
iso3 & country & score\_ratio\_legacy & rank\_ratio\_legacy & score\_minmax & rank\_minmax & score\_rank & rank\_rank & score\_minmax\_pref\_tariff & rank\_minmax\_pref\_tariff \\
\midrule
CHE & Switzerland & 6.119 & 1 & 8.241 & 1 & 7.913 & 1 & 8.241 & 1 \\
SGP & Singapore & 5.812 & 2 & 7.078 & 5 & 7.140 & 2 & 7.078 & 8 \\
DNK & Denmark & 5.099 & 3 & 7.355 & 2 & 6.947 & 3 & 7.696 & 2 \\
NLD & Netherlands & 4.846 & 4 & 7.267 & 3 & 6.885 & 4 & 7.608 & 3 \\
CAN & Canada & 4.804 & 5 & 7.148 & 4 & 6.207 & 6 & 7.550 & 4 \\
DEU & Germany & 4.743 & 6 & 6.988 & 6 & 6.399 & 5 & 7.330 & 5 \\
SWE & Sweden & 4.633 & 7 & 6.841 & 8 & 5.947 & 9 & 7.182 & 7 \\
PAN & Panama & 4.628 & 8 & 5.316 & 23 & 4.605 & 21 & 5.285 & 23 \\
AUT & Austria & 4.578 & 9 & 6.871 & 7 & 6.059 & 7 & 7.212 & 6 \\
PRT & Portugal & 4.574 & 10 & 6.340 & 11 & 5.358 & 15 & 6.681 & 12 \\
BEL & Belgium & 4.458 & 11 & 6.567 & 9 & 5.936 & 10 & 6.908 & 9 \\
USA & United States & 4.418 & 12 & 6.007 & 17 & 5.771 & 11 & 6.762 & 11 \\
FRA & France & 4.394 & 13 & 6.481 & 10 & 5.465 & 14 & 6.823 & 10 \\
CZE & Czech Republic & 4.251 & 14 & 6.229 & 12 & 4.996 & 19 & 6.571 & 13 \\
ARE & United Arab Emirates & 4.167 & 15 & 5.590 & 20 & 5.695 & 12 & 5.568 & 21 \\
GBR & United Kingdom & 4.161 & 16 & 6.129 & 14 & 5.270 & 16 & 6.450 & 14 \\
KOR & South Korea & 4.154 & 17 & 6.213 & 13 & 6.049 & 8 & 6.373 & 16 \\
ITA & Italy & 4.123 & 18 & 6.039 & 16 & 4.693 & 20 & 6.380 & 15 \\
AUS & Australia & 4.080 & 19 & 6.100 & 15 & 5.541 & 13 & 6.112 & 19 \\
ESP & Spain & 4.048 & 20 & 5.985 & 18 & 5.088 & 18 & 6.326 & 17 \\
POL & Poland & 4.015 & 21 & 5.917 & 19 & 4.017 & 23 & 6.258 & 18 \\
JPN & Japan & 3.918 & 22 & 5.451 & 22 & 5.221 & 17 & 5.056 & 24 \\
SVK & Slovakia & 3.802 & 23 & 5.533 & 21 & 3.586 & 26 & 5.874 & 20 \\
CHN & China & 3.676 & 24 & 4.580 & 27 & 3.845 & 25 & 4.555 & 27 \\
ROU & Romania & 3.607 & 25 & 5.227 & 24 & 3.194 & 27 & 5.568 & 22 \\
MEX & Mexico & 3.561 & 26 & 4.983 & 25 & 4.184 & 22 & 4.989 & 25 \\
TUR & Turkey & 3.166 & 27 & 3.404 & 29 & 3.025 & 29 & 3.404 & 29 \\
RUS & Russia & 3.161 & 28 & 4.239 & 28 & 3.180 & 28 & 4.141 & 28 \\
SAU & Saudi Arabia & 3.137 & 29 & 4.667 & 26 & 3.980 & 24 & 4.595 & 26 \\
VNM & Viet Nam & 2.959 & 30 & 3.269 & 30 & 2.807 & 30 & 3.188 & 30 \\
\bottomrule
\end{tabular}
\end{table}
```
