# Manual data drops

Place files that cannot be fetched automatically here. Do not invent values.

Expected subfolders (created in later phases):

- `hofstede/` — Hofstede six-dimension country scores (CSV)
- `wits/` — WITS/TRAINS applied-tariff CSV exports (document export settings)
- `baci/` — BACI zip if the CEPII download URL is unavailable
- `cepii_gravity/` — Gravity database dump if the download URL is unavailable
- `legacy_preferential_tariffs.csv` — Colombia→destination applied tariffs (AHS)
  for HS chapter 64, used only in the legacy robustness method
  `minmax_pref_tariff`. Columns: `iso3`, `tariff_pct`, `source`.

### `legacy_preferential_tariffs.csv` — FILLED (2026-11-17)

Filled from the WITS-TRAINS SDMX API (no manual values). Value = simple average
of the HS6 subheadings of chapter 64 (each HS6 is itself WITS's simple average
of national lines). Extra columns: `tariff_type` (PREF = preferential rate for
partner COL 170; MFN = no agreement, partner 000; MFN_AVE = ad-valorem
equivalents because of specific duties; PREF_PARTIAL = preference on only part
of the lines), `year`, `wits_reporter` (EU members use reporter 918),
`partner`, `datatype`, `n_hs6`, `notes`, plus the exact API URL in `source`.

- HS6-level detail: `wits/legacy_hs64_hs6_detail.csv`.
- Scripts used: `wits/fetch.py`, `wits/fetch_mfn.py`, `wits/parse.py`,
  `wits/build_csv.py` (reference only; Phase 2 implements `download/wits.py`).
- Rows flagged `MANUAL CHECK` in `notes`: **MEX** (2018 data, partial
  preference vs 0.0 in the 2017 AVE file) and **PAN** (MFN used; an older
  partial preference existed in 2013).
- Caveats: years differ by reporter (latest available in WITS: 2021 for
  preferential data, 2023 for most MFN). 21 of 30 values are 0, so the legacy
  ratio formula (`min/y`) is undefined here: use it only with min-max/rank.

### Filling `legacy_preferential_tariffs.csv` (original instructions, kept for reference)

1. Open [WITS](https://wits.worldbank.org/) → TRAINS / tariff download.
2. Reporter = each destination ISO3; Partner = Colombia (`COL`);
   Product = HS 64 (or 6-digit headings under 64, then simple average);
   Tariff type = **AHS (effectively applied)**, not MFN.
3. Enter the percentage in `tariff_pct` and cite the WITS extract in `source`
   (URL or local filename + download date). Leave no blanks.
4. `imsfe legacy` will refuse the preferential-tariff ranking until every
   `tariff_pct` for the 30 ISO3 codes is filled. Do **not** invent values.

Each drop must be documented (source URL, download date, version) when added.
