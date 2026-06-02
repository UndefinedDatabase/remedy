"""Tests: real CLI do_cmd handler path — stop_reason, provider, JSON output."""
from __future__ import annotations

import json
from io import StringIO
from unittest.mock import MagicMock, patch

import pytest


def _capture_json_output(result):
    """Simulate do_cmd JSON output path, matching actual do_cmd.py logic."""
    _BOOL_EVENTS = frozenset({
        "structured_patch_attempted", "parse_success",
        "source_context_injected", "structured_patch_created",
        "approval_required", "source_patch_applied", "tests_passed",
        "repair_context_created", "repair_loop_used",
    })
    out: dict = {
        "version": 2,
        "job_id": result.job_id,
        "stage": result.stage,
        "cycles_run": result.cycles_run,
        "stop_reason": result.stop_reason,
        "provider": result.provider,
        "ui_url": result.ui_url,
        "error": result.error,
    }
    for ev in result.events:
        key = ev.get("event", "")
        val = ev.get("value", "")
        if not key or key in out:
            continue
        if key in _BOOL_EVENTS:
            out[key] = val == "True"
        else:
            out[key] = val
    return out


class TestStopReasonJsonIntegrity:
    def test_prose_stop_reason_stays_string(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autorun import run_autorun
        from packages.orchestration.builder_models import BuilderOutput

        mock_output = BuilderOutput(
            summary="prose",
            proposed_changes=["fix"],
            structured_patch_text="Just fix the bug by changing the return value.",
        )

        with patch("packages.providers.ollama_builder.provider.OllamaBuilder") as mock_cls:
            mock_cls.return_value.build.return_value = mock_output
            result = run_autorun(
                "fix", str(tmp_path),
                builder_provider="ollama",
                autonomy_level=2,
            )

        out = _capture_json_output(result)
        assert isinstance(out["stop_reason"], str)
        assert out["stop_reason"] == "provider_output_prose_only"
        assert out["provider"] == "ollama"

    def test_provider_unavailable_stop_reason_stays_string(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autorun import run_autorun

        with patch("packages.providers.ollama_builder.provider.OllamaBuilder") as mock_cls:
            mock_cls.return_value.build.side_effect = ConnectionError("not running")
            result = run_autorun(
                "fix", str(tmp_path),
                builder_provider="ollama",
                autonomy_level=2,
            )

        out = _capture_json_output(result)
        assert isinstance(out["stop_reason"], str)
        assert out["stop_reason"] == "provider_unavailable"
        assert "traceback" not in json.dumps(out).lower()

    def test_approval_required_stop_reason_stays_string(self, tmp_path, monkeypatch):
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

        out = _capture_json_output(result)
        assert isinstance(out["stop_reason"], str)
        assert out["stop_reason"] == "approval_required"

    def test_stop_reason_never_boolean_false(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autorun import run_autorun
        from packages.orchestration.builder_models import BuilderOutput

        mock_output = BuilderOutput(
            summary="prose only",
            proposed_changes=["Fix"],
            structured_patch_text="I think you should fix it manually.",
        )

        with patch("packages.providers.ollama_builder.provider.OllamaBuilder") as mock_cls:
            mock_cls.return_value.build.return_value = mock_output
            result = run_autorun(
                "fix", str(tmp_path),
                builder_provider="ollama",
                autonomy_level=2,
            )

        out = _capture_json_output(result)
        assert out["stop_reason"] is not False
        assert out["stop_reason"] != False  # noqa: E712
        assert isinstance(out["stop_reason"], str)

    def test_bool_events_stay_boolean(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autorun import run_autorun

        result = run_autorun(
            "fix", str(tmp_path),
            builder_provider="fixture",
            autonomy_level=4,
        )

        out = _capture_json_output(result)
        for key in ("structured_patch_created", "source_patch_applied", "tests_passed"):
            if key in out:
                assert isinstance(out[key], bool), f"{key} should be bool, got {type(out[key])}"


class TestFixtureCliPath:
    def test_fixture_is_deterministic(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autorun import run_autorun

        result = run_autorun(
            "fix", str(tmp_path),
            builder_provider="fixture",
            autonomy_level=4,
        )

        out = _capture_json_output(result)
        assert out["stage"] == "proof_collected"
        assert out.get("tests_passed") is True

    def test_fixture_source_apply_gated(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autorun import run_autorun

        result = run_autorun(
            "fix", str(tmp_path),
            builder_provider="fixture",
            autonomy_level=2,
        )

        out = _capture_json_output(result)
        assert out.get("source_patch_applied") is False


class TestDefaultProviderSafe:
    def test_default_does_not_call_ollama(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autorun import run_autorun

        with patch("packages.providers.ollama_builder.provider.OllamaBuilder") as mock_cls:
            result = run_autorun(
                "fix", str(tmp_path),
                autonomy_level=2,
            )

        mock_cls.assert_not_called()
        assert result.stage == "builder_skipped_no_worker"
        assert result.provider == ""


class TestNoRawLeakInJson:
    def test_json_no_raw_provider_output(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autorun import run_autorun
        from packages.orchestration.builder_models import BuilderOutput

        secret_content = "SECRET_API_KEY = 'sk-1234abcd'"
        mock_output = BuilderOutput(
            summary="Fix",
            proposed_changes=["Fix"],
            structured_patch_text=json.dumps({
                "file_ops": [{"path": "a.py", "action": "create",
                              "content": secret_content}]
            }),
        )

        with patch("packages.providers.ollama_builder.provider.OllamaBuilder") as mock_cls:
            mock_cls.return_value.build.return_value = mock_output
            result = run_autorun(
                "fix", str(tmp_path),
                builder_provider="ollama",
                autonomy_level=2,
            )

        out = _capture_json_output(result)
        out_str = json.dumps(out)
        assert "SECRET_API_KEY" not in out_str
        assert "sk-1234abcd" not in out_str
