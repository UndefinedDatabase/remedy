"""F051 — escalate instead of block.

T001: the ``needs_decision`` records themselves — enqueue, cross-referencing,
awaiting-branch derivation, answering, attended-vs-unattended default handling,
the mid-run assumption log, and the additive ``decision_queue`` derivation that
surfaces them.  That section is pure: no clock of its own (the clock is
injected), no filesystem except the assumption-log test, no provider.

T002: the same behavior through the real conductor — the three-branch fixture
that is this feature's acceptance heart, the batch-boundary pickup with its
check count (the no-polling proof), the blocked terminal, answer-and-resume,
and the linear-plan regression.  Nothing here sleeps.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from packages.core.models import Job, RunState, Task
from packages.orchestration.decision_queue import (
    DECISION_TYPES,
    export_decision_json,
    list_decisions,
)
from packages.orchestration.escalation import (
    ANSWER_SOURCE_DEFAULT,
    ANSWER_SOURCE_HUMAN,
    DECISION_ID_PREFIX,
    DECISION_TYPE_TASK_DECISION,
    ESCALATION_STATUS_ANSWERED,
    ESCALATION_STATUS_OPEN,
    JOB_METADATA_ESCALATIONS_KEY,
    TASK_INPUTS_ANSWERS_KEY,
    TASK_OUTCOME_NEEDS_DECISION,
    answer_task_decision,
    answered_task_decisions,
    auto_apply_safe_default,
    awaiting_decision_task_ids,
    enqueue_task_decision,
    escalation_records,
    find_task_decision,
    open_task_decisions,
    render_escalation_assumptions_md,
    task_decision_answer_command,
    write_escalation_assumptions_md,
)

UTC = timezone.utc
T0 = datetime(2026, 7, 30, 12, 0, 0, tzinfo=UTC)
T1 = datetime(2026, 7, 30, 12, 5, 0, tzinfo=UTC)


# ---------------------------------------------------------------------------
# Fixture builders
# ---------------------------------------------------------------------------


def make_job(task_count: int = 2, *, name: str = "escalation-job") -> Job:
    return Job(
        name=name,
        user_prompt="build the thing",
        tasks=[Task(description=f"task {i}", inputs={"task_type": "documentation"})
               for i in range(task_count)],
        state=RunState.PLANNED,
    )


def escalate(job: Job, task_index: int = 0, *, question: str = "Which database?",
             options=("postgres", "sqlite"), safe_default: str = "",
             now: datetime = T0) -> dict:
    return enqueue_task_decision(
        job,
        task_id=job.tasks[task_index].id,
        question=question,
        options=options,
        safe_default=safe_default,
        now=now,
    )


# ---------------------------------------------------------------------------
# The record and its id
# ---------------------------------------------------------------------------


class TestEnqueue:
    def test_one_call_enqueues_exactly_one_record(self):
        job = make_job()
        record = escalate(job)

        assert escalation_records(job) == [record]
        assert job.metadata[JOB_METADATA_ESCALATIONS_KEY] == [record]

    def test_the_record_carries_task_question_options_and_default(self):
        job = make_job()
        record = escalate(job, safe_default="sqlite")

        assert record["task_id"] == str(job.tasks[0].id)
        assert record["question"] == "Which database?"
        assert record["options"] == ["postgres", "sqlite"]
        assert record["safe_default"] == "sqlite"
        assert record["status"] == ESCALATION_STATUS_OPEN
        assert record["created_at"] == T0.isoformat()
        assert record["answer"] == "" and record["answered_at"] == ""

    def test_the_decision_id_is_task_scoped_and_prefixed(self):
        job = make_job()
        record = escalate(job)

        assert record["decision_id"].startswith(DECISION_ID_PREFIX)
        assert job.tasks[0].id.hex[:8] in record["decision_id"]

    def test_a_second_decision_for_the_same_task_gets_its_own_id(self):
        job = make_job()
        first = escalate(job, question="Which database?")
        second = escalate(job, question="Which cache?")

        assert first["decision_id"] != second["decision_id"]
        assert second["decision_id"].endswith("-2")
        assert len(escalation_records(job)) == 2

    def test_the_record_is_json_safe(self):
        # It rides job.metadata, which is persisted as JSON.
        import json
        job = make_job()
        escalate(job, safe_default="sqlite")
        assert json.loads(json.dumps(escalation_records(job)))


class TestSameQuestionTwice:
    """Two tasks, one question: two decisions, cross-referenced — never merged."""

    def test_two_tasks_raising_the_same_question_get_two_decisions(self):
        job = make_job()
        first = escalate(job, 0, question="Which database?")
        second = escalate(job, 1, question="Which database?")

        assert len(escalation_records(job)) == 2
        assert first["decision_id"] != second["decision_id"]

    def test_they_cross_reference_each_other_in_both_directions(self):
        job = make_job()
        first = escalate(job, 0, question="Which database?")
        second = escalate(job, 1, question="Which database?")

        assert second["cross_references"] == [first["decision_id"]]
        assert first["cross_references"] == [second["decision_id"]]

    def test_cross_referencing_ignores_whitespace_and_case(self):
        job = make_job()
        first = escalate(job, 0, question="Which  database?")
        second = escalate(job, 1, question="which database?")

        assert second["cross_references"] == [first["decision_id"]]

    def test_a_different_question_is_not_cross_referenced(self):
        job = make_job()
        escalate(job, 0, question="Which database?")
        second = escalate(job, 1, question="Which cache?")

        assert second["cross_references"] == []

    def test_an_answered_decision_is_not_cross_referenced(self):
        job = make_job()
        first = escalate(job, 0, question="Which database?")
        answer_task_decision(job, first["decision_id"], answer="postgres", now=T1)
        second = escalate(job, 1, question="Which database?")

        assert second["cross_references"] == []


# ---------------------------------------------------------------------------
# Awaiting is not failure
# ---------------------------------------------------------------------------


class TestAwaitingBranch:
    def test_an_open_decision_marks_its_task_awaiting(self):
        job = make_job()
        escalate(job, 0)

        assert awaiting_decision_task_ids(job) == {job.tasks[0].id}

    def test_the_task_keeps_its_pending_status(self):
        # Awaiting is NOT failed: no FAILED task state, so the job stays
        # resumable and the DAG treats the branch exactly like a blocked one.
        job = make_job()
        escalate(job, 0)

        assert job.tasks[0].status == RunState.PENDING

    def test_answering_clears_the_awaiting_mark(self):
        job = make_job()
        record = escalate(job, 0)
        answer_task_decision(job, record["decision_id"], answer="postgres", now=T1)

        assert awaiting_decision_task_ids(job) == set()

    def test_a_job_without_escalations_awaits_nothing(self):
        job = make_job()

        assert awaiting_decision_task_ids(job) == set()
        assert escalation_records(job) == []
        assert open_task_decisions(job) == []

    def test_a_malformed_task_id_blocks_nothing(self):
        job = make_job()
        job.metadata[JOB_METADATA_ESCALATIONS_KEY] = [
            {"decision_id": "td:bogus", "task_id": "not-a-uuid",
             "status": ESCALATION_STATUS_OPEN},
        ]

        assert awaiting_decision_task_ids(job) == set()


# ---------------------------------------------------------------------------
# Answering
# ---------------------------------------------------------------------------


class TestAnswering:
    def test_answering_records_answer_source_and_time(self):
        job = make_job()
        record = escalate(job, 0)
        updated = answer_task_decision(
            job, record["decision_id"], answer="postgres", now=T1)

        assert updated is not None
        assert updated["status"] == ESCALATION_STATUS_ANSWERED
        assert updated["answer"] == "postgres"
        assert updated["answer_source"] == ANSWER_SOURCE_HUMAN
        assert updated["answered_at"] == T1.isoformat()
        assert answered_task_decisions(job) == [updated]

    def test_the_answer_lands_on_the_task_for_its_next_attempt(self):
        job = make_job()
        record = escalate(job, 0)
        answer_task_decision(job, record["decision_id"], answer="postgres", now=T1)

        assert job.tasks[0].inputs[TASK_INPUTS_ANSWERS_KEY] == {
            record["decision_id"]: "postgres"}

    def test_answering_an_unknown_decision_returns_none(self):
        job = make_job()
        escalate(job, 0)

        assert answer_task_decision(job, "td:nope", answer="x", now=T1) is None

    def test_answering_twice_is_refused(self):
        # Answers are written once: a late second answer must not overwrite the
        # one the run already acted on.
        job = make_job()
        record = escalate(job, 0)
        answer_task_decision(job, record["decision_id"], answer="postgres", now=T1)
        again = answer_task_decision(
            job, record["decision_id"], answer="sqlite", now=T1)

        assert again is None
        assert find_task_decision(job, record["decision_id"])["answer"] == "postgres"


class TestSafeDefaults:
    def test_a_safe_default_is_still_asked_and_stays_open(self):
        # A9 consistency: enqueueing never applies the default by itself.
        job = make_job()
        record = escalate(job, 0, safe_default="sqlite")

        assert record["status"] == ESCALATION_STATUS_OPEN
        assert record["answer"] == ""
        assert awaiting_decision_task_ids(job) == {job.tasks[0].id}

    def test_auto_apply_answers_from_the_default_and_says_so(self):
        job = make_job()
        record = escalate(job, 0, safe_default="sqlite")
        applied = auto_apply_safe_default(job, record, now=T1)

        assert applied is not None
        assert applied["answer"] == "sqlite"
        assert applied["answer_source"] == ANSWER_SOURCE_DEFAULT
        assert awaiting_decision_task_ids(job) == set()

    def test_auto_apply_refuses_a_record_without_a_default(self):
        job = make_job()
        record = escalate(job, 0, safe_default="")

        assert auto_apply_safe_default(job, record, now=T1) is None
        assert open_task_decisions(job) == [record]


# ---------------------------------------------------------------------------
# The assumption log
# ---------------------------------------------------------------------------


class TestEscalationAssumptionLog:
    def test_it_records_answer_and_source_per_decision(self):
        job = make_job()
        human = escalate(job, 0, question="Which database?")
        answer_task_decision(job, human["decision_id"], answer="postgres", now=T1)
        defaulted = escalate(job, 1, question="Which cache?", safe_default="none")
        auto_apply_safe_default(job, defaulted, now=T1)

        text = render_escalation_assumptions_md(job)

        assert "Which database?" in text and "postgres" in text
        assert "Which cache?" in text and "none" in text
        assert "Sources: 1 human, 1 default, 0 unresolved." in text

    def test_an_open_decision_is_reported_unresolved(self):
        job = make_job()
        escalate(job, 0)

        text = render_escalation_assumptions_md(job)

        assert "unanswered" in text
        assert "Sources: 0 human, 0 default, 1 unresolved." in text

    def test_a_run_without_escalations_says_so(self):
        text = render_escalation_assumptions_md(make_job())

        assert "No escalations" in text

    def test_it_is_written_next_to_the_other_job_evidence(self, tmp_path: Path):
        job = make_job()
        escalate(job, 0)
        path = write_escalation_assumptions_md(job, tmp_path / "evidence")

        assert path.name == "escalation_assumptions.md"
        assert "Which database?" in path.read_text(encoding="utf-8")

    def test_it_is_not_the_flight_plan_assumption_log(self, tmp_path: Path):
        # The plan-time log states nothing in it was asked mid-run; mid-run
        # escalations therefore get their own file rather than making it lie.
        from packages.orchestration.flight_plan import write_assumptions_md
        job = make_job()
        escalate(job, 0)
        evidence = tmp_path / "evidence"
        plan_log = write_assumptions_md([], evidence)
        escalation_log = write_escalation_assumptions_md(job, evidence)

        assert plan_log != escalation_log
        assert "Which database?" not in plan_log.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# The decision queue derives them — no second queue
# ---------------------------------------------------------------------------


class TestDecisionQueueDerivation:
    def test_the_type_is_registered(self):
        assert DECISION_TYPE_TASK_DECISION in DECISION_TYPES

    def test_an_open_escalation_appears_as_an_open_blocker(self):
        job = make_job()
        record = escalate(job, 0)

        derived = [d for d in list_decisions(job, [])
                   if d.type == DECISION_TYPE_TASK_DECISION]

        assert len(derived) == 1
        assert derived[0].id == record["decision_id"]
        assert derived[0].status == "open"
        assert derived[0].severity == "blocker"
        assert "Which database?" in derived[0].safe_summary

    def test_it_carries_the_exact_answer_command_per_option(self):
        job = make_job()
        record = escalate(job, 0, options=("postgres", "sqlite"))

        d = next(d for d in list_decisions(job, [])
                 if d.type == DECISION_TYPE_TASK_DECISION)

        assert d.next_actions == (
            task_decision_answer_command(str(job.id), record["decision_id"], "postgres"),
            task_decision_answer_command(str(job.id), record["decision_id"], "sqlite"),
        )
        assert all(a.startswith("remedy decision resolve ") for a in d.next_actions)

    def test_a_decision_without_options_still_offers_the_command(self):
        job = make_job()
        record = escalate(job, 0, options=())

        d = next(d for d in list_decisions(job, [])
                 if d.type == DECISION_TYPE_TASK_DECISION)

        assert d.next_actions == (
            task_decision_answer_command(str(job.id), record["decision_id"]),)

    def test_the_payload_carries_question_options_default_and_refs(self):
        job = make_job()
        first = escalate(job, 0, question="Which database?", safe_default="sqlite")
        escalate(job, 1, question="Which database?")

        d = next(d for d in list_decisions(job, [])
                 if d.id == first["decision_id"])

        assert d.payload["question"] == "Which database?"
        assert d.payload["options"] == ["postgres", "sqlite"]
        assert d.payload["safe_default"] == "sqlite"
        assert d.payload["task_id"] == str(job.tasks[0].id)
        assert len(d.payload["cross_references"]) == 1

    def test_an_answered_escalation_is_resolved_not_open(self):
        job = make_job()
        record = escalate(job, 0)
        answer_task_decision(job, record["decision_id"], answer="postgres", now=T1)

        d = next(d for d in list_decisions(job, [])
                 if d.type == DECISION_TYPE_TASK_DECISION)

        assert d.status == "resolved"
        assert d.severity == "info"
        assert d.next_actions == ()
        assert "postgres" in d.safe_summary

    def test_it_exports_as_safe_json(self):
        job = make_job()
        escalate(job, 0)

        d = next(d for d in list_decisions(job, [])
                 if d.type == DECISION_TYPE_TASK_DECISION)
        exported = export_decision_json(d)

        assert exported["type"] == DECISION_TYPE_TASK_DECISION
        assert exported["payload"]["question"] == "Which database?"

    def test_a_job_without_escalations_derives_none(self):
        job = make_job()

        assert [d for d in list_decisions(job, [])
                if d.type == DECISION_TYPE_TASK_DECISION] == []


def test_the_outcome_name_is_the_one_the_feature_specifies():
    assert TASK_OUTCOME_NEEDS_DECISION == "needs_decision"


# ---------------------------------------------------------------------------
# T002 — the same behavior through the real conductor
# ---------------------------------------------------------------------------

from packages.orchestration.builder_models import (  # noqa: E402 — section-local
    BuilderOutput,
    TaskExecutionContext,
)
from packages.orchestration.long_run_executor import (  # noqa: E402
    LEDGER_EVENT_TASK_NEEDS_DECISION,
    TERMINAL_ALL_GREEN,
    TERMINAL_BLOCKED,
    VERIFY_PASSED,
    CycleLimits,
    TaskAttempt,
    awaiting_downstream_tasks,
    ready_tasks,
    run_cycles,
)
from packages.orchestration.pingpong_job import JOB_BLOCKED  # noqa: E402


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path: Path, monkeypatch) -> Path:
    """Autouse: a cycle writes evidence and a checkpoint, so no test here may
    ever reach the repository's real data root."""
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


