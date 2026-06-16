"""Approved Repair Apply Cycle tests (Steps 1221-1237).

A repair patch intent flows through the SAME `do continue` path (snapshot → apply
→ test → proof → stop). These tests prove: approved repair applies once, post-
repair test links, failure resolves only with proven evidence + source_fix,
docs-only never overclaims, idempotency, redaction, and architecture guards.
Reuses the do_continue tmp-repo harness.
"""
from __future__ import annotations

from pathlib import Path
from uuid import UUID

from packages.orchestration import do_continue as dc
from packages.orchestration import repair_loop as RL
from packages.orchestration.storage import load_job, save_job
from tests.orchestration.test_do_continue import _fake_test, env, make_continue_job  # noqa: F401


def _attach_repair(data_dir, job, intent_id, *, expected_effect):
    """Make the approved intent a repair intent: add a failure + RepairAttempt."""
    from packages.core.models import Artifact, ArtifactKind
    task_id = str(job.tasks[0].id)
    fa = Artifact(
        name="tf", content="fail", kind=ArtifactKind.VERIFICATION, task_id=job.tasks[0].id,
        metadata={
            "test_failure": True, "failure_kind": "test_failed",
            "related_test_run_id": "tr-orig", "related_apply_id": "ap-orig",
            "related_task_id": task_id, "exit_code": 1, "safe_summary": "orig fail",
            "related_files": [],
        },
    )
    job.artifacts.append(fa)
    save_job(job, root=data_dir)
    attempt = RL.RepairAttempt(
        attempt_id="att-" + intent_id[:6], job_id=str(job.id),
        failure_artifact_id=str(fa.id), repair_intent_id=intent_id,
        status="approval_required", expected_effect=expected_effect,
        repair_kind="source_fixture" if expected_effect == "source_fix" else "docs_fixture",
        source="cli_v1", created_at="t",
    )
    RL.save_repair_attempt(job, attempt)
    return str(fa.id), attempt.attempt_id


def _run(data_dir, job, monkeypatch, *, status="passed", evidence="complete", fa_id=""):
    import packages.orchestration.test_execution_service as tes
    fn, calls = _fake_test(data_dir, status=status, evidence=evidence, fa_id=fa_id)
    monkeypatch.setattr(tes, "execute_test_run", fn)
    result = dc.run_do_continue(dc.ContinueRequest(job_id=str(job.id)), data_dir)
    return result, calls


# ---------------------------------------------------------------------------
# Apply cycle (1223-1226)
# ---------------------------------------------------------------------------


class TestRepairApplyCycle:
    def test_source_fix_pass_resolves_failure(self, env, monkeypatch):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo)
        fa_id, att_id = _attach_repair(data_dir, job, iid, expected_effect="source_fix")
        result, calls = _run(data_dir, job, monkeypatch, status="passed")
        assert result.is_repair is True
        assert result.repair_attempt_id == att_id
        assert result.repair_status == "tested_passed"
        assert result.repair_resolved_failure is True
        assert calls["n"] == 1
        job2 = load_job(UUID(str(job.id)), data_dir)
        fa = next(a for a in job2.artifacts if str(a.id) == fa_id)
        assert fa.metadata.get("failure_resolved") is True
        assert fa.metadata.get("resolved_by_repair_attempt_id") == att_id

    def test_docs_only_pass_does_not_resolve(self, env, monkeypatch):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo)
        fa_id, att_id = _attach_repair(data_dir, job, iid, expected_effect="documentation_only")
        result, _ = _run(data_dir, job, monkeypatch, status="passed")
        assert result.is_repair is True
        assert result.repair_status == "tested_passed"
        assert result.repair_resolved_failure is False  # no overclaim
        job2 = load_job(UUID(str(job.id)), data_dir)
        fa = next(a for a in job2.artifacts if str(a.id) == fa_id)
        assert not fa.metadata.get("failure_resolved")

    def test_failing_repair_keeps_failure_open(self, env, monkeypatch):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo)
        fa_id, att_id = _attach_repair(data_dir, job, iid, expected_effect="source_fix")
        result, _ = _run(data_dir, job, monkeypatch, status="failed", fa_id="new-fa")
        assert result.repair_status == "tested_failed"
        assert result.repair_resolved_failure is False
        job2 = load_job(UUID(str(job.id)), data_dir)
        fa = next(a for a in job2.artifacts if str(a.id) == fa_id)
        assert not fa.metadata.get("failure_resolved")

    def test_normal_intent_not_repair(self, env, monkeypatch):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo)  # no repair attempt
        result, _ = _run(data_dir, job, monkeypatch, status="passed")
        assert result.is_repair is False
        assert result.repair_attempt_id == ""


