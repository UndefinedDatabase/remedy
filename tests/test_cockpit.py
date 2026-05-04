"""
Tests for packages/orchestration/cockpit.py and the `remedy cockpit` CLI command.

Coverage:
  - completed job with medium patch risk: attention + can_auto logic
  - pending task + workspace_write allowed: can continue automatically
  - pending task + workspace_write denied: needs attention, auto no
  - repo_generated_write denied but workspace_write allowed: auto yes, repo attention
  - verification failure shown as attention item
  - no pending tasks: next action suggests inspect/create-job
  - interrupted task_run_started without terminal: flagged in situation + attention
  - unknown events do not crash
  - no run logs still renders useful job status
  - no raw diff/content/exception text printed
  - CLI: prints cockpit output for valid job
  - CLI: invalid job ID exits 1
  - CLI: unknown job ID exits 1
"""

from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

import pytest

from packages.core.models import Job, RunState, Task
from packages.orchestration.cockpit import summarize_cockpit
from packages.orchestration.permissions import Capability, set_permission
from packages.orchestration.storage import save_job


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _ts(offset: int = 0) -> str:
    return f"2026-05-04T10:{offset:02d}:00+00:00"


def _make_job(**kwargs) -> Job:
    defaults: dict = {"name": "Test cockpit job", "state": RunState.PENDING}
    defaults.update(kwargs)
    return Job(**defaults)


def _make_pending_task(**kwargs) -> Task:
    return Task(description="do work", inputs={"task_type": "write_readme"}, **kwargs)


def _completed_task(**kwargs) -> Task:
    t = Task(description="done", inputs={"task_type": "write_readme"}, **kwargs)
    t.status = RunState.COMPLETED
    return t


def _ev(name: str, job_id: str, **extra) -> dict:
    base = {"event": name, "job_id": job_id, "run_id": "r", "timestamp": _ts(0), "metadata": {}}
    base.update(extra)
    return base


def _task_run_succeeded(job_id: str, task_id: str | None = None) -> list[dict]:
    return [
        {"event": "task_run_started", "job_id": job_id, "run_id": "r",
         "timestamp": _ts(0), "task_id": task_id,
         "metadata": {"task_type": "write_readme"}},
        {"event": "builder_completed", "job_id": job_id, "run_id": "r",
         "timestamp": _ts(1), "task_id": task_id, "metadata": {"elapsed_ms": 1000}},
        {"event": "workspace_materialized", "job_id": job_id, "run_id": "r",
         "timestamp": _ts(2), "task_id": task_id,
         "metadata": {"workspace_file": "/ws/readme.txt"}},
        {"event": "verification_passed", "job_id": job_id, "run_id": "r",
         "timestamp": _ts(3), "task_id": task_id, "outcome": "pass", "metadata": {}},
        {"event": "task_run_completed", "job_id": job_id, "run_id": "r",
         "timestamp": _ts(4), "task_id": task_id, "outcome": "pass", "metadata": {}},
    ]


# ---------------------------------------------------------------------------
# Header and structure
# ---------------------------------------------------------------------------


class TestCockpitHeader:
    def test_includes_remedy_cockpit_title(self):
        job = _make_job()
        out = summarize_cockpit(job, [])
        assert "Remedy Cockpit" in out

    def test_includes_short_job_id(self):
        job = _make_job()
        out = summarize_cockpit(job, [])
        assert str(job.id)[:8] in out

    def test_includes_job_state(self):
        job = _make_job(state=RunState.COMPLETED)
        out = summarize_cockpit(job, [])
        assert "completed" in out

    def test_includes_progress_with_tasks(self):
        job = _make_job()
        job.tasks.append(_completed_task())
        job.tasks.append(_make_pending_task())
        out = summarize_cockpit(job, [])
        assert "1/2" in out

    def test_unplanned_job_shows_no_tasks(self):
        job = _make_job()
        out = summarize_cockpit(job, [])
        assert "unplanned" in out.lower() or "no tasks" in out.lower()

    def test_truncates_long_job_name(self):
        job = _make_job(name="X" * 80)
        out = summarize_cockpit(job, [])
        assert "…" in out
        assert "X" * 80 not in out

    def test_has_situation_section(self):
        job = _make_job()
        out = summarize_cockpit(job, [])
        assert "Situation" in out

    def test_has_needs_attention_section(self):
        job = _make_job()
        out = summarize_cockpit(job, [])
        assert "Needs your attention" in out

    def test_has_can_continue_section(self):
        job = _make_job()
        out = summarize_cockpit(job, [])
        assert "Can continue automatically" in out

    def test_has_next_best_action_section(self):
        job = _make_job()
        out = summarize_cockpit(job, [])
        assert "Next best action" in out


