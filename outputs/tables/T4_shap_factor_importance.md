# T4c. SHAP vs expert vs learned factor shares

| factor          |   shap_share |   expert_share |   learned_share |
|:----------------|-------------:|---------------:|----------------:|
| competition     |       0.0905 |         0.145  |          0.1438 |
| cost_access     |       0.253  |         0.161  |          0.1736 |
| demand          |       0.1961 |         0.125  |          0.08   |
| institutional   |       0.0875 |         0.098  |          0.0995 |
| logistics       |       0.0358 |         0.1385 |          0.0934 |
| macro_risk      |       0.0727 |         0.115  |          0.1179 |
| openness_legacy |       0.1285 |         0.125  |          0.0688 |
| product_fit     |       0.1359 |         0.0925 |          0.223  |

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
competition & 0.0905 & 0.1450 & 0.1438 \\
cost\_access & 0.2530 & 0.1610 & 0.1736 \\
demand & 0.1961 & 0.1250 & 0.0800 \\
institutional & 0.0875 & 0.0980 & 0.0995 \\
logistics & 0.0358 & 0.1385 & 0.0934 \\
macro\_risk & 0.0727 & 0.1150 & 0.1179 \\
openness\_legacy & 0.1285 & 0.1250 & 0.0688 \\
product\_fit & 0.1359 & 0.0925 & 0.2230 \\
\bottomrule
\end{tabular}
\end{table}
```
