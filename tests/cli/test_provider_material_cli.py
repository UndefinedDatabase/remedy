"""Runtime CLI tests for provider patch materialization (Step 1354).

Subprocess tests on tiny jobs. No provider execution, no network, no shell=True,
no nested full pytest, bounded timeout.
"""
from __future__ import annotations

import json
from uuid import uuid4

import pytest

from tests.cli.runtime_helpers import run_grouped_cli


def _job(data_dir, *, related=("docs/guide.md",)):
    from packages.core.models import Artifact, ArtifactKind, Job, RunState, Task
    from packages.orchestration.storage import save_job
    task = Task(description="t")
    fa = Artifact(name="tf", content="x", kind=ArtifactKind.VERIFICATION, task_id=task.id,
                  metadata={"test_failure": True, "failure_kind": "test_failed",
                            "related_task_id": str(task.id), "related_files": list(related),
                            "safe_summary": "boom"})
    job = Job(id=uuid4(), name="ov-pm", user_prompt="x", state=RunState.RUNNING,
              tasks=[task], artifacts=[fa], metadata={"target_repo": "."})
    save_job(job, root=data_dir)
    return str(job.id), str(fa.id)


def _md(path="docs/guide.md"):
    return (f"Fix.\n```diff\n--- a/{path}\n+++ b/{path}\n@@ -1,2 +1,3 @@\n line one\n+new\n line two\n```\n")


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    return d


def test_md_intake_materializes_pending_intent(env):
    job_id, fid = _job(env)
    p = env / "g.md"; p.write_text(_md())
    r = run_grouped_cli(["provider", "intake-repair", job_id, "--input", str(p),
                         "--failure-artifact-id", fid, "--provider", "claude", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["trust_status"] == "accepted"
    assert d["material_state"] == "materialized"
    assert d["repair_intent_id"]
    assert d["next_safe_action"] == f"remedy patch approve {job_id} {d['repair_intent_id']} --json"
    assert "@@" not in r.stdout and "+++" not in r.stdout


def test_json_ops_intake_materializes(env):
    job_id, fid = _job(env, related=("docs/notes.md",))
    obj = json.dumps({"summary": "doc fix", "target_files": ["docs/notes.md"],
                      "patch_format": "structured_operations",
                      "structured_operations": [{"path": "docs/notes.md", "op": "modify",
                                                 "content": ["a", "b"]}]})
    p = env / "o.json"; p.write_text(obj)
    r = run_grouped_cli(["provider", "intake-repair", job_id, "--input", str(p),
                         "--failure-artifact-id", fid, "--json"], env)
    d = json.loads(r.stdout)
    assert d["material_state"] == "materialized"
    assert d["repair_intent_id"]


def test_source_diff_not_materialized(env):
    job_id, fid = _job(env, related=("src/app.py",))
    p = env / "s.md"
    p.write_text("Fix.\n```diff\n--- a/src/app.py\n+++ b/src/app.py\n@@ -1 +1 @@\n-a\n+b\n```\n")
    r = run_grouped_cli(["provider", "intake-repair", job_id, "--input", str(p),
                         "--failure-artifact-id", fid, "--json"], env)
    d = json.loads(r.stdout)
    assert d["material_state"] == "unsupported_patch_shape"
    assert not d["repair_intent_id"]


def test_delete_diff_not_materialized(env):
    job_id, fid = _job(env)
    p = env / "del.md"
    p.write_text("```diff\n--- a/docs/guide.md\n+++ /dev/null\n@@ -1 +0,0 @@\n-a\n```\n")
    r = run_grouped_cli(["provider", "intake-repair", job_id, "--input", str(p),
                         "--failure-artifact-id", fid, "--json"], env)
    d = json.loads(r.stdout)
    assert not d["repair_intent_id"]


def test_protected_path_rejected(env):
    job_id, fid = _job(env)
    p = env / "pr.md"
    p.write_text("```diff\n--- a/.env\n+++ b/.env\n@@ -1 +1 @@\n-A=1\n+A=2\n```\n")
    r = run_grouped_cli(["provider", "intake-repair", job_id, "--input", str(p),
                         "--failure-artifact-id", fid, "--json"], env)
    d = json.loads(r.stdout)
    assert d["trust_status"] == "rejected"
    assert not d["repair_intent_id"]


def test_secret_rejected_no_echo(env):
    job_id, fid = _job(env)
    p = env / "sec.md"
    p.write_text('```diff\n--- a/docs/guide.md\n+++ b/docs/guide.md\n@@ -1 +1,2 @@\n a\n'
                 '+token = "ghp_abcdefghijklmnopqrstuvwxyz0123"\n```\n')
    r = run_grouped_cli(["provider", "intake-repair", job_id, "--input", str(p),
                         "--failure-artifact-id", fid, "--json"], env)
    d = json.loads(r.stdout)
    assert d["trust_status"] == "rejected"
    assert "ghp_" not in r.stdout


def test_material_show_safe(env):
    job_id, fid = _job(env)
    p = env / "g.md"; p.write_text(_md())
    r = run_grouped_cli(["provider", "intake-repair", job_id, "--input", str(p),
                         "--failure-artifact-id", fid, "--json"], env)
    mid = json.loads(r.stdout)["material_id"]
    r2 = run_grouped_cli(["provider", "material-show", job_id, mid, "--json"], env)
    assert r2.returncode == 0, r2.stderr
    d2 = json.loads(r2.stdout)
    assert d2["material_state"] == "materialized"
    assert d2["verification"]["ok"] is True
    assert "@@" not in r2.stdout and "/home/" not in r2.stdout
    assert "Traceback" not in r2.stderr