# ---------------------------------------------------------------------------
# Situation: last run status
# ---------------------------------------------------------------------------


class TestSituationLastRun:
    def test_no_runs_shows_no_recorded(self):
        job = _make_job()
        out = summarize_cockpit(job, [])
        assert "No task runs" in out or "no task runs" in out.lower()

    def test_completed_run_shows_passed(self):
        job = _make_job()
        events = _task_run_succeeded(str(job.id))
        out = summarize_cockpit(job, events)
        assert "passed" in out.lower() or "Last run: passed" in out

    def test_permission_denied_shows_blocked(self):
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
        out = summarize_cockpit(job, events)
        assert "blocked" in out.lower() or "permission denied" in out.lower()
        assert "workspace_write" in out

    def test_verification_failed_shows_fail(self):
        job = _make_job()
        task_id = str(uuid4())
        events = [
            {"event": "task_run_started", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "task_id": task_id,
             "metadata": {"task_type": "write_readme"}},
            {"event": "verification_failed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(1), "task_id": task_id, "outcome": "fail",
             "metadata": {"failure_count": 2, "failed_checks": ["required_section:Summary:"]}},
            {"event": "task_run_failed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(2), "task_id": task_id, "outcome": "fail",
             "metadata": {}},
        ]
        out = summarize_cockpit(job, events)
        assert "verification failed" in out.lower()


class TestSituationPermissions:
    def test_workspace_write_allowed_by_default(self):
        job = _make_job()
        out = summarize_cockpit(job, [])
        assert "Workspace writes: allowed" in out

    def test_workspace_write_denied_shown(self):
        job = _make_job()
        set_permission(job, Capability.workspace_write, allow=False)
        out = summarize_cockpit(job, [])
        assert "Workspace writes: denied" in out

    def test_repo_write_shown(self):
        job = _make_job()
        out = summarize_cockpit(job, [])
        assert "Repo writes:" in out


# ---------------------------------------------------------------------------
# Attention items
# ---------------------------------------------------------------------------


class TestNeedsAttention:
    def test_nothing_needs_attention_when_clean(self):
        job = _make_job(state=RunState.COMPLETED)
        job.tasks.append(_completed_task())
        events = _task_run_succeeded(str(job.id))
        out = summarize_cockpit(job, events)
        assert "Nothing needs your attention" in out

    def test_workspace_denied_with_pending_raises_attention(self):
        job = _make_job()
        job.tasks.append(_make_pending_task())
        set_permission(job, Capability.workspace_write, allow=False)
        out = summarize_cockpit(job, [])
        assert "workspace_write" in out
        assert "Nothing needs your attention" not in out

    def test_medium_patch_risk_raises_attention(self):
        job = _make_job()
        task_id = str(uuid4())
        events = _task_run_succeeded(str(job.id), task_id) + [
            {"event": "patch_intent_created", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(10), "task_id": task_id, "outcome": "created",
             "metadata": {"intent_count": 1, "risk_levels": ["medium"]}},
        ]
        out = summarize_cockpit(job, events)
        assert "Review patch intent" in out or "risk" in out.lower()

    def test_low_patch_risk_no_attention(self):
        job = _make_job(state=RunState.COMPLETED)
        job.tasks.append(_completed_task())
        task_id = str(uuid4())
        events = _task_run_succeeded(str(job.id), task_id) + [
            {"event": "patch_intent_created", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(10), "task_id": task_id, "outcome": "created",
             "metadata": {"intent_count": 1, "risk_levels": ["low"]}},
        ]
        out = summarize_cockpit(job, events)
        assert "Nothing needs your attention" in out

    def test_verification_failure_in_attention(self):
        job = _make_job()
        task_id = str(uuid4())
        events = [
            {"event": "task_run_started", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "task_id": task_id,
             "metadata": {"task_type": "write_readme"}},
            {"event": "verification_failed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(1), "task_id": task_id, "outcome": "fail",
             "metadata": {
                 "failure_count": 1,
                 "failed_checks": ["required_section:Summary:"],
             }},
            {"event": "task_run_failed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(2), "task_id": task_id, "outcome": "fail",
             "metadata": {}},
        ]
        out = summarize_cockpit(job, events)
        assert "Verification failed" in out or "verification failed" in out.lower()
        assert "required_section:Summary:" in out

    def test_interrupted_run_raises_attention(self):
        job = _make_job()
        task_id = str(uuid4())
        events = [
            {"event": "task_run_started", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "task_id": task_id,
             "metadata": {"task_type": "write_readme"}},
            # No terminal event — interrupted
        ]
        out = summarize_cockpit(job, events)
        assert "Interrupted" in out or "interrupted" in out

    def test_repo_write_denied_with_patch_output_raises_attention(self):
        job = _make_job(state=RunState.COMPLETED)
        job.tasks.append(_completed_task())
        task_id = str(uuid4())
        set_permission(job, Capability.repo_generated_write, allow=False)
        events = _task_run_succeeded(str(job.id), task_id) + [
            {"event": "patch_intent_created", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(10), "task_id": task_id, "outcome": "created",
             "metadata": {"intent_count": 1, "risk_levels": ["low"]}},
        ]
        out = summarize_cockpit(job, events)
        assert "repo_generated_write" in out or "Repo writes" in out


