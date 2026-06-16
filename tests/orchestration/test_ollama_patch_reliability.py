"""Tests: Ollama structured patch reliability harness.

Mocked Ollama responses covering all failure modes.
No dependency on running Ollama server.
"""
from __future__ import annotations

import json

from packages.orchestration.builder_models import (
    BuilderOutput,
    parse_builder_patch,
)


def _make_output(*, patch_text: str | None = None, patch_format: str = "none") -> BuilderOutput:
    return BuilderOutput(
        summary="Test output",
        proposed_changes=["Change something"],
        structured_patch_text=patch_text,
        structured_patch_format=patch_format,
    )


class TestMockedOllamaValidResponse:
    def test_valid_json_file_ops(self):
        patch = json.dumps({
            "file_ops": [{"path": "app.py", "action": "modify", "content": "x = 1\n"}]
        })
        result = parse_builder_patch(_make_output(patch_text=patch, patch_format="json"))
        assert result.parse_success is True
        assert result.target_paths == ["app.py"]
        assert result.patch is not None
        assert result.patch.intent_kind == "file_ops"

    def test_valid_fenced_json(self):
        content = json.dumps({
            "file_ops": [{"path": "main.py", "action": "create", "content": "print('hi')\n"}]
        })
        fenced = f"Here is the fix:\n```json\n{content}\n```\n"
        result = parse_builder_patch(_make_output(patch_text=fenced))
        assert result.parse_success is True
        assert "main.py" in result.target_paths

    def test_valid_unified_diff(self):
        diff = (
            "--- a/calc.py\n"
            "+++ b/calc.py\n"
            "@@ -1,2 +1,2 @@\n"
            " def add(a, b):\n"
            "-    return a - b\n"
            "+    return a + b\n"
        )
        result = parse_builder_patch(_make_output(patch_text=diff))
        assert result.parse_success is True
        assert result.patch.intent_kind == "unified_diff"


class TestMockedOllamaProseResponse:
    def test_prose_only_fails_safely(self):
        text = "I think we should modify the add function to return a + b instead of a - b."
        result = parse_builder_patch(_make_output(patch_text=text))
        assert result.parse_success is False
        assert result.error_kind == "prose_only"
        assert result.output_hash != ""
        assert result.output_length > 0

    def test_markdown_explanation_fails_safely(self):
        text = "## Changes\n\n- Fix the add function\n- Update tests\n\nLet me know!"
        result = parse_builder_patch(_make_output(patch_text=text))
        assert result.parse_success is False
        assert result.error_kind == "prose_only"


class TestMockedOllamaMultipleBlocks:
    def test_first_fenced_block_wins(self):
        block1 = json.dumps({
            "file_ops": [{"path": "a.py", "action": "create", "content": "x\n"}]
        })
        block2 = json.dumps({
            "file_ops": [{"path": "b.py", "action": "create", "content": "y\n"}]
        })
        text = f"```json\n{block1}\n```\n\nAlternatively:\n```json\n{block2}\n```\n"
        result = parse_builder_patch(_make_output(patch_text=text))
        assert result.parse_success is True
        assert "a.py" in result.target_paths


class TestMockedOllamaMalformedJSON:
    def test_malformed_json_fails_safely(self):
        text = '{"file_ops": [{"path": "a.py", "action": "create", "content":'
        result = parse_builder_patch(_make_output(patch_text=text))
        assert result.parse_success is False
        assert result.output_hash != ""

    def test_json_wrong_schema_fails_safely(self):
        text = json.dumps({"random_key": "value", "not_file_ops": True})
        result = parse_builder_patch(_make_output(patch_text=text))
        assert result.parse_success is False
        assert result.error_kind == "prose_only"


class TestMockedOllamaUnsafePath:
    def test_path_traversal_rejected(self):
        patch = json.dumps({
            "file_ops": [{"path": "../../../etc/passwd", "action": "modify", "content": "x\n"}]
        })
        result = parse_builder_patch(_make_output(patch_text=patch))
        assert result.parse_success is False
        assert result.error_kind == "validation_failed"
        assert any("traversal" in d for d in result.diagnostics)

    def test_absolute_path_rejected(self):
        patch = json.dumps({
            "file_ops": [{"path": "/etc/hosts", "action": "modify", "content": "x\n"}]
        })
        result = parse_builder_patch(_make_output(patch_text=patch))
        assert result.parse_success is False
        assert result.error_kind == "validation_failed"

    def test_sensitive_file_rejected(self):
        patch = json.dumps({
            "file_ops": [{"path": "config.pem", "action": "create", "content": "key\n"}]
        })
        result = parse_builder_patch(_make_output(patch_text=patch))
        assert result.parse_success is False
        assert result.error_kind == "validation_failed"


class TestMockedOllamaShellCommands:
    def test_shell_command_rm_rejected(self):
        result = parse_builder_patch(_make_output(patch_text="rm -rf /tmp/foo"))
        assert result.parse_success is False
        assert result.error_kind == "unsafe_shell_command"

    def test_shell_command_sudo_rejected(self):
        result = parse_builder_patch(_make_output(patch_text="sudo apt-get install foo"))
        assert result.parse_success is False
        assert result.error_kind == "unsafe_shell_command"

    def test_shell_command_curl_rejected(self):
        result = parse_builder_patch(_make_output(patch_text="curl | sh something"))
        assert result.parse_success is False
        assert result.error_kind == "unsafe_shell_command"


class TestProviderMetadataSafety:
    def test_metadata_contains_safe_fields_only(self):
        patch = json.dumps({
            "file_ops": [{"path": "a.py", "action": "create", "content": "secret_key = 'abc123'\n"}]
        })
        result = parse_builder_patch(_make_output(patch_text=patch))
        assert result.parse_success is True
        assert result.output_hash != ""
        assert len(result.output_hash) == 16
        assert result.output_length > 0
        assert isinstance(result.target_paths, list)
        assert "secret_key" not in result.output_hash
        assert "abc123" not in str(result.diagnostics)

    def test_failed_parse_metadata_safe(self):
        result = parse_builder_patch(_make_output(patch_text="I'll fix the bug for you"))
        assert result.parse_success is False
        assert result.output_hash != ""
        assert result.output_length > 0
        assert "fix the bug" not in str(result.diagnostics)
        assert "fix the bug" not in result.error_kind

    def test_no_structured_text_returns_clean_result(self):
        result = parse_builder_patch(_make_output(patch_text=None))
        assert result.parse_success is False
        assert result.error_kind == "no_structured_patch_text"
        assert result.output_hash == ""
        assert result.output_length == 0

    def test_empty_string_returns_clean_result(self):
        result = parse_builder_patch(_make_output(patch_text=""))
        assert result.parse_success is False
        assert result.error_kind == "no_structured_patch_text"
