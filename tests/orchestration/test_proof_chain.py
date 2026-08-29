"""Tests for proof chain v2.

Covers:
- Proof status truth rules (strict: no false verified)
- Test linking (intent, task, sole_change, not_required, none)
- Proof chain builder with deterministic fixtures
- Safe next action (structured object + legacy string)
- Redaction: no raw diffs, content, secrets, stdout/stderr, tracebacks
- File provenance alignment
- Path traversal rejection in CLI
- JSON stability
- Edge cases: empty job, missing events, path filter, unlinked tests
"""

from __future__ import annotations

import json

from packages.core.models import (
    Artifact,
    ArtifactKind,
    Job,
    Task,
)
from packages.orchestration.approval_queue import make_intent_id
from packages.orchestration.proof_chain import (
    PROOF_FAILED,
    PROOF_INCOMPLETE,
    PROOF_NOT_APPLICABLE,
    PROOF_UNVERIFIED,
    PROOF_VERIFIED,
    TEST_LINK_INTENT,
    TEST_LINK_NONE,
    TEST_LINK_NOT_REQUIRED,
    TEST_LINK_SOLE_CHANGE,
    TEST_LINK_TASK,
    NextSafeAction,
    ProofChain,
    ProofChange,
    TaskApplyState,
    _classify_proof_status,
    _derive_missing_links,
    _event_timestamp,
    _is_after_or_same,
    _link_test_to_change,
    build_proof_chain,
    export_proof_chain_json,
    fold_task_apply_states,
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
    return {
        "file": target_path,
        "action": action,
        "risk": risk,
        "reason": "",
        "summary": "",
    }


def _make_full_chain_job(*, test_linked=True):
    """Create a job with one task, one intent, approved + applied + proof + linked test passed."""
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
    art.metadata["patch_intent_apply_records"] = {
        intent_id: {"snapshot_verified": True}
    }

    job = _make_job(tasks=[task], artifacts=[art])

    # Test event linked to intent
    test_meta = {"status": "passed", "exit_code": 0}
    if test_linked:
        test_meta["intent_id"] = intent_id

    events = [
        {"event": "task_execution_completed", "metadata": {"task_id": str(task_id), "exec_status": "completed"}},
        {"event": "patch_intent_applied", "timestamp": "2026-01-01T00:00:00Z", "metadata": {"intent_id": intent_id, "outcome": "applied", "bytes_written": 100, "line_count": 10}},
        {"event": "patch_apply_proof_recorded", "metadata": {"intent_id": intent_id, "before_sha256": "abc123", "after_sha256": "def456", "bytes_delta": 50}},
        {"event": "test_run_completed", "timestamp": "2026-01-01T00:01:00Z", "metadata": test_meta},
    ]
    return job, events, intent_id


# ---------------------------------------------------------------------------
# Truth rules (Step 827/833)
# ---------------------------------------------------------------------------


class TestProofStatusTruthRules:

    def test_verified_full_chain(self):
        """approved + applied + apply_event + proof + snapshot_verified + linked passed test → verified"""
        assert _classify_proof_status(
            approval_state="approved", apply_state="applied",
            test_state="passed", test_link=TEST_LINK_INTENT,
            has_proof=True, has_apply_event=True,
            task_blocked=False, task_failed=False,
            snapshot_verified=True,
        ) == PROOF_VERIFIED

    def test_verified_not_required(self):
        """approved + applied + proof + snapshot_verified + explicit not_required → verified"""
        assert _classify_proof_status(
            approval_state="approved", apply_state="applied",
            test_state="not_required", test_link=TEST_LINK_NOT_REQUIRED,
            has_proof=True, has_apply_event=True,
            task_blocked=False, task_failed=False,
            snapshot_verified=True,
        ) == PROOF_VERIFIED

    def test_verified_requires_snapshot_verified(self):
        """CRITICAL: full chain without snapshot_verified → UNVERIFIED, never verified"""
        assert _classify_proof_status(
            approval_state="approved", apply_state="applied",
            test_state="passed", test_link=TEST_LINK_INTENT,
            has_proof=True, has_apply_event=True,
            task_blocked=False, task_failed=False,
            snapshot_verified=False,
        ) == PROOF_UNVERIFIED

    def test_not_tested_is_NOT_verified(self):
        """CRITICAL: approved + applied + proof + not_tested → INCOMPLETE, never verified"""
        assert _classify_proof_status(
            approval_state="approved", apply_state="applied",
            test_state="not_tested", test_link=TEST_LINK_NONE,
            has_proof=True, has_apply_event=True,
            task_blocked=False, task_failed=False,
        ) == PROOF_INCOMPLETE

    def test_unlinked_passed_test_is_NOT_verified(self):
        """passed test with no link → incomplete (test not linked to change)"""
        assert _classify_proof_status(
            approval_state="approved", apply_state="applied",
            test_state="passed", test_link=TEST_LINK_NONE,
            has_proof=True, has_apply_event=True,
            task_blocked=False, task_failed=False,
        ) == PROOF_INCOMPLETE

    def test_failed_linked_test(self):
        assert _classify_proof_status(
            approval_state="approved", apply_state="applied",
            test_state="failed", test_link=TEST_LINK_INTENT,
            has_proof=True, has_apply_event=True,
            task_blocked=False, task_failed=False,
        ) == PROOF_FAILED

    def test_failed_task_blocked(self):
        assert _classify_proof_status(
            approval_state="approved", apply_state="applied",
            test_state="not_tested", test_link=TEST_LINK_NONE,
            has_proof=True, has_apply_event=True,
            task_blocked=True, task_failed=False,
        ) == PROOF_FAILED

    def test_failed_task_failed(self):
        assert _classify_proof_status(
            approval_state="approved", apply_state="applied",
            test_state="not_tested", test_link=TEST_LINK_NONE,
            has_proof=True, has_apply_event=True,
            task_blocked=False, task_failed=True,
        ) == PROOF_FAILED

    def test_incomplete_pending_approval(self):
        assert _classify_proof_status(
            approval_state="pending", apply_state="not_applied",
            test_state="not_tested", test_link=TEST_LINK_NONE,
            has_proof=False, has_apply_event=False,
            task_blocked=False, task_failed=False,
        ) == PROOF_INCOMPLETE

    def test_incomplete_approved_not_applied(self):
        assert _classify_proof_status(
            approval_state="approved", apply_state="not_applied",
            test_state="not_tested", test_link=TEST_LINK_NONE,
            has_proof=False, has_apply_event=False,
            task_blocked=False, task_failed=False,
        ) == PROOF_INCOMPLETE

    def test_incomplete_applied_no_proof(self):
        assert _classify_proof_status(
            approval_state="approved", apply_state="applied",
            test_state="not_tested", test_link=TEST_LINK_NONE,
            has_proof=False, has_apply_event=True,
            task_blocked=False, task_failed=False,
        ) == PROOF_INCOMPLETE

    def test_incomplete_no_apply_event(self):
        """applied but no apply event → incomplete"""
        assert _classify_proof_status(
            approval_state="approved", apply_state="applied",
            test_state="not_tested", test_link=TEST_LINK_NONE,
            has_proof=True, has_apply_event=False,
            task_blocked=False, task_failed=False,
        ) == PROOF_INCOMPLETE

    def test_not_applicable_rejected(self):
        assert _classify_proof_status(
            approval_state="rejected", apply_state="not_applied",
            test_state="not_tested", test_link=TEST_LINK_NONE,
            has_proof=False, has_apply_event=False,
            task_blocked=False, task_failed=False,
        ) == PROOF_NOT_APPLICABLE

    def test_task_linked_test_verified(self):
        """task_linked test can verify"""
        assert _classify_proof_status(
            approval_state="approved", apply_state="applied",
            test_state="passed", test_link=TEST_LINK_TASK,
            has_proof=True, has_apply_event=True,
            task_blocked=False, task_failed=False,
            snapshot_verified=True,
        ) == PROOF_VERIFIED

    def test_sole_change_test_verified(self):
        """sole_change test can verify"""
        assert _classify_proof_status(
            approval_state="approved", apply_state="applied",
            test_state="passed", test_link=TEST_LINK_SOLE_CHANGE,
            has_proof=True, has_apply_event=True,
            task_blocked=False, task_failed=False,
            snapshot_verified=True,
        ) == PROOF_VERIFIED


class TestMissingLinks:

    def test_pending_approval(self):
        missing = _derive_missing_links(
            approval_state="pending", apply_state="not_applied",
            test_state="not_tested", test_link=TEST_LINK_NONE,
            has_proof=False, has_apply_event=False,
        )
        assert "approval_pending" in missing

    def test_not_applied(self):
        missing = _derive_missing_links(
            approval_state="approved", apply_state="not_applied",
            test_state="not_tested", test_link=TEST_LINK_NONE,
            has_proof=False, has_apply_event=False,
        )
        assert "not_applied" in missing

    def test_no_apply_event(self):
        missing = _derive_missing_links(
            approval_state="approved", apply_state="applied",
            test_state="not_tested", test_link=TEST_LINK_NONE,
            has_proof=True, has_apply_event=False,
        )
        assert "no_apply_event" in missing

    def test_no_proof(self):
        missing = _derive_missing_links(
            approval_state="approved", apply_state="applied",
            test_state="not_tested", test_link=TEST_LINK_NONE,
            has_proof=False, has_apply_event=True,
        )
        assert "no_apply_proof" in missing

    def test_no_linked_test(self):
        missing = _derive_missing_links(
            approval_state="approved", apply_state="applied",
            test_state="not_tested", test_link=TEST_LINK_NONE,
            has_proof=True, has_apply_event=True,
        )
        assert "no_linked_test" in missing

    def test_test_not_linked(self):
        """Test ran but not linked to change"""
        missing = _derive_missing_links(
            approval_state="approved", apply_state="applied",
            test_state="passed", test_link=TEST_LINK_NONE,
            has_proof=True, has_apply_event=True,
        )
        assert "no_linked_test" in missing

    def test_complete_chain_no_missing(self):
        missing = _derive_missing_links(
            approval_state="approved", apply_state="applied",
            test_state="passed", test_link=TEST_LINK_INTENT,
            has_proof=True, has_apply_event=True,
            snapshot_verified=True,
        )
        assert missing == []

    def test_no_snapshot_proof(self):
        """applied without verified snapshot → no_snapshot_proof in missing"""
        missing = _derive_missing_links(
            approval_state="approved", apply_state="applied",
            test_state="passed", test_link=TEST_LINK_INTENT,
            has_proof=True, has_apply_event=True,
            snapshot_verified=False,
        )
        assert "no_snapshot_proof" in missing


# ---------------------------------------------------------------------------
# Test linking (Step 828)
# ---------------------------------------------------------------------------


class TestTestLinking:

    def test_intent_linked(self):
        events = [{"event": "test_run_completed", "metadata": {"intent_id": "abc-0", "status": "passed"}}]
        state, link, _ = _link_test_to_change(
            intent_id="abc-0", task_id="t1",
            test_events=events, apply_events={"abc-0": {}},
            total_applied_changes=1,
        )
        assert state == "passed"
        assert link == TEST_LINK_INTENT

    def test_task_linked(self):
        events = [{"event": "test_run_completed", "metadata": {"task_id": "t1", "status": "failed"}}]
        state, link, _ = _link_test_to_change(
            intent_id="abc-0", task_id="t1",
            test_events=events, apply_events={"abc-0": {}},
            total_applied_changes=2,
        )
        assert state == "failed"
        assert link == TEST_LINK_TASK

    def test_sole_change_after_apply(self):
        events = [{"event": "test_run_completed", "timestamp": "2026-01-01T00:01:00Z", "metadata": {"status": "passed"}}]
        state, link, _ = _link_test_to_change(
            intent_id="abc-0", task_id="t1",
            test_events=events, apply_events={"abc-0": {"timestamp": "2026-01-01T00:00:00Z"}},
            total_applied_changes=1,
        )
        assert state == "passed"
        assert link == TEST_LINK_SOLE_CHANGE

    def test_sole_change_before_apply_not_linked(self):
        events = [{"event": "test_run_completed", "timestamp": "2025-12-31T23:59:00Z", "metadata": {"status": "passed"}}]
        state, link, meta = _link_test_to_change(
            intent_id="abc-0", task_id="t1",
            test_events=events, apply_events={"abc-0": {"timestamp": "2026-01-01T00:00:00Z"}},
            total_applied_changes=1,
        )
        assert state == "not_tested"
        assert link == TEST_LINK_NONE
        assert meta["missing_link"] == "no_test_after_apply"

    def test_sole_change_missing_timestamps_not_linked(self):
        events = [{"event": "test_run_completed", "metadata": {"status": "passed"}}]
        state, link, meta = _link_test_to_change(
            intent_id="abc-0", task_id="t1",
            test_events=events, apply_events={"abc-0": {}},
            total_applied_changes=1,
        )
        assert state == "not_tested"
        assert link == TEST_LINK_NONE
        assert meta["missing_link"] == "test_order_unknown"

    def test_timestamp_helpers_unknown_for_missing_or_invalid(self):
        assert _event_timestamp({"timestamp": "not-a-time"}) is None
        assert _is_after_or_same("", "2026-01-01T00:00:00Z") is None
        assert _is_after_or_same("2026-01-01T00:00:00Z", "bad") is None
        assert _is_after_or_same("2026-01-01T00:00:00Z", "2026-01-01T00:00:00Z") is True

    def test_timestamp_ordering_uses_parsed_offsets(self):
        assert _is_after_or_same(
            "2026-01-01T01:00:00+02:00",
            "2026-01-01T00:30:00+00:00",
        ) is False

    def test_no_link_multiple_changes(self):
        """Generic test with multiple applied changes → no link"""
        events = [{"event": "test_run_completed", "metadata": {"status": "passed"}}]
        state, link, _ = _link_test_to_change(
            intent_id="abc-0", task_id="t1",
            test_events=events, apply_events={"abc-0": {}, "def-0": {}},
            total_applied_changes=2,
        )
        assert state == "not_tested"
        assert link == TEST_LINK_NONE

    def test_no_test_events(self):
        state, link, _ = _link_test_to_change(
            intent_id="abc-0", task_id="t1",
            test_events=[], apply_events={"abc-0": {}},
            total_applied_changes=1,
        )
        assert state == "not_tested"
        assert link == TEST_LINK_NONE

    def test_explicit_not_required(self):
        events = [{"event": "test_run_completed", "metadata": {"intent_id": "abc-0", "test_not_required": True}}]
        state, link, _ = _link_test_to_change(
            intent_id="abc-0", task_id="t1",
            test_events=events, apply_events={"abc-0": {}},
            total_applied_changes=1,
        )
        assert state == "not_required"
        assert link == TEST_LINK_NOT_REQUIRED

    def test_unrelated_test_not_linked(self):
        """Test for different intent → no link to this change"""
        events = [{"event": "test_run_completed", "metadata": {"intent_id": "other-0", "status": "passed"}}]
        state, link, _ = _link_test_to_change(
            intent_id="abc-0", task_id="t1",
            test_events=events, apply_events={"abc-0": {}},
            total_applied_changes=2,
        )
        assert state == "not_tested"
        assert link == TEST_LINK_NONE


# ---------------------------------------------------------------------------
# Builder (Steps 826-829)
# ---------------------------------------------------------------------------


class TestBuildProofChain:

    def test_empty_job(self):
        job = _make_job()
        chain = build_proof_chain(job, [])
        assert chain.overall_status == PROOF_NOT_APPLICABLE
        assert chain.changes == ()

    def test_full_verified_chain(self):
        job, events, intent_id = _make_full_chain_job(test_linked=True)
        chain = build_proof_chain(job, events)
        assert chain.overall_status == PROOF_VERIFIED
        assert len(chain.changes) == 1
        c = chain.changes[0]
        assert c.proof_status == PROOF_VERIFIED
        assert c.target_path == "src/auth.py"
        assert c.approval_state == "approved"
        assert c.apply_state == "applied"
        assert c.test_state == "passed"
        assert c.test_link == TEST_LINK_INTENT

    def test_unlinked_test_not_verified(self):
        """CRITICAL: unlinked test does NOT verify when multiple changes exist"""
        task = Task(description="Fix bug")
        explanations = [
            _explanation_record("src/a.py"),
            _explanation_record("src/b.py"),
        ]
        art = _make_artifact_with_intents(task.id, explanations)
        iid_a = make_intent_id(art.id, 0)
        iid_b = make_intent_id(art.id, 1)
        approvals = {
            iid_a: {"state": "approved", "decided_at": "", "decided_by": ""},
            iid_b: {"state": "approved", "decided_at": "", "decided_by": ""},
        }
        art.metadata["patch_intent_approvals"] = approvals
        job = _make_job(tasks=[task], artifacts=[art])
        events = [
            {"event": "patch_intent_applied", "metadata": {"intent_id": iid_a, "outcome": "applied", "bytes_written": 50, "line_count": 5}},
            {"event": "patch_intent_applied", "metadata": {"intent_id": iid_b, "outcome": "applied", "bytes_written": 50, "line_count": 5}},
            {"event": "patch_apply_proof_recorded", "metadata": {"intent_id": iid_a, "before_sha256": "a", "after_sha256": "b", "bytes_delta": 10}},
            {"event": "patch_apply_proof_recorded", "metadata": {"intent_id": iid_b, "before_sha256": "c", "after_sha256": "d", "bytes_delta": 10}},
            # Generic test — no intent_id, no task_id
            {"event": "test_run_completed", "metadata": {"status": "passed", "exit_code": 0}},
        ]
        chain = build_proof_chain(job, events)
        # Neither change should be verified — test not linked
        for c in chain.changes:
            assert c.proof_status != PROOF_VERIFIED, f"{c.target_path} should not be verified"
            assert c.test_link == TEST_LINK_NONE

    def test_sole_change_gets_generic_test(self):
        """Single applied change in job → generic test links as sole_change"""
        job, events, intent_id = _make_full_chain_job(test_linked=False)
        chain = build_proof_chain(job, events)
        c = chain.changes[0]
        assert c.test_link == TEST_LINK_SOLE_CHANGE
        assert c.proof_status == PROOF_VERIFIED

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
        assert len(chain.goal) <= 201

    def test_generated_at_present(self):
        job = _make_job()
        chain = build_proof_chain(job, [])
        assert chain.generated_at


# ---------------------------------------------------------------------------
# JSON export (Step 834)
# ---------------------------------------------------------------------------


class TestExportJson:

    def test_json_stable(self):
        job, events, _ = _make_full_chain_job()
        chain = build_proof_chain(job, events)
        data = export_proof_chain_json(chain)
        text = json.dumps(data, sort_keys=True)
        data2 = json.loads(text)
        assert data2["version"] == 2
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
        assert "next_safe_action_obj" in data
        assert "missing_links" in data
        assert "changes" in data
        c = data["changes"][0]
        for field in ("target_path", "intent_id", "task_id", "approval_state",
                      "apply_state", "test_state", "test_link", "proof_status",
                      "safe_summary", "next_safe_action", "next_safe_action_obj",
                      "missing_links"):
            assert field in c, f"Missing field: {field}"

    def test_json_next_action_structured(self):
        job, events, _ = _make_full_chain_job()
        chain = build_proof_chain(job, events)
        data = export_proof_chain_json(chain)
        nsa = data["next_safe_action_obj"]
        assert "label" in nsa
        assert "command" in nsa
        assert "reason" in nsa
        assert "available" in nsa


# ---------------------------------------------------------------------------
# Redaction / safety (Step 832)
# ---------------------------------------------------------------------------


class TestRedaction:

    def test_no_raw_diff(self):
        job, events, _ = _make_full_chain_job()
        chain = build_proof_chain(job, events)
        text = json.dumps(export_proof_chain_json(chain))
        # bytes_delta ok, but no "diff" as key name
        assert "\"diff\"" not in text.lower()

    def test_no_raw_content(self):
        job, events, _ = _make_full_chain_job()
        chain = build_proof_chain(job, events)
        text = json.dumps(export_proof_chain_json(chain))
        assert "\"content\"" not in text.lower()

    def test_no_stdout_stderr(self):
        job, events, _ = _make_full_chain_job()
        chain = build_proof_chain(job, events)
        text = json.dumps(export_proof_chain_json(chain))
        assert "stdout" not in text.lower()
        assert "stderr" not in text.lower()

    def test_no_traceback(self):
        job, events, _ = _make_full_chain_job()
        chain = build_proof_chain(job, events)
        text = json.dumps(export_proof_chain_json(chain))
        assert "traceback" not in text.lower()
        assert "Traceback" not in text

    def test_no_approval_reason(self):
        job, events, _ = _make_full_chain_job()
        chain = build_proof_chain(job, events)
        text = json.dumps(export_proof_chain_json(chain))
        assert "approval_reason" not in text

    def test_no_command_output(self):
        job, events, _ = _make_full_chain_job()
        chain = build_proof_chain(job, events)
        text = json.dumps(export_proof_chain_json(chain))
        assert "command_output" not in text.lower()

    def test_output_bounded(self):
        job, events, _ = _make_full_chain_job()
        chain = build_proof_chain(job, events)
        text = summarize_proof_chain(chain)
        assert len(text) < 10000

    def test_summary_bounded_many_changes(self):
        """Even with many changes, summary stays bounded"""
        task = Task(description="Multi-file fix")
        explanations = [_explanation_record(f"src/file_{i}.py") for i in range(20)]
        art = _make_artifact_with_intents(task.id, explanations)
        job = _make_job(tasks=[task], artifacts=[art])
        chain = build_proof_chain(job, [])
        text = summarize_proof_chain(chain)
        assert len(text) < 10000


# ---------------------------------------------------------------------------
# Next safe action (Step 830)
# ---------------------------------------------------------------------------


class TestNextSafeAction:

    def test_verified_no_action(self):
        job, events, _ = _make_full_chain_job()
        chain = build_proof_chain(job, events)
        assert "no action" in chain.next_safe_action.lower()
        assert chain.next_safe_action_obj is not None

    def test_pending_approval_action(self):
        task = Task(description="Fix bug")
        explanations = [_explanation_record("src/bug.py")]
        art = _make_artifact_with_intents(task.id, explanations)
        job = _make_job(tasks=[task], artifacts=[art])
        chain = build_proof_chain(job, [])
        assert "approve" in chain.next_safe_action.lower() or "pending" in chain.next_safe_action.lower()
        obj = chain.next_safe_action_obj
        assert obj is not None
        assert obj.available is True

    def test_next_action_obj_on_change(self):
        job, events, _ = _make_full_chain_job()
        chain = build_proof_chain(job, events)
        c = chain.changes[0]
        assert c.next_safe_action_obj is not None
        assert isinstance(c.next_safe_action_obj, NextSafeAction)


# ---------------------------------------------------------------------------
# Incomplete chain tests (Step 833)
# ---------------------------------------------------------------------------


class TestIncompleteChains:

    def _make_intent_only_job(self, state="pending", *, snapshot_verified: bool = False):
        task = Task(description="Task")
        explanations = [_explanation_record("src/file.py")]
        art = _make_artifact_with_intents(task.id, explanations)
        intent_id = make_intent_id(art.id, 0)
        approvals = {}
        if state != "pending":
            approvals[intent_id] = {"state": state, "decided_at": "", "decided_by": ""}
        art.metadata["patch_intent_approvals"] = approvals
        if snapshot_verified:
            art.metadata["patch_intent_apply_records"] = {
                intent_id: {"snapshot_verified": True}
            }
        return _make_job(tasks=[task], artifacts=[art]), intent_id

    def test_pending_approval(self):
        job, iid = self._make_intent_only_job("pending")
        chain = build_proof_chain(job, [])
        assert chain.overall_status == PROOF_INCOMPLETE
        assert "approval_pending" in chain.changes[0].missing_links

    def test_approved_not_applied(self):
        job, iid = self._make_intent_only_job("approved")
        chain = build_proof_chain(job, [])
        assert chain.overall_status == PROOF_INCOMPLETE
        assert "not_applied" in chain.changes[0].missing_links

    def test_applied_no_proof_no_test(self):
        job, iid = self._make_intent_only_job("approved")
        events = [
            {"event": "patch_intent_applied", "metadata": {"intent_id": iid, "outcome": "applied", "bytes_written": 50, "line_count": 5}},
        ]
        chain = build_proof_chain(job, events)
        c = chain.changes[0]
        assert c.proof_status == PROOF_INCOMPLETE
        assert "no_apply_proof" in c.missing_links
        assert "no_linked_test" in c.missing_links

    def test_applied_with_proof_but_no_test(self):
        """CRITICAL: proof exists but no test → INCOMPLETE, not verified"""
        job, iid = self._make_intent_only_job("approved")
        events = [
            {"event": "patch_intent_applied", "metadata": {"intent_id": iid, "outcome": "applied", "bytes_written": 50, "line_count": 5}},
            {"event": "patch_apply_proof_recorded", "metadata": {"intent_id": iid, "before_sha256": "a", "after_sha256": "b", "bytes_delta": 10}},
        ]
        chain = build_proof_chain(job, events)
        c = chain.changes[0]
        assert c.proof_status == PROOF_INCOMPLETE
        assert c.test_state == "not_tested"
        assert "no_linked_test" in c.missing_links

    def test_linked_test_failed(self):
        job, iid = self._make_intent_only_job("approved")
        events = [
            {"event": "patch_intent_applied", "metadata": {"intent_id": iid, "outcome": "applied", "bytes_written": 50, "line_count": 5}},
            {"event": "patch_apply_proof_recorded", "metadata": {"intent_id": iid, "before_sha256": "a", "after_sha256": "b", "bytes_delta": 10}},
            {"event": "test_run_completed", "metadata": {"intent_id": iid, "status": "failed", "exit_code": 1}},
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

    def test_unrelated_later_test_does_not_verify(self):
        """Generic test after apply on multi-change job → INCOMPLETE"""
        task = Task(description="Multi-file fix")
        explanations = [
            _explanation_record("src/a.py"),
            _explanation_record("src/b.py"),
        ]
        art = _make_artifact_with_intents(task.id, explanations)
        iid_a = make_intent_id(art.id, 0)
        iid_b = make_intent_id(art.id, 1)
        approvals = {
            iid_a: {"state": "approved", "decided_at": "", "decided_by": ""},
            iid_b: {"state": "approved", "decided_at": "", "decided_by": ""},
        }
        art.metadata["patch_intent_approvals"] = approvals
        job = _make_job(tasks=[task], artifacts=[art])
        events = [
            {"event": "patch_intent_applied", "metadata": {"intent_id": iid_a, "outcome": "applied", "bytes_written": 50, "line_count": 5}},
            {"event": "patch_intent_applied", "metadata": {"intent_id": iid_b, "outcome": "applied", "bytes_written": 50, "line_count": 5}},
            {"event": "patch_apply_proof_recorded", "metadata": {"intent_id": iid_a, "before_sha256": "a", "after_sha256": "b", "bytes_delta": 10}},
            {"event": "patch_apply_proof_recorded", "metadata": {"intent_id": iid_b, "before_sha256": "c", "after_sha256": "d", "bytes_delta": 10}},
            # Generic test — cannot link to either change
            {"event": "test_run_completed", "metadata": {"status": "passed", "exit_code": 0}},
        ]
        chain = build_proof_chain(job, events)
        assert chain.overall_status != PROOF_VERIFIED
        for c in chain.changes:
            assert c.proof_status != PROOF_VERIFIED

    def test_explicit_not_required_verifies(self):
        """Explicit test_not_required event → verified"""
        job, iid = self._make_intent_only_job("approved", snapshot_verified=True)
        events = [
            {"event": "patch_intent_applied", "metadata": {"intent_id": iid, "outcome": "applied", "bytes_written": 50, "line_count": 5}},
            {"event": "patch_apply_proof_recorded", "metadata": {"intent_id": iid, "before_sha256": "a", "after_sha256": "b", "bytes_delta": 10}},
            {"event": "test_run_completed", "metadata": {"intent_id": iid, "test_not_required": True}},
        ]
        chain = build_proof_chain(job, events)
        c = chain.changes[0]
        assert c.proof_status == PROOF_VERIFIED
        assert c.test_state == "not_required"
        assert c.test_link == TEST_LINK_NOT_REQUIRED

    def test_generic_before_apply_sole_change_does_not_verify(self):
        job, iid = self._make_intent_only_job("approved")
        events = [
            {"event": "patch_intent_applied", "timestamp": "2026-01-01T00:01:00Z", "metadata": {"intent_id": iid, "outcome": "applied", "bytes_written": 50, "line_count": 5}},
            {"event": "patch_apply_proof_recorded", "metadata": {"intent_id": iid, "before_sha256": "a", "after_sha256": "b", "bytes_delta": 10}},
            {"event": "test_run_completed", "timestamp": "2026-01-01T00:00:00Z", "metadata": {"status": "passed", "exit_code": 0}},
        ]
        c = build_proof_chain(job, events).changes[0]
        assert c.proof_status == PROOF_INCOMPLETE
        assert c.test_link == TEST_LINK_NONE
        assert "no_test_after_apply" in c.missing_links

    def test_generic_after_apply_sole_change_verifies(self):
        job, iid = self._make_intent_only_job("approved", snapshot_verified=True)
        events = [
            {"event": "patch_intent_applied", "timestamp": "2026-01-01T00:00:00Z", "metadata": {"intent_id": iid, "outcome": "applied", "bytes_written": 50, "line_count": 5}},
            {"event": "patch_apply_proof_recorded", "metadata": {"intent_id": iid, "before_sha256": "a", "after_sha256": "b", "bytes_delta": 10}},
            {"event": "test_run_completed", "timestamp": "2026-01-01T00:01:00Z", "metadata": {"status": "passed", "exit_code": 0}},
        ]
        c = build_proof_chain(job, events).changes[0]
        assert c.proof_status == PROOF_VERIFIED
        assert c.test_link == TEST_LINK_SOLE_CHANGE

    def test_generic_missing_timestamp_sole_change_does_not_verify(self):
        job, iid = self._make_intent_only_job("approved")
        events = [
            {"event": "patch_intent_applied", "metadata": {"intent_id": iid, "outcome": "applied", "bytes_written": 50, "line_count": 5}},
            {"event": "patch_apply_proof_recorded", "metadata": {"intent_id": iid, "before_sha256": "a", "after_sha256": "b", "bytes_delta": 10}},
            {"event": "test_run_completed", "metadata": {"status": "passed", "exit_code": 0}},
        ]
        c = build_proof_chain(job, events).changes[0]
        assert c.proof_status == PROOF_INCOMPLETE
        assert c.test_link == TEST_LINK_NONE
        assert "test_order_unknown" in c.missing_links

    def test_intent_linked_missing_timestamp_can_verify(self):
        job, iid = self._make_intent_only_job("approved", snapshot_verified=True)
        events = [
            {"event": "patch_intent_applied", "metadata": {"intent_id": iid, "outcome": "applied", "bytes_written": 50, "line_count": 5}},
            {"event": "patch_apply_proof_recorded", "metadata": {"intent_id": iid, "before_sha256": "a", "after_sha256": "b", "bytes_delta": 10}},
            {"event": "test_run_completed", "metadata": {"intent_id": iid, "status": "passed", "exit_code": 0}},
        ]
        c = build_proof_chain(job, events).changes[0]
        assert c.proof_status == PROOF_VERIFIED
        assert c.test_link == TEST_LINK_INTENT

    def test_task_linked_missing_timestamp_can_verify(self):
        task = Task(description="Task")
        art = _make_artifact_with_intents(task.id, [_explanation_record("src/file.py")])
        iid = make_intent_id(art.id, 0)
        art.metadata["patch_intent_approvals"] = {iid: {"state": "approved", "decided_at": "", "decided_by": ""}}
        art.metadata["patch_intent_apply_records"] = {iid: {"snapshot_verified": True}}
        job = _make_job(tasks=[task], artifacts=[art])
        events = [
            {"event": "patch_intent_applied", "metadata": {"intent_id": iid, "outcome": "applied", "bytes_written": 50, "line_count": 5}},
            {"event": "patch_apply_proof_recorded", "metadata": {"intent_id": iid, "before_sha256": "a", "after_sha256": "b", "bytes_delta": 10}},
            {"event": "test_run_completed", "metadata": {"task_id": str(task.id), "status": "passed", "exit_code": 0}},
        ]
        c = build_proof_chain(job, events).changes[0]
        assert c.proof_status == PROOF_VERIFIED
        assert c.test_link == TEST_LINK_TASK

    def test_task_execution_blocked_linked(self):
        """task_execution_blocked for linked task → FAILED"""
        task = Task(description="Task")
        explanations = [_explanation_record("src/file.py")]
        art = _make_artifact_with_intents(task.id, explanations)
        intent_id = make_intent_id(art.id, 0)
        approvals = {intent_id: {"state": "approved", "decided_at": "", "decided_by": ""}}
        art.metadata["patch_intent_approvals"] = approvals
        job = _make_job(tasks=[task], artifacts=[art])
        events = [
            {"event": "patch_intent_applied", "metadata": {"intent_id": intent_id, "outcome": "applied", "bytes_written": 50, "line_count": 5}},
            {"event": "patch_apply_proof_recorded", "metadata": {"intent_id": intent_id, "before_sha256": "a", "after_sha256": "b", "bytes_delta": 10}},
            {"event": "task_execution_blocked", "metadata": {"task_id": str(task.id)}},
        ]
        chain = build_proof_chain(job, events)
        assert chain.changes[0].proof_status == PROOF_FAILED


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

    def test_summary_shows_test_link(self):
        job, events, _ = _make_full_chain_job()
        chain = build_proof_chain(job, events)
        text = summarize_proof_chain(chain)
        assert "test_link=" in text


# ---------------------------------------------------------------------------
# File provenance alignment (Step 835)
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

    def test_provenance_no_silent_swallow(self):
        """proof_error field exists and is empty on success"""
        from packages.orchestration.file_provenance import build_file_provenance
        job, events, _ = _make_full_chain_job()
        prov = build_file_provenance(job, events, "src/auth.py")
        assert prov.proof_error == ""

    def test_provenance_matches_change_proof(self):
        """file.why proof_status matches change proof --path"""
        from packages.orchestration.file_provenance import build_file_provenance
        job, events, _ = _make_full_chain_job()
        prov = build_file_provenance(job, events, "src/auth.py")
        chain = build_proof_chain(job, events, path="src/auth.py")
        if chain.changes:
            assert prov.proof_status == chain.changes[0].proof_status

    def test_provenance_omits_unlinked_global_test(self):
        """file.why must not show a generic test as proof when ordering is unknown."""
        from packages.orchestration.file_provenance import build_file_provenance
        task = Task(description="Task")
        art = _make_artifact_with_intents(task.id, [_explanation_record("src/file.py")])
        iid = make_intent_id(art.id, 0)
        art.metadata["patch_intent_approvals"] = {iid: {"state": "approved", "decided_at": "", "decided_by": ""}}
        job = _make_job(tasks=[task], artifacts=[art])
        events = [
            {"event": "patch_intent_applied", "metadata": {"intent_id": iid, "outcome": "applied", "bytes_written": 50, "line_count": 5}},
            {"event": "patch_apply_proof_recorded", "metadata": {"intent_id": iid, "before_sha256": "a", "after_sha256": "b", "bytes_delta": 10}},
            {"event": "test_run_completed", "metadata": {"status": "passed", "exit_code": 0, "command": "pytest"}},
        ]
        prov = build_file_provenance(job, events, "src/file.py")
        chain = build_proof_chain(job, events, path="src/file.py")
        assert prov.proof_status == chain.changes[0].proof_status == PROOF_INCOMPLETE
        assert all(link.step != "test_run" for link in prov.chain)

    def test_provenance_includes_intent_linked_test(self):
        """Linked test evidence may appear in file provenance."""
        from packages.orchestration.file_provenance import build_file_provenance
        job, events, _ = _make_full_chain_job(test_linked=True)
        prov = build_file_provenance(job, events, "src/auth.py")
        test_links = [link for link in prov.chain if link.step == "test_run"]
        assert len(test_links) == 1
        assert test_links[0].status == "passed"
        assert test_links[0].detail["test_link"] == TEST_LINK_INTENT

    def test_change_proof_path_does_not_turn_multichange_generic_test_into_sole_change(self):
        """Path filtering must not make a multi-change generic test look like sole-change proof."""
        task = Task(description="Multi-file fix")
        art = _make_artifact_with_intents(task.id, [_explanation_record("src/a.py"), _explanation_record("src/b.py")])
        iid_a = make_intent_id(art.id, 0)
        iid_b = make_intent_id(art.id, 1)
        art.metadata["patch_intent_approvals"] = {
            iid_a: {"state": "approved", "decided_at": "", "decided_by": ""},
            iid_b: {"state": "approved", "decided_at": "", "decided_by": ""},
        }
        job = _make_job(tasks=[task], artifacts=[art])
        events = [
            {"event": "patch_intent_applied", "timestamp": "2026-01-01T00:00:00Z", "metadata": {"intent_id": iid_a, "outcome": "applied", "bytes_written": 50, "line_count": 5}},
            {"event": "patch_intent_applied", "timestamp": "2026-01-01T00:00:00Z", "metadata": {"intent_id": iid_b, "outcome": "applied", "bytes_written": 50, "line_count": 5}},
            {"event": "patch_apply_proof_recorded", "metadata": {"intent_id": iid_a, "before_sha256": "a", "after_sha256": "b", "bytes_delta": 10}},
            {"event": "patch_apply_proof_recorded", "metadata": {"intent_id": iid_b, "before_sha256": "c", "after_sha256": "d", "bytes_delta": 10}},
            {"event": "test_run_completed", "timestamp": "2026-01-01T00:01:00Z", "metadata": {"status": "passed", "exit_code": 0}},
        ]
        chain = build_proof_chain(job, events, path="src/a.py")
        assert chain.changes[0].proof_status == PROOF_INCOMPLETE
        assert chain.changes[0].test_link == TEST_LINK_NONE


# ---------------------------------------------------------------------------
# Command catalog truth (Step 836)
# ---------------------------------------------------------------------------


class TestCommandCatalogTruth:

    def _get_all_next_action_commands(self):
        """Collect all possible next action commands from proof chain."""
        from packages.orchestration.proof_chain import _CATALOG_COMMANDS
        return _CATALOG_COMMANDS

    def test_catalog_commands_exist(self):
        from apps.cli.command_catalog import CATALOG
        catalog_ids = {c.command_id for c in CATALOG}
        for cmd_id in self._get_all_next_action_commands():
            assert cmd_id in catalog_ids, f"Next action references non-existent command: {cmd_id}"

    def test_verified_action_has_no_command(self):
        job, events, _ = _make_full_chain_job()
        chain = build_proof_chain(job, events)
        obj = chain.next_safe_action_obj
        assert obj is not None
        assert obj.command == ""  # no action needed = no command

    def test_pending_action_has_valid_command(self):
        task = Task(description="Fix bug")
        explanations = [_explanation_record("src/bug.py")]
        art = _make_artifact_with_intents(task.id, explanations)
        job = _make_job(tasks=[task], artifacts=[art])
        chain = build_proof_chain(job, [])
        obj = chain.next_safe_action_obj
        assert obj is not None
        assert obj.command != ""
        assert obj.available is True


# ---------------------------------------------------------------------------
# Durable snapshot truth in proof chain (Step 1158)
# ---------------------------------------------------------------------------


class TestProofChainDurableTruth:
    """build_proof_chain(data_dir=...) uses authoritative snapshot truth.

    Artifact metadata / events are never authoritative for the snapshot fact.
    """

    def _durable(self, data_dir, repo_root, job_id, intent_id, *,
                 state="applied", snapshot_id=None, make_snapshot=True):
        from packages.orchestration.repository_snapshot import (
            DurableApplyRecord,
            create_snapshot,
            save_durable_apply_record,
            verify_snapshot,
        )
        sid = snapshot_id
        if make_snapshot:
            (repo_root / "src").mkdir(parents=True, exist_ok=True)
            (repo_root / "src" / "auth.py").write_text("before\n")
            snap = create_snapshot(job_id, intent_id, ["src/auth.py"], repo_root, data_dir)
            verify_snapshot(snap.snapshot_id, job_id, data_dir)
            sid = snap.snapshot_id
        rec = DurableApplyRecord(
            apply_id=intent_id, job_id=job_id, intent_id=intent_id,
            snapshot_id=sid or "missing-snap", state=state,
            target_paths=["src/auth.py"], applied_at="2026-01-01T00:00:00Z",
            before_proof={}, after_proof={}, snapshot_verified=make_snapshot,
        )
        save_durable_apply_record(rec, job_id, data_dir)
        return sid

    def test_durable_snapshot_verifies(self, tmp_path):
        data_dir = tmp_path / "data"; data_dir.mkdir()
        repo = tmp_path / "repo"; repo.mkdir()
        job, events, iid = _make_full_chain_job()
        self._durable(data_dir, repo, str(job.id), iid)
        chain = build_proof_chain(job, events, data_dir=data_dir)
        assert chain.changes[0].proof_status == PROOF_VERIFIED

    def test_stale_metadata_but_snapshot_missing(self, tmp_path):
        """Artifact says snapshot_verified=True but durable snapshot is gone → NOT verified."""
        data_dir = tmp_path / "data"; data_dir.mkdir()
        repo = tmp_path / "repo"; repo.mkdir()
        job, events, iid = _make_full_chain_job()
        # Apply record references a snapshot that does not exist on disk.
        self._durable(data_dir, repo, str(job.id), iid, make_snapshot=False)
        chain = build_proof_chain(job, events, data_dir=data_dir)
        assert chain.changes[0].proof_status != PROOF_VERIFIED
        assert "no_snapshot_proof" in chain.changes[0].missing_links

    def test_reverted_apply_not_currently_applied(self, tmp_path):
        data_dir = tmp_path / "data"; data_dir.mkdir()
        repo = tmp_path / "repo"; repo.mkdir()
        job, events, iid = _make_full_chain_job()
        self._durable(data_dir, repo, str(job.id), iid, state="reverted")
        chain = build_proof_chain(job, events, data_dir=data_dir)
        assert chain.changes[0].apply_state == "reverted"
        assert chain.changes[0].proof_status != PROOF_VERIFIED

    def test_drift_blocked_revert_leaves_apply_active(self, tmp_path):
        from packages.orchestration.repository_snapshot import (
            _update_snapshot_state,
            load_durable_apply_record,
            save_durable_apply_record,
        )
        data_dir = tmp_path / "data"; data_dir.mkdir()
        repo = tmp_path / "repo"; repo.mkdir()
        job, events, iid = _make_full_chain_job()
        sid = self._durable(data_dir, repo, str(job.id), iid, state="applied")
        # Simulate a drift-blocked revert: snapshot flagged blocked_drift,
        # apply record stays applied with revert_state drifted.
        _update_snapshot_state(sid, str(job.id), "blocked_drift", data_dir)
        rec = load_durable_apply_record(iid, str(job.id), data_dir)
        import dataclasses
        save_durable_apply_record(
            dataclasses.replace(rec, revert_state="drifted"), str(job.id), data_dir
        )
        chain = build_proof_chain(job, events, data_dir=data_dir)
        # Drift block leaves the apply active and provable.
        assert chain.changes[0].apply_state == "applied"
        assert chain.changes[0].proof_status == PROOF_VERIFIED

    def test_missing_recovery_blob_blocks_verified(self, tmp_path):
        from packages.orchestration.repository_snapshot import _snapshot_dir
        data_dir = tmp_path / "data"; data_dir.mkdir()
        repo = tmp_path / "repo"; repo.mkdir()
        job, events, iid = _make_full_chain_job()
        sid = self._durable(data_dir, repo, str(job.id), iid)
        for blob in _snapshot_dir(str(job.id), sid, data_dir).glob("blob_*.bin"):
            blob.unlink()
        chain = build_proof_chain(job, events, data_dir=data_dir)
        assert chain.changes[0].proof_status != PROOF_VERIFIED

    def test_tampered_manifest_blocks_verified(self, tmp_path):
        from packages.orchestration.repository_snapshot import _snapshot_dir
        data_dir = tmp_path / "data"; data_dir.mkdir()
        repo = tmp_path / "repo"; repo.mkdir()
        job, events, iid = _make_full_chain_job()
        sid = self._durable(data_dir, repo, str(job.id), iid)
        manifest = _snapshot_dir(str(job.id), sid, data_dir) / "manifest.json"
        data = json.loads(manifest.read_text())
        data["path_count"] = 999
        manifest.write_text(json.dumps(data, indent=2, sort_keys=True))
        chain = build_proof_chain(job, events, data_dir=data_dir)
        assert chain.changes[0].proof_status != PROOF_VERIFIED


# ---------------------------------------------------------------------------
# The task apply fold (finding R-0738)
# ---------------------------------------------------------------------------


def _apply_change(task_id: str, apply_state: str) -> ProofChange:
    """One ProofChange carrying only the two fields the apply fold reads."""
    return ProofChange(
        target_path="a.py",
        intent_id="i",
        task_id=task_id,
        task_title="t",
        artifact_id="art",
        patch_intent_id="pi",
        approval_state="approved",
        apply_state=apply_state,
        test_state="passed",
        test_link=TEST_LINK_TASK,
        proof_status=PROOF_VERIFIED,
        safe_summary="",
        next_safe_action="",
    )


def _apply_chain(*changes: ProofChange) -> ProofChain:
    """A ProofChain around the given changes and nothing else."""
    return ProofChain(
        job_id="j",
        goal="g",
        path_filter="",
        changes=tuple(changes),
        overall_status=PROOF_VERIFIED,
        next_safe_action="",
    )


class TestFoldTaskApplyStates:
    """The apply fold AS A FUNCTION, from explicit inputs.

    Until this round the fold was reachable only through the cockpit, so every reading
    of it was also a reading of `_task_truth_maps`. Each case below is BUILT rather
    than observed: the mixed group in particular is constructed on purpose, which is
    what finding R-0738's resolution clause asks for.
    """

    def test_all_applied_folds_to_applied(self):
        folded = fold_task_apply_states(_apply_chain(
            _apply_change("t1", "applied"),
            _apply_change("t1", "applied"),
        ))
        assert folded["t1"].state == "applied"

    def test_all_reverted_folds_to_reverted(self):
        folded = fold_task_apply_states(_apply_chain(
            _apply_change("t1", "reverted"),
            _apply_change("t1", "reverted"),
        ))
        assert folded["t1"].state == "reverted"

    def test_none_applied_or_reverted_folds_to_not_applied(self):
        folded = fold_task_apply_states(_apply_chain(
            _apply_change("t1", "not_applied"),
            _apply_change("t1", "not_applied"),
            _apply_change("t1", "not_applied"),
        ))
        assert folded["t1"].state == "not_applied"

    def test_a_mixed_group_folds_to_partial(self):
        # THE DISCRIMINATOR: one change of three applied. The membership test this
        # fold replaced answered "applied" here, indistinguishable from a task where
        # every change had landed.
        folded = fold_task_apply_states(_apply_chain(
            _apply_change("t1", "applied"),
            _apply_change("t1", "not_applied"),
            _apply_change("t1", "not_applied"),
        ))
        assert folded["t1"].state == "partial"
        assert folded["t1"].state != "applied"

    def test_applied_and_reverted_together_fold_to_partial(self):
        folded = fold_task_apply_states(_apply_chain(
            _apply_change("t1", "applied"),
            _apply_change("t1", "reverted"),
        ))
        assert folded["t1"].state == "partial"

    def test_the_counts_on_a_mixed_group_differ_from_each_other(self):
        # Equal numbers would let a fold that returned the same value for both fields
        # pass, so the mixed case is the one that pins them apart.
        folded = fold_task_apply_states(_apply_chain(
            _apply_change("t1", "applied"),
            _apply_change("t1", "applied"),
            _apply_change("t1", "not_applied"),
            _apply_change("t1", "reverted"),
        ))
        assert folded["t1"].applied == 2
        assert folded["t1"].total == 4
        assert folded["t1"].applied != folded["t1"].total

    def test_the_total_is_the_group_size_when_nothing_applied(self):
        folded = fold_task_apply_states(_apply_chain(
            _apply_change("t1", "not_applied"),
            _apply_change("t1", "not_applied"),
            _apply_change("t1", "not_applied"),
        ))
        assert folded["t1"].applied == 0
        assert folded["t1"].total == 3

    def test_a_unanimous_apply_counts_every_change(self):
        folded = fold_task_apply_states(_apply_chain(
            _apply_change("t1", "applied"),
            _apply_change("t1", "applied"),
        ))
        assert folded["t1"].applied == 2
        assert folded["t1"].total == 2

    def test_a_reverted_change_is_not_counted_as_applied(self):
        folded = fold_task_apply_states(_apply_chain(
            _apply_change("t1", "reverted"),
            _apply_change("t1", "reverted"),
        ))
        assert folded["t1"].applied == 0
        assert folded["t1"].total == 2

    def test_the_entry_is_a_task_apply_state(self):
        folded = fold_task_apply_states(_apply_chain(_apply_change("t1", "applied")))
        assert isinstance(folded["t1"], TaskApplyState)

    def test_a_none_chain_folds_to_an_empty_dict(self):
        assert fold_task_apply_states(None) == {}

    def test_a_change_with_an_empty_task_id_is_skipped(self):
        folded = fold_task_apply_states(_apply_chain(
            _apply_change("", "applied"),
            _apply_change("t1", "applied"),
        ))
        assert "" not in folded
        assert folded["t1"].total == 1

    def test_two_tasks_in_one_chain_are_folded_independently(self):
        folded = fold_task_apply_states(_apply_chain(
            _apply_change("t1", "applied"),
            _apply_change("t1", "applied"),
            _apply_change("t2", "applied"),
            _apply_change("t2", "not_applied"),
        ))
        assert folded["t1"].state == "applied"
        assert folded["t1"].applied == 2
        assert folded["t1"].total == 2
        assert folded["t2"].state == "partial"
        assert folded["t2"].applied == 1
        assert folded["t2"].total == 2

    def test_the_full_task_id_is_the_key(self):
        # Keyed by the FULL id, never a prefix: two tasks whose ids share a prefix
        # must not collapse onto one entry.
        long_id = "0123456789abcdef-task-one"
        other_id = "0123456789abcdef-task-two"
        folded = fold_task_apply_states(_apply_chain(
            _apply_change(long_id, "applied"),
            _apply_change(other_id, "not_applied"),
        ))
        assert folded[long_id].state == "applied"
        assert folded[other_id].state == "not_applied"
