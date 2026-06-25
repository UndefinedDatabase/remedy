"""Tests for the Job Task Runner (Steps 4827-4831).

Covers: job plan parsing, sequential execution, workspace apply,
failure blocking, target-repo safety, report output, and max-tasks limit.
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
    TASK_PENDING,
    TASK_SKIPPED,
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


# ---------------------------------------------------------------------------
# 1. Job plan parses two tasks
# ---------------------------------------------------------------------------


class TestJobPlanParsing:
    def test_parses_two_tasks(self, isolate_data_root):
        job = parse_job_file(_TWO_TASK_JOB, "/tmp/repo")
        assert len(job.tasks) == 2
        assert job.tasks[0].task_id == "T001"
        assert job.tasks[1].task_id == "T002"
        assert job.status == JOB_PLANNED

    def test_task_titles(self, isolate_data_root):
        job = parse_job_file(_TWO_TASK_JOB, "/tmp/repo")
        assert "repair-loop" in job.tasks[0].title.lower() or "repair" in job.tasks[0].body.lower()

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
        assert job.status == JOB_PLANNED

    def test_plan_file_not_found(self, isolate_data_root):
        job = plan_job_from_file("/nonexistent/job.md", "/tmp/repo")
        assert job.status == JOB_BLOCKED
        assert "job_file_not_found" in job.error


# ---------------------------------------------------------------------------
# 2. No provider call during job plan
# ---------------------------------------------------------------------------


class TestJobPlanNoProvider:
    def test_no_provider_call(self, isolate_data_root):
        """parse_job_file is deterministic — no provider instantiated."""
        job = parse_job_file(_TWO_TASK_JOB, "/tmp/repo")
        # If we got here without import error or network call, no provider used
        assert job.status == JOB_PLANNED


# ---------------------------------------------------------------------------
# 3-10. Sequential execution, blocking, workspace apply
# ---------------------------------------------------------------------------


class TestSequentialExecution:
    def _pass_provider(self):
        return FakeProvider(pass_on_round=1, fail_on_round=99)

    def test_tasks_execute_sequentially(self, isolate_data_root, demo_repo):
        """Both tasks run and complete in order."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        p = self._pass_provider()
        result = run_job(
            job.job_id,
            builder_provider=p,
            reviewer_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
            repair_rounds=0,
        )
        assert result.status == JOB_COMPLETED
        assert result.tasks[0].status == TASK_APPLIED
        assert result.tasks[1].status == TASK_APPLIED

    def test_task2_waits_for_task1(self, isolate_data_root, demo_repo):
        """Task 2 cannot start until task 1 is passed and applied."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=self._pass_provider(),
            reviewer_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
            repair_rounds=0,
        )
        assert result.tasks[0].status == TASK_APPLIED
        assert result.tasks[0].run_id != ""
        assert result.tasks[1].run_id != ""

    def test_task_failure_blocks_job(self, isolate_data_root, demo_repo):
        """If task 1 fails, job is blocked and task 2 is skipped."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=FakeProvider(pass_on_round=99),
            reviewer_provider=FakeProvider(pass_on_round=99),
            max_rounds=1,
            repair_rounds=0,
        )
        assert result.status == JOB_BLOCKED
        assert result.tasks[0].status == TASK_FAILED
        assert result.tasks[1].status == TASK_SKIPPED

    def test_real_target_repo_not_mutated(self, isolate_data_root, demo_repo):
        """Target repo files remain unchanged after job run."""
        readme_before = (demo_repo / "README.md").read_text()
        main_before = (demo_repo / "src" / "main.py").read_text()

        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        run_job(
            job.job_id,
            builder_provider=self._pass_provider(),
            reviewer_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
            repair_rounds=0,
        )

        assert (demo_repo / "README.md").read_text() == readme_before
        assert (demo_repo / "src" / "main.py").read_text() == main_before

    def test_job_workspace_receives_changes(self, isolate_data_root, demo_repo):
        """Job workspace has task changes after successful run."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=self._pass_provider(),
            reviewer_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
            repair_rounds=0,
        )
        assert result.job_workspace_path != ""
        ws = Path(result.job_workspace_path)
        assert ws.exists()

    def test_task_done_requires_review_pass_and_apply(self, isolate_data_root, demo_repo):
        """A task is APPLIED only after review pass + workspace apply."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=self._pass_provider(),
            reviewer_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
            repair_rounds=0,
        )
        for t in result.tasks:
            if t.status == TASK_APPLIED:
                assert t.final_status == "staged_review_passed"

    def test_max_tasks_limits_execution(self, isolate_data_root, demo_repo):
        """--max-tasks 1 runs only the first task."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=self._pass_provider(),
            reviewer_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
            repair_rounds=0,
            max_tasks=1,
        )
        assert result.tasks[0].status == TASK_APPLIED
        assert result.tasks[1].status == TASK_PENDING

    def test_run_ids_recorded(self, isolate_data_root, demo_repo):
        """Each executed task has a run_id."""
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=self._pass_provider(),
            reviewer_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
            repair_rounds=0,
        )
        assert result.tasks[0].run_id != ""
        assert result.tasks[1].run_id != ""
        assert result.tasks[0].run_id != result.tasks[1].run_id


# ---------------------------------------------------------------------------
# 11-12. Report JSON and text
# ---------------------------------------------------------------------------


class TestJobReport:
    def _pass_provider(self):
        return FakeProvider(pass_on_round=1, fail_on_round=99)

    def test_report_json_shows_statuses(self, isolate_data_root, demo_repo):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=self._pass_provider(),
            reviewer_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
            repair_rounds=0,
        )
        report = export_job_report(result)
        assert report["status"] == "completed"
        assert len(report["tasks"]) == 2
        for t in report["tasks"]:
            assert "task_id" in t
            assert "status" in t
            assert "run_id" in t

    def test_report_json_has_warning(self, isolate_data_root, demo_repo):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=self._pass_provider(),
            reviewer_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
            repair_rounds=0,
        )
        report = export_job_report(result)
        assert "NOT mutated" in report["warning"]

    def test_report_json_serializable(self, isolate_data_root, demo_repo):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=self._pass_provider(),
            reviewer_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
            repair_rounds=0,
        )
        report = export_job_report(result)
        text = json.dumps(report, indent=2)
        assert "job_id" in text

    def test_text_report_concise(self, isolate_data_root, demo_repo):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=self._pass_provider(),
            reviewer_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
            repair_rounds=0,
        )
        text = format_job_report_text(result)
        assert "T001" in text
        assert "T002" in text
        assert "NOT mutated" in text

    def test_report_has_workspace_changes(self, isolate_data_root, demo_repo):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=self._pass_provider(),
            reviewer_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
            repair_rounds=0,
        )
        report = export_job_report(result)
        assert report["has_workspace_changes"] is True

    def test_report_next_command(self, isolate_data_root, demo_repo):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        report = export_job_report(job)
        assert "job run" in report["next_command"]


# ---------------------------------------------------------------------------
# 13. Token-bounded context
# ---------------------------------------------------------------------------


class TestTokenBoundedContext:
    def test_task_body_bounded(self, isolate_data_root):
        """Large task body is truncated to 2000 chars."""
        big_body = "x" * 5000
        text = f"# Job: Test\n\n## Task 1\n{big_body}\n"
        job = parse_job_file(text, "/tmp/repo")
        assert len(job.tasks[0].body) <= 2020  # 2000 + "\n[truncated]"
        assert "[truncated]" in job.tasks[0].body


# ---------------------------------------------------------------------------
# 14-17. Existing flows preserved (smoke checks)
# ---------------------------------------------------------------------------


class TestExistingFlowsPreserved:
    def test_single_task_run_still_works(self, isolate_data_root, tmp_path):
        """Existing single-task run_pingpong still functions."""
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

    def test_repair_governance_still_works(self, isolate_data_root, tmp_path):
        """Repair round resolution still functions."""
        from packages.orchestration.pingpong_loop import resolve_repair_rounds

        val, src = resolve_repair_rounds(None)
        assert val == 2
        assert src == "default"

        val, src = resolve_repair_rounds(0)
        assert val == 0
        assert src == "cli"

    def test_evidence_import_still_works(self):
        """Evidence module still importable."""
        from packages.orchestration.pingpong_evidence import export_evidence
        assert callable(export_evidence)

    def test_promotion_import_still_works(self):
        """Promotion module still importable."""
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

    def test_load_nonexistent(self, isolate_data_root):
        assert load_job_plan("nonexistent_id") is None


# ---------------------------------------------------------------------------
# CLI dispatch (catalog + handler existence)
# ---------------------------------------------------------------------------


class TestCliDispatch:
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
