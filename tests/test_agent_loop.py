"""
Tests for packages/orchestration/agent_loop.py and the `remedy agent-loop` CLI command.

Coverage:
  - default state fields
  - pending tasks → continue/build
  - permission_denied event (still active) → blocked
  - blocked takes priority over pending tasks
  - completed tasks + pending medium/high/unknown intent → needs_approval
  - completed tasks + approved intent → complete
  - unknown/high risks treated conservatively (needs_approval)
  - low-risk pending intent does not force approval
  - no tasks → continue/planned (NOT complete)
  - custom max_cycles
  - job_id preserved in state
  - frozen models reject mutation
  - AgentAdapterSpec defaults
  - summarize output: header, short id, job name, stage, decision, cycle
  - summarize sections: Agents, Loop state, Next action
  - next action for each decision type
  - blockers display: "permission_denied (workspace_write)"
  - next action uses concrete capability: "remedy job permit … workspace_write allow"
  - stale blocker fix: historical perm_denied + task_run_completed → not blocked
  - historical perm_denied + later pass + pending medium intent → needs_approval
  - historical perm_denied + later pass + approved intent → complete
  - current workspace_write explicitly denied + pending task → blocked (no event needed)
  - no tasks + old perm_denied event → planned/continue, not blocked
  - no pending tasks + old perm_denied event → complete or non-blocked
  - redaction: sentinels never appear in summary or run log
  - CLI: invalid UUID exits 1
  - CLI: unknown job exits 1
  - CLI: valid job prints report
  - CLI: logs agent_loop_inspected with exactly the required metadata keys
  - CLI: run log event contains no raw artifact content
  - CLI: exactly one run log file created
"""

from __future__ import annotations

import json
from uuid import uuid4

import pytest

from packages.core.models import Artifact, ArtifactKind, Job, RunState, Task
from packages.orchestration.agent_loop import (
    AgentAdapterSpec,
    AgentLoopDecision,
    AgentLoopStage,
    AgentRole,
    default_agent_loop_state,
    derive_agent_loop_state,
    summarize_agent_loop_state,
)
from packages.orchestration.approval_queue import (
    APPROVAL_APPROVED,
    make_intent_id,
    set_approval_state,
)
from packages.orchestration.patch_intent import (
    RISK_HIGH,
    RISK_LOW,
    RISK_MEDIUM,
    RISK_UNKNOWN,
)
from packages.orchestration.permissions import Capability, set_permission
from packages.orchestration.storage import save_job

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_job(**kwargs) -> Job:
    defaults: dict = {"name": "Test loop job", "state": RunState.PENDING}
    defaults.update(kwargs)
    return Job(**defaults)


def _pending_task(**kwargs) -> Task:
    return Task(description="write docs", inputs={"task_type": "write_readme"}, **kwargs)


def _completed_task(**kwargs) -> Task:
    t = Task(description="done", inputs={"task_type": "write_readme"}, **kwargs)
    t.status = RunState.COMPLETED
    return t


def _add_patch_artifact(job: Job, *, risk: str = RISK_MEDIUM, intent_count: int = 1) -> str:
    """Add a patch-intent artifact to job. Returns the first intent_id."""
    explanations = [
        {
            "file": f"docs/file_{i}.md",
            "action": "modify",
            "risk": risk,
            "reason": "task type 'write_readme'",
            "summary": f"Change {i}",
        }
        for i in range(intent_count)
    ]
    artifact = Artifact(
        name="proposal",
        content="",
        kind=ArtifactKind.BUILDER_PROPOSAL,
        task_id=uuid4(),
        metadata={
            "patch_intent_explanations": explanations,
            "patch_intent_risks": [risk] * intent_count,
        },
    )
    job.artifacts.append(artifact)
    return make_intent_id(artifact.id, 0)


def _perm_denied_event(job_id: str, *, task_id: str | None = None) -> dict:
    ev: dict = {
        "event": "task_run_failed",
        "job_id": job_id,
        "run_id": "r1",
        "timestamp": "2026-05-06T10:00:00+00:00",
        "outcome": "permission_denied",
        "metadata": {"capability": "workspace_write"},
    }
    if task_id is not None:
        ev["task_id"] = task_id
    return ev


def _task_completed_event(job_id: str, task_id: str) -> dict:
    return {
        "event": "task_run_completed",
        "job_id": job_id,
        "run_id": "r2",
        "timestamp": "2026-05-06T10:01:00+00:00",
        "task_id": task_id,
        "outcome": "pass",
        "metadata": {},
    }


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


