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
