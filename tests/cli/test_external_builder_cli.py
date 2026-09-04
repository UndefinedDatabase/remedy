"""Runtime CLI tests for `remedy external-builder` — External Builder Sandbox v0 (Step 1698).

Subprocess tests. Ingress only — no execution/apply/approve/test. Bounded + safe. No raw candidate.
"""
from __future__ import annotations

import json
from uuid import uuid4

import pytest

from tests.cli.runtime_helpers import run_grouped_cli

_SAFE_CAND = json.dumps({
    "summary": "Add note", "rationale": "addresses the documentation gap",
    "target_files": ["docs/note.md"],
    "structured_operations": [{"op": "create", "path": "docs/note.md", "content": "hi"}],
})


def _job(env):
    from packages.core.models import Artifact, ArtifactKind, Job, RunState, Task
    from packages.orchestration.storage import save_job
    task = Task(description="t")
    fa = Artifact(name="tf", content="x", kind=ArtifactKind.VERIFICATION, task_id=task.id,
                  metadata={"test_failure": True, "related_files": ["docs/note.md"],
                            "test_command": "pytest", "safe_summary": "boom"})
    job = Job(id=uuid4(), name="eb", user_prompt="x", state=RunState.RUNNING,
              tasks=[task], artifacts=[fa], metadata={"target_repo": "."})
    save_job(job, root=env)
    return str(job.id)


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    ad = tmp_path / "agent"; ad.mkdir()
    (ad / "live_review.md").write_text("## Verdict\nPASS\n")
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    monkeypatch.setenv("REMEDY_REVIEW_FILE", str(ad / "live_review.md"))
    return d


def test_package_create_show_list(env):
    job_id = _job(env)
    r = run_grouped_cli(["external-builder", "package-create", job_id, "--json"], env)
    assert r.returncode == 0, r.stderr
    pkg = json.loads(r.stdout)
    pid = pkg["package_id"]
    assert pid and "Traceback" not in r.stdout
    r2 = run_grouped_cli(["external-builder", "package-show", pid, "--json"], env)
    assert r2.returncode == 0, r2.stderr
    assert json.loads(r2.stdout)["package_id"] == pid
    r3 = run_grouped_cli(["external-builder", "package-list", job_id, "--json"], env)
    assert json.loads(r3.stdout)["package_count"] == 1


def test_submit_candidate_json(env):
    job_id = _job(env)
    pkg = json.loads(run_grouped_cli(["external-builder", "package-create", job_id, "--json"], env).stdout)
    cf = env / "resp.md"; cf.write_text(_SAFE_CAND)
    r = run_grouped_cli(["external-builder", "submit", pkg["package_id"],
                         "--candidate-file", str(cf), "--source-label", "claude", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["state"] == "pending_approval"
    assert d["intent_id"]
    assert "hi" not in r.stdout and "documentation gap" not in r.stdout
    sid = d["submission_id"]
    # evaluate
    r2 = run_grouped_cli(["external-builder", "evaluate", sid, "--json"], env)
    assert r2.returncode == 0, r2.stderr
    assert json.loads(r2.stdout)["outcome"] == "pending_approval"


def test_submit_requires_candidate_file(env):
    job_id = _job(env)
    pkg = json.loads(run_grouped_cli(["external-builder", "package-create", job_id, "--json"], env).stdout)
    r = run_grouped_cli(["external-builder", "submit", pkg["package_id"], "--json"], env)
    assert r.returncode == 1
    assert "Traceback" not in r.stderr


def test_submit_bad_package(env):
    cf = env / "resp.md"; cf.write_text(_SAFE_CAND)
    r = run_grouped_cli(["external-builder", "submit", "nope", "--candidate-file", str(cf), "--json"], env)
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout)["stop_reason"] == "package_not_found"


def test_submit_oversized(env):
    job_id = _job(env)
    pkg = json.loads(run_grouped_cli(["external-builder", "package-create", job_id, "--json"], env).stdout)
    big = env / "big.md"; big.write_text("x" * (300 * 1024))
    r = run_grouped_cli(["external-builder", "submit", pkg["package_id"],
                         "--candidate-file", str(big), "--json"], env)
    d = json.loads(r.stdout)
    assert d["stop_reason"] == "candidate_oversized"
    assert not d["intent_id"]


def test_integrity_json(env):
    r = run_grouped_cli(["external-builder", "integrity", "--json"], env)
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout)["passed"] is True


def test_package_missing_job(env):
    r = run_grouped_cli(["external-builder", "package-create", str(uuid4()), "--json"], env)
    assert r.returncode == 1
    assert "Traceback" not in r.stderr


def test_submission_list_json_has_received_at(env):
    job_id = _job(env)
    pkg = json.loads(run_grouped_cli(["external-builder", "package-create", job_id, "--json"], env).stdout)
    cf = env / "resp.md"; cf.write_text(_SAFE_CAND)
    run_grouped_cli(["external-builder", "submit", pkg["package_id"],
                     "--candidate-file", str(cf), "--source-label", "claude", "--json"], env)
    r = run_grouped_cli(["external-builder", "submission-list", job_id, "--json"], env)
    d = json.loads(r.stdout)
    assert d["submissions"][0]["received_at"]


def test_submission_list_text_shows_per_row(env):
    job_id = _job(env)
    pkg = json.loads(run_grouped_cli(["external-builder", "package-create", job_id, "--json"], env).stdout)
    cf = env / "resp.md"; cf.write_text(_SAFE_CAND)
    r = run_grouped_cli(["external-builder", "submit", pkg["package_id"],
                         "--candidate-file", str(cf), "--source-label", "claude", "--json"], env)
    sid = json.loads(r.stdout)["submission_id"]
    r2 = run_grouped_cli(["external-builder", "submission-list", job_id], env)
    assert r2.returncode == 0
    assert sid in r2.stdout
    assert "received=" in r2.stdout
