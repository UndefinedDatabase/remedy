"""F258 T003 — tests for surfacing a self-use run's own defects verbatim.

The load-bearing test is
:meth:`TestDescribeSelfUseRunDefects.test_a_blocked_run_surfaces_the_jobs_own_error_text`,
which pins that the returned strings quote the ``JobPlan``'s real fields —
never a summary this module invented.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from packages.core.models import RunState
from packages.orchestration.pingpong_job import (
    JOB_STOPPED,
    TASK_PENDING,
    JobPlan,
    TaskEntry,
    parse_job_file,
    run_job,
)
from packages.orchestration.pingpong_provider import FakeProvider
from packages.orchestration.self_use_findings import describe_self_use_run_defects

_ONE_TASK_JOB = "# Job: Demo\n\n## Task 1\nDo the thing.\n\nAcceptance:\n- it is done\n"


@pytest.fixture
def isolate_data_root(tmp_path: Path, monkeypatch) -> Path:
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


@pytest.fixture
def demo_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("# demo\n")
    return repo


class TestDescribeSelfUseRunDefects:
    """Every returned string is the job's own field, never an invented one."""

    def test_a_completed_run_surfaces_no_defects(self, isolate_data_root, demo_repo):
        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
            reviewer_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
            repair_rounds=0,
        )
        assert describe_self_use_run_defects(result) == ()

    def test_a_blocked_run_surfaces_the_jobs_own_error_text(self, isolate_data_root, demo_repo):
        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=FakeProvider(pass_on_round=99, fail_on_round=1),
            reviewer_provider=FakeProvider(pass_on_round=99, fail_on_round=1),
            max_rounds=1,
            repair_rounds=0,
        )
        defects = describe_self_use_run_defects(result)
        assert len(defects) == 2
        assert defects[0] == f"job {result.job_id} ({result.state}): {result.error}"
        assert defects[1] == f"{result.tasks[0].task_id} ({result.tasks[0].status}): {result.tasks[0].error}"
        assert result.error in defects[0]
        assert result.tasks[0].error in defects[1]

    def test_task_order_is_preserved(self, isolate_data_root, demo_repo):
        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        result = run_job(
            job.job_id,
            builder_provider=FakeProvider(pass_on_round=99, fail_on_round=1),
            reviewer_provider=FakeProvider(pass_on_round=99, fail_on_round=1),
            max_rounds=1,
            repair_rounds=0,
        )
        defects = describe_self_use_run_defects(result)
        # the job-level entry always comes first, task entries follow in task order
        assert defects[0].startswith("job ")
        assert defects[1].startswith(result.tasks[0].task_id + " (")

    def test_a_budget_stopped_run_with_blank_errors_surfaces_the_stop(self):
        """R-0972: SU-020's run — job stopped on its budget, task stopped, every error blank.

        A stop clears the job's ``error`` and sends the task's ``status`` back to
        ``pending``, recording the stop in the task's ``final_status`` only.
        """
        result = JobPlan(
            job_id="5edc7cfc1dee4d75",
            state=JOB_STOPPED,
            stop_reason="budget_exhausted:max_provider_calls",
            stop_source="budget",
            tasks=[TaskEntry(task_id="T001", status=TASK_PENDING, final_status="stopped")],
        )
        assert result.error == ""
        assert result.tasks[0].error == ""
        assert describe_self_use_run_defects(result) == (
            "job 5edc7cfc1dee4d75 (stopped): stop_reason=budget_exhausted:max_provider_calls; "
            "stop_source=budget",
            "T001 (pending): final_status=stopped",
        )

    def test_a_stop_that_never_finalized_surfaces_its_stop_and_its_manifest_error(self):
        """R-0826: SU-012's run — the stop was recorded but the manifest write failed,
        so the state stayed ``running`` while every ``error`` stayed blank."""
        manifest_error = "run_manifest_write_failed: ManifestError: disk gone"
        result = JobPlan(
            job_id="020c1ef366af4f07",
            state=RunState.RUNNING,
            stop_reason="budget_exhausted:max_provider_calls",
            stop_source="budget",
            stopped_at="2026-09-07T15:03:52.142876+00:00",
            run_manifest_error=manifest_error,
            tasks=[TaskEntry(task_id="T001", status=TASK_PENDING, final_status="stopped")],
        )
        assert result.error == "" and result.tasks[0].error == ""
        assert describe_self_use_run_defects(result) == (
            "job 020c1ef366af4f07 (running): stop_reason=budget_exhausted:max_provider_calls; "
            "stop_source=budget",
            f"job 020c1ef366af4f07 (running): run_manifest_error={manifest_error}",
            "T001 (pending): final_status=stopped",
        )

    def test_a_task_that_did_not_pass_with_a_blank_error_is_named(self):
        """R-0826: any final status other than ``staged_review_passed`` is a defect
        when the task's own ``error`` says nothing; a task that never ran is not."""
        result = JobPlan(
            job_id="aaaabbbbccccdddd",
            state=RunState.COMPLETED,
            tasks=[
                TaskEntry(task_id="T001", status=RunState.COMPLETED,
                          final_status="staged_review_passed"),
                TaskEntry(task_id="T002", status=RunState.COMPLETED,
                          final_status="review_failed"),
                TaskEntry(task_id="T003", status=TASK_PENDING),
            ],
        )
        assert describe_self_use_run_defects(result) == (
            "T002 (completed): final_status=review_failed",
        )
