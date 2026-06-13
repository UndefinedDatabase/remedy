"""Tests for remedy do --continue v1 (Steps 1164-1178)."""

from __future__ import annotations

import dataclasses
from pathlib import Path
from uuid import uuid4

import pytest

from packages.core.models import Artifact, ArtifactKind, Job, RunState, Task
from packages.orchestration.approval_queue import make_intent_id, set_approval_state
from packages.orchestration.permissions import Capability, set_permission
from packages.orchestration.run_contract import (
    build_default_run_contract, save_contract, ContractAction,
)
from packages.orchestration.storage import save_job


ARTIFACT_CONTENT = "Summary:\n  - safe doc\nProposed Changes:\n  - add a line\nNotes:\n  - none\n"


def make_continue_job(
    data_dir: Path,
    repo_root: Path,
    *,
    approve: bool = True,
    write_perm: bool = True,
    test_perm: bool = True,
    allow_apply: bool = True,
    stop_before_apply: bool = False,
    max_test_runs: int = 1,
    target_path: str = "docs/CHANGES.md",
    extra_intents: int = 0,
):
    """Build a continuation-ready job. Returns (job, intent_id)."""
    repo_root.mkdir(parents=True, exist_ok=True)
    task = Task(description="Continue task")
    explanations = [
        {"file": target_path, "action": "create", "risk": "low",
         "reason": "", "summary": "safe doc"}
    ]
    for n in range(extra_intents):
        explanations.append(
            {"file": f"docs/EXTRA{n}.md", "action": "create", "risk": "low",
             "reason": "", "summary": "extra"}
        )
    art = Artifact(
        name="build", content=ARTIFACT_CONTENT, kind=ArtifactKind.BUILDER_PROPOSAL,
        task_id=task.id,
        metadata={"patch_intent_explanations": explanations, "patch_intent_approvals": {}},
    )
    job = Job(
        id=uuid4(), name="cont-job", user_prompt="continue", state=RunState.RUNNING,
        tasks=[task], artifacts=[art],
        metadata={"target_repo": str(repo_root.resolve())},
    )
    intent_id = make_intent_id(art.id, 0)
    if write_perm:
        set_permission(job, Capability.repo_generated_write, allow=True)
    if test_perm:
        set_permission(job, Capability.repo_test_run, allow=True)
    if approve:
        set_approval_state(job, intent_id, "approved", decided_by="human")
        for n in range(extra_intents):
            set_approval_state(job, make_intent_id(art.id, n + 1), "approved", decided_by="human")

    contract = build_default_run_contract(job)
    allowed = list(contract.allowed_actions)
    denied = [a for a in contract.denied_actions if a != ContractAction.PATCH_APPLY]
    if allow_apply and ContractAction.PATCH_APPLY not in allowed:
        allowed.append(ContractAction.PATCH_APPLY)
    contract = dataclasses.replace(
        contract,
        allowed_actions=tuple(allowed),
        denied_actions=tuple(denied),
        stop_before_apply=stop_before_apply,
        max_test_runs=max_test_runs,
    )
    save_contract(job, contract)
    save_job(job, root=data_dir)
    return job, intent_id


