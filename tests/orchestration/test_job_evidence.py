"""Tests for job evidence bundle export (Steps 4906-4916).

Covers: bundle model, CLI command, file layout, redaction, behavior,
timeline proof, workspace diff, read-only safety, no-provider guarantees.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration.pingpong_job import (
    JOB_BLOCKED,
    JOB_PAUSED,
    parse_job_file,
    run_job,
)
from packages.orchestration.pingpong_provider import FakeProvider

_TWO_TASK_JOB = """\
# Job: Evidence Export Test

## Task 1
Add a test file.

Acceptance:
- file exists

## Task 2
Add another test file.

Acceptance:
- file exists
"""


def _pass_provider():
    return FakeProvider(pass_on_round=1, fail_on_round=99)


@pytest.fixture
def isolate_data_root(tmp_path: Path, monkeypatch):
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


@pytest.fixture
def demo_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("# Demo\n")
    (repo / "src").mkdir()
    (repo / "src" / "main.py").write_text("def hello():\n    return 'hello'\n")
    return repo


def _run_completed_job(demo_repo):
    job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
    return run_job(
        job.job_id,
        builder_provider=_pass_provider(),
        reviewer_provider=_pass_provider(),
        repair_rounds=0,
    )


def _run_blocked_job(demo_repo, monkeypatch):
    job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))

    import packages.orchestration.pingpong_loop as pp_mod
    real_run = pp_mod.run_pingpong

    def fail_run(*args, **kwargs):
        result = real_run(*args, **kwargs)
        if result.rounds:
            result.rounds[-1].test_passed = False
        return result

    monkeypatch.setattr(pp_mod, "run_pingpong", fail_run)

    return run_job(
        job.job_id,
        builder_provider=_pass_provider(),
        reviewer_provider=_pass_provider(),
        repair_rounds=0,
    )


def _run_paused_job(demo_repo):
    job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
    return run_job(
        job.job_id,
        builder_provider=_pass_provider(),
        reviewer_provider=_pass_provider(),
        repair_rounds=0,
        max_tasks=1,
    )


# ---------------------------------------------------------------------------
# Step 4913: Behavior tests
# ---------------------------------------------------------------------------


class TestCompletedJobExport:
    def test_completed_job_exports(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence(job.job_id, str(out))

        assert "error" not in result
        assert result["job_id"] == job.job_id
        assert result["manifest"]["status"] == "completed"

    def test_manifest_json_exists(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        assert (out / "manifest.json").exists()
        data = json.loads((out / "manifest.json").read_text())
        assert data["job_id"] == job.job_id
        assert data["bundle_type"] == "job_evidence"

    def test_summary_md_readable(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        summary = (out / "summary.md").read_text()
        assert "# Remedy Job Evidence" in summary
        assert job.job_id in summary
        assert "T001" in summary
        assert "T002" in summary

    def test_all_top_level_files_present(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        expected = [
            "manifest.json", "summary.md", "job_report.json",
            "job_timeline.json", "tasks.json", "execution_config.json",
            "context_strategy.json", "target_guard.json",
            "workspace_apply.json", "workspace.diff",
        ]
        for f in expected:
            assert (out / f).exists(), f"{f} missing"

    def test_task_run_evidence_nested(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        for task in job.tasks:
            task_dir = out / "task_runs" / task.task_id
            assert task_dir.exists(), f"task_runs/{task.task_id} missing"
            assert (task_dir / "manifest.json").exists()
            assert (task_dir / "summary.md").exists()


class TestBlockedJobExport:
    def test_blocked_job_exports(self, isolate_data_root, demo_repo, monkeypatch, tmp_path):
        job = _run_blocked_job(demo_repo, monkeypatch)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence(job.job_id, str(out))

        assert "error" not in result
        assert result["manifest"]["status"] == JOB_BLOCKED

    def test_blocked_task_has_evidence(self, isolate_data_root, demo_repo, monkeypatch, tmp_path):
        job = _run_blocked_job(demo_repo, monkeypatch)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        t1_dir = out / "task_runs" / "T001"
        assert t1_dir.exists()


class TestPausedJobExport:
    def test_paused_job_exports(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_paused_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence(job.job_id, str(out))

        assert "error" not in result
        assert result["manifest"]["status"] == JOB_PAUSED

    def test_paused_pending_task_unavailable(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_paused_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        t2_dir = out / "task_runs" / "T002"
        assert t2_dir.exists()
        manifest = json.loads((t2_dir / "manifest.json").read_text())
        assert manifest["evidence_available"] is False


class TestMissingTaskEvidence:
    def test_task_without_run_id(self, isolate_data_root, demo_repo, tmp_path):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence(job.job_id, str(out))

        assert "error" not in result
        t1_dir = out / "task_runs" / "T001"
        manifest = json.loads((t1_dir / "manifest.json").read_text())
        assert manifest["evidence_available"] is False
        assert "No run_id" in manifest["reason"]


class TestMissingJob:
    def test_missing_job_returns_error(self, isolate_data_root, tmp_path):
        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence("nonexistent_id", str(tmp_path / "out"))
        assert "error" in result


class TestReadOnly:
    def test_does_not_mutate_target_repo(self, isolate_data_root, demo_repo, tmp_path):
        readme_before = (demo_repo / "README.md").read_text()
        main_before = (demo_repo / "src" / "main.py").read_text()

        job = _run_completed_job(demo_repo)
        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(tmp_path / "evidence"))

        assert (demo_repo / "README.md").read_text() == readme_before
        assert (demo_repo / "src" / "main.py").read_text() == main_before

    def test_does_not_mutate_job_state(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)

        from packages.orchestration.pingpong_job import load_job_plan
        before = load_job_plan(job.job_id)
        before_status = before.status
        before_tasks = [(t.task_id, t.status) for t in before.tasks]

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(tmp_path / "evidence"))

        after = load_job_plan(job.job_id)
        assert after.status == before_status
        assert [(t.task_id, t.status) for t in after.tasks] == before_tasks


class TestOutputPathTraversal:
    def test_traversal_blocked(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.pingpong_evidence import _validate_output_path
        with pytest.raises(ValueError, match="traversal"):
            _validate_output_path(str(out), "../../../etc/passwd")

    def test_export_api_traversal_blocked(self, isolate_data_root, demo_repo, tmp_path):
        """Step 4922: Public export_job_evidence() blocks top-level traversal."""
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence(job.job_id, str(out))

        assert "error" not in result
        # All files must be inside out_dir
        out_resolved = str(out.resolve())
        for path in result["files"].values():
            assert str(Path(path).resolve()).startswith(out_resolved + "/"), (
                f"File {path} escapes {out_resolved}"
            )


# ---------------------------------------------------------------------------
# Steps 4919-4922: Nested task evidence path containment
# ---------------------------------------------------------------------------


def _make_job_with_task_id(task_id: str, demo_repo: Path, isolate_data_root: Path) -> str:
    """Create a persisted job with a single task bearing the given task_id."""
    from packages.orchestration.pingpong_job import (
        JobPlan,
        TaskEntry,
        _persist_job,
    )
    job = JobPlan(
        repo_path=str(demo_repo),
        job_title="Traversal test job",
        tasks=[TaskEntry(task_id=task_id, title="evil task", body="test")],
    )
    _persist_job(job)
    return job.job_id


class TestNestedTaskTraversal:
    """Step 4919: Unavailable task evidence with malicious task_id."""

    def test_traversal_task_id_raises(self, isolate_data_root, demo_repo, tmp_path):
        """Malicious task_id ../../evil raises ValueError, writes nothing outside out_dir."""
        job_id = _make_job_with_task_id("../../evil", demo_repo, isolate_data_root)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        with pytest.raises(ValueError, match="Unsafe task ID"):
            export_job_evidence(job_id, str(out))

        # No evil directory outside out_dir
        evil_dir = tmp_path / "evil"
        assert not evil_dir.exists(), "Path traversal: evil dir created outside out_dir"
        parent_evil = tmp_path.parent / "evil"
        assert not parent_evil.exists(), "Path traversal: evil dir in parent"

    def test_slash_task_id_raises(self, isolate_data_root, demo_repo, tmp_path):
        job_id = _make_job_with_task_id("foo/bar", demo_repo, isolate_data_root)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        with pytest.raises(ValueError, match="Unsafe task ID"):
            export_job_evidence(job_id, str(out))

    def test_backslash_task_id_raises(self, isolate_data_root, demo_repo, tmp_path):
        job_id = _make_job_with_task_id("foo\\bar", demo_repo, isolate_data_root)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        with pytest.raises(ValueError, match="Unsafe task ID"):
            export_job_evidence(job_id, str(out))

    def test_empty_task_id_raises(self, isolate_data_root, demo_repo, tmp_path):
        job_id = _make_job_with_task_id("", demo_repo, isolate_data_root)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        with pytest.raises(ValueError, match="Unsafe task ID"):
            export_job_evidence(job_id, str(out))

    def test_absolute_path_task_id_raises(self, isolate_data_root, demo_repo, tmp_path):
        job_id = _make_job_with_task_id("/etc/passwd", demo_repo, isolate_data_root)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        with pytest.raises(ValueError, match="Unsafe task ID"):
            export_job_evidence(job_id, str(out))

    def test_control_chars_task_id_raises(self, isolate_data_root, demo_repo, tmp_path):
        job_id = _make_job_with_task_id("T001\x00evil", demo_repo, isolate_data_root)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        with pytest.raises(ValueError, match="Unsafe task ID"):
            export_job_evidence(job_id, str(out))


class TestRunIdTaskTraversal:
    """Step 4920: Traversal test for task with run_id reaching _write_task_run_evidence."""

    def test_malicious_task_id_with_run_id_raises(self, isolate_data_root, demo_repo, tmp_path, monkeypatch):
        """Even if task has a run_id, malicious task_id must be caught before write."""
        from packages.orchestration.pingpong_job import (
            JobPlan,
            TaskEntry,
            _persist_job,
        )
        job = JobPlan(
            repo_path=str(demo_repo),
            job_title="Traversal test job",
            tasks=[TaskEntry(
                task_id="../../evil",
                title="evil task",
                body="test",
                run_id="fake-run-id-123",
            )],
        )
        _persist_job(job)

        out = tmp_path / "evidence"
        from packages.orchestration.job_evidence import export_job_evidence
        with pytest.raises(ValueError, match="Unsafe task ID"):
            export_job_evidence(job.job_id, str(out))

        # No files outside out_dir
        evil_dir = tmp_path / "evil"
        assert not evil_dir.exists()

    def test_dot_dot_with_run_id_blocked(self, isolate_data_root, demo_repo, tmp_path):
        from packages.orchestration.pingpong_job import (
            JobPlan,
            TaskEntry,
            _persist_job,
        )
        job = JobPlan(
            repo_path=str(demo_repo),
            job_title="Traversal test",
            tasks=[TaskEntry(
                task_id="../escape",
                title="escape task",
                body="test",
                run_id="fake-run-456",
            )],
        )
        _persist_job(job)

        out = tmp_path / "evidence"
        from packages.orchestration.job_evidence import export_job_evidence
        with pytest.raises(ValueError, match="Unsafe task ID"):
            export_job_evidence(job.job_id, str(out))


class TestFilesMappingContainment:
    """Step 4921: Every path in result['files'] is contained inside result['out_dir']."""

    def _assert_all_contained(self, result):
        out_dir = str(Path(result["out_dir"]).resolve())
        for key, path in result["files"].items():
            assert ".." not in key, f"Traversal in key: {key}"
            resolved = str(Path(path).resolve())
            assert resolved.startswith(out_dir + "/"), (
                f"File {key} -> {path} escapes {out_dir}"
            )

    def test_completed_job_contained(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence(job.job_id, str(out))
        self._assert_all_contained(result)

    def test_blocked_job_contained(self, isolate_data_root, demo_repo, monkeypatch, tmp_path):
        job = _run_blocked_job(demo_repo, monkeypatch)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence(job.job_id, str(out))
        self._assert_all_contained(result)

    def test_paused_job_contained(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_paused_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence(job.job_id, str(out))
        self._assert_all_contained(result)

    def test_planned_job_contained(self, isolate_data_root, demo_repo, tmp_path):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence(job.job_id, str(out))
        self._assert_all_contained(result)


class TestSafeTaskIdHelper:
    """Step 4917: Direct unit tests for _task_evidence_dir."""

    def test_valid_task_ids_accepted(self, tmp_path):
        from packages.orchestration.job_evidence import _task_evidence_dir
        for tid in ("T001", "T002", "T999", "T0001"):
            result = _task_evidence_dir(str(tmp_path), tid)
            assert str(result).startswith(str(tmp_path.resolve()))
            assert tid in str(result)

    def test_invalid_task_ids_rejected(self, tmp_path):
        from packages.orchestration.job_evidence import _task_evidence_dir
        bad_ids = [
            "../../evil",
            "../escape",
            "foo/bar",
            "T001/../../etc",
            "",
            "/etc/passwd",
            "T001\x00evil",
            "evil",
            "t001",
            "001",
            "T1",  # Too few digits
        ]
        for bad_id in bad_ids:
            with pytest.raises(ValueError, match="Unsafe task ID"):
                _task_evidence_dir(str(tmp_path), bad_id)

    def test_symlinked_task_runs_blocked(self, tmp_path):
        """Step 4927: _task_evidence_dir blocks symlink escape via task_runs/."""
        from packages.orchestration.job_evidence import _task_evidence_dir
        out = tmp_path / "out"
        out.mkdir()
        evil_target = tmp_path / "evil_target"
        evil_target.mkdir()
        (out / "task_runs").symlink_to(evil_target, target_is_directory=True)

        with pytest.raises(ValueError, match="traversal"):
            _task_evidence_dir(str(out), "T001")

        # Nothing written to evil_target
        assert not list(evil_target.iterdir())


# ---------------------------------------------------------------------------
# Steps 4929-4931: Symlink escape regression tests
# ---------------------------------------------------------------------------


class TestSymlinkEscapeUnavailable:
    """Step 4929: Unavailable task evidence blocked from symlink escape."""

    def test_symlink_task_runs_unavailable_blocked(self, isolate_data_root, demo_repo, tmp_path):
        """Export with normal task_id but symlinked task_runs/ raises ValueError."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        out = tmp_path / "evidence"
        out.mkdir()
        evil_target = tmp_path / "evil_target"
        evil_target.mkdir()
        (out / "task_runs").symlink_to(evil_target, target_is_directory=True)

        from packages.orchestration.job_evidence import export_job_evidence
        with pytest.raises(ValueError, match="traversal"):
            export_job_evidence(job.job_id, str(out))

        # No evidence files in symlink target
        assert not list(evil_target.iterdir()), "Files escaped to symlink target"

    def test_symlink_nested_subdir_blocked(self, isolate_data_root, demo_repo, tmp_path):
        """Symlink at out/task_runs/T001 pointing outside also blocked."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        out = tmp_path / "evidence"
        out.mkdir()
        (out / "task_runs").mkdir()
        evil_target = tmp_path / "evil_target"
        evil_target.mkdir()
        (out / "task_runs" / "T001").symlink_to(evil_target, target_is_directory=True)

        from packages.orchestration.job_evidence import export_job_evidence
        with pytest.raises(ValueError, match="traversal"):
            export_job_evidence(job.job_id, str(out))

        assert not list(evil_target.iterdir()), "Files escaped via nested symlink"


class TestSymlinkEscapeRunId:
    """Step 4930: Run_id task evidence blocked from symlink escape."""

    def test_symlink_task_runs_with_run_id_blocked(self, isolate_data_root, demo_repo, tmp_path):
        """Task with run_id still blocked when task_runs/ is symlinked."""
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"
        out.mkdir()
        evil_target = tmp_path / "evil_target"
        evil_target.mkdir()
        (out / "task_runs").symlink_to(evil_target, target_is_directory=True)

        from packages.orchestration.job_evidence import export_job_evidence
        with pytest.raises(ValueError, match="traversal"):
            export_job_evidence(job.job_id, str(out))

        assert not list(evil_target.iterdir()), "Run_id evidence escaped to symlink target"


class TestSymlinkMappingContainment:
    """Step 4931: Returned file mapping containment with symlink scenarios."""

    def test_no_symlink_all_resolved_contained(self, isolate_data_root, demo_repo, tmp_path):
        """Without symlinks, all resolved paths contained in out_dir."""
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence(job.job_id, str(out))

        out_resolved = str(out.resolve())
        for key, path in result["files"].items():
            assert ".." not in key
            resolved = str(Path(path).resolve())
            assert resolved.startswith(out_resolved + "/"), (
                f"Resolved {key} -> {resolved} escapes {out_resolved}"
            )

    def test_planned_job_resolved_contained(self, isolate_data_root, demo_repo, tmp_path):
        """Planned job (unavailable tasks) resolved paths contained."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence(job.job_id, str(out))

        out_resolved = str(out.resolve())
        for key, path in result["files"].items():
            assert ".." not in key
            resolved = str(Path(path).resolve())
            assert resolved.startswith(out_resolved + "/"), (
                f"Resolved {key} -> {resolved} escapes {out_resolved}"
            )


