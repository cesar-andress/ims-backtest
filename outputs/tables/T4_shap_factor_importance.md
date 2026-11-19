# T4c. SHAP vs expert vs learned factor shares

| factor          |   shap_share |   expert_share |   learned_share |
|:----------------|-------------:|---------------:|----------------:|
| competition     |       0.0888 |         0.145  |          0.1084 |
| cost_access     |       0.2429 |         0.161  |          0.2677 |
| demand          |       0.2135 |         0.125  |          0.0934 |
| institutional   |       0.0979 |         0.098  |          0.0732 |
| logistics       |       0.0193 |         0.1385 |          0.1035 |
| macro_risk      |       0.0671 |         0.115  |          0.1912 |
| openness_legacy |       0.1006 |         0.125  |          0.0934 |
| product_fit     |       0.1698 |         0.0925 |          0.0691 |

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
competition & 0.0888 & 0.1450 & 0.1084 \\
cost\_access & 0.2429 & 0.1610 & 0.2677 \\
demand & 0.2135 & 0.1250 & 0.0934 \\
institutional & 0.0979 & 0.0980 & 0.0732 \\
logistics & 0.0193 & 0.1385 & 0.1035 \\
macro\_risk & 0.0671 & 0.1150 & 0.1912 \\
openness\_legacy & 0.1006 & 0.1250 & 0.0934 \\
product\_fit & 0.1698 & 0.0925 & 0.0691 \\
\bottomrule
\end{tabular}
\end{table}
```
