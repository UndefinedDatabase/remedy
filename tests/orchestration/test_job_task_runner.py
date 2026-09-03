"""Tests for the Job Task Runner (Steps 4827-4895).

Covers: job plan parsing, deterministic task IDs, strict workspace apply,
sequential execution, target repo guard, token-bounded context, report output,
blocking-path E2E, CLI dispatch, existing flow preservation, repair-round
CLI control, execution metadata, partial-run status, target mutation
negative guard, deterministic completion gate, continuation config,
pre-apply target guard, and post-apply target guard.
"""

from __future__ import annotations

import json
import types
from pathlib import Path

import pytest

from packages.orchestration.pingpong_job import (
    JOB_BLOCKED,
    JOB_COMPLETED,
    JOB_PAUSED,
    JOB_PLANNED,
    TASK_APPLIED,
    TASK_BLOCKED,
    TASK_FAILED,
    TASK_PASSED,
    TASK_PENDING,
    TASK_SKIPPED,
    TaskEntry,
    _build_task_prompt,
    _is_unsafe_path,
    _strict_apply_to_workspace,
    _suggest_next_command,
    export_job_report,
    format_job_report_text,
    load_job_plan,
    parse_job_file,
    plan_job_from_file,
    run_job,
    save_job_plan,
    task_entry_to_planned_task,
    validate_job_task_result,
)
from packages.orchestration.pingpong_provider import FakeProvider

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_TWO_TASK_JOB = """\
# Job: Improve report clarity

## Task 1
Clarify the repair-loop summary in the text report.

Acceptance:
- report still renders
- repair-loop tests pass

## Task 2
Add one focused test for repair-disabled output.

Acceptance:
- new test passes
- no unrelated files touched
"""

_NO_TASK_JOB = """\
# Job: Empty job

This file has no task headings.
"""

_NON_CONTIGUOUS_JOB = """\
# Job: Non-contiguous

## Task 7
First task (heading 7).

Acceptance:
- done

## Task 9
Second task (heading 9).

Acceptance:
- done
"""

_DUPLICATE_HEADING_JOB = """\
# Job: Duplicate headings

## Task 1
First occurrence.

Acceptance:
- done

## Task 1
Second occurrence.

Acceptance:
- done
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
    (repo / "README.md").write_text("# Demo\nA demo project.\n")
    (repo / "src").mkdir()
    (repo / "src" / "main.py").write_text("def hello():\n    return 'hello'\n")
    (repo / "docs").mkdir()
    (repo / "docs" / "README.md").write_text("# Docs\n")
    return repo


@pytest.fixture
def job_file(tmp_path: Path) -> Path:
    f = tmp_path / "job.md"
    f.write_text(_TWO_TASK_JOB)
    return f


def _run_success_job(demo_repo, **kwargs):
    """Helper: parse + run a two-task job with pass providers."""
    job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
    return run_job(
        job.job_id,
        builder_provider=_pass_provider(),
        reviewer_provider=_pass_provider(),
        repair_rounds=0,
        **kwargs,
    )


# ---------------------------------------------------------------------------
# Step 4832 — CLI command truth
# ---------------------------------------------------------------------------


class TestCliCommandTruth:
    def test_next_command_uses_hyphen_for_planned(self, isolate_data_root):
        job = parse_job_file(_TWO_TASK_JOB, "/tmp/repo")
        cmd = _suggest_next_command(job)
        assert "job-run" in cmd
        assert "job run" not in cmd.replace("job-run", "")

    def test_next_command_uses_hyphen_for_completed(self, isolate_data_root, demo_repo):
        result = _run_success_job(demo_repo)
        cmd = _suggest_next_command(result)
        assert "job-promote" in cmd
        assert "job promote" not in cmd.replace("job-promote", "")

    def test_next_command_uses_hyphen_for_blocked(self, isolate_data_root, demo_repo):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=FakeProvider(pass_on_round=99),
            reviewer_provider=FakeProvider(pass_on_round=99),
            max_rounds=1, repair_rounds=0,
        )
        cmd = _suggest_next_command(result)
        assert "job-report" in cmd

    def test_report_json_next_command_copyable(self, isolate_data_root, demo_repo):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        report = export_job_report(job)
        assert "remedy do job-run" in report["next_command"]

    def test_no_stale_space_commands_in_report(self, isolate_data_root, demo_repo):
        result = _run_success_job(demo_repo)
        report_json = json.dumps(export_job_report(result))
        text = format_job_report_text(result)
        for stale in ["remedy do job run", "remedy do job plan", "remedy do job report"]:
            # Must not appear as bare space-separated (allow "job-run" etc)
            cleaned = report_json.replace("job-run", "JR").replace("job-plan", "JP").replace("job-report", "JRE")
            assert stale not in cleaned
            cleaned_text = text.replace("job-run", "JR").replace("job-plan", "JP").replace("job-report", "JRE")
            assert stale not in cleaned_text


# ---------------------------------------------------------------------------
# Step 4833 — CLI E2E tests
# ---------------------------------------------------------------------------


class TestCliE2E:
    def test_catalog_has_job_plan(self):
        from apps.cli.command_catalog import CATALOG
        ids = [c.command_id for c in CATALOG]
        assert "do.job-plan" in ids

    def test_catalog_has_job_run(self):
        from apps.cli.command_catalog import CATALOG
        ids = [c.command_id for c in CATALOG]
        assert "do.job-run" in ids

    def test_catalog_has_job_report(self):
        from apps.cli.command_catalog import CATALOG
        ids = [c.command_id for c in CATALOG]
        assert "do.job-report" in ids

    def test_handlers_exist(self):
        from apps.cli.commands.do_cmd import COMMAND_HANDLERS
        assert "do.job-plan" in COMMAND_HANDLERS
        assert "do.job-run" in COMMAND_HANDLERS
        assert "do.job-report" in COMMAND_HANDLERS

    def test_job_plan_json_has_next_command(self, isolate_data_root, demo_repo):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        report = export_job_report(job)
        assert "remedy do job-run" in report["next_command"]
        assert job.job_id in report["next_command"]


# ---------------------------------------------------------------------------
# Step 4834 — Deterministic task IDs by parse order
# ---------------------------------------------------------------------------


class TestDeterministicTaskIds:
    def test_non_contiguous_headings(self, isolate_data_root):
        """## Task 7, ## Task 9 → T001, T002."""
        job = parse_job_file(_NON_CONTIGUOUS_JOB, "/tmp/repo")
        assert len(job.tasks) == 2
        assert job.tasks[0].task_id == "T001"
        assert job.tasks[1].task_id == "T002"

    def test_source_heading_preserved(self, isolate_data_root):
        """Original heading numbers stored in source_heading_number."""
        job = parse_job_file(_NON_CONTIGUOUS_JOB, "/tmp/repo")
        assert job.tasks[0].source_heading_number == 7
        assert job.tasks[1].source_heading_number == 9

    def test_duplicate_headings(self, isolate_data_root):
        """Duplicate ## Task 1, ## Task 1 → T001, T002."""
        job = parse_job_file(_DUPLICATE_HEADING_JOB, "/tmp/repo")
        assert len(job.tasks) == 2
        assert job.tasks[0].task_id == "T001"
        assert job.tasks[1].task_id == "T002"

    def test_task_order_preserved(self, isolate_data_root):
        job = parse_job_file(_NON_CONTIGUOUS_JOB, "/tmp/repo")
        assert "First task" in job.tasks[0].body or "heading 7" in job.tasks[0].body
        assert "Second task" in job.tasks[1].body or "heading 9" in job.tasks[1].body

    def test_standard_two_task(self, isolate_data_root):
        job = parse_job_file(_TWO_TASK_JOB, "/tmp/repo")
        assert job.tasks[0].task_id == "T001"
        assert job.tasks[1].task_id == "T002"


# ---------------------------------------------------------------------------
# Step 4835 — Strict workspace apply
# ---------------------------------------------------------------------------


class TestStrictWorkspaceApply:
    def test_unsafe_path_absolute(self):
        assert _is_unsafe_path("/etc/passwd") != ""

    def test_unsafe_path_traversal(self):
        assert _is_unsafe_path("../../etc/passwd") != ""

    def test_unsafe_path_env(self):
        assert _is_unsafe_path(".env") != ""
        assert _is_unsafe_path(".env.local") != ""
        assert _is_unsafe_path(".env-production") != ""

    def test_unsafe_path_git(self):
        assert _is_unsafe_path(".git/config") != ""

    def test_unsafe_path_private_key(self):
        assert _is_unsafe_path("secret.pem") != ""
        assert _is_unsafe_path("key.p12") != ""

    def test_unsafe_path_node_modules(self):
        assert _is_unsafe_path("node_modules/foo/bar.js") != ""

    def test_safe_path(self):
        assert _is_unsafe_path("docs/README.md") == ""
        assert _is_unsafe_path("src/main.py") == ""

    def test_manifest_records_applied_files(self, isolate_data_root, demo_repo):
        result = _run_success_job(demo_repo)
        for t in result.tasks:
            if t.apply_manifest:
                assert t.apply_manifest.status == "applied"
                assert len(t.apply_manifest.applied_files) > 0


# ---------------------------------------------------------------------------
# Step 4836 — Reuse promotion safety
# ---------------------------------------------------------------------------


class TestPromotionSafetyReuse:
    def test_traversal_blocked(self):
        assert "path_traversal" in _is_unsafe_path("../escape.txt")

    def test_env_blocked(self):
        assert "env_file" in _is_unsafe_path(".env")

    def test_git_blocked(self):
        assert "git_directory" in _is_unsafe_path(".git/HEAD")


# ---------------------------------------------------------------------------
# Step 4837 — Target repo snapshot guard
# ---------------------------------------------------------------------------


class TestTargetRepoGuard:
    def test_guard_passes_on_clean_run(self, isolate_data_root, demo_repo):
        result = _run_success_job(demo_repo)
        assert result.target_guard is not None
        assert result.target_guard.target_mutated is False

    def test_target_files_unchanged(self, isolate_data_root, demo_repo):
        readme_before = (demo_repo / "README.md").read_text()
        main_before = (demo_repo / "src" / "main.py").read_text()
        _run_success_job(demo_repo)
        assert (demo_repo / "README.md").read_text() == readme_before
        assert (demo_repo / "src" / "main.py").read_text() == main_before


# ---------------------------------------------------------------------------
# Step 4838 — Task completion gate
# ---------------------------------------------------------------------------


class TestTaskCompletionGate:
    def test_applied_requires_review_pass(self, isolate_data_root, demo_repo):
        result = _run_success_job(demo_repo)
        for t in result.tasks:
            if t.status == TASK_APPLIED:
                assert t.final_status == "staged_review_passed"

    def test_applied_requires_workspace_apply(self, isolate_data_root, demo_repo):
        result = _run_success_job(demo_repo)
        for t in result.tasks:
            if t.status == TASK_APPLIED:
                assert t.apply_manifest is not None
                assert t.apply_manifest.status == "applied"

    def test_failed_task_blocks_job(self, isolate_data_root, demo_repo):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=FakeProvider(pass_on_round=99),
            reviewer_provider=FakeProvider(pass_on_round=99),
            max_rounds=1, repair_rounds=0,
        )
        assert result.status == JOB_BLOCKED
        assert result.tasks[0].status in (TASK_FAILED, TASK_BLOCKED)
        assert result.tasks[1].status == TASK_SKIPPED


# ---------------------------------------------------------------------------
# Step 4839 — Per-task proof summaries
# ---------------------------------------------------------------------------


class TestProofSummaries:
    def test_proof_summary_recorded(self, isolate_data_root, demo_repo):
        result = _run_success_job(demo_repo)
        for t in result.tasks:
            if t.status == TASK_APPLIED:
                assert t.proof_summary is not None
                assert t.proof_summary.task_id == t.task_id
                assert t.proof_summary.run_id == t.run_id
                assert t.proof_summary.final_status == "staged_review_passed"

    def test_proof_summary_in_report(self, isolate_data_root, demo_repo):
        result = _run_success_job(demo_repo)
        report = export_job_report(result)
        for t in report["tasks"]:
            if t["status"] == TASK_APPLIED:
                assert t["proof_summary"] is not None
                assert t["proof_summary"]["task_id"] == t["task_id"]

    def test_proof_summary_has_applied_files(self, isolate_data_root, demo_repo):
        result = _run_success_job(demo_repo)
        for t in result.tasks:
            if t.proof_summary:
                assert isinstance(t.proof_summary.applied_files, list)


