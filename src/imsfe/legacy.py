"""Reproduce and audit the original IMSFE Excel ranking (legacy module)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import numpy as np
import pandas as pd
import yaml
from openpyxl import load_workbook
from scipy.stats import kendalltau, rankdata

from imsfe.config import project_root
from imsfe.countries import to_iso3

LEGACY_EXCEL_REL = Path(
    "../old_submission/a. Technique IMSFE FOOTWEAR 2025 10 score Shoes - Baena & Cano.xlsx"
)

FACTORS: list[str] = ["COST", "LOGI", "COMM", "ECON", "POLI", "CULT"]

# Exact order from SPEC / prompt (DPV=benefit, IPV=cost).
VARIABLES: list[str] = [
    "PPAD",
    "INTC",
    "CIBC",
    "LPIN",
    "CPTR",
    "ITTT",
    "CUTA",
    "CCTI",
    "IOEF",
    "CLI",
    "INAN",
    "UNRA",
    "FSIN",
    "INRI",
    "DEIN",
    "GLIN",
    "CPIN",
    "CUDI",
]

DIRECTIONS: dict[str, Literal["benefit", "cost"]] = {
    "PPAD": "benefit",
    "INTC": "cost",
    "CIBC": "cost",
    "LPIN": "benefit",
    "CPTR": "benefit",
    "ITTT": "cost",
    "CUTA": "cost",
    "CCTI": "cost",
    "IOEF": "benefit",
    "CLI": "benefit",
    "INAN": "cost",
    "UNRA": "cost",
    "FSIN": "cost",
    "INRI": "cost",
    "DEIN": "benefit",
    "GLIN": "benefit",
    "CPIN": "benefit",
    "CUDI": "cost",
}

FACTOR_OF: dict[str, str] = {
    "PPAD": "COST",
    "INTC": "COST",
    "CIBC": "COST",
    "LPIN": "LOGI",
    "CPTR": "LOGI",
    "ITTT": "LOGI",
    "CUTA": "COMM",
    "CCTI": "COMM",
    "IOEF": "COMM",
    "CLI": "ECON",
    "INAN": "ECON",
    "UNRA": "ECON",
    "FSIN": "POLI",
    "INRI": "POLI",
    "DEIN": "POLI",
    "GLIN": "CULT",
    "CPIN": "CULT",
    "CUDI": "CULT",
}

# Columns on sheet "3. Standardization of criteria" for the 18 raw variables.
RAW_COLS: list[str] = [
    "E",
    "F",
    "G",
    "I",
    "J",
    "K",
    "M",
    "N",
    "O",
    "Q",
    "R",
    "S",
    "U",
    "V",
    "W",
    "Y",
    "Z",
    "AA",
]

FACTOR_WEIGHT_COLS = {"COST": "C", "LOGI": "G", "COMM": "K", "ECON": "O", "POLI": "S", "CULT": "W"}
VARIABLE_WEIGHT_COLS = {
    "PPAD": "C",
    "INTC": "D",
    "CIBC": "E",
    "LPIN": "G",
    "CPTR": "H",
    "ITTT": "I",
    "CUTA": "K",
    "CCTI": "L",
    "IOEF": "M",
    "CLI": "O",
    "INAN": "P",
    "UNRA": "Q",
    "FSIN": "S",
    "INRI": "T",
    "DEIN": "U",
    "GLIN": "W",
    "CPIN": "X",
    "CUDI": "Y",
}

# Paper / Excel rounded factor weights used in reproduction tests.
LEGACY_FACTOR_WEIGHTS: dict[str, float] = {
    "COST": 0.2147,
    "LOGI": 0.1847,
    "COMM": 0.1933,
    "ECON": 0.1533,
    "POLI": 0.1307,
    "CULT": 0.1233,
}

UNIFIED_COMBOS: list[tuple[str, float, float]] = [
    ("ponderado_30_70", 0.30, 0.70),
    ("ponderado_40_60", 0.40, 0.60),
    ("ponderado_50_50", 0.50, 0.50),
    ("ponderado_60_40", 0.60, 0.40),
    ("ponderado_70_30", 0.70, 0.30),
]

COLLAPSE_NORM_THRESHOLD = 1.0


@dataclass(frozen=True)
class ExpertWeights:
    """Individual and summary expert weights."""

    factor_weights: pd.DataFrame  # experts × factors
    variable_weights: pd.DataFrame  # experts × variables
    factor_summary: pd.DataFrame
    variable_summary: pd.DataFrame
    kendall_w_factors: float


def default_excel_path() -> Path:
    """Absolute path to the read-only legacy Excel workbook."""
    return (project_root() / LEGACY_EXCEL_REL).resolve()


def preferential_tariffs_path() -> Path:
    """Path to the manual preferential-tariff CSV for the legacy audit."""
    return project_root() / "data" / "manual" / "legacy_preferential_tariffs.csv"


def _col_index(letter: str) -> int:
    from openpyxl.utils import column_index_from_string

    return column_index_from_string(letter)


def _summarize_weights(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "mean": df.mean(axis=0),
            "sd": df.std(axis=0, ddof=1),
            "min": df.min(axis=0),
            "max": df.max(axis=0),
        }
    )


def kendalls_w(ratings: np.ndarray) -> float:
    """Kendall's W from a matrix of shape (m_raters, n_objects).

    Objects are ranked within each rater (higher rating -> better / lower rank
    number). Midranks are used for ties; the standard tie correction is applied.
    """
    ratings = np.asarray(ratings, dtype=float)
    if ratings.ndim != 2:
        raise ValueError("ratings must be 2-D")
    m, n = ratings.shape
    if m < 2 or n < 2:
        raise ValueError("need at least 2 raters and 2 objects")
    ranks = np.vstack([rankdata(-row, method="average") for row in ratings])
    rank_sums = ranks.sum(axis=0)
    mean_rank_sum = rank_sums.mean()
    s = float(np.sum((rank_sums - mean_rank_sum) ** 2))
    # Tie correction per rater: T = sum(t_k^3 - t_k)
    tie_sum = 0.0
    for row in ranks:
        _, counts = np.unique(row, return_counts=True)
        tie_sum += float(np.sum(counts**3 - counts))
    denominator = m**2 * (n**3 - n) - m * tie_sum
    if denominator <= 0:
        return 0.0
    return 12.0 * s / denominator


def load_expert_weights(excel_path: Path | None = None) -> ExpertWeights:
    """Load the 15 experts' factor and variable weights from sheet 1."""
    path = excel_path or default_excel_path()
    wb = load_workbook(path, data_only=True, read_only=True)
    try:
        ws = wb["1. Total Average for criteria"]
        experts: list[str] = []
        factor_rows: list[list[float]] = []
        for row in range(6, 21):
            name = ws.cell(row, 2).value
            if name is None:
                raise ValueError(f"Missing expert name at row {row}")
            experts.append(str(name))
            factor_rows.append(
                [float(ws.cell(row, _col_index(FACTOR_WEIGHT_COLS[f])).value) for f in FACTORS]
            )
        factor_weights = pd.DataFrame(factor_rows, index=experts, columns=FACTORS)

        var_rows: list[list[float]] = []
        for row in range(25, 40):
            var_rows.append(
                [
                    float(ws.cell(row, _col_index(VARIABLE_WEIGHT_COLS[v])).value)
                    for v in VARIABLES
                ]
            )
        variable_weights = pd.DataFrame(var_rows, index=experts, columns=VARIABLES)
    finally:
        wb.close()

    return ExpertWeights(
        factor_weights=factor_weights,
        variable_weights=variable_weights,
        factor_summary=_summarize_weights(factor_weights),
        variable_summary=_summarize_weights(variable_weights),
        kendall_w_factors=kendalls_w(factor_weights.to_numpy()),
    )


