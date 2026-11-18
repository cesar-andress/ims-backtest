"""Construct intensive, extensive, and level export outcomes for backtesting."""

from __future__ import annotations

import numpy as np
import pandas as pd

from imsfe.config import Settings, load_settings


def add_outcomes(
    panel: pd.DataFrame,
    settings: Settings | None = None,
    *,
    threshold: float | None = None,
    horizons: list[int] | None = None,
) -> pd.DataFrame:
    """Add y_int, y_ext, y_level for each horizon k (SPEC §3.3).

    Definitions (BACI flow i→j of the chapter):
    - y_int_k = log(X_{t+k}+1) − log(X_t+1) if X_t > threshold, else NaN
    - y_ext_k = 1 if X_t ≤ threshold and X_{t+k} > threshold, else 0
      (NaN when t+k is outside the sample)
    - y_level_k = X_{t+k}
    """
    settings = settings or load_settings()
    thr = float(settings.entry_threshold_usd if threshold is None else threshold)
    ks = list(settings.horizons if horizons is None else horizons)
    out = panel.copy()

    # Look up future bilateral flows from the same panel keys.
    lookup = out.set_index(["iso3_o", "iso3_d", "year"])["X_ijt"]

    for k in ks:
        y_int = []
        y_ext = []
        y_level = []
        for o, d, t, x_t in zip(
            out["iso3_o"], out["iso3_d"], out["year"], out["X_ijt"], strict=False
        ):
            key_fut = (o, d, int(t) + int(k))
            if key_fut not in lookup.index:
                y_int.append(np.nan)
                y_ext.append(np.nan)
                y_level.append(np.nan)
                continue
            x_fut = lookup.loc[key_fut]
            if isinstance(x_fut, pd.Series):
                x_fut = float(x_fut.iloc[0])
            else:
                x_fut = float(x_fut)
            x0 = float(x_t) if pd.notna(x_t) else 0.0
            y_level.append(x_fut)
            if x0 > thr:
                y_int.append(np.log(x_fut + 1.0) - np.log(x0 + 1.0))
            else:
                y_int.append(np.nan)
            y_ext.append(1.0 if (x0 <= thr and x_fut > thr) else 0.0)
        out[f"y_int_k{k}"] = y_int
        out[f"y_ext_k{k}"] = y_ext
        out[f"y_level_k{k}"] = y_level

    out.attrs["entry_threshold_usd"] = thr
    out.attrs["horizons"] = ks
    return out