# ---------------------------------------------------------------------------
# Step 4840 — Token context policy
# ---------------------------------------------------------------------------


class TestTokenContextPolicy:
    def test_report_has_context_strategy(self, isolate_data_root, demo_repo):
        result = _run_success_job(demo_repo)
        report = export_job_report(result)
        cs = report["context_strategy"]
        assert cs["strategy"] == "task_bounded_sequential_job"
        assert cs["previous_task_summary_limit"] == 5
        assert cs["full_job_history_in_prompt"] is False
        assert cs["full_repo_in_prompt"] is False


# ---------------------------------------------------------------------------
# Step 4841 — Token-bounded prompt tests
# ---------------------------------------------------------------------------


class TestTokenBoundedPrompt:
    def test_task_body_bounded(self, isolate_data_root):
        big_body = "x" * 5000
        text = f"# Job: Test\n\n## Task 1\n{big_body}\n"
        job = parse_job_file(text, "/tmp/repo")
        assert len(job.tasks[0].body) <= 2020
        assert "[truncated]" in job.tasks[0].body

    def test_task2_prompt_has_bounded_task1_summary(self, isolate_data_root, demo_repo):
        from packages.orchestration.pingpong_job import TaskProofSummary

        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        ps = TaskProofSummary(
            task_id="T001", title="Fix readme",
            run_id="abc123", final_status="staged_review_passed",
            applied_files=["docs/README.md"],
            reviewer_verdict="pass",
        )
        prompt = _build_task_prompt(job, job.tasks[1], [ps])
        assert "T001" in prompt
        assert "Fix readme" in prompt
        assert "staged_review_passed" in prompt
        assert "docs/README.md" in prompt

    def test_task2_prompt_no_full_body(self, isolate_data_root, demo_repo):
        from packages.orchestration.pingpong_job import TaskProofSummary

        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        ps = TaskProofSummary(
            task_id="T001", title="Fix readme",
            run_id="abc123", final_status="staged_review_passed",
        )
        prompt = _build_task_prompt(job, job.tasks[1], [ps])
        # Task 1 body should NOT appear in task 2 prompt
        assert "repair-loop summary" not in prompt

    def test_only_last_n_summaries(self, isolate_data_root, demo_repo):
        from packages.orchestration.pingpong_job import TaskProofSummary

        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        # Create 7 summaries — only last 5 should appear in Previous tasks
        summaries = [
            TaskProofSummary(
                task_id=f"T{i:03d}", title=f"Task {i}",
                run_id=f"run{i}", final_status="staged_review_passed",
            )
            for i in range(1, 8)
        ]
        prompt = _build_task_prompt(job, job.tasks[0], summaries)
        # T001, T002 are in first 2 summaries — excluded by [-5:]
        # But T001 also appears as "Current task: T001" — check Previous section only
        prev_section = prompt.split("## Current task:")[0]
        assert "T001" not in prev_section
        assert "T002" not in prev_section
        assert "T003" in prev_section
        assert "T007" in prev_section

    def test_prompt_length_bounded(self, isolate_data_root):
        big_body = "x" * 5000
        text = f"# Job: Test\n\n## Task 1\n{big_body}\n## Task 2\nSmall task.\n"
        job = parse_job_file(text, "/tmp/repo")
        prompt = _build_task_prompt(job, job.tasks[1], [])
        # Task body is truncated at parse time, prompt should be reasonable
        assert len(prompt) < 3000


# ---------------------------------------------------------------------------
# Step 4842 — Blocking-path E2E tests
# ---------------------------------------------------------------------------


class TestBlockingPathE2E:
    def test_missing_staged_file_blocks(self, isolate_data_root, demo_repo):
        """Missing staged source file blocks workspace apply."""

        class FakeResult:
            staging_path = str(demo_repo)  # exists but file won't be there
            staged_files = ["nonexistent/file.py"]
            run_id = "test_run"

        from packages.orchestration.pingpong_job import TaskEntry
        task = TaskEntry(task_id="T001")
        manifest = _strict_apply_to_workspace(task, FakeResult(), str(demo_repo))
        assert manifest.status == "blocked"
        assert len(manifest.missing_files) > 0

    def test_unsupported_env_blocks(self, isolate_data_root, demo_repo):
        """Staged .env file blocks workspace apply."""

        class FakeResult:
            staging_path = str(demo_repo)
            staged_files = [".env"]
            run_id = "test_run"

        from packages.orchestration.pingpong_job import TaskEntry
        task = TaskEntry(task_id="T001")
        manifest = _strict_apply_to_workspace(task, FakeResult(), str(demo_repo))
        assert manifest.status == "blocked"
        assert len(manifest.unsupported_files) > 0

    def test_traversal_blocks(self, isolate_data_root, demo_repo):
        """Path traversal in staged files blocks workspace apply."""

        class FakeResult:
            staging_path = str(demo_repo)
            staged_files = ["../../etc/passwd"]
            run_id = "test_run"

        from packages.orchestration.pingpong_job import TaskEntry
        task = TaskEntry(task_id="T001")
        manifest = _strict_apply_to_workspace(task, FakeResult(), str(demo_repo))
        assert manifest.status == "blocked"
        assert len(manifest.unsupported_files) > 0

    def test_duplicate_files_block(self, isolate_data_root, demo_repo):
        """Duplicate staged file paths block workspace apply."""

        class FakeResult:
            staging_path = str(demo_repo)
            staged_files = ["README.md", "README.md"]
            run_id = "test_run"

        from packages.orchestration.pingpong_job import TaskEntry
        task = TaskEntry(task_id="T001")
        manifest = _strict_apply_to_workspace(task, FakeResult(), str(demo_repo))
        assert manifest.status == "blocked"
        assert len(manifest.duplicate_files) > 0

    def test_task_not_applied_when_blocked(self, isolate_data_root, demo_repo):
        """Task status is not APPLIED when workspace apply blocks."""
        # This is implicitly tested by the sequential tests, but let's be explicit
        from packages.orchestration.pingpong_job import TaskEntry
        task = TaskEntry(task_id="T001", status=TASK_PASSED)

        class FakeResult:
            staging_path = str(demo_repo)
            staged_files = [".env"]
            run_id = "test_run"

        manifest = _strict_apply_to_workspace(task, FakeResult(), str(demo_repo))
        assert manifest.status == "blocked"
        # Task stays PASSED, not APPLIED
        assert task.status == TASK_PASSED


# ---------------------------------------------------------------------------
# Step 5006: Staged source symlink outside staging blocks
# ---------------------------------------------------------------------------


class TestStagedSourceSymlinkBlocks:
    def test_staged_source_symlink_blocks(self, isolate_data_root, tmp_path):
        """Staged file that is a symlink to outside staging is blocked."""
        staging = tmp_path / "staging"
        staging.mkdir()
        workspace = tmp_path / "workspace"
        workspace.mkdir()

        external = tmp_path / "secret.txt"
        external.write_text("secret content\n")
        (staging / "leak.txt").symlink_to(external)

        class FakeResult:
            staging_path = str(staging)
            staged_files = ["leak.txt"]
            run_id = "run1"

        from packages.orchestration.pingpong_job import TaskEntry
        task = TaskEntry(task_id="T001")
        manifest = _strict_apply_to_workspace(task, FakeResult(), str(workspace))

        assert manifest.status == "blocked"
        assert any("staging_source_is_symlink" in f for f in manifest.unsupported_files)
        assert not (workspace / "leak.txt").exists()

    def test_staged_source_symlink_inside_staging_also_blocks(self, isolate_data_root, tmp_path):
        """Even a symlink resolving inside staging is blocked."""
        staging = tmp_path / "staging"
        staging.mkdir()
        workspace = tmp_path / "workspace"
        workspace.mkdir()

        (staging / "real.txt").write_text("real content\n")
        (staging / "link.txt").symlink_to(staging / "real.txt")

        class FakeResult:
            staging_path = str(staging)
            staged_files = ["link.txt"]
            run_id = "run1"

        from packages.orchestration.pingpong_job import TaskEntry
        task = TaskEntry(task_id="T001")
        manifest = _strict_apply_to_workspace(task, FakeResult(), str(workspace))

        assert manifest.status == "blocked"
        assert any("staging_source_is_symlink" in f for f in manifest.unsupported_files)


# ---------------------------------------------------------------------------
# Step 5007: Staged source parent symlink blocks
# ---------------------------------------------------------------------------


class TestStagedSourceParentSymlinkBlocks:
    def test_staged_parent_symlink_blocks(self, isolate_data_root, tmp_path):
        """Parent directory symlink in staging path blocks apply."""
        staging = tmp_path / "staging"
        staging.mkdir()
        workspace = tmp_path / "workspace"
        workspace.mkdir()

        outside_dir = tmp_path / "outside_dir"
        outside_dir.mkdir()
        (outside_dir / "file.py").write_text("outside content\n")

        (staging / "linkdir").symlink_to(outside_dir)

        class FakeResult:
            staging_path = str(staging)
            staged_files = ["linkdir/file.py"]
            run_id = "run1"

        from packages.orchestration.pingpong_job import TaskEntry
        task = TaskEntry(task_id="T001")
        manifest = _strict_apply_to_workspace(task, FakeResult(), str(workspace))

        assert manifest.status == "blocked"
        assert any("staging_source_parent_symlink" in f for f in manifest.unsupported_files)
        assert not (workspace / "linkdir" / "file.py").exists()


# ---------------------------------------------------------------------------
# Step 5009: Workspace destination symlink blocks
# ---------------------------------------------------------------------------


class TestWorkspaceDestSymlinkBlocks:
    def test_workspace_dest_symlink_blocks(self, isolate_data_root, tmp_path):
        """Workspace destination symlink blocks apply."""
        staging = tmp_path / "staging"
        staging.mkdir()
        workspace = tmp_path / "workspace"
        workspace.mkdir()

        (workspace / "victim.py").write_text("victim baseline\n")
        (workspace / "planned.py").symlink_to(workspace / "victim.py")
        (staging / "planned.py").write_text("job final\n")

        class FakeResult:
            staging_path = str(staging)
            staged_files = ["planned.py"]
            run_id = "run1"

        from packages.orchestration.pingpong_job import TaskEntry
        task = TaskEntry(task_id="T001")
        manifest = _strict_apply_to_workspace(task, FakeResult(), str(workspace))

        assert manifest.status == "blocked"
        assert any("workspace_dest_is_symlink" in f for f in manifest.unsupported_files)
        assert (workspace / "victim.py").read_text() == "victim baseline\n"
        assert (workspace / "planned.py").is_symlink()
        assert len(manifest.applied_files) == 0


# ---------------------------------------------------------------------------
# Step 5010: Workspace destination parent symlink blocks
# ---------------------------------------------------------------------------


class TestWorkspaceDestParentSymlinkBlocks:
    def test_workspace_dest_parent_symlink_blocks(self, isolate_data_root, tmp_path):
        """Workspace destination parent symlink blocks apply."""
        staging = tmp_path / "staging"
        staging.mkdir()
        workspace = tmp_path / "workspace"
        workspace.mkdir()

        victim_dir = workspace / "victim_dir"
        victim_dir.mkdir()
        (victim_dir / "file.py").write_text("victim content\n")

        (workspace / "linkdir").symlink_to(victim_dir)

        staging_linkdir = staging / "linkdir"
        staging_linkdir.mkdir()
        (staging_linkdir / "file.py").write_text("job final\n")

        class FakeResult:
            staging_path = str(staging)
            staged_files = ["linkdir/file.py"]
            run_id = "run1"

        from packages.orchestration.pingpong_job import TaskEntry
        task = TaskEntry(task_id="T001")
        manifest = _strict_apply_to_workspace(task, FakeResult(), str(workspace))

        assert manifest.status == "blocked"
        assert any("workspace_dest_parent_symlink" in f for f in manifest.unsupported_files)
        assert (victim_dir / "file.py").read_text() == "victim content\n"
        assert len(manifest.applied_files) == 0


# ---------------------------------------------------------------------------
# Step 5012: Copy does not follow symlinks (safe read/write)
# ---------------------------------------------------------------------------