@pytest.fixture()
def env(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"; data_dir.mkdir()
    repo = tmp_path / "repo"; repo.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir, repo


# ---------------------------------------------------------------------------
# Eligibility (Step 1165)
# ---------------------------------------------------------------------------


class TestEligibility:
    def _elig(self, job, data_dir, intent_id=None):
        from packages.orchestration.do_continue import evaluate_continue_eligibility
        return evaluate_continue_eligibility(str(job.id), intent_id, data_dir)

    def test_eligible_happy_path(self, env):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo)
        e = self._elig(job, data_dir)
        assert e.eligible is True
        assert e.intent_id == iid
        assert e.blockers == []

    def test_job_not_found(self, env):
        data_dir, _ = env
        from packages.orchestration.do_continue import evaluate_continue_eligibility
        e = evaluate_continue_eligibility(str(uuid4()), None, data_dir)
        assert not e.eligible
        assert "job_not_found" in e.blockers

    def test_no_approved_intent(self, env):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo, approve=False)
        e = self._elig(job, data_dir)
        assert not e.eligible
        assert "no_approved_intent" in e.blockers

    def test_multiple_approved_intents(self, env):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo, extra_intents=1)
        e = self._elig(job, data_dir)
        assert not e.eligible
        assert "multiple_approved_intents" in e.blockers
        assert "--intent-id" in e.next_safe_action

    def test_explicit_intent_id_resolves(self, env):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo, extra_intents=1)
        e = self._elig(job, data_dir, intent_id=iid)
        assert e.eligible is True
        assert e.intent_id == iid

    def test_permission_denied(self, env):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo, write_perm=False)
        e = self._elig(job, data_dir)
        assert not e.eligible
        assert "permission_denied" in e.blockers

    def test_contract_apply_denied(self, env):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo, allow_apply=False)
        e = self._elig(job, data_dir)
        assert not e.eligible
        assert "contract_apply_denied" in e.blockers

    def test_stop_before_apply_true(self, env):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo, stop_before_apply=True)
        e = self._elig(job, data_dir)
        assert not e.eligible
        assert "stop_before_apply_true" in e.blockers

    def test_no_target_repo(self, env):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo)
        job.metadata["target_repo"] = ""
        save_job(job, root=data_dir)
        e = self._elig(job, data_dir)
        assert not e.eligible
        assert "no_target_repo" in e.blockers

    def test_test_budget_unconfigured(self, env):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo, max_test_runs=0)
        e = self._elig(job, data_dir)
        assert not e.eligible
        assert "test_budget_unconfigured" in e.blockers

    def test_test_permission_missing(self, env):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo, test_perm=False)
        e = self._elig(job, data_dir)
        assert not e.eligible
        assert "test_permission_missing" in e.blockers

    def test_blocked_has_next_safe_action(self, env):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo, approve=False)
        e = self._elig(job, data_dir)
        assert e.next_safe_action


# ---------------------------------------------------------------------------
# Orchestrator runtime + idempotency (Steps 1169-1178)
# ---------------------------------------------------------------------------


def _fake_test(data_dir, *, status="passed", evidence="complete", fa_id=""):
    """Build a fake execute_test_run that emits a linked test event."""
    from uuid import UUID as _UUID
    from packages.orchestration.timeline import append_run_event
    from packages.orchestration.test_execution_service import TestExecutionResult
    calls = {"n": 0}

    def _fn(request):
        calls["n"] += 1
        append_run_event(data_dir, _UUID(request.job_id), event="test_run_completed",
                         metadata={"intent_id": request.intent_id, "status": status,
                                   "exit_code": 0 if status == "passed" else 1,
                                   "timestamp": "2030-01-01T00:00:00+00:00"})
        return TestExecutionResult(
            job_id=request.job_id, status=status, test_run_id="tr-1",
            evidence_status=evidence, failure_artifact_id=fa_id,
        )
    return _fn, calls


