"""Runtime CLI tests for `remedy provider` — Provider Trust Gate v0 (Step 1327).

Subprocess tests on tiny jobs. No provider execution, no network, no shell=True,
no nested full pytest, bounded timeout.
"""
from __future__ import annotations

import json
from uuid import uuid4

import pytest

from tests.cli.runtime_helpers import run_grouped_cli


def _job(data_dir, *, with_failure=True):
    from packages.core.models import Artifact, ArtifactKind, Job, RunState, Task
    from packages.orchestration.storage import save_job
    task = Task(description="t")
    arts = []
    fid = ""
    if with_failure:
        fa = Artifact(name="tf", content="x", kind=ArtifactKind.VERIFICATION, task_id=task.id,
                      metadata={"test_failure": True, "failure_kind": "test_failed",
                                "related_task_id": str(task.id), "related_files": ["src/app.py"],
                                "safe_summary": "boom"})
        arts.append(fa); fid = str(fa.id)
    job = Job(id=uuid4(), name="ov-prov", user_prompt="x", state=RunState.RUNNING,
              tasks=[task], artifacts=arts, metadata={"target_repo": "."})
    save_job(job, root=data_dir)
    return str(job.id), fid


_GOOD = ("Fix.\n```diff\n--- a/src/app.py\n+++ b/src/app.py\n@@ -1,2 +1,2 @@\n-x = 1\n+x = 2\n```\n")


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    return d


def test_missing_job(env):
    p = env / "in.md"; p.write_text(_GOOD)
    r = run_grouped_cli(["provider", "intake-repair", str(uuid4()),
                         "--input", str(p), "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["trust_status"] == "rejected"
    assert "Traceback" not in r.stdout and "Traceback" not in r.stderr


def test_bad_input_path(env):
    job_id, fid = _job(env)
    r = run_grouped_cli(["provider", "intake-repair", job_id,
                         "--input", str(env / "nope.md"), "--failure-artifact-id", fid, "--json"], env)
    d = json.loads(r.stdout)
    assert d["trust_status"] == "rejected"
    assert any(f["code"] == "input_not_found" for f in d["findings"])


def test_oversized_rejected(env):
    job_id, fid = _job(env)
    p = env / "big.md"; p.write_text("x" * (256 * 1024 + 50))
    r = run_grouped_cli(["provider", "intake-repair", job_id, "--input", str(p),
                         "--failure-artifact-id", fid, "--json"], env)
    d = json.loads(r.stdout)
    assert d["trust_status"] == "rejected"
    assert any(f["code"] == "input_too_large" for f in d["findings"])


def test_unparseable_no_intent(env):
    job_id, fid = _job(env)
    p = env / "u.md"; p.write_text("???")
    r = run_grouped_cli(["provider", "intake-repair", job_id, "--input", str(p),
                         "--failure-artifact-id", fid, "--json"], env)
    d = json.loads(r.stdout)
    assert not d["repair_intent_id"]


def test_secret_rejected(env):
    job_id, fid = _job(env)
    p = env / "s.md"
    p.write_text('Fix.\n```diff\n--- a/src/app.py\n+++ b/src/app.py\n@@ -1 +1,2 @@\n a\n'
                 '+token = "ghp_abcdefghijklmnopqrstuvwxyz0123"\n```\n')
    r = run_grouped_cli(["provider", "intake-repair", job_id, "--input", str(p),
                         "--failure-artifact-id", fid, "--json"], env)
    d = json.loads(r.stdout)
    assert d["trust_status"] == "rejected"
    assert not d["repair_intent_id"]
    assert "ghp_" not in r.stdout  # secret value never echoed


def test_protected_path_rejected(env):
    job_id, fid = _job(env)
    p = env / "pr.md"
    p.write_text("```diff\n--- a/.env\n+++ b/.env\n@@ -1 +1 @@\n-A=1\n+A=2\n```\n")
    r = run_grouped_cli(["provider", "intake-repair", job_id, "--input", str(p),
                         "--failure-artifact-id", fid, "--json"], env)
    d = json.loads(r.stdout)
    assert d["trust_status"] == "rejected"
    assert not d["repair_intent_id"]


def test_accepted_creates_pending_intent_and_trust_show(env):
    job_id, fid = _job(env)
    p = env / "g.md"; p.write_text(_GOOD)
    r = run_grouped_cli(["provider", "intake-repair", job_id, "--input", str(p),
                         "--failure-artifact-id", fid, "--provider", "claude", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["trust_status"] == "accepted"
    assert d["repair_intent_id"]
    assert d["next_safe_action"] == f"remedy patch approve {job_id} {d['repair_intent_id']} --json"
    assert "x = 2" not in r.stdout  # no raw diff line

    rid = d["trust_report_id"]
    r2 = run_grouped_cli(["provider", "trust-show", job_id, rid, "--json"], env)
    assert r2.returncode == 0, r2.stderr
    d2 = json.loads(r2.stdout)
    assert d2["trust_status"] == "accepted"
    assert d2["repair_intent_id"] == d["repair_intent_id"]
    assert "x = 2" not in r2.stdout


def test_stdin_input(env):
    job_id, fid = _job(env)
    # run_grouped_cli uses DEVNULL stdin; stdin path is covered by unit tests.
    # Here just assert --stdin flag is accepted by the parser (no input → safe reject).
    r = run_grouped_cli(["provider", "intake-repair", job_id, "--stdin",
                         "--failure-artifact-id", fid, "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["trust_status"] == "rejected"  # empty stdin
    assert "Traceback" not in r.stderr