@pytest.fixture
def control_root(tmp_path: Path) -> Path:
    root = tmp_path / "control"
    root.mkdir()
    return root


class FakeClock:
    """A clock that advances only when it is read — the loop never sleeps."""

    def __init__(self, start: datetime = T0,
                 step: timedelta = timedelta(seconds=1)) -> None:
        self.now = start
        self.step = step

    def __call__(self) -> datetime:
        current = self.now
        self.now = self.now + self.step
        return current


class FakeProvider:
    def __init__(self) -> None:
        self.calls = 0

    def __call__(self, context: TaskExecutionContext) -> BuilderOutput:
        self.calls += 1
        return BuilderOutput(summary=f"did {context.task_description}",
                            proposed_changes=["change"])


class RecordingLog:
    def __init__(self) -> None:
        self.events: list[tuple[str, dict]] = []

    def log(self, event: str, **meta) -> None:
        self.events.append((event, meta))


def passing_verify(job: Job, cycle_index: int, verify_command) -> str:
    return VERIFY_PASSED


def no_save(job: Job) -> None:
    return None


def make_fanout_job(name: str = "fanout-job") -> Job:
    """R -> (B1a -> B1b, B2, B3): one root, three branches, one with downstream.

    Branch 1 is the one that will raise a question, and B1b exists precisely so
    the fixture can prove that a paused branch pauses its OWN downstream and
    nothing else.  Plan order puts branch 1 first, so a scheduler that just took
    the first PENDING task would stall on it.
    """
    def task(planned_id: str, *depends_on: str) -> Task:
        return Task(
            description=f"task {planned_id}",
            inputs={"task_type": "documentation",
                    "flight": {"planned_id": planned_id, "title": planned_id,
                               "depends_on": list(depends_on)}},
        )

    return Job(
        name=name,
        user_prompt="build the thing",
        tasks=[task("R"), task("B1a", "R"), task("B1b", "B1a"),
               task("B2", "R"), task("B3", "R")],
        state=RunState.PLANNED,
    )


