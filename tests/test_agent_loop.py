"""
Tests for packages/orchestration/agent_loop.py and the `remedy agent-loop` CLI command.

Coverage:
  - default state fields
  - pending tasks → continue/build
  - permission_denied event → blocked
  - blocked takes priority over pending tasks
  - completed tasks + pending medium/high/unknown intent → needs_approval
  - completed tasks + approved intent → complete
  - unknown/high risks treated conservatively (needs_approval)
  - low-risk pending intent does not force approval
  - no tasks → continue/planned
  - no tasks + completed → complete
  - custom max_cycles
  - job_id preserved in state
  - frozen models reject mutation
  - AgentAdapterSpec defaults
  - summarize output: header, short id, job name, stage, decision, cycle
  - summarize sections: Agents, Loop state, Next action
  - next action for each decision type
  - redaction: no artifact content, approval reasons, raw event.message
  - patch intent count shown in output
  - CLI: invalid UUID exits 1
  - CLI: unknown job exits 1
  - CLI: valid job prints report
  - CLI: logs agent_loop_inspected with counts/labels only
  - CLI: run log event contains no raw artifact content
  - CLI: exactly one run log file created
"""

from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

import pytest

from packages.core.models import Artifact, ArtifactKind, Job, RunState, Task
from packages.orchestration.agent_loop import (
    AgentAdapterSpec,
    AgentLoopDecision,
    AgentLoopStage,
    AgentLoopState,
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


def _perm_denied_event(job_id: str) -> dict:
    return {
        "event": "task_run_failed",
        "job_id": job_id,
        "run_id": "r1",
        "timestamp": "2026-05-06T10:00:00+00:00",
        "outcome": "permission_denied",
        "metadata": {"capability": "workspace_write"},
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

    def test_permission_denied_event_gives_blocked(self):
        job = _make_job()
        events = [_perm_denied_event(str(job.id))]
        state = derive_agent_loop_state(job, events)
        assert state.decision == AgentLoopDecision.BLOCKED
        assert state.current_stage == AgentLoopStage.BLOCKED
        assert state.blocked_reason == "permission_denied"

    def test_permission_denied_takes_priority_over_pending_tasks(self):
        job = _make_job()
        job.tasks.append(_pending_task())
        events = [_perm_denied_event(str(job.id))]
        state = derive_agent_loop_state(job, events)
        assert state.decision == AgentLoopDecision.BLOCKED

    def test_permission_denied_in_metadata_also_blocked(self):
        job = _make_job()
        ev = {
            "event": "task_run_failed",
            "job_id": str(job.id),
            "run_id": "r1",
            "timestamp": "2026-05-06T10:00:00+00:00",
            "metadata": {"outcome": "permission_denied"},
        }
        state = derive_agent_loop_state(job, [ev])
        assert state.decision == AgentLoopDecision.BLOCKED

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
        assert "run-next-task-local" in out

    def test_next_action_planned_suggests_plan(self):
        job = _make_job()
        state = derive_agent_loop_state(job, [])
        out = summarize_agent_loop_state(job, state)
        assert "plan-job-local" in out

    def test_next_action_blocked_suggests_set_permission(self):
        job = _make_job()
        events = [_perm_denied_event(str(job.id))]
        state = derive_agent_loop_state(job, events)
        out = summarize_agent_loop_state(job, state)
        assert "set-permission" in out

    def test_next_action_needs_approval_suggests_list_intents(self):
        job = _make_job()
        job.tasks.append(_completed_task())
        _add_patch_artifact(job, risk=RISK_MEDIUM)
        state = derive_agent_loop_state(job, [])
        out = summarize_agent_loop_state(job, state)
        assert "list-patch-intents" in out

    def test_next_action_complete_suggests_trust_report(self):
        job = _make_job()
        job.tasks.append(_completed_task())
        state = derive_agent_loop_state(job, [])
        out = summarize_agent_loop_state(job, state)
        assert "trust-report" in out

    def test_blockers_shown_when_blocked(self):
        job = _make_job()
        events = [_perm_denied_event(str(job.id))]
        state = derive_agent_loop_state(job, events)
        out = summarize_agent_loop_state(job, state)
        assert "permission_denied" in out

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
# CLI tests
# ---------------------------------------------------------------------------


class TestCLIAgentLoop:
    def test_invalid_uuid_exits_1(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from apps.cli.main import _cmd_agent_loop
        with pytest.raises(SystemExit) as exc:
            _cmd_agent_loop("not-a-uuid")
        assert exc.value.code == 1

    def test_unknown_job_exits_1(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from apps.cli.main import _cmd_agent_loop
        with pytest.raises(SystemExit) as exc:
            _cmd_agent_loop(str(uuid4()))
        assert exc.value.code == 1

    def test_valid_job_prints_report(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        from apps.cli.main import _cmd_agent_loop
        _cmd_agent_loop(str(job.id))
        out = capsys.readouterr().out
        assert "Remedy Agent Loop" in out
        assert str(job.id)[:8] in out

    def test_cli_logs_agent_loop_inspected_event(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        from apps.cli.main import _cmd_agent_loop
        _cmd_agent_loop(str(job.id))
        capsys.readouterr()
        runs_dir = tmp_path / "runs" / str(job.id)
        events = []
        for f in runs_dir.glob("*.jsonl"):
            for line in f.read_text().splitlines():
                if line.strip():
                    events.append(json.loads(line))
        ev = next((e for e in events if e.get("event") == "agent_loop_inspected"), None)
        assert ev is not None

    def test_run_log_metadata_has_required_fields(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        from apps.cli.main import _cmd_agent_loop
        _cmd_agent_loop(str(job.id))
        capsys.readouterr()
        runs_dir = tmp_path / "runs" / str(job.id)
        events = []
        for f in runs_dir.glob("*.jsonl"):
            for line in f.read_text().splitlines():
                if line.strip():
                    events.append(json.loads(line))
        ev = next(e for e in events if e.get("event") == "agent_loop_inspected")
        meta = ev.get("metadata", {})
        assert "stage" in meta
        assert "decision" in meta
        assert "cycle" in meta
        assert "max_cycles" in meta
        assert "pending_finding_count" in meta

    def test_run_log_event_no_raw_artifact_content(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        job.artifacts.append(Artifact(
            name="proposal",
            content="ARTIFACT RAW CONTENT MUST NOT BE LOGGED",
            kind=ArtifactKind.BUILDER_PROPOSAL,
        ))
        save_job(job)
        from apps.cli.main import _cmd_agent_loop
        _cmd_agent_loop(str(job.id))
        capsys.readouterr()
        runs_dir = tmp_path / "runs" / str(job.id)
        combined = "".join(f.read_text() for f in runs_dir.glob("*.jsonl"))
        assert "ARTIFACT RAW CONTENT MUST NOT BE LOGGED" not in combined

    def test_exactly_one_run_log_file_created(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        from apps.cli.main import _cmd_agent_loop
        _cmd_agent_loop(str(job.id))
        capsys.readouterr()
        runs_dir = tmp_path / "runs" / str(job.id)
        assert len(list(runs_dir.glob("*.jsonl"))) == 1

    def test_cli_output_no_raw_approval_reason(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        job.tasks.append(_completed_task())
        intent_id = _add_patch_artifact(job, risk=RISK_MEDIUM)
        set_approval_state(job, intent_id, APPROVAL_APPROVED, reason="top secret reason")
        save_job(job)
        from apps.cli.main import _cmd_agent_loop
        _cmd_agent_loop(str(job.id))
        out = capsys.readouterr().out
        assert "top secret reason" not in out
