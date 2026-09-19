"""Tests: builder provider mode selection and Ollama wiring."""
from __future__ import annotations

import pytest


class TestBuilderProviderParse:
    """F268 (R-0933): `do`'s `--builder-provider` takes the four providers
    `create_provider` builds; the old none/fixture values are refused."""

    def test_the_four_providers_and_omission_are_accepted(self):
        from apps.cli.commands.do_cmd import _validate_role_override
        for name in ("fake", "claude", "claude-cli", "ollama", None):
            _validate_role_override("builder", "provider", name)

    def test_the_retired_values_exit_2(self):
        from apps.cli.commands.do_cmd import _validate_role_override
        for bad in ("none", "fixture"):
            with pytest.raises(SystemExit) as exc:
                _validate_role_override("builder", "provider", bad)
            assert exc.value.code == 2

    def test_parse_invalid_exits(self):
        from apps.cli.commands.do_cmd import _validate_role_override
        with pytest.raises(SystemExit):
            _validate_role_override("builder", "provider", "invalid")

    def test_catalog_has_builder_provider_arg(self):
        from apps.cli.command_catalog import CATALOG
        do_entry = next(c for c in CATALOG if c.command_id == "do.run")
        arg_names = [a.name for a in do_entry.args]
        assert "--builder-provider" in arg_names


class TestProviderModelWiring:
    def test_build_claude_cli_args_includes_model(self):
        from packages.orchestration.pingpong_provider import build_claude_cli_args
        argv = build_claude_cli_args("/usr/bin/claude", "test prompt", model="claude-opus-4-20250514")
        assert "--model" in argv
        idx = argv.index("--model")
        assert argv[idx + 1] == "claude-opus-4-20250514"

    def test_build_claude_cli_args_no_model_when_empty(self):
        from packages.orchestration.pingpong_provider import build_claude_cli_args
        argv = build_claude_cli_args("/usr/bin/claude", "test prompt")
        assert "--model" not in argv

    def test_claude_cli_provider_stores_model(self):
        from packages.orchestration.pingpong_provider import ClaudeCliProvider
        p = ClaudeCliProvider(model="claude-opus-4-20250514")
        assert p.model == "claude-opus-4-20250514"

    def test_claude_cli_provider_default_model_empty(self):
        from packages.orchestration.pingpong_provider import ClaudeCliProvider
        p = ClaudeCliProvider()
        assert p.model == ""

    def test_create_provider_passes_model_to_claude_cli(self):
        from packages.orchestration.pingpong_provider import create_provider
        p = create_provider("claude-cli", model="claude-opus-4-20250514")
        assert hasattr(p, "model")
        assert p.model == "claude-opus-4-20250514"

    def test_create_provider_fake_ignores_model(self):
        from packages.orchestration.pingpong_provider import create_provider
        p = create_provider("fake", model="whatever")
        assert p.name == "fake"

    def test_execution_config_has_model_fields(self):
        from packages.orchestration.pingpong_job import ExecutionConfig
        ec = ExecutionConfig(
            builder="claude-cli",
            builder_model="claude-opus-4-20250514",
            builder_effort="high",
            reviewer="claude-cli",
            reviewer_model="claude-opus-4-20250514",
            reviewer_effort="medium",
        )
        assert ec.builder_model == "claude-opus-4-20250514"
        assert ec.builder_effort == "high"
        assert ec.reviewer_model == "claude-opus-4-20250514"
        assert ec.reviewer_effort == "medium"

    def test_execution_config_export_import_roundtrip(self):
        from packages.orchestration.pingpong_job import (
            ExecutionConfig,
            _export_execution_config,
            _import_execution_config,
        )
        ec = ExecutionConfig(
            builder="claude-cli",
            builder_model="claude-opus-4-20250514",
            builder_model_source="cli",
            reviewer="claude-cli",
            reviewer_model="claude-opus-4-20250514",
            repair_provider="fake",
            repair_model="fake-model",
            repair_effort="low",
        )
        exported = _export_execution_config(ec)
        imported = _import_execution_config(exported)
        assert imported.builder_model == "claude-opus-4-20250514"
        assert imported.builder_model_source == "cli"
        assert imported.reviewer_model == "claude-opus-4-20250514"
        assert imported.repair_provider == "fake"
        assert imported.repair_model == "fake-model"
        assert imported.repair_effort == "low"

    def test_prompt_trace_has_model(self):
        from packages.orchestration.prompt_trace import build_trace_entry
        entry = build_trace_entry(
            prompt_text="test prompt",
            role="builder",
            provider="claude-cli",
            configured_model="claude-opus-4-20250514",
        )
        assert entry.configured_model == "claude-opus-4-20250514"

    def test_trace_summary_has_per_role_model_summary(self):
        from packages.orchestration.prompt_trace import (
            PromptTraceEntry,
            build_trace_summary,
        )
        entries = [
            PromptTraceEntry(role="builder", provider="claude-cli", configured_model="opus", prompt_chars=100),
            PromptTraceEntry(role="reviewer", provider="claude-cli", configured_model="opus", prompt_chars=50),
        ]
        summary = build_trace_summary(entries)
        assert "per_role_model_summary" in summary
        assert "builder" in summary["per_role_model_summary"]
        assert summary["per_role_model_summary"]["builder"]["configured_model"] == "opus"
        assert "reviewer" in summary["per_role_model_summary"]