class TestModels:
    def test_default_state_fields(self):
        job = _make_job()
        state = default_agent_loop_state(job)
        assert state.job_id == job.id
        assert state.current_stage == AgentLoopStage.PLANNED
        assert state.cycle == 0
        assert state.max_cycles == 3
        assert state.decision == AgentLoopDecision.CONTINUE
        assert state.builder is None
        assert state.reviewer is None
        assert state.pending_findings == ()
        assert state.completed_cycles == 0
        assert state.blocked_reason is None

    def test_default_state_custom_max_cycles(self):
        job = _make_job()
        state = default_agent_loop_state(job, max_cycles=5)
        assert state.max_cycles == 5

    def test_agent_adapter_spec_defaults(self):
        spec = AgentAdapterSpec(name="test", role=AgentRole.BUILDER, provider="local")
        assert spec.dry_run_only is True
        assert spec.capabilities == frozenset()
        assert spec.notes == ()
        assert spec.command_hint is None

    def test_agent_adapter_spec_frozen(self):
        spec = AgentAdapterSpec(name="test", role=AgentRole.REVIEWER, provider="local")
        with pytest.raises((AttributeError, TypeError)):
            spec.name = "other"  # type: ignore[misc]

    def test_loop_state_frozen(self):
        job = _make_job()
        state = default_agent_loop_state(job)
        with pytest.raises((AttributeError, TypeError)):
            state.cycle = 1  # type: ignore[misc]

    def test_agent_role_values(self):
        assert AgentRole.PLANNER.value == "planner"
        assert AgentRole.BUILDER.value == "builder"
        assert AgentRole.REVIEWER.value == "reviewer"
        assert AgentRole.FIXER.value == "fixer"
        assert AgentRole.VERIFIER.value == "verifier"
        assert AgentRole.REPORTER.value == "reporter"

    def test_loop_stage_values(self):
        assert AgentLoopStage.BUILD.value == "build"
        assert AgentLoopStage.BLOCKED.value == "blocked"
        assert AgentLoopStage.COMPLETED.value == "completed"

    def test_loop_decision_continue_value(self):
        assert AgentLoopDecision.CONTINUE.value == "continue"

    def test_loop_decision_complete_value(self):
        assert AgentLoopDecision.COMPLETE.value == "complete"


# ---------------------------------------------------------------------------
# derive_agent_loop_state
# ---------------------------------------------------------------------------