class TestSafeCopyNoSymlinkFollow:
    def test_normal_file_copies_correctly(self, isolate_data_root, tmp_path):
        """Normal (non-symlink) file copies via read_bytes/write_bytes."""
        staging = tmp_path / "staging"
        staging.mkdir()
        workspace = tmp_path / "workspace"
        workspace.mkdir()

        (staging / "normal.py").write_text("normal content\n")

        class FakeResult:
            staging_path = str(staging)
            staged_files = ["normal.py"]
            run_id = "run1"

        from packages.orchestration.pingpong_job import TaskEntry
        task = TaskEntry(task_id="T001")
        manifest = _strict_apply_to_workspace(task, FakeResult(), str(workspace))

        assert manifest.status == "applied"
        assert (workspace / "normal.py").read_text() == "normal content\n"
        assert not (workspace / "normal.py").is_symlink()


# ---------------------------------------------------------------------------
# Step 4843 — Existing flows preserved
# ---------------------------------------------------------------------------


class TestExistingFlowsPreserved:
    def test_two_task_success(self, isolate_data_root, demo_repo):
        result = _run_success_job(demo_repo)
        assert result.status == JOB_COMPLETED
        assert result.tasks[0].status == TASK_APPLIED
        assert result.tasks[1].status == TASK_APPLIED

    def test_max_tasks_partial(self, isolate_data_root, demo_repo):
        result = _run_success_job(demo_repo, max_tasks=1)
        assert result.tasks[0].status == TASK_APPLIED
        assert result.tasks[1].status == TASK_PENDING

    def test_run_ids_unique(self, isolate_data_root, demo_repo):
        result = _run_success_job(demo_repo)
        assert result.tasks[0].run_id != result.tasks[1].run_id

    def test_report_json_serializable(self, isolate_data_root, demo_repo):
        result = _run_success_job(demo_repo)
        text = json.dumps(export_job_report(result), indent=2)
        assert "job_id" in text

    def test_text_report_concise(self, isolate_data_root, demo_repo):
        result = _run_success_job(demo_repo)
        text = format_job_report_text(result)
        assert "T001" in text
        assert "NOT mutated" in text

    def test_single_task_run_still_works(self, isolate_data_root, tmp_path):
        from packages.orchestration.pingpong_loop import run_pingpong
        repo = tmp_path / "repo2"
        repo.mkdir()
        (repo / "README.md").write_text("# Demo\n")
        (repo / "docs").mkdir()
        (repo / "docs" / "README.md").write_text("# Docs\n")
        result = run_pingpong(
            "Fix README", str(repo),
            builder_name="fake", reviewer_name="fake",
        )
        assert result.final_status in (
            "staged_review_passed", "max_rounds_reached",
            "staged_blocked", "repair_exhausted",
        )

    def test_repair_governance_still_works(self, isolate_data_root):
        from packages.orchestration.pingpong_loop import resolve_repair_rounds
        val, src = resolve_repair_rounds(None)
        assert val == 2 and src == "default"
        val, src = resolve_repair_rounds(0)
        assert val == 0 and src == "cli"

    def test_evidence_import_still_works(self):
        from packages.orchestration.pingpong_evidence import export_evidence
        assert callable(export_evidence)

    def test_promotion_import_still_works(self):
        from packages.orchestration.pingpong_promote import promote_run
        assert callable(promote_run)


# ---------------------------------------------------------------------------
# Persistence round-trip
# ---------------------------------------------------------------------------


class TestPersistence:
    def test_persist_and_load(self, isolate_data_root):
        job = parse_job_file(_TWO_TASK_JOB, "/tmp/repo")
        loaded = load_job_plan(job.job_id)
        assert loaded is not None
        assert loaded.job_id == job.job_id
        assert len(loaded.tasks) == 2
        assert loaded.tasks[0].task_id == "T001"
        assert loaded.tasks[0].source_heading_number == 1

    def test_load_nonexistent(self, isolate_data_root):
        assert load_job_plan("nonexistent_id") is None

    def test_metadata_round_trips_through_persist_and_load(self, isolate_data_root):
        job = parse_job_file(_TWO_TASK_JOB, "/tmp/repo")
        job.metadata["escalations"] = [{"decision_id": "D1", "status": "open"}]
        save_job_plan(job)

        loaded = load_job_plan(job.job_id)

        assert loaded is not None
        assert loaded.metadata == {"escalations": [{"decision_id": "D1", "status": "open"}]}

    def test_metadata_defaults_to_an_empty_dict(self, isolate_data_root):
        job = parse_job_file(_TWO_TASK_JOB, "/tmp/repo")

        loaded = load_job_plan(job.job_id)

        assert loaded is not None
        assert loaded.metadata == {}

    def test_task_class_defaults_to_standard_build(self, isolate_data_root):
        job = parse_job_file(_TWO_TASK_JOB, "/tmp/repo")
        assert job.tasks[0].task_class == "standard_build"

        loaded = load_job_plan(job.job_id)

        assert loaded is not None
        assert loaded.tasks[0].task_class == "standard_build"

    def test_task_class_round_trips_through_persist_and_load(self, isolate_data_root):
        job = parse_job_file(_TWO_TASK_JOB, "/tmp/repo")
        job.tasks[0].task_class = "architecture"
        save_job_plan(job)

        loaded = load_job_plan(job.job_id)

        assert loaded is not None
        assert loaded.tasks[0].task_class == "architecture"

    def test_default_task_class_is_a_seeded_model_routing_class(self):
        from packages.orchestration.model_routing import TASK_CLASS_TIERS
        from packages.orchestration.pingpong_job import TASK_CLASS_DEFAULT
        assert TASK_CLASS_DEFAULT in TASK_CLASS_TIERS

    def test_persist_with_manifests(self, isolate_data_root, demo_repo):
        result = _run_success_job(demo_repo)
        loaded = load_job_plan(result.job_id)
        assert loaded is not None
        for t in loaded.tasks:
            if t.status == TASK_APPLIED:
                assert t.apply_manifest is not None
                assert t.proof_summary is not None


# ---------------------------------------------------------------------------
# Job plan parsing
# ---------------------------------------------------------------------------


class TestJobPlanParsing:
    def test_parses_two_tasks(self, isolate_data_root):
        job = parse_job_file(_TWO_TASK_JOB, "/tmp/repo")
        assert len(job.tasks) == 2
        assert job.status == JOB_PLANNED

    def test_job_title_extracted(self, isolate_data_root):
        job = parse_job_file(_TWO_TASK_JOB, "/tmp/repo")
        assert "report clarity" in job.job_title.lower()

    def test_acceptance_extracted(self, isolate_data_root):
        job = parse_job_file(_TWO_TASK_JOB, "/tmp/repo")
        assert "repair-loop tests pass" in job.tasks[0].acceptance

    def test_no_tasks_blocks(self, isolate_data_root):
        job = parse_job_file(_NO_TASK_JOB, "/tmp/repo")
        assert job.status == JOB_BLOCKED
        assert "no_tasks_found" in job.error

    def test_sha256_recorded(self, isolate_data_root):
        job = parse_job_file(_TWO_TASK_JOB, "/tmp/repo")
        assert len(job.job_file_sha256) == 64

    def test_plan_from_file(self, isolate_data_root, job_file, demo_repo):
        job = plan_job_from_file(str(job_file), str(demo_repo))
        assert len(job.tasks) == 2

    def test_plan_file_not_found(self, isolate_data_root):
        job = plan_job_from_file("/nonexistent/job.md", "/tmp/repo")
        assert job.status == JOB_BLOCKED

    def test_no_provider_call(self, isolate_data_root):
        job = parse_job_file(_TWO_TASK_JOB, "/tmp/repo")
        assert job.status == JOB_PLANNED


# ---------------------------------------------------------------------------
# Step 4845 — Preserve explicit --repair-rounds 0
# ---------------------------------------------------------------------------


class TestRepairRoundsCoercion:
    def test_resolve_none_gives_default(self):
        from packages.orchestration.pingpong_loop import resolve_repair_rounds
        val, src = resolve_repair_rounds(None)
        assert val == 2
        assert src == "default"

    def test_resolve_zero_stays_zero(self):
        from packages.orchestration.pingpong_loop import resolve_repair_rounds
        val, src = resolve_repair_rounds(0)
        assert val == 0
        assert src == "cli"

    def test_resolve_one_stays_one(self):
        from packages.orchestration.pingpong_loop import resolve_repair_rounds
        val, src = resolve_repair_rounds(1)
        assert val == 1
        assert src == "cli"

    def test_negative_raises(self):
        from packages.orchestration.pingpong_loop import resolve_repair_rounds
        with pytest.raises(ValueError, match="must be >= 0"):
            resolve_repair_rounds(-1)

    def test_above_hard_cap_raises(self):
        from packages.orchestration.pingpong_loop import resolve_repair_rounds
        with pytest.raises(ValueError, match="must be <="):
            resolve_repair_rounds(99)

    def test_job_run_explicit_zero(self, isolate_data_root, demo_repo):
        """run_job with repair_rounds=0 must NOT coerce to 2."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
            repair_rounds_source="cli",
        )
        assert result.repair_rounds_allowed == 0
        assert result.repair_rounds_source == "cli"
        for t in result.tasks:
            if t.status == TASK_APPLIED:
                assert t.repair_rounds_allowed == 0

    def test_job_run_default_two(self, isolate_data_root, demo_repo):
        """run_job with repair_rounds=2/default source records correctly."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=2,
            repair_rounds_source="default",
        )
        assert result.repair_rounds_allowed == 2
        assert result.repair_rounds_source == "default"


# ---------------------------------------------------------------------------
# Steps 4848-4850 — Real CLI handler path tests
# ---------------------------------------------------------------------------


def _make_args(**kwargs):
    """Build a namespace that mimics argparse output for do.job-run.

    Continuation-critical args default to None (omitted). Pass explicit
    values to simulate CLI flags. This matches catalog default=None.
    """
    ns = types.SimpleNamespace()
    ns.job_id = kwargs.get("job_id", "test_job")
    ns.builder = kwargs.get("builder", None)
    ns.reviewer = kwargs.get("reviewer", None)
    ns.max_rounds = kwargs.get("max_rounds", None)
    ns.repair_rounds = kwargs.get("repair_rounds", None)
    ns.test_command = kwargs.get("test_command", None)
    ns.claude_cli_write_mode = kwargs.get("claude_cli_write_mode", None)
    ns.max_tasks = kwargs.get("max_tasks", "0")
    ns.json = kwargs.get("json", True)
    return ns


class TestCliHandlerRepairRounds:
    def test_omitted_gives_default(self, isolate_data_root, demo_repo, capsys):
        """CLI handler with no --repair-rounds uses default 2."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        args = _make_args(job_id=job.job_id)

        from apps.cli.commands.do_cmd import COMMAND_HANDLERS
        COMMAND_HANDLERS["do.job-run"](args)

        out = capsys.readouterr().out
        data = json.loads(out)
        assert data["repair_rounds_allowed"] == 2
        assert data["repair_rounds_source"] == "default"

    def test_explicit_zero(self, isolate_data_root, demo_repo, capsys):
        """CLI handler with --repair-rounds 0 passes 0, not coerced to 2."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        args = _make_args(job_id=job.job_id, repair_rounds=0)

        from apps.cli.commands.do_cmd import COMMAND_HANDLERS
        COMMAND_HANDLERS["do.job-run"](args)

        out = capsys.readouterr().out
        data = json.loads(out)
        assert data["repair_rounds_allowed"] == 0
        assert data["repair_rounds_source"] == "cli"

    def test_explicit_one(self, isolate_data_root, demo_repo, capsys):
        """CLI handler with --repair-rounds 1 passes 1."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        args = _make_args(job_id=job.job_id, repair_rounds=1)

        from apps.cli.commands.do_cmd import COMMAND_HANDLERS
        COMMAND_HANDLERS["do.job-run"](args)

        out = capsys.readouterr().out
        data = json.loads(out)
        assert data["repair_rounds_allowed"] == 1
        assert data["repair_rounds_source"] == "cli"

    def test_explicit_zero_no_repair_attempt(self, isolate_data_root, demo_repo):
        """With repair_rounds=0, reviewer findings don't trigger repair."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
            repair_rounds_source="cli",
        )
        for t in result.tasks:
            if t.status == TASK_APPLIED:
                assert t.repair_rounds_used == 0

    def test_report_shows_repair_disabled(self, isolate_data_root, demo_repo):
        """Job report text shows repair disabled when rounds=0."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
            repair_rounds_source="cli",
        )
        text = format_job_report_text(result)
        assert "disabled" in text.lower() or "0 rounds" in text

    def test_report_json_repair_source(self, isolate_data_root, demo_repo):
        """Job report JSON includes repair_rounds_source."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
            repair_rounds_source="cli",
        )
        report = export_job_report(result)
        assert report["repair_rounds_allowed"] == 0
        assert report["repair_rounds_source"] == "cli"


