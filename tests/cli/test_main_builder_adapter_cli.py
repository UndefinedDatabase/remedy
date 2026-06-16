"""Runtime CLI tests for the Main Builder Adapter v0 (Step 1981).

Subprocess tests. adapter-list/show/enable, package-create, session-create/show/list,
session-record-output, session-intake, integrity. Safe JSON, safe errors, no tracebacks.
"""
from __future__ import annotations

import json
from uuid import uuid4

import pytest

from tests.cli.runtime_helpers import run_grouped_cli


def _job(env):
    from packages.core.models import Job, RunState, Task
    from packages.orchestration.storage import save_job
    repo = env / f"repo-{uuid4().hex[:6]}"
    repo.mkdir(parents=True)
    (repo / "a.py").write_text("x=1\n")
    job = Job(id=uuid4(), name="m", user_prompt="x", state=RunState.RUNNING,
              tasks=[Task(description="t")], metadata={"target_repo": str(repo)})
    save_job(job, root=env)
    return str(job.id)


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"
    d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    return d


def test_adapter_list(env):
    r = run_grouped_cli(["builder", "adapter-list", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["count"] == 5
    assert all(not a.get("allows_direct_repo_write") for a in d["adapters"])


def test_adapter_show(env):
    r = run_grouped_cli(["builder", "adapter-show", "claude-code-v0", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["adapter_id"] == "claude-code-v0"
    assert d["enabled"] is False


def test_adapter_enable_and_disable(env):
    r = run_grouped_cli(["builder", "adapter-enable", "claude-code-v0",
                          "--mode", "operator_launched", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["enabled"] is True
    assert d["mode"] == "operator_launched"
    # Disable
    r2 = run_grouped_cli(["builder", "adapter-enable", "claude-code-v0",
                           "--mode", "disabled", "--json"], env)
    d2 = json.loads(r2.stdout)
    assert d2["enabled"] is False


def test_package_create(env):
    jid = _job(env)
    r = run_grouped_cli(["builder", "package-create", jid, "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["job_id"] == jid
    assert d["package_id"]
    assert "UNTRUSTED" in d["expected_output_contract"]


def test_session_create_and_show(env):
    jid = _job(env)
    # Enable adapter first
    run_grouped_cli(["builder", "adapter-enable", "claude-code-v0",
                      "--mode", "operator_launched", "--json"], env)
    pkg = json.loads(run_grouped_cli(["builder", "package-create", jid, "--json"], env).stdout)
    r = run_grouped_cli(["builder", "session-create", pkg["package_id"],
                          "--adapter-id", "claude-code-v0", "--job-id", jid, "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    sid = d["session_id"]
    assert d["status"] in ("waiting_for_operator", "package_ready")
    # Show
    r2 = run_grouped_cli(["builder", "session-show", sid, "--json"], env)
    assert json.loads(r2.stdout)["session_id"] == sid


def test_session_list(env):
    jid = _job(env)
    r = run_grouped_cli(["builder", "session-list", jid, "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert "count" in d


def test_session_record_output_and_intake(env):
    jid = _job(env)
    run_grouped_cli(["builder", "adapter-enable", "claude-code-v0",
                      "--mode", "operator_launched", "--json"], env)
    pkg = json.loads(run_grouped_cli(["builder", "package-create", jid, "--json"], env).stdout)
    session = json.loads(run_grouped_cli(
        ["builder", "session-create", pkg["package_id"],
         "--adapter-id", "claude-code-v0", "--job-id", jid, "--json"], env).stdout)
    sid = session["session_id"]
    # Record output
    r = run_grouped_cli(["builder", "session-record-output", sid,
                          "--artifact-ref", "candidate-123", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["status"] == "candidate_received"
    # Intake
    r2 = run_grouped_cli(["builder", "session-intake", sid, "--json"], env)
    assert r2.returncode == 0, r2.stderr
    d2 = json.loads(r2.stdout)
    assert d2["status"] == "completed_intake_only"


def test_integrity(env):
    r = run_grouped_cli(["builder", "integrity", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["passed"] is True


def test_invalid_adapter_show(env):
    r = run_grouped_cli(["builder", "adapter-show", "nonexistent", "--json"], env)
    assert r.returncode == 1
    assert "Traceback" not in r.stderr


def test_invalid_session_show(env):
    r = run_grouped_cli(["builder", "session-show", "nonexistent", "--json"], env)
    assert r.returncode == 1
    assert "Traceback" not in r.stderr
