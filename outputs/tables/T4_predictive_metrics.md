# T4. Predictive validation metrics (bootstrap means and 95% CIs)

| method                          | metric       |   mean |   ci95_low |   ci95_high |   n_blocks | target      |   horizon |
|:--------------------------------|:-------------|-------:|-----------:|------------:|-----------:|:------------|----------:|
| eoc                             | ndcg@10      |  0.702 |      0.651 |       0.751 |         28 | intensive   |         1 |
| equal_weights                   | ndcg@10      |  0.838 |      0.801 |       0.874 |         28 | intensive   |         1 |
| gravity_ppml                    | ndcg@10      |  0.755 |      0.705 |       0.805 |         28 | intensive   |         1 |
| import_volume                   | ndcg@10      |  0.745 |      0.696 |       0.795 |         28 | intensive   |         1 |
| promethee_ii|minmax|expert_mean | ndcg@10      |  0.837 |      0.8   |       0.871 |         28 | intensive   |         1 |
| random                          | ndcg@10      |  0.718 |      0.674 |       0.761 |         28 | intensive   |         1 |
| topsis|minmax|expert_mean       | ndcg@10      |  0.847 |      0.816 |       0.88  |         28 | intensive   |         1 |
| vikor|minmax|expert_mean        | ndcg@10      |  0.842 |      0.807 |       0.874 |         28 | intensive   |         1 |
| wsm|minmax|equal                | ndcg@10      |  0.838 |      0.802 |       0.872 |         28 | intensive   |         1 |
| wsm|minmax|expert_mean          | ndcg@10      |  0.834 |      0.799 |       0.869 |         28 | intensive   |         1 |
| wsm|minmax|learned              | ndcg@10      |  0.842 |      0.807 |       0.878 |         28 | intensive   |         1 |
| eoc                             | spearman     | -0.051 |     -0.179 |       0.072 |         28 | intensive   |         1 |
| equal_weights                   | spearman     |  0.012 |     -0.169 |       0.2   |         27 | intensive   |         1 |
| gravity_ppml                    | spearman     |  0.123 |     -0.017 |       0.258 |         28 | intensive   |         1 |
| import_volume                   | spearman     |  0.04  |     -0.091 |       0.16  |         28 | intensive   |         1 |
| promethee_ii|minmax|expert_mean | spearman     | -0.001 |     -0.177 |       0.169 |         27 | intensive   |         1 |
| random                          | spearman     | -0.003 |     -0.025 |       0.016 |         28 | intensive   |         1 |
| topsis|minmax|expert_mean       | spearman     |  0.012 |     -0.166 |       0.185 |         27 | intensive   |         1 |
| vikor|minmax|expert_mean        | spearman     |  0.001 |     -0.17  |       0.174 |         27 | intensive   |         1 |
| wsm|minmax|equal                | spearman     |  0.012 |     -0.161 |       0.181 |         27 | intensive   |         1 |
| wsm|minmax|expert_mean          | spearman     | -0.009 |     -0.168 |       0.173 |         27 | intensive   |         1 |
| wsm|minmax|learned              | spearman     |  0.007 |     -0.167 |       0.177 |         27 | intensive   |         1 |
| eoc                             | precision@10 |  0.704 |      0.586 |       0.807 |         28 | intensive   |         1 |
| equal_weights                   | precision@10 |  0.904 |      0.836 |       0.964 |         28 | intensive   |         1 |
| gravity_ppml                    | precision@10 |  0.718 |      0.604 |       0.829 |         28 | intensive   |         1 |
| import_volume                   | precision@10 |  0.696 |      0.578 |       0.818 |         28 | intensive   |         1 |
| promethee_ii|minmax|expert_mean | precision@10 |  0.904 |      0.836 |       0.961 |         28 | intensive   |         1 |
| random                          | precision@10 |  0.691 |      0.571 |       0.805 |         28 | intensive   |         1 |
| topsis|minmax|expert_mean       | precision@10 |  0.911 |      0.846 |       0.964 |         28 | intensive   |         1 |
| vikor|minmax|expert_mean        | precision@10 |  0.911 |      0.846 |       0.964 |         28 | intensive   |         1 |
| wsm|minmax|equal                | precision@10 |  0.904 |      0.836 |       0.964 |         28 | intensive   |         1 |
| wsm|minmax|expert_mean          | precision@10 |  0.904 |      0.832 |       0.961 |         28 | intensive   |         1 |
| wsm|minmax|learned              | precision@10 |  0.911 |      0.846 |       0.964 |         28 | intensive   |         1 |
| eoc                             | auc          |  0.409 |      0.318 |       0.496 |         24 | intensive   |         1 |
| equal_weights                   | auc          |  0.482 |      0.365 |       0.599 |         17 | intensive   |         1 |
| gravity_ppml                    | auc          |  0.529 |      0.442 |       0.604 |         24 | intensive   |         1 |
| import_volume                   | auc          |  0.627 |      0.53  |       0.715 |         24 | intensive   |         1 |
| promethee_ii|minmax|expert_mean | auc          |  0.458 |      0.348 |       0.563 |         17 | intensive   |         1 |
| random                          | auc          |  0.49  |      0.478 |       0.5   |         24 | intensive   |         1 |
| topsis|minmax|expert_mean       | auc          |  0.489 |      0.369 |       0.609 |         17 | intensive   |         1 |
| vikor|minmax|expert_mean        | auc          |  0.505 |      0.399 |       0.614 |         17 | intensive   |         1 |
| wsm|minmax|equal                | auc          |  0.482 |      0.36  |       0.598 |         17 | intensive   |         1 |
| wsm|minmax|expert_mean          | auc          |  0.481 |      0.355 |       0.594 |         17 | intensive   |         1 |
| wsm|minmax|learned              | auc          |  0.487 |      0.345 |       0.619 |         17 | intensive   |         1 |
| eoc                             | ndcg@10      |  0.676 |      0.641 |       0.71  |         25 | new_markets |         1 |
| equal_weights                   | ndcg@10      |  0.879 |      0.842 |       0.912 |         21 | new_markets |         1 |
| gravity_ppml                    | ndcg@10      |  0.682 |      0.644 |       0.719 |         25 | new_markets |         1 |
| import_volume                   | ndcg@10      |  0.722 |      0.691 |       0.752 |         25 | new_markets |         1 |
| promethee_ii|minmax|expert_mean | ndcg@10      |  0.876 |      0.837 |       0.914 |         21 | new_markets |         1 |
| random                          | ndcg@10      |  0.583 |      0.576 |       0.593 |         25 | new_markets |         1 |
| topsis|minmax|expert_mean       | ndcg@10      |  0.871 |      0.833 |       0.911 |         21 | new_markets |         1 |
| vikor|minmax|expert_mean        | ndcg@10      |  0.887 |      0.849 |       0.923 |         21 | new_markets |         1 |
| wsm|minmax|equal                | ndcg@10      |  0.879 |      0.843 |       0.915 |         21 | new_markets |         1 |
| wsm|minmax|expert_mean          | ndcg@10      |  0.867 |      0.826 |       0.906 |         21 | new_markets |         1 |
| wsm|minmax|learned              | ndcg@10      |  0.875 |      0.839 |       0.909 |         21 | new_markets |         1 |
| eoc                             | spearman     |  0.122 |      0.057 |       0.187 |         25 | new_markets |         1 |
| equal_weights                   | spearman     |  0.236 |      0.127 |       0.341 |         17 | new_markets |         1 |
| gravity_ppml                    | spearman     |  0.292 |      0.224 |       0.359 |         25 | new_markets |         1 |
| import_volume                   | spearman     |  0.395 |      0.352 |       0.439 |         25 | new_markets |         1 |
| promethee_ii|minmax|expert_mean | spearman     |  0.212 |      0.081 |       0.348 |         17 | new_markets |         1 |
| random                          | spearman     | -0.011 |     -0.02  |      -0.002 |         25 | new_markets |         1 |
| topsis|minmax|expert_mean       | spearman     |  0.234 |      0.114 |       0.354 |         17 | new_markets |         1 |
| vikor|minmax|expert_mean        | spearman     |  0.323 |      0.205 |       0.443 |         17 | new_markets |         1 |
| wsm|minmax|equal                | spearman     |  0.236 |      0.122 |       0.344 |         17 | new_markets |         1 |
| wsm|minmax|expert_mean          | spearman     |  0.188 |      0.069 |       0.307 |         17 | new_markets |         1 |
| wsm|minmax|learned              | spearman     |  0.251 |      0.144 |       0.361 |         17 | new_markets |         1 |
| eoc                             | precision@10 |  0.396 |      0.348 |       0.45  |         25 | new_markets |         1 |
| equal_weights                   | precision@10 |  0.848 |      0.796 |       0.895 |         21 | new_markets |         1 |
| gravity_ppml                    | precision@10 |  0.464 |      0.404 |       0.525 |         25 | new_markets |         1 |
| import_volume                   | precision@10 |  0.532 |      0.493 |       0.571 |         25 | new_markets |         1 |
| promethee_ii|minmax|expert_mean | precision@10 |  0.838 |      0.784 |       0.888 |         21 | new_markets |         1 |
| random                          | precision@10 |  0.332 |      0.327 |       0.337 |         25 | new_markets |         1 |
| topsis|minmax|expert_mean       | precision@10 |  0.843 |      0.792 |       0.895 |         21 | new_markets |         1 |
| vikor|minmax|expert_mean        | precision@10 |  0.852 |      0.8   |       0.905 |         21 | new_markets |         1 |
| wsm|minmax|equal                | precision@10 |  0.848 |      0.796 |       0.896 |         21 | new_markets |         1 |
| wsm|minmax|expert_mean          | precision@10 |  0.848 |      0.795 |       0.895 |         21 | new_markets |         1 |
| wsm|minmax|learned              | precision@10 |  0.843 |      0.791 |       0.895 |         21 | new_markets |         1 |
| eoc                             | ndcg@10      |  0.536 |      0.491 |       0.581 |         28 | growth      |         1 |
| equal_weights                   | ndcg@10      |  0.681 |      0.626 |       0.74  |         28 | growth      |         1 |
| gravity_ppml                    | ndcg@10      |  0.55  |      0.51  |       0.588 |         28 | growth      |         1 |
| import_volume                   | ndcg@10      |  0.547 |      0.515 |       0.58  |         28 | growth      |         1 |
| promethee_ii|minmax|expert_mean | ndcg@10      |  0.68  |      0.635 |       0.731 |         28 | growth      |         1 |
| random                          | ndcg@10      |  0.541 |      0.537 |       0.545 |         28 | growth      |         1 |
| topsis|minmax|expert_mean       | ndcg@10      |  0.686 |      0.635 |       0.739 |         28 | growth      |         1 |
| vikor|minmax|expert_mean        | ndcg@10      |  0.682 |      0.636 |       0.732 |         28 | growth      |         1 |
| wsm|minmax|equal                | ndcg@10      |  0.681 |      0.625 |       0.742 |         28 | growth      |         1 |
| wsm|minmax|expert_mean          | ndcg@10      |  0.683 |      0.63  |       0.74  |         28 | growth      |         1 |
| wsm|minmax|learned              | ndcg@10      |  0.68  |      0.626 |       0.737 |         28 | growth      |         1 |
| eoc                             | spearman     |  0.014 |     -0.033 |       0.06  |         28 | growth      |         1 |
| equal_weights                   | spearman     |  0.042 |     -0.066 |       0.154 |         28 | growth      |         1 |
| gravity_ppml                    | spearman     |  0.028 |     -0.039 |       0.096 |         28 | growth      |         1 |
| import_volume                   | spearman     |  0.004 |     -0.045 |       0.054 |         28 | growth      |         1 |
| promethee_ii|minmax|expert_mean | spearman     |  0.025 |     -0.069 |       0.122 |         28 | growth      |         1 |
| random                          | spearman     |  0.001 |     -0.004 |       0.006 |         28 | growth      |         1 |
| topsis|minmax|expert_mean       | spearman     |  0.042 |     -0.056 |       0.14  |         28 | growth      |         1 |
| vikor|minmax|expert_mean        | spearman     |  0.034 |     -0.067 |       0.129 |         28 | growth      |         1 |
| wsm|minmax|equal                | spearman     |  0.042 |     -0.068 |       0.149 |         28 | growth      |         1 |
| wsm|minmax|expert_mean          | spearman     |  0.038 |     -0.068 |       0.14  |         28 | growth      |         1 |
| wsm|minmax|learned              | spearman     |  0.005 |     -0.113 |       0.113 |         28 | growth      |         1 |
| eoc                             | precision@10 |  0.193 |      0.154 |       0.236 |         28 | growth      |         1 |
| equal_weights                   | precision@10 |  0.529 |      0.411 |       0.646 |         28 | growth      |         1 |
| gravity_ppml                    | precision@10 |  0.139 |      0.096 |       0.189 |         28 | growth      |         1 |
| import_volume                   | precision@10 |  0.125 |      0.089 |       0.164 |         28 | growth      |         1 |
| promethee_ii|minmax|expert_mean | precision@10 |  0.539 |      0.425 |       0.661 |         28 | growth      |         1 |
| random                          | precision@10 |  0.169 |      0.166 |       0.172 |         28 | growth      |         1 |
| topsis|minmax|expert_mean       | precision@10 |  0.536 |      0.414 |       0.657 |         28 | growth      |         1 |
| vikor|minmax|expert_mean        | precision@10 |  0.536 |      0.429 |       0.657 |         28 | growth      |         1 |
| wsm|minmax|equal                | precision@10 |  0.529 |      0.411 |       0.654 |         28 | growth      |         1 |
| wsm|minmax|expert_mean          | precision@10 |  0.529 |      0.411 |       0.654 |         28 | growth      |         1 |
| wsm|minmax|learned              | precision@10 |  0.525 |      0.4   |       0.65  |         28 | growth      |         1 |
| eoc                             | ndcg@10      |  0.688 |      0.626 |       0.741 |         14 | intensive   |         3 |
| equal_weights                   | ndcg@10      |  0.868 |      0.832 |       0.908 |         14 | intensive   |         3 |
| gravity_ppml                    | ndcg@10      |  0.806 |      0.732 |       0.873 |         14 | intensive   |         3 |
| import_volume                   | ndcg@10      |  0.745 |      0.691 |       0.801 |         14 | intensive   |         3 |
| promethee_ii|minmax|expert_mean | ndcg@10      |  0.853 |      0.819 |       0.891 |         14 | intensive   |         3 |
| random                          | ndcg@10      |  0.718 |      0.659 |       0.777 |         14 | intensive   |         3 |
| topsis|minmax|expert_mean       | ndcg@10      |  0.862 |      0.822 |       0.905 |         14 | intensive   |         3 |
| vikor|minmax|expert_mean        | ndcg@10      |  0.848 |      0.813 |       0.881 |         14 | intensive   |         3 |
| wsm|minmax|equal                | ndcg@10      |  0.868 |      0.832 |       0.907 |         14 | intensive   |         3 |
| wsm|minmax|expert_mean          | ndcg@10      |  0.862 |      0.824 |       0.905 |         14 | intensive   |         3 |
| wsm|minmax|learned              | ndcg@10      |  0.865 |      0.819 |       0.909 |         14 | intensive   |         3 |
| eoc                             | spearman     | -0.133 |     -0.243 |      -0.024 |         14 | intensive   |         3 |
| equal_weights                   | spearman     |  0.023 |     -0.228 |       0.266 |         13 | intensive   |         3 |
| gravity_ppml                    | spearman     |  0.329 |      0.171 |       0.483 |         14 | intensive   |         3 |
| import_volume                   | spearman     | -0.005 |     -0.22  |       0.186 |         14 | intensive   |         3 |
| promethee_ii|minmax|expert_mean | spearman     |  0.033 |     -0.199 |       0.267 |         13 | intensive   |         3 |
| random                          | spearman     |  0.007 |     -0.021 |       0.034 |         14 | intensive   |         3 |
| topsis|minmax|expert_mean       | spearman     |  0.046 |     -0.236 |       0.334 |         13 | intensive   |         3 |
| vikor|minmax|expert_mean        | spearman     | -0.006 |     -0.279 |       0.243 |         13 | intensive   |         3 |
| wsm|minmax|equal                | spearman     |  0.023 |     -0.225 |       0.268 |         13 | intensive   |         3 |
| wsm|minmax|expert_mean          | spearman     |  0.059 |     -0.221 |       0.323 |         13 | intensive   |         3 |
| wsm|minmax|learned              | spearman     |  0.066 |     -0.175 |       0.285 |         13 | intensive   |         3 |
| eoc                             | precision@10 |  0.707 |      0.557 |       0.843 |         14 | intensive   |         3 |
| equal_weights                   | precision@10 |  0.929 |      0.85  |       0.986 |         14 | intensive   |         3 |
| gravity_ppml                    | precision@10 |  0.729 |      0.571 |       0.879 |         14 | intensive   |         3 |
| import_volume                   | precision@10 |  0.686 |      0.507 |       0.836 |         14 | intensive   |         3 |
| promethee_ii|minmax|expert_mean | precision@10 |  0.936 |      0.864 |       0.986 |         14 | intensive   |         3 |
| random                          | precision@10 |  0.691 |      0.531 |       0.839 |         14 | intensive   |         3 |
| topsis|minmax|expert_mean       | precision@10 |  0.921 |      0.843 |       0.993 |         14 | intensive   |         3 |
| vikor|minmax|expert_mean        | precision@10 |  0.921 |      0.843 |       0.986 |         14 | intensive   |         3 |
| wsm|minmax|equal                | precision@10 |  0.929 |      0.864 |       0.986 |         14 | intensive   |         3 |
| wsm|minmax|expert_mean          | precision@10 |  0.921 |      0.843 |       0.986 |         14 | intensive   |         3 |
| wsm|minmax|learned              | precision@10 |  0.929 |      0.857 |       0.986 |         14 | intensive   |         3 |
| eoc                             | auc          |  0.399 |      0.287 |       0.502 |         12 | intensive   |         3 |
| equal_weights                   | auc          |  0.482 |      0.326 |       0.609 |          9 | intensive   |         3 |
| gravity_ppml                    | auc          |  0.526 |      0.411 |       0.628 |         12 | intensive   |         3 |
| import_volume                   | auc          |  0.61  |      0.454 |       0.746 |         12 | intensive   |         3 |
| promethee_ii|minmax|expert_mean | auc          |  0.468 |      0.328 |       0.572 |          9 | intensive   |         3 |
| random                          | auc          |  0.487 |      0.473 |       0.499 |         12 | intensive   |         3 |
| topsis|minmax|expert_mean       | auc          |  0.478 |      0.331 |       0.599 |          9 | intensive   |         3 |
| vikor|minmax|expert_mean        | auc          |  0.504 |      0.362 |       0.625 |          9 | intensive   |         3 |
| wsm|minmax|equal                | auc          |  0.482 |      0.336 |       0.606 |          9 | intensive   |         3 |
| wsm|minmax|expert_mean          | auc          |  0.488 |      0.341 |       0.606 |          9 | intensive   |         3 |
| wsm|minmax|learned              | auc          |  0.514 |      0.354 |       0.662 |          9 | intensive   |         3 |
| eoc                             | ndcg@10      |  0.682 |      0.643 |       0.719 |         13 | new_markets |         3 |
| equal_weights                   | ndcg@10      |  0.878 |      0.841 |       0.919 |         11 | new_markets |         3 |
| gravity_ppml                    | ndcg@10      |  0.709 |      0.67  |       0.746 |         13 | new_markets |         3 |
| import_volume                   | ndcg@10      |  0.724 |      0.683 |       0.763 |         13 | new_markets |         3 |
| promethee_ii|minmax|expert_mean | ndcg@10      |  0.88  |      0.835 |       0.928 |         11 | new_markets |         3 |
| random                          | ndcg@10      |  0.587 |      0.575 |       0.604 |         13 | new_markets |         3 |
| topsis|minmax|expert_mean       | ndcg@10      |  0.879 |      0.845 |       0.921 |         11 | new_markets |         3 |
| vikor|minmax|expert_mean        | ndcg@10      |  0.895 |      0.857 |       0.934 |         11 | new_markets |         3 |
| wsm|minmax|equal                | ndcg@10      |  0.878 |      0.84  |       0.923 |         11 | new_markets |         3 |
| wsm|minmax|expert_mean          | ndcg@10      |  0.868 |      0.826 |       0.915 |         11 | new_markets |         3 |
| wsm|minmax|learned              | ndcg@10      |  0.886 |      0.845 |       0.929 |         11 | new_markets |         3 |
| eoc                             | spearman     |  0.121 |      0.034 |       0.201 |         13 | new_markets |         3 |
| equal_weights                   | spearman     |  0.267 |      0.187 |       0.358 |          9 | new_markets |         3 |
| gravity_ppml                    | spearman     |  0.312 |      0.245 |       0.377 |         13 | new_markets |         3 |
| import_volume                   | spearman     |  0.409 |      0.373 |       0.444 |         13 | new_markets |         3 |
| promethee_ii|minmax|expert_mean | spearman     |  0.242 |      0.113 |       0.39  |          9 | new_markets |         3 |
| random                          | spearman     | -0.014 |     -0.026 |      -0.001 |         13 | new_markets |         3 |
| topsis|minmax|expert_mean       | spearman     |  0.291 |      0.222 |       0.363 |          9 | new_markets |         3 |
| vikor|minmax|expert_mean        | spearman     |  0.4   |      0.328 |       0.473 |          9 | new_markets |         3 |
| wsm|minmax|equal                | spearman     |  0.267 |      0.19  |       0.357 |          9 | new_markets |         3 |
| wsm|minmax|expert_mean          | spearman     |  0.214 |      0.144 |       0.275 |          9 | new_markets |         3 |
| wsm|minmax|learned              | spearman     |  0.299 |      0.213 |       0.373 |          9 | new_markets |         3 |
| eoc                             | precision@10 |  0.385 |      0.321 |       0.454 |         13 | new_markets |         3 |
| equal_weights                   | precision@10 |  0.882 |      0.833 |       0.933 |         11 | new_markets |         3 |
| gravity_ppml                    | precision@10 |  0.462 |      0.4   |       0.525 |         13 | new_markets |         3 |
| import_volume                   | precision@10 |  0.508 |      0.454 |       0.558 |         13 | new_markets |         3 |
| promethee_ii|minmax|expert_mean | precision@10 |  0.873 |      0.822 |       0.925 |         11 | new_markets |         3 |
| random                          | precision@10 |  0.326 |      0.32  |       0.331 |         13 | new_markets |         3 |
| topsis|minmax|expert_mean       | precision@10 |  0.882 |      0.833 |       0.933 |         11 | new_markets |         3 |
| vikor|minmax|expert_mean        | precision@10 |  0.9   |      0.85  |       0.95  |         11 | new_markets |         3 |
| wsm|minmax|equal                | precision@10 |  0.882 |      0.833 |       0.933 |         11 | new_markets |         3 |
| wsm|minmax|expert_mean          | precision@10 |  0.882 |      0.833 |       0.936 |         11 | new_markets |         3 |
| wsm|minmax|learned              | precision@10 |  0.864 |      0.8   |       0.927 |         11 | new_markets |         3 |
| eoc                             | ndcg@10      |  0.539 |      0.481 |       0.601 |         14 | growth      |         3 |
| equal_weights                   | ndcg@10      |  0.73  |      0.657 |       0.802 |         14 | growth      |         3 |
| gravity_ppml                    | ndcg@10      |  0.583 |      0.523 |       0.634 |         14 | growth      |         3 |
| import_volume                   | ndcg@10      |  0.553 |      0.515 |       0.587 |         14 | growth      |         3 |
| promethee_ii|minmax|expert_mean | ndcg@10      |  0.731 |      0.669 |       0.794 |         14 | growth      |         3 |
| random                          | ndcg@10      |  0.541 |      0.536 |       0.545 |         14 | growth      |         3 |
| topsis|minmax|expert_mean       | ndcg@10      |  0.732 |      0.669 |       0.796 |         14 | growth      |         3 |
| vikor|minmax|expert_mean        | ndcg@10      |  0.725 |      0.667 |       0.783 |         14 | growth      |         3 |
| wsm|minmax|equal                | ndcg@10      |  0.73  |      0.655 |       0.802 |         14 | growth      |         3 |
| wsm|minmax|expert_mean          | ndcg@10      |  0.733 |      0.66  |       0.805 |         14 | growth      |         3 |
| wsm|minmax|learned              | ndcg@10      |  0.718 |      0.648 |       0.789 |         14 | growth      |         3 |
| eoc                             | spearman     |  0.015 |     -0.033 |       0.062 |         14 | growth      |         3 |
| equal_weights                   | spearman     |  0.073 |     -0.104 |       0.24  |         14 | growth      |         3 |
| gravity_ppml                    | spearman     |  0.113 |      0.039 |       0.18  |         14 | growth      |         3 |
| import_volume                   | spearman     |  0.021 |     -0.055 |       0.092 |         14 | growth      |         3 |
| promethee_ii|minmax|expert_mean | spearman     |  0.086 |     -0.051 |       0.234 |         14 | growth      |         3 |
| random                          | spearman     |  0.001 |     -0.005 |       0.007 |         14 | growth      |         3 |
| topsis|minmax|expert_mean       | spearman     |  0.059 |     -0.154 |       0.245 |         14 | growth      |         3 |
| vikor|minmax|expert_mean        | spearman     |  0.075 |     -0.108 |       0.252 |         14 | growth      |         3 |
| wsm|minmax|equal                | spearman     |  0.073 |     -0.104 |       0.238 |         14 | growth      |         3 |
| wsm|minmax|expert_mean          | spearman     |  0.085 |     -0.094 |       0.258 |         14 | growth      |         3 |
| wsm|minmax|learned              | spearman     |  0.102 |      0.025 |       0.174 |         14 | growth      |         3 |
| eoc                             | precision@10 |  0.214 |      0.15  |       0.279 |         14 | growth      |         3 |
| equal_weights                   | precision@10 |  0.571 |      0.429 |       0.721 |         14 | growth      |         3 |
| gravity_ppml                    | precision@10 |  0.143 |      0.1   |       0.186 |         14 | growth      |         3 |
| import_volume                   | precision@10 |  0.1   |      0.043 |       0.171 |         14 | growth      |         3 |
| promethee_ii|minmax|expert_mean | precision@10 |  0.579 |      0.429 |       0.729 |         14 | growth      |         3 |
| random                          | precision@10 |  0.174 |      0.167 |       0.179 |         14 | growth      |         3 |
| topsis|minmax|expert_mean       | precision@10 |  0.6   |      0.464 |       0.743 |         14 | growth      |         3 |
| vikor|minmax|expert_mean        | precision@10 |  0.593 |      0.457 |       0.743 |         14 | growth      |         3 |
| wsm|minmax|equal                | precision@10 |  0.571 |      0.429 |       0.721 |         14 | growth      |         3 |
| wsm|minmax|expert_mean          | precision@10 |  0.586 |      0.443 |       0.743 |         14 | growth      |         3 |
| wsm|minmax|learned              | precision@10 |  0.571 |      0.443 |       0.721 |         14 | growth      |         3 |
| ml_gbm                          | ndcg@10      |  0.73  |      0.672 |       0.783 |         28 | nan         |           |
| ml_gbm                          | spearman     |  0.093 |     -0.017 |       0.198 |         28 | nan         |           |
| ml_gbm                          | precision@10 |  0.682 |      0.55  |       0.804 |         28 | nan         |           |
| ml_gbm                          | auc          |  0.578 |      0.49  |       0.658 |         24 | nan         |           |

