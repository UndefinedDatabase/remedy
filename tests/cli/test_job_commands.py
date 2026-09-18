"""
Domain tests: cli/test_job_commands.py
Migrated from step-numbered test files.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch
from uuid import uuid4

from packages.core.models import RunState
from packages.orchestration.pingpong_job import JobPlan, TaskEntry

_ROOT = Path(__file__).resolve().parent.parent.parent


def _make_job():
    job = MagicMock()
    job.job_id = uuid4()
    job.job_title = "test-job"
    job.state.value = "active"
    job.tasks = []
    job.artifacts = []
    job.metadata = {}
    return job


def _make_job_s101(task_count: int = 3):
    job = MagicMock()
    job.job_id = uuid4()
    job.job_title = "test-job"
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
    job = JobPlan(job_title=name)
    if tasks:
        for t in tasks:
            task = TaskEntry(
                title=t.get("description", t.get("type", "task")),
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
    job = JobPlan(job_title=name)
    if tasks:
        for t in tasks:
            task_type = t.get("type", "readme_draft")
            inputs = dict(t.get("metadata", {}))
            inputs.setdefault("task_type", task_type)
            task = TaskEntry(
                title=t.get("description", task_type),
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
    job = JobPlan(job_title=name)
    if tasks:
        for t in tasks:
            task_type = t.get("type", "readme_draft")
            inputs = dict(t.get("metadata", {}))
            inputs.setdefault("task_type", task_type)
            task = TaskEntry(title=t.get("description", task_type), inputs=inputs)
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
        # R-0969 and DECISION F268 D17 (3): `do` runs a job, which writes the repository.
        assert cmd.may_mutate_repo is True


# ---------------------------------------------------------------------------
# Step 97 — Source Context Injection
# ---------------------------------------------------------------------------




# ---------------------------------------------------------------------------
# Step 109 — Source Context Finalization
# ---------------------------------------------------------------------------




class TestJobFocusedSingleOrigin:
    """Only the requested job_id should be is_origin=true."""

    def test_single_job_has_one_origin(self):
        """Basic case: single job graph has exactly one origin."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s122(tasks=[{"type": "t1", "status": "completed"}])
        vm = build_brain_view_model(job, [])
        origins = [n for n in vm["nodes"] if n["is_origin"]]
        assert len(origins) == 1
        assert origins[0]["id"] == str(job.job_id)

    def test_origin_is_focus_job(self):
        """Origin node id matches the passed job's id."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s122()
        vm = build_brain_view_model(job, [])
        origin = next(n for n in vm["nodes"] if n["is_origin"])
        assert origin["id"] == str(job.job_id)
        assert vm["origin"] == str(job.job_id)

    def test_child_job_not_origin(self):
        """Child/continuation job nodes must NOT be is_origin."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s122()
        child_id = str(uuid4())
        events = [{
            "event": "job_continued",
            "metadata": {
                "child_job_id": child_id,
                "origin_node_id": str(job.job_id),
            },
        }]
        vm = build_brain_view_model(job, events)
        origins = [n for n in vm["nodes"] if n["is_origin"]]
        assert len(origins) == 1, f"Expected 1 origin, got {len(origins)}"
        assert origins[0]["id"] == str(job.job_id)

    def test_child_job_demoted_zoom(self):
        """Child job nodes should be visible_from_zoom >= 5."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s122()
        child_id = str(uuid4())
        events = [{
            "event": "job_continued",
            "metadata": {
                "child_job_id": child_id,
                "origin_node_id": str(job.job_id),
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
                "origin_node_id": str(job.job_id),
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




class TestDoDirectGoalCommandRewrite:
    """remedy do '<goal>' must work via default-command rewrite."""

    def test_do_default_rewrite(self):
        """remedy do 'Make tests pass' should rewrite to do run 'Make tests pass'."""
        from apps.cli.command_catalog import get_commands_for_group

        subcmds = {c.subcommand for c in get_commands_for_group("do")}
        assert "run" in subcmds
        # "Make tests pass" is not a known subcommand
        assert "Make tests pass" not in subcmds

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

    def test_default_rewrite_dict(self):
        """Default command dict includes both ui and do."""
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
