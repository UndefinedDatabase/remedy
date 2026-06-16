"""Opt-in real `remedy do` Ollama smoke test.

Tests the actual autorun path with --builder-provider ollama.
Requires: REMEDY_REAL_OLLAMA_SMOKE=1 and running Ollama server.

Usage:
  # CI fixture (always runs):
  python3 -m pytest tests/orchestration/test_real_do_ollama_smoke.py::TestFixtureDoSmoke -v

  # Real Ollama (opt-in):
  REMEDY_REAL_OLLAMA_SMOKE=1 python3 -m pytest tests/orchestration/test_real_do_ollama_smoke.py::TestRealDoOllamaSmoke -v
"""
from __future__ import annotations

import os

import pytest

from tests.orchestration.small_repo_fixtures import create_missing_function_repo


class TestFixtureDoSmoke:
    def test_fixture_provider_full_pipeline(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.orchestration.autorun import run_autorun
        result = run_autorun(
            "fix the add function", str(tmp_path),
            builder_provider="fixture",
            autonomy_level=4,
            max_cycles=1,
        )
        assert result.stage != "builder_skipped_no_worker"
        assert any(e["event"] == "structured_patch_created" for e in result.events)

    def test_fixture_provider_json_output_shape(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.orchestration.autorun import run_autorun
        result = run_autorun(
            "fix", str(tmp_path),
            builder_provider="fixture",
            autonomy_level=4,
            json_output=True,
        )
        out = {
            "version": 2,
            "job_id": result.job_id,
            "stage": result.stage,
            "stop_reason": result.stop_reason,
            "provider": result.provider,
        }
        assert "job_id" in out
        assert "stop_reason" in out
        assert isinstance(out["stop_reason"], str)


def _ollama_available() -> bool:
    try:
        import ollama
        client = ollama.Client()
        client.list()
        return True
    except Exception:
        return False


@pytest.mark.skipif(
    not os.environ.get("REMEDY_REAL_OLLAMA_SMOKE"),
    reason="Set REMEDY_REAL_OLLAMA_SMOKE=1 to run real Ollama do smoke",
)
class TestRealDoOllamaSmoke:
    def test_real_ollama_do_pipeline(self, tmp_path, monkeypatch):
        if not _ollama_available():
            pytest.skip("Ollama server not available")

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        repo = create_missing_function_repo(tmp_path / "repo")

        from packages.orchestration.autorun import run_autorun
        result = run_autorun(
            "add a hello() function that returns 'hello'",
            str(repo),
            builder_provider="ollama",
            autonomy_level=2,
            max_cycles=1,
        )

        assert result.provider == "ollama"
        assert any(e["event"] == "structured_patch_attempted" for e in result.events)
        assert result.stop_reason != "" or result.stage in ("approval_pending", "proof_collected")

    def test_real_ollama_do_no_raw_leak(self, tmp_path, monkeypatch):
        if not _ollama_available():
            pytest.skip("Ollama server not available")

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        repo = create_missing_function_repo(tmp_path / "repo")

        from packages.orchestration.autorun import run_autorun
        from packages.orchestration.timeline import load_run_events
        result = run_autorun(
            "add hello()", str(repo),
            builder_provider="ollama",
            autonomy_level=2,
            max_cycles=1,
        )

        events = load_run_events(tmp_path / "data", result.job_id)
        for event in events:
            meta_str = str(event.get("metadata", {}))
            assert "def hello" not in meta_str
