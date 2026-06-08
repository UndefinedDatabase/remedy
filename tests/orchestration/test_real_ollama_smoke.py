"""Opt-in real Ollama smoke test.

Requires: REMEDY_REAL_OLLAMA_SMOKE=1 and running Ollama server with a model.
Skips cleanly in CI and when Ollama is unavailable.

Usage:
  # Fixture smoke (always runs in CI):
  python3 -m pytest tests/orchestration/test_real_ollama_smoke.py::TestFixtureSmoke -v

  # Real Ollama smoke (opt-in):
  REMEDY_REAL_OLLAMA_SMOKE=1 python3 -m pytest tests/orchestration/test_real_ollama_smoke.py::TestRealOllamaSmoke -v

  # Free VRAM after testing:
  ollama stop <model-name>
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import pytest

from packages.orchestration.builder_models import BuilderOutput, parse_builder_patch
from tests.orchestration.small_repo_fixtures import (
    create_missing_function_repo,
    fixture_patch_missing_function,
)


class TestFixtureSmoke:
    """CI-safe fixture smoke — no Ollama, deterministic."""

    def test_fixture_pipeline_on_real_repo(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.core.models import Job
        from packages.orchestration.builder_bridge import run_builder_bridge

        repo = create_missing_function_repo(tmp_path / "repo")
        patch = fixture_patch_missing_function()
        output = BuilderOutput(
            summary="Add hello function",
            proposed_changes=["Add hello()"],
            structured_patch_text=json.dumps(patch),
            structured_patch_format="json",
        )
        job = Job(name="fixture-smoke")
        result = run_builder_bridge(
            output, repo, job=job, data_dir=tmp_path / "data",
            autonomy_level=4,
        )
        assert result.parse_result.parse_success is True
        assert result.apply_success is True
        assert result.test_passed is True
        assert result.stage == "proof_collected"

    def test_fixture_pipeline_stops_at_approval(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.core.models import Job
        from packages.orchestration.builder_bridge import run_builder_bridge

        repo = create_missing_function_repo(tmp_path / "repo")
        patch = fixture_patch_missing_function()
        output = BuilderOutput(
            summary="Add hello function",
            proposed_changes=["Add hello()"],
            structured_patch_text=json.dumps(patch),
            structured_patch_format="json",
        )
        job = Job(name="fixture-smoke")
        result = run_builder_bridge(
            output, repo, job=job, data_dir=tmp_path / "data",
            autonomy_level=2,
        )
        assert result.stage == "approval_pending"
        assert result.apply_success is False


def _ollama_available() -> bool:
    """Check if Ollama server is reachable."""
    try:
        import ollama
        client = ollama.Client()
        client.list()
        return True
    except Exception:
        return False


@pytest.mark.skipif(
    not os.environ.get("REMEDY_REAL_OLLAMA_SMOKE"),
    reason="Set REMEDY_REAL_OLLAMA_SMOKE=1 to run real Ollama smoke",
)
class TestRealOllamaSmoke:
    """Real Ollama smoke — requires running server."""

    def test_skip_reason_clear_if_unavailable(self):
        if not _ollama_available():
            pytest.skip("Ollama server not available — skipping real smoke")

    def test_real_ollama_structured_patch_attempt(self, tmp_path, monkeypatch):
        if not _ollama_available():
            pytest.skip("Ollama server not available")

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from uuid import uuid4
        from packages.orchestration.builder_models import TaskExecutionContext
        from packages.providers.ollama_builder.provider import OllamaBuilder

        repo = create_missing_function_repo(tmp_path / "repo")
        builder = OllamaBuilder()
        context = TaskExecutionContext(
            job_id=uuid4(),
            task_id=uuid4(),
            job_prompt="Add a hello() function that returns 'hello'",
            task_type="code_change",
            task_description="Write hello() in app.py that returns the string 'hello'",
        )
        output = builder.build(context)
        assert isinstance(output, BuilderOutput)
        assert output.summary

        # Verify pipeline behavior, not guaranteed model success
        result = parse_builder_patch(output)
        assert result.output_hash != "" or result.error_kind == "no_structured_patch_text"

        # Safe metadata recorded
        if result.parse_success:
            assert len(result.target_paths) > 0
            assert result.patch is not None
        else:
            assert result.error_kind != ""

    def test_real_ollama_no_raw_output_leak(self, tmp_path, monkeypatch):
        if not _ollama_available():
            pytest.skip("Ollama server not available")

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from uuid import uuid4
        from packages.core.models import Job
        from packages.orchestration.builder_bridge import run_builder_bridge
        from packages.orchestration.builder_models import TaskExecutionContext
        from packages.orchestration.timeline import load_run_events
        from packages.providers.ollama_builder.provider import OllamaBuilder

        repo = create_missing_function_repo(tmp_path / "repo")
        builder = OllamaBuilder()
        context = TaskExecutionContext(
            job_id=uuid4(),
            task_id=uuid4(),
            job_prompt="Add a hello() function",
            task_type="code_change",
            task_description="Write hello() in app.py",
        )
        output = builder.build(context)

        job = Job(name="ollama-smoke")
        result = run_builder_bridge(
            output, repo, job=job, data_dir=tmp_path / "data",
            autonomy_level=3,
        )

        # No raw provider output in events
        events = load_run_events(tmp_path / "data", job.id)
        for event in events:
            meta_str = str(event.get("metadata", {}))
            assert "def hello" not in meta_str
