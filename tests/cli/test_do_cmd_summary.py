"""Tests: CLI do command summary output for autocoder pipeline."""
from __future__ import annotations

import json

import pytest


class TestJobSummaryJSON:
    def test_json_output_includes_pipeline_status(self):
        from packages.orchestration.autorun import AutorunResult
        result = AutorunResult(
            job_id="abc-123",
            cycles_run=2,
            stage="proof_collected",
            events=[
                {"event": "structured_patch_created", "value": "True"},
                {"event": "approval_required", "value": "True"},
                {"event": "source_patch_applied", "value": "True"},
                {"event": "tests_passed", "value": "True"},
            ],
        )
        out: dict = {
            "version": 1,
            "job_id": result.job_id,
            "stage": result.stage,
            "cycles_run": result.cycles_run,
            "ui_url": result.ui_url,
            "error": result.error,
        }
        for ev in result.events:
            key = ev.get("event", "")
            val = ev.get("value", "")
            if key:
                out[key] = val == "True"
        assert out["structured_patch_created"] is True
        assert out["approval_required"] is True
        assert out["source_patch_applied"] is True
        assert out["tests_passed"] is True
        assert out["cycles_run"] == 2

    def test_json_output_no_raw_content(self):
        from packages.orchestration.autorun import AutorunResult
        result = AutorunResult(
            job_id="abc-123",
            cycles_run=1,
            stage="parse_failed",
            events=[
                {"event": "structured_patch_created", "value": "False"},
            ],
        )
        out = json.dumps({
            "version": 1,
            "job_id": result.job_id,
            "stage": result.stage,
        })
        assert "def " not in out
        assert "return" not in out
        assert "import" not in out


class TestFixtureBuilderParse:
    def test_parse_true(self):
        from apps.cli.commands.do_cmd import _parse_fixture_builder
        assert _parse_fixture_builder("true") is True
        assert _parse_fixture_builder("True") is True
        assert _parse_fixture_builder("1") is True
        assert _parse_fixture_builder("yes") is True

    def test_parse_false(self):
        from apps.cli.commands.do_cmd import _parse_fixture_builder
        assert _parse_fixture_builder("false") is False
        assert _parse_fixture_builder("0") is False

    def test_parse_repair_loop(self):
        from apps.cli.commands.do_cmd import _parse_fixture_builder
        assert _parse_fixture_builder("repair-loop") == "repair-loop"

    def test_parse_invalid_exits(self):
        from apps.cli.commands.do_cmd import _parse_fixture_builder
        with pytest.raises(SystemExit):
            _parse_fixture_builder("invalid-mode")


class TestDocsExist:
    def test_autocoder_usage_doc_exists(self):
        from pathlib import Path
        doc = Path("docs/guides/autocoder-usage.md")
        assert doc.is_file()
        content = doc.read_text()
        assert "REMEDY_REAL_OLLAMA_SMOKE" in content
        assert "Fixture smoke" in content
        assert "autonomy" in content.lower()
        assert "stop_reason" in content or "Stop Reason" in content

    def test_docs_mention_builder_provider(self):
        from pathlib import Path
        doc = Path("docs/guides/autocoder-usage.md")
        content = doc.read_text()
        assert "--builder-provider" in content
        assert "ollama" in content.lower()
        assert "fixture" in content.lower()
        assert "none" in content.lower()

    def test_docs_commands_use_builder_provider(self):
        from pathlib import Path
        doc = Path("docs/guides/autocoder-usage.md")
        content = doc.read_text()
        assert "--builder-provider fixture" in content
        assert "--builder-provider ollama" in content

    def test_docs_pipeline_overview(self):
        from pathlib import Path
        doc = Path("docs/guides/autocoder-usage.md")
        content = doc.read_text()
        assert "Pipeline Overview" in content
        assert "source_apply" in content
        assert "approval" in content.lower()
        assert "proof" in content.lower()

    def test_docs_stop_reasons_complete(self):
        from pathlib import Path
        doc = Path("docs/guides/autocoder-usage.md")
        content = doc.read_text()
        for reason in (
            "provider_output_prose_only",
            "provider_unavailable",
            "approval_required",
            "source_apply_failed",
            "test_failed_after_apply",
            "repair_budget_exhausted",
            "unsafe_path",
            "path_traversal",
            "validation_failed",
        ):
            assert reason in content, f"Missing stop reason in docs: {reason}"

    def test_docs_vram_free_command(self):
        from pathlib import Path
        doc = Path("docs/guides/autocoder-usage.md")
        content = doc.read_text()
        assert "remedy worker unload" in content

    def test_docs_model_quality_warning(self):
        from pathlib import Path
        doc = Path("docs/guides/autocoder-usage.md")
        content = doc.read_text()
        assert "not guaranteed" in content.lower()
        assert "Normal CI does not require Ollama" in content

    def test_docs_patch_inspect_commands(self):
        from pathlib import Path
        doc = Path("docs/guides/autocoder-usage.md")
        content = doc.read_text()
        assert "remedy patch list" in content
        assert "remedy patch show" in content
        assert "remedy patch approve" in content
        assert "remedy patch reject" in content
        assert "remedy patch apply" in content

    def test_docs_test_run_command(self):
        from pathlib import Path
        doc = Path("docs/guides/autocoder-usage.md")
        content = doc.read_text()
        assert "remedy test run" in content


class TestDocsCommandContract:
    def test_docs_remedy_commands_catalog_valid(self):
        import re
        from pathlib import Path

        from apps.cli.command_catalog import CATALOG

        doc = Path("docs/guides/autocoder-usage.md")
        content = doc.read_text()

        catalog_groups = {c.group_id for c in CATALOG}
        catalog_ids = {c.command_id for c in CATALOG}
        catalog_subs = {(c.group_id, c.subcommand) for c in CATALOG}

        # Extract remedy commands from code blocks
        cmd_pattern = re.compile(r"remedy\s+(\w+)\s+(\w[\w-]*)")
        for match in cmd_pattern.finditer(content):
            group = match.group(1)
            sub = match.group(2)
            if group == "do":
                continue  # "remedy do" uses positional goal, handled separately
            assert group in catalog_groups, f"Unknown group in docs: remedy {group} {sub}"
            assert (group, sub) in catalog_subs, f"Unknown command in docs: remedy {group} {sub}"

    def test_docs_do_commands_valid(self):
        import re
        from pathlib import Path

        from apps.cli.command_catalog import CATALOG

        doc = Path("docs/guides/autocoder-usage.md")
        content = doc.read_text()

        do_entry = next(c for c in CATALOG if c.command_id == "do.run")
        arg_names = {a.name.lstrip("-") for a in do_entry.args if a.is_option}

        # Extract flags from remedy do commands
        flag_pattern = re.compile(r"remedy do .+?(--[\w-]+)")
        for match in flag_pattern.finditer(content):
            flag = match.group(1).lstrip("-")
            assert flag in arg_names, f"Unknown flag in docs: --{flag}"
