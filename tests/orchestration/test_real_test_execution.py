"""Real Test Execution + Snapshot/Rollback Proof v1 tests (Steps 1895).

Unit (models, allowed-command resolution, policy blocking, honest snapshot/rollback proof, integrity,
audit, redaction) + architecture guards. The facade delegates execution to the existing safe runner;
these tests never execute the real test suite (they exercise policy-block + proof + integrity paths).
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from uuid import uuid4

import pytest

from packages.orchestration import real_test_execution as rte


def _job(env: Path, *, files: dict[str, str] | None = None, repo: bool = True) -> str:
    from packages.core.models import Job, RunState, Task
    from packages.orchestration.storage import save_job
    meta: dict = {}
    if repo:
        rp = env / f"repo-{uuid4().hex[:6]}"
        rp.mkdir(parents=True)
        for rel, content in (files or {"a.py": "x = 1\n"}).items():
            (rp / rel).write_text(content)
        meta["target_repo"] = str(rp)
    job = Job(id=uuid4(), name="m", user_prompt="x", state=RunState.RUNNING,
              tasks=[Task(description="t")], artifacts=[], metadata=meta)
    save_job(job, root=env)
    return str(job.id)


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    return d


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class TestModels:
    def test_result_roundtrip_scrubs(self):
        r = rte.TestRunResult(test_run_id="t1", job_id="j", safe_summary="ok /home/u/.env sk-ant-x" )
        d = rte.export_test_run_result_json(r)
        assert d["test_run_id"] == "t1" and d["schema_version"]
        assert "/home/u" not in d["safe_summary"]

    def test_snapshot_proof_metadata_no_restore(self):
        s = rte.SnapshotProof(snapshot_id="s1", strategy="metadata_only", restore_available=False)
        assert rte.export_snapshot_proof_json(s)["restore_available"] is False

    def test_argv_safety(self):
        assert rte._argv_is_safe(["python3", "-m", "pytest"])[0] is True
        assert rte._argv_is_safe(["pytest;", "rm", "-rf"])[0] is False
        assert rte._argv_is_safe(["rm", "-rf", "/"])[0] is False
        assert rte._argv_is_safe(["git", "push"])[0] is False
        assert rte._argv_is_safe(["sh", "-c", "echo $X"])[0] is False


# ---------------------------------------------------------------------------
# Allowed command resolution + policy blocking
# ---------------------------------------------------------------------------


class TestAllowedCommand:
    def test_unknown_command_blocked(self, env):
        jid = _job(env)
        ok, _c, reason = rte.resolve_allowed_command(jid, "no.such.command", data_dir=env)
        assert ok is False and "unknown" in reason

    def test_no_repo_blocked(self, env):
        jid = _job(env, repo=False)
        ok, _c, reason = rte.resolve_allowed_command(jid, "x", data_dir=env)
        assert ok is False

    def test_empty_command_id_allowed(self, env):
        jid = _job(env)
        ok, cand, _r = rte.resolve_allowed_command(jid, "", data_dir=env)
        assert ok is True and cand is None  # runner will select

    def test_run_allowed_test_blocks_unknown_command(self, env):
        jid = _job(env)
        res = rte.run_allowed_test(jid, command_id="no.such.command", data_dir=env)
        assert res.status == rte.TestRunStatus.BLOCKED_BY_POLICY
        assert res.next_safe_action.startswith("remedy ")


# ---------------------------------------------------------------------------
# Snapshot / rollback proof — honesty
# ---------------------------------------------------------------------------


class TestProofs:
    def test_snapshot_metadata_only(self, env):
        jid = _job(env)
        sp = rte.create_snapshot_proof(jid, data_dir=env)
        assert sp.strategy == "metadata_only"
        assert sp.restore_available is False
        assert sp.tracked_files_hash

    def test_snapshot_no_repo_unavailable(self, env):
        jid = _job(env, repo=False)
        sp = rte.create_snapshot_proof(jid, data_dir=env)
        assert sp.restore_available is False

    def test_rollback_proof_honest(self, env):
        jid = _job(env)
        sp = rte.create_snapshot_proof(jid, data_dir=env)
        rb = rte.create_rollback_proof(jid, sp.snapshot_id, data_dir=env)
        assert rb.restore_available is False  # metadata snapshot → no restore
        assert rb.restore_tested is False
        assert rb.limitations

    def test_snapshot_show_list_roundtrip(self, env):
        jid = _job(env)
        sp = rte.create_snapshot_proof(jid, data_dir=env)
        assert rte.get_snapshot_proof(sp.snapshot_id, data_dir=env) is not None
        assert len(rte.list_snapshot_proofs(job_id=jid, data_dir=env)) == 1


# ---------------------------------------------------------------------------
# Integrity + audit
# ---------------------------------------------------------------------------


class TestIntegrity:
    def test_clean_passes(self, env):
        jid = _job(env)
        sp = rte.create_snapshot_proof(jid, data_dir=env)
        rte.create_rollback_proof(jid, sp.snapshot_id, data_dir=env)
        ig = rte.test_execution_integrity(data_dir=env)
        assert ig["passed"] is True

    def test_audit_passed_with_nonzero_exit(self):
        bad = {"test_run_id": "t", "status": "passed", "exit_code": 1}
        codes = {v["code"] for v in rte.audit_test_run_safety(bad)}
        assert "passed_with_nonzero_exit" in codes

    def test_audit_rollback_restore_on_metadata(self):
        snaps = {"s1": {"snapshot_id": "s1", "strategy": "metadata_only"}}
        rb = {"rollback_proof_id": "r", "snapshot_id": "s1", "restore_available": True}
        codes = {v["code"] for v in rte.audit_rollback_safety(rb, snaps)}
        assert "restore_available_on_metadata_snapshot" in codes

    def test_audit_restore_tested_without_available(self):
        rb = {"rollback_proof_id": "r", "snapshot_id": "s", "restore_tested": True,
              "restore_available": False}
        codes = {v["code"] for v in rte.audit_rollback_safety(rb, {})}
        assert "restore_tested_without_available" in codes

    def test_integrity_flags_supplied_bad_run(self, env):
        ig = rte.test_execution_integrity(
            data_dir=env, test_runs=[{"test_run_id": "t", "status": "passed", "exit_code": 2}])
        assert ig["passed"] is False


# ---------------------------------------------------------------------------
# Mission gate consumption (Step 1886)
# ---------------------------------------------------------------------------


class TestMissionGates:
    def test_snapshot_gate_blocks_without_snapshot(self, env, monkeypatch):
        from packages.orchestration import overnight_mission as om
        rf = env.parent / "lr.md"; rf.write_text("## Verdict\nPASS\n")
        monkeypatch.setenv("REMEDY_REVIEW_FILE", str(rf))
        jid = _job(env)
        c = om.create_mission_contract_from_job(
            jid, acceptance_criteria=["done"],
            required_gates=[om.GATE_CLEAN_REVIEW, om.GATE_SNAPSHOT_BEFORE_APPLY], data_dir=env)
        e = om.evaluate_mission_contract(c, data_dir=env)
        assert e.satisfied is False
        assert any("snapshot_before_apply" in m for m in e.missing_proofs)

    def test_snapshot_gate_satisfied_after_snapshot(self, env, monkeypatch):
        from packages.orchestration import overnight_mission as om
        rf = env.parent / "lr.md"; rf.write_text("## Verdict\nPASS\n")
        monkeypatch.setenv("REMEDY_REVIEW_FILE", str(rf))
        jid = _job(env)
        rte.create_snapshot_proof(jid, data_dir=env)
        c = om.create_mission_contract_from_job(
            jid, acceptance_criteria=["done"],
            required_gates=[om.GATE_CLEAN_REVIEW, om.GATE_SNAPSHOT_BEFORE_APPLY], data_dir=env)
        e = om.evaluate_mission_contract(c, data_dir=env)
        assert not any("snapshot_before_apply" in m for m in e.missing_proofs)

    def test_rollback_gate_blocks_metadata_only(self, env, monkeypatch):
        from packages.orchestration import overnight_mission as om
        rf = env.parent / "lr.md"; rf.write_text("## Verdict\nPASS\n")
        monkeypatch.setenv("REMEDY_REVIEW_FILE", str(rf))
        jid = _job(env)
        sp = rte.create_snapshot_proof(jid, data_dir=env)
        rte.create_rollback_proof(jid, sp.snapshot_id, data_dir=env)
        c = om.create_mission_contract_from_job(
            jid, acceptance_criteria=["done"],
            required_gates=[om.GATE_CLEAN_REVIEW, om.GATE_ROLLBACK_RESTORE], data_dir=env)
        e = om.evaluate_mission_contract(c, data_dir=env)
        assert e.satisfied is False
        assert any("rollback_restore" in m for m in e.missing_proofs)


# ---------------------------------------------------------------------------
# Architecture guards (Step 1895)
# ---------------------------------------------------------------------------


class TestArchitectureGuards:
    def _src(self) -> str:
        p = Path(__file__).resolve().parents[2] / "packages" / "orchestration" / "real_test_execution.py"
        src = p.read_text(encoding="utf-8")
        src = re.sub(r'"""[\s\S]*?"""', "", src)
        src = re.sub(r"'''[\s\S]*?'''", "", src)
        src = re.sub(r'"(?:\\.|[^"\\])*"', '""', src)
        src = re.sub(r"'(?:\\.|[^'\\])*'", "''", src)
        return src

    def test_no_forbidden_in_facade(self):
        src = self._src()
        # The facade itself must contain no execution primitives — it delegates to the safe runner.
        for bad in ("import subprocess", "subprocess.", "shell=True", "os.system", "Popen",
                    "import requests", "import socket", "import ollama", "import openai",
                    "import anthropic", "faiss", "chromadb", "import numpy", "git "):
            assert bad not in src, bad

    def test_no_execution_or_apply(self):
        src = self._src()
        for bad in ("do_continue(", "apply_patch(", ".approve(", "eval(", "exec(", "os.fork"):
            assert bad not in src, bad
