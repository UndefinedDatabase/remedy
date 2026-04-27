"""
CLI-level tests for permission-related commands in apps/cli/main.py.

Tests cover:
  - set-permission: reserved capability notice printed to stdout
  - set-permission: no notice for active capabilities
  - show-permissions: displays all four capabilities
  - show-permissions: reserved capabilities are labeled
  - show-permissions: effective allow/deny is reflected correctly

All tests are deterministic — no live Ollama, no builder, no verifier.
A temporary REMEDY_DATA_DIR is injected via monkeypatch so tests do not
touch the real .data/ directory.
"""

from __future__ import annotations

import pytest

from packages.core.models import Job, RunState
from packages.orchestration.permissions import Capability, set_permission
from packages.orchestration.storage import save_job


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
        assert "reserved" in out

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
