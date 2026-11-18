# T4. Predictive validation metrics (bootstrap means and 95% CIs)

| method                          | metric       |   mean |   ci95_low |   ci95_high |   n_blocks |
|:--------------------------------|:-------------|-------:|-----------:|------------:|-----------:|
| eoc                             | ndcg@10      |  0.702 |      0.651 |       0.751 |         28 |
| equal_weights                   | ndcg@10      |  0.75  |      0.702 |       0.8   |         28 |
| gravity_ppml                    | ndcg@10      |  0.748 |      0.696 |       0.796 |         28 |
| import_volume                   | ndcg@10      |  0.745 |      0.696 |       0.795 |         28 |
| promethee_ii|minmax|expert_mean | ndcg@10      |  0.763 |      0.718 |       0.807 |         28 |
| random                          | ndcg@10      |  0.718 |      0.674 |       0.761 |         28 |
| topsis|minmax|expert_mean       | ndcg@10      |  0.763 |      0.716 |       0.808 |         28 |
| vikor|minmax|expert_mean        | ndcg@10      |  0.752 |      0.709 |       0.794 |         28 |
| wsm|minmax|equal                | ndcg@10      |  0.75  |      0.7   |       0.799 |         28 |
| wsm|minmax|expert_mean          | ndcg@10      |  0.758 |      0.709 |       0.806 |         28 |
| wsm|minmax|learned              | ndcg@10      |  0.761 |      0.716 |       0.806 |         28 |
| eoc                             | spearman     | -0.051 |     -0.179 |       0.072 |         28 |
| equal_weights                   | spearman     |  0.031 |     -0.116 |       0.183 |         28 |
| gravity_ppml                    | spearman     |  0.129 |      0.005 |       0.251 |         28 |
| import_volume                   | spearman     |  0.04  |     -0.091 |       0.16  |         28 |
| promethee_ii|minmax|expert_mean | spearman     |  0.065 |     -0.084 |       0.201 |         28 |
| random                          | spearman     | -0.003 |     -0.025 |       0.016 |         28 |
| topsis|minmax|expert_mean       | spearman     |  0.055 |     -0.085 |       0.186 |         28 |
| vikor|minmax|expert_mean        | spearman     |  0.071 |     -0.065 |       0.202 |         28 |
| wsm|minmax|equal                | spearman     |  0.031 |     -0.129 |       0.177 |         28 |
| wsm|minmax|expert_mean          | spearman     |  0.057 |     -0.086 |       0.202 |         28 |
| wsm|minmax|learned              | spearman     |  0.053 |     -0.088 |       0.18  |         28 |
| eoc                             | precision@10 |  0.704 |      0.586 |       0.807 |         28 |
| equal_weights                   | precision@10 |  0.743 |      0.625 |       0.854 |         28 |
| gravity_ppml                    | precision@10 |  0.711 |      0.596 |       0.821 |         28 |
| import_volume                   | precision@10 |  0.696 |      0.578 |       0.818 |         28 |
| promethee_ii|minmax|expert_mean | precision@10 |  0.746 |      0.636 |       0.85  |         28 |
| random                          | precision@10 |  0.691 |      0.571 |       0.805 |         28 |
| topsis|minmax|expert_mean       | precision@10 |  0.746 |      0.632 |       0.85  |         28 |
| vikor|minmax|expert_mean        | precision@10 |  0.75  |      0.636 |       0.843 |         28 |
| wsm|minmax|equal                | precision@10 |  0.743 |      0.625 |       0.847 |         28 |
| wsm|minmax|expert_mean          | precision@10 |  0.75  |      0.636 |       0.857 |         28 |
| wsm|minmax|learned              | precision@10 |  0.736 |      0.614 |       0.843 |         28 |
| eoc                             | auc          |  0.409 |      0.318 |       0.496 |         24 |
| equal_weights                   | auc          |  0.521 |      0.423 |       0.615 |         24 |
| gravity_ppml                    | auc          |  0.512 |      0.421 |       0.597 |         24 |
| import_volume                   | auc          |  0.627 |      0.53  |       0.715 |         24 |
| promethee_ii|minmax|expert_mean | auc          |  0.51  |      0.41  |       0.597 |         24 |
| random                          | auc          |  0.49  |      0.478 |       0.5   |         24 |
| topsis|minmax|expert_mean       | auc          |  0.518 |      0.424 |       0.609 |         24 |
| vikor|minmax|expert_mean        | auc          |  0.539 |      0.44  |       0.636 |         24 |
| wsm|minmax|equal                | auc          |  0.521 |      0.426 |       0.611 |         24 |
| wsm|minmax|expert_mean          | auc          |  0.509 |      0.408 |       0.6   |         24 |
| wsm|minmax|learned              | auc          |  0.504 |      0.411 |       0.595 |         24 |
| ml_gbm                          | ndcg@10      |  0.749 |      0.699 |       0.794 |         28 |
| ml_gbm                          | spearman     |  0.106 |     -0.007 |       0.212 |         28 |
| ml_gbm                          | precision@10 |  0.689 |      0.553 |       0.807 |         28 |
| ml_gbm                          | auc          |  0.668 |      0.583 |       0.749 |         24 |

