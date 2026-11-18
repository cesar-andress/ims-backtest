"""Compute IMS feature variables for each origin-destination-year."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from imsfe.config import Settings, VariableConfig, VariablesConfig, load_settings, load_variables
from imsfe.io import raw_dir

ASIA_SUPPLIERS = ("CHN", "VNM")
WGI_IDS = ["VA.EST", "PV.EST", "GE.EST", "RQ.EST", "RL.EST", "CC.EST"]
HOFSTEDE_DIMS = ["pdi", "idv", "mas", "uai", "ltowvs", "ivr"]


def _wdi_pivot(path: Path | None = None) -> pd.DataFrame:
    p = path or (raw_dir() / "worldbank" / "wdi_indicators.parquet")
    if not p.is_file():
        return pd.DataFrame(columns=["iso3", "year"])
    long = pd.read_parquet(p)
    wide = long.pivot_table(
        index=["iso3", "year"], columns="indicator", values="value", aggfunc="first"
    ).reset_index()
    wide.columns.name = None
    return wide


def _wgi_mean(path: Path | None = None) -> pd.DataFrame:
    p = path or (raw_dir() / "worldbank" / "wgi_indicators.parquet")
    if not p.is_file():
        return pd.DataFrame(columns=["iso3", "year", "GOV_raw"])
    long = pd.read_parquet(p)
    sub = long.loc[long["indicator"].isin(WGI_IDS)]
    if sub.empty:
        return pd.DataFrame(columns=["iso3", "year", "GOV_raw"])
    wide = sub.pivot_table(
        index=["iso3", "year"], columns="indicator", values="value", aggfunc="first"
    )
    out = wide.mean(axis=1, skipna=True).rename("GOV_raw").reset_index()
    return out


def _load_gravity(path: Path | None = None) -> pd.DataFrame:
    p = path or (raw_dir() / "cepii_gravity" / "gravity.parquet")
    if not p.is_file():
        return pd.DataFrame(
            columns=[
                "iso3_o",
                "iso3_d",
                "year",
                "distw_harmonic",
                "comlang_off",
                "fta_wto",
            ]
        )
    return pd.read_parquet(p)


def _load_hofstede(path: Path | None = None) -> pd.DataFrame:
    """Load Hofstede raw parquet or manual CSV; empty frame if absent."""
    raw_p = path or (raw_dir() / "hofstede" / "hofstede.parquet")
    if raw_p.is_file():
        return pd.read_parquet(raw_p)
    manual = raw_dir().parent / "manual" / "hofstede"
    csvs = sorted(manual.glob("*.csv")) if manual.is_dir() else []
    if not csvs:
        return pd.DataFrame(columns=["iso3", *HOFSTEDE_DIMS])
    from imsfe.download.hofstede import load_hofstede_csv

    return load_hofstede_csv(csvs[0])


def _load_wits(path: Path | None = None) -> pd.DataFrame:
    p = path or (raw_dir() / "wits" / "ahs_tariffs.parquet")
    if not p.is_file():
        return pd.DataFrame(
            columns=["reporter_iso3", "partner_iso3", "year", "hs_chapter", "ahs_simple_avg"]
        )
    return pd.read_parquet(p)


def interpolate_lpi(series_by_year: pd.Series) -> tuple[pd.Series, pd.Series]:
    """Linear interpolation between observed LPI editions only (no extrapolation).

    Returns (values, imputed_flag) aligned to the input index (years).
    """
    s = series_by_year.sort_index()
    observed = s.notna()
    interp = s.interpolate(method="linear", limit_area="inside")
    imputed = interp.notna() & ~observed
    return interp, imputed.astype(bool)


def destination_market_stats(flows: pd.DataFrame) -> pd.DataFrame:
    """Per destination-year aggregates from chapter flows (anti-leakage: year-native)."""
    # Imports of j
    imports = (
        flows.groupby(["iso3_d", "year"], as_index=False)
        .agg(
            import_value=("value_usd", "sum"),
            import_qty=("qty_tons", "sum"),
        )
        .rename(columns={"iso3_d": "iso3"})
    )
    # Exports of j (as exporter)
    exports = (
        flows.groupby(["iso3_o", "year"], as_index=False)
        .agg(export_value=("value_usd", "sum"))
        .rename(columns={"iso3_o": "iso3"})
    )
    mkt = imports.merge(exports, on=["iso3", "year"], how="left")
    mkt["export_value"] = mkt["export_value"].fillna(0.0)

    # Asia share + HHI of suppliers
    rows: list[dict] = []
    for (dest, year), grp in flows.groupby(["iso3_d", "year"]):
        total = float(grp["value_usd"].sum())
        if total <= 0:
            rows.append(
                {
                    "iso3": dest,
                    "year": int(year),
                    "ASIASH_raw": float("nan"),
                    "HHI_raw": float("nan"),
                }
            )
            continue
        by_exp = grp.groupby("iso3_o")["value_usd"].sum()
        asia = float(by_exp.reindex(list(ASIA_SUPPLIERS)).fillna(0.0).sum())
        shares = (by_exp / total).to_numpy(dtype=float)
        rows.append(
            {
                "iso3": dest,
                "year": int(year),
                "ASIASH_raw": asia / total,
                "HHI_raw": float(np.sum(shares**2)),
            }
        )
    comp = pd.DataFrame.from_records(rows)
    mkt = mkt.merge(comp, on=["iso3", "year"], how="left")
    mkt["REEXP_raw"] = np.where(
        mkt["import_value"] > 0,
        mkt["export_value"] / mkt["import_value"],
        np.nan,
    )
    mkt["uv_import"] = np.where(
        mkt["import_qty"] > 0,
        mkt["import_value"] / mkt["import_qty"],
        np.nan,
    )
    return mkt


def origin_world_export_uv(flows: pd.DataFrame) -> pd.DataFrame:
    """Unit value of origin i's world exports of the chapter by year."""
    agg = (
        flows.groupby(["iso3_o", "year"], as_index=False)
        .agg(export_value=("value_usd", "sum"), export_qty=("qty_tons", "sum"))
        .rename(columns={"iso3_o": "iso3"})
    )
    agg["uv_export"] = np.where(
        agg["export_qty"] > 0,
        agg["export_value"] / agg["export_qty"],
        np.nan,
    )
    return agg[["iso3", "year", "uv_export"]]


