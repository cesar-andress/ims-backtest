# T4. Predictive validation metrics (bootstrap means and 95% CIs)

| method                          | metric       |   mean |   ci95_low |   ci95_high |   n_blocks | target      |   horizon |
|:--------------------------------|:-------------|-------:|-----------:|------------:|-----------:|:------------|----------:|
| eoc                             | ndcg@10      |  0.702 |      0.651 |       0.751 |         28 | intensive   |         1 |
| equal_weights                   | ndcg@10      |  0.737 |      0.689 |       0.783 |         28 | intensive   |         1 |
| gravity_ppml                    | ndcg@10      |  0.755 |      0.705 |       0.805 |         28 | intensive   |         1 |
| import_volume                   | ndcg@10      |  0.745 |      0.696 |       0.795 |         28 | intensive   |         1 |
| promethee_ii|minmax|expert_mean | ndcg@10      |  0.751 |      0.707 |       0.794 |         28 | intensive   |         1 |
| random                          | ndcg@10      |  0.718 |      0.674 |       0.761 |         28 | intensive   |         1 |
| topsis|minmax|expert_mean       | ndcg@10      |  0.734 |      0.688 |       0.78  |         28 | intensive   |         1 |
| vikor|minmax|expert_mean        | ndcg@10      |  0.732 |      0.688 |       0.775 |         28 | intensive   |         1 |
| wsm|minmax|equal                | ndcg@10      |  0.737 |      0.688 |       0.783 |         28 | intensive   |         1 |
| wsm|minmax|expert_mean          | ndcg@10      |  0.738 |      0.685 |       0.789 |         28 | intensive   |         1 |
| wsm|minmax|learned              | ndcg@10      |  0.748 |      0.697 |       0.794 |         28 | intensive   |         1 |
| eoc                             | spearman     | -0.051 |     -0.179 |       0.072 |         28 | intensive   |         1 |
| equal_weights                   | spearman     |  0.028 |     -0.114 |       0.169 |         28 | intensive   |         1 |
| gravity_ppml                    | spearman     |  0.123 |     -0.017 |       0.258 |         28 | intensive   |         1 |
| import_volume                   | spearman     |  0.04  |     -0.091 |       0.16  |         28 | intensive   |         1 |
| promethee_ii|minmax|expert_mean | spearman     |  0.076 |     -0.072 |       0.213 |         28 | intensive   |         1 |
| random                          | spearman     | -0.003 |     -0.025 |       0.016 |         28 | intensive   |         1 |
| topsis|minmax|expert_mean       | spearman     |  0.043 |     -0.094 |       0.175 |         28 | intensive   |         1 |
| vikor|minmax|expert_mean        | spearman     |  0.024 |     -0.112 |       0.158 |         28 | intensive   |         1 |
| wsm|minmax|equal                | spearman     |  0.028 |     -0.118 |       0.164 |         28 | intensive   |         1 |
| wsm|minmax|expert_mean          | spearman     |  0.041 |     -0.086 |       0.18  |         28 | intensive   |         1 |
| wsm|minmax|learned              | spearman     |  0.073 |     -0.066 |       0.196 |         28 | intensive   |         1 |
| eoc                             | precision@10 |  0.704 |      0.586 |       0.807 |         28 | intensive   |         1 |
| equal_weights                   | precision@10 |  0.707 |      0.586 |       0.814 |         28 | intensive   |         1 |
| gravity_ppml                    | precision@10 |  0.718 |      0.604 |       0.829 |         28 | intensive   |         1 |
| import_volume                   | precision@10 |  0.696 |      0.578 |       0.818 |         28 | intensive   |         1 |
| promethee_ii|minmax|expert_mean | precision@10 |  0.725 |      0.618 |       0.832 |         28 | intensive   |         1 |
| random                          | precision@10 |  0.691 |      0.571 |       0.805 |         28 | intensive   |         1 |
| topsis|minmax|expert_mean       | precision@10 |  0.714 |      0.596 |       0.825 |         28 | intensive   |         1 |
| vikor|minmax|expert_mean        | precision@10 |  0.711 |      0.593 |       0.814 |         28 | intensive   |         1 |
| wsm|minmax|equal                | precision@10 |  0.707 |      0.589 |       0.814 |         28 | intensive   |         1 |
| wsm|minmax|expert_mean          | precision@10 |  0.711 |      0.593 |       0.825 |         28 | intensive   |         1 |
| wsm|minmax|learned              | precision@10 |  0.707 |      0.582 |       0.814 |         28 | intensive   |         1 |
| eoc                             | auc          |  0.409 |      0.318 |       0.496 |         24 | intensive   |         1 |
| equal_weights                   | auc          |  0.546 |      0.444 |       0.645 |         24 | intensive   |         1 |
| gravity_ppml                    | auc          |  0.529 |      0.442 |       0.604 |         24 | intensive   |         1 |
| import_volume                   | auc          |  0.627 |      0.53  |       0.715 |         24 | intensive   |         1 |
| promethee_ii|minmax|expert_mean | auc          |  0.528 |      0.432 |       0.611 |         24 | intensive   |         1 |
| random                          | auc          |  0.49  |      0.478 |       0.5   |         24 | intensive   |         1 |
| topsis|minmax|expert_mean       | auc          |  0.534 |      0.445 |       0.618 |         24 | intensive   |         1 |
| vikor|minmax|expert_mean        | auc          |  0.521 |      0.429 |       0.611 |         24 | intensive   |         1 |
| wsm|minmax|equal                | auc          |  0.546 |      0.446 |       0.636 |         24 | intensive   |         1 |
| wsm|minmax|expert_mean          | auc          |  0.535 |      0.435 |       0.628 |         24 | intensive   |         1 |
| wsm|minmax|learned              | auc          |  0.53  |      0.435 |       0.622 |         24 | intensive   |         1 |
| eoc                             | ndcg@10      |  0.676 |      0.641 |       0.71  |         25 | new_markets |         1 |
| equal_weights                   | ndcg@10      |  0.736 |      0.697 |       0.773 |         25 | new_markets |         1 |
| gravity_ppml                    | ndcg@10      |  0.682 |      0.644 |       0.719 |         25 | new_markets |         1 |
| import_volume                   | ndcg@10      |  0.722 |      0.691 |       0.752 |         25 | new_markets |         1 |
| promethee_ii|minmax|expert_mean | ndcg@10      |  0.726 |      0.697 |       0.755 |         25 | new_markets |         1 |
| random                          | ndcg@10      |  0.583 |      0.576 |       0.593 |         25 | new_markets |         1 |
| topsis|minmax|expert_mean       | ndcg@10      |  0.738 |      0.698 |       0.774 |         25 | new_markets |         1 |
| vikor|minmax|expert_mean        | ndcg@10      |  0.725 |      0.689 |       0.757 |         25 | new_markets |         1 |
| wsm|minmax|equal                | ndcg@10      |  0.736 |      0.699 |       0.775 |         25 | new_markets |         1 |
| wsm|minmax|expert_mean          | ndcg@10      |  0.723 |      0.684 |       0.76  |         25 | new_markets |         1 |
| wsm|minmax|learned              | ndcg@10      |  0.732 |      0.691 |       0.769 |         25 | new_markets |         1 |
| eoc                             | spearman     |  0.122 |      0.057 |       0.187 |         25 | new_markets |         1 |
| equal_weights                   | spearman     |  0.369 |      0.304 |       0.43  |         25 | new_markets |         1 |
| gravity_ppml                    | spearman     |  0.292 |      0.224 |       0.359 |         25 | new_markets |         1 |
| import_volume                   | spearman     |  0.395 |      0.352 |       0.439 |         25 | new_markets |         1 |
| promethee_ii|minmax|expert_mean | spearman     |  0.328 |      0.272 |       0.385 |         25 | new_markets |         1 |
| random                          | spearman     | -0.011 |     -0.02  |      -0.002 |         25 | new_markets |         1 |
| topsis|minmax|expert_mean       | spearman     |  0.363 |      0.299 |       0.419 |         25 | new_markets |         1 |
| vikor|minmax|expert_mean        | spearman     |  0.366 |      0.306 |       0.424 |         25 | new_markets |         1 |
| wsm|minmax|equal                | spearman     |  0.369 |      0.307 |       0.432 |         25 | new_markets |         1 |
| wsm|minmax|expert_mean          | spearman     |  0.348 |      0.28  |       0.41  |         25 | new_markets |         1 |
| wsm|minmax|learned              | spearman     |  0.338 |      0.271 |       0.4   |         25 | new_markets |         1 |
| eoc                             | precision@10 |  0.396 |      0.348 |       0.45  |         25 | new_markets |         1 |
| equal_weights                   | precision@10 |  0.436 |      0.383 |       0.488 |         25 | new_markets |         1 |
| gravity_ppml                    | precision@10 |  0.464 |      0.404 |       0.525 |         25 | new_markets |         1 |
| import_volume                   | precision@10 |  0.532 |      0.493 |       0.571 |         25 | new_markets |         1 |
| promethee_ii|minmax|expert_mean | precision@10 |  0.44  |      0.389 |       0.492 |         25 | new_markets |         1 |
| random                          | precision@10 |  0.332 |      0.327 |       0.337 |         25 | new_markets |         1 |
| topsis|minmax|expert_mean       | precision@10 |  0.452 |      0.396 |       0.504 |         25 | new_markets |         1 |
| vikor|minmax|expert_mean        | precision@10 |  0.456 |      0.396 |       0.516 |         25 | new_markets |         1 |
| wsm|minmax|equal                | precision@10 |  0.436 |      0.384 |       0.488 |         25 | new_markets |         1 |
| wsm|minmax|expert_mean          | precision@10 |  0.428 |      0.375 |       0.473 |         25 | new_markets |         1 |
| wsm|minmax|learned              | precision@10 |  0.44  |      0.387 |       0.488 |         25 | new_markets |         1 |
| eoc                             | ndcg@10      |  0.536 |      0.491 |       0.581 |         28 | growth      |         1 |
| equal_weights                   | ndcg@10      |  0.576 |      0.54  |       0.615 |         28 | growth      |         1 |
| gravity_ppml                    | ndcg@10      |  0.55  |      0.51  |       0.588 |         28 | growth      |         1 |
| import_volume                   | ndcg@10      |  0.547 |      0.515 |       0.58  |         28 | growth      |         1 |
| promethee_ii|minmax|expert_mean | ndcg@10      |  0.572 |      0.536 |       0.611 |         28 | growth      |         1 |
| random                          | ndcg@10      |  0.541 |      0.537 |       0.545 |         28 | growth      |         1 |
| topsis|minmax|expert_mean       | ndcg@10      |  0.579 |      0.539 |       0.618 |         28 | growth      |         1 |
| vikor|minmax|expert_mean        | ndcg@10      |  0.577 |      0.546 |       0.613 |         28 | growth      |         1 |
| wsm|minmax|equal                | ndcg@10      |  0.576 |      0.543 |       0.615 |         28 | growth      |         1 |
| wsm|minmax|expert_mean          | ndcg@10      |  0.578 |      0.54  |       0.621 |         28 | growth      |         1 |
| wsm|minmax|learned              | ndcg@10      |  0.574 |      0.529 |       0.619 |         28 | growth      |         1 |
| eoc                             | spearman     |  0.014 |     -0.033 |       0.06  |         28 | growth      |         1 |
| equal_weights                   | spearman     |  0.034 |     -0.027 |       0.091 |         28 | growth      |         1 |
| gravity_ppml                    | spearman     |  0.028 |     -0.039 |       0.096 |         28 | growth      |         1 |
| import_volume                   | spearman     |  0.004 |     -0.045 |       0.054 |         28 | growth      |         1 |
| promethee_ii|minmax|expert_mean | spearman     |  0.034 |     -0.022 |       0.091 |         28 | growth      |         1 |
| random                          | spearman     |  0.001 |     -0.004 |       0.006 |         28 | growth      |         1 |
| topsis|minmax|expert_mean       | spearman     |  0.047 |     -0.01  |       0.099 |         28 | growth      |         1 |
| vikor|minmax|expert_mean        | spearman     |  0.047 |     -0.006 |       0.097 |         28 | growth      |         1 |
| wsm|minmax|equal                | spearman     |  0.034 |     -0.026 |       0.095 |         28 | growth      |         1 |
| wsm|minmax|expert_mean          | spearman     |  0.038 |     -0.019 |       0.097 |         28 | growth      |         1 |
| wsm|minmax|learned              | spearman     |  0.035 |     -0.033 |       0.097 |         28 | growth      |         1 |
| eoc                             | precision@10 |  0.193 |      0.154 |       0.236 |         28 | growth      |         1 |
| equal_weights                   | precision@10 |  0.161 |      0.114 |       0.207 |         28 | growth      |         1 |
| gravity_ppml                    | precision@10 |  0.139 |      0.096 |       0.189 |         28 | growth      |         1 |
| import_volume                   | precision@10 |  0.125 |      0.089 |       0.164 |         28 | growth      |         1 |
| promethee_ii|minmax|expert_mean | precision@10 |  0.189 |      0.143 |       0.243 |         28 | growth      |         1 |
| random                          | precision@10 |  0.169 |      0.166 |       0.172 |         28 | growth      |         1 |
| topsis|minmax|expert_mean       | precision@10 |  0.164 |      0.114 |       0.218 |         28 | growth      |         1 |
| vikor|minmax|expert_mean        | precision@10 |  0.175 |      0.129 |       0.221 |         28 | growth      |         1 |
| wsm|minmax|equal                | precision@10 |  0.161 |      0.118 |       0.207 |         28 | growth      |         1 |
| wsm|minmax|expert_mean          | precision@10 |  0.164 |      0.118 |       0.214 |         28 | growth      |         1 |
| wsm|minmax|learned              | precision@10 |  0.154 |      0.107 |       0.204 |         28 | growth      |         1 |
| eoc                             | ndcg@10      |  0.688 |      0.626 |       0.741 |         14 | intensive   |         3 |
| equal_weights                   | ndcg@10      |  0.77  |      0.714 |       0.826 |         14 | intensive   |         3 |
| gravity_ppml                    | ndcg@10      |  0.806 |      0.732 |       0.873 |         14 | intensive   |         3 |
| import_volume                   | ndcg@10      |  0.745 |      0.691 |       0.801 |         14 | intensive   |         3 |
| promethee_ii|minmax|expert_mean | ndcg@10      |  0.759 |      0.708 |       0.814 |         14 | intensive   |         3 |
| random                          | ndcg@10      |  0.718 |      0.659 |       0.777 |         14 | intensive   |         3 |
| topsis|minmax|expert_mean       | ndcg@10      |  0.763 |      0.71  |       0.817 |         14 | intensive   |         3 |
| vikor|minmax|expert_mean        | ndcg@10      |  0.761 |      0.711 |       0.815 |         14 | intensive   |         3 |
| wsm|minmax|equal                | ndcg@10      |  0.77  |      0.716 |       0.825 |         14 | intensive   |         3 |
| wsm|minmax|expert_mean          | ndcg@10      |  0.771 |      0.719 |       0.827 |         14 | intensive   |         3 |
| wsm|minmax|learned              | ndcg@10      |  0.808 |      0.755 |       0.858 |         14 | intensive   |         3 |
| eoc                             | spearman     | -0.133 |     -0.243 |      -0.024 |         14 | intensive   |         3 |
| equal_weights                   | spearman     |  0.132 |     -0.061 |       0.332 |         14 | intensive   |         3 |
| gravity_ppml                    | spearman     |  0.329 |      0.171 |       0.483 |         14 | intensive   |         3 |
| import_volume                   | spearman     | -0.005 |     -0.22  |       0.186 |         14 | intensive   |         3 |
| promethee_ii|minmax|expert_mean | spearman     |  0.114 |     -0.078 |       0.301 |         14 | intensive   |         3 |
| random                          | spearman     |  0.007 |     -0.021 |       0.034 |         14 | intensive   |         3 |
| topsis|minmax|expert_mean       | spearman     |  0.091 |     -0.144 |       0.309 |         14 | intensive   |         3 |
| vikor|minmax|expert_mean        | spearman     |  0.087 |     -0.129 |       0.298 |         14 | intensive   |         3 |
| wsm|minmax|equal                | spearman     |  0.132 |     -0.063 |       0.334 |         14 | intensive   |         3 |
| wsm|minmax|expert_mean          | spearman     |  0.108 |     -0.086 |       0.319 |         14 | intensive   |         3 |
| wsm|minmax|learned              | spearman     |  0.251 |      0.126 |       0.406 |         14 | intensive   |         3 |
| eoc                             | precision@10 |  0.707 |      0.557 |       0.843 |         14 | intensive   |         3 |
| equal_weights                   | precision@10 |  0.736 |      0.579 |       0.872 |         14 | intensive   |         3 |
| gravity_ppml                    | precision@10 |  0.729 |      0.571 |       0.879 |         14 | intensive   |         3 |
| import_volume                   | precision@10 |  0.686 |      0.507 |       0.836 |         14 | intensive   |         3 |
| promethee_ii|minmax|expert_mean | precision@10 |  0.736 |      0.586 |       0.872 |         14 | intensive   |         3 |
| random                          | precision@10 |  0.691 |      0.531 |       0.839 |         14 | intensive   |         3 |
| topsis|minmax|expert_mean       | precision@10 |  0.736 |      0.586 |       0.879 |         14 | intensive   |         3 |
| vikor|minmax|expert_mean        | precision@10 |  0.743 |      0.586 |       0.879 |         14 | intensive   |         3 |
| wsm|minmax|equal                | precision@10 |  0.736 |      0.586 |       0.872 |         14 | intensive   |         3 |
| wsm|minmax|expert_mean          | precision@10 |  0.729 |      0.579 |       0.864 |         14 | intensive   |         3 |
| wsm|minmax|learned              | precision@10 |  0.743 |      0.586 |       0.886 |         14 | intensive   |         3 |
| eoc                             | auc          |  0.399 |      0.287 |       0.502 |         12 | intensive   |         3 |
| equal_weights                   | auc          |  0.503 |      0.389 |       0.61  |         12 | intensive   |         3 |
| gravity_ppml                    | auc          |  0.526 |      0.411 |       0.628 |         12 | intensive   |         3 |
| import_volume                   | auc          |  0.61  |      0.454 |       0.746 |         12 | intensive   |         3 |
| promethee_ii|minmax|expert_mean | auc          |  0.489 |      0.371 |       0.589 |         12 | intensive   |         3 |
| random                          | auc          |  0.487 |      0.473 |       0.499 |         12 | intensive   |         3 |
| topsis|minmax|expert_mean       | auc          |  0.502 |      0.381 |       0.601 |         12 | intensive   |         3 |
| vikor|minmax|expert_mean        | auc          |  0.501 |      0.395 |       0.595 |         12 | intensive   |         3 |
| wsm|minmax|equal                | auc          |  0.503 |      0.386 |       0.609 |         12 | intensive   |         3 |
| wsm|minmax|expert_mean          | auc          |  0.498 |      0.378 |       0.597 |         12 | intensive   |         3 |
| wsm|minmax|learned              | auc          |  0.508 |      0.39  |       0.605 |         12 | intensive   |         3 |
| eoc                             | ndcg@10      |  0.682 |      0.643 |       0.719 |         13 | new_markets |         3 |
| equal_weights                   | ndcg@10      |  0.733 |      0.694 |       0.78  |         13 | new_markets |         3 |
| gravity_ppml                    | ndcg@10      |  0.709 |      0.67  |       0.746 |         13 | new_markets |         3 |
| import_volume                   | ndcg@10      |  0.724 |      0.683 |       0.763 |         13 | new_markets |         3 |
| promethee_ii|minmax|expert_mean | ndcg@10      |  0.728 |      0.689 |       0.777 |         13 | new_markets |         3 |
| random                          | ndcg@10      |  0.587 |      0.575 |       0.604 |         13 | new_markets |         3 |
| topsis|minmax|expert_mean       | ndcg@10      |  0.726 |      0.682 |       0.776 |         13 | new_markets |         3 |
| vikor|minmax|expert_mean        | ndcg@10      |  0.697 |      0.663 |       0.734 |         13 | new_markets |         3 |
| wsm|minmax|equal                | ndcg@10      |  0.733 |      0.696 |       0.781 |         13 | new_markets |         3 |
| wsm|minmax|expert_mean          | ndcg@10      |  0.712 |      0.668 |       0.766 |         13 | new_markets |         3 |
| wsm|minmax|learned              | ndcg@10      |  0.723 |      0.676 |       0.78  |         13 | new_markets |         3 |
| eoc                             | spearman     |  0.121 |      0.034 |       0.201 |         13 | new_markets |         3 |
| equal_weights                   | spearman     |  0.358 |      0.278 |       0.438 |         13 | new_markets |         3 |
| gravity_ppml                    | spearman     |  0.312 |      0.245 |       0.377 |         13 | new_markets |         3 |
| import_volume                   | spearman     |  0.409 |      0.373 |       0.444 |         13 | new_markets |         3 |
| promethee_ii|minmax|expert_mean | spearman     |  0.295 |      0.211 |       0.382 |         13 | new_markets |         3 |
| random                          | spearman     | -0.014 |     -0.026 |      -0.001 |         13 | new_markets |         3 |
| topsis|minmax|expert_mean       | spearman     |  0.343 |      0.262 |       0.422 |         13 | new_markets |         3 |
| vikor|minmax|expert_mean        | spearman     |  0.336 |      0.265 |       0.403 |         13 | new_markets |         3 |
| wsm|minmax|equal                | spearman     |  0.358 |      0.281 |       0.434 |         13 | new_markets |         3 |
| wsm|minmax|expert_mean          | spearman     |  0.333 |      0.252 |       0.414 |         13 | new_markets |         3 |
| wsm|minmax|learned              | spearman     |  0.321 |      0.236 |       0.409 |         13 | new_markets |         3 |
| eoc                             | precision@10 |  0.385 |      0.321 |       0.454 |         13 | new_markets |         3 |
| equal_weights                   | precision@10 |  0.423 |      0.354 |       0.485 |         13 | new_markets |         3 |
| gravity_ppml                    | precision@10 |  0.462 |      0.4   |       0.525 |         13 | new_markets |         3 |
| import_volume                   | precision@10 |  0.508 |      0.454 |       0.558 |         13 | new_markets |         3 |
| promethee_ii|minmax|expert_mean | precision@10 |  0.423 |      0.364 |       0.479 |         13 | new_markets |         3 |
| random                          | precision@10 |  0.326 |      0.32  |       0.331 |         13 | new_markets |         3 |
| topsis|minmax|expert_mean       | precision@10 |  0.415 |      0.346 |       0.477 |         13 | new_markets |         3 |
| vikor|minmax|expert_mean        | precision@10 |  0.385 |      0.329 |       0.436 |         13 | new_markets |         3 |
| wsm|minmax|equal                | precision@10 |  0.423 |      0.357 |       0.485 |         13 | new_markets |         3 |
| wsm|minmax|expert_mean          | precision@10 |  0.392 |      0.331 |       0.446 |         13 | new_markets |         3 |
| wsm|minmax|learned              | precision@10 |  0.4   |      0.342 |       0.454 |         13 | new_markets |         3 |
| eoc                             | ndcg@10      |  0.539 |      0.481 |       0.601 |         14 | growth      |         3 |
| equal_weights                   | ndcg@10      |  0.576 |      0.528 |       0.629 |         14 | growth      |         3 |
| gravity_ppml                    | ndcg@10      |  0.583 |      0.523 |       0.634 |         14 | growth      |         3 |
| import_volume                   | ndcg@10      |  0.553 |      0.515 |       0.587 |         14 | growth      |         3 |
| promethee_ii|minmax|expert_mean | ndcg@10      |  0.593 |      0.545 |       0.643 |         14 | growth      |         3 |
| random                          | ndcg@10      |  0.541 |      0.536 |       0.545 |         14 | growth      |         3 |
| topsis|minmax|expert_mean       | ndcg@10      |  0.594 |      0.536 |       0.648 |         14 | growth      |         3 |
| vikor|minmax|expert_mean        | ndcg@10      |  0.573 |      0.512 |       0.628 |         14 | growth      |         3 |
| wsm|minmax|equal                | ndcg@10      |  0.576 |      0.525 |       0.627 |         14 | growth      |         3 |
| wsm|minmax|expert_mean          | ndcg@10      |  0.593 |      0.547 |       0.643 |         14 | growth      |         3 |
| wsm|minmax|learned              | ndcg@10      |  0.606 |      0.557 |       0.652 |         14 | growth      |         3 |
| eoc                             | spearman     |  0.015 |     -0.033 |       0.062 |         14 | growth      |         3 |
| equal_weights                   | spearman     |  0.052 |     -0.021 |       0.131 |         14 | growth      |         3 |
| gravity_ppml                    | spearman     |  0.113 |      0.039 |       0.18  |         14 | growth      |         3 |
| import_volume                   | spearman     |  0.021 |     -0.055 |       0.092 |         14 | growth      |         3 |
| promethee_ii|minmax|expert_mean | spearman     |  0.062 |     -0.012 |       0.139 |         14 | growth      |         3 |
| random                          | spearman     |  0.001 |     -0.005 |       0.007 |         14 | growth      |         3 |
| topsis|minmax|expert_mean       | spearman     |  0.07  |     -0.002 |       0.146 |         14 | growth      |         3 |
| vikor|minmax|expert_mean        | spearman     |  0.061 |     -0.011 |       0.137 |         14 | growth      |         3 |
| wsm|minmax|equal                | spearman     |  0.052 |     -0.021 |       0.128 |         14 | growth      |         3 |
| wsm|minmax|expert_mean          | spearman     |  0.058 |     -0.016 |       0.134 |         14 | growth      |         3 |
| wsm|minmax|learned              | spearman     |  0.071 |     -0.006 |       0.143 |         14 | growth      |         3 |
| eoc                             | precision@10 |  0.214 |      0.15  |       0.279 |         14 | growth      |         3 |
| equal_weights                   | precision@10 |  0.129 |      0.071 |       0.186 |         14 | growth      |         3 |
| gravity_ppml                    | precision@10 |  0.143 |      0.1   |       0.186 |         14 | growth      |         3 |
| import_volume                   | precision@10 |  0.1   |      0.043 |       0.171 |         14 | growth      |         3 |
| promethee_ii|minmax|expert_mean | precision@10 |  0.164 |      0.107 |       0.229 |         14 | growth      |         3 |
| random                          | precision@10 |  0.174 |      0.167 |       0.179 |         14 | growth      |         3 |
| topsis|minmax|expert_mean       | precision@10 |  0.15  |      0.093 |       0.214 |         14 | growth      |         3 |
| vikor|minmax|expert_mean        | precision@10 |  0.164 |      0.086 |       0.236 |         14 | growth      |         3 |
| wsm|minmax|equal                | precision@10 |  0.129 |      0.071 |       0.186 |         14 | growth      |         3 |
| wsm|minmax|expert_mean          | precision@10 |  0.136 |      0.079 |       0.2   |         14 | growth      |         3 |
| wsm|minmax|learned              | precision@10 |  0.114 |      0.057 |       0.179 |         14 | growth      |         3 |
| ml_gbm                          | ndcg@10      |  0.719 |      0.659 |       0.773 |         28 | nan         |           |
| ml_gbm                          | spearman     |  0.109 |      0.021 |       0.201 |         28 | nan         |           |
| ml_gbm                          | precision@10 |  0.686 |      0.554 |       0.804 |         28 | nan         |           |
| ml_gbm                          | auc          |  0.586 |      0.491 |       0.675 |         24 | nan         |           |

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
equal\_weights & ndcg@10 & 0.737 & 0.689 & 0.783 & 28 & intensive & 1.000 \\
gravity\_ppml & ndcg@10 & 0.755 & 0.705 & 0.805 & 28 & intensive & 1.000 \\
import\_volume & ndcg@10 & 0.745 & 0.696 & 0.795 & 28 & intensive & 1.000 \\
promethee\_ii|minmax|expert\_mean & ndcg@10 & 0.751 & 0.707 & 0.794 & 28 & intensive & 1.000 \\
random & ndcg@10 & 0.718 & 0.674 & 0.761 & 28 & intensive & 1.000 \\
topsis|minmax|expert\_mean & ndcg@10 & 0.734 & 0.688 & 0.780 & 28 & intensive & 1.000 \\
vikor|minmax|expert\_mean & ndcg@10 & 0.732 & 0.688 & 0.775 & 28 & intensive & 1.000 \\
wsm|minmax|equal & ndcg@10 & 0.737 & 0.688 & 0.783 & 28 & intensive & 1.000 \\
wsm|minmax|expert\_mean & ndcg@10 & 0.738 & 0.685 & 0.789 & 28 & intensive & 1.000 \\
wsm|minmax|learned & ndcg@10 & 0.748 & 0.697 & 0.794 & 28 & intensive & 1.000 \\
eoc & spearman & -0.051 & -0.179 & 0.072 & 28 & intensive & 1.000 \\
equal\_weights & spearman & 0.028 & -0.114 & 0.169 & 28 & intensive & 1.000 \\
gravity\_ppml & spearman & 0.123 & -0.017 & 0.258 & 28 & intensive & 1.000 \\
import\_volume & spearman & 0.040 & -0.091 & 0.160 & 28 & intensive & 1.000 \\
promethee\_ii|minmax|expert\_mean & spearman & 0.076 & -0.072 & 0.213 & 28 & intensive & 1.000 \\
random & spearman & -0.003 & -0.025 & 0.016 & 28 & intensive & 1.000 \\
topsis|minmax|expert\_mean & spearman & 0.043 & -0.094 & 0.175 & 28 & intensive & 1.000 \\
vikor|minmax|expert\_mean & spearman & 0.024 & -0.112 & 0.158 & 28 & intensive & 1.000 \\
wsm|minmax|equal & spearman & 0.028 & -0.118 & 0.164 & 28 & intensive & 1.000 \\
wsm|minmax|expert\_mean & spearman & 0.041 & -0.086 & 0.180 & 28 & intensive & 1.000 \\
wsm|minmax|learned & spearman & 0.073 & -0.066 & 0.196 & 28 & intensive & 1.000 \\
eoc & precision@10 & 0.704 & 0.586 & 0.807 & 28 & intensive & 1.000 \\
equal\_weights & precision@10 & 0.707 & 0.586 & 0.814 & 28 & intensive & 1.000 \\
gravity\_ppml & precision@10 & 0.718 & 0.604 & 0.829 & 28 & intensive & 1.000 \\
import\_volume & precision@10 & 0.696 & 0.578 & 0.818 & 28 & intensive & 1.000 \\
promethee\_ii|minmax|expert\_mean & precision@10 & 0.725 & 0.618 & 0.832 & 28 & intensive & 1.000 \\
random & precision@10 & 0.691 & 0.571 & 0.805 & 28 & intensive & 1.000 \\
topsis|minmax|expert\_mean & precision@10 & 0.714 & 0.596 & 0.825 & 28 & intensive & 1.000 \\
vikor|minmax|expert\_mean & precision@10 & 0.711 & 0.593 & 0.814 & 28 & intensive & 1.000 \\
wsm|minmax|equal & precision@10 & 0.707 & 0.589 & 0.814 & 28 & intensive & 1.000 \\
wsm|minmax|expert\_mean & precision@10 & 0.711 & 0.593 & 0.825 & 28 & intensive & 1.000 \\
wsm|minmax|learned & precision@10 & 0.707 & 0.582 & 0.814 & 28 & intensive & 1.000 \\
eoc & auc & 0.409 & 0.318 & 0.496 & 24 & intensive & 1.000 \\
equal\_weights & auc & 0.546 & 0.444 & 0.645 & 24 & intensive & 1.000 \\
gravity\_ppml & auc & 0.529 & 0.442 & 0.604 & 24 & intensive & 1.000 \\
import\_volume & auc & 0.627 & 0.530 & 0.715 & 24 & intensive & 1.000 \\
promethee\_ii|minmax|expert\_mean & auc & 0.528 & 0.432 & 0.611 & 24 & intensive & 1.000 \\
random & auc & 0.490 & 0.478 & 0.500 & 24 & intensive & 1.000 \\
topsis|minmax|expert\_mean & auc & 0.534 & 0.445 & 0.618 & 24 & intensive & 1.000 \\
vikor|minmax|expert\_mean & auc & 0.521 & 0.429 & 0.611 & 24 & intensive & 1.000 \\
wsm|minmax|equal & auc & 0.546 & 0.446 & 0.636 & 24 & intensive & 1.000 \\
wsm|minmax|expert\_mean & auc & 0.535 & 0.435 & 0.628 & 24 & intensive & 1.000 \\
wsm|minmax|learned & auc & 0.530 & 0.435 & 0.622 & 24 & intensive & 1.000 \\
eoc & ndcg@10 & 0.676 & 0.641 & 0.710 & 25 & new\_markets & 1.000 \\
equal\_weights & ndcg@10 & 0.736 & 0.697 & 0.773 & 25 & new\_markets & 1.000 \\
gravity\_ppml & ndcg@10 & 0.682 & 0.644 & 0.719 & 25 & new\_markets & 1.000 \\
import\_volume & ndcg@10 & 0.722 & 0.691 & 0.752 & 25 & new\_markets & 1.000 \\
promethee\_ii|minmax|expert\_mean & ndcg@10 & 0.726 & 0.697 & 0.755 & 25 & new\_markets & 1.000 \\
random & ndcg@10 & 0.583 & 0.576 & 0.593 & 25 & new\_markets & 1.000 \\
topsis|minmax|expert\_mean & ndcg@10 & 0.738 & 0.698 & 0.774 & 25 & new\_markets & 1.000 \\
vikor|minmax|expert\_mean & ndcg@10 & 0.725 & 0.689 & 0.757 & 25 & new\_markets & 1.000 \\
wsm|minmax|equal & ndcg@10 & 0.736 & 0.699 & 0.775 & 25 & new\_markets & 1.000 \\
wsm|minmax|expert\_mean & ndcg@10 & 0.723 & 0.684 & 0.760 & 25 & new\_markets & 1.000 \\
wsm|minmax|learned & ndcg@10 & 0.732 & 0.691 & 0.769 & 25 & new\_markets & 1.000 \\
eoc & spearman & 0.122 & 0.057 & 0.187 & 25 & new\_markets & 1.000 \\
equal\_weights & spearman & 0.369 & 0.304 & 0.430 & 25 & new\_markets & 1.000 \\
gravity\_ppml & spearman & 0.292 & 0.224 & 0.359 & 25 & new\_markets & 1.000 \\
import\_volume & spearman & 0.395 & 0.352 & 0.439 & 25 & new\_markets & 1.000 \\
promethee\_ii|minmax|expert\_mean & spearman & 0.328 & 0.272 & 0.385 & 25 & new\_markets & 1.000 \\
random & spearman & -0.011 & -0.020 & -0.002 & 25 & new\_markets & 1.000 \\
topsis|minmax|expert\_mean & spearman & 0.363 & 0.299 & 0.419 & 25 & new\_markets & 1.000 \\
vikor|minmax|expert\_mean & spearman & 0.366 & 0.306 & 0.424 & 25 & new\_markets & 1.000 \\
wsm|minmax|equal & spearman & 0.369 & 0.307 & 0.432 & 25 & new\_markets & 1.000 \\
wsm|minmax|expert\_mean & spearman & 0.348 & 0.280 & 0.410 & 25 & new\_markets & 1.000 \\
wsm|minmax|learned & spearman & 0.338 & 0.271 & 0.400 & 25 & new\_markets & 1.000 \\
eoc & precision@10 & 0.396 & 0.348 & 0.450 & 25 & new\_markets & 1.000 \\
equal\_weights & precision@10 & 0.436 & 0.383 & 0.488 & 25 & new\_markets & 1.000 \\
gravity\_ppml & precision@10 & 0.464 & 0.404 & 0.525 & 25 & new\_markets & 1.000 \\
import\_volume & precision@10 & 0.532 & 0.493 & 0.571 & 25 & new\_markets & 1.000 \\
promethee\_ii|minmax|expert\_mean & precision@10 & 0.440 & 0.389 & 0.492 & 25 & new\_markets & 1.000 \\
random & precision@10 & 0.332 & 0.327 & 0.337 & 25 & new\_markets & 1.000 \\
topsis|minmax|expert\_mean & precision@10 & 0.452 & 0.396 & 0.504 & 25 & new\_markets & 1.000 \\
vikor|minmax|expert\_mean & precision@10 & 0.456 & 0.396 & 0.516 & 25 & new\_markets & 1.000 \\
wsm|minmax|equal & precision@10 & 0.436 & 0.384 & 0.488 & 25 & new\_markets & 1.000 \\
wsm|minmax|expert\_mean & precision@10 & 0.428 & 0.375 & 0.473 & 25 & new\_markets & 1.000 \\
wsm|minmax|learned & precision@10 & 0.440 & 0.387 & 0.488 & 25 & new\_markets & 1.000 \\
eoc & ndcg@10 & 0.536 & 0.491 & 0.581 & 28 & growth & 1.000 \\
equal\_weights & ndcg@10 & 0.576 & 0.540 & 0.615 & 28 & growth & 1.000 \\
gravity\_ppml & ndcg@10 & 0.550 & 0.510 & 0.588 & 28 & growth & 1.000 \\
import\_volume & ndcg@10 & 0.547 & 0.515 & 0.580 & 28 & growth & 1.000 \\
promethee\_ii|minmax|expert\_mean & ndcg@10 & 0.572 & 0.536 & 0.611 & 28 & growth & 1.000 \\
random & ndcg@10 & 0.541 & 0.537 & 0.545 & 28 & growth & 1.000 \\
topsis|minmax|expert\_mean & ndcg@10 & 0.579 & 0.539 & 0.618 & 28 & growth & 1.000 \\
vikor|minmax|expert\_mean & ndcg@10 & 0.577 & 0.546 & 0.613 & 28 & growth & 1.000 \\
wsm|minmax|equal & ndcg@10 & 0.576 & 0.543 & 0.615 & 28 & growth & 1.000 \\
wsm|minmax|expert\_mean & ndcg@10 & 0.578 & 0.540 & 0.621 & 28 & growth & 1.000 \\
wsm|minmax|learned & ndcg@10 & 0.574 & 0.529 & 0.619 & 28 & growth & 1.000 \\
eoc & spearman & 0.014 & -0.033 & 0.060 & 28 & growth & 1.000 \\
equal\_weights & spearman & 0.034 & -0.027 & 0.091 & 28 & growth & 1.000 \\
gravity\_ppml & spearman & 0.028 & -0.039 & 0.096 & 28 & growth & 1.000 \\
import\_volume & spearman & 0.004 & -0.045 & 0.054 & 28 & growth & 1.000 \\
promethee\_ii|minmax|expert\_mean & spearman & 0.034 & -0.022 & 0.091 & 28 & growth & 1.000 \\
random & spearman & 0.001 & -0.004 & 0.006 & 28 & growth & 1.000 \\
topsis|minmax|expert\_mean & spearman & 0.047 & -0.010 & 0.099 & 28 & growth & 1.000 \\
vikor|minmax|expert\_mean & spearman & 0.047 & -0.006 & 0.097 & 28 & growth & 1.000 \\
wsm|minmax|equal & spearman & 0.034 & -0.026 & 0.095 & 28 & growth & 1.000 \\
wsm|minmax|expert\_mean & spearman & 0.038 & -0.019 & 0.097 & 28 & growth & 1.000 \\
wsm|minmax|learned & spearman & 0.035 & -0.033 & 0.097 & 28 & growth & 1.000 \\
eoc & precision@10 & 0.193 & 0.154 & 0.236 & 28 & growth & 1.000 \\
equal\_weights & precision@10 & 0.161 & 0.114 & 0.207 & 28 & growth & 1.000 \\
gravity\_ppml & precision@10 & 0.139 & 0.096 & 0.189 & 28 & growth & 1.000 \\
import\_volume & precision@10 & 0.125 & 0.089 & 0.164 & 28 & growth & 1.000 \\
promethee\_ii|minmax|expert\_mean & precision@10 & 0.189 & 0.143 & 0.243 & 28 & growth & 1.000 \\
random & precision@10 & 0.169 & 0.166 & 0.172 & 28 & growth & 1.000 \\
topsis|minmax|expert\_mean & precision@10 & 0.164 & 0.114 & 0.218 & 28 & growth & 1.000 \\
vikor|minmax|expert\_mean & precision@10 & 0.175 & 0.129 & 0.221 & 28 & growth & 1.000 \\
wsm|minmax|equal & precision@10 & 0.161 & 0.118 & 0.207 & 28 & growth & 1.000 \\
wsm|minmax|expert\_mean & precision@10 & 0.164 & 0.118 & 0.214 & 28 & growth & 1.000 \\
wsm|minmax|learned & precision@10 & 0.154 & 0.107 & 0.204 & 28 & growth & 1.000 \\
eoc & ndcg@10 & 0.688 & 0.626 & 0.741 & 14 & intensive & 3.000 \\
equal\_weights & ndcg@10 & 0.770 & 0.714 & 0.826 & 14 & intensive & 3.000 \\
gravity\_ppml & ndcg@10 & 0.806 & 0.732 & 0.873 & 14 & intensive & 3.000 \\
import\_volume & ndcg@10 & 0.745 & 0.691 & 0.801 & 14 & intensive & 3.000 \\
promethee\_ii|minmax|expert\_mean & ndcg@10 & 0.759 & 0.708 & 0.814 & 14 & intensive & 3.000 \\
random & ndcg@10 & 0.718 & 0.659 & 0.777 & 14 & intensive & 3.000 \\
topsis|minmax|expert\_mean & ndcg@10 & 0.763 & 0.710 & 0.817 & 14 & intensive & 3.000 \\
vikor|minmax|expert\_mean & ndcg@10 & 0.761 & 0.711 & 0.815 & 14 & intensive & 3.000 \\
wsm|minmax|equal & ndcg@10 & 0.770 & 0.716 & 0.825 & 14 & intensive & 3.000 \\
wsm|minmax|expert\_mean & ndcg@10 & 0.771 & 0.719 & 0.827 & 14 & intensive & 3.000 \\
wsm|minmax|learned & ndcg@10 & 0.808 & 0.755 & 0.858 & 14 & intensive & 3.000 \\
eoc & spearman & -0.133 & -0.243 & -0.024 & 14 & intensive & 3.000 \\
equal\_weights & spearman & 0.132 & -0.061 & 0.332 & 14 & intensive & 3.000 \\
gravity\_ppml & spearman & 0.329 & 0.171 & 0.483 & 14 & intensive & 3.000 \\
import\_volume & spearman & -0.005 & -0.220 & 0.186 & 14 & intensive & 3.000 \\
promethee\_ii|minmax|expert\_mean & spearman & 0.114 & -0.078 & 0.301 & 14 & intensive & 3.000 \\
random & spearman & 0.007 & -0.021 & 0.034 & 14 & intensive & 3.000 \\
topsis|minmax|expert\_mean & spearman & 0.091 & -0.144 & 0.309 & 14 & intensive & 3.000 \\
vikor|minmax|expert\_mean & spearman & 0.087 & -0.129 & 0.298 & 14 & intensive & 3.000 \\
wsm|minmax|equal & spearman & 0.132 & -0.063 & 0.334 & 14 & intensive & 3.000 \\
wsm|minmax|expert\_mean & spearman & 0.108 & -0.086 & 0.319 & 14 & intensive & 3.000 \\
wsm|minmax|learned & spearman & 0.251 & 0.126 & 0.406 & 14 & intensive & 3.000 \\
eoc & precision@10 & 0.707 & 0.557 & 0.843 & 14 & intensive & 3.000 \\
equal\_weights & precision@10 & 0.736 & 0.579 & 0.872 & 14 & intensive & 3.000 \\
gravity\_ppml & precision@10 & 0.729 & 0.571 & 0.879 & 14 & intensive & 3.000 \\
import\_volume & precision@10 & 0.686 & 0.507 & 0.836 & 14 & intensive & 3.000 \\
promethee\_ii|minmax|expert\_mean & precision@10 & 0.736 & 0.586 & 0.872 & 14 & intensive & 3.000 \\
random & precision@10 & 0.691 & 0.531 & 0.839 & 14 & intensive & 3.000 \\
topsis|minmax|expert\_mean & precision@10 & 0.736 & 0.586 & 0.879 & 14 & intensive & 3.000 \\
vikor|minmax|expert\_mean & precision@10 & 0.743 & 0.586 & 0.879 & 14 & intensive & 3.000 \\
wsm|minmax|equal & precision@10 & 0.736 & 0.586 & 0.872 & 14 & intensive & 3.000 \\
wsm|minmax|expert\_mean & precision@10 & 0.729 & 0.579 & 0.864 & 14 & intensive & 3.000 \\
wsm|minmax|learned & precision@10 & 0.743 & 0.586 & 0.886 & 14 & intensive & 3.000 \\
eoc & auc & 0.399 & 0.287 & 0.502 & 12 & intensive & 3.000 \\
equal\_weights & auc & 0.503 & 0.389 & 0.610 & 12 & intensive & 3.000 \\
gravity\_ppml & auc & 0.526 & 0.411 & 0.628 & 12 & intensive & 3.000 \\
import\_volume & auc & 0.610 & 0.454 & 0.746 & 12 & intensive & 3.000 \\
promethee\_ii|minmax|expert\_mean & auc & 0.489 & 0.371 & 0.589 & 12 & intensive & 3.000 \\
random & auc & 0.487 & 0.473 & 0.499 & 12 & intensive & 3.000 \\
topsis|minmax|expert\_mean & auc & 0.502 & 0.381 & 0.601 & 12 & intensive & 3.000 \\
vikor|minmax|expert\_mean & auc & 0.501 & 0.395 & 0.595 & 12 & intensive & 3.000 \\
wsm|minmax|equal & auc & 0.503 & 0.386 & 0.609 & 12 & intensive & 3.000 \\
wsm|minmax|expert\_mean & auc & 0.498 & 0.378 & 0.597 & 12 & intensive & 3.000 \\
wsm|minmax|learned & auc & 0.508 & 0.390 & 0.605 & 12 & intensive & 3.000 \\
eoc & ndcg@10 & 0.682 & 0.643 & 0.719 & 13 & new\_markets & 3.000 \\
equal\_weights & ndcg@10 & 0.733 & 0.694 & 0.780 & 13 & new\_markets & 3.000 \\
gravity\_ppml & ndcg@10 & 0.709 & 0.670 & 0.746 & 13 & new\_markets & 3.000 \\
import\_volume & ndcg@10 & 0.724 & 0.683 & 0.763 & 13 & new\_markets & 3.000 \\
promethee\_ii|minmax|expert\_mean & ndcg@10 & 0.728 & 0.689 & 0.777 & 13 & new\_markets & 3.000 \\
random & ndcg@10 & 0.587 & 0.575 & 0.604 & 13 & new\_markets & 3.000 \\
topsis|minmax|expert\_mean & ndcg@10 & 0.726 & 0.682 & 0.776 & 13 & new\_markets & 3.000 \\
vikor|minmax|expert\_mean & ndcg@10 & 0.697 & 0.663 & 0.734 & 13 & new\_markets & 3.000 \\
wsm|minmax|equal & ndcg@10 & 0.733 & 0.696 & 0.781 & 13 & new\_markets & 3.000 \\
wsm|minmax|expert\_mean & ndcg@10 & 0.712 & 0.668 & 0.766 & 13 & new\_markets & 3.000 \\
wsm|minmax|learned & ndcg@10 & 0.723 & 0.676 & 0.780 & 13 & new\_markets & 3.000 \\
eoc & spearman & 0.121 & 0.034 & 0.201 & 13 & new\_markets & 3.000 \\
equal\_weights & spearman & 0.358 & 0.278 & 0.438 & 13 & new\_markets & 3.000 \\
gravity\_ppml & spearman & 0.312 & 0.245 & 0.377 & 13 & new\_markets & 3.000 \\
import\_volume & spearman & 0.409 & 0.373 & 0.444 & 13 & new\_markets & 3.000 \\
promethee\_ii|minmax|expert\_mean & spearman & 0.295 & 0.211 & 0.382 & 13 & new\_markets & 3.000 \\
random & spearman & -0.014 & -0.026 & -0.001 & 13 & new\_markets & 3.000 \\
topsis|minmax|expert\_mean & spearman & 0.343 & 0.262 & 0.422 & 13 & new\_markets & 3.000 \\
vikor|minmax|expert\_mean & spearman & 0.336 & 0.265 & 0.403 & 13 & new\_markets & 3.000 \\
wsm|minmax|equal & spearman & 0.358 & 0.281 & 0.434 & 13 & new\_markets & 3.000 \\
wsm|minmax|expert\_mean & spearman & 0.333 & 0.252 & 0.414 & 13 & new\_markets & 3.000 \\
wsm|minmax|learned & spearman & 0.321 & 0.236 & 0.409 & 13 & new\_markets & 3.000 \\
eoc & precision@10 & 0.385 & 0.321 & 0.454 & 13 & new\_markets & 3.000 \\
equal\_weights & precision@10 & 0.423 & 0.354 & 0.485 & 13 & new\_markets & 3.000 \\
gravity\_ppml & precision@10 & 0.462 & 0.400 & 0.525 & 13 & new\_markets & 3.000 \\
import\_volume & precision@10 & 0.508 & 0.454 & 0.558 & 13 & new\_markets & 3.000 \\
promethee\_ii|minmax|expert\_mean & precision@10 & 0.423 & 0.364 & 0.479 & 13 & new\_markets & 3.000 \\
random & precision@10 & 0.326 & 0.320 & 0.331 & 13 & new\_markets & 3.000 \\
topsis|minmax|expert\_mean & precision@10 & 0.415 & 0.346 & 0.477 & 13 & new\_markets & 3.000 \\
vikor|minmax|expert\_mean & precision@10 & 0.385 & 0.329 & 0.436 & 13 & new\_markets & 3.000 \\
wsm|minmax|equal & precision@10 & 0.423 & 0.357 & 0.485 & 13 & new\_markets & 3.000 \\
wsm|minmax|expert\_mean & precision@10 & 0.392 & 0.331 & 0.446 & 13 & new\_markets & 3.000 \\
wsm|minmax|learned & precision@10 & 0.400 & 0.342 & 0.454 & 13 & new\_markets & 3.000 \\
eoc & ndcg@10 & 0.539 & 0.481 & 0.601 & 14 & growth & 3.000 \\
equal\_weights & ndcg@10 & 0.576 & 0.528 & 0.629 & 14 & growth & 3.000 \\
gravity\_ppml & ndcg@10 & 0.583 & 0.523 & 0.634 & 14 & growth & 3.000 \\
import\_volume & ndcg@10 & 0.553 & 0.515 & 0.587 & 14 & growth & 3.000 \\
promethee\_ii|minmax|expert\_mean & ndcg@10 & 0.593 & 0.545 & 0.643 & 14 & growth & 3.000 \\
random & ndcg@10 & 0.541 & 0.536 & 0.545 & 14 & growth & 3.000 \\
topsis|minmax|expert\_mean & ndcg@10 & 0.594 & 0.536 & 0.648 & 14 & growth & 3.000 \\
vikor|minmax|expert\_mean & ndcg@10 & 0.573 & 0.512 & 0.628 & 14 & growth & 3.000 \\
wsm|minmax|equal & ndcg@10 & 0.576 & 0.525 & 0.627 & 14 & growth & 3.000 \\
wsm|minmax|expert\_mean & ndcg@10 & 0.593 & 0.547 & 0.643 & 14 & growth & 3.000 \\
wsm|minmax|learned & ndcg@10 & 0.606 & 0.557 & 0.652 & 14 & growth & 3.000 \\
eoc & spearman & 0.015 & -0.033 & 0.062 & 14 & growth & 3.000 \\
equal\_weights & spearman & 0.052 & -0.021 & 0.131 & 14 & growth & 3.000 \\
gravity\_ppml & spearman & 0.113 & 0.039 & 0.180 & 14 & growth & 3.000 \\
import\_volume & spearman & 0.021 & -0.055 & 0.092 & 14 & growth & 3.000 \\
promethee\_ii|minmax|expert\_mean & spearman & 0.062 & -0.012 & 0.139 & 14 & growth & 3.000 \\
random & spearman & 0.001 & -0.005 & 0.007 & 14 & growth & 3.000 \\
topsis|minmax|expert\_mean & spearman & 0.070 & -0.002 & 0.146 & 14 & growth & 3.000 \\
vikor|minmax|expert\_mean & spearman & 0.061 & -0.011 & 0.137 & 14 & growth & 3.000 \\
wsm|minmax|equal & spearman & 0.052 & -0.021 & 0.128 & 14 & growth & 3.000 \\
wsm|minmax|expert\_mean & spearman & 0.058 & -0.016 & 0.134 & 14 & growth & 3.000 \\
wsm|minmax|learned & spearman & 0.071 & -0.006 & 0.143 & 14 & growth & 3.000 \\
eoc & precision@10 & 0.214 & 0.150 & 0.279 & 14 & growth & 3.000 \\
equal\_weights & precision@10 & 0.129 & 0.071 & 0.186 & 14 & growth & 3.000 \\
gravity\_ppml & precision@10 & 0.143 & 0.100 & 0.186 & 14 & growth & 3.000 \\
import\_volume & precision@10 & 0.100 & 0.043 & 0.171 & 14 & growth & 3.000 \\
promethee\_ii|minmax|expert\_mean & precision@10 & 0.164 & 0.107 & 0.229 & 14 & growth & 3.000 \\
random & precision@10 & 0.174 & 0.167 & 0.179 & 14 & growth & 3.000 \\
topsis|minmax|expert\_mean & precision@10 & 0.150 & 0.093 & 0.214 & 14 & growth & 3.000 \\
vikor|minmax|expert\_mean & precision@10 & 0.164 & 0.086 & 0.236 & 14 & growth & 3.000 \\
wsm|minmax|equal & precision@10 & 0.129 & 0.071 & 0.186 & 14 & growth & 3.000 \\
wsm|minmax|expert\_mean & precision@10 & 0.136 & 0.079 & 0.200 & 14 & growth & 3.000 \\
wsm|minmax|learned & precision@10 & 0.114 & 0.057 & 0.179 & 14 & growth & 3.000 \\
ml\_gbm & ndcg@10 & 0.719 & 0.659 & 0.773 & 28 & nan &  \\
ml\_gbm & spearman & 0.109 & 0.021 & 0.201 & 28 & nan &  \\
ml\_gbm & precision@10 & 0.686 & 0.554 & 0.804 & 28 & nan &  \\
ml\_gbm & auc & 0.586 & 0.491 & 0.675 & 24 & nan &  \\
\bottomrule
\end{tabular}
\end{table}
```
