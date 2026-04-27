"""
CLI-level tests for permission-related commands in apps/cli/main.py.

Tests cover:
  - set-permission: reserved capability notice printed to stdout
  - set-permission: no notice for active capabilities
  - show-permissions: displays all four capabilities
  - show-permissions: all capabilities labeled [active] or [reserved]
  - show-permissions: effective allow/deny is reflected correctly
  - workspace_write denial: exits non-zero before builder call, no state mutation

All tests are deterministic — no live Ollama, no builder, no verifier.
A temporary REMEDY_DATA_DIR is injected via monkeypatch so tests do not
touch the real .data/ directory.
"""

from __future__ import annotations

import pytest

from packages.core.models import Job, RunState, Task
from packages.orchestration.permissions import Capability, set_permission
from packages.orchestration.storage import load_job, save_job


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_and_save_job(tmp_path, monkeypatch, **metadata_overrides) -> Job:
    """Create a minimal job, persist it in a temp data dir, and return it."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job = Job(name="test", state=RunState.PENDING)
    job.metadata.update(metadata_overrides)
    save_job(job)
    return job


# ---------------------------------------------------------------------------
# set-permission: reserved capability notice
# ---------------------------------------------------------------------------


class TestSetPermissionReservedNotice:
    def test_reserved_cap_prints_notice_on_allow(self, tmp_path, monkeypatch, capsys):
        job = _make_and_save_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_set_permission

        _cmd_set_permission(str(job.id), "allow", "repo_overwrite")
        out = capsys.readouterr().out
        assert "reserved" in out
        assert "repo_overwrite" in out

    def test_reserved_cap_prints_notice_on_deny(self, tmp_path, monkeypatch, capsys):
        job = _make_and_save_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_set_permission

        _cmd_set_permission(str(job.id), "deny", "shell_exec")
        out = capsys.readouterr().out
        assert "reserved" in out
        assert "shell_exec" in out

    def test_active_cap_no_reserved_notice(self, tmp_path, monkeypatch, capsys):
        job = _make_and_save_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_set_permission

        _cmd_set_permission(str(job.id), "allow", "repo_generated_write")
        out = capsys.readouterr().out
        assert "reserved" not in out

    def test_workspace_write_no_reserved_notice(self, tmp_path, monkeypatch, capsys):
        job = _make_and_save_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_set_permission

        _cmd_set_permission(str(job.id), "deny", "workspace_write")
        out = capsys.readouterr().out
        assert "reserved" not in out

    def test_set_permission_still_persists_for_reserved_cap(self, tmp_path, monkeypatch):
        job = _make_and_save_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_set_permission
        from packages.orchestration.storage import load_job

        _cmd_set_permission(str(job.id), "allow", "repo_overwrite")
        reloaded = load_job(job.id)
        assert reloaded.metadata["permissions"]["repo_overwrite"] == "allow"


# ---------------------------------------------------------------------------
# show-permissions
# ---------------------------------------------------------------------------


class TestShowPermissions:
    def test_shows_all_four_capabilities(self, tmp_path, monkeypatch, capsys):
        job = _make_and_save_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_show_permissions

        _cmd_show_permissions(str(job.id))
        out = capsys.readouterr().out
        assert "workspace_write" in out
        assert "repo_generated_write" in out
        assert "repo_overwrite" in out
        assert "shell_exec" in out

    def test_reserved_capabilities_are_labeled(self, tmp_path, monkeypatch, capsys):
        job = _make_and_save_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_show_permissions

        _cmd_show_permissions(str(job.id))
        out = capsys.readouterr().out
        assert "[reserved]" in out

    def test_active_capabilities_are_labeled(self, tmp_path, monkeypatch, capsys):
        job = _make_and_save_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_show_permissions

        _cmd_show_permissions(str(job.id))
        out = capsys.readouterr().out
        assert "[active]" in out

    def test_workspace_write_line_has_active_label(self, tmp_path, monkeypatch, capsys):
        job = _make_and_save_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_show_permissions

        _cmd_show_permissions(str(job.id))
        out = capsys.readouterr().out
        lines = [l for l in out.splitlines() if "workspace_write" in l]
        assert any("[active]" in l for l in lines)

    def test_repo_overwrite_line_has_reserved_label(self, tmp_path, monkeypatch, capsys):
        job = _make_and_save_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_show_permissions

        _cmd_show_permissions(str(job.id))
        out = capsys.readouterr().out
        lines = [l for l in out.splitlines() if "repo_overwrite" in l]
        assert any("[reserved]" in l for l in lines)

    def test_default_workspace_write_shows_allow(self, tmp_path, monkeypatch, capsys):
        job = _make_and_save_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_show_permissions

        _cmd_show_permissions(str(job.id))
        out = capsys.readouterr().out
        # workspace_write is allowed by default
        lines = [l for l in out.splitlines() if "workspace_write" in l]
        assert any("allow" in l for l in lines)

    def test_explicit_allow_reflected(self, tmp_path, monkeypatch, capsys):
        job = _make_and_save_job(tmp_path, monkeypatch)
        set_permission(job, Capability.repo_generated_write, allow=True)
        save_job(job)

        from apps.cli.main import _cmd_show_permissions

        _cmd_show_permissions(str(job.id))
        out = capsys.readouterr().out
        lines = [l for l in out.splitlines() if "repo_generated_write" in l]
        assert any("allow" in l for l in lines)

    def test_explicit_deny_reflected(self, tmp_path, monkeypatch, capsys):
        job = _make_and_save_job(tmp_path, monkeypatch)
        set_permission(job, Capability.workspace_write, allow=False)
        save_job(job)

        from apps.cli.main import _cmd_show_permissions

        _cmd_show_permissions(str(job.id))
        out = capsys.readouterr().out
        lines = [l for l in out.splitlines() if "workspace_write" in l]
        assert any("deny" in l for l in lines)


# ---------------------------------------------------------------------------
# workspace_write denial: pre-builder enforcement (Step 9.6)
# ---------------------------------------------------------------------------


class TestWorkspaceWriteDenialPreBuilder:
    """workspace_write denial must stop execution before the builder is called.

    These tests verify the early guard in _cmd_run_next_task_local:
    - exits non-zero immediately
    - prints a clear error to stderr naming the denied permission
    - does not mutate task state (no RUNNING tasks)
    - does not create artifacts
    - does not save any modified job state
    """

    def _setup_denied_job(self, tmp_path, monkeypatch) -> Job:
        job = _make_and_save_job(tmp_path, monkeypatch)
        # Add a pending task so the scenario is meaningful
        task = Task(description="test task", inputs={"task_type": "test"})
        job.tasks.append(task)
        set_permission(job, Capability.workspace_write, allow=False)
        save_job(job)
        return job

    def test_denied_exits_nonzero(self, tmp_path, monkeypatch):
        job = self._setup_denied_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_run_next_task_local

        with pytest.raises(SystemExit) as exc_info:
            _cmd_run_next_task_local(str(job.id))
        assert exc_info.value.code == 1

    def test_denied_prints_error_to_stderr(self, tmp_path, monkeypatch, capsys):
        job = self._setup_denied_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_run_next_task_local

        with pytest.raises(SystemExit):
            _cmd_run_next_task_local(str(job.id))
        err = capsys.readouterr().err
        assert "workspace_write" in err
        assert "permission" in err.lower()

    def test_denied_does_not_mutate_task_state(self, tmp_path, monkeypatch):
        job = self._setup_denied_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_run_next_task_local

        with pytest.raises(SystemExit):
            _cmd_run_next_task_local(str(job.id))
        reloaded = load_job(job.id)
        # No task should have transitioned to RUNNING (builder was never called)
        assert all(t.status == RunState.PENDING for t in reloaded.tasks)

    def test_denied_does_not_create_artifacts(self, tmp_path, monkeypatch):
        job = self._setup_denied_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_run_next_task_local

        with pytest.raises(SystemExit):
            _cmd_run_next_task_local(str(job.id))
        reloaded = load_job(job.id)
        assert len(reloaded.artifacts) == 0
