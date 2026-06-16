"""Contract tests for memory context summary — bounded, redacted, approved-only."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _setup_memory(tmp_path, monkeypatch, entries=None):
    """Set up test memory with given entries."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    from packages.memory.local_gateway import store_memory

    if entries:
        for e in entries:
            store_memory(**e)


class TestEmptyMemory:
    def test_empty_returns_empty_summary(self, tmp_path, monkeypatch):
        _setup_memory(tmp_path, monkeypatch)
        from packages.memory.context_summary import build_memory_context

        ctx = build_memory_context(project_id="test-proj")
        assert ctx.item_count == 0
        assert ctx.items == ()
        assert ctx.estimated_tokens == 0
        assert not ctx.truncated

    def test_empty_format_returns_empty_string(self, tmp_path, monkeypatch):
        _setup_memory(tmp_path, monkeypatch)
        from packages.memory.context_summary import build_memory_context, format_memory_section

        ctx = build_memory_context(project_id="test-proj")
        assert format_memory_section(ctx) == ""


class TestApprovedMemoryAppears:
    def test_approved_active_included(self, tmp_path, monkeypatch):
        _setup_memory(tmp_path, monkeypatch, [
            {"key": "test-pattern", "value": "Use pytest -x for fast fail",
             "project_id": "proj1", "approved": True, "tags": ["testing"]},
        ])
        from packages.memory.context_summary import build_memory_context

        ctx = build_memory_context(project_id="proj1")
        assert ctx.item_count == 1
        assert ctx.items[0].approved is True

    def test_approved_item_title_bounded(self, tmp_path, monkeypatch):
        _setup_memory(tmp_path, monkeypatch, [
            {"key": "k", "value": "x" * 500,
             "project_id": "proj1", "approved": True},
        ])
        from packages.memory.context_summary import build_memory_context

        ctx = build_memory_context(project_id="proj1")
        assert len(ctx.items[0].title) <= 200


class TestUnapprovedExcluded:
    def test_unapproved_not_in_summary(self, tmp_path, monkeypatch):
        _setup_memory(tmp_path, monkeypatch, [
            {"key": "unapproved-item", "value": "secret stuff",
             "project_id": "proj1", "approved": False},
        ])
        from packages.memory.context_summary import build_memory_context

        ctx = build_memory_context(project_id="proj1")
        assert ctx.item_count == 0

    def test_mixed_approved_unapproved(self, tmp_path, monkeypatch):
        _setup_memory(tmp_path, monkeypatch, [
            {"key": "approved-one", "value": "good",
             "project_id": "proj1", "approved": True},
            {"key": "unapproved-one", "value": "bad",
             "project_id": "proj1", "approved": False},
        ])
        from packages.memory.context_summary import build_memory_context

        ctx = build_memory_context(project_id="proj1")
        assert ctx.item_count == 1
        assert ctx.items[0].title == "approved-one"


class TestBudgetTruncation:
    def test_budget_enforced_deterministically(self, tmp_path, monkeypatch):
        entries = [
            {"key": f"item-{i}", "value": "x" * 200,
             "project_id": "proj1", "approved": True}
            for i in range(20)
        ]
        _setup_memory(tmp_path, monkeypatch, entries)
        from packages.memory.context_summary import build_memory_context

        ctx = build_memory_context(project_id="proj1", budget=100)
        assert ctx.truncated is True
        assert ctx.item_count < 20
        assert ctx.estimated_tokens <= 100

    def test_same_input_same_hash(self, tmp_path, monkeypatch):
        _setup_memory(tmp_path, monkeypatch, [
            {"key": "stable", "value": "data",
             "project_id": "proj1", "approved": True},
        ])
        from packages.memory.context_summary import build_memory_context

        ctx1 = build_memory_context(project_id="proj1")
        ctx2 = build_memory_context(project_id="proj1")
        assert ctx1.context_hash == ctx2.context_hash


class TestRedactionPolicy:
    def test_redaction_field_present(self, tmp_path, monkeypatch):
        _setup_memory(tmp_path, monkeypatch)
        from packages.memory.context_summary import build_memory_context

        ctx = build_memory_context(project_id="proj1")
        assert ctx.redaction == "redact_secrets"

    def test_no_raw_value_in_export(self, tmp_path, monkeypatch):
        _setup_memory(tmp_path, monkeypatch, [
            {"key": "pattern", "value": "detailed raw content here",
             "project_id": "proj1", "approved": True},
        ])
        from packages.memory.context_summary import (
            build_memory_context,
            export_memory_context_json,
        )

        ctx = build_memory_context(project_id="proj1")
        exported = export_memory_context_json(ctx)
        # Raw value must not appear in export
        flat = str(exported)
        assert "detailed raw content here" not in flat


class TestContextHashChanges:
    def test_hash_changes_with_different_items(self, tmp_path, monkeypatch):
        _setup_memory(tmp_path, monkeypatch, [
            {"key": "a", "value": "x", "project_id": "proj1", "approved": True},
        ])
        from packages.memory.context_summary import build_memory_context

        ctx1 = build_memory_context(project_id="proj1")

        from packages.memory.local_gateway import store_memory
        store_memory(key="b", value="y", project_id="proj1", approved=True)

        ctx2 = build_memory_context(project_id="proj1")
        assert ctx1.context_hash != ctx2.context_hash


class TestModelContract:
    def test_module_exists(self):
        f = REPO_ROOT / "packages" / "memory" / "context_summary.py"
        assert f.is_file()

    def test_exports_expected_types(self):
        from packages.memory.context_summary import (
            build_memory_context,
            export_memory_context_json,
            format_memory_section,
        )
        assert callable(build_memory_context)
        assert callable(export_memory_context_json)
        assert callable(format_memory_section)
