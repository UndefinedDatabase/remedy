"""Runtime CLI tests for `remedy repair request` / `request-show` (Step 1383).

Subprocess tests on tiny jobs. No provider/network/subprocess/apply, no nested full
pytest, bounded timeout.
"""
from __future__ import annotations

import json
from uuid import uuid4

import pytest

from tests.cli.runtime_helpers import run_grouped_cli


def _job(data_dir):
    from packages.core.models import Artifact, ArtifactKind, Job, RunState, Task
    from packages.orchestration.storage import save_job
    task = Task(description="t")
    fa = Artifact(name="tf", content="x", kind=ArtifactKind.VERIFICATION, task_id=task.id,
                  metadata={"test_failure": True, "failure_kind": "test_failed",
                            "related_task_id": str(task.id), "related_files": ["docs/guide.md"],
                            "exit_code": 1, "safe_summary": "boom", "command_display": "pytest x"})
    job = Job(id=uuid4(), name="ov-rr", user_prompt="x", state=RunState.RUNNING,
              tasks=[task], artifacts=[fa], metadata={"target_repo": "."})
    save_job(job, root=data_dir)
    return str(job.id), str(fa.id)


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    return d


def test_missing_job(env):
    r = run_grouped_cli(["repair", "request", str(uuid4()),
                         "--failure-artifact-id", str(uuid4()), "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["stop_reason"] == "job_not_found"
    assert "Traceback" not in r.stdout and "Traceback" not in r.stderr


def test_missing_failure_artifact_flag(env):
    job_id, _ = _job(env)
    r = run_grouped_cli(["repair", "request", job_id, "--json"], env)
    assert r.returncode != 0  # requires --failure-artifact-id


def test_valid_request_json(env):
    job_id, fid = _job(env)
    r = run_grouped_cli(["repair", "request", job_id, "--failure-artifact-id", fid,
                         "--target", "markdown_only", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["stop_reason"] == "ready"
    assert d["request_package_id"]
    assert d["output_intake_command"].startswith(f"remedy provider intake-repair {job_id}")
    assert "diff --git" not in r.stdout


def test_text_includes_request_and_intake(env):
    job_id, fid = _job(env)
    r = run_grouped_cli(["repair", "request", job_id, "--failure-artifact-id", fid], env)
    assert r.returncode == 0, r.stderr
    assert "Repair request" in r.stdout
    assert "provider intake-repair" in r.stdout


def test_request_show_json(env):
    job_id, fid = _job(env)
    r = run_grouped_cli(["repair", "request", job_id, "--failure-artifact-id", fid, "--json"], env)
    rpid = json.loads(r.stdout)["request_package_id"]
    r2 = run_grouped_cli(["repair", "request-show", job_id, rpid, "--json"], env)
    assert r2.returncode == 0, r2.stderr
    d2 = json.loads(r2.stdout)
    assert d2["request_package_id"] == rpid
    assert len(d2["sections"]) >= 5
    assert "/home/" not in r2.stdout


def test_repeated_request_idempotent(env):
    job_id, fid = _job(env)
    r1 = run_grouped_cli(["repair", "request", job_id, "--failure-artifact-id", fid, "--json"], env)
    r2 = run_grouped_cli(["repair", "request", job_id, "--failure-artifact-id", fid, "--json"], env)
    assert json.loads(r1.stdout)["request_package_id"] == json.loads(r2.stdout)["request_package_id"]
