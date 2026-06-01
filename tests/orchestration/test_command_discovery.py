"""
Domain tests: orchestration/test_command_discovery.py
Migrated from step-numbered test files.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch
from uuid import uuid4
import json
import os
import pytest
import subprocess
import sys
import tempfile

from packages.core.models import Job, RunState, Task

_ROOT = Path(__file__).resolve().parent.parent.parent


def _make_job(*, tasks=None, name="test"):
    from packages.core.models import Job, Task, RunState
    job = Job(name=name)
    if tasks:
        for t in tasks:
            task = Task(
                task_type=t.get("type", "readme_draft"),
                description=t.get("description", t.get("type", "task")),
            )
            if "status" in t:
                task.status = RunState(t["status"])
            if "metadata" in t:
                task.inputs = t["metadata"]
            job.tasks.append(task)
    return job


# ═══════════════════════════════════════════════════════════════════════════
# Step 122 — Job-focused Origin Semantics
# ═══════════════════════════════════════════════════════════════════════════


def _make_job_s127(*, tasks=None, name="test"):
    from packages.core.models import Job, Task, RunState
    job = Job(name=name)
    if tasks:
        for t in tasks:
            task = Task(
                task_type=t.get("type", "readme_draft"),
                description=t.get("description", t.get("type", "task")),
            )
            if "status" in t:
                task.status = RunState(t["status"])
            if "metadata" in t:
                task.inputs = t["metadata"]
            job.tasks.append(task)
    return job


# ═══════════════════════════════════════════════════════════════════════════
# Step 127 — Task Progress API Contract Closure
# ═══════════════════════════════════════════════════════════════════════════




class TestWorkerUnloadJsonSchema:
    """Worker unload JSON must have flat stopped/skipped/errors/unavailable."""

    def test_unload_unavailable_schema(self):
        """When ollama not found, schema has unavailable=true."""
        from apps.cli.commands.worker import _cmd_worker_unload
        with patch("shutil.which", return_value=None):
            with patch("builtins.print") as mock_print:
                _cmd_worker_unload(provider="ollama", unload_all=True, json_output=True)
                output = mock_print.call_args[0][0]
                data = json.loads(output)
                assert data["version"] == 1
                assert data["unavailable"] is True
                assert data["attempted"] == 0
                assert data["stopped"] == []
                assert data["skipped"] == []
                assert data["errors"] == []
                assert data["provider"] == "ollama"

    def test_unload_required_fields(self):
        """Unload JSON must have all required top-level fields."""
        from apps.cli.commands.worker import _cmd_worker_unload
        with patch("shutil.which", return_value=None):
            with patch("builtins.print") as mock_print:
                _cmd_worker_unload(provider="ollama", unload_all=True, json_output=True)
                data = json.loads(mock_print.call_args[0][0])
                required = {"version", "provider", "attempted", "stopped", "skipped", "errors", "unavailable"}
                missing = required - set(data.keys())
                assert not missing, f"Missing: {missing}"

    def test_unload_stopped_is_list(self):
        """stopped field must be a list of model names."""
        from apps.cli.commands.worker import _cmd_worker_unload
        mock_ps = MagicMock(stdout="NAME\nllama3:8b\n", returncode=0)
        mock_stop = MagicMock(stdout="", stderr="", returncode=0)

        with patch("shutil.which", return_value="/usr/bin/ollama"):
            with patch("subprocess.run", side_effect=[mock_ps, mock_stop]):
                with patch("builtins.print") as mock_print:
                    _cmd_worker_unload(provider="ollama", unload_all=True, json_output=True)
                    data = json.loads(mock_print.call_args[0][0])
                    assert isinstance(data["stopped"], list)
                    assert "llama3:8b" in data["stopped"]
                    assert data["unavailable"] is False

    def test_unload_errors_populated_on_failure(self):
        """errors list should contain model names that failed to stop."""
        from apps.cli.commands.worker import _cmd_worker_unload
        mock_ps = MagicMock(stdout="NAME\nbad-model\n", returncode=0)
        mock_stop = MagicMock(stdout="", stderr="model not found", returncode=1)

        with patch("shutil.which", return_value="/usr/bin/ollama"):
            with patch("subprocess.run", side_effect=[mock_ps, mock_stop]):
                with patch("builtins.print") as mock_print:
                    _cmd_worker_unload(provider="ollama", unload_all=True, json_output=True)
                    data = json.loads(mock_print.call_args[0][0])
                    assert "bad-model" in data["errors"]
                    assert data["stopped"] == []


# ═══════════════════════════════════════════════════════════════════════════
# Step 125 — Autocoder calc.py Fixture + --no-ui
# ═══════════════════════════════════════════════════════════════════════════




class TestWorkerUnloadExactSchemaEdgeCases:
    """Worker unload must have exact schema and handle all edge cases."""

    def test_unload_exact_schema(self):
        from apps.cli.commands.worker import _cmd_worker_unload
        with patch("shutil.which", return_value=None):
            with patch("builtins.print") as mock_print:
                _cmd_worker_unload(provider="ollama", unload_all=True, json_output=True)
                data = json.loads(mock_print.call_args[0][0])
                assert set(data.keys()) == {
                    "version", "provider", "attempted",
                    "stopped", "skipped", "errors", "unavailable",
                }

    def test_missing_ollama_exit_0(self):
        """Missing ollama should not crash — exits normally."""
        from apps.cli.commands.worker import _cmd_worker_unload
        with patch("shutil.which", return_value=None):
            with patch("builtins.print"):
                # Should not raise
                _cmd_worker_unload(provider="ollama", unload_all=True, json_output=True)

    def test_errors_includes_silent_failures(self):
        """Models with returncode!=0 and empty stderr still in errors list."""
        from apps.cli.commands.worker import _cmd_worker_unload
        mock_ps = MagicMock(stdout="NAME\nsilent-fail\n", returncode=0)
        mock_stop = MagicMock(stdout="", stderr="", returncode=1)

        with patch("shutil.which", return_value="/usr/bin/ollama"):
            with patch("subprocess.run", side_effect=[mock_ps, mock_stop]):
                with patch("builtins.print") as mock_print:
                    _cmd_worker_unload(provider="ollama", unload_all=True, json_output=True)
                    data = json.loads(mock_print.call_args[0][0])
                    assert "silent-fail" in data["errors"]

    def test_no_shell_true(self):
        src = Path("apps/cli/commands/worker.py").read_text()
        for line in src.splitlines():
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith('"""'):
                continue
            assert "shell=True" not in stripped

    def test_smoke_has_unload_section(self):
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "REMEDY_SMOKE_UNLOAD_MODELS" in content

    def test_resources_missing_nvidia_smi(self):
        """Missing nvidia-smi should not crash resources command."""
        from apps.cli.commands.worker import _cmd_worker_resources
        with patch("shutil.which", return_value=None):
            with patch("builtins.print"):
                _cmd_worker_resources(json_output=True)


