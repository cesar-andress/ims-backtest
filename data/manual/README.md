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

### Filling `legacy_preferential_tariffs.csv` (human task)

1. Open [WITS](https://wits.worldbank.org/) → TRAINS / tariff download.
2. Reporter = each destination ISO3; Partner = Colombia (`COL`);
   Product = HS 64 (or 6-digit headings under 64, then simple average);
   Tariff type = **AHS (effectively applied)**, not MFN.
3. Enter the percentage in `tariff_pct` and cite the WITS extract in `source`
   (URL or local filename + download date). Leave no blanks.
4. `imsfe legacy` will refuse the preferential-tariff ranking until every
   `tariff_pct` for the 30 ISO3 codes is filled. Do **not** invent values.

Each drop must be documented (source URL, download date, version) when added.
