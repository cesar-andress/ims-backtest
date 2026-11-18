# Reproducibility check

Date (UTC): 2026-11-18T01:36:56.985302+00:00
Procedure: remove `.venv`, `uv sync --group dev`, `make all`, compare `outputs/logs/build.json` to pre-run committed snapshot.

## Summary

- Pre-run committed manifest files: 63
- Post-`make all` manifest files: 65
- Identical SHA-256: **37**
- Changed SHA-256: **26**
- Added paths: 2 (outputs/logs/refs_check.json, outputs/logs/refs_check.md)

## Numeric stability (key tables vs git HEAD)

- `A1_extra_robustness.csv`, `case_recommended_vs_actual.csv`, `T2_kendall_w.csv`, `T9_legacy_comparison.csv`: **identical**
- `T4_predictive_metrics.csv`: **differs only for `wsm|minmax|learned`** (max |Δmean| ≈ 0.033 on spearman); expert/baseline/ml rows unchanged at compared precision
- `T8_smaa_col.csv`: ranks/scores stable; `p_top1` / rank quantiles show small Monte-Carlo / float drift (max |Δp_top1| ≈ 0.006)
- Learned factor/variable weights (`T4_learned_vs_expert_weights.csv`) **not bit-stable** across fresh-venv `make all` (e.g. LPI weight moved substantially)

## Coverage

- `pytest --cov=imsfe`: **81 passed**, total line coverage **≈ 57%**
- Low coverage hotspots: `cli.py` (0%), `validation/run.py`, `validation/learned.py`, `validation/gravity.py`, `report/tables.py`

## Manuscript number sourcing (`../manuscript/manuscript.qmd`)

- Result claims for NDCG/CIs/Kendall W / n_vars use `{python}` inlines from `paper/outputs/` (via `_imsfe_data.py`).
- Non-sourced numeric tokens in prose/YAML (not result tables):
  - Metric/label text: `NDCG@10`, scale mentions, `IMSFE 2.0`, heading `HS 64`
  - `[CITE: … 1985/1988/2007/2011]` placeholder years (not empirical results; not in `refs.bib` yet)
  - ORCID identifiers in author YAML (identity metadata, not from `outputs/`)
- No hardcoded T4/T8/case export values found in manuscript prose.

## Changed files (SHA-256)

- `outputs/figures/F1_framework.pdf`: `1e4d07922fbcee63…` → `366b293fdd71adc5…`
- `outputs/figures/F2_smaa_rank_acceptability.pdf`: `5ae26ac91700fc69…` → `38fd2a03376f9c5b…`
- `outputs/figures/F2_smaa_rank_acceptability.png`: `0fefdad589db7e4c…` → `a3a4c519bc2d7359…`
- `outputs/figures/F3_attractiveness_fit_matrix.pdf`: `34340eb6824be60f…` → `23e6073e4ccf94b3…`
- `outputs/figures/F3_attractiveness_fit_matrix.png`: `4fd08c4cd896fc76…` → `adb1c1d7465659ae…`
- `outputs/figures/F3_attractiveness_fit_matrix_fixed5.pdf`: `f688689b5fa9cde0…` → `0c6231cf635f1788…`
- `outputs/figures/F4_ndcg_by_year.pdf`: `1706ade2116caad4…` → `80d2643d06678921…`
- `outputs/figures/F4_ndcg_by_year.png`: `4c4d7b656ca95b03…` → `9407162a26fe3d52…`
- `outputs/figures/F5_shap_vs_weights.pdf`: `26ccaab93fc0a4b5…` → `49becafcb0dd49b9…`
- `outputs/figures/F5_shap_vs_weights.png`: `86556870f4a2a5b0…` → `e639c55400b3c31c…`
- `outputs/logs/coverage.md`: `7cb6ae618e682e62…` → `c40eef75509422fe…`
- `outputs/tables/T2_expert_weights_mapped.csv`: `6898d57991051c5b…` → `689ba08fae0d6d84…`
- `outputs/tables/T2_expert_weights_mapped.md`: `6370bdfd3c9e5b28…` → `288fa3a148a83ef4…`
- `outputs/tables/T4_learned_vs_expert_weights.csv`: `cedbbea97e8a7815…` → `5e795e5793b9cc9d…`
- `outputs/tables/T4_learned_vs_expert_weights.md`: `824ddeac32d6b34b…` → `b1fd7e1a7a362bd8…`
- `outputs/tables/T4_predictive_metrics.csv`: `902dc4b5cf2a68a4…` → `0b1effebd3990d71…`
- `outputs/tables/T4_predictive_metrics.md`: `763508277bce2806…` → `d84ec0e18cb71d27…`
- `outputs/tables/T4_shap_factor_importance.csv`: `72bbf02ae3507f55…` → `6e3158039c8d1955…`
- `outputs/tables/T4_shap_factor_importance.md`: `4692a3726d230435…` → `a34c9559fba2a5ea…`
- `outputs/tables/T5_ppml.csv`: `18b47cf329092714…` → `467535c580a2e6fb…`
- `outputs/tables/T8_smaa_col.csv`: `cd2d1252c47653ea…` → `82c704c276ae4684…`
- `outputs/tables/T8_smaa_col.md`: `e420dacaa12f6a91…` → `6d3aba3f8f207ff8…`
- `outputs/tables/case_matrix_scores.csv`: `3c7b62501c74a0e9…` → `a23d78ef7b3281e7…`
- `outputs/tables/case_recommended_vs_actual.csv`: `0768bf13fc4582cf…` → `e1dce9a551eefe39…`
- `outputs/tables/ml_runtime_log.json`: `d138331eafb4179d…` → `17d5982a227d8d22…`
- `outputs/tables/validation_summary.txt`: `2f61f511ffddf6cb…` → `9d15c933e73db89b…`
