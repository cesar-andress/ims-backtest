"""Anti-leakage tests: features at year t must ignore data with year > t."""

from __future__ import annotations

import numpy as np
import pandas as pd

from imsfe.build.features import cagr_3y, compute_features, interpolate_lpi
from imsfe.build.outcomes import add_outcomes
from imsfe.config import load_settings, load_variables


def _toy_flows() -> pd.DataFrame:
    """Minimal chapter flows spanning 2015–2020 for two exporters/importers."""
    rows = []
    # Destination USA imports from CHN/VNM/COL; COL exports to USA/DEU
    for year in range(2015, 2021):
        rows.append(
            {
                "year": year,
                "iso3_o": "CHN",
                "iso3_d": "USA",
                "value_usd": 1000.0 * (year - 2010),
                "qty_tons": 10.0,
                "hs_chapter": "64",
            }
        )
        rows.append(
            {
                "year": year,
                "iso3_o": "VNM",
                "iso3_d": "USA",
                "value_usd": 500.0 * (year - 2010),
                "qty_tons": 5.0,
                "hs_chapter": "64",
            }
        )
        rows.append(
            {
                "year": year,
                "iso3_o": "COL",
                "iso3_d": "USA",
                "value_usd": 200.0 * (year - 2010),
                "qty_tons": 2.0,
                "hs_chapter": "64",
            }
        )
        rows.append(
            {
                "year": year,
                "iso3_o": "COL",
                "iso3_d": "DEU",
                "value_usd": 50.0 * (year - 2010),
                "qty_tons": 1.0,
                "hs_chapter": "64",
            }
        )
        # USA re-exports (hub-ish)
        rows.append(
            {
                "year": year,
                "iso3_o": "USA",
                "iso3_d": "CAN",
                "value_usd": 100.0,
                "qty_tons": 1.0,
                "hs_chapter": "64",
            }
        )
    return pd.DataFrame.from_records(rows)


def _toy_panel() -> pd.DataFrame:
    rows = []
    for year in range(2015, 2021):
        for dest in ("USA", "DEU"):
            rows.append(
                {
                    "iso3_o": "COL",
                    "iso3_d": dest,
                    "year": year,
                    "hs_chapter": "64",
                    "X_ijt": 200.0 * (year - 2010) if dest == "USA" else 50.0 * (year - 2010),
                    "Q_ijt": 2.0 if dest == "USA" else 1.0,
                }
            )
    return pd.DataFrame.from_records(rows)


def _toy_wdi() -> pd.DataFrame:
    rows = []
    for iso in ("USA", "DEU", "COL"):
        for year in range(2015, 2021):
            row = {
                "iso3": iso,
                "year": year,
                "SP.POP.TOTL": 300e6 if iso == "USA" else 80e6,
                "NY.GDP.PCAP.PP.KD": 50_000.0,
                "FP.CPI.TOTL.ZG": 2.5,
                "SL.UEM.TOTL.ZS": 5.0,
                "NE.TRD.GNFS.ZS": 30.0,
                "LP.LPI.OVRL.XQ": np.nan,
            }
            # LPI editions only in 2016 and 2018
            if year in (2016, 2018):
                row["LP.LPI.OVRL.XQ"] = 3.5 if year == 2016 else 3.9
            rows.append(row)
    return pd.DataFrame.from_records(rows)


def _toy_wgi() -> pd.DataFrame:
    rows = []
    for iso in ("USA", "DEU"):
        for year in range(2015, 2021):
            rows.append({"iso3": iso, "year": year, "GOV_raw": 1.2})
    return pd.DataFrame.from_records(rows)


def _toy_gravity() -> pd.DataFrame:
    rows = []
    for year in range(2015, 2021):
        for dest in ("USA", "DEU"):
            rows.append(
                {
                    "iso3_o": "COL",
                    "iso3_d": dest,
                    "year": year,
                    "distw_harmonic": 4000.0 if dest == "USA" else 9000.0,
                    "comlang_off": 0.0,
                    "fta_wto": 1.0 if year >= 2018 and dest == "USA" else 0.0,
                }
            )
    return pd.DataFrame.from_records(rows)