# ---------------------------------------------------------------------------
# Can continue automatically
# ---------------------------------------------------------------------------


class TestCanAutoContinue:
    def test_pending_workspace_allowed_yes(self):
        job = _make_job()
        job.tasks.append(_make_pending_task())
        out = summarize_cockpit(job, [])
        assert "yes" in out

    def test_pending_workspace_denied_no(self):
        job = _make_job()
        job.tasks.append(_make_pending_task())
        set_permission(job, Capability.workspace_write, allow=False)
        out = summarize_cockpit(job, [])
        section = out.split("Can continue automatically")[1].split("\n── ")[0]
        assert "no" in section

    def test_no_pending_no(self):
        job = _make_job(state=RunState.COMPLETED)
        job.tasks.append(_completed_task())
        out = summarize_cockpit(job, [])
        section = out.split("Can continue automatically")[1].split("\n── ")[0]
        assert "no" in section

    def test_repo_denied_workspace_allowed_yes(self):
        """repo_generated_write is optional; workspace_write allowed → can continue."""
        job = _make_job()
        job.tasks.append(_make_pending_task())
        set_permission(job, Capability.repo_generated_write, allow=False)
        out = summarize_cockpit(job, [])
        section = out.split("Can continue automatically")[1].split("\n── ")[0]
        assert "yes" in section

    def test_interrupted_run_no_when_pending(self):
        """Interrupted run + pending tasks: cannot auto-continue (conservative for autonomy)."""
        job = _make_job()
        job.tasks.append(_make_pending_task())
        task_id = str(uuid4())
        events = [
            {"event": "task_run_started", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "task_id": task_id,
             "metadata": {"task_type": "write_readme"}},
        ]
        out = summarize_cockpit(job, events)
        section = out.split("Can continue automatically")[1].split("\n── ")[0]
        assert "no" in section

    def test_interrupted_run_reason_mentions_inspect(self):
        """Reason for no-auto-continue on interrupted run should guide the user."""
        job = _make_job()
        job.tasks.append(_make_pending_task())
        task_id = str(uuid4())
        events = [
            {"event": "task_run_started", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "task_id": task_id,
             "metadata": {"task_type": "write_readme"}},
        ]
        out = summarize_cockpit(job, events)
        section = out.split("Can continue automatically")[1].split("\n── ")[0]
        assert "interrupted" in section or "inspect" in section


# ---------------------------------------------------------------------------
# Next best action
# ---------------------------------------------------------------------------