# ---------------------------------------------------------------------------
# Step 4851 — Command catalog execution metadata
# ---------------------------------------------------------------------------


class TestCatalogMetadata:
    def test_job_run_may_execute_commands(self):
        from apps.cli.command_catalog import CATALOG
        entry = [c for c in CATALOG if c.command_id == "do.job-run"][0]
        assert entry.may_execute_commands is True

    def test_job_run_no_mutate_repo(self):
        from apps.cli.command_catalog import CATALOG
        entry = [c for c in CATALOG if c.command_id == "do.job-run"][0]
        assert entry.may_mutate_repo is False

    def test_job_plan_no_execute(self):
        from apps.cli.command_catalog import CATALOG
        entry = [c for c in CATALOG if c.command_id == "do.job-plan"][0]
        assert entry.may_execute_commands is False

    def test_job_report_no_execute(self):
        from apps.cli.command_catalog import CATALOG
        entry = [c for c in CATALOG if c.command_id == "do.job-report"][0]
        assert entry.may_execute_commands is False


# ---------------------------------------------------------------------------
# Step 4852 — Target repo mutation guard NEGATIVE test
# ---------------------------------------------------------------------------


class TestTargetMutationNegative:
    def test_target_mutation_blocks_job(self, isolate_data_root, demo_repo, monkeypatch):
        """If target repo is mutated during job, job is blocked."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))

        call_count = [0]

        import packages.orchestration.pingpong_loop as pp_mod
        real_run = pp_mod.run_pingpong

        def mutating_run(*args, **kwargs):
            result = real_run(*args, **kwargs)
            call_count[0] += 1
            if call_count[0] == 1:
                (demo_repo / "INJECTED.txt").write_text("malicious mutation")
            return result

        monkeypatch.setattr(pp_mod, "run_pingpong", mutating_run)

        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
            repair_rounds_source="cli",
        )

        assert result.status == JOB_BLOCKED
        assert result.target_guard is not None
        assert result.target_guard.target_mutated is True
        assert "INJECTED.txt" in result.target_guard.changed_target_files
        assert any(
            t.status in (TASK_BLOCKED, TASK_FAILED) or t.error
            for t in result.tasks
        )
        assert result.tasks[1].status in (TASK_SKIPPED, TASK_BLOCKED, TASK_PENDING)

    def test_mutation_reports_changed_files(self, isolate_data_root, demo_repo, monkeypatch):
        """Blocked job report lists which target files changed."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))

        import packages.orchestration.pingpong_loop as pp_mod
        real_run = pp_mod.run_pingpong

        def mutating_run(*args, **kwargs):
            result = real_run(*args, **kwargs)
            (demo_repo / "README.md").write_text("overwritten")
            return result

        monkeypatch.setattr(pp_mod, "run_pingpong", mutating_run)

        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )

        report = export_job_report(result)
        guard = report["target_guard"]
        assert guard["target_mutated"] is True
        assert len(guard["changed_target_files"]) > 0


# ---------------------------------------------------------------------------
# Step 4853 — Partial-run status (paused)
# ---------------------------------------------------------------------------


class TestPartialRunStatus:
    def test_max_tasks_gives_paused(self, isolate_data_root, demo_repo):
        """--max-tasks 1 on 2-task job sets status to paused."""
        result = _run_success_job(demo_repo, max_tasks=1)
        assert result.status == JOB_PAUSED
        assert result.tasks[0].status == TASK_APPLIED
        assert result.tasks[1].status == TASK_PENDING

    def test_paused_not_running(self, isolate_data_root, demo_repo):
        """Paused status != running (no false implication of background work)."""
        result = _run_success_job(demo_repo, max_tasks=1)
        assert result.status != "running"

    def test_paused_next_command_copyable(self, isolate_data_root, demo_repo):
        """Paused job suggests job-run as next command."""
        result = _run_success_job(demo_repo, max_tasks=1)
        cmd = _suggest_next_command(result)
        assert "job-run" in cmd
        assert result.job_id in cmd

    def test_paused_report_shows_pending(self, isolate_data_root, demo_repo):
        """Report for paused job shows pending task count."""
        result = _run_success_job(demo_repo, max_tasks=1)
        report = export_job_report(result)
        assert report["pending_tasks"] == 1
        assert report["status"] == "paused"

    def test_continuation_after_pause(self, isolate_data_root, demo_repo):
        """Re-running job-run after max-tasks pause continues pending tasks."""
        result = _run_success_job(demo_repo, max_tasks=1)
        assert result.status == JOB_PAUSED
        assert result.tasks[1].status == TASK_PENDING

        # Continue the remaining tasks
        result2 = run_job(
            result.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )
        assert result2.status == JOB_COMPLETED
        assert result2.tasks[0].status == TASK_APPLIED
        assert result2.tasks[1].status == TASK_APPLIED

    def test_full_run_gives_completed(self, isolate_data_root, demo_repo):
        """Full run (no --max-tasks) still gives completed."""
        result = _run_success_job(demo_repo)
        assert result.status == JOB_COMPLETED


# ---------------------------------------------------------------------------
# Step 4854 — Job report repair metadata
# ---------------------------------------------------------------------------


class TestReportRepairMetadata:
    def test_report_has_repair_rounds_allowed(self, isolate_data_root, demo_repo):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=3,
            repair_rounds_source="cli",
        )
        report = export_job_report(result)
        assert report["repair_rounds_allowed"] == 3

    def test_report_has_repair_rounds_source(self, isolate_data_root, demo_repo):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=2,
            repair_rounds_source="default",
        )
        report = export_job_report(result)
        assert report["repair_rounds_source"] == "default"

    def test_per_task_repair_used(self, isolate_data_root, demo_repo):
        result = _run_success_job(demo_repo)
        report = export_job_report(result)
        for t in report["tasks"]:
            assert "repair_rounds_used" in t
            assert "repair_rounds_allowed" in t

    def test_text_report_repair_info(self, isolate_data_root, demo_repo):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
            repair_rounds_source="cli",
        )
        text = format_job_report_text(result)
        assert "0 rounds" in text
        assert "source: cli" in text

    def test_context_strategy_present(self, isolate_data_root, demo_repo):
        result = _run_success_job(demo_repo)
        report = export_job_report(result)
        assert report["context_strategy"]["strategy"] == "task_bounded_sequential_job"


# ---------------------------------------------------------------------------
# Step 4857-4858 — Deterministic completion gate + corrupted-result tests
# ---------------------------------------------------------------------------


_SENTINEL_NO_REVIEWER = object()


def _make_fake_result(
    *,
    final_status="staged_review_passed",
    test_passed=True,
    reviewer_verdict="pass",
    reviewer_findings=None,
    reviewer_output=_SENTINEL_NO_REVIEWER,
    target_mutated=False,
    staged_files=None,
    staging_path="/tmp/fake_staging",
):
    """Build a fake PingPongResult-like object for gate testing.

    Pass reviewer_output=None to simulate missing reviewer evidence.
    Default builds a ReviewerOutput from reviewer_verdict/reviewer_findings.
    """
    if reviewer_output is _SENTINEL_NO_REVIEWER:
        from packages.orchestration.pingpong_provider import ReviewerOutput, ReviewFinding
        ro = ReviewerOutput(verdict=reviewer_verdict)
        if reviewer_findings:
            ro.findings = [
                ReviewFinding(id=f"F{i}", severity="high", summary=f)
                for i, f in enumerate(reviewer_findings)
            ]
    else:
        ro = reviewer_output

    from packages.orchestration.pingpong_loop import PingPongRound

    round_ = PingPongRound(
        round_number=1,
        test_passed=test_passed,
        reviewer_output=ro,
    )

    effective_files = staged_files if staged_files is not None else ["README.md"]
    return types.SimpleNamespace(
        run_id="fake_run",
        final_status=final_status,
        target_mutated=target_mutated,
        rounds=[round_],
        staged_files=effective_files,
        staging_path=staging_path,
        safe_diff_files=effective_files,
        repair_rounds_used=0,
        repair_rounds_allowed=0,
    )


