# Data download coverage

Years in settings: 2012–2023
HS chapters: 09, 42, 61, 62, 64
Origins: COL, PER, MEX, CHL, ECU, BRA, ARG

## Run status

- **worldbank_wdi**: ok
- **worldbank_wgi**: ok
- **baci**: skipped (idempotent)
- **cepii_gravity**: skipped (idempotent)
- **wits**: skipped (idempotent)
- **hofstede**: skipped (idempotent)

## World Bank

- **WDI**: countries=261, years=2012–2023 (n_years=12), indicators=7, missing_year_share=0.000, rows=14599
  - indicators: FP.CPI.TOTL.ZG, LP.LPI.OVRL.XQ, NE.TRD.GNFS.ZS, NY.GDP.MKTP.CD, NY.GDP.PCAP.PP.KD, SL.UEM.TOTL.ZS, SP.POP.TOTL
- **WGI**: countries=207, years=2012–2023 (n_years=12), indicators=6, missing_year_share=0.000, rows=14768
  - indicators: CC.EST, GE.EST, PV.EST, RL.EST, RQ.EST, VA.EST

## BACI

- **BACI trade**: partitions=12, years=2012–2023, exporters=227, importers=227, rows=13204559, missing_year_share=0.000
- **baci/country_codes.parquet**: rows=238
- **baci/product_codes.parquet**: rows=5202

## CEPII Gravity

- **Gravity**: rows=635040, iso3_o=243, iso3_d=243, years=2012–2021, missing_year_share=0.167
  - distw_harmonic: missing_share=0.130
  - contig: missing_share=0.130
  - comlang_off: missing_share=0.203
  - fta_wto: missing_share=0.130

## WITS

- **WITS (TRN API)**: rows=25200, reporters=60, partners=7, years=2012–2023, missing_year_share=0.000
  - hs_chapter values: ['09', '42', '61', '62', '64']
  - missing_chapter_share_vs_settings=0.000
  - LOCF: enabled in settings=True; flagged_cells=2291; share_of_nonnull=0.094
  - LOCF fills carry the last observed AHS forward within (reporter, partner, chapter); flagged in column `tarif_locf`.
  - tarif_source counts: mfn_no_preference=14865, partner_specific=7149, partner_locf=2291, missing=895
  - still-missing AHS cells after MFN fallback: 895
  - cached TRN XML files: 4060

## Hofstede

- **Hofstede**: countries=104, rows=104
  - pdi: missing_share=0.308
  - idv: missing_share=0.308
  - mas: missing_share=0.308
  - uai: missing_share=0.308
  - ltowvs: missing_share=0.087
  - ivr: missing_share=0.077

