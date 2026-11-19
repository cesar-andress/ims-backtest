# T8. Colombia case: top destinations with SMAA probabilities

| dest   | country       |   score |   rank |   p_top1 |   p_top5 |   rank_q05 |   rank_q95 |
|:-------|:--------------|--------:|-------:|---------:|---------:|-----------:|-----------:|
| NLD    | Netherlands   |  8.3414 |      1 |   0.5845 |   0.9995 |          1 |          3 |
| IRL    | Ireland       |  8.2688 |      2 |   0.1831 |   0.9745 |          1 |          4 |
| SGP    | Singapore     |  8.2102 |      3 |   0.2074 |   0.8627 |          1 |          9 |
| DNK    | Denmark       |  8.0811 |      4 |   0.0206 |   0.7801 |          2 |          8 |
| BEL    | Belgium       |  8.0328 |      5 |   0      |   0.8318 |          3 |          6 |
| AUT    | Austria       |  7.8678 |      6 |   0      |   0.0127 |          6 |         12 |
| PRT    | Portugal      |  7.8086 |      7 |   0.0014 |   0.124  |          4 |         17 |
| DEU    | Germany       |  7.7935 |      8 |   0      |   0.0467 |          6 |         17 |
| ITA    | Italy         |  7.7798 |      9 |   0.0001 |   0.0644 |          5 |         19 |
| HKG    | Hong Kong SAR |  7.7668 |     10 |   0      |   0.1895 |          4 |         25 |

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
NLD & Netherlands & 8.3414 & 1 & 0.5845 & 0.9995 & 1.0000 & 3.0000 \\
IRL & Ireland & 8.2688 & 2 & 0.1831 & 0.9745 & 1.0000 & 4.0000 \\
SGP & Singapore & 8.2102 & 3 & 0.2074 & 0.8627 & 1.0000 & 9.0000 \\
DNK & Denmark & 8.0811 & 4 & 0.0206 & 0.7801 & 2.0000 & 8.0000 \\
BEL & Belgium & 8.0328 & 5 & 0.0000 & 0.8318 & 3.0000 & 6.0000 \\
AUT & Austria & 7.8678 & 6 & 0.0000 & 0.0127 & 6.0000 & 12.0000 \\
PRT & Portugal & 7.8086 & 7 & 0.0014 & 0.1240 & 4.0000 & 17.0000 \\
DEU & Germany & 7.7935 & 8 & 0.0000 & 0.0467 & 6.0000 & 17.0000 \\
ITA & Italy & 7.7798 & 9 & 0.0001 & 0.0644 & 5.0000 & 19.0000 \\
HKG & Hong Kong SAR & 7.7668 & 10 & 0.0000 & 0.1895 & 4.0000 & 25.0000 \\
\bottomrule
\end{tabular}
\end{table}
```
