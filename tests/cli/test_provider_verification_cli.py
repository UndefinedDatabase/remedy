"""Runtime CLI tests for `remedy provider verify` / `provider verification-show` (Step 1561).

Subprocess tests on tiny jobs. No provider execution, no network, no shell=True, no apply,
no approval. No raw candidate/diff/output/secrets in any surface. Bounded timeout.
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
                            "related_files": list(related), "test_command": "pytest",
                            "safe_summary": "boom"})
    job = Job(id=uuid4(), name="v-prov", user_prompt="x", state=RunState.RUNNING,
              tasks=[task], artifacts=[fa], metadata={"target_repo": "."})
    save_job(job, root=data_dir)
    return str(job.id), str(fa.id)


_GOOD = ("Fix.\n```diff\n--- a/docs/guide.md\n+++ b/docs/guide.md\n@@ -1,2 +1,3 @@\n line one\n"
         "+fixed line\n line two\n```\n")


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    return d


def _intake(env, job_id, fid, raw):
    p = env / f"in_{uuid4().hex[:6]}.md"; p.write_text(raw)
    r = run_grouped_cli(["provider", "intake-repair", job_id, "--input", str(p),
                         "--failure-artifact-id", fid, "--provider", "claude", "--json"], env)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def test_missing_job(env):
    r = run_grouped_cli(["provider", "verify", str(uuid4()), "tr", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["decision"] == "verification_incomplete"
    assert "Traceback" not in r.stdout and "Traceback" not in r.stderr


def test_missing_trust_report(env):
    job_id, _ = _job(env)
    r = run_grouped_cli(["provider", "verify", job_id, "does-not-exist", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["decision"] == "verification_incomplete"
    assert not d["allowed_to_create_intent"]


def test_accepted_candidate_verifies(env):
    job_id, fid = _job(env)
    out = _intake(env, job_id, fid, _GOOD)
    assert out["trust_status"] == "accepted"
    # Inline verification already ran during intake.
    assert out["verification_decision"] in ("verification_passed", "needs_human_review")
    trid = out["trust_report_id"]
    r = run_grouped_cli(["provider", "verify", job_id, trid, "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["decision"] in ("verification_passed", "needs_human_review")
    # No raw diff ever surfaced.
    assert "@@" not in r.stdout and "+++" not in r.stdout


def test_verification_show(env):
    job_id, fid = _job(env)
    out = _intake(env, job_id, fid, _GOOD)
    vid = out["verification_id"]
    assert vid
    r = run_grouped_cli(["provider", "verification-show", job_id, vid, "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["verification_id"] == vid
    assert "decision" in d and "score" in d
    assert "@@" not in r.stdout


def test_show_missing_report(env):
    job_id, _ = _job(env)
    r = run_grouped_cli(["provider", "verification-show", job_id, "nope", "--json"], env)
    assert r.returncode == 1
    assert "Traceback" not in r.stderr


def test_secret_candidate_no_echo(env):
    job_id, fid = _job(env)
    raw = ('Fix.\n```diff\n--- a/docs/guide.md\n+++ b/docs/guide.md\n@@ -1 +1,2 @@\n a\n'
           '+token = "ghp_abcdefghijklmnopqrstuvwxyz0123"\n```\n')
    out = _intake(env, job_id, fid, raw)
    # Secret is caught by the trust gate (rejected) → no intent; value never echoed.
    assert not out["repair_intent_id"]
    assert "ghp_" not in json.dumps(out)


def test_idempotent_verify(env):
    job_id, fid = _job(env)
    out = _intake(env, job_id, fid, _GOOD)
    trid = out["trust_report_id"]
    r1 = run_grouped_cli(["provider", "verify", job_id, trid, "--json"], env)
    r2 = run_grouped_cli(["provider", "verify", job_id, trid, "--json"], env)
    d1, d2 = json.loads(r1.stdout), json.loads(r2.stdout)
    assert d1["verification_id"] == d2["verification_id"]
