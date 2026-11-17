"""I/O helpers for parquet, manifests, and path conventions."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from imsfe.config import project_root


def raw_dir() -> Path:
    """Return data/raw/."""
    path = project_root() / "data" / "raw"
    path.mkdir(parents=True, exist_ok=True)
    return path


def manual_dir() -> Path:
    """Return data/manual/."""
    return project_root() / "data" / "manual"


def outputs_logs_dir() -> Path:
    """Return outputs/logs/."""
    path = project_root() / "outputs" / "logs"
    path.mkdir(parents=True, exist_ok=True)
    return path


def manifest_path() -> Path:
    """Return data/raw/manifest.json."""
    return raw_dir() / "manifest.json"


def load_manifest() -> dict[str, Any]:
    """Load the download manifest, or an empty structure."""
    path = manifest_path()
    if not path.is_file():
        return {"artifacts": {}}
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if "artifacts" not in data:
        data["artifacts"] = {}
    return data


def save_manifest(manifest: dict[str, Any]) -> None:
    """Write manifest.json atomically."""
    path = manifest_path()
    tmp = path.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=True)
        fh.write("\n")
    tmp.replace(path)


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    """Compute SHA-256 of a file."""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        while True:
            chunk = fh.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    """Compute SHA-256 of an in-memory buffer."""
    return hashlib.sha256(data).hexdigest()


def utc_now_iso() -> str:
    """UTC timestamp in ISO-8601."""
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def artifact_exists(relative_paths: list[str]) -> bool:
    """True if every relative path under data/raw exists."""
    base = raw_dir()
    return all((base / rel).exists() for rel in relative_paths)


def should_skip(
    source_id: str,
    version: str,
    relative_paths: list[str],
    *,
    force: bool,
) -> bool:
    """Skip download when the same version is already recorded and files exist."""
    if force:
        return False
    manifest = load_manifest()
    entry = manifest.get("artifacts", {}).get(source_id)
    if not entry:
        return False
    if str(entry.get("version", "")) != str(version):
        return False
    return artifact_exists(relative_paths)


def record_artifact(
    source_id: str,
    *,
    url: str,
    version: str,
    relative_paths: list[str],
    sha256: str,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Upsert one artifact entry in the manifest and return it."""
    manifest = load_manifest()
    entry: dict[str, Any] = {
        "source_id": source_id,
        "url": url,
        "version": version,
        "timestamp": utc_now_iso(),
        "sha256": sha256,
        "paths": relative_paths,
    }
    if extra:
        entry.update(extra)
    manifest.setdefault("artifacts", {})[source_id] = entry
    save_manifest(manifest)
    return entry
