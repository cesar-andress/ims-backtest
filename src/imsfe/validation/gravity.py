"""PPML gravity baselines and explanatory export regressions (pyfixest)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from pyfixest.estimation import fepois


@dataclass
class PPMLResult:
    label: str
    formula: str
    n_obs: int
    coef: pd.Series
    se: pd.Series
    conf_low: pd.Series | None = None
    conf_high: pd.Series | None = None
    notes: str = ""

    def to_frame(self) -> pd.DataFrame:
        out = pd.DataFrame(
            {
                "term": self.coef.index.astype(str),
                "estimate": self.coef.to_numpy(dtype=float),
                "std_error": self.se.reindex(self.coef.index).to_numpy(dtype=float),
            }
        )
        if self.conf_low is not None:
            out["ci95_low"] = self.conf_low.reindex(self.coef.index).to_numpy(dtype=float)
        if self.conf_high is not None:
            out["ci95_high"] = self.conf_high.reindex(self.coef.index).to_numpy(dtype=float)
        out.insert(0, "model", self.label)
        out["n_obs"] = self.n_obs
        out["formula"] = self.formula
        out["notes"] = self.notes
        return out


def _attach_contig(df: pd.DataFrame) -> pd.DataFrame:
    """Left-join CEPII contig when missing from the panel."""
    if "contig" in df.columns and df["contig"].notna().any():
        return df
    from imsfe.io import raw_dir

    path = raw_dir() / "cepii_gravity" / "gravity.parquet"
    if not path.is_file():
        df = df.copy()
        df["contig"] = 0.0
        return df
    grav = pd.read_parquet(path, columns=["iso3_o", "iso3_d", "year", "contig"])
    grav = grav.drop_duplicates(["iso3_o", "iso3_d", "year"], keep="first")
    out = df.merge(grav, on=["iso3_o", "iso3_d", "year"], how="left", suffixes=("", "_g"))
    if "contig_g" in out.columns:
        out["contig"] = out["contig_g"]
        out = out.drop(columns=["contig_g"])
    return out


def _prepare_gravity_frame(panel: pd.DataFrame) -> pd.DataFrame:
    """Covariates for gravity: log GDP_j, log dist, fta, comlang, contig."""
    df = _attach_contig(panel.copy())
    # GDP of destination: use GDPPC_raw (PPP levels) as a destination mass proxy
    if "GDPPC_raw" in df.columns:
        df["log_gdp_j"] = np.log(
            pd.to_numeric(df["GDPPC_raw"], errors="coerce").clip(lower=1e-12)
        )
    elif "GDPPC" in df.columns:
        df["log_gdp_j"] = pd.to_numeric(df["GDPPC"], errors="coerce")
    else:
        df["log_gdp_j"] = np.nan
    dist = pd.to_numeric(df.get("DIST_raw", df.get("DIST")), errors="coerce")
    df["log_dist"] = np.log(dist.clip(lower=1e-12))
    for col, src in [("fta", "FTA_raw"), ("comlang", "LANG_raw")]:
        if src in df.columns:
            df[col] = pd.to_numeric(df[src], errors="coerce")
        else:
            alt = "FTA" if col == "fta" else "LANG"
            df[col] = pd.to_numeric(df.get(alt), errors="coerce")
    df["contig"] = pd.to_numeric(df.get("contig"), errors="coerce")
    df["oy"] = df["iso3_o"].astype(str) + "#" + df["year"].astype(str)
    df["pair"] = df["iso3_o"].astype(str) + "#" + df["iso3_d"].astype(str)
    df["X"] = pd.to_numeric(df["X_ijt"], errors="coerce").fillna(0.0).clip(lower=0.0)
    return df


def fit_gravity_ppml(
    panel: pd.DataFrame,
    train_years: list[int],
    *,
    destination_fe: bool = False,
) -> Any:
    """Fit PPML ``X ~ log_gdp_j + log_dist + fta + comlang + contig | oy`` on train years."""
    df = _prepare_gravity_frame(panel)
    df = df.loc[df["year"].isin(train_years)].copy()
    df = df.dropna(subset=["X", "log_gdp_j", "log_dist"])
    # Binary missings -> 0 (no FTA / language / contiguity); continuous already dropped.
    for c in ("fta", "comlang", "contig"):
        df[c] = df[c].fillna(0.0)
    if df.empty:
        raise RuntimeError("Gravity PPML: no training rows after dropping missing covariates")
    fe = "oy + iso3_d" if destination_fe else "oy"
    fml = f"X ~ log_gdp_j + log_dist + fta + comlang + contig | {fe}"
    est = fepois(fml, data=df, vcov={"CRV1": "pair"})
    return est


def predict_gravity_scores(
    panel: pd.DataFrame,
    est: Any,
    years: list[int],
) -> pd.DataFrame:
    """Gravity ranking score for the given years.

    Within an origin-year cross-section the origin-year FE is constant across
    destinations, so out-of-sample ranking uses the covariate index
    ``exp(x'β)`` only (avoids NaNs from unseen ``oy`` levels in ``predict``).
    """
    df = _prepare_gravity_frame(panel)
    df = df.loc[df["year"].isin(years)].copy()
    for c in ("fta", "comlang", "contig"):
        df[c] = df[c].fillna(0.0)
    coef = est.coef()
    xb = np.zeros(len(df), dtype=float)
    for name, col in [
        ("log_gdp_j", "log_gdp_j"),
        ("log_dist", "log_dist"),
        ("fta", "fta"),
        ("comlang", "comlang"),
        ("contig", "contig"),
    ]:
        if name in coef.index:
            xb = xb + float(coef[name]) * pd.to_numeric(df[col], errors="coerce").fillna(
                0.0
            ).to_numpy(dtype=float)
    mu = np.exp(np.clip(xb, -50, 50))
    out = df[["iso3_o", "iso3_d", "year"]].copy()
    out["score"] = mu
    out = out.drop_duplicates(["iso3_o", "iso3_d", "year"], keep="first")
    return out


def explanatory_ppml_score(
    panel: pd.DataFrame,
    scores: pd.DataFrame,
    *,
    horizon: int = 1,
    label: str = "y_level_on_ims",
) -> PPMLResult:
    """PPML of ``y_level`` on IMS score with origin-year and destination FE; CRV1 by pair."""
    ycol = f"y_level_k{horizon}"
    df = panel[["iso3_o", "iso3_d", "year", ycol]].merge(
        scores,
        left_on=["iso3_o", "year", "iso3_d"],
        right_on=["origin", "year", "dest"],
        how="inner",
    )
    df = df.rename(columns={ycol: "y_level", "score": "ims_score"})
    df["y_level"] = pd.to_numeric(df["y_level"], errors="coerce")
    df = df.dropna(subset=["y_level", "ims_score"])
    df["oy"] = df["iso3_o"].astype(str) + "#" + df["year"].astype(str)
    df["pair"] = df["iso3_o"].astype(str) + "#" + df["iso3_d"].astype(str)
    fml = "y_level ~ ims_score | oy + iso3_d"
    est = fepois(fml, data=df, vcov={"CRV1": "pair"})
    coef = est.coef()
    se = est.se()
    try:
        ci = est.confint()
        low, high = ci.iloc[:, 0], ci.iloc[:, 1]
    except Exception:  # noqa: BLE001
        low = coef - 1.96 * se
        high = coef + 1.96 * se
    return PPMLResult(
        label=label,
        formula=fml,
        n_obs=int(len(df)),
        coef=coef,
        se=se,
        conf_low=low,
        conf_high=high,
        notes=f"cluster=pair; horizon=k{horizon}",
    )


def explanatory_ppml_factors(
    panel: pd.DataFrame,
    factor_scores: pd.DataFrame,
    *,
    horizon: int = 1,
    label: str = "y_level_on_factors",
) -> PPMLResult:
    """PPML of ``y_level`` on factor scores with oy + destination FE."""
    ycol = f"y_level_k{horizon}"
    df = panel[["iso3_o", "iso3_d", "year", ycol]].merge(
        factor_scores,
        on=["iso3_o", "iso3_d", "year"],
        how="inner",
    )
    df = df.rename(columns={ycol: "y_level"})
    df["y_level"] = pd.to_numeric(df["y_level"], errors="coerce")
    factor_cols = [c for c in factor_scores.columns if c not in ("iso3_o", "iso3_d", "year")]
    df = df.dropna(subset=["y_level", *factor_cols])
    df["oy"] = df["iso3_o"].astype(str) + "#" + df["year"].astype(str)
    df["pair"] = df["iso3_o"].astype(str) + "#" + df["iso3_d"].astype(str)
    rhs = " + ".join(factor_cols)
    # Origin-year FE only: destination FE plus many factor scores often
    # separates / drops all rows in short panels.
    fml = f"y_level ~ {rhs} | oy"
    est = fepois(fml, data=df, vcov={"CRV1": "pair"})
    coef = est.coef()
    se = est.se()
    try:
        ci = est.confint()
        low, high = ci.iloc[:, 0], ci.iloc[:, 1]
    except Exception:  # noqa: BLE001
        low = coef - 1.96 * se
        high = coef + 1.96 * se
    return PPMLResult(
        label=label,
        formula=fml,
        n_obs=int(len(df)),
        coef=coef,
        se=se,
        conf_low=low,
        conf_high=high,
        notes=f"cluster=pair; horizon=k{horizon}; factors={factor_cols}",
    )
