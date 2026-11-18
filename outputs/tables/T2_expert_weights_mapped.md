# T2b. IMSFE 2.0 factor weights derived from expert means

| imsfe_factor    |   weight | legacy_map       |
|:----------------|---------:|:-----------------|
| cost_access     |   0.161  | COST             |
| competition     |   0.145  | COMM             |
| logistics       |   0.1385 | LOGI             |
| product_fit     |   0.0925 | CULT             |
| institutional   |   0.098  | POLI             |
| macro_risk      |   0.115  | ECON             |
| demand          |   0.125  | (equal residual) |
| openness_legacy |   0.125  | (equal residual) |

## Booktabs (copy into manuscript; not a repo .tex file)

```latex
\begin{table}[htbp]
\centering
\caption{T2b. IMSFE 2.0 factor weights derived from expert means}
\label{tab:T2_expert_weights_mapped}
\begin{tabular}{lll}
\toprule
imsfe\_factor & weight & legacy\_map \\
\midrule
cost\_access & 0.1610 & COST \\
competition & 0.1450 & COMM \\
logistics & 0.1385 & LOGI \\
product\_fit & 0.0925 & CULT \\
institutional & 0.0980 & POLI \\
macro\_risk & 0.1150 & ECON \\
demand & 0.1250 & (equal residual) \\
openness\_legacy & 0.1250 & (equal residual) \\
\bottomrule
\end{tabular}
\end{table}
```
