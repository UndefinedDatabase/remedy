"""Runtime CLI tests for `remedy overnight` (Step 1264).

Subprocess tests on tiny jobs. Read-only: no mutation, no shell=True, no nested
pytest, bounded timeout.
"""
from __future__ import annotations

import json
from uuid import uuid4

import pytest

from tests.cli.runtime_helpers import run_grouped_cli


def _job(data_dir, *, with_failure=False, pending_repair=False):
    from packages.core.models import Artifact, ArtifactKind, Job, RunState, Task
    from packages.orchestration.storage import save_job

    task = Task(description="t")
    arts = []
    fa_id = ""
    if with_failure or pending_repair:
        fa = Artifact(name="tf", content="x", kind=ArtifactKind.VERIFICATION, task_id=task.id,
                      metadata={"test_failure": True, "failure_kind": "test_failed",
                                "related_test_run_id": "tr", "related_apply_id": "ap",
                                "related_task_id": str(task.id), "exit_code": 1,
                                "safe_summary": "fail", "related_files": []})
        arts.append(fa); fa_id = str(fa.id)
    job = Job(id=uuid4(), name="ov-cli", user_prompt="x", state=RunState.RUNNING,
              tasks=[task], artifacts=arts,
              permissions={"repo_generated_write": "allow", "repo_test_run": "allow"},
              metadata={"target_repo": "."})
    if pending_repair:
        from packages.orchestration import repair_loop as RL
        att = RL.RepairAttempt(attempt_id="a1", job_id=str(job.id), failure_artifact_id=fa_id,
                               repair_intent_id="ri-1", status="approval_required",
                               source="cli_v1", created_at="t")
        job.metadata.setdefault("repair_attempts_v1", {})[f"{fa_id}::cli_v1"] = att.to_dict()
    save_job(job, root=data_dir)
    return str(job.id), fa_id


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    return d


def test_readiness_missing_job(env):
    r = run_grouped_cli(["overnight", "readiness", str(uuid4()), "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["ready"] is False
    assert "job_not_found" in d["blockers"]
    assert "Traceback" not in r.stdout and "Traceback" not in r.stderr


def test_readiness_empty_job(env):
    job_id, _ = _job(env)
    r = run_grouped_cli(["overnight", "readiness", job_id, "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["can_run_unattended"] is False  # default policy report-only
    assert d["next_action"]["command"].startswith("remedy ")


def test_readiness_text(env):
    job_id, _ = _job(env)
    r = run_grouped_cli(["overnight", "readiness", job_id], env)
    assert r.returncode == 0, r.stderr
    assert "Overnight readiness" in r.stdout


def test_plan_json(env):
    job_id, _ = _job(env)
    r = run_grouped_cli(["overnight", "plan", job_id, "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["would_run"] is False


def test_report_markdown(env):
    job_id, _ = _job(env, with_failure=True)
    r = run_grouped_cli(["overnight", "report", job_id, "--markdown"], env)
    assert r.returncode == 0, r.stderr
    assert "# Overnight Report" in r.stdout
    assert "/home/" not in r.stdout and "Traceback" not in r.stdout


def test_pending_repair_blocks(env):
    job_id, _ = _job(env, pending_repair=True)
    r = run_grouped_cli(["overnight", "readiness", job_id, "--json"], env)
    d = json.loads(r.stdout)
    assert "repair_pending_approval" in d["blockers"]
    assert d["next_action"]["command"] == f"remedy patch approve {job_id} ri-1"


def test_report_json(env):
    job_id, _ = _job(env)
    r = run_grouped_cli(["overnight", "report", job_id, "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert "report" in d and "completed_checklist" in d["report"]
