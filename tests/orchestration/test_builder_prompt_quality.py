"""Tests: builder prompt quality and parser alignment for Ollama responses."""
from __future__ import annotations

import json

import pytest

from packages.orchestration.builder_models import BuilderOutput, parse_builder_patch


class TestPromptContent:
    def test_system_prompt_contains_file_ops_schema(self):
        from packages.providers.ollama_builder.provider import _SYSTEM_PROMPT
        assert "file_ops" in _SYSTEM_PROMPT
        assert '"path"' in _SYSTEM_PROMPT
        assert '"action"' in _SYSTEM_PROMPT
        assert '"content"' in _SYSTEM_PROMPT

    def test_system_prompt_discourages_prose(self):
        from packages.providers.ollama_builder.provider import _SYSTEM_PROMPT
        assert "No markdown" in _SYSTEM_PROMPT or "no prose" in _SYSTEM_PROMPT.lower()

    def test_system_prompt_forbids_shell_commands(self):
        from packages.providers.ollama_builder.provider import _SYSTEM_PROMPT
        assert "shell" in _SYSTEM_PROMPT.lower() or "rm" in _SYSTEM_PROMPT

    def test_system_prompt_requires_relative_paths(self):
        from packages.providers.ollama_builder.provider import _SYSTEM_PROMPT
        assert "relative" in _SYSTEM_PROMPT.lower()

    def test_system_prompt_forbids_traversal(self):
        from packages.providers.ollama_builder.provider import _SYSTEM_PROMPT
        assert ".." in _SYSTEM_PROMPT

    def test_user_message_includes_goal(self):
        from uuid import uuid4
        from packages.orchestration.builder_models import TaskExecutionContext
        from packages.providers.ollama_builder.provider import _build_user_message
        ctx = TaskExecutionContext(
            job_id=uuid4(), task_id=uuid4(),
            job_prompt="add hello function",
            task_type="code_change",
            task_description="Write hello() in app.py",
        )
        msg = _build_user_message(ctx)
        assert "add hello function" in msg
        assert "code_change" in msg

    def test_user_message_includes_memory_context(self):
        from uuid import uuid4
        from packages.orchestration.builder_models import TaskExecutionContext
        from packages.providers.ollama_builder.provider import _build_user_message
        ctx = TaskExecutionContext(
            job_id=uuid4(), task_id=uuid4(),
            job_prompt="fix",
            task_type="code_change",
            task_description="Fix the bug",
            memory_context="Project uses pytest for testing.",
        )
        msg = _build_user_message(ctx)
        assert "Project uses pytest" in msg


class TestParserOllamaMistakes:
    def test_wrapper_text_before_json_block(self):
        text = 'Here is the fix:\n```json\n{"file_ops": [{"path": "a.py", "action": "create", "content": "x=1\\n"}]}\n```\n'
        result = parse_builder_patch(BuilderOutput(
            summary="Fix", proposed_changes=["Fix"],
            structured_patch_text=text,
        ))
        assert result.parse_success is True

    def test_trailing_explanation_after_json(self):
        patch = json.dumps({"file_ops": [{"path": "a.py", "action": "create", "content": "x=1\n"}]})
        text = f"{patch}\n\nThis should fix the issue."
        result = parse_builder_patch(BuilderOutput(
            summary="Fix", proposed_changes=["Fix"],
            structured_patch_text=text,
        ))
        assert result.parse_success is True

    def test_missing_code_fence_plain_json(self):
        text = json.dumps({"file_ops": [{"path": "a.py", "action": "create", "content": "x=1\n"}]})
        result = parse_builder_patch(BuilderOutput(
            summary="Fix", proposed_changes=["Fix"],
            structured_patch_text=text,
        ))
        assert result.parse_success is True

    def test_json_with_leading_whitespace(self):
        text = "   \n" + json.dumps({"file_ops": [{"path": "a.py", "action": "create", "content": "x=1\n"}]})
        result = parse_builder_patch(BuilderOutput(
            summary="Fix", proposed_changes=["Fix"],
            structured_patch_text=text,
        ))
        assert result.parse_success is True

    def test_bad_path_names_rejected(self):
        text = json.dumps({"file_ops": [{"path": "/etc/passwd", "action": "modify", "content": "x\n"}]})
        result = parse_builder_patch(BuilderOutput(
            summary="Fix", proposed_changes=["Fix"],
            structured_patch_text=text,
        ))
        assert result.parse_success is False

    def test_pure_prose_no_json(self):
        result = parse_builder_patch(BuilderOutput(
            summary="Fix", proposed_changes=["Fix"],
            structured_patch_text="I recommend modifying the hello function to return the correct value.",
        ))
        assert result.parse_success is False
        assert result.error_kind == "prose_only"

    def test_json_with_wrong_keys(self):
        text = json.dumps({"changes": [{"file": "a.py", "type": "edit"}]})
        result = parse_builder_patch(BuilderOutput(
            summary="Fix", proposed_changes=["Fix"],
            structured_patch_text=text,
        ))
        assert result.parse_success is False