class TestCompletionGate:
    def test_clean_result_passes(self, tmp_path):
        staging = tmp_path / "staging"
        staging.mkdir()
        (staging / "README.md").write_text("ok")
        result = _make_fake_result(staging_path=str(staging))
        ok, reasons = validate_job_task_result(result)
        assert ok is True
        assert reasons == []

    def test_failed_test_blocks(self):
        result = _make_fake_result(test_passed=False)
        ok, reasons = validate_job_task_result(result)
        assert ok is False
        assert any("test_passed=False" in r for r in reasons)

    def test_reviewer_fail_blocks(self):
        result = _make_fake_result(reviewer_verdict="fail")
        ok, reasons = validate_job_task_result(result)
        assert ok is False
        assert any("reviewer_verdict=fail" in r for r in reasons)

    def test_reviewer_pass_with_findings_blocks(self):
        result = _make_fake_result(
            reviewer_verdict="pass",
            reviewer_findings=["bug in line 5"],
        )
        ok, reasons = validate_job_task_result(result)
        assert ok is False
        assert any("findings" in r for r in reasons)

    def test_target_mutated_blocks(self):
        result = _make_fake_result(target_mutated=True)
        ok, reasons = validate_job_task_result(result)
        assert ok is False
        assert any("target_mutated" in r for r in reasons)

    def test_bad_final_status_blocks(self):
        result = _make_fake_result(final_status="max_rounds_reached")
        ok, reasons = validate_job_task_result(result)
        assert ok is False
        assert any("final_status" in r for r in reasons)

    def test_staging_path_missing_blocks(self):
        result = _make_fake_result(staging_path="/nonexistent/path")
        ok, reasons = validate_job_task_result(result)
        assert ok is False
        assert any("staging_path_missing" in r for r in reasons)

    def test_builder_no_changes_with_reviewer_pass(self):
        result = _make_fake_result(
            final_status="staged_review_passed",
            staged_files=[],
            reviewer_verdict="pass",
        )
        ok, reasons = validate_job_task_result(result)
        assert ok is True
        assert reasons == []

    def test_builder_no_changes_without_reviewer_blocks(self):
        result = _make_fake_result(
            final_status="builder_no_changes",
            staged_files=[],
            reviewer_output=None,
        )
        ok, reasons = validate_job_task_result(result)
        assert ok is False

    def test_builder_no_changes_without_tests_blocks(self):
        result = _make_fake_result(
            final_status="staged_review_passed",
            staged_files=[],
            test_passed=False,
            reviewer_verdict="pass",
        )
        ok, reasons = validate_job_task_result(result)
        assert ok is False

    def test_later_tasks_run_after_no_change(self, isolate_data_root, demo_repo):
        """A no-change T001 that passes must not skip T002."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )
        task_statuses = {
            t.task_id: t.status for t in result.tasks
        }
        assert task_statuses.get("T001") not in (None, "skipped")
        assert task_statuses.get("T002") not in (None, "skipped")


class TestCorruptedResultJobBlock:
    """Tests that internally inconsistent results block the job."""

    def _run_with_corrupt_result(self, demo_repo, monkeypatch, **overrides):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))

        import packages.orchestration.pingpong_loop as pp_mod
        real_run = pp_mod.run_pingpong

        def corrupt_run(*args, **kwargs):
            result = real_run(*args, **kwargs)
            for k, v in overrides.items():
                if k == "test_passed" and result.rounds:
                    result.rounds[-1].test_passed = v
                elif k == "reviewer_output" and result.rounds:
                    result.rounds[-1].reviewer_output = v
                elif k == "reviewer_verdict" and result.rounds:
                    if result.rounds[-1].reviewer_output:
                        result.rounds[-1].reviewer_output.verdict = v
                elif k == "reviewer_findings" and result.rounds:
                    if result.rounds[-1].reviewer_output:
                        from packages.orchestration.pingpong_provider import ReviewFinding
                        result.rounds[-1].reviewer_output.findings = [
                            ReviewFinding(id="F1", severity="high", summary=f)
                            for f in v
                        ]
                elif k == "target_mutated":
                    result.target_mutated = v
                else:
                    setattr(result, k, v)
            return result

        monkeypatch.setattr(pp_mod, "run_pingpong", corrupt_run)

        return run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )

    def test_test_failed_but_final_pass_blocks(self, isolate_data_root, demo_repo, monkeypatch):
        result = self._run_with_corrupt_result(demo_repo, monkeypatch, test_passed=False)
        assert result.status == JOB_BLOCKED
        assert any("test_passed" in (t.error or "") for t in result.tasks)

    def test_reviewer_fail_but_final_pass_blocks(self, isolate_data_root, demo_repo, monkeypatch):
        result = self._run_with_corrupt_result(demo_repo, monkeypatch, reviewer_verdict="fail")
        assert result.status == JOB_BLOCKED
        assert any("reviewer_verdict" in (t.error or "") for t in result.tasks)

    def test_reviewer_pass_with_findings_blocks(self, isolate_data_root, demo_repo, monkeypatch):
        result = self._run_with_corrupt_result(
            demo_repo, monkeypatch,
            reviewer_findings=["unexpected bug"],
        )
        assert result.status == JOB_BLOCKED
        assert any("findings" in (t.error or "") for t in result.tasks)

    def test_target_mutated_but_final_pass_blocks(self, isolate_data_root, demo_repo, monkeypatch):
        result = self._run_with_corrupt_result(demo_repo, monkeypatch, target_mutated=True)
        assert result.status == JOB_BLOCKED
        assert any("target_mutated" in (t.error or "") for t in result.tasks)

    def test_blocked_result_not_applied(self, isolate_data_root, demo_repo, monkeypatch):
        result = self._run_with_corrupt_result(demo_repo, monkeypatch, test_passed=False)
        for t in result.tasks:
            assert t.status != TASK_APPLIED

    def test_task2_does_not_start_after_block(self, isolate_data_root, demo_repo, monkeypatch):
        result = self._run_with_corrupt_result(demo_repo, monkeypatch, test_passed=False)
        assert result.tasks[1].status in (TASK_SKIPPED, TASK_PENDING)


# ---------------------------------------------------------------------------
# Steps 4859-4864 — Execution config persistence and continuation
# ---------------------------------------------------------------------------


class TestExecutionConfig:
    def test_config_persisted_on_run(self, isolate_data_root, demo_repo):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            builder_name="claude-cli",
            reviewer_name="claude-cli",
            repair_rounds=1,
            repair_rounds_source="cli",
            test_command="true",
        )
        assert result.execution_config is not None
        assert result.execution_config.builder == "claude-cli"
        assert result.execution_config.reviewer == "claude-cli"
        assert result.execution_config.repair_rounds_allowed == 1
        assert result.execution_config.repair_rounds_source == "cli"
        assert result.execution_config.test_command == "true"

    def test_config_persisted_in_json(self, isolate_data_root, demo_repo):
        result = _run_success_job(demo_repo)
        loaded = load_job_plan(result.job_id)
        assert loaded is not None
        assert loaded.execution_config is not None
        assert loaded.execution_config.builder == "fake"

    def test_config_in_report(self, isolate_data_root, demo_repo):
        result = _run_success_job(demo_repo)
        report = export_job_report(result)
        assert "execution_config" in report
        ec = report["execution_config"]
        assert ec["builder"] == "fake"
        assert ec["context_strategy"] == "task_bounded_sequential_job"


class TestContinuationConfig:
    def test_pause_preserves_config(self, isolate_data_root, demo_repo):
        """Config is persisted after paused run."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            builder_name="claude-cli",
            reviewer_name="claude-cli",
            repair_rounds=1,
            repair_rounds_source="cli",
            test_command="true",
            max_tasks=1,
        )
        assert result.status == JOB_PAUSED
        loaded = load_job_plan(result.job_id)
        assert loaded.execution_config.builder == "claude-cli"
        assert loaded.execution_config.test_command == "true"
        assert loaded.execution_config.repair_rounds_allowed == 1

    def test_continuation_restores_config(self, isolate_data_root, demo_repo):
        """Continuation without flags restores persisted config."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            builder_name="claude-cli",
            reviewer_name="claude-cli",
            repair_rounds=1,
            repair_rounds_source="cli",
            test_command="true",
            max_tasks=1,
        )
        # Continue with defaults (simulating omitted CLI flags)
        result2 = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
        )
        assert result2.status == JOB_COMPLETED
        # Config should be restored, not fallen back to defaults
        assert result2.execution_config.builder == "claude-cli"
        assert result2.execution_config.reviewer == "claude-cli"
        assert result2.execution_config.test_command == "true"
        assert result2.execution_config.repair_rounds_allowed == 1

    def test_task2_uses_same_config(self, isolate_data_root, demo_repo):
        """Task 2 on continuation uses same repair rounds as task 1."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=1,
            repair_rounds_source="cli",
            max_tasks=1,
        )
        result2 = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
        )
        assert result2.tasks[1].repair_rounds_allowed == 1

    def test_continuation_report_shows_config(self, isolate_data_root, demo_repo):
        """Report for paused job shows persisted config."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            builder_name="claude-cli",
            test_command="true",
            max_tasks=1,
        )
        text = format_job_report_text(result)
        assert "claude-cli" in text
        assert "persisted" in text.lower()

    def test_no_silent_fallback(self, isolate_data_root, demo_repo):
        """Continuation without flags does NOT silently change config."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            builder_name="claude-cli",
            reviewer_name="claude-cli",
            repair_rounds=0,
            repair_rounds_source="cli",
            max_tasks=1,
        )
        result2 = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
        )
        # Must NOT fall back to default repair_rounds=2
        assert result2.repair_rounds_allowed == 0
        assert result2.repair_rounds_source == "persisted"


class TestConfigOverride:
    def test_explicit_override_takes_effect(self, isolate_data_root, demo_repo):
        """Explicit CLI flag overrides persisted config."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=1,
            repair_rounds_source="cli",
            max_tasks=1,
        )
        # Override repair_rounds on continuation
        result2 = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
            repair_rounds_source="cli",
        )
        assert result2.repair_rounds_allowed == 0
        assert result2.execution_config.repair_rounds_allowed == 0

    def test_override_updates_persisted_config(self, isolate_data_root, demo_repo):
        """Override updates the persisted config for next run."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=1,
            repair_rounds_source="cli",
            max_tasks=1,
        )
        run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
            repair_rounds_source="cli",
        )
        loaded = load_job_plan(job.job_id)
        assert loaded.execution_config.repair_rounds_allowed == 0

    def test_report_shows_active_config(self, isolate_data_root, demo_repo):
        """Report after override shows active config, not original."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=1,
            repair_rounds_source="cli",
            max_tasks=1,
        )
        result2 = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
            repair_rounds_source="cli",
        )
        report = export_job_report(result2)
        assert report["repair_rounds_allowed"] == 0
        assert report["execution_config"]["repair_rounds_allowed"] == 0


# ---------------------------------------------------------------------------
# Step 4867 — CLI smoke / command-path pause-continue proof
# ---------------------------------------------------------------------------


class TestCliPauseContinueSmoke:
    def test_full_pause_continue_cycle(self, isolate_data_root, demo_repo, capsys):
        """Handler-level proof of pause → continue with persisted config."""
        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        # Step 1: Plan
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))

        # Step 2: Run with --max-tasks 1, --repair-rounds 1
        args1 = _make_args(
            job_id=job.job_id,
            builder="fake",
            reviewer="fake",
            repair_rounds=1,
            max_tasks="1",
        )
        COMMAND_HANDLERS["do.job-run"](args1)
        out1 = json.loads(capsys.readouterr().out)

        assert out1["status"] == "paused"
        assert out1["pending_tasks"] == 1
        assert out1["repair_rounds_allowed"] == 1
        assert out1["repair_rounds_source"] == "cli"
        assert out1["execution_config"]["repair_rounds_allowed"] == 1

        # Step 3: Report
        args_report = types.SimpleNamespace(job_id=job.job_id, json=True)
        COMMAND_HANDLERS["do.job-report"](args_report)
        report1 = json.loads(capsys.readouterr().out)
        assert report1["status"] == "paused"
        assert report1["execution_config"]["repair_rounds_allowed"] == 1

        # Step 4: Continue without restating flags
        args2 = _make_args(job_id=job.job_id)
        COMMAND_HANDLERS["do.job-run"](args2)
        out2 = json.loads(capsys.readouterr().out)

        assert out2["status"] == "completed"
        # Config must be preserved from first run, not fallen back to default 2
        assert out2["repair_rounds_allowed"] == 1
        assert out2["execution_config"]["repair_rounds_allowed"] == 1

        # Step 5: Final report
        COMMAND_HANDLERS["do.job-report"](args_report)
        report2 = json.loads(capsys.readouterr().out)
        assert report2["status"] == "completed"

        # Both tasks should be applied
        applied = [t for t in report2["tasks"] if t["status"] == TASK_APPLIED]
        assert len(applied) == 2

    def test_target_repo_unchanged_after_smoke(self, isolate_data_root, demo_repo, capsys):
        """Target repo is not mutated during pause/continue cycle."""
        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        readme_before = (demo_repo / "README.md").read_text()
        main_before = (demo_repo / "src" / "main.py").read_text()

        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        args1 = _make_args(job_id=job.job_id, max_tasks="1")
        COMMAND_HANDLERS["do.job-run"](args1)
        capsys.readouterr()

        args2 = _make_args(job_id=job.job_id)
        COMMAND_HANDLERS["do.job-run"](args2)
        capsys.readouterr()

        assert (demo_repo / "README.md").read_text() == readme_before
        assert (demo_repo / "src" / "main.py").read_text() == main_before


# ---------------------------------------------------------------------------
# Step 4870 — max_rounds continuation (the bug fix)
# ---------------------------------------------------------------------------


class TestMaxRoundsContinuation:
    def test_max_rounds_persisted_on_pause(self, isolate_data_root, demo_repo):
        """max_rounds=7 persists when job is paused with --max-tasks 1."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            builder_name="fake",
            reviewer_name="fake",
            max_rounds=7,
            max_tasks=1,
        )
        assert result.status == JOB_PAUSED
        assert result.execution_config.max_rounds == 7
        assert result.execution_config.max_rounds_source == "cli"

    def test_max_rounds_restored_on_continuation(self, isolate_data_root, demo_repo):
        """Continuation with omitted --max-rounds restores persisted 7."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            max_rounds=7,
            max_tasks=1,
        )
        result2 = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
        )
        assert result2.status == JOB_COMPLETED
        assert result2.execution_config.max_rounds == 7
        assert result2.execution_config.max_rounds_source == "persisted"

    def test_max_rounds_explicit_override(self, isolate_data_root, demo_repo):
        """Explicit --max-rounds 3 overrides persisted 7."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            max_rounds=7,
            max_tasks=1,
        )
        result2 = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            max_rounds=3,
        )
        assert result2.execution_config.max_rounds == 3
        assert result2.execution_config.max_rounds_source == "cli"

    def test_cli_handler_max_rounds_continuation(
        self, isolate_data_root, demo_repo, capsys
    ):
        """Handler-level: max_rounds persists through pause/continue."""
        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        args1 = _make_args(
            job_id=job.job_id, builder="fake", reviewer="fake",
            max_rounds="7", max_tasks="1",
        )
        COMMAND_HANDLERS["do.job-run"](args1)
        out1 = json.loads(capsys.readouterr().out)
        assert out1["status"] == "paused"
        assert out1["execution_config"]["max_rounds"] == 7

        args2 = _make_args(job_id=job.job_id)
        COMMAND_HANDLERS["do.job-run"](args2)
        out2 = json.loads(capsys.readouterr().out)
        assert out2["status"] == "completed"
        assert out2["execution_config"]["max_rounds"] == 7
        assert out2["execution_config"]["max_rounds_source"] == "persisted"


# ---------------------------------------------------------------------------
# Step 4871 — Explicit provider override back to fake (the bug fix)
# ---------------------------------------------------------------------------


