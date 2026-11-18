# T4d. Paired bootstrap lift vs import_volume / gravity / random

| contrast                                        | method                          | baseline      | metric   | target      |   horizon |   delta_mean |   ci95_low |   ci95_high |   n_blocks |
|:------------------------------------------------|:--------------------------------|:--------------|:---------|:------------|----------:|-------------:|-----------:|------------:|-----------:|
| eoc - import_volume                             | eoc                             | import_volume | ndcg@10  | intensive   |         1 |      -0.0434 |    -0.0809 |     -0.0042 |         28 |
| eoc - gravity_ppml                              | eoc                             | gravity_ppml  | ndcg@10  | intensive   |         1 |      -0.0528 |    -0.0949 |     -0.0069 |         28 |
| eoc - random                                    | eoc                             | random        | ndcg@10  | intensive   |         1 |      -0.0161 |    -0.0477 |      0.0163 |         28 |
| equal_weights - import_volume                   | equal_weights                   | import_volume | ndcg@10  | intensive   |         1 |       0.0923 |     0.0419 |      0.1451 |         28 |
| equal_weights - gravity_ppml                    | equal_weights                   | gravity_ppml  | ndcg@10  | intensive   |         1 |       0.0829 |     0.0433 |      0.1203 |         28 |
| equal_weights - random                          | equal_weights                   | random        | ndcg@10  | intensive   |         1 |       0.1196 |     0.0752 |      0.1638 |         28 |
| promethee_ii|minmax|expert_mean - import_volume | promethee_ii|minmax|expert_mean | import_volume | ndcg@10  | intensive   |         1 |       0.0919 |     0.0475 |      0.1445 |         28 |
| promethee_ii|minmax|expert_mean - gravity_ppml  | promethee_ii|minmax|expert_mean | gravity_ppml  | ndcg@10  | intensive   |         1 |       0.0825 |     0.0433 |      0.1239 |         28 |
| promethee_ii|minmax|expert_mean - random        | promethee_ii|minmax|expert_mean | random        | ndcg@10  | intensive   |         1 |       0.1191 |     0.0761 |      0.1619 |         28 |
| topsis|minmax|expert_mean - import_volume       | topsis|minmax|expert_mean       | import_volume | ndcg@10  | intensive   |         1 |       0.1014 |     0.0525 |      0.1552 |         28 |
| topsis|minmax|expert_mean - gravity_ppml        | topsis|minmax|expert_mean       | gravity_ppml  | ndcg@10  | intensive   |         1 |       0.092  |     0.0491 |      0.1361 |         28 |
| topsis|minmax|expert_mean - random              | topsis|minmax|expert_mean       | random        | ndcg@10  | intensive   |         1 |       0.1287 |     0.084  |      0.1722 |         28 |
| vikor|minmax|expert_mean - import_volume        | vikor|minmax|expert_mean        | import_volume | ndcg@10  | intensive   |         1 |       0.0965 |     0.047  |      0.148  |         28 |
| vikor|minmax|expert_mean - gravity_ppml         | vikor|minmax|expert_mean        | gravity_ppml  | ndcg@10  | intensive   |         1 |       0.0871 |     0.0457 |      0.1295 |         28 |
| vikor|minmax|expert_mean - random               | vikor|minmax|expert_mean        | random        | ndcg@10  | intensive   |         1 |       0.1238 |     0.0782 |      0.1691 |         28 |
| wsm|minmax|equal - import_volume                | wsm|minmax|equal                | import_volume | ndcg@10  | intensive   |         1 |       0.0923 |     0.0444 |      0.142  |         28 |
| wsm|minmax|equal - gravity_ppml                 | wsm|minmax|equal                | gravity_ppml  | ndcg@10  | intensive   |         1 |       0.0829 |     0.0458 |      0.1215 |         28 |
| wsm|minmax|equal - random                       | wsm|minmax|equal                | random        | ndcg@10  | intensive   |         1 |       0.1196 |     0.0745 |      0.1636 |         28 |
| wsm|minmax|expert_mean - import_volume          | wsm|minmax|expert_mean          | import_volume | ndcg@10  | intensive   |         1 |       0.0882 |     0.0422 |      0.1386 |         28 |
| wsm|minmax|expert_mean - gravity_ppml           | wsm|minmax|expert_mean          | gravity_ppml  | ndcg@10  | intensive   |         1 |       0.0789 |     0.0405 |      0.116  |         28 |
| wsm|minmax|expert_mean - random                 | wsm|minmax|expert_mean          | random        | ndcg@10  | intensive   |         1 |       0.1155 |     0.0712 |      0.1581 |         28 |
| wsm|minmax|learned - import_volume              | wsm|minmax|learned              | import_volume | ndcg@10  | intensive   |         1 |       0.0966 |     0.0443 |      0.1509 |         28 |
| wsm|minmax|learned - gravity_ppml               | wsm|minmax|learned              | gravity_ppml  | ndcg@10  | intensive   |         1 |       0.0872 |     0.045  |      0.1295 |         28 |
| wsm|minmax|learned - random                     | wsm|minmax|learned              | random        | ndcg@10  | intensive   |         1 |       0.1238 |     0.0753 |      0.1734 |         28 |
| eoc - import_volume                             | eoc                             | import_volume | ndcg@10  | new_markets |         1 |      -0.0462 |    -0.0878 |     -0.0049 |         25 |
| eoc - gravity_ppml                              | eoc                             | gravity_ppml  | ndcg@10  | new_markets |         1 |      -0.0064 |    -0.0626 |      0.0511 |         25 |
| eoc - random                                    | eoc                             | random        | ndcg@10  | new_markets |         1 |       0.0931 |     0.06   |      0.1286 |         25 |
| equal_weights - import_volume                   | equal_weights                   | import_volume | ndcg@10  | new_markets |         1 |       0.1617 |     0.1132 |      0.2129 |         21 |
| equal_weights - gravity_ppml                    | equal_weights                   | gravity_ppml  | ndcg@10  | new_markets |         1 |       0.1941 |     0.136  |      0.2527 |         21 |
| equal_weights - random                          | equal_weights                   | random        | ndcg@10  | new_markets |         1 |       0.2956 |     0.262  |      0.3304 |         21 |
| promethee_ii|minmax|expert_mean - import_volume | promethee_ii|minmax|expert_mean | import_volume | ndcg@10  | new_markets |         1 |       0.1592 |     0.11   |      0.2054 |         21 |
| promethee_ii|minmax|expert_mean - gravity_ppml  | promethee_ii|minmax|expert_mean | gravity_ppml  | ndcg@10  | new_markets |         1 |       0.1915 |     0.128  |      0.2587 |         21 |
| promethee_ii|minmax|expert_mean - random        | promethee_ii|minmax|expert_mean | random        | ndcg@10  | new_markets |         1 |       0.2931 |     0.258  |      0.3283 |         21 |
| topsis|minmax|expert_mean - import_volume       | topsis|minmax|expert_mean       | import_volume | ndcg@10  | new_markets |         1 |       0.1538 |     0.1002 |      0.2047 |         21 |
| topsis|minmax|expert_mean - gravity_ppml        | topsis|minmax|expert_mean       | gravity_ppml  | ndcg@10  | new_markets |         1 |       0.1862 |     0.1255 |      0.2473 |         21 |
| topsis|minmax|expert_mean - random              | topsis|minmax|expert_mean       | random        | ndcg@10  | new_markets |         1 |       0.2877 |     0.2512 |      0.3249 |         21 |
| vikor|minmax|expert_mean - import_volume        | vikor|minmax|expert_mean        | import_volume | ndcg@10  | new_markets |         1 |       0.1704 |     0.1189 |      0.2222 |         21 |
| vikor|minmax|expert_mean - gravity_ppml         | vikor|minmax|expert_mean        | gravity_ppml  | ndcg@10  | new_markets |         1 |       0.2027 |     0.1444 |      0.2603 |         21 |
| vikor|minmax|expert_mean - random               | vikor|minmax|expert_mean        | random        | ndcg@10  | new_markets |         1 |       0.3043 |     0.2682 |      0.3389 |         21 |
| wsm|minmax|equal - import_volume                | wsm|minmax|equal                | import_volume | ndcg@10  | new_markets |         1 |       0.1617 |     0.1112 |      0.2144 |         21 |
| wsm|minmax|equal - gravity_ppml                 | wsm|minmax|equal                | gravity_ppml  | ndcg@10  | new_markets |         1 |       0.1941 |     0.1377 |      0.2526 |         21 |
| wsm|minmax|equal - random                       | wsm|minmax|equal                | random        | ndcg@10  | new_markets |         1 |       0.2956 |     0.2637 |      0.3273 |         21 |
| wsm|minmax|expert_mean - import_volume          | wsm|minmax|expert_mean          | import_volume | ndcg@10  | new_markets |         1 |       0.1497 |     0.0966 |      0.201  |         21 |
| wsm|minmax|expert_mean - gravity_ppml           | wsm|minmax|expert_mean          | gravity_ppml  | ndcg@10  | new_markets |         1 |       0.1821 |     0.1206 |      0.2463 |         21 |
| wsm|minmax|expert_mean - random                 | wsm|minmax|expert_mean          | random        | ndcg@10  | new_markets |         1 |       0.2836 |     0.2478 |      0.319  |         21 |
| wsm|minmax|learned - import_volume              | wsm|minmax|learned              | import_volume | ndcg@10  | new_markets |         1 |       0.1575 |     0.1101 |      0.206  |         21 |
| wsm|minmax|learned - gravity_ppml               | wsm|minmax|learned              | gravity_ppml  | ndcg@10  | new_markets |         1 |       0.1898 |     0.1293 |      0.2503 |         21 |
| wsm|minmax|learned - random                     | wsm|minmax|learned              | random        | ndcg@10  | new_markets |         1 |       0.2914 |     0.2579 |      0.3234 |         21 |
| eoc - import_volume                             | eoc                             | import_volume | ndcg@10  | growth      |         1 |      -0.0106 |    -0.0686 |      0.0441 |         28 |
| eoc - gravity_ppml                              | eoc                             | gravity_ppml  | ndcg@10  | growth      |         1 |      -0.0135 |    -0.061  |      0.0362 |         28 |
| eoc - random                                    | eoc                             | random        | ndcg@10  | growth      |         1 |      -0.0047 |    -0.0504 |      0.0435 |         28 |
| equal_weights - import_volume                   | equal_weights                   | import_volume | ndcg@10  | growth      |         1 |       0.1344 |     0.0654 |      0.2077 |         28 |
| equal_weights - gravity_ppml                    | equal_weights                   | gravity_ppml  | ndcg@10  | growth      |         1 |       0.1315 |     0.0772 |      0.1869 |         28 |
| equal_weights - random                          | equal_weights                   | random        | ndcg@10  | growth      |         1 |       0.1402 |     0.0844 |      0.2005 |         28 |
| promethee_ii|minmax|expert_mean - import_volume | promethee_ii|minmax|expert_mean | import_volume | ndcg@10  | growth      |         1 |       0.1333 |     0.0691 |      0.2004 |         28 |
| promethee_ii|minmax|expert_mean - gravity_ppml  | promethee_ii|minmax|expert_mean | gravity_ppml  | ndcg@10  | growth      |         1 |       0.1304 |     0.0813 |      0.1836 |         28 |
| promethee_ii|minmax|expert_mean - random        | promethee_ii|minmax|expert_mean | random        | ndcg@10  | growth      |         1 |       0.1391 |     0.0876 |      0.1928 |         28 |
| topsis|minmax|expert_mean - import_volume       | topsis|minmax|expert_mean       | import_volume | ndcg@10  | growth      |         1 |       0.1386 |     0.0764 |      0.2064 |         28 |
| topsis|minmax|expert_mean - gravity_ppml        | topsis|minmax|expert_mean       | gravity_ppml  | ndcg@10  | growth      |         1 |       0.1357 |     0.0813 |      0.1876 |         28 |
| topsis|minmax|expert_mean - random              | topsis|minmax|expert_mean       | random        | ndcg@10  | growth      |         1 |       0.1444 |     0.095  |      0.1986 |         28 |
| vikor|minmax|expert_mean - import_volume        | vikor|minmax|expert_mean        | import_volume | ndcg@10  | growth      |         1 |       0.1352 |     0.0728 |      0.1992 |         28 |
| vikor|minmax|expert_mean - gravity_ppml         | vikor|minmax|expert_mean        | gravity_ppml  | ndcg@10  | growth      |         1 |       0.1323 |     0.0816 |      0.1831 |         28 |
| vikor|minmax|expert_mean - random               | vikor|minmax|expert_mean        | random        | ndcg@10  | growth      |         1 |       0.1411 |     0.0939 |      0.1895 |         28 |
| wsm|minmax|equal - import_volume                | wsm|minmax|equal                | import_volume | ndcg@10  | growth      |         1 |       0.1344 |     0.0692 |      0.2055 |         28 |
| wsm|minmax|equal - gravity_ppml                 | wsm|minmax|equal                | gravity_ppml  | ndcg@10  | growth      |         1 |       0.1315 |     0.0761 |      0.1847 |         28 |
| wsm|minmax|equal - random                       | wsm|minmax|equal                | random        | ndcg@10  | growth      |         1 |       0.1402 |     0.0825 |      0.1991 |         28 |
| wsm|minmax|expert_mean - import_volume          | wsm|minmax|expert_mean          | import_volume | ndcg@10  | growth      |         1 |       0.1364 |     0.0739 |      0.2037 |         28 |
| wsm|minmax|expert_mean - gravity_ppml           | wsm|minmax|expert_mean          | gravity_ppml  | ndcg@10  | growth      |         1 |       0.1335 |     0.0761 |      0.1912 |         28 |
| wsm|minmax|expert_mean - random                 | wsm|minmax|expert_mean          | random        | ndcg@10  | growth      |         1 |       0.1422 |     0.0867 |      0.1999 |         28 |
| wsm|minmax|learned - import_volume              | wsm|minmax|learned              | import_volume | ndcg@10  | growth      |         1 |       0.1331 |     0.072  |      0.198  |         28 |
| wsm|minmax|learned - gravity_ppml               | wsm|minmax|learned              | gravity_ppml  | ndcg@10  | growth      |         1 |       0.1302 |     0.0711 |      0.181  |         28 |
| wsm|minmax|learned - random                     | wsm|minmax|learned              | random        | ndcg@10  | growth      |         1 |       0.139  |     0.0886 |      0.1917 |         28 |
| eoc - import_volume                             | eoc                             | import_volume | ndcg@10  | intensive   |         3 |      -0.0577 |    -0.0982 |     -0.0146 |         14 |
| eoc - gravity_ppml                              | eoc                             | gravity_ppml  | ndcg@10  | intensive   |         3 |      -0.1187 |    -0.1922 |     -0.0331 |         14 |
| eoc - random                                    | eoc                             | random        | ndcg@10  | intensive   |         3 |      -0.0304 |    -0.0698 |      0.0168 |         14 |
| equal_weights - import_volume                   | equal_weights                   | import_volume | ndcg@10  | intensive   |         3 |       0.123  |     0.0451 |      0.2023 |         14 |
| equal_weights - gravity_ppml                    | equal_weights                   | gravity_ppml  | ndcg@10  | intensive   |         3 |       0.0619 |    -0.0097 |      0.1336 |         14 |
| equal_weights - random                          | equal_weights                   | random        | ndcg@10  | intensive   |         3 |       0.1503 |     0.0796 |      0.2236 |         14 |
| promethee_ii|minmax|expert_mean - import_volume | promethee_ii|minmax|expert_mean | import_volume | ndcg@10  | intensive   |         3 |       0.108  |     0.0274 |      0.1837 |         14 |
| promethee_ii|minmax|expert_mean - gravity_ppml  | promethee_ii|minmax|expert_mean | gravity_ppml  | ndcg@10  | intensive   |         3 |       0.0469 |    -0.0278 |      0.1259 |         14 |
| promethee_ii|minmax|expert_mean - random        | promethee_ii|minmax|expert_mean | random        | ndcg@10  | intensive   |         3 |       0.1353 |     0.0608 |      0.2087 |         14 |
| topsis|minmax|expert_mean - import_volume       | topsis|minmax|expert_mean       | import_volume | ndcg@10  | intensive   |         3 |       0.1169 |     0.0407 |      0.1922 |         14 |
| topsis|minmax|expert_mean - gravity_ppml        | topsis|minmax|expert_mean       | gravity_ppml  | ndcg@10  | intensive   |         3 |       0.0558 |    -0.0133 |      0.1286 |         14 |
| topsis|minmax|expert_mean - random              | topsis|minmax|expert_mean       | random        | ndcg@10  | intensive   |         3 |       0.1442 |     0.0771 |      0.2112 |         14 |
| vikor|minmax|expert_mean - import_volume        | vikor|minmax|expert_mean        | import_volume | ndcg@10  | intensive   |         3 |       0.1022 |     0.0302 |      0.1783 |         14 |
| vikor|minmax|expert_mean - gravity_ppml         | vikor|minmax|expert_mean        | gravity_ppml  | ndcg@10  | intensive   |         3 |       0.0411 |    -0.0304 |      0.1156 |         14 |
| vikor|minmax|expert_mean - random               | vikor|minmax|expert_mean        | random        | ndcg@10  | intensive   |         3 |       0.1295 |     0.0592 |      0.2036 |         14 |
| wsm|minmax|equal - import_volume                | wsm|minmax|equal                | import_volume | ndcg@10  | intensive   |         3 |       0.123  |     0.0397 |      0.2016 |         14 |
| wsm|minmax|equal - gravity_ppml                 | wsm|minmax|equal                | gravity_ppml  | ndcg@10  | intensive   |         3 |       0.0619 |    -0.0067 |      0.1357 |         14 |
| wsm|minmax|equal - random                       | wsm|minmax|equal                | random        | ndcg@10  | intensive   |         3 |       0.1503 |     0.0781 |      0.2222 |         14 |
| wsm|minmax|expert_mean - import_volume          | wsm|minmax|expert_mean          | import_volume | ndcg@10  | intensive   |         3 |       0.1168 |     0.0369 |      0.1935 |         14 |
| wsm|minmax|expert_mean - gravity_ppml           | wsm|minmax|expert_mean          | gravity_ppml  | ndcg@10  | intensive   |         3 |       0.0558 |    -0.011  |      0.1278 |         14 |
| wsm|minmax|expert_mean - random                 | wsm|minmax|expert_mean          | random        | ndcg@10  | intensive   |         3 |       0.1441 |     0.0717 |      0.2102 |         14 |
| wsm|minmax|learned - import_volume              | wsm|minmax|learned              | import_volume | ndcg@10  | intensive   |         3 |       0.12   |     0.0296 |      0.2113 |         14 |
| wsm|minmax|learned - gravity_ppml               | wsm|minmax|learned              | gravity_ppml  | ndcg@10  | intensive   |         3 |       0.059  |    -0.02   |      0.1365 |         14 |
| wsm|minmax|learned - random                     | wsm|minmax|learned              | random        | ndcg@10  | intensive   |         3 |       0.1473 |     0.0654 |      0.2322 |         14 |
| eoc - import_volume                             | eoc                             | import_volume | ndcg@10  | new_markets |         3 |      -0.0419 |    -0.091  |      0.0067 |         13 |
| eoc - gravity_ppml                              | eoc                             | gravity_ppml  | ndcg@10  | new_markets |         3 |      -0.0267 |    -0.0708 |      0.0175 |         13 |
| eoc - random                                    | eoc                             | random        | ndcg@10  | new_markets |         3 |       0.0954 |     0.0592 |      0.1325 |         13 |
| equal_weights - import_volume                   | equal_weights                   | import_volume | ndcg@10  | new_markets |         3 |       0.1583 |     0.092  |      0.2327 |         11 |
| equal_weights - gravity_ppml                    | equal_weights                   | gravity_ppml  | ndcg@10  | new_markets |         3 |       0.1701 |     0.1198 |      0.2198 |         11 |
| equal_weights - random                          | equal_weights                   | random        | ndcg@10  | new_markets |         3 |       0.2903 |     0.2565 |      0.3274 |         11 |
| promethee_ii|minmax|expert_mean - import_volume | promethee_ii|minmax|expert_mean | import_volume | ndcg@10  | new_markets |         3 |       0.1599 |     0.0989 |      0.2376 |         11 |
| promethee_ii|minmax|expert_mean - gravity_ppml  | promethee_ii|minmax|expert_mean | gravity_ppml  | ndcg@10  | new_markets |         3 |       0.1717 |     0.1083 |      0.23   |         11 |
| promethee_ii|minmax|expert_mean - random        | promethee_ii|minmax|expert_mean | random        | ndcg@10  | new_markets |         3 |       0.2919 |     0.2563 |      0.3345 |         11 |
| topsis|minmax|expert_mean - import_volume       | topsis|minmax|expert_mean       | import_volume | ndcg@10  | new_markets |         3 |       0.1597 |     0.0957 |      0.2355 |         11 |
| topsis|minmax|expert_mean - gravity_ppml        | topsis|minmax|expert_mean       | gravity_ppml  | ndcg@10  | new_markets |         3 |       0.1716 |     0.1229 |      0.2198 |         11 |
| topsis|minmax|expert_mean - random              | topsis|minmax|expert_mean       | random        | ndcg@10  | new_markets |         3 |       0.2917 |     0.26   |      0.328  |         11 |
| vikor|minmax|expert_mean - import_volume        | vikor|minmax|expert_mean        | import_volume | ndcg@10  | new_markets |         3 |       0.1749 |     0.1098 |      0.2512 |         11 |
| vikor|minmax|expert_mean - gravity_ppml         | vikor|minmax|expert_mean        | gravity_ppml  | ndcg@10  | new_markets |         3 |       0.1867 |     0.1388 |      0.2324 |         11 |
| vikor|minmax|expert_mean - random               | vikor|minmax|expert_mean        | random        | ndcg@10  | new_markets |         3 |       0.3068 |     0.2729 |      0.3437 |         11 |
| wsm|minmax|equal - import_volume                | wsm|minmax|equal                | import_volume | ndcg@10  | new_markets |         3 |       0.1583 |     0.099  |      0.2328 |         11 |
| wsm|minmax|equal - gravity_ppml                 | wsm|minmax|equal                | gravity_ppml  | ndcg@10  | new_markets |         3 |       0.1701 |     0.1225 |      0.2221 |         11 |
| wsm|minmax|equal - random                       | wsm|minmax|equal                | random        | ndcg@10  | new_markets |         3 |       0.2903 |     0.2578 |      0.3302 |         11 |
| wsm|minmax|expert_mean - import_volume          | wsm|minmax|expert_mean          | import_volume | ndcg@10  | new_markets |         3 |       0.1488 |     0.0821 |      0.229  |         11 |
| wsm|minmax|expert_mean - gravity_ppml           | wsm|minmax|expert_mean          | gravity_ppml  | ndcg@10  | new_markets |         3 |       0.1606 |     0.109  |      0.2152 |         11 |
| wsm|minmax|expert_mean - random                 | wsm|minmax|expert_mean          | random        | ndcg@10  | new_markets |         3 |       0.2808 |     0.244  |      0.32   |         11 |
| wsm|minmax|learned - import_volume              | wsm|minmax|learned              | import_volume | ndcg@10  | new_markets |         3 |       0.166  |     0.1056 |      0.2423 |         11 |
| wsm|minmax|learned - gravity_ppml               | wsm|minmax|learned              | gravity_ppml  | ndcg@10  | new_markets |         3 |       0.1778 |     0.1311 |      0.2257 |         11 |
| wsm|minmax|learned - random                     | wsm|minmax|learned              | random        | ndcg@10  | new_markets |         3 |       0.298  |     0.2625 |      0.3384 |         11 |
| eoc - import_volume                             | eoc                             | import_volume | ndcg@10  | growth      |         3 |      -0.0138 |    -0.0622 |      0.0345 |         14 |
| eoc - gravity_ppml                              | eoc                             | gravity_ppml  | ndcg@10  | growth      |         3 |      -0.0435 |    -0.1169 |      0.0323 |         14 |
| eoc - random                                    | eoc                             | random        | ndcg@10  | growth      |         3 |      -0.0018 |    -0.0604 |      0.0623 |         14 |
| equal_weights - import_volume                   | equal_weights                   | import_volume | ndcg@10  | growth      |         3 |       0.1774 |     0.1045 |      0.2622 |         14 |
| equal_weights - gravity_ppml                    | equal_weights                   | gravity_ppml  | ndcg@10  | growth      |         3 |       0.1477 |     0.0888 |      0.2041 |         14 |
| equal_weights - random                          | equal_weights                   | random        | ndcg@10  | growth      |         3 |       0.1894 |     0.1143 |      0.2633 |         14 |
| promethee_ii|minmax|expert_mean - import_volume | promethee_ii|minmax|expert_mean | import_volume | ndcg@10  | growth      |         3 |       0.1778 |     0.1118 |      0.2535 |         14 |
| promethee_ii|minmax|expert_mean - gravity_ppml  | promethee_ii|minmax|expert_mean | gravity_ppml  | ndcg@10  | growth      |         3 |       0.1481 |     0.0947 |      0.199  |         14 |
| promethee_ii|minmax|expert_mean - random        | promethee_ii|minmax|expert_mean | random        | ndcg@10  | growth      |         3 |       0.1898 |     0.1264 |      0.2503 |         14 |
| topsis|minmax|expert_mean - import_volume       | topsis|minmax|expert_mean       | import_volume | ndcg@10  | growth      |         3 |       0.1795 |     0.1135 |      0.252  |         14 |
| topsis|minmax|expert_mean - gravity_ppml        | topsis|minmax|expert_mean       | gravity_ppml  | ndcg@10  | growth      |         3 |       0.1499 |     0.0965 |      0.2061 |         14 |
| topsis|minmax|expert_mean - random              | topsis|minmax|expert_mean       | random        | ndcg@10  | growth      |         3 |       0.1915 |     0.1292 |      0.2524 |         14 |
| vikor|minmax|expert_mean - import_volume        | vikor|minmax|expert_mean        | import_volume | ndcg@10  | growth      |         3 |       0.172  |     0.1087 |      0.251  |         14 |
| vikor|minmax|expert_mean - gravity_ppml         | vikor|minmax|expert_mean        | gravity_ppml  | ndcg@10  | growth      |         3 |       0.1423 |     0.0965 |      0.1878 |         14 |
| vikor|minmax|expert_mean - random               | vikor|minmax|expert_mean        | random        | ndcg@10  | growth      |         3 |       0.184  |     0.1226 |      0.245  |         14 |
| wsm|minmax|equal - import_volume                | wsm|minmax|equal                | import_volume | ndcg@10  | growth      |         3 |       0.1774 |     0.1046 |      0.2603 |         14 |
| wsm|minmax|equal - gravity_ppml                 | wsm|minmax|equal                | gravity_ppml  | ndcg@10  | growth      |         3 |       0.1477 |     0.0947 |      0.2049 |         14 |
| wsm|minmax|equal - random                       | wsm|minmax|equal                | random        | ndcg@10  | growth      |         3 |       0.1894 |     0.1165 |      0.2647 |         14 |
| wsm|minmax|expert_mean - import_volume          | wsm|minmax|expert_mean          | import_volume | ndcg@10  | growth      |         3 |       0.1801 |     0.1067 |      0.262  |         14 |
| wsm|minmax|expert_mean - gravity_ppml           | wsm|minmax|expert_mean          | gravity_ppml  | ndcg@10  | growth      |         3 |       0.1504 |     0.0955 |      0.208  |         14 |
| wsm|minmax|expert_mean - random                 | wsm|minmax|expert_mean          | random        | ndcg@10  | growth      |         3 |       0.1921 |     0.122  |      0.2598 |         14 |
| wsm|minmax|learned - import_volume              | wsm|minmax|learned              | import_volume | ndcg@10  | growth      |         3 |       0.1656 |     0.0902 |      0.2494 |         14 |
| wsm|minmax|learned - gravity_ppml               | wsm|minmax|learned              | gravity_ppml  | ndcg@10  | growth      |         3 |       0.1359 |     0.0708 |      0.1968 |         14 |
| wsm|minmax|learned - random                     | wsm|minmax|learned              | random        | ndcg@10  | growth      |         3 |       0.1776 |     0.1041 |      0.2559 |         14 |

