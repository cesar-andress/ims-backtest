"""WITS MFN fallback and cross-check against the manual reference CSV."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from imsfe.download import wits as wits_mod

ROOT = Path(__file__).resolve().parents[1]
REF_CSV = ROOT / "data" / "manual" / "wits" / "wits_ahs_dest_origin_chapter.csv"


def test_apply_mfn_fallback_fills_never_preferred() -> None:
    panel = pd.DataFrame(
        {
            "reporter_iso3": ["USA", "USA", "CHN", "CHN"],
            "partner_iso3": ["COL", "COL", "COL", "COL"],
            "hs_chapter": ["64", "64", "64", "64"],
            "year": [2018, 2019, 2018, 2019],
            "ahs_simple_avg": [2.0, np.nan, np.nan, np.nan],
            "tarif_locf": [False, False, False, False],
            "tarif_source": [pd.NA, pd.NA, pd.NA, pd.NA],
        }
    )
    # LOCF first for USA-COL
    panel = wits_mod.apply_locf(panel, enabled=True)
    usa19 = panel.loc[(panel.reporter_iso3 == "USA") & (panel.year == 2019)].iloc[0]
    assert usa19["tarif_source"] == "partner_locf"
    assert usa19["ahs_simple_avg"] == 2.0
    mfn = pd.DataFrame(
        {
            "reporter_iso3": ["USA", "CHN", "CHN"],
            "year": [2019, 2018, 2019],
            "hs_chapter": ["64", "64", "64"],
            "mfn_simple_avg": [10.0, 7.5, 8.0],
        }
    )
    out = wits_mod.apply_mfn_fallback(panel, mfn)
    chn = out.loc[out.reporter_iso3 == "CHN"].sort_values("year")
    assert list(chn["ahs_simple_avg"]) == [7.5, 8.0]
    assert (chn["tarif_source"] == "mfn_no_preference").all()
    # USA 2019 stayed LOCF, not overwritten by MFN
    usa19 = out.loc[(out.reporter_iso3 == "USA") & (out.year == 2019)].iloc[0]
    assert usa19["ahs_simple_avg"] == 2.0
    assert usa19["tarif_source"] == "partner_locf"


@pytest.mark.skipif(not REF_CSV.is_file(), reason="reference WITS CSV not present")
def test_mfn_fallback_crosscheck_reference_csv() -> None:
    """Values flagged mfn_no_preference should match the manual reference AHS."""
    ref = pd.read_csv(REF_CSV)
    ref["hs_chapter"] = ref["hs_chapter"].astype(str).str.zfill(2)
    ref_mfn = ref.loc[
        ref["ahs_source"].astype(str).str.startswith("mfn_no_preference")
    ].copy()
    assert not ref_mfn.empty

    # Simulate pipeline: empty partner-specific → MFN fill from reference MFN column
    panel = ref_mfn[
        ["reporter_iso3", "partner_iso3", "year", "hs_chapter"]
    ].drop_duplicates()
    panel["ahs_simple_avg"] = np.nan
    panel["tarif_locf"] = False
    panel["tarif_source"] = pd.NA
    mfn = (
        ref_mfn.groupby(["reporter_iso3", "year", "hs_chapter"], as_index=False)[
            "mfn_simple_avg"
        ]
        .mean()
    )
    out = wits_mod.apply_mfn_fallback(panel, mfn)
    assert (out["tarif_source"] == "mfn_no_preference").all()

    merged = out.merge(
        ref_mfn[
            [
                "reporter_iso3",
                "partner_iso3",
                "year",
                "hs_chapter",
                "ahs_simple_avg",
            ]
        ].rename(columns={"ahs_simple_avg": "ref_ahs"}),
        on=["reporter_iso3", "partner_iso3", "year", "hs_chapter"],
        how="inner",
    )
    assert len(merged) > 100
    # Allow tiny float noise
    abs_err = (merged["ahs_simple_avg"] - merged["ref_ahs"]).abs()
    assert float(abs_err.median()) < 1e-6
    assert float((abs_err > 0.05).mean()) < 0.01
