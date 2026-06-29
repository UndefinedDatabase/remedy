"""Prompt-trace lens redaction tests — path sanitization breadth + no raw leak.

Steps 5451-5480, T004 — redaction-safe fixtures.

These tests deliberately avoid redaction-triggering identifiers. Prompt bodies
use a benign marker string instead of sensitive tokens so the assertions prove
the *path* sanitization breadth without smuggling redaction-bait into safe.diff.
"""
from __future__ import annotations

import json

from packages.orchestration.ui_server import (
    _build_prompt_trace,
    _redact_preview,
    _safe_rel_file,
)

# Benign sentinel: if a raw prompt body ever leaked into the dashboard payload,
# this exact string would appear verbatim. It is NOT a redaction trigger.
marker_string = "TOP_LEVEL_PROMPT_BODY_SHOULD_NOT_LEAK_INTO_DASHBOARD"


def _write_trace(ev_dir, task_id: str, records: list[dict]) -> None:
    d = ev_dir / "task_runs" / task_id
    d.mkdir(parents=True)
    lines = "\n".join(json.dumps(r) for r in records)
    (d / "prompt_trace.jsonl").write_text(lines + "\n")


def _record(**overrides) -> dict:
    rec = {
        "run_id": "runABC",
        "job_id": "jobABC",
        "task_id": "T001",
        "round": 1,
        "role": "builder",
        "provider": "fake",
        "provider_kind": "synthetic_test",
        "prompt_kind": "initial",
        "prompt_sha256": "feedface",
        "prompt_chars": 80,
        "prompt_tokens_estimated": 20,
        "context_categories": ["goal"],
        "changed_files": ["docs/NOTES.md"],
        "safe_diff_files": [],
        "prompt_text_redacted": f"Builder body {marker_string} end.",
        "prompt_text_truncated": False,
    }
    rec.update(overrides)
    return rec


class TestNoRawLeak:
    def test_no_raw_prompt_field_in_serialized_section(self, tmp_path):
        _write_trace(tmp_path, "T001", [_record()])
        blob = json.dumps(_build_prompt_trace(tmp_path))
        for forbidden in ("prompt_text\"", "prompt_text_redacted", "promptText"):
            assert forbidden not in blob

    def test_marker_only_in_bounded_preview_not_raw_field(self, tmp_path):
        # The marker may legitimately appear inside the bounded redactedPreview,
        # but never via a raw/unredacted field name.
        _write_trace(tmp_path, "T001", [_record()])
        item = _build_prompt_trace(tmp_path)["items"][0]
        assert marker_string in item["redactedPreview"]
        assert "prompt_text_redacted" not in item
        assert "promptText" not in item


class TestPreviewPathStripping:
    def test_home_stripped_from_preview(self, tmp_path):
        leaky = f"{marker_string} at /home/alice/work/file.py done"
        _write_trace(tmp_path, "T001", [_record(prompt_text_redacted=leaky)])
        preview = _build_prompt_trace(tmp_path)["items"][0]["redactedPreview"]
        assert "/home/" not in preview
        assert "[local]" in preview

    def test_tmp_stripped_from_preview(self, tmp_path):
        leaky = f"{marker_string} at /tmp/remedy-build/file.py done"
        _write_trace(tmp_path, "T001", [_record(prompt_text_redacted=leaky)])
        preview = _build_prompt_trace(tmp_path)["items"][0]["redactedPreview"]
        assert "/tmp/" not in preview
        assert "[staging]" in preview

    def test_users_stripped_from_preview(self, tmp_path):
        leaky = f"{marker_string} at /Users/bob/code/file.py done"
        _write_trace(tmp_path, "T001", [_record(prompt_text_redacted=leaky)])
        preview = _build_prompt_trace(tmp_path)["items"][0]["redactedPreview"]
        assert "/Users/" not in preview
        assert "[local]" in preview

    def test_mnt_stripped_from_preview(self, tmp_path):
        leaky = f"{marker_string} at /mnt/data/vol/file.py done"
        _write_trace(tmp_path, "T001", [_record(prompt_text_redacted=leaky)])
        preview = _build_prompt_trace(tmp_path)["items"][0]["redactedPreview"]
        assert "/mnt/" not in preview
        assert "[local]" in preview

    def test_private_stripped_from_preview(self, tmp_path):
        leaky = f"{marker_string} at /private/var/file.py done"
        _write_trace(tmp_path, "T001", [_record(prompt_text_redacted=leaky)])
        preview = _build_prompt_trace(tmp_path)["items"][0]["redactedPreview"]
        assert "/private/" not in preview
        assert "[local]" in preview

    def test_job_workspaces_stripped_from_preview(self, tmp_path):
        leaky = f"{marker_string} at .data/job_workspaces/job9/file.py done"
        _write_trace(tmp_path, "T001", [_record(prompt_text_redacted=leaky)])
        preview = _build_prompt_trace(tmp_path)["items"][0]["redactedPreview"]
        assert ".data/job_workspaces/" not in preview
        assert "[workspace]" in preview


class TestChangedFilesSafe:
    def test_home_and_tmp_stripped_from_changed_files(self, tmp_path):
        _write_trace(tmp_path, "T001", [_record(changed_files=[
            "/home/alice/proj/notes.py",
            "/tmp/scratch/draft.py",
        ])])
        changed = _build_prompt_trace(tmp_path)["items"][0]["changedFilesSafe"]
        joined = "/".join(changed)
        assert "/home/" not in joined
        assert "/tmp/" not in joined
        # Absolute prefixes with no repo marker collapse to basename only.
        assert changed == ["notes.py", "draft.py"]

    def test_repo_relative_structure_preserved(self, tmp_path):
        _write_trace(tmp_path, "T001", [_record(changed_files=[
            "/abs/root/packages/orchestration/ui_server.py",
            "/somewhere/apps/ui/src/main.tsx",
        ])])
        changed = _build_prompt_trace(tmp_path)["items"][0]["changedFilesSafe"]
        assert changed == [
            "packages/orchestration/ui_server.py",
            "apps/ui/src/main.tsx",
        ]


class TestNoAbsolutePaths:
    def test_no_absolute_paths_in_serialized_section(self, tmp_path):
        leaky = (
            f"{marker_string} /home/u /tmp/x /Users/u /mnt/d /private/v "
            ".data/job_workspaces/w"
        )
        _write_trace(tmp_path, "T001", [_record(
            prompt_text_redacted=leaky,
            changed_files=["/home/u/a.py", "/tmp/x/b.py"],
            safe_diff_files=["/Users/u/c.py"],
        )])
        blob = json.dumps(_build_prompt_trace(tmp_path))
        for leak in ("/home/", "/tmp/", "/Users/", "/mnt/", "/private/",
                     ".data/job_workspaces/"):
            assert leak not in blob


class TestLensHelpersDirect:
    def test_redact_preview_collapses_every_family(self):
        text = "/tmp/a /home/b /Users/c /private/d /mnt/e .data/job_workspaces/f"
        out = _redact_preview(text)
        for leak in ("/tmp/", "/home/", "/Users/", "/private/", "/mnt/",
                     ".data/job_workspaces/"):
            assert leak not in out

    def test_safe_rel_file_strips_private_absolute_prefix(self):
        assert _safe_rel_file("/Users/dev/throwaway.py") == "throwaway.py"
        assert _safe_rel_file("/abs/tests/ui_server/x.py") == "tests/ui_server/x.py"
