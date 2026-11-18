"""Data dictionary, descriptives, correlations, and VIF for the built panel."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor

from imsfe.config import VariablesConfig, load_variables, project_root


def outputs_tables_dir() -> Path:
    path = project_root() / "outputs" / "tables"
    path.mkdir(parents=True, exist_ok=True)
    return path


def variable_coverage(
    panel: pd.DataFrame, variables: VariablesConfig | None = None
) -> pd.DataFrame:
    """Coverage % for each configured variable (non-null share of transformed column)."""
    variables = variables or load_variables()
    rows = []
    n = len(panel)
    for var in variables.variables:
        col = var.id if var.id in panel.columns else f"{var.id}_raw"
        if col not in panel.columns:
            cov = 0.0
        else:
            cov = float(panel[col].notna().mean() * 100.0) if n else 0.0
        rows.append(
            {
                "variable": var.id,
                "factor": var.factor,
                "direction": var.direction,
                "source": var.source,
                "coverage_pct": round(cov, 2),
            }
        )
    return pd.DataFrame.from_records(rows)


def write_data_dictionary(
    panel: pd.DataFrame,
    variables: VariablesConfig | None = None,
    path: Path | None = None,
) -> Path:
    """Write outputs/tables/T1_variables.csv."""
    variables = variables or load_variables()
    out = path or (outputs_tables_dir() / "T1_variables.csv")
    df = variable_coverage(panel, variables)
    df.to_csv(out, index=False)
    return out


def write_descriptives(
    panel: pd.DataFrame,
    variables: VariablesConfig | None = None,
    path: Path | None = None,
) -> Path:
    """Write T3_descriptives.csv for transformed feature columns."""
    variables = variables or load_variables()
    cols = [v.id for v in variables.variables if v.id in panel.columns]
    rows = []
    for c in cols:
        s = panel[c].dropna()
        rows.append(
            {
                "variable": c,
                "n": int(s.shape[0]),
                "mean": float(s.mean()) if len(s) else np.nan,
                "std": float(s.std(ddof=1)) if len(s) > 1 else np.nan,
                "min": float(s.min()) if len(s) else np.nan,
                "p25": float(s.quantile(0.25)) if len(s) else np.nan,
                "p50": float(s.quantile(0.50)) if len(s) else np.nan,
                "p75": float(s.quantile(0.75)) if len(s) else np.nan,
                "max": float(s.max()) if len(s) else np.nan,
                "missing_share": float(panel[c].isna().mean()) if len(panel) else np.nan,
            }
        )
    out = path or (outputs_tables_dir() / "T3_descriptives.csv")
    pd.DataFrame.from_records(rows).to_csv(out, index=False)
    return out


def write_correlation_and_vif(
    panel: pd.DataFrame,
    variables: VariablesConfig | None = None,
    *,
    corr_path: Path | None = None,
    vif_path: Path | None = None,
) -> tuple[Path, Path]:
    """Pearson correlation matrix and VIF on complete cases of feature columns."""
    variables = variables or load_variables()
    cols = [v.id for v in variables.variables if v.id in panel.columns]
    sub = panel[cols].apply(pd.to_numeric, errors="coerce")
    # Drop columns that are entirely missing (e.g. CULT/TARIF without manual data)
    usable = [c for c in cols if sub[c].notna().any()]
    sub = sub[usable]
    corr = sub.corr(method="pearson")
    cpath = corr_path or (outputs_tables_dir() / "T3_correlation.csv")
    corr.to_csv(cpath)

    # VIF needs at least 2 columns and complete rows
    complete = sub.dropna()
    vif_rows = []
    if complete.shape[1] >= 2 and complete.shape[0] >= complete.shape[1] + 1:
        X = complete.to_numpy(dtype=float)
        for i, name in enumerate(complete.columns):
            try:
                vif = float(variance_inflation_factor(X, i))
            except Exception:  # noqa: BLE001
                vif = float("nan")
            vif_rows.append({"variable": name, "vif": vif, "n_complete": int(len(complete))})
    else:
        for name in usable:
            vif_rows.append(
                {
                    "variable": name,
                    "vif": float("nan"),
                    "n_complete": int(len(complete)),
                    "note": "insufficient complete cases for VIF",
                }
            )
    vpath = vif_path or (outputs_tables_dir() / "T3_vif.csv")
    pd.DataFrame.from_records(vif_rows).to_csv(vpath, index=False)
    return cpath, vpath
