"""Tests for agent run trace model and helpers."""
from __future__ import annotations

from packages.orchestration.agent_run_trace import (
    build_trace_summary,
    create_trace_event,
    load_trace_jsonl,
    trace_event_to_dict,
    write_trace_jsonl,
)


class TestRunTraceEventCreation:
    def test_creates_event_with_required_fields(self):
        ev = create_trace_event("job_flow_started", job_id="abc123")
        assert ev.event_kind == "job_flow_started"
        assert ev.job_id == "abc123"
        assert ev.created_at

    def test_event_has_all_optional_fields(self):
        ev = create_trace_event(
            "builder_prompt_created",
            job_id="j1", task_id="T001", run_id="r1",
            round_num=2, role="builder", provider="fake",
            provider_kind="synthetic_test", prompt_kind="repair",
            prompt_sha256="abc", prompt_chars=1000,
            changed_files_safe=["main.py"],
            finding_ids=["F1"], verdict="pass",
            status="completed", outcome="applied",
            safe_summary="Built changes",
        )
        assert ev.task_id == "T001"
        assert ev.round == 2
        assert ev.provider_kind == "synthetic_test"
        assert ev.changed_files_safe == ["main.py"]
        assert ev.finding_ids == ["F1"]

    def test_safe_summary_capped_at_500(self):
        ev = create_trace_event("job_planned", safe_summary="x" * 1000)
        assert len(ev.safe_summary) == 500

    def test_empty_safe_summary_ok(self):
        ev = create_trace_event("job_planned")
        assert ev.safe_summary == ""


class TestRunTraceJsonl:
    def test_write_and_load_roundtrip(self, tmp_path):
        events = [
            create_trace_event("job_flow_started", job_id="j1"),
            create_trace_event("task_started", job_id="j1", task_id="T001"),
            create_trace_event("final_audit_completed", job_id="j1", status="READY"),
        ]
        path = tmp_path / "trace.jsonl"
        write_trace_jsonl(events, path)
        loaded = load_trace_jsonl(path)
        assert len(loaded) == 3
        assert loaded[0]["event_kind"] == "job_flow_started"
        assert loaded[1]["task_id"] == "T001"
        assert loaded[2]["status"] == "READY"

    def test_load_missing_file_returns_empty(self, tmp_path):
        result = load_trace_jsonl(tmp_path / "nonexistent.jsonl")
        assert result == []

    def test_load_skips_invalid_json_lines(self, tmp_path):
        path = tmp_path / "trace.jsonl"
        path.write_text('{"event_kind": "ok"}\nnot json\n{"event_kind": "also_ok"}\n')
        loaded = load_trace_jsonl(path)
        assert len(loaded) == 2

    def test_trace_event_to_dict(self):
        ev = create_trace_event("task_started", job_id="j1", task_id="T001")
        d = trace_event_to_dict(ev)
        assert isinstance(d, dict)
        assert d["event_kind"] == "task_started"
        assert d["task_id"] == "T001"


class TestRunTraceSummary:
    def test_summary_counts_event_kinds(self):
        events = [
            create_trace_event("builder_prompt_created", provider="fake"),
            create_trace_event("reviewer_prompt_created", provider="fake"),
            create_trace_event("builder_prompt_created", provider="fake"),
            create_trace_event("repair_prompt_created", provider="fake"),
        ]
        summary = build_trace_summary(events)
        assert summary["total_events"] == 4
        assert summary["event_counts"]["builder_prompt_created"] == 2
        assert summary["event_counts"]["reviewer_prompt_created"] == 1
        assert summary["has_builder_events"] is True
        assert summary["has_reviewer_events"] is True
        assert summary["has_repair_events"] is True

    def test_summary_tracks_tasks_and_providers(self):
        events = [
            create_trace_event("task_started", task_id="T001", provider="fake"),
            create_trace_event("task_started", task_id="T002", provider="claude-cli"),
        ]
        summary = build_trace_summary(events)
        assert sorted(summary["tasks_traced"]) == ["T001", "T002"]
        assert sorted(summary["providers"]) == ["claude-cli", "fake"]

    def test_summary_tracks_max_round(self):
        events = [
            create_trace_event("builder_prompt_created", round_num=1),
            create_trace_event("reviewer_prompt_created", round_num=3),
        ]
        summary = build_trace_summary(events)
        assert summary["max_round"] == 3

    def test_empty_summary(self):
        summary = build_trace_summary([])
        assert summary["total_events"] == 0
        assert summary["has_builder_events"] is False
        assert summary["has_final_audit"] is False


class TestNoRawContentInTrace:
    def test_event_has_no_raw_content_fields(self):
        ev = create_trace_event(
            "builder_output_received",
            safe_summary="Applied 3 files",
        )
        d = trace_event_to_dict(ev)
        for key in d:
            assert "stdout" not in key
            assert "stderr" not in key
            assert "raw" not in key
            assert "diff" not in key.lower() or key == "safe_diff_files"
