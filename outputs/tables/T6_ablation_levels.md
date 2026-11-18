# T6b. Ablation level metrics

| method        | metric   |   mean |   ci95_low |   ci95_high |   n_blocks |
|:--------------|:---------|-------:|-----------:|------------:|-----------:|
| base_macro    | ndcg@10  | 0.7166 |     0.667  |      0.764  |         28 |
| plus_fit      | ndcg@10  | 0.8405 |     0.8028 |      0.8788 |         28 |
| plus_fit_comp | ndcg@10  | 0.8365 |     0.8034 |      0.8697 |         28 |

## Booktabs (copy into manuscript; not a repo .tex file)

```latex
\begin{table}[htbp]
\centering
\caption{T6b. Ablation level metrics}
\label{tab:T6_ablation_levels}
\begin{tabular}{llllll}
\toprule
method & metric & mean & ci95\_low & ci95\_high & n\_blocks \\
\midrule
base\_macro & ndcg@10 & 0.7166 & 0.6670 & 0.7640 & 28 \\
plus\_fit & ndcg@10 & 0.8405 & 0.8028 & 0.8788 & 28 \\
plus\_fit\_comp & ndcg@10 & 0.8365 & 0.8034 & 0.8697 & 28 \\
\bottomrule
\end{tabular}
\end{table}
```