class TestProviderOverrideToFake:
    def test_provider_persisted_on_pause(self, isolate_data_root, demo_repo):
        """builder=claude-cli persists when job is paused."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            builder_name="claude-cli",
            reviewer_name="claude-cli",
            max_tasks=1,
        )
        assert result.status == JOB_PAUSED
        assert result.execution_config.builder == "claude-cli"
        assert result.execution_config.reviewer == "claude-cli"

    def test_provider_restored_on_continuation(self, isolate_data_root, demo_repo):
        """Omitted --builder/--reviewer restores persisted claude-cli."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            builder_name="claude-cli",
            reviewer_name="claude-cli",
            max_tasks=1,
        )
        result2 = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
        )
        assert result2.execution_config.builder == "claude-cli"
        assert result2.execution_config.builder_source == "persisted"
        assert result2.execution_config.reviewer == "claude-cli"
        assert result2.execution_config.reviewer_source == "persisted"

    def test_explicit_fake_overrides_persisted_provider(
        self, isolate_data_root, demo_repo
    ):
        """Explicit --builder fake overrides persisted claude-cli."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            builder_name="claude-cli",
            reviewer_name="claude-cli",
            max_tasks=1,
        )
        result2 = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            builder_name="fake",
            reviewer_name="fake",
        )
        assert result2.execution_config.builder == "fake"
        assert result2.execution_config.builder_source == "cli"
        assert result2.execution_config.reviewer == "fake"
        assert result2.execution_config.reviewer_source == "cli"

    def test_cli_handler_provider_override(
        self, isolate_data_root, demo_repo, capsys
    ):
        """Handler-level: explicit --builder fake overrides persisted."""
        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        args1 = _make_args(
            job_id=job.job_id,
            builder="claude-cli",
            reviewer="claude-cli",
            max_tasks="1",
        )
        COMMAND_HANDLERS["do.job-run"](args1)
        out1 = json.loads(capsys.readouterr().out)
        assert out1["execution_config"]["builder"] == "claude-cli"

        args2 = _make_args(
            job_id=job.job_id,
            builder="fake",
            reviewer="fake",
        )
        COMMAND_HANDLERS["do.job-run"](args2)
        out2 = json.loads(capsys.readouterr().out)
        assert out2["execution_config"]["builder"] == "fake"
        assert out2["execution_config"]["builder_source"] == "cli"
        assert out2["execution_config"]["reviewer"] == "fake"
        assert out2["execution_config"]["reviewer_source"] == "cli"


# ---------------------------------------------------------------------------
# Step 4872-4873 — Test command and write mode continuation
# ---------------------------------------------------------------------------


class TestTestCommandContinuation:
    def test_test_command_persisted(self, isolate_data_root, demo_repo):
        """test_command persisted on pause."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            test_command="true",
            max_tasks=1,
        )
        assert result.execution_config.test_command == "true"
        assert result.execution_config.test_command_source == "cli"

    def test_test_command_restored(self, isolate_data_root, demo_repo):
        """Omitted --test-command restores persisted value."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            test_command="true",
            max_tasks=1,
        )
        result2 = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
        )
        assert result2.execution_config.test_command == "true"
        assert result2.execution_config.test_command_source == "persisted"

    def test_test_command_override(self, isolate_data_root, demo_repo):
        """Explicit --test-command overrides persisted."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            test_command="true",
            max_tasks=1,
        )
        result2 = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            test_command="echo ok",
        )
        assert result2.execution_config.test_command == "echo ok"
        assert result2.execution_config.test_command_source == "cli"


class TestWriteModeContinuation:
    def test_write_mode_persisted(self, isolate_data_root, demo_repo):
        """write_mode persisted on pause."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            claude_cli_write_mode="allowed-tools",
            max_tasks=1,
        )
        assert result.execution_config.claude_cli_write_mode == "allowed-tools"
        assert result.execution_config.claude_cli_write_mode_source == "cli"

    def test_write_mode_restored(self, isolate_data_root, demo_repo):
        """Omitted --claude-cli-write-mode restores persisted."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            claude_cli_write_mode="allowed-tools",
            max_tasks=1,
        )
        result2 = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
        )
        assert result2.execution_config.claude_cli_write_mode == "allowed-tools"
        assert result2.execution_config.claude_cli_write_mode_source == "persisted"

    def test_write_mode_override(self, isolate_data_root, demo_repo):
        """Explicit --claude-cli-write-mode overrides persisted."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            claude_cli_write_mode="allowed-tools",
            max_tasks=1,
        )
        result2 = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            claude_cli_write_mode="none",
        )
        assert result2.execution_config.claude_cli_write_mode == "none"
        assert result2.execution_config.claude_cli_write_mode_source == "cli"


# ---------------------------------------------------------------------------
# Step 4874 — Execution config source/audit fields
# ---------------------------------------------------------------------------


class TestConfigSourceAudit:
    def test_first_run_sources_all_cli(self, isolate_data_root, demo_repo):
        """First run with explicit args: all sources are 'cli'."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            builder_name="fake",
            reviewer_name="fake",
            max_rounds=5,
            repair_rounds=1,
            repair_rounds_source="cli",
            test_command="true",
            claude_cli_write_mode="none",
        )
        ec = result.execution_config
        assert ec.builder_source == "cli"
        assert ec.reviewer_source == "cli"
        assert ec.max_rounds_source == "cli"
        assert ec.repair_rounds_source == "cli"
        assert ec.test_command_source == "cli"
        assert ec.claude_cli_write_mode_source == "cli"

    def test_first_run_sources_all_default(self, isolate_data_root, demo_repo):
        """First run with no args: all sources are 'default'."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
        )
        ec = result.execution_config
        assert ec.builder_source == "default"
        assert ec.reviewer_source == "default"
        assert ec.max_rounds_source == "default"
        assert ec.repair_rounds_source == "default"
        assert ec.test_command_source == "default"
        assert ec.claude_cli_write_mode_source == "default"

    def test_continuation_sources_persisted(self, isolate_data_root, demo_repo):
        """Continuation with omitted args: sources are 'persisted'."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            builder_name="claude-cli",
            reviewer_name="claude-cli",
            max_rounds=7,
            repair_rounds=1,
            repair_rounds_source="cli",
            test_command="true",
            claude_cli_write_mode="allowed-tools",
            max_tasks=1,
        )
        result2 = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
        )
        ec = result2.execution_config
        assert ec.builder_source == "persisted"
        assert ec.reviewer_source == "persisted"
        assert ec.max_rounds_source == "persisted"
        assert ec.repair_rounds_source == "persisted"
        assert ec.test_command_source == "persisted"
        assert ec.claude_cli_write_mode_source == "persisted"

    def test_source_in_json_report(self, isolate_data_root, demo_repo):
        """JSON report includes source fields."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            builder_name="fake",
            max_rounds=5,
        )
        report = export_job_report(result)
        ec_data = report["execution_config"]
        assert ec_data["builder_source"] == "cli"
        assert ec_data["max_rounds_source"] == "cli"
        assert "test_command_present" in ec_data
        assert "test_command_source" in ec_data

    def test_source_in_text_report(self, isolate_data_root, demo_repo):
        """Text report shows source info."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            builder_name="fake",
            max_rounds=5,
        )
        text = format_job_report_text(result)
        assert "(source: cli)" in text
        assert "Max rounds: 5" in text


# ---------------------------------------------------------------------------
# Step 4875 — Real command-path pause/continue full config test
# ---------------------------------------------------------------------------


class TestCommandPathFullConfigContinuation:
    def test_full_config_preserved_through_pause(
        self, isolate_data_root, demo_repo, capsys
    ):
        """All config fields survive pause/continue through handler path."""
        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))

        args1 = _make_args(
            job_id=job.job_id,
            builder="fake",
            reviewer="fake",
            max_rounds="7",
            repair_rounds=1,
            test_command="true",
            claude_cli_write_mode="none",
            max_tasks="1",
        )
        COMMAND_HANDLERS["do.job-run"](args1)
        out1 = json.loads(capsys.readouterr().out)

        assert out1["status"] == "paused"
        ec1 = out1["execution_config"]
        assert ec1["max_rounds"] == 7
        assert ec1["repair_rounds_allowed"] == 1
        assert ec1["builder"] == "fake"
        assert ec1["test_command_present"] is True

        # Continue without restating any flags
        args2 = _make_args(job_id=job.job_id)
        COMMAND_HANDLERS["do.job-run"](args2)
        out2 = json.loads(capsys.readouterr().out)

        assert out2["status"] == "completed"
        ec2 = out2["execution_config"]
        assert ec2["max_rounds"] == 7
        assert ec2["max_rounds_source"] == "persisted"
        assert ec2["repair_rounds_allowed"] == 1
        assert ec2["repair_rounds_source"] == "persisted"
        assert ec2["builder"] == "fake"
        assert ec2["builder_source"] == "persisted"
        assert ec2["test_command_present"] is True
        assert ec2["test_command_source"] == "persisted"

    def test_no_config_drift_in_report(
        self, isolate_data_root, demo_repo, capsys
    ):
        """Report after continuation shows no drift from original config."""
        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))

        args1 = _make_args(
            job_id=job.job_id, builder="fake", reviewer="fake",
            max_rounds="7", max_tasks="1",
        )
        COMMAND_HANDLERS["do.job-run"](args1)
        capsys.readouterr()

        args2 = _make_args(job_id=job.job_id)
        COMMAND_HANDLERS["do.job-run"](args2)
        capsys.readouterr()

        args_report = types.SimpleNamespace(job_id=job.job_id, json=True)
        COMMAND_HANDLERS["do.job-report"](args_report)
        report = json.loads(capsys.readouterr().out)

        assert report["execution_config"]["max_rounds"] == 7
        applied = [t for t in report["tasks"] if t["status"] == TASK_APPLIED]
        assert len(applied) == 2


# ---------------------------------------------------------------------------
# Step 4876 — Explicit override tests through command path
# ---------------------------------------------------------------------------


class TestCommandPathExplicitOverrides:
    def test_provider_override_to_fake(
        self, isolate_data_root, demo_repo, capsys
    ):
        """Persisted claude-cli overridden by explicit --builder fake."""
        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        args1 = _make_args(
            job_id=job.job_id,
            builder="claude-cli",
            reviewer="claude-cli",
            max_tasks="1",
        )
        COMMAND_HANDLERS["do.job-run"](args1)
        out1 = json.loads(capsys.readouterr().out)
        assert out1["execution_config"]["builder"] == "claude-cli"

        args2 = _make_args(
            job_id=job.job_id,
            builder="fake",
            reviewer="fake",
        )
        COMMAND_HANDLERS["do.job-run"](args2)
        out2 = json.loads(capsys.readouterr().out)
        assert out2["execution_config"]["builder"] == "fake"
        assert out2["execution_config"]["builder_source"] == "cli"
        assert out2["execution_config"]["reviewer"] == "fake"
        assert out2["execution_config"]["reviewer_source"] == "cli"

    def test_max_rounds_override(self, isolate_data_root, demo_repo, capsys):
        """Persisted max_rounds=7 overridden by explicit --max-rounds 3."""
        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        args1 = _make_args(
            job_id=job.job_id, max_rounds="7", max_tasks="1",
        )
        COMMAND_HANDLERS["do.job-run"](args1)
        capsys.readouterr()

        args2 = _make_args(job_id=job.job_id, max_rounds="3")
        COMMAND_HANDLERS["do.job-run"](args2)
        out2 = json.loads(capsys.readouterr().out)
        assert out2["execution_config"]["max_rounds"] == 3
        assert out2["execution_config"]["max_rounds_source"] == "cli"

    def test_repair_rounds_override_to_zero(
        self, isolate_data_root, demo_repo, capsys
    ):
        """Persisted repair_rounds=1 overridden by explicit --repair-rounds 0."""
        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        args1 = _make_args(
            job_id=job.job_id, repair_rounds=1, max_tasks="1",
        )
        COMMAND_HANDLERS["do.job-run"](args1)
        capsys.readouterr()

        args2 = _make_args(job_id=job.job_id, repair_rounds=0)
        COMMAND_HANDLERS["do.job-run"](args2)
        out2 = json.loads(capsys.readouterr().out)
        assert out2["execution_config"]["repair_rounds_allowed"] == 0
        assert out2["execution_config"]["repair_rounds_source"] == "cli"

    def test_test_command_override(self, isolate_data_root, demo_repo, capsys):
        """Persisted test_command overridden by explicit --test-command."""
        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        args1 = _make_args(
            job_id=job.job_id, test_command="true", max_tasks="1",
        )
        COMMAND_HANDLERS["do.job-run"](args1)
        capsys.readouterr()

        args2 = _make_args(job_id=job.job_id, test_command="echo ok")
        COMMAND_HANDLERS["do.job-run"](args2)
        out2 = json.loads(capsys.readouterr().out)
        assert out2["execution_config"]["test_command_source"] == "cli"

    def test_report_shows_override(self, isolate_data_root, demo_repo, capsys):
        """Report after override shows new active config, not original."""
        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        args1 = _make_args(
            job_id=job.job_id, max_rounds="7", max_tasks="1",
        )
        COMMAND_HANDLERS["do.job-run"](args1)
        capsys.readouterr()

        args2 = _make_args(job_id=job.job_id, max_rounds="3")
        COMMAND_HANDLERS["do.job-run"](args2)
        capsys.readouterr()

        args_report = types.SimpleNamespace(job_id=job.job_id, json=True)
        COMMAND_HANDLERS["do.job-report"](args_report)
        report = json.loads(capsys.readouterr().out)
        assert report["execution_config"]["max_rounds"] == 3
        assert report["execution_config"]["max_rounds_source"] == "cli"


