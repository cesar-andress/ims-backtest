"""Load explicit expert_mapping.yaml (new criterion → legacy Excel variable(s))."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from imsfe.config import config_dir


@lru_cache(maxsize=1)
def load_expert_mapping(path: str | None = None) -> dict[str, Any]:
    """Return ``{criterion_id: list[legacy_ids] | 'unmapped'}``."""
    p = Path(path) if path else (config_dir() / "expert_mapping.yaml")
    with p.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict) or "criteria" not in data:
        raise ValueError(f"Invalid expert_mapping file: {p}")
    out: dict[str, Any] = {}
    for vid, raw in data["criteria"].items():
        if raw is None or raw == "unmapped":
            out[str(vid)] = "unmapped"
        elif isinstance(raw, str):
            out[str(vid)] = [raw]
        elif isinstance(raw, list):
            out[str(vid)] = [str(x) for x in raw]
        else:
            raise ValueError(f"Bad mapping for {vid}: {raw!r}")
    return out


def unmapped_criteria(mapping: dict[str, Any] | None = None) -> list[str]:
    mapping = mapping or load_expert_mapping()
    return sorted(k for k, v in mapping.items() if v == "unmapped")


def mapped_legacy_ids(criterion: str, mapping: dict[str, Any] | None = None) -> list[str]:
    mapping = mapping or load_expert_mapping()
    raw = mapping.get(criterion, "unmapped")
    if raw == "unmapped":
        return []
    return list(raw)
