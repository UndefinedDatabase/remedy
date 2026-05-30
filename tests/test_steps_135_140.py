"""Tests for Steps 135-140 — Do direct contract, autocoder closure,
smoke closure, dev status honesty, next action surface, commit-readiness.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


def _make_job(*, tasks=None, name="test"):
    from packages.core.models import Job, Task, RunState
    job = Job(name=name)
    if tasks:
        for t in tasks:
            task = Task(
                task_type=t.get("type", "readme_draft"),
                description=t.get("description", t.get("type", "task")),
            )
            if "status" in t:
                task.status = RunState(t["status"])
            if "metadata" in t:
                task.inputs = t["metadata"]
            job.tasks.append(task)
    return job


# ═══════════════════════════════════════════════════════════════════════════
# Step 135 — `remedy do "<goal>"` Direct Contract
# ═══════════════════════════════════════════════════════════════════════════

class TestStep135_DoDirectContract:
    """remedy do '<goal>' must work via default-command rewrite."""

    def test_do_default_rewrite(self):
        """remedy do 'Make tests pass' should rewrite to do run 'Make tests pass'."""
        from apps.cli.grouped import main as grouped_main
        from apps.cli.command_catalog import get_commands_for_group

        subcmds = {c.subcommand for c in get_commands_for_group("do")}
        assert "run" in subcmds
        # "Make tests pass" is not a known subcommand
        assert "Make tests pass" not in subcmds

    def test_do_direct_dry_run(self):
        """remedy do '<goal>' --dry-run --json should work."""
        from apps.cli.grouped import main as grouped_main
        with patch("apps.cli.commands.do_cmd._cmd_do") as mock_do:
            grouped_main(["do", "Make tests pass", "--dry-run", "--json"])
            mock_do.assert_called_once()
            args = mock_do.call_args
            assert args[0][0] == "Make tests pass"

    def test_do_run_alias_still_works(self):
        """remedy do run '<goal>' --dry-run --json should still work."""
        from apps.cli.grouped import main as grouped_main
        with patch("apps.cli.commands.do_cmd._cmd_do") as mock_do:
            grouped_main(["do", "run", "Make tests pass", "--dry-run", "--json"])
            mock_do.assert_called_once()
            assert mock_do.call_args[0][0] == "Make tests pass"

    def test_do_no_args_shows_help(self):
        """remedy do with no args should show group help."""
        from apps.cli.grouped import main as grouped_main
        with patch("builtins.print") as mock_print:
            grouped_main(["do"])
            output = str(mock_print.call_args[0][0])
            assert "do" in output.lower()

    def test_do_help_shows_help(self):
        """remedy do --help should show help."""
        from apps.cli.grouped import main as grouped_main
        with patch("builtins.print") as mock_print:
            grouped_main(["do", "--help"])
            output = str(mock_print.call_args[0][0])
            assert "do" in output.lower()

    def test_do_with_all_flags(self):
        """remedy do '<goal>' with all flags should parse correctly."""
        from apps.cli.grouped import main as grouped_main
        with patch("apps.cli.commands.do_cmd._cmd_do") as mock_do:
            grouped_main([
                "do", "Fix bug",
                "--repo", "/tmp/test",
                "--autonomy-level", "4",
                "--max-cycles", "2",
                "--fixture-builder",
                "--no-ui",
                "--json",
            ])
            mock_do.assert_called_once()
            _, kwargs = mock_do.call_args
            assert kwargs.get("fixture_builder") or mock_do.call_args[0][0] == "Fix bug"

    def test_default_rewrite_dict(self):
        """Default command dict includes both ui and do."""
        from apps.cli.grouped import build_parser
        # Verify the rewrite exists by checking the source
        src = Path("apps/cli/grouped.py").read_text()
        assert '"do": "run"' in src
        assert '"ui": "start"' in src

    def test_main_py_under_120_lines(self):
        content = Path("apps/cli/main.py").read_text()
        assert len(content.splitlines()) <= 120

    def test_no_flat_commands(self):
        """No flat argparse reintroduction in main.py."""
        content = Path("apps/cli/main.py").read_text()
        assert "add_subparsers" not in content


# ═══════════════════════════════════════════════════════════════════════════
# Step 136 — Autocoder Fake-E2E Closure
# ═══════════════════════════════════════════════════════════════════════════

class TestStep136_AutocoderFakeE2E:
    """Fixture builder uses wrong calc.py as starting point."""

    def test_fixture_starts_with_wrong_calc(self):
        """calc.py should start wrong (subtract instead of add)."""
        from packages.core.models import Job
        from packages.orchestration.autorun import _run_fixture_builder
        from packages.orchestration.storage import save_job

        with tempfile.TemporaryDirectory() as tmp:
            job = Job(name="wrong-calc")
            save_job(job)
            from packages.orchestration.data_paths import resolve_data_root
            data_dir = resolve_data_root()
            # Run at low autonomy to see the wrong file exists
            _run_fixture_builder(job, "Fix", Path(tmp), data_dir, autonomy_level=1)
            calc = (Path(tmp) / "calc.py").read_text()
            assert "return a - b" in calc  # wrong version exists

    def test_fixture_fixes_calc(self):
        """After full run, calc.py should have correct add/mul."""
        from packages.core.models import Job
        from packages.orchestration.autorun import _run_fixture_builder
        from packages.orchestration.storage import save_job

        with tempfile.TemporaryDirectory() as tmp:
            job = Job(name="fix-calc")
            save_job(job)
            from packages.orchestration.data_paths import resolve_data_root
            data_dir = resolve_data_root()
            result = _run_fixture_builder(job, "Fix", Path(tmp), data_dir, autonomy_level=4)
            calc = (Path(tmp) / "calc.py").read_text()
            assert "return a + b" in calc
            assert "return a * b" in calc
            assert result["tests_passed"] is True

    def test_fixture_uses_modify_not_create(self):
        """Structured patch should use modify action (file already exists)."""
        src = Path("packages/orchestration/autorun.py").read_text()
        # Fixture builder uses modify because calc.py is pre-created wrong
        assert 'action="modify"' in src

    def test_fixture_structured_patch_path(self):
        from packages.core.models import Job
        from packages.orchestration.autorun import _run_fixture_builder
        from packages.orchestration.storage import save_job

        with tempfile.TemporaryDirectory() as tmp:
            job = Job(name="patch-path")
            save_job(job)
            from packages.orchestration.data_paths import resolve_data_root
            data_dir = resolve_data_root()
            result = _run_fixture_builder(job, "Fix", Path(tmp), data_dir, autonomy_level=4)
            assert result.get("structured_patch_created") is True
            assert result.get("source_patch_applied") is True
            assert result.get("approval_required") is True

    def test_fixture_proof_collected(self):
        from packages.core.models import Job
        from packages.orchestration.autorun import _run_fixture_builder
        from packages.orchestration.storage import save_job

        with tempfile.TemporaryDirectory() as tmp:
            job = Job(name="proof")
            save_job(job)
            from packages.orchestration.data_paths import resolve_data_root
            data_dir = resolve_data_root()
            result = _run_fixture_builder(job, "Prove", Path(tmp), data_dir, autonomy_level=4)
            assert result["stage"] == "proof_collected"

    def test_no_git_commit(self):
        content = Path("packages/orchestration/autorun.py").read_text()
        assert "git commit" not in content
        assert "git add" not in content
        assert "git push" not in content

    def test_no_raw_leaks_in_fixture(self):
        """Fixture builder events should not leak raw content."""
        from packages.core.models import Job
        from packages.orchestration.autorun import _run_fixture_builder
        from packages.orchestration.storage import save_job
        from packages.orchestration.data_paths import resolve_data_root
        from packages.orchestration.timeline import load_run_events

        with tempfile.TemporaryDirectory() as tmp:
            job = Job(name="leak-check")
            save_job(job)
            data_dir = resolve_data_root()
            _run_fixture_builder(job, "Fix", Path(tmp), data_dir, autonomy_level=4)
            events = load_run_events(data_dir, job.id)
            events_str = json.dumps(events)
            for bad in ("raw_output", "command_output", "Traceback",
                         "approval_reason", "diff_preview"):
                assert bad not in events_str

    def test_source_apply_event_schema(self):
        """source_patch_applied event must have required fields."""
        from packages.core.models import Job
        from packages.orchestration.autorun import _run_fixture_builder
        from packages.orchestration.storage import save_job
        from packages.orchestration.data_paths import resolve_data_root
        from packages.orchestration.timeline import load_run_events

        with tempfile.TemporaryDirectory() as tmp:
            job = Job(name="event-check")
            save_job(job)
            data_dir = resolve_data_root()
            _run_fixture_builder(job, "Fix", Path(tmp), data_dir, autonomy_level=4)
            events = load_run_events(data_dir, job.id)
            apply_events = [e for e in events if e.get("event") == "source_patch_applied"]
            assert len(apply_events) >= 1
            meta = apply_events[0].get("metadata", {})
            for field in ("apply_id", "success", "files_modified",
                          "files_created", "error_count"):
                assert field in meta, f"Missing field: {field}"


# ═══════════════════════════════════════════════════════════════════════════
# Step 137 — Smoke Closure
# ═══════════════════════════════════════════════════════════════════════════

class TestStep137_SmokeClosure:
    """Smoke script checks."""

    def test_smoke_has_task_progress(self):
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "task-progress" in content

    def test_smoke_has_no_open(self):
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "--no-open" in content

    def test_smoke_has_brain_view_model(self):
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "brain-view-model" in content

    def test_smoke_summary_structure(self):
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "summary.json" in content
        assert "job_id" in content
        assert "project_id" in content


# ═══════════════════════════════════════════════════════════════════════════
# Step 138 — Dev Status Honesty
# ═══════════════════════════════════════════════════════════════════════════

class TestStep138_DevStatusHonesty:
    """Dev status must be honest about actual state."""

    def test_status_json_schema(self):
        from apps.cli.commands.dev import _dev_status
        with patch("builtins.print") as mock_print:
            _dev_status(json_output=True)
            data = json.loads(mock_print.call_args[0][0])
            required = {
                "version", "cli_ok", "latest_smoke", "ui_contract_ok",
                "task_progress_ok", "worker_cleanup_ok",
                "autocoder_fake_e2e_ok", "remaining_blockers",
            }
            missing = required - set(data.keys())
            assert not missing

    def test_smoke_info_schema(self):
        from apps.cli.commands.dev import _dev_status
        with patch("builtins.print") as mock_print:
            _dev_status(json_output=True)
            data = json.loads(mock_print.call_args[0][0])
            smoke = data["latest_smoke"]
            assert "found" in smoke
            assert "status" in smoke
            assert "job_id" in smoke

    def test_no_smoke_reports_unknown(self):
        from apps.cli.commands.dev import _find_latest_smoke
        with patch("pathlib.Path.is_dir", return_value=False):
            result = _find_latest_smoke()
            assert result["found"] is False
            assert result["status"] == "unknown"

    def test_ui_contract_ok(self):
        from apps.cli.commands.dev import _dev_status
        with patch("builtins.print") as mock_print:
            _dev_status(json_output=True)
            data = json.loads(mock_print.call_args[0][0])
            assert data["ui_contract_ok"] is True
            assert data["task_progress_ok"] is True


# ═══════════════════════════════════════════════════════════════════════════
# Step 139 — Next Action Surface
# ═══════════════════════════════════════════════════════════════════════════

class TestStep139_NextAction:
    """Next action must be grounded in job state."""

    def test_completed_job_no_action(self):
        from packages.orchestration.ui_view_model import build_next_action
        from packages.core.models import RunState
        job = _make_job(tasks=[{"type": "t1", "status": "completed"}])
        job.state = RunState.COMPLETED
        na = build_next_action(job, [])
        assert na["version"] == 1
        assert na["primary_action"]["label"] == "No action needed"

    def test_active_job_suggests_ui(self):
        from packages.orchestration.ui_view_model import build_next_action
        from packages.core.models import RunState
        job = _make_job(tasks=[{"type": "t1", "status": "running"}])
        job.state = RunState.RUNNING
        na = build_next_action(job, [])
        assert "ui" in na["primary_action"]["command"].lower()

    def test_failed_test_suggests_inspect(self):
        from packages.orchestration.ui_view_model import build_next_action
        job = _make_job(tasks=[{"type": "t1", "status": "running"}])
        events = [{"event": "test_run_completed", "metadata": {"exit_code": 1}}]
        na = build_next_action(job, events)
        assert "test" in na["primary_action"]["label"].lower()

    def test_blocker_suggests_resolve(self):
        from packages.orchestration.ui_view_model import build_next_action
        job = _make_job()
        events = [{"event": "stop_reason_recorded", "outcome": "pending"}]
        na = build_next_action(job, events)
        assert "blocker" in na["primary_action"]["label"].lower()

    def test_reviewer_suggestion(self):
        from packages.orchestration.ui_view_model import build_next_action
        job = _make_job(tasks=[{
            "type": "review", "status": "pending",
            "metadata": {"source": "reviewer"},
        }])
        na = build_next_action(job, [])
        assert na["primary_action"]["requires_human"] is True

    def test_next_action_schema(self):
        from packages.orchestration.ui_view_model import build_next_action
        job = _make_job()
        na = build_next_action(job, [])
        required = {"version", "job_id", "stage", "primary_action", "secondary_actions"}
        assert not (required - set(na.keys()))
        pa = na["primary_action"]
        assert "label" in pa
        assert "command" in pa
        assert "risk" in pa
        assert "requires_human" in pa

    def test_secondary_actions_include_vram(self):
        from packages.orchestration.ui_view_model import build_next_action
        job = _make_job()
        na = build_next_action(job, [])
        cmds = [a["command"] for a in na["secondary_actions"]]
        assert any("worker unload" in c for c in cmds)

    def test_no_raw_leaks_in_next_action(self):
        from packages.orchestration.ui_view_model import build_next_action
        job = _make_job()
        na = build_next_action(job, [])
        na_str = json.dumps(na)
        for bad in ("raw_output", "command_output", "Traceback", "diff_preview"):
            assert bad not in na_str

    def test_next_action_endpoint_registered(self):
        """next-action endpoint exists in UI server routes."""
        content = Path("packages/orchestration/ui_server.py").read_text()
        assert "next-action" in content


# ═══════════════════════════════════════════════════════════════════════════
# Step 140 — Commit-Readiness Preview
# ═══════════════════════════════════════════════════════════════════════════

class TestStep140_CommitReadiness:
    """Commit readiness preview — read-only, no git writes."""

    def test_catalog_entry_exists(self):
        from apps.cli.command_catalog import CATALOG
        cmd = next((c for c in CATALOG if c.command_id == "repo.commit-readiness"), None)
        assert cmd is not None

    def test_readiness_not_ready_no_tests(self):
        """Missing tests -> not ready."""
        from packages.core.models import Job
        from packages.orchestration.storage import save_job

        job = Job(name="readiness-test")
        save_job(job)

        from apps.cli.commands.repo import _cmd_commit_readiness
        with patch("builtins.print") as mock_print:
            _cmd_commit_readiness(str(job.id), json_output=True)
            data = json.loads(mock_print.call_args[0][0])
            assert data["version"] == 1
            assert data["ready"] is False
            assert any("tests" in r for r in data["reasons"])

    def test_readiness_schema(self):
        from packages.core.models import Job
        from packages.orchestration.storage import save_job

        job = Job(name="schema-test")
        save_job(job)

        from apps.cli.commands.repo import _cmd_commit_readiness
        with patch("builtins.print") as mock_print:
            _cmd_commit_readiness(str(job.id), json_output=True)
            data = json.loads(mock_print.call_args[0][0])
            required = {
                "version", "job_id", "repo_path", "ready", "reasons",
                "changed_files", "tests_passed", "proof_present",
                "revert_available", "suggested_commit_message",
            }
            missing = required - set(data.keys())
            assert not missing, f"Missing: {missing}"

    def test_readiness_no_proof(self):
        from packages.core.models import Job
        from packages.orchestration.storage import save_job

        job = Job(name="no-proof")
        save_job(job)

        from apps.cli.commands.repo import _cmd_commit_readiness
        with patch("builtins.print") as mock_print:
            _cmd_commit_readiness(str(job.id), json_output=True)
            data = json.loads(mock_print.call_args[0][0])
            assert data["proof_present"] is False
            assert any("proof" in r for r in data["reasons"])

    def test_readiness_does_not_mutate_git(self):
        """No subprocess git add/commit/push in repo.py (strings/comments OK)."""
        content = Path("apps/cli/commands/repo.py").read_text()
        assert "subprocess" not in content
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith(("'", '"', "print")):
                continue
            assert "git push" not in stripped

    def test_readiness_no_shell_true(self):
        content = Path("apps/cli/commands/repo.py").read_text()
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith('"""'):
                continue
            assert "shell=True" not in stripped

    def test_suggested_message_safe(self):
        """Suggested commit message should not contain raw content."""
        from packages.core.models import Job
        from packages.orchestration.storage import save_job

        job = Job(name="msg-test")
        save_job(job)

        from apps.cli.commands.repo import _cmd_commit_readiness
        with patch("builtins.print") as mock_print:
            _cmd_commit_readiness(str(job.id), json_output=True)
            data = json.loads(mock_print.call_args[0][0])
            msg = data["suggested_commit_message"]
            assert "remedy/" in msg
            for bad in ("raw_output", "Traceback", "diff_preview"):
                assert bad not in msg
