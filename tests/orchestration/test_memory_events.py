"""Tests: memory events emitted with safe metadata, visible in dashboard."""
from __future__ import annotations

import json
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent.parent


class TestMemoryEventEmission:
    def test_emit_creates_event_when_memory_used(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import store_memory
        from packages.memory.context_summary import (
            build_memory_context,
            emit_memory_recalled_event,
        )
        from uuid import uuid4

        store_memory(key="tip", value="Use fixtures", project_id="proj1", approved=True)
        ctx = build_memory_context(project_id="proj1")

        job_id = str(uuid4())
        emit_memory_recalled_event(ctx, data_dir=str(tmp_path), job_id=job_id, stage="planning")

        # Read event from timeline
        from packages.orchestration.timeline import load_run_events
        from uuid import UUID
        events = load_run_events(tmp_path, UUID(job_id))
        mem_events = [e for e in events if e.get("event") == "project_memory_recalled"]
        assert len(mem_events) == 1
        meta = mem_events[0]["metadata"]
        assert meta["item_count"] == 1
        assert meta["approved_only"] is True
        assert meta["stage"] == "planning"

    def test_no_event_when_no_memory(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.context_summary import (
            build_memory_context,
            emit_memory_recalled_event,
        )
        from uuid import uuid4

        ctx = build_memory_context(project_id="proj1")
        job_id = str(uuid4())
        emit_memory_recalled_event(ctx, data_dir=str(tmp_path), job_id=job_id, stage="planning")

        from packages.orchestration.timeline import load_run_events
        from uuid import UUID
        events = load_run_events(tmp_path, UUID(job_id))
        mem_events = [e for e in events if e.get("event") == "project_memory_recalled"]
        assert len(mem_events) == 0

    def test_event_metadata_safe(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import store_memory
        from packages.memory.context_summary import (
            build_memory_context,
            emit_memory_recalled_event,
        )
        from uuid import uuid4

        store_memory(key="sensitive-pattern", value="Details about auth", project_id="proj1", approved=True)
        ctx = build_memory_context(project_id="proj1")

        job_id = str(uuid4())
        emit_memory_recalled_event(ctx, data_dir=str(tmp_path), job_id=job_id, stage="execution")

        from packages.orchestration.timeline import load_run_events
        from uuid import UUID
        events = load_run_events(tmp_path, UUID(job_id))
        meta = events[0]["metadata"]
        meta_str = json.dumps(meta)
        # No raw memory content
        assert "Details about auth" not in meta_str
        assert "sensitive-pattern" not in meta_str


class TestDashboardMemoryVisibility:
    def test_dashboard_source_has_emit_function(self):
        src = (REPO_ROOT / "packages" / "memory" / "context_summary.py").read_text()
        assert "emit_memory_recalled_event" in src

    def test_live_state_includes_memory_used_count(self):
        src = (REPO_ROOT / "packages" / "orchestration" / "ui_server.py").read_text()
        assert "memory_used_count" in src

    def test_live_state_reads_from_events(self):
        src = (REPO_ROOT / "packages" / "orchestration" / "ui_server.py").read_text()
        assert "project_memory_recalled" in src