def cagr_3y(values: pd.Series) -> pd.Series:
    """3-year CAGR at each year t using only V_t and V_{t-3}."""
    out = pd.Series(np.nan, index=values.index, dtype=float)
    for t in values.index:
        v_t = values.get(t)
        v_lag = values.get(t - 3)
        if v_t is None or v_lag is None:
            continue
        if pd.isna(v_t) or pd.isna(v_lag) or v_lag <= 0 or v_t <= 0:
            continue
        out.loc[t] = (float(v_t) / float(v_lag)) ** (1.0 / 3.0) - 1.0
    return out


def kogut_singh(origin_row: pd.Series, dest_row: pd.Series, variances: pd.Series) -> float:
    """Kogut-Singh cultural distance (6 Hofstede dimensions, variance-scaled)."""
    diffs = []
    for dim in HOFSTEDE_DIMS:
        a = origin_row.get(dim)
        b = dest_row.get(dim)
        var = variances.get(dim)
        if pd.isna(a) or pd.isna(b) or pd.isna(var) or var <= 0:
            continue
        diffs.append(((float(a) - float(b)) ** 2) / float(var))
    if not diffs:
        return float("nan")
    return float(np.mean(diffs))


def apply_transform(raw: pd.Series, transform: str) -> pd.Series:
    values = pd.to_numeric(raw, errors="coerce")
    if transform == "none":
        return values.astype(float)
    out = pd.Series(np.nan, index=values.index, dtype=float)
    if transform == "log":
        mask = values > 0
        out.loc[mask] = np.log(values.loc[mask].to_numpy(dtype=float))
        return out
    if transform == "log1p":
        mask = values >= 0
        out.loc[mask] = np.log1p(values.loc[mask].to_numpy(dtype=float))
        return out
    raise ValueError(f"Unknown transform: {transform}")