def planned_id_of(job: Job, task_id) -> str:
    for task in job.tasks:
        if str(task.id) == str(task_id):
            return task.inputs["flight"]["planned_id"]
    raise AssertionError(f"no task {task_id} in this job")


def task_by_planned_id(job: Job, planned_id: str) -> Task:
    for task in job.tasks:
        if task.inputs.get("flight", {}).get("planned_id") == planned_id:
            return task
    raise AssertionError(f"no task {planned_id} in this job")


class EscalatingStep:
    """Runs the task the ready set selected; named ones raise needs_decision.

    A task escalates only the FIRST time it is selected — after an answer it
    proceeds, which is what makes answer-and-continue observable.  ``on_execute``
    is a hook the pickup test uses to answer a decision mid-run.
    """

    def __init__(self, *escalate_planned_ids: str, safe_default: str = "",
                 on_execute=None) -> None:
        self.escalate = set(escalate_planned_ids)
        self.safe_default = safe_default
        self.on_execute = on_execute
        self.executed: list[str] = []
        self.escalated: list[str] = []

    def __call__(self, job: Job, provider_call, task_id=None) -> TaskAttempt:
        task = (next((t for t in job.tasks if t.id == task_id), None)
                if task_id is not None
                else next((t for t in job.tasks
                           if t.status == RunState.PENDING), None))
        if task is None:
            return TaskAttempt()

        planned_id = task.inputs["flight"]["planned_id"]
        if planned_id in self.escalate:
            self.escalate.discard(planned_id)     # asked once
            self.escalated.append(planned_id)
            return TaskAttempt(
                task_id=task.id,
                needs_decision=True,
                question=f"How should {planned_id} proceed?",
                options=("fast", "safe"),
                safe_default=self.safe_default,
            )

        provider_call(TaskExecutionContext(
            job_id=job.id, job_prompt=job.user_prompt, task_id=task.id,
            task_type=task.inputs.get("task_type", "unknown"),
            task_description=task.description))
        self.executed.append(planned_id)
        task.status = RunState.COMPLETED
        if all(t.status == RunState.COMPLETED for t in job.tasks):
            job.state = RunState.COMPLETED
        if self.on_execute is not None:
            self.on_execute(job, planned_id)
        return TaskAttempt(task_id=task.id, executed=True, verified=True)


