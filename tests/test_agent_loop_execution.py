"""Tests for agent loop execution (Step 46).

Tests: run_agent_loop, job.run-loop CLI, run-log events.
"""

from __future__ import annotations

import json
import subprocess
import sys
from uuid import uuid4

from packages.core.models import Job, RunState, Task
from packages.orchestration.agent_loop import (
    AgentLoopDecision,
    AgentLoopStage,
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
        runs_dir = tmp_path / "job_logs" / str(job.id)
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

        runs_dir = tmp_path / "job_logs" / str(job.id)
        events = []
        for lf in runs_dir.glob("*.jsonl"):
            for line in lf.read_text().splitlines():
                if line.strip():
                    events.append(json.loads(line))
        event_types = [e["event"] for e in events]
        assert "agent_loop_cycle_started" in event_types


REQUIRED_META_KEYS = frozenset({
    "cycle", "max_cycles", "decision", "stage", "reason",
    "task_count", "pending_task_count", "pending_approval_count",
    "applied_count", "test_run_count",
})


class TestAgentLoopEventSchema:
    """Every agent_loop_* event must have the exact 11-key metadata schema."""

    def _collect_events(self, tmp_path, job_id):
        runs_dir = tmp_path / "job_logs" / str(job_id)
        events = []
        if runs_dir.exists():
            for lf in runs_dir.glob("*.jsonl"):
                for line in lf.read_text().splitlines():
                    if line.strip():
                        events.append(json.loads(line))
        return events

    def test_completed_job_exact_schema(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = Job(
            id=uuid4(), name="done", user_prompt="done",
            tasks=[Task(description="t", status=RunState.COMPLETED)],
        )
        save_job(job)
        run_agent_loop(job, max_cycles=1)
        events = self._collect_events(tmp_path, job.id)
        loop_events = [e for e in events if e["event"].startswith("agent_loop_")]
        assert len(loop_events) >= 2  # started + completed at minimum
        for ev in loop_events:
            meta = ev.get("metadata", {})
            got = frozenset(meta.keys())
            assert got == REQUIRED_META_KEYS, (
                f"Event {ev['event']} has wrong keys: "
                f"extra={got - REQUIRED_META_KEYS}, missing={REQUIRED_META_KEYS - got}"
            )

    def test_no_generic_cycle_events(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        run_agent_loop(job, max_cycles=1)
        events = self._collect_events(tmp_path, job.id)
        event_names = [e["event"] for e in events]
        assert "cycle_started" not in event_names
        assert "cycle_completed" not in event_names
        assert "agent_loop_task_exit" not in event_names

    def test_empty_job_logs_started_and_completed(self, tmp_path, monkeypatch):
        """No-op completed job logs agent_loop_started + agent_loop_completed."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = Job(
            id=uuid4(), name="done", user_prompt="done",
            tasks=[Task(description="t", status=RunState.COMPLETED)],
        )
        save_job(job)
        run_agent_loop(job, max_cycles=1)
        events = self._collect_events(tmp_path, job.id)
        event_names = [e["event"] for e in events]
        assert "agent_loop_started" in event_names
        assert "agent_loop_completed" in event_names

    def test_no_raw_output_leak(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        run_agent_loop(job, max_cycles=1)
        events = self._collect_events(tmp_path, job.id)
        full = json.dumps(events)
        for forbidden in ("stdout", "stderr", "raw_output", "command_output",
                          "Traceback", "diff_preview", "approval_reason"):
            assert forbidden not in full, f"Forbidden string in events: {forbidden}"


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
            metadata={"target_repo": "."},
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
