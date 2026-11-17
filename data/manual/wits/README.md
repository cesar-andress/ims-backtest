# Manual WITS / TRAINS tariff exports

The public WITS SDMX TradeStats key space does not expose a reliable single
product code for an entire HS chapter. For SPEC variables (AHS, origin→destination,
HS chapters in settings), export from the WITS website and place CSVs here.

## Recommended export settings (WITS Advanced Query / Tariff View)

1. **Database:** UNCTAD TRAINS via WITS.
2. **Duty type:** AHS (effectively applied), **simple average**.
3. **Reporter:** destination country (ISO3).
4. **Partner:** each origin in `config/settings.yaml` (COL, PER, MEX, …).
5. **Product:** HS chapter(s) `09`, `42`, `61`, `62`, `64` (or all 6-digit lines
   under those chapters, then average yourself to chapter level).
6. **Years:** cover `settings.years` (2012–2023).

## Required CSV columns

```text
reporter_iso3,partner_iso3,year,hs_chapter,ahs_simple_avg
```

Example:

```csv
reporter_iso3,partner_iso3,year,hs_chapter,ahs_simple_avg
USA,COL,2020,64,0.0
DEU,COL,2020,64,0.0
```

Multiple CSV files are concatenated. Do not invent tariff values.