def export_weights_expert_yaml(
    weights: ExpertWeights,
    path: Path | None = None,
) -> Path:
    """Write config/weights_expert.yaml from loaded expert summaries."""
    out = path or (project_root() / "config" / "weights_expert.yaml")
    payload: dict[str, Any] = {
        "source": str(LEGACY_EXCEL_REL).replace("\\", "/"),
        "sheet": "1. Total Average for criteria",
        "n_experts": int(weights.factor_weights.shape[0]),
        "kendall_w_factors": float(weights.kendall_w_factors),
        "factors": {
            f: {
                "mean": float(weights.factor_summary.loc[f, "mean"]),
                "sd": float(weights.factor_summary.loc[f, "sd"]),
                "min": float(weights.factor_summary.loc[f, "min"]),
                "max": float(weights.factor_summary.loc[f, "max"]),
            }
            for f in FACTORS
        },
        "variables": {
            v: {
                "mean": float(weights.variable_summary.loc[v, "mean"]),
                "sd": float(weights.variable_summary.loc[v, "sd"]),
                "min": float(weights.variable_summary.loc[v, "min"]),
                "max": float(weights.variable_summary.loc[v, "max"]),
                "factor": FACTOR_OF[v],
            }
            for v in VARIABLES
        },
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(payload, fh, sort_keys=False, allow_unicode=True)
    return out


def load_raw_criteria(excel_path: Path | None = None) -> pd.DataFrame:
    """Load raw 18-variable values for the 30 countries from sheet 3."""
    path = excel_path or default_excel_path()
    wb = load_workbook(path, data_only=True, read_only=True)
    try:
        ws = wb["3. Standardization of criteria"]
        header_row = None
        for row in range(1, min(20, ws.max_row + 1)):
            if ws.cell(row, _col_index("D")).value == "Countries":
                header_row = row
                break
        if header_row is None:
            raise ValueError("Could not find 'Countries' header in column D")

        records: list[dict[str, Any]] = []
        row = header_row + 1
        while True:
            name = ws.cell(row, _col_index("D")).value
            if name is None or not isinstance(name, str) or name.strip() == "":
                break
            if name.strip().startswith("Table") or name.strip() == "Pre-selection":
                break
            rec: dict[str, Any] = {
                "country": name.strip(),
                "iso3": to_iso3(name.strip()),
            }
            for var, col in zip(VARIABLES, RAW_COLS, strict=True):
                val = ws.cell(row, _col_index(col)).value
                if val is None:
                    raise ValueError(f"Missing {var} for {name} at row {row}")
                rec[var] = float(val)
            records.append(rec)
            row += 1
            if len(records) > 40:
                raise ValueError("Unexpectedly many country rows in raw block")
    finally:
        wb.close()

    if len(records) != 30:
        raise ValueError(f"Expected 30 countries, found {len(records)}")
    return pd.DataFrame.from_records(records).set_index("iso3")


def ratio_normalize(raw: pd.DataFrame) -> pd.DataFrame:
    """Legacy ratio normalisation: benefit y/max*10, cost min/y*10."""
    out = pd.DataFrame(index=raw.index)
    for var in VARIABLES:
        series = raw[var].astype(float)
        direction = DIRECTIONS[var]
        if direction == "benefit":
            vmax = series.max()
            if vmax == 0:
                raise ValueError(f"max is zero for benefit variable {var}")
            out[var] = series / vmax * 10.0
        else:
            vmin = series.min()
            if (series <= 0).any():
                raise ValueError(f"non-positive values in cost variable {var}")
            out[var] = vmin / series * 10.0
    return out


def minmax_normalize(raw: pd.DataFrame) -> pd.DataFrame:
    """Min-max normalisation to [0, 10] respecting benefit/cost direction."""
    out = pd.DataFrame(index=raw.index)
    for var in VARIABLES:
        series = raw[var].astype(float)
        vmin, vmax = float(series.min()), float(series.max())
        span = vmax - vmin
        if span == 0:
            out[var] = 5.0
            continue
        if DIRECTIONS[var] == "benefit":
            out[var] = (series - vmin) / span * 10.0
        else:
            out[var] = (vmax - series) / span * 10.0
    return out


def rank_normalize(raw: pd.DataFrame) -> pd.DataFrame:
    """Rank normalisation to (0, 10]: best value gets 10, worst gets 10/n."""
    out = pd.DataFrame(index=raw.index)
    n = len(raw)
    for var in VARIABLES:
        series = raw[var].astype(float)
        # Higher rank number = better. For cost, lower raw is better.
        if DIRECTIONS[var] == "benefit":
            ranks = rankdata(series.to_numpy(), method="average")
        else:
            ranks = rankdata(-series.to_numpy(), method="average")
        out[var] = ranks / n * 10.0
    return out


def aggregate_imsfe(
    normalized: pd.DataFrame,
    variable_weights: pd.Series,
    factor_weights: pd.Series | None = None,
) -> tuple[pd.Series, pd.DataFrame]:
    """Hierarchical WSM: variables -> factors -> overall IMSFE score."""
    fw = factor_weights if factor_weights is not None else pd.Series(LEGACY_FACTOR_WEIGHTS)
    # Renormalise within each factor in case of floating noise.
    factor_scores = pd.DataFrame(index=normalized.index, columns=FACTORS, dtype=float)
    for factor in FACTORS:
        vars_f = [v for v in VARIABLES if FACTOR_OF[v] == factor]
        w = variable_weights[vars_f].astype(float)
        w = w / w.sum()
        factor_scores[factor] = normalized[vars_f].mul(w, axis=1).sum(axis=1)
    fw = fw[FACTORS].astype(float)
    fw = fw / fw.sum()
    scores = factor_scores.mul(fw, axis=1).sum(axis=1)
    scores.name = "imsfe"
    return scores, factor_scores


def load_eoc(excel_path: Path | None = None) -> pd.DataFrame:
    """Load EOC (CAE) for countries from the Pre-selection sheet."""
    path = excel_path or default_excel_path()
    wb = load_workbook(path, data_only=True, read_only=True)
    try:
        ws = wb["Pre-selection"]
        records: list[dict[str, Any]] = []
        row = 14
        while True:
            name = ws.cell(row, _col_index("B")).value
            eoc = ws.cell(row, _col_index("G")).value
            if name is None or eoc is None:
                break
            name_s = str(name).strip()
            try:
                iso3 = to_iso3(name_s)
            except KeyError:
                row += 1
                continue
            records.append({"iso3": iso3, "country": name_s, "eoc": float(eoc)})
            row += 1
    finally:
        wb.close()
    df = pd.DataFrame.from_records(records).drop_duplicates(subset=["iso3"]).set_index("iso3")
    return df


def normalize_eoc(eoc: pd.Series) -> pd.Series:
    """NEOC = eoc / max(eoc) * 10 (Normalización Propuesta)."""
    vmax = float(eoc.max())
    if vmax <= 0:
        raise ValueError("EOC max must be positive")
    out = eoc / vmax * 10.0
    out.name = "neoc"
    return out


def unified_scores(nimsfe: pd.Series, neoc: pd.Series) -> pd.DataFrame:
    """Five EOC/IMSFE weighting combinations from the Pre-selection sheet."""
    aligned = pd.concat([nimsfe.rename("nimsfe"), neoc.rename("neoc")], axis=1).dropna()
    out = pd.DataFrame(index=aligned.index)
    out["nimsfe"] = aligned["nimsfe"]
    out["neoc"] = aligned["neoc"]
    for name, w_eoc, w_imsfe in UNIFIED_COMBOS:
        out[name] = w_eoc * aligned["neoc"] + w_imsfe * aligned["nimsfe"]
    return out


def load_preferential_tariffs(path: Path | None = None) -> pd.Series:
    """Load preferential tariffs; raise if any value is missing."""
    csv_path = path or preferential_tariffs_path()
    if not csv_path.is_file():
        raise FileNotFoundError(f"Preferential tariff file not found: {csv_path}")
    df = pd.read_csv(csv_path)
    required = {"iso3", "tariff_pct", "source"}
    if not required.issubset(df.columns):
        raise ValueError(f"{csv_path} must have columns {sorted(required)}")
    df = df.set_index("iso3")
    missing = df["tariff_pct"].isna() | (df["tariff_pct"].astype(str).str.strip() == "")
    if missing.any():
        miss = sorted(df.index[missing].tolist())
        raise ValueError(
            "Preferential tariffs are incomplete; fill tariff_pct in "
            f"{csv_path} from WITS (AHS, HS64, origin Colombia). Missing: {miss}"
        )
    return df["tariff_pct"].astype(float)


def score_pipeline(
    raw: pd.DataFrame,
    variable_weights: pd.Series,
    method: Literal["ratio_legacy", "minmax", "rank", "minmax_pref_tariff"],
    factor_weights: pd.Series | None = None,
    pref_tariffs: pd.Series | None = None,
) -> pd.Series:
    """Normalise and aggregate under one method label."""
    data = raw[VARIABLES].copy()
    if method == "minmax_pref_tariff":
        if pref_tariffs is None:
            pref_tariffs = load_preferential_tariffs()
        missing = [i for i in data.index if i not in pref_tariffs.index]
        if missing:
            raise ValueError(f"Preferential tariffs missing ISO3: {missing}")
        data["CUTA"] = pref_tariffs.reindex(data.index).astype(float)
        norm = minmax_normalize(data)
    elif method == "ratio_legacy":
        norm = ratio_normalize(data)
    elif method == "minmax":
        norm = minmax_normalize(data)
    elif method == "rank":
        norm = rank_normalize(data)
    else:
        raise ValueError(f"Unknown method: {method}")
    scores, _ = aggregate_imsfe(norm, variable_weights, factor_weights)
    return scores


def variable_contributions(
    normalized: pd.DataFrame,
    variable_weights: pd.Series,
    factor_weights: pd.Series | None = None,
) -> pd.DataFrame:
    """Additive per-variable contribution to the overall IMSFE score."""
    fw = factor_weights if factor_weights is not None else pd.Series(LEGACY_FACTOR_WEIGHTS)
    fw = fw[FACTORS].astype(float)
    fw = fw / fw.sum()
    contrib = pd.DataFrame(index=normalized.index, columns=VARIABLES, dtype=float)
    for factor in FACTORS:
        vars_f = [v for v in VARIABLES if FACTOR_OF[v] == factor]
        w = variable_weights[vars_f].astype(float)
        w = w / w.sum()
        for v in vars_f:
            contrib[v] = normalized[v] * w[v] * fw[factor]
    return contrib


def find_identical_values(raw: pd.DataFrame) -> list[dict[str, Any]]:
    """Find variables where distinct countries share the exact same raw value."""
    findings: list[dict[str, Any]] = []
    for var in VARIABLES:
        groups = raw.groupby(var)["country"].apply(list)
        for value, countries in groups.items():
            if len(countries) >= 2:
                findings.append(
                    {
                        "variable": var,
                        "value": float(value),
                        "countries": sorted(countries),
                        "iso3": sorted(raw.loc[raw[var] == value].index.tolist()),
                    }
                )
    return findings


def collapse_diagnostics(raw: pd.DataFrame) -> pd.DataFrame:
    """Detect ratio-normalisation near-binary collapse.

    A variable collapses when most countries get a normalised score < 1 and the
    ratio formula is driven by a near-zero (or relatively tiny) extremum: cost
    variables with min < 1 or min/max < 0.01, or benefit variables where the
    max dwarfs the rest (share of scores < 1 at least 80%).
    """
    rows: list[dict[str, Any]] = []
    for var in VARIABLES:
        series = raw[var].astype(float)
        direction = DIRECTIONS[var]
        vmin, vmax = float(series.min()), float(series.max())
        if direction == "benefit":
            norm = series / vmax * 10.0
        else:
            norm = vmin / series * 10.0
        share_lt_1 = float((norm < COLLAPSE_NORM_THRESHOLD).mean())
        ratio_mm = (vmin / vmax) if vmax != 0 else 0.0
        if direction == "cost":
            collapses = share_lt_1 >= 0.45 and (vmin < 1.0 or ratio_mm < 0.01)
        else:
            collapses = share_lt_1 >= 0.80
        rows.append(
            {
                "variable": var,
                "direction": direction,
                "min": vmin,
                "max": vmax,
                "min_over_max": ratio_mm,
                "share_norm_lt_1": share_lt_1,
                "collapses": collapses,
            }
        )
    return pd.DataFrame(rows)


def build_audit_report(
    raw: pd.DataFrame,
    normalized: pd.DataFrame,
    scores: pd.Series,
    contributions: pd.DataFrame,
) -> str:
    """Markdown audit report with computed evidence + manual-check placeholders."""
    identical = find_identical_values(raw)
    collapse = collapse_diagnostics(raw)
    collapsing = collapse.loc[collapse["collapses"], "variable"].tolist()

    lines: list[str] = [
        "# Legacy IMSFE audit report",
        "",
        "Generated from the original Excel (read-only). Numbers below are computed",
        "from the data; manuscript-only issues are marked **MANUAL CHECK**.",
        "",
        "## 1. Identical raw values across countries",
        "",
    ]
    if not identical:
        lines.append("No identical cross-country values detected.")
    else:
        lines.append("| Variable | Value | Countries | ISO3 |")
        lines.append("|---|---:|---|---|")
        for item in identical:
            countries = ", ".join(item["countries"])
            iso = ", ".join(item["iso3"])
            value = item["value"]
            value_s = f"{value:.0f}" if float(value).is_integer() else f"{value:g}"
            lines.append(f"| {item['variable']} | {value_s} | {countries} | {iso} |")
    lines.extend(
        [
            "",
            "Expected finding: **CPTR Austria == Australia == 9375992**.",
            "",
            "## 2. Ratio normalisation near-binary collapse",
            "",
            "For cost variables with a near-zero minimum, `min/y*10` leaves most",
            "countries near 0 and only the minimum near 10.",
            "",
            "| Variable | Direction | Min | Max | Share norm < 1 | Collapses |",
            "|---|---|---:|---:|---:|:---:|",
        ]
    )
    for _, row in collapse.iterrows():
        lines.append(
            f"| {row['variable']} | {row['direction']} | {row['min']:g} | "
            f"{row['max']:g} | {row['share_norm_lt_1']:.2f} | "
            f"{'yes' if row['collapses'] else 'no'} |"
        )
    lines.extend(
        [
            "",
            "Variables flagged as collapsing: "
            + (", ".join(collapsing) if collapsing else "(none)")
            + ".",
            "Expected: CUTA, CIBC, CCTI, CPTR, INAN.",
            "",
            "## 3. Per-variable contribution to Switzerland and Singapore",
            "",
        ]
    )
    for iso, label in [("CHE", "Switzerland"), ("SGP", "Singapore")]:
        score = float(scores.loc[iso])
        mean_contrib = contributions.mean(axis=0)
        own = contributions.loc[iso]
        excess = own - mean_contrib
        lines.append(f"### {label} (`{iso}`), IMSFE = {score:.4f}")
        lines.append("")
        lines.append("| Variable | Contribution | Excess vs mean |")
        lines.append("|---|---:|---:|")
        order = excess.sort_values(ascending=False).index
        for var in order:
            lines.append(
                f"| {var} | {own[var]:.4f} | {excess[var]:+.4f} |"
            )
        lines.append("")

    lines.extend(
        [
            "## 4. Manuscript-only issues (MANUAL CHECK)",
            "",
            "- **MANUAL CHECK — Table 8 row misalignment:** several manuscript rows",
            "  appear to show another country's normalised values / unified scores",
            "  (e.g. Vietnam/Switzerland, Poland/Denmark, Korea/Panama,",
            "  Mexico/France, Japan/USA). Verify against `outputs/tables/legacy_comparison.csv`",
            "  and the Excel sheet `3. Standardization of criteria`.",
            "- **MANUAL CHECK — Table 7 Argentina vs Australia:** the manuscript Table 7",
            "  lists Argentina, which is not among the 30 pre-selected markets in the",
            "  Excel; Australia is present in the Excel pre-selection but may be missing",
            "  from the manuscript table.",
            "",
            "## 5. Ranking snapshot (ratio_legacy)",
            "",
            "| Rank | ISO3 | Country | IMSFE |",
            "|---:|---|---|---:|",
        ]
    )
    ranked = scores.sort_values(ascending=False)
    for i, (iso, score) in enumerate(ranked.items(), start=1):
        country = str(raw.loc[iso, "country"])
        lines.append(f"| {i} | {iso} | {country} | {score:.4f} |")
    lines.append("")
    return "\n".join(lines)


def run_legacy(
    excel_path: Path | None = None,
    include_pref_tariff: bool = True,
) -> dict[str, Any]:
    """Run the full legacy reproduction, audit, and comparison pipeline."""
    path = excel_path or default_excel_path()
    if not path.is_file():
        raise FileNotFoundError(f"Legacy Excel not found (read-only expected): {path}")

    experts = load_expert_weights(path)
    yaml_path = export_weights_expert_yaml(experts)

    raw = load_raw_criteria(path)
    var_w = experts.variable_summary["mean"]
    # Use the Excel total-average variable weights (already means).
    factor_w = pd.Series(LEGACY_FACTOR_WEIGHTS)

    methods: dict[str, pd.Series] = {
        "ratio_legacy": score_pipeline(raw, var_w, "ratio_legacy", factor_w),
        "minmax": score_pipeline(raw, var_w, "minmax", factor_w),
        "rank": score_pipeline(raw, var_w, "rank", factor_w),
    }

    pref_error: str | None = None
    if include_pref_tariff:
        try:
            methods["minmax_pref_tariff"] = score_pipeline(
                raw, var_w, "minmax_pref_tariff", factor_w
            )
        except ValueError as exc:
            pref_error = str(exc)

    norm_legacy = ratio_normalize(raw[VARIABLES])
    contrib = variable_contributions(norm_legacy, var_w, factor_w)
    audit_md = build_audit_report(raw, norm_legacy, methods["ratio_legacy"], contrib)

    eoc_df = load_eoc(path)
    eoc_30 = eoc_df.reindex(raw.index)["eoc"]
    if eoc_30.isna().any():
        missing = eoc_30[eoc_30.isna()].index.tolist()
        raise ValueError(f"EOC missing for pre-selected ISO3: {missing}")
    neoc = normalize_eoc(eoc_30)
    nimsfe = methods["ratio_legacy"] / methods["ratio_legacy"].max() * 10.0
    unified = unified_scores(nimsfe, neoc)

    # Comparison table
    baseline = methods["ratio_legacy"].sort_values(ascending=False)
    rows: list[dict[str, Any]] = []
    for iso in baseline.index:
        row: dict[str, Any] = {
            "iso3": iso,
            "country": raw.loc[iso, "country"],
            "score_ratio_legacy": float(methods["ratio_legacy"].loc[iso]),
            "rank_ratio_legacy": int(baseline.index.get_loc(iso) + 1),
        }
        for method, scores in methods.items():
            ordered = scores.sort_values(ascending=False)
            row[f"score_{method}"] = float(scores.loc[iso])
            row[f"rank_{method}"] = int(ordered.index.get_loc(iso) + 1)
        rows.append(row)
    comparison = pd.DataFrame(rows)

    tau_rows = []
    base_ranks = comparison.set_index("iso3")["rank_ratio_legacy"]
    for method in methods:
        other = comparison.set_index("iso3")[f"rank_{method}"]
        tau, p = kendalltau(base_ranks, other)
        tau_rows.append(
            {
                "method": method,
                "kendall_tau_vs_ratio_legacy": float(tau),
                "p_value": float(p),
            }
        )
    tau_df = pd.DataFrame(tau_rows)

    out_tables = project_root() / "outputs" / "tables"
    out_tables.mkdir(parents=True, exist_ok=True)
    audit_path = out_tables / "legacy_audit.md"
    comparison_path = out_tables / "legacy_comparison.csv"
    tau_path = out_tables / "legacy_kendall_tau.csv"
    unified_path = out_tables / "legacy_unified_scores.csv"

    audit_path.write_text(audit_md, encoding="utf-8")
    comparison.to_csv(comparison_path, index=False, float_format="%.6f")
    tau_df.to_csv(tau_path, index=False, float_format="%.6f")
    unified_out = unified.copy()
    unified_out.insert(0, "country", raw.loc[unified_out.index, "country"].values)
    unified_out.to_csv(unified_path, float_format="%.6f")

    return {
        "excel_path": path,
        "weights_yaml": yaml_path,
        "experts": experts,
        "raw": raw,
        "scores": methods,
        "neoc": neoc,
        "unified": unified,
        "audit_path": audit_path,
        "comparison_path": comparison_path,
        "tau_path": tau_path,
        "unified_path": unified_path,
        "pref_tariff_error": pref_error,
        "comparison": comparison,
        "tau": tau_df,
    }