def run_fanout(control_root: Path, step: EscalatingStep, *,
               batch_size: int = 1, max_cycles: int = 10,
               unattended: bool = False, job: Job | None = None,
               log=None):
    job = job if job is not None else make_fanout_job()
    result = run_cycles(
        job, CycleLimits(max_cycles=max_cycles, batch_size=batch_size),
        FakeProvider(), task_step=step, verify=passing_verify,
        clock=FakeClock(), save=no_save, control_root_path=control_root,
        unattended=unattended, log=log,
    )
    return job, result


# ---------------------------------------------------------------------------
# The three-branch fixture — this feature's acceptance heart
# ---------------------------------------------------------------------------


class TestThreeBranchFixture:
    def test_the_free_branches_complete_while_branch_one_waits(self, control_root):
        job, result = run_fanout(control_root, EscalatingStep("B1a"))

        assert result.terminal_status == TERMINAL_BLOCKED
        assert result.job_status == JOB_BLOCKED
        # Root first, then the question, then both free branches — in plan order.
        assert step_order(job, result) == ["R", "B2", "B3"]
        assert task_by_planned_id(job, "B2").status == RunState.COMPLETED
        assert task_by_planned_id(job, "B3").status == RunState.COMPLETED

    def test_the_paused_branch_pauses_only_its_own_downstream(self, control_root):
        job, result = run_fanout(control_root, EscalatingStep("B1a"))

        assert task_by_planned_id(job, "B1a").status == RunState.PENDING
        assert task_by_planned_id(job, "B1b").status == RunState.PENDING
        assert awaiting_downstream_tasks(job, awaiting_decision_task_ids(job)) == [
            task_by_planned_id(job, "B1b").id]

    def test_exactly_one_open_decision_is_listed(self, control_root):
        job, result = run_fanout(control_root, EscalatingStep("B1a"))

        assert len(open_task_decisions(job)) == 1
        assert result.open_decision_ids == (
            open_task_decisions(job)[0]["decision_id"],)
        assert "awaiting_decision" in result.stop_reason
        assert result.open_decision_ids[0] in result.stop_reason

    def test_the_run_is_paused_not_failed(self, control_root):
        # Nothing failed: the job must stay resumable, and no cycle may report
        # the escalation as a failure.
        job, result = run_fanout(control_root, EscalatingStep("B1a"))

        assert job.state == RunState.PAUSED
        assert sum(c.tasks_failed for c in result.cycles) == 0
        assert sum(c.tasks_escalated for c in result.cycles) == 1

    def test_answering_and_resuming_completes_the_remainder(self, control_root):
        step = EscalatingStep("B1a")
        job, first = run_fanout(control_root, step)
        decision_id = first.open_decision_ids[0]

        answer_task_decision(job, decision_id, answer="fast", now=T1)
        resumed_step = EscalatingStep()          # nothing escalates any more
        job, second = run_fanout(control_root, resumed_step, job=job)

        assert second.terminal_status == TERMINAL_ALL_GREEN
        assert resumed_step.executed == ["B1a", "B1b"]
        assert all(t.status == RunState.COMPLETED for t in job.tasks)
        assert open_task_decisions(job) == []

    def test_answering_through_the_existing_decision_cli_completes_the_rest(
            self, control_root, capsys):
        # The acceptance path exactly as a human walks it: the command the
        # status view printed, then a resume.  No new CLI, no new queue.
        from apps.cli.commands.decision import _cmd_decision_resolve
        from packages.orchestration.storage import load_job, save_job

        step = EscalatingStep("B1a")
        job, first = run_fanout(control_root, step)
        save_job(job)
        decision_id = first.open_decision_ids[0]

        _cmd_decision_resolve(str(job.id), decision_id, reason="fast")
        out = capsys.readouterr().out

        assert f"Answered {decision_id}" in out and "fast" in out
        reloaded = load_job(job.id)
        assert open_task_decisions(reloaded) == []
        assert answered_task_decisions(reloaded)[0]["answer"] == "fast"
        assert answered_task_decisions(reloaded)[0]["answer_source"] == (
            ANSWER_SOURCE_HUMAN)

        resumed_step = EscalatingStep()
        reloaded, second = run_fanout(control_root, resumed_step, job=reloaded)

        assert second.terminal_status == TERMINAL_ALL_GREEN
        assert resumed_step.executed == ["B1a", "B1b"]

    def test_the_cli_refuses_to_overwrite_an_answer(self, control_root, capsys):
        from apps.cli.commands.decision import _cmd_decision_resolve
        from packages.orchestration.storage import save_job

        step = EscalatingStep("B1a")
        job, first = run_fanout(control_root, step)
        save_job(job)
        decision_id = first.open_decision_ids[0]

        _cmd_decision_resolve(str(job.id), decision_id, reason="fast")
        capsys.readouterr()
        with pytest.raises(SystemExit) as exit_info:
            _cmd_decision_resolve(str(job.id), decision_id, reason="safe")

        assert exit_info.value.code == 1
        assert "already answered" in capsys.readouterr().err

    def test_the_cli_refuses_an_empty_answer_without_a_default(
            self, control_root, capsys):
        from apps.cli.commands.decision import _cmd_decision_resolve
        from packages.orchestration.storage import save_job

        step = EscalatingStep("B1a", safe_default="")
        job, first = run_fanout(control_root, step)
        save_job(job)

        with pytest.raises(SystemExit) as exit_info:
            _cmd_decision_resolve(str(job.id), first.open_decision_ids[0], reason="")

        assert exit_info.value.code == 1
        assert "--reason carries the answer" in capsys.readouterr().err

    def test_the_answer_reaches_the_task_that_asked(self, control_root):
        step = EscalatingStep("B1a")
        job, first = run_fanout(control_root, step)
        answer_task_decision(job, first.open_decision_ids[0], answer="fast", now=T1)

        assert task_by_planned_id(job, "B1a").inputs[TASK_INPUTS_ANSWERS_KEY] == {
            first.open_decision_ids[0]: "fast"}

    def test_the_cycle_evidence_names_the_awaiting_branch(self, control_root):
        job, result = run_fanout(control_root, EscalatingStep("B1a"))
        awaiting_task = task_by_planned_id(job, "B1a")

        # From the cycle that raised it onwards, every record names the branch.
        naming = [c for c in result.cycles
                  if str(awaiting_task.id) in c.awaiting_task_ids]
        assert naming, "no cycle record named the awaiting task"
        assert str(task_by_planned_id(job, "B1b").id) in (
            naming[-1].awaiting_downstream_task_ids)
        raised = [c for c in result.cycles if c.open_decision_ids]
        assert len(raised) == 1
        assert raised[0].tasks_escalated == 1
        assert raised[0].to_json()["open_decision_ids"] == list(
            raised[0].open_decision_ids)

    def test_the_escalation_is_emitted_to_the_ledger(self, control_root):
        log = RecordingLog()
        job, result = run_fanout(control_root, EscalatingStep("B1a"), log=log)

        raised = [meta for event, meta in log.events
                  if event == LEDGER_EVENT_TASK_NEEDS_DECISION]
        assert len(raised) == 1
        assert raised[0]["decision_id"] == result.open_decision_ids[0]
        assert raised[0]["question"] == "How should B1a proceed?"


