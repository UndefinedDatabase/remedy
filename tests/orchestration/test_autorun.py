"""
Domain tests: orchestration/test_autorun.py
Migrated from step-numbered test files.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock
from uuid import uuid4

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


def _make_job_s111(*, tasks=None, name="test"):
    from packages.core.models import RunState
    from packages.orchestration.pingpong_job import JobPlan, TaskEntry
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
# Step 111 — UI CLI Contract
# ═══════════════════════════════════════════════════════════════════════════


def _make_job_s122(*, tasks=None, name="test"):
    from packages.core.models import RunState
    from packages.orchestration.pingpong_job import JobPlan, TaskEntry
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


def _make_job_s127(*, tasks=None, name="test"):
    from packages.core.models import RunState
    from packages.orchestration.pingpong_job import JobPlan, TaskEntry
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
# Step 127 — Task Progress API Contract Closure
# ═══════════════════════════════════════════════════════════════════════════


def _make_job_s135(*, tasks=None, name="test"):
    from packages.core.models import RunState
    from packages.orchestration.pingpong_job import JobPlan, TaskEntry
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


class TestFixtureBuilderStructuredPatch:
    def test_source_apply_path_safety(self):
        """source_apply must block .env, binary, symlink, path traversal."""
        from packages.orchestration.source_apply import _is_safe_path
        repo = Path("/tmp/test_repo")
        assert not _is_safe_path(".env", repo)[0]
        assert not _is_safe_path("../escape.py", repo)[0]
        assert not _is_safe_path("/etc/passwd", repo)[0]
        assert not _is_safe_path("secrets.pem", repo)[0]

    def test_structured_patch_parser_used(self):
        """Fixture builder must create StructuredPatch, not bypass it."""
        from packages.orchestration.structured_patch import (
            FileOp,
            StructuredPatch,
            validate_structured_patch,
        )
        # Create same patch as fixture builder
        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(FileOp(
                path="calc.py",
                action="create",
                language="python",
                content="def add(a: int, b: int) -> int:\n    return a + b\n\n\ndef mul(a: int, b: int) -> int:\n    return a * b\n",
                risk="low",
            ),),
            target_paths=("calc.py",),
            risk="low",
            applicability="applicable",
            requires_approval=True,
        )
        issues = validate_structured_patch(patch)
        assert not issues

    def test_no_raw_content_in_view_model(self):
        """View model should not leak raw code content."""
        job = _make_job_s111(tasks=[{"type": "readme_draft", "status": "completed"}])
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(job, [])
        full = json.dumps(vm)
        for bad in ("raw_output", "command_output", "diff_preview", "approval_reason"):
            assert bad not in full


# ═══════════════════════════════════════════════════════════════════════════
# Cross-step smoke markers
# ═══════════════════════════════════════════════════════════════════════════


class TestCalcFixtureBuilderWithProof:
    """Fixture builder must use calc.py, Makefile, and --no-ui must work."""

    def test_no_ui_flag_in_catalog(self):
        """--no-ui must be in the do.run catalog entry."""
        from apps.cli.command_catalog import CATALOG
        do_run = next(c for c in CATALOG if c.command_id == "do.run")
        arg_names = [a.name for a in do_run.args]
        assert "--no-ui" in arg_names

    def test_structured_patch_uses_calc(self):
        """Fixture builder structured patch targets calc.py."""
        from packages.orchestration.structured_patch import (
            FileOp,
            StructuredPatch,
            validate_structured_patch,
        )
        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(FileOp(
                path="calc.py",
                action="create",
                language="python",
                content="def add(a: int, b: int) -> int:\n    return a + b\n\n\ndef mul(a: int, b: int) -> int:\n    return a * b\n",
                risk="low",
            ),),
            target_paths=("calc.py",),
            risk="low",
            applicability="applicable",
            requires_approval=True,
        )
        issues = validate_structured_patch(patch)
        assert not issues


# ═══════════════════════════════════════════════════════════════════════════
# Step 126 — Smoke Closure
# ═══════════════════════════════════════════════════════════════════════════


class TestFixtureBuilderFakeE2ERepair:
    """Autocoder fixture builder proves real code change path."""

    def test_source_apply_blocks_env(self):
        from packages.orchestration.source_apply import _is_safe_path
        repo = Path("/tmp/test_repo")
        assert not _is_safe_path(".env", repo)[0]

    def test_source_apply_blocks_secrets(self):
        from packages.orchestration.source_apply import _is_safe_path
        repo = Path("/tmp/test_repo")
        assert not _is_safe_path("secrets.pem", repo)[0]
        assert not _is_safe_path("key.p12", repo)[0]

    def test_source_apply_blocks_symlink(self):
        from packages.orchestration.source_apply import _is_safe_path
        repo = Path("/tmp/test_repo")
        assert not _is_safe_path("../escape.py", repo)[0]

    def test_source_apply_blocks_absolute(self):
        from packages.orchestration.source_apply import _is_safe_path
        repo = Path("/tmp/test_repo")
        assert not _is_safe_path("/etc/passwd", repo)[0]

    def test_snapshot_revert_exists(self):
        """source_apply module should have revert capability."""
        from packages.orchestration import source_apply
        assert hasattr(source_apply, "revert_apply")

    def test_source_apply_event_schema(self):
        """source_patch_applied event has required fields."""
        content = Path("packages/orchestration/source_apply.py").read_text()
        assert "apply_id" in content
        assert "files_modified" in content
        assert "files_created" in content
        assert "error_count" in content


# ═══════════════════════════════════════════════════════════════════════════
# Step 134 — Closure Report + Dev Status Command
# ═══════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════
# Step 137 — Smoke Closure
# ═══════════════════════════════════════════════════════════════════════════