## Booktabs (copy into manuscript; not a repo .tex file)

```latex
\begin{table}[htbp]
\centering
\caption{T4d. Paired bootstrap lift vs import_volume / gravity / random}
\label{tab:T4_paired_lift}
\begin{tabular}{llllllllll}
\toprule
contrast & method & baseline & metric & target & horizon & delta\_mean & ci95\_low & ci95\_high & n\_blocks \\
\midrule
eoc - import\_volume & eoc & import\_volume & ndcg@10 & intensive & 1 & -0.0434 & -0.0809 & -0.0042 & 28 \\
eoc - gravity\_ppml & eoc & gravity\_ppml & ndcg@10 & intensive & 1 & -0.0528 & -0.0949 & -0.0069 & 28 \\
eoc - random & eoc & random & ndcg@10 & intensive & 1 & -0.0161 & -0.0477 & 0.0163 & 28 \\
equal\_weights - import\_volume & equal\_weights & import\_volume & ndcg@10 & intensive & 1 & 0.0923 & 0.0419 & 0.1451 & 28 \\
equal\_weights - gravity\_ppml & equal\_weights & gravity\_ppml & ndcg@10 & intensive & 1 & 0.0829 & 0.0433 & 0.1203 & 28 \\
equal\_weights - random & equal\_weights & random & ndcg@10 & intensive & 1 & 0.1196 & 0.0752 & 0.1638 & 28 \\
promethee\_ii|minmax|expert\_mean - import\_volume & promethee\_ii|minmax|expert\_mean & import\_volume & ndcg@10 & intensive & 1 & 0.0919 & 0.0475 & 0.1445 & 28 \\
promethee\_ii|minmax|expert\_mean - gravity\_ppml & promethee\_ii|minmax|expert\_mean & gravity\_ppml & ndcg@10 & intensive & 1 & 0.0825 & 0.0433 & 0.1239 & 28 \\
promethee\_ii|minmax|expert\_mean - random & promethee\_ii|minmax|expert\_mean & random & ndcg@10 & intensive & 1 & 0.1191 & 0.0761 & 0.1619 & 28 \\
topsis|minmax|expert\_mean - import\_volume & topsis|minmax|expert\_mean & import\_volume & ndcg@10 & intensive & 1 & 0.1014 & 0.0525 & 0.1552 & 28 \\
topsis|minmax|expert\_mean - gravity\_ppml & topsis|minmax|expert\_mean & gravity\_ppml & ndcg@10 & intensive & 1 & 0.0920 & 0.0491 & 0.1361 & 28 \\
topsis|minmax|expert\_mean - random & topsis|minmax|expert\_mean & random & ndcg@10 & intensive & 1 & 0.1287 & 0.0840 & 0.1722 & 28 \\
vikor|minmax|expert\_mean - import\_volume & vikor|minmax|expert\_mean & import\_volume & ndcg@10 & intensive & 1 & 0.0965 & 0.0470 & 0.1480 & 28 \\
vikor|minmax|expert\_mean - gravity\_ppml & vikor|minmax|expert\_mean & gravity\_ppml & ndcg@10 & intensive & 1 & 0.0871 & 0.0457 & 0.1295 & 28 \\
vikor|minmax|expert\_mean - random & vikor|minmax|expert\_mean & random & ndcg@10 & intensive & 1 & 0.1238 & 0.0782 & 0.1691 & 28 \\
wsm|minmax|equal - import\_volume & wsm|minmax|equal & import\_volume & ndcg@10 & intensive & 1 & 0.0923 & 0.0444 & 0.1420 & 28 \\
wsm|minmax|equal - gravity\_ppml & wsm|minmax|equal & gravity\_ppml & ndcg@10 & intensive & 1 & 0.0829 & 0.0458 & 0.1215 & 28 \\
wsm|minmax|equal - random & wsm|minmax|equal & random & ndcg@10 & intensive & 1 & 0.1196 & 0.0745 & 0.1636 & 28 \\
wsm|minmax|expert\_mean - import\_volume & wsm|minmax|expert\_mean & import\_volume & ndcg@10 & intensive & 1 & 0.0882 & 0.0422 & 0.1386 & 28 \\
wsm|minmax|expert\_mean - gravity\_ppml & wsm|minmax|expert\_mean & gravity\_ppml & ndcg@10 & intensive & 1 & 0.0789 & 0.0405 & 0.1160 & 28 \\
wsm|minmax|expert\_mean - random & wsm|minmax|expert\_mean & random & ndcg@10 & intensive & 1 & 0.1155 & 0.0712 & 0.1581 & 28 \\
wsm|minmax|learned - import\_volume & wsm|minmax|learned & import\_volume & ndcg@10 & intensive & 1 & 0.0966 & 0.0443 & 0.1509 & 28 \\
wsm|minmax|learned - gravity\_ppml & wsm|minmax|learned & gravity\_ppml & ndcg@10 & intensive & 1 & 0.0872 & 0.0450 & 0.1295 & 28 \\
wsm|minmax|learned - random & wsm|minmax|learned & random & ndcg@10 & intensive & 1 & 0.1238 & 0.0753 & 0.1734 & 28 \\
eoc - import\_volume & eoc & import\_volume & ndcg@10 & new\_markets & 1 & -0.0462 & -0.0878 & -0.0049 & 25 \\
eoc - gravity\_ppml & eoc & gravity\_ppml & ndcg@10 & new\_markets & 1 & -0.0064 & -0.0626 & 0.0511 & 25 \\
eoc - random & eoc & random & ndcg@10 & new\_markets & 1 & 0.0931 & 0.0600 & 0.1286 & 25 \\
equal\_weights - import\_volume & equal\_weights & import\_volume & ndcg@10 & new\_markets & 1 & 0.1617 & 0.1132 & 0.2129 & 21 \\
equal\_weights - gravity\_ppml & equal\_weights & gravity\_ppml & ndcg@10 & new\_markets & 1 & 0.1941 & 0.1360 & 0.2527 & 21 \\
equal\_weights - random & equal\_weights & random & ndcg@10 & new\_markets & 1 & 0.2956 & 0.2620 & 0.3304 & 21 \\
promethee\_ii|minmax|expert\_mean - import\_volume & promethee\_ii|minmax|expert\_mean & import\_volume & ndcg@10 & new\_markets & 1 & 0.1592 & 0.1100 & 0.2054 & 21 \\
promethee\_ii|minmax|expert\_mean - gravity\_ppml & promethee\_ii|minmax|expert\_mean & gravity\_ppml & ndcg@10 & new\_markets & 1 & 0.1915 & 0.1280 & 0.2587 & 21 \\
promethee\_ii|minmax|expert\_mean - random & promethee\_ii|minmax|expert\_mean & random & ndcg@10 & new\_markets & 1 & 0.2931 & 0.2580 & 0.3283 & 21 \\
topsis|minmax|expert\_mean - import\_volume & topsis|minmax|expert\_mean & import\_volume & ndcg@10 & new\_markets & 1 & 0.1538 & 0.1002 & 0.2047 & 21 \\
topsis|minmax|expert\_mean - gravity\_ppml & topsis|minmax|expert\_mean & gravity\_ppml & ndcg@10 & new\_markets & 1 & 0.1862 & 0.1255 & 0.2473 & 21 \\
topsis|minmax|expert\_mean - random & topsis|minmax|expert\_mean & random & ndcg@10 & new\_markets & 1 & 0.2877 & 0.2512 & 0.3249 & 21 \\
vikor|minmax|expert\_mean - import\_volume & vikor|minmax|expert\_mean & import\_volume & ndcg@10 & new\_markets & 1 & 0.1704 & 0.1189 & 0.2222 & 21 \\
vikor|minmax|expert\_mean - gravity\_ppml & vikor|minmax|expert\_mean & gravity\_ppml & ndcg@10 & new\_markets & 1 & 0.2027 & 0.1444 & 0.2603 & 21 \\
vikor|minmax|expert\_mean - random & vikor|minmax|expert\_mean & random & ndcg@10 & new\_markets & 1 & 0.3043 & 0.2682 & 0.3389 & 21 \\
wsm|minmax|equal - import\_volume & wsm|minmax|equal & import\_volume & ndcg@10 & new\_markets & 1 & 0.1617 & 0.1112 & 0.2144 & 21 \\
wsm|minmax|equal - gravity\_ppml & wsm|minmax|equal & gravity\_ppml & ndcg@10 & new\_markets & 1 & 0.1941 & 0.1377 & 0.2526 & 21 \\
wsm|minmax|equal - random & wsm|minmax|equal & random & ndcg@10 & new\_markets & 1 & 0.2956 & 0.2637 & 0.3273 & 21 \\
wsm|minmax|expert\_mean - import\_volume & wsm|minmax|expert\_mean & import\_volume & ndcg@10 & new\_markets & 1 & 0.1497 & 0.0966 & 0.2010 & 21 \\
wsm|minmax|expert\_mean - gravity\_ppml & wsm|minmax|expert\_mean & gravity\_ppml & ndcg@10 & new\_markets & 1 & 0.1821 & 0.1206 & 0.2463 & 21 \\
wsm|minmax|expert\_mean - random & wsm|minmax|expert\_mean & random & ndcg@10 & new\_markets & 1 & 0.2836 & 0.2478 & 0.3190 & 21 \\
wsm|minmax|learned - import\_volume & wsm|minmax|learned & import\_volume & ndcg@10 & new\_markets & 1 & 0.1575 & 0.1101 & 0.2060 & 21 \\
wsm|minmax|learned - gravity\_ppml & wsm|minmax|learned & gravity\_ppml & ndcg@10 & new\_markets & 1 & 0.1898 & 0.1293 & 0.2503 & 21 \\
wsm|minmax|learned - random & wsm|minmax|learned & random & ndcg@10 & new\_markets & 1 & 0.2914 & 0.2579 & 0.3234 & 21 \\
eoc - import\_volume & eoc & import\_volume & ndcg@10 & growth & 1 & -0.0106 & -0.0686 & 0.0441 & 28 \\
eoc - gravity\_ppml & eoc & gravity\_ppml & ndcg@10 & growth & 1 & -0.0135 & -0.0610 & 0.0362 & 28 \\
eoc - random & eoc & random & ndcg@10 & growth & 1 & -0.0047 & -0.0504 & 0.0435 & 28 \\
equal\_weights - import\_volume & equal\_weights & import\_volume & ndcg@10 & growth & 1 & 0.1344 & 0.0654 & 0.2077 & 28 \\
equal\_weights - gravity\_ppml & equal\_weights & gravity\_ppml & ndcg@10 & growth & 1 & 0.1315 & 0.0772 & 0.1869 & 28 \\
equal\_weights - random & equal\_weights & random & ndcg@10 & growth & 1 & 0.1402 & 0.0844 & 0.2005 & 28 \\
promethee\_ii|minmax|expert\_mean - import\_volume & promethee\_ii|minmax|expert\_mean & import\_volume & ndcg@10 & growth & 1 & 0.1333 & 0.0691 & 0.2004 & 28 \\
promethee\_ii|minmax|expert\_mean - gravity\_ppml & promethee\_ii|minmax|expert\_mean & gravity\_ppml & ndcg@10 & growth & 1 & 0.1304 & 0.0813 & 0.1836 & 28 \\
promethee\_ii|minmax|expert\_mean - random & promethee\_ii|minmax|expert\_mean & random & ndcg@10 & growth & 1 & 0.1391 & 0.0876 & 0.1928 & 28 \\
topsis|minmax|expert\_mean - import\_volume & topsis|minmax|expert\_mean & import\_volume & ndcg@10 & growth & 1 & 0.1386 & 0.0764 & 0.2064 & 28 \\
topsis|minmax|expert\_mean - gravity\_ppml & topsis|minmax|expert\_mean & gravity\_ppml & ndcg@10 & growth & 1 & 0.1357 & 0.0813 & 0.1876 & 28 \\
topsis|minmax|expert\_mean - random & topsis|minmax|expert\_mean & random & ndcg@10 & growth & 1 & 0.1444 & 0.0950 & 0.1986 & 28 \\
vikor|minmax|expert\_mean - import\_volume & vikor|minmax|expert\_mean & import\_volume & ndcg@10 & growth & 1 & 0.1352 & 0.0728 & 0.1992 & 28 \\
vikor|minmax|expert\_mean - gravity\_ppml & vikor|minmax|expert\_mean & gravity\_ppml & ndcg@10 & growth & 1 & 0.1323 & 0.0816 & 0.1831 & 28 \\
vikor|minmax|expert\_mean - random & vikor|minmax|expert\_mean & random & ndcg@10 & growth & 1 & 0.1411 & 0.0939 & 0.1895 & 28 \\
wsm|minmax|equal - import\_volume & wsm|minmax|equal & import\_volume & ndcg@10 & growth & 1 & 0.1344 & 0.0692 & 0.2055 & 28 \\
wsm|minmax|equal - gravity\_ppml & wsm|minmax|equal & gravity\_ppml & ndcg@10 & growth & 1 & 0.1315 & 0.0761 & 0.1847 & 28 \\
wsm|minmax|equal - random & wsm|minmax|equal & random & ndcg@10 & growth & 1 & 0.1402 & 0.0825 & 0.1991 & 28 \\
wsm|minmax|expert\_mean - import\_volume & wsm|minmax|expert\_mean & import\_volume & ndcg@10 & growth & 1 & 0.1364 & 0.0739 & 0.2037 & 28 \\
wsm|minmax|expert\_mean - gravity\_ppml & wsm|minmax|expert\_mean & gravity\_ppml & ndcg@10 & growth & 1 & 0.1335 & 0.0761 & 0.1912 & 28 \\
wsm|minmax|expert\_mean - random & wsm|minmax|expert\_mean & random & ndcg@10 & growth & 1 & 0.1422 & 0.0867 & 0.1999 & 28 \\
wsm|minmax|learned - import\_volume & wsm|minmax|learned & import\_volume & ndcg@10 & growth & 1 & 0.1331 & 0.0720 & 0.1980 & 28 \\
wsm|minmax|learned - gravity\_ppml & wsm|minmax|learned & gravity\_ppml & ndcg@10 & growth & 1 & 0.1302 & 0.0711 & 0.1810 & 28 \\
wsm|minmax|learned - random & wsm|minmax|learned & random & ndcg@10 & growth & 1 & 0.1390 & 0.0886 & 0.1917 & 28 \\
eoc - import\_volume & eoc & import\_volume & ndcg@10 & intensive & 3 & -0.0577 & -0.0982 & -0.0146 & 14 \\
eoc - gravity\_ppml & eoc & gravity\_ppml & ndcg@10 & intensive & 3 & -0.1187 & -0.1922 & -0.0331 & 14 \\
eoc - random & eoc & random & ndcg@10 & intensive & 3 & -0.0304 & -0.0698 & 0.0168 & 14 \\
equal\_weights - import\_volume & equal\_weights & import\_volume & ndcg@10 & intensive & 3 & 0.1230 & 0.0451 & 0.2023 & 14 \\
equal\_weights - gravity\_ppml & equal\_weights & gravity\_ppml & ndcg@10 & intensive & 3 & 0.0619 & -0.0097 & 0.1336 & 14 \\
equal\_weights - random & equal\_weights & random & ndcg@10 & intensive & 3 & 0.1503 & 0.0796 & 0.2236 & 14 \\
promethee\_ii|minmax|expert\_mean - import\_volume & promethee\_ii|minmax|expert\_mean & import\_volume & ndcg@10 & intensive & 3 & 0.1080 & 0.0274 & 0.1837 & 14 \\
promethee\_ii|minmax|expert\_mean - gravity\_ppml & promethee\_ii|minmax|expert\_mean & gravity\_ppml & ndcg@10 & intensive & 3 & 0.0469 & -0.0278 & 0.1259 & 14 \\
promethee\_ii|minmax|expert\_mean - random & promethee\_ii|minmax|expert\_mean & random & ndcg@10 & intensive & 3 & 0.1353 & 0.0608 & 0.2087 & 14 \\
topsis|minmax|expert\_mean - import\_volume & topsis|minmax|expert\_mean & import\_volume & ndcg@10 & intensive & 3 & 0.1169 & 0.0407 & 0.1922 & 14 \\
topsis|minmax|expert\_mean - gravity\_ppml & topsis|minmax|expert\_mean & gravity\_ppml & ndcg@10 & intensive & 3 & 0.0558 & -0.0133 & 0.1286 & 14 \\
topsis|minmax|expert\_mean - random & topsis|minmax|expert\_mean & random & ndcg@10 & intensive & 3 & 0.1442 & 0.0771 & 0.2112 & 14 \\
vikor|minmax|expert\_mean - import\_volume & vikor|minmax|expert\_mean & import\_volume & ndcg@10 & intensive & 3 & 0.1022 & 0.0302 & 0.1783 & 14 \\
vikor|minmax|expert\_mean - gravity\_ppml & vikor|minmax|expert\_mean & gravity\_ppml & ndcg@10 & intensive & 3 & 0.0411 & -0.0304 & 0.1156 & 14 \\
vikor|minmax|expert\_mean - random & vikor|minmax|expert\_mean & random & ndcg@10 & intensive & 3 & 0.1295 & 0.0592 & 0.2036 & 14 \\
wsm|minmax|equal - import\_volume & wsm|minmax|equal & import\_volume & ndcg@10 & intensive & 3 & 0.1230 & 0.0397 & 0.2016 & 14 \\
wsm|minmax|equal - gravity\_ppml & wsm|minmax|equal & gravity\_ppml & ndcg@10 & intensive & 3 & 0.0619 & -0.0067 & 0.1357 & 14 \\
wsm|minmax|equal - random & wsm|minmax|equal & random & ndcg@10 & intensive & 3 & 0.1503 & 0.0781 & 0.2222 & 14 \\
wsm|minmax|expert\_mean - import\_volume & wsm|minmax|expert\_mean & import\_volume & ndcg@10 & intensive & 3 & 0.1168 & 0.0369 & 0.1935 & 14 \\
wsm|minmax|expert\_mean - gravity\_ppml & wsm|minmax|expert\_mean & gravity\_ppml & ndcg@10 & intensive & 3 & 0.0558 & -0.0110 & 0.1278 & 14 \\
wsm|minmax|expert\_mean - random & wsm|minmax|expert\_mean & random & ndcg@10 & intensive & 3 & 0.1441 & 0.0717 & 0.2102 & 14 \\
wsm|minmax|learned - import\_volume & wsm|minmax|learned & import\_volume & ndcg@10 & intensive & 3 & 0.1200 & 0.0296 & 0.2113 & 14 \\
wsm|minmax|learned - gravity\_ppml & wsm|minmax|learned & gravity\_ppml & ndcg@10 & intensive & 3 & 0.0590 & -0.0200 & 0.1365 & 14 \\
wsm|minmax|learned - random & wsm|minmax|learned & random & ndcg@10 & intensive & 3 & 0.1473 & 0.0654 & 0.2322 & 14 \\
eoc - import\_volume & eoc & import\_volume & ndcg@10 & new\_markets & 3 & -0.0419 & -0.0910 & 0.0067 & 13 \\
eoc - gravity\_ppml & eoc & gravity\_ppml & ndcg@10 & new\_markets & 3 & -0.0267 & -0.0708 & 0.0175 & 13 \\
eoc - random & eoc & random & ndcg@10 & new\_markets & 3 & 0.0954 & 0.0592 & 0.1325 & 13 \\
equal\_weights - import\_volume & equal\_weights & import\_volume & ndcg@10 & new\_markets & 3 & 0.1583 & 0.0920 & 0.2327 & 11 \\
equal\_weights - gravity\_ppml & equal\_weights & gravity\_ppml & ndcg@10 & new\_markets & 3 & 0.1701 & 0.1198 & 0.2198 & 11 \\
equal\_weights - random & equal\_weights & random & ndcg@10 & new\_markets & 3 & 0.2903 & 0.2565 & 0.3274 & 11 \\
promethee\_ii|minmax|expert\_mean - import\_volume & promethee\_ii|minmax|expert\_mean & import\_volume & ndcg@10 & new\_markets & 3 & 0.1599 & 0.0989 & 0.2376 & 11 \\
promethee\_ii|minmax|expert\_mean - gravity\_ppml & promethee\_ii|minmax|expert\_mean & gravity\_ppml & ndcg@10 & new\_markets & 3 & 0.1717 & 0.1083 & 0.2300 & 11 \\
promethee\_ii|minmax|expert\_mean - random & promethee\_ii|minmax|expert\_mean & random & ndcg@10 & new\_markets & 3 & 0.2919 & 0.2563 & 0.3345 & 11 \\
topsis|minmax|expert\_mean - import\_volume & topsis|minmax|expert\_mean & import\_volume & ndcg@10 & new\_markets & 3 & 0.1597 & 0.0957 & 0.2355 & 11 \\
topsis|minmax|expert\_mean - gravity\_ppml & topsis|minmax|expert\_mean & gravity\_ppml & ndcg@10 & new\_markets & 3 & 0.1716 & 0.1229 & 0.2198 & 11 \\
topsis|minmax|expert\_mean - random & topsis|minmax|expert\_mean & random & ndcg@10 & new\_markets & 3 & 0.2917 & 0.2600 & 0.3280 & 11 \\
vikor|minmax|expert\_mean - import\_volume & vikor|minmax|expert\_mean & import\_volume & ndcg@10 & new\_markets & 3 & 0.1749 & 0.1098 & 0.2512 & 11 \\
vikor|minmax|expert\_mean - gravity\_ppml & vikor|minmax|expert\_mean & gravity\_ppml & ndcg@10 & new\_markets & 3 & 0.1867 & 0.1388 & 0.2324 & 11 \\
vikor|minmax|expert\_mean - random & vikor|minmax|expert\_mean & random & ndcg@10 & new\_markets & 3 & 0.3068 & 0.2729 & 0.3437 & 11 \\
wsm|minmax|equal - import\_volume & wsm|minmax|equal & import\_volume & ndcg@10 & new\_markets & 3 & 0.1583 & 0.0990 & 0.2328 & 11 \\
wsm|minmax|equal - gravity\_ppml & wsm|minmax|equal & gravity\_ppml & ndcg@10 & new\_markets & 3 & 0.1701 & 0.1225 & 0.2221 & 11 \\
wsm|minmax|equal - random & wsm|minmax|equal & random & ndcg@10 & new\_markets & 3 & 0.2903 & 0.2578 & 0.3302 & 11 \\
wsm|minmax|expert\_mean - import\_volume & wsm|minmax|expert\_mean & import\_volume & ndcg@10 & new\_markets & 3 & 0.1488 & 0.0821 & 0.2290 & 11 \\
wsm|minmax|expert\_mean - gravity\_ppml & wsm|minmax|expert\_mean & gravity\_ppml & ndcg@10 & new\_markets & 3 & 0.1606 & 0.1090 & 0.2152 & 11 \\
wsm|minmax|expert\_mean - random & wsm|minmax|expert\_mean & random & ndcg@10 & new\_markets & 3 & 0.2808 & 0.2440 & 0.3200 & 11 \\
wsm|minmax|learned - import\_volume & wsm|minmax|learned & import\_volume & ndcg@10 & new\_markets & 3 & 0.1660 & 0.1056 & 0.2423 & 11 \\
wsm|minmax|learned - gravity\_ppml & wsm|minmax|learned & gravity\_ppml & ndcg@10 & new\_markets & 3 & 0.1778 & 0.1311 & 0.2257 & 11 \\
wsm|minmax|learned - random & wsm|minmax|learned & random & ndcg@10 & new\_markets & 3 & 0.2980 & 0.2625 & 0.3384 & 11 \\
eoc - import\_volume & eoc & import\_volume & ndcg@10 & growth & 3 & -0.0138 & -0.0622 & 0.0345 & 14 \\
eoc - gravity\_ppml & eoc & gravity\_ppml & ndcg@10 & growth & 3 & -0.0435 & -0.1169 & 0.0323 & 14 \\
eoc - random & eoc & random & ndcg@10 & growth & 3 & -0.0018 & -0.0604 & 0.0623 & 14 \\
equal\_weights - import\_volume & equal\_weights & import\_volume & ndcg@10 & growth & 3 & 0.1774 & 0.1045 & 0.2622 & 14 \\
equal\_weights - gravity\_ppml & equal\_weights & gravity\_ppml & ndcg@10 & growth & 3 & 0.1477 & 0.0888 & 0.2041 & 14 \\
equal\_weights - random & equal\_weights & random & ndcg@10 & growth & 3 & 0.1894 & 0.1143 & 0.2633 & 14 \\
promethee\_ii|minmax|expert\_mean - import\_volume & promethee\_ii|minmax|expert\_mean & import\_volume & ndcg@10 & growth & 3 & 0.1778 & 0.1118 & 0.2535 & 14 \\
promethee\_ii|minmax|expert\_mean - gravity\_ppml & promethee\_ii|minmax|expert\_mean & gravity\_ppml & ndcg@10 & growth & 3 & 0.1481 & 0.0947 & 0.1990 & 14 \\
promethee\_ii|minmax|expert\_mean - random & promethee\_ii|minmax|expert\_mean & random & ndcg@10 & growth & 3 & 0.1898 & 0.1264 & 0.2503 & 14 \\
topsis|minmax|expert\_mean - import\_volume & topsis|minmax|expert\_mean & import\_volume & ndcg@10 & growth & 3 & 0.1795 & 0.1135 & 0.2520 & 14 \\
topsis|minmax|expert\_mean - gravity\_ppml & topsis|minmax|expert\_mean & gravity\_ppml & ndcg@10 & growth & 3 & 0.1499 & 0.0965 & 0.2061 & 14 \\
topsis|minmax|expert\_mean - random & topsis|minmax|expert\_mean & random & ndcg@10 & growth & 3 & 0.1915 & 0.1292 & 0.2524 & 14 \\
vikor|minmax|expert\_mean - import\_volume & vikor|minmax|expert\_mean & import\_volume & ndcg@10 & growth & 3 & 0.1720 & 0.1087 & 0.2510 & 14 \\
vikor|minmax|expert\_mean - gravity\_ppml & vikor|minmax|expert\_mean & gravity\_ppml & ndcg@10 & growth & 3 & 0.1423 & 0.0965 & 0.1878 & 14 \\
vikor|minmax|expert\_mean - random & vikor|minmax|expert\_mean & random & ndcg@10 & growth & 3 & 0.1840 & 0.1226 & 0.2450 & 14 \\
wsm|minmax|equal - import\_volume & wsm|minmax|equal & import\_volume & ndcg@10 & growth & 3 & 0.1774 & 0.1046 & 0.2603 & 14 \\
wsm|minmax|equal - gravity\_ppml & wsm|minmax|equal & gravity\_ppml & ndcg@10 & growth & 3 & 0.1477 & 0.0947 & 0.2049 & 14 \\
wsm|minmax|equal - random & wsm|minmax|equal & random & ndcg@10 & growth & 3 & 0.1894 & 0.1165 & 0.2647 & 14 \\
wsm|minmax|expert\_mean - import\_volume & wsm|minmax|expert\_mean & import\_volume & ndcg@10 & growth & 3 & 0.1801 & 0.1067 & 0.2620 & 14 \\
wsm|minmax|expert\_mean - gravity\_ppml & wsm|minmax|expert\_mean & gravity\_ppml & ndcg@10 & growth & 3 & 0.1504 & 0.0955 & 0.2080 & 14 \\
wsm|minmax|expert\_mean - random & wsm|minmax|expert\_mean & random & ndcg@10 & growth & 3 & 0.1921 & 0.1220 & 0.2598 & 14 \\
wsm|minmax|learned - import\_volume & wsm|minmax|learned & import\_volume & ndcg@10 & growth & 3 & 0.1656 & 0.0902 & 0.2494 & 14 \\
wsm|minmax|learned - gravity\_ppml & wsm|minmax|learned & gravity\_ppml & ndcg@10 & growth & 3 & 0.1359 & 0.0708 & 0.1968 & 14 \\
wsm|minmax|learned - random & wsm|minmax|learned & random & ndcg@10 & growth & 3 & 0.1776 & 0.1041 & 0.2559 & 14 \\
\bottomrule
\end{tabular}
\end{table}
```