def step_order(job: Job, result) -> list[str]:
    """Planned ids this run executed, in execution order, from the records."""
    return [planned_id_of(job, task_id)
            for cycle in result.cycles for task_id in cycle.executed_task_ids]


# ---------------------------------------------------------------------------
# Continuation and batch-boundary pickup
# ---------------------------------------------------------------------------


class TestContinuationAndPickup:
    def test_disjoint_branches_run_in_the_same_cycle_as_the_question(self, control_root):
        # batch_size 3: the escalation must not consume the cycle.
        job, result = run_fanout(control_root, EscalatingStep("B1a"), batch_size=3)

        first_working_cycle = next(c for c in result.cycles if c.open_decision_ids)
        assert len(first_working_cycle.executed_task_ids) >= 1
        assert step_order(job, result) == ["R", "B2", "B3"]

    def test_a_decision_answered_mid_run_is_picked_up_without_a_restart(self, control_root):
        # B2's execution answers B1a's decision. No restart, no resume: the very
        # next batch boundary of THIS run must release branch 1.
        answered: list[str] = []

        def answer_when_b2_runs(job: Job, planned_id: str) -> None:
            if planned_id != "B2" or answered:
                return
            open_now = open_task_decisions(job)
            if open_now:
                answer_task_decision(job, open_now[0]["decision_id"],
                                     answer="fast", now=T1)
                answered.append(open_now[0]["decision_id"])

        step = EscalatingStep("B1a", on_execute=answer_when_b2_runs)
        job, result = run_fanout(control_root, step)

        assert answered, "the fixture never answered the decision"
        assert result.terminal_status == TERMINAL_ALL_GREEN
        # Released at the boundary right after B2, so branch 1 resumes ahead of
        # B3 — plan order, exactly as if it had never paused.
        assert step.executed == ["R", "B2", "B1a", "B1b", "B3"]
        assert all(t.status == RunState.COMPLETED for t in job.tasks)
        assert open_task_decisions(job) == []

    def test_the_awaiting_check_runs_exactly_once_per_batch_boundary(self, control_root):
        # The no-polling proof: one check per boundary, and the loop has exactly
        # one boundary more than the cycles it ran (the last one finds nothing).
        job, result = run_fanout(control_root, EscalatingStep("B1a"))

        assert result.awaiting_checks == result.cycles_run + 1
        assert result.to_json()["awaiting_checks"] == result.awaiting_checks

    def test_the_check_count_does_not_grow_while_a_branch_waits(self, control_root):
        # A polling implementation would spin extra checks for the waiting
        # branch; this asserts the exact number for a known topology.
        job, result = run_fanout(control_root, EscalatingStep("B1a"))

        # R, the escalation, B2, B3 — four cycles, five boundaries.
        assert result.cycles_run == 4
        assert result.awaiting_checks == 5

    def test_an_awaiting_task_is_withheld_from_the_ready_set(self, control_root):
        job, result = run_fanout(control_root, EscalatingStep("B1a"))
        awaiting = awaiting_decision_task_ids(job)

        assert ready_tasks(job, 10, awaiting_ids=awaiting) == []
        # And the moment it is answered, the branch is ready again.
        answer_task_decision(job, result.open_decision_ids[0], answer="fast", now=T1)
        assert ready_tasks(job, 10, awaiting_ids=awaiting_decision_task_ids(job)) == [
            task_by_planned_id(job, "B1a").id]

    def test_the_checkpoint_never_names_an_awaiting_task_as_the_next_intent(
            self, control_root, isolate_data_root):
        from packages.orchestration.checkpoints import (
            INTENT_NONE,
            checkpoint_paths,
            load_latest_valid,
            read_checkpoint,
        )

        step = EscalatingStep("B1a")
        job = make_fanout_job()
        result = run_cycles(
            job, CycleLimits(max_cycles=10, batch_size=1), FakeProvider(),
            task_step=step, verify=passing_verify, clock=FakeClock(),
            save=no_save, control_root_path=control_root,
        )
        awaiting_task_id = str(task_by_planned_id(job, "B1a").id)
        escalating_cycle = next(c.cycle_index for c in result.cycles
                                if c.tasks_escalated)

        assert checkpoint_paths(str(job.id)), "the run wrote no checkpoint"
        # From the escalating cycle onwards, no checkpoint may point a resume at
        # the awaiting task.  Earlier ones legitimately name it: at that point
        # the question had not been raised yet.
        checked = 0
        for path in checkpoint_paths(str(job.id)):
            checkpoint = read_checkpoint(path)
            assert checkpoint is not None
            if checkpoint.cycle_index < escalating_cycle:
                continue
            checked += 1
            assert checkpoint.next_intent.get("task_id", "") != awaiting_task_id
        assert checked >= 1
        latest = load_latest_valid(str(job.id))
        assert latest is not None
        assert latest.next_intent.get("kind") == INTENT_NONE
        assert result.terminal_status == TERMINAL_BLOCKED


