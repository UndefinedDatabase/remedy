"""Bounded Overnight Executor v0 tests (Steps 1294-1296).

Models/policy/selection/adapters/idempotency/checkpoints/lease/stop-reasons,
redaction, and architecture guards for the FOREGROUND, explicitly-invoked,
at-most-one-cycle executor. No daemon/scheduler/background/loop, no provider, no
subprocess for command execution.
"""
from __future__ import annotations

import json
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from packages.core.models import Artifact, ArtifactKind, Job, Task
from packages.orchestration import overnight_executor as OX
from packages.orchestration import repair_loop as RL
from packages.orchestration.storage import load_job, save_job


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    # Default: a clean PASS review so non-review tests are not blocked by the gate.
    rf = tmp_path / "review_pass.md"
    rf.write_text("# Live Review\n\n## Verdict\nPASS — clean\n")
    monkeypatch.setenv("REMEDY_REVIEW_FILE", str(rf))
    return d


def _job(data_dir, *, tasks=True):
    t = [Task(description="t")] if tasks else []
    job = Job(id=uuid4(), name="ov", tasks=t, metadata={"target_repo": "."},
              permissions={"repo_generated_write": "allow", "repo_test_run": "allow"})
    save_job(job, root=data_dir)
    return job


def _add_failure(data_dir, job, *, resolved=False, related_files=None, safe_summary="fail"):
    t = job.tasks[0]
    fa = Artifact(name="tf", content="x", kind=ArtifactKind.VERIFICATION, task_id=t.id,
                  metadata={"test_failure": True, "failure_kind": "test_failed",
                            "related_test_run_id": "tr", "related_apply_id": "ap",
                            "related_task_id": str(t.id), "exit_code": 1,
                            "safe_summary": safe_summary, "related_files": related_files or [],
                            **({"failure_resolved": True} if resolved else {})})
    job.artifacts.append(fa)
    save_job(job, root=data_dir)
    return str(fa.id)


def _run(job_id, data_dir, **policy_kw):
    pol = OX.build_executor_policy(**policy_kw)
    return OX.run_overnight_executor(OX.OvernightRunRequest(job_id=job_id, policy=pol), data_dir)


# ---------------------------------------------------------------------------
# Policy (Step 1277)
# ---------------------------------------------------------------------------


class TestPolicy:
    def test_default_not_permitted(self):
        assert OX.executor_execution_permitted(OX.build_executor_policy()) is False

    def test_apply_requires_one_cycle(self):
        # apply flag alone (no --allow-one-cycle) must NOT enable execution.
        assert OX.executor_execution_permitted(
            OX.build_executor_policy(allow_apply=True)) is False

    def test_one_cycle_apply_permitted(self):
        p = OX.build_executor_policy(allow_one_cycle=True, allow_apply=True)
        assert OX.executor_execution_permitted(p) is True
        assert p.max_cycles == 1

    def test_one_cycle_repair_propose_permitted(self):
        assert OX.executor_execution_permitted(
            OX.build_executor_policy(allow_one_cycle=True, allow_repair_propose=True)) is True

    def test_one_cycle_no_action_not_permitted(self):
        # --allow-one-cycle with no action flag → nothing may execute.
        assert OX.executor_execution_permitted(
            OX.build_executor_policy(allow_one_cycle=True)) is False


# ---------------------------------------------------------------------------
# Report-only + models (Steps 1276/1283)
# ---------------------------------------------------------------------------


class TestReportOnly:
    def test_default_run_is_report_only(self, env):
        job = _job(env)
        r = _run(str(job.id), env)
        assert r.mode == OX.OvernightExecutionMode.REPORT_ONLY
        assert r.executed_action.get("kind") == OX.OvernightActionKind.NONE
        assert r.stop_reason in OX._CANONICAL_STOP_REASONS

    def test_flags_without_one_cycle_stay_report_only(self, env):
        job = _job(env)
        r = _run(str(job.id), env, allow_apply=True)  # no allow_one_cycle
        assert r.mode == OX.OvernightExecutionMode.REPORT_ONLY
        assert r.executed_action.get("kind") == OX.OvernightActionKind.NONE

    def test_record_persisted_and_appended(self, env):
        job = _job(env)
        _run(str(job.id), env)
        _run(str(job.id), env)
        recs = OX.list_run_records(str(job.id), env)
        assert len(recs) == 2  # append-only, never overwritten
        assert all(rec.get("run_id") for rec in recs)

    def test_checkpoints_durable(self, env):
        job = _job(env)
        r = _run(str(job.id), env)
        cps = OX.load_overnight_checkpoints(str(job.id), r.run_id, env)
        phases = {c.phase for c in cps}
        assert OX.OvernightExecutionPhase.REQUESTED in phases
        assert OX.OvernightExecutionPhase.STOPPED in phases

    def test_job_not_found_safe(self, env):
        r = _run(str(uuid4()), env)
        assert r.stop_reason == OX.OvernightStopReason.UNSUPPORTED_STATE
        assert r.evidence_status == "unknown"

    def test_export_shapes(self, env):
        job = _job(env)
        r = _run(str(job.id), env)
        rec = OX.export_run_record_json(r)
        res = OX.export_run_result_json(r)
        assert rec["run_id"] == r.run_id
        assert "readiness_before" in res and "readiness_after" in res
        assert res["record_path"].startswith("overnight_runs/")
        assert "/home/" not in res["record_path"]


