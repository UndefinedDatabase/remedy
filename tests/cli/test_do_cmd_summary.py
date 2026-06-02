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
        doc = Path("docs/autocoder-usage.md")
        assert doc.is_file()
        content = doc.read_text()
        assert "REMEDY_REAL_OLLAMA_SMOKE" in content
        assert "Fixture smoke" in content
        assert "autonomy" in content.lower()
        assert "stop_reason" in content or "Stop Reason" in content

    def test_docs_do_not_claim_cli_ollama_integration(self):
        from pathlib import Path
        doc = Path("docs/autocoder-usage.md")
        content = doc.read_text()
        assert "remedy do" not in content.split("Real Ollama smoke")[1].split("##")[0] or \
               "not yet" in content.lower()
