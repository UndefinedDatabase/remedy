"""Runtime CLI tests for `remedy tournament` — Model/Route Tournament Harness v0 (Step 1806/1814).

Subprocess tests. EVIDENCE + REPORTING only — no execution. Safe JSON, safe errors, no tracebacks,
no raw evidence.
"""
from __future__ import annotations

import json

import pytest

from tests.cli.runtime_helpers import run_grouped_cli


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    return d


def test_report_no_evidence_no_winner(env):
    r = run_grouped_cli(["tournament", "report", "job-1", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["status"] == "insufficient_evidence"
    assert d["winner_competitor_id"] == ""
    assert "Traceback" not in r.stdout


def test_report_then_list_show(env):
    r = run_grouped_cli(["tournament", "report", "job-2", "--json"], env)
    tid = json.loads(r.stdout)["tournament_id"]
    r2 = run_grouped_cli(["tournament", "list", "job-2", "--json"], env)
    assert json.loads(r2.stdout)["report_count"] == 1
    r3 = run_grouped_cli(["tournament", "show", tid, "--json"], env)
    assert json.loads(r3.stdout)["tournament_id"] == tid


def test_show_invalid_id(env):
    r = run_grouped_cli(["tournament", "show", "nope", "--json"], env)
    assert r.returncode == 1
    assert "Traceback" not in r.stderr and "Traceback" not in r.stdout


def test_integrity(env):
    run_grouped_cli(["tournament", "report", "job-3", "--json"], env)
    r = run_grouped_cli(["tournament", "integrity", "--json"], env)
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout)["passed"] is True


def test_report_task_type(env):
    r = run_grouped_cli(["tournament", "report", "job-4", "--task-type", "repair", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["task_type"] == "repair"
    for a in d.get("next_safe_actions", []):
        assert a.startswith("remedy ") and " run" not in a


def test_json_purity(env):
    r = run_grouped_cli(["tournament", "report", "job-5", "--json"], env)
    blob = r.stdout.lower()
    for marker in ("sk-ant", "/home/", "/users/", "api_key", "traceback"):
        assert marker not in blob, marker


def test_list_json_has_created_at(env):
    run_grouped_cli(["tournament", "report", "job-6", "--json"], env)
    r = run_grouped_cli(["tournament", "list", "job-6", "--json"], env)
    d = json.loads(r.stdout)
    assert d["reports"][0]["created_at"]


def test_list_text_shows_per_row(env):
    r = run_grouped_cli(["tournament", "report", "job-7", "--json"], env)
    tid = json.loads(r.stdout)["tournament_id"]
    r2 = run_grouped_cli(["tournament", "list", "job-7"], env)
    assert r2.returncode == 0
    assert tid in r2.stdout
    assert "created=" in r2.stdout


def test_limit_caps_the_report_count(env):
    run_grouped_cli(["tournament", "report", "job-8", "--json"], env)
    run_grouped_cli(["tournament", "report", "job-8", "--json"], env)
    run_grouped_cli(["tournament", "report", "job-8", "--json"], env)
    r = run_grouped_cli(["tournament", "list", "job-8", "--json", "--limit", "2"], env)
    d = json.loads(r.stdout)
    assert d["report_count"] == 2


def test_unknown_sort_field_exits_nonzero(env):
    run_grouped_cli(["tournament", "report", "job-9", "--json"], env)
    r = run_grouped_cli(["tournament", "list", "job-9", "--sort", "bogus"], env)
    assert r.returncode == 1
    assert "created_at" in r.stderr