class TestNextBestAction:
    def test_pending_workspace_allowed_suggests_run(self):
        job = _make_job()
        job.tasks.append(_make_pending_task())
        out = summarize_cockpit(job, [])
        assert "run-next-task-local" in out
        assert str(job.id) in out

    def test_workspace_denied_suggests_set_permission(self):
        job = _make_job()
        job.tasks.append(_make_pending_task())
        set_permission(job, Capability.workspace_write, allow=False)
        out = summarize_cockpit(job, [])
        assert "set-permission" in out
        assert "workspace_write" in out

    def test_no_pending_suggests_inspect(self):
        job = _make_job(state=RunState.COMPLETED)
        job.tasks.append(_completed_task())
        out = summarize_cockpit(job, [])
        action_section = out.split("Next best action")[1]
        assert "create-job" in action_section or "Inspect" in action_section

    def test_interrupted_run_suggests_timeline_first(self):
        job = _make_job()
        job.tasks.append(_make_pending_task())
        task_id = str(uuid4())
        events = [
            {"event": "task_run_started", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "task_id": task_id,
             "metadata": {"task_type": "write_readme"}},
        ]
        out = summarize_cockpit(job, events)
        action_section = out.split("Next best action")[1]
        assert "timeline" in action_section

    def test_medium_risk_with_pending_still_suggests_run(self):
        job = _make_job()
        job.tasks.append(_make_pending_task())
        task_id = str(uuid4())
        events = [
            {"event": "patch_intent_created", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "task_id": task_id, "outcome": "created",
             "metadata": {"intent_count": 1, "risk_levels": ["medium"]}},
        ]
        out = summarize_cockpit(job, events)
        assert "run-next-task-local" in out


# ---------------------------------------------------------------------------
# Important artifacts
# ---------------------------------------------------------------------------


class TestImportantArtifacts:
    def test_workspace_file_shown(self):
        job = _make_job()
        task_id = str(uuid4())
        events = _task_run_succeeded(str(job.id), task_id)
        out = summarize_cockpit(job, events)
        assert "/ws/readme.txt" in out

    def test_repo_file_shown(self):
        job = _make_job()
        task_id = str(uuid4())
        events = _task_run_succeeded(str(job.id), task_id) + [
            {"event": "repo_application_completed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(10), "task_id": task_id, "outcome": "applied",
             "metadata": {"file_count": 1, "files": ["/repo/README.md"]}},
        ]
        out = summarize_cockpit(job, events)
        assert "/repo/README.md" in out

    def test_patch_intent_count_shown(self):
        job = _make_job()
        task_id = str(uuid4())
        events = _task_run_succeeded(str(job.id), task_id) + [
            {"event": "patch_intent_created", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(10), "task_id": task_id, "outcome": "created",
             "metadata": {"intent_count": 3, "risk_levels": ["low"]}},
        ]
        out = summarize_cockpit(job, events)
        assert "patch intents:" in out or "patch intent" in out.lower()
        assert "3" in out

    def test_run_log_dir_shown_when_data_dir_provided(self):
        job = _make_job()
        out = summarize_cockpit(job, [], data_dir=Path("/tmp/remedy"))
        assert str(job.id) in out
        assert "run log" in out.lower() or "runs" in out

    def test_run_log_dir_absent_when_data_dir_none(self):
        """data_dir=None: workspace/repo/patch artifacts shown but run log dir is not."""
        job = _make_job(state=RunState.COMPLETED)
        job.tasks.append(_completed_task())
        task_id = str(uuid4())
        events = _task_run_succeeded(str(job.id), task_id) + [
            {"event": "patch_intent_created", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(10), "task_id": task_id, "outcome": "created",
             "metadata": {"intent_count": 2, "risk_levels": ["low"]}},
        ]
        out = summarize_cockpit(job, events, data_dir=None)
        assert "workspace:" in out
        assert "patch intents:" in out or "patch intent" in out.lower()
        assert "run log" not in out.lower()

    def test_no_artifacts_section_when_no_artifacts(self):
        job = _make_job()
        out = summarize_cockpit(job, [])
        assert "Important artifacts" not in out

    def test_default_repo_permission_no_attention_item(self):
        """repo_generated_write not explicitly denied → no repo-denial attention item."""
        job = _make_job(state=RunState.COMPLETED)
        job.tasks.append(_completed_task())
        task_id = str(uuid4())
        # patch with low risk so no patch-risk attention item either
        events = _task_run_succeeded(str(job.id), task_id) + [
            {"event": "patch_intent_created", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(10), "task_id": task_id, "outcome": "created",
             "metadata": {"intent_count": 1, "risk_levels": ["low"]}},
        ]
        # No set_permission call — repo_generated_write stays at its default (False/opt-in)
        out = summarize_cockpit(job, events)
        assert "Repo writes are denied" not in out
        assert "repo_generated_write" not in out


