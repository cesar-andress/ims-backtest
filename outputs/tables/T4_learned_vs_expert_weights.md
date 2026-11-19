# T4b. Learned vs expert variable weights

| variable   |   learned |   expert_mean |   equal | has_train_data   |
|:-----------|----------:|--------------:|--------:|:-----------------|
| IMPV       |    0.0398 |        0.0312 |  0.0312 | True             |
| IMPC       |    0.0179 |        0.0312 |  0.0312 | True             |
| GRW        |    0.0179 |        0.0312 |  0.0312 | True             |
| GDPPC      |    0.0179 |        0.0312 |  0.0312 | True             |
| DIST       |    0.141  |        0.0537 |  0.0417 | True             |
| TARIF      |    0.0634 |        0.0537 |  0.0417 | True             |
| FTA        |    0.0634 |        0.0537 |  0.0417 | True             |
| LPI        |    0.1035 |        0.1385 |  0.125  | True             |
| ASIASH     |    0.0542 |        0.0725 |  0.0625 | True             |
| HHI        |    0.0542 |        0.0725 |  0.0625 | True             |
| UVGAP      |    0.0364 |        0.0308 |  0.0417 | True             |
| CULT       |    0.0164 |        0.0308 |  0.0417 | True             |
| LANG       |    0.0164 |        0.0308 |  0.0417 | True             |
| INFL       |    0.132  |        0.0575 |  0.0625 | True             |
| UNEMP      |    0.0593 |        0.0575 |  0.0625 | True             |
| GOV        |    0.0732 |        0.098  |  0.125  | True             |
| EOC        |    0.0644 |        0.0625 |  0.0625 | True             |
| REEXP      |    0.029  |        0.0625 |  0.0625 | True             |

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
IMPV & 0.0398 & 0.0312 & 0.0312 & True \\
IMPC & 0.0179 & 0.0312 & 0.0312 & True \\
GRW & 0.0179 & 0.0312 & 0.0312 & True \\
GDPPC & 0.0179 & 0.0312 & 0.0312 & True \\
DIST & 0.1410 & 0.0537 & 0.0417 & True \\
TARIF & 0.0634 & 0.0537 & 0.0417 & True \\
FTA & 0.0634 & 0.0537 & 0.0417 & True \\
LPI & 0.1035 & 0.1385 & 0.1250 & True \\
ASIASH & 0.0542 & 0.0725 & 0.0625 & True \\
HHI & 0.0542 & 0.0725 & 0.0625 & True \\
UVGAP & 0.0364 & 0.0308 & 0.0417 & True \\
CULT & 0.0164 & 0.0308 & 0.0417 & True \\
LANG & 0.0164 & 0.0308 & 0.0417 & True \\
INFL & 0.1320 & 0.0575 & 0.0625 & True \\
UNEMP & 0.0593 & 0.0575 & 0.0625 & True \\
GOV & 0.0732 & 0.0980 & 0.1250 & True \\
EOC & 0.0644 & 0.0625 & 0.0625 & True \\
REEXP & 0.0290 & 0.0625 & 0.0625 & True \\
\bottomrule
\end{tabular}
\end{table}
```
