# T2. Expert weights (mean, SD, CV) and Kendall W

Legacy expert panel (n=15); Kendall W on factor ratings = 0.2190. IMSFE 2.0 factors inherit mapped legacy means; unmapped factors share residual mass. Unmapped criteria (expert_mapping.yaml): GDPPC, GRW, IMPC, IMPV, REEXP, UVGAP.

| level    | id   | parent   |   mean |     sd |     cv |   min |   max |
|:---------|:-----|:---------|-------:|-------:|-------:|------:|------:|
| factor   | COST |          | 0.2147 | 0.0549 | 0.2557 |  0.15 |  0.3  |
| factor   | LOGI |          | 0.1847 | 0.053  | 0.2872 |  0.1  |  0.25 |
| factor   | COMM |          | 0.1933 | 0.0753 | 0.3894 |  0.1  |  0.35 |
| factor   | ECON |          | 0.1533 | 0.0611 | 0.3987 |  0.05 |  0.3  |
| factor   | POLI |          | 0.1307 | 0.0518 | 0.396  |  0.05 |  0.2  |
| factor   | CULT |          | 0.1233 | 0.0563 | 0.4563 |  0.05 |  0.2  |
| variable | PPAD | COST     | 0.43   | 0.0775 | 0.1801 |  0.3  |  0.6  |
| variable | INTC | COST     | 0.35   | 0.0802 | 0.2291 |  0.25 |  0.5  |
| variable | CIBC | COST     | 0.22   | 0.0455 | 0.2069 |  0.15 |  0.3  |
| variable | LPIN | LOGI     | 0.4    | 0.1439 | 0.3598 |  0.2  |  0.7  |
| variable | CPTR | LOGI     | 0.2633 | 0.0743 | 0.2822 |  0.15 |  0.4  |
| variable | ITTT | LOGI     | 0.3367 | 0.1356 | 0.4027 |  0.15 |  0.6  |
| variable | CUTA | COMM     | 0.49   | 0.1466 | 0.2992 |  0.3  |  0.85 |
| variable | CCTI | COMM     | 0.2533 | 0.0935 | 0.369  |  0.05 |  0.4  |
| variable | IOEF | COMM     | 0.2567 | 0.1067 | 0.4156 |  0.1  |  0.4  |
| variable | CLI  | ECON     | 0.34   | 0.0849 | 0.2498 |  0.2  |  0.5  |
| variable | INAN | ECON     | 0.3467 | 0.1232 | 0.3552 |  0.2  |  0.7  |
| variable | UNRA | ECON     | 0.3133 | 0.0954 | 0.3044 |  0.1  |  0.5  |
| variable | FSIN | POLI     | 0.3433 | 0.0678 | 0.1974 |  0.2  |  0.4  |
| variable | INRI | POLI     | 0.3733 | 0.0942 | 0.2524 |  0.3  |  0.6  |
| variable | DEIN | POLI     | 0.2833 | 0.0673 | 0.2374 |  0.2  |  0.4  |
| variable | GLIN | CULT     | 0.2933 | 0.0704 | 0.2399 |  0.2  |  0.4  |
| variable | CPIN | CULT     | 0.32   | 0.1162 | 0.3631 |  0.1  |  0.5  |
| variable | CUDI | CULT     | 0.3867 | 0.1395 | 0.3607 |  0.2  |  0.7  |

## Booktabs (copy into manuscript; not a repo .tex file)

```latex
\begin{table}[htbp]
\centering
\caption{T2. Expert weights (mean, SD, CV) and Kendall W}
\label{tab:T2_expert_weights}
\begin{tabular}{llllllll}
\toprule
level & id & parent & mean & sd & cv & min & max \\
\midrule
factor & COST &  & 0.2147 & 0.0549 & 0.2557 & 0.1500 & 0.3000 \\
factor & LOGI &  & 0.1847 & 0.0530 & 0.2872 & 0.1000 & 0.2500 \\
factor & COMM &  & 0.1933 & 0.0753 & 0.3894 & 0.1000 & 0.3500 \\
factor & ECON &  & 0.1533 & 0.0611 & 0.3987 & 0.0500 & 0.3000 \\
factor & POLI &  & 0.1307 & 0.0518 & 0.3960 & 0.0500 & 0.2000 \\
factor & CULT &  & 0.1233 & 0.0563 & 0.4563 & 0.0500 & 0.2000 \\
variable & PPAD & COST & 0.4300 & 0.0775 & 0.1801 & 0.3000 & 0.6000 \\
variable & INTC & COST & 0.3500 & 0.0802 & 0.2291 & 0.2500 & 0.5000 \\
variable & CIBC & COST & 0.2200 & 0.0455 & 0.2069 & 0.1500 & 0.3000 \\
variable & LPIN & LOGI & 0.4000 & 0.1439 & 0.3598 & 0.2000 & 0.7000 \\
variable & CPTR & LOGI & 0.2633 & 0.0743 & 0.2822 & 0.1500 & 0.4000 \\
variable & ITTT & LOGI & 0.3367 & 0.1356 & 0.4027 & 0.1500 & 0.6000 \\
variable & CUTA & COMM & 0.4900 & 0.1466 & 0.2992 & 0.3000 & 0.8500 \\
variable & CCTI & COMM & 0.2533 & 0.0935 & 0.3690 & 0.0500 & 0.4000 \\
variable & IOEF & COMM & 0.2567 & 0.1067 & 0.4156 & 0.1000 & 0.4000 \\
variable & CLI & ECON & 0.3400 & 0.0849 & 0.2498 & 0.2000 & 0.5000 \\
variable & INAN & ECON & 0.3467 & 0.1232 & 0.3552 & 0.2000 & 0.7000 \\
variable & UNRA & ECON & 0.3133 & 0.0954 & 0.3044 & 0.1000 & 0.5000 \\
variable & FSIN & POLI & 0.3433 & 0.0678 & 0.1974 & 0.2000 & 0.4000 \\
variable & INRI & POLI & 0.3733 & 0.0942 & 0.2524 & 0.3000 & 0.6000 \\
variable & DEIN & POLI & 0.2833 & 0.0673 & 0.2374 & 0.2000 & 0.4000 \\
variable & GLIN & CULT & 0.2933 & 0.0704 & 0.2399 & 0.2000 & 0.4000 \\
variable & CPIN & CULT & 0.3200 & 0.1162 & 0.3631 & 0.1000 & 0.5000 \\
variable & CUDI & CULT & 0.3867 & 0.1395 & 0.3607 & 0.2000 & 0.7000 \\
\bottomrule
\end{tabular}
\end{table}
```
