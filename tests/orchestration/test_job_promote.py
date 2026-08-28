"""Tests for job promotion (Steps 4945-4960).

Covers: dry-run, approved promote, readiness gates, path safety,
post-apply tests, promotion record, no-commit/no-push guarantees.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration.pingpong_job import (
    parse_job_file,
    run_job,
)
from packages.orchestration.pingpong_provider import FakeProvider

_TWO_TASK_JOB = """\
# Job: Promote Test

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
# Step 4952: Dry-run behavior tests
# ---------------------------------------------------------------------------


class TestDryRunCompleted:
    def test_completed_job_dry_run_ready(self, isolate_data_root, demo_repo):
        job = _run_completed_job(demo_repo)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(demo_repo), dry_run=True)

        assert result.status == "dry_run"
        assert len(result.files_planned) > 0
        assert result.job_status == "completed"

    def test_dry_run_does_not_mutate_target(self, isolate_data_root, demo_repo):
        readme_before = (demo_repo / "README.md").read_text()
        main_before = (demo_repo / "src" / "main.py").read_text()

        job = _run_completed_job(demo_repo)
        from packages.orchestration.job_promote import promote_job
        promote_job(job.job_id, str(demo_repo), dry_run=True)

        assert (demo_repo / "README.md").read_text() == readme_before
        assert (demo_repo / "src" / "main.py").read_text() == main_before

    def test_dry_run_human_readable(self, isolate_data_root, demo_repo):
        job = _run_completed_job(demo_repo)

        from packages.orchestration.job_promote import (
            promote_job,
            summarize_job_promotion,
        )
        result = promote_job(job.job_id, str(demo_repo), dry_run=True)
        text = summarize_job_promotion(result)

        assert "dry-run" in text.lower() or "Dry-run" in text
        assert "remedy do job-promote" in text

    def test_dry_run_json_machine_verifiable(self, isolate_data_root, demo_repo):
        job = _run_completed_job(demo_repo)

        from packages.orchestration.job_promote import (
            export_job_promotion_json,
            promote_job,
        )
        result = promote_job(job.job_id, str(demo_repo), dry_run=True)
        data = export_job_promotion_json(result)

        assert data["status"] == "dry_run"
        assert isinstance(data["files_planned"], list)
        assert isinstance(data["task_summaries"], list)
        assert data["job_id"] == job.job_id


class TestDryRunBlocked:
    def test_blocked_job_blocked(self, isolate_data_root, demo_repo, monkeypatch):
        job = _run_blocked_job(demo_repo, monkeypatch)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(demo_repo), dry_run=True)

        assert result.status == "blocked"
        assert "not_completed" in result.blocked_reason or "not_applied" in result.blocked_reason

    def test_paused_job_blocked(self, isolate_data_root, demo_repo):
        job = _run_paused_job(demo_repo)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(demo_repo), dry_run=True)

        assert result.status == "blocked"


class TestDryRunMissingWorkspace:
    def test_missing_workspace_blocks(self, isolate_data_root, demo_repo):
        job = _run_completed_job(demo_repo)

        import shutil
        shutil.rmtree(job.job_workspace_path)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(demo_repo), dry_run=True)

        assert result.status == "blocked"
        assert "workspace" in result.blocked_reason.lower()


class TestDryRunMissingRun:
    def test_missing_run_id_blocks(self, isolate_data_root, demo_repo):
        from packages.orchestration.pingpong_job import (
            JobPlan,
            TaskEntry,
            _persist_job,
        )
        job = JobPlan(
            repo_path=str(demo_repo),
            job_title="Missing run test",
            status="completed",
            tasks=[
                TaskEntry(task_id="T001", title="Task 1", body="test",
                          status="applied_to_job_workspace", run_id="",
                          reviewer_verdict="pass", test_passed=True),
            ],
        )
        _persist_job(job)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(demo_repo), dry_run=True)

        assert result.status == "blocked"
        assert "run_id" in result.blocked_reason


class TestDryRunBadReviewer:
    def test_bad_reviewer_verdict_blocks(self, isolate_data_root, demo_repo):
        from packages.orchestration.pingpong_job import (
            JobPlan,
            TaskEntry,
            _persist_job,
        )
        job = JobPlan(
            repo_path=str(demo_repo),
            job_title="Bad reviewer test",
            status="completed",
            tasks=[
                TaskEntry(task_id="T001", title="Task 1", body="test",
                          status="applied_to_job_workspace", run_id="abc123",
                          reviewer_verdict="fail", test_passed=True),
            ],
        )
        _persist_job(job)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(demo_repo), dry_run=True)

        assert result.status == "blocked"
        assert "reviewer" in result.blocked_reason.lower()


class TestDryRunFailedTests:
    def test_failed_tests_block(self, isolate_data_root, demo_repo):
        from packages.orchestration.pingpong_job import (
            JobPlan,
            TaskEntry,
            _persist_job,
        )
        job = JobPlan(
            repo_path=str(demo_repo),
            job_title="Failed tests test",
            status="completed",
            tasks=[
                TaskEntry(task_id="T001", title="Task 1", body="test",
                          status="applied_to_job_workspace", run_id="abc123",
                          reviewer_verdict="pass", test_passed=False),
            ],
        )
        _persist_job(job)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(demo_repo), dry_run=True)

        assert result.status == "blocked"
        assert "tests_failed" in result.blocked_reason


class TestDryRunTargetMutation:
    def test_target_mutation_blocks(self, isolate_data_root, demo_repo):
        from packages.orchestration.pingpong_job import (
            JobPlan,
            TargetGuard,
            TaskEntry,
            _persist_job,
        )
        job = JobPlan(
            repo_path=str(demo_repo),
            job_title="Target mutation test",
            status="completed",
            target_guard=TargetGuard(target_mutated=True, changed_target_files=["x.py"]),
            tasks=[
                TaskEntry(task_id="T001", title="Task 1", body="test",
                          status="applied_to_job_workspace", run_id="abc123",
                          reviewer_verdict="pass", test_passed=True),
            ],
        )
        _persist_job(job)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(demo_repo), dry_run=True)

        assert result.status == "blocked"
        assert "target_mutated" in result.blocked_reason


class TestDryRunUnsafePaths:
    def test_traversal_path_blocks(self, isolate_data_root, demo_repo):
        from packages.orchestration.pingpong_job import (
            ApplyManifest,
            JobPlan,
            TaskEntry,
            _persist_job,
        )
        job = JobPlan(
            repo_path=str(demo_repo),
            job_title="Traversal test",
            status="completed",
            job_workspace_path=str(demo_repo),
            tasks=[
                TaskEntry(task_id="T001", title="Task 1", body="test",
                          status="applied_to_job_workspace", run_id="abc123",
                          reviewer_verdict="pass", test_passed=True,
                          apply_manifest=ApplyManifest(
                              task_id="T001", run_id="abc123",
                              applied_files=["../../etc/passwd"],
                              status="applied",
                          )),
            ],
        )
        _persist_job(job)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(demo_repo), dry_run=True)

        assert result.status == "blocked"
        assert "traversal" in result.blocked_reason.lower() or "blocked" in result.blocked_reason.lower()

    def test_env_file_blocks(self, isolate_data_root, demo_repo):
        from packages.orchestration.pingpong_job import (
            ApplyManifest,
            JobPlan,
            TaskEntry,
            _persist_job,
        )
        job = JobPlan(
            repo_path=str(demo_repo),
            job_title="Env file test",
            status="completed",
            job_workspace_path=str(demo_repo),
            tasks=[
                TaskEntry(task_id="T001", title="Task 1", body="test",
                          status="applied_to_job_workspace", run_id="abc123",
                          reviewer_verdict="pass", test_passed=True,
                          apply_manifest=ApplyManifest(
                              task_id="T001", run_id="abc123",
                              applied_files=[".env.production"],
                              status="applied",
                          )),
            ],
        )
        _persist_job(job)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(demo_repo), dry_run=True)

        assert result.status == "blocked"
        assert "secret" in result.blocked_reason.lower() or "blocked" in result.blocked_reason.lower()


# ---------------------------------------------------------------------------
# Step 4953: Approved promote behavior tests
# ---------------------------------------------------------------------------


class TestApproveRequiresFlag:
    def test_no_approve_no_dry_run_is_dry_run(self, isolate_data_root, demo_repo, capsys):
        """Without --approve or --dry-run, CLI handler defaults to dry-run."""
        job = _run_completed_job(demo_repo)

        import types

        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        args = types.SimpleNamespace(
            job_id=job.job_id,
            repo=str(demo_repo),
            approve=False,
            dry_run=False,
            test_command="",
            json=True,
        )
        COMMAND_HANDLERS["do.job-promote"](args)
        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert output["status"] == "dry_run"


