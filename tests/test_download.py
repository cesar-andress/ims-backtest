"""Unit tests for the download layer (mocked HTTP; no network)."""

from __future__ import annotations

import io
import zipfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from imsfe.config import load_settings
from imsfe.download import baci as baci_mod
from imsfe.download import cepii_gravity as gravity_mod
from imsfe.download import hofstede as hofstede_mod
from imsfe.download import wits as wits_mod
from imsfe.download.coverage import write_coverage_report
from imsfe.download.http_util import download_file
from imsfe.io import raw_dir, record_artifact, should_skip


@pytest.fixture()
def isolated_raw(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point project raw/manual/outputs at a temporary tree."""
    root = tmp_path / "proj"
    (root / "config").mkdir(parents=True)
    # Reuse real YAML configs by symlink/copy is heavy; monkeypatch paths instead.
    monkeypatch.setattr("imsfe.io.project_root", lambda: root)
    monkeypatch.setattr("imsfe.config.project_root", lambda: root)
    (root / "data" / "raw").mkdir(parents=True)
    (root / "data" / "manual" / "baci").mkdir(parents=True)
    (root / "data" / "manual" / "cepii_gravity").mkdir(parents=True)
    (root / "data" / "manual" / "wits").mkdir(parents=True)
    (root / "data" / "manual" / "hofstede").mkdir(parents=True)
    (root / "outputs" / "logs").mkdir(parents=True)
    # Copy settings into temp config so load_settings works if called with default.
    import shutil

    real_root = Path(__file__).resolve().parents[1]
    shutil.copy(real_root / "config" / "settings.yaml", root / "config" / "settings.yaml")
    shutil.copy(real_root / "config" / "variables.yaml", root / "config" / "variables.yaml")
    shutil.copy(real_root / "config" / "experiments.yaml", root / "config" / "experiments.yaml")
    return root


def test_download_file_streams(tmp_path: Path) -> None:
    dest = tmp_path / "f.bin"
    content = b"abc123"

    class FakeResp:
        status_code = 200

        def iter_content(self, chunk_size: int = 1):
            yield content

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    session = MagicMock()
    session.get.return_value = FakeResp()
    download_file("https://example.test/file", dest, session=session)
    assert dest.read_bytes() == content


def test_download_file_rejects_http_error(tmp_path: Path) -> None:
    class FakeResp:
        status_code = 404

        def iter_content(self, chunk_size: int = 1):
            yield b""

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    session = MagicMock()
    session.get.return_value = FakeResp()
    with pytest.raises(RuntimeError, match="HTTP 404"):
        download_file("https://example.test/missing", tmp_path / "x", session=session)


def test_should_skip_idempotent(isolated_raw: Path) -> None:
    path = raw_dir() / "demo.parquet"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"data")
    record_artifact(
        "demo",
        url="https://example.test",
        version="v1",
        relative_paths=["demo.parquet"],
        sha256="abc",
    )
    assert should_skip("demo", "v1", ["demo.parquet"], force=False) is True
    assert should_skip("demo", "v1", ["demo.parquet"], force=True) is False
    assert should_skip("demo", "v2", ["demo.parquet"], force=False) is False


def test_baci_convert_filters_chapters(isolated_raw: Path) -> None:
    settings = load_settings()
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr(
            "country_codes_V202601.csv",
            "country_code,country_name,country_iso3\n1,Test,TST\n",
        )
        zf.writestr(
            "product_codes_V202601.csv",
            "code,description\n640110,boots\n010121,horses\n",
        )
        # Include in-range and out-of-range years; chapter 64 vs 01.
        zf.writestr(
            "BACI_HS12_Y2020_V202601.csv",
            "t,i,j,k,v,q\n2020,1,2,640110,10,1\n2020,1,2,010121,9,1\n",
        )
        zf.writestr(
            "BACI_HS12_Y2000_V202601.csv",
            "t,i,j,k,v,q\n2000,1,2,640110,10,1\n",
        )
    zip_path = raw_dir() / "baci" / "baci_download.zip"
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    zip_path.write_bytes(buf.getvalue())

    converted = baci_mod.convert_baci_zip(zip_path, settings)
    part = Path(converted["trade_dir"]) / "year=2020" / "part.parquet"
    assert part.is_file()
    df = pd.read_parquet(part)
    assert set(df["k"].str[:2]) == {"64"}
    assert not (Path(converted["trade_dir"]) / "year=2000").exists()


def test_gravity_convert_keeps_columns(isolated_raw: Path) -> None:
    settings = load_settings()
    csv = (
        "iso3_o,iso3_d,year,distw_harmonic,distw,contig,comlang_off,fta_wto\n"
        "COL,USA,2020,5000,5100,0,0,1\n"
        "COL,USA,2000,5000,5100,0,0,0\n"
    )
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("Gravity_V202211.csv", csv)
    archive = raw_dir() / "cepii_gravity" / "gravity_download.zip"
    archive.parent.mkdir(parents=True, exist_ok=True)
    archive.write_bytes(buf.getvalue())
    out = gravity_mod.convert_gravity(archive, settings)
    df = pd.read_parquet(out)
    assert list(df.columns) == [
        "iso3_o",
        "iso3_d",
        "year",
        "distw_harmonic",
        "distw",
        "contig",
        "comlang_off",
        "fta_wto",
    ]
    assert set(df["year"]) == {2020}


def test_wits_manual_loader(isolated_raw: Path) -> None:
    path = isolated_raw / "data" / "manual" / "wits" / "sample.csv"
    path.write_text(
        "reporter_iso3,partner_iso3,year,hs_chapter,ahs_simple_avg\n"
        "USA,COL,2020,64,0.0\n",
        encoding="utf-8",
    )
    df = wits_mod.load_manual_wits_csvs([path])
    assert len(df) == 1
    assert df.iloc[0]["ahs_simple_avg"] == 0.0


def test_hofstede_manual_loader(isolated_raw: Path) -> None:
    path = isolated_raw / "data" / "manual" / "hofstede" / "hofstede.csv"
    path.write_text(
        "iso3,pdi,idv,mas,uai,ltowvs,ivr\n"
        "COL,67,13,64,80,13,83\n",
        encoding="utf-8",
    )
    df = hofstede_mod.load_hofstede_csv(path)
    assert df.loc[0, "iso3"] == "COL"
    assert df.loc[0, "pdi"] == 67


def test_hofstede_refuses_without_file(isolated_raw: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Hofstede"):
        hofstede_mod.fetch_hofstede(force=True)


def test_worldbank_fetch_mocked(isolated_raw: Path) -> None:
    settings = load_settings()

    def fake_fetch(series, economy, time=None, skipBlanks=True):
        years = [time] if isinstance(time, int) else list(time)
        for year in years:
            yield {
                "economy": "USA",
                "series": series,
                "time": year,
                "value": 1.0,
            }

    with patch("imsfe.download.worldbank.wb") as mock_wb:
        mock_wb.db = 2
        mock_wb.series.get.return_value = {"id": "x"}
        mock_wb.data.fetch.side_effect = fake_fetch
        mock_wb.series.list.return_value = [
            {"id": sid}
            for sid in [
                "GOV_WGI_VA.EST",
                "GOV_WGI_PV.EST",
                "GOV_WGI_GE.EST",
                "GOV_WGI_RQ.EST",
                "GOV_WGI_RL.EST",
                "GOV_WGI_CC.EST",
            ]
        ]
        from imsfe.download import worldbank as wb_mod

        path = wb_mod.fetch_wdi(settings, force=True)
        assert path.is_file()
        df = pd.read_parquet(path)
        assert set(df.columns) == {"iso3", "year", "indicator", "value"}
        assert not df.empty

        wgi_path = wb_mod.fetch_wgi(settings, force=True)
        wgi = pd.read_parquet(wgi_path)
        assert set(wgi["indicator"]).issubset(
            {"VA.EST", "PV.EST", "GE.EST", "RQ.EST", "RL.EST", "CC.EST"}
        )


def test_coverage_report_writes(isolated_raw: Path) -> None:
    path = write_coverage_report(load_settings(), status={"baci": {"error": "boom"}})
    text = path.read_text(encoding="utf-8")
    assert "Data download coverage" in text
    assert "boom" in text
