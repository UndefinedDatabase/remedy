"""Memory safety and regression tests — prove memory cannot leak or corrupt."""
from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _setup(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))


class TestApprovedMemoryIncluded:
    def test_approved_project_memory_in_summary(self, tmp_path, monkeypatch):
        _setup(tmp_path, monkeypatch)
        from packages.memory.local_gateway import store_memory
        from packages.memory.context_summary import build_memory_context

        store_memory(key="build-pattern", value="Use make test", project_id="proj1", approved=True)
        ctx = build_memory_context(project_id="proj1")
        assert ctx.item_count == 1
        assert ctx.items[0].approved is True


class TestUnrelatedProjectExcluded:
    def test_different_project_memory_excluded(self, tmp_path, monkeypatch):
        _setup(tmp_path, monkeypatch)
        from packages.memory.local_gateway import store_memory
        from packages.memory.context_summary import build_memory_context

        store_memory(key="other-proj", value="Irrelevant", project_id="proj-other", approved=True)
        ctx = build_memory_context(project_id="proj1")
        assert ctx.item_count == 0


class TestUnapprovedExcluded:
    def test_unapproved_memory_absent(self, tmp_path, monkeypatch):
        _setup(tmp_path, monkeypatch)
        from packages.memory.local_gateway import store_memory
        from packages.memory.context_summary import build_memory_context

        store_memory(key="draft", value="Draft idea", project_id="proj1", approved=False)
        ctx = build_memory_context(project_id="proj1")
        assert ctx.item_count == 0


class TestRejectedStaleExcluded:
    def test_rejected_memory_excluded(self, tmp_path, monkeypatch):
        _setup(tmp_path, monkeypatch)
        from packages.memory.local_gateway import store_memory, reject_memory_card

        entry = store_memory(key="bad-idea", value="Wrong", project_id="proj1", approved=True)
        reject_memory_card(str(entry.id), project_id="proj1")
        from packages.memory.context_summary import build_memory_context
        ctx = build_memory_context(project_id="proj1")
        # Rejected cards have approved=False
        assert ctx.item_count == 0

    def test_stale_memory_excluded(self, tmp_path, monkeypatch):
        _setup(tmp_path, monkeypatch)
        from packages.memory.local_gateway import store_memory, mark_stale

        entry = store_memory(key="old-fact", value="Outdated", project_id="proj1", approved=True)
        mark_stale(str(entry.id), project_id="proj1")
        from packages.memory.context_summary import build_memory_context
        ctx = build_memory_context(project_id="proj1")
        # Stale has validity != "active"
        assert ctx.item_count == 0


class TestSecretLikeContentRedacted:
    def test_secret_pattern_rejected_at_store(self, tmp_path, monkeypatch):
        _setup(tmp_path, monkeypatch)
        from packages.memory.local_gateway import store_memory, MemoryRedactionError

        with pytest.raises(MemoryRedactionError):
            store_memory(key="api-config", value="token=sk-abc123", project_id="proj1", approved=True)

    def test_forbidden_key_rejected(self, tmp_path, monkeypatch):
        _setup(tmp_path, monkeypatch)
        from packages.memory.local_gateway import store_memory, MemoryRedactionError

        with pytest.raises(MemoryRedactionError):
            store_memory(key="artifact.content", value="raw stuff", project_id="proj1", approved=True)


class TestLargeMemoryBounded:
    def test_large_set_truncated(self, tmp_path, monkeypatch):
        _setup(tmp_path, monkeypatch)
        from packages.memory.local_gateway import store_memory
        from packages.memory.context_summary import build_memory_context

        for i in range(100):
            store_memory(
                key=f"fact-{i:03d}-{'x' * 80}", value="details",
                project_id="proj1", approved=True,
            )
        ctx = build_memory_context(project_id="proj1", budget=200)
        assert ctx.truncated is True
        assert ctx.estimated_tokens <= 200


class TestDeterministicOrdering:
    def test_ordering_stable(self, tmp_path, monkeypatch):
        _setup(tmp_path, monkeypatch)
        from packages.memory.local_gateway import store_memory
        from packages.memory.context_summary import build_memory_context

        store_memory(key="alpha", value="First", project_id="proj1", approved=True)
        store_memory(key="beta", value="Second", project_id="proj1", approved=True)

        ctx1 = build_memory_context(project_id="proj1")
        ctx2 = build_memory_context(project_id="proj1")
        ids1 = [i.id for i in ctx1.items]
        ids2 = [i.id for i in ctx2.items]
        assert ids1 == ids2


class TestContextHashIntegrity:
    def test_hash_changes_when_memory_changes(self, tmp_path, monkeypatch):
        _setup(tmp_path, monkeypatch)
        from packages.memory.local_gateway import store_memory
        from packages.memory.context_summary import build_memory_context

        store_memory(key="initial", value="v1", project_id="proj1", approved=True)
        h1 = build_memory_context(project_id="proj1").context_hash

        store_memory(key="new-item", value="v2", project_id="proj1", approved=True)
        h2 = build_memory_context(project_id="proj1").context_hash
        assert h1 != h2


class TestNoRawMemoryLeaks:
    """Verify no raw memory text leaks into system surfaces."""

    def test_no_raw_in_run_log_event(self, tmp_path, monkeypatch):
        _setup(tmp_path, monkeypatch)
        from packages.memory.local_gateway import store_memory
        from packages.memory.context_summary import (
            build_memory_context,
            emit_memory_recalled_event,
        )

        store_memory(key="secret-pattern", value="Do not leak this", project_id="proj1", approved=True)
        ctx = build_memory_context(project_id="proj1")

        job_id = str(uuid4())
        emit_memory_recalled_event(ctx, data_dir=str(tmp_path), job_id=job_id, stage="test")

        from packages.orchestration.timeline import load_run_events
        from uuid import UUID
        events = load_run_events(tmp_path, UUID(job_id))
        all_text = json.dumps(events)
        assert "Do not leak this" not in all_text

    def test_no_raw_in_export_json(self, tmp_path, monkeypatch):
        _setup(tmp_path, monkeypatch)
        from packages.memory.local_gateway import store_memory
        from packages.memory.context_summary import build_memory_context, export_memory_context_json

        store_memory(key="info", value="Private details about auth system", project_id="proj1", approved=True)
        ctx = build_memory_context(project_id="proj1")
        exported = json.dumps(export_memory_context_json(ctx))
        assert "Private details about auth system" not in exported

    def test_no_raw_in_format_section(self, tmp_path, monkeypatch):
        _setup(tmp_path, monkeypatch)
        from packages.memory.local_gateway import store_memory
        from packages.memory.context_summary import build_memory_context, format_memory_section

        store_memory(key="config-note", value="Internal implementation secrets", project_id="proj1", approved=True)
        ctx = build_memory_context(project_id="proj1")
        section = format_memory_section(ctx)
        assert "Internal implementation secrets" not in section


class TestNoFakeMemoryInEmptyRuntime:
    def test_empty_runtime_no_memory_nodes(self, tmp_path, monkeypatch):
        _setup(tmp_path, monkeypatch)
        from packages.memory.context_summary import build_memory_context, format_memory_section

        ctx = build_memory_context(project_id="empty-proj")
        assert ctx.item_count == 0
        assert format_memory_section(ctx) == ""
