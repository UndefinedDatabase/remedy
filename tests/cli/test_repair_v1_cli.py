"""Runtime CLI tests for `remedy repair propose` / `repair status` (Step 1212).

Subprocess tests on a tiny job. No nested pytest, no shell=True, bounded timeout.
"""
from __future__ import annotations

import json
from uuid import uuid4

import pytest

from tests.cli.runtime_helpers import run_grouped_cli


def _make_job_with_failure(data_dir):
    from packages.core.models import Artifact, ArtifactKind, Job, RunState, Task
    from packages.orchestration.storage import save_job

    task = Task(description="orig")
    fa = Artifact(
        name="test-failure", content="Test test_failed: exit 1",
        kind=ArtifactKind.VERIFICATION, task_id=task.id,
        metadata={
            "test_failure": True, "failure_kind": "test_failed",
            "related_test_run_id": "tr-abc12345", "related_apply_id": "ap-1",
            "related_task_id": str(task.id), "failing_phase": "test",
            "command_safe": "pytest -q", "exit_code": 1,
            "related_files": [], "safe_summary": "Test test_failed: exit 1",
        },
    )
    job = Job(id=uuid4(), name="cli-repair", user_prompt="x", state=RunState.RUNNING,
              tasks=[task], artifacts=[fa],
              permissions={"repo_generated_write": "allow", "repo_test_run": "allow"},
              metadata={"target_repo": "."})
    save_job(job, root=data_dir)
    return str(job.id), str(fa.id)


@pytest.fixture()
def env(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


def test_missing_job(env):
    r = run_grouped_cli(["repair", "propose", str(uuid4()), "fa", "--json"], env)
    data = json.loads(r.stdout)
    assert data["status"] == "blocked"
    assert "Traceback" not in r.stdout and "Traceback" not in r.stderr


def test_missing_failure_artifact(env):
    job_id, _ = _make_job_with_failure(env)
    r = run_grouped_cli(["repair", "propose", job_id, "nope", "--json"], env)
    data = json.loads(r.stdout)
    assert data["status"] == "blocked"


def test_propose_without_fixture_builder(env):
    job_id, fa = _make_job_with_failure(env)
    r = run_grouped_cli(["repair", "propose", job_id, fa, "--json"], env)
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert data["status"] == "fix_task_created"
    assert data["repair_task_id"]
    assert not data["repair_intent_id"]


def test_propose_with_fixture_builder(env):
    job_id, fa = _make_job_with_failure(env)
    r = run_grouped_cli(["repair", "propose", job_id, fa, "--fixture-builder", "--json"], env)
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert data["status"] == "approval_required"
    assert data["repair_intent_id"]
    assert data["next_safe_action"]["command"].startswith("remedy patch approve")


def test_status_json(env):
    job_id, fa = _make_job_with_failure(env)
    run_grouped_cli(["repair", "propose", job_id, fa, "--fixture-builder", "--json"], env)
    r = run_grouped_cli(["repair", "status", job_id, "--json"], env)
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert data["job_id"] == job_id
    assert len(data["attempts"]) == 1
    assert data["attempts"][0]["status"] == "approval_required"


def test_idempotent_second_propose(env):
    job_id, fa = _make_job_with_failure(env)
    r1 = run_grouped_cli(["repair", "propose", job_id, fa, "--fixture-builder", "--json"], env)
    r2 = run_grouped_cli(["repair", "propose", job_id, fa, "--fixture-builder", "--json"], env)
    d1, d2 = json.loads(r1.stdout), json.loads(r2.stdout)
    assert d1["repair_intent_id"] == d2["repair_intent_id"]
    assert d2["resumed"] is True


def test_no_traceback_text_output(env):
    job_id, fa = _make_job_with_failure(env)
    r = run_grouped_cli(["repair", "propose", job_id, fa], env)
    assert r.returncode == 0, r.stderr
    assert "Traceback" not in r.stdout and "Traceback" not in r.stderr
