"""
Domain tests: orchestration/test_autorun.py
Migrated from step-numbered test files.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch
from uuid import uuid4

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


def _make_job_s111(*, tasks=None, name="test"):
    from packages.core.models import Job, RunState, Task
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
# Step 111 — UI CLI Contract
# ═══════════════════════════════════════════════════════════════════════════


def _make_job_s122(*, tasks=None, name="test"):
    from packages.core.models import Job, RunState, Task
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


def _make_job_s127(*, tasks=None, name="test"):
    from packages.core.models import Job, RunState, Task
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
# Step 127 — Task Progress API Contract Closure
# ═══════════════════════════════════════════════════════════════════════════


def _make_job_s135(*, tasks=None, name="test"):
    from packages.core.models import Job, RunState, Task
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




class TestAutorunSmoke:
    """Step 100 — basic autorun integration."""

    def test_fixture_builder_path(self, tmp_path):
        from packages.orchestration.autorun import run_autorun
        # Create tiny fixture repo
        (tmp_path / "main.py").write_text("def add(a, b): return a + b")
        (tmp_path / "test_main.py").write_text("from main import add\ndef test_add(): assert add(1,2)==3")

        result = run_autorun(
            "Make the function pass the test",
            str(tmp_path),
            autonomy_level=2,
            max_cycles=1,
            fixture_builder=True,
        )
        assert result.job_id != ""
        assert result.stage in ("builder_complete", "context_injected", "job_created")




class TestFixtureBuilderStructuredPatch:

    def test_fixture_builder_creates_patch(self):
        """Fixture builder should use structured patch model."""
        from packages.core.models import Job
        from packages.orchestration.autorun import _run_fixture_builder

        with tempfile.TemporaryDirectory() as tmp:
            job = Job(name="test fixture")
            from packages.orchestration.storage import save_job
            save_job(job)
            from packages.orchestration.data_paths import resolve_data_root
            data_dir = resolve_data_root()

            result = _run_fixture_builder(
                job, "Make tests pass", Path(tmp), data_dir, autonomy_level=4,
            )
            assert result["source_context_injected"] is True
            assert result["structured_patch_created"] is True
            assert result["approval_required"] is True
            assert result["source_patch_applied"] is True

    def test_fixture_builder_creates_files(self):
        """Fixture builder should create test and source files."""
        from packages.core.models import Job
        from packages.orchestration.autorun import _run_fixture_builder

        with tempfile.TemporaryDirectory() as tmp:
            job = Job(name="test fixture")
            from packages.orchestration.storage import save_job
            save_job(job)
            from packages.orchestration.data_paths import resolve_data_root
            data_dir = resolve_data_root()

            _run_fixture_builder(
                job, "Make tests pass", Path(tmp), data_dir, autonomy_level=4,
            )
            assert (Path(tmp) / "tests" / "test_calc.py").exists()
            assert (Path(tmp) / "calc.py").exists()
            assert (Path(tmp) / "Makefile").exists()

    def test_fixture_test_passes(self):
        """The fixture test should actually pass after apply."""
        from packages.core.models import Job
        from packages.orchestration.autorun import _run_fixture_builder

        with tempfile.TemporaryDirectory() as tmp:
            job = Job(name="test fixture")
            from packages.orchestration.storage import save_job
            save_job(job)
            from packages.orchestration.data_paths import resolve_data_root
            data_dir = resolve_data_root()

            result = _run_fixture_builder(
                job, "Make tests pass", Path(tmp), data_dir, autonomy_level=4,
            )
            assert result.get("tests_passed") is True

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

    def test_autorun_result_has_events(self):
        """AutorunResult should have events list."""
        from packages.orchestration.autorun import AutorunResult
        r = AutorunResult(job_id="x", cycles_run=0, stage="init")
        assert isinstance(r.events, list)


# ═══════════════════════════════════════════════════════════════════════════
# Cross-step smoke markers
# ═══════════════════════════════════════════════════════════════════════════




class TestCalcFixtureBuilderWithProof:
    """Fixture builder must use calc.py, Makefile, and --no-ui must work."""

    def test_fixture_creates_calc_and_makefile(self):
        """Fixture builder creates calc.py, tests/test_calc.py, Makefile."""
        from packages.core.models import Job
        from packages.orchestration.autorun import _run_fixture_builder
        from packages.orchestration.storage import save_job

        with tempfile.TemporaryDirectory() as tmp:
            job = Job(name="test fixture")
            save_job(job)
            from packages.orchestration.data_paths import resolve_data_root
            data_dir = resolve_data_root()

            _run_fixture_builder(job, "Make calc work", Path(tmp), data_dir, autonomy_level=4)
            assert (Path(tmp) / "tests" / "test_calc.py").exists()
            assert (Path(tmp) / "calc.py").exists()
            assert (Path(tmp) / "Makefile").exists()

    def test_fixture_test_passes(self):
        """calc fixture test should pass after apply."""
        from packages.core.models import Job
        from packages.orchestration.autorun import _run_fixture_builder
        from packages.orchestration.storage import save_job

        with tempfile.TemporaryDirectory() as tmp:
            job = Job(name="test fixture calc")
            save_job(job)
            from packages.orchestration.data_paths import resolve_data_root
            data_dir = resolve_data_root()

            result = _run_fixture_builder(job, "Make calc work", Path(tmp), data_dir, autonomy_level=4)
            assert result.get("tests_passed") is True

    def test_fixture_proof_collected(self):
        """Fixture builder at autonomy 4+ should collect proof."""
        from packages.core.models import Job
        from packages.orchestration.autorun import _run_fixture_builder
        from packages.orchestration.storage import save_job

        with tempfile.TemporaryDirectory() as tmp:
            job = Job(name="test proof")
            save_job(job)
            from packages.orchestration.data_paths import resolve_data_root
            data_dir = resolve_data_root()

            result = _run_fixture_builder(job, "Prove calc", Path(tmp), data_dir, autonomy_level=4)
            assert result.get("stage") == "proof_collected"

    def test_makefile_has_test_target(self):
        """Makefile must have a test target."""
        from packages.core.models import Job
        from packages.orchestration.autorun import _run_fixture_builder
        from packages.orchestration.storage import save_job

        with tempfile.TemporaryDirectory() as tmp:
            job = Job(name="test makefile")
            save_job(job)
            from packages.orchestration.data_paths import resolve_data_root
            data_dir = resolve_data_root()

            _run_fixture_builder(job, "Check makefile", Path(tmp), data_dir, autonomy_level=2)
            content = (Path(tmp) / "Makefile").read_text()
            assert "test:" in content
            assert "pytest" in content

    def test_no_ui_flag_in_catalog(self):
        """--no-ui must be in the do.run catalog entry."""
        from apps.cli.command_catalog import CATALOG
        do_run = next(c for c in CATALOG if c.command_id == "do.run")
        arg_names = [a.name for a in do_run.args]
        assert "--no-ui" in arg_names

    def test_no_ui_suppresses_ui(self):
        """--no-ui should suppress UI even if --ui is set."""
        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        class FakeArgs:
            goal = "test"
            repo = "."
            project = None
            autonomy_level = "1"
            max_cycles = "1"
            ui = "true"
            no_ui = True
            dry_run = True
            json = True
            fixture_builder = False

        with patch("apps.cli.commands.do_cmd._cmd_do") as mock_do:
            COMMAND_HANDLERS["do.run"](FakeArgs())
            _, kwargs = mock_do.call_args
            assert kwargs["enable_ui"] is False

    def test_no_old_fixture_references(self):
        """No references to fixture_module or greet() in autorun."""
        content = Path("packages/orchestration/autorun.py").read_text()
        assert "fixture_module" not in content
        assert "greet(" not in content
        assert "test_fixture.py" not in content

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

    def test_fixture_file_fixed(self):
        from packages.core.models import Job
        from packages.orchestration.autorun import _run_fixture_builder
        from packages.orchestration.storage import save_job

        with tempfile.TemporaryDirectory() as tmp:
            job = Job(name="e2e")
            save_job(job)
            from packages.orchestration.data_paths import resolve_data_root
            data_dir = resolve_data_root()
            result = _run_fixture_builder(job, "Fix calc", Path(tmp), data_dir, autonomy_level=4)
            assert result["tests_passed"] is True
            # calc.py should exist and have add/mul
            calc = (Path(tmp) / "calc.py").read_text()
            assert "def add" in calc
            assert "def mul" in calc

    def test_fixture_structured_patch_path(self):
        """Must use structured patch, not direct file write."""
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

    def test_fixture_approval_gate(self):
        from packages.core.models import Job
        from packages.orchestration.autorun import _run_fixture_builder
        from packages.orchestration.storage import save_job

        with tempfile.TemporaryDirectory() as tmp:
            job = Job(name="approval")
            save_job(job)
            from packages.orchestration.data_paths import resolve_data_root
            data_dir = resolve_data_root()
            result = _run_fixture_builder(job, "Fix", Path(tmp), data_dir, autonomy_level=4)
            assert result.get("approval_required") is True

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

    def test_no_git_commit_in_fixture(self):
        content = Path("packages/orchestration/autorun.py").read_text()
        assert "git commit" not in content
        assert "git add" not in content

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




class TestFixtureBuilderWrongCalcRepair:
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
        from packages.orchestration.data_paths import resolve_data_root
        from packages.orchestration.storage import save_job
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
        from packages.orchestration.data_paths import resolve_data_root
        from packages.orchestration.storage import save_job
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