# ---------------------------------------------------------------------------
# Stop reasons + no fake next action (Steps 1281/1286)
# ---------------------------------------------------------------------------


class TestStopReasonsAndSelection:
    def test_stop_reason_canonical(self, env):
        job = _job(env)
        _add_failure(env, job)
        r = _run(str(job.id), env)
        assert r.stop_reason in OX._CANONICAL_STOP_REASONS

    def test_selected_command_catalog_backed(self, env):
        from packages.orchestration.do_run import validate_next_safe_action_command
        job = _job(env)
        _add_failure(env, job)
        r = _run(str(job.id), env)
        cmd = r.selected_action.get("command", "")
        assert cmd  # there is a real action
        assert validate_next_safe_action_command(cmd)

    def test_no_command_for_empty_job(self, env):
        job = _job(env)
        r = _run(str(job.id), env)
        # No approved intent / failure → review action only, never a fabricated apply.
        assert "do continue" not in r.selected_action.get("command", "")
        assert "repair propose" not in r.selected_action.get("command", "")


# ---------------------------------------------------------------------------
# Review-findings source (Step 1285)
# ---------------------------------------------------------------------------


class TestReviewFindings:
    def _write(self, tmp_path, body):
        p = tmp_path / "lr.md"
        p.write_text(body)
        return p

    def test_pass_not_blocking(self, tmp_path):
        p = self._write(tmp_path, "## Verdict\nPASS — clean\n")
        f = OX.parse_review_findings(p)
        assert f.verdict == "pass"
        assert OX.review_findings_block_execution(f)[0] is False

    def test_pass_with_risks_low_only_allows(self, tmp_path):
        p = self._write(tmp_path, "## Verdict\nPASS WITH RISKS\n\n"
                                  "### R-0001: x\n- **Status**: Open\n- **Severity**: Low\n")
        f = OX.parse_review_findings(p)
        assert f.verdict == "pass_with_risks"
        assert f.open_low == 1 and f.open_blocker_or_high == 0
        assert OX.review_findings_block_execution(f)[0] is False

    def test_pending_blocks(self, tmp_path):
        f = OX.parse_review_findings(self._write(tmp_path, "## Verdict\nPENDING\n"))
        assert OX.review_findings_block_execution(f) == (True, OX.OvernightStopReason.REVIEW_FINDINGS_OPEN)

    def test_fail_blocks(self, tmp_path):
        f = OX.parse_review_findings(self._write(tmp_path, "## Verdict\nFAIL\n"))
        assert OX.review_findings_block_execution(f)[0] is True

    def test_open_blocker_blocks(self, tmp_path):
        p = self._write(tmp_path, "## Verdict\nPASS\n\n"
                                  "### R-0009: bad\n- **Status**: Open\n- **Severity**: Blocker\n")
        f = OX.parse_review_findings(p)
        assert f.open_blocker == 1
        assert OX.review_findings_block_execution(f)[0] is True

    def test_missing_file_unknown_blocks(self, tmp_path):
        f = OX.parse_review_findings(tmp_path / "nope.md")
        assert f.verdict == "unknown" and f.source == "unavailable"
        assert OX.review_findings_block_execution(f)[0] is True

    def test_resolved_finding_not_counted_open(self, tmp_path):
        p = self._write(tmp_path, "## Verdict\nPASS\n\n"
                                  "### R-0002: x\n- **Status**: Resolved\n- **Severity**: High\n")
        f = OX.parse_review_findings(p)
        assert f.open_high == 0


# ---------------------------------------------------------------------------
# Policy gate (Step 1284)
# ---------------------------------------------------------------------------


