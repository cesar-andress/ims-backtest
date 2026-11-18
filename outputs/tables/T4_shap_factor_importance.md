# T4c. SHAP vs expert vs learned factor shares

| factor          |   shap_share |   expert_share |   learned_share |
|:----------------|-------------:|---------------:|----------------:|
| competition     |       0.0923 |         0.145  |          0.0951 |
| cost_access     |       0.2608 |         0.161  |          0.2127 |
| demand          |       0.1995 |         0.125  |          0.1652 |
| institutional   |       0.1312 |         0.098  |          0.0643 |
| logistics       |       0.0023 |         0.1385 |          0.183  |
| macro_risk      |       0.0699 |         0.115  |          0.0755 |
| openness_legacy |       0.1061 |         0.125  |          0.082  |
| product_fit     |       0.1379 |         0.0925 |          0.1222 |

## Booktabs (copy into manuscript; not a repo .tex file)

```latex
\begin{table}[htbp]
\centering
\caption{T4c. SHAP vs expert vs learned factor shares}
\label{tab:T4_shap_factor_importance}
\begin{tabular}{llll}
\toprule
factor & shap\_share & expert\_share & learned\_share \\
\midrule
competition & 0.0923 & 0.1450 & 0.0951 \\
cost\_access & 0.2608 & 0.1610 & 0.2127 \\
demand & 0.1995 & 0.1250 & 0.1652 \\
institutional & 0.1312 & 0.0980 & 0.0643 \\
logistics & 0.0023 & 0.1385 & 0.1830 \\
macro\_risk & 0.0699 & 0.1150 & 0.0755 \\
openness\_legacy & 0.1061 & 0.1250 & 0.0820 \\
product\_fit & 0.1379 & 0.0925 & 0.1222 \\
\bottomrule
\end{tabular}
\end{table}
```
