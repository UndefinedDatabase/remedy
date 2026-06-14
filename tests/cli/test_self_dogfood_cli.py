"""Runtime CLI tests for `remedy self` — Self-Dogfood Planner v0 (Step 1423).

Subprocess tests on tiny jobs. Read-only inspect/plan/report + metadata-only propose.
No apply/approval/git/provider/network, bounded timeout.
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
                            "related_task_id": str(task.id), "safe_summary": "boom"})
    job = Job(id=uuid4(), name="ov-sd", user_prompt="x", state=RunState.RUNNING,
              tasks=[task], artifacts=[fa], metadata={"target_repo": "."})
    save_job(job, root=data_dir)
    return str(job.id)


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    ad = tmp_path / "agent"; ad.mkdir()
    (ad / "live_review.md").write_text("## Verdict\nPASS\n")
    (ad / "plan.md").write_text("# Plan\n")
    (ad / "context.md").write_text("# Context\n")
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    monkeypatch.setenv("REMEDY_AGENT_DIR", str(ad))
    return d


def test_inspect_no_job(env):
    r = run_grouped_cli(["self", "inspect", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert "item_count" in d
    assert "Traceback" not in r.stdout and "Traceback" not in r.stderr


def test_inspect_with_job(env):
    job_id = _job(env)
    r = run_grouped_cli(["self", "inspect", "--job-id", job_id, "--json"], env)
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout)["item_count"] >= 1


def test_plan(env):
    job_id = _job(env)
    r = run_grouped_cli(["self", "plan", "--job-id", job_id, "--json"], env)
    assert r.returncode == 0, r.stderr
    assert "groups" in json.loads(r.stdout)


def test_report_markdown(env):
    job_id = _job(env)
    r = run_grouped_cli(["self", "report", "--job-id", job_id, "--markdown"], env)
    assert r.returncode == 0, r.stderr
    assert "# Self-Dogfood Report" in r.stdout
    assert "/home/" not in r.stdout


def test_propose_top_then_idempotent(env):
    job_id = _job(env)
    r1 = run_grouped_cli(["self", "propose", job_id, "--top", "2", "--json"], env)
    assert r1.returncode == 0, r1.stderr
    d1 = json.loads(r1.stdout)
    assert d1["stop_reason"] == "ok" and len(d1["proposed_task_ids"]) == 2
    r2 = run_grouped_cli(["self", "propose", job_id, "--top", "2", "--json"], env)
    d2 = json.loads(r2.stdout)
    assert not d2["proposed_task_ids"] and len(d2["skipped_existing"]) == 2


def test_propose_explicit_item(env):
    job_id = _job(env)
    insp = json.loads(run_grouped_cli(["self", "inspect", "--job-id", job_id, "--json"], env).stdout)
    iid = insp["items"][0]["item_id"]
    r = run_grouped_cli(["self", "propose", job_id, "--item-id", iid, "--json"], env)
    assert r.returncode == 0, r.stderr
    assert len(json.loads(r.stdout)["proposed_task_ids"]) == 1


def test_propose_contract_denied(env):
    import dataclasses
    from packages.orchestration.storage import load_job, save_job
    from packages.orchestration.run_contract import (
        build_default_run_contract, save_contract, ContractAction,
    )
    from uuid import UUID
    job_id = _job(env)
    job = load_job(UUID(job_id), env)
    c = build_default_run_contract(job)
    c = dataclasses.replace(c, allowed_actions=tuple(
        a for a in c.allowed_actions if a != ContractAction.SELF_PROPOSE_TASK))
    save_contract(job, c); save_job(job, root=env)
    r = run_grouped_cli(["self", "propose", job_id, "--top", "1", "--json"], env)
    d = json.loads(r.stdout)
    assert d["stop_reason"] == "contract_blocked"
    assert not d["proposed_task_ids"]
