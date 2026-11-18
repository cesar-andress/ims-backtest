#!/usr/bin/env python3
"""Verify manuscript/refs.bib DOIs against the Crossref API.

Never invents references. Writes a human-readable report to
``outputs/logs/refs_check.md`` and a JSON summary beside it.

Usage (from paper/):
  uv run python scripts/check_refs.py
"""

from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # paper/
IMR = ROOT.parent
BIB = IMR / "manuscript" / "refs.bib"
EXTRACTED = IMR / "manuscript" / "refs_extracted.json"
OUT_MD = ROOT / "outputs" / "logs" / "refs_check.md"
OUT_JSON = ROOT / "outputs" / "logs" / "refs_check.json"


def _mailto() -> str:
    return os.environ.get("CROSSREF_MAILTO") or os.environ.get("MAILTO") or "anonymous@example.com"


def _user_agent() -> str:
    custom = os.environ.get("CROSSREF_USER_AGENT")
    if custom:
        return custom
    return f"imsfe-refs-check/0.1 (mailto:{_mailto()})"


def crossref_works(doi: str) -> dict | None:
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    req = urllib.request.Request(url, headers={"User-Agent": _user_agent()})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        return payload.get("message")
    except urllib.error.HTTPError as exc:
        return {"_error": f"HTTP {exc.code}", "_doi": doi}
    except Exception as exc:  # noqa: BLE001
        return {"_error": str(exc), "_doi": doi}


def _norm(s: str | None) -> str:
    if not s:
        return ""
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def title_overlap(a: str, b: str) -> float:
    ta = set(_norm(a).split())
    tb = set(_norm(b).split())
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / max(len(ta), len(tb))


def load_entries() -> list[dict]:
    if EXTRACTED.is_file():
        return json.loads(EXTRACTED.read_text(encoding="utf-8"))
    # Fallback: parse DOI lines from bib
    text = BIB.read_text(encoding="utf-8")
    entries = []
    key = None
    doi = None
    for line in text.splitlines():
        m = re.match(r"@\w+\{([^,]+),", line)
        if m:
            if key:
                entries.append({"key": key, "doi": doi})
            key = m.group(1)
            doi = None
        md = re.search(r"doi\s*=\s*\{([^}]+)\}", line, re.I)
        if md:
            doi = md.group(1)
    if key:
        entries.append({"key": key, "doi": doi})
    return entries


def main() -> int:
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    entries = load_entries()
    rows = []
    for i, e in enumerate(entries):
        key = e.get("key")
        doi = e.get("doi")
        raw_title = e.get("title") or ""
        raw_year = str(e.get("year") or "")
        status = "ok"
        notes: list[str] = []
        cr_title = ""
        cr_year = ""
        if not doi:
            status = "no_doi"
            notes.append("No DOI in legacy reference (URL-only / book chapter / missing).")
        else:
            msg = crossref_works(doi)
            time.sleep(0.2)  # polite pacing
            if not msg or msg.get("_error"):
                status = "doi_lookup_failed"
                notes.append(str((msg or {}).get("_error", "empty response")))
            else:
                titles = msg.get("title") or []
                cr_title = titles[0] if titles else ""
                cr_year = str(
                    (msg.get("published-print") or msg.get("published-online") or {})
                    .get("date-parts", [[None]])[0][0]
                    or msg.get("created", {}).get("date-parts", [[None]])[0][0]
                    or ""
                )
                overlap = title_overlap(raw_title, cr_title)
                if overlap < 0.4 and raw_title:
                    status = "metadata_mismatch"
                    notes.append(
                        f"Title overlap={overlap:.2f}: legacy={raw_title!r} vs crossref={cr_title!r}"
                    )
                y_legacy = re.sub(r"[^0-9]", "", raw_year)
                if y_legacy and cr_year and y_legacy != str(cr_year):
                    if status == "ok":
                        status = "year_mismatch"
                    notes.append(f"Year legacy={raw_year} crossref={cr_year}")
        rows.append(
            {
                "key": key,
                "doi": doi,
                "status": status,
                "legacy_title": raw_title,
                "crossref_title": cr_title,
                "legacy_year": raw_year,
                "crossref_year": cr_year,
                "notes": "; ".join(notes),
            }
        )
        print(f"[{i+1}/{len(entries)}] {key}: {status}", flush=True)

    OUT_JSON.write_text(json.dumps(rows, indent=2), encoding="utf-8")

    counts: dict[str, int] = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1

    lines = [
        "# Reference DOI check (Crossref)",
        "",
        f"Source bibliography: `{BIB}`",
        f"Entries: **{len(rows)}**",
        "",
        "## Summary",
        "",
    ]
    for k, v in sorted(counts.items()):
        lines.append(f"- `{k}`: {v}")
    lines.extend(["", "## Flagged entries", ""])
    flagged = [r for r in rows if r["status"] != "ok"]
    if not flagged:
        lines.append("None.")
    else:
        lines.append("| key | status | doi | notes |")
        lines.append("|---|---|---|---|")
        for r in flagged:
            notes = (r["notes"] or "").replace("|", "\\|")
            lines.append(
                f"| `{r['key']}` | {r['status']} | {r['doi'] or ''} | {notes} |"
            )
    lines.extend(["", "## All entries", ""])
    lines.append("| key | status | doi | legacy year | crossref year |")
    lines.append("|---|---|---|---|---|")
    for r in rows:
        lines.append(
            f"| `{r['key']}` | {r['status']} | {r['doi'] or ''} | {r['legacy_year']} | {r['crossref_year']} |"
        )
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    # Mirror beside manuscript for authors working outside the git tree
    mirror = IMR / "manuscript" / "refs_check.md"
    mirror.write_text(OUT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"wrote {OUT_MD}")
    print(f"wrote {mirror}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
