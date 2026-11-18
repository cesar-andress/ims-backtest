# T4b. Learned vs expert variable weights

| variable   |   learned |   expert_mean |   equal |
|:-----------|----------:|--------------:|--------:|
| DIST       |    0.0597 |        0.0537 |  0.0417 |
| TARIF      |    0.0393 |        0.0537 |  0.0417 |
| FTA        |    0.0935 |        0.0537 |  0.0417 |
| UVGAP      |    0.0195 |        0.0308 |  0.0417 |
| CULT       |    0.0137 |        0.0308 |  0.0417 |
| LANG       |    0.0233 |        0.0308 |  0.0417 |
| LPI        |    0.207  |        0.1385 |  0.125  |
| INFL       |    0.0664 |        0.0575 |  0.0625 |
| UNEMP      |    0.1226 |        0.0575 |  0.0625 |
| ASIASH     |    0.016  |        0.0725 |  0.0625 |
| HHI        |    0.0401 |        0.0725 |  0.0625 |
| GOV        |    0.0525 |        0.098  |  0.125  |
| IMPV       |    0.0284 |        0.0312 |  0.0312 |
| IMPC       |    0.0222 |        0.0312 |  0.0312 |
| GRW        |    0.0574 |        0.0312 |  0.0312 |
| GDPPC      |    0.0288 |        0.0312 |  0.0312 |
| EOC        |    0.0537 |        0.0625 |  0.0625 |
| REEXP      |    0.0558 |        0.0625 |  0.0625 |

## Booktabs (copy into manuscript; not a repo .tex file)

```latex
\begin{table}[htbp]
\centering
\caption{T4b. Learned vs expert variable weights}
\label{tab:T4_learned_vs_expert_weights}
\begin{tabular}{llll}
\toprule
variable & learned & expert\_mean & equal \\
\midrule
DIST & 0.0597 & 0.0537 & 0.0417 \\
TARIF & 0.0393 & 0.0537 & 0.0417 \\
FTA & 0.0935 & 0.0537 & 0.0417 \\
UVGAP & 0.0195 & 0.0308 & 0.0417 \\
CULT & 0.0137 & 0.0308 & 0.0417 \\
LANG & 0.0233 & 0.0308 & 0.0417 \\
LPI & 0.2070 & 0.1385 & 0.1250 \\
INFL & 0.0664 & 0.0575 & 0.0625 \\
UNEMP & 0.1226 & 0.0575 & 0.0625 \\
ASIASH & 0.0160 & 0.0725 & 0.0625 \\
HHI & 0.0401 & 0.0725 & 0.0625 \\
GOV & 0.0525 & 0.0980 & 0.1250 \\
IMPV & 0.0284 & 0.0312 & 0.0312 \\
IMPC & 0.0222 & 0.0312 & 0.0312 \\
GRW & 0.0574 & 0.0312 & 0.0312 \\
GDPPC & 0.0288 & 0.0312 & 0.0312 \\
EOC & 0.0537 & 0.0625 & 0.0625 \\
REEXP & 0.0558 & 0.0625 & 0.0625 \\
\bottomrule
\end{tabular}
\end{table}
```
