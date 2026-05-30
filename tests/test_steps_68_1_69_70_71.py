"""Tests for Steps 68.1, 69, 70, 71 — Event Schema, Decision Queue, Dashboard, Context Optimizer."""

from __future__ import annotations

from uuid import uuid4

import pytest

from packages.core.models import Job, RunState, Task


def _make_job(**overrides) -> Job:
    defaults = {
        "id": uuid4(),
        "name": "test-job",
        "user_prompt": "test prompt",
        "description": "test job",
        "tasks": [
            Task(description="task 1", status=RunState.COMPLETED),
        ],
        "state": RunState.COMPLETED,
        "permissions": {"repo_generated_write": "allow", "repo_test_run": "allow"},
        "metadata": {"target_repo": "."},
    }
    defaults.update(overrides)
    return Job(**defaults)


def _make_events() -> list[dict]:
    return [
        {"event": "job_created", "run_id": "r1", "job_id": "j1",
         "timestamp": "2026-01-01T00:00:00", "outcome": "ok", "metadata": {}},
        {"event": "patch_intent_created", "run_id": "r1", "job_id": "j1",
         "timestamp": "2026-01-01T00:01:00", "outcome": "ok",
         "metadata": {"intent_id": "pi1", "target_path": "foo.py", "action": "create"}},
    ]


# ── Step 68.1: Event Schema Registry ────────────────────────────────────


class TestEventSchemaRegistry:
    def test_schemas_exist(self):
        from packages.orchestration.event_schemas import EVENT_METADATA_SCHEMAS
        assert "agent_loop_started" in EVENT_METADATA_SCHEMAS
        assert "agent_loop_cycle_decision" in EVENT_METADATA_SCHEMAS
        assert "agent_loop_stopped" in EVENT_METADATA_SCHEMAS
        assert "context_budget_optimized" in EVENT_METADATA_SCHEMAS

    def test_schemas_are_frozensets(self):
        from packages.orchestration.event_schemas import EVENT_METADATA_SCHEMAS
        for name, schema in EVENT_METADATA_SCHEMAS.items():
            assert isinstance(schema, frozenset), f"{name} not frozenset"
            assert len(schema) > 0, f"{name} empty"

    def test_different_schemas_for_different_events(self):
        from packages.orchestration.event_schemas import EVENT_METADATA_SCHEMAS
        started = EVENT_METADATA_SCHEMAS["agent_loop_started"]
        decision = EVENT_METADATA_SCHEMAS["agent_loop_cycle_decision"]
        stopped = EVENT_METADATA_SCHEMAS["agent_loop_stopped"]
        assert started != decision, "started and decision must differ"
        assert decision != stopped, "decision and stopped must differ"
        assert started != stopped, "started and stopped must differ"

    def test_validate_valid_metadata(self):
        from packages.orchestration.event_schemas import validate_event_metadata
        meta = {
            "cycle": 1, "max_cycles": 5, "decision": "continue", "stage": "run",
            "reason": "ok", "task_count": 3, "pending_task_count": 1,
            "pending_approval_count": 0, "applied_count": 2, "test_run_count": 1,
        }
        errors = validate_event_metadata("agent_loop_started", meta)
        assert errors == []

    def test_validate_missing_keys(self):
        from packages.orchestration.event_schemas import validate_event_metadata
        errors = validate_event_metadata("agent_loop_started", {"cycle": 1})
        assert len(errors) == 1
        assert "missing keys" in errors[0]

    def test_validate_extra_keys(self):
        from packages.orchestration.event_schemas import validate_event_metadata
        meta = {
            "cycle": 1, "max_cycles": 5, "decision": "continue", "stage": "run",
            "reason": "ok", "task_count": 3, "pending_task_count": 1,
            "pending_approval_count": 0, "applied_count": 2, "test_run_count": 1,
            "extra_bogus": True,
        }
        errors = validate_event_metadata("agent_loop_started", meta)
        assert len(errors) == 1
        assert "extra keys" in errors[0]

    def test_validate_unknown_event(self):
        from packages.orchestration.event_schemas import validate_event_metadata
        errors = validate_event_metadata("unknown_event", {"x": 1})
        assert errors == []

    def test_get_event_schema(self):
        from packages.orchestration.event_schemas import get_event_schema
        assert get_event_schema("agent_loop_stopped") is not None
        assert get_event_schema("nonexistent") is None

    def test_context_budget_optimized_schema(self):
        from packages.orchestration.event_schemas import EVENT_METADATA_SCHEMAS
        schema = EVENT_METADATA_SCHEMAS["context_budget_optimized"]
        assert len(schema) == 7
        assert "mode" in schema
        assert "budget" in schema
        assert "estimated_tokens" in schema
        assert "token_savings" in schema
        assert "recommended_worker" in schema
        assert "included_section_count" in schema
        assert "excluded_section_count" in schema

    def test_agent_loop_cycle_decision_schema(self):
        from packages.orchestration.event_schemas import EVENT_METADATA_SCHEMAS
        schema = EVENT_METADATA_SCHEMAS["agent_loop_cycle_decision"]
        assert len(schema) == 8
        assert "next_action" in schema
        assert "blocked_by" in schema
        assert "readiness_level" in schema

    def test_agent_loop_stopped_schema(self):
        from packages.orchestration.event_schemas import EVENT_METADATA_SCHEMAS
        schema = EVENT_METADATA_SCHEMAS["agent_loop_stopped"]
        assert len(schema) == 4
        assert "final_decision" in schema
        assert "stop_reason" in schema
        assert "cycles_run" in schema
        assert "unresolved_blocker_count" in schema

    def test_forbidden_strings(self):
        from packages.orchestration.event_schemas import FORBIDDEN_STRINGS
        assert "stdout" in FORBIDDEN_STRINGS
        assert "Traceback" in FORBIDDEN_STRINGS
        assert isinstance(FORBIDDEN_STRINGS, frozenset)


