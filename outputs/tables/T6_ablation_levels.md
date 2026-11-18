# T6b. Ablation level metrics

| method        | metric   |   mean |   ci95_low |   ci95_high |   n_blocks |
|:--------------|:---------|-------:|-----------:|------------:|-----------:|
| base_macro    | ndcg@10  | 0.7166 |     0.667  |      0.764  |         28 |
| plus_fit      | ndcg@10  | 0.7364 |     0.689  |      0.7803 |         28 |
| plus_fit_comp | ndcg@10  | 0.7398 |     0.6963 |      0.7848 |         28 |

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
plus\_fit & ndcg@10 & 0.7364 & 0.6890 & 0.7803 & 28 \\
plus\_fit\_comp & ndcg@10 & 0.7398 & 0.6963 & 0.7848 & 28 \\
\bottomrule
\end{tabular}
\end{table}
```