def test_cagr_uses_only_lag() -> None:
    s = pd.Series({2015: 100.0, 2016: 110.0, 2017: 120.0, 2018: 130.0})
    g = cagr_3y(s)
    assert pd.isna(g.loc[2015])
    assert pd.isna(g.loc[2017])
    assert abs(g.loc[2018] - ((130 / 100) ** (1 / 3) - 1)) < 1e-9


def test_lpi_interpolation_flag() -> None:
    s = pd.Series({2016: 3.0, 2017: np.nan, 2018: 5.0})
    interp, imputed = interpolate_lpi(s)
    assert abs(interp.loc[2017] - 4.0) < 1e-9
    assert bool(imputed.loc[2017]) is True
    assert bool(imputed.loc[2016]) is False


def test_features_invariant_to_future_perturbation() -> None:
    settings = load_settings()
    # Shrink years so toy data covers the range used in compute_features LPI loop
    settings = settings.model_copy(
        update={"years": settings.years.model_copy(update={"start": 2015, "end": 2020})}
    )
    variables = load_variables()
    flows = _toy_flows()
    panel = _toy_panel()
    wdi = _toy_wdi()
    base = compute_features(
        panel,
        flows,
        settings,
        variables,
        wdi=wdi,
        wgi=_toy_wgi(),
        gravity=_toy_gravity(),
        hofstede=pd.DataFrame(columns=["iso3", "pdi", "idv", "mas", "uai", "ltowvs", "ivr"]),
        wits=pd.DataFrame(
            columns=["reporter_iso3", "partner_iso3", "year", "hs_chapter", "ahs_simple_avg"]
        ),
    )

    # Perturb all years > 2017 in every source
    flows_p = flows.copy()
    flows_p.loc[flows_p["year"] > 2017, "value_usd"] *= 10.0
    flows_p.loc[flows_p["year"] > 2017, "qty_tons"] *= 10.0
    wdi_p = wdi.copy()
    for col in wdi_p.columns:
        if col in ("iso3", "year"):
            continue
        wdi_p.loc[wdi_p["year"] > 2017, col] = wdi_p.loc[wdi_p["year"] > 2017, col] * 10.0
    grav_p = _toy_gravity()
    grav_p.loc[grav_p["year"] > 2017, "distw_harmonic"] = 1.0
    grav_p.loc[grav_p["year"] > 2017, "fta_wto"] = 1.0

    pert = compute_features(
        panel,
        flows_p,
        settings,
        variables,
        wdi=wdi_p,
        wgi=_toy_wgi(),
        gravity=grav_p,
        hofstede=pd.DataFrame(columns=["iso3", "pdi", "idv", "mas", "uai", "ltowvs", "ivr"]),
        wits=pd.DataFrame(
            columns=["reporter_iso3", "partner_iso3", "year", "hs_chapter", "ahs_simple_avg"]
        ),
    )

    feature_cols = [
        c
        for c in base.columns
        if c.endswith("_raw") or c in {v.id for v in variables.variables} or c == "lpi_imputed"
    ]
    left = base.loc[base["year"] == 2017, feature_cols].reset_index(drop=True)
    right = pert.loc[pert["year"] == 2017, feature_cols].reset_index(drop=True)
    pd.testing.assert_frame_equal(left, right, check_dtype=False, rtol=1e-9, atol=1e-9)

    # And features at 2018 must change for at least one market variable
    assert not np.allclose(
        base.loc[base["year"] == 2018, "IMPV_raw"].to_numpy(dtype=float),
        pert.loc[pert["year"] == 2018, "IMPV_raw"].to_numpy(dtype=float),
        equal_nan=True,
    )


def test_outcomes_use_future_by_design() -> None:
    """Outcomes intentionally look ahead; ensure formula matches SPEC."""
    settings = load_settings()
    panel = _toy_panel()
    out = add_outcomes(panel, settings, threshold=1000.0, horizons=[1])
    row = out.loc[(out.iso3_o == "COL") & (out.iso3_d == "USA") & (out.year == 2017)].iloc[0]
    # X_2017 = 200*7 = 1400 > 1000; X_2018 = 1600
    expected = np.log(1600 + 1) - np.log(1400 + 1)
    assert abs(row["y_int_k1"] - expected) < 1e-9
    assert row["y_level_k1"] == 1600.0
