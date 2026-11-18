"""Download layer for World Bank, BACI, CEPII Gravity, WITS, and Hofstede."""

from __future__ import annotations

from typing import Any

from imsfe.config import load_settings
from imsfe.download.baci import fetch_baci
from imsfe.download.cepii_gravity import fetch_cepii_gravity
from imsfe.download.coverage import write_coverage_report
from imsfe.download.hofstede import fetch_hofstede
from imsfe.download.wits import fetch_wits
from imsfe.download.worldbank import fetch_worldbank


def run_download(*, force: bool = False, report_only: bool = False) -> dict[str, Any]:
    """Fetch all sources (unless report_only) and write the coverage report."""
    settings = load_settings()
    status: dict[str, Any] = {}

    if not report_only:
        wb = fetch_worldbank(settings, force=force)
        status["worldbank_wdi"] = {
            "path": wb.get("paths", {}).get("wdi"),
            "error": wb.get("errors", {}).get("wdi"),
        }
        status["worldbank_wgi"] = {
            "path": wb.get("paths", {}).get("wgi"),
            "error": wb.get("errors", {}).get("wgi"),
        }

        for name, fn in [
            ("baci", fetch_baci),
            ("cepii_gravity", fetch_cepii_gravity),
            ("wits", fetch_wits),
        ]:
            try:
                status[name] = fn(settings, force=force)
            except Exception as exc:  # noqa: BLE001 — continue other sources
                status[name] = {"error": str(exc)}

        # Hofstede is required for CULT — fail loudly if the manual CSV is absent.
        try:
            status["hofstede"] = fetch_hofstede(force=force)
        except FileNotFoundError:
            raise
        except Exception as exc:  # noqa: BLE001
            status["hofstede"] = {"error": str(exc)}

    coverage_path = write_coverage_report(settings, status=status)
    return {"status": status, "coverage_path": coverage_path}