class TestRunDoContinue:
    def _run(self, data_dir, job, monkeypatch, *, status="passed", evidence="complete", fa_id=""):
        from packages.orchestration import do_continue as dc
        import packages.orchestration.test_execution_service as tes
        fn, calls = _fake_test(data_dir, status=status, evidence=evidence, fa_id=fa_id)
        monkeypatch.setattr(tes, "execute_test_run", fn)
        result = dc.run_do_continue(dc.ContinueRequest(job_id=str(job.id)), data_dir)
        return result, calls

    def test_passing_test_completed_verified(self, env, monkeypatch):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo)
        result, calls = self._run(data_dir, job, monkeypatch)
        from packages.orchestration.do_continue import ContinueStopReason
        assert result.stop_reason == ContinueStopReason.COMPLETED_VERIFIED
        assert result.proof_status == "verified"
        assert result.evidence_status == "complete"
        assert result.apply_id == iid
        assert result.snapshot_id
        assert calls["n"] == 1

    def test_failing_test_repair_available(self, env, monkeypatch):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo)
        result, calls = self._run(data_dir, job, monkeypatch, status="failed", fa_id="fa-1")
        from packages.orchestration.do_continue import ContinueStopReason
        assert result.stop_reason == ContinueStopReason.TEST_FAILED_REPAIR_AVAILABLE
        assert "repair start" in result.next_safe_action
        assert "fa-1" in result.next_safe_action

    def test_timeout_repair_available(self, env, monkeypatch):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo)
        result, calls = self._run(data_dir, job, monkeypatch, status="timeout", fa_id="fa-2")
        from packages.orchestration.do_continue import ContinueStopReason
        assert result.stop_reason == ContinueStopReason.TEST_FAILED_REPAIR_AVAILABLE

    def test_ineligible_blocks(self, env, monkeypatch):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo, approve=False)
        result, calls = self._run(data_dir, job, monkeypatch)
        from packages.orchestration.do_continue import ContinueStopReason
        assert result.stop_reason == ContinueStopReason.BLOCKED_INELIGIBLE
        assert calls["n"] == 0  # never ran a test

    def test_evidence_degraded_not_verified(self, env, monkeypatch):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo)
        result, calls = self._run(data_dir, job, monkeypatch, evidence="failed")
        from packages.orchestration.do_continue import ContinueStopReason
        assert result.stop_reason == ContinueStopReason.EVIDENCE_INCOMPLETE
        assert result.evidence_status == "degraded"
        assert result.stop_reason != ContinueStopReason.COMPLETED_VERIFIED

    def test_retry_no_double_apply_or_test(self, env, monkeypatch):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo)
        from packages.orchestration import do_continue as dc
        import packages.orchestration.test_execution_service as tes
        import packages.orchestration.patch_apply as pa
        fn, tcalls = _fake_test(data_dir, status="passed")
        monkeypatch.setattr(tes, "execute_test_run", fn)
        acalls = {"n": 0}
        orig_apply = pa.apply_patch_intent
        def _counting_apply(job_, iid_, **kw):
            acalls["n"] += 1
            return orig_apply(job_, iid_, **kw)
        monkeypatch.setattr(pa, "apply_patch_intent", _counting_apply)

        r1 = dc.run_do_continue(dc.ContinueRequest(job_id=str(job.id)), data_dir)
        r2 = dc.run_do_continue(dc.ContinueRequest(job_id=str(job.id)), data_dir)
        # Apply ran once; second cycle resumed. Test budget consumed once.
        assert acalls["n"] == 1
        assert tcalls["n"] == 1
        assert r1.stop_reason == r2.stop_reason == "completed_verified"

    def test_retry_after_apply_runs_test_once(self, env, monkeypatch):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo)
        # Apply manually (simulate crash after apply, before test).
        from packages.orchestration.patch_apply import apply_patch_intent
        from packages.orchestration.storage import load_job
        from uuid import UUID
        apply_patch_intent(load_job(UUID(str(job.id)), data_dir), iid, data_dir=data_dir)
        # Now continue — should resume apply, run test exactly once.
        result, calls = self._run(data_dir, job, monkeypatch)
        assert calls["n"] == 1
        # Apply phase should be 'resumed', not re-applied.
        apply_phase = next(p for p in result.phases if p.phase == "apply")
        assert apply_phase.status == "resumed"

    def test_active_lease_blocks(self, env, monkeypatch):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo)
        from packages.orchestration.do_continue import (
            ContinuationLease, _continue_dir, _repo_key, ContinueStopReason,
        )
        lease = ContinuationLease(
            job_id=str(job.id), repo_key=_repo_key(job), intent_id=iid,
            lease_dir=_continue_dir(str(job.id), data_dir) / "leases",
        )
        assert lease.acquire()
        try:
            result, calls = self._run(data_dir, job, monkeypatch)
            assert result.stop_reason == ContinueStopReason.BLOCKED_INELIGIBLE
            assert calls["n"] == 0
        finally:
            lease.release()

    def test_no_traceback_or_raw_content(self, env, monkeypatch):
        import json as _json
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo)
        result, _ = self._run(data_dir, job, monkeypatch)
        from packages.orchestration.do_continue import export_continue_result_json
        blob = _json.dumps(export_continue_result_json(result))
        assert "Traceback" not in blob
        assert str(repo.resolve()) not in blob
        assert str(data_dir) not in blob
        assert "blob_" not in blob

    def test_json_export_keys(self, env, monkeypatch):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo)
        result, _ = self._run(data_dir, job, monkeypatch)
        from packages.orchestration.do_continue import export_continue_result_json
        d = export_continue_result_json(result)
        for k in ("job_id", "intent_id", "apply_id", "snapshot_id", "test_run_id",
                  "stop_reason", "proof_status", "evidence_status", "phases",
                  "usage_before", "usage_after", "next_safe_action"):
            assert k in d


# ---------------------------------------------------------------------------
# Continuation integrations: Progress / Feature / Review (Steps 1176-1177)
# ---------------------------------------------------------------------------