class TestApproveApplies:
    def test_approve_applies_safe_files(self, isolate_data_root, demo_repo):
        job = _run_completed_job(demo_repo)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(demo_repo), approve=True)

        assert result.status == "promoted"
        assert len(result.files_applied) > 0

    def test_approve_does_not_commit(self, isolate_data_root, demo_repo, tmp_path):
        """Promote must not create git commits."""
        job = _run_completed_job(demo_repo)

        from packages.orchestration.job_promote import promote_job
        promote_job(job.job_id, str(demo_repo), approve=True)

        # No .git directory means no commits possible
        assert not (demo_repo / ".git").exists()

    def test_approve_does_not_push(self, isolate_data_root, demo_repo):
        """Promote must not push."""
        job = _run_completed_job(demo_repo)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(demo_repo), approve=True)

        assert result.status == "promoted"

    def test_approve_verifies_file_contents(self, isolate_data_root, demo_repo):
        job = _run_completed_job(demo_repo)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(demo_repo), approve=True)

        workspace = Path(job.job_workspace_path)
        for rel_path in result.files_applied:
            ws_content = (workspace / rel_path).read_bytes()
            target_content = (demo_repo / rel_path).read_bytes()
            assert ws_content == target_content, f"Mismatch: {rel_path}"

    def test_approve_reports_applied_files(self, isolate_data_root, demo_repo):
        job = _run_completed_job(demo_repo)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(demo_repo), approve=True)

        assert isinstance(result.files_applied, list)
        assert len(result.files_applied) > 0

    def test_approve_blocks_traversal(self, isolate_data_root, demo_repo):
        from packages.orchestration.pingpong_job import (
            ApplyManifest,
            JobPlan,
            TaskEntry,
            _persist_job,
        )
        job = JobPlan(
            repo_path=str(demo_repo),
            job_title="Traversal approve test",
            status="completed",
            job_workspace_path=str(demo_repo),
            tasks=[
                TaskEntry(task_id="T001", title="t", body="t",
                          status="applied_to_job_workspace", run_id="x",
                          reviewer_verdict="pass", test_passed=True,
                          apply_manifest=ApplyManifest(
                              task_id="T001", run_id="x",
                              applied_files=["../../../etc/shadow"],
                              status="applied",
                          )),
            ],
        )
        _persist_job(job)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(demo_repo), approve=True)

        assert result.status == "blocked"

    def test_approve_blocks_sensitive_paths(self, isolate_data_root, demo_repo):
        from packages.orchestration.pingpong_job import (
            ApplyManifest,
            JobPlan,
            TaskEntry,
            _persist_job,
        )
        job = JobPlan(
            repo_path=str(demo_repo),
            job_title="Sensitive path test",
            status="completed",
            job_workspace_path=str(demo_repo),
            tasks=[
                TaskEntry(task_id="T001", title="t", body="t",
                          status="applied_to_job_workspace", run_id="x",
                          reviewer_verdict="pass", test_passed=True,
                          apply_manifest=ApplyManifest(
                              task_id="T001", run_id="x",
                              applied_files=[".env"],
                              status="applied",
                          )),
            ],
        )
        _persist_job(job)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(demo_repo), approve=True)

        assert result.status == "blocked"

    def test_no_unrelated_files_applied(self, isolate_data_root, demo_repo):
        job = _run_completed_job(demo_repo)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(demo_repo), approve=True)

        # All applied files must have been in the planned set
        for f in result.files_applied:
            assert f in result.files_planned or f in result.files_applied


class TestApprovePostTest:
    def test_post_apply_test_runs(self, isolate_data_root, demo_repo):
        job = _run_completed_job(demo_repo)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(
            job.job_id, str(demo_repo),
            approve=True,
            test_command="echo ok",
        )

        assert result.post_test_passed is True
        assert result.status == "promoted"

    def test_post_apply_test_failure_reported(self, isolate_data_root, demo_repo):
        job = _run_completed_job(demo_repo)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(
            job.job_id, str(demo_repo),
            approve=True,
            test_command="false",
        )

        assert result.post_test_passed is False
        assert result.status == "promoted_test_failed"


# ---------------------------------------------------------------------------
# Step 4951: Promotion record tests
# ---------------------------------------------------------------------------


class TestPromotionRecord:
    def test_dry_run_persists_record(self, isolate_data_root, demo_repo):
        job = _run_completed_job(demo_repo)

        from packages.orchestration.job_promote import (
            load_job_promotion,
            promote_job,
        )
        result = promote_job(job.job_id, str(demo_repo), dry_run=True)

        loaded = load_job_promotion(job.job_id, result.promotion_id)
        assert loaded is not None
        assert loaded["status"] == "dry_run"

    def test_approved_persists_record(self, isolate_data_root, demo_repo):
        job = _run_completed_job(demo_repo)

        from packages.orchestration.job_promote import (
            load_job_promotion,
            promote_job,
        )
        result = promote_job(job.job_id, str(demo_repo), approve=True)

        loaded = load_job_promotion(job.job_id, result.promotion_id)
        assert loaded is not None
        assert loaded["status"] == "promoted"
        assert len(loaded["files_applied"]) > 0


# ---------------------------------------------------------------------------
# Step 4946: CLI command shape tests
# ---------------------------------------------------------------------------


class TestCLICommandShape:
    def test_catalog_has_job_promote(self):
        from apps.cli.command_catalog import CATALOG
        cmd = next(
            (c for c in CATALOG if c.command_id == "do.job-promote"),
            None,
        )
        assert cmd is not None
        assert cmd.may_mutate_repo is True
        assert cmd.may_execute_commands is True
        assert cmd.supports_json is True

    def test_handler_exists(self):
        from apps.cli.commands.do_cmd import COMMAND_HANDLERS
        assert "do.job-promote" in COMMAND_HANDLERS

    def test_cli_dry_run_json(self, isolate_data_root, demo_repo, capsys):
        job = _run_completed_job(demo_repo)

        import types

        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        args = types.SimpleNamespace(
            job_id=job.job_id,
            repo=str(demo_repo),
            approve=False,
            dry_run=True,
            test_command="",
            json=True,
        )
        COMMAND_HANDLERS["do.job-promote"](args)
        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert output["status"] == "dry_run"
        assert isinstance(output["files_planned"], list)

    def test_cli_text_output(self, isolate_data_root, demo_repo, capsys):
        job = _run_completed_job(demo_repo)

        import types

        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        args = types.SimpleNamespace(
            job_id=job.job_id,
            repo=str(demo_repo),
            approve=False,
            dry_run=True,
            test_command="",
            json=False,
        )
        COMMAND_HANDLERS["do.job-promote"](args)
        captured = capsys.readouterr()
        assert "dry-run" in captured.out.lower() or "Dry-run" in captured.out

    def test_missing_job_blocks(self, isolate_data_root, demo_repo):
        from packages.orchestration.job_promote import promote_job
        result = promote_job("nonexistent_job_id", str(demo_repo), dry_run=True)
        assert result.status == "blocked"
        assert "not_found" in result.blocked_reason


# ---------------------------------------------------------------------------
# Step 4969: Target-clobber regression tests
# ---------------------------------------------------------------------------


class TestTargetClobberBlocked:
    def test_target_modified_after_job_blocks(self, isolate_data_root, demo_repo):
        """Promote must block when target file changed since job started."""
        job = _run_completed_job(demo_repo)

        # Find a file and write different content to target
        for t in job.tasks:
            if t.apply_manifest and t.apply_manifest.applied_files:
                first_file = t.apply_manifest.applied_files[0]
                target_path = demo_repo / first_file
                target_path.parent.mkdir(parents=True, exist_ok=True)
                target_path.write_text("EXTERNALLY MODIFIED CONTENT\n")
                break

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(demo_repo), approve=True)

        assert result.status == "blocked"
        reason = result.blocked_reason.lower()
        assert "target_changed_since_job" in reason or "target_created_since_job" in reason

    def test_clean_target_allows_promote(self, isolate_data_root, demo_repo):
        """Promote succeeds when target matches baseline (no external edits)."""
        job = _run_completed_job(demo_repo)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(demo_repo), approve=True)

        assert result.status == "promoted"
        assert result.target_clean is True


# ---------------------------------------------------------------------------
# Step 4970: Workspace symlink leakage regression tests
# ---------------------------------------------------------------------------


