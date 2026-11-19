# T6b. Ablation level metrics

| method        | metric   |   mean |   ci95_low |   ci95_high |   n_blocks |
|:--------------|:---------|-------:|-----------:|------------:|-----------:|
| base_macro    | ndcg@10  | 0.7159 |     0.6657 |      0.7639 |         28 |
| plus_fit      | ndcg@10  | 0.7213 |     0.6733 |      0.7668 |         28 |
| plus_fit_comp | ndcg@10  | 0.7189 |     0.6723 |      0.7685 |         28 |

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
base\_macro & ndcg@10 & 0.7159 & 0.6657 & 0.7639 & 28 \\
plus\_fit & ndcg@10 & 0.7213 & 0.6733 & 0.7668 & 28 \\
plus\_fit\_comp & ndcg@10 & 0.7189 & 0.6723 & 0.7685 & 28 \\
\bottomrule
\end{tabular}
\end{table}
```