class TestDeriveLoopState:
    def test_no_tasks_gives_continue_planned(self):
        job = _make_job()
        state = derive_agent_loop_state(job, [])
        assert state.decision == AgentLoopDecision.CONTINUE
        assert state.current_stage == AgentLoopStage.PLANNED

    def test_pending_task_gives_continue_build(self):
        job = _make_job()
        job.tasks.append(_pending_task())
        state = derive_agent_loop_state(job, [])
        assert state.decision == AgentLoopDecision.CONTINUE
        assert state.current_stage == AgentLoopStage.BUILD

    def test_active_perm_denied_event_with_pending_task_gives_blocked(self):
        """Unresolved permission_denied + pending task → blocked."""
        job = _make_job()
        task = _pending_task()
        job.tasks.append(task)
        events = [_perm_denied_event(str(job.id), task_id=str(task.id))]
        state = derive_agent_loop_state(job, events)
        assert state.decision == AgentLoopDecision.BLOCKED
        assert state.current_stage == AgentLoopStage.BLOCKED
        assert state.blocked_reason is not None
        assert "permission_denied" in state.blocked_reason

    def test_blocked_reason_includes_capability(self):
        """blocked_reason encodes the denied capability."""
        job = _make_job()
        task = _pending_task()
        job.tasks.append(task)
        events = [_perm_denied_event(str(job.id), task_id=str(task.id))]
        state = derive_agent_loop_state(job, events)
        assert state.blocked_reason == "permission_denied:workspace_write"

    def test_perm_denied_no_task_id_conservative_with_pending_tasks(self):
        """No task_id → cannot prove stale → still blocked when pending tasks exist."""
        job = _make_job()
        job.tasks.append(_pending_task())
        events = [_perm_denied_event(str(job.id))]  # no task_id
        state = derive_agent_loop_state(job, events)
        assert state.decision == AgentLoopDecision.BLOCKED

    def test_blocked_takes_priority_over_pending_tasks(self):
        job = _make_job()
        task = _pending_task()
        job.tasks.append(task)
        events = [_perm_denied_event(str(job.id), task_id=str(task.id))]
        state = derive_agent_loop_state(job, events)
        assert state.decision == AgentLoopDecision.BLOCKED

    # ── Stale-blocker fix ──────────────────────────────────────────────────

    def test_historical_perm_denied_then_completed_is_not_blocked(self):
        """task_run_completed supersedes historical permission_denied — not blocked."""
        task = _completed_task()
        job = _make_job()
        job.tasks.append(task)
        events = [
            _perm_denied_event(str(job.id), task_id=str(task.id)),
            _task_completed_event(str(job.id), str(task.id)),
        ]
        state = derive_agent_loop_state(job, events)
        assert state.decision != AgentLoopDecision.BLOCKED

    def test_historical_perm_denied_then_completed_then_pending_medium_intent(self):
        """Stale perm_denied + task success + pending medium intent → needs_approval."""
        task = _completed_task()
        job = _make_job()
        job.tasks.append(task)
        _add_patch_artifact(job, risk=RISK_MEDIUM)
        events = [
            _perm_denied_event(str(job.id), task_id=str(task.id)),
            _task_completed_event(str(job.id), str(task.id)),
        ]
        state = derive_agent_loop_state(job, events)
        assert state.decision == AgentLoopDecision.NEEDS_APPROVAL
        assert state.current_stage == AgentLoopStage.REVIEW

    def test_historical_perm_denied_then_completed_then_approved_intent(self):
        """Stale perm_denied + task success + approved intent → complete."""
        task = _completed_task()
        job = _make_job()
        job.tasks.append(task)
        intent_id = _add_patch_artifact(job, risk=RISK_MEDIUM)
        set_approval_state(job, intent_id, APPROVAL_APPROVED)
        events = [
            _perm_denied_event(str(job.id), task_id=str(task.id)),
            _task_completed_event(str(job.id), str(task.id)),
        ]
        state = derive_agent_loop_state(job, events)
        assert state.decision == AgentLoopDecision.COMPLETE

    def test_no_tasks_plus_old_perm_denied_gives_planned_not_blocked(self):
        """Old perm_denied event with no pending tasks → planned/continue, not blocked."""
        job = _make_job()
        events = [_perm_denied_event(str(job.id))]
        state = derive_agent_loop_state(job, events)
        assert state.decision == AgentLoopDecision.CONTINUE
        assert state.current_stage == AgentLoopStage.PLANNED
        assert state.blocked_reason is None

    def test_no_pending_tasks_plus_old_perm_denied_not_blocked(self):
        """Completed task + old perm_denied for it → complete or non-blocked."""
        task = _completed_task()
        job = _make_job()
        job.tasks.append(task)
        events = [_perm_denied_event(str(job.id), task_id=str(task.id))]
        state = derive_agent_loop_state(job, events)
        assert state.decision != AgentLoopDecision.BLOCKED

    def test_perm_denied_in_metadata_no_tasks_gives_continue(self):
        """Perm denied in metadata only + no tasks → continue/planned, not blocked."""
        job = _make_job()
        ev = {
            "event": "task_run_failed",
            "job_id": str(job.id),
            "run_id": "r1",
            "timestamp": "2026-05-06T10:00:00+00:00",
            "metadata": {"outcome": "permission_denied"},
        }
        state = derive_agent_loop_state(job, [ev])
        assert state.decision == AgentLoopDecision.CONTINUE
        assert state.blocked_reason is None

    # ── Current permission model block ─────────────────────────────────────

    def test_current_workspace_write_denied_and_pending_task_gives_blocked(self):
        """Explicit capability denial in job permissions + pending task → blocked."""
        job = _make_job()
        job.tasks.append(_pending_task())
        set_permission(job, Capability.workspace_write, allow=False)
        state = derive_agent_loop_state(job, [])  # no events needed
        assert state.decision == AgentLoopDecision.BLOCKED
        assert state.blocked_reason == "permission_denied:workspace_write"

    def test_current_deny_no_pending_tasks_does_not_block(self):
        """Explicit capability denial but no pending tasks → not blocked."""
        job = _make_job()
        job.tasks.append(_completed_task())
        set_permission(job, Capability.workspace_write, allow=False)
        state = derive_agent_loop_state(job, [])
        assert state.decision != AgentLoopDecision.BLOCKED

    # ── Patch intent tests ─────────────────────────────────────────────────

    def test_pending_medium_intent_gives_needs_approval(self):
        job = _make_job()
        job.tasks.append(_completed_task())
        _add_patch_artifact(job, risk=RISK_MEDIUM)
        state = derive_agent_loop_state(job, [])
        assert state.decision == AgentLoopDecision.NEEDS_APPROVAL
        assert state.current_stage == AgentLoopStage.REVIEW

    def test_pending_high_risk_is_conservative(self):
        job = _make_job()
        job.tasks.append(_completed_task())
        _add_patch_artifact(job, risk=RISK_HIGH)
        state = derive_agent_loop_state(job, [])
        assert state.decision == AgentLoopDecision.NEEDS_APPROVAL

    def test_pending_unknown_risk_is_conservative(self):
        job = _make_job()
        job.tasks.append(_completed_task())
        _add_patch_artifact(job, risk=RISK_UNKNOWN)
        state = derive_agent_loop_state(job, [])
        assert state.decision == AgentLoopDecision.NEEDS_APPROVAL

    def test_pending_low_risk_does_not_force_approval(self):
        job = _make_job()
        job.tasks.append(_completed_task())
        _add_patch_artifact(job, risk=RISK_LOW)
        state = derive_agent_loop_state(job, [])
        assert state.decision != AgentLoopDecision.NEEDS_APPROVAL

    def test_completed_tasks_all_non_low_approved_gives_complete(self):
        job = _make_job()
        job.tasks.append(_completed_task())
        intent_id = _add_patch_artifact(job, risk=RISK_MEDIUM)
        set_approval_state(job, intent_id, APPROVAL_APPROVED)
        state = derive_agent_loop_state(job, [])
        assert state.decision == AgentLoopDecision.COMPLETE
        assert state.current_stage == AgentLoopStage.COMPLETED

    def test_completed_tasks_no_intents_gives_complete(self):
        job = _make_job()
        job.tasks.append(_completed_task())
        state = derive_agent_loop_state(job, [])
        assert state.decision == AgentLoopDecision.COMPLETE

    def test_low_risk_pending_still_complete_when_tasks_done(self):
        job = _make_job()
        job.tasks.append(_completed_task())
        _add_patch_artifact(job, risk=RISK_LOW)
        state = derive_agent_loop_state(job, [])
        assert state.decision == AgentLoopDecision.COMPLETE

    def test_pending_tasks_plus_pending_non_low_gives_needs_approval(self):
        job = _make_job()
        job.tasks.append(_pending_task())
        _add_patch_artifact(job, risk=RISK_HIGH)
        state = derive_agent_loop_state(job, [])
        assert state.decision == AgentLoopDecision.NEEDS_APPROVAL

    # ── General ────────────────────────────────────────────────────────────

    def test_job_id_preserved(self):
        job = _make_job()
        state = derive_agent_loop_state(job, [])
        assert state.job_id == job.id

    def test_custom_max_cycles_preserved(self):
        job = _make_job()
        state = derive_agent_loop_state(job, [], max_cycles=7)
        assert state.max_cycles == 7

    def test_no_events_no_tasks_no_intents_is_continue(self):
        job = _make_job()
        state = derive_agent_loop_state(job, [])
        assert state.decision == AgentLoopDecision.CONTINUE
        assert state.blocked_reason is None

    def test_irrelevant_events_ignored(self):
        job = _make_job()
        job.tasks.append(_pending_task())
        events = [
            {"event": "project_constitution_loaded", "job_id": str(job.id),
             "run_id": "r1", "timestamp": "2026-05-06T10:00:00+00:00",
             "metadata": {"source_count": 3}},
        ]
        state = derive_agent_loop_state(job, events)
        assert state.decision == AgentLoopDecision.CONTINUE
        assert state.current_stage == AgentLoopStage.BUILD


