# T4b. Learned vs expert variable weights

| variable   |   learned |   expert_mean |   equal | has_train_data   |
|:-----------|----------:|--------------:|--------:|:-----------------|
| IMPV       |    0.0552 |        0.0312 |  0.0312 | True             |
| IMPC       |    0.0274 |        0.0312 |  0.0312 | True             |
| GRW        |    0.0552 |        0.0312 |  0.0312 | True             |
| GDPPC      |    0.0274 |        0.0312 |  0.0312 | True             |
| DIST       |    0.0852 |        0.0537 |  0.0417 | True             |
| TARIF      |    0.0423 |        0.0537 |  0.0417 | True             |
| FTA        |    0.0852 |        0.0537 |  0.0417 | True             |
| LPI        |    0.183  |        0.1385 |  0.125  | True             |
| ASIASH     |    0.0316 |        0.0725 |  0.0625 | True             |
| HHI        |    0.0636 |        0.0725 |  0.0625 | True             |
| UVGAP      |    0.0304 |        0.0308 |  0.0417 | True             |
| CULT       |    0.0613 |        0.0308 |  0.0417 | True             |
| LANG       |    0.0304 |        0.0308 |  0.0417 | True             |
| INFL       |    0.0504 |        0.0575 |  0.0625 | True             |
| UNEMP      |    0.025  |        0.0575 |  0.0625 | True             |
| GOV        |    0.0643 |        0.098  |  0.125  | True             |
| EOC        |    0.0548 |        0.0625 |  0.0625 | True             |
| REEXP      |    0.0272 |        0.0625 |  0.0625 | True             |

## Booktabs (copy into manuscript; not a repo .tex file)

```latex
\begin{table}[htbp]
\centering
\caption{T4b. Learned vs expert variable weights}
\label{tab:T4_learned_vs_expert_weights}
\begin{tabular}{lllll}
\toprule
variable & learned & expert\_mean & equal & has\_train\_data \\
\midrule
IMPV & 0.0552 & 0.0312 & 0.0312 & True \\
IMPC & 0.0274 & 0.0312 & 0.0312 & True \\
GRW & 0.0552 & 0.0312 & 0.0312 & True \\
GDPPC & 0.0274 & 0.0312 & 0.0312 & True \\
DIST & 0.0852 & 0.0537 & 0.0417 & True \\
TARIF & 0.0423 & 0.0537 & 0.0417 & True \\
FTA & 0.0852 & 0.0537 & 0.0417 & True \\
LPI & 0.1830 & 0.1385 & 0.1250 & True \\
ASIASH & 0.0316 & 0.0725 & 0.0625 & True \\
HHI & 0.0636 & 0.0725 & 0.0625 & True \\
UVGAP & 0.0304 & 0.0308 & 0.0417 & True \\
CULT & 0.0613 & 0.0308 & 0.0417 & True \\
LANG & 0.0304 & 0.0308 & 0.0417 & True \\
INFL & 0.0504 & 0.0575 & 0.0625 & True \\
UNEMP & 0.0250 & 0.0575 & 0.0625 & True \\
GOV & 0.0643 & 0.0980 & 0.1250 & True \\
EOC & 0.0548 & 0.0625 & 0.0625 & True \\
REEXP & 0.0272 & 0.0625 & 0.0625 & True \\
\bottomrule
\end{tabular}
\end{table}
```
