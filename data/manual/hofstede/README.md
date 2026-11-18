# Manual Hofstede 6-dimension scores

Hofstede data cannot be redistributed in this repository: the files here are
gitignored, only this README is versioned. To reproduce, download the source file
yourself and run the conversion described below.

## Current local drop (2026-11-18)

- **Source:** https://geerthofstede.com/research-and-vsm/dimension-data-matrix/
  file `6-dimensions-for-website-2015-08-16.csv` ("the data as used in our books",
  *Cultures and Organizations* 3rd ed., 2010). The page states researchers may use
  them without asking for permission; commercial use requires contacting the authors.
  Kept unmodified in `source/` (SHA-256
  `71bff58cf610ec44b870d5aa4b06bb36e3a573860d513ff802488764d6e029a6`).
- **Not used:** the `0-100` variant, which caps outliers (e.g. UAI Greece 112→100).
- **Loaded file:** `hofstede_6d_iso3.csv`, columns
  `iso3,country,hofstede_ctr,pdi,idv,mas,uai,ltowvs,ivr`.

## Why a converted file: `ctr` is NOT ISO3

Hofstede's `ctr` codes look like ISO3 but are not, and some collide with real ISO3
codes of other countries. Treating `ctr` as `iso3` silently mismatches countries:

| ctr | Hofstede country | ISO3 | collision if used as ISO3 |
|-----|------------------|------|---------------------------|
| SLV | Slovenia | SVN | El Salvador |
| MNG | Montenegro | MNE | Mongolia |
| BEN | Belgium Netherl (sub-group) | dropped | Benin |
| GER, NET, SIN, SWI, DEN, CHI, … | Germany, Netherlands, Singapore, Switzerland, Denmark, China | DEU, NLD, SGP, CHE, DNK, CHN | no match at all |

The conversion uses an explicit 101-entry map (no fuzzy matching) and drops the
10 regional or sub-national rows: AFE, AFW, ARA (Arab countries), BEF, BEN, CAF,
GEE, SAW, SWF, SWG. `#NULL!` becomes blank (NaN). Nothing is imputed.

## Coverage of the panel (61 destinations, 7 origins)

- 4 classic dimensions (PDI, IDV, MAS, UAI): 50 of 61 destinations.
- Missing all 4: ARE, DZA, IRQ, KAZ, KGZ, KWT, QAT, SAU, UKR, ZAF (ZAF only has
  LTO and IVR) and S19 (BACI code for Taiwan; Hofstede has TWN, so a
  S19→TWN alias in the panel would recover it).
- 6 dimensions: 49 of 61 (ISR lacks LTO/IVR). Origin ECU lacks LTO/IVR.
- Recommendation: Kogut-Singh on the 4 classic dimensions (the original
  definition), and keep CULT missing (flagged) for the uncovered destinations.
  Using the regional "Arab countries" score for ARE/SAU/KWT/QAT/IRQ would be a
  proxy choice: only if made explicit in config and reported.

## Loader contract

`src/imsfe/download/hofstede.py` reads the first `*.csv` in this folder (not
`source/`) and needs `iso3,pdi,idv,mas,uai,ltowvs,ivr`. The loader's `ctr`
alias must not be used with the raw Hofstede file (see table above).
