"""Runtime CLI tests for the Token-Aware Repair Loop v1/v2 (Step 1930).

Subprocess tests. item-create-from-failure/review, item-show/list, context-pack, route-recommend,
evaluate, attempts, policy-show/set, integrity. Safe JSON, safe errors, no tracebacks, no raw leak.
"""
from __future__ import annotations

import json
from uuid import uuid4

import pytest

from tests.cli.runtime_helpers import run_grouped_cli


def _job(env, *, with_failure=False):
    from packages.core.models import Artifact, ArtifactKind, Job, RunState, Task
    from packages.orchestration.storage import save_job
    repo = env / f"repo-{uuid4().hex[:6]}"; repo.mkdir(parents=True); (repo / "a.py").write_text("x=1\n")
    arts = []
    fa = ""
    if with_failure:
        art = Artifact(name="f", content="x", kind=ArtifactKind.BUILDER_PROPOSAL, metadata={
            "test_failure": True, "failure_kind": "test_failed", "safe_summary": "failed",
            "related_files": ["/home/u/m.py"], "exit_code": 1})
        arts.append(art); fa = str(art.id)
    job = Job(id=uuid4(), name="m", user_prompt="x", state=RunState.RUNNING,
              tasks=[Task(description="t")], artifacts=arts, metadata={"target_repo": str(repo)})
    save_job(job, root=env)
    return str(job.id), fa


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    return d


def test_policy_show_and_set(env):
    jid, _ = _job(env)
    r = run_grouped_cli(["repair", "policy-show", jid, "--json"], env)
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout)["max_attempts"] == 3
    r2 = run_grouped_cli(["repair", "policy-set", jid, "--max-attempts", "5",
                          "--require-reviewer-pass", "false", "--json"], env)
    d = json.loads(r2.stdout)
    assert d["max_attempts"] == 5 and d["require_reviewer_pass"] is False


def test_item_create_show_list_evaluate(env):
    jid, fa = _job(env, with_failure=True)
    r = run_grouped_cli(["repair", "item-create-from-failure", fa, "--job-id", jid, "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    rid = d["repair_id"]
    assert "/home/u" not in r.stdout
    r2 = run_grouped_cli(["repair", "item-show", rid, "--json"], env)
    assert json.loads(r2.stdout)["repair_id"] == rid
    r3 = run_grouped_cli(["repair", "item-list", jid, "--json"], env)
    assert json.loads(r3.stdout)["count"] == 1
    r4 = run_grouped_cli(["repair", "evaluate", rid, "--json"], env)
    assert json.loads(r4.stdout)["status"] == "context_needed"


def test_context_pack_and_route(env):
    jid, fa = _job(env, with_failure=True)
    rid = json.loads(run_grouped_cli(
        ["repair", "item-create-from-failure", fa, "--job-id", jid, "--json"], env).stdout)["repair_id"]
    r = run_grouped_cli(["repair", "context-pack", rid, "--json"], env)
    assert r.returncode == 0, r.stderr
    blob = r.stdout.lower()
    for marker in ("sk-ant", "/home/", "traceback", "diff --git"):
        assert marker not in blob
    r2 = run_grouped_cli(["repair", "route-recommend", rid, "--json"], env)
    assert r2.returncode == 0 and "recommended_route_kind" in r2.stdout


def test_integrity_and_attempts(env):
    jid, fa = _job(env, with_failure=True)
    rid = json.loads(run_grouped_cli(
        ["repair", "item-create-from-failure", fa, "--job-id", jid, "--json"], env).stdout)["repair_id"]
    r = run_grouped_cli(["repair", "integrity", "--json"], env)
    assert json.loads(r.stdout)["passed"] is True
    r2 = run_grouped_cli(["repair", "attempts", rid, "--json"], env)
    assert json.loads(r2.stdout)["count"] == 0


def test_invalid_ids(env):
    r1 = run_grouped_cli(["repair", "item-show", "nope", "--json"], env)
    assert r1.returncode == 1 and "Traceback" not in r1.stderr
    jid, _ = _job(env)
    r2 = run_grouped_cli(["repair", "item-create-from-failure", "nope", "--job-id", jid, "--json"], env)
    assert r2.returncode == 1 and "Traceback" not in r2.stderr
