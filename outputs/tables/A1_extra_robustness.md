# A1. Extra robustness: origins, horizons, thresholds, chapters

WSM + minmax + expert_mean. Chapter rows with status=skipped_no_panel require a separate `imsfe build --chapter` run.

| sweep          | origin   |   hs_chapter |   horizon_k |   entry_threshold_usd | status           |   mean_ndcg@10 |   n_blocks |
|:---------------|:---------|-------------:|------------:|----------------------:|:-----------------|---------------:|-----------:|
| origin_horizon | COL      |           64 |           1 |                50,000 | ok               |         0.7632 |          4 |
| origin_horizon | COL      |           64 |           3 |                50,000 | ok               |         0.8224 |          2 |
| origin_horizon | PER      |           64 |           1 |                50,000 | ok               |         0.7842 |          4 |
| origin_horizon | PER      |           64 |           3 |                50,000 | ok               |         0.7164 |          2 |
| origin_horizon | MEX      |           64 |           1 |                50,000 | ok               |         0.6567 |          4 |
| origin_horizon | MEX      |           64 |           3 |                50,000 | ok               |         0.7622 |          2 |
| origin_horizon | CHL      |           64 |           1 |                50,000 | ok               |         0.8337 |          4 |
| origin_horizon | CHL      |           64 |           3 |                50,000 | ok               |         0.7919 |          2 |
| origin_horizon | ECU      |           64 |           1 |                50,000 | ok               |         0.7861 |          4 |
| origin_horizon | ECU      |           64 |           3 |                50,000 | ok               |         0.8834 |          2 |
| origin_horizon | BRA      |           64 |           1 |                50,000 | ok               |         0.5322 |          4 |
| origin_horizon | BRA      |           64 |           3 |                50,000 | ok               |         0.6002 |          2 |
| origin_horizon | ARG      |           64 |           1 |                50,000 | ok               |         0.8106 |          4 |
| origin_horizon | ARG      |           64 |           3 |                50,000 | ok               |         0.8181 |          2 |
| threshold      | ALL      |           64 |           1 |                10,000 | ok               |         0.6562 |         28 |
| threshold      | ALL      |           64 |           3 |                10,000 | ok               |         0.6754 |         14 |
| threshold      | ALL      |           64 |           1 |                50,000 | ok               |         0.7381 |         28 |
| threshold      | ALL      |           64 |           3 |                50,000 | ok               |         0.7706 |         14 |
| threshold      | ALL      |           64 |           1 |               100,000 | ok               |         0.7741 |         28 |
| threshold      | ALL      |           64 |           3 |               100,000 | ok               |         0.8024 |         14 |
| chapter        | ALL      |           64 |           1 |                50,000 | ok               |         0.7381 |         28 |
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
origin\_horizon & COL & 64 & 1 & 50,000 & ok & 0.7632 & 4 \\
origin\_horizon & COL & 64 & 3 & 50,000 & ok & 0.8224 & 2 \\
origin\_horizon & PER & 64 & 1 & 50,000 & ok & 0.7842 & 4 \\
origin\_horizon & PER & 64 & 3 & 50,000 & ok & 0.7164 & 2 \\
origin\_horizon & MEX & 64 & 1 & 50,000 & ok & 0.6567 & 4 \\
origin\_horizon & MEX & 64 & 3 & 50,000 & ok & 0.7622 & 2 \\
origin\_horizon & CHL & 64 & 1 & 50,000 & ok & 0.8337 & 4 \\
origin\_horizon & CHL & 64 & 3 & 50,000 & ok & 0.7919 & 2 \\
origin\_horizon & ECU & 64 & 1 & 50,000 & ok & 0.7861 & 4 \\
origin\_horizon & ECU & 64 & 3 & 50,000 & ok & 0.8834 & 2 \\
origin\_horizon & BRA & 64 & 1 & 50,000 & ok & 0.5322 & 4 \\
origin\_horizon & BRA & 64 & 3 & 50,000 & ok & 0.6002 & 2 \\
origin\_horizon & ARG & 64 & 1 & 50,000 & ok & 0.8106 & 4 \\
origin\_horizon & ARG & 64 & 3 & 50,000 & ok & 0.8181 & 2 \\
threshold & ALL & 64 & 1 & 10,000 & ok & 0.6562 & 28 \\
threshold & ALL & 64 & 3 & 10,000 & ok & 0.6754 & 14 \\
threshold & ALL & 64 & 1 & 50,000 & ok & 0.7381 & 28 \\
threshold & ALL & 64 & 3 & 50,000 & ok & 0.7706 & 14 \\
threshold & ALL & 64 & 1 & 100,000 & ok & 0.7741 & 28 \\
threshold & ALL & 64 & 3 & 100,000 & ok & 0.8024 & 14 \\
chapter & ALL & 64 & 1 & 50,000 & ok & 0.7381 & 28 \\
chapter & ALL & 61 & 1 & 50,000 & skipped\_no\_panel &  & 0 \\
chapter & ALL & 62 & 1 & 50,000 & skipped\_no\_panel &  & 0 \\
chapter & ALL & 42 & 1 & 50,000 & skipped\_no\_panel &  & 0 \\
chapter & ALL & 09 & 1 & 50,000 & skipped\_no\_panel &  & 0 \\
\bottomrule
\end{tabular}
\end{table}
```
