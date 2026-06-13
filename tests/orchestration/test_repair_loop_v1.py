"""Repair Loop v1 tests (Steps 1195-1214).

Covers context builder, eligibility, attempt persistence, fix task, fixture
repair builder, repair patch intent, idempotency, proof/provenance alignment,
redaction, and architecture guards. No apply, no test execution, no provider.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from packages.core.models import Artifact, ArtifactKind, Job, RunState, Task
from packages.orchestration.storage import save_job, load_job
from packages.orchestration.test_failure_artifact import (
    TestFailureArtifact, persist_failure_artifact,
)
from packages.orchestration import repair_loop as RL
from packages.orchestration.approval_queue import get_patch_intent


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_job_with_failure(data_dir, *, failure_kind="test_failed", exit_code=1,
                           safe_summary="Test test_failed: exit 1", related_files=None):
    task = Task(description="orig task", status=RunState.COMPLETED)
    job = Job(
        name="repair-v1", tasks=[task],
        permissions={"repo_generated_write": "allow", "repo_test_run": "allow"},
        metadata={"target_repo": "."},
    )
    save_job(job, root=data_dir)
    fail = TestFailureArtifact(
        job_id=str(job.id), task_id=str(task.id), related_test_run_id="tr-abc12345",
        related_apply_id="ap-xyz", failing_phase="test", command_safe="pytest -q",
        exit_code=exit_code, safe_summary=safe_summary, failure_kind=failure_kind,
        related_files=related_files or [],
    )
    # persist_failure_artifact uses default root; re-save under data_dir explicitly.
    from packages.core.models import Artifact as _A
    art = _A(
        name=f"test-failure-{fail.artifact_id}", content=fail.safe_summary[:500],
        kind=ArtifactKind.VERIFICATION, task_id=task.id,
        metadata={
            "test_failure": True, "failure_kind": fail.failure_kind,
            "related_test_run_id": fail.related_test_run_id,
            "related_intent_id": "", "related_apply_id": fail.related_apply_id,
            "related_task_id": str(task.id), "failing_phase": "test",
            "command_safe": fail.command_safe, "exit_code": fail.exit_code,
            "related_files": fail.related_files, "safe_summary": fail.safe_summary,
        },
    )
    job.artifacts.append(art)
    save_job(job, root=data_dir)
    return str(job.id), str(art.id), str(task.id)


@pytest.fixture()
def data_dir(tmp_path, monkeypatch):
    d = tmp_path / "data"
    d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    return d


# ---------------------------------------------------------------------------
# Step 1195 — context
# ---------------------------------------------------------------------------


class TestRepairContext:
    def test_safe_summary_present(self, data_dir):
        jid, fa, _ = _make_job_with_failure(data_dir)
        ctx = RL.build_repair_context(jid, fa, data_dir)
        assert ctx.status == "context_ready"
        assert ctx.safe_summary
        assert ctx.failure_kind == "test_failed"
        assert ctx.command_display == "pytest -q"

    def test_missing_failure_blocks(self, data_dir):
        jid, _, _ = _make_job_with_failure(data_dir)
        ctx = RL.build_repair_context(jid, "does-not-exist", data_dir)
        assert ctx.status == "blocked"
        assert ctx.blocker == "failure_artifact_not_found"

    def test_stale_link_blocks(self, data_dir):
        jid, fa, _ = _make_job_with_failure(data_dir, exit_code=0)
        ctx = RL.build_repair_context(jid, fa, data_dir)
        assert ctx.status == "blocked"
        assert ctx.blocker == "stale_failure_link"

    def test_protected_paths_redacted(self, data_dir):
        jid, fa, _ = _make_job_with_failure(
            data_dir, related_files=["/home/secret/.env", "/etc/passwd", "src/app.py"])
        ctx = RL.build_repair_context(jid, fa, data_dir)
        # Only basenames, no absolute paths.
        for f in ctx.changed_files_safe:
            assert "/" not in f
        assert "app.py" in ctx.changed_files_safe


# ---------------------------------------------------------------------------
# Step 1196 — eligibility
# ---------------------------------------------------------------------------


class TestEligibility:
    def test_eligible(self, data_dir):
        jid, fa, _ = _make_job_with_failure(data_dir)
        elig = RL.evaluate_repair_eligibility(jid, fa, data_dir)
        assert elig.eligible
        assert not elig.blockers

    def test_missing_job(self, data_dir):
        from uuid import uuid4
        elig = RL.evaluate_repair_eligibility(str(uuid4()), "fa", data_dir)
        assert not elig.eligible
        assert "job_not_found" in elig.blockers
        assert elig.next_safe_action

    def test_missing_failure_artifact(self, data_dir):
        jid, _, _ = _make_job_with_failure(data_dir)
        elig = RL.evaluate_repair_eligibility(jid, "nope", data_dir)
        assert not elig.eligible
        assert "failure_artifact_not_found" in elig.blockers

    def test_already_resolved(self, data_dir):
        jid, fa, _ = _make_job_with_failure(data_dir, exit_code=0)
        elig = RL.evaluate_repair_eligibility(jid, fa, data_dir)
        assert not elig.eligible
        assert "failure_already_resolved" in elig.blockers

    def test_blocked_has_catalog_next_action(self, data_dir):
        from packages.orchestration.do_run import validate_next_safe_action_command
        jid, _, _ = _make_job_with_failure(data_dir)
        elig = RL.evaluate_repair_eligibility(jid, "nope", data_dir)
        assert validate_next_safe_action_command(elig.next_safe_action.command)


# ---------------------------------------------------------------------------
# Steps 1198-1200 — fix task, fixture builder, patch intent
# ---------------------------------------------------------------------------


class TestProposeFixtureBuilder:
    def test_approval_required_with_resolvable_intent(self, data_dir):
        jid, fa, _ = _make_job_with_failure(data_dir)
        r = RL.run_repair_attempt(jid, fa, fixture_builder=True, data_dir=data_dir)
        assert r.status == "approval_required"
        assert r.stop_reason == "approval_required"
        assert r.repair_intent_id
        job = load_job(__import__("uuid").UUID(jid), data_dir)
        assert get_patch_intent(job, r.repair_intent_id) is not None
        assert r.next_safe_action.command == f"remedy patch approve {jid} {r.repair_intent_id}"

    def test_fix_task_only_without_builder(self, data_dir):
        jid, fa, _ = _make_job_with_failure(data_dir)
        r = RL.run_repair_attempt(jid, fa, fixture_builder=False, data_dir=data_dir)
        assert r.status == "fix_task_created"
        assert r.repair_task_id
        assert not r.repair_intent_id

    def test_unsupported_kind_unavailable(self, data_dir):
        jid, fa, _ = _make_job_with_failure(data_dir, failure_kind="timeout",
                                            safe_summary="Test timeout")
        r = RL.run_repair_attempt(jid, fa, fixture_builder=True, data_dir=data_dir)
        assert r.stop_reason == "repair_builder_unavailable"
        assert not r.repair_intent_id
        assert r.repair_task_id  # fix task still created

    def test_next_actions_catalog_backed(self, data_dir):
        from packages.orchestration.do_run import validate_next_safe_action_command
        jid, fa, _ = _make_job_with_failure(data_dir)
        r = RL.run_repair_attempt(jid, fa, fixture_builder=True, data_dir=data_dir)
        assert validate_next_safe_action_command(r.next_safe_action.command)


# ---------------------------------------------------------------------------
# Step 1211 — idempotency
# ---------------------------------------------------------------------------


class TestIdempotency:
    def test_repeated_propose_same_attempt(self, data_dir):
        jid, fa, _ = _make_job_with_failure(data_dir)
        r1 = RL.run_repair_attempt(jid, fa, fixture_builder=True, data_dir=data_dir)
        r2 = RL.run_repair_attempt(jid, fa, fixture_builder=True, data_dir=data_dir)
        assert r1.repair_intent_id == r2.repair_intent_id
        assert r2.resumed is True

    def test_no_duplicate_task_artifact_intent(self, data_dir):
        import uuid
        jid, fa, _ = _make_job_with_failure(data_dir)
        RL.run_repair_attempt(jid, fa, fixture_builder=True, data_dir=data_dir)
        RL.run_repair_attempt(jid, fa, fixture_builder=True, data_dir=data_dir)
        RL.run_repair_attempt(jid, fa, fixture_builder=True, data_dir=data_dir)
        job = load_job(uuid.UUID(jid), data_dir)
        fix_tasks = [t for t in job.tasks if (t.inputs or {}).get("repair_fix_task")]
        repair_arts = [a for a in job.artifacts if (a.metadata or {}).get("repair_v1")]
        attempts = RL.load_repair_attempts(job)
        assert len(fix_tasks) == 1
        assert len(repair_arts) == 1
        assert len(attempts) == 1

    def test_resolved_failure_blocks(self, data_dir):
        jid, fa, _ = _make_job_with_failure(data_dir, exit_code=0)
        r = RL.run_repair_attempt(jid, fa, fixture_builder=True, data_dir=data_dir)
        assert r.status == "blocked"
        assert r.stop_reason == "blocked_ineligible"

    def test_invalid_failure_artifact_safe(self, data_dir):
        jid, _, _ = _make_job_with_failure(data_dir)
        r = RL.run_repair_attempt(jid, "nope", fixture_builder=True, data_dir=data_dir)
        assert r.status == "blocked"
        assert r.next_safe_action is not None


# ---------------------------------------------------------------------------
# Step 1209 — proof / provenance alignment
# ---------------------------------------------------------------------------


class TestProofAlignment:
    def test_repair_intent_not_applied_or_verified(self, data_dir):
        import uuid
        jid, fa, _ = _make_job_with_failure(data_dir)
        r = RL.run_repair_attempt(jid, fa, fixture_builder=True, data_dir=data_dir)
        job = load_job(uuid.UUID(jid), data_dir)
        intent = get_patch_intent(job, r.repair_intent_id)
        assert intent is not None
        assert intent.get("state") == "pending"  # not approved, not applied
        from packages.orchestration.proof_chain import build_proof_chain, PROOF_VERIFIED
        from packages.orchestration.timeline import load_run_events
        events = load_run_events(data_dir, uuid.UUID(jid))
        chain = build_proof_chain(job, events, data_dir=data_dir)
        for c in chain.changes:
            if c.intent_id == r.repair_intent_id:
                assert c.apply_state != "applied"
                assert c.proof_status != PROOF_VERIFIED


# ---------------------------------------------------------------------------
# Step 1213 — redaction
# ---------------------------------------------------------------------------


class TestRedaction:
    def test_no_raw_leakage_in_result_and_events(self, data_dir):
        import json
        import uuid
        jid, fa, _ = _make_job_with_failure(
            data_dir,
            safe_summary="Test test_failed: exit 1",  # safe summary is bounded
            related_files=["/home/u/.env", "secret_token.py"],
        )
        r = RL.run_repair_attempt(jid, fa, fixture_builder=True, data_dir=data_dir)
        payload = json.dumps(RL.export_repair_attempt_json(r))
        ctx = RL.export_repair_context_json(RL.build_repair_context(jid, fa, data_dir))
        from packages.orchestration.timeline import load_run_events
        events_blob = json.dumps(load_run_events(data_dir, uuid.UUID(jid)))
        for blob in (payload, json.dumps(ctx), events_blob):
            assert "Traceback" not in blob
            assert "/home/" not in blob
            assert "diff --git" not in blob
            assert "BEGIN " not in blob


# ---------------------------------------------------------------------------
# Step 1214 — architecture guards
# ---------------------------------------------------------------------------


class TestArchitectureGuards:
    SRC = Path("packages/orchestration/repair_loop.py").read_text()

    def _import_lines(self):
        return [ln for ln in self.SRC.splitlines()
                if ln.strip().startswith(("import ", "from "))]

    def test_no_source_apply_import(self):
        for ln in self._import_lines():
            assert "source_apply" not in ln

    def test_no_apply_service_import(self):
        for ln in self._import_lines():
            assert "patch_apply" not in ln
            assert "apply_patch_intent" not in ln

    def test_no_test_execution_import(self):
        for ln in self._import_lines():
            assert "test_execution_service" not in ln
            assert "execute_test_run" not in ln

    def test_no_provider_or_ollama(self):
        assert "ollama" not in self.SRC.lower()
        for ln in self._import_lines():
            assert "provider" not in ln.lower()

    def test_no_shell_true(self):
        assert "shell=True" not in self.SRC

    def test_no_subprocess(self):
        for ln in self._import_lines():
            assert "subprocess" not in ln

    def test_fixture_builder_deterministic_target(self):
        # The fixture repair target is derived deterministically from the
        # failure id (no randomness in the proposed change path).
        assert 'f"docs/repairs/{fa_short}.md"' in self.SRC