## Booktabs (copy into manuscript; not a repo .tex file)

```latex
\begin{table}[htbp]
\centering
\caption{T4. Predictive validation metrics (bootstrap means and 95% CIs)}
\label{tab:T4_predictive_metrics}
\begin{tabular}{llllllll}
\toprule
method & metric & mean & ci95\_low & ci95\_high & n\_blocks & target & horizon \\
\midrule
eoc & ndcg@10 & 0.702 & 0.651 & 0.751 & 28 & intensive & 1.000 \\
equal\_weights & ndcg@10 & 0.838 & 0.801 & 0.874 & 28 & intensive & 1.000 \\
gravity\_ppml & ndcg@10 & 0.755 & 0.705 & 0.805 & 28 & intensive & 1.000 \\
import\_volume & ndcg@10 & 0.745 & 0.696 & 0.795 & 28 & intensive & 1.000 \\
promethee\_ii|minmax|expert\_mean & ndcg@10 & 0.837 & 0.800 & 0.871 & 28 & intensive & 1.000 \\
random & ndcg@10 & 0.718 & 0.674 & 0.761 & 28 & intensive & 1.000 \\
topsis|minmax|expert\_mean & ndcg@10 & 0.847 & 0.816 & 0.880 & 28 & intensive & 1.000 \\
vikor|minmax|expert\_mean & ndcg@10 & 0.842 & 0.807 & 0.874 & 28 & intensive & 1.000 \\
wsm|minmax|equal & ndcg@10 & 0.838 & 0.802 & 0.872 & 28 & intensive & 1.000 \\
wsm|minmax|expert\_mean & ndcg@10 & 0.834 & 0.799 & 0.869 & 28 & intensive & 1.000 \\
wsm|minmax|learned & ndcg@10 & 0.842 & 0.807 & 0.878 & 28 & intensive & 1.000 \\
eoc & spearman & -0.051 & -0.179 & 0.072 & 28 & intensive & 1.000 \\
equal\_weights & spearman & 0.012 & -0.169 & 0.200 & 27 & intensive & 1.000 \\
gravity\_ppml & spearman & 0.123 & -0.017 & 0.258 & 28 & intensive & 1.000 \\
import\_volume & spearman & 0.040 & -0.091 & 0.160 & 28 & intensive & 1.000 \\
promethee\_ii|minmax|expert\_mean & spearman & -0.001 & -0.177 & 0.169 & 27 & intensive & 1.000 \\
random & spearman & -0.003 & -0.025 & 0.016 & 28 & intensive & 1.000 \\
topsis|minmax|expert\_mean & spearman & 0.012 & -0.166 & 0.185 & 27 & intensive & 1.000 \\
vikor|minmax|expert\_mean & spearman & 0.001 & -0.170 & 0.174 & 27 & intensive & 1.000 \\
wsm|minmax|equal & spearman & 0.012 & -0.161 & 0.181 & 27 & intensive & 1.000 \\
wsm|minmax|expert\_mean & spearman & -0.009 & -0.168 & 0.173 & 27 & intensive & 1.000 \\
wsm|minmax|learned & spearman & 0.007 & -0.167 & 0.177 & 27 & intensive & 1.000 \\
eoc & precision@10 & 0.704 & 0.586 & 0.807 & 28 & intensive & 1.000 \\
equal\_weights & precision@10 & 0.904 & 0.836 & 0.964 & 28 & intensive & 1.000 \\
gravity\_ppml & precision@10 & 0.718 & 0.604 & 0.829 & 28 & intensive & 1.000 \\
import\_volume & precision@10 & 0.696 & 0.578 & 0.818 & 28 & intensive & 1.000 \\
promethee\_ii|minmax|expert\_mean & precision@10 & 0.904 & 0.836 & 0.961 & 28 & intensive & 1.000 \\
random & precision@10 & 0.691 & 0.571 & 0.805 & 28 & intensive & 1.000 \\
topsis|minmax|expert\_mean & precision@10 & 0.911 & 0.846 & 0.964 & 28 & intensive & 1.000 \\
vikor|minmax|expert\_mean & precision@10 & 0.911 & 0.846 & 0.964 & 28 & intensive & 1.000 \\
wsm|minmax|equal & precision@10 & 0.904 & 0.836 & 0.964 & 28 & intensive & 1.000 \\
wsm|minmax|expert\_mean & precision@10 & 0.904 & 0.832 & 0.961 & 28 & intensive & 1.000 \\
wsm|minmax|learned & precision@10 & 0.911 & 0.846 & 0.964 & 28 & intensive & 1.000 \\
eoc & auc & 0.409 & 0.318 & 0.496 & 24 & intensive & 1.000 \\
equal\_weights & auc & 0.482 & 0.365 & 0.599 & 17 & intensive & 1.000 \\
gravity\_ppml & auc & 0.529 & 0.442 & 0.604 & 24 & intensive & 1.000 \\
import\_volume & auc & 0.627 & 0.530 & 0.715 & 24 & intensive & 1.000 \\
promethee\_ii|minmax|expert\_mean & auc & 0.458 & 0.348 & 0.563 & 17 & intensive & 1.000 \\
random & auc & 0.490 & 0.478 & 0.500 & 24 & intensive & 1.000 \\
topsis|minmax|expert\_mean & auc & 0.489 & 0.369 & 0.609 & 17 & intensive & 1.000 \\
vikor|minmax|expert\_mean & auc & 0.505 & 0.399 & 0.614 & 17 & intensive & 1.000 \\
wsm|minmax|equal & auc & 0.482 & 0.360 & 0.598 & 17 & intensive & 1.000 \\
wsm|minmax|expert\_mean & auc & 0.481 & 0.355 & 0.594 & 17 & intensive & 1.000 \\
wsm|minmax|learned & auc & 0.487 & 0.345 & 0.619 & 17 & intensive & 1.000 \\
eoc & ndcg@10 & 0.676 & 0.641 & 0.710 & 25 & new\_markets & 1.000 \\
equal\_weights & ndcg@10 & 0.879 & 0.842 & 0.912 & 21 & new\_markets & 1.000 \\
gravity\_ppml & ndcg@10 & 0.682 & 0.644 & 0.719 & 25 & new\_markets & 1.000 \\
import\_volume & ndcg@10 & 0.722 & 0.691 & 0.752 & 25 & new\_markets & 1.000 \\
promethee\_ii|minmax|expert\_mean & ndcg@10 & 0.876 & 0.837 & 0.914 & 21 & new\_markets & 1.000 \\
random & ndcg@10 & 0.583 & 0.576 & 0.593 & 25 & new\_markets & 1.000 \\
topsis|minmax|expert\_mean & ndcg@10 & 0.871 & 0.833 & 0.911 & 21 & new\_markets & 1.000 \\
vikor|minmax|expert\_mean & ndcg@10 & 0.887 & 0.849 & 0.923 & 21 & new\_markets & 1.000 \\
wsm|minmax|equal & ndcg@10 & 0.879 & 0.843 & 0.915 & 21 & new\_markets & 1.000 \\
wsm|minmax|expert\_mean & ndcg@10 & 0.867 & 0.826 & 0.906 & 21 & new\_markets & 1.000 \\
wsm|minmax|learned & ndcg@10 & 0.875 & 0.839 & 0.909 & 21 & new\_markets & 1.000 \\
eoc & spearman & 0.122 & 0.057 & 0.187 & 25 & new\_markets & 1.000 \\
equal\_weights & spearman & 0.236 & 0.127 & 0.341 & 17 & new\_markets & 1.000 \\
gravity\_ppml & spearman & 0.292 & 0.224 & 0.359 & 25 & new\_markets & 1.000 \\
import\_volume & spearman & 0.395 & 0.352 & 0.439 & 25 & new\_markets & 1.000 \\
promethee\_ii|minmax|expert\_mean & spearman & 0.212 & 0.081 & 0.348 & 17 & new\_markets & 1.000 \\
random & spearman & -0.011 & -0.020 & -0.002 & 25 & new\_markets & 1.000 \\
topsis|minmax|expert\_mean & spearman & 0.234 & 0.114 & 0.354 & 17 & new\_markets & 1.000 \\
vikor|minmax|expert\_mean & spearman & 0.323 & 0.205 & 0.443 & 17 & new\_markets & 1.000 \\
wsm|minmax|equal & spearman & 0.236 & 0.122 & 0.344 & 17 & new\_markets & 1.000 \\
wsm|minmax|expert\_mean & spearman & 0.188 & 0.069 & 0.307 & 17 & new\_markets & 1.000 \\
wsm|minmax|learned & spearman & 0.251 & 0.144 & 0.361 & 17 & new\_markets & 1.000 \\
eoc & precision@10 & 0.396 & 0.348 & 0.450 & 25 & new\_markets & 1.000 \\
equal\_weights & precision@10 & 0.848 & 0.796 & 0.895 & 21 & new\_markets & 1.000 \\
gravity\_ppml & precision@10 & 0.464 & 0.404 & 0.525 & 25 & new\_markets & 1.000 \\
import\_volume & precision@10 & 0.532 & 0.493 & 0.571 & 25 & new\_markets & 1.000 \\
promethee\_ii|minmax|expert\_mean & precision@10 & 0.838 & 0.784 & 0.888 & 21 & new\_markets & 1.000 \\
random & precision@10 & 0.332 & 0.327 & 0.337 & 25 & new\_markets & 1.000 \\
topsis|minmax|expert\_mean & precision@10 & 0.843 & 0.792 & 0.895 & 21 & new\_markets & 1.000 \\
vikor|minmax|expert\_mean & precision@10 & 0.852 & 0.800 & 0.905 & 21 & new\_markets & 1.000 \\
wsm|minmax|equal & precision@10 & 0.848 & 0.796 & 0.896 & 21 & new\_markets & 1.000 \\
wsm|minmax|expert\_mean & precision@10 & 0.848 & 0.795 & 0.895 & 21 & new\_markets & 1.000 \\
wsm|minmax|learned & precision@10 & 0.843 & 0.791 & 0.895 & 21 & new\_markets & 1.000 \\
eoc & ndcg@10 & 0.536 & 0.491 & 0.581 & 28 & growth & 1.000 \\
equal\_weights & ndcg@10 & 0.681 & 0.626 & 0.740 & 28 & growth & 1.000 \\
gravity\_ppml & ndcg@10 & 0.550 & 0.510 & 0.588 & 28 & growth & 1.000 \\
import\_volume & ndcg@10 & 0.547 & 0.515 & 0.580 & 28 & growth & 1.000 \\
promethee\_ii|minmax|expert\_mean & ndcg@10 & 0.680 & 0.635 & 0.731 & 28 & growth & 1.000 \\
random & ndcg@10 & 0.541 & 0.537 & 0.545 & 28 & growth & 1.000 \\
topsis|minmax|expert\_mean & ndcg@10 & 0.686 & 0.635 & 0.739 & 28 & growth & 1.000 \\
vikor|minmax|expert\_mean & ndcg@10 & 0.682 & 0.636 & 0.732 & 28 & growth & 1.000 \\
wsm|minmax|equal & ndcg@10 & 0.681 & 0.625 & 0.742 & 28 & growth & 1.000 \\
wsm|minmax|expert\_mean & ndcg@10 & 0.683 & 0.630 & 0.740 & 28 & growth & 1.000 \\
wsm|minmax|learned & ndcg@10 & 0.680 & 0.626 & 0.737 & 28 & growth & 1.000 \\
eoc & spearman & 0.014 & -0.033 & 0.060 & 28 & growth & 1.000 \\
equal\_weights & spearman & 0.042 & -0.066 & 0.154 & 28 & growth & 1.000 \\
gravity\_ppml & spearman & 0.028 & -0.039 & 0.096 & 28 & growth & 1.000 \\
import\_volume & spearman & 0.004 & -0.045 & 0.054 & 28 & growth & 1.000 \\
promethee\_ii|minmax|expert\_mean & spearman & 0.025 & -0.069 & 0.122 & 28 & growth & 1.000 \\
random & spearman & 0.001 & -0.004 & 0.006 & 28 & growth & 1.000 \\
topsis|minmax|expert\_mean & spearman & 0.042 & -0.056 & 0.140 & 28 & growth & 1.000 \\
vikor|minmax|expert\_mean & spearman & 0.034 & -0.067 & 0.129 & 28 & growth & 1.000 \\
wsm|minmax|equal & spearman & 0.042 & -0.068 & 0.149 & 28 & growth & 1.000 \\
wsm|minmax|expert\_mean & spearman & 0.038 & -0.068 & 0.140 & 28 & growth & 1.000 \\
wsm|minmax|learned & spearman & 0.005 & -0.113 & 0.113 & 28 & growth & 1.000 \\
eoc & precision@10 & 0.193 & 0.154 & 0.236 & 28 & growth & 1.000 \\
equal\_weights & precision@10 & 0.529 & 0.411 & 0.646 & 28 & growth & 1.000 \\
gravity\_ppml & precision@10 & 0.139 & 0.096 & 0.189 & 28 & growth & 1.000 \\
import\_volume & precision@10 & 0.125 & 0.089 & 0.164 & 28 & growth & 1.000 \\
promethee\_ii|minmax|expert\_mean & precision@10 & 0.539 & 0.425 & 0.661 & 28 & growth & 1.000 \\
random & precision@10 & 0.169 & 0.166 & 0.172 & 28 & growth & 1.000 \\
topsis|minmax|expert\_mean & precision@10 & 0.536 & 0.414 & 0.657 & 28 & growth & 1.000 \\
vikor|minmax|expert\_mean & precision@10 & 0.536 & 0.429 & 0.657 & 28 & growth & 1.000 \\
wsm|minmax|equal & precision@10 & 0.529 & 0.411 & 0.654 & 28 & growth & 1.000 \\
wsm|minmax|expert\_mean & precision@10 & 0.529 & 0.411 & 0.654 & 28 & growth & 1.000 \\
wsm|minmax|learned & precision@10 & 0.525 & 0.400 & 0.650 & 28 & growth & 1.000 \\
eoc & ndcg@10 & 0.688 & 0.626 & 0.741 & 14 & intensive & 3.000 \\
equal\_weights & ndcg@10 & 0.868 & 0.832 & 0.908 & 14 & intensive & 3.000 \\
gravity\_ppml & ndcg@10 & 0.806 & 0.732 & 0.873 & 14 & intensive & 3.000 \\
import\_volume & ndcg@10 & 0.745 & 0.691 & 0.801 & 14 & intensive & 3.000 \\
promethee\_ii|minmax|expert\_mean & ndcg@10 & 0.853 & 0.819 & 0.891 & 14 & intensive & 3.000 \\
random & ndcg@10 & 0.718 & 0.659 & 0.777 & 14 & intensive & 3.000 \\
topsis|minmax|expert\_mean & ndcg@10 & 0.862 & 0.822 & 0.905 & 14 & intensive & 3.000 \\
vikor|minmax|expert\_mean & ndcg@10 & 0.848 & 0.813 & 0.881 & 14 & intensive & 3.000 \\
wsm|minmax|equal & ndcg@10 & 0.868 & 0.832 & 0.907 & 14 & intensive & 3.000 \\
wsm|minmax|expert\_mean & ndcg@10 & 0.862 & 0.824 & 0.905 & 14 & intensive & 3.000 \\
wsm|minmax|learned & ndcg@10 & 0.865 & 0.819 & 0.909 & 14 & intensive & 3.000 \\
eoc & spearman & -0.133 & -0.243 & -0.024 & 14 & intensive & 3.000 \\
equal\_weights & spearman & 0.023 & -0.228 & 0.266 & 13 & intensive & 3.000 \\
gravity\_ppml & spearman & 0.329 & 0.171 & 0.483 & 14 & intensive & 3.000 \\
import\_volume & spearman & -0.005 & -0.220 & 0.186 & 14 & intensive & 3.000 \\
promethee\_ii|minmax|expert\_mean & spearman & 0.033 & -0.199 & 0.267 & 13 & intensive & 3.000 \\
random & spearman & 0.007 & -0.021 & 0.034 & 14 & intensive & 3.000 \\
topsis|minmax|expert\_mean & spearman & 0.046 & -0.236 & 0.334 & 13 & intensive & 3.000 \\
vikor|minmax|expert\_mean & spearman & -0.006 & -0.279 & 0.243 & 13 & intensive & 3.000 \\
wsm|minmax|equal & spearman & 0.023 & -0.225 & 0.268 & 13 & intensive & 3.000 \\
wsm|minmax|expert\_mean & spearman & 0.059 & -0.221 & 0.323 & 13 & intensive & 3.000 \\
wsm|minmax|learned & spearman & 0.066 & -0.175 & 0.285 & 13 & intensive & 3.000 \\
eoc & precision@10 & 0.707 & 0.557 & 0.843 & 14 & intensive & 3.000 \\
equal\_weights & precision@10 & 0.929 & 0.850 & 0.986 & 14 & intensive & 3.000 \\
gravity\_ppml & precision@10 & 0.729 & 0.571 & 0.879 & 14 & intensive & 3.000 \\
import\_volume & precision@10 & 0.686 & 0.507 & 0.836 & 14 & intensive & 3.000 \\
promethee\_ii|minmax|expert\_mean & precision@10 & 0.936 & 0.864 & 0.986 & 14 & intensive & 3.000 \\
random & precision@10 & 0.691 & 0.531 & 0.839 & 14 & intensive & 3.000 \\
topsis|minmax|expert\_mean & precision@10 & 0.921 & 0.843 & 0.993 & 14 & intensive & 3.000 \\
vikor|minmax|expert\_mean & precision@10 & 0.921 & 0.843 & 0.986 & 14 & intensive & 3.000 \\
wsm|minmax|equal & precision@10 & 0.929 & 0.864 & 0.986 & 14 & intensive & 3.000 \\
wsm|minmax|expert\_mean & precision@10 & 0.921 & 0.843 & 0.986 & 14 & intensive & 3.000 \\
wsm|minmax|learned & precision@10 & 0.929 & 0.857 & 0.986 & 14 & intensive & 3.000 \\
eoc & auc & 0.399 & 0.287 & 0.502 & 12 & intensive & 3.000 \\
equal\_weights & auc & 0.482 & 0.326 & 0.609 & 9 & intensive & 3.000 \\
gravity\_ppml & auc & 0.526 & 0.411 & 0.628 & 12 & intensive & 3.000 \\
import\_volume & auc & 0.610 & 0.454 & 0.746 & 12 & intensive & 3.000 \\
promethee\_ii|minmax|expert\_mean & auc & 0.468 & 0.328 & 0.572 & 9 & intensive & 3.000 \\
random & auc & 0.487 & 0.473 & 0.499 & 12 & intensive & 3.000 \\
topsis|minmax|expert\_mean & auc & 0.478 & 0.331 & 0.599 & 9 & intensive & 3.000 \\
vikor|minmax|expert\_mean & auc & 0.504 & 0.362 & 0.625 & 9 & intensive & 3.000 \\
wsm|minmax|equal & auc & 0.482 & 0.336 & 0.606 & 9 & intensive & 3.000 \\
wsm|minmax|expert\_mean & auc & 0.488 & 0.341 & 0.606 & 9 & intensive & 3.000 \\
wsm|minmax|learned & auc & 0.514 & 0.354 & 0.662 & 9 & intensive & 3.000 \\
eoc & ndcg@10 & 0.682 & 0.643 & 0.719 & 13 & new\_markets & 3.000 \\
equal\_weights & ndcg@10 & 0.878 & 0.841 & 0.919 & 11 & new\_markets & 3.000 \\
gravity\_ppml & ndcg@10 & 0.709 & 0.670 & 0.746 & 13 & new\_markets & 3.000 \\
import\_volume & ndcg@10 & 0.724 & 0.683 & 0.763 & 13 & new\_markets & 3.000 \\
promethee\_ii|minmax|expert\_mean & ndcg@10 & 0.880 & 0.835 & 0.928 & 11 & new\_markets & 3.000 \\
random & ndcg@10 & 0.587 & 0.575 & 0.604 & 13 & new\_markets & 3.000 \\
topsis|minmax|expert\_mean & ndcg@10 & 0.879 & 0.845 & 0.921 & 11 & new\_markets & 3.000 \\
vikor|minmax|expert\_mean & ndcg@10 & 0.895 & 0.857 & 0.934 & 11 & new\_markets & 3.000 \\
wsm|minmax|equal & ndcg@10 & 0.878 & 0.840 & 0.923 & 11 & new\_markets & 3.000 \\
wsm|minmax|expert\_mean & ndcg@10 & 0.868 & 0.826 & 0.915 & 11 & new\_markets & 3.000 \\
wsm|minmax|learned & ndcg@10 & 0.886 & 0.845 & 0.929 & 11 & new\_markets & 3.000 \\
eoc & spearman & 0.121 & 0.034 & 0.201 & 13 & new\_markets & 3.000 \\
equal\_weights & spearman & 0.267 & 0.187 & 0.358 & 9 & new\_markets & 3.000 \\
gravity\_ppml & spearman & 0.312 & 0.245 & 0.377 & 13 & new\_markets & 3.000 \\
import\_volume & spearman & 0.409 & 0.373 & 0.444 & 13 & new\_markets & 3.000 \\
promethee\_ii|minmax|expert\_mean & spearman & 0.242 & 0.113 & 0.390 & 9 & new\_markets & 3.000 \\
random & spearman & -0.014 & -0.026 & -0.001 & 13 & new\_markets & 3.000 \\
topsis|minmax|expert\_mean & spearman & 0.291 & 0.222 & 0.363 & 9 & new\_markets & 3.000 \\
vikor|minmax|expert\_mean & spearman & 0.400 & 0.328 & 0.473 & 9 & new\_markets & 3.000 \\
wsm|minmax|equal & spearman & 0.267 & 0.190 & 0.357 & 9 & new\_markets & 3.000 \\
wsm|minmax|expert\_mean & spearman & 0.214 & 0.144 & 0.275 & 9 & new\_markets & 3.000 \\
wsm|minmax|learned & spearman & 0.299 & 0.213 & 0.373 & 9 & new\_markets & 3.000 \\
eoc & precision@10 & 0.385 & 0.321 & 0.454 & 13 & new\_markets & 3.000 \\
equal\_weights & precision@10 & 0.882 & 0.833 & 0.933 & 11 & new\_markets & 3.000 \\
gravity\_ppml & precision@10 & 0.462 & 0.400 & 0.525 & 13 & new\_markets & 3.000 \\
import\_volume & precision@10 & 0.508 & 0.454 & 0.558 & 13 & new\_markets & 3.000 \\
promethee\_ii|minmax|expert\_mean & precision@10 & 0.873 & 0.822 & 0.925 & 11 & new\_markets & 3.000 \\
random & precision@10 & 0.326 & 0.320 & 0.331 & 13 & new\_markets & 3.000 \\
topsis|minmax|expert\_mean & precision@10 & 0.882 & 0.833 & 0.933 & 11 & new\_markets & 3.000 \\
vikor|minmax|expert\_mean & precision@10 & 0.900 & 0.850 & 0.950 & 11 & new\_markets & 3.000 \\
wsm|minmax|equal & precision@10 & 0.882 & 0.833 & 0.933 & 11 & new\_markets & 3.000 \\
wsm|minmax|expert\_mean & precision@10 & 0.882 & 0.833 & 0.936 & 11 & new\_markets & 3.000 \\
wsm|minmax|learned & precision@10 & 0.864 & 0.800 & 0.927 & 11 & new\_markets & 3.000 \\
eoc & ndcg@10 & 0.539 & 0.481 & 0.601 & 14 & growth & 3.000 \\
equal\_weights & ndcg@10 & 0.730 & 0.657 & 0.802 & 14 & growth & 3.000 \\
gravity\_ppml & ndcg@10 & 0.583 & 0.523 & 0.634 & 14 & growth & 3.000 \\
import\_volume & ndcg@10 & 0.553 & 0.515 & 0.587 & 14 & growth & 3.000 \\
promethee\_ii|minmax|expert\_mean & ndcg@10 & 0.731 & 0.669 & 0.794 & 14 & growth & 3.000 \\
random & ndcg@10 & 0.541 & 0.536 & 0.545 & 14 & growth & 3.000 \\
topsis|minmax|expert\_mean & ndcg@10 & 0.732 & 0.669 & 0.796 & 14 & growth & 3.000 \\
vikor|minmax|expert\_mean & ndcg@10 & 0.725 & 0.667 & 0.783 & 14 & growth & 3.000 \\
wsm|minmax|equal & ndcg@10 & 0.730 & 0.655 & 0.802 & 14 & growth & 3.000 \\
wsm|minmax|expert\_mean & ndcg@10 & 0.733 & 0.660 & 0.805 & 14 & growth & 3.000 \\
wsm|minmax|learned & ndcg@10 & 0.718 & 0.648 & 0.789 & 14 & growth & 3.000 \\
eoc & spearman & 0.015 & -0.033 & 0.062 & 14 & growth & 3.000 \\
equal\_weights & spearman & 0.073 & -0.104 & 0.240 & 14 & growth & 3.000 \\
gravity\_ppml & spearman & 0.113 & 0.039 & 0.180 & 14 & growth & 3.000 \\
import\_volume & spearman & 0.021 & -0.055 & 0.092 & 14 & growth & 3.000 \\
promethee\_ii|minmax|expert\_mean & spearman & 0.086 & -0.051 & 0.234 & 14 & growth & 3.000 \\
random & spearman & 0.001 & -0.005 & 0.007 & 14 & growth & 3.000 \\
topsis|minmax|expert\_mean & spearman & 0.059 & -0.154 & 0.245 & 14 & growth & 3.000 \\
vikor|minmax|expert\_mean & spearman & 0.075 & -0.108 & 0.252 & 14 & growth & 3.000 \\
wsm|minmax|equal & spearman & 0.073 & -0.104 & 0.238 & 14 & growth & 3.000 \\
wsm|minmax|expert\_mean & spearman & 0.085 & -0.094 & 0.258 & 14 & growth & 3.000 \\
wsm|minmax|learned & spearman & 0.102 & 0.025 & 0.174 & 14 & growth & 3.000 \\
eoc & precision@10 & 0.214 & 0.150 & 0.279 & 14 & growth & 3.000 \\
equal\_weights & precision@10 & 0.571 & 0.429 & 0.721 & 14 & growth & 3.000 \\
gravity\_ppml & precision@10 & 0.143 & 0.100 & 0.186 & 14 & growth & 3.000 \\
import\_volume & precision@10 & 0.100 & 0.043 & 0.171 & 14 & growth & 3.000 \\
promethee\_ii|minmax|expert\_mean & precision@10 & 0.579 & 0.429 & 0.729 & 14 & growth & 3.000 \\
random & precision@10 & 0.174 & 0.167 & 0.179 & 14 & growth & 3.000 \\
topsis|minmax|expert\_mean & precision@10 & 0.600 & 0.464 & 0.743 & 14 & growth & 3.000 \\
vikor|minmax|expert\_mean & precision@10 & 0.593 & 0.457 & 0.743 & 14 & growth & 3.000 \\
wsm|minmax|equal & precision@10 & 0.571 & 0.429 & 0.721 & 14 & growth & 3.000 \\
wsm|minmax|expert\_mean & precision@10 & 0.586 & 0.443 & 0.743 & 14 & growth & 3.000 \\
wsm|minmax|learned & precision@10 & 0.571 & 0.443 & 0.721 & 14 & growth & 3.000 \\
ml\_gbm & ndcg@10 & 0.730 & 0.672 & 0.783 & 28 & nan &  \\
ml\_gbm & spearman & 0.093 & -0.017 & 0.198 & 28 & nan &  \\
ml\_gbm & precision@10 & 0.682 & 0.550 & 0.804 & 28 & nan &  \\
ml\_gbm & auc & 0.578 & 0.490 & 0.658 & 24 & nan &  \\
\bottomrule
\end{tabular}
\end{table}
```
