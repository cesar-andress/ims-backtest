# T6. Ablation deltas (fit / competition) with bootstrap CIs

| contrast                   | metric   |   delta_mean |   ci95_low |   ci95_high |   n_blocks |
|:---------------------------|:---------|-------------:|-----------:|------------:|-----------:|
| plus_fit - base_macro      | ndcg@10  |       0.0199 |    -0.0068 |      0.0496 |         28 |
| plus_fit_comp - base_macro | ndcg@10  |       0.0232 |    -0.0119 |      0.0597 |         28 |

## Booktabs (copy into manuscript; not a repo .tex file)

```latex
\begin{table}[htbp]
\centering
\caption{T6. Ablation deltas (fit / competition) with bootstrap CIs}
\label{tab:T6_ablation}
\begin{tabular}{llllll}
\toprule
contrast & metric & delta\_mean & ci95\_low & ci95\_high & n\_blocks \\
\midrule
plus\_fit - base\_macro & ndcg@10 & 0.0199 & -0.0068 & 0.0496 & 28 \\
plus\_fit\_comp - base\_macro & ndcg@10 & 0.0232 & -0.0119 & 0.0597 & 28 \\
\bottomrule
\end{tabular}
\end{table}
```