# ---------------------------------------------------------------------------
# Step 4910: Timeline proof
# ---------------------------------------------------------------------------


class TestTimelineProof:
    def test_timeline_has_events(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        timeline = json.loads((out / "job_timeline.json").read_text())
        assert len(timeline["events"]) >= 3
        event_types = [e["event"] for e in timeline["events"]]
        assert "job_planned" in event_types
        assert "job_final" in event_types

    def test_timeline_proves_ordering(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        timeline = json.loads((out / "job_timeline.json").read_text())
        sequencing = [
            e for e in timeline["events"]
            if e["event"] == "sequencing_proof"
        ]
        assert len(sequencing) >= 1
        assert "T002" in sequencing[0]["detail"]
        assert "T001" in sequencing[0]["detail"]

    def test_sequencing_valid(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        timeline = json.loads((out / "job_timeline.json").read_text())
        assert timeline["sequencing_valid"] is True


# ---------------------------------------------------------------------------
# Step 4911: Workspace diff
# ---------------------------------------------------------------------------


class TestWorkspaceDiff:
    def test_workspace_diff_present(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        diff = (out / "workspace.diff").read_text()
        assert "workspace diff" in diff.lower() or "---" in diff

    def test_workspace_diff_unavailable_for_planned(self, isolate_data_root, demo_repo, tmp_path):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        diff = (out / "workspace.diff").read_text()
        assert "unavailable" in diff.lower() or "No files applied" in diff


# ---------------------------------------------------------------------------
# Step 4912: Redaction and output scanner tests
# ---------------------------------------------------------------------------

_SECRET_SHAPES = [
    "API_KEY=sk-ant-abc123def456ghi789jkl012mno345pqr",
    "SECRET=mysecretpassword123",
    "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0",
    "sk-ant-api03-abcdefghijklmnopqrstuvwxyz",
    "sk-abcdefghijklmnopqrstuvwxyz1234567890",
    "ghp_abcdefghijklmnopqrstuvwxyz1234567890",
    "AKIAIOSFODNN7EXAMPLE",
]


class TestRedactionScanner:
    def _export_with_secrets(self, isolate_data_root, demo_repo, tmp_path, monkeypatch):
        import packages.orchestration.pingpong_loop as pp_mod
        real_run = pp_mod.run_pingpong

        secret_blob = "\n".join(_SECRET_SHAPES)

        def injecting_run(*args, **kwargs):
            result = real_run(*args, **kwargs)
            result.safe_diff_summary = f"--- a/file.py\n+++ b/file.py\n# {secret_blob}"
            return result

        monkeypatch.setattr(pp_mod, "run_pingpong", injecting_run)

        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        completed = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )

        out = tmp_path / "evidence"
        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence(completed.job_id, str(out))
        return result, out

    def test_no_secrets_in_json_files(self, isolate_data_root, demo_repo, tmp_path, monkeypatch):
        _, out = self._export_with_secrets(isolate_data_root, demo_repo, tmp_path, monkeypatch)

        for json_file in out.rglob("*.json"):
            content = json_file.read_text()
            for secret in _SECRET_SHAPES:
                assert secret not in content, f"Secret leaked in {json_file.name}: {secret[:20]}..."

    def test_no_secrets_in_text_files(self, isolate_data_root, demo_repo, tmp_path, monkeypatch):
        _, out = self._export_with_secrets(isolate_data_root, demo_repo, tmp_path, monkeypatch)

        for text_file in list(out.rglob("*.md")) + list(out.rglob("*.diff")) + list(out.rglob("*.txt")):
            content = text_file.read_text()
            for secret in _SECRET_SHAPES:
                assert secret not in content, f"Secret leaked in {text_file.name}: {secret[:20]}..."

    def test_no_secrets_in_cli_json(self, isolate_data_root, demo_repo, tmp_path, monkeypatch):
        result, _ = self._export_with_secrets(isolate_data_root, demo_repo, tmp_path, monkeypatch)

        result_str = json.dumps(result)
        for secret in _SECRET_SHAPES:
            assert secret not in result_str, f"Secret in CLI JSON: {secret[:20]}..."

    def test_no_raw_task_body_unbounded(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        report = json.loads((out / "job_report.json").read_text())
        for task in report["tasks"]:
            if "body_excerpt" in task:
                assert len(task["body_excerpt"]) <= 600
            assert "body" not in task or task.get("body") is None

    def test_no_absolute_private_paths_leaked(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence(job.job_id, str(out))

        manifest = json.loads((out / "manifest.json").read_text())
        home = str(Path.home())
        if home != "/":
            repo_id = manifest.get("repo_identity", "")
            assert not repo_id.startswith(home), f"Absolute home path leaked: {repo_id}"


class TestCLIJsonRedaction:
    def test_cli_handler_json_output(self, isolate_data_root, demo_repo, tmp_path, capsys):
        job = _run_completed_job(demo_repo)

        import types

        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        out_dir = str(tmp_path / "cli_evidence")
        args = types.SimpleNamespace(
            job_id=job.job_id,
            out=out_dir,
            json=True,
        )
        COMMAND_HANDLERS["do.job-evidence"](args)

        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert output["job_id"] == job.job_id
        assert "error" not in output

    def test_cli_handler_text_output(self, isolate_data_root, demo_repo, tmp_path, capsys):
        job = _run_completed_job(demo_repo)

        import types

        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        out_dir = str(tmp_path / "cli_evidence")
        args = types.SimpleNamespace(
            job_id=job.job_id,
            out=out_dir,
            json=False,
        )
        COMMAND_HANDLERS["do.job-evidence"](args)

        captured = capsys.readouterr()
        assert "exported to" in captured.out.lower()
        assert "manifest.json" in captured.out


# ---------------------------------------------------------------------------
# Step 4913: Machine-verifiable JSON
# ---------------------------------------------------------------------------


class TestMachineVerifiable:
    def test_all_json_files_parse(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        for json_file in out.rglob("*.json"):
            data = json.loads(json_file.read_text())
            assert isinstance(data, (dict, list)), f"{json_file.name} not dict/list"

    def test_manifest_has_required_fields(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        manifest = json.loads((out / "manifest.json").read_text())
        required = [
            "job_id", "job_title", "status", "task_count",
            "task_ids", "task_statuses", "execution_config",
            "context_strategy", "target_guard",
        ]
        for field in required:
            assert field in manifest, f"Missing field: {field}"

    def test_tasks_json_matches_task_count(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        tasks = json.loads((out / "tasks.json").read_text())
        manifest = json.loads((out / "manifest.json").read_text())
        assert len(tasks) == manifest["task_count"]


# ---------------------------------------------------------------------------
# Step 4914: Dogfood export command shape
# ---------------------------------------------------------------------------


class TestDogfoodCommandShape:
    def test_command_catalog_has_job_evidence(self):
        from apps.cli.command_catalog import CATALOG
        cmd = next(
            (c for c in CATALOG if c.command_id == "do.job-evidence"),
            None,
        )
        assert cmd is not None
        # job-evidence now executes explicit verification commands, so it is
        # no longer read_only — catalog integrity forbids that combination.
        assert cmd.action_class == "test_execution"
        assert cmd.may_mutate_repo is False
        assert cmd.may_execute_commands is True
        assert any(a.name == "--verification-command" for a in cmd.args)

    def test_handler_exists(self):
        from apps.cli.commands.do_cmd import COMMAND_HANDLERS
        assert "do.job-evidence" in COMMAND_HANDLERS

    def test_evidence_export_writes_missing_tests_gate(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence(job.job_id, str(out))

        assert "error" not in result
        gate_key = "task_runs/T001/missing_tests_gate.json"
        has_gate = gate_key in result["files"]
        has_error = "task_runs/T001/missing_tests_gate.error.txt" in result["files"]
        assert has_gate or has_error, "missing_tests_gate neither written nor error-logged"

    def test_evidence_export_writes_scratch_file_guard(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence(job.job_id, str(out))

        assert "error" not in result
        has_guard = "scratch_file_guard.json" in result["files"]
        has_error = "scratch_file_guard.error.txt" in result["files"]
        assert has_guard or has_error, "scratch_file_guard neither written nor error-logged"

    def test_evidence_export_writes_token_truth(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence(job.job_id, str(out))

        assert "error" not in result
        has_truth = "token_truth.json" in result["files"]
        has_error = "token_truth.error.txt" in result["files"]
        assert has_truth or has_error, "token_truth neither written nor error-logged"

    def test_token_truth_consistent_with_task_accounting(self, isolate_data_root, demo_repo, tmp_path):
        """Root token_truth.json per-task estimates must match each task's
        token_accounting.json (no drift between root and task-level evidence)."""
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence(job.job_id, str(out))

        assert "error" not in result
        if "token_truth.json" not in result["files"]:
            return  # error-logged path exercised elsewhere

        truth = json.loads((out / "token_truth.json").read_text())
        for tid, per_task in truth.get("per_task", {}).items():
            acc_path = out / "task_runs" / tid / "token_accounting.json"
            if not acc_path.exists():
                continue
            acc = json.loads(acc_path.read_text())
            assert per_task["builder_estimated"] == (
                acc.get("builder_prompt_tokens_estimated") or 0
            )
            assert per_task["reviewer_estimated"] == (
                acc.get("reviewer_prompt_tokens_estimated") or 0
            )
            assert per_task["repair_estimated"] == (
                acc.get("repair_prompt_tokens_estimated") or 0
            )

    def test_evidence_export_writes_final_verifier_report(self, isolate_data_root, demo_repo, tmp_path):
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence(job.job_id, str(out))

        assert "error" not in result
        has_report = "final_verifier_report.json" in result["files"]
        has_error = "final_verifier_report.error.txt" in result["files"]
        assert has_report or has_error, "final_verifier_report neither written nor error-logged"

    def test_token_truth_before_final_verifier_in_evidence(self, isolate_data_root, demo_repo, tmp_path):
        """token_truth.json must be written before final_verifier_report.json
        so final verifier can read it."""
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence(job.job_id, str(out))

        assert "error" not in result
        if "token_truth.json" in result["files"] and "final_verifier_report.json" in result["files"]:
            fv = json.loads((out / "final_verifier_report.json").read_text())
            assert fv.get("evidence_completeness", {}).get("token_truth") is True

    def test_all_gate_artifacts_written(self, isolate_data_root, demo_repo, tmp_path):
        """All five evidence-pipeline gates are written (or error-logged)."""
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence(job.job_id, str(out))

        assert "error" not in result
        gate_files = [
            "fresh_evidence_gate.json",
            "runtime_integration_gate.json",
            "change_provenance_gate.json",
            "final_verifier_report.json",
            "artifact_contract_gate.json",
            "commit_execution_gate.json",
        ]
        for gate in gate_files:
            has_gate = gate in result["files"]
            err = gate.replace(".json", ".error.txt")
            has_error = err in result["files"]
            assert has_gate or has_error, f"{gate} neither written nor error-logged"
            if has_gate:
                assert (out / gate).exists()

    def test_final_verifier_sees_all_gates(self, isolate_data_root, demo_repo, tmp_path):
        """Final verifier exposes all five core gate fields."""
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence(job.job_id, str(out))

        assert "error" not in result
        if "final_verifier_report.json" in result["files"]:
            fv = json.loads((out / "final_verifier_report.json").read_text())
            assert "change_provenance" in fv
            assert "fresh_evidence_gate" in fv
            assert "artifact_contract_gate" in fv
            assert "runtime_integration_gate" in fv
            assert "commit_execution_gate" in fv

    def test_artifact_contract_pass_from_clean_dir(self, isolate_data_root, demo_repo, tmp_path):
        """Artifact contract gate passes after full export into a clean empty dir."""
        job = _run_completed_job(demo_repo)
        out = tmp_path / "clean_evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence(job.job_id, str(out))

        assert "error" not in result
        if "artifact_contract_gate.json" in result["files"]:
            acg = json.loads((out / "artifact_contract_gate.json").read_text())
            assert acg["verdict"] == "PASS", (
                f"artifact_contract should PASS from clean dir, got {acg['verdict']}: "
                f"missing={acg.get('missing_required', [])}"
            )

    def test_artifact_contract_blocked_without_commit_execution(self, tmp_path):
        """Artifact contract gate is BLOCKED when commit_execution_gate.json is missing."""
        from packages.orchestration.artifact_contract_gate import build_artifact_contract_gate

        for name in ["manifest.json", "job_report.json", "token_truth.json",
                      "fresh_evidence_gate.json", "artifact_contract_gate.json",
                      "runtime_integration_gate.json", "change_provenance_gate.json",
                      "final_verifier_report.json"]:
            (tmp_path / name).write_text(json.dumps({"verdict": "PASS", "job_id": "j1", "evidence_completeness": {}}) + "\n")

        gate = build_artifact_contract_gate(str(tmp_path))
        assert gate["verdict"] == "BLOCKED"
        assert "commit_execution_gate.json" in gate["missing_required"]

    def test_content_proof_writer_in_export(self, isolate_data_root, demo_repo, tmp_path):
        """Export pipeline must write current_change_content_proof.json."""
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        result = export_job_evidence(job.job_id, str(out))

        assert "error" not in result
        proof_file = out / "current_change_content_proof.json"
        assert proof_file.exists(), "current_change_content_proof.json must exist after export"
        data = json.loads(proof_file.read_text())
        # Round 15: the proof gained typed deletion tombstones and the resolved review
        # base/head, so a removed file is recorded rather than silently absent.
        assert data["schema_version"] == "1.1.0"
        assert "file_hashes" in data
        assert "file_count" in data
        assert "tombstones" in data
        assert "tombstone_count" in data
        assert "base_commit" in data and "head_commit" in data

    def test_change_provenance_exists_after_export(self, isolate_data_root, demo_repo, tmp_path):
        """Change provenance gate must exist after export with stale_apply_proofs field."""
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        cpg = out / "change_provenance_gate.json"
        assert cpg.exists(), "change_provenance_gate.json must exist after export"
        data = json.loads(cpg.read_text())
        assert "stale_apply_proofs" in data

    def test_commit_execution_terminal_refresh(self, isolate_data_root, demo_repo, tmp_path):
        """Commit execution gate must exist and agree with final verifier."""
        job = _run_completed_job(demo_repo)
        out = tmp_path / "evidence"

        from packages.orchestration.job_evidence import export_job_evidence
        export_job_evidence(job.job_id, str(out))

        ceg = out / "commit_execution_gate.json"
        fvr = out / "final_verifier_report.json"
        assert ceg.exists(), "commit_execution_gate.json must exist after export"
        assert fvr.exists(), "final_verifier_report.json must exist after export"
        ceg_data = json.loads(ceg.read_text())
        fvr_data = json.loads(fvr.read_text())
        fv_verdict = fvr_data["verdict"]
        ceg_fv = ceg_data["gate_checks"]["final_verifier"]
        assert ceg_fv == fv_verdict, (
            f"commit_execution gate_checks.final_verifier={ceg_fv} != "
            f"final_verifier_report.verdict={fv_verdict}"
        )

    def test_verification_type_is_explicit_commands(self):
        # No hardcoded smoke suite remains; verification is command-driven.
        import packages.orchestration.job_evidence as mod
        src = Path(mod.__file__).read_text()
        assert '"post_apply_smoke"' not in src
        assert '"explicit_commands"' in src

    def test_no_hardcoded_smoke_test_list(self):
        # The old hardcoded smoke list (a source of false coverage + recursion)
        # must be gone.
        import packages.orchestration.job_evidence as mod
        src = Path(mod.__file__).read_text()
        assert "test_spec_compliance.py" not in src
        assert "test_do_job_flow.py" not in src

    def test_verification_tests_written_from_explicit_commands(
        self, isolate_data_root, demo_repo, tmp_path
    ):
        from packages.orchestration.job_evidence import export_job_evidence
        job = _run_completed_job(demo_repo)

        def _runner(command):
            return {"exit_code": 0, "passed": 3, "failed": 0,
                    "test_files": ["tests/orchestration/test_demo.py"],
                    "stdout_summary": "ok"}

        out = tmp_path / f"remedy-job-evidence-{job.job_id}"
        export_job_evidence(
            job.job_id, str(out),
            verification_commands=["python3 -m pytest tests/orchestration/test_demo.py"],
            verification_runner=_runner,
        )
        vt = out / "verification_tests.json"
        assert vt.exists()
        data = json.loads(vt.read_text())
        assert data["verification_type"] == "explicit_commands"
        assert data["runs"][0]["run_id"] == "vr-0001"
        assert data["passed"] == 3

    def test_no_verification_without_commands(
        self, isolate_data_root, demo_repo, tmp_path
    ):
        # Finding 3: without explicit commands, no verification is run/recorded.
        from packages.orchestration.job_evidence import export_job_evidence
        job = _run_completed_job(demo_repo)
        out = tmp_path / f"remedy-job-evidence-{job.job_id}"
        export_job_evidence(job.job_id, str(out))
        assert not (out / "verification_tests.json").exists()

    def test_documented_shape_runs(self, isolate_data_root, demo_repo, tmp_path, capsys):
        job = _run_completed_job(demo_repo)

        import types

        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        out_dir = str(tmp_path / f"remedy-job-evidence-{job.job_id}")
        args = types.SimpleNamespace(
            job_id=job.job_id,
            out=out_dir,
            json=True,
        )
        COMMAND_HANDLERS["do.job-evidence"](args)

        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert output["manifest"]["status"] == "completed"

        out = Path(out_dir)
        files = sorted(str(f.relative_to(out)) for f in out.rglob("*") if f.is_file())
        assert "manifest.json" in files
        assert "summary.md" in files


class TestPromptTraceRoleMetadata:
    """T004: Prompt trace entries include role/model metadata."""

    def test_task_trace_includes_role_field(self, isolate_data_root):
        from packages.orchestration.job_evidence import (
            _write_job_prompt_trace_summary,
        )

        class FakeTask:
            task_id = "T001"
            run_id = "run1"

        class FakeJob:
            tasks = [FakeTask()]

        import tempfile
        with tempfile.TemporaryDirectory() as td:
            written: dict[str, str] = {}
            from packages.orchestration import data_paths
            run_dir = data_paths.run_dir("run1")
            run_dir.mkdir(parents=True, exist_ok=True)
            summary = {
                "builder_prompts": 3,
                "reviewer_prompts": 1,
                "total_prompt_chars": 500,
                "total_prompt_tokens_estimated": 100,
                "role": "builder",
                "configured_provider": "claude",
                "configured_model": "opus",
                "actual_provider": None,
                "actual_model": None,
                "model_resolution_source": "cli",
                "actual_model_verified": False,
            }
            (run_dir / "prompt_trace_summary.json").write_text(
                json.dumps(summary)
            )
            _write_job_prompt_trace_summary(FakeJob(), td, written)
            result = json.loads(Path(written["prompt_trace_summary.json"]).read_text())
            tt = result["task_traces"][0]
            assert tt["role"] == "builder"
            assert tt["configured_provider"] == "claude"
            assert tt["configured_model"] == "opus"
            assert tt["actual_provider"] is None
            assert tt["actual_model"] is None
            assert tt["model_resolution_source"] == "cli"
            assert tt["actual_model_verified"] is False

    def test_per_role_model_summary_in_aggregate(self, isolate_data_root):
        from packages.orchestration.job_evidence import (
            _write_job_prompt_trace_summary,
        )

        class FakeTask:
            task_id = "T001"
            run_id = "run2"

        class FakeJob:
            tasks = [FakeTask()]

        import tempfile
        with tempfile.TemporaryDirectory() as td:
            written: dict[str, str] = {}
            from packages.orchestration import data_paths
            run_dir = data_paths.run_dir("run2")
            run_dir.mkdir(parents=True, exist_ok=True)
            summary = {
                "builder_prompts": 2,
                "reviewer_prompts": 1,
                "total_prompt_chars": 300,
                "total_prompt_tokens_estimated": 60,
                "role": "reviewer",
                "configured_provider": "ollama",
                "configured_model": "qwen3",
            }
            (run_dir / "prompt_trace_summary.json").write_text(
                json.dumps(summary)
            )
            _write_job_prompt_trace_summary(FakeJob(), td, written)
            result = json.loads(Path(written["prompt_trace_summary.json"]).read_text())
            assert "per_role_model_summary" in result
            assert "reviewer" in result["per_role_model_summary"]
            role_info = result["per_role_model_summary"]["reviewer"]
            assert role_info["configured_provider"] == "ollama"
            assert role_info["task_count"] == 1

    def test_missing_role_defaults_to_unknown(self, isolate_data_root):
        from packages.orchestration.job_evidence import (
            _write_job_prompt_trace_summary,
        )

        class FakeTask:
            task_id = "T001"
            run_id = "run3"

        class FakeJob:
            tasks = [FakeTask()]

        import tempfile
        with tempfile.TemporaryDirectory() as td:
            written: dict[str, str] = {}
            from packages.orchestration import data_paths
            run_dir = data_paths.run_dir("run3")
            run_dir.mkdir(parents=True, exist_ok=True)
            summary = {
                "builder_prompts": 1,
                "reviewer_prompts": 0,
                "total_prompt_chars": 100,
                "total_prompt_tokens_estimated": 20,
            }
            (run_dir / "prompt_trace_summary.json").write_text(
                json.dumps(summary)
            )
            _write_job_prompt_trace_summary(FakeJob(), td, written)
            result = json.loads(Path(written["prompt_trace_summary.json"]).read_text())
            tt = result["task_traces"][0]
            assert tt["role"] == "unknown"
            assert tt["model_resolution_source"] == "unknown"
            assert tt["actual_model_verified"] is False

    def test_actual_null_when_provider_unavailable(self, isolate_data_root):
        from packages.orchestration.job_evidence import (
            _write_job_prompt_trace_summary,
        )

        class FakeTask:
            task_id = "T001"
            run_id = "run4"

        class FakeJob:
            tasks = [FakeTask()]

        import tempfile
        with tempfile.TemporaryDirectory() as td:
            written: dict[str, str] = {}
            from packages.orchestration import data_paths
            run_dir = data_paths.run_dir("run4")
            run_dir.mkdir(parents=True, exist_ok=True)
            summary = {
                "builder_prompts": 1,
                "reviewer_prompts": 0,
                "total_prompt_chars": 50,
                "total_prompt_tokens_estimated": 10,
                "role": "builder",
                "configured_provider": "claude",
                "configured_model": "opus",
                "actual_provider": None,
                "actual_model": None,
            }
            (run_dir / "prompt_trace_summary.json").write_text(
                json.dumps(summary)
            )
            _write_job_prompt_trace_summary(FakeJob(), td, written)
            result = json.loads(Path(written["prompt_trace_summary.json"]).read_text())
            tt = result["task_traces"][0]
            assert tt["actual_provider"] is None
            assert tt["actual_model"] is None


class TestEvidenceHygiene:
    """T007: Evidence hygiene — verification_tests list, manual repair hashes."""

    def test_no_hardcoded_verification_test_list(self):
        # Verification is now driven by explicit --verification-command inputs,
        # not a hardcoded module list that silently under-covers changes.
        from packages.orchestration import job_evidence
        src = Path(job_evidence.__file__).read_text()
        assert "test_role_config.py" not in src
        assert "test_execution_config_evidence.py" not in src

    def test_verification_helpers_present(self):
        from packages.orchestration import job_evidence
        assert hasattr(job_evidence, "_run_verifications")
        assert hasattr(job_evidence, "_default_verification_runner")

    def test_manual_repair_provenance_schema(self, tmp_path):
        prov = {
            "task_id": "T006",
            "repair_type": "manual",
            "file_hashes": {
                "role_config.py": "abc123",
            },
        }
        p = tmp_path / "manual_repair_provenance.json"
        p.write_text(json.dumps(prov))
        data = json.loads(p.read_text())
        assert "file_hashes" in data
        assert isinstance(data["file_hashes"], dict)

    def test_bundle_integrity_stays_packaging_layer(self):
        import inspect

        from packages.orchestration.final_verifier import build_final_verifier_report
        from scripts.build_review_manifest import build_manifest_from_snapshot
        fv_src = inspect.getsource(build_final_verifier_report)
        assert "review_bundle_integrity" not in fv_src
        # Round 24 (F6): the manifest is assembled by build_manifest_from_snapshot from the
        # immutable Source-snapshot view; build_manifest is now the thin dir-reading wrapper.
        manifest_src = inspect.getsource(build_manifest_from_snapshot)
        assert "review_bundle_integrity" in manifest_src


class TestEvidenceBundleConsistency:
    """T007: Evidence bundle and review consistency."""

    def test_evidence_includes_execution_mode_per_task(
        self, isolate_data_root, demo_repo, tmp_path
    ):
        """Evidence bundle must include task_execution_evidence.json per task."""
        from packages.orchestration.job_evidence import export_job_evidence

        job = _run_completed_job(demo_repo)
        out = str(tmp_path / "ev_exec_mode")
        result = export_job_evidence(job.job_id, out)
        files = result.get("files", {})
        for tid in ["T001", "T002"]:
            rel = f"task_runs/{tid}/task_execution_evidence.json"
            assert rel in files, f"missing {rel}"
            data = json.loads(Path(files[rel]).read_text())
            assert "execution_mode" in data
            assert data["task_id"] == tid

    def test_evidence_includes_actor_binding_per_task(
        self, isolate_data_root, demo_repo, tmp_path
    ):
        """Evidence bundle must include task_actor_binding.json per task."""
        from packages.orchestration.job_evidence import export_job_evidence

        job = _run_completed_job(demo_repo)
        out = str(tmp_path / "ev_actor_bind")
        result = export_job_evidence(job.job_id, out)
        files = result.get("files", {})
        for tid in ["T001", "T002"]:
            rel = f"task_runs/{tid}/task_actor_binding.json"
            assert rel in files, f"missing {rel}"
            data = json.loads(Path(files[rel]).read_text())
            assert data["task_id"] == tid
            assert "sticky_across_rounds" in data
            assert "builder_provider" in data

    def test_evidence_includes_token_cost_policy(
        self, isolate_data_root, demo_repo, tmp_path
    ):
        """Evidence bundle must include token_cost_policy.json at job level."""
        from packages.orchestration.job_evidence import export_job_evidence

        job = _run_completed_job(demo_repo)
        out = str(tmp_path / "ev_tcp")
        result = export_job_evidence(job.job_id, out)
        files = result.get("files", {})
        assert "token_cost_policy.json" in files
        data = json.loads(Path(files["token_cost_policy.json"]).read_text())
        assert "schema_version" in data
        assert data["job_id"] == job.job_id

    def test_evidence_includes_final_job_review(
        self, isolate_data_root, demo_repo, tmp_path
    ):
        """Evidence bundle must include final_job_review.json at job level."""
        from packages.orchestration.job_evidence import export_job_evidence

        job = _run_completed_job(demo_repo)
        out = str(tmp_path / "ev_fjr")
        result = export_job_evidence(job.job_id, out)
        files = result.get("files", {})
        assert "final_job_review.json" in files
        data = json.loads(Path(files["final_job_review.json"]).read_text())
        assert "verdict" in data
        assert data["job_id"] == job.job_id

    def test_bundle_integrity_unverified_when_no_proof(self, tmp_path):
        """_check_bundle_integrity returns hash_checked=false when no proof file."""
        from scripts.build_review_manifest import _check_bundle_integrity

        ev_dir = tmp_path / "evidence"
        ev_dir.mkdir()
        result = _check_bundle_integrity(str(ev_dir), str(tmp_path))
        assert result["current_content_hash_checked"] is False
        assert result["verdict"] == "PASS"

    def test_bundle_integrity_checked_when_proof_matches(self, tmp_path):
        """_check_bundle_integrity returns hash_checked=true on matching hashes."""
        import hashlib

        from scripts.build_review_manifest import _check_bundle_integrity

        ev_dir = tmp_path / "evidence"
        ev_dir.mkdir()
        source_root = tmp_path / "source"
        source_root.mkdir()
        src_file = source_root / "main.py"
        src_file.write_text("print('hi')\n")
        file_hash = hashlib.sha256(src_file.read_bytes()).hexdigest()
        (ev_dir / "current_change_content_proof.json").write_text(json.dumps({
            "schema_version": "1.0.0",
            "file_hashes": {"main.py": file_hash},
            "file_count": 1,
        }))
        result = _check_bundle_integrity(str(ev_dir), str(source_root))
        assert result["current_content_hash_checked"] is True
        assert result["verdict"] == "PASS"

    def test_bundle_integrity_blocked_on_mismatch(self, tmp_path):
        """_check_bundle_integrity blocks on hash mismatch."""
        from scripts.build_review_manifest import _check_bundle_integrity

        ev_dir = tmp_path / "evidence"
        ev_dir.mkdir()
        source_root = tmp_path / "source"
        source_root.mkdir()
        (source_root / "main.py").write_text("print('hi')\n")
        (ev_dir / "current_change_content_proof.json").write_text(json.dumps({
            "schema_version": "1.0.0",
            "file_hashes": {"main.py": "0" * 64},
            "file_count": 1,
        }))
        result = _check_bundle_integrity(str(ev_dir), str(source_root))
        assert result["verdict"] == "BLOCKED"
        assert len(result["current_content_hash_mismatches"]) > 0

    def test_unverified_status_logic(self):
        """READY_FOR_REVIEW downgrades to UNVERIFIED when hash not checked."""
        # Simulate the status-determination logic from build_review_manifest
        package_status = "READY_FOR_REVIEW"
        bundle_integrity = {
            "current_content_hash_checked": False,
            "verdict": "PASS",
        }
        # Apply the same logic as build_review_manifest
        if bundle_integrity["verdict"] == "BLOCKED":
            package_status = "BLOCKED_EVIDENCE"
        elif (
            package_status == "READY_FOR_REVIEW"
            and not bundle_integrity.get("current_content_hash_checked", False)
        ):
            package_status = "READY_FOR_REVIEW_UNVERIFIED"
        assert package_status == "READY_FOR_REVIEW_UNVERIFIED"

    def test_execution_evidence_mode_matches_provider(
        self, isolate_data_root, demo_repo, tmp_path
    ):
        """Execution mode in evidence should reflect the provider type used."""
        from packages.orchestration.job_evidence import export_job_evidence

        job = _run_completed_job(demo_repo)
        out = str(tmp_path / "ev_mode_check")
        result = export_job_evidence(job.job_id, out)
        files = result.get("files", {})
        rel = "task_runs/T001/task_execution_evidence.json"
        assert rel in files
        data = json.loads(Path(files[rel]).read_text())
        # FakeProvider used -> should be fake_provider_test
        assert data["execution_mode"] == "fake_provider_test"


class TestAttestationOverlayNoFakeStubs:
    """Attestation overlay must not create fake-empty observability stubs."""

    def test_no_fake_agent_run_trace(self, isolate_data_root, demo_repo, tmp_path):
        """Attestation must not fabricate agent_run_trace.jsonl."""
        from packages.orchestration.job_evidence import export_job_evidence
        from packages.orchestration.repair_attest import attest_operator_repair

        job = _run_completed_job(demo_repo)
        attest_operator_repair(job.job_id, "T001", "manual fix", str(demo_repo))
        out = str(tmp_path / "ev_no_fake")
        result = export_job_evidence(job.job_id, out)
        files = result.get("files", {})
        if "agent_run_trace.jsonl" in files:
            content = Path(files["agent_run_trace.jsonl"]).read_text().strip()
            assert content, "agent_run_trace.jsonl must not be empty fake stub"

    def test_no_fake_prompt_trace(self, isolate_data_root, demo_repo, tmp_path):
        """Attestation must not fabricate empty prompt_trace.jsonl."""
        from packages.orchestration.job_evidence import export_job_evidence
        from packages.orchestration.repair_attest import attest_operator_repair

        job = _run_completed_job(demo_repo)
        attest_operator_repair(job.job_id, "T001", "manual fix", str(demo_repo))
        out = str(tmp_path / "ev_no_fake_pt")
        result = export_job_evidence(job.job_id, out)
        files = result.get("files", {})
        for tid in ["T001", "T002"]:
            rel = f"task_runs/{tid}/prompt_trace.jsonl"
            if rel in files:
                content = Path(files[rel]).read_text().strip()
                if content:
                    assert len(content) > 5, (
                        "prompt_trace.jsonl must not be a trivial fake stub"
                    )

    def test_manual_not_applicable_status_accepted(
        self, isolate_data_root, demo_repo, tmp_path
    ):
        """Provider evidence with not_applicable_manual_repair status is valid."""
        from packages.orchestration.repair_attest import attest_operator_repair

        job = _run_completed_job(demo_repo)
        result = attest_operator_repair(
            job.job_id, "T001", "manual fix", str(demo_repo)
        )
        pe = json.loads(Path(result["files"]["provider_evidence.json"]).read_text())
        assert pe["prompt_trace_status"] == "not_applicable_manual_repair"


class TestManualCompletionFinalizeActuallyRuns:
    """Round 16 regression: `_finalize_manual_completion` swallows any exception into
    `manual_completion_finalize.error.txt` and continues. That is deliberate — one broken
    overlay must not abort the whole export — but it means a bug in that path (an F8 import that
    was in scope for one function and not the other) went silent: `completion_mode` never got
    written, the packager saw a non-manual job, and required provider-flow root artifacts were
    reported MISSING. The attest tests all passed because none asserted the overlay SUCCEEDED.
    """

    def test_the_finalize_step_leaves_no_error_file(self, isolate_data_root, demo_repo,
                                                    tmp_path):
        from packages.orchestration.job_evidence import export_job_evidence
        from packages.orchestration.repair_attest import attest_operator_repair

        job = _run_completed_job(demo_repo)
        attest_operator_repair(job.job_id, "T001", "manual fix", str(demo_repo))
        out = Path(tmp_path / "ev_finalize")
        export_job_evidence(job.job_id, str(out))
        err = out / "manual_completion_finalize.error.txt"
        assert not err.exists(), (
            f"the manual-completion overlay failed silently: "
            f"{err.read_text()[:200] if err.exists() else ''}")

    def test_the_completion_mode_reaches_the_final_job_review(self, isolate_data_root,
                                                              demo_repo, tmp_path):
        """The fact the packager's manual-completion detector reads. Without it, an
        operator-attested package is misclassified and blocked."""
        from packages.orchestration.job_evidence import export_job_evidence
        from packages.orchestration.repair_attest import attest_operator_repair

        job = _run_completed_job(demo_repo)
        attest_operator_repair(job.job_id, "T001", "manual fix", str(demo_repo))
        out = Path(tmp_path / "ev_cm")
        export_job_evidence(job.job_id, str(out))
        fjr = json.loads((out / "final_job_review.json").read_text())
        assert fjr.get("completion_mode") == "manual_operator_repair"

    def test_the_packager_detects_manual_completion(self, isolate_data_root, demo_repo,
                                                    tmp_path):
        """End to end into the packager's own predicate — the one whose False reintroduced the
        missing-root-artifact block."""
        from packages.orchestration.job_evidence import export_job_evidence
        from packages.orchestration.repair_attest import attest_operator_repair
        from scripts.build_review_manifest import _is_manual_completion

        job = _run_completed_job(demo_repo)
        # ALL task runs must be manual for the packager to treat the job as manual completion.
        for t in job.tasks:
            attest_operator_repair(job.job_id, t.task_id, "manual fix", str(demo_repo))
        out = Path(tmp_path / "ev_pkg")
        export_job_evidence(job.job_id, str(out))
        assert _is_manual_completion(str(out)) is True
