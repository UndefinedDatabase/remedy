"""`remedy stats valuations` and `remedy stats recompute-costs` through the real command line, and
F158's end-to-end path (DECISION F158 D7): calls in a project's ledger, a catalog imported with its
shown difference, the calls revalued, and the raw `calls` rows unchanged throughout."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from packages.orchestration.model_aliases import builtin_model_ids
from packages.orchestration.price_catalog import PRICE_CATALOG_DIR
from packages.orchestration.token_ledger import (
    COST_BASIS_PROVIDER_REPORTED,
    CallRecord,
    open_ledger,
    record_call,
    token_ledger_path_for,
)

REPO = Path(__file__).resolve().parents[2]
MODEL = builtin_model_ids()[0]


def _catalog(version: int, valid_from: str) -> str:
    return f"""[catalog]
adapter = "claude-cli"
pricing_version = {version}

[models."{MODEL}"]
input_per_million = 3.0
output_per_million = 15.0
cache_read_per_million = 0.3
cache_write_per_million = 3.75
currency = "usd"
valid_from = {valid_from}
source = "the operator's maintained catalog"
"""


@pytest.fixture
def data_root(tmp_path, monkeypatch) -> Path:
    root = tmp_path / "remedy_data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


@pytest.fixture
def project_id(data_root) -> str:
    from packages.orchestration.project_registry import RemyProject, save_project

    project = RemyProject(name="F158 Valuations", slug="f158-valuations")
    save_project(project)
    return str(project.id)


@pytest.fixture
def ledger(project_id, tmp_path) -> Path:
    path = token_ledger_path_for(project_id)
    assert tmp_path in path.parents, "the test would have written the real data root"
    common = dict(model=MODEL, ts_utc="2026-10-24T09:00:00+00:00", job_id="job-f158",
                  tokens_in=1000, tokens_out=500, cache_read=0, cache_write=0)
    assert record_call(CallRecord(call_id="job-f158:T001", task_id="T001", cost_usd=0.02,
                                  cost_basis=COST_BASIS_PROVIDER_REPORTED, **common), path=path)
    assert record_call(CallRecord(call_id="job-f158:T002", task_id="T002", **common), path=path)
    return path


@pytest.fixture
def catalogs(tmp_path) -> Path:
    folder = tmp_path / "catalogs"
    folder.mkdir()
    shutil.copyfile(PRICE_CATALOG_DIR / "claude-cli.toml", folder / "claude-cli.toml")
    return folder


def _remedy(*args: str, **extra_env: str) -> subprocess.CompletedProcess:
    env = {**os.environ, "PYTHONPATH": str(REPO), **extra_env}
    return subprocess.run([sys.executable, "-m", "apps.cli.grouped", *args], capture_output=True,
                          text=True, timeout=60, cwd=REPO, env=env)


def _json(*args: str) -> dict:
    r = _remedy(*args, "--json")
    assert r.returncode == 0, r.stdout + r.stderr
    return json.loads(r.stdout)


def _calls_digest(path: Path) -> str:
    conn = open_ledger(path)
    try:
        rows = conn.execute("SELECT * FROM calls ORDER BY call_id").fetchall()
    finally:
        conn.close()
    return hashlib.sha256(repr(rows).encode()).hexdigest()


@pytest.mark.subprocess
class TestTheEndToEndPath:
    def test_import_recompute_and_read_with_the_raw_rows_unchanged(
            self, project_id, ledger, catalogs, tmp_path) -> None:
        raw = _calls_digest(ledger)

        first = _json("stats", "recompute-costs", "--project", project_id, "--catalog-dir", str(catalogs))
        assert (first["examined"], first["revalued"], first["unchanged"]) == (2, 2, 0)
        before = _json("stats", "valuations", "--project", project_id, "--catalog-dir", str(catalogs))
        assert before["bases"] == [
            {"basis": "provider_reported", "calls": 1, "normalized_cost": 0.02},
            {"basis": "unknown", "calls": 1, "normalized_cost": None}]

        imported = tmp_path / "imported.toml"
        imported.write_text(_catalog(2, "2026-10-01"), encoding="utf-8")
        shown = _remedy("worker", "pricing-update", str(imported), "--catalog-dir", str(catalogs))
        assert shown.returncode == 0 and "Nothing was written" in shown.stdout
        written = _remedy("worker", "pricing-update", str(imported), "--catalog-dir", str(catalogs), "--yes")
        assert written.returncode == 0 and "stats recompute-costs" in written.stdout

        second = _json("stats", "recompute-costs", "--project", project_id, "--catalog-dir", str(catalogs))
        assert (second["examined"], second["revalued"], second["unchanged"]) == (2, 2, 0)
        third = _json("stats", "recompute-costs", "--project", project_id, "--catalog-dir", str(catalogs))
        assert (third["revalued"], third["unchanged"]) == (0, 2)

        after = _json("stats", "valuations", "--project", project_id, "--catalog-dir", str(catalogs))
        assert after["currency"] == "usd"
        assert after["bases"] == [
            {"basis": "provider_reported", "calls": 1, "normalized_cost": 0.02},
            {"basis": "price_table", "calls": 1, "normalized_cost": 0.0105}]
        assert after["flagged"] == [{"call_id": "job-f158:T001", "model": MODEL, "normalized_cost": 0.02,
                                     "catalog_cost": 0.0105, "deviation_percent": 47.5}]
        assert after["stale"] == []
        assert _calls_digest(ledger) == raw


@pytest.mark.subprocess
class TestTheReadings:
    def test_the_human_reading_names_each_basis_and_warns_on_a_flagged_call(
            self, project_id, ledger, catalogs) -> None:
        (catalogs / "claude-cli.toml").write_text(_catalog(2, "2026-10-01"), encoding="utf-8")
        assert _remedy("stats", "recompute-costs", "--project", project_id,
                       "--catalog-dir", str(catalogs)).returncode == 0
        r = _remedy("stats", "valuations", "--project", project_id, "--catalog-dir", str(catalogs))
        assert r.returncode == 0, r.stderr
        lines = r.stdout.splitlines()
        assert any(line.split()[:3] == ["provider_reported", "1", "call(s)"] for line in lines)
        assert any(line.split()[:3] == ["price_table", "1", "call(s)"] for line in lines)
        assert "warning: cross-check: call job-f158:T001" in r.stdout
        assert "47.5 percent apart" in r.stdout

    def test_a_stale_catalog_price_is_warned_about_and_nothing_fails(
            self, project_id, ledger, catalogs) -> None:
        (catalogs / "claude-cli.toml").write_text(_catalog(2, "2000-01-01"), encoding="utf-8")
        r = _remedy("stats", "valuations", "--project", project_id, "--catalog-dir", str(catalogs))
        assert r.returncode == 0, r.stderr
        assert (f"warning: stale price: the claude-cli catalog's price for {MODEL} is valid from "
                "2000-01-01, more than 60 days ago; it is still used") in r.stdout
        body = _json("stats", "valuations", "--project", project_id, "--catalog-dir", str(catalogs))
        assert body["stale"] == [{"adapter": "claude-cli", "model": MODEL, "valid_from": "2000-01-01"}]
        assert body["stale_window_days"] == 60

    def test_the_configured_stale_window_is_the_one_used(self, project_id, ledger, catalogs) -> None:
        (catalogs / "claude-cli.toml").write_text(_catalog(2, "2000-01-01"), encoding="utf-8")
        r = _remedy("stats", "valuations", "--project", project_id, "--catalog-dir", str(catalogs),
                    "--json", REMEDY_COST_CATALOG_STALE_DAYS="100000")
        body = json.loads(r.stdout)
        assert (body["stale_window_days"], body["stale"]) == (100000, [])

    def test_an_unknown_cost_prints_the_word_and_never_a_zero(self, project_id, ledger, catalogs) -> None:
        assert _remedy("stats", "recompute-costs", "--project", project_id,
                       "--catalog-dir", str(catalogs)).returncode == 0
        r = _remedy("stats", "valuations", "--project", project_id, "--catalog-dir", str(catalogs))
        assert r.returncode == 0, r.stderr
        assert ["unknown", "1", "call(s)", "unknown"] in [line.split() for line in r.stdout.splitlines()]

    def test_an_unvalued_ledger_says_so_rather_than_printing_a_zero(self, project_id, ledger, catalogs) -> None:
        r = _remedy("stats", "valuations", "--project", project_id, "--catalog-dir", str(catalogs))
        assert r.returncode == 0, r.stderr
        assert "no call has been valued yet" in r.stdout

    def test_a_malformed_catalog_folder_is_refused(self, project_id, ledger, tmp_path) -> None:
        folder = tmp_path / "bad"
        folder.mkdir()
        (folder / "claude-cli.toml").write_text("[catalog\n", encoding="utf-8")
        r = _remedy("stats", "recompute-costs", "--project", project_id, "--catalog-dir", str(folder))
        assert r.returncode == 1
        assert "not valid TOML" in r.stdout + r.stderr

    def test_all_projects_is_refused_for_both(self, project_id, ledger) -> None:
        for command in ("valuations", "recompute-costs"):
            assert _remedy("stats", command, "--all-projects").returncode == 2
