# A1. Extra robustness: origins, horizons, thresholds, chapters

WSM + minmax + expert_mean. Chapter rows with status=skipped_no_panel require a separate `imsfe build --chapter` run.

| sweep          | origin   |   hs_chapter |   horizon_k |   entry_threshold_usd | status           |   mean_ndcg@10 |   n_blocks |
|:---------------|:---------|-------------:|------------:|----------------------:|:-----------------|---------------:|-----------:|
| origin_horizon | COL      |           64 |           1 |                50,000 | ok               |         0.7605 |          4 |
| origin_horizon | COL      |           64 |           3 |                50,000 | ok               |         0.8426 |          2 |
| origin_horizon | PER      |           64 |           1 |                50,000 | ok               |         0.799  |          4 |
| origin_horizon | PER      |           64 |           3 |                50,000 | ok               |         0.7346 |          2 |
| origin_horizon | MEX      |           64 |           1 |                50,000 | ok               |         0.6818 |          4 |
| origin_horizon | MEX      |           64 |           3 |                50,000 | ok               |         0.775  |          2 |
| origin_horizon | CHL      |           64 |           1 |                50,000 | ok               |         0.844  |          4 |
| origin_horizon | CHL      |           64 |           3 |                50,000 | ok               |         0.8047 |          2 |
| origin_horizon | ECU      |           64 |           1 |                50,000 | ok               |         0.8031 |          4 |
| origin_horizon | ECU      |           64 |           3 |                50,000 | ok               |         0.8834 |          2 |
| origin_horizon | BRA      |           64 |           1 |                50,000 | ok               |         0.5786 |          4 |
| origin_horizon | BRA      |           64 |           3 |                50,000 | ok               |         0.6724 |          2 |
| origin_horizon | ARG      |           64 |           1 |                50,000 | ok               |         0.838  |          4 |
| origin_horizon | ARG      |           64 |           3 |                50,000 | ok               |         0.8707 |          2 |
| threshold      | ALL      |           64 |           1 |                10,000 | ok               |         0.6701 |         28 |
| threshold      | ALL      |           64 |           3 |                10,000 | ok               |         0.7002 |         14 |
| threshold      | ALL      |           64 |           1 |                50,000 | ok               |         0.7579 |         28 |
| threshold      | ALL      |           64 |           3 |                50,000 | ok               |         0.7976 |         14 |
| threshold      | ALL      |           64 |           1 |               100,000 | ok               |         0.7835 |         28 |
| threshold      | ALL      |           64 |           3 |               100,000 | ok               |         0.8259 |         14 |
| chapter        | ALL      |           64 |           1 |                50,000 | ok               |         0.7579 |         28 |
| chapter        | ALL      |           61 |           1 |                50,000 | skipped_no_panel |                |          0 |
| chapter        | ALL      |           62 |           1 |                50,000 | skipped_no_panel |                |          0 |
| chapter        | ALL      |           42 |           1 |                50,000 | skipped_no_panel |                |          0 |
| chapter        | ALL      |           09 |           1 |                50,000 | skipped_no_panel |                |          0 |

## Booktabs (copy into manuscript; not a repo .tex file)

```latex
\begin{table}[htbp]
\centering
\caption{A1. Extra robustness: origins, horizons, thresholds, chapters}
\label{tab:A1_extra_robustness}
\begin{tabular}{llllllll}
\toprule
sweep & origin & hs\_chapter & horizon\_k & entry\_threshold\_usd & status & mean\_ndcg@10 & n\_blocks \\
\midrule
origin\_horizon & COL & 64 & 1 & 50,000 & ok & 0.7605 & 4 \\
origin\_horizon & COL & 64 & 3 & 50,000 & ok & 0.8426 & 2 \\
origin\_horizon & PER & 64 & 1 & 50,000 & ok & 0.7990 & 4 \\
origin\_horizon & PER & 64 & 3 & 50,000 & ok & 0.7346 & 2 \\
origin\_horizon & MEX & 64 & 1 & 50,000 & ok & 0.6818 & 4 \\
origin\_horizon & MEX & 64 & 3 & 50,000 & ok & 0.7750 & 2 \\
origin\_horizon & CHL & 64 & 1 & 50,000 & ok & 0.8440 & 4 \\
origin\_horizon & CHL & 64 & 3 & 50,000 & ok & 0.8047 & 2 \\
origin\_horizon & ECU & 64 & 1 & 50,000 & ok & 0.8031 & 4 \\
origin\_horizon & ECU & 64 & 3 & 50,000 & ok & 0.8834 & 2 \\
origin\_horizon & BRA & 64 & 1 & 50,000 & ok & 0.5786 & 4 \\
origin\_horizon & BRA & 64 & 3 & 50,000 & ok & 0.6724 & 2 \\
origin\_horizon & ARG & 64 & 1 & 50,000 & ok & 0.8380 & 4 \\
origin\_horizon & ARG & 64 & 3 & 50,000 & ok & 0.8707 & 2 \\
threshold & ALL & 64 & 1 & 10,000 & ok & 0.6701 & 28 \\
threshold & ALL & 64 & 3 & 10,000 & ok & 0.7002 & 14 \\
threshold & ALL & 64 & 1 & 50,000 & ok & 0.7579 & 28 \\
threshold & ALL & 64 & 3 & 50,000 & ok & 0.7976 & 14 \\
threshold & ALL & 64 & 1 & 100,000 & ok & 0.7835 & 28 \\
threshold & ALL & 64 & 3 & 100,000 & ok & 0.8259 & 14 \\
chapter & ALL & 64 & 1 & 50,000 & ok & 0.7579 & 28 \\
chapter & ALL & 61 & 1 & 50,000 & skipped\_no\_panel &  & 0 \\
chapter & ALL & 62 & 1 & 50,000 & skipped\_no\_panel &  & 0 \\
chapter & ALL & 42 & 1 & 50,000 & skipped\_no\_panel &  & 0 \\
chapter & ALL & 09 & 1 & 50,000 & skipped\_no\_panel &  & 0 \\
\bottomrule
\end{tabular}
\end{table}
```
