"""Runtime CLI tests for `remedy self execute/status/reconcile/integrity` (Step 1451).

Subprocess tests on tiny jobs. Metadata-only execute/reconcile; read-only status/
integrity. No apply/provider/git/main mutation. Bounded timeout.
"""
from __future__ import annotations

import json
import subprocess
from uuid import uuid4

import pytest

from tests.cli.runtime_helpers import run_grouped_cli


def _approved_task(data_dir):
    from packages.core.models import Artifact, ArtifactKind, Job, RunState, Task
    from packages.orchestration import self_dogfood as SD
    from packages.orchestration.proposed_tasks import (
        ProposedTaskStatus,
        load_proposed_tasks,
        save_proposed_tasks,
        transition_status,
    )
    from packages.orchestration.storage import save_job
    task = Task(description="t")
    fa = Artifact(name="tf", content="x", kind=ArtifactKind.VERIFICATION, task_id=task.id,
                  metadata={"test_failure": True, "failure_kind": "test_failed",
                            "related_task_id": str(task.id), "safe_summary": "boom"})
    job = Job(id=uuid4(), name="ov-se", user_prompt="x", state=RunState.RUNNING,
              tasks=[task], artifacts=[fa], metadata={"target_repo": "."})
    save_job(job, root=data_dir)
    SD.propose_self_improvement(str(job.id), top=1, data_dir=data_dir)
    tasks = load_proposed_tasks(str(job.id), data_dir)
    transition_status(tasks[0], ProposedTaskStatus.APPROVED_FOR_BUILD, by="human")
    save_proposed_tasks(str(job.id), tasks, data_dir)
    return str(job.id), tasks[0].id


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    ad = tmp_path / "agent"; ad.mkdir()
    for f in ("live_review.md", "plan.md", "context.md"):
        (ad / f).write_text("## Verdict\nPASS\n")
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    monkeypatch.setenv("REMEDY_AGENT_DIR", str(ad))
    return d


@pytest.fixture()
def work_repo(tmp_path):
    """A checkout on a feature branch, for the subprocess to run inside.

    `self execute` refuses main, master and an unknown branch, and it reads that
    branch from `.git/HEAD` relative to the working directory. Run from this
    repository the answer is whatever branch the suite happens to sit on, and
    `actions/checkout` leaves a pull_request build on a DETACHED head, which the
    guard reads as unknown and refuses — so on a runner these tests measured the
    checkout rather than the guard. Owning the branch makes the outcome the
    test's own.
    """
    repo = tmp_path / "work"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "feature/self-exec-test", str(repo)],
                   check=True, capture_output=True)
    return repo


def test_missing_proposed_task(env):
    r = run_grouped_cli(["self", "execute", "nope", "--job-id", str(uuid4()), "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["stop_reason"] == "proposed_task_not_found"
    assert "Traceback" not in r.stdout and "Traceback" not in r.stderr


def test_approved_execute_awaits_candidate(env, work_repo):
    job_id, pt = _approved_task(env)
    r = run_grouped_cli(["self", "execute", pt, "--job-id", job_id, "--json"], env, cwd=work_repo)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["state"] == "awaiting_external_candidate"
    assert d["next_safe_action"].startswith(f"remedy provider intake-repair {job_id}")


def test_execute_idempotent(env, work_repo):
    job_id, pt = _approved_task(env)
    r1 = json.loads(run_grouped_cli(["self", "execute", pt, "--job-id", job_id, "--json"], env, cwd=work_repo).stdout)
    r2 = json.loads(run_grouped_cli(["self", "execute", pt, "--job-id", job_id, "--json"], env, cwd=work_repo).stdout)
    assert r1["attempt_id"] == r2["attempt_id"]


def test_status_and_reconcile_json(env, work_repo):
    job_id, pt = _approved_task(env)
    aid = json.loads(run_grouped_cli(["self", "execute", pt, "--job-id", job_id, "--json"], env, cwd=work_repo).stdout)["attempt_id"]
    rs = run_grouped_cli(["self", "status", "--json"], env, cwd=work_repo)
    assert rs.returncode == 0 and len(json.loads(rs.stdout)["attempts"]) == 1
    rr = run_grouped_cli(["self", "reconcile", aid, "--json"], env, cwd=work_repo)
    assert rr.returncode == 0, rr.stderr
    assert json.loads(rr.stdout)["attempt_id"] == aid


def test_integrity_json(env, work_repo):
    job_id, pt = _approved_task(env)
    run_grouped_cli(["self", "execute", pt, "--job-id", job_id, "--json"], env, cwd=work_repo)
    r = run_grouped_cli(["self", "integrity", "--json"], env, cwd=work_repo)
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout)["passed"] is True


def test_unapproved_blocks(env):
    from packages.orchestration import self_dogfood as SD
    from packages.orchestration.proposed_tasks import ProposedTaskStatus, load_proposed_tasks
    job_id, _ = _approved_task(env)
    SD.propose_self_improvement(job_id, top=2, data_dir=env)
    tasks = load_proposed_tasks(job_id, env)
    unapproved = next(t for t in tasks if t.status == ProposedTaskStatus.PROPOSED)
    r = run_grouped_cli(["self", "execute", unapproved.id, "--job-id", job_id, "--json"], env)
    d = json.loads(r.stdout)
    assert d["stop_reason"] == "not_approved"