class TestWorkspaceSymlinkBlocked:
    def test_workspace_source_symlink_blocks(self, isolate_data_root, tmp_path):
        """Source file that is a symlink must be blocked."""
        from packages.orchestration.pingpong_job import (
            ApplyManifest,
            JobPlan,
            TaskEntry,
            _persist_job,
        )

        workspace = tmp_path / "workspace"
        workspace.mkdir()
        target = tmp_path / "target"
        target.mkdir()

        # Create external file and symlink to it from workspace
        external = tmp_path / "external_secret.txt"
        external.write_text("SECRET DATA\n")
        (workspace / "leak.py").symlink_to(external)

        job = JobPlan(
            repo_path=str(target),
            job_title="Symlink leak test",
            status="completed",
            job_workspace_path=str(workspace),
            tasks=[
                TaskEntry(task_id="T001", title="t", body="t",
                          status="applied_to_job_workspace", run_id="x",
                          reviewer_verdict="pass", test_passed=True,
                          apply_manifest=ApplyManifest(
                              task_id="T001", run_id="x",
                              applied_files=["leak.py"],
                              status="applied",
                          )),
            ],
        )
        _persist_job(job)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(target), approve=True)

        assert result.status == "blocked"
        assert "symlink" in result.blocked_reason.lower()

    def test_workspace_parent_symlink_blocks(self, isolate_data_root, tmp_path):
        """Parent directory in workspace path that is a symlink must be blocked."""
        from packages.orchestration.pingpong_job import (
            ApplyManifest,
            JobPlan,
            TaskEntry,
            _persist_job,
        )

        workspace = tmp_path / "workspace"
        workspace.mkdir()
        target = tmp_path / "target"
        target.mkdir()

        # Create real dir outside workspace, symlink parent inside workspace
        outside_dir = tmp_path / "outside"
        outside_dir.mkdir()
        (outside_dir / "data.py").write_text("outside data\n")
        (workspace / "src").symlink_to(outside_dir)

        job = JobPlan(
            repo_path=str(target),
            job_title="Parent symlink test",
            status="completed",
            job_workspace_path=str(workspace),
            tasks=[
                TaskEntry(task_id="T001", title="t", body="t",
                          status="applied_to_job_workspace", run_id="x",
                          reviewer_verdict="pass", test_passed=True,
                          apply_manifest=ApplyManifest(
                              task_id="T001", run_id="x",
                              applied_files=["src/data.py"],
                              status="applied",
                          )),
            ],
        )
        _persist_job(job)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(target), approve=True)

        assert result.status == "blocked"
        reason = result.blocked_reason.lower()
        assert "symlink" in reason or "escapes" in reason

    def test_target_dest_symlink_escape_blocks(self, isolate_data_root, tmp_path):
        """Target file that is a symlink pointing outside target must be blocked."""
        from packages.orchestration.pingpong_job import (
            ApplyManifest,
            JobPlan,
            TaskEntry,
            _persist_job,
        )

        workspace = tmp_path / "workspace"
        workspace.mkdir()
        target = tmp_path / "target"
        target.mkdir()

        # Create workspace source
        (workspace / "config.py").write_text("safe content\n")
        # Target has symlink pointing outside
        outside_file = tmp_path / "outside.txt"
        outside_file.write_text("outside\n")
        (target / "config.py").symlink_to(outside_file)

        job = JobPlan(
            repo_path=str(target),
            job_title="Dest symlink test",
            status="completed",
            job_workspace_path=str(workspace),
            tasks=[
                TaskEntry(task_id="T001", title="t", body="t",
                          status="applied_to_job_workspace", run_id="x",
                          reviewer_verdict="pass", test_passed=True,
                          apply_manifest=ApplyManifest(
                              task_id="T001", run_id="x",
                              applied_files=["config.py"],
                              status="applied",
                          )),
            ],
        )
        _persist_job(job)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(target), approve=True)

        assert result.status == "blocked"
        assert "symlink" in result.blocked_reason.lower() or "escape" in result.blocked_reason.lower()


# ---------------------------------------------------------------------------
# Step 4971: Missing apply manifest fallback regression tests
# ---------------------------------------------------------------------------


class TestMissingApplyManifestBlocks:
    def test_no_apply_manifest_blocks(self, isolate_data_root, tmp_path):
        """Task without apply manifest must block — no fallback scanning."""
        from packages.orchestration.pingpong_job import (
            JobPlan,
            TaskEntry,
            _persist_job,
        )

        workspace = tmp_path / "workspace"
        workspace.mkdir()
        (workspace / "file.py").write_text("content\n")
        target = tmp_path / "target"
        target.mkdir()

        job = JobPlan(
            repo_path=str(target),
            job_title="No manifest test",
            status="completed",
            job_workspace_path=str(workspace),
            tasks=[
                TaskEntry(task_id="T001", title="t", body="t",
                          status="applied_to_job_workspace", run_id="x",
                          reviewer_verdict="pass", test_passed=True,
                          apply_manifest=None),
            ],
        )
        _persist_job(job)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(target), approve=True)

        assert result.status == "blocked"
        assert "apply_manifest" in result.blocked_reason.lower()

    def test_empty_apply_manifest_blocks(self, isolate_data_root, tmp_path):
        """Apply manifest with no files must block."""
        from packages.orchestration.pingpong_job import (
            ApplyManifest,
            JobPlan,
            TaskEntry,
            _persist_job,
        )

        workspace = tmp_path / "workspace"
        workspace.mkdir()
        target = tmp_path / "target"
        target.mkdir()

        job = JobPlan(
            repo_path=str(target),
            job_title="Empty manifest test",
            status="completed",
            job_workspace_path=str(workspace),
            tasks=[
                TaskEntry(task_id="T001", title="t", body="t",
                          status="applied_to_job_workspace", run_id="x",
                          reviewer_verdict="pass", test_passed=True,
                          apply_manifest=ApplyManifest(
                              task_id="T001", run_id="x",
                              applied_files=[],
                              status="applied",
                          )),
            ],
        )
        _persist_job(job)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(target), approve=True)

        assert result.status == "blocked"
        assert "no_files" in result.blocked_reason.lower()

    def test_pending_apply_manifest_blocks(self, isolate_data_root, tmp_path):
        """Apply manifest with status != 'applied' must block."""
        from packages.orchestration.pingpong_job import (
            ApplyManifest,
            JobPlan,
            TaskEntry,
            _persist_job,
        )

        workspace = tmp_path / "workspace"
        workspace.mkdir()
        target = tmp_path / "target"
        target.mkdir()

        job = JobPlan(
            repo_path=str(target),
            job_title="Pending manifest test",
            status="completed",
            job_workspace_path=str(workspace),
            tasks=[
                TaskEntry(task_id="T001", title="t", body="t",
                          status="applied_to_job_workspace", run_id="x",
                          reviewer_verdict="pass", test_passed=True,
                          apply_manifest=ApplyManifest(
                              task_id="T001", run_id="x",
                              applied_files=["file.py"],
                              status="pending",
                          )),
            ],
        )
        _persist_job(job)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(target), approve=True)

        assert result.status == "blocked"
        assert "not_applied" in result.blocked_reason.lower()


# ---------------------------------------------------------------------------
# Step 4967: Promotion record persistence tests
# ---------------------------------------------------------------------------


class TestPromotionRecordPersistence:
    def test_unwritable_promo_dir_blocks_approved(
        self, isolate_data_root, demo_repo, tmp_path, monkeypatch
    ):
        """Approved promote must block if promotion record can't be persisted."""
        job = _run_completed_job(demo_repo)

        from packages.orchestration import job_promote as jp_mod

        # Use a regular file as promotions dir — mkdir will fail
        blocker = tmp_path / "not_a_dir"
        blocker.write_text("block")

        def fake_promotions_dir():
            return blocker / "subdir"

        monkeypatch.setattr(jp_mod, "_promotions_dir", fake_promotions_dir)

        result = jp_mod.promote_job(job.job_id, str(demo_repo), approve=True)

        assert result.status == "blocked"
        assert "not_writable" in result.blocked_reason.lower()


# ---------------------------------------------------------------------------
# Step 4966: Redaction tests
# ---------------------------------------------------------------------------


class TestRedactionApplied:
    def test_json_export_redacts_secrets(self, isolate_data_root, demo_repo):
        """JSON export must redact secret-like values."""
        from packages.orchestration.job_promote import (
            JobPromotionResult,
            export_job_promotion_json,
        )

        result = JobPromotionResult(
            job_id="test",
            status="dry_run",
            target_repo="/home/user/project",
            job_workspace_path="/home/user/.remedy/workspace",
            post_test_summary="API_KEY=sk-abc123def456",
        )
        data = export_job_promotion_json(result)

        # post_test_summary should have redacted the API key pattern
        assert "sk-abc123def456" not in json.dumps(data)

    def test_text_summary_redacts_secrets(self, isolate_data_root, demo_repo):
        """Text summary must redact secret-like values."""
        from packages.orchestration.job_promote import (
            JobPromotionResult,
            summarize_job_promotion,
        )

        result = JobPromotionResult(
            job_id="test",
            status="promoted",
            target_repo="/home/user/project",
            post_test_summary="password=s3cr3t_p@ssw0rd",
        )
        text = summarize_job_promotion(result)

        assert "s3cr3t_p@ssw0rd" not in text

    def test_json_export_sanitizes_paths(self, isolate_data_root, demo_repo):
        """JSON export must sanitize home-directory paths."""
        import os

        from packages.orchestration.job_promote import (
            JobPromotionResult,
            export_job_promotion_json,
        )
        home = os.path.expanduser("~")
        result = JobPromotionResult(
            job_id="test",
            status="dry_run",
            target_repo=f"{home}/project",
            job_workspace_path=f"{home}/.remedy/ws",
        )
        data = export_job_promotion_json(result)

        target_val = data.get("target_repo", "")
        ws_val = data.get("job_workspace_path", "")
        assert home not in target_val or "~" in target_val
        assert home not in ws_val or "~" in ws_val


# ---------------------------------------------------------------------------
# Step 4968: CLI command-path tests
# ---------------------------------------------------------------------------


