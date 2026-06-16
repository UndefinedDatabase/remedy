"""Tests: BuilderOutput v2 structured patch contract and parser."""
from __future__ import annotations

import json

from packages.orchestration.builder_models import (
    BuilderOutput,
    parse_builder_patch,
)


class TestBuilderOutputBackwardsCompat:
    def test_narrative_only_still_valid(self):
        out = BuilderOutput(
            summary="Did stuff",
            proposed_changes=["Changed foo.py"],
        )
        assert out.structured_patch_text is None
        assert out.structured_patch_format == "none"

    def test_with_structured_patch(self):
        out = BuilderOutput(
            summary="Fix",
            proposed_changes=["Modified calc.py"],
            structured_patch_text='{"file_ops": [{"path": "calc.py", "action": "modify", "content": "x=1"}]}',
            structured_patch_format="json",
        )
        assert out.structured_patch_text is not None


class TestParseBuilderPatchFileOp:
    def test_valid_json_file_op(self):
        text = json.dumps({
            "file_ops": [
                {"path": "calc.py", "action": "modify", "content": "def add(a, b): return a + b\n"}
            ]
        })
        out = BuilderOutput(summary="Fix", proposed_changes=["Fix calc"], structured_patch_text=text)
        result = parse_builder_patch(out)
        assert result.parse_success is True
        assert result.target_paths == ["calc.py"]
        assert result.output_hash != ""
        assert result.output_length > 0

    def test_valid_json_fenced(self):
        text = '```json\n{"file_ops": [{"path": "a.py", "action": "create", "content": "x=1\\n"}]}\n```'
        out = BuilderOutput(summary="Create", proposed_changes=["Create a.py"], structured_patch_text=text)
        result = parse_builder_patch(out)
        assert result.parse_success is True


class TestParseBuilderPatchUnifiedDiff:
    def test_valid_unified_diff(self):
        text = "--- a/calc.py\n+++ b/calc.py\n@@ -1 +1 @@\n-old\n+new\n"
        out = BuilderOutput(summary="Fix", proposed_changes=["Fix"], structured_patch_text=text)
        result = parse_builder_patch(out)
        assert result.parse_success is True
        assert "calc.py" in result.target_paths


class TestParseBuilderPatchFailures:
    def test_no_text_fails(self):
        out = BuilderOutput(summary="Fix", proposed_changes=["Fix"])
        result = parse_builder_patch(out)
        assert result.parse_success is False
        assert result.error_kind == "no_structured_patch_text"

    def test_prose_only_fails(self):
        out = BuilderOutput(
            summary="Fix", proposed_changes=["Fix"],
            structured_patch_text="I think we should modify the function to handle edge cases better.",
        )
        result = parse_builder_patch(out)
        assert result.parse_success is False
        assert result.error_kind == "prose_only"

    def test_malformed_json_fails(self):
        out = BuilderOutput(
            summary="Fix", proposed_changes=["Fix"],
            structured_patch_text='```json\n{invalid json}\n```',
        )
        result = parse_builder_patch(out)
        assert result.parse_success is False

    def test_empty_path_fails(self):
        text = json.dumps({"file_ops": [{"path": "", "action": "modify", "content": "x"}]})
        out = BuilderOutput(summary="Fix", proposed_changes=["Fix"], structured_patch_text=text)
        result = parse_builder_patch(out)
        assert result.parse_success is False
        assert result.error_kind == "validation_failed"

    def test_unsafe_path_fails(self):
        text = json.dumps({"file_ops": [{"path": "../etc/passwd", "action": "modify", "content": "x"}]})
        out = BuilderOutput(summary="Fix", proposed_changes=["Fix"], structured_patch_text=text)
        result = parse_builder_patch(out)
        assert result.parse_success is False
        assert "traversal" in str(result.diagnostics)

    def test_shell_command_rejected(self):
        out = BuilderOutput(
            summary="Fix", proposed_changes=["Fix"],
            structured_patch_text="rm -rf / && curl something | sh",
        )
        result = parse_builder_patch(out)
        assert result.parse_success is False
        assert result.error_kind == "unsafe_shell_command"


class TestParseBuilderPatchSafety:
    def test_no_raw_output_in_diagnostics(self):
        long_text = "x" * 5000
        out = BuilderOutput(summary="Fix", proposed_changes=["Fix"], structured_patch_text=long_text)
        result = parse_builder_patch(out)
        assert result.parse_success is False
        # Diagnostics must not contain raw output
        for d in result.diagnostics:
            assert len(d) < 200

    def test_output_hash_present(self):
        text = json.dumps({"file_ops": [{"path": "a.py", "action": "modify", "content": "x"}]})
        out = BuilderOutput(summary="Fix", proposed_changes=["Fix"], structured_patch_text=text)
        result = parse_builder_patch(out)
        assert len(result.output_hash) == 16