# ---------------------------------------------------------------------------
# summarize_agent_loop_state
# ---------------------------------------------------------------------------


class TestSummarizeLoopState:
    def test_header_present(self):
        job = _make_job()
        state = default_agent_loop_state(job)
        out = summarize_agent_loop_state(job, state)
        assert "Remedy Agent Loop" in out

    def test_short_job_id_shown(self):
        job = _make_job()
        state = default_agent_loop_state(job)
        out = summarize_agent_loop_state(job, state)
        assert str(job.id)[:8] in out

    def test_job_name_shown(self):
        job = _make_job(name="My agent job")
        state = default_agent_loop_state(job)
        out = summarize_agent_loop_state(job, state)
        assert "My agent job" in out

    def test_stage_shown(self):
        job = _make_job()
        state = default_agent_loop_state(job)
        out = summarize_agent_loop_state(job, state)
        assert "Stage:" in out
        assert "planned" in out

    def test_decision_shown(self):
        job = _make_job()
        state = default_agent_loop_state(job)
        out = summarize_agent_loop_state(job, state)
        assert "Decision:" in out
        assert "continue" in out

    def test_cycle_shown(self):
        job = _make_job()
        state = default_agent_loop_state(job)
        out = summarize_agent_loop_state(job, state)
        assert "Cycle: 0/3" in out

    def test_agents_section_present(self):
        job = _make_job()
        state = default_agent_loop_state(job)
        out = summarize_agent_loop_state(job, state)
        assert "Agents" in out
        assert "builder:" in out
        assert "reviewer:" in out
        assert "not configured" in out

    def test_loop_state_section_present(self):
        job = _make_job()
        state = default_agent_loop_state(job)
        out = summarize_agent_loop_state(job, state)
        assert "Loop state" in out
        assert "pending tasks:" in out
        assert "patch decisions:" in out
        assert "blockers:" in out

    def test_next_action_section_present(self):
        job = _make_job()
        state = default_agent_loop_state(job)
        out = summarize_agent_loop_state(job, state)
        assert "Next action" in out

    def test_next_action_build_suggests_run_task(self):
        job = _make_job()
        job.tasks.append(_pending_task())
        state = derive_agent_loop_state(job, [])
        out = summarize_agent_loop_state(job, state)
        assert "job run-next" in out

    def test_next_action_planned_suggests_plan(self):
        job = _make_job()
        state = derive_agent_loop_state(job, [])
        out = summarize_agent_loop_state(job, state)
        assert "job plan" in out

    def test_next_action_blocked_suggests_set_permission_with_capability(self):
        """Next action for BLOCKED must include the concrete capability name."""
        job = _make_job()
        task = _pending_task()
        job.tasks.append(task)
        events = [_perm_denied_event(str(job.id), task_id=str(task.id))]
        state = derive_agent_loop_state(job, events)
        out = summarize_agent_loop_state(job, state)
        assert "job permit" in out
        assert "workspace_write" in out

    def test_next_action_blocked_no_capability_fallback(self):
        """BLOCKED with no known capability falls back to <capability>."""
        job = _make_job()
        job.tasks.append(_pending_task())
        # Event with no task_id and no capability in metadata
        ev = {
            "event": "task_run_failed",
            "job_id": str(job.id),
            "run_id": "r1",
            "timestamp": "2026-05-06T10:00:00+00:00",
            "outcome": "permission_denied",
            "metadata": {},
        }
        state = derive_agent_loop_state(job, [ev])
        out = summarize_agent_loop_state(job, state)
        assert "job permit" in out
        assert "<capability>" in out

    def test_next_action_needs_approval_suggests_list_intents(self):
        job = _make_job()
        job.tasks.append(_completed_task())
        _add_patch_artifact(job, risk=RISK_MEDIUM)
        state = derive_agent_loop_state(job, [])
        out = summarize_agent_loop_state(job, state)
        assert "patch list" in out

    def test_next_action_complete_suggests_trust_report(self):
        job = _make_job()
        job.tasks.append(_completed_task())
        state = derive_agent_loop_state(job, [])
        out = summarize_agent_loop_state(job, state)
        assert "brain trust" in out

    def test_blockers_display_includes_capability_parens(self):
        """Blocker with capability → 'permission_denied (workspace_write)'."""
        job = _make_job()
        task = _pending_task()
        job.tasks.append(task)
        events = [_perm_denied_event(str(job.id), task_id=str(task.id))]
        state = derive_agent_loop_state(job, events)
        out = summarize_agent_loop_state(job, state)
        assert "permission_denied (workspace_write)" in out

    def test_blockers_none_when_clean(self):
        job = _make_job()
        state = default_agent_loop_state(job)
        out = summarize_agent_loop_state(job, state)
        assert "blockers: none" in out

    def test_patch_intent_count_shown(self):
        job = _make_job()
        _add_patch_artifact(job, risk=RISK_MEDIUM)
        state = derive_agent_loop_state(job, [])
        out = summarize_agent_loop_state(job, state)
        assert "patch decisions" in out
        assert "medium" in out

    def test_no_raw_artifact_content_in_output(self):
        job = _make_job()
        job.artifacts.append(Artifact(
            name="proposal",
            content="SUPER SECRET CONTENT MUST NOT APPEAR",
            kind=ArtifactKind.BUILDER_PROPOSAL,
        ))
        state = derive_agent_loop_state(job, [])
        out = summarize_agent_loop_state(job, state)
        assert "SUPER SECRET CONTENT MUST NOT APPEAR" not in out

    def test_no_approval_reason_in_output(self):
        job = _make_job()
        job.tasks.append(_completed_task())
        intent_id = _add_patch_artifact(job, risk=RISK_MEDIUM)
        set_approval_state(job, intent_id, APPROVAL_APPROVED, reason="sensitive approval reason")
        state = derive_agent_loop_state(job, [])
        out = summarize_agent_loop_state(job, state)
        assert "sensitive approval reason" not in out

    def test_no_raw_event_message_in_output(self):
        job = _make_job()
        events = [
            {
                "event": "task_run_failed",
                "job_id": str(job.id),
                "run_id": "r1",
                "timestamp": "2026-05-06T10:00:00+00:00",
                "outcome": "permission_denied",
                "message": "RAW EXCEPTION TEXT MUST NOT APPEAR IN OUTPUT",
                "metadata": {},
            }
        ]
        state = derive_agent_loop_state(job, events)
        out = summarize_agent_loop_state(job, state)
        assert "RAW EXCEPTION TEXT MUST NOT APPEAR IN OUTPUT" not in out

    def test_long_name_truncated(self):
        name = "A" * 80
        job = _make_job(name=name)
        state = default_agent_loop_state(job)
        out = summarize_agent_loop_state(job, state)
        assert name not in out
        assert "…" in out

    def test_pending_tasks_count_shown(self):
        job = _make_job()
        job.tasks.append(_pending_task())
        job.tasks.append(_pending_task())
        state = derive_agent_loop_state(job, [])
        out = summarize_agent_loop_state(job, state)
        assert "pending tasks: 2" in out