# ---------------------------------------------------------------------------
# Proof awareness (1227)
# ---------------------------------------------------------------------------


class TestProofAwareness:
    def test_pending_repair_intent_not_verified(self, env):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo, approve=False)
        _attach_repair(data_dir, job, iid, expected_effect="source_fix")
        from packages.orchestration.proof_chain import PROOF_VERIFIED, build_proof_chain
        from packages.orchestration.timeline import load_run_events
        job2 = load_job(UUID(str(job.id)), data_dir)
        events = load_run_events(data_dir, UUID(str(job.id)))
        chain = build_proof_chain(job2, events, data_dir=data_dir)
        for c in chain.changes:
            if c.intent_id == iid:
                assert c.apply_state != "applied"
                assert c.proof_status != PROOF_VERIFIED


# ---------------------------------------------------------------------------
# Idempotency + crash resume (1234)
# ---------------------------------------------------------------------------


class TestIdempotency:
    def test_retry_no_double_apply_or_resolve(self, env, monkeypatch):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo)
        fa_id, att_id = _attach_repair(data_dir, job, iid, expected_effect="source_fix")
        r1, c1 = _run(data_dir, job, monkeypatch, status="passed")
        assert c1["n"] == 1 and r1.repair_resolved_failure is True
        # Re-run: resume, no second apply, no second test, still resolved once.
        r2, c2 = _run(data_dir, job, monkeypatch, status="passed")
        assert c2["n"] == 0  # test not re-run
        assert r2.repair_status == "tested_passed"
        job2 = load_job(UUID(str(job.id)), data_dir)
        attempts = RL.load_repair_attempts(job2)
        assert len(attempts) == 1
        fa = next(a for a in job2.artifacts if str(a.id) == fa_id)
        assert fa.metadata.get("resolved_by_test_run_id") == "tr-1"


# ---------------------------------------------------------------------------
# Redaction (1236)
# ---------------------------------------------------------------------------


class TestRedaction:
    def test_no_raw_leak_in_continue_result(self, env, monkeypatch):
        import json
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo)
        _attach_repair(data_dir, job, iid, expected_effect="source_fix")
        result, _ = _run(data_dir, job, monkeypatch, status="passed")
        blob = json.dumps(dc.export_continue_result_json(result))
        for bad in ("Traceback", "/home/", "diff --git", "BEGIN "):
            assert bad not in blob


# ---------------------------------------------------------------------------
# Architecture guards (1237)
# ---------------------------------------------------------------------------


class TestArchitectureGuards:
    def test_do_continue_uses_reconcile_not_repair_apply(self):
        src = Path("packages/orchestration/do_continue.py").read_text()
        assert "reconcile_repair_after_continue" in src
        # apply still happens via the central apply_patch_intent path.
        assert "apply_patch_intent" in src

    def test_repair_loop_no_apply_or_test_imports(self):
        src = Path("packages/orchestration/repair_loop.py").read_text()
        import_lines = [ln for ln in src.splitlines()
                        if ln.strip().startswith(("import ", "from "))]
        for ln in import_lines:
            assert "source_apply" not in ln
            assert "patch_apply" not in ln
            assert "test_execution_service" not in ln
            assert "provider" not in ln.lower()
        assert "shell=True" not in src

    def test_reconcile_next_actions_real(self):
        # The continue cycle's repair next actions use catalog commands.
        from packages.orchestration.do_run import validate_next_safe_action_command
        assert validate_next_safe_action_command("remedy patch approve j i")
        assert validate_next_safe_action_command("remedy repair propose j fa --json")
