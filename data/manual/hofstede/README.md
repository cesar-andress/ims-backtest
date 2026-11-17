# Manual Hofstede 6-dimension scores

There is no automated download. Obtain the official 6-dimension country scores
from Geert Hofstede’s dataset (commonly distributed as a CSV from
https://geerthofstede.com/research-and-vsm/dimension-data-matrix/ ).

Place a CSV in this folder with columns:

```text
iso3,pdi,idv,mas,uai,ltowvs,ivr
```

`ctr` is accepted as an alias for `iso3`. Missing dimension values must remain
blank (NaN) — never impute.
