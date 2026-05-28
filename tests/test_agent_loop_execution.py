"""Tests for agent loop execution (Step 46).

Tests: run_agent_loop, job.run-loop CLI, run-log events.
"""

from __future__ import annotations

import json
import subprocess
import sys
from uuid import uuid4

import pytest

from packages.core.models import Job, RunState, Task
from packages.orchestration.agent_loop import (
    AgentLoopDecision,
    AgentLoopStage,
    derive_agent_loop_state,
    run_agent_loop,
)
from packages.orchestration.storage import save_job


def _make_job() -> Job:
    return Job(
        id=uuid4(),
        name="test-loop-job",
        user_prompt="test loop prompt",
    )


def _make_planned_job() -> Job:
    job = Job(
        id=uuid4(),
        name="planned-loop-job",
        user_prompt="test loop prompt",
        state=RunState.PLANNED,
        tasks=[Task(description="task-0", status=RunState.PENDING)],
    )
    return job


class TestRunAgentLoopBasic:
    def test_empty_job_returns_planned(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        state = run_agent_loop(job, max_cycles=1)
        # No tasks → planned stage, loop pauses (needs planning)
        assert state.current_stage == AgentLoopStage.PLANNED

    def test_completed_job_returns_complete(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = Job(
            id=uuid4(),
            name="done-job",
            user_prompt="done",
            tasks=[Task(description="t", status=RunState.COMPLETED)],
        )
        save_job(job)
        state = run_agent_loop(job, max_cycles=3)
        assert state.decision == AgentLoopDecision.COMPLETE

    def test_max_cycles_limit(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        state = run_agent_loop(job, max_cycles=1)
        assert state is not None

    def test_default_no_auto_approve(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        # Default auto_approve_low_risk=False
        state = run_agent_loop(job, max_cycles=1)
        assert state is not None


class TestRunAgentLoopEvents:
    def test_emits_started_event(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        run_agent_loop(job, max_cycles=1)

        # Check run log for agent_loop_started event
        runs_dir = tmp_path / "runs" / str(job.id)
        assert runs_dir.exists()
        log_files = list(runs_dir.glob("*.jsonl"))
        assert log_files
        events = []
        for lf in log_files:
            for line in lf.read_text().splitlines():
                if line.strip():
                    events.append(json.loads(line))
        event_types = [e["event"] for e in events]
        assert "agent_loop_started" in event_types

    def test_emits_cycle_started(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        run_agent_loop(job, max_cycles=1)

        runs_dir = tmp_path / "runs" / str(job.id)
        events = []
        for lf in runs_dir.glob("*.jsonl"):
            for line in lf.read_text().splitlines():
                if line.strip():
                    events.append(json.loads(line))
        event_types = [e["event"] for e in events]
        assert "cycle_started" in event_types


class TestRunLoopCLI:
    def _run(self, argv: list[str], env_extra: dict | None = None) -> tuple[str, str, int]:
        env = {**subprocess.os.environ, **(env_extra or {})}
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped"] + argv,
            capture_output=True, text=True, timeout=30, env=env,
        )
        return result.stdout, result.stderr, result.returncode

    def test_run_loop_help(self) -> None:
        stdout, _, rc = self._run(["job", "run-loop", "--help"])
        assert rc == 0
        assert "job_id" in stdout.lower()

    def test_run_loop_missing_job(self, tmp_path) -> None:
        env = {"REMEDY_DATA_DIR": str(tmp_path)}
        stdout, stderr, rc = self._run(
            ["job", "run-loop", str(uuid4())], env_extra=env,
        )
        assert rc != 0

    def test_run_loop_completed_job(self, tmp_path, monkeypatch) -> None:
        # Must patch _DATA_DIR on storage module — it's cached at import time,
        # so monkeypatch.setenv alone won't redirect save_job.
        import packages.orchestration.storage as _storage
        monkeypatch.setattr(_storage, "_DATA_DIR", tmp_path / "jobs")
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = Job(
            id=uuid4(), name="done", user_prompt="done",
            tasks=[Task(description="t", status=RunState.COMPLETED)],
        )
        save_job(job)
        assert (tmp_path / "jobs" / f"{job.id}.json").exists()
        # Run via subprocess sharing same data dir
        stdout, stderr, rc = self._run(
            ["job", "run-loop", str(job.id)],
            env_extra={"REMEDY_DATA_DIR": str(tmp_path)},
        )
        assert rc == 0, f"stderr={stderr}\nstdout={stdout}"
        assert "complete" in stdout.lower() or "completed" in stdout.lower()


class TestRunLoopGroupedHelp:
    def _run(self, argv: list[str]) -> tuple[str, str, int]:
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped"] + argv,
            capture_output=True, text=True, timeout=30,
        )
        return result.stdout, result.stderr, result.returncode

    def test_job_group_shows_run_loop(self) -> None:
        stdout, _, rc = self._run(["job"])
        assert rc == 0
        assert "run-loop" in stdout