# ---------------------------------------------------------------------------
# Attended vs unattended, and the linear regression
# ---------------------------------------------------------------------------


class TestUnattendedDefaults:
    def test_attended_asks_even_when_a_safe_default_exists(self, control_root):
        job, result = run_fanout(
            control_root, EscalatingStep("B1a", safe_default="safe"))

        assert result.terminal_status == TERMINAL_BLOCKED
        assert len(open_task_decisions(job)) == 1
        assert open_task_decisions(job)[0]["safe_default"] == "safe"
        assert task_by_planned_id(job, "B1a").status == RunState.PENDING

    def test_unattended_applies_the_default_and_the_run_finishes(self, control_root):
        job, result = run_fanout(
            control_root, EscalatingStep("B1a", safe_default="safe"),
            unattended=True)

        assert result.terminal_status == TERMINAL_ALL_GREEN
        assert open_task_decisions(job) == []
        answered = answered_task_decisions(job)
        assert len(answered) == 1
        assert answered[0]["answer"] == "safe"
        assert answered[0]["answer_source"] == ANSWER_SOURCE_DEFAULT

    def test_unattended_still_waits_when_there_is_no_default(self, control_root):
        # Escalation exists so Remedy never invents an answer.
        job, result = run_fanout(
            control_root, EscalatingStep("B1a", safe_default=""), unattended=True)

        assert result.terminal_status == TERMINAL_BLOCKED
        assert len(open_task_decisions(job)) == 1

    def test_the_auto_applied_default_is_in_the_assumption_log(self, control_root):
        job, _ = run_fanout(
            control_root, EscalatingStep("B1a", safe_default="safe"),
            unattended=True)

        text = render_escalation_assumptions_md(job)

        assert "How should B1a proceed?" in text
        assert "Sources: 0 human, 1 default, 0 unresolved." in text


