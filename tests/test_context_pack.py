"""Tests for context pack v0 (Step 49)."""

from __future__ import annotations

import json
import subprocess
import sys
from uuid import uuid4

from packages.core.models import Job, RunState, Task
from packages.orchestration.context_pack import (
    build_context_pack,
    export_context_pack_json,
    summarize_context_pack,
)


def _make_job(**extra_meta) -> Job:
    return Job(
        id=uuid4(),
        name="pack-test",
        user_prompt="test context pack",
        tasks=[Task(description="t", status=RunState.PENDING)],
        metadata=extra_meta,
    )


class TestContextPackBasic:
    def test_compact_mode(self):
        job = _make_job()
        pack = build_context_pack(job, [], budget=2000, mode="compact")
        assert pack.version == 1
        assert pack.mode == "compact"
        assert len(pack.sections) > 0

    def test_caveman_mode(self):
        job = _make_job()
        pack = build_context_pack(job, [], budget=2000, mode="caveman")
        assert pack.mode == "caveman"
        assert len(pack.sections) > 0

    def test_caveman_shorter_than_compact(self):
        job = _make_job()
        compact = build_context_pack(job, [], budget=5000, mode="compact")
        caveman = build_context_pack(job, [], budget=5000, mode="caveman")
        assert caveman.estimated_tokens <= compact.estimated_tokens

    def test_budget_enforced(self):
        job = _make_job()
        pack = build_context_pack(job, [], budget=10, mode="compact")
        assert pack.estimated_tokens <= 10 or pack.truncated is True

    def test_tiny_budget_truncates(self):
        job = _make_job()
        pack = build_context_pack(job, [], budget=1, mode="compact")
        assert pack.truncated is True

    def test_large_budget_not_truncated(self):
        job = _make_job()
        pack = build_context_pack(job, [], budget=50000, mode="compact")
        assert pack.truncated is False

    def test_sections_have_priority(self):
        job = _make_job()
        pack = build_context_pack(job, [], budget=5000, mode="compact")
        priorities = [s.priority for s in pack.sections]
        assert priorities == sorted(priorities)


class TestContextPackJSON:
    def test_json_schema(self):
        job = _make_job()
        pack = build_context_pack(job, [], budget=2000, mode="compact")
        data = export_context_pack_json(pack)
        assert data["version"] == 1
        assert "job_id" in data
        assert "mode" in data
        assert "budget" in data
        assert "estimated_tokens" in data
        assert "truncated" in data
        assert "sections" in data

    def test_section_schema(self):
        job = _make_job()
        pack = build_context_pack(job, [], budget=5000, mode="compact")
        data = export_context_pack_json(pack)
        for s in data["sections"]:
            assert "name" in s
            assert "priority" in s
            assert "content" in s
            assert "estimated_tokens" in s

    def test_no_raw_leak(self):
        job = _make_job()
        pack = build_context_pack(job, [], budget=5000, mode="compact")
        full = json.dumps(export_context_pack_json(pack))
        for forbidden in ("raw_output", "command_output",
                          "Traceback", "diff_preview", "approval_reason"):
            assert forbidden not in full

    def test_json_is_pure(self):
        job = _make_job()
        pack = build_context_pack(job, [], budget=2000, mode="compact")
        raw = json.dumps(export_context_pack_json(pack))
        json.loads(raw)


class TestContextPackText:
    def test_summarize_mentions_mode(self):
        job = _make_job()
        pack = build_context_pack(job, [], budget=2000, mode="compact")
        text = summarize_context_pack(pack)
        assert "compact" in text

    def test_summarize_truncated_note(self):
        job = _make_job()
        pack = build_context_pack(job, [], budget=1, mode="compact")
        text = summarize_context_pack(pack)
        assert "TRUNCATED" in text


class TestContextPackCLI:
    def _run(self, argv):
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped"] + argv,
            capture_output=True, text=True, timeout=30,
        )
        return result.stdout, result.stderr, result.returncode

    def test_pack_help(self):
        stdout, _, rc = self._run(["context", "pack", "--help"])
        assert rc == 0
        assert "job_id" in stdout.lower()

    def test_pack_json_output(self, tmp_path, monkeypatch):
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
             "context", "pack", str(job.id), "--json"],
            capture_output=True, text=True, timeout=30, env=env,
        )
        assert result.returncode == 0, f"stderr={result.stderr}"
        data = json.loads(result.stdout)
        assert data["version"] == 1
        assert "sections" in data

    def test_pack_caveman_json(self, tmp_path, monkeypatch):
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
             "context", "pack", str(job.id), "--mode", "caveman", "--json"],
            capture_output=True, text=True, timeout=30, env=env,
        )
        assert result.returncode == 0, f"stderr={result.stderr}"
        data = json.loads(result.stdout)
        assert data["mode"] == "caveman"