class TestContinuationIntegrations:
    def _run(self, data_dir, job, monkeypatch, *, status="passed", fa_id=""):
        from packages.orchestration import do_continue as dc
        import packages.orchestration.test_execution_service as tes
        fn, _ = _fake_test(data_dir, status=status, fa_id=fa_id)
        monkeypatch.setattr(tes, "execute_test_run", fn)
        return dc.run_do_continue(dc.ContinueRequest(job_id=str(job.id)), data_dir)

    def test_progress_ledger_has_continuation_items(self, env, monkeypatch):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo)
        self._run(data_dir, job, monkeypatch)
        from packages.orchestration.storage import load_job
        from packages.orchestration.timeline import load_run_events
        from packages.orchestration.progress_ledger import build_progress_ledger
        from uuid import UUID
        job = load_job(UUID(str(job.id)), data_dir)
        events = load_run_events(data_dir, UUID(str(job.id)))
        ledger = build_progress_ledger(job=job, events=events)
        ids = [i.item_id for i in ledger.items]
        assert any(i.startswith("cont-") for i in ids)
        assert "cont-test-pass" in ids
        assert "cont-proof" in ids

    def test_feature_planner_failed_continuation_repair(self, env, monkeypatch):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo)
        self._run(data_dir, job, monkeypatch, status="failed", fa_id="fa-1")
        from packages.orchestration.storage import load_job
        from packages.orchestration.timeline import load_run_events
        from packages.orchestration.progress_ledger import build_progress_ledger
        from packages.orchestration.feature_planner import build_feature_plan
        from uuid import UUID
        job = load_job(UUID(str(job.id)), data_dir)
        events = load_run_events(data_dir, UUID(str(job.id)))
        ledger = build_progress_ledger(job=job, events=events)
        plan = build_feature_plan(ledger)
        repair = [s for s in plan.suggestions if "repair start" in s.next_action]
        assert repair, "expected a repair-continuation suggestion"
        assert repair[0].priority.value == "high"

    def test_review_bundle_continuation_summary(self, env, monkeypatch):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo)
        self._run(data_dir, job, monkeypatch)
        from packages.orchestration.review_bundle import build_review_bundle
        import zipfile, json as _json
        result = build_review_bundle(str(job.id))
        with zipfile.ZipFile(result.output_path) as zf:
            raw = zf.read("continuation_summary.json").decode()
        summary = _json.loads(raw)
        assert summary["present"] is True
        assert summary["stop_reason"] == "completed_verified"
        assert summary["apply_status"] == "completed"
        assert str(repo.resolve()) not in raw
        assert "blob_" not in raw
        assert result.safety.is_safe


# ---------------------------------------------------------------------------
# Architecture guards (Step 1178)
# ---------------------------------------------------------------------------


class TestContinuationArchitecture:
    def _src(self):
        from pathlib import Path
        import packages.orchestration.do_continue as m
        return Path(m.__file__).read_text()

    def test_no_shell_true(self):
        assert "shell=True" not in self._src()

    def test_no_background_pytest_or_git_reset(self):
        src = self._src()
        assert "git reset" not in src
        assert "git checkout" not in src
        assert "git clean" not in src

    def test_uses_central_services(self):
        src = self._src()
        # Apply, test, snapshot truth, and proof all go through central services.
        assert "apply_patch_intent" in src
        assert "execute_test_run" in src
        assert "build_snapshot_truth" in src
        assert "build_proof_chain" in src

    def test_no_auto_repair_or_revert(self):
        src = self._src()
        assert "revert_repository_apply" not in src   # no automatic revert
        assert "start_repair_loop" not in src          # no automatic repair


class TestCrashAtomicTestPhase:
    """R-0068: a crash between test start and confirmation must not re-run."""

    def test_in_flight_test_does_not_rerun(self, env, monkeypatch):
        data_dir, repo = env
        job, iid = make_continue_job(data_dir, repo)
        # Apply first so the test phase is the one in flight.
        from packages.orchestration.patch_apply import apply_patch_intent
        from packages.orchestration.storage import load_job
        from uuid import UUID
        apply_patch_intent(load_job(UUID(str(job.id)), data_dir), iid, data_dir=data_dir)
        # Simulate a crash mid-test: an in_flight TEST checkpoint with no completion.
        from packages.orchestration import do_continue as dc
        dc.save_checkpoint(str(job.id), data_dir, dc.ContinueCheckpoint(
            phase=dc.ContinuePhase.TEST, status="in_flight",
            at="2030-01-01T00:00:00+00:00", ids={"apply_id": iid},
        ))
        import packages.orchestration.test_execution_service as tes
        fn, calls = _fake_test(data_dir, status="passed")
        monkeypatch.setattr(tes, "execute_test_run", fn)
        result = dc.run_do_continue(dc.ContinueRequest(job_id=str(job.id)), data_dir)
        # Never re-ran the test; never claimed success.
        assert calls["n"] == 0
        assert result.stop_reason == dc.ContinueStopReason.EVIDENCE_INCOMPLETE
        assert result.evidence_status == "degraded"
        assert result.stop_reason != "completed_verified"
