"""
Domain tests: cli/test_job_commands.py
Migrated from step-numbered test files.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import MagicMock, patch
from unittest.mock import patch
from uuid import uuid4
import json
import os
import pytest
import subprocess
import sys
import tempfile

from packages.core.models import Job, RunState, Task

_ROOT = Path(__file__).resolve().parent.parent.parent


def _make_job():
    job = MagicMock()
    job.id = uuid4()
    job.name = "test-job"
    job.state.value = "active"
    job.tasks = []
    job.artifacts = []
    job.metadata = {}
    return job


def _make_job_s101(task_count: int = 3):
    job = MagicMock()
    job.id = uuid4()
    job.name = "test-job"
    job.state.value = "active"
    job.tasks = []
    job.artifacts = []
    job.metadata = {}
    for i in range(task_count):
        t = MagicMock()
        t.id = uuid4()
        t.task_type = "test_task"
        t.status.value = "completed" if i == 0 else "pending"
        t.metadata = {}
        job.tasks.append(t)
    return job


# ---------------------------------------------------------------------------
# Step 101 — Smoke/UX Contract Reset
# ---------------------------------------------------------------------------


def _make_job_s122(*, tasks=None, name="test"):
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
# Step 122 — Job-focused Origin Semantics
# ═══════════════════════════════════════════════════════════════════════════


def _make_job_s135(*, tasks=None, name="test"):
    from packages.core.models import Job, Task, RunState
    job = Job(name=name)
    if tasks:
        for t in tasks:
            task_type = t.get("type", "readme_draft")
            inputs = dict(t.get("metadata", {}))
            inputs.setdefault("task_type", task_type)
            task = Task(
                description=t.get("description", task_type),
                inputs=inputs,
            )
            if "status" in t:
                task.status = RunState(t["status"])
            job.tasks.append(task)
    return job


# ═══════════════════════════════════════════════════════════════════════════
# Step 135 — `remedy do "<goal>"` Direct Contract
# ═══════════════════════════════════════════════════════════════════════════


def _make_job_s141(*, tasks=None, name="test"):
    from packages.core.models import Job, Task, RunState
    job = Job(name=name)
    if tasks:
        for t in tasks:
            task_type = t.get("type", "readme_draft")
            inputs = dict(t.get("metadata", {}))
            inputs.setdefault("task_type", task_type)
            task = Task(description=t.get("description", task_type), inputs=inputs)
            if "status" in t:
                task.status = RunState(t["status"])
            job.tasks.append(task)
    return job


# ═══════════════════════════════════════════════════════════════════════════
# Step 141 — Commit-Readiness Task Summary Bugfix
# ═══════════════════════════════════════════════════════════════════════════


def _make_permitted_job():
    """Create a job with repo_generated_write permission granted."""
    job = _make_job()
    job.metadata["permissions"] = {"repo_generated_write": "allow"}
    return job


def _make_approved_job() -> tuple:
    """Create a job with permission + an approved patch intent. Returns (job, intent_id)."""
    job = _make_permitted_job()
    # Create artifact with patch intent explanation + approval
    artifact = MagicMock()
    artifact.id = uuid4()
    artifact.task_id = uuid4()
    intent_id = f"{artifact.id.hex[:8]}-0"
    artifact.metadata = {
        "patch_intent_explanations": [
            {"file": "test.py", "action": "create", "risk": "low", "reason": "test", "summary": "test"}
        ],
        "patch_intent_approvals": {
            intent_id: {
                "intent_id": intent_id,
                "state": "approved",
                "decided_at": "2026-01-01T00:00:00Z",
                "decided_by": "test",
            }
        },
    }
    job.artifacts = [artifact]
    return job, intent_id


# ---------------------------------------------------------------------------
# Step 91 — ELK Directional Layout
# ---------------------------------------------------------------------------




class TestRemedyDo:
    def test_dry_run_no_side_effects(self, tmp_path):
        from packages.orchestration.autorun import dry_run_autorun
        plan = dry_run_autorun("test goal", str(tmp_path))
        assert plan["dry_run"] is True
        assert plan["goal"] == "test goal"
        assert "phases" in plan

    def test_dry_run_phases_by_autonomy(self, tmp_path):
        from packages.orchestration.autorun import dry_run_autorun
        plan0 = dry_run_autorun("g", str(tmp_path), autonomy_level=0)
        plan4 = dry_run_autorun("g", str(tmp_path), autonomy_level=4)
        assert "run_builder" not in plan0["phases"]
        assert "run_tests" in plan4["phases"]

    def test_do_creates_job(self, tmp_path):
        from packages.orchestration.autorun import run_autorun
        result = run_autorun("test", str(tmp_path), autonomy_level=0, max_cycles=1)
        assert result.job_id != ""
        assert result.stage == "job_created"

    def test_do_respects_max_cycles(self, tmp_path):
        from packages.orchestration.autorun import run_autorun
        result = run_autorun("test", str(tmp_path), max_cycles=1, autonomy_level=0)
        assert result.cycles_run <= 1

    def test_do_command_in_catalog(self):
        from apps.cli.command_catalog import get_command
        cmd = get_command("do.run")
        assert cmd.group_id == "do"
        assert cmd.may_mutate_repo is True


# ---------------------------------------------------------------------------
# Step 97 — Source Context Injection
# ---------------------------------------------------------------------------




class TestReviewCLI:
    def test_review_group_in_catalog(self):
        from apps.cli.command_catalog import CATALOG, GROUPS
        assert "review" in GROUPS
        cmd_ids = [c.command_id for c in CATALOG]
        assert "review.run" in cmd_ids
        assert "review.list" in cmd_ids
        assert "review.accept" in cmd_ids
        assert "review.reject" in cmd_ids

    def test_review_handlers_registered(self):
        from apps.cli.commands import collect_all_handlers
        handlers = collect_all_handlers()
        assert "review.run" in handlers
        assert "review.list" in handlers
        assert "review.accept" in handlers
        assert "review.reject" in handlers

    def test_after_task_arg_in_catalog(self):
        from apps.cli.command_catalog import CATALOG
        run_cmd = next(c for c in CATALOG if c.command_id == "review.run")
        arg_names = [a.name for a in run_cmd.args]
        assert "--after-task" in arg_names


# ---------------------------------------------------------------------------
# Step 109 — Source Context Finalization
# ---------------------------------------------------------------------------




class TestStep122_JobFocusedOrigin:
    """Only the requested job_id should be is_origin=true."""

    def test_single_job_has_one_origin(self):
        """Basic case: single job graph has exactly one origin."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s122(tasks=[{"type": "t1", "status": "completed"}])
        vm = build_brain_view_model(job, [])
        origins = [n for n in vm["nodes"] if n["is_origin"]]
        assert len(origins) == 1
        assert origins[0]["id"] == str(job.id)

    def test_origin_is_focus_job(self):
        """Origin node id matches the passed job's id."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s122()
        vm = build_brain_view_model(job, [])
        origin = next(n for n in vm["nodes"] if n["is_origin"])
        assert origin["id"] == str(job.id)
        assert vm["origin"] == str(job.id)

    def test_child_job_not_origin(self):
        """Child/continuation job nodes must NOT be is_origin."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s122()
        child_id = str(uuid4())
        events = [{
            "event": "job_continued",
            "metadata": {
                "child_job_id": child_id,
                "origin_node_id": str(job.id),
            },
        }]
        vm = build_brain_view_model(job, events)
        origins = [n for n in vm["nodes"] if n["is_origin"]]
        assert len(origins) == 1, f"Expected 1 origin, got {len(origins)}"
        assert origins[0]["id"] == str(job.id)

    def test_child_job_demoted_zoom(self):
        """Child job nodes should be visible_from_zoom >= 5."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s122()
        child_id = str(uuid4())
        events = [{
            "event": "job_continued",
            "metadata": {
                "child_job_id": child_id,
                "origin_node_id": str(job.id),
            },
        }]
        vm = build_brain_view_model(job, events)
        child_nodes = [n for n in vm["nodes"]
                       if n["type"] == "job" and not n["is_origin"]]
        for cn in child_nodes:
            assert cn["visible_from_zoom"] >= 5

    def test_child_job_flow_role_continuation(self):
        """Child job flow_role must be 'continuation', not 'origin'."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s122()
        child_id = str(uuid4())
        events = [{
            "event": "job_continued",
            "metadata": {
                "child_job_id": child_id,
                "origin_node_id": str(job.id),
            },
        }]
        vm = build_brain_view_model(job, events)
        for n in vm["nodes"]:
            if n["type"] == "job" and not n["is_origin"]:
                assert n["flow_role"] == "continuation"
            elif n["type"] == "job" and n["is_origin"]:
                assert n["flow_role"] == "origin"

    def test_origin_at_zoom_0(self):
        """Origin node must be visible at zoom level 0."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s122()
        vm = build_brain_view_model(job, [])
        origin = next(n for n in vm["nodes"] if n["is_origin"])
        assert origin["visible_from_zoom"] == 0


# ═══════════════════════════════════════════════════════════════════════════
# Step 123 — View-model Hardening
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




class TestStep141_SafeTaskLabel:
    """_safe_task_label must not crash and must sanitize output."""

    def test_task_with_inputs_task_type(self):
        from apps.cli.commands.repo import _safe_task_label
        from packages.core.models import Task
        t = Task(description="d", inputs={"task_type": "readme_draft"})
        assert _safe_task_label(t) == "readme_draft"

    def test_task_with_inputs_type(self):
        from apps.cli.commands.repo import _safe_task_label
        from packages.core.models import Task
        t = Task(description="d", inputs={"type": "code_fix"})
        assert _safe_task_label(t) == "code_fix"

    def test_task_with_description_only(self):
        from apps.cli.commands.repo import _safe_task_label
        from packages.core.models import Task
        t = Task(description="Fix the broken auth module")
        assert _safe_task_label(t) == "Fix the broken auth module"

    def test_task_with_neither(self):
        from apps.cli.commands.repo import _safe_task_label
        from packages.core.models import Task
        t = Task(description="")
        assert _safe_task_label(t) == "task"

    def test_malicious_multiline_description(self):
        from apps.cli.commands.repo import _safe_task_label
        from packages.core.models import Task
        t = Task(description="Line one\nLine two\nLine three")
        label = _safe_task_label(t)
        assert "\n" not in label
        assert label == "Line one"

    def test_long_description_truncated(self):
        from apps.cli.commands.repo import _safe_task_label
        from packages.core.models import Task
        t = Task(description="A" * 200)
        label = _safe_task_label(t)
        assert len(label) <= 60

    def test_no_raw_leaks(self):
        from apps.cli.commands.repo import _safe_task_label
        from packages.core.models import Task
        t = Task(description="raw_output is bad", inputs={"task_type": "safe_label"})
        label = _safe_task_label(t)
        assert "raw_output" not in label

    def test_commit_readiness_no_crash(self):
        """The actual crash site: commit-readiness with real Task objects."""
        from packages.core.models import Job, Task
        from packages.orchestration.storage import save_job
        job = Job(name="no-crash")
        job.tasks.append(Task(description="fix stuff", inputs={"task_type": "bugfix"}))
        save_job(job)

        from apps.cli.commands.repo import _cmd_commit_readiness
        with patch("builtins.print") as mock_print:
            _cmd_commit_readiness(str(job.id), json_output=True)
            data = json.loads(mock_print.call_args[0][0])
            assert "suggested_commit_message" in data
            assert "remedy/" in data["suggested_commit_message"]
            assert "bugfix" in data["suggested_commit_message"]

    def test_commit_readiness_no_task_type_attr(self):
        """Task objects must not require .task_type attribute."""
        from packages.core.models import Task
        t = Task(description="some work")
        assert not hasattr(t, "task_type") or getattr(t, "task_type", None) is None


# ═══════════════════════════════════════════════════════════════════════════
# Step 142 — Commit-Readiness Contract Hardening
# ═══════════════════════════════════════════════════════════════════════════




class TestGitStatusCLI:
    def test_repo_status_help(self):
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", "repo", "status", "--help"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0
        assert "status" in result.stdout.lower()

    def test_repo_status_json(self):
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", "repo", "status", "--json"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["version"] == 1
        assert data["is_git_repo"] is True

