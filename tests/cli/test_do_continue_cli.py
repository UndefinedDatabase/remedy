"""Runtime CLI tests for `remedy do continue` (Step 1166).

Canonical public form: remedy do continue <job_id> [--intent-id <id>] [--json].
Uses an ineligible job so the full CLI surface (text + stable JSON, no traceback,
no raw content) is exercised without nested pytest execution.
"""

from __future__ import annotations

import json
from uuid import uuid4

import pytest

from tests.cli.runtime_helpers import run_grouped_cli
from packages.orchestration.data_paths import mint_job_id


def _make_ineligible_job(data_dir):
    """Create a job with an unapproved intent under data_dir. Returns job_id."""
    from packages.core.models import Artifact, ArtifactKind, RunState
    from packages.orchestration.pingpong_job import JobPlan, TaskEntry
    from packages.orchestration.pingpong_job import save_job_plan

    task = TaskEntry(title="t")
    art = Artifact(
        name="b", content="", kind=ArtifactKind.BUILDER_PROPOSAL, task_id=str(task.task_id),
        metadata={
            "patch_intent_explanations": [
                {"file": "docs/X.md", "action": "create", "risk": "low",
                 "reason": "", "summary": "x"}
            ],
            "patch_intent_approvals": {},  # not approved
        },
    )
    job = JobPlan(job_id=mint_job_id(), job_title="cli-cont", user_prompt="x", state=RunState.RUNNING,
              tasks=[task], artifacts=[art], metadata={})
    save_job_plan(job, root=data_dir)
    return str(job.job_id)


@pytest.fixture()
def env(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


def test_continue_json_ineligible(env):
    job_id = _make_ineligible_job(env)
    r = run_grouped_cli(["do", "continue", job_id, "--json"], env)
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert data["job_id"] == job_id
    assert data["stop_reason"] == "blocked_ineligible"
    assert data["next_safe_action"]
    assert "Traceback" not in r.stdout
    assert "Traceback" not in r.stderr


def test_continue_text_ineligible(env):
    job_id = _make_ineligible_job(env)
    r = run_grouped_cli(["do", "continue", job_id], env)
    assert r.returncode == 0, r.stderr
    assert "Stop:" in r.stdout
    assert "blocked_ineligible" in r.stdout
    assert "Traceback" not in r.stdout


def test_continue_missing_job(env):
    r = run_grouped_cli(["do", "continue", str(uuid4()), "--json"], env)
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert data["stop_reason"] == "blocked_ineligible"


def test_continue_intent_id_flag_parses(env):
    job_id = _make_ineligible_job(env)
    # --intent-id should parse without error even when the intent is unapproved.
    r = run_grouped_cli(["do", "continue", job_id, "--intent-id", "deadbeef-0", "--json"], env)
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert data["job_id"] == job_id