class TestPolicyGate:
    def test_pending_review_blocks_execution(self, env, tmp_path, monkeypatch):
        # Even with one-cycle apply flags, a PENDING review blocks execution.
        pend = tmp_path / "pend.md"; pend.write_text("## Verdict\nPENDING\n")
        monkeypatch.setenv("REMEDY_REVIEW_FILE", str(pend))
        job = _job(env)
        _add_failure(env, job)
        r = _run(str(job.id), env, allow_one_cycle=True, allow_repair_propose=True)
        assert r.executed_action.get("kind") == OX.OvernightActionKind.NONE
        assert r.stop_reason == OX.OvernightStopReason.REVIEW_FINDINGS_OPEN

    def test_budget_exhausted_blocks_apply(self, env):
        # An exhausted test/loop budget blocks an apply cycle before any execution.
        from packages.orchestration.run_contract import load_usage, save_usage
        from tests.orchestration.test_do_continue import make_continue_job
        repo = env.parent / "repo"; repo.mkdir(exist_ok=True)
        job, _ = make_continue_job(env, repo, max_test_runs=1)
        u = load_usage(job); u.test_runs_used = 1; u.loops_used = 99; save_usage(job, u)
        save_job(job, root=env)
        r = _run(str(job.id), env, allow_one_cycle=True, allow_apply=True)
        assert r.executed_action.get("kind") == OX.OvernightActionKind.NONE
        assert r.stop_reason == OX.OvernightStopReason.BUDGET_EXHAUSTED


# ---------------------------------------------------------------------------
# Repair propose adapter + idempotency (Steps 1282/1288)
# ---------------------------------------------------------------------------


class TestRepairProposeAdapter:
    def test_executes_repair_propose(self, env):
        job = _job(env)
        _add_failure(env, job)
        r = _run(str(job.id), env, allow_one_cycle=True, allow_repair_propose=True)
        assert r.executed_action.get("kind") == OX.OvernightActionKind.REPAIR_PROPOSE
        assert r.stop_reason == OX.OvernightStopReason.REPAIR_PENDING_APPROVAL
        assert r.executed_action.get("repair_intent_id")

    def test_repair_propose_idempotent(self, env):
        job = _job(env)
        _add_failure(env, job)
        r1 = _run(str(job.id), env, allow_one_cycle=True, allow_repair_propose=True)
        intent = r1.executed_action.get("repair_intent_id")
        assert intent
        # Second run: the proposal already exists and is pending approval. The
        # executor must NOT create a duplicate; it routes to the human approval.
        r2 = _run(str(job.id), env, allow_one_cycle=True, allow_repair_propose=True)
        j = load_job(UUID(str(job.id)), env)
        attempts = list(RL.load_repair_attempts(j).values())
        assert len(attempts) == 1  # no duplicate Fix Task / Repair Artifact / Intent
        assert r2.executed_action.get("kind") == OX.OvernightActionKind.NONE
        assert r2.stop_reason == OX.OvernightStopReason.HUMAN_APPROVAL_REQUIRED
        assert intent in r2.selected_action.get("command", "")

    def test_lease_released_no_leftover_locks(self, env):
        job = _job(env)
        _add_failure(env, job)
        _run(str(job.id), env, allow_one_cycle=True, allow_repair_propose=True)
        assert list(env.rglob("*.lock")) == []

    def test_action_checkpoints_durably_flushed(self, env):
        # R-0081: ACTION_STARTED/COMPLETED are flushed to disk around the action,
        # not only at finalize — durable trail survives a crash.
        job = _job(env)
        _add_failure(env, job)
        r = _run(str(job.id), env, allow_one_cycle=True, allow_repair_propose=True)
        cps = OX.load_overnight_checkpoints(str(job.id), r.run_id, env)
        phases = {c.phase for c in cps}
        assert OX.OvernightExecutionPhase.ACTION_STARTED in phases
        assert OX.OvernightExecutionPhase.ACTION_COMPLETED in phases
        assert OX.OvernightExecutionPhase.STOPPED in phases

    def test_executed_entity_equals_selected_entity(self, env):
        # R-0082: the proposed failure id is exactly the one in the selected command.
        job = _job(env)
        fa = _add_failure(env, job)
        r = _run(str(job.id), env, allow_one_cycle=True, allow_repair_propose=True)
        assert fa in r.selected_action.get("command", "")
        assert r.executed_action.get("kind") == OX.OvernightActionKind.REPAIR_PROPOSE
        # The repair attempt is keyed to that exact failure artifact.
        j = load_job(UUID(str(job.id)), env)
        attempts = list(RL.load_repair_attempts(j).values())
        assert len(attempts) == 1 and attempts[0].failure_artifact_id == fa


# ---------------------------------------------------------------------------
# do_continue adapter + idempotency (Steps 1282/1288)
# ---------------------------------------------------------------------------


