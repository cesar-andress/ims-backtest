"""Shared HTTP download helpers with streaming and clear failures."""

from __future__ import annotations

from pathlib import Path

import requests


def download_file(
    url: str,
    dest: Path,
    *,
    timeout: int = 120,
    chunk_size: int = 1024 * 1024,
    session: requests.Session | None = None,
) -> Path:
    """Stream a URL to ``dest``. Raises on non-200 responses."""
    if not url:
        raise ValueError("Download URL is empty; set it in config/settings.yaml")
    dest.parent.mkdir(parents=True, exist_ok=True)
    sess = session or requests.Session()
    if session is None:
        sess.trust_env = False
    with sess.get(url, stream=True, timeout=timeout) as resp:
        if resp.status_code != 200:
            raise RuntimeError(
                f"Download failed for {url!r}: HTTP {resp.status_code}. "
                "Place the file manually under data/manual/ and re-run."
            )
        tmp = dest.with_suffix(dest.suffix + ".partial")
        with tmp.open("wb") as fh:
            for chunk in resp.iter_content(chunk_size=chunk_size):
                if chunk:
                    fh.write(chunk)
        tmp.replace(dest)
    return dest
