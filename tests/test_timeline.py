"""
Tests for packages/orchestration/timeline.py and the `remedy timeline` CLI command.

Coverage:
  - load_run_events: missing directory returns []
  - load_run_events: loads multiple JSONL files, sorted by timestamp
  - load_run_events: ignores empty lines
  - load_run_events: ignores malformed JSON lines
  - summarize_timeline: unknown events do not crash
  - summarize_timeline: renders job_created
  - summarize_timeline: renders planning_completed (changed + noop)
  - summarize_timeline: renders planning_failed with detail
  - summarize_timeline: renders permission_denied with capability name
  - summarize_timeline: renders verification_failed with check count
  - summarize_timeline: renders repo_application_completed file path
  - summarize_timeline: renders patch_intent_created risk levels
  - summarize_timeline: renders task_run_noop / no_pending_tasks
  - summarize_timeline: renders no_change distinctly from no_pending_tasks
  - summarize_timeline: interrupted task (no terminal event) does not crash
  - summarize_timeline: empty events renders gracefully
  - summarize_timeline: includes header (job id, state, task counts)
  - summarize_timeline: includes status and next-action sections
  - next action: suggests run-next-task-local when pending tasks exist
  - next action: suggests set-permission when last event is permission_denied
  - next action: flags patch intent risk when medium/high present
  - CLI: prints timeline for a job with run logs
  - CLI: handles missing run logs gracefully (no crash, clear message)
  - CLI: handles invalid job ID
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from uuid import uuid4

import pytest

from packages.core.models import Job, RunState, Task
from packages.orchestration.storage import save_job
from packages.orchestration.timeline import (
    append_run_event,
    load_run_events,
    summarize_timeline,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _ts(offset: int = 0) -> str:
    """ISO timestamp strings ordered by offset for sort testing."""
    return f"2026-05-03T12:{offset:02d}:00+00:00"


def _write_jsonl(path: Path, events: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for ev in events:
            f.write(json.dumps(ev) + "\n")


def _runs_path(data_dir: Path, job_id) -> Path:
    """One job's run-log directory, hand-spelled: ``<data_dir>/job_logs/<job_id>``.

    DECISION F272 D1 moved this log out of ``runs/`` so that ``runs/`` is keyed by
    RUN id and by nothing else. The join stays spelled by hand on purpose — that
    is what keeps these tests an independent observer of ``run_log_dir``.
    """
    return data_dir / "job_logs" / str(job_id)


def _make_job(**kwargs) -> Job:
    defaults: dict = {"name": "Test job", "state": RunState.PENDING}
    defaults.update(kwargs)
    return Job(**defaults)


def _simple_events(job_id_str: str, run_id: str = "run1") -> list[dict[str, Any]]:
    """Minimal event list: job_created + planning_completed."""
    return [
        {
            "event": "job_created",
            "job_id": job_id_str,
            "run_id": run_id,
            "timestamp": _ts(0),
            "outcome": "created",
            "metadata": {},
        },
        {
            "event": "planning_completed",
            "job_id": job_id_str,
            "run_id": run_id,
            "timestamp": _ts(1),
            "outcome": "changed",
            "model": "qwen3",
            "metadata": {"task_count": 2, "elapsed_ms": 4500},
        },
    ]


def _task_run_events(
    job_id_str: str,
    task_id: str,
    run_id: str = "run2",
    *,
    terminal: str = "task_run_completed",
    outcome: str = "pass",
    extra_meta: dict | None = None,
) -> list[dict[str, Any]]:
    """Task run block: started → builder_started → builder_completed → terminal."""
    base_meta = {"task_type": "write_readme"}
    if extra_meta:
        base_meta.update(extra_meta)
    events = [
        {
            "event": "task_run_started",
            "job_id": job_id_str,
            "run_id": run_id,
            "timestamp": _ts(10),
            "task_id": task_id,
            "metadata": {"task_type": "write_readme"},
        },
        {
            "event": "builder_started",
            "job_id": job_id_str,
            "run_id": run_id,
            "timestamp": _ts(11),
            "task_id": task_id,
            "provider": "ollama",
            "role": "builder",
            "model": "qwen3",
            "metadata": {"task_type": "write_readme"},
        },
        {
            "event": "builder_completed",
            "job_id": job_id_str,
            "run_id": run_id,
            "timestamp": _ts(12),
            "task_id": task_id,
            "outcome": "changed",
            "metadata": {"elapsed_ms": 3200},
        },
        {
            "event": terminal,
            "job_id": job_id_str,
            "run_id": run_id,
            "timestamp": _ts(20),
            "task_id": task_id,
            "outcome": outcome,
            "metadata": base_meta,
        },
    ]
    return events


# ---------------------------------------------------------------------------
# load_run_events — unit tests
# ---------------------------------------------------------------------------


class TestLoadRunEvents:
    def test_missing_directory_returns_empty(self, tmp_path):
        result = load_run_events(tmp_path, uuid4())
        assert result == []

    def test_loads_single_jsonl_file(self, tmp_path):
        job_id = uuid4()
        events = _simple_events(str(job_id))
        _write_jsonl(_runs_path(tmp_path, job_id) / "r1.jsonl", events)

        loaded = load_run_events(tmp_path, job_id)
        assert len(loaded) == 2
        assert loaded[0]["event"] == "job_created"
        assert loaded[1]["event"] == "planning_completed"

    def test_loads_multiple_files_sorted_by_timestamp(self, tmp_path):
        job_id = uuid4()
        job_str = str(job_id)
        run_dir = _runs_path(tmp_path, job_id)

        # File b written first with a later timestamp, file a with earlier
        _write_jsonl(run_dir / "b.jsonl", [
            {"event": "planning_completed", "job_id": job_str, "run_id": "r2",
             "timestamp": _ts(5), "metadata": {}},
        ])
        _write_jsonl(run_dir / "a.jsonl", [
            {"event": "job_created", "job_id": job_str, "run_id": "r1",
             "timestamp": _ts(1), "metadata": {}},
        ])

        loaded = load_run_events(tmp_path, job_id)
        assert len(loaded) == 2
        assert loaded[0]["event"] == "job_created"
        assert loaded[1]["event"] == "planning_completed"

    def test_ignores_empty_lines(self, tmp_path):
        job_id = uuid4()
        run_dir = _runs_path(tmp_path, job_id)
        run_dir.mkdir(parents=True, exist_ok=True)
        log = run_dir / "r.jsonl"
        log.write_text(
            '\n{"event":"job_created","job_id":"x","run_id":"r","timestamp":"t","metadata":{}}\n\n',
            encoding="utf-8",
        )
        loaded = load_run_events(tmp_path, job_id)
        assert len(loaded) == 1

    def test_ignores_malformed_json_lines(self, tmp_path):
        job_id = uuid4()
        run_dir = _runs_path(tmp_path, job_id)
        run_dir.mkdir(parents=True, exist_ok=True)
        log = run_dir / "r.jsonl"
        log.write_text(
            'not-valid-json\n'
            '{"event":"job_created","job_id":"x","run_id":"r","timestamp":"t","metadata":{}}\n',
            encoding="utf-8",
        )
        loaded = load_run_events(tmp_path, job_id)
        assert len(loaded) == 1
        assert loaded[0]["event"] == "job_created"

    def test_accepts_uuid_or_str_job_id(self, tmp_path):
        job_id = uuid4()
        events = _simple_events(str(job_id))
        _write_jsonl(_runs_path(tmp_path, job_id) / "r.jsonl", events)

        by_uuid = load_run_events(tmp_path, job_id)
        by_str = load_run_events(tmp_path, str(job_id))
        assert len(by_uuid) == len(by_str) == 2


# ---------------------------------------------------------------------------
# append_run_event — one run per invocation
# ---------------------------------------------------------------------------


class TestOneRunPerInvocation:
    """All events one invocation appends to a job belong to ONE run.

    These tests read the BYTES the writer left rather than asking the writer
    what it did, and they spell the run-log join literally, so they stay an
    independent observer of `data_paths.run_log_dir` (DECISION F260 D6).
    """

    RESUME_EVENTS = [
        "resume_blocked",
        "resume_started",
        "resume_test_started",
        "resume_test_completed",
        "resume_completed",
    ]

    def test_all_events_of_one_invocation_share_one_run(self, tmp_path):
        job_id = uuid4()
        for name in self.RESUME_EVENTS:
            append_run_event(tmp_path, job_id, event=name, metadata={"exit_code": 0})

        job_dir = tmp_path / "job_logs" / str(job_id)
        files = sorted(job_dir.glob("*.jsonl"))
        assert len(files) == 1

        lines = [
            raw for raw in files[0].read_text(encoding="utf-8").splitlines() if raw.strip()
        ]
        assert len(lines) == 5

        run_ids = {json.loads(raw)["run_id"] for raw in lines}
        assert len(run_ids) == 1

    def test_two_jobs_do_not_share_a_run_file(self, tmp_path):
        job_a = uuid4()
        job_b = uuid4()
        append_run_event(tmp_path, job_a, event="resume_started", metadata={})
        append_run_event(tmp_path, job_b, event="resume_started", metadata={})

        dir_a = tmp_path / "job_logs" / str(job_a)
        dir_b = tmp_path / "job_logs" / str(job_b)
        assert dir_a.is_dir()
        assert dir_b.is_dir()
        assert dir_a != dir_b
        assert len(sorted(dir_a.glob("*.jsonl"))) == 1
        assert len(sorted(dir_b.glob("*.jsonl"))) == 1

    def test_events_come_back_in_append_order(self, tmp_path):
        job_id = uuid4()
        for name in self.RESUME_EVENTS:
            append_run_event(tmp_path, job_id, event=name, metadata={"exit_code": 0})

        loaded = load_run_events(tmp_path, job_id)
        assert [ev["event"] for ev in loaded] == self.RESUME_EVENTS


# ---------------------------------------------------------------------------
# summarize_timeline — header and structure
# ---------------------------------------------------------------------------


class TestSummarizeTimelineHeader:
    def test_includes_job_short_id(self):
        job = _make_job()
        out = summarize_timeline(job, [])
        assert str(job.id)[:8] in out

    def test_includes_state(self):
        job = _make_job(state=RunState.COMPLETED)
        out = summarize_timeline(job, [])
        assert "completed" in out

    def test_includes_task_counts(self):
        job = _make_job()
        task = Task(description="t", inputs={"task_type": "write_readme"})
        task.status = RunState.COMPLETED
        job.tasks.append(task)
        out = summarize_timeline(job, [])
        assert "1 completed" in out
        assert "0 pending" in out

    def test_truncates_long_job_name(self):
        long_name = "A" * 80
        job = _make_job(name=long_name)
        out = summarize_timeline(job, [])
        assert "…" in out
        assert "A" * 80 not in out

    def test_empty_events_renders_without_crash(self):
        job = _make_job()
        out = summarize_timeline(job, [])
        assert "No run log events found" in out

    def test_has_status_section(self):
        job = _make_job()
        out = summarize_timeline(job, [])
        assert "Current status" in out

    def test_has_next_action_section(self):
        job = _make_job()
        out = summarize_timeline(job, [])
        assert "Next suggested action" in out


# ---------------------------------------------------------------------------
# summarize_timeline — individual event rendering
# ---------------------------------------------------------------------------


class TestRenderJobCreated:
    def test_job_created_renders_ok(self):
        job = _make_job()
        events = [{"event": "job_created", "job_id": str(job.id), "run_id": "r",
                   "timestamp": _ts(0), "outcome": "created", "metadata": {}}]
        out = summarize_timeline(job, events)
        assert "Job created" in out


class TestRenderPlanningEvents:
    def test_planning_completed_changed(self):
        job = _make_job()
        events = [
            {"event": "planning_started", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "metadata": {}},
            {"event": "planning_completed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(1), "outcome": "changed", "model": "qwen3",
             "metadata": {"task_count": 3, "elapsed_ms": 5000}},
        ]
        out = summarize_timeline(job, events)
        assert "Planning completed" in out
        assert "tasks=3" in out
        assert "model=qwen3" in out
        assert "5.0s" in out

    def test_planning_started_not_rendered_separately(self):
        job = _make_job()
        events = [
            {"event": "planning_started", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "metadata": {}},
            {"event": "planning_completed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(1), "outcome": "changed", "metadata": {"task_count": 1}},
        ]
        out = summarize_timeline(job, events)
        # planning_started is skipped; only one "Planning" line visible
        assert out.count("Planning") == 1

    def test_planning_completed_noop(self):
        job = _make_job()
        events = [{"event": "planning_completed", "job_id": str(job.id), "run_id": "r",
                   "timestamp": _ts(0), "outcome": "noop", "metadata": {}}]
        out = summarize_timeline(job, events)
        assert "already planned" in out or "no change" in out

    def test_planning_failed_renders_detail(self):
        job = _make_job()
        events = [{"event": "planning_failed", "job_id": str(job.id), "run_id": "r",
                   "timestamp": _ts(0), "outcome": "error", "message": "planning failed",
                   "metadata": {"error_category": "RuntimeError"}}]
        out = summarize_timeline(job, events)
        assert "Planning failed" in out
        assert "RuntimeError" in out

    def test_planning_failed_without_error_category_renders_unknown_error(self):
        """When error_category is absent, timeline must show 'unknown error', not raw message."""
        job = _make_job()
        events = [{"event": "planning_failed", "job_id": str(job.id), "run_id": "r",
                   "timestamp": _ts(0), "outcome": "error",
                   "message": "secret-token SHOULD_NOT_RENDER",
                   "metadata": {}}]
        out = summarize_timeline(job, events)
        assert "Planning failed" in out
        assert "unknown error" in out
        assert "secret-token" not in out
        assert "SHOULD_NOT_RENDER" not in out

    def test_planning_failed_message_field_never_rendered_as_detail(self):
        """message field is silenced even when it looks like a connection error with secrets."""
        job = _make_job()
        events = [{"event": "planning_failed", "job_id": str(job.id), "run_id": "r",
                   "timestamp": _ts(0), "outcome": "error",
                   "message": "connection refused password=abc",
                   "metadata": {}}]
        out = summarize_timeline(job, events)
        assert "connection refused" not in out
        assert "password=abc" not in out
        assert "Planning failed" in out

    def test_planning_failed_error_category_wins_over_message(self):
        """When both error_category and a sensitive message are present, error_category wins."""
        job = _make_job()
        events = [{"event": "planning_failed", "job_id": str(job.id), "run_id": "r",
                   "timestamp": _ts(0), "outcome": "error",
                   "message": "secret-token SHOULD_NOT_RENDER",
                   "metadata": {"error_category": "RuntimeError"}}]
        out = summarize_timeline(job, events)
        assert "Planning failed" in out
        assert "RuntimeError" in out
        assert "secret-token" not in out
        assert "SHOULD_NOT_RENDER" not in out


class TestRenderTaskRunNoop:
    def test_no_pending_tasks_renders(self):
        job = _make_job()
        events = [{"event": "task_run_noop", "job_id": str(job.id), "run_id": "r",
                   "timestamp": _ts(0), "outcome": "no_pending_tasks", "metadata": {}}]
        out = summarize_timeline(job, events)
        assert "No pending tasks" in out

    def test_no_change_renders_distinctly(self):
        """task_run_noop/no_change after task_run_started differs from no_pending_tasks."""
        job = _make_job()
        task_id = str(uuid4())
        events = [
            {"event": "task_run_started", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "task_id": task_id,
             "metadata": {"task_type": "write_readme"}},
            {"event": "task_run_noop", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(1), "task_id": task_id, "outcome": "no_change",
             "metadata": {"task_type": "write_readme", "reason": "builder_returned_no_change"}},
        ]
        out = summarize_timeline(job, events)
        assert "no change" in out.lower()
        # The EVENTS section must not say "No pending tasks" — check only up to the status section
        events_section = out.split("Current status")[0]
        assert "No pending tasks" not in events_section

    def test_no_change_not_confused_with_no_pending(self):
        """no_change and no_pending_tasks must produce different output text."""
        job = _make_job()
        task_id = str(uuid4())
        no_pending_events = [
            {"event": "task_run_noop", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "outcome": "no_pending_tasks", "metadata": {}}
        ]
        no_change_events = [
            {"event": "task_run_started", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "task_id": task_id,
             "metadata": {"task_type": "write_readme"}},
            {"event": "task_run_noop", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(1), "task_id": task_id, "outcome": "no_change",
             "metadata": {}},
        ]
        pending_out = summarize_timeline(job, no_pending_events)
        change_out = summarize_timeline(job, no_change_events)
        assert pending_out != change_out


class TestRenderPermissionDenied:
    def test_renders_blocked_with_capability(self):
        job = _make_job()
        task_id = str(uuid4())
        events = [
            {"event": "task_run_started", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "task_id": task_id,
             "metadata": {"task_type": "write_readme"}},
            {"event": "task_run_failed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(1), "task_id": task_id, "outcome": "permission_denied",
             "metadata": {"capability": "workspace_write", "task_type": "write_readme"}},
        ]
        out = summarize_timeline(job, events)
        assert "permission denied" in out.lower()
        assert "workspace_write" in out

    def test_renders_task_type_in_denied_line(self):
        job = _make_job()
        task_id = str(uuid4())
        events = [
            {"event": "task_run_started", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "task_id": task_id,
             "metadata": {"task_type": "write_readme"}},
            {"event": "task_run_failed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(1), "task_id": task_id, "outcome": "permission_denied",
             "metadata": {"capability": "workspace_write", "task_type": "write_readme"}},
        ]
        out = summarize_timeline(job, events)
        assert "write_readme" in out


class TestRenderVerificationFailed:
    def test_renders_failure_count(self):
        job = _make_job()
        task_id = str(uuid4())
        events = [
            {"event": "task_run_started", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "task_id": task_id,
             "metadata": {"task_type": "write_readme"}},
            {"event": "builder_started", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(1), "task_id": task_id,
             "model": "qwen3", "metadata": {}},
            {"event": "builder_completed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(2), "task_id": task_id,
             "metadata": {"elapsed_ms": 1000}},
            {"event": "workspace_materialized", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(3), "task_id": task_id,
             "metadata": {"workspace_file": "/tmp/ws.txt"}},
            {"event": "verification_failed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(4), "task_id": task_id, "outcome": "fail",
             "metadata": {
                 "failure_count": 2,
                 "failed_checks": ["required_section:Summary:", "min_proposed_changes"],
             }},
            {"event": "task_run_failed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(5), "task_id": task_id, "outcome": "fail",
             "metadata": {"task_type": "write_readme"}},
        ]
        out = summarize_timeline(job, events)
        assert "verification failed" in out.lower()
        assert "2" in out  # failure count

    def test_renders_failed_check_names(self):
        job = _make_job()
        task_id = str(uuid4())
        events = [
            {"event": "task_run_started", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "task_id": task_id,
             "metadata": {"task_type": "write_readme"}},
            {"event": "verification_failed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(1), "task_id": task_id, "outcome": "fail",
             "metadata": {"failure_count": 1, "failed_checks": ["required_section:Summary:"]}},
            {"event": "task_run_failed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(2), "task_id": task_id, "outcome": "fail",
             "metadata": {"task_type": "write_readme"}},
        ]
        out = summarize_timeline(job, events)
        assert "required_section:Summary:" in out


class TestRenderRepoApplication:
    def test_renders_repo_file_path(self):
        job = _make_job()
        task_id = str(uuid4())
        events = [
            {"event": "task_run_started", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "task_id": task_id,
             "metadata": {"task_type": "write_readme"}},
            {"event": "builder_completed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(1), "task_id": task_id, "metadata": {}},
            {"event": "workspace_materialized", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(2), "task_id": task_id,
             "metadata": {"workspace_file": "/ws/readme.txt"}},
            {"event": "verification_passed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(3), "task_id": task_id, "outcome": "pass", "metadata": {}},
            {"event": "repo_application_completed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(4), "task_id": task_id, "outcome": "applied",
             "metadata": {"file_count": 1, "files": ["/repo/README.md"]}},
            {"event": "task_run_completed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(5), "task_id": task_id, "outcome": "pass",
             "metadata": {}},
        ]
        out = summarize_timeline(job, events)
        assert "/repo/README.md" in out

    def test_renders_repo_skip_reason(self):
        job = _make_job()
        task_id = str(uuid4())
        events = [
            {"event": "task_run_started", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "task_id": task_id,
             "metadata": {"task_type": "write_readme"}},
            {"event": "builder_completed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(1), "task_id": task_id, "metadata": {}},
            {"event": "workspace_materialized", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(2), "task_id": task_id,
             "metadata": {"workspace_file": "/ws/readme.txt"}},
            {"event": "verification_passed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(3), "task_id": task_id, "outcome": "pass", "metadata": {}},
            {"event": "repo_application_skipped", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(4), "task_id": task_id, "outcome": "skipped",
             "metadata": {"reason": "permission_denied"}},
            {"event": "task_run_completed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(5), "task_id": task_id, "outcome": "pass",
             "metadata": {}},
        ]
        out = summarize_timeline(job, events)
        assert "repo write skipped" in out
        assert "permission_denied" in out


class TestRenderPatchIntent:
    def test_renders_intent_count_and_risks(self):
        job = _make_job()
        task_id = str(uuid4())
        events = [
            {"event": "task_run_started", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "task_id": task_id,
             "metadata": {"task_type": "write_readme"}},
            {"event": "builder_completed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(1), "task_id": task_id, "metadata": {}},
            {"event": "workspace_materialized", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(2), "task_id": task_id,
             "metadata": {"workspace_file": "/ws/readme.txt"}},
            {"event": "verification_passed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(3), "task_id": task_id, "outcome": "pass", "metadata": {}},
            {"event": "patch_intent_created", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(4), "task_id": task_id, "outcome": "created",
             "metadata": {"intent_count": 2, "risk_levels": ["low", "medium"]}},
            {"event": "task_run_completed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(5), "task_id": task_id, "outcome": "pass",
             "metadata": {}},
        ]
        out = summarize_timeline(job, events)
        assert "intents" in out
        assert "2" in out
        assert "medium" in out


class TestRenderUnknownEvents:
    def test_unknown_event_outside_task_block_does_not_crash(self):
        job = _make_job()
        events = [
            {"event": "totally_unknown_event_xyz", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "metadata": {}},
        ]
        out = summarize_timeline(job, events)  # must not raise
        assert "totally_unknown_event_xyz" in out

    def test_unknown_event_inside_task_block_does_not_crash(self):
        job = _make_job()
        task_id = str(uuid4())
        events = [
            {"event": "task_run_started", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "task_id": task_id,
             "metadata": {"task_type": "write_readme"}},
            {"event": "surprise_event", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(1), "task_id": task_id, "metadata": {}},
            {"event": "task_run_completed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(2), "task_id": task_id, "outcome": "pass",
             "metadata": {}},
        ]
        out = summarize_timeline(job, events)  # must not raise
        assert "write_readme" in out

    def test_interrupted_task_block_does_not_crash(self):
        """task_run_started with no terminal event renders as interrupted."""
        job = _make_job()
        task_id = str(uuid4())
        events = [
            {"event": "task_run_started", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "task_id": task_id,
             "metadata": {"task_type": "write_readme"}},
        ]
        out = summarize_timeline(job, events)
        assert "interrupted" in out


# ---------------------------------------------------------------------------
# summarize_timeline — status and next action
# ---------------------------------------------------------------------------


class TestDeriveStatus:
    def test_unplanned_job_no_tasks(self):
        job = _make_job()
        out = summarize_timeline(job, [])
        assert "Unplanned" in out or "no tasks" in out.lower()

    def test_pending_tasks_shown(self):
        job = _make_job()
        job.tasks.append(Task(description="t", inputs={}))
        out = summarize_timeline(job, [])
        assert "Pending" in out or "pending" in out

    def test_all_completed(self):
        job = _make_job(state=RunState.COMPLETED)
        t = Task(description="t", inputs={})
        t.status = RunState.COMPLETED
        job.tasks.append(t)
        out = summarize_timeline(job, [])
        assert "Complete" in out or "completed" in out


class TestDeriveNextAction:
    def test_pending_tasks_suggests_run(self):
        job = _make_job()
        job.tasks.append(Task(description="t", inputs={}))
        out = summarize_timeline(job, [])
        assert "job run-next" in out
        assert str(job.id) in out

    def test_permission_denied_suggests_set_permission(self):
        job = _make_job()
        task_id = str(uuid4())
        events = [
            {"event": "task_run_started", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "task_id": task_id,
             "metadata": {"task_type": "write_readme"}},
            {"event": "task_run_failed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(1), "task_id": task_id, "outcome": "permission_denied",
             "metadata": {"capability": "workspace_write"}},
        ]
        out = summarize_timeline(job, events)
        assert "job permit" in out
        assert "workspace_write" in out

    def test_patch_intent_with_high_risk_warns(self):
        job = _make_job()
        task_id = str(uuid4())
        events = [
            {"event": "task_run_started", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "task_id": task_id,
             "metadata": {"task_type": "write_readme"}},
            {"event": "patch_intent_created", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(1), "task_id": task_id, "outcome": "created",
             "metadata": {"intent_count": 1, "risk_levels": ["high"]}},
            {"event": "task_run_completed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(2), "task_id": task_id, "outcome": "pass", "metadata": {}},
        ]
        out = summarize_timeline(job, events)
        assert "risk" in out.lower()

    def test_no_pending_suggests_inspect(self):
        job = _make_job(state=RunState.COMPLETED)
        t = Task(description="t", inputs={})
        t.status = RunState.COMPLETED
        job.tasks.append(t)
        out = summarize_timeline(job, [])
        assert "No pending tasks" in out or "create-job" in out


# ---------------------------------------------------------------------------
# CLI integration
# ---------------------------------------------------------------------------


class TestCmdTimeline:
    def _make_and_save_job(self, tmp_path, monkeypatch) -> Job:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = Job(name="test job", state=RunState.PENDING)
        save_job(job)
        return job

    def _write_events(self, tmp_path, job_id, events: list[dict]) -> None:
        run_dir = tmp_path / "job_logs" / str(job_id)
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "run1.jsonl").write_text(
            "\n".join(json.dumps(e) for e in events) + "\n", encoding="utf-8"
        )

    def test_prints_timeline_for_job_with_logs(
        self, tmp_path, monkeypatch, capsys
    ):
        job = self._make_and_save_job(tmp_path, monkeypatch)
        self._write_events(tmp_path, job.id, _simple_events(str(job.id)))

        from apps.cli.commands.brain import _cmd_timeline

        _cmd_timeline(str(job.id))

        out = capsys.readouterr().out
        assert "Remedy Timeline" in out
        assert str(job.id)[:8] in out

    def test_prints_planning_completed_in_output(
        self, tmp_path, monkeypatch, capsys
    ):
        job = self._make_and_save_job(tmp_path, monkeypatch)
        self._write_events(tmp_path, job.id, _simple_events(str(job.id)))

        from apps.cli.commands.brain import _cmd_timeline

        _cmd_timeline(str(job.id))

        out = capsys.readouterr().out
        assert "Planning completed" in out

    def test_no_logs_prints_graceful_message(
        self, tmp_path, monkeypatch, capsys
    ):
        job = self._make_and_save_job(tmp_path, monkeypatch)

        from apps.cli.commands.brain import _cmd_timeline

        _cmd_timeline(str(job.id))  # must not raise

        out = capsys.readouterr().out
        assert "No run logs found" in out

    def test_no_logs_exits_0(self, tmp_path, monkeypatch):
        job = self._make_and_save_job(tmp_path, monkeypatch)

        from apps.cli.commands.brain import _cmd_timeline

        # Should not raise SystemExit
        _cmd_timeline(str(job.id))

    def test_invalid_job_id_exits_1(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))

        from apps.cli.commands.brain import _cmd_timeline

        with pytest.raises(SystemExit) as exc_info:
            _cmd_timeline("not-a-uuid")
        assert exc_info.value.code == 1

    def test_unknown_job_id_exits_1(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))

        from apps.cli.commands.brain import _cmd_timeline

        with pytest.raises(SystemExit) as exc_info:
            _cmd_timeline(str(uuid4()))
        assert exc_info.value.code == 1

    def test_timeline_output_includes_next_action(
        self, tmp_path, monkeypatch, capsys
    ):
        job = self._make_and_save_job(tmp_path, monkeypatch)
        self._write_events(tmp_path, job.id, _simple_events(str(job.id)))

        from apps.cli.commands.brain import _cmd_timeline

        _cmd_timeline(str(job.id))

        out = capsys.readouterr().out
        assert "Next suggested action" in out
