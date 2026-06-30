"""Tests for token-saving reviewer prompts driven by the review scope packet.

``_build_reviewer_prompt`` renders a focused scope section when a scope packet
is supplied. A caller-supplied runtime packet (built by
``_build_runtime_scope_packet`` from the just-computed safe diff) takes
priority; otherwise it falls back to ``review_scope_packet.json`` on disk; and
when neither is present it falls back to the prior full-diff behavior.
"""
from __future__ import annotations

import json
from pathlib import Path

from packages.orchestration.pingpong_loop import (
    _build_reviewer_prompt,
    _build_runtime_scope_packet,
)


def _write_packet(tmp_path: Path, task_id: str, packet: dict) -> Path:
    run_dir = tmp_path / "task_runs" / task_id
    run_dir.mkdir(parents=True)
    (run_dir / "review_scope_packet.json").write_text(
        json.dumps(packet), encoding="utf-8"
    )
    return tmp_path


def _sample_packet(recommended_scope: str = "hunk_only") -> dict:
    return {
        "schema_version": "1.0.0",
        "task_id": "T001",
        "task_title": "Add scope packet rendering",
        "changed_files": ["packages/orchestration/pingpong_loop.py"],
        "changed_line_ranges": {
            "packages/orchestration/pingpong_loop.py": [[785, 843]]
        },
        "changed_symbols": {
            "packages/orchestration/pingpong_loop.py": ["_build_reviewer_prompt"]
        },
        "risk_tags": {
            "packages/orchestration/pingpong_loop.py": ["new_function"]
        },
        "prompt_hashes": ["abc123"],
        "evidence_refs": ["task_runs/T001/safe.diff"],
        "related_tests": ["tests/orchestration/test_reviewer_prompt_scope.py"],
        "open_findings": [],
        "estimated_review_tokens": 512,
        "recommended_scope": recommended_scope,
        "scope_reason": f"Recommended {recommended_scope}.",
    }


_NEW_FILE_DIFF = (
    "--- /dev/null\n"
    "+++ b/packages/orchestration/widget.py\n"
    "@@ -0,0 +1,3 @@\n"
    "+def make_widget():\n"
    "+    return 1\n"
    "+import os\n"
)


def test_reviewer_prompt_includes_scope_packet_fields(tmp_path: Path):
    prompt = _build_reviewer_prompt(
        "the goal",
        "builder summary",
        safe_diff="--- a/x\n+++ b/x\n",
        scope_packet=_sample_packet("file_level"),
    )

    # Changed files + symbols + risk tags + recommended scope all present.
    assert "packages/orchestration/pingpong_loop.py" in prompt
    assert "_build_reviewer_prompt" in prompt
    assert "new_function" in prompt
    assert "file_level" in prompt
    assert "Recommended file_level." in prompt
    assert "task_runs/T001/safe.diff" in prompt
    assert "abc123" in prompt
    assert "512" in prompt
    assert "Add scope packet rendering" in prompt
    assert "You may escalate scope" in prompt


def test_reviewer_prompt_hunk_only_focuses_hunks(tmp_path: Path):
    prompt = _build_reviewer_prompt(
        "the goal",
        "builder summary",
        scope_packet=_sample_packet("hunk_only"),
    )

    assert "hunk_only" in prompt
    assert "focus only on the listed hunks" in prompt.lower()


def test_reviewer_prompt_full_job_escalation(tmp_path: Path):
    prompt = _build_reviewer_prompt(
        "the goal",
        "builder summary",
        scope_packet=_sample_packet("full_job"),
    )

    assert "full_job" in prompt
    assert "full task evidence" in prompt.lower()
    assert "may escalate" in prompt.lower()


def test_reviewer_prompt_loads_packet_from_evidence_dir(tmp_path: Path):
    ev = _write_packet(tmp_path, "T001", _sample_packet("file_level"))

    prompt = _build_reviewer_prompt(
        "the goal",
        "builder summary",
        safe_diff="--- a/x\n+++ b/x\n",
        evidence_dir=str(ev),
        task_id="T001",
    )

    assert "Review Scope Packet" in prompt
    assert "Add scope packet rendering" in prompt


def test_reviewer_prompt_fallback_without_scope_packet(tmp_path: Path):
    # No packet supplied and none on disk -> fall back to full-diff behavior.
    prompt = _build_reviewer_prompt(
        "the goal",
        "builder summary",
        safe_diff="--- a/x\n+++ b/x\n@@ -1 +1 @@\n-old\n+new\n",
        evidence_dir=str(tmp_path),
        task_id="T001",
    )

    assert "Review Scope Packet" not in prompt
    assert "## Staged Unified Diff" in prompt
    assert "+new" in prompt