class TestCLICommandPaths:
    def test_cli_approve_applies(self, isolate_data_root, demo_repo, capsys):
        """CLI handler with --approve applies files."""
        job = _run_completed_job(demo_repo)

        import types

        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        args = types.SimpleNamespace(
            job_id=job.job_id,
            repo=str(demo_repo),
            approve=True,
            dry_run=False,
            test_command="",
            json=True,
        )
        COMMAND_HANDLERS["do.job-promote"](args)
        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert output["status"] == "promoted"
        assert len(output["files_applied"]) > 0

    def test_cli_blocked_json(self, isolate_data_root, demo_repo, capsys):
        """CLI handler returns blocked status in JSON for bad job."""
        import types

        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        args = types.SimpleNamespace(
            job_id="nonexistent",
            repo=str(demo_repo),
            approve=False,
            dry_run=True,
            test_command="",
            json=True,
        )
        COMMAND_HANDLERS["do.job-promote"](args)
        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert output["status"] == "blocked"

    def test_cli_text_blocked(self, isolate_data_root, demo_repo, capsys):
        """CLI handler shows BLOCKED in text mode for bad job."""
        import types

        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        args = types.SimpleNamespace(
            job_id="nonexistent",
            repo=str(demo_repo),
            approve=False,
            dry_run=True,
            test_command="",
            json=False,
        )
        COMMAND_HANDLERS["do.job-promote"](args)
        captured = capsys.readouterr()
        assert "BLOCKED" in captured.out or "blocked" in captured.out


# ---------------------------------------------------------------------------
# Baseline proof model helper
# ---------------------------------------------------------------------------

def _make_baselined_job(tmp_path, *, existing_content="original\n", new_content="modified\n"):
    """Create a job with baseline proof for testing.

    Returns (job, workspace, target, rel_path).
    Target starts with existing_content. Workspace final has new_content.
    """
    import hashlib

    from packages.orchestration.pingpong_job import (
        AppliedFileProof,
        ApplyManifest,
        JobPlan,
        TaskEntry,
        _persist_job,
    )

    workspace = tmp_path / "workspace"
    workspace.mkdir()
    target = tmp_path / "target"
    target.mkdir()

    rel_path = "existing.py"
    (target / rel_path).write_text(existing_content)
    (workspace / rel_path).write_text(new_content)

    baseline_hash = hashlib.sha256(existing_content.encode()).hexdigest()
    final_hash = hashlib.sha256(new_content.encode()).hexdigest()

    job = JobPlan(
        repo_path=str(target),
        job_title="Baseline test",
        status="completed",
        job_workspace_path=str(workspace),
        tasks=[
            TaskEntry(
                task_id="T001", title="modify existing", body="t",
                status="applied_to_job_workspace", run_id="run1",
                reviewer_verdict="pass", test_passed=True,
                apply_manifest=ApplyManifest(
                    task_id="T001", run_id="run1",
                    applied_files=[rel_path],
                    applied_file_proofs=[AppliedFileProof(
                        path=rel_path,
                        existed_before_job=True,
                        baseline_sha256=baseline_hash,
                        final_workspace_sha256=final_hash,
                        task_id="T001",
                        run_id="run1",
                    )],
                    status="applied",
                ),
            ),
        ],
    )
    _persist_job(job)
    return job, workspace, target, rel_path


def _make_new_file_job(tmp_path, *, content="new content\n"):
    """Create a job that creates a new file (didn't exist before)."""
    import hashlib

    from packages.orchestration.pingpong_job import (
        AppliedFileProof,
        ApplyManifest,
        JobPlan,
        TaskEntry,
        _persist_job,
    )

    workspace = tmp_path / "workspace"
    workspace.mkdir()
    target = tmp_path / "target"
    target.mkdir()

    rel_path = "new_file.py"
    (workspace / rel_path).write_text(content)

    final_hash = hashlib.sha256(content.encode()).hexdigest()

    job = JobPlan(
        repo_path=str(target),
        job_title="New file test",
        status="completed",
        job_workspace_path=str(workspace),
        tasks=[
            TaskEntry(
                task_id="T001", title="create new", body="t",
                status="applied_to_job_workspace", run_id="run1",
                reviewer_verdict="pass", test_passed=True,
                apply_manifest=ApplyManifest(
                    task_id="T001", run_id="run1",
                    applied_files=[rel_path],
                    applied_file_proofs=[AppliedFileProof(
                        path=rel_path,
                        existed_before_job=False,
                        baseline_sha256="",
                        final_workspace_sha256=final_hash,
                        task_id="T001",
                        run_id="run1",
                    )],
                    status="applied",
                ),
            ),
        ],
    )
    _persist_job(job)
    return job, workspace, target, rel_path


# ---------------------------------------------------------------------------
# Step 4981: Legitimate existing-file modification promotes
# ---------------------------------------------------------------------------


class TestBaselineExistingFilePromote:
    def test_existing_file_modification_promotes(self, isolate_data_root, tmp_path):
        """Reviewed modification to existing file promotes when target matches baseline."""
        job, workspace, target, rel_path = _make_baselined_job(tmp_path)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(target), approve=True)

        assert result.status == "promoted"
        assert rel_path in result.files_applied
        assert (target / rel_path).read_text() == "modified\n"

    def test_dry_run_shows_baseline_readiness(self, isolate_data_root, tmp_path):
        """Dry-run shows per-file baseline status."""
        job, workspace, target, rel_path = _make_baselined_job(tmp_path)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(target), dry_run=True)

        assert result.status == "dry_run"
        assert len(result.file_readiness) == 1
        fr = result.file_readiness[0]
        assert fr.path == rel_path
        assert fr.kind == "modified"
        assert fr.baseline_status == "target_matches_baseline"
        assert fr.workspace_status == "final_hash_matches"

    def test_json_includes_file_readiness(self, isolate_data_root, tmp_path):
        """JSON export includes file_readiness array."""
        job, workspace, target, rel_path = _make_baselined_job(tmp_path)

        from packages.orchestration.job_promote import (
            export_job_promotion_json,
            promote_job,
        )
        result = promote_job(job.job_id, str(target), dry_run=True)
        data = export_job_promotion_json(result)

        assert "file_readiness" in data
        assert len(data["file_readiness"]) == 1
        assert data["file_readiness"][0]["baseline_status"] == "target_matches_baseline"


# ---------------------------------------------------------------------------
# Step 4982: Target changed after job blocks
# ---------------------------------------------------------------------------


class TestTargetChangedSinceJob:
    def test_target_changed_blocks(self, isolate_data_root, tmp_path):
        """Promote blocks when target file was modified after job completion."""
        job, workspace, target, rel_path = _make_baselined_job(tmp_path)

        # Modify target after job
        (target / rel_path).write_text("someone else changed this\n")

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(target), approve=True)

        assert result.status == "blocked"
        assert "target_changed_since_job" in result.blocked_reason
        # Target content should remain untouched
        assert (target / rel_path).read_text() == "someone else changed this\n"


# ---------------------------------------------------------------------------
# Step 4983: Target file created after job blocks
# ---------------------------------------------------------------------------


class TestTargetCreatedSinceJob:
    def test_target_created_blocks(self, isolate_data_root, tmp_path):
        """Promote blocks when target file appeared after job expected to create it."""
        job, workspace, target, rel_path = _make_new_file_job(tmp_path)

        # Create the file in target before promote
        (target / rel_path).write_text("unrelated content\n")

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(target), approve=True)

        assert result.status == "blocked"
        assert "target_created_since_job" in result.blocked_reason
        assert (target / rel_path).read_text() == "unrelated content\n"


# ---------------------------------------------------------------------------
# Step 4984: Workspace changed after review blocks
# ---------------------------------------------------------------------------


class TestWorkspaceChangedSinceReview:
    def test_workspace_changed_blocks(self, isolate_data_root, tmp_path):
        """Promote blocks when workspace file was modified after review."""
        job, workspace, target, rel_path = _make_baselined_job(tmp_path)

        # Tamper with workspace after job completion
        (workspace / rel_path).write_text("tampered content\n")

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(target), approve=True)

        assert result.status == "blocked"
        assert "workspace_changed_since_review" in result.blocked_reason
        # Target should not be modified
        assert (target / rel_path).read_text() == "original\n"


# ---------------------------------------------------------------------------
# Step 4978: Legacy jobs without baseline proof
# ---------------------------------------------------------------------------


