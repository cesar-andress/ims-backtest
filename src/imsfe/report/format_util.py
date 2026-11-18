"""English number formatting and Markdown / booktabs exporters (no .tex files)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from imsfe.build.descriptives import outputs_tables_dir
from imsfe.countries import country_name


def fmt_number(value: Any, *, digits: int = 3, comma: bool = True) -> str:
    """Format a scalar in English: dot decimal, optional thousands comma."""
    if value is None or (isinstance(value, float) and not np.isfinite(value)):
        return ""
    if isinstance(value, (np.integer, int)) and not isinstance(value, bool):
        return f"{int(value):,}" if comma else str(int(value))
    try:
        x = float(value)
    except (TypeError, ValueError):
        return str(value)
    if not np.isfinite(x):
        return ""
    if abs(x - round(x)) < 1e-12 and abs(x) >= 1000:
        return f"{int(round(x)):,}" if comma else str(int(round(x)))
    s = f"{x:,.{digits}f}" if comma else f"{x:.{digits}f}"
    return s


def format_dataframe(
    df: pd.DataFrame,
    *,
    float_digits: int = 3,
    int_cols: set[str] | None = None,
    float_cols: set[str] | None = None,
) -> pd.DataFrame:
    """Return a string-formatted copy suitable for Markdown display."""
    int_cols = int_cols or set()
    float_cols = float_cols or set()
    out = df.copy()
    for col in out.columns:
        if col in int_cols:
            out[col] = out[col].map(lambda v: fmt_number(v, digits=0))
        elif col in float_cols or pd.api.types.is_float_dtype(df[col]):
            out[col] = out[col].map(lambda v: fmt_number(v, digits=float_digits))
        elif pd.api.types.is_integer_dtype(df[col]):
            out[col] = out[col].map(lambda v: fmt_number(v, digits=0))
    return out


def dataframe_to_markdown(df: pd.DataFrame, *, title: str, notes: str = "") -> str:
    """GitHub-flavoured Markdown table with a title."""
    lines = [f"# {title}", ""]
    if notes:
        lines.extend([notes.strip(), ""])
    if df.empty:
        lines.append("_Empty table._")
        return "\n".join(lines) + "\n"
    # pandas.to_markdown needs tabulate; fall back to manual pipe table.
    try:
        body = df.to_markdown(index=False)
    except (ImportError, ValueError):
        cols = list(df.columns)
        header = "| " + " | ".join(str(c) for c in cols) + " |"
        sep = "| " + " | ".join("---" for _ in cols) + " |"
        rows = []
        for _, row in df.iterrows():
            rows.append("| " + " | ".join(str(row[c]) for c in cols) + " |")
        body = "\n".join([header, sep, *rows])
    lines.append(body)
    return "\n".join(lines) + "\n"


def dataframe_to_booktabs(df: pd.DataFrame, *, caption: str, label: str) -> str:
    """Booktabs snippet as a string (embedded in Markdown; never written as .tex)."""
    cols = list(df.columns)
    align = "l" * len(cols)
    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        rf"\caption{{{caption}}}",
        rf"\label{{{label}}}",
        rf"\begin{{tabular}}{{{align}}}",
        r"\toprule",
        " & ".join(str(c).replace("_", r"\_") for c in cols) + r" \\",
        r"\midrule",
    ]
    for _, row in df.iterrows():
        cells = [str(row[c]).replace("_", r"\_") for c in cols]
        lines.append(" & ".join(cells) + r" \\")
    lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{table}", ""])
    return "\n".join(lines)


def write_table_bundle(
    df: pd.DataFrame,
    stem: str,
    *,
    title: str,
    notes: str = "",
    float_digits: int = 3,
    int_cols: set[str] | None = None,
    float_cols: set[str] | None = None,
    iso_cols: tuple[str, ...] = (),
) -> dict[str, Path]:
    """Write CSV + Markdown (with embedded booktabs code fence). No .tex files."""
    tables = outputs_tables_dir()
    out_df = df.copy()
    for col in iso_cols:
        if col in out_df.columns and f"{col}_name" not in out_df.columns:
            name_col = "country" if col in {"iso3", "dest", "origin"} else f"{col}_name"
            if col == "dest":
                name_col = "country"
            out_df.insert(
                out_df.columns.get_loc(col) + 1,
                name_col,
                out_df[col].map(lambda x: country_name(str(x))),
            )
    csv_path = tables / f"{stem}.csv"
    out_df.to_csv(csv_path, index=False)

    display = format_dataframe(
        out_df, float_digits=float_digits, int_cols=int_cols, float_cols=float_cols
    )
    md = dataframe_to_markdown(display, title=title, notes=notes)
    booktabs = dataframe_to_booktabs(display, caption=title, label=f"tab:{stem}")
    md += "\n## Booktabs (copy into manuscript; not a repo .tex file)\n\n"
    md += "```latex\n" + booktabs + "```\n"
    md_path = tables / f"{stem}.md"
    md_path.write_text(md, encoding="utf-8")
    return {"csv": csv_path, "md": md_path}