# ---------------------------------------------------------------------------
# Step 4879-4880 — Missing reviewer output gate tests
# ---------------------------------------------------------------------------


class TestMissingReviewerOutputGate:
    """Completion gate blocks when reviewer_output is None."""

    def test_missing_reviewer_with_test_passed_blocks(self):
        """staged_review_passed + test_passed=True + reviewer_output=None blocks."""
        result = _make_fake_result(
            test_passed=True, reviewer_output=None,
        )
        ok, reasons = validate_job_task_result(result)
        assert ok is False
        assert any("missing_reviewer_output" in r for r in reasons)

    def test_missing_reviewer_with_test_none_blocks(self):
        """staged_review_passed + test_passed=None + reviewer_output=None blocks."""
        result = _make_fake_result(
            test_passed=None, reviewer_output=None,
        )
        ok, reasons = validate_job_task_result(result)
        assert ok is False
        assert any("missing_reviewer_output" in r for r in reasons)

    def test_clean_reviewer_pass_with_empty_findings_passes(self, tmp_path):
        """staged_review_passed + reviewer pass + findings=[] passes."""
        staging = tmp_path / "staging"
        staging.mkdir()
        (staging / "README.md").write_text("ok")
        result = _make_fake_result(
            reviewer_verdict="pass",
            reviewer_findings=None,
            staging_path=str(staging),
        )
        ok, reasons = validate_job_task_result(result)
        assert ok is True
        assert reasons == []

    def test_reviewer_pass_with_findings_still_blocks(self):
        """staged_review_passed + reviewer pass + findings=[...] blocks."""
        result = _make_fake_result(
            reviewer_verdict="pass",
            reviewer_findings=["leftover issue"],
        )
        ok, reasons = validate_job_task_result(result)
        assert ok is False
        assert any("findings" in r for r in reasons)

    def test_reviewer_fail_still_blocks(self):
        """staged_review_passed + reviewer fail blocks."""
        result = _make_fake_result(reviewer_verdict="fail")
        ok, reasons = validate_job_task_result(result)
        assert ok is False
        assert any("reviewer_verdict=fail" in r for r in reasons)

    def test_target_mutated_still_blocks(self):
        """staged_review_passed + target_mutated=True still blocks."""
        result = _make_fake_result(target_mutated=True)
        ok, reasons = validate_job_task_result(result)
        assert ok is False
        assert any("target_mutated" in r for r in reasons)


# ---------------------------------------------------------------------------
# Step 4881 — E2E regression: missing reviewer_output blocks run_job
# ---------------------------------------------------------------------------


class TestMissingReviewerE2E:
    """run_job blocks when run_pingpong returns reviewer_output=None."""

    def test_missing_reviewer_blocks_job(self, isolate_data_root, demo_repo, monkeypatch):
        """Job blocks when corrupted result has reviewer_output=None."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))

        import packages.orchestration.pingpong_loop as pp_mod
        real_run = pp_mod.run_pingpong

        def no_reviewer_run(*args, **kwargs):
            result = real_run(*args, **kwargs)
            if result.rounds:
                result.rounds[-1].reviewer_output = None
            return result

        monkeypatch.setattr(pp_mod, "run_pingpong", no_reviewer_run)

        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )
        assert result.status == JOB_BLOCKED
        assert any("missing_reviewer_output" in (t.error or "") for t in result.tasks)

    def test_missing_reviewer_no_workspace_apply(self, isolate_data_root, demo_repo, monkeypatch):
        """Staged files not applied when reviewer evidence is missing."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))

        import packages.orchestration.pingpong_loop as pp_mod
        real_run = pp_mod.run_pingpong

        def no_reviewer_run(*args, **kwargs):
            result = real_run(*args, **kwargs)
            if result.rounds:
                result.rounds[-1].reviewer_output = None
            return result

        monkeypatch.setattr(pp_mod, "run_pingpong", no_reviewer_run)

        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )
        for t in result.tasks:
            assert t.status != TASK_APPLIED

    def test_task2_skipped_after_missing_reviewer(self, isolate_data_root, demo_repo, monkeypatch):
        """Task 2 does not start after task 1 blocked for missing reviewer."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))

        import packages.orchestration.pingpong_loop as pp_mod
        real_run = pp_mod.run_pingpong

        def no_reviewer_run(*args, **kwargs):
            result = real_run(*args, **kwargs)
            if result.rounds:
                result.rounds[-1].reviewer_output = None
            return result

        monkeypatch.setattr(pp_mod, "run_pingpong", no_reviewer_run)

        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )
        assert result.tasks[1].status in (TASK_SKIPPED, TASK_PENDING)


# ---------------------------------------------------------------------------
# Step 4882 — No-test-command valid behavior
# ---------------------------------------------------------------------------


class TestNoTestCommandValid:
    """test_passed=None is valid when no test command was configured."""

    def test_no_test_command_with_reviewer_pass(self, tmp_path):
        """No test command (test_passed=None) + clean reviewer pass = gate OK."""
        staging = tmp_path / "staging"
        staging.mkdir()
        (staging / "README.md").write_text("ok")
        result = _make_fake_result(
            test_passed=None,
            reviewer_verdict="pass",
            staging_path=str(staging),
        )
        ok, reasons = validate_job_task_result(result)
        assert ok is True
        assert reasons == []

    def test_no_test_command_without_reviewer_blocks(self):
        """No test command (test_passed=None) + missing reviewer = blocked."""
        result = _make_fake_result(
            test_passed=None,
            reviewer_output=None,
        )
        ok, reasons = validate_job_task_result(result)
        assert ok is False
        assert any("missing_reviewer_output" in r for r in reasons)


# ---------------------------------------------------------------------------
# Step 4883 — Report exposes missing-reviewer block reason
# ---------------------------------------------------------------------------


class TestMissingReviewerReport:
    """Report correctly shows missing-reviewer block reason."""

    def test_json_report_shows_block_reason(self, isolate_data_root, demo_repo, monkeypatch):
        """JSON report includes missing_reviewer_output in task error."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))

        import packages.orchestration.pingpong_loop as pp_mod
        real_run = pp_mod.run_pingpong

        def no_reviewer_run(*args, **kwargs):
            result = real_run(*args, **kwargs)
            if result.rounds:
                result.rounds[-1].reviewer_output = None
            return result

        monkeypatch.setattr(pp_mod, "run_pingpong", no_reviewer_run)

        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )
        report = export_job_report(result)
        assert report["status"] == JOB_BLOCKED
        blocked_tasks = [t for t in report["tasks"] if t["status"] == TASK_BLOCKED]
        assert len(blocked_tasks) >= 1
        assert "missing_reviewer_output" in blocked_tasks[0].get("error", "")

    def test_text_report_shows_blocked(self, isolate_data_root, demo_repo, monkeypatch):
        """Text report shows task blocked status."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))

        import packages.orchestration.pingpong_loop as pp_mod
        real_run = pp_mod.run_pingpong

        def no_reviewer_run(*args, **kwargs):
            result = real_run(*args, **kwargs)
            if result.rounds:
                result.rounds[-1].reviewer_output = None
            return result

        monkeypatch.setattr(pp_mod, "run_pingpong", no_reviewer_run)

        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )
        text = format_job_report_text(result)
        assert "blocked" in text.lower()

    def test_no_proof_summary_for_blocked_task(self, isolate_data_root, demo_repo, monkeypatch):
        """Blocked task does not get a proof summary implying completion."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))

        import packages.orchestration.pingpong_loop as pp_mod
        real_run = pp_mod.run_pingpong

        def no_reviewer_run(*args, **kwargs):
            result = real_run(*args, **kwargs)
            if result.rounds:
                result.rounds[-1].reviewer_output = None
            return result

        monkeypatch.setattr(pp_mod, "run_pingpong", no_reviewer_run)

        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )
        blocked = [t for t in result.tasks if t.status == TASK_BLOCKED]
        assert len(blocked) >= 1
        assert blocked[0].proof_summary is None


# ---------------------------------------------------------------------------
# Step 4885 — Command-path smoke for fixed gate
# ---------------------------------------------------------------------------


class TestCommandPathGateSmoke:
    """Handler-level proof that gate works correctly."""

    def test_normal_two_task_job_completes(self, isolate_data_root, demo_repo, capsys):
        """Normal fake two-task job still completes through handler."""
        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        args = _make_args(job_id=job.job_id, builder="fake", reviewer="fake")
        COMMAND_HANDLERS["do.job-run"](args)
        out = json.loads(capsys.readouterr().out)
        assert out["status"] == "completed"
        applied = [t for t in out["tasks"] if t["status"] == TASK_APPLIED]
        assert len(applied) == 2

    def test_config_unaffected_by_gate_block(self, isolate_data_root, demo_repo, monkeypatch, capsys):
        """Continuation config survives even when gate blocks."""
        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))

        import packages.orchestration.pingpong_loop as pp_mod
        real_run = pp_mod.run_pingpong

        def no_reviewer_run(*args, **kwargs):
            result = real_run(*args, **kwargs)
            if result.rounds:
                result.rounds[-1].reviewer_output = None
            return result

        monkeypatch.setattr(pp_mod, "run_pingpong", no_reviewer_run)

        args = _make_args(
            job_id=job.job_id, max_rounds="7", repair_rounds=1,
        )
        COMMAND_HANDLERS["do.job-run"](args)
        out = json.loads(capsys.readouterr().out)
        assert out["status"] == "blocked"
        ec = out["execution_config"]
        assert ec["max_rounds"] == 7
        assert ec["repair_rounds_allowed"] == 1


# ---------------------------------------------------------------------------
# Steps 4887-4889 — Pre-apply target guard and post-apply defense-in-depth
# ---------------------------------------------------------------------------


