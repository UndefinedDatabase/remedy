"""Tests for proof chain v1.

Covers:
- Proof status truth rules (verified, failed, incomplete, unverified, not_applicable)
- Proof chain builder with deterministic fixtures
- Safe next action derivation
- Redaction: no raw diffs, content, secrets
- File provenance alignment
- Path traversal rejection in CLI
- JSON stability
- Edge cases: empty job, missing events, path filter
"""

from __future__ import annotations

import json
from uuid import uuid4

import pytest

from packages.core.models import (
    Artifact,
    ArtifactKind,
    Job,
    Task,
    RunState,
)
from packages.orchestration.approval_queue import make_intent_id
from packages.orchestration.proof_chain import (
    PROOF_FAILED,
    PROOF_INCOMPLETE,
    PROOF_NOT_APPLICABLE,
    PROOF_UNVERIFIED,
    PROOF_VERIFIED,
    ProofChain,
    ProofChange,
    _classify_proof_status,
    _derive_missing_links,
    build_proof_chain,
    derive_next_safe_action,
    export_proof_chain_json,
    summarize_proof_chain,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_job(*, tasks=None, artifacts=None, user_prompt="Fix the bug"):
    job = Job(name="test-job", user_prompt=user_prompt)
    if tasks:
        job.tasks = tasks
    if artifacts:
        job.artifacts = artifacts
    return job


def _make_artifact_with_intents(task_id, explanations, *, approvals=None):
    """Create artifact with patch_intent_explanations like real approval_queue expects."""
    art = Artifact(
        name="patch-intent",
        content="",
        kind=ArtifactKind.PATCH_INTENT,
        task_id=task_id,
        metadata={
            "patch_intent_explanations": explanations,
            "patch_intent_approvals": approvals or {},
        },
    )
    return art


def _explanation_record(target_path, *, action="modify", risk="medium"):
    """Patch intent explanation format matching approval_queue expectations."""
    return {
        "file": target_path,
        "action": action,
        "risk": risk,
        "reason": "",
        "summary": "",
    }


def _make_full_chain_job():
    """Create a job with one task, one intent, approved + applied + proof + test passed."""
    task = Task(description="Fix auth bug")
    task_id = task.id

    explanations = [_explanation_record("src/auth.py")]
    art = _make_artifact_with_intents(task_id, explanations)
    intent_id = make_intent_id(art.id, 0)

    approvals = {
        intent_id: {
            "state": "approved",
            "decided_at": "2026-01-01T00:00:00Z",
            "decided_by": "human",
        }
    }
    art.metadata["patch_intent_approvals"] = approvals

    job = _make_job(tasks=[task], artifacts=[art])

    events = [
        {"event": "task_execution_completed", "metadata": {"task_id": str(task_id), "exec_status": "completed"}},
        {"event": "patch_intent_applied", "metadata": {"intent_id": intent_id, "outcome": "applied", "bytes_written": 100, "line_count": 10}},
        {"event": "patch_apply_proof_recorded", "metadata": {"intent_id": intent_id, "before_sha256": "abc123", "after_sha256": "def456", "bytes_delta": 50}},
        {"event": "test_run_completed", "metadata": {"status": "passed", "exit_code": 0}},
    ]
    return job, events, intent_id


# ---------------------------------------------------------------------------
# Truth rules
# ---------------------------------------------------------------------------


class TestProofStatusTruthRules:

    def test_verified(self):
        assert _classify_proof_status(
            approval_state="approved", apply_state="applied",
            test_state="passed", has_proof=True,
            task_blocked=False, task_failed=False,
        ) == PROOF_VERIFIED

    def test_verified_no_test(self):
        assert _classify_proof_status(
            approval_state="approved", apply_state="applied",
            test_state="not_tested", has_proof=True,
            task_blocked=False, task_failed=False,
        ) == PROOF_VERIFIED

    def test_failed_test(self):
        assert _classify_proof_status(
            approval_state="approved", apply_state="applied",
            test_state="failed", has_proof=True,
            task_blocked=False, task_failed=False,
        ) == PROOF_FAILED

    def test_failed_task_blocked(self):
        assert _classify_proof_status(
            approval_state="approved", apply_state="applied",
            test_state="not_tested", has_proof=True,
            task_blocked=True, task_failed=False,
        ) == PROOF_FAILED

    def test_failed_task_failed(self):
        assert _classify_proof_status(
            approval_state="approved", apply_state="applied",
            test_state="not_tested", has_proof=True,
            task_blocked=False, task_failed=True,
        ) == PROOF_FAILED

    def test_incomplete_pending_approval(self):
        assert _classify_proof_status(
            approval_state="pending", apply_state="not_applied",
            test_state="not_tested", has_proof=False,
            task_blocked=False, task_failed=False,
        ) == PROOF_INCOMPLETE

    def test_incomplete_approved_not_applied(self):
        assert _classify_proof_status(
            approval_state="approved", apply_state="not_applied",
            test_state="not_tested", has_proof=False,
            task_blocked=False, task_failed=False,
        ) == PROOF_INCOMPLETE

    def test_incomplete_applied_no_proof(self):
        assert _classify_proof_status(
            approval_state="approved", apply_state="applied",
            test_state="not_tested", has_proof=False,
            task_blocked=False, task_failed=False,
        ) == PROOF_INCOMPLETE

    def test_not_applicable_rejected(self):
        assert _classify_proof_status(
            approval_state="rejected", apply_state="not_applied",
            test_state="not_tested", has_proof=False,
            task_blocked=False, task_failed=False,
        ) == PROOF_NOT_APPLICABLE


class TestMissingLinks:

    def test_pending_approval(self):
        missing = _derive_missing_links(
            approval_state="pending", apply_state="not_applied",
            test_state="not_tested", has_proof=False,
        )
        assert "approval_pending" in missing

    def test_not_applied(self):
        missing = _derive_missing_links(
            approval_state="approved", apply_state="not_applied",
            test_state="not_tested", has_proof=False,
        )
        assert "not_applied" in missing

    def test_no_proof(self):
        missing = _derive_missing_links(
            approval_state="approved", apply_state="applied",
            test_state="not_tested", has_proof=False,
        )
        assert "no_apply_proof" in missing

    def test_not_tested(self):
        missing = _derive_missing_links(
            approval_state="approved", apply_state="applied",
            test_state="not_tested", has_proof=True,
        )
        assert "not_tested" in missing

    def test_complete_chain_no_missing(self):
        missing = _derive_missing_links(
            approval_state="approved", apply_state="applied",
            test_state="passed", has_proof=True,
        )
        assert missing == []


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


class TestBuildProofChain:

    def test_empty_job(self):
        job = _make_job()
        chain = build_proof_chain(job, [])
        assert chain.overall_status == PROOF_NOT_APPLICABLE
        assert chain.changes == ()

    def test_full_verified_chain(self):
        job, events, intent_id = _make_full_chain_job()
        chain = build_proof_chain(job, events)
        assert chain.overall_status == PROOF_VERIFIED
        assert len(chain.changes) == 1
        c = chain.changes[0]
        assert c.proof_status == PROOF_VERIFIED
        assert c.target_path == "src/auth.py"
        assert c.approval_state == "approved"
        assert c.apply_state == "applied"
        assert c.test_state == "passed"

    def test_path_filter(self):
        job, events, intent_id = _make_full_chain_job()
        chain = build_proof_chain(job, events, path="nonexistent.py")
        assert chain.changes == ()

    def test_path_filter_match(self):
        job, events, intent_id = _make_full_chain_job()
        chain = build_proof_chain(job, events, path="src/auth.py")
        assert len(chain.changes) == 1

    def test_goal_truncation(self):
        job = _make_job(user_prompt="x" * 300)
        chain = build_proof_chain(job, [])
        assert len(chain.goal) <= 201  # 200 + "…"

    def test_generated_at_present(self):
        job = _make_job()
        chain = build_proof_chain(job, [])
        assert chain.generated_at


# ---------------------------------------------------------------------------
# JSON export
# ---------------------------------------------------------------------------


class TestExportJson:

    def test_json_stable(self):
        job, events, _ = _make_full_chain_job()
        chain = build_proof_chain(job, events)
        data = export_proof_chain_json(chain)
        text = json.dumps(data, sort_keys=True)
        data2 = json.loads(text)
        assert data2["version"] == 1
        assert data2["overall_status"] == PROOF_VERIFIED
        assert len(data2["changes"]) == 1

    def test_json_has_required_fields(self):
        job, events, _ = _make_full_chain_job()
        chain = build_proof_chain(job, events)
        data = export_proof_chain_json(chain)
        assert "job_id" in data
        assert "goal" in data
        assert "overall_status" in data
        assert "next_safe_action" in data
        assert "missing_links" in data
        assert "changes" in data
        c = data["changes"][0]
        for field in ("target_path", "intent_id", "task_id", "approval_state",
                      "apply_state", "test_state", "proof_status", "safe_summary",
                      "next_safe_action", "missing_links"):
            assert field in c, f"Missing field: {field}"


# ---------------------------------------------------------------------------
# Redaction / safety
# ---------------------------------------------------------------------------


class TestRedaction:

    def test_no_raw_diff(self):
        job, events, _ = _make_full_chain_job()
        chain = build_proof_chain(job, events)
        text = json.dumps(export_proof_chain_json(chain))
        assert "diff" not in text.lower() or "bytes_delta" in text  # bytes_delta is ok

    def test_no_raw_content(self):
        job, events, _ = _make_full_chain_job()
        chain = build_proof_chain(job, events)
        text = json.dumps(export_proof_chain_json(chain))
        assert "content" not in text.lower() or "context" in text.lower()  # context in goal ok

    def test_no_stdout_stderr(self):
        job, events, _ = _make_full_chain_job()
        chain = build_proof_chain(job, events)
        text = json.dumps(export_proof_chain_json(chain))
        assert "stdout" not in text.lower()
        assert "stderr" not in text.lower()

    def test_output_bounded(self):
        job, events, _ = _make_full_chain_job()
        chain = build_proof_chain(job, events)
        text = summarize_proof_chain(chain)
        assert len(text) < 10000


# ---------------------------------------------------------------------------
# Next safe action
# ---------------------------------------------------------------------------


class TestNextSafeAction:

    def test_verified_no_action(self):
        job, events, _ = _make_full_chain_job()
        chain = build_proof_chain(job, events)
        assert "no action" in chain.next_safe_action.lower()

    def test_pending_approval_action(self):
        task = Task(description="Fix bug")
        explanations = [_explanation_record("src/bug.py")]
        art = _make_artifact_with_intents(task.id, explanations)
        job = _make_job(tasks=[task], artifacts=[art])
        chain = build_proof_chain(job, [])
        assert "approve" in chain.next_safe_action.lower() or "pending" in chain.next_safe_action.lower()


# ---------------------------------------------------------------------------
# Incomplete chain tests
# ---------------------------------------------------------------------------


class TestIncompleteChains:

    def _make_intent_only_job(self, state="pending"):
        task = Task(description="Task")
        explanations = [_explanation_record("src/file.py")]
        art = _make_artifact_with_intents(task.id, explanations)
        intent_id = make_intent_id(art.id, 0)
        approvals = {}
        if state != "pending":
            approvals[intent_id] = {"state": state, "decided_at": "", "decided_by": ""}
        art.metadata["patch_intent_approvals"] = approvals
        return _make_job(tasks=[task], artifacts=[art]), intent_id

    def test_pending_approval(self):
        job, iid = self._make_intent_only_job("pending")
        chain = build_proof_chain(job, [])
        assert chain.overall_status == PROOF_INCOMPLETE
        assert chain.changes[0].missing_links == ["approval_pending"]

    def test_approved_not_applied(self):
        job, iid = self._make_intent_only_job("approved")
        chain = build_proof_chain(job, [])
        assert chain.overall_status == PROOF_INCOMPLETE
        assert "not_applied" in chain.changes[0].missing_links

    def test_applied_no_test(self):
        job, iid = self._make_intent_only_job("approved")
        events = [
            {"event": "patch_intent_applied", "metadata": {"intent_id": iid, "outcome": "applied", "bytes_written": 50, "line_count": 5}},
        ]
        chain = build_proof_chain(job, events)
        assert chain.changes[0].proof_status == PROOF_INCOMPLETE
        assert "no_apply_proof" in chain.changes[0].missing_links

    def test_test_failed(self):
        job, iid = self._make_intent_only_job("approved")
        events = [
            {"event": "patch_intent_applied", "metadata": {"intent_id": iid, "outcome": "applied", "bytes_written": 50, "line_count": 5}},
            {"event": "patch_apply_proof_recorded", "metadata": {"intent_id": iid, "before_sha256": "a", "after_sha256": "b", "bytes_delta": 10}},
            {"event": "test_run_completed", "metadata": {"status": "failed", "exit_code": 1}},
        ]
        chain = build_proof_chain(job, events)
        assert chain.changes[0].proof_status == PROOF_FAILED

    def test_missing_task(self):
        job = _make_job()
        chain = build_proof_chain(job, [])
        assert chain.changes == ()

    def test_rejected(self):
        job, iid = self._make_intent_only_job("rejected")
        chain = build_proof_chain(job, [])
        assert chain.changes[0].proof_status == PROOF_NOT_APPLICABLE


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------


class TestSummary:

    def test_summary_contains_status(self):
        job, events, _ = _make_full_chain_job()
        chain = build_proof_chain(job, events)
        text = summarize_proof_chain(chain)
        assert "verified" in text.lower()
        assert "[OK]" in text

    def test_summary_incomplete(self):
        task = Task(description="Task")
        explanations = [_explanation_record("src/file.py")]
        art = _make_artifact_with_intents(task.id, explanations)
        job = _make_job(tasks=[task], artifacts=[art])
        text = summarize_proof_chain(build_proof_chain(job, []))
        assert "[...]" in text


# ---------------------------------------------------------------------------
# File provenance alignment
# ---------------------------------------------------------------------------


class TestFileProvenanceAlignment:

    def test_provenance_has_proof_status(self):
        from packages.orchestration.file_provenance import build_file_provenance
        job, events, _ = _make_full_chain_job()
        prov = build_file_provenance(job, events, "src/auth.py")
        assert prov.proof_status == PROOF_VERIFIED

    def test_provenance_no_match(self):
        from packages.orchestration.file_provenance import build_file_provenance
        job, events, _ = _make_full_chain_job()
        prov = build_file_provenance(job, events, "nonexistent.py")
        assert prov.proof_status == ""