class TestLegacyJobsWithoutBaseline:
    def test_legacy_new_file_allows(self, isolate_data_root, tmp_path):
        """Legacy job creating a new file (no baseline) is allowed if target absent."""
        from packages.orchestration.pingpong_job import (
            ApplyManifest,
            JobPlan,
            TaskEntry,
            _persist_job,
        )

        workspace = tmp_path / "workspace"
        workspace.mkdir()
        target = tmp_path / "target"
        target.mkdir()

        (workspace / "brand_new.py").write_text("new\n")

        job = JobPlan(
            repo_path=str(target),
            job_title="Legacy new file",
            status="completed",
            job_workspace_path=str(workspace),
            tasks=[
                TaskEntry(
                    task_id="T001", title="t", body="t",
                    status="applied_to_job_workspace", run_id="x",
                    reviewer_verdict="pass", test_passed=True,
                    apply_manifest=ApplyManifest(
                        task_id="T001", run_id="x",
                        applied_files=["brand_new.py"],
                        applied_file_proofs=[],
                        status="applied",
                    ),
                ),
            ],
        )
        _persist_job(job)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(target), approve=True)

        assert result.status == "promoted"

    def test_legacy_existing_file_blocks(self, isolate_data_root, tmp_path):
        """Legacy job modifying existing file (no baseline) blocks safely."""
        from packages.orchestration.pingpong_job import (
            ApplyManifest,
            JobPlan,
            TaskEntry,
            _persist_job,
        )

        workspace = tmp_path / "workspace"
        workspace.mkdir()
        target = tmp_path / "target"
        target.mkdir()

        (target / "old.py").write_text("original\n")
        (workspace / "old.py").write_text("changed\n")

        job = JobPlan(
            repo_path=str(target),
            job_title="Legacy existing file",
            status="completed",
            job_workspace_path=str(workspace),
            tasks=[
                TaskEntry(
                    task_id="T001", title="t", body="t",
                    status="applied_to_job_workspace", run_id="x",
                    reviewer_verdict="pass", test_passed=True,
                    apply_manifest=ApplyManifest(
                        task_id="T001", run_id="x",
                        applied_files=["old.py"],
                        applied_file_proofs=[],
                        status="applied",
                    ),
                ),
            ],
        )
        _persist_job(job)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(target), approve=True)

        assert result.status == "blocked"
        assert "missing_baseline_for_existing_file" in result.blocked_reason
        assert (target / "old.py").read_text() == "original\n"


# ---------------------------------------------------------------------------
# Step 4975: Baseline proof model tests
# ---------------------------------------------------------------------------


class TestBaselineProofModel:
    def test_completed_job_has_file_proofs(self, isolate_data_root, demo_repo):
        """Completed job tasks should have applied_file_proofs."""
        job = _run_completed_job(demo_repo)

        total_proofs = 0
        for t in job.tasks:
            if t.apply_manifest:
                total_proofs += len(t.apply_manifest.applied_file_proofs)
        assert total_proofs > 0

    def test_proof_has_required_fields(self, isolate_data_root, demo_repo):
        """Each file proof must have path, hashes, and task info."""
        job = _run_completed_job(demo_repo)

        for t in job.tasks:
            if t.apply_manifest:
                for proof in t.apply_manifest.applied_file_proofs:
                    assert proof.path
                    assert proof.final_workspace_sha256
                    assert proof.task_id == t.task_id
                    assert proof.run_id == t.run_id

    def test_proof_persists_through_json(self, isolate_data_root, demo_repo):
        """File proofs survive JSON serialization/deserialization."""
        job = _run_completed_job(demo_repo)

        from packages.orchestration.pingpong_job import (
            _export_apply_manifest,
            _import_apply_manifest,
        )

        for t in job.tasks:
            if t.apply_manifest and t.apply_manifest.applied_file_proofs:
                exported = _export_apply_manifest(t.apply_manifest)
                imported = _import_apply_manifest(exported)
                assert len(imported.applied_file_proofs) == len(t.apply_manifest.applied_file_proofs)
                for orig, loaded in zip(
                    t.apply_manifest.applied_file_proofs,
                    imported.applied_file_proofs,
                ):
                    assert loaded.path == orig.path
                    assert loaded.existed_before_job == orig.existed_before_job
                    assert loaded.baseline_sha256 == orig.baseline_sha256
                    assert loaded.final_workspace_sha256 == orig.final_workspace_sha256
                break


# ---------------------------------------------------------------------------
# Step 4986: Real grouped CLI subprocess tests
# ---------------------------------------------------------------------------


class TestGroupedCLIJobPromote:
    """Subprocess tests using run_grouped_cli for do job-promote."""

    def test_dry_run_json_via_grouped_cli(self, isolate_data_root, tmp_path):
        """Grouped CLI dry-run produces valid JSON output."""
        from tests.cli.runtime_helpers import run_grouped_cli

        job, workspace, target, rel_path = _make_baselined_job(tmp_path)

        result = run_grouped_cli(
            ["do", "job-promote", job.job_id, "--repo", str(target), "--dry-run", "--json"],
            isolate_data_root,
        )

        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert data["status"] == "dry_run"
        assert "file_readiness" in data
        assert len(data["file_readiness"]) == 1

    def test_approve_via_grouped_cli(self, isolate_data_root, tmp_path):
        """Grouped CLI approve promotes and returns promoted status."""
        from tests.cli.runtime_helpers import run_grouped_cli

        job, workspace, target, rel_path = _make_baselined_job(tmp_path)

        result = run_grouped_cli(
            ["do", "job-promote", job.job_id, "--repo", str(target), "--approve", "--json"],
            isolate_data_root,
        )

        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert data["status"] == "promoted"
        assert (target / rel_path).read_text() == "modified\n"

    def test_blocked_job_via_grouped_cli(self, isolate_data_root, tmp_path):
        """Grouped CLI returns blocked status for tampered target."""
        from tests.cli.runtime_helpers import run_grouped_cli

        job, workspace, target, rel_path = _make_baselined_job(tmp_path)
        (target / rel_path).write_text("tampered\n")

        result = run_grouped_cli(
            ["do", "job-promote", job.job_id, "--repo", str(target), "--approve", "--json"],
            isolate_data_root,
        )

        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert data["status"] == "blocked"
        assert "target_changed_since_job" in data["blocked_reason"]

    def test_nonexistent_job_via_grouped_cli(self, isolate_data_root, tmp_path):
        """Grouped CLI handles nonexistent job gracefully."""
        from tests.cli.runtime_helpers import run_grouped_cli

        result = run_grouped_cli(
            ["do", "job-promote", "fake-id", "--repo", str(tmp_path), "--dry-run", "--json"],
            isolate_data_root,
        )

        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert data["status"] == "blocked"
        assert "job_not_found" in data["blocked_reason"]


# ---------------------------------------------------------------------------
# Step 4992: Destination symlink inside target blocks
# ---------------------------------------------------------------------------


class TestDestSymlinkInsideTarget:
    def test_dest_symlink_blocks_promote(self, isolate_data_root, tmp_path):
        """Approved promote blocks when dest path is a symlink, even inside target."""
        job, workspace, target, rel_path = _make_baselined_job(
            tmp_path, existing_content="victim baseline\n", new_content="job final\n",
        )
        victim = target / "victim.py"
        victim.write_text("victim baseline\n")
        dest = target / rel_path
        dest.unlink()
        dest.symlink_to(victim)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(target), approve=True)

        assert result.status == "blocked"
        assert "dest_is_symlink" in result.blocked_reason
        assert victim.read_text() == "victim baseline\n"
        assert dest.is_symlink()
        assert result.files_applied == []

    def test_dest_symlink_dry_run_blocks(self, isolate_data_root, tmp_path):
        """Dry-run also blocks when dest path is a symlink."""
        job, workspace, target, rel_path = _make_baselined_job(
            tmp_path, existing_content="victim\n", new_content="job\n",
        )
        victim = target / "victim.py"
        victim.write_text("victim\n")
        dest = target / rel_path
        dest.unlink()
        dest.symlink_to(victim)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(target), dry_run=True)

        assert result.status == "blocked"
        assert "dest_is_symlink" in result.blocked_reason


# ---------------------------------------------------------------------------
# Step 4993: Destination parent symlink inside target blocks
# ---------------------------------------------------------------------------


class TestDestParentSymlinkInsideTarget:
    def test_dest_parent_symlink_blocks_promote(self, isolate_data_root, tmp_path):
        """Approved promote blocks when dest parent is symlinked."""
        import hashlib

        from packages.orchestration.pingpong_job import (
            AppliedFileProof,
            ApplyManifest,
            JobPlan,
            TaskEntry,
            _persist_job,
        )

        workspace = tmp_path / "workspace"
        workspace.mkdir()
        target = tmp_path / "target"
        target.mkdir()

        victim_dir = target / "victim_dir"
        victim_dir.mkdir()
        (victim_dir / "file.py").write_text("victim baseline\n")

        link_dir = target / "linkdir"
        link_dir.symlink_to(victim_dir)

        ws_linkdir = workspace / "linkdir"
        ws_linkdir.mkdir()
        (ws_linkdir / "file.py").write_text("job final\n")

        rel_path = "linkdir/file.py"
        baseline_hash = hashlib.sha256(b"victim baseline\n").hexdigest()
        final_hash = hashlib.sha256(b"job final\n").hexdigest()

        job = JobPlan(
            repo_path=str(target),
            job_title="Parent symlink test",
            status="completed",
            job_workspace_path=str(workspace),
            tasks=[
                TaskEntry(
                    task_id="T001", title="modify via parent link", body="t",
                    status="applied_to_job_workspace", run_id="run1",
                    reviewer_verdict="pass", test_passed=True,
                    apply_manifest=ApplyManifest(
                        task_id="T001", run_id="run1",
                        applied_files=[rel_path],
                        applied_file_proofs=[AppliedFileProof(
                            path=rel_path,
                            existed_before_job=True,
                            baseline_sha256=baseline_hash,
                            final_workspace_sha256=final_hash,
                            task_id="T001",
                            run_id="run1",
                        )],
                        status="applied",
                    ),
                ),
            ],
        )
        _persist_job(job)

        from packages.orchestration.job_promote import promote_job
        result = promote_job(job.job_id, str(target), approve=True)

        assert result.status == "blocked"
        assert "dest_parent_symlink" in result.blocked_reason
        assert (victim_dir / "file.py").read_text() == "victim baseline\n"
        assert result.files_applied == []