def test_build_runtime_scope_packet_from_diff():
    packet = _build_runtime_scope_packet(
        safe_diff=_NEW_FILE_DIFF,
        staged_files=["packages/orchestration/widget.py"],
        task_title="Add widget",
        task_id="T001",
        test_passed=True,
        repair_rounds=0,
    )

    assert packet is not None
    assert packet["changed_files"] == ["packages/orchestration/widget.py"]
    assert "make_widget" in packet["changed_symbols"][
        "packages/orchestration/widget.py"
    ]
    tags = packet["risk_tags"]["packages/orchestration/widget.py"]
    assert "new_file" in tags
    assert "new_function" in tags
    assert packet["recommended_scope"]
    assert packet["estimated_review_tokens"] > 0


def test_build_runtime_scope_packet_empty_inputs():
    assert _build_runtime_scope_packet(
        safe_diff="", staged_files=[],
    ) is None
    assert _build_runtime_scope_packet(
        safe_diff="--- a/x\n+++ b/x\n", staged_files=[],
    ) is None


def test_runtime_packet_flows_into_reviewer_prompt():
    packet = _build_runtime_scope_packet(
        safe_diff=_NEW_FILE_DIFF,
        staged_files=["packages/orchestration/widget.py"],
        task_title="Add widget",
        task_id="T001",
    )
    prompt = _build_reviewer_prompt(
        "the goal",
        "builder summary",
        safe_diff=_NEW_FILE_DIFF,
        scope_packet=packet,
    )

    assert "Review Scope Packet" in prompt
    assert "packages/orchestration/widget.py" in prompt
    assert "make_widget" in prompt


def test_scoped_prompt_includes_focused_diff():
    prompt = _build_reviewer_prompt(
        "the goal",
        "builder summary",
        safe_diff="--- a/x\n+++ b/x\n@@ -1 +1 @@\n-old\n+new\n",
        scope_packet=_sample_packet("hunk_only"),
    )
    assert "## Focused Staged Diff" in prompt


def test_scoped_prompt_omits_task_input_summary():
    prompt = _build_reviewer_prompt(
        "the goal",
        "builder summary",
        safe_diff="--- a/x\n+++ b/x\n",
        task_excerpt="some task excerpt",
        task_sha256="abc",
        task_tokens_estimated=100,
        scope_packet=_sample_packet("hunk_only"),
    )
    assert "## Task Input Summary" not in prompt


def test_scoped_prompt_omits_staged_unified_diff():
    prompt = _build_reviewer_prompt(
        "the goal",
        "builder summary",
        safe_diff="--- a/x\n+++ b/x\n@@ -1 +1 @@\n-old\n+new\n",
        scope_packet=_sample_packet("hunk_only"),
    )
    assert "## Staged Unified Diff" not in prompt


def test_scoped_prompt_omits_duplicate_files_changed():
    prompt = _build_reviewer_prompt(
        "the goal",
        "builder summary",
        safe_diff="--- a/x\n+++ b/x\n",
        files_changed=["packages/orchestration/pingpong_loop.py"],
        scope_packet=_sample_packet("hunk_only"),
    )
    assert "## Files Changed" not in prompt


def test_scoped_prompt_shorter_than_fallback_for_large_diff():
    large_diff = "--- a/x\n+++ b/x\n@@ -1 +1 @@\n" + "+line\n" * 8000
    scoped = _build_reviewer_prompt(
        "the goal",
        "builder summary",
        safe_diff=large_diff,
        files_changed=["x"],
        task_excerpt="task excerpt text",
        scope_packet=_sample_packet("hunk_only"),
    )
    fallback = _build_reviewer_prompt(
        "the goal",
        "builder summary",
        safe_diff=large_diff,
        files_changed=["x"],
        task_excerpt="task excerpt text",
    )
    assert len(scoped) < len(fallback)


def test_scoped_prompt_truncates_with_marker():
    large_diff = "--- a/x\n+++ b/x\n@@ -1 +1 @@\n" + "+line\n" * 5000
    assert len(large_diff) > 12000
    prompt = _build_reviewer_prompt(
        "the goal",
        "builder summary",
        safe_diff=large_diff,
        scope_packet=_sample_packet("hunk_only"),
    )
    assert "[FOCUSED DIFF TRUNCATED]" in prompt


def test_changed_test_file_is_in_scope():
    packet = _sample_packet("hunk_only")
    packet["changed_files"] = ["tests/orchestration/test_reviewer_prompt_scope.py"]
    packet["related_tests"] = ["tests/orchestration/test_reviewer_prompt_scope.py"]
    prompt = _build_reviewer_prompt(
        "the goal",
        "builder summary",
        scope_packet=packet,
    )
    assert "within review scope" in prompt.lower()
    assert "Do not flag" in prompt


def test_fallback_without_scope_packet_still_uses_full_diff():
    prompt = _build_reviewer_prompt(
        "the goal",
        "builder summary",
        safe_diff="--- a/x\n+++ b/x\n@@ -1 +1 @@\n-old\n+new\n",
    )
    assert "## Staged Unified Diff" in prompt
    assert "## Focused Staged Diff" not in prompt
