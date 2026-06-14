"""Runtime CLI tests for `remedy overnight run` (Step 1293).

Subprocess tests on tiny jobs. Report-only by default; execution requires explicit
flags AND a clean review verdict. No nested full pytest (repair-propose path is
docs-only, do_continue is exercised at unit level), no shell=True, bounded timeout.
"""
from __future__ import annotations

import json
from uuid import uuid4

import pytest

from tests.cli.runtime_helpers import run_grouped_cli, assert_no_leftover_locks


def _job(data_dir, *, with_failure=False, approved_intent=False):
    from packages.core.models import Artifact, ArtifactKind, Job, RunState, Task
    from packages.orchestration.storage import save_job

    task = Task(description="t")
    arts = []
    if with_failure:
        fa = Artifact(name="tf", content="x", kind=ArtifactKind.VERIFICATION, task_id=task.id,
                      metadata={"test_failure": True, "failure_kind": "test_failed",
                                "related_test_run_id": "tr", "related_apply_id": "ap",
                                "related_task_id": str(task.id), "exit_code": 1,
                                "safe_summary": "fail", "related_files": []})
        arts.append(fa)
    job = Job(id=uuid4(), name="ov-run-cli", user_prompt="x", state=RunState.RUNNING,
              tasks=[task], artifacts=arts,
              permissions={"repo_generated_write": "allow", "repo_test_run": "allow"},
              metadata={"target_repo": "."})
    save_job(job, root=data_dir)
    return str(job.id)


def _review(tmp_path, verdict_body):
    p = tmp_path / "review.md"
    p.write_text(f"# Live Review\n\n## Verdict\n{verdict_body}\n")
    return str(p)


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    # Default clean review so flag-gating (not the review gate) is what's tested.
    monkeypatch.setenv("REMEDY_REVIEW_FILE", _review(tmp_path, "PASS — clean"))
    return d


def test_default_run_is_report_only(env):
    job_id = _job(env)
    r = run_grouped_cli(["overnight", "run", job_id, "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["mode"] == "report_only"
    assert d["executed_action"]["kind"] == "none"
    assert "Traceback" not in r.stdout and "Traceback" not in r.stderr


def test_flag_without_one_cycle_stays_report_only(env):
    job_id = _job(env, with_failure=True)
    r = run_grouped_cli(
        ["overnight", "run", job_id, "--allow-repair-propose", "--json"], env)
    d = json.loads(r.stdout)
    assert d["mode"] == "report_only"
    assert d["executed_action"]["kind"] == "none"


def test_apply_blocked_by_default(env):
    # No approved intent + report-only default → never an apply.
    job_id = _job(env)
    r = run_grouped_cli(["overnight", "run", job_id, "--json"], env)
    d = json.loads(r.stdout)
    assert d["executed_action"]["kind"] == "none"
    assert "do continue" not in d["selected_action"].get("command", "")


def test_repair_propose_executes_with_flag(env):
    job_id = _job(env, with_failure=True)
    r = run_grouped_cli(
        ["overnight", "run", job_id, "--allow-one-cycle", "--allow-repair-propose", "--json"],
        env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["mode"] == "execute_one"
    assert d["executed_action"]["kind"] == "repair_propose"
    assert d["stop_reason"] == "repair_pending_approval"
    assert_no_leftover_locks(env)


def test_pending_review_blocks_execution(env, tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_REVIEW_FILE", _review(tmp_path, "PENDING"))
    job_id = _job(env, with_failure=True)
    r = run_grouped_cli(
        ["overnight", "run", job_id, "--allow-one-cycle", "--allow-repair-propose", "--json"],
        env)
    d = json.loads(r.stdout)
    assert d["executed_action"]["kind"] == "none"
    assert d["stop_reason"] == "review_findings_open"


def test_fail_review_blocks_execution(env, tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_REVIEW_FILE", _review(tmp_path, "FAIL"))
    job_id = _job(env, with_failure=True)
    r = run_grouped_cli(
        ["overnight", "run", job_id, "--allow-one-cycle", "--allow-repair-propose", "--json"],
        env)
    d = json.loads(r.stdout)
    assert d["executed_action"]["kind"] == "none"
    assert d["stop_reason"] == "review_findings_open"


def test_text_output(env):
    job_id = _job(env)
    r = run_grouped_cli(["overnight", "run", job_id], env)
    assert r.returncode == 0, r.stderr
    assert "overnight run:" in r.stdout
    assert "Mode: report_only" in r.stdout


def test_no_daemon_or_watch_flags(env):
    job_id = _job(env)
    for bad in ("--watch", "--daemon", "--schedule", "--repeat", "--background"):
        r = run_grouped_cli(["overnight", "run", job_id, bad], env)
        assert r.returncode != 0  # argparse rejects unknown flags


def test_json_has_no_abs_paths(env):
    job_id = _job(env, with_failure=True)
    r = run_grouped_cli(
        ["overnight", "run", job_id, "--allow-one-cycle", "--allow-repair-propose", "--json"],
        env)
    assert "/home/" not in r.stdout
    assert "Traceback" not in r.stdout and "Traceback" not in r.stderr