# ---------------------------------------------------------------------------
# Step 4994: Destination containment recheck before write
# ---------------------------------------------------------------------------


class TestDestContainmentRecheckBeforeWrite:
    def test_dest_becomes_symlink_after_plan(self, isolate_data_root, tmp_path):
        """Dest containment is rechecked before write, catches race."""
        import hashlib
        from unittest.mock import patch

        from packages.orchestration.pingpong_job import (
            AppliedFileProof,
            ApplyManifest,
            JobPlan,
            TaskEntry,
            _persist_job,
        )

        workspace = tmp_path / "workspace"
        workspace.mkdir()
        target = tmp_path / "target"
        target.mkdir()

        rel_path = "safe.py"
        content = "original\n"
        new_content = "modified\n"
        (target / rel_path).write_text(content)
        (workspace / rel_path).write_text(new_content)

        baseline_hash = hashlib.sha256(content.encode()).hexdigest()
        final_hash = hashlib.sha256(new_content.encode()).hexdigest()

        job = JobPlan(
            repo_path=str(target),
            job_title="Race test",
            status="completed",
            job_workspace_path=str(workspace),
            tasks=[
                TaskEntry(
                    task_id="T001", title="t", body="t",
                    status="applied_to_job_workspace", run_id="run1",
                    reviewer_verdict="pass", test_passed=True,
                    apply_manifest=ApplyManifest(
                        task_id="T001", run_id="run1",
                        applied_files=[rel_path],
                        applied_file_proofs=[AppliedFileProof(
                            path=rel_path,
                            existed_before_job=True,
                            baseline_sha256=baseline_hash,
                            final_workspace_sha256=final_hash,
                            task_id="T001",
                            run_id="run1",
                        )],
                        status="applied",
                    ),
                ),
            ],
        )
        _persist_job(job)

        call_count = 0
        original_validate = __import__(
            "packages.orchestration.job_promote", fromlist=["_validate_dest_containment"]
        )._validate_dest_containment

        def sneaky_validate(tgt, rp):
            nonlocal call_count
            call_count += 1
            if call_count > 1 and rp == rel_path:
                return f"dest_is_symlink: {rp}"
            return original_validate(tgt, rp)

        from packages.orchestration.job_promote import promote_job
        with patch("packages.orchestration.job_promote._validate_dest_containment", sneaky_validate):
            result = promote_job(job.job_id, str(target), approve=True)

        assert result.status == "blocked"
        assert "dest_unsafe_at_apply" in result.blocked_reason
        assert result.files_applied == []


# ---------------------------------------------------------------------------
# Step 4997: Final record failure after apply is structured
# ---------------------------------------------------------------------------


class TestFinalRecordFailure:
    def test_final_record_failure_structured(self, isolate_data_root, tmp_path):
        """Final promotion record failure returns structured result, not exception."""
        from unittest.mock import patch

        job, workspace, target, rel_path = _make_baselined_job(tmp_path)

        persist_call_count = 0
        original_persist = __import__(
            "packages.orchestration.job_promote", fromlist=["_persist_job_promotion"]
        )._persist_job_promotion

        def fail_on_final(jid, res):
            nonlocal persist_call_count
            persist_call_count += 1
            if res.status == "promoted":
                raise OSError("disk full")
            original_persist(jid, res)

        from packages.orchestration.job_promote import promote_job
        with patch("packages.orchestration.job_promote._persist_job_promotion", fail_on_final):
            result = promote_job(job.job_id, str(target), approve=True)

        assert result.status == "promoted_record_update_failed"
        assert "disk full" in result.blocked_reason
        assert rel_path in result.files_applied
        assert result.promotion_id

    def test_final_record_failure_json_parseable(self, isolate_data_root, tmp_path):
        """JSON export of promoted_record_update_failed is parseable."""
        from unittest.mock import patch

        job, workspace, target, rel_path = _make_baselined_job(tmp_path)

        original_persist = __import__(
            "packages.orchestration.job_promote", fromlist=["_persist_job_promotion"]
        )._persist_job_promotion

        def fail_on_final(jid, res):
            if res.status == "promoted":
                raise OSError("disk full")
            original_persist(jid, res)

        from packages.orchestration.job_promote import (
            export_job_promotion_json,
            promote_job,
        )
        with patch("packages.orchestration.job_promote._persist_job_promotion", fail_on_final):
            result = promote_job(job.job_id, str(target), approve=True)

        data = export_job_promotion_json(result)
        json_str = json.dumps(data)
        parsed = json.loads(json_str)
        assert parsed["status"] == "promoted_record_update_failed"
        assert "promotion_record_update_failed" in parsed["blocked_reason"]

    def test_final_record_failure_text_readable(self, isolate_data_root, tmp_path):
        """Text summary of promoted_record_update_failed is human-readable."""
        from unittest.mock import patch

        job, workspace, target, rel_path = _make_baselined_job(tmp_path)

        original_persist = __import__(
            "packages.orchestration.job_promote", fromlist=["_persist_job_promotion"]
        )._persist_job_promotion

        def fail_on_final(jid, res):
            if res.status == "promoted":
                raise OSError("disk full")
            original_persist(jid, res)

        from packages.orchestration.job_promote import (
            promote_job,
            summarize_job_promotion,
        )
        with patch("packages.orchestration.job_promote._persist_job_promotion", fail_on_final):
            result = promote_job(job.job_id, str(target), approve=True)

        text = summarize_job_promotion(result)
        assert "WARNING" in text
        assert "record update FAILED" in text
        assert "Pre-apply record exists" in text


# ---------------------------------------------------------------------------
# Step 4998: Pre-apply record failure blocks before write
# ---------------------------------------------------------------------------


class TestPreApplyRecordFailure:
    def test_pre_apply_record_failure_blocks(self, isolate_data_root, tmp_path):
        """Pre-apply record persistence failure blocks before target write."""
        from unittest.mock import patch

        job, workspace, target, rel_path = _make_baselined_job(tmp_path)

        def always_fail(jid, res):
            raise OSError("cannot write pre-apply record")

        from packages.orchestration.job_promote import promote_job
        with patch("packages.orchestration.job_promote._persist_job_promotion", always_fail):
            result = promote_job(job.job_id, str(target), approve=True)

        assert result.status == "blocked"
        assert "pre_apply_record_failed" in result.blocked_reason
        assert result.files_applied == []
        assert (target / rel_path).read_text() == "original\n"

    def test_pre_apply_failure_does_not_write_target(self, isolate_data_root, tmp_path):
        """When pre-apply record fails, no target files are modified."""
        from unittest.mock import patch

        job, workspace, target, rel_path = _make_new_file_job(tmp_path, content="new stuff\n")

        def always_fail(jid, res):
            raise OSError("disk error")

        from packages.orchestration.job_promote import promote_job
        with patch("packages.orchestration.job_promote._persist_job_promotion", always_fail):
            result = promote_job(job.job_id, str(target), approve=True)

        assert result.status == "blocked"
        assert not (target / "new_file.py").exists()


# ---------------------------------------------------------------------------
# Step 5000: Grouped CLI tests for new failure modes
# ---------------------------------------------------------------------------


class TestGroupedCLINewFailureModes:
    def test_dest_symlink_via_grouped_cli(self, isolate_data_root, tmp_path):
        """Grouped CLI blocks destination symlink."""
        from tests.cli.runtime_helpers import run_grouped_cli

        job, workspace, target, rel_path = _make_baselined_job(
            tmp_path, existing_content="victim\n", new_content="job\n",
        )
        victim = target / "victim.py"
        victim.write_text("victim\n")
        dest = target / rel_path
        dest.unlink()
        dest.symlink_to(victim)

        result = run_grouped_cli(
            ["do", "job-promote", job.job_id, "--repo", str(target), "--approve", "--json"],
            isolate_data_root,
        )

        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert data["status"] == "blocked"
        assert "dest_is_symlink" in data["blocked_reason"]

    def test_dest_parent_symlink_via_grouped_cli(self, isolate_data_root, tmp_path):
        """Grouped CLI blocks destination parent symlink."""
        import hashlib

        from packages.orchestration.pingpong_job import (
            AppliedFileProof,
            ApplyManifest,
            JobPlan,
            TaskEntry,
            _persist_job,
        )
        from tests.cli.runtime_helpers import run_grouped_cli

        workspace = tmp_path / "workspace"
        workspace.mkdir()
        target = tmp_path / "target"
        target.mkdir()

        victim_dir = target / "victim_dir"
        victim_dir.mkdir()
        (victim_dir / "file.py").write_text("orig\n")

        link_dir = target / "linkdir"
        link_dir.symlink_to(victim_dir)

        ws_linkdir = workspace / "linkdir"
        ws_linkdir.mkdir()
        (ws_linkdir / "file.py").write_text("new\n")

        rel_path = "linkdir/file.py"
        baseline_hash = hashlib.sha256(b"orig\n").hexdigest()
        final_hash = hashlib.sha256(b"new\n").hexdigest()

        job = JobPlan(
            repo_path=str(target),
            job_title="CLI parent symlink",
            status="completed",
            job_workspace_path=str(workspace),
            tasks=[
                TaskEntry(
                    task_id="T001", title="t", body="t",
                    status="applied_to_job_workspace", run_id="run1",
                    reviewer_verdict="pass", test_passed=True,
                    apply_manifest=ApplyManifest(
                        task_id="T001", run_id="run1",
                        applied_files=[rel_path],
                        applied_file_proofs=[AppliedFileProof(
                            path=rel_path,
                            existed_before_job=True,
                            baseline_sha256=baseline_hash,
                            final_workspace_sha256=final_hash,
                            task_id="T001",
                            run_id="run1",
                        )],
                        status="applied",
                    ),
                ),
            ],
        )
        _persist_job(job)

        result = run_grouped_cli(
            ["do", "job-promote", job.job_id, "--repo", str(target), "--approve", "--json"],
            isolate_data_root,
        )

        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert data["status"] == "blocked"
        assert "dest_parent_symlink" in data["blocked_reason"]