def compute_features(
    panel: pd.DataFrame,
    flows: pd.DataFrame,
    settings: Settings | None = None,
    variables: VariablesConfig | None = None,
    *,
    wdi: pd.DataFrame | None = None,
    wgi: pd.DataFrame | None = None,
    gravity: pd.DataFrame | None = None,
    hofstede: pd.DataFrame | None = None,
    wits: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Attach raw and transformed feature columns to the panel.

    A feature at year t uses only information with year <= t (GRW uses t-3..t;
    LPI interpolates only between editions already observed by t).
    """
    settings = settings or load_settings()
    variables = variables or load_variables()
    out = panel.copy()

    mkt = destination_market_stats(flows)
    uv_o = origin_world_export_uv(flows)
    wdi_df = wdi if wdi is not None else _wdi_pivot()
    wgi_df = wgi if wgi is not None else _wgi_mean()
    grav = gravity if gravity is not None else _load_gravity()
    hof = hofstede if hofstede is not None else _load_hofstede()
    wits_df = wits if wits is not None else _load_wits()

    # --- destination-year demand / market ---
    dest = mkt.rename(
        columns={
            "iso3": "iso3_d",
            "import_value": "IMPV_raw",
            "uv_import": "uv_import",
        }
    )
    out = out.merge(
        dest[
            [
                "iso3_d",
                "year",
                "IMPV_raw",
                "ASIASH_raw",
                "HHI_raw",
                "REEXP_raw",
                "uv_import",
            ]
        ],
        on=["iso3_d", "year"],
        how="left",
    )

    # GRW from destination IMPV series (per destination, years <= t only via lag)
    grw_frames = []
    for dest_iso, g in mkt.groupby("iso3"):
        s = g.set_index("year")["import_value"].sort_index()
        grw = cagr_3y(s)
        grw_frames.append(
            pd.DataFrame({"iso3_d": dest_iso, "year": grw.index, "GRW_raw": grw.values})
        )
    if grw_frames:
        out = out.merge(pd.concat(grw_frames, ignore_index=True), on=["iso3_d", "year"], how="left")
    else:
        out["GRW_raw"] = np.nan

    # Population + macros from WDI (destination, same year)
    pop_col = "SP.POP.TOTL"
    if pop_col in wdi_df.columns:
        pop = wdi_df[["iso3", "year", pop_col]].rename(
            columns={"iso3": "iso3_d", pop_col: "pop"}
        )
        out = out.merge(pop, on=["iso3_d", "year"], how="left")
        out["IMPC_raw"] = np.where(out["pop"] > 0, out["IMPV_raw"] / out["pop"], np.nan)
    else:
        out["IMPC_raw"] = np.nan

    def _merge_wdi(indicator: str, col: str) -> None:
        nonlocal out
        if indicator not in wdi_df.columns:
            out[col] = np.nan
            return
        tmp = wdi_df[["iso3", "year", indicator]].rename(
            columns={"iso3": "iso3_d", indicator: col}
        )
        out = out.merge(tmp, on=["iso3_d", "year"], how="left")

    _merge_wdi("NY.GDP.PCAP.PP.KD", "GDPPC_raw")
    _merge_wdi("FP.CPI.TOTL.ZG", "cpi")
    out["INFL_raw"] = (out["cpi"] - 2.0).abs() if "cpi" in out.columns else np.nan
    _merge_wdi("SL.UEM.TOTL.ZS", "UNEMP_raw")
    _merge_wdi("NE.TRD.GNFS.ZS", "EOC_raw")

    # LPI with interpolation between editions, causal at t (only editions with year <= t)
    out["LPI_raw"] = np.nan
    out["lpi_imputed"] = False
    if "LP.LPI.OVRL.XQ" in wdi_df.columns:
        lpi_long = wdi_df[["iso3", "year", "LP.LPI.OVRL.XQ"]].dropna()
        years = list(range(settings.years.start, settings.years.end + 1))
        records = []
        for iso, g in lpi_long.groupby("iso3"):
            observed = g.set_index("year")["LP.LPI.OVRL.XQ"].sort_index()
            for t in years:
                # Causal: only editions with year <= t
                hist = observed.loc[observed.index <= t]
                if hist.empty:
                    records.append(
                        {"iso3_d": iso, "year": t, "LPI_raw": np.nan, "lpi_imputed": False}
                    )
                    continue
                full_idx = pd.Index(range(int(hist.index.min()), t + 1))
                series = hist.reindex(full_idx)
                interp, imputed = interpolate_lpi(series)
                records.append(
                    {
                        "iso3_d": iso,
                        "year": t,
                        "LPI_raw": (
                            float(interp.loc[t]) if pd.notna(interp.loc[t]) else np.nan
                        ),
                        "lpi_imputed": bool(imputed.loc[t]) if t in imputed.index else False,
                    }
                )
        lpi_panel = pd.DataFrame.from_records(records)
        out = out.drop(columns=["LPI_raw", "lpi_imputed"], errors="ignore")
        out = out.merge(lpi_panel, on=["iso3_d", "year"], how="left")
        out["lpi_imputed"] = out["lpi_imputed"].fillna(False).astype(bool)

    # GOV
    if not wgi_df.empty:
        gov = wgi_df.rename(columns={"iso3": "iso3_d"})
        out = out.merge(gov, on=["iso3_d", "year"], how="left")
    else:
        out["GOV_raw"] = np.nan

    # UVGAP
    out = out.merge(
        uv_o.rename(columns={"iso3": "iso3_o"}),
        on=["iso3_o", "year"],
        how="left",
    )
    uv_j = pd.to_numeric(out["uv_import"], errors="coerce")
    uv_i = pd.to_numeric(out["uv_export"], errors="coerce")
    gap = pd.Series(np.nan, index=out.index, dtype=float)
    mask = (uv_j > 0) & (uv_i > 0)
    gap.loc[mask] = (np.log(uv_j.loc[mask]) - np.log(uv_i.loc[mask])).abs()
    out["UVGAP_raw"] = gap

    # Gravity (exact year match only — no silent LOCF)
    if not grav.empty:
        gcols = ["iso3_o", "iso3_d", "year"]
        keep = [c for c in ["distw_harmonic", "comlang_off", "fta_wto"] if c in grav.columns]
        g = grav[gcols + keep].copy()
        if "distw_harmonic" in g.columns:
            g = g.rename(columns={"distw_harmonic": "DIST_raw"})
        else:
            g["DIST_raw"] = np.nan
        if "comlang_off" in g.columns:
            g = g.rename(columns={"comlang_off": "LANG_raw"})
        else:
            g["LANG_raw"] = np.nan
        if "fta_wto" in g.columns:
            g = g.rename(columns={"fta_wto": "FTA_raw"})
        else:
            g["FTA_raw"] = np.nan
        out = out.merge(
            g[["iso3_o", "iso3_d", "year", "DIST_raw", "LANG_raw", "FTA_raw"]],
            on=["iso3_o", "iso3_d", "year"],
            how="left",
        )
    else:
        out["DIST_raw"] = np.nan
        out["LANG_raw"] = np.nan
        out["FTA_raw"] = np.nan

    # CULT (Hofstede cross-section; no year leakage)
    out["CULT_raw"] = np.nan
    if not hof.empty:
        h = hof.copy()
        h.columns = [c.lower() if str(c).lower() != "iso3" else "iso3" for c in h.columns]
        if "iso3" in h.columns and set(HOFSTEDE_DIMS).issubset(h.columns):
            h["iso3"] = h["iso3"].astype(str).str.upper()
            variances = h[HOFSTEDE_DIMS].var(ddof=1)
            h_idx = h.drop_duplicates("iso3").set_index("iso3")
            cult_vals = []
            for o, d in zip(out["iso3_o"], out["iso3_d"], strict=False):
                if o not in h_idx.index or d not in h_idx.index:
                    cult_vals.append(np.nan)
                    continue
                cult_vals.append(kogut_singh(h_idx.loc[o], h_idx.loc[d], variances))
            out["CULT_raw"] = cult_vals

    # TARIF from WITS (reporter=destination, partner=origin)
    out["TARIF_raw"] = np.nan
    if not wits_df.empty:
        w = wits_df.copy()
        w["hs_chapter"] = w["hs_chapter"].astype(str).str.zfill(2)
        if len(out):
            chapter = str(out["hs_chapter"].iloc[0]).zfill(2)
        else:
            chapter = str(settings.hs_chapters.primary).zfill(2)
        w = w.loc[w["hs_chapter"] == chapter]
        w = w.rename(
            columns={
                "reporter_iso3": "iso3_d",
                "partner_iso3": "iso3_o",
                "ahs_simple_avg": "TARIF_raw",
            }
        )
        out = out.drop(columns=["TARIF_raw"], errors="ignore")
        out = out.merge(
            w[["iso3_o", "iso3_d", "year", "TARIF_raw"]],
            on=["iso3_o", "iso3_d", "year"],
            how="left",
        )

    # Apply YAML transforms: keep *_raw and transformed id columns
    var_by_id: dict[str, VariableConfig] = {v.id: v for v in variables.variables}
    for vid, cfg in var_by_id.items():
        raw_col = f"{vid}_raw"
        if raw_col not in out.columns:
            out[raw_col] = np.nan
        transformed = apply_transform(out[raw_col], cfg.transform)
        out[vid] = transformed

    # Drop helper cols that are not features
    drop_helpers = [c for c in ["pop", "cpi", "uv_import", "uv_export"] if c in out.columns]
    out = out.drop(columns=drop_helpers, errors="ignore")
    return out