# ═══════════════════════════════════════════════════════════════════════════
# Step 131 — UX Visual Contract Stabilization
# ═══════════════════════════════════════════════════════════════════════════




class TestWorkerShow:
    def test_show_known_provider(self):
        from packages.orchestration.worker_adapters import list_worker_specs

        specs = list_worker_specs()
        assert any(s.provider_id == "ollama" for s in specs)

    def test_show_cli_help(self):
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", "worker", "show", "--help"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0
        assert "provider_id" in result.stdout.lower()

    def test_show_cli_ollama(self):
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", "worker", "show", "ollama"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0
        assert "Ollama" in result.stdout

    def test_show_cli_unknown(self):
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", "worker", "show", "nonexistent"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode != 0
        assert "unknown provider" in result.stderr.lower()




class TestWorkerExplain:
    def test_explain_cli_help(self):
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", "worker", "explain", "--help"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0
        assert "job_id" in result.stdout.lower()

    def test_explain_produces_scoring(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.storage import save_job
        from packages.orchestration.worker_recommend import recommend_worker

        job = Job(
            id=uuid4(), name="explain-test", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
        )
        save_job(job)
        rec = recommend_worker(job, [])
        assert rec.recommended_worker == "ollama"
        assert len(rec.candidates) >= 3
        # ollama should score highest (local + available)
        assert rec.candidates[0].provider_id == "ollama"
        assert rec.candidates[0].score > rec.candidates[-1].score




class TestWorkerBrainNode:
    def test_worker_adapter_node_in_graph(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import build_project_brain
        from packages.orchestration.storage import save_job

        job = Job(
            id=uuid4(), name="brain-wa", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
        )
        save_job(job)
        graph = build_project_brain(job, [])
        wa_nodes = [n for n in graph.nodes if n.type == "worker_adapter"]
        assert len(wa_nodes) >= 1
        assert any(n.id == "worker_adapter:ollama" for n in wa_nodes)


# ── Step 65: Git Safety Readiness ────────────────────────────────────────