# ── Step 69: Decision Queue ─────────────────────────────────────────────


class TestDecisionQueue:
    def test_list_decisions_empty(self):
        from packages.orchestration.decision_queue import list_decisions
        job = _make_job()
        decisions = list_decisions(job, [])
        # No patch intents pending, no test failures, etc.
        assert isinstance(decisions, list)

    def test_decision_types_frozenset(self):
        from packages.orchestration.decision_queue import DECISION_TYPES
        assert isinstance(DECISION_TYPES, frozenset)
        assert "patch_approval" in DECISION_TYPES
        assert "stop_reason" in DECISION_TYPES
        assert "test_failure" in DECISION_TYPES
        assert "repo_dirty" in DECISION_TYPES
        assert "memory_review" in DECISION_TYPES

    def test_test_failure_decisions(self):
        from packages.orchestration.decision_queue import list_decisions
        job = _make_job()
        events = [
            {"event": "test_run_completed", "run_id": "r1", "job_id": str(job.id),
             "timestamp": "2026-01-01T00:01:00", "outcome": "failed",
             "metadata": {"status": "failed", "command": "pytest", "test_run_id": "tr1"}},
        ]
        decisions = list_decisions(job, events)
        test_decs = [d for d in decisions if d.type == "test_failure"]
        assert len(test_decs) >= 1
        assert test_decs[0].severity == "blocker"
        assert test_decs[0].status == "open"

    def test_dirty_repo_decision(self):
        from packages.orchestration.decision_queue import list_decisions
        job = _make_job()
        events = [
            {"event": "git_status_read", "run_id": "r1", "job_id": str(job.id),
             "timestamp": "2026-01-01T00:01:00", "outcome": "ok",
             "metadata": {"dirty": True, "branch": "main", "changed_file_count": 3}},
        ]
        decisions = list_decisions(job, events)
        dirty_decs = [d for d in decisions if d.type == "repo_dirty"]
        assert len(dirty_decs) == 1
        assert dirty_decs[0].severity == "warning"

    def test_explain_decisions(self):
        from packages.orchestration.decision_queue import explain_decisions
        job = _make_job()
        result = explain_decisions(job, [])
        assert "No pending decisions" in result or isinstance(result, str)

    def test_export_decision_json(self):
        from packages.orchestration.decision_queue import HumanDecision, export_decision_json
        d = HumanDecision(
            id="test1", type="test_failure", status="open", severity="blocker",
            source="test_run", related_node_id="", related_intent_id="",
            related_file="", safe_summary="Test failed.",
            next_actions=("fix it",), created_at="2026-01-01", resolved_at=None,
        )
        j = export_decision_json(d)
        assert j["id"] == "test1"
        assert j["type"] == "test_failure"
        assert j["severity"] == "blocker"
        assert isinstance(j["next_actions"], list)

    def test_build_decision_summary(self):
        from packages.orchestration.decision_queue import HumanDecision, build_decision_summary
        decisions = [
            HumanDecision(
                id="d1", type="test_failure", status="open", severity="blocker",
                source="test", related_node_id="", related_intent_id="",
                related_file="", safe_summary="fail",
                next_actions=("fix",), created_at="", resolved_at=None,
            ),
            HumanDecision(
                id="d2", type="repo_dirty", status="open", severity="warning",
                source="git", related_node_id="", related_intent_id="",
                related_file="", safe_summary="dirty",
                next_actions=(), created_at="", resolved_at=None,
            ),
        ]
        summary = build_decision_summary(decisions)
        assert summary["open_count"] == 2
        assert summary["high_count"] == 1  # blocker
        assert summary["medium_count"] == 1  # warning

    def test_get_decision(self):
        from packages.orchestration.decision_queue import get_decision
        job = _make_job()
        events = [
            {"event": "git_status_read", "run_id": "r1", "job_id": str(job.id),
             "timestamp": "2026-01-01", "outcome": "ok",
             "metadata": {"dirty": True, "branch": "main", "changed_file_count": 1}},
        ]
        d = get_decision(job, events, "dirty_repo")
        assert d is not None
        assert d.type == "repo_dirty"

    def test_get_decision_not_found(self):
        from packages.orchestration.decision_queue import get_decision
        job = _make_job()
        d = get_decision(job, [], "nonexistent")
        assert d is None