# ---------------------------------------------------------------------------
# Redaction hardening
# ---------------------------------------------------------------------------


class TestRedactionHardening:
    """Verify that sentinel strings never appear in any output or run log."""

    SENTINELS = {
        "DIFF_PREVIEW_MUST_NOT_RENDER",
        "RAW_COMMAND_OUTPUT_MUST_NOT_RENDER",
        "APPROVAL_REASON_MUST_NOT_RENDER",
        "EVENT_MESSAGE_MUST_NOT_RENDER",
        "ARTIFACT_CONTENT_MUST_NOT_RENDER",
    }

    def _make_job_with_sentinels(self) -> Job:
        job = _make_job()
        job.tasks.append(_completed_task())
        artifact = Artifact(
            name="proposal",
            content="ARTIFACT_CONTENT_MUST_NOT_RENDER",
            kind=ArtifactKind.BUILDER_PROPOSAL,
            task_id=uuid4(),
            metadata={
                "patch_intent_explanations": [
                    {
                        "file": "docs/x.md",
                        "action": "modify",
                        "risk": RISK_MEDIUM,
                        "reason": "test",
                        "summary": "s",
                    }
                ],
                "patch_intent_risks": [RISK_MEDIUM],
                "patch_intent_diff_preview": "DIFF_PREVIEW_MUST_NOT_RENDER",
            },
        )
        job.artifacts.append(artifact)
        intent_id = make_intent_id(artifact.id, 0)
        set_approval_state(
            job, intent_id, APPROVAL_APPROVED,
            reason="APPROVAL_REASON_MUST_NOT_RENDER",
        )
        return job

    def _sentinel_events(self, job_id: str) -> list[dict]:
        return [
            {
                "event": "task_run_completed",
                "job_id": job_id,
                "run_id": "r1",
                "timestamp": "2026-05-06T10:00:00+00:00",
                "message": "EVENT_MESSAGE_MUST_NOT_RENDER",
                "metadata": {"command_output": "RAW_COMMAND_OUTPUT_MUST_NOT_RENDER"},
            }
        ]

    def test_no_sentinels_in_summary_output(self):
        job = self._make_job_with_sentinels()
        events = self._sentinel_events(str(job.id))
        state = derive_agent_loop_state(job, events)
        out = summarize_agent_loop_state(job, state)
        for sentinel in self.SENTINELS:
            assert sentinel not in out, f"sentinel {sentinel!r} leaked into summary"

    def test_no_sentinels_in_run_log_event(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = self._make_job_with_sentinels()
        save_job(job)
        from apps.cli.commands.brain import _cmd_agent_loop
        _cmd_agent_loop(str(job.id))
        capsys.readouterr()
        runs_dir = tmp_path / "job_logs" / str(job.id)
        combined = "".join(f.read_text() for f in runs_dir.glob("*.jsonl"))
        for sentinel in self.SENTINELS:
            assert sentinel not in combined, f"sentinel {sentinel!r} leaked into run log"


# ---------------------------------------------------------------------------
# CLI tests
# ---------------------------------------------------------------------------


class TestCLIAgentLoop:
    def test_invalid_uuid_exits_1(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from apps.cli.commands.brain import _cmd_agent_loop
        with pytest.raises(SystemExit) as exc:
            _cmd_agent_loop("not-a-uuid")
        assert exc.value.code == 1

    def test_unknown_job_exits_1(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from apps.cli.commands.brain import _cmd_agent_loop
        with pytest.raises(SystemExit) as exc:
            _cmd_agent_loop(str(uuid4()))
        assert exc.value.code == 1

    def test_valid_job_prints_report(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        from apps.cli.commands.brain import _cmd_agent_loop
        _cmd_agent_loop(str(job.id))
        out = capsys.readouterr().out
        assert "Remedy Agent Loop" in out
        assert str(job.id)[:8] in out

    def test_cli_logs_agent_loop_inspected_event(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        from apps.cli.commands.brain import _cmd_agent_loop
        _cmd_agent_loop(str(job.id))
        capsys.readouterr()
        runs_dir = tmp_path / "job_logs" / str(job.id)
        events = []
        for f in runs_dir.glob("*.jsonl"):
            for line in f.read_text().splitlines():
                if line.strip():
                    events.append(json.loads(line))
        ev = next((e for e in events if e.get("event") == "agent_loop_inspected"), None)
        assert ev is not None

    def test_run_log_metadata_has_exactly_required_fields(self, tmp_path, monkeypatch, capsys):
        """agent_loop_inspected metadata must contain exactly the fixed schema."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        from apps.cli.commands.brain import _cmd_agent_loop
        _cmd_agent_loop(str(job.id))
        capsys.readouterr()
        runs_dir = tmp_path / "job_logs" / str(job.id)
        events = []
        for f in runs_dir.glob("*.jsonl"):
            for line in f.read_text().splitlines():
                if line.strip():
                    events.append(json.loads(line))
        ev = next(e for e in events if e.get("event") == "agent_loop_inspected")
        meta = ev.get("metadata", {})
        assert set(meta.keys()) == {
            "stage", "decision", "cycle", "max_cycles", "pending_finding_count"
        }

    def test_run_log_event_no_raw_artifact_content(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        job.artifacts.append(Artifact(
            name="proposal",
            content="ARTIFACT RAW CONTENT MUST NOT BE LOGGED",
            kind=ArtifactKind.BUILDER_PROPOSAL,
        ))
        save_job(job)
        from apps.cli.commands.brain import _cmd_agent_loop
        _cmd_agent_loop(str(job.id))
        capsys.readouterr()
        runs_dir = tmp_path / "job_logs" / str(job.id)
        combined = "".join(f.read_text() for f in runs_dir.glob("*.jsonl"))
        assert "ARTIFACT RAW CONTENT MUST NOT BE LOGGED" not in combined

    def test_exactly_one_run_log_file_created(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        from apps.cli.commands.brain import _cmd_agent_loop
        _cmd_agent_loop(str(job.id))
        capsys.readouterr()
        runs_dir = tmp_path / "job_logs" / str(job.id)
        assert len(list(runs_dir.glob("*.jsonl"))) == 1

    def test_cli_output_no_raw_approval_reason(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        job.tasks.append(_completed_task())
        intent_id = _add_patch_artifact(job, risk=RISK_MEDIUM)
        set_approval_state(job, intent_id, APPROVAL_APPROVED, reason="top secret reason")
        save_job(job)
        from apps.cli.commands.brain import _cmd_agent_loop
        _cmd_agent_loop(str(job.id))
        out = capsys.readouterr().out
        assert "top secret reason" not in out
