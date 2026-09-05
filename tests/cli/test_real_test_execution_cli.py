"""Runtime CLI tests for Real Test Execution + Snapshot/Rollback Proof v1 (Step 1887/1895).

Subprocess tests. Read result/list/integrity + record snapshot/rollback proofs. No execution of the
real suite here. Safe JSON, safe errors, no tracebacks, honest restore flags.
"""
from __future__ import annotations

import json
from uuid import uuid4

import pytest

from tests.cli.runtime_helpers import run_grouped_cli


def _job(env):
    from packages.core.models import Job, RunState, Task
    from packages.orchestration.storage import save_job
    repo = env / f"repo-{uuid4().hex[:6]}"; repo.mkdir(parents=True); (repo / "a.py").write_text("x=1\n")
    job = Job(id=uuid4(), name="m", user_prompt="x", state=RunState.RUNNING,
              tasks=[Task(description="t")], artifacts=[], metadata={"target_repo": str(repo)})
    save_job(job, root=env)
    return str(job.id)


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    return d


def test_snapshot_create_show(env):
    jid = _job(env)
    r = run_grouped_cli(["snapshot", "create", jid, "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["restore_available"] is False and "Traceback" not in r.stdout
    r2 = run_grouped_cli(["snapshot", "show", d["snapshot_id"], "--json"], env)
    assert json.loads(r2.stdout)["snapshot_id"] == d["snapshot_id"]


def test_rollback_proof_honest(env):
    jid = _job(env)
    sid = json.loads(run_grouped_cli(["snapshot", "create", jid, "--json"], env).stdout)["snapshot_id"]
    r = run_grouped_cli(["rollback", "proof", jid, "--snapshot-id", sid, "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["restore_available"] is False and d["restore_tested"] is False
    assert d["limitations"]
    r2 = run_grouped_cli(["rollback", "show", d["rollback_proof_id"], "--json"], env)
    assert json.loads(r2.stdout)["rollback_proof_id"] == d["rollback_proof_id"]


def test_test_list_empty(env):
    jid = _job(env)
    r = run_grouped_cli(["test", "list", jid, "--json"], env)
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout)["run_count"] == 0


def test_test_list_empty_text_message(env):
    jid = _job(env)
    r = run_grouped_cli(["test", "list", jid], env)
    assert r.returncode == 0, r.stderr
    assert f"No test runs for {jid[:8]}." in r.stdout


def test_test_list_text_shows_per_row(capsys):
    from argparse import Namespace
    from unittest.mock import patch

    from apps.cli.commands.real_test_execution_cmd import _cmd_test_list

    job_id = str(uuid4())
    fake_runs = [{"test_run_id": "run-1", "status": "passed", "exit_code": 0,
                  "created_at": "2026-09-04T00:00:00+00:00"}]
    args = Namespace(job_id=job_id, json=False)
    with patch("packages.orchestration.real_test_execution.list_test_runs", return_value=fake_runs):
        _cmd_test_list(args)

    out = capsys.readouterr().out
    assert "run-1" in out
    assert "status=passed" in out
    assert "exit=0" in out
    assert "created=2026-09-04T00:00:00+00:00" in out


def test_test_integrity(env):
    jid = _job(env)
    run_grouped_cli(["snapshot", "create", jid, "--json"], env)
    r = run_grouped_cli(["test", "integrity", "--json"], env)
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout)["passed"] is True


def test_invalid_ids(env):
    r1 = run_grouped_cli(["test", "result", "nope", "--json"], env)
    assert r1.returncode == 1 and "Traceback" not in r1.stderr
    r2 = run_grouped_cli(["snapshot", "show", "nope", "--json"], env)
    assert r2.returncode == 1
    r3 = run_grouped_cli(["rollback", "show", "nope", "--json"], env)
    assert r3.returncode == 1


def test_json_purity(env):
    jid = _job(env)
    r = run_grouped_cli(["snapshot", "create", jid, "--json"], env)
    blob = r.stdout.lower()
    for marker in ("sk-ant", "/home/", "/users/", "traceback"):
        assert marker not in blob, marker
