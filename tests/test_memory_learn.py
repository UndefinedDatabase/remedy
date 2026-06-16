"""Tests for memory learn v0 (Step 50)."""

from __future__ import annotations

import json
import subprocess
import sys
from uuid import uuid4

from packages.core.models import Job, RunState, Task
from packages.orchestration.memory_learn import export_learn_json, learn_from_job


def _make_job(**extra_meta) -> Job:
    return Job(
        id=uuid4(),
        name="learn-test",
        user_prompt="test learn",
        tasks=[Task(description="t", status=RunState.PENDING)],
        metadata=extra_meta,
    )


class TestLearnBasic:
    def test_learn_empty_events(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        result = learn_from_job(job, [])
        assert result.version == 1
        assert result.learned_count >= 0
        assert result.skipped_count >= 0

    def test_learn_creates_entries_from_test_run(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        events = [
            {"event": "test_run_completed", "metadata": {
                "command": "make test", "status": "passed",
                "exit_code": 0, "duration_ms": 500,
            }},
        ]
        result = learn_from_job(job, events)
        assert result.learned_count >= 2  # test_command + last_verified

    def test_learn_creates_entries_from_apply_proof(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        events = [
            {"event": "patch_apply_proof_recorded", "metadata": {
                "target_path": "README.md",
                "after_sha256": "a" * 64,
            }},
        ]
        result = learn_from_job(job, events)
        found = [e for e in result.entries if e["key"] == "patch.last_applied_target"]
        assert len(found) == 1
        assert found[0]["value"] == "README.md"

    def test_learn_idempotent(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        events = [
            {"event": "test_run_completed", "metadata": {
                "command": "make test", "status": "passed",
            }},
        ]
        r1 = learn_from_job(job, events)
        r2 = learn_from_job(job, events)
        # Second run should skip (update, not create)
        assert r2.learned_count == 0
        assert r2.skipped_count >= r1.learned_count

    def test_learn_no_duplicate_explosion(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        events = [
            {"event": "test_run_completed", "metadata": {
                "command": "make test", "status": "passed",
            }},
        ]
        for _ in range(5):
            learn_from_job(job, events)
        from packages.memory.local_gateway import list_memory
        entries = list_memory(job_id=str(job.id))
        keys = [e.key for e in entries if e.key == "repo.test_command.primary"]
        assert len(keys) == 1

    def test_learn_repo_basename(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job(target_repo="/tmp/my-repo")
        result = learn_from_job(job, [])
        found = [e for e in result.entries if e["key"] == "repo.basename"]
        assert len(found) == 1
        assert found[0]["value"] == "my-repo"


class TestLearnJSON:
    def test_export_schema(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        result = learn_from_job(job, [])
        data = export_learn_json(result)
        assert data["version"] == 1
        assert "job_id" in data
        assert "learned_count" in data
        assert "skipped_count" in data
        assert "entries" in data

    def test_no_raw_leak(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        result = learn_from_job(job, [])
        full = json.dumps(export_learn_json(result))
        for forbidden in ("raw_output", "command_output", "Traceback",
                          "diff_preview", "approval_reason"):
            assert forbidden not in full


class TestLearnCLI:
    def _run(self, argv):
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped"] + argv,
            capture_output=True, text=True, timeout=30,
        )
        return result.stdout, result.stderr, result.returncode

    def test_learn_help(self):
        stdout, _, rc = self._run(["memory", "learn", "--help"])
        assert rc == 0
        assert "job_id" in stdout.lower()

    def test_learn_json_output(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        import packages.orchestration.storage as _storage
        monkeypatch.setattr(_storage, "_DATA_DIR", tmp_path / "jobs")
        from packages.orchestration.storage import save_job
        job = Job(
            id=uuid4(), name="done", user_prompt="done",
            tasks=[Task(description="t", status=RunState.COMPLETED)],
        )
        save_job(job)
        import os
        env = {**os.environ, "REMEDY_DATA_DIR": str(tmp_path)}
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped",
             "memory", "learn", str(job.id), "--json"],
            capture_output=True, text=True, timeout=30, env=env,
        )
        assert result.returncode == 0, f"stderr={result.stderr}"
        data = json.loads(result.stdout)
        assert data["version"] == 1

    def test_learn_approved_flag(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        import packages.orchestration.storage as _storage
        monkeypatch.setattr(_storage, "_DATA_DIR", tmp_path / "jobs")
        from packages.orchestration.storage import save_job
        job = Job(
            id=uuid4(), name="done", user_prompt="done",
            tasks=[Task(description="t", status=RunState.COMPLETED)],
            metadata={"target_repo": "/tmp/test"},
        )
        save_job(job)
        import os
        env = {**os.environ, "REMEDY_DATA_DIR": str(tmp_path)}
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped",
             "memory", "learn", str(job.id), "--approved", "--json"],
            capture_output=True, text=True, timeout=30, env=env,
        )
        assert result.returncode == 0, f"stderr={result.stderr}"
        data = json.loads(result.stdout)
        assert data["learned_count"] >= 1

    def test_learn_improves_context_coverage(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.storage import save_job
        job = Job(
            id=uuid4(), name="done", user_prompt="done",
            tasks=[Task(description="t", status=RunState.COMPLETED)],
            metadata={"target_repo": "/tmp/test"},
        )
        save_job(job)
        # Learn with approved=True so memory appears
        learn_from_job(job, [], approved=True)
        from packages.memory.local_gateway import has_approved_memory
        assert has_approved_memory(job_id=str(job.id)) is True


class TestUpsertMemory:
    def test_upsert_creates(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import upsert_memory
        entry, created = upsert_memory("k1", "v1", source_id="src1")
        assert created is True
        assert entry.key == "k1"

    def test_upsert_updates(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import upsert_memory
        upsert_memory("k1", "v1", source_id="src1")
        entry, created = upsert_memory("k1", "v2", source_id="src1")
        assert created is False
        assert entry.value == "v2"

    def test_upsert_different_source_creates(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import upsert_memory
        upsert_memory("k1", "v1", source_id="src1")
        entry, created = upsert_memory("k1", "v2", source_id="src2")
        assert created is True