class TestLinearPlansAreUnchanged:
    def test_a_linear_plan_without_escalations_behaves_exactly_as_before(
            self, control_root):
        job = make_job(3)
        step = LinearStep()
        result = run_cycles(
            job, CycleLimits(max_cycles=10, batch_size=1), FakeProvider(),
            task_step=step, verify=passing_verify, clock=FakeClock(),
            save=no_save, control_root_path=control_root,
        )

        assert result.terminal_status == TERMINAL_ALL_GREEN
        assert len(step.executed) == 3
        assert result.open_decision_ids == ()
        assert escalation_records(job) == []
        assert all(c.tasks_escalated == 0 for c in result.cycles)

    def test_a_step_that_never_heard_of_escalation_is_untouched(self, control_root):
        # TaskAttempt's new fields default to "no decision needed", so a step
        # written before F051 cannot accidentally escalate.
        attempt = TaskAttempt()

        assert attempt.needs_decision is False
        assert attempt.question == "" and attempt.options == ()
        assert attempt.safe_default == ""


class TestUnattendedRunLoopCliFlag:
    """R-0157: the unattended mode must be reachable from the product surface.

    ``run_cycles(unattended=…)`` existed with no CLI call site passing it, so the
    A9 rule ("defaults auto-apply only under --yes/unattended") was unreachable.
    These drive the real ``remedy job run`` handler.
    """

    @pytest.fixture
    def cli_job(self, monkeypatch):
        """A saved 2-task job with the cycle loop reachable and a fake builder."""
        import packages.orchestration.long_run_executor as lre
        from packages.orchestration.storage import save_job
        from packages.providers.ollama_builder import provider as provider_mod

        class FakeBuilder:
            model = "fake-model"

            def build(self, context: TaskExecutionContext) -> BuilderOutput:
                return BuilderOutput(summary="did it", proposed_changes=["change"])

        # The F046 rollout cap collapses every run to the single pass; the loop
        # itself is what F051 hangs off, so the cap is lifted for these tests
        # exactly as the existing job.run multi-cycle test does.
        monkeypatch.setattr(lre, "CYCLE_SAFETY_CAP", 5)
        monkeypatch.setattr(provider_mod, "OllamaBuilder", FakeBuilder)
        monkeypatch.setattr(lre, "default_task_step",
                            EscalatingStep("T0", safe_default="safe"))

        job = Job(
            name="cli-unattended-job",
            user_prompt="build the thing",
            tasks=[Task(description=f"task {i}",
                        inputs={"task_type": "documentation",
                                "flight": {"planned_id": f"T{i}", "title": f"T{i}",
                                           "depends_on": ([f"T{i - 1}"] if i else [])}})
                   for i in range(2)],
            state=RunState.PLANNED,
        )
        save_job(job)
        return job

    def test_the_flag_auto_answers_a_safe_default_and_the_run_continues(
            self, cli_job, monkeypatch, capsys):
        from apps.cli.commands import job as job_cmd
        from packages.orchestration.storage import load_job

        job_cmd._cmd_job_run_cycles(str(cli_job.id), cycles=3, unattended=True)
        out = capsys.readouterr().out

        stored = load_job(cli_job.id)
        answered = answered_task_decisions(stored)
        assert len(answered) == 1
        assert answered[0]["answer"] == "safe"
        assert answered[0]["answer_source"] == ANSWER_SOURCE_DEFAULT
        assert open_task_decisions(stored) == []
        # The run went past the question instead of parking on it.
        assert f"terminal={TERMINAL_ALL_GREEN}" in out
        assert all(t.status == RunState.COMPLETED for t in stored.tasks)

    def test_without_the_flag_the_same_fixture_leaves_the_decision_open(
            self, cli_job, monkeypatch, capsys):
        from apps.cli.commands import job as job_cmd
        from packages.orchestration.storage import load_job

        with pytest.raises(SystemExit) as exit_info:
            job_cmd._cmd_job_run_cycles(str(cli_job.id), cycles=3)
        out = capsys.readouterr().out

        assert exit_info.value.code == 1          # blocked is a non-zero exit
        stored = load_job(cli_job.id)
        assert len(open_task_decisions(stored)) == 1
        assert open_task_decisions(stored)[0]["safe_default"] == "safe"
        assert answered_task_decisions(stored) == []
        assert f"terminal={TERMINAL_BLOCKED}" in out

    def test_the_flag_is_registered_in_the_catalog(self):
        from apps.cli.command_catalog import CATALOG

        entry = next(c for c in CATALOG if c.command_id == "job.run")
        flag = next(a for a in entry.args if a.name == "--unattended")

        assert flag.is_option and flag.is_flag and not flag.required
        assert "safe default" in flag.help
        assert "still waits" in flag.help

    def test_the_handler_passes_the_flag_through(self, monkeypatch):
        from apps.cli.command_catalog import ArgDef  # noqa: F401 — import guard
        from apps.cli.commands import job as job_cmd

        seen: dict = {}
        monkeypatch.setattr(job_cmd, "_cmd_job_run_cycles",
                            lambda job_id, **kw: seen.update(kw))

        class Args:
            job_id = "abc12345"
            cycles = None
            unattended = True
            json = False

        job_cmd.COMMAND_HANDLERS["job.run"](Args())

        assert seen["unattended"] is True

    def test_an_old_namespace_without_the_flag_still_works(self, monkeypatch):
        # argparse namespaces from before this flag existed must not crash.
        from apps.cli.commands import job as job_cmd

        seen: dict = {}
        monkeypatch.setattr(job_cmd, "_cmd_job_run_cycles",
                            lambda job_id, **kw: seen.update(kw))

        class OldArgs:
            job_id = "abc12345"
            cycles = None
            json = False

        job_cmd.COMMAND_HANDLERS["job.run"](OldArgs())

        assert seen["unattended"] is False

    def test_the_single_pass_says_the_flag_had_no_effect(self, monkeypatch, capsys):
        # Honesty over silence: with the rollout cap in place the loop never
        # runs, so the flag cannot do what its help promises.
        from apps.cli.commands import job as job_cmd

        monkeypatch.setattr(job_cmd, "_cmd_run_next_task_local", lambda _: None)
        job_cmd._cmd_job_run_cycles("abc12345", unattended=True)

        assert "--unattended has no effect" in capsys.readouterr().err

    def test_the_single_pass_is_silent_without_the_flag(self, monkeypatch, capsys):
        from apps.cli.commands import job as job_cmd

        monkeypatch.setattr(job_cmd, "_cmd_run_next_task_local", lambda _: None)
        job_cmd._cmd_job_run_cycles("abc12345")

        assert "--unattended" not in capsys.readouterr().err