class TestPreApplyTargetGuard:
    """Step 4890: target mutation before apply blocks without workspace apply."""

    def test_mutation_before_apply_blocks_job(self, isolate_data_root, demo_repo, monkeypatch):
        """Target mutation during pingpong blocks job before workspace apply."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))

        import packages.orchestration.pingpong_loop as pp_mod
        real_run = pp_mod.run_pingpong

        def mutating_run(*args, **kwargs):
            result = real_run(*args, **kwargs)
            (demo_repo / "INJECTED.txt").write_text("side effect")
            return result

        monkeypatch.setattr(pp_mod, "run_pingpong", mutating_run)

        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )

        assert result.status == JOB_BLOCKED
        assert result.tasks[0].status == TASK_BLOCKED
        assert "target_repo_mutated" in result.tasks[0].error
        assert result.target_guard.target_mutated is True
        assert "INJECTED.txt" in result.target_guard.changed_target_files

    def test_no_workspace_apply_after_mutation(self, isolate_data_root, demo_repo, monkeypatch):
        """Workspace apply must not happen when target is mutated."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))

        import packages.orchestration.pingpong_loop as pp_mod
        real_run = pp_mod.run_pingpong

        def mutating_run(*args, **kwargs):
            result = real_run(*args, **kwargs)
            (demo_repo / "INJECTED.txt").write_text("side effect")
            return result

        monkeypatch.setattr(pp_mod, "run_pingpong", mutating_run)

        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )

        task = result.tasks[0]
        assert task.apply_manifest is None
        assert task.status == TASK_BLOCKED

    def test_workspace_unchanged_after_mutation(self, isolate_data_root, demo_repo, monkeypatch):
        """Job workspace must not receive task's staged artifacts after target mutation."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))

        import packages.orchestration.pingpong_loop as pp_mod
        real_run = pp_mod.run_pingpong

        def mutating_run(*args, **kwargs):
            result = real_run(*args, **kwargs)
            (demo_repo / "INJECTED.txt").write_text("side effect")
            return result

        monkeypatch.setattr(pp_mod, "run_pingpong", mutating_run)

        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )

        assert result.tasks[0].apply_manifest is None
        assert result.tasks[0].status == TASK_BLOCKED
        assert not any(t.status == TASK_APPLIED for t in result.tasks)

    def test_task2_does_not_start_after_mutation(self, isolate_data_root, demo_repo, monkeypatch):
        """Task 2 must not start when task 1 is blocked by target mutation."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))

        import packages.orchestration.pingpong_loop as pp_mod
        real_run = pp_mod.run_pingpong

        def mutating_run(*args, **kwargs):
            result = real_run(*args, **kwargs)
            (demo_repo / "INJECTED.txt").write_text("side effect")
            return result

        monkeypatch.setattr(pp_mod, "run_pingpong", mutating_run)

        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )

        assert result.tasks[1].status in (TASK_SKIPPED, TASK_PENDING)

    def test_no_proof_summary_after_mutation(self, isolate_data_root, demo_repo, monkeypatch):
        """Proof summary must be absent for task blocked by target mutation."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))

        import packages.orchestration.pingpong_loop as pp_mod
        real_run = pp_mod.run_pingpong

        def mutating_run(*args, **kwargs):
            result = real_run(*args, **kwargs)
            (demo_repo / "INJECTED.txt").write_text("side effect")
            return result

        monkeypatch.setattr(pp_mod, "run_pingpong", mutating_run)

        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )

        assert result.tasks[0].proof_summary is None

    def test_guard_runs_before_apply_not_after(self, isolate_data_root, demo_repo, monkeypatch):
        """Pre-apply guard must catch mutation. Error must not say 'after_apply'."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))

        import packages.orchestration.pingpong_loop as pp_mod
        real_run = pp_mod.run_pingpong

        def mutating_run(*args, **kwargs):
            result = real_run(*args, **kwargs)
            (demo_repo / "INJECTED.txt").write_text("side effect")
            return result

        monkeypatch.setattr(pp_mod, "run_pingpong", mutating_run)

        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )

        assert "target_repo_mutated" in result.tasks[0].error
        assert "after_apply" not in result.tasks[0].error


class TestPreApplyTargetGuardReport:
    """Step 4891: report does not claim apply after target mutation."""

    def test_json_report_shows_blocked(self, isolate_data_root, demo_repo, monkeypatch):
        """JSON report must show task blocked, not applied."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))

        import packages.orchestration.pingpong_loop as pp_mod
        real_run = pp_mod.run_pingpong

        def mutating_run(*args, **kwargs):
            result = real_run(*args, **kwargs)
            (demo_repo / "INJECTED.txt").write_text("side effect")
            return result

        monkeypatch.setattr(pp_mod, "run_pingpong", mutating_run)

        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )

        report = export_job_report(result)
        task_report = report["tasks"][0]
        assert task_report["status"] == TASK_BLOCKED
        assert "target_repo_mutated" in task_report["error"]

    def test_json_report_no_applied_manifest(self, isolate_data_root, demo_repo, monkeypatch):
        """JSON report must not show apply_manifest.status='applied'."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))

        import packages.orchestration.pingpong_loop as pp_mod
        real_run = pp_mod.run_pingpong

        def mutating_run(*args, **kwargs):
            result = real_run(*args, **kwargs)
            (demo_repo / "INJECTED.txt").write_text("side effect")
            return result

        monkeypatch.setattr(pp_mod, "run_pingpong", mutating_run)

        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )

        report = export_job_report(result)
        manifest = report["tasks"][0]["apply_manifest"]
        if manifest is not None:
            assert manifest.get("status") != "applied"
            assert manifest.get("applied_files", []) == []

    def test_text_report_shows_blocked(self, isolate_data_root, demo_repo, monkeypatch):
        """Text report must show blocked task, not applied."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))

        import packages.orchestration.pingpong_loop as pp_mod
        real_run = pp_mod.run_pingpong

        def mutating_run(*args, **kwargs):
            result = real_run(*args, **kwargs)
            (demo_repo / "INJECTED.txt").write_text("side effect")
            return result

        monkeypatch.setattr(pp_mod, "run_pingpong", mutating_run)

        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )

        text = format_job_report_text(result)
        assert "blocked" in text.lower()
        assert "target_repo_mutated" in text

    def test_no_proof_summary_in_report(self, isolate_data_root, demo_repo, monkeypatch):
        """Proof summary must be absent in JSON report for mutation-blocked task."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))

        import packages.orchestration.pingpong_loop as pp_mod
        real_run = pp_mod.run_pingpong

        def mutating_run(*args, **kwargs):
            result = real_run(*args, **kwargs)
            (demo_repo / "INJECTED.txt").write_text("side effect")
            return result

        monkeypatch.setattr(pp_mod, "run_pingpong", mutating_run)

        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )

        report = export_job_report(result)
        assert report["tasks"][0]["proof_summary"] is None


class TestPostApplyTargetGuard:
    """Step 4889: post-apply defense-in-depth target guard."""

    def test_post_apply_mutation_blocks(self, isolate_data_root, demo_repo, monkeypatch):
        """If target mutates during workspace apply, post-apply guard catches it."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))

        import packages.orchestration.pingpong_job as job_mod
        real_apply = job_mod._strict_apply_to_workspace

        def mutating_apply(*args, **kwargs):
            manifest = real_apply(*args, **kwargs)
            (demo_repo / "LATE_INJECT.txt").write_text("late mutation")
            return manifest

        monkeypatch.setattr(job_mod, "_strict_apply_to_workspace", mutating_apply)

        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )

        assert result.status == JOB_BLOCKED
        blocked_task = next(t for t in result.tasks if t.status == TASK_BLOCKED)
        assert "target_repo_mutated_after_apply" in blocked_task.error

    def test_post_apply_guard_reports_changed_files(self, isolate_data_root, demo_repo, monkeypatch):
        """Post-apply guard must report which files changed."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))

        import packages.orchestration.pingpong_job as job_mod
        real_apply = job_mod._strict_apply_to_workspace

        def mutating_apply(*args, **kwargs):
            manifest = real_apply(*args, **kwargs)
            (demo_repo / "LATE_INJECT.txt").write_text("late mutation")
            return manifest

        monkeypatch.setattr(job_mod, "_strict_apply_to_workspace", mutating_apply)

        result = run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )

        assert result.target_guard.target_mutated is True
        assert "LATE_INJECT.txt" in result.target_guard.changed_target_files


class TestTargetMutatedResultGatePreserved:
    """Step 4892: result.target_mutated=True still blocks at completion gate."""

    def test_target_mutated_result_blocks_at_gate(self, isolate_data_root, demo_repo, monkeypatch):
        """result.target_mutated=True blocks at completion gate, before target guard."""
        result_obj = self._run_with_target_mutated_result(demo_repo, monkeypatch)
        assert result_obj.status == JOB_BLOCKED
        assert result_obj.tasks[0].status == TASK_BLOCKED
        assert "target_mutated" in result_obj.tasks[0].error
        assert "completion_gate_failed" in result_obj.tasks[0].error

    def test_no_workspace_apply_on_result_target_mutated(self, isolate_data_root, demo_repo, monkeypatch):
        """Workspace apply must not happen when result reports target_mutated."""
        result_obj = self._run_with_target_mutated_result(demo_repo, monkeypatch)
        assert result_obj.tasks[0].apply_manifest is None

    def test_no_proof_summary_on_result_target_mutated(self, isolate_data_root, demo_repo, monkeypatch):
        """Proof summary must be absent when result reports target_mutated."""
        result_obj = self._run_with_target_mutated_result(demo_repo, monkeypatch)
        assert result_obj.tasks[0].proof_summary is None

    def test_task2_skipped_on_result_target_mutated(self, isolate_data_root, demo_repo, monkeypatch):
        """Task 2 must not start when result target_mutated blocks task 1."""
        result_obj = self._run_with_target_mutated_result(demo_repo, monkeypatch)
        assert result_obj.tasks[1].status in (TASK_SKIPPED, TASK_PENDING)

    def _run_with_target_mutated_result(self, demo_repo, monkeypatch):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))

        import packages.orchestration.pingpong_loop as pp_mod
        real_run = pp_mod.run_pingpong

        def corrupt_run(*args, **kwargs):
            result = real_run(*args, **kwargs)
            result.target_mutated = True
            return result

        monkeypatch.setattr(pp_mod, "run_pingpong", corrupt_run)

        return run_job(
            job.job_id,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )


class TestCommandPathPreApplySmoke:
    """Step 4895: handler-level smoke tests for pre-apply target guard."""

    def test_handler_mutation_blocks(self, isolate_data_root, demo_repo, monkeypatch, capsys):
        """Target mutation blocks through full CLI handler path."""
        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))

        import packages.orchestration.pingpong_loop as pp_mod
        real_run = pp_mod.run_pingpong

        def mutating_run(*args, **kwargs):
            result = real_run(*args, **kwargs)
            (demo_repo / "INJECTED.txt").write_text("side effect")
            return result

        monkeypatch.setattr(pp_mod, "run_pingpong", mutating_run)

        args = _make_args(job_id=job.job_id, builder="fake", reviewer="fake")
        COMMAND_HANDLERS["do.job-run"](args)
        out = json.loads(capsys.readouterr().out)
        assert out["status"] == "blocked"
        assert out["tasks"][0]["status"] == TASK_BLOCKED
        assert "target_repo_mutated" in out["tasks"][0]["error"]

    def test_handler_clean_run_unaffected(self, isolate_data_root, demo_repo, capsys):
        """Normal clean run still completes with pre-apply guard present."""
        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        args = _make_args(job_id=job.job_id, builder="fake", reviewer="fake")
        COMMAND_HANDLERS["do.job-run"](args)
        out = json.loads(capsys.readouterr().out)
        assert out["status"] == "completed"
        applied = [t for t in out["tasks"] if t["status"] == TASK_APPLIED]
        assert len(applied) == 2


class TestTaskEntryToPlannedTaskAdapter:
    """task_entry_to_planned_task (DECISION F112 D2/D3) translates one
    dispatched TaskEntry into the granularity machinery's PlannedTask."""

    def test_maps_fields_and_splits_acceptance_on_newlines(self):
        task = TaskEntry(
            task_id="T009",
            title="Add OAuth support",
            body="Wire the OAuth handshake into the login flow.",
            acceptance="Login redirects to provider\n\nToken is persisted\n",
        )

        planned = task_entry_to_planned_task(task)

        assert planned is not None
        assert planned.id == "T009"
        assert planned.title == "Add OAuth support"
        assert planned.goal == "Wire the OAuth handshake into the login flow."
        assert planned.acceptance == [
            "Login redirects to provider", "Token is persisted",
        ]
        assert planned.files_hint == []
        assert planned.est_tokens_band == "XL"

    def test_goal_falls_back_to_title_when_body_is_empty(self):
        task = TaskEntry(task_id="T010", title="Bump dependency", acceptance="Version pinned")

        planned = task_entry_to_planned_task(task)

        assert planned is not None
        assert planned.goal == "Bump dependency"

    def test_returns_none_when_acceptance_has_no_non_blank_line(self):
        task = TaskEntry(task_id="T011", title="Empty", body="x", acceptance="\n\n  \n")

        assert task_entry_to_planned_task(task) is None

    def test_output_is_accepted_by_split_one_task_and_clusters_one_child_per_line(self):
        from packages.orchestration.task_granularity import split_one_task

        task = TaskEntry(
            task_id="T012",
            title="Large task",
            body="Large task",
            acceptance="First acceptance item\nSecond acceptance item\nThird acceptance item",
        )
        planned = task_entry_to_planned_task(task)
        assert planned is not None

        children = split_one_task(planned)

        assert children is not None
        assert len(children) == 3
        assert [c.acceptance for c in children] == [
            ["First acceptance item"],
            ["Second acceptance item"],
            ["Third acceptance item"],
        ]
