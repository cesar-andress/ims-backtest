# T8. Colombia case: top destinations with SMAA probabilities

| dest   | country     |   score |   rank |   p_top1 |   p_top5 |   rank_q05 |   rank_q95 |
|:-------|:------------|--------:|-------:|---------:|---------:|-----------:|-----------:|
| NLD    | Netherlands |  8.1756 |      1 |   0.8939 |   1      |          1 |          2 |
| IRL    | Ireland     |  7.953  |      2 |   0.0542 |   0.9898 |          1 |          3 |
| SGP    | Singapore   |  7.6971 |      3 |   0.0503 |   0.7762 |          1 |         11 |
| BEL    | Belgium     |  7.6786 |      4 |   0      |   0.9619 |          3 |          5 |
| DNK    | Denmark     |  7.6323 |      5 |   0.0015 |   0.8217 |          2 |          7 |
| PRT    | Portugal    |  7.3149 |      6 |   0      |   0.1679 |          4 |         15 |
| DEU    | Germany     |  7.3064 |      7 |   0      |   0.0732 |          5 |         15 |
| SWE    | Sweden      |  7.2509 |      8 |   0      |   0.0168 |          6 |         19 |
| ITA    | Italy       |  7.2475 |      9 |   0      |   0.0485 |          6 |         17 |
| AUT    | Austria     |  7.244  |     10 |   0      |   0.0001 |          7 |         16 |

## Booktabs (copy into manuscript; not a repo .tex file)

```latex
\begin{table}[htbp]
\centering
\caption{T8. Colombia case: top destinations with SMAA probabilities}
\label{tab:T8_smaa_col}
\begin{tabular}{llllllll}
\toprule
dest & country & score & rank & p\_top1 & p\_top5 & rank\_q05 & rank\_q95 \\
\midrule
NLD & Netherlands & 8.1756 & 1 & 0.8939 & 1.0000 & 1.0000 & 2.0000 \\
IRL & Ireland & 7.9530 & 2 & 0.0542 & 0.9898 & 1.0000 & 3.0000 \\
SGP & Singapore & 7.6971 & 3 & 0.0503 & 0.7762 & 1.0000 & 11.0000 \\
BEL & Belgium & 7.6786 & 4 & 0.0000 & 0.9619 & 3.0000 & 5.0000 \\
DNK & Denmark & 7.6323 & 5 & 0.0015 & 0.8217 & 2.0000 & 7.0000 \\
PRT & Portugal & 7.3149 & 6 & 0.0000 & 0.1679 & 4.0000 & 15.0000 \\
DEU & Germany & 7.3064 & 7 & 0.0000 & 0.0732 & 5.0000 & 15.0000 \\
SWE & Sweden & 7.2509 & 8 & 0.0000 & 0.0168 & 6.0000 & 19.0000 \\
ITA & Italy & 7.2475 & 9 & 0.0000 & 0.0485 & 6.0000 & 17.0000 \\
AUT & Austria & 7.2440 & 10 & 0.0000 & 0.0001 & 7.0000 & 16.0000 \\
\bottomrule
\end{tabular}
\end{table}
```