class LinearStep:
    """Completes the first PENDING task — the pre-F051 step shape, no task_id."""

    def __init__(self) -> None:
        self.executed: list[str] = []

    def __call__(self, job: Job, provider_call) -> TaskAttempt:
        task = next((t for t in job.tasks if t.status == RunState.PENDING), None)
        if task is None:
            return TaskAttempt()
        provider_call(TaskExecutionContext(
            job_id=job.id, job_prompt=job.user_prompt, task_id=task.id,
            task_type="documentation", task_description=task.description))
        self.executed.append(task.description)
        task.status = RunState.COMPLETED
        if all(t.status == RunState.COMPLETED for t in job.tasks):
            job.state = RunState.COMPLETED
        return TaskAttempt(task_id=task.id, executed=True, verified=True)


class TestJobPlanCompatibility:
    """DECISION F112 D4: enqueue_task_decision/auto_apply_safe_default must
    work against a pingpong JobPlan/TaskEntry, not only Core Job/Task."""

    def test_auto_apply_safe_default_answers_and_records_on_a_job_plan_task(self):
        from packages.orchestration.pingpong_job import JobPlan, TaskEntry

        job = JobPlan(tasks=[TaskEntry(task_id="T003", title="Oversized task")])
        record = enqueue_task_decision(
            job,
            task_id=job.tasks[0].task_id,
            question="task context exceeds its class cap",
            options=["split task"],
            safe_default="split task",
            now=T0,
        )

        answered = auto_apply_safe_default(job, record, now=T1)

        assert answered is not None
        assert answered["status"] == ESCALATION_STATUS_ANSWERED
        assert answered["answer"] == "split task"
        assert answered["answer_source"] == ANSWER_SOURCE_DEFAULT
        assert (job.tasks[0].inputs[TASK_INPUTS_ANSWERS_KEY][answered["decision_id"]]
                == "split task")

    def test_answer_task_decision_matches_by_task_id_not_id(self):
        from packages.orchestration.pingpong_job import JobPlan, TaskEntry

        job = JobPlan(tasks=[
            TaskEntry(task_id="T001", title="First"),
            TaskEntry(task_id="T002", title="Second"),
        ])
        record = enqueue_task_decision(
            job, task_id="T002", question="q", safe_default="d", now=T0,
        )

        auto_apply_safe_default(job, record, now=T1)

        assert job.tasks[0].inputs == {}
        assert TASK_INPUTS_ANSWERS_KEY in job.tasks[1].inputs