class TestDoContinueAdapter:
    def _continue_job(self, env, monkeypatch):
        import packages.orchestration.test_execution_service as tes
        from tests.orchestration.test_do_continue import _fake_test, make_continue_job
        repo = env.parent / "repo"; repo.mkdir(exist_ok=True)
        job, iid = make_continue_job(env, repo)
        fn, _ = _fake_test(env, status="passed")
        monkeypatch.setattr(tes, "execute_test_run", fn)
        return job, iid

    def test_executes_one_cycle(self, env, monkeypatch):
        job, _ = self._continue_job(env, monkeypatch)
        r = _run(str(job.id), env, allow_one_cycle=True, allow_apply=True)
        assert r.executed_action.get("kind") == OX.OvernightActionKind.DO_CONTINUE
        assert r.stop_reason == OX.OvernightStopReason.COMPLETED_VERIFIED

    def test_retry_does_not_double_apply(self, env, monkeypatch):
        job, _ = self._continue_job(env, monkeypatch)
        OX.OvernightRunRequest  # noqa
        r1 = _run(str(job.id), env, allow_one_cycle=True, allow_apply=True)
        u_after_1 = r1.readiness_after.get("budget_summary", {}).get("test_runs_used")
        r2 = _run(str(job.id), env, allow_one_cycle=True, allow_apply=True)
        u_after_2 = r2.readiness_after.get("budget_summary", {}).get("test_runs_used")
        # Idempotent: the second run does not consume more test budget.
        assert u_after_1 == u_after_2
        assert r2.stop_reason == OX.OvernightStopReason.COMPLETED_VERIFIED

    def test_apply_without_flag_not_executed(self, env, monkeypatch):
        job, _ = self._continue_job(env, monkeypatch)
        r = _run(str(job.id), env, allow_one_cycle=True, allow_repair_propose=True)  # wrong flag
        assert r.executed_action.get("kind") == OX.OvernightActionKind.NONE


# ---------------------------------------------------------------------------
# Redaction (Step 1295)
# ---------------------------------------------------------------------------


class TestRedaction:
    def test_no_raw_leak(self, env):
        job = _job(env)
        _add_failure(env, job, related_files=["/home/u/.env", "/etc/passwd"],
                     safe_summary="token=sk-secret-123 Traceback (most recent call last)")
        r = _run(str(job.id), env, allow_one_cycle=True, allow_repair_propose=True)
        from packages.orchestration.progress_ledger import (
            extract_overnight_run_items,
        )
        from packages.orchestration.review_bundle import _build_overnight_run_summary
        from packages.orchestration.ui_server import _build_overnight_run_section
        rec = OX.load_run_record(str(job.id), r.run_id, env)
        items = extract_overnight_run_items(rec)
        blobs = [
            json.dumps(OX.export_run_result_json(r)),
            json.dumps(OX.export_run_record_json(r)),
            OX.render_overnight_run_report_markdown(r),
            json.dumps([{"id": i.item_id, "s": i.safe_summary} for i in items]),
            json.dumps(_build_overnight_run_summary(job, env)),
            json.dumps(_build_overnight_run_section(job, env)),
        ]
        for b in blobs:
            assert "/home/" not in b
            assert "/etc/passwd" not in b
            assert "Traceback" not in b
            assert "sk-secret-123" not in b
            assert "diff --git" not in b


# ---------------------------------------------------------------------------
# Architecture guards (Step 1296)
# ---------------------------------------------------------------------------


class TestArchitectureGuards:
    SRC = Path("packages/orchestration/overnight_executor.py").read_text()

    def _imports(self):
        return [ln for ln in self.SRC.splitlines()
                if ln.strip().startswith(("import ", "from "))]

    def test_no_subprocess(self):
        # No subprocess IMPORT or call (the word may appear in safe prose). No shell.
        for ln in self._imports():
            assert "subprocess" not in ln
        assert "import subprocess" not in self.SRC
        assert "subprocess.run" not in self.SRC and "subprocess.Popen" not in self.SRC
        assert "shell=True" not in self.SRC

    def test_no_provider_or_ollama(self):
        for ln in self._imports():
            assert "ollama" not in ln.lower()
            assert "provider" not in ln.lower()

    def test_no_direct_apply_or_test_execution_import(self):
        # Apply / test execution only via the do_continue service (not imported here).
        for ln in self._imports():
            assert "patch_apply" not in ln
            assert "source_apply" not in ln
            assert "test_execution_service" not in ln

    def test_no_scheduler_daemon_or_background(self):
        low = self.SRC.lower()
        for word in ("import schedule", "crontab", "import asyncio",
                     "threading", "multiprocessing", "daemon=true"):
            assert word not in low

    def test_no_git_or_arbitrary_command_execution(self):
        # The only ways to run git/arbitrary commands are subprocess/os.system —
        # neither is present, so no git commit/push/reset/checkout/clean is possible.
        assert "os.system" not in self.SRC
        assert "import subprocess" not in self.SRC

    def test_max_cycles_never_exceeds_one(self):
        # No code path constructs a policy that permits more than one cycle.
        assert "max_cycles=1" in self.SRC
        assert "max_cycles=2" not in self.SRC
