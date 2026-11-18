# T1. Variables, sources, direction, and coverage

Coverage is the non-null share of the transformed feature column in the panel.

| variable   | name                                                                | factor          | direction   | source        | transform   |   coverage_pct |
|:-----------|:--------------------------------------------------------------------|:----------------|:------------|:--------------|:------------|---------------:|
| IMPV       | HS chapter imports (USD)                                            | demand          | benefit     | BACI          | log         |         100    |
| IMPC       | HS chapter imports per capita                                       | demand          | benefit     | BACI+WB       | log         |          98.33 |
| GRW        | HS chapter import growth (3-year CAGR)                              | demand          | benefit     | BACI          | none        |          75    |
| GDPPC      | GDP per capita PPP                                                  | demand          | benefit     | WB            | log         |          98.33 |
| DIST       | Population-weighted distance                                        | cost_access     | cost        | CEPII Gravity | log         |          81.94 |
| TARIF      | Applied preferential tariff (AHS), origin to destination            | cost_access     | cost        | WITS/TRAINS   | none        |          37.22 |
| FTA        | Preferential trade agreement in force                               | cost_access     | benefit     | CEPII Gravity | none        |          81.94 |
| LPI        | Logistics Performance Index (overall)                               | logistics       | benefit     | WB            | none        |          40.42 |
| ASIASH     | China+Vietnam share of destination HS imports                       | competition     | cost        | BACI          | none        |         100    |
| HHI        | Supplier concentration (HHI) in destination HS imports              | competition     | cost        | BACI          | none        |         100    |
| UVGAP      | Absolute log unit-value gap (destination imports vs origin exports) | product_fit     | cost        | BACI          | none        |         100    |
| CULT       | Cultural distance (Kogut-Singh, Hofstede 6 dimensions)              | product_fit     | cost        | Hofstede      | none        |          90.48 |
| LANG       | Common official language                                            | product_fit     | benefit     | CEPII Gravity | none        |          81.94 |
| INFL       | Inflation deviation from 2 percent                                  | macro_risk      | cost        | WB            | none        |          40.5  |
| UNEMP      | Unemployment rate                                                   | macro_risk      | cost        | WB            | none        |          24.44 |
| GOV        | Mean Worldwide Governance Indicators                                | institutional   | benefit     | WB WGI        | none        |          98.33 |
| EOC        | External Opening Coefficient (trade/GDP)                            | openness_legacy | benefit     | WB            | none        |          98.19 |
| REEXP      | Re-export intensity (chapter X_j / M_j)                             | openness_legacy | cost        | BACI          | none        |         100    |

## Booktabs (copy into manuscript; not a repo .tex file)

```latex
\begin{table}[htbp]
\centering
\caption{T1. Variables, sources, direction, and coverage}
\label{tab:T1_variables}
\begin{tabular}{lllllll}
\toprule
variable & name & factor & direction & source & transform & coverage\_pct \\
\midrule
IMPV & HS chapter imports (USD) & demand & benefit & BACI & log & 100.000 \\
IMPC & HS chapter imports per capita & demand & benefit & BACI+WB & log & 98.330 \\
GRW & HS chapter import growth (3-year CAGR) & demand & benefit & BACI & none & 75.000 \\
GDPPC & GDP per capita PPP & demand & benefit & WB & log & 98.330 \\
DIST & Population-weighted distance & cost\_access & cost & CEPII Gravity & log & 81.940 \\
TARIF & Applied preferential tariff (AHS), origin to destination & cost\_access & cost & WITS/TRAINS & none & 37.220 \\
FTA & Preferential trade agreement in force & cost\_access & benefit & CEPII Gravity & none & 81.940 \\
LPI & Logistics Performance Index (overall) & logistics & benefit & WB & none & 40.420 \\
ASIASH & China+Vietnam share of destination HS imports & competition & cost & BACI & none & 100.000 \\
HHI & Supplier concentration (HHI) in destination HS imports & competition & cost & BACI & none & 100.000 \\
UVGAP & Absolute log unit-value gap (destination imports vs origin exports) & product\_fit & cost & BACI & none & 100.000 \\
CULT & Cultural distance (Kogut-Singh, Hofstede 6 dimensions) & product\_fit & cost & Hofstede & none & 90.480 \\
LANG & Common official language & product\_fit & benefit & CEPII Gravity & none & 81.940 \\
INFL & Inflation deviation from 2 percent & macro\_risk & cost & WB & none & 40.500 \\
UNEMP & Unemployment rate & macro\_risk & cost & WB & none & 24.440 \\
GOV & Mean Worldwide Governance Indicators & institutional & benefit & WB WGI & none & 98.330 \\
EOC & External Opening Coefficient (trade/GDP) & openness\_legacy & benefit & WB & none & 98.190 \\
REEXP & Re-export intensity (chapter X\_j / M\_j) & openness\_legacy & cost & BACI & none & 100.000 \\
\bottomrule
\end{tabular}
\end{table}
```
