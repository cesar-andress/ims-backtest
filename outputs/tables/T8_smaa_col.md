# T8. Colombia case: top destinations with SMAA probabilities

| dest   | country     |   score |   rank |   p_top1 |   p_top5 |   rank_q05 |   rank_q95 |
|:-------|:------------|--------:|-------:|---------:|---------:|-----------:|-----------:|
| IRL    | Ireland     |  8.0549 |      1 |   0.7017 |   0.9961 |          1 |          3 |
| NLD    | Netherlands |  7.9245 |      2 |   0.2601 |   0.9987 |          1 |          2 |
| DNK    | Denmark     |  7.6427 |      3 |   0.033  |   0.9101 |          2 |          7 |
| AUT    | Austria     |  7.4381 |      4 |   0      |   0.8391 |          3 |          7 |
| BEL    | Belgium     |  7.2941 |      5 |   0      |   0.3313 |          4 |         11 |
| SWE    | Sweden      |  7.224  |      6 |   0      |   0.2208 |          4 |         19 |
| HRV    | Croatia     |  7.2033 |      7 |   0.0047 |   0.2564 |          3 |         16 |
| DEU    | Germany     |  7.1493 |      8 |   0      |   0.0544 |          5 |         17 |
| GRC    | Greece      |  7.0916 |      9 |   0.0003 |   0.1114 |          4 |         17 |
| CHE    | Switzerland |  7.0781 |     10 |   0      |   0.1301 |          5 |         23 |

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
IRL & Ireland & 8.0549 & 1 & 0.7017 & 0.9961 & 1.0000 & 3.0000 \\
NLD & Netherlands & 7.9245 & 2 & 0.2601 & 0.9987 & 1.0000 & 2.0000 \\
DNK & Denmark & 7.6427 & 3 & 0.0330 & 0.9101 & 2.0000 & 7.0000 \\
AUT & Austria & 7.4381 & 4 & 0.0000 & 0.8391 & 3.0000 & 7.0000 \\
BEL & Belgium & 7.2941 & 5 & 0.0000 & 0.3313 & 4.0000 & 11.0000 \\
SWE & Sweden & 7.2240 & 6 & 0.0000 & 0.2208 & 4.0000 & 19.0000 \\
HRV & Croatia & 7.2033 & 7 & 0.0047 & 0.2564 & 3.0000 & 16.0000 \\
DEU & Germany & 7.1493 & 8 & 0.0000 & 0.0544 & 5.0000 & 17.0000 \\
GRC & Greece & 7.0916 & 9 & 0.0003 & 0.1114 & 4.0000 & 17.0000 \\
CHE & Switzerland & 7.0781 & 10 & 0.0000 & 0.1301 & 5.0000 & 23.0000 \\
\bottomrule
\end{tabular}
\end{table}
```