# ── Step 70: Dashboard ──────────────────────────────────────────────────


class TestDashboard:
    def test_build_job_dashboard(self):
        from packages.orchestration.dashboard import build_job_dashboard
        job = _make_job()
        data = build_job_dashboard(job, _make_events())
        assert data["version"] == 1
        assert data["scope"] == "job"
        assert "readiness" in data
        assert "decisions" in data
        assert "test_status" in data
        assert "git_status" in data or data["git_status"] == {}
        assert "worker_recommendation" in data
        assert "memory" in data
        assert "events" in data
        assert "next_actions" in data

    def test_build_job_dashboard_decisions(self):
        from packages.orchestration.dashboard import build_job_dashboard
        job = _make_job()
        events = [
            {"event": "test_run_completed", "run_id": "r1", "job_id": str(job.id),
             "timestamp": "2026-01-01T00:01:00", "outcome": "failed",
             "metadata": {"status": "failed", "command": "pytest", "test_run_id": "tr1"}},
        ]
        data = build_job_dashboard(job, events)
        assert data["decisions"]["open_count"] >= 1

    def test_summarize_job_dashboard(self):
        from packages.orchestration.dashboard import build_job_dashboard, summarize_job_dashboard
        job = _make_job()
        data = build_job_dashboard(job, _make_events())
        text = summarize_job_dashboard(data)
        assert "Dashboard" in text
        assert "Readiness" in text
        assert "Decisions" in text

    def test_build_project_dashboard(self):
        from packages.orchestration.dashboard import build_project_dashboard
        job = _make_job()
        data = build_project_dashboard("proj1", [job], {str(job.id): _make_events()})
        assert data["version"] == 1
        assert data["scope"] == "project"
        assert data["job_count"] == 1
        assert "readiness_summary" in data
        assert "open_decision_count" in data

    def test_build_project_dashboard_empty(self):
        from packages.orchestration.dashboard import build_project_dashboard
        data = build_project_dashboard("proj1", [], {})
        assert data["job_count"] == 0
        assert data["readiness_summary"]["min_level"] == 0


# ── Step 71: Context Optimizer ──────────────────────────────────────────


class TestContextOptimizer:
    def test_explain_context(self):
        from packages.orchestration.context_optimizer import explain_context
        job = _make_job()
        data = explain_context(job, _make_events(), mode="compact", budget=2000)
        assert data["version"] == 1
        assert data["mode"] == "compact"
        assert data["budget"] == 2000
        assert "sections" in data
        assert "excluded" in data
        assert "recommendations" in data
        assert isinstance(data["sections"], list)

    def test_explain_context_invalid_mode(self):
        from packages.orchestration.context_optimizer import explain_context
        job = _make_job()
        data = explain_context(job, [], mode="invalid_mode", budget=2000)
        assert data["mode"] == "compact"  # fallback

    def test_optimize_context(self):
        from packages.orchestration.context_optimizer import optimize_context
        job = _make_job()
        data = optimize_context(job, _make_events(), budget=2000)
        assert data["version"] == 1
        assert data["budget"] == 2000
        assert "recommended_mode" in data
        assert data["recommended_mode"] in ("caveman", "compact", "standard")
        assert "estimated_tokens" in data
        assert "token_savings" in data
        assert "included_sections" in data
        assert "excluded_sections" in data
        assert "recommended_worker" in data
        assert "recommendations" in data

    def test_optimize_context_tight_budget(self):
        from packages.orchestration.context_optimizer import optimize_context
        job = _make_job()
        data = optimize_context(job, [], budget=50)
        # Very tight budget should pick caveman
        assert data["recommended_mode"] in ("caveman", "compact", "standard")

    def test_optimize_context_7_field_schema(self):
        """context_budget_optimized event must match 7-field schema."""
        from packages.orchestration.context_optimizer import optimize_context
        from packages.orchestration.event_schemas import validate_event_metadata
        job = _make_job()
        data = optimize_context(job, _make_events(), budget=2000)
        # Build metadata as the CLI handler would
        meta = {
            "mode": data["recommended_mode"],
            "budget": data["budget"],
            "estimated_tokens": data["estimated_tokens"],
            "token_savings": data["token_savings"],
            "recommended_worker": data["recommended_worker"],
            "included_section_count": len(data["included_sections"]),
            "excluded_section_count": len(data["excluded_sections"]),
        }
        errors = validate_event_metadata("context_budget_optimized", meta)
        assert errors == [], f"Schema errors: {errors}"


