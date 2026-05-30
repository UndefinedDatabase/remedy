"""Tests for Steps 64-65 — Worker Adapter Contract v1 & Git Safety Readiness v1."""

from __future__ import annotations

import json
import subprocess
import sys
from uuid import uuid4

import pytest

from packages.core.models import Job, RunState, Task


# ── Step 64: Worker Adapter Contract ─────────────────────────────────────


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


class TestGitStatusReader:
    def test_read_current_repo(self):
        from packages.orchestration.git_status import read_git_status

        status = read_git_status(".")
        assert status.is_git_repo is True
        assert len(status.current_branch) > 0
        assert len(status.head_sha) > 0

    def test_read_nonexistent_dir(self):
        from packages.orchestration.git_status import read_git_status

        status = read_git_status("/tmp/nonexistent_dir_xyz_12345")
        assert status.is_git_repo is False
        assert "not a directory" in status.error

    def test_read_non_git_dir(self, tmp_path):
        from packages.orchestration.git_status import read_git_status

        status = read_git_status(str(tmp_path))
        assert status.is_git_repo is False

    def test_read_git_repo_with_untracked(self, tmp_path):
        from packages.orchestration.git_status import read_git_status

        # Create a git repo with an untracked file
        subprocess.run(["git", "init", str(tmp_path)], capture_output=True)
        subprocess.run(
            ["git", "-C", str(tmp_path), "config", "user.email", "test@test.com"],
            capture_output=True,
        )
        subprocess.run(
            ["git", "-C", str(tmp_path), "config", "user.name", "Test"],
            capture_output=True,
        )
        # Need at least one commit for HEAD to exist
        (tmp_path / "README.md").write_text("hello")
        subprocess.run(["git", "-C", str(tmp_path), "add", "."], capture_output=True)
        subprocess.run(
            ["git", "-C", str(tmp_path), "commit", "-m", "init"],
            capture_output=True,
        )
        # Add untracked file
        (tmp_path / "untracked.txt").write_text("x")

        status = read_git_status(str(tmp_path))
        assert status.is_git_repo is True
        assert status.is_clean is False
        assert "untracked.txt" in status.untracked_files

    def test_export_json(self):
        from packages.orchestration.git_status import (
            export_git_status_json,
            read_git_status,
        )

        status = read_git_status(".")
        data = export_git_status_json(status)
        assert data["version"] == 1
        assert data["is_git_repo"] is True
        assert isinstance(data["modified_files"], list)

    def test_summarize(self):
        from packages.orchestration.git_status import (
            read_git_status,
            summarize_git_status,
        )

        status = read_git_status(".")
        text = summarize_git_status(status)
        assert "Branch:" in text

    def test_no_shell_true(self):
        """Verify _run_git never uses shell=True."""
        import ast

        with open("packages/orchestration/git_status.py") as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.keyword) and node.arg == "shell":
                if isinstance(node.value, ast.Constant) and node.value.value is True:
                    pytest.fail("shell=True found in git_status.py")


class TestGitStatusCLI:
    def test_repo_status_help(self):
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", "repo", "status", "--help"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0
        assert "status" in result.stdout.lower()

    def test_repo_status_json(self):
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", "repo", "status", "--json"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["version"] == 1
        assert data["is_git_repo"] is True


class TestGitStatusBrainNode:
    def test_git_status_node_in_graph(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import build_project_brain
        from packages.orchestration.storage import save_job

        job = Job(
            id=uuid4(), name="brain-git", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
            metadata={"target_repo": "."},
        )
        save_job(job)
        graph = build_project_brain(job, [])
        git_nodes = [n for n in graph.nodes if n.type == "git_status"]
        assert len(git_nodes) == 1
        meta = git_nodes[0].metadata
        assert "current_branch" in meta
        assert "is_clean" in meta
        assert "head_sha" in meta

    def test_git_status_node_no_repo(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import build_project_brain
        from packages.orchestration.storage import save_job

        job = Job(
            id=uuid4(), name="brain-no-git", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
        )
        save_job(job)
        graph = build_project_brain(job, [])
        git_nodes = [n for n in graph.nodes if n.type == "git_status"]
        # No target_repo → no git_status node
        assert len(git_nodes) == 0


class TestGitReadinessSignal:
    def test_signal_present(self):
        from packages.orchestration.autonomy_readiness import _collect_signals

        job = Job(
            id=uuid4(), name="sig-test", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
        )
        signals = _collect_signals(job, [])
        assert "git_status" in signals
        assert signals["git_status"] is False

    def test_signal_true_with_event(self):
        from packages.orchestration.autonomy_readiness import _collect_signals

        job = Job(
            id=uuid4(), name="sig-test", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
        )
        events = [{"event": "git_status_read", "metadata": {}}]
        signals = _collect_signals(job, events)
        assert signals["git_status"] is True


class TestContextPackMemory:
    def test_approved_only(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import store_memory
        from packages.orchestration.context_pack import build_context_pack

        job = Job(
            id=uuid4(), name="ctx-mem", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
        )
        # Store globally (context pack reads global scope)
        store_memory("approved.key", "val1", approved=True)
        store_memory("unapproved.key", "val2", approved=False)

        pack = build_context_pack(job, [], budget=5000, mode="compact")
        mem_section = next((s for s in pack.sections if s.name == "memory_keys"), None)
        assert mem_section is not None
        assert "approved.key" in mem_section.content
        assert "unapproved.key" not in mem_section.content

    def test_caveman_mode_count(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import store_memory
        from packages.orchestration.context_pack import build_context_pack

        job = Job(
            id=uuid4(), name="ctx-cave", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
        )
        store_memory("k1", "v1", approved=True)
        pack = build_context_pack(job, [], budget=5000, mode="caveman")
        mem_section = next((s for s in pack.sections if s.name == "memory_keys"), None)
        assert mem_section is not None
        assert "mem:" in mem_section.content

    def test_no_raw_values_in_pack(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import store_memory
        from packages.orchestration.context_pack import build_context_pack

        job = Job(
            id=uuid4(), name="ctx-raw", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
        )
        store_memory("secret.key", "SECRET_RAW_VALUE_12345", approved=True)
        pack = build_context_pack(job, [], budget=5000, mode="compact")
        mem_section = next((s for s in pack.sections if s.name == "memory_keys"), None)
        assert mem_section is not None
        assert "SECRET_RAW_VALUE_12345" not in mem_section.content
