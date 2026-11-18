# T5. PPML: scores / factors and exports

| model                    | term          |   estimate |   std_error |   ci95_low |   ci95_high |   n_obs | formula                                                                                      | notes                                                                                                                    |
|:-------------------------|:--------------|-----------:|------------:|-----------:|------------:|--------:|:---------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------|
| y_level_on_ims_score     | ims_score     |     0.613  |      0.2112 |     0.199  |      1.0269 |     700 | y_level ~ ims_score | oy + iso3_d                                                            | cluster=pair; horizon=k1                                                                                                 |
| y_level_on_factor_scores | demand        |     1.3372 |      0.2595 |     0.8285 |      1.8459 |     528 | y_level ~ demand + cost_access + competition + product_fit + institutional + macro_risk | oy | cluster=pair; horizon=k1; factors=['demand', 'cost_access', 'competition', 'product_fit', 'institutional', 'macro_risk'] |
| y_level_on_factor_scores | cost_access   |     0.8063 |      0.2008 |     0.4127 |      1.1999 |     528 | y_level ~ demand + cost_access + competition + product_fit + institutional + macro_risk | oy | cluster=pair; horizon=k1; factors=['demand', 'cost_access', 'competition', 'product_fit', 'institutional', 'macro_risk'] |
| y_level_on_factor_scores | competition   |    -0.1216 |      0.1002 |    -0.318  |      0.0748 |     528 | y_level ~ demand + cost_access + competition + product_fit + institutional + macro_risk | oy | cluster=pair; horizon=k1; factors=['demand', 'cost_access', 'competition', 'product_fit', 'institutional', 'macro_risk'] |
| y_level_on_factor_scores | product_fit   |     0.3811 |      0.1235 |     0.1391 |      0.6232 |     528 | y_level ~ demand + cost_access + competition + product_fit + institutional + macro_risk | oy | cluster=pair; horizon=k1; factors=['demand', 'cost_access', 'competition', 'product_fit', 'institutional', 'macro_risk'] |
| y_level_on_factor_scores | institutional |    -0.7697 |      0.1335 |    -1.0313 |     -0.5081 |     528 | y_level ~ demand + cost_access + competition + product_fit + institutional + macro_risk | oy | cluster=pair; horizon=k1; factors=['demand', 'cost_access', 'competition', 'product_fit', 'institutional', 'macro_risk'] |
| y_level_on_factor_scores | macro_risk    |     0.0205 |      0.0941 |    -0.164  |      0.2051 |     528 | y_level ~ demand + cost_access + competition + product_fit + institutional + macro_risk | oy | cluster=pair; horizon=k1; factors=['demand', 'cost_access', 'competition', 'product_fit', 'institutional', 'macro_risk'] |

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
y\_level\_on\_ims\_score & ims\_score & 0.6130 & 0.2112 & 0.1990 & 1.0269 & 700 & y\_level ~ ims\_score | oy + iso3\_d & cluster=pair; horizon=k1 \\
y\_level\_on\_factor\_scores & demand & 1.3372 & 0.2595 & 0.8285 & 1.8459 & 528 & y\_level ~ demand + cost\_access + competition + product\_fit + institutional + macro\_risk | oy & cluster=pair; horizon=k1; factors=['demand', 'cost\_access', 'competition', 'product\_fit', 'institutional', 'macro\_risk'] \\
y\_level\_on\_factor\_scores & cost\_access & 0.8063 & 0.2008 & 0.4127 & 1.1999 & 528 & y\_level ~ demand + cost\_access + competition + product\_fit + institutional + macro\_risk | oy & cluster=pair; horizon=k1; factors=['demand', 'cost\_access', 'competition', 'product\_fit', 'institutional', 'macro\_risk'] \\
y\_level\_on\_factor\_scores & competition & -0.1216 & 0.1002 & -0.3180 & 0.0748 & 528 & y\_level ~ demand + cost\_access + competition + product\_fit + institutional + macro\_risk | oy & cluster=pair; horizon=k1; factors=['demand', 'cost\_access', 'competition', 'product\_fit', 'institutional', 'macro\_risk'] \\
y\_level\_on\_factor\_scores & product\_fit & 0.3811 & 0.1235 & 0.1391 & 0.6232 & 528 & y\_level ~ demand + cost\_access + competition + product\_fit + institutional + macro\_risk | oy & cluster=pair; horizon=k1; factors=['demand', 'cost\_access', 'competition', 'product\_fit', 'institutional', 'macro\_risk'] \\
y\_level\_on\_factor\_scores & institutional & -0.7697 & 0.1335 & -1.0313 & -0.5081 & 528 & y\_level ~ demand + cost\_access + competition + product\_fit + institutional + macro\_risk | oy & cluster=pair; horizon=k1; factors=['demand', 'cost\_access', 'competition', 'product\_fit', 'institutional', 'macro\_risk'] \\
y\_level\_on\_factor\_scores & macro\_risk & 0.0205 & 0.0941 & -0.1640 & 0.2051 & 528 & y\_level ~ demand + cost\_access + competition + product\_fit + institutional + macro\_risk | oy & cluster=pair; horizon=k1; factors=['demand', 'cost\_access', 'competition', 'product\_fit', 'institutional', 'macro\_risk'] \\
\bottomrule
\end{tabular}
\end{table}
```
