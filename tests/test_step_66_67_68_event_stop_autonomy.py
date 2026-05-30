"""Tests for Steps 66-68 — Event Ledger, Stop Reasons, Autonomy Loop."""

from __future__ import annotations

import json
import subprocess
import sys
from uuid import uuid4

import pytest

from packages.core.models import Job, RunState, Task


# ── Step 66: Event Ledger ────────────────────────────────────────────────


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


class TestEventCLIHelp:
    def test_event_list_help(self):
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", "event", "list", "--help"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0
        assert "job_id" in result.stdout.lower()

    def test_event_timeline_help(self):
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", "event", "timeline", "--help"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0


# ── Step 67: Stop Reasons ────────────────────────────────────────────────


class TestStopReasonsCRUD:
    def test_create_and_list(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.stop_reasons import (
            create_stop_reason,
            list_stop_reasons,
        )

        job_id = uuid4().hex[:16]
        sr = create_stop_reason(
            job_id,
            source="test",
            reason_code="test_failed",
            safe_summary="Test failed in CI.",
            next_actions=("re-run tests",),
        )
        assert sr.status == "active"
        assert sr.reason_code == "test_failed"

        all_stops = list_stop_reasons(job_id)
        assert len(all_stops) == 1
        assert all_stops[0].id == sr.id

    def test_get_stop_reason(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.stop_reasons import (
            create_stop_reason,
            get_stop_reason,
        )

        job_id = uuid4().hex[:16]
        sr = create_stop_reason(
            job_id, source="test", reason_code="no_target_repo",
            safe_summary="No repo.", next_actions=(),
        )
        found = get_stop_reason(job_id, sr.id)
        assert found is not None
        assert found.reason_code == "no_target_repo"

        missing = get_stop_reason(job_id, "nonexistent")
        assert missing is None

    def test_resolve(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.stop_reasons import (
            create_stop_reason,
            get_stop_reason,
            resolve_stop_reason,
        )

        job_id = uuid4().hex[:16]
        sr = create_stop_reason(
            job_id, source="test", reason_code="not_approved",
            safe_summary="Waiting.", next_actions=(),
        )
        resolved = resolve_stop_reason(job_id, sr.id, "approved now")
        assert resolved is not None
        assert resolved.status == "resolved"
        assert resolved.resolved_at is not None

        # Verify persistence
        loaded = get_stop_reason(job_id, sr.id)
        assert loaded.status == "resolved"


class TestStopReasonsDerive:
    def test_derive_no_repo(self):
        from packages.orchestration.stop_reasons import derive_stop_reasons

        job = Job(id=uuid4(), name="d1", user_prompt="test", metadata={})
        reasons = derive_stop_reasons(job, [])
        codes = [r.reason_code for r in reasons]
        assert "no_target_repo" in codes

    def test_derive_test_failed(self):
        from packages.orchestration.stop_reasons import derive_stop_reasons

        job = Job(
            id=uuid4(), name="d2", user_prompt="test",
            metadata={"target_repo": "/tmp/repo"},
        )
        events = [
            {"event": "test_run_completed", "metadata": {"status": "failed"}},
        ]
        reasons = derive_stop_reasons(job, events)
        codes = [r.reason_code for r in reasons]
        assert "test_failed" in codes

    def test_derive_dirty_repo(self):
        from packages.orchestration.stop_reasons import derive_stop_reasons

        job = Job(
            id=uuid4(), name="d3", user_prompt="test",
            metadata={"target_repo": "/tmp/repo"},
        )
        events = [
            {"event": "git_status_read", "metadata": {"dirty": True}},
        ]
        reasons = derive_stop_reasons(job, events)
        codes = [r.reason_code for r in reasons]
        assert "dirty_repo_blocks_level" in codes


class TestStopReasonExport:
    def test_export_json(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.stop_reasons import (
            create_stop_reason,
            export_stop_reason_json,
        )

        job_id = uuid4().hex[:16]
        sr = create_stop_reason(
            job_id, source="test", reason_code="test_failed",
            safe_summary="Failed.", next_actions=("fix",),
        )
        data = export_stop_reason_json(sr)
        assert data["reason_code"] == "test_failed"
        assert data["status"] == "active"
        assert isinstance(data["next_actions"], list)


class TestStopReasonBrainNode:
    def test_stop_reason_node_in_graph(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import build_project_brain
        from packages.orchestration.storage import save_job

        job = Job(
            id=uuid4(), name="brain-sr", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
            metadata={},  # No target_repo → derives no_target_repo
        )
        save_job(job)
        graph = build_project_brain(job, [])
        sr_nodes = [n for n in graph.nodes if n.type == "stop_reason"]
        assert len(sr_nodes) >= 1
        codes = [n.metadata.get("reason_code") for n in sr_nodes]
        assert "no_target_repo" in codes


class TestBlockerCLIHelp:
    def test_blocker_list_help(self):
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", "blocker", "list", "--help"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0
        assert "job_id" in result.stdout.lower()


# ── Step 68: Autonomy Loop ──────────────────────────────────────────────


class TestAutonomyLoopBasic:
    def test_level_0_observe(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autonomy_loop import run_autonomy_loop
        from packages.orchestration.storage import save_job

        job = Job(
            id=uuid4(), name="loop0", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
            metadata={"target_repo": "."},
        )
        save_job(job)
        result = run_autonomy_loop(job, [], max_cycles=1, autonomy_level=0)
        assert result.version == 1
        assert result.final_decision == "complete"
        assert result.autonomy_level == 0
        assert len(result.cycles) == 1
        assert result.cycles[0].decision == "complete"

    def test_level_1_needs_approval(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autonomy_loop import run_autonomy_loop
        from packages.orchestration.storage import save_job

        job = Job(
            id=uuid4(), name="loop1", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
            metadata={"target_repo": "."},
        )
        save_job(job)
        result = run_autonomy_loop(job, [], max_cycles=3, autonomy_level=1)
        assert result.final_decision == "needs_approval"

    def test_completed_job(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autonomy_loop import run_autonomy_loop
        from packages.orchestration.storage import save_job

        job = Job(
            id=uuid4(), name="loop-done", user_prompt="test",
            tasks=[Task(description="t", status=RunState.COMPLETED)],
            state=RunState.COMPLETED,
            metadata={"target_repo": "."},
        )
        save_job(job)
        result = run_autonomy_loop(job, [], max_cycles=3, autonomy_level=1)
        assert result.final_decision == "complete"

    def test_blocked_by_stop_reason(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autonomy_loop import run_autonomy_loop
        from packages.orchestration.storage import save_job

        job = Job(
            id=uuid4(), name="loop-blocked", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
            metadata={},  # No target_repo → blocker
        )
        save_job(job)
        result = run_autonomy_loop(job, [], max_cycles=3, autonomy_level=1)
        assert result.final_decision == "blocked"
        assert len(result.stop_reasons) >= 1


class TestAutonomyLoopExport:
    def test_export_json(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autonomy_loop import (
            export_loop_result_json,
            run_autonomy_loop,
        )
        from packages.orchestration.storage import save_job

        job = Job(
            id=uuid4(), name="loop-ex", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
            metadata={"target_repo": "."},
        )
        save_job(job)
        result = run_autonomy_loop(job, [], max_cycles=1, autonomy_level=0)
        data = export_loop_result_json(result)
        assert data["version"] == 1
        assert isinstance(data["cycles"], list)
        assert data["final_decision"] == "complete"

    def test_summarize(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autonomy_loop import (
            run_autonomy_loop,
            summarize_loop_result,
        )
        from packages.orchestration.storage import save_job

        job = Job(
            id=uuid4(), name="loop-sum", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
            metadata={"target_repo": "."},
        )
        save_job(job)
        result = run_autonomy_loop(job, [], max_cycles=1, autonomy_level=0)
        text = summarize_loop_result(result)
        assert "Autonomy Loop" in text
        assert "Level: 0" in text


class TestRunLoopCLIHelp:
    def test_run_loop_help(self):
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", "job", "run-loop", "--help"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0
        assert "autonomy" in result.stdout.lower()
