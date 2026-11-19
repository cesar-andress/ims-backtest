# T4d. Paired bootstrap lift vs import_volume / gravity / random

| contrast                                        | method                          | baseline      | metric   | target      |   horizon |   delta_mean |   ci95_low |   ci95_high |   n_blocks |
|:------------------------------------------------|:--------------------------------|:--------------|:---------|:------------|----------:|-------------:|-----------:|------------:|-----------:|
| eoc - import_volume                             | eoc                             | import_volume | ndcg@10  | intensive   |         1 |      -0.0434 |    -0.0809 |     -0.0042 |         28 |
| eoc - gravity_ppml                              | eoc                             | gravity_ppml  | ndcg@10  | intensive   |         1 |      -0.0528 |    -0.0949 |     -0.0069 |         28 |
| eoc - random                                    | eoc                             | random        | ndcg@10  | intensive   |         1 |      -0.0161 |    -0.0477 |      0.0163 |         28 |
| equal_weights - import_volume                   | equal_weights                   | import_volume | ndcg@10  | intensive   |         1 |      -0.0089 |    -0.0457 |      0.0245 |         28 |
| equal_weights - gravity_ppml                    | equal_weights                   | gravity_ppml  | ndcg@10  | intensive   |         1 |      -0.0182 |    -0.0533 |      0.0168 |         28 |
| equal_weights - random                          | equal_weights                   | random        | ndcg@10  | intensive   |         1 |       0.0184 |    -0.0179 |      0.0544 |         28 |
| promethee_ii|minmax|expert_mean - import_volume | promethee_ii|minmax|expert_mean | import_volume | ndcg@10  | intensive   |         1 |       0.006  |    -0.0257 |      0.0362 |         28 |
| promethee_ii|minmax|expert_mean - gravity_ppml  | promethee_ii|minmax|expert_mean | gravity_ppml  | ndcg@10  | intensive   |         1 |      -0.0033 |    -0.0401 |      0.0351 |         28 |
| promethee_ii|minmax|expert_mean - random        | promethee_ii|minmax|expert_mean | random        | ndcg@10  | intensive   |         1 |       0.0333 |    -0.0046 |      0.0708 |         28 |
| topsis|minmax|expert_mean - import_volume       | topsis|minmax|expert_mean       | import_volume | ndcg@10  | intensive   |         1 |      -0.0116 |    -0.0416 |      0.0181 |         28 |
| topsis|minmax|expert_mean - gravity_ppml        | topsis|minmax|expert_mean       | gravity_ppml  | ndcg@10  | intensive   |         1 |      -0.0209 |    -0.058  |      0.0162 |         28 |
| topsis|minmax|expert_mean - random              | topsis|minmax|expert_mean       | random        | ndcg@10  | intensive   |         1 |       0.0157 |    -0.0181 |      0.0494 |         28 |
| vikor|minmax|expert_mean - import_volume        | vikor|minmax|expert_mean        | import_volume | ndcg@10  | intensive   |         1 |      -0.0135 |    -0.0509 |      0.0216 |         28 |
| vikor|minmax|expert_mean - gravity_ppml         | vikor|minmax|expert_mean        | gravity_ppml  | ndcg@10  | intensive   |         1 |      -0.0229 |    -0.0579 |      0.0154 |         28 |
| vikor|minmax|expert_mean - random               | vikor|minmax|expert_mean        | random        | ndcg@10  | intensive   |         1 |       0.0138 |    -0.0213 |      0.0501 |         28 |
| wsm|minmax|equal - import_volume                | wsm|minmax|equal                | import_volume | ndcg@10  | intensive   |         1 |      -0.0089 |    -0.0444 |      0.0267 |         28 |
| wsm|minmax|equal - gravity_ppml                 | wsm|minmax|equal                | gravity_ppml  | ndcg@10  | intensive   |         1 |      -0.0182 |    -0.0552 |      0.0175 |         28 |
| wsm|minmax|equal - random                       | wsm|minmax|equal                | random        | ndcg@10  | intensive   |         1 |       0.0184 |    -0.0156 |      0.0539 |         28 |
| wsm|minmax|expert_mean - import_volume          | wsm|minmax|expert_mean          | import_volume | ndcg@10  | intensive   |         1 |      -0.0073 |    -0.0425 |      0.0268 |         28 |
| wsm|minmax|expert_mean - gravity_ppml           | wsm|minmax|expert_mean          | gravity_ppml  | ndcg@10  | intensive   |         1 |      -0.0167 |    -0.054  |      0.0185 |         28 |
| wsm|minmax|expert_mean - random                 | wsm|minmax|expert_mean          | random        | ndcg@10  | intensive   |         1 |       0.02   |    -0.0191 |      0.0574 |         28 |
| wsm|minmax|learned - import_volume              | wsm|minmax|learned              | import_volume | ndcg@10  | intensive   |         1 |       0.0024 |    -0.034  |      0.039  |         28 |
| wsm|minmax|learned - gravity_ppml               | wsm|minmax|learned              | gravity_ppml  | ndcg@10  | intensive   |         1 |      -0.0069 |    -0.0346 |      0.0251 |         28 |
| wsm|minmax|learned - random                     | wsm|minmax|learned              | random        | ndcg@10  | intensive   |         1 |       0.0297 |    -0.0084 |      0.0676 |         28 |
| eoc - import_volume                             | eoc                             | import_volume | ndcg@10  | new_markets |         1 |      -0.0462 |    -0.0878 |     -0.0049 |         25 |
| eoc - gravity_ppml                              | eoc                             | gravity_ppml  | ndcg@10  | new_markets |         1 |      -0.0064 |    -0.0626 |      0.0511 |         25 |
| eoc - random                                    | eoc                             | random        | ndcg@10  | new_markets |         1 |       0.0931 |     0.06   |      0.1286 |         25 |
| equal_weights - import_volume                   | equal_weights                   | import_volume | ndcg@10  | new_markets |         1 |       0.0137 |    -0.0285 |      0.056  |         25 |
| equal_weights - gravity_ppml                    | equal_weights                   | gravity_ppml  | ndcg@10  | new_markets |         1 |       0.0535 |     0.0075 |      0.0981 |         25 |
| equal_weights - random                          | equal_weights                   | random        | ndcg@10  | new_markets |         1 |       0.153  |     0.1156 |      0.1867 |         25 |
| promethee_ii|minmax|expert_mean - import_volume | promethee_ii|minmax|expert_mean | import_volume | ndcg@10  | new_markets |         1 |       0.0035 |    -0.0315 |      0.0341 |         25 |
| promethee_ii|minmax|expert_mean - gravity_ppml  | promethee_ii|minmax|expert_mean | gravity_ppml  | ndcg@10  | new_markets |         1 |       0.0433 |     0.0033 |      0.0848 |         25 |
| promethee_ii|minmax|expert_mean - random        | promethee_ii|minmax|expert_mean | random        | ndcg@10  | new_markets |         1 |       0.1428 |     0.1145 |      0.1697 |         25 |
| topsis|minmax|expert_mean - import_volume       | topsis|minmax|expert_mean       | import_volume | ndcg@10  | new_markets |         1 |       0.0164 |    -0.0285 |      0.0579 |         25 |
| topsis|minmax|expert_mean - gravity_ppml        | topsis|minmax|expert_mean       | gravity_ppml  | ndcg@10  | new_markets |         1 |       0.0562 |     0.0074 |      0.1064 |         25 |
| topsis|minmax|expert_mean - random              | topsis|minmax|expert_mean       | random        | ndcg@10  | new_markets |         1 |       0.1557 |     0.1206 |      0.1878 |         25 |
| vikor|minmax|expert_mean - import_volume        | vikor|minmax|expert_mean        | import_volume | ndcg@10  | new_markets |         1 |       0.003  |    -0.0397 |      0.0454 |         25 |
| vikor|minmax|expert_mean - gravity_ppml         | vikor|minmax|expert_mean        | gravity_ppml  | ndcg@10  | new_markets |         1 |       0.0428 |    -0.0032 |      0.0882 |         25 |
| vikor|minmax|expert_mean - random               | vikor|minmax|expert_mean        | random        | ndcg@10  | new_markets |         1 |       0.1424 |     0.1072 |      0.1737 |         25 |
| wsm|minmax|equal - import_volume                | wsm|minmax|equal                | import_volume | ndcg@10  | new_markets |         1 |       0.0137 |    -0.0284 |      0.0569 |         25 |
| wsm|minmax|equal - gravity_ppml                 | wsm|minmax|equal                | gravity_ppml  | ndcg@10  | new_markets |         1 |       0.0535 |     0.0064 |      0.1012 |         25 |
| wsm|minmax|equal - random                       | wsm|minmax|equal                | random        | ndcg@10  | new_markets |         1 |       0.153  |     0.1162 |      0.1843 |         25 |
| wsm|minmax|expert_mean - import_volume          | wsm|minmax|expert_mean          | import_volume | ndcg@10  | new_markets |         1 |       0.0013 |    -0.0439 |      0.0444 |         25 |
| wsm|minmax|expert_mean - gravity_ppml           | wsm|minmax|expert_mean          | gravity_ppml  | ndcg@10  | new_markets |         1 |       0.0411 |    -0.0089 |      0.0895 |         25 |
| wsm|minmax|expert_mean - random                 | wsm|minmax|expert_mean          | random        | ndcg@10  | new_markets |         1 |       0.1406 |     0.1049 |      0.1745 |         25 |
| wsm|minmax|learned - import_volume              | wsm|minmax|learned              | import_volume | ndcg@10  | new_markets |         1 |       0.0096 |    -0.0326 |      0.0511 |         25 |
| wsm|minmax|learned - gravity_ppml               | wsm|minmax|learned              | gravity_ppml  | ndcg@10  | new_markets |         1 |       0.0494 |    -0.0009 |      0.1021 |         25 |
| wsm|minmax|learned - random                     | wsm|minmax|learned              | random        | ndcg@10  | new_markets |         1 |       0.1489 |     0.1118 |      0.1825 |         25 |
| eoc - import_volume                             | eoc                             | import_volume | ndcg@10  | growth      |         1 |      -0.0106 |    -0.0686 |      0.0441 |         28 |
| eoc - gravity_ppml                              | eoc                             | gravity_ppml  | ndcg@10  | growth      |         1 |      -0.0135 |    -0.061  |      0.0362 |         28 |
| eoc - random                                    | eoc                             | random        | ndcg@10  | growth      |         1 |      -0.0047 |    -0.0504 |      0.0435 |         28 |
| equal_weights - import_volume                   | equal_weights                   | import_volume | ndcg@10  | growth      |         1 |       0.0294 |    -0.0088 |      0.0712 |         28 |
| equal_weights - gravity_ppml                    | equal_weights                   | gravity_ppml  | ndcg@10  | growth      |         1 |       0.0265 |    -0.0228 |      0.0785 |         28 |
| equal_weights - random                          | equal_weights                   | random        | ndcg@10  | growth      |         1 |       0.0352 |     0.0013 |      0.0765 |         28 |
| promethee_ii|minmax|expert_mean - import_volume | promethee_ii|minmax|expert_mean | import_volume | ndcg@10  | growth      |         1 |       0.0245 |    -0.0198 |      0.069  |         28 |
| promethee_ii|minmax|expert_mean - gravity_ppml  | promethee_ii|minmax|expert_mean | gravity_ppml  | ndcg@10  | growth      |         1 |       0.0216 |    -0.0239 |      0.0679 |         28 |
| promethee_ii|minmax|expert_mean - random        | promethee_ii|minmax|expert_mean | random        | ndcg@10  | growth      |         1 |       0.0303 |    -0.0074 |      0.0699 |         28 |
| topsis|minmax|expert_mean - import_volume       | topsis|minmax|expert_mean       | import_volume | ndcg@10  | growth      |         1 |       0.0317 |    -0.0107 |      0.0756 |         28 |
| topsis|minmax|expert_mean - gravity_ppml        | topsis|minmax|expert_mean       | gravity_ppml  | ndcg@10  | growth      |         1 |       0.0288 |    -0.0192 |      0.0792 |         28 |
| topsis|minmax|expert_mean - random              | topsis|minmax|expert_mean       | random        | ndcg@10  | growth      |         1 |       0.0375 |    -0.0002 |      0.0805 |         28 |
| vikor|minmax|expert_mean - import_volume        | vikor|minmax|expert_mean        | import_volume | ndcg@10  | growth      |         1 |       0.0301 |    -0.0169 |      0.0779 |         28 |
| vikor|minmax|expert_mean - gravity_ppml         | vikor|minmax|expert_mean        | gravity_ppml  | ndcg@10  | growth      |         1 |       0.0272 |    -0.0166 |      0.0742 |         28 |
| vikor|minmax|expert_mean - random               | vikor|minmax|expert_mean        | random        | ndcg@10  | growth      |         1 |       0.0359 |     0.0019 |      0.0709 |         28 |
| wsm|minmax|equal - import_volume                | wsm|minmax|equal                | import_volume | ndcg@10  | growth      |         1 |       0.0294 |    -0.0086 |      0.07   |         28 |
| wsm|minmax|equal - gravity_ppml                 | wsm|minmax|equal                | gravity_ppml  | ndcg@10  | growth      |         1 |       0.0265 |    -0.0248 |      0.0766 |         28 |
| wsm|minmax|equal - random                       | wsm|minmax|equal                | random        | ndcg@10  | growth      |         1 |       0.0352 |     0      |      0.0753 |         28 |
| wsm|minmax|expert_mean - import_volume          | wsm|minmax|expert_mean          | import_volume | ndcg@10  | growth      |         1 |       0.0305 |    -0.0121 |      0.0751 |         28 |
| wsm|minmax|expert_mean - gravity_ppml           | wsm|minmax|expert_mean          | gravity_ppml  | ndcg@10  | growth      |         1 |       0.0276 |    -0.0232 |      0.0764 |         28 |
| wsm|minmax|expert_mean - random                 | wsm|minmax|expert_mean          | random        | ndcg@10  | growth      |         1 |       0.0363 |    -0.0027 |      0.0781 |         28 |
| wsm|minmax|learned - import_volume              | wsm|minmax|learned              | import_volume | ndcg@10  | growth      |         1 |       0.0267 |    -0.024  |      0.0753 |         28 |
| wsm|minmax|learned - gravity_ppml               | wsm|minmax|learned              | gravity_ppml  | ndcg@10  | growth      |         1 |       0.0238 |    -0.0229 |      0.0694 |         28 |
| wsm|minmax|learned - random                     | wsm|minmax|learned              | random        | ndcg@10  | growth      |         1 |       0.0325 |    -0.0106 |      0.0778 |         28 |
| eoc - import_volume                             | eoc                             | import_volume | ndcg@10  | intensive   |         3 |      -0.0577 |    -0.0982 |     -0.0146 |         14 |
| eoc - gravity_ppml                              | eoc                             | gravity_ppml  | ndcg@10  | intensive   |         3 |      -0.1187 |    -0.1922 |     -0.0331 |         14 |
| eoc - random                                    | eoc                             | random        | ndcg@10  | intensive   |         3 |      -0.0304 |    -0.0698 |      0.0168 |         14 |
| equal_weights - import_volume                   | equal_weights                   | import_volume | ndcg@10  | intensive   |         3 |       0.0244 |    -0.0361 |      0.0845 |         14 |
| equal_weights - gravity_ppml                    | equal_weights                   | gravity_ppml  | ndcg@10  | intensive   |         3 |      -0.0366 |    -0.1089 |      0.0411 |         14 |
| equal_weights - random                          | equal_weights                   | random        | ndcg@10  | intensive   |         3 |       0.0517 |     0.0038 |      0.0992 |         14 |
| promethee_ii|minmax|expert_mean - import_volume | promethee_ii|minmax|expert_mean | import_volume | ndcg@10  | intensive   |         3 |       0.0138 |    -0.0446 |      0.0699 |         14 |
| promethee_ii|minmax|expert_mean - gravity_ppml  | promethee_ii|minmax|expert_mean | gravity_ppml  | ndcg@10  | intensive   |         3 |      -0.0472 |    -0.1217 |      0.0311 |         14 |
| promethee_ii|minmax|expert_mean - random        | promethee_ii|minmax|expert_mean | random        | ndcg@10  | intensive   |         3 |       0.0411 |    -0.0109 |      0.0987 |         14 |
| topsis|minmax|expert_mean - import_volume       | topsis|minmax|expert_mean       | import_volume | ndcg@10  | intensive   |         3 |       0.0177 |    -0.0406 |      0.0772 |         14 |
| topsis|minmax|expert_mean - gravity_ppml        | topsis|minmax|expert_mean       | gravity_ppml  | ndcg@10  | intensive   |         3 |      -0.0434 |    -0.1197 |      0.0396 |         14 |
| topsis|minmax|expert_mean - random              | topsis|minmax|expert_mean       | random        | ndcg@10  | intensive   |         3 |       0.0449 |    -0.012  |      0.1007 |         14 |
| vikor|minmax|expert_mean - import_volume        | vikor|minmax|expert_mean        | import_volume | ndcg@10  | intensive   |         3 |       0.0161 |    -0.0422 |      0.0707 |         14 |
| vikor|minmax|expert_mean - gravity_ppml         | vikor|minmax|expert_mean        | gravity_ppml  | ndcg@10  | intensive   |         3 |      -0.045  |    -0.1251 |      0.0369 |         14 |
| vikor|minmax|expert_mean - random               | vikor|minmax|expert_mean        | random        | ndcg@10  | intensive   |         3 |       0.0434 |    -0.0097 |      0.0975 |         14 |
| wsm|minmax|equal - import_volume                | wsm|minmax|equal                | import_volume | ndcg@10  | intensive   |         3 |       0.0244 |    -0.0352 |      0.0815 |         14 |
| wsm|minmax|equal - gravity_ppml                 | wsm|minmax|equal                | gravity_ppml  | ndcg@10  | intensive   |         3 |      -0.0366 |    -0.1102 |      0.0393 |         14 |
| wsm|minmax|equal - random                       | wsm|minmax|equal                | random        | ndcg@10  | intensive   |         3 |       0.0517 |     0.0008 |      0.0981 |         14 |
| wsm|minmax|expert_mean - import_volume          | wsm|minmax|expert_mean          | import_volume | ndcg@10  | intensive   |         3 |       0.0253 |    -0.0336 |      0.0816 |         14 |
| wsm|minmax|expert_mean - gravity_ppml           | wsm|minmax|expert_mean          | gravity_ppml  | ndcg@10  | intensive   |         3 |      -0.0357 |    -0.105  |      0.0404 |         14 |
| wsm|minmax|expert_mean - random                 | wsm|minmax|expert_mean          | random        | ndcg@10  | intensive   |         3 |       0.0526 |     0.0016 |      0.1013 |         14 |
| wsm|minmax|learned - import_volume              | wsm|minmax|learned              | import_volume | ndcg@10  | intensive   |         3 |       0.0623 |     0.0144 |      0.1101 |         14 |
| wsm|minmax|learned - gravity_ppml               | wsm|minmax|learned              | gravity_ppml  | ndcg@10  | intensive   |         3 |       0.0013 |    -0.0553 |      0.061  |         14 |
| wsm|minmax|learned - random                     | wsm|minmax|learned              | random        | ndcg@10  | intensive   |         3 |       0.0896 |     0.0508 |      0.1257 |         14 |
| eoc - import_volume                             | eoc                             | import_volume | ndcg@10  | new_markets |         3 |      -0.0419 |    -0.091  |      0.0067 |         13 |
| eoc - gravity_ppml                              | eoc                             | gravity_ppml  | ndcg@10  | new_markets |         3 |      -0.0267 |    -0.0708 |      0.0175 |         13 |
| eoc - random                                    | eoc                             | random        | ndcg@10  | new_markets |         3 |       0.0954 |     0.0592 |      0.1325 |         13 |
| equal_weights - import_volume                   | equal_weights                   | import_volume | ndcg@10  | new_markets |         3 |       0.0094 |    -0.0312 |      0.0475 |         13 |
| equal_weights - gravity_ppml                    | equal_weights                   | gravity_ppml  | ndcg@10  | new_markets |         3 |       0.0246 |    -0.0318 |      0.0915 |         13 |
| equal_weights - random                          | equal_weights                   | random        | ndcg@10  | new_markets |         3 |       0.1467 |     0.1144 |      0.1805 |         13 |
| promethee_ii|minmax|expert_mean - import_volume | promethee_ii|minmax|expert_mean | import_volume | ndcg@10  | new_markets |         3 |       0.0045 |    -0.0405 |      0.0484 |         13 |
| promethee_ii|minmax|expert_mean - gravity_ppml  | promethee_ii|minmax|expert_mean | gravity_ppml  | ndcg@10  | new_markets |         3 |       0.0196 |    -0.041  |      0.085  |         13 |
| promethee_ii|minmax|expert_mean - random        | promethee_ii|minmax|expert_mean | random        | ndcg@10  | new_markets |         3 |       0.1417 |     0.1058 |      0.1789 |         13 |
| topsis|minmax|expert_mean - import_volume       | topsis|minmax|expert_mean       | import_volume | ndcg@10  | new_markets |         3 |       0.002  |    -0.0403 |      0.044  |         13 |
| topsis|minmax|expert_mean - gravity_ppml        | topsis|minmax|expert_mean       | gravity_ppml  | ndcg@10  | new_markets |         3 |       0.0172 |    -0.0426 |      0.0847 |         13 |
| topsis|minmax|expert_mean - random              | topsis|minmax|expert_mean       | random        | ndcg@10  | new_markets |         3 |       0.1393 |     0.1016 |      0.1804 |         13 |
| vikor|minmax|expert_mean - import_volume        | vikor|minmax|expert_mean        | import_volume | ndcg@10  | new_markets |         3 |      -0.0264 |    -0.0694 |      0.0184 |         13 |
| vikor|minmax|expert_mean - gravity_ppml         | vikor|minmax|expert_mean        | gravity_ppml  | ndcg@10  | new_markets |         3 |      -0.0112 |    -0.0669 |      0.0448 |         13 |
| vikor|minmax|expert_mean - random               | vikor|minmax|expert_mean        | random        | ndcg@10  | new_markets |         3 |       0.1109 |     0.0816 |      0.1421 |         13 |
| wsm|minmax|equal - import_volume                | wsm|minmax|equal                | import_volume | ndcg@10  | new_markets |         3 |       0.0094 |    -0.0299 |      0.0499 |         13 |
| wsm|minmax|equal - gravity_ppml                 | wsm|minmax|equal                | gravity_ppml  | ndcg@10  | new_markets |         3 |       0.0246 |    -0.0325 |      0.0906 |         13 |
| wsm|minmax|equal - random                       | wsm|minmax|equal                | random        | ndcg@10  | new_markets |         3 |       0.1467 |     0.1123 |      0.1821 |         13 |
| wsm|minmax|expert_mean - import_volume          | wsm|minmax|expert_mean          | import_volume | ndcg@10  | new_markets |         3 |      -0.0118 |    -0.0585 |      0.0342 |         13 |
| wsm|minmax|expert_mean - gravity_ppml           | wsm|minmax|expert_mean          | gravity_ppml  | ndcg@10  | new_markets |         3 |       0.0033 |    -0.0559 |      0.0694 |         13 |
| wsm|minmax|expert_mean - random                 | wsm|minmax|expert_mean          | random        | ndcg@10  | new_markets |         3 |       0.1254 |     0.0873 |      0.1682 |         13 |
| wsm|minmax|learned - import_volume              | wsm|minmax|learned              | import_volume | ndcg@10  | new_markets |         3 |      -0.0006 |    -0.0479 |      0.0444 |         13 |
| wsm|minmax|learned - gravity_ppml               | wsm|minmax|learned              | gravity_ppml  | ndcg@10  | new_markets |         3 |       0.0146 |    -0.0484 |      0.0862 |         13 |
| wsm|minmax|learned - random                     | wsm|minmax|learned              | random        | ndcg@10  | new_markets |         3 |       0.1367 |     0.091  |      0.1805 |         13 |
| eoc - import_volume                             | eoc                             | import_volume | ndcg@10  | growth      |         3 |      -0.0138 |    -0.0622 |      0.0345 |         14 |
| eoc - gravity_ppml                              | eoc                             | gravity_ppml  | ndcg@10  | growth      |         3 |      -0.0435 |    -0.1169 |      0.0323 |         14 |
| eoc - random                                    | eoc                             | random        | ndcg@10  | growth      |         3 |      -0.0018 |    -0.0604 |      0.0623 |         14 |
| equal_weights - import_volume                   | equal_weights                   | import_volume | ndcg@10  | growth      |         3 |       0.0227 |    -0.0138 |      0.0615 |         14 |
| equal_weights - gravity_ppml                    | equal_weights                   | gravity_ppml  | ndcg@10  | growth      |         3 |      -0.007  |    -0.082  |      0.0747 |         14 |
| equal_weights - random                          | equal_weights                   | random        | ndcg@10  | growth      |         3 |       0.0347 |    -0.0183 |      0.09   |         14 |
| promethee_ii|minmax|expert_mean - import_volume | promethee_ii|minmax|expert_mean | import_volume | ndcg@10  | growth      |         3 |       0.0404 |     0.003  |      0.079  |         14 |
| promethee_ii|minmax|expert_mean - gravity_ppml  | promethee_ii|minmax|expert_mean | gravity_ppml  | ndcg@10  | growth      |         3 |       0.0107 |    -0.0705 |      0.0892 |         14 |
| promethee_ii|minmax|expert_mean - random        | promethee_ii|minmax|expert_mean | random        | ndcg@10  | growth      |         3 |       0.0524 |    -0.0003 |      0.1041 |         14 |
| topsis|minmax|expert_mean - import_volume       | topsis|minmax|expert_mean       | import_volume | ndcg@10  | growth      |         3 |       0.0415 |     0.0041 |      0.0837 |         14 |
| topsis|minmax|expert_mean - gravity_ppml        | topsis|minmax|expert_mean       | gravity_ppml  | ndcg@10  | growth      |         3 |       0.0118 |    -0.0688 |      0.0955 |         14 |
| topsis|minmax|expert_mean - random              | topsis|minmax|expert_mean       | random        | ndcg@10  | growth      |         3 |       0.0535 |    -0.0041 |      0.1154 |         14 |
| vikor|minmax|expert_mean - import_volume        | vikor|minmax|expert_mean        | import_volume | ndcg@10  | growth      |         3 |       0.0203 |    -0.0266 |      0.0657 |         14 |
| vikor|minmax|expert_mean - gravity_ppml         | vikor|minmax|expert_mean        | gravity_ppml  | ndcg@10  | growth      |         3 |      -0.0094 |    -0.099  |      0.0705 |         14 |
| vikor|minmax|expert_mean - random               | vikor|minmax|expert_mean        | random        | ndcg@10  | growth      |         3 |       0.0323 |    -0.0305 |      0.0943 |         14 |
| wsm|minmax|equal - import_volume                | wsm|minmax|equal                | import_volume | ndcg@10  | growth      |         3 |       0.0227 |    -0.0131 |      0.0632 |         14 |
| wsm|minmax|equal - gravity_ppml                 | wsm|minmax|equal                | gravity_ppml  | ndcg@10  | growth      |         3 |      -0.007  |    -0.0834 |      0.0759 |         14 |
| wsm|minmax|equal - random                       | wsm|minmax|equal                | random        | ndcg@10  | growth      |         3 |       0.0347 |    -0.0202 |      0.0926 |         14 |
| wsm|minmax|expert_mean - import_volume          | wsm|minmax|expert_mean          | import_volume | ndcg@10  | growth      |         3 |       0.0405 |     0.0096 |      0.0721 |         14 |
| wsm|minmax|expert_mean - gravity_ppml           | wsm|minmax|expert_mean          | gravity_ppml  | ndcg@10  | growth      |         3 |       0.0108 |    -0.0621 |      0.0902 |         14 |
| wsm|minmax|expert_mean - random                 | wsm|minmax|expert_mean          | random        | ndcg@10  | growth      |         3 |       0.0525 |     0.0006 |      0.1086 |         14 |
| wsm|minmax|learned - import_volume              | wsm|minmax|learned              | import_volume | ndcg@10  | growth      |         3 |       0.053  |     0.0264 |      0.082  |         14 |
| wsm|minmax|learned - gravity_ppml               | wsm|minmax|learned              | gravity_ppml  | ndcg@10  | growth      |         3 |       0.0233 |    -0.046  |      0.0903 |         14 |
| wsm|minmax|learned - random                     | wsm|minmax|learned              | random        | ndcg@10  | growth      |         3 |       0.065  |     0.0131 |      0.1144 |         14 |

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
equal\_weights - import\_volume & equal\_weights & import\_volume & ndcg@10 & intensive & 1 & -0.0089 & -0.0457 & 0.0245 & 28 \\
equal\_weights - gravity\_ppml & equal\_weights & gravity\_ppml & ndcg@10 & intensive & 1 & -0.0182 & -0.0533 & 0.0168 & 28 \\
equal\_weights - random & equal\_weights & random & ndcg@10 & intensive & 1 & 0.0184 & -0.0179 & 0.0544 & 28 \\
promethee\_ii|minmax|expert\_mean - import\_volume & promethee\_ii|minmax|expert\_mean & import\_volume & ndcg@10 & intensive & 1 & 0.0060 & -0.0257 & 0.0362 & 28 \\
promethee\_ii|minmax|expert\_mean - gravity\_ppml & promethee\_ii|minmax|expert\_mean & gravity\_ppml & ndcg@10 & intensive & 1 & -0.0033 & -0.0401 & 0.0351 & 28 \\
promethee\_ii|minmax|expert\_mean - random & promethee\_ii|minmax|expert\_mean & random & ndcg@10 & intensive & 1 & 0.0333 & -0.0046 & 0.0708 & 28 \\
topsis|minmax|expert\_mean - import\_volume & topsis|minmax|expert\_mean & import\_volume & ndcg@10 & intensive & 1 & -0.0116 & -0.0416 & 0.0181 & 28 \\
topsis|minmax|expert\_mean - gravity\_ppml & topsis|minmax|expert\_mean & gravity\_ppml & ndcg@10 & intensive & 1 & -0.0209 & -0.0580 & 0.0162 & 28 \\
topsis|minmax|expert\_mean - random & topsis|minmax|expert\_mean & random & ndcg@10 & intensive & 1 & 0.0157 & -0.0181 & 0.0494 & 28 \\
vikor|minmax|expert\_mean - import\_volume & vikor|minmax|expert\_mean & import\_volume & ndcg@10 & intensive & 1 & -0.0135 & -0.0509 & 0.0216 & 28 \\
vikor|minmax|expert\_mean - gravity\_ppml & vikor|minmax|expert\_mean & gravity\_ppml & ndcg@10 & intensive & 1 & -0.0229 & -0.0579 & 0.0154 & 28 \\
vikor|minmax|expert\_mean - random & vikor|minmax|expert\_mean & random & ndcg@10 & intensive & 1 & 0.0138 & -0.0213 & 0.0501 & 28 \\
wsm|minmax|equal - import\_volume & wsm|minmax|equal & import\_volume & ndcg@10 & intensive & 1 & -0.0089 & -0.0444 & 0.0267 & 28 \\
wsm|minmax|equal - gravity\_ppml & wsm|minmax|equal & gravity\_ppml & ndcg@10 & intensive & 1 & -0.0182 & -0.0552 & 0.0175 & 28 \\
wsm|minmax|equal - random & wsm|minmax|equal & random & ndcg@10 & intensive & 1 & 0.0184 & -0.0156 & 0.0539 & 28 \\
wsm|minmax|expert\_mean - import\_volume & wsm|minmax|expert\_mean & import\_volume & ndcg@10 & intensive & 1 & -0.0073 & -0.0425 & 0.0268 & 28 \\
wsm|minmax|expert\_mean - gravity\_ppml & wsm|minmax|expert\_mean & gravity\_ppml & ndcg@10 & intensive & 1 & -0.0167 & -0.0540 & 0.0185 & 28 \\
wsm|minmax|expert\_mean - random & wsm|minmax|expert\_mean & random & ndcg@10 & intensive & 1 & 0.0200 & -0.0191 & 0.0574 & 28 \\
wsm|minmax|learned - import\_volume & wsm|minmax|learned & import\_volume & ndcg@10 & intensive & 1 & 0.0024 & -0.0340 & 0.0390 & 28 \\
wsm|minmax|learned - gravity\_ppml & wsm|minmax|learned & gravity\_ppml & ndcg@10 & intensive & 1 & -0.0069 & -0.0346 & 0.0251 & 28 \\
wsm|minmax|learned - random & wsm|minmax|learned & random & ndcg@10 & intensive & 1 & 0.0297 & -0.0084 & 0.0676 & 28 \\
eoc - import\_volume & eoc & import\_volume & ndcg@10 & new\_markets & 1 & -0.0462 & -0.0878 & -0.0049 & 25 \\
eoc - gravity\_ppml & eoc & gravity\_ppml & ndcg@10 & new\_markets & 1 & -0.0064 & -0.0626 & 0.0511 & 25 \\
eoc - random & eoc & random & ndcg@10 & new\_markets & 1 & 0.0931 & 0.0600 & 0.1286 & 25 \\
equal\_weights - import\_volume & equal\_weights & import\_volume & ndcg@10 & new\_markets & 1 & 0.0137 & -0.0285 & 0.0560 & 25 \\
equal\_weights - gravity\_ppml & equal\_weights & gravity\_ppml & ndcg@10 & new\_markets & 1 & 0.0535 & 0.0075 & 0.0981 & 25 \\
equal\_weights - random & equal\_weights & random & ndcg@10 & new\_markets & 1 & 0.1530 & 0.1156 & 0.1867 & 25 \\
promethee\_ii|minmax|expert\_mean - import\_volume & promethee\_ii|minmax|expert\_mean & import\_volume & ndcg@10 & new\_markets & 1 & 0.0035 & -0.0315 & 0.0341 & 25 \\
promethee\_ii|minmax|expert\_mean - gravity\_ppml & promethee\_ii|minmax|expert\_mean & gravity\_ppml & ndcg@10 & new\_markets & 1 & 0.0433 & 0.0033 & 0.0848 & 25 \\
promethee\_ii|minmax|expert\_mean - random & promethee\_ii|minmax|expert\_mean & random & ndcg@10 & new\_markets & 1 & 0.1428 & 0.1145 & 0.1697 & 25 \\
topsis|minmax|expert\_mean - import\_volume & topsis|minmax|expert\_mean & import\_volume & ndcg@10 & new\_markets & 1 & 0.0164 & -0.0285 & 0.0579 & 25 \\
topsis|minmax|expert\_mean - gravity\_ppml & topsis|minmax|expert\_mean & gravity\_ppml & ndcg@10 & new\_markets & 1 & 0.0562 & 0.0074 & 0.1064 & 25 \\
topsis|minmax|expert\_mean - random & topsis|minmax|expert\_mean & random & ndcg@10 & new\_markets & 1 & 0.1557 & 0.1206 & 0.1878 & 25 \\
vikor|minmax|expert\_mean - import\_volume & vikor|minmax|expert\_mean & import\_volume & ndcg@10 & new\_markets & 1 & 0.0030 & -0.0397 & 0.0454 & 25 \\
vikor|minmax|expert\_mean - gravity\_ppml & vikor|minmax|expert\_mean & gravity\_ppml & ndcg@10 & new\_markets & 1 & 0.0428 & -0.0032 & 0.0882 & 25 \\
vikor|minmax|expert\_mean - random & vikor|minmax|expert\_mean & random & ndcg@10 & new\_markets & 1 & 0.1424 & 0.1072 & 0.1737 & 25 \\
wsm|minmax|equal - import\_volume & wsm|minmax|equal & import\_volume & ndcg@10 & new\_markets & 1 & 0.0137 & -0.0284 & 0.0569 & 25 \\
wsm|minmax|equal - gravity\_ppml & wsm|minmax|equal & gravity\_ppml & ndcg@10 & new\_markets & 1 & 0.0535 & 0.0064 & 0.1012 & 25 \\
wsm|minmax|equal - random & wsm|minmax|equal & random & ndcg@10 & new\_markets & 1 & 0.1530 & 0.1162 & 0.1843 & 25 \\
wsm|minmax|expert\_mean - import\_volume & wsm|minmax|expert\_mean & import\_volume & ndcg@10 & new\_markets & 1 & 0.0013 & -0.0439 & 0.0444 & 25 \\
wsm|minmax|expert\_mean - gravity\_ppml & wsm|minmax|expert\_mean & gravity\_ppml & ndcg@10 & new\_markets & 1 & 0.0411 & -0.0089 & 0.0895 & 25 \\
wsm|minmax|expert\_mean - random & wsm|minmax|expert\_mean & random & ndcg@10 & new\_markets & 1 & 0.1406 & 0.1049 & 0.1745 & 25 \\
wsm|minmax|learned - import\_volume & wsm|minmax|learned & import\_volume & ndcg@10 & new\_markets & 1 & 0.0096 & -0.0326 & 0.0511 & 25 \\
wsm|minmax|learned - gravity\_ppml & wsm|minmax|learned & gravity\_ppml & ndcg@10 & new\_markets & 1 & 0.0494 & -0.0009 & 0.1021 & 25 \\
wsm|minmax|learned - random & wsm|minmax|learned & random & ndcg@10 & new\_markets & 1 & 0.1489 & 0.1118 & 0.1825 & 25 \\
eoc - import\_volume & eoc & import\_volume & ndcg@10 & growth & 1 & -0.0106 & -0.0686 & 0.0441 & 28 \\
eoc - gravity\_ppml & eoc & gravity\_ppml & ndcg@10 & growth & 1 & -0.0135 & -0.0610 & 0.0362 & 28 \\
eoc - random & eoc & random & ndcg@10 & growth & 1 & -0.0047 & -0.0504 & 0.0435 & 28 \\
equal\_weights - import\_volume & equal\_weights & import\_volume & ndcg@10 & growth & 1 & 0.0294 & -0.0088 & 0.0712 & 28 \\
equal\_weights - gravity\_ppml & equal\_weights & gravity\_ppml & ndcg@10 & growth & 1 & 0.0265 & -0.0228 & 0.0785 & 28 \\
equal\_weights - random & equal\_weights & random & ndcg@10 & growth & 1 & 0.0352 & 0.0013 & 0.0765 & 28 \\
promethee\_ii|minmax|expert\_mean - import\_volume & promethee\_ii|minmax|expert\_mean & import\_volume & ndcg@10 & growth & 1 & 0.0245 & -0.0198 & 0.0690 & 28 \\
promethee\_ii|minmax|expert\_mean - gravity\_ppml & promethee\_ii|minmax|expert\_mean & gravity\_ppml & ndcg@10 & growth & 1 & 0.0216 & -0.0239 & 0.0679 & 28 \\
promethee\_ii|minmax|expert\_mean - random & promethee\_ii|minmax|expert\_mean & random & ndcg@10 & growth & 1 & 0.0303 & -0.0074 & 0.0699 & 28 \\
topsis|minmax|expert\_mean - import\_volume & topsis|minmax|expert\_mean & import\_volume & ndcg@10 & growth & 1 & 0.0317 & -0.0107 & 0.0756 & 28 \\
topsis|minmax|expert\_mean - gravity\_ppml & topsis|minmax|expert\_mean & gravity\_ppml & ndcg@10 & growth & 1 & 0.0288 & -0.0192 & 0.0792 & 28 \\
topsis|minmax|expert\_mean - random & topsis|minmax|expert\_mean & random & ndcg@10 & growth & 1 & 0.0375 & -0.0002 & 0.0805 & 28 \\
vikor|minmax|expert\_mean - import\_volume & vikor|minmax|expert\_mean & import\_volume & ndcg@10 & growth & 1 & 0.0301 & -0.0169 & 0.0779 & 28 \\
vikor|minmax|expert\_mean - gravity\_ppml & vikor|minmax|expert\_mean & gravity\_ppml & ndcg@10 & growth & 1 & 0.0272 & -0.0166 & 0.0742 & 28 \\
vikor|minmax|expert\_mean - random & vikor|minmax|expert\_mean & random & ndcg@10 & growth & 1 & 0.0359 & 0.0019 & 0.0709 & 28 \\
wsm|minmax|equal - import\_volume & wsm|minmax|equal & import\_volume & ndcg@10 & growth & 1 & 0.0294 & -0.0086 & 0.0700 & 28 \\
wsm|minmax|equal - gravity\_ppml & wsm|minmax|equal & gravity\_ppml & ndcg@10 & growth & 1 & 0.0265 & -0.0248 & 0.0766 & 28 \\
wsm|minmax|equal - random & wsm|minmax|equal & random & ndcg@10 & growth & 1 & 0.0352 & 0.0000 & 0.0753 & 28 \\
wsm|minmax|expert\_mean - import\_volume & wsm|minmax|expert\_mean & import\_volume & ndcg@10 & growth & 1 & 0.0305 & -0.0121 & 0.0751 & 28 \\
wsm|minmax|expert\_mean - gravity\_ppml & wsm|minmax|expert\_mean & gravity\_ppml & ndcg@10 & growth & 1 & 0.0276 & -0.0232 & 0.0764 & 28 \\
wsm|minmax|expert\_mean - random & wsm|minmax|expert\_mean & random & ndcg@10 & growth & 1 & 0.0363 & -0.0027 & 0.0781 & 28 \\
wsm|minmax|learned - import\_volume & wsm|minmax|learned & import\_volume & ndcg@10 & growth & 1 & 0.0267 & -0.0240 & 0.0753 & 28 \\
wsm|minmax|learned - gravity\_ppml & wsm|minmax|learned & gravity\_ppml & ndcg@10 & growth & 1 & 0.0238 & -0.0229 & 0.0694 & 28 \\
wsm|minmax|learned - random & wsm|minmax|learned & random & ndcg@10 & growth & 1 & 0.0325 & -0.0106 & 0.0778 & 28 \\
eoc - import\_volume & eoc & import\_volume & ndcg@10 & intensive & 3 & -0.0577 & -0.0982 & -0.0146 & 14 \\
eoc - gravity\_ppml & eoc & gravity\_ppml & ndcg@10 & intensive & 3 & -0.1187 & -0.1922 & -0.0331 & 14 \\
eoc - random & eoc & random & ndcg@10 & intensive & 3 & -0.0304 & -0.0698 & 0.0168 & 14 \\
equal\_weights - import\_volume & equal\_weights & import\_volume & ndcg@10 & intensive & 3 & 0.0244 & -0.0361 & 0.0845 & 14 \\
equal\_weights - gravity\_ppml & equal\_weights & gravity\_ppml & ndcg@10 & intensive & 3 & -0.0366 & -0.1089 & 0.0411 & 14 \\
equal\_weights - random & equal\_weights & random & ndcg@10 & intensive & 3 & 0.0517 & 0.0038 & 0.0992 & 14 \\
promethee\_ii|minmax|expert\_mean - import\_volume & promethee\_ii|minmax|expert\_mean & import\_volume & ndcg@10 & intensive & 3 & 0.0138 & -0.0446 & 0.0699 & 14 \\
promethee\_ii|minmax|expert\_mean - gravity\_ppml & promethee\_ii|minmax|expert\_mean & gravity\_ppml & ndcg@10 & intensive & 3 & -0.0472 & -0.1217 & 0.0311 & 14 \\
promethee\_ii|minmax|expert\_mean - random & promethee\_ii|minmax|expert\_mean & random & ndcg@10 & intensive & 3 & 0.0411 & -0.0109 & 0.0987 & 14 \\
topsis|minmax|expert\_mean - import\_volume & topsis|minmax|expert\_mean & import\_volume & ndcg@10 & intensive & 3 & 0.0177 & -0.0406 & 0.0772 & 14 \\
topsis|minmax|expert\_mean - gravity\_ppml & topsis|minmax|expert\_mean & gravity\_ppml & ndcg@10 & intensive & 3 & -0.0434 & -0.1197 & 0.0396 & 14 \\
topsis|minmax|expert\_mean - random & topsis|minmax|expert\_mean & random & ndcg@10 & intensive & 3 & 0.0449 & -0.0120 & 0.1007 & 14 \\
vikor|minmax|expert\_mean - import\_volume & vikor|minmax|expert\_mean & import\_volume & ndcg@10 & intensive & 3 & 0.0161 & -0.0422 & 0.0707 & 14 \\
vikor|minmax|expert\_mean - gravity\_ppml & vikor|minmax|expert\_mean & gravity\_ppml & ndcg@10 & intensive & 3 & -0.0450 & -0.1251 & 0.0369 & 14 \\
vikor|minmax|expert\_mean - random & vikor|minmax|expert\_mean & random & ndcg@10 & intensive & 3 & 0.0434 & -0.0097 & 0.0975 & 14 \\
wsm|minmax|equal - import\_volume & wsm|minmax|equal & import\_volume & ndcg@10 & intensive & 3 & 0.0244 & -0.0352 & 0.0815 & 14 \\
wsm|minmax|equal - gravity\_ppml & wsm|minmax|equal & gravity\_ppml & ndcg@10 & intensive & 3 & -0.0366 & -0.1102 & 0.0393 & 14 \\
wsm|minmax|equal - random & wsm|minmax|equal & random & ndcg@10 & intensive & 3 & 0.0517 & 0.0008 & 0.0981 & 14 \\
wsm|minmax|expert\_mean - import\_volume & wsm|minmax|expert\_mean & import\_volume & ndcg@10 & intensive & 3 & 0.0253 & -0.0336 & 0.0816 & 14 \\
wsm|minmax|expert\_mean - gravity\_ppml & wsm|minmax|expert\_mean & gravity\_ppml & ndcg@10 & intensive & 3 & -0.0357 & -0.1050 & 0.0404 & 14 \\
wsm|minmax|expert\_mean - random & wsm|minmax|expert\_mean & random & ndcg@10 & intensive & 3 & 0.0526 & 0.0016 & 0.1013 & 14 \\
wsm|minmax|learned - import\_volume & wsm|minmax|learned & import\_volume & ndcg@10 & intensive & 3 & 0.0623 & 0.0144 & 0.1101 & 14 \\
wsm|minmax|learned - gravity\_ppml & wsm|minmax|learned & gravity\_ppml & ndcg@10 & intensive & 3 & 0.0013 & -0.0553 & 0.0610 & 14 \\
wsm|minmax|learned - random & wsm|minmax|learned & random & ndcg@10 & intensive & 3 & 0.0896 & 0.0508 & 0.1257 & 14 \\
eoc - import\_volume & eoc & import\_volume & ndcg@10 & new\_markets & 3 & -0.0419 & -0.0910 & 0.0067 & 13 \\
eoc - gravity\_ppml & eoc & gravity\_ppml & ndcg@10 & new\_markets & 3 & -0.0267 & -0.0708 & 0.0175 & 13 \\
eoc - random & eoc & random & ndcg@10 & new\_markets & 3 & 0.0954 & 0.0592 & 0.1325 & 13 \\
equal\_weights - import\_volume & equal\_weights & import\_volume & ndcg@10 & new\_markets & 3 & 0.0094 & -0.0312 & 0.0475 & 13 \\
equal\_weights - gravity\_ppml & equal\_weights & gravity\_ppml & ndcg@10 & new\_markets & 3 & 0.0246 & -0.0318 & 0.0915 & 13 \\
equal\_weights - random & equal\_weights & random & ndcg@10 & new\_markets & 3 & 0.1467 & 0.1144 & 0.1805 & 13 \\
promethee\_ii|minmax|expert\_mean - import\_volume & promethee\_ii|minmax|expert\_mean & import\_volume & ndcg@10 & new\_markets & 3 & 0.0045 & -0.0405 & 0.0484 & 13 \\
promethee\_ii|minmax|expert\_mean - gravity\_ppml & promethee\_ii|minmax|expert\_mean & gravity\_ppml & ndcg@10 & new\_markets & 3 & 0.0196 & -0.0410 & 0.0850 & 13 \\
promethee\_ii|minmax|expert\_mean - random & promethee\_ii|minmax|expert\_mean & random & ndcg@10 & new\_markets & 3 & 0.1417 & 0.1058 & 0.1789 & 13 \\
topsis|minmax|expert\_mean - import\_volume & topsis|minmax|expert\_mean & import\_volume & ndcg@10 & new\_markets & 3 & 0.0020 & -0.0403 & 0.0440 & 13 \\
topsis|minmax|expert\_mean - gravity\_ppml & topsis|minmax|expert\_mean & gravity\_ppml & ndcg@10 & new\_markets & 3 & 0.0172 & -0.0426 & 0.0847 & 13 \\
topsis|minmax|expert\_mean - random & topsis|minmax|expert\_mean & random & ndcg@10 & new\_markets & 3 & 0.1393 & 0.1016 & 0.1804 & 13 \\
vikor|minmax|expert\_mean - import\_volume & vikor|minmax|expert\_mean & import\_volume & ndcg@10 & new\_markets & 3 & -0.0264 & -0.0694 & 0.0184 & 13 \\
vikor|minmax|expert\_mean - gravity\_ppml & vikor|minmax|expert\_mean & gravity\_ppml & ndcg@10 & new\_markets & 3 & -0.0112 & -0.0669 & 0.0448 & 13 \\
vikor|minmax|expert\_mean - random & vikor|minmax|expert\_mean & random & ndcg@10 & new\_markets & 3 & 0.1109 & 0.0816 & 0.1421 & 13 \\
wsm|minmax|equal - import\_volume & wsm|minmax|equal & import\_volume & ndcg@10 & new\_markets & 3 & 0.0094 & -0.0299 & 0.0499 & 13 \\
wsm|minmax|equal - gravity\_ppml & wsm|minmax|equal & gravity\_ppml & ndcg@10 & new\_markets & 3 & 0.0246 & -0.0325 & 0.0906 & 13 \\
wsm|minmax|equal - random & wsm|minmax|equal & random & ndcg@10 & new\_markets & 3 & 0.1467 & 0.1123 & 0.1821 & 13 \\
wsm|minmax|expert\_mean - import\_volume & wsm|minmax|expert\_mean & import\_volume & ndcg@10 & new\_markets & 3 & -0.0118 & -0.0585 & 0.0342 & 13 \\
wsm|minmax|expert\_mean - gravity\_ppml & wsm|minmax|expert\_mean & gravity\_ppml & ndcg@10 & new\_markets & 3 & 0.0033 & -0.0559 & 0.0694 & 13 \\
wsm|minmax|expert\_mean - random & wsm|minmax|expert\_mean & random & ndcg@10 & new\_markets & 3 & 0.1254 & 0.0873 & 0.1682 & 13 \\
wsm|minmax|learned - import\_volume & wsm|minmax|learned & import\_volume & ndcg@10 & new\_markets & 3 & -0.0006 & -0.0479 & 0.0444 & 13 \\
wsm|minmax|learned - gravity\_ppml & wsm|minmax|learned & gravity\_ppml & ndcg@10 & new\_markets & 3 & 0.0146 & -0.0484 & 0.0862 & 13 \\
wsm|minmax|learned - random & wsm|minmax|learned & random & ndcg@10 & new\_markets & 3 & 0.1367 & 0.0910 & 0.1805 & 13 \\
eoc - import\_volume & eoc & import\_volume & ndcg@10 & growth & 3 & -0.0138 & -0.0622 & 0.0345 & 14 \\
eoc - gravity\_ppml & eoc & gravity\_ppml & ndcg@10 & growth & 3 & -0.0435 & -0.1169 & 0.0323 & 14 \\
eoc - random & eoc & random & ndcg@10 & growth & 3 & -0.0018 & -0.0604 & 0.0623 & 14 \\
equal\_weights - import\_volume & equal\_weights & import\_volume & ndcg@10 & growth & 3 & 0.0227 & -0.0138 & 0.0615 & 14 \\
equal\_weights - gravity\_ppml & equal\_weights & gravity\_ppml & ndcg@10 & growth & 3 & -0.0070 & -0.0820 & 0.0747 & 14 \\
equal\_weights - random & equal\_weights & random & ndcg@10 & growth & 3 & 0.0347 & -0.0183 & 0.0900 & 14 \\
promethee\_ii|minmax|expert\_mean - import\_volume & promethee\_ii|minmax|expert\_mean & import\_volume & ndcg@10 & growth & 3 & 0.0404 & 0.0030 & 0.0790 & 14 \\
promethee\_ii|minmax|expert\_mean - gravity\_ppml & promethee\_ii|minmax|expert\_mean & gravity\_ppml & ndcg@10 & growth & 3 & 0.0107 & -0.0705 & 0.0892 & 14 \\
promethee\_ii|minmax|expert\_mean - random & promethee\_ii|minmax|expert\_mean & random & ndcg@10 & growth & 3 & 0.0524 & -0.0003 & 0.1041 & 14 \\
topsis|minmax|expert\_mean - import\_volume & topsis|minmax|expert\_mean & import\_volume & ndcg@10 & growth & 3 & 0.0415 & 0.0041 & 0.0837 & 14 \\
topsis|minmax|expert\_mean - gravity\_ppml & topsis|minmax|expert\_mean & gravity\_ppml & ndcg@10 & growth & 3 & 0.0118 & -0.0688 & 0.0955 & 14 \\
topsis|minmax|expert\_mean - random & topsis|minmax|expert\_mean & random & ndcg@10 & growth & 3 & 0.0535 & -0.0041 & 0.1154 & 14 \\
vikor|minmax|expert\_mean - import\_volume & vikor|minmax|expert\_mean & import\_volume & ndcg@10 & growth & 3 & 0.0203 & -0.0266 & 0.0657 & 14 \\
vikor|minmax|expert\_mean - gravity\_ppml & vikor|minmax|expert\_mean & gravity\_ppml & ndcg@10 & growth & 3 & -0.0094 & -0.0990 & 0.0705 & 14 \\
vikor|minmax|expert\_mean - random & vikor|minmax|expert\_mean & random & ndcg@10 & growth & 3 & 0.0323 & -0.0305 & 0.0943 & 14 \\
wsm|minmax|equal - import\_volume & wsm|minmax|equal & import\_volume & ndcg@10 & growth & 3 & 0.0227 & -0.0131 & 0.0632 & 14 \\
wsm|minmax|equal - gravity\_ppml & wsm|minmax|equal & gravity\_ppml & ndcg@10 & growth & 3 & -0.0070 & -0.0834 & 0.0759 & 14 \\
wsm|minmax|equal - random & wsm|minmax|equal & random & ndcg@10 & growth & 3 & 0.0347 & -0.0202 & 0.0926 & 14 \\
wsm|minmax|expert\_mean - import\_volume & wsm|minmax|expert\_mean & import\_volume & ndcg@10 & growth & 3 & 0.0405 & 0.0096 & 0.0721 & 14 \\
wsm|minmax|expert\_mean - gravity\_ppml & wsm|minmax|expert\_mean & gravity\_ppml & ndcg@10 & growth & 3 & 0.0108 & -0.0621 & 0.0902 & 14 \\
wsm|minmax|expert\_mean - random & wsm|minmax|expert\_mean & random & ndcg@10 & growth & 3 & 0.0525 & 0.0006 & 0.1086 & 14 \\
wsm|minmax|learned - import\_volume & wsm|minmax|learned & import\_volume & ndcg@10 & growth & 3 & 0.0530 & 0.0264 & 0.0820 & 14 \\
wsm|minmax|learned - gravity\_ppml & wsm|minmax|learned & gravity\_ppml & ndcg@10 & growth & 3 & 0.0233 & -0.0460 & 0.0903 & 14 \\
wsm|minmax|learned - random & wsm|minmax|learned & random & ndcg@10 & growth & 3 & 0.0650 & 0.0131 & 0.1144 & 14 \\
\bottomrule
\end{tabular}
\end{table}
```