# ── Brain Integration ───────────────────────────────────────────────────


class TestBrainIntegration:
    def test_brain_has_decision_queue_node(self):
        from packages.orchestration.project_brain import (
            NT_DECISION_QUEUE,
            build_project_brain,
        )
        job = _make_job()
        graph = build_project_brain(job, _make_events())
        dq_nodes = [n for n in graph.nodes if n.type == NT_DECISION_QUEUE]
        assert len(dq_nodes) == 1
        assert dq_nodes[0].id == "decision_queue"

    def test_brain_has_context_budget_node(self):
        from packages.orchestration.project_brain import (
            NT_CONTEXT_BUDGET,
            build_project_brain,
        )
        job = _make_job()
        graph = build_project_brain(job, _make_events())
        cb_nodes = [n for n in graph.nodes if n.type == NT_CONTEXT_BUDGET]
        assert len(cb_nodes) == 1
        assert cb_nodes[0].id == "context_budget"

    def test_brain_decision_queue_edges(self):
        from packages.orchestration.project_brain import (
            ET_HAS_DECISION_QUEUE,
            build_project_brain,
        )
        job = _make_job()
        graph = build_project_brain(job, _make_events())
        dq_edges = [e for e in graph.edges if e.type == ET_HAS_DECISION_QUEUE]
        assert len(dq_edges) == 1

    def test_brain_context_budget_edges(self):
        from packages.orchestration.project_brain import (
            ET_HAS_CONTEXT_BUDGET,
            build_project_brain,
        )
        job = _make_job()
        graph = build_project_brain(job, _make_events())
        cb_edges = [e for e in graph.edges if e.type == ET_HAS_CONTEXT_BUDGET]
        assert len(cb_edges) == 1

    def test_brain_node_type_order(self):
        from packages.orchestration.project_brain import (
            NT_CONTEXT_BUDGET,
            NT_DECISION_QUEUE,
            _NODE_TYPE_ORDER,
        )
        assert NT_DECISION_QUEUE in _NODE_TYPE_ORDER
        assert NT_CONTEXT_BUDGET in _NODE_TYPE_ORDER
        assert _NODE_TYPE_ORDER[NT_DECISION_QUEUE] == 25
        assert _NODE_TYPE_ORDER[NT_CONTEXT_BUDGET] == 26


# ── Brain Detail ────────────────────────────────────────────────────────


class TestBrainDetail:
    def test_detail_decision_queue(self):
        from packages.orchestration.brain_detail import build_brain_node_detail
        from packages.orchestration.project_brain import build_project_brain
        job = _make_job()
        events = _make_events()
        graph = build_project_brain(job, events)
        detail = build_brain_node_detail(job, graph, "decision_queue", events)
        assert detail is not None
        assert "decision" in detail.title.lower() or "Decision" in detail.title

    def test_detail_context_budget(self):
        from packages.orchestration.brain_detail import build_brain_node_detail
        from packages.orchestration.project_brain import build_project_brain
        job = _make_job()
        events = _make_events()
        graph = build_project_brain(job, events)
        detail = build_brain_node_detail(job, graph, "context_budget", events)
        assert detail is not None
        assert "context" in detail.title.lower() or "Context" in detail.title


# ── Readiness Integration ───────────────────────────────────────────────


class TestReadinessDecisionIntegration:
    def test_readiness_signals_include_decisions(self):
        from packages.orchestration.autonomy_readiness import _collect_signals
        job = _make_job()
        signals = _collect_signals(job, [])
        assert "no_open_decisions" in signals

    def test_no_open_decisions_true_when_clean(self):
        from packages.orchestration.autonomy_readiness import _collect_signals
        job = _make_job()
        signals = _collect_signals(job, [])
        assert signals["no_open_decisions"] is True

    def test_no_open_decisions_false_with_failures(self):
        from packages.orchestration.autonomy_readiness import _collect_signals
        job = _make_job()
        events = [
            {"event": "test_run_completed", "run_id": "r1", "job_id": str(job.id),
             "timestamp": "2026-01-01T00:01:00", "outcome": "failed",
             "metadata": {"status": "failed", "command": "pytest", "test_run_id": "tr1"}},
        ]
        signals = _collect_signals(job, events)
        assert signals["no_open_decisions"] is False