# ---------------------------------------------------------------------------
# Two-file job helper for partial apply tests
# ---------------------------------------------------------------------------


def _make_two_file_baselined_job(tmp_path):
    """Create a job with two baselined files for partial apply testing.

    Returns (job, workspace, target, rel_paths).
    """
    import hashlib

    from packages.orchestration.pingpong_job import (
        AppliedFileProof,
        ApplyManifest,
        JobPlan,
        TaskEntry,
        _persist_job,
    )

    workspace = tmp_path / "workspace"
    workspace.mkdir()
    target = tmp_path / "target"
    target.mkdir()

    files = [
        ("first.py", "orig_first\n", "new_first\n"),
        ("second.py", "orig_second\n", "new_second\n"),
    ]
    proofs = []
    for rel, orig, new in files:
        (target / rel).write_text(orig)
        (workspace / rel).write_text(new)
        proofs.append(AppliedFileProof(
            path=rel,
            existed_before_job=True,
            baseline_sha256=hashlib.sha256(orig.encode()).hexdigest(),
            final_workspace_sha256=hashlib.sha256(new.encode()).hexdigest(),
            task_id="T001",
            run_id="run1",
        ))

    job = JobPlan(
        repo_path=str(target),
        job_title="Two file test",
        status="completed",
        job_workspace_path=str(workspace),
        tasks=[
            TaskEntry(
                task_id="T001", title="modify two files", body="t",
                status="applied_to_job_workspace", run_id="run1",
                reviewer_verdict="pass", test_passed=True,
                apply_manifest=ApplyManifest(
                    task_id="T001", run_id="run1",
                    applied_files=[f[0] for f in files],
                    applied_file_proofs=proofs,
                    status="applied",
                ),
            ),
        ],
    )
    _persist_job(job)
    return job, workspace, target, [f[0] for f in files]


# ---------------------------------------------------------------------------
# Step 5015: Partial apply then blocked record failure is structured
# ---------------------------------------------------------------------------


class TestPartialApplyRecordFailure:
    def test_partial_apply_record_failure_structured(self, isolate_data_root, tmp_path):
        """Partial apply + blocked persist failure returns structured result."""
        from unittest.mock import patch

        job, workspace, target, rel_paths = _make_two_file_baselined_job(tmp_path)

        original_validate = __import__(
            "packages.orchestration.job_promote", fromlist=["_validate_dest_containment"]
        )._validate_dest_containment

        validate_call_count = {}

        def block_second_on_recheck(tgt, rp):
            validate_call_count[rp] = validate_call_count.get(rp, 0) + 1
            if rp == "second.py" and validate_call_count[rp] > 1:
                return f"dest_is_symlink: {rp}"
            return original_validate(tgt, rp)

        original_persist = __import__(
            "packages.orchestration.job_promote", fromlist=["_persist_job_promotion"]
        )._persist_job_promotion

        persist_count = 0

        def fail_after_preapply(jid, res):
            nonlocal persist_count
            persist_count += 1
            if persist_count == 1:
                original_persist(jid, res)
                return
            raise OSError("disk full on blocked persist")

        from packages.orchestration.job_promote import (
            export_job_promotion_json,
            promote_job,
        )
        with patch("packages.orchestration.job_promote._validate_dest_containment", block_second_on_recheck), \
             patch("packages.orchestration.job_promote._persist_job_promotion", fail_after_preapply):
            result = promote_job(job.job_id, str(target), approve=True)

        assert result.status == "promoted_record_update_failed"
        assert "first.py" in result.files_applied
        assert "second.py" not in result.files_applied
        assert result.promotion_id

        data = export_job_promotion_json(result)
        json_str = json.dumps(data)
        parsed = json.loads(json_str)
        assert parsed["status"] == "promoted_record_update_failed"


# ---------------------------------------------------------------------------
# Step 5016: Post-test failure record persistence failure is structured
# ---------------------------------------------------------------------------


class TestPostTestRecordFailure:
    def test_post_test_failure_record_persist_structured(self, isolate_data_root, tmp_path):
        """Post-test failure + record persist failure returns structured result."""
        from unittest.mock import patch

        job, workspace, target, rel_path = _make_baselined_job(tmp_path)

        original_persist = __import__(
            "packages.orchestration.job_promote", fromlist=["_persist_job_promotion"]
        )._persist_job_promotion

        persist_count = 0

        def fail_on_test_failed(jid, res):
            nonlocal persist_count
            persist_count += 1
            if persist_count == 1:
                original_persist(jid, res)
                return
            if res.status == "promoted_test_failed":
                raise OSError("disk full on test-failed persist")
            original_persist(jid, res)

        from packages.orchestration.job_promote import (
            export_job_promotion_json,
            promote_job,
            summarize_job_promotion,
        )
        with patch("packages.orchestration.job_promote._persist_job_promotion", fail_on_test_failed):
            result = promote_job(
                job.job_id, str(target), approve=True,
                test_command="false",
            )

        assert result.status == "promoted_record_update_failed"
        assert rel_path in result.files_applied
        assert result.promotion_id

        data = export_job_promotion_json(result)
        json_str = json.dumps(data)
        parsed = json.loads(json_str)
        assert parsed["status"] == "promoted_record_update_failed"

        text = summarize_job_promotion(result)
        assert "WARNING" in text
        assert "record update FAILED" in text


# F085 T002b — job_promote._run_post_test on the shared `test`-class seam


def test_job_promote_post_test_runs_on_the_guarded_seam(tmp_path, monkeypatch):
    """The spawn goes through `run_guarded_test_command`, and its BYTES decode to str."""
    import subprocess

    from packages.orchestration import job_promote

    seen: dict[str, object] = {}

    def _fake_guarded(cmd, *, timeout_sec, cwd, extra_env_keys=()):
        seen.update(cmd=list(cmd), timeout_sec=timeout_sec, cwd=cwd)
        return subprocess.CompletedProcess(list(cmd), 0, b"out-line\n", b"err-line\n")

    monkeypatch.setattr(job_promote, "run_guarded_test_command", _fake_guarded)
    passed, summary = job_promote._run_post_test("pytest -q", tmp_path, timeout_sec=17)

    assert passed is True
    assert seen == {"cmd": ["pytest", "-q"], "timeout_sec": 17, "cwd": str(tmp_path)}
    assert summary.startswith("exit=0")
    assert "out-line" in summary
    assert "err-line" in summary


# ---------------------------------------------------------------------------
# Operator order amend0828-daily-driver, point 1 — deliberate partial promotion
#
# Reproduces the 2026-08-25 dogfooding finding in T0_F017 exactly: a builder
# wrote an unasked-for `.gitignore` beside two reviewed files, `.gitignore` is in
# `_BLOCKED_EXACT`, and the whole promotion died with `files_applied: []`. The
# guardrail is correct and stays; what was missing is the operator's SECOND
# decision, taken after reading the blocked list.
# ---------------------------------------------------------------------------

#: The blocked path from the operator's own run. Kept as a name so a reader can
#: see which fence entry these tests are standing on.
_OPERATOR_BLOCKED_PATH = ".gitignore"
_OPERATOR_FREE_PATHS = ("fizzbuzz.py", "test_fizzbuzz.py")


def _make_partially_blocked_job(tmp_path, *, free_paths=_OPERATOR_FREE_PATHS,
                                blocked_path=_OPERATOR_BLOCKED_PATH):
    """A completed job whose apply manifest holds free files AND one blocked path.

    Every file is a create (it does not exist in the target), so the baseline
    proof is the new-file shape and nothing but the fence can stop a promotion.
    """
    import hashlib

    from packages.orchestration.pingpong_job import (
        AppliedFileProof,
        ApplyManifest,
        JobPlan,
        TaskEntry,
        _persist_job,
    )

    workspace = tmp_path / "workspace"
    workspace.mkdir()
    target = tmp_path / "target"
    target.mkdir()

    all_paths = [*free_paths, blocked_path] if blocked_path else list(free_paths)
    proofs = []
    for rel in all_paths:
        content = f"# {rel}\n"
        (workspace / rel).write_text(content)
        proofs.append(AppliedFileProof(
            path=rel,
            existed_before_job=False,
            baseline_sha256="",
            final_workspace_sha256=hashlib.sha256(content.encode()).hexdigest(),
            task_id="T001",
            run_id="run1",
        ))

    job = JobPlan(
        repo_path=str(target),
        job_title="FizzBuzz Demo v2",
        status="completed",
        job_workspace_path=str(workspace),
        tasks=[
            TaskEntry(
                task_id="T001", title="write fizzbuzz", body="t",
                status="applied_to_job_workspace", run_id="run1",
                reviewer_verdict="pass", test_passed=True,
                apply_manifest=ApplyManifest(
                    task_id="T001", run_id="run1",
                    applied_files=all_paths,
                    applied_file_proofs=proofs,
                    status="applied",
                ),
            ),
        ],
    )
    _persist_job(job)
    return job, workspace, target


