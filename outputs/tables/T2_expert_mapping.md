# T2c. Criterion → legacy Excel variable mapping

Unmapped criteria are listed explicitly. SMAA dispersion for unmapped uses the empirical SD of mapped experts within the same factor.

| criterion   | factor          | legacy_variables   | mapped   |
|:------------|:----------------|:-------------------|:---------|
| ASIASH      | competition     | CUTA               | True     |
| CULT        | product_fit     | CUDI               | True     |
| DIST        | cost_access     | INTC               | True     |
| EOC         | openness_legacy | CLI                | True     |
| FTA         | cost_access     | PPAD               | True     |
| GDPPC       | demand          | unmapped           | False    |
| GOV         | institutional   | FSIN, INRI, DEIN   | True     |
| GRW         | demand          | unmapped           | False    |
| HHI         | competition     | CCTI               | True     |
| IMPC        | demand          | unmapped           | False    |
| IMPV        | demand          | unmapped           | False    |
| INFL        | macro_risk      | INAN               | True     |
| LANG        | product_fit     | GLIN               | True     |
| LPI         | logistics       | LPIN               | True     |
| REEXP       | openness_legacy | unmapped           | False    |
| TARIF       | cost_access     | CIBC               | True     |
| UNEMP       | macro_risk      | UNRA               | True     |
| UVGAP       | product_fit     | unmapped           | False    |

## Booktabs (copy into manuscript; not a repo .tex file)

```latex
\begin{table}[htbp]
\centering
\caption{T2c. Criterion → legacy Excel variable mapping}
\label{tab:T2_expert_mapping}
\begin{tabular}{llll}
\toprule
criterion & factor & legacy\_variables & mapped \\
\midrule
ASIASH & competition & CUTA & True \\
CULT & product\_fit & CUDI & True \\
DIST & cost\_access & INTC & True \\
EOC & openness\_legacy & CLI & True \\
FTA & cost\_access & PPAD & True \\
GDPPC & demand & unmapped & False \\
GOV & institutional & FSIN, INRI, DEIN & True \\
GRW & demand & unmapped & False \\
HHI & competition & CCTI & True \\
IMPC & demand & unmapped & False \\
IMPV & demand & unmapped & False \\
INFL & macro\_risk & INAN & True \\
LANG & product\_fit & GLIN & True \\
LPI & logistics & LPIN & True \\
REEXP & openness\_legacy & unmapped & False \\
TARIF & cost\_access & CIBC & True \\
UNEMP & macro\_risk & UNRA & True \\
UVGAP & product\_fit & unmapped & False \\
\bottomrule
\end{tabular}
\end{table}
```
