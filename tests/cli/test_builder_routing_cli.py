"""Runtime CLI tests for `remedy builder-routing decide` / `report` (Step 1598).

Subprocess tests on tiny jobs. Routing/planning ONLY — no builder/model/provider execution,
no candidate generation, no network, no shell=True, no apply/approval. No raw content in any
surface. Bounded timeout.
"""
from __future__ import annotations

import json
from uuid import uuid4

import pytest

from tests.cli.runtime_helpers import run_grouped_cli


def _job(data_dir, *, failure=True):
    from packages.core.models import Artifact, ArtifactKind, Job, RunState, Task
    from packages.orchestration.storage import save_job
    task = Task(description="t")
    arts = []
    fid = ""
    if failure:
        fa = Artifact(name="tf", content="x", kind=ArtifactKind.VERIFICATION, task_id=task.id,
                      metadata={"test_failure": True, "related_files": ["docs/g.md"]})
        arts.append(fa); fid = str(fa.id)
    job = Job(id=uuid4(), name="br", user_prompt="x", state=RunState.RUNNING,
              tasks=[task], artifacts=arts, metadata={"target_repo": "."})
    save_job(job, root=data_dir)
    return str(job.id), fid


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    ad = tmp_path / "agent"; ad.mkdir()
    (ad / "live_review.md").write_text("## Verdict\nPASS\n")
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    monkeypatch.setenv("REMEDY_REVIEW_FILE", str(ad / "live_review.md"))
    return d


def test_decide_json(env):
    job_id, fid = _job(env)
    r = run_grouped_cli(["builder-routing", "decide", "--job-id", job_id,
                         "--failure-artifact-id", fid, "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["selected_tier"] in (
        "deterministic_only", "local_advisor", "human_review_required", "no_safe_route")
    assert d["next_safe_action"].startswith("remedy ")
    assert "Traceback" not in r.stdout and "Traceback" not in r.stderr


def test_report_markdown(env):
    job_id, fid = _job(env)
    r = run_grouped_cli(["builder-routing", "report", "--job-id", job_id, "--markdown"], env)
    assert r.returncode == 0, r.stderr
    assert "# Builder Routing Report" in r.stdout
    assert "## Budget" in r.stdout
    assert "## Loop guard" in r.stdout
    assert "Traceback" not in r.stderr


def test_missing_job_safe(env):
    r = run_grouped_cli(["builder-routing", "decide", "--job-id", str(uuid4()), "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["selected_tier"] == "no_safe_route"
    assert d["stop_reason"] == "job_not_found"


def test_failure_route(env):
    job_id, fid = _job(env)
    r = run_grouped_cli(["builder-routing", "decide", "--job-id", job_id,
                         "--failure-artifact-id", fid, "--json"], env)
    d = json.loads(r.stdout)
    # Unresolved failure, no repair attempt → deterministic repair propose.
    assert d["selected_tier"] == "deterministic_only"
    assert "repair propose" in d["next_safe_action"]


def test_external_disabled_default(env):
    # Default policy never recommends external via the CLI.
    job_id, fid = _job(env)
    r = run_grouped_cli(["builder-routing", "decide", "--job-id", job_id,
                         "--failure-artifact-id", fid, "--user-requested", "--json"], env)
    d = json.loads(r.stdout)
    assert d["selected_tier"] != "external_candidate_generator"


def test_no_raw_secret_echo(env):
    from uuid import UUID

    from packages.orchestration.storage import load_job, save_job
    job_id, fid = _job(env)
    job = load_job(UUID(job_id), env)
    fa = job.artifacts[0]
    fa.metadata["related_files"] = ["sk-ABCDEFGHIJKLMNOP /home/u/.ssh/id_rsa"]
    save_job(job, root=env)
    r = run_grouped_cli(["builder-routing", "decide", "--job-id", job_id,
                         "--failure-artifact-id", fid, "--json"], env)
    assert r.returncode == 0, r.stderr
    assert "sk-ABCDEFGHIJKLMNOP" not in r.stdout
    assert "/home/u/.ssh/id_rsa" not in r.stdout


def test_idempotent_decide(env):
    job_id, fid = _job(env)
    r1 = run_grouped_cli(["builder-routing", "decide", "--job-id", job_id,
                          "--failure-artifact-id", fid, "--json"], env)
    r2 = run_grouped_cli(["builder-routing", "decide", "--job-id", job_id,
                          "--failure-artifact-id", fid, "--json"], env)
    assert json.loads(r1.stdout)["routing_id"] == json.loads(r2.stdout)["routing_id"]