# ---------------------------------------------------------------------------
# Redaction and crash safety
# ---------------------------------------------------------------------------


class TestRedactionAndSafety:
    def test_unknown_events_do_not_crash(self):
        job = _make_job()
        events = [{"event": "totally_unknown_zyx", "job_id": str(job.id), "run_id": "r",
                   "timestamp": _ts(0), "metadata": {}}]
        out = summarize_cockpit(job, events)  # must not raise
        assert "Remedy Cockpit" in out

    def test_no_run_logs_renders_useful_status(self):
        job = _make_job()
        job.tasks.append(_make_pending_task())
        out = summarize_cockpit(job, [])
        assert "Remedy Cockpit" in out
        assert "Pending tasks" in out or "pending" in out.lower()

    def test_no_raw_artifact_content_printed(self):
        """Artifact content is never rendered; only paths and counts."""
        job = _make_job()
        task_id = str(uuid4())
        events = _task_run_succeeded(str(job.id), task_id)
        out = summarize_cockpit(job, events)
        # The workspace event has workspace_file path — that is safe.
        # What must NOT appear: artifact content or diff previews.
        assert "Proposed Changes:" not in out
        assert "diff --git" not in out

    def test_no_raw_exception_text(self):
        """Even if a planning_failed event has message with raw text, cockpit never shows it."""
        job = _make_job()
        events = [
            {"event": "planning_failed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "outcome": "error",
             "message": "secret-token MUST_NOT_APPEAR",
             "metadata": {}},
        ]
        out = summarize_cockpit(job, events)
        assert "secret-token" not in out
        assert "MUST_NOT_APPEAR" not in out

    def test_missing_metadata_fields_do_not_crash(self):
        """Events with incomplete metadata are handled gracefully."""
        job = _make_job()
        events = [
            {"event": "patch_intent_created"},         # no metadata, no job_id
            {"event": "task_run_failed", "outcome": "permission_denied"},  # no metadata
        ]
        out = summarize_cockpit(job, events)  # must not raise
        assert "Remedy Cockpit" in out


# ---------------------------------------------------------------------------
# CLI integration
# ---------------------------------------------------------------------------


class TestCmdCockpit:
    def _save(self, tmp_path, monkeypatch, **kwargs) -> Job:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job(**kwargs)
        save_job(job)
        return job

    def test_prints_cockpit_for_valid_job(self, tmp_path, monkeypatch, capsys):
        job = self._save(tmp_path, monkeypatch)

        from apps.cli.main import _cmd_cockpit

        _cmd_cockpit(str(job.id))
        out = capsys.readouterr().out
        assert "Remedy Cockpit" in out
        assert str(job.id)[:8] in out

    def test_includes_next_best_action(self, tmp_path, monkeypatch, capsys):
        job = self._save(tmp_path, monkeypatch)
        job.tasks.append(_make_pending_task())
        save_job(job)

        from apps.cli.main import _cmd_cockpit

        _cmd_cockpit(str(job.id))
        out = capsys.readouterr().out
        assert "Next best action" in out

    def test_invalid_job_id_exits_1(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))

        from apps.cli.main import _cmd_cockpit

        with pytest.raises(SystemExit) as exc_info:
            _cmd_cockpit("not-a-uuid")
        assert exc_info.value.code == 1

    def test_unknown_job_id_exits_1(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))

        from apps.cli.main import _cmd_cockpit

        with pytest.raises(SystemExit) as exc_info:
            _cmd_cockpit(str(uuid4()))
        assert exc_info.value.code == 1

    def test_no_run_logs_still_prints_cockpit(self, tmp_path, monkeypatch, capsys):
        """Cockpit renders job state even when no run logs exist."""
        job = self._save(tmp_path, monkeypatch)

        from apps.cli.main import _cmd_cockpit

        _cmd_cockpit(str(job.id))  # must not raise
        out = capsys.readouterr().out
        assert "Remedy Cockpit" in out
