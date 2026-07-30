"""F051 T003 — open decisions render FIRST, with the command that answers them.

Covers the pure view helpers in ``decision_queue`` and the two CLI views that
use them (``remedy job status`` and ``remedy job report``), in text and JSON.
The point being pinned: a returning human sees what the run needs before
anything else, and the exact command is in the output — never paraphrased.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from apps.cli.commands.job import _cmd_job_report, _cmd_job_status
from packages.core.models import Job, RunState, Task
from packages.orchestration.decision_queue import (
    HumanDecision,
    list_decisions,
    open_decisions,
    open_decisions_next_action,
    render_open_decisions_lines,
    sort_open_decisions_first,
)
from packages.orchestration.escalation import (
    answer_task_decision,
    enqueue_task_decision,
    task_decision_answer_command,
)
from packages.orchestration.storage import save_job

UTC = timezone.utc
T0 = datetime(2026, 7, 30, 12, 0, 0, tzinfo=UTC)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path: Path, monkeypatch) -> Path:
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


def make_job(*, name: str = "view-job", state: RunState = RunState.PAUSED,
             target_repo: str = "/tmp/repo") -> Job:
    """A job with a repo attached, so the queue's baseline is empty.

    Without ``target_repo`` the queue derives its own ``no_target_repo`` blocker
    (stop_reasons.py) — real behavior, pinned by its own test below, but noise
    for the assertions about task decisions.
    """
    return Job(
        name=name,
        user_prompt="build the thing",
        tasks=[Task(description=f"task {i}", inputs={"task_type": "documentation"})
               for i in range(2)],
        state=state,
        metadata={"target_repo": target_repo},
    )


def saved_job_with_open_decision(*, question: str = "Which database?",
                                 options=("postgres", "sqlite")) -> tuple[Job, dict]:
    """A persisted blocked job whose first task awaits a decision."""
    job = make_job()
    record = enqueue_task_decision(
        job, task_id=job.tasks[0].id, question=question,
        options=options, safe_default="", now=T0)
    save_job(job)
    return job, record


def decision(id_: str, *, status: str = "open", severity: str = "blocker",
             type_: str = "task_decision", actions=()) -> HumanDecision:
    return HumanDecision(
        id=id_, type=type_, status=status, severity=severity, source="test",
        related_node_id="", related_intent_id="", related_file="",
        safe_summary=f"summary {id_}", next_actions=tuple(actions),
        created_at="", resolved_at=None if status == "open" else "")


# ---------------------------------------------------------------------------
# The pure view helpers
# ---------------------------------------------------------------------------


class TestOrdering:
    def test_open_decisions_come_before_resolved_ones(self):
        items = [decision("resolved-1", status="resolved", severity="info"),
                 decision("open-1")]

        assert [d.id for d in sort_open_decisions_first(items)] == [
            "open-1", "resolved-1"]

    def test_blockers_come_before_warnings_and_info(self):
        items = [decision("i", severity="info"),
                 decision("w", severity="warning"),
                 decision("b", severity="blocker")]

        assert [d.id for d in sort_open_decisions_first(items)] == ["b", "w", "i"]

    def test_equal_severity_keeps_its_original_order(self):
        items = [decision("first"), decision("second")]

        assert [d.id for d in sort_open_decisions_first(items)] == [
            "first", "second"]

    def test_an_unknown_severity_sorts_last_instead_of_raising(self):
        items = [decision("odd", severity="chartreuse"), decision("info-1",
                                                                  severity="info")]

        assert [d.id for d in sort_open_decisions_first(items)] == ["info-1", "odd"]

    def test_open_decisions_filters_out_the_resolved_ones(self):
        items = [decision("open-1"), decision("done", status="resolved")]

        assert [d.id for d in open_decisions(items)] == ["open-1"]


class TestRenderedBlock:
    def test_nothing_open_renders_nothing(self):
        assert render_open_decisions_lines([]) == []
        assert render_open_decisions_lines(
            [decision("done", status="resolved")]) == []

    def test_the_header_counts_the_open_decisions(self):
        lines = render_open_decisions_lines(
            [decision("a", actions=("cmd a",)), decision("b", actions=("cmd b",))])

        assert lines[0] == "Open decisions: 2 — the run needs an answer"

    def test_every_answer_command_appears_in_full(self):
        long_command = ('remedy decision resolve deadbeef td:cafebabe '
                        '--reason "a rather long answer that must not be cut"')
        lines = render_open_decisions_lines([decision("x", actions=(long_command,))])

        assert any(line.endswith(long_command) for line in lines)

    def test_the_summary_and_severity_are_shown(self):
        lines = render_open_decisions_lines([decision("td:abc", actions=("cmd",))])

        assert "[blocker] task_decision td:abc: summary td:abc" in lines[1]

    def test_the_next_action_is_the_most_urgent_open_command(self):
        items = [decision("info-1", severity="info", actions=("cmd info",)),
                 decision("block-1", severity="blocker", actions=("cmd block",))]

        assert open_decisions_next_action(items) == "cmd block"

    def test_the_next_action_is_empty_when_nothing_is_open(self):
        assert open_decisions_next_action([]) == ""
        assert open_decisions_next_action([decision("d", status="resolved")]) == ""

    def test_an_open_decision_without_a_command_is_skipped_for_next_action(self):
        items = [decision("no-cmd", actions=()),
                 decision("has-cmd", actions=("cmd here",))]

        assert open_decisions_next_action(items) == "cmd here"


# ---------------------------------------------------------------------------
# remedy job status
# ---------------------------------------------------------------------------


class TestJobStatusView:
    def test_the_open_decision_block_is_printed_first(self, capsys):
        job, record = saved_job_with_open_decision()

        _cmd_job_status(str(job.id))
        out = capsys.readouterr().out.splitlines()

        assert out[0] == "Open decisions: 1 — the run needs an answer"
        assert out[0:1] and out[1].strip().startswith("[blocker] task_decision")
        # The job summary follows the block, never precedes it.
        assert any(line.startswith("Job ") for line in out)
        assert out.index(f"Job {job.id}") > 0

    def test_the_exact_answer_command_is_in_the_output(self, capsys):
        job, record = saved_job_with_open_decision()
        expected = task_decision_answer_command(
            str(job.id), record["decision_id"], "postgres")

        _cmd_job_status(str(job.id))
        out = capsys.readouterr().out

        assert expected in out

    def test_awaiting_decision_is_the_first_blocker(self, capsys):
        job, _ = saved_job_with_open_decision()

        _cmd_job_status(str(job.id), json_output=True)
        status = json.loads(capsys.readouterr().out)

        assert status["blockers"][0] == "awaiting_decision"

    def test_the_json_carries_the_open_decisions_and_the_count(self, capsys):
        job, record = saved_job_with_open_decision()

        _cmd_job_status(str(job.id), json_output=True)
        status = json.loads(capsys.readouterr().out)

        assert status["open_decision_count"] == 1
        assert status["open_decisions"][0]["id"] == record["decision_id"]
        assert status["open_decisions"][0]["payload"]["question"] == "Which database?"

    def test_the_next_safe_action_answers_the_decision(self, capsys):
        job, record = saved_job_with_open_decision()

        _cmd_job_status(str(job.id), json_output=True)
        status = json.loads(capsys.readouterr().out)

        assert status["next_safe_action"] == task_decision_answer_command(
            str(job.id), record["decision_id"], "postgres")

    def test_a_job_without_open_decisions_is_unchanged(self, capsys):
        job = make_job(state=RunState.PLANNED)
        save_job(job)

        _cmd_job_status(str(job.id))
        out = capsys.readouterr().out.splitlines()

        assert out[0] == f"Job {job.id}"
        assert "Open decisions" not in capsys.readouterr().out

    def test_an_answered_decision_disappears_from_the_view(self, capsys):
        job, record = saved_job_with_open_decision()
        answer_task_decision(job, record["decision_id"], answer="postgres", now=T0)
        save_job(job)

        _cmd_job_status(str(job.id), json_output=True)
        status = json.loads(capsys.readouterr().out)

        assert status["open_decision_count"] == 0
        assert "awaiting_decision" not in status["blockers"]


# ---------------------------------------------------------------------------
# remedy job report
# ---------------------------------------------------------------------------


class TestJobReportView:
    def test_the_open_decision_block_is_printed_first(self, capsys):
        job, _ = saved_job_with_open_decision()

        _cmd_job_report(str(job.id))
        out = capsys.readouterr().out.splitlines()

        assert out[0] == "Open decisions: 1 — the run needs an answer"
        assert out.index(f"Job Report: {job.id}") > 0

    def test_the_final_next_action_line_names_the_answer_command(self, capsys):
        job, record = saved_job_with_open_decision()
        expected = task_decision_answer_command(
            str(job.id), record["decision_id"], "postgres")

        _cmd_job_report(str(job.id))
        out = [line for line in capsys.readouterr().out.splitlines() if line.strip()]

        assert out[-1].strip() == f"Next:      {expected}"

    def test_the_json_report_carries_the_open_decisions(self, capsys):
        job, record = saved_job_with_open_decision()

        _cmd_job_report(str(job.id), json_output=True)
        report = json.loads(capsys.readouterr().out)

        assert report["open_decision_count"] == 1
        assert report["open_decisions"][0]["id"] == record["decision_id"]
        assert report["next_safe_action"] == task_decision_answer_command(
            str(job.id), record["decision_id"], "postgres")

    def test_two_tasks_asking_the_same_question_are_both_listed(self, capsys):
        job = make_job()
        first = enqueue_task_decision(
            job, task_id=job.tasks[0].id, question="Which database?",
            options=("postgres",), now=T0)
        second = enqueue_task_decision(
            job, task_id=job.tasks[1].id, question="Which database?",
            options=("postgres",), now=T0)
        save_job(job)

        _cmd_job_report(str(job.id), json_output=True)
        report = json.loads(capsys.readouterr().out)

        listed = [d["id"] for d in report["open_decisions"]]
        assert listed == [first["decision_id"], second["decision_id"]]
        # Cross-referenced, not merged — deduplication is a human call.
        assert report["open_decisions"][0]["payload"]["cross_references"] == [
            second["decision_id"]]

    def test_a_job_without_open_decisions_reports_as_before(self, capsys):
        job = make_job(state=RunState.PLANNED)
        save_job(job)

        _cmd_job_report(str(job.id))
        out = capsys.readouterr().out.splitlines()

        assert out[0] == f"Job Report: {job.id}"


# ---------------------------------------------------------------------------
# The queue is the one surface
# ---------------------------------------------------------------------------


def test_the_view_reads_the_existing_decision_queue():
    # No second queue: what the views render is exactly what
    # ``remedy decision list`` derives for the same job.
    job, record = saved_job_with_open_decision()
    derived = [d.id for d in open_decisions(list_decisions(job, []))]

    assert record["decision_id"] in derived


def test_the_block_is_queue_wide_not_task_decision_only(capsys):
    # A job with no repo attached has an open blocker of a different type; it
    # renders first too.  The view surfaces the QUEUE, not one producer.
    job = make_job(target_repo="")
    save_job(job)

    _cmd_job_status(str(job.id), json_output=True)
    status = json.loads(capsys.readouterr().out)

    assert status["open_decision_count"] == 1
    assert status["open_decisions"][0]["type"] == "stop_reason"
    assert status["blockers"][0] == "awaiting_decision"
    assert status["next_safe_action"] == "remedy job attach-repo <job_id> <path>"
