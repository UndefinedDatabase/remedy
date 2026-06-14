"""Runtime CLI tests for `remedy orchestrator` (Step 1488).

Subprocess tests on tiny jobs. Read-only inspect/report + metadata-only decide/idea.
No execution/provider/network. Bounded timeout.
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
    job = Job(id=uuid4(), name="ov-orch", user_prompt="x", state=RunState.RUNNING,
              tasks=[task], artifacts=[fa], metadata={"target_repo": "."})
    save_job(job, root=data_dir)
    return str(job.id)


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    ad = tmp_path / "agent"; ad.mkdir()
    for f in ("live_review.md", "plan.md", "context.md"):
        (ad / f).write_text("## Verdict\nPASS\n")
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    monkeypatch.setenv("REMEDY_AGENT_DIR", str(ad))
    return d


def test_inspect_json(env):
    r = run_grouped_cli(["orchestrator", "inspect", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert "current_phase" in d and "model_routing_plan" in d
    assert "Traceback" not in r.stdout and "Traceback" not in r.stderr


def test_decide_json(env):
    job_id = _job(env)
    r = run_grouped_cli(["orchestrator", "decide", "--job-id", job_id, "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["stop_reason"] in ("selected", "human_review_required", "no_safe_action",
                                "evidence_incomplete")
    if d.get("selected_option") and d["selected_option"].get("command"):
        assert d["next_safe_action"].startswith("remedy ")


def test_report_markdown(env):
    job_id = _job(env)
    r = run_grouped_cli(["orchestrator", "report", "--job-id", job_id, "--markdown"], env)
    assert r.returncode == 0, r.stderr
    assert "# Orchestrator Report" in r.stdout
    assert "/home/" not in r.stdout


def test_idea_json(env):
    r = run_grouped_cli(["orchestrator", "idea", "add a security audit feature", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["classification"] == "safety_concern"


def test_missing_job_safe(env):
    r = run_grouped_cli(["orchestrator", "decide", "--job-id", str(uuid4()), "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["next_safe_action"]  # safe baseline action
    assert "Traceback" not in r.stderr


def test_invalid_job_safe(env):
    r = run_grouped_cli(["orchestrator", "inspect", "--job-id", "not-a-uuid", "--json"], env)
    assert r.returncode == 0, r.stderr
    assert "Traceback" not in r.stdout and "Traceback" not in r.stderr
