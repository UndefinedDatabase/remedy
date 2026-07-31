"""F053 T002 — every terminal path writes exactly one final report.

The acceptance rule this file pins: one report file per terminal job,
REGENERATED on resume-then-finish rather than appended to, written from the
single terminal-state hook so no path can be forgotten — and never, under any
failure, allowed to kill the run it is only describing.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

import packages.orchestration.long_run_executor as lre
from packages.core.models import Job, RunState, Task
from packages.orchestration.long_run_executor import (
    REPORTED_TERMINALS,
    TERMINAL_ALL_GREEN,
    TERMINAL_BLOCKED,
    TERMINAL_BUDGET_EXHAUSTED,
    TERMINAL_DEADLINE_REACHED,
    TERMINAL_MAX_CYCLES_REACHED,
    TERMINAL_STOPPED_BY_OPERATOR,
    _apply_terminal,
)
from packages.orchestration.run_report import (
    REPORT_ERROR_METADATA_KEY,
    REPORT_FILENAME,
    report_path,
    write_final_report,
)

pytestmark = pytest.mark.integration

UTC = timezone.utc
T0 = datetime(2026, 7, 31, 9, 0, 0, tzinfo=UTC)

#: The five terminals that end a run. Enumerated explicitly rather than
#: derived, so adding a terminal without deciding whether it reports is a
#: test failure and not a silent gap.
ALL_TERMINALS = (
    TERMINAL_ALL_GREEN,
    TERMINAL_STOPPED_BY_OPERATOR,
    TERMINAL_BUDGET_EXHAUSTED,
    TERMINAL_DEADLINE_REACHED,
    TERMINAL_BLOCKED,
)


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path: Path, monkeypatch) -> Path:
    """The report lands in the evidence area — never the real data root."""
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


def make_job(task_count: int = 1) -> Job:
    return Job(
        name="reporting-job",
        user_prompt="build the thing",
        tasks=[Task(description=f"task {i}", inputs={"task_type": "documentation"})
               for i in range(task_count)],
        state=RunState.PLANNED,
    )


class TestEveryTerminalPathWritesOneReport:

    @pytest.mark.parametrize("terminal", ALL_TERMINALS)
    def test_each_terminal_writes_exactly_one_report(self, terminal):
        job = make_job()
        _apply_terminal(job, terminal, "some reason")
        path = report_path(str(job.id))
        assert path.is_file(), f"{terminal} wrote no report"
        assert path.name == REPORT_FILENAME
        siblings = list(path.parent.glob("report*"))
        assert siblings == [path], siblings

    @pytest.mark.parametrize("terminal", ALL_TERMINALS)
    def test_the_report_names_the_terminal_it_was_written_for(self, terminal):
        job = make_job()
        _apply_terminal(job, terminal, "some reason")
        text = report_path(str(job.id)).read_text(encoding="utf-8")
        assert f"- Terminal status: {terminal}" in text
        assert "INTERIM SNAPSHOT" not in text          # a final report, not a snapshot

    def test_the_reported_set_is_exactly_the_five_terminals(self):
        assert REPORTED_TERMINALS == frozenset(ALL_TERMINALS)

    def test_max_cycles_reached_is_not_terminal_and_writes_nothing(self):
        """The job still has work; a "final" report would lie about that."""
        job = make_job()
        _apply_terminal(job, TERMINAL_MAX_CYCLES_REACHED, "")
        assert not report_path(str(job.id)).exists()

    def test_the_report_sits_beside_the_cycle_records(self):
        job = make_job()
        _apply_terminal(job, TERMINAL_ALL_GREEN, "")
        expected = lre.cycle_evidence_dir(str(job.id)).parent / REPORT_FILENAME
        assert report_path(str(job.id)) == expected

    def test_the_stop_reason_reaches_the_report(self):
        job = make_job()
        _apply_terminal(job, TERMINAL_BUDGET_EXHAUSTED, "budget_exhausted:tokens")
        text = report_path(str(job.id)).read_text(encoding="utf-8")
        assert "- Stop reason: budget_exhausted:tokens" in text


class TestRegeneratedNotAppended:
    """Finish → resume → finish leaves ONE file, holding the latest run."""

    def test_a_second_terminal_regenerates_the_same_file(self):
        job = make_job()
        _apply_terminal(job, TERMINAL_BLOCKED, "no_ready_tasks")
        first = report_path(str(job.id)).read_text(encoding="utf-8")
        assert "- Terminal status: blocked" in first

        # …resume, finish for real.
        for task in job.tasks:
            task.status = RunState.COMPLETED
        job.state = RunState.COMPLETED
        _apply_terminal(job, TERMINAL_ALL_GREEN, "")

        path = report_path(str(job.id))
        assert list(path.parent.glob("report*")) == [path]
        second = path.read_text(encoding="utf-8")
        assert "- Terminal status: all_green" in second
        assert "- Terminal status: blocked" not in second, "appended instead of regenerated"

    def test_the_file_never_grows_by_concatenation(self):
        job = make_job()
        _apply_terminal(job, TERMINAL_ALL_GREEN, "")
        once = report_path(str(job.id)).read_text(encoding="utf-8")
        for _ in range(3):
            _apply_terminal(job, TERMINAL_ALL_GREEN, "")
        assert report_path(str(job.id)).read_text(encoding="utf-8") == once

    def test_exactly_one_report_heading_per_file(self):
        job = make_job()
        _apply_terminal(job, TERMINAL_ALL_GREEN, "")
        _apply_terminal(job, TERMINAL_ALL_GREEN, "")
        text = report_path(str(job.id)).read_text(encoding="utf-8")
        assert text.count("# Run report — ") == 1


class TestAReportFailureNeverKillsTheRun:
    """The report is an account of the run, not a gate on it."""

    def test_a_write_failure_is_recorded_and_swallowed(self, monkeypatch):
        job = make_job()

        def boom(*_args, **_kwargs):
            raise OSError("disk gone")

        monkeypatch.setattr("packages.orchestration.run_report.report_path", boom)
        assert write_final_report(job) is None
        assert "OSError: disk gone" in job.metadata[REPORT_ERROR_METADATA_KEY]

    def test_the_terminal_transition_still_completes(self, monkeypatch):
        job = make_job()

        def boom(*_args, **_kwargs):
            raise OSError("disk gone")

        monkeypatch.setattr("packages.orchestration.run_report.report_path", boom)
        status = _apply_terminal(job, TERMINAL_ALL_GREEN, "")
        assert status == lre.TERMINAL_JOB_STATUS[TERMINAL_ALL_GREEN]
        assert job.state == RunState.COMPLETED
        assert job.metadata["cycle_terminal_status"] == TERMINAL_ALL_GREEN

    def test_a_later_success_clears_the_recorded_error(self, monkeypatch):
        job = make_job()

        def boom(*_args, **_kwargs):
            raise OSError("disk gone")

        monkeypatch.setattr("packages.orchestration.run_report.report_path", boom)
        _apply_terminal(job, TERMINAL_ALL_GREEN, "")
        assert REPORT_ERROR_METADATA_KEY in job.metadata

        monkeypatch.undo()
        _apply_terminal(job, TERMINAL_ALL_GREEN, "")
        assert REPORT_ERROR_METADATA_KEY not in job.metadata

    def test_write_report_false_skips_the_writer_entirely(self):
        """The seam that lets a caller apply a terminal without an account."""
        job = make_job()
        _apply_terminal(job, TERMINAL_ALL_GREEN, "", write_report=False)
        assert not report_path(str(job.id)).exists()


class TestThroughTheRealLoop:
    """The hook is reached by run_cycles itself, not only when called directly."""

    def test_a_completed_run_leaves_a_report(self):
        job = make_job()

        def completing_step(current_job: Job, provider_call) -> lre.TaskAttempt:
            task = next((t for t in current_job.tasks
                         if t.status == RunState.PENDING), None)
            if task is None:
                return lre.TaskAttempt()
            task.status = RunState.COMPLETED
            if all(t.status == RunState.COMPLETED for t in current_job.tasks):
                current_job.state = RunState.COMPLETED
            return lre.TaskAttempt(task_id=task.id, executed=True, verified=True)

        result = lre.run_cycles(
            job, lre.CycleLimits(max_cycles=2), lambda _ctx: None,
            task_step=completing_step, clock=_FakeClock(),
            save=lambda _job: None, record_checkpoint=False)
        assert result.terminal_status == TERMINAL_ALL_GREEN
        text = report_path(str(job.id)).read_text(encoding="utf-8")
        assert "- Terminal status: all_green" in text
        assert "## Recommended next action" in text


class _FakeClock:
    def __init__(self, start: datetime = T0,
                 step: timedelta = timedelta(seconds=1)) -> None:
        self.now = start
        self.step = step

    def __call__(self) -> datetime:
        current = self.now
        self.now = self.now + self.step
        return current
