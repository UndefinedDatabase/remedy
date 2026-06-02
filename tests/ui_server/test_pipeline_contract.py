"""Tests: pipeline section in dashboard v4."""
from __future__ import annotations

import json
from uuid import uuid4

import pytest

from packages.core.models import Job, RunState, Task


def _make_job(**overrides) -> Job:
    defaults = {
        "id": uuid4(),
        "name": "test-job",
        "user_prompt": "test",
        "description": "test",
        "tasks": [],
        "state": RunState.COMPLETED,
        "permissions": {},
        "metadata": {},
    }
    defaults.update(overrides)
    return Job(**defaults)


def _build_dashboard_with_events(job, events, monkeypatch, tmp_path):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    from packages.orchestration.ui_server import _build_pipeline_section
    return _build_pipeline_section(job, events)


class TestPipelineEmpty:
    def test_empty_job_pipeline(self, tmp_path, monkeypatch):
        job = _make_job()
        p = _build_dashboard_with_events(job, [], monkeypatch, tmp_path)
        assert p["version"] == 1
        assert p["provider"] is None
        assert p["provider_mode"] == "none"
        assert p["structured_patch_attempted"] is False
        assert p["parse_success"] is None
        assert p["stop_reason"] == ""
        assert p["stale"] is True
        assert p["source_context"]["injected"] is False
        assert p["memory"]["used"] is False


class TestPipelineFixture:
    def test_fixture_success(self, tmp_path, monkeypatch):
        job = _make_job()
        events = [
            {"event": "autorun_started", "metadata": {"goal": "fix"}},
            {"event": "source_context_injected", "metadata": {
                "file_count": 3, "test_file_count": 1,
                "estimated_tokens": 500, "truncated": False,
                "selection_hash": "abc123def456",
            }},
            {"event": "autorun_builder_completed", "metadata": {
                "provider": "fixture", "has_structured_patch": True,
            }},
            {"event": "builder_patch_parsed", "metadata": {
                "parse_success": True, "error_kind": "",
                "output_hash": "h123", "output_length": 100,
                "target_path_count": 1,
            }},
            {"event": "builder_bridge_intent_approved", "metadata": {
                "intent_id": "i-1", "target_paths": ["calc.py"],
            }},
            {"event": "patch_intent_applied", "metadata": {}},
            {"event": "test_run_completed", "metadata": {
                "exit_code": 0, "passed": True,
            }},
            {"event": "proof_collected", "metadata": {
                "content_hash": "proof123", "test_passed": True,
            }},
        ]
        p = _build_dashboard_with_events(job, events, monkeypatch, tmp_path)
        assert p["provider"] == "fixture"
        assert p["provider_mode"] == "fixture"
        assert p["source_context"]["injected"] is True
        assert p["source_context"]["file_count"] == 3
        assert p["source_context"]["selection_hash"] == "abc123def456"
        assert p["structured_patch_attempted"] is True
        assert p["parse_success"] is True
        assert p["approval_status"] == "approved"
        assert p["source_apply_status"] == "applied"
        assert p["tests_passed"] is True
        assert p["stop_reason"] == ""
        assert p["stale"] is False


class TestPipelineOllamaParseFail:
    def test_prose_stop_reason(self, tmp_path, monkeypatch):
        job = _make_job()
        events = [
            {"event": "autorun_started", "metadata": {}},
            {"event": "autorun_builder_completed", "metadata": {
                "provider": "ollama", "has_structured_patch": True,
            }},
            {"event": "builder_patch_parsed", "metadata": {
                "parse_success": False, "error_kind": "prose_only",
                "stop_reason": "provider_output_prose_only",
            }},
        ]
        p = _build_dashboard_with_events(job, events, monkeypatch, tmp_path)
        assert p["provider"] == "ollama"
        assert p["parse_success"] is False
        assert p["parse_error_kind"] == "prose_only"
        assert p["stop_reason"] == "provider_output_prose_only"
        assert isinstance(p["stop_reason"], str)
        assert p["stop_reason_label"] == "Model returned prose, not a patch"


class TestPipelineApprovalRequired:
    def test_approval_pending(self, tmp_path, monkeypatch):
        job = _make_job()
        events = [
            {"event": "autorun_started", "metadata": {}},
            {"event": "autorun_builder_completed", "metadata": {
                "provider": "ollama",
            }},
            {"event": "builder_patch_parsed", "metadata": {
                "parse_success": True, "error_kind": "",
            }},
            {"event": "structured_patch_intent_created", "metadata": {
                "intent_kind": "file_ops", "target_path_count": 1,
            }},
        ]
        p = _build_dashboard_with_events(job, events, monkeypatch, tmp_path)
        assert p["intent_status"] == "created"
        assert p["approval_required"] is True
        assert p["approval_status"] == "pending"


