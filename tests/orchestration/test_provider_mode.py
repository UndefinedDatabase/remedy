"""Tests: builder provider mode selection and Ollama wiring."""
from __future__ import annotations

import json
from unittest.mock import patch

import pytest


class TestProviderModeSelection:
    def test_default_no_provider_gives_skipped(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autorun import run_autorun
        result = run_autorun("test goal", str(tmp_path), autonomy_level=2)
        assert result.stage == "builder_skipped_no_worker"
        assert result.provider == ""

    def test_fixture_provider_works(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autorun import run_autorun
        result = run_autorun(
            "fix the bug", str(tmp_path),
            builder_provider="fixture",
            autonomy_level=4,
        )
        assert result.stage != "builder_skipped_no_worker"
        assert any(e["event"] == "structured_patch_created" for e in result.events)

    def test_ollama_unavailable_gives_provider_unavailable(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autorun import run_autorun

        def mock_build(*args, **kwargs):
            raise ConnectionError("Ollama not running")

        with patch("packages.providers.ollama_builder.provider.OllamaBuilder") as mock_cls:
            mock_cls.return_value.build.side_effect = mock_build
            result = run_autorun(
                "fix bug", str(tmp_path),
                builder_provider="ollama",
                autonomy_level=2,
            )

        assert result.stage == "provider_error"
        assert result.stop_reason == "provider_unavailable"
        assert result.provider == "ollama"

    def test_ollama_valid_patch_creates_intent(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autorun import run_autorun
        from packages.orchestration.builder_models import BuilderOutput

        (tmp_path / "app.py").write_text("# placeholder\n")
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "test_app.py").write_text(
            "from app import hello\ndef test_hello():\n    assert hello() == 'hello'\n"
        )

        mock_output = BuilderOutput(
            summary="Add hello function",
            proposed_changes=["Add hello()"],
            structured_patch_text=json.dumps({
                "file_ops": [{"path": "app.py", "action": "modify",
                              "content": "def hello():\n    return 'hello'\n"}]
            }),
            structured_patch_format="json",
        )

        with patch("packages.providers.ollama_builder.provider.OllamaBuilder") as mock_cls:
            mock_cls.return_value.build.return_value = mock_output
            result = run_autorun(
                "add hello", str(tmp_path),
                builder_provider="ollama",
                autonomy_level=4,
            )

        assert result.provider == "ollama"
        assert result.stage == "proof_collected"
        assert result.stop_reason == ""
        assert any(e["event"] == "parse_success" and e["value"] == "True" for e in result.events)
        assert any(e["event"] == "tests_passed" and e["value"] == "True" for e in result.events)

    def test_ollama_prose_output_stops_with_reason(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autorun import run_autorun
        from packages.orchestration.builder_models import BuilderOutput

        mock_output = BuilderOutput(
            summary="I think you should fix the bug",
            proposed_changes=["Fix the bug"],
            structured_patch_text="I suggest changing the return value to be correct.",
        )

        with patch("packages.providers.ollama_builder.provider.OllamaBuilder") as mock_cls:
            mock_cls.return_value.build.return_value = mock_output
            result = run_autorun(
                "fix bug", str(tmp_path),
                builder_provider="ollama",
                autonomy_level=4,
            )

        assert result.provider == "ollama"
        assert result.stop_reason == "provider_output_prose_only"
        assert result.stage == "parse_failed"

    def test_ollama_approval_required_at_low_autonomy(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autorun import run_autorun
        from packages.orchestration.builder_models import BuilderOutput

        mock_output = BuilderOutput(
            summary="Fix",
            proposed_changes=["Fix"],
            structured_patch_text=json.dumps({
                "file_ops": [{"path": "a.py", "action": "create", "content": "x=1\n"}]
            }),
        )

        with patch("packages.providers.ollama_builder.provider.OllamaBuilder") as mock_cls:
            mock_cls.return_value.build.return_value = mock_output
            result = run_autorun(
                "fix", str(tmp_path),
                builder_provider="ollama",
                autonomy_level=2,
            )

        assert result.stop_reason == "approval_required"
        assert result.stage == "approval_pending"

    def test_no_raw_output_in_events(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autorun import run_autorun
        from packages.orchestration.builder_models import BuilderOutput
        from packages.orchestration.timeline import load_run_events

        mock_output = BuilderOutput(
            summary="Fix",
            proposed_changes=["Fix"],
            structured_patch_text=json.dumps({
                "file_ops": [{"path": "a.py", "action": "create",
                              "content": "SECRET_KEY = 'abc123'\n"}]
            }),
        )

        with patch("packages.providers.ollama_builder.provider.OllamaBuilder") as mock_cls:
            mock_cls.return_value.build.return_value = mock_output
            result = run_autorun(
                "fix", str(tmp_path),
                builder_provider="ollama",
                autonomy_level=2,
            )

        events = load_run_events(tmp_path, result.job_id)
        for event in events:
            meta_str = str(event.get("metadata", {}))
            assert "SECRET_KEY" not in meta_str
            assert "abc123" not in meta_str


class TestStopReasonPropagation:
    def test_fixture_stop_reason_in_result(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autorun import run_autorun
        result = run_autorun(
            "fix", str(tmp_path),
            builder_provider="fixture",
            autonomy_level=2,
        )
        # Fixture at autonomy 2 should have structured_patch_created but no apply
        assert result.stage != "builder_skipped_no_worker"

    def test_json_output_has_stop_reason_and_provider(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autorun import run_autorun
        from packages.orchestration.builder_models import BuilderOutput

        mock_output = BuilderOutput(
            summary="prose only",
            proposed_changes=["Fix"],
            structured_patch_text="Just fix it",
        )

        with patch("packages.providers.ollama_builder.provider.OllamaBuilder") as mock_cls:
            mock_cls.return_value.build.return_value = mock_output
            result = run_autorun(
                "fix", str(tmp_path),
                builder_provider="ollama",
                autonomy_level=2,
            )

        out = {
            "version": 2,
            "job_id": result.job_id,
            "stage": result.stage,
            "stop_reason": result.stop_reason,
            "provider": result.provider,
        }
        assert out["stop_reason"] == "provider_output_prose_only"
        assert out["provider"] == "ollama"
        assert out["stage"] == "parse_failed"


class TestBuilderProviderParse:
    def test_parse_none(self):
        from apps.cli.commands.do_cmd import _parse_builder_provider
        assert _parse_builder_provider("none") == "none"

    def test_parse_fixture(self):
        from apps.cli.commands.do_cmd import _parse_builder_provider
        assert _parse_builder_provider("fixture") == "fixture"

    def test_parse_ollama(self):
        from apps.cli.commands.do_cmd import _parse_builder_provider
        assert _parse_builder_provider("ollama") == "ollama"

    def test_parse_invalid_exits(self):
        from apps.cli.commands.do_cmd import _parse_builder_provider
        with pytest.raises(SystemExit):
            _parse_builder_provider("invalid")

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
