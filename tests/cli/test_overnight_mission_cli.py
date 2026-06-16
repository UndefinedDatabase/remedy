"""Runtime CLI tests for `remedy overnight` mission-contract commands (Step 1850/1854).

Subprocess tests. METADATA + EVALUATION only — no execution. Safe JSON, safe errors, no tracebacks.
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


def _create(env, job="job-1", *, acceptance="tests pass"):
    args = ["overnight", "contract-create", job, "--user-goal", "Fix it", "--json"]
    if acceptance:
        args[5:5] = ["--acceptance", acceptance]
    r = run_grouped_cli(args, env)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)["contract_id"]


def test_create_and_show(env):
    cid = _create(env)
    r = run_grouped_cli(["overnight", "contract-show", cid, "--json"], env)
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout)["contract_id"] == cid
    assert "Traceback" not in r.stdout


def test_create_without_acceptance_then_evaluate(env):
    cid = _create(env, job="job-2", acceptance="")
    r = run_grouped_cli(["overnight", "evaluate", cid, "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["status"] == "needs_user_acceptance_criteria"
    assert d["satisfied"] is False


def test_next_action(env):
    cid = _create(env, job="job-3")
    r = run_grouped_cli(["overnight", "next-action", cid, "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    for a in d["next_safe_actions"]:
        assert a.startswith("remedy ") and " run" not in a
    assert "Traceback" not in r.stdout


def test_cycles_empty(env):
    cid = _create(env, job="job-4")
    r = run_grouped_cli(["overnight", "cycles", cid, "--json"], env)
    assert json.loads(r.stdout)["cycle_count"] == 0


def test_contract_readiness_honest(env):
    r = run_grouped_cli(["overnight", "contract-readiness", "job-5", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["full_overnight_autonomy"] is False
    assert d["worker_execution_available"] is False


def test_integrity(env):
    _create(env, job="job-6")
    r = run_grouped_cli(["overnight", "integrity", "--json"], env)
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout)["passed"] is True


def test_show_invalid_id(env):
    r = run_grouped_cli(["overnight", "contract-show", "nope", "--json"], env)
    assert r.returncode == 1
    assert "Traceback" not in r.stderr and "Traceback" not in r.stdout


def test_json_purity(env):
    cid = _create(env, job="job-7")
    r = run_grouped_cli(["overnight", "evaluate", cid, "--json"], env)
    blob = r.stdout.lower()
    for marker in ("sk-ant", "/home/", "/users/", "traceback"):
        assert marker not in blob, marker
