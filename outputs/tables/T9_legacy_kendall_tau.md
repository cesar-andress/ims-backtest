# T9b. Kendall τ of corrected rankings vs ratio_legacy

| method             |   kendall_tau_vs_ratio_legacy |   p_value |
|:-------------------|------------------------------:|----------:|
| ratio_legacy       |                        1      |         0 |
| minmax             |                        0.8069 |         0 |
| rank               |                        0.7609 |         0 |
| minmax_pref_tariff |                        0.7977 |         0 |

## Booktabs (copy into manuscript; not a repo .tex file)

```latex
\begin{table}[htbp]
\centering
\caption{T9b. Kendall τ of corrected rankings vs ratio_legacy}
\label{tab:T9_legacy_kendall_tau}
\begin{tabular}{lll}
\toprule
method & kendall\_tau\_vs\_ratio\_legacy & p\_value \\
\midrule
ratio\_legacy & 1.0000 & 0.0000 \\
minmax & 0.8069 & 0.0000 \\
rank & 0.7609 & 0.0000 \\
minmax\_pref\_tariff & 0.7977 & 0.0000 \\
\bottomrule
\end{tabular}
\end{table}
```
