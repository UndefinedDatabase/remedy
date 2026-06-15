"""Runtime CLI tests for `remedy local-candidate` — Automated Local Candidate Generator v0
(Step 1631).

Subprocess tests. Generator DISABLED by default; a missing/disabled local model must never break
deterministic orchestration. No real Ollama in CI: tests use the disabled path + an unreachable
loopback endpoint (connection refused) — never an external host. Bounded timeout.
"""
from __future__ import annotations

import json
from uuid import uuid4

import pytest

from tests.cli.runtime_helpers import run_grouped_cli


def _job(data_dir, *, with_pkg=True):
    from packages.core.models import Artifact, ArtifactKind, Job, RunState, Task
    from packages.orchestration.storage import save_job
    task = Task(description="t")
    fa = Artifact(name="tf", content="x", kind=ArtifactKind.VERIFICATION, task_id=task.id,
                  metadata={"test_failure": True, "related_files": ["docs/g.md"], "test_command": "pytest"})
    job = Job(id=uuid4(), name="lc", user_prompt="x", state=RunState.RUNNING,
              tasks=[task], artifacts=[fa], metadata={"target_repo": "."})
    if with_pkg:
        job.metadata["repair_request_packages_v0"] = {
            "rp1": {"request_package_id": "rp1", "job_id": str(job.id),
                    "failure_artifact_id": str(fa.id), "target_kind": "docs",
                    "sections": [{"title": "G", "body": "fix", "files": ["docs/g.md"]}]}}
    save_job(job, root=data_dir)
    return str(job.id), str(fa.id)


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    ad = tmp_path / "agent"; ad.mkdir()
    (ad / "live_review.md").write_text("## Verdict\nPASS\n")
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    monkeypatch.setenv("REMEDY_REVIEW_FILE", str(ad / "live_review.md"))
    for k in ("REMEDY_LOCAL_CANDIDATE_GENERATOR_ENABLED", "REMEDY_LOCAL_CANDIDATE_GENERATOR_ENDPOINT",
              "REMEDY_LOCAL_CANDIDATE_GENERATOR_MODEL"):
        monkeypatch.delenv(k, raising=False)
    return d


def test_status_disabled_json(env):
    r = run_grouped_cli(["local-candidate", "status", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["enabled"] is False
    assert d["available"] is False
    assert "Traceback" not in r.stdout and "Traceback" not in r.stderr


def test_status_external_endpoint_blocked(env, monkeypatch):
    monkeypatch.setenv("REMEDY_LOCAL_CANDIDATE_GENERATOR_ENABLED", "1")
    monkeypatch.setenv("REMEDY_LOCAL_CANDIDATE_GENERATOR_ENDPOINT", "http://evil.example.com:11434")
    monkeypatch.setenv("REMEDY_LOCAL_CANDIDATE_GENERATOR_MODEL", "m")
    r = run_grouped_cli(["local-candidate", "status", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["available"] is False
    assert "evil.example.com" not in r.stdout


def test_generate_requires_request_package(env):
    job_id, _ = _job(env)
    r = run_grouped_cli(["local-candidate", "generate", "--job-id", job_id, "--json"], env)
    assert r.returncode == 1   # missing --request-package-id
    assert "Traceback" not in r.stderr


def test_generate_disabled_blocks(env):
    job_id, fid = _job(env)
    r = run_grouped_cli(["local-candidate", "generate", "--request-package-id", "rp1",
                         "--job-id", job_id, "--failure-artifact-id", fid, "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["status"] == "disabled"
    assert d["stop_reason"] == "disabled"


def test_generate_enabled_unreachable_safe(env, monkeypatch):
    # Enabled + loopback but nothing listening → connection refused → unavailable, never a crash.
    monkeypatch.setenv("REMEDY_LOCAL_CANDIDATE_GENERATOR_ENABLED", "1")
    monkeypatch.setenv("REMEDY_LOCAL_CANDIDATE_GENERATOR_ENDPOINT", "http://127.0.0.1:9")  # unused port
    monkeypatch.setenv("REMEDY_LOCAL_CANDIDATE_GENERATOR_MODEL", "m")
    job_id, fid = _job(env)
    # Need a failed repair so routing can reach local_candidate_generator.
    from packages.orchestration.storage import load_job, save_job
    from uuid import UUID
    job = load_job(UUID(job_id), env)
    job.metadata["repair_attempts_v1"] = {"a1": {"attempt_id": "a1", "failure_artifact_id": fid,
                                                  "status": "tested_failed"}}
    save_job(job, root=env)
    r = run_grouped_cli(["local-candidate", "generate", "--request-package-id", "rp1",
                         "--job-id", job_id, "--failure-artifact-id", fid, "--json"], env, timeout=30)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    # Either unavailable (model unreachable) or blocked (routing/budget) — never a crash/intent.
    assert d["status"] in ("unavailable", "blocked")
    assert not d["linkage"]["intent_id"]
    assert "Traceback" not in r.stderr


def test_missing_job_safe(env):
    r = run_grouped_cli(["local-candidate", "generate", "--request-package-id", "rp1",
                         "--job-id", str(uuid4()), "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["status"] in ("disabled", "blocked")
    assert "Traceback" not in r.stderr
