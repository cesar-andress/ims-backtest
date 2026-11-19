# T5. PPML: scores / factors and exports

| model                    | term          |   estimate |   std_error |   ci95_low |   ci95_high |   n_obs | formula                                                                                      | notes                                                                                                                    |
|:-------------------------|:--------------|-----------:|------------:|-----------:|------------:|--------:|:---------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------|
| y_level_on_ims_score     | ims_score     |     1.3853 |      0.4102 |     0.5813 |      2.1893 |   1,680 | y_level ~ ims_score | oy + iso3_d                                                            | cluster=pair; horizon=k1                                                                                                 |
| y_level_on_factor_scores | demand        |     1.3809 |      0.2787 |     0.8347 |      1.9271 |   1,260 | y_level ~ demand + cost_access + competition + product_fit + institutional + macro_risk | oy | cluster=pair; horizon=k1; factors=['demand', 'cost_access', 'competition', 'product_fit', 'institutional', 'macro_risk'] |
| y_level_on_factor_scores | cost_access   |     0.6369 |      0.1515 |     0.3399 |      0.9339 |   1,260 | y_level ~ demand + cost_access + competition + product_fit + institutional + macro_risk | oy | cluster=pair; horizon=k1; factors=['demand', 'cost_access', 'competition', 'product_fit', 'institutional', 'macro_risk'] |
| y_level_on_factor_scores | competition   |    -0.221  |      0.1633 |    -0.541  |      0.099  |   1,260 | y_level ~ demand + cost_access + competition + product_fit + institutional + macro_risk | oy | cluster=pair; horizon=k1; factors=['demand', 'cost_access', 'competition', 'product_fit', 'institutional', 'macro_risk'] |
| y_level_on_factor_scores | product_fit   |     0.294  |      0.1468 |     0.0062 |      0.5818 |   1,260 | y_level ~ demand + cost_access + competition + product_fit + institutional + macro_risk | oy | cluster=pair; horizon=k1; factors=['demand', 'cost_access', 'competition', 'product_fit', 'institutional', 'macro_risk'] |
| y_level_on_factor_scores | institutional |    -0.2194 |      0.1436 |    -0.5009 |      0.0622 |   1,260 | y_level ~ demand + cost_access + competition + product_fit + institutional + macro_risk | oy | cluster=pair; horizon=k1; factors=['demand', 'cost_access', 'competition', 'product_fit', 'institutional', 'macro_risk'] |
| y_level_on_factor_scores | macro_risk    |    -0.1255 |      0.0969 |    -0.3154 |      0.0645 |   1,260 | y_level ~ demand + cost_access + competition + product_fit + institutional + macro_risk | oy | cluster=pair; horizon=k1; factors=['demand', 'cost_access', 'competition', 'product_fit', 'institutional', 'macro_risk'] |

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
y\_level\_on\_ims\_score & ims\_score & 1.3853 & 0.4102 & 0.5813 & 2.1893 & 1,680 & y\_level ~ ims\_score | oy + iso3\_d & cluster=pair; horizon=k1 \\
y\_level\_on\_factor\_scores & demand & 1.3809 & 0.2787 & 0.8347 & 1.9271 & 1,260 & y\_level ~ demand + cost\_access + competition + product\_fit + institutional + macro\_risk | oy & cluster=pair; horizon=k1; factors=['demand', 'cost\_access', 'competition', 'product\_fit', 'institutional', 'macro\_risk'] \\
y\_level\_on\_factor\_scores & cost\_access & 0.6369 & 0.1515 & 0.3399 & 0.9339 & 1,260 & y\_level ~ demand + cost\_access + competition + product\_fit + institutional + macro\_risk | oy & cluster=pair; horizon=k1; factors=['demand', 'cost\_access', 'competition', 'product\_fit', 'institutional', 'macro\_risk'] \\
y\_level\_on\_factor\_scores & competition & -0.2210 & 0.1633 & -0.5410 & 0.0990 & 1,260 & y\_level ~ demand + cost\_access + competition + product\_fit + institutional + macro\_risk | oy & cluster=pair; horizon=k1; factors=['demand', 'cost\_access', 'competition', 'product\_fit', 'institutional', 'macro\_risk'] \\
y\_level\_on\_factor\_scores & product\_fit & 0.2940 & 0.1468 & 0.0062 & 0.5818 & 1,260 & y\_level ~ demand + cost\_access + competition + product\_fit + institutional + macro\_risk | oy & cluster=pair; horizon=k1; factors=['demand', 'cost\_access', 'competition', 'product\_fit', 'institutional', 'macro\_risk'] \\
y\_level\_on\_factor\_scores & institutional & -0.2194 & 0.1436 & -0.5009 & 0.0622 & 1,260 & y\_level ~ demand + cost\_access + competition + product\_fit + institutional + macro\_risk | oy & cluster=pair; horizon=k1; factors=['demand', 'cost\_access', 'competition', 'product\_fit', 'institutional', 'macro\_risk'] \\
y\_level\_on\_factor\_scores & macro\_risk & -0.1255 & 0.0969 & -0.3154 & 0.0645 & 1,260 & y\_level ~ demand + cost\_access + competition + product\_fit + institutional + macro\_risk | oy & cluster=pair; horizon=k1; factors=['demand', 'cost\_access', 'competition', 'product\_fit', 'institutional', 'macro\_risk'] \\
\bottomrule
\end{tabular}
\end{table}
```
