"""Tests for packages/memory/local_gateway.py and memory CLI commands."""

from __future__ import annotations

import json
import subprocess
import sys

import pytest

from packages.memory.local_gateway import (
    LocalMemoryGateway,
    MemoryRedactionError,
    delete_memory,
    has_approved_memory,
    list_memory,
    recall_memory,
    store_memory,
)
from packages.memory.models import MemoryEntry


class TestMemoryEntry:
    def test_round_trip(self) -> None:
        entry = MemoryEntry(key="test_key", value="test_value", tags=["a", "b"])
        line = entry.to_json_line()
        parsed = json.loads(line)
        restored = MemoryEntry.from_dict(parsed)
        assert restored.key == "test_key"
        assert restored.value == "test_value"
        assert restored.tags == ["a", "b"]
        assert restored.id == entry.id

    def test_defaults(self) -> None:
        entry = MemoryEntry()
        assert entry.version == 1
        assert entry.approved is False
        assert entry.redaction_policy == "redact_secrets"
        assert entry.confidence_source == "human_explicit"


class TestStoreAndRecall:
    def test_store_and_recall(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        entry = store_memory("greeting", "hello world", project_id="proj1")
        assert entry.key == "greeting"

        results = recall_memory(project_id="proj1")
        assert len(results) == 1
        assert results[0].key == "greeting"
        assert results[0].value == "hello world"

    def test_recall_with_keyword(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        store_memory("api_url", "https://example.com", project_id="proj2")
        store_memory("db_host", "localhost", project_id="proj2")

        results = recall_memory(project_id="proj2", keyword="api")
        assert len(results) == 1
        assert results[0].key == "api_url"

    def test_recall_max_results(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        for i in range(10):
            store_memory(f"key_{i}", f"value_{i}", project_id="proj3")

        results = recall_memory(project_id="proj3", max_results=3)
        assert len(results) == 3

    def test_recall_newest_first(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        store_memory("old", "old_val", project_id="proj4")
        store_memory("new", "new_val", project_id="proj4")

        results = recall_memory(project_id="proj4")
        assert results[0].key == "new"

    def test_recall_tag_match(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        store_memory("tagged", "val", project_id="proj5", tags=["important"])
        store_memory("untagged", "val2", project_id="proj5")

        results = recall_memory(project_id="proj5", keyword="important")
        assert len(results) == 1
        assert results[0].key == "tagged"


class TestListMemory:
    def test_list_empty(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        results = list_memory(project_id="empty_proj")
        assert results == []

    def test_list_all(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        store_memory("a", "1", project_id="proj6")
        store_memory("b", "2", project_id="proj6")

        results = list_memory(project_id="proj6")
        assert len(results) == 2


class TestDeleteMemory:
    def test_delete(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        entry = store_memory("to_delete", "val", project_id="proj7")
        assert delete_memory(str(entry.id), project_id="proj7") is True
        assert list_memory(project_id="proj7") == []

    def test_delete_nonexistent(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        assert delete_memory("nonexistent-id", project_id="proj8") is False


class TestHasApprovedMemory:
    def test_no_approved(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        store_memory("key", "val", project_id="proj9")
        assert has_approved_memory(project_id="proj9") is False

    def test_with_approved(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        store_memory("key", "val", project_id="proj10", approved=True)
        assert has_approved_memory(project_id="proj10") is True


class TestLocalMemoryGateway:
    def test_write_and_read(self, tmp_path, monkeypatch) -> None:
        import asyncio
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        gw = LocalMemoryGateway(project_id="gw_proj")
        asyncio.run(gw.write("test_key", "test_value"))
        result = asyncio.run(gw.read("test_key"))
        assert result == "test_value"

    def test_read_missing(self, tmp_path, monkeypatch) -> None:
        import asyncio
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        gw = LocalMemoryGateway(project_id="gw_proj2")
        result = asyncio.run(gw.read("nonexistent"))
        assert result is None

    def test_delete(self, tmp_path, monkeypatch) -> None:
        import asyncio
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        gw = LocalMemoryGateway(project_id="gw_proj3")
        asyncio.run(gw.write("to_del", "val"))
        asyncio.run(gw.delete("to_del"))
        result = asyncio.run(gw.read("to_del"))
        assert result is None


class TestUnscopedMemory:
    def test_job_scoped(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        store_memory("jk", "jv", job_id="job-123")
        results = recall_memory(job_id="job-123")
        assert len(results) == 1
        assert results[0].key == "jk"

    def test_global_scope(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        store_memory("gk", "gv")
        results = recall_memory()
        assert len(results) == 1
        assert results[0].key == "gk"


class TestMemoryCLI:
    def _run(self, argv: list[str]) -> tuple[str, str, int]:
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped"] + argv,
            capture_output=True, text=True, timeout=30,
        )
        return result.stdout, result.stderr, result.returncode

    def test_memory_group_help(self) -> None:
        stdout, _, rc = self._run(["memory"])
        assert rc == 0
        assert "store" in stdout
        assert "recall" in stdout
        assert "list" in stdout

    def test_memory_store_and_list(self, tmp_path, monkeypatch) -> None:
        env = {"REMEDY_DATA_DIR": str(tmp_path)}
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", "memory", "store", "test_k", "test_v"],
            capture_output=True, text=True, timeout=30,
            env={**subprocess.os.environ, **env},
        )
        assert result.returncode == 0
        assert "Stored:" in result.stdout

        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", "memory", "list", "--json"],
            capture_output=True, text=True, timeout=30,
            env={**subprocess.os.environ, **env},
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["count"] >= 1

    def test_memory_recall_json(self, tmp_path, monkeypatch) -> None:
        env = {"REMEDY_DATA_DIR": str(tmp_path)}
        subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", "memory", "store", "rk", "rv"],
            capture_output=True, text=True, timeout=30,
            env={**subprocess.os.environ, **env},
        )
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", "memory", "recall", "--keyword", "rk", "--json"],
            capture_output=True, text=True, timeout=30,
            env={**subprocess.os.environ, **env},
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["count"] >= 1


class TestContextCoverageMemorySignal:
    def test_project_memory_present_with_approved_entries(self, tmp_path, monkeypatch) -> None:
        from uuid import uuid4
        from packages.core.models import Job
        from packages.orchestration.context_coverage import derive_context_coverage

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = Job(name="test", user_prompt="test")
        job.metadata["project_id"] = "test_proj_cc"

        # Without approved memory
        snapshot = derive_context_coverage(job, [])
        pm_signal = next(s for s in snapshot.signals if s.key == "project_memory")
        assert pm_signal.present is False

        # With approved memory
        store_memory("k", "v", project_id="test_proj_cc", approved=True)
        snapshot = derive_context_coverage(job, [])
        pm_signal = next(s for s in snapshot.signals if s.key == "project_memory")
        assert pm_signal.present is True


class TestMemoryRedactionBlocklist:
    """R-0031: store_memory() must reject forbidden patterns and keys."""

    @pytest.mark.parametrize("pattern", [
        "sk-abc123secret",
        "ghp_abcdefgh",
        "xoxb-tokenvalue",
        "-----BEGIN PRIVATE KEY-----",
        "db_password=hunter2",
        "api_key=abcdefg",
        "secret=mysecret",
        "Traceback (most recent call last)",
    ])
    def test_rejects_forbidden_value_patterns(self, tmp_path, monkeypatch, pattern) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        with pytest.raises(MemoryRedactionError, match="forbidden pattern"):
            store_memory("some_key", f"prefix {pattern} suffix", project_id="proj")

    @pytest.mark.parametrize("key", [
        "artifact.content",
        "raw_stdout",
        "raw_stderr",
        "diff_preview",
        "command_output",
    ])
    def test_rejects_forbidden_keys(self, tmp_path, monkeypatch, key) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        with pytest.raises(MemoryRedactionError, match="Forbidden memory key"):
            store_memory(key, "safe value", project_id="proj")

    def test_allows_safe_content(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        entry = store_memory("architecture", "uses hexagonal pattern", project_id="proj")
        assert entry.key == "architecture"

    def test_forbidden_key_case_insensitive(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        with pytest.raises(MemoryRedactionError):
            store_memory("Raw_Stdout", "safe value", project_id="proj")
