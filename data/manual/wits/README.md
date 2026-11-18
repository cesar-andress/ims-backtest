# WITS / TRAINS tariffs

**Primary path (Phase 12+):** `imsfe download` calls the WITS TRN SDMX API

```text
https://wits.worldbank.org/API/V1/SDMX/V21/datasource/TRN/reporter/{rep}/partner/{origin}/product/all/year/{y}/datatype/{reported|aveestimated}
```

Reporters are the top-N destinations (EU members → reporter `918`); partners are
the configured origins. HS6 lines in configured chapters are aggregated to a
simple-average AHS. Raw XML is cached under `data/raw/wits/`. Missing years can
be filled by LOCF with column `tarif_locf` (see `outputs/logs/coverage.md`).

Manual CSVs in this folder are optional legacy inputs / cross-checks only.

## Optional CSV schema (legacy)

```text
reporter_iso3,partner_iso3,year,hs_chapter,ahs_simple_avg
```
