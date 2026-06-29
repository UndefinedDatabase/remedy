"""Tests for the safe prompt trace dashboard payload + path sanitization.

Steps 5451-5480, T001 — backend completion (path sanitization, prompt trace
payload, activity metadata).
"""
from __future__ import annotations

import json

from packages.orchestration.ui_server import (
    _build_prompt_trace,
    _empty_prompt_trace,
    _redact_preview,
    _safe_rel_file,
)


def _write_trace(ev_dir, task_id: str, records: list[dict]) -> None:
    d = ev_dir / "task_runs" / task_id
    d.mkdir(parents=True)
    lines = "\n".join(json.dumps(r) for r in records)
    (d / "prompt_trace.jsonl").write_text(lines + "\n")


def _base_record(**overrides) -> dict:
    rec = {
        "run_id": "run123",
        "job_id": "job123",
        "task_id": "T001",
        "round": 1,
        "role": "builder",
        "provider": "fake",
        "provider_kind": "synthetic_test",
        "prompt_kind": "initial",
        "prompt_sha256": "deadbeef",
        "prompt_chars": 100,
        "prompt_tokens_estimated": 25,
        "context_categories": ["goal", "file_tree"],
        "changed_files": ["docs/README.md"],
        "safe_diff_files": [],
        "prompt_text_redacted": "You are a Builder. Goal: add test.",
        "prompt_text_truncated": False,
    }
    rec.update(overrides)
    return rec


class TestRedactPreview:
    def test_strips_all_listed_path_families(self):
        text = (
            "a /tmp/x b /home/u c /Users/u d /private/v "
            "e /mnt/d f .data/job_workspaces/w g remedy-pingpong-abc done"
        )
        out = _redact_preview(text)
        for leak in ("/tmp/x", "/home/u", "/Users/u", "/private/v",
                     "/mnt/d", ".data/job_workspaces/w", "remedy-pingpong-abc"):
            assert leak not in out
        assert "[staging]" in out
        assert "[local]" in out
        assert "[workspace]" in out

    def test_empty_passthrough(self):
        assert _redact_preview("") == ""


class TestSafeRelFile:
    def test_preserves_repo_relative_structure(self):
        assert _safe_rel_file("/abs/root/packages/orchestration/x.py") == \
            "packages/orchestration/x.py"
        assert _safe_rel_file("/x/apps/ui/main.ts") == "apps/ui/main.ts"

    def test_falls_back_to_basename_without_marker(self):
        assert _safe_rel_file("/abs/path/secret.py") == "secret.py"

    def test_relative_path_unchanged(self):
        assert _safe_rel_file("docs/README.md") == "docs/README.md"

    def test_empty(self):
        assert _safe_rel_file("") == ""


class TestPromptTracePayload:
    def test_items_read_from_jsonl(self, tmp_path):
        _write_trace(tmp_path, "T001", [
            _base_record(role="builder", prompt_kind="initial"),
            _base_record(role="reviewer", prompt_kind="review"),
        ])
        section = _build_prompt_trace(tmp_path)
        assert section["source"] == "prompt_trace_jsonl"
        assert section["totalPrompts"] == 2
        assert section["builderPrompts"] == 1
        assert section["reviewerPrompts"] == 1
        assert len(section["items"]) == 2

    def test_full_items_have_all_fields(self, tmp_path):
        _write_trace(tmp_path, "T001", [_base_record()])
        item = _build_prompt_trace(tmp_path)["items"][0]
        for field in (
            "id", "taskId", "runId", "round", "role", "promptKind", "provider",
            "providerKind", "promptSha256", "promptChars", "promptTokensEstimated",
            "contextCategories", "changedFilesSafe", "safeDiffFiles", "evidenceRef",
            "redactedPreview", "redactedPreviewTruncated",
        ):
            assert field in item

    def test_no_raw_unredacted_field(self, tmp_path):
        _write_trace(tmp_path, "T001", [_base_record()])
        blob = json.dumps(_build_prompt_trace(tmp_path))
        for forbidden in ("prompt_text\"", "prompt_text_redacted", "promptText"):
            assert forbidden not in blob

    def test_preview_truncated_at_1200(self, tmp_path):
        _write_trace(tmp_path, "T001", [_base_record(prompt_text_redacted="x" * 5000)])
        item = _build_prompt_trace(tmp_path)["items"][0]
        assert len(item["redactedPreview"]) == 1200
        assert item["redactedPreviewTruncated"] is True

    def test_short_preview_not_truncated(self, tmp_path):
        _write_trace(tmp_path, "T001", [_base_record(prompt_text_redacted="short")])
        item = _build_prompt_trace(tmp_path)["items"][0]
        assert item["redactedPreview"] == "short"
        assert item["redactedPreviewTruncated"] is False

    def test_evidence_ref_is_relative(self, tmp_path):
        _write_trace(tmp_path, "T001", [_base_record()])
        item = _build_prompt_trace(tmp_path)["items"][0]
        assert item["evidenceRef"] == "task_runs/T001/prompt_trace.jsonl"

    def test_no_absolute_paths_in_payload(self, tmp_path):
        leaky = "work dir /tmp/remedy-pingpong-abc/x and done"
        _write_trace(tmp_path, "T001", [
            _base_record(prompt_text_redacted=leaky, changed_files=["/abs/path/secret.py"]),
        ])
        item = _build_prompt_trace(tmp_path)["items"][0]
        assert "/tmp/remedy-pingpong-abc" not in item["redactedPreview"]
        assert "[staging]" in item["redactedPreview"]
        assert item["changedFilesSafe"] == ["secret.py"]

    def test_missing_evidence_dir_is_absent(self):
        section = _build_prompt_trace(None)
        assert section["source"] == "absent"
        assert section["missingReason"] == "evidence_dir_unavailable"
        assert section["items"] == []

    def test_missing_task_runs_is_absent(self, tmp_path):
        section = _build_prompt_trace(tmp_path)
        assert section["source"] == "absent"
        assert section["missingReason"] == "task_runs_missing"

    def test_missing_trace_file_is_absent(self, tmp_path):
        (tmp_path / "task_runs").mkdir()
        section = _build_prompt_trace(tmp_path)
        assert section["source"] == "absent"
        assert section["missingReason"] == "prompt_trace_jsonl_missing"

    def test_repair_prompt_counted(self, tmp_path):
        _write_trace(tmp_path, "T001", [
            _base_record(role="builder", prompt_kind="repair", round=2),
            _base_record(role="reviewer", prompt_kind="re-review", round=2),
        ])
        assert _build_prompt_trace(tmp_path)["repairPrompts"] == 2

    def test_unknown_role_and_kind_normalized(self, tmp_path):
        _write_trace(tmp_path, "T001", [_base_record(role="ghost", prompt_kind="weird")])
        item = _build_prompt_trace(tmp_path)["items"][0]
        assert item["role"] == "system"
        assert item["promptKind"] == "unknown"

    def test_tokens_summed(self, tmp_path):
        _write_trace(tmp_path, "T001", [
            _base_record(prompt_tokens_estimated=25),
            _base_record(prompt_tokens_estimated=75),
        ])
        assert _build_prompt_trace(tmp_path)["totalPromptTokensEstimated"] == 100

    def test_empty_prompt_trace_helper(self):
        section = _empty_prompt_trace("some_reason")
        assert section["source"] == "absent"
        assert section["missingReason"] == "some_reason"
        assert section["totalPrompts"] == 0
        assert section["items"] == []