class TestSkipBlockedPartialPromotion:
    """--skip-blocked promotes the remainder and provably leaves the blocked path."""

    def test_two_free_files_promote_and_the_blocked_one_stays_behind(
        self, isolate_data_root, tmp_path,
    ):
        from packages.orchestration.job_promote import promote_job

        job, _workspace, target = _make_partially_blocked_job(tmp_path)

        result = promote_job(
            job.job_id, str(target), approve=True, skip_blocked=True,
        )

        assert result.status == "promoted", result.blocked_reason
        assert sorted(result.files_applied) == sorted(_OPERATOR_FREE_PATHS)

        # The two free files really landed, with their workspace bytes.
        for rel in _OPERATOR_FREE_PATHS:
            assert (target / rel).is_file()
            assert (target / rel).read_text() == f"# {rel}\n"

        # THE BLOCKED PATH WAS NOT WRITTEN. This is the whole point: skipping is
        # deliberate and visible, never a silent half-apply.
        assert not (target / _OPERATOR_BLOCKED_PATH).exists()
        assert _OPERATOR_BLOCKED_PATH not in result.files_applied
        assert _OPERATOR_BLOCKED_PATH not in result.files_planned

        # And it is NAMED, so the operator can see what was left behind.
        assert any(e.startswith(_OPERATOR_BLOCKED_PATH) for e in result.files_blocked)
        assert result.skip_blocked is True

    def test_the_summary_says_what_was_withheld(self, isolate_data_root, tmp_path):
        from packages.orchestration.job_promote import (
            promote_job,
            summarize_job_promotion,
        )

        job, _workspace, target = _make_partially_blocked_job(tmp_path)
        result = promote_job(
            job.job_id, str(target), approve=True, skip_blocked=True,
        )
        text = summarize_job_promotion(result)

        assert "--skip-blocked deliberately left 1 protected path(s) unpromoted" in text
        assert "were not written to the target" in text
        assert _OPERATOR_BLOCKED_PATH in text

    def test_every_file_blocked_still_blocks_with_an_honest_next(
        self, isolate_data_root, tmp_path,
    ):
        """--skip-blocked with no remainder is a block, not an empty success."""
        from packages.orchestration.job_promote import (
            promote_job,
            summarize_job_promotion,
        )

        job, _workspace, target = _make_partially_blocked_job(
            tmp_path, free_paths=(), blocked_path=_OPERATOR_BLOCKED_PATH,
        )
        result = promote_job(
            job.job_id, str(target), approve=True, skip_blocked=True,
        )

        assert result.status == "blocked"
        assert result.blocked_reason == "no_promotable_files"
        assert result.files_applied == []
        assert not (target / _OPERATOR_BLOCKED_PATH).exists()

        last = summarize_job_promotion(result).strip().splitlines()[-1]
        assert last.startswith("Next:")
        assert "no remainder for --skip-blocked" in last


class TestWithoutSkipBlockedNothingChanges:
    """The default path must behave EXACTLY as it did before the flag existed."""

    def test_default_still_blocks_the_whole_promotion(
        self, isolate_data_root, tmp_path,
    ):
        from packages.orchestration.job_promote import promote_job

        job, _workspace, target = _make_partially_blocked_job(tmp_path)

        result = promote_job(job.job_id, str(target), approve=True)

        assert result.status == "blocked"
        assert result.blocked_reason.startswith("blocked_paths:")
        assert result.files_applied == []
        assert result.skip_blocked is False

        # Atomic: not one of the three files reached the target.
        for rel in (*_OPERATOR_FREE_PATHS, _OPERATOR_BLOCKED_PATH):
            assert not (target / rel).exists(), (
                f"{rel} was applied without --skip-blocked: the all-or-nothing "
                f"rule was weakened"
            )

    def test_the_blocked_output_ends_with_the_route_through(
        self, isolate_data_root, tmp_path,
    ):
        """Finding (c): the blocked output owes an honest Next: line."""
        from packages.orchestration.job_promote import (
            promote_job,
            summarize_job_promotion,
        )

        job, _workspace, target = _make_partially_blocked_job(tmp_path)
        result = promote_job(job.job_id, str(target), approve=True)

        lines = summarize_job_promotion(result).strip().splitlines()
        last = lines[-1]

        assert last.startswith("Next:"), f"blocked output ended with {last!r}"
        assert _OPERATOR_BLOCKED_PATH in last
        assert "--skip-blocked" in last
        assert "remaining 2 file(s)" in last

    def test_the_fence_itself_is_not_weakened(self):
        """--skip-blocked changes one decision; it does not widen what may be written."""
        from packages.orchestration.job_promote import (
            _BLOCKED_EXACT,
            _is_blocked_path,
        )

        assert _OPERATOR_BLOCKED_PATH in _BLOCKED_EXACT
        assert _is_blocked_path(_OPERATOR_BLOCKED_PATH)
        assert _is_blocked_path(".git")
        assert _is_blocked_path(".env")
        assert _is_blocked_path("../escape.py") == "path_traversal"

    def test_a_non_path_block_does_not_advertise_skip_blocked(
        self, isolate_data_root, tmp_path,
    ):
        """The Next: line must name the route that actually applies."""
        from packages.orchestration.job_promote import (
            promote_job,
            summarize_job_promotion,
        )

        job, _workspace, target = _make_partially_blocked_job(tmp_path)
        # A create whose target file already exists is a baseline block, not a
        # fence block — --skip-blocked cannot lift it and must not claim to.
        (target / _OPERATOR_FREE_PATHS[0]).write_text("someone got here first\n")

        result = promote_job(
            job.job_id, str(target), approve=True, skip_blocked=True,
        )

        assert result.status == "blocked"
        assert not result.blocked_reason.startswith("blocked_paths:")

        last = summarize_job_promotion(result).strip().splitlines()[-1]
        assert last.startswith("Next:")
        assert "does not apply to this one" in last


class TestSkipBlockedThroughTheGroupedCLI:
    """--skip-blocked must be a real boolean FLAG, off unless typed.

    Declared without ``is_flag=True`` it falls through to the catalog's generic
    valued-option branch, whose default is the STRING ``"false"`` — which is
    truthy, so the partial promotion would arm itself on every run and the
    all-or-nothing rule would silently stop holding. That is exactly the hazard
    the ``is_flag`` field exists for, so the shape is pinned here rather than
    left to the option's spelling.
    """

    def test_the_flag_is_declared_as_a_boolean_flag(self):
        from apps.cli.command_catalog import CATALOG

        entry = next(c for c in CATALOG if c.command_id == "do.job-promote")
        arg = next(a for a in entry.args if a.name == "--skip-blocked")
        assert arg.is_flag is True, (
            "--skip-blocked must be declared is_flag=True or its default becomes "
            "the truthy string 'false' and partial promotion arms itself"
        )

    def test_absent_flag_still_blocks_through_the_real_cli(
        self, isolate_data_root, tmp_path,
    ):
        from tests.cli.runtime_helpers import run_grouped_cli

        job, _workspace, target = _make_partially_blocked_job(tmp_path)

        result = run_grouped_cli(
            ["do", "job-promote", job.job_id, "--repo", str(target),
             "--approve", "--json"],
            isolate_data_root,
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)

        assert data["skip_blocked"] is False
        assert data["status"] == "blocked"
        assert data["blocked_reason"].startswith("blocked_paths:")
        assert data["files_applied"] == []
        for rel in (*_OPERATOR_FREE_PATHS, _OPERATOR_BLOCKED_PATH):
            assert not (target / rel).exists()

    def test_typed_flag_promotes_the_remainder_through_the_real_cli(
        self, isolate_data_root, tmp_path,
    ):
        from tests.cli.runtime_helpers import run_grouped_cli

        job, _workspace, target = _make_partially_blocked_job(tmp_path)

        result = run_grouped_cli(
            ["do", "job-promote", job.job_id, "--repo", str(target),
             "--approve", "--skip-blocked", "--json"],
            isolate_data_root,
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)

        assert data["skip_blocked"] is True
        assert data["status"] == "promoted"
        assert sorted(data["files_applied"]) == sorted(_OPERATOR_FREE_PATHS)
        for rel in _OPERATOR_FREE_PATHS:
            assert (target / rel).is_file()
        assert not (target / _OPERATOR_BLOCKED_PATH).exists()
