"""
Domain tests: orchestration/test_event_ledger.py
Migrated from step-numbered test files.
"""

from __future__ import annotations

from uuid import uuid4
import json
import pytest
import subprocess
import sys

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




class TestEventLedgerNormalize:
    def test_list_events_basic(self):
        from packages.orchestration.event_ledger import list_events

        events = [
            {"event": "job_created", "run_id": "r1", "job_id": "j1",
             "timestamp": "2026-01-01T00:00:00", "outcome": "ok", "metadata": {}},
            {"event": "test_run_completed", "run_id": "r1", "job_id": "j1",
             "timestamp": "2026-01-01T00:01:00", "outcome": "failed",
             "metadata": {"status": "failed"}},
        ]
        result = list_events("j1", events)
        assert len(result) == 2
        assert result[0].event_type == "job_created"
        assert result[1].event_type == "test_run_completed"

    def test_list_events_filter_type(self):
        from packages.orchestration.event_ledger import list_events

        events = [
            {"event": "job_created", "run_id": "r1", "job_id": "j1",
             "timestamp": "2026-01-01T00:00:00", "outcome": "ok", "metadata": {}},
            {"event": "test_run_completed", "run_id": "r1", "job_id": "j1",
             "timestamp": "2026-01-01T00:01:00", "outcome": "ok", "metadata": {}},
        ]
        result = list_events("j1", events, event_type="test_run_completed")
        assert len(result) == 1
        assert result[0].event_type == "test_run_completed"

    def test_event_id_deterministic(self):
        from packages.orchestration.event_ledger import _make_event_id

        id1 = _make_event_id("run1", 0)
        id2 = _make_event_id("run1", 0)
        id3 = _make_event_id("run1", 1)
        assert id1 == id2
        assert id1 != id3
        assert len(id1) == 16

    def test_redact_metadata(self):
        from packages.orchestration.event_ledger import _redact_metadata

        meta = {"status": "ok", "stdout": "SECRET", "diff_preview": "HIDDEN", "safe_key": 42}
        safe = _redact_metadata(meta)
        assert "stdout" not in safe
        assert "diff_preview" not in safe
        assert safe["status"] == "ok"
        assert safe["safe_key"] == 42




class TestEventLedgerScope:
    def test_scope_derivation(self):
        from packages.orchestration.event_ledger import _normalize_event

        cases = [
            ("patch_applied", "patch"),
            ("test_run_completed", "test"),
            ("agent_loop_cycle_decision", "agent"),
            ("memory_stored", "memory"),
            ("token_budget_check", "policy"),
            ("git_status_read", "repo"),
            ("job_created", "system"),
        ]
        for event_type, expected_scope in cases:
            e = _normalize_event({"event": event_type, "run_id": "r1", "metadata": {}}, 0)
            assert e.scope == expected_scope, f"{event_type} → {e.scope}, expected {expected_scope}"




class TestEventLedgerTimeline:
    def test_build_timeline(self):
        from packages.orchestration.event_ledger import build_event_timeline

        events = [
            {"event": "job_created", "run_id": "r1", "job_id": "j1",
             "timestamp": "2026-01-01T00:00:00", "outcome": "ok", "metadata": {}},
        ]
        timeline = build_event_timeline("j1", events)
        assert timeline.version == 1
        assert timeline.event_count == 1
        assert len(timeline.events) == 1




class TestEventLedgerSummary:
    def test_build_summary(self):
        from packages.orchestration.event_ledger import build_event_summary

        events = [
            {"event": "job_created", "run_id": "r1", "timestamp": "2026-01-01T00:00:00",
             "outcome": "ok", "metadata": {}},
            {"event": "test_run_completed", "run_id": "r1", "timestamp": "2026-01-01T00:01:00",
             "outcome": "failed", "metadata": {}},
            {"event": "patch_apply_proof", "run_id": "r1", "timestamp": "2026-01-01T00:02:00",
             "outcome": "ok", "metadata": {}},
        ]
        summary = build_event_summary(events)
        assert summary.event_count == 3
        assert summary.failed_count == 1
        assert summary.proof_count == 1
        assert summary.test_count == 1
        assert summary.last_event_at == "2026-01-01T00:02:00"




class TestEventLedgerExport:
    def test_export_json(self):
        from packages.orchestration.event_ledger import (
            export_ledger_event_json,
            list_events,
        )

        events = [
            {"event": "job_created", "run_id": "r1", "job_id": "j1",
             "timestamp": "2026-01-01T00:00:00", "outcome": "ok", "metadata": {"safe": 1}},
        ]
        ledger = list_events("j1", events)
        data = export_ledger_event_json(ledger[0])
        assert data["event_type"] == "job_created"
        assert data["event_id"]
        assert data["scope"] == "system"
        assert "safe" in data["metadata"]




class TestEventLedgerBrainNode:
    def test_event_ledger_node_in_graph(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import build_project_brain
        from packages.orchestration.storage import save_job

        job = Job(
            id=uuid4(), name="brain-el", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
        )
        save_job(job)
        events = [
            {"event": "job_created", "run_id": "r1", "job_id": str(job.id),
             "timestamp": "2026-01-01T00:00:00", "outcome": "ok", "metadata": {}},
            {"event": "test_run_completed", "run_id": "r1", "job_id": str(job.id),
             "timestamp": "2026-01-01T00:01:00", "outcome": "failed", "metadata": {}},
        ]
        graph = build_project_brain(job, events)
        el_nodes = [n for n in graph.nodes if n.type == "event_ledger"]
        assert len(el_nodes) == 1
        meta = el_nodes[0].metadata
        assert meta["event_count"] == 2
        assert meta["failed_count"] == 1