## Booktabs (copy into manuscript; not a repo .tex file)

```latex
\begin{table}[htbp]
\centering
\caption{T4. Predictive validation metrics (bootstrap means and 95% CIs)}
\label{tab:T4_predictive_metrics}
\begin{tabular}{llllll}
\toprule
method & metric & mean & ci95\_low & ci95\_high & n\_blocks \\
\midrule
eoc & ndcg@10 & 0.702 & 0.651 & 0.751 & 28 \\
equal\_weights & ndcg@10 & 0.750 & 0.702 & 0.800 & 28 \\
gravity\_ppml & ndcg@10 & 0.748 & 0.696 & 0.796 & 28 \\
import\_volume & ndcg@10 & 0.745 & 0.696 & 0.795 & 28 \\
promethee\_ii|minmax|expert\_mean & ndcg@10 & 0.763 & 0.718 & 0.807 & 28 \\
random & ndcg@10 & 0.718 & 0.674 & 0.761 & 28 \\
topsis|minmax|expert\_mean & ndcg@10 & 0.763 & 0.716 & 0.808 & 28 \\
vikor|minmax|expert\_mean & ndcg@10 & 0.752 & 0.709 & 0.794 & 28 \\
wsm|minmax|equal & ndcg@10 & 0.750 & 0.700 & 0.799 & 28 \\
wsm|minmax|expert\_mean & ndcg@10 & 0.758 & 0.709 & 0.806 & 28 \\
wsm|minmax|learned & ndcg@10 & 0.761 & 0.716 & 0.806 & 28 \\
eoc & spearman & -0.051 & -0.179 & 0.072 & 28 \\
equal\_weights & spearman & 0.031 & -0.116 & 0.183 & 28 \\
gravity\_ppml & spearman & 0.129 & 0.005 & 0.251 & 28 \\
import\_volume & spearman & 0.040 & -0.091 & 0.160 & 28 \\
promethee\_ii|minmax|expert\_mean & spearman & 0.065 & -0.084 & 0.201 & 28 \\
random & spearman & -0.003 & -0.025 & 0.016 & 28 \\
topsis|minmax|expert\_mean & spearman & 0.055 & -0.085 & 0.186 & 28 \\
vikor|minmax|expert\_mean & spearman & 0.071 & -0.065 & 0.202 & 28 \\
wsm|minmax|equal & spearman & 0.031 & -0.129 & 0.177 & 28 \\
wsm|minmax|expert\_mean & spearman & 0.057 & -0.086 & 0.202 & 28 \\
wsm|minmax|learned & spearman & 0.053 & -0.088 & 0.180 & 28 \\
eoc & precision@10 & 0.704 & 0.586 & 0.807 & 28 \\
equal\_weights & precision@10 & 0.743 & 0.625 & 0.854 & 28 \\
gravity\_ppml & precision@10 & 0.711 & 0.596 & 0.821 & 28 \\
import\_volume & precision@10 & 0.696 & 0.578 & 0.818 & 28 \\
promethee\_ii|minmax|expert\_mean & precision@10 & 0.746 & 0.636 & 0.850 & 28 \\
random & precision@10 & 0.691 & 0.571 & 0.805 & 28 \\
topsis|minmax|expert\_mean & precision@10 & 0.746 & 0.632 & 0.850 & 28 \\
vikor|minmax|expert\_mean & precision@10 & 0.750 & 0.636 & 0.843 & 28 \\
wsm|minmax|equal & precision@10 & 0.743 & 0.625 & 0.847 & 28 \\
wsm|minmax|expert\_mean & precision@10 & 0.750 & 0.636 & 0.857 & 28 \\
wsm|minmax|learned & precision@10 & 0.736 & 0.614 & 0.843 & 28 \\
eoc & auc & 0.409 & 0.318 & 0.496 & 24 \\
equal\_weights & auc & 0.521 & 0.423 & 0.615 & 24 \\
gravity\_ppml & auc & 0.512 & 0.421 & 0.597 & 24 \\
import\_volume & auc & 0.627 & 0.530 & 0.715 & 24 \\
promethee\_ii|minmax|expert\_mean & auc & 0.510 & 0.410 & 0.597 & 24 \\
random & auc & 0.490 & 0.478 & 0.500 & 24 \\
topsis|minmax|expert\_mean & auc & 0.518 & 0.424 & 0.609 & 24 \\
vikor|minmax|expert\_mean & auc & 0.539 & 0.440 & 0.636 & 24 \\
wsm|minmax|equal & auc & 0.521 & 0.426 & 0.611 & 24 \\
wsm|minmax|expert\_mean & auc & 0.509 & 0.408 & 0.600 & 24 \\
wsm|minmax|learned & auc & 0.504 & 0.411 & 0.595 & 24 \\
ml\_gbm & ndcg@10 & 0.749 & 0.699 & 0.794 & 28 \\
ml\_gbm & spearman & 0.106 & -0.007 & 0.212 & 28 \\
ml\_gbm & precision@10 & 0.689 & 0.553 & 0.807 & 28 \\
ml\_gbm & auc & 0.668 & 0.583 & 0.749 & 24 \\
\bottomrule
\end{tabular}
\end{table}
```
