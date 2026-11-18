# T5. PPML: scores / factors and exports

| model                    | term          |   estimate |   std_error |   ci95_low |   ci95_high |   n_obs | formula                                                                                      | notes                                                                                                                    |
|:-------------------------|:--------------|-----------:|------------:|-----------:|------------:|--------:|:---------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------|
| y_level_on_ims_score     | ims_score     |     0.9288 |      0.3376 |     0.2671 |      1.5905 |   1,554 | y_level ~ ims_score | oy + iso3_d                                                            | cluster=pair; horizon=k1                                                                                                 |
| y_level_on_factor_scores | demand        |     1.2813 |      0.2098 |     0.87   |      1.6926 |     770 | y_level ~ demand + cost_access + competition + product_fit + institutional + macro_risk | oy | cluster=pair; horizon=k1; factors=['demand', 'cost_access', 'competition', 'product_fit', 'institutional', 'macro_risk'] |
| y_level_on_factor_scores | cost_access   |     0.573  |      0.0867 |     0.4031 |      0.7429 |     770 | y_level ~ demand + cost_access + competition + product_fit + institutional + macro_risk | oy | cluster=pair; horizon=k1; factors=['demand', 'cost_access', 'competition', 'product_fit', 'institutional', 'macro_risk'] |
| y_level_on_factor_scores | competition   |    -0.1409 |      0.1315 |    -0.3986 |      0.1168 |     770 | y_level ~ demand + cost_access + competition + product_fit + institutional + macro_risk | oy | cluster=pair; horizon=k1; factors=['demand', 'cost_access', 'competition', 'product_fit', 'institutional', 'macro_risk'] |
| y_level_on_factor_scores | product_fit   |     0.113  |      0.0914 |    -0.0662 |      0.2921 |     770 | y_level ~ demand + cost_access + competition + product_fit + institutional + macro_risk | oy | cluster=pair; horizon=k1; factors=['demand', 'cost_access', 'competition', 'product_fit', 'institutional', 'macro_risk'] |
| y_level_on_factor_scores | institutional |    -0.3346 |      0.1244 |    -0.5785 |     -0.0907 |     770 | y_level ~ demand + cost_access + competition + product_fit + institutional + macro_risk | oy | cluster=pair; horizon=k1; factors=['demand', 'cost_access', 'competition', 'product_fit', 'institutional', 'macro_risk'] |
| y_level_on_factor_scores | macro_risk    |    -0.042  |      0.0719 |    -0.183  |      0.0991 |     770 | y_level ~ demand + cost_access + competition + product_fit + institutional + macro_risk | oy | cluster=pair; horizon=k1; factors=['demand', 'cost_access', 'competition', 'product_fit', 'institutional', 'macro_risk'] |

## Booktabs (copy into manuscript; not a repo .tex file)

```latex
\begin{table}[htbp]
\centering
\caption{T5. PPML: scores / factors and exports}
\label{tab:T5_ppml}
\begin{tabular}{lllllllll}
\toprule
model & term & estimate & std\_error & ci95\_low & ci95\_high & n\_obs & formula & notes \\
\midrule
y\_level\_on\_ims\_score & ims\_score & 0.9288 & 0.3376 & 0.2671 & 1.5905 & 1,554 & y\_level ~ ims\_score | oy + iso3\_d & cluster=pair; horizon=k1 \\
y\_level\_on\_factor\_scores & demand & 1.2813 & 0.2098 & 0.8700 & 1.6926 & 770 & y\_level ~ demand + cost\_access + competition + product\_fit + institutional + macro\_risk | oy & cluster=pair; horizon=k1; factors=['demand', 'cost\_access', 'competition', 'product\_fit', 'institutional', 'macro\_risk'] \\
y\_level\_on\_factor\_scores & cost\_access & 0.5730 & 0.0867 & 0.4031 & 0.7429 & 770 & y\_level ~ demand + cost\_access + competition + product\_fit + institutional + macro\_risk | oy & cluster=pair; horizon=k1; factors=['demand', 'cost\_access', 'competition', 'product\_fit', 'institutional', 'macro\_risk'] \\
y\_level\_on\_factor\_scores & competition & -0.1409 & 0.1315 & -0.3986 & 0.1168 & 770 & y\_level ~ demand + cost\_access + competition + product\_fit + institutional + macro\_risk | oy & cluster=pair; horizon=k1; factors=['demand', 'cost\_access', 'competition', 'product\_fit', 'institutional', 'macro\_risk'] \\
y\_level\_on\_factor\_scores & product\_fit & 0.1130 & 0.0914 & -0.0662 & 0.2921 & 770 & y\_level ~ demand + cost\_access + competition + product\_fit + institutional + macro\_risk | oy & cluster=pair; horizon=k1; factors=['demand', 'cost\_access', 'competition', 'product\_fit', 'institutional', 'macro\_risk'] \\
y\_level\_on\_factor\_scores & institutional & -0.3346 & 0.1244 & -0.5785 & -0.0907 & 770 & y\_level ~ demand + cost\_access + competition + product\_fit + institutional + macro\_risk | oy & cluster=pair; horizon=k1; factors=['demand', 'cost\_access', 'competition', 'product\_fit', 'institutional', 'macro\_risk'] \\
y\_level\_on\_factor\_scores & macro\_risk & -0.0420 & 0.0719 & -0.1830 & 0.0991 & 770 & y\_level ~ demand + cost\_access + competition + product\_fit + institutional + macro\_risk | oy & cluster=pair; horizon=k1; factors=['demand', 'cost\_access', 'competition', 'product\_fit', 'institutional', 'macro\_risk'] \\
\bottomrule
\end{tabular}
\end{table}
```
