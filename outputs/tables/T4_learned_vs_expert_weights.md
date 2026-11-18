# T4b. Learned vs expert variable weights

| variable   |   learned |   expert_mean |   equal |
|:-----------|----------:|--------------:|--------:|
| DIST       |    0.0581 |        0.0537 |  0.0417 |
| TARIF      |    0.0751 |        0.0537 |  0.0417 |
| FTA        |    0.0404 |        0.0537 |  0.0417 |
| ASIASH     |    0.0716 |        0.0725 |  0.0625 |
| HHI        |    0.0722 |        0.0725 |  0.0625 |
| GOV        |    0.0995 |        0.098  |  0.125  |
| INFL       |    0.0619 |        0.0575 |  0.0625 |
| UNEMP      |    0.056  |        0.0575 |  0.0625 |
| UVGAP      |    0.0551 |        0.0308 |  0.0417 |
| CULT       |    0.0864 |        0.0308 |  0.0417 |
| LANG       |    0.0815 |        0.0308 |  0.0417 |
| LPI        |    0.0934 |        0.1385 |  0.125  |
| IMPV       |    0.0242 |        0.0312 |  0.0312 |
| IMPC       |    0.0175 |        0.0312 |  0.0312 |
| GRW        |    0.022  |        0.0312 |  0.0312 |
| GDPPC      |    0.0162 |        0.0312 |  0.0312 |
| EOC        |    0.0314 |        0.0625 |  0.0625 |
| REEXP      |    0.0373 |        0.0625 |  0.0625 |

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
DIST & 0.0581 & 0.0537 & 0.0417 \\
TARIF & 0.0751 & 0.0537 & 0.0417 \\
FTA & 0.0404 & 0.0537 & 0.0417 \\
ASIASH & 0.0716 & 0.0725 & 0.0625 \\
HHI & 0.0722 & 0.0725 & 0.0625 \\
GOV & 0.0995 & 0.0980 & 0.1250 \\
INFL & 0.0619 & 0.0575 & 0.0625 \\
UNEMP & 0.0560 & 0.0575 & 0.0625 \\
UVGAP & 0.0551 & 0.0308 & 0.0417 \\
CULT & 0.0864 & 0.0308 & 0.0417 \\
LANG & 0.0815 & 0.0308 & 0.0417 \\
LPI & 0.0934 & 0.1385 & 0.1250 \\
IMPV & 0.0242 & 0.0312 & 0.0312 \\
IMPC & 0.0175 & 0.0312 & 0.0312 \\
GRW & 0.0220 & 0.0312 & 0.0312 \\
GDPPC & 0.0162 & 0.0312 & 0.0312 \\
EOC & 0.0314 & 0.0625 & 0.0625 \\
REEXP & 0.0373 & 0.0625 & 0.0625 \\
\bottomrule
\end{tabular}
\end{table}
```