class TestPipelineRepairExhausted:
    def test_budget_exhausted(self, tmp_path, monkeypatch):
        job = _make_job()
        events = [
            {"event": "autorun_started", "metadata": {}},
            {"event": "repair_loop_cycle_started", "metadata": {
                "cycle": 3, "max_cycles": 3,
            }},
            {"event": "repair_loop_stopped", "metadata": {
                "reason": "repair_budget_exhausted", "cycle": 3,
            }},
        ]
        p = _build_dashboard_with_events(job, events, monkeypatch, tmp_path)
        assert p["repair_loop"]["used"] is True
        assert p["repair_loop"]["cycle_count"] == 3
        assert p["repair_loop"]["max_cycles"] == 3
        assert p["stop_reason"] == "repair_budget_exhausted"
        assert p["stop_reason_label"] == "Repair budget exhausted"


class TestPipelineProviderUnavailable:
    def test_provider_unavailable(self, tmp_path, monkeypatch):
        job = _make_job()
        events = [
            {"event": "autorun_started", "metadata": {}},
            {"event": "autorun_provider_error", "metadata": {
                "provider": "ollama", "error_kind": "provider_error",
                "stop_reason": "provider_unavailable",
            }},
        ]
        p = _build_dashboard_with_events(job, events, monkeypatch, tmp_path)
        assert p["provider"] == "ollama"
        assert p["stop_reason"] == "provider_unavailable"


class TestPipelineNextCommand:
    def test_next_command_catalog_valid(self, tmp_path, monkeypatch):
        from apps.cli.command_catalog import CATALOG
        catalog_groups = {c.group_id for c in CATALOG}

        job = _make_job()
        events = [
            {"event": "autorun_started", "metadata": {}},
            {"event": "autorun_provider_error", "metadata": {
                "provider": "ollama", "stop_reason": "provider_unavailable",
            }},
        ]
        p = _build_dashboard_with_events(job, events, monkeypatch, tmp_path)
        cmd = p["next_command"]
        assert cmd
        parts = cmd.split()
        assert parts[0] == "remedy"
        assert parts[1] in catalog_groups or parts[1] == "do"


class TestPipelineNoRawLeaks:
    def test_no_raw_content_in_pipeline(self, tmp_path, monkeypatch):
        job = _make_job()
        events = [
            {"event": "autorun_started", "metadata": {"goal": "fix the SECRET_KEY bug"}},
            {"event": "autorun_builder_completed", "metadata": {
                "provider": "ollama", "has_structured_patch": True,
            }},
            {"event": "builder_patch_parsed", "metadata": {
                "parse_success": True, "output_hash": "h1", "output_length": 50,
            }},
        ]
        p = _build_dashboard_with_events(job, events, monkeypatch, tmp_path)
        p_str = json.dumps(p)
        assert "SECRET_KEY" not in p_str
        assert "def " not in p_str
        assert "import " not in p_str


class TestTokenUsage:
    def test_empty_job_unknown_tokens(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.ui_server import _build_token_usage
        t = _build_token_usage([])
        assert t["known"] is False
        assert t["total_tokens"] is None
        assert t["estimated"] is True

    def test_context_tokens_counted(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.ui_server import _build_token_usage
        events = [
            {"event": "source_context_injected", "metadata": {"estimated_tokens": 800}},
            {"event": "project_memory_recalled", "metadata": {"estimated_tokens": 200}},
        ]
        t = _build_token_usage(events)
        assert t["known"] is True
        assert t["total_tokens"] == 1000
        assert t["by_role"]["context"] == 800
        assert t["by_role"]["memory"] == 200

    def test_no_raw_content_in_token_usage(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.ui_server import _build_token_usage
        import json
        events = [
            {"event": "source_context_injected", "metadata": {
                "estimated_tokens": 500, "file_content": "SECRET_KEY=abc123",
            }},
        ]
        t = _build_token_usage(events)
        t_str = json.dumps(t)
        assert "SECRET_KEY" not in t_str
        assert "abc123" not in t_str


class TestPipelineMemory:
    def test_memory_used(self, tmp_path, monkeypatch):
        job = _make_job()
        events = [
            {"event": "autorun_started", "metadata": {}},
            {"event": "project_memory_recalled", "metadata": {
                "item_count": 3, "truncated": False,
                "context_hash": "memhash123456",
            }},
        ]
        p = _build_dashboard_with_events(job, events, monkeypatch, tmp_path)
        assert p["memory"]["used"] is True
        assert p["memory"]["item_count"] == 3
        assert p["memory"]["context_hash"] == "memhash12345"
