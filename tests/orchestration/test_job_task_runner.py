"""Tests for the Job Task Runner (Steps 4827-4844).

Covers: job plan parsing, deterministic task IDs, strict workspace apply,
sequential execution, target repo guard, token-bounded context, report output,
blocking-path E2E, CLI dispatch, and existing flow preservation.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration.pingpong_job import (
    JOB_BLOCKED,
    JOB_COMPLETED,
    JOB_PLANNED,
    TASK_APPLIED,
    TASK_FAILED,
    TASK_PASSED,
    TASK_PENDING,
    TASK_SKIPPED,
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
        assert "job-report" in cmd
        assert "job report" not in cmd.replace("job-report", "")

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
        assert result.tasks[0].status == TASK_FAILED
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
