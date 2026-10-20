"""F312 R2 C4 — the question after two refusals, tested (DECISION F312 D3).

Drives `plan_order_job` with a mocked planner, exactly as
`tests/orchestration/test_do_sequence_scope_order.py` does, counting the calls of the patched
`job_plan.plan_job_llm`.
"""
from __future__ import annotations

import pytest

#: The second lab order of 2026-10-20 (R-1369): no file name, no fence — an open order.
LAB_OPEN_ORDER = "Super, jetzt mach ein schickes design"

#: The lab's README fence (amend1016p D1): a fenced order refuses at once, with no second call.
LAB_FENCED_ORDER = "Ändere nur die README. Verändere sonst nichts."


def _task(tid: str, title: str, hint: str):
    return {"id": tid, "title": title, "goal": title, "acceptance": [f"{title} is done"],
            "depends_on": [], "est_tokens_band": "S", "files_hint": [hint]}


def _checksum_plan():
    """A plan whose one task makes nothing but a checking artifact the order never asked for."""
    from packages.orchestration.schemas.models import TaskPlan

    return TaskPlan.model_validate({"schema_v": "task_plan_v1", "tasks": [
        _task("T001", "Write a checksum manifest of the site", "checksums.json")]})


def _style_plan():
    """A plan whose one task delivers `style.css`."""
    from packages.orchestration.schemas.models import TaskPlan

    return TaskPlan.model_validate({"schema_v": "task_plan_v1", "tasks": [
        _task("T001", "Add a modern colour scheme", "style.css")]})


def _mock_intake(monkeypatch):
    """The intake branch, mocked exactly as `test_do_sequence_scope_order.py` mocks it."""
    monkeypatch.setattr(
        "packages.orchestration.intake.make_provider_call_fn",
        lambda: (lambda p, a: '{"schema_v": "ji1", "goal": "g", "context_refs": [], '
                 '"constraints": [], "acceptance_hints": [], "truncated_input": false, '
                 '"clarifications": []}'))
    monkeypatch.setattr(
        "packages.orchestration.intake.make_structured_call_fn",
        lambda model_cls, **kw: (lambda p, a: ""))


def _mock_plan_calls(monkeypatch, *plans):
    """Patch `job_plan.plan_job_llm` to answer with *plans* in call order (repeating the last).

    Returns the list `plan_job_llm` appends one entry to per call, so a test can read its length.
    """
    from packages.orchestration.job_plan import TaskPlanResult

    calls: list[int] = []

    def _fake(intake, call_fn, **kw):
        calls.append(1)
        plan = plans[min(len(calls) - 1, len(plans) - 1)]
        return TaskPlanResult(plan=plan, source="llm", calls=1, transformations=[])

    monkeypatch.setattr("packages.orchestration.job_plan.plan_job_llm", _fake)
    return calls


def test_scope_question_options_takes_each_tasks_first_files_hint_once():
    from packages.orchestration.schemas.models import TaskPlan
    from packages.orchestration.scope_question import scope_question_options

    plan = TaskPlan.model_validate({"schema_v": "task_plan_v1", "tasks": [
        _task("T001", "A", " style.css "),
        _task("T002", "B", "style.css"),
        _task("T003", "C", ""),
        _task("T004", "D", "index.html")]})

    assert scope_question_options(plan) == ["style.css", "index.html"]


def test_scope_question_text_trims_one_trailing_full_stop():
    from packages.orchestration.scope_question import SCOPE_QUESTION_MARKER, scope_question_text

    refusal = "task plan rejected: every task delivers a file the order did not ask for (T002)."

    assert scope_question_text(refusal) == (
        f"{SCOPE_QUESTION_MARKER} Remedy planned it twice and refused both plans; the last refusal was: "
        "task plan rejected: every task delivers a file the order did not ask for (T002). "
        "Answer with the names of the files you mean, separated by commas.")


def test_a_refusal_with_no_trailing_full_stop_is_carried_unchanged():
    from packages.orchestration.scope_question import SCOPE_QUESTION_MARKER, scope_question_text

    refusal = "task plan rejected: parse failure"

    assert scope_question_text(refusal) == (
        f"{SCOPE_QUESTION_MARKER} Remedy planned it twice and refused both plans; the last refusal was: "
        "task plan rejected: parse failure. Answer with the names of the files you mean, separated "
        "by commas.")


def test_an_open_order_refused_twice_asks_which_files_it_means(tmp_path, monkeypatch):
    from packages.orchestration.escalation import open_task_decisions
    from packages.orchestration.pingpong_job import load_job_plan
    from packages.orchestration.project_registry import resolve_project
    from packages.orchestration.scope_question import (
        SCOPE_QUESTION_MARKER,
        SCOPE_QUESTION_STOP_REASON,
        ScopeQuestionRaised,
    )
    from tests.orchestration.test_do_sequence_order_digest import _registered_repo, _shape_order

    repo = _registered_repo(tmp_path, monkeypatch)
    _mock_intake(monkeypatch)
    calls = _mock_plan_calls(monkeypatch, _checksum_plan())

    with pytest.raises(ScopeQuestionRaised) as excinfo:
        _shape_order(repo, LAB_OPEN_ORDER)

    assert len(calls) == 2
    job = load_job_plan(excinfo.value.job_id)
    assert (job.state.value, job.stop_reason) == ("stopped", SCOPE_QUESTION_STOP_REASON)
    assert job.project_id == str(resolve_project(repo).id)
    assert excinfo.value.job_id in resolve_project(repo).job_ids
    [decision] = open_task_decisions(job)
    assert decision["question"].startswith(SCOPE_QUESTION_MARKER)
    assert decision["options"] == ["checksums.json"]
    assert decision["safe_default"] == ""


def test_an_open_order_whose_second_attempt_passes_is_planned_with_it(tmp_path, monkeypatch):
    from packages.orchestration.task_deliverables import task_deliverable
    from tests.orchestration.test_do_sequence_order_digest import _registered_repo, _shape_order

    repo = _registered_repo(tmp_path, monkeypatch)
    _mock_intake(monkeypatch)
    calls = _mock_plan_calls(monkeypatch, _checksum_plan(), _style_plan())

    shaped = _shape_order(repo, LAB_OPEN_ORDER)

    assert len(calls) == 2
    assert [task_deliverable(t) for t in shaped.job.tasks] == ["style.css"]


def test_a_fenced_order_refused_once_fails_at_once_with_no_second_call(tmp_path, monkeypatch):
    from packages.orchestration.do_sequence import OrderJobPlanError
    from tests.orchestration.test_do_sequence_order_digest import _registered_repo, _shape_order

    repo = _registered_repo(tmp_path, monkeypatch)
    _mock_intake(monkeypatch)
    calls = _mock_plan_calls(monkeypatch, _style_plan())

    with pytest.raises(OrderJobPlanError, match=r"every task delivers a file the order did not ask for \(T001\)"):
        _shape_order(repo, LAB_FENCED_ORDER)

    assert len(calls) == 1


# ---------------------------------------------------------------------------
# F312 R3 C3 — DECISION F312 D4: an answer to the scope question (`apply_scope_answer`,
# called by `escalation.answer_task_decision`), and R-1378's prompt traces.
# ---------------------------------------------------------------------------


def _build_stopped_question_job(tmp_path, monkeypatch):
    """A real scope-question-stopped job, raised exactly as the tests above raise it."""
    from packages.orchestration.escalation import open_task_decisions
    from packages.orchestration.pingpong_job import load_job_plan
    from packages.orchestration.scope_question import ScopeQuestionRaised
    from tests.orchestration.test_do_sequence_order_digest import _registered_repo, _shape_order

    repo = _registered_repo(tmp_path, monkeypatch)
    _mock_intake(monkeypatch)
    _mock_plan_calls(monkeypatch, _checksum_plan())

    with pytest.raises(ScopeQuestionRaised) as excinfo:
        _shape_order(repo, LAB_OPEN_ORDER)

    job = load_job_plan(excinfo.value.job_id)
    [decision] = open_task_decisions(job)
    return job, decision["decision_id"]


def test_apply_scope_answer_plans_the_job_with_both_names_as_tasks_in_order():
    from packages.core.models import RunState
    from packages.orchestration.pingpong_job import JobPlan
    from packages.orchestration.scope_question import (
        SCOPE_QUESTION_MARKER,
        SCOPE_QUESTION_STOP_REASON,
        apply_scope_answer,
    )
    from packages.orchestration.task_deliverables import task_deliverable

    job = JobPlan(job_title="t", mission=LAB_OPEN_ORDER, state=RunState.STOPPED,
                 stop_reason=SCOPE_QUESTION_STOP_REASON)
    record = {"question": f"{SCOPE_QUESTION_MARKER} the planner's last refusal.",
             "answer": "style.css, index.html"}

    assert apply_scope_answer(job, record) is True
    assert job.state == RunState.PLANNED
    assert job.stop_reason == ""
    assert job.finished_at == ""
    assert job.task_plan is None
    assert [task_deliverable(t) for t in job.tasks] == ["style.css", "index.html"]


def test_answering_through_answer_task_decision_plans_the_job_with_both_tasks_in_order(
        tmp_path, monkeypatch):
    from datetime import datetime, timezone

    from packages.core.models import RunState
    from packages.orchestration.escalation import answer_task_decision
    from packages.orchestration.task_deliverables import task_deliverable

    job, decision_id = _build_stopped_question_job(tmp_path, monkeypatch)

    record = answer_task_decision(
        job, decision_id, answer="style.css, index.html", now=datetime.now(timezone.utc))

    assert record is not None and record["status"] == "answered"
    assert job.state == RunState.PLANNED
    assert job.stop_reason == ""
    assert job.task_plan is None
    assert [task_deliverable(t) for t in job.tasks] == ["style.css", "index.html"]


def test_an_answer_with_junk_and_repeats_keeps_only_the_one_safe_name(tmp_path, monkeypatch):
    from datetime import datetime, timezone

    from packages.orchestration.escalation import answer_task_decision
    from packages.orchestration.task_deliverables import task_deliverable

    job, decision_id = _build_stopped_question_job(tmp_path, monkeypatch)

    answer_task_decision(
        job, decision_id, answer="/etc/passwd, ../x.css, , style.css, style.css",
        now=datetime.now(timezone.utc))

    assert [task_deliverable(t) for t in job.tasks] == ["style.css"]


def test_an_answer_naming_no_usable_file_leaves_the_job_stopped(tmp_path, monkeypatch):
    from datetime import datetime, timezone

    from packages.core.models import RunState
    from packages.orchestration.escalation import answer_task_decision
    from packages.orchestration.scope_question import SCOPE_QUESTION_STOP_REASON

    job, decision_id = _build_stopped_question_job(tmp_path, monkeypatch)
    before_task_ids = [t.task_id for t in job.tasks]

    record = answer_task_decision(
        job, decision_id, answer="/etc/passwd", now=datetime.now(timezone.utc))

    assert record is not None and record["status"] == "answered"
    assert job.state == RunState.STOPPED
    assert job.stop_reason == SCOPE_QUESTION_STOP_REASON
    assert [t.task_id for t in job.tasks] == before_task_ids


def test_a_task_decision_on_a_job_not_stopped_by_the_scope_question_is_unchanged_by_the_hook():
    """A remainder decision, or any other task decision, on any OTHER job: the hook does nothing
    because `job.stop_reason` is not `scope_question` (DECISION F312 D4)."""
    from datetime import datetime, timezone

    from packages.core.models import RunState
    from packages.orchestration.escalation import answer_task_decision, enqueue_task_decision
    from packages.orchestration.pingpong_job import JobPlan, TaskEntry

    task = TaskEntry(title="Do a thing")
    job = JobPlan(job_title="t", mission="m", state=RunState.RUNNING, tasks=[task])
    record = enqueue_task_decision(
        job, task_id=task.task_id, question="Proceed with the risky approach?",
        now=datetime.now(timezone.utc))

    answered = answer_task_decision(
        job, record["decision_id"], answer="yes", now=datetime.now(timezone.utc))

    assert answered is not None and answered["status"] == "answered"
    assert job.state == RunState.RUNNING
    assert [t.task_id for t in job.tasks] == [task.task_id]
    assert job.tasks[0].title == "Do a thing"


def _fake_structured_calls(monkeypatch, task_plan_json: str):
    """Fake only the LEAF call, so the real `plan_job_llm` runs and records its own `on_call`
    trace (R-1378) — unlike `_mock_plan_calls` above, which replaces `plan_job_llm` itself and so
    never invokes the recorder it is handed."""
    monkeypatch.setattr(
        "packages.orchestration.intake.make_provider_call_fn",
        lambda: (lambda prompt, attempt: '{"schema_v": "ji1", "goal": "g", "context_refs": [], '
                 '"constraints": [], "acceptance_hints": [], "truncated_input": false, '
                 '"clarifications": []}'))
    monkeypatch.setattr(
        "packages.orchestration.intake.make_structured_call_fn",
        lambda model_cls, **kw: (lambda prompt, attempt: task_plan_json))


def test_the_question_jobs_prompt_trace_holds_at_least_two_task_plan_rows(tmp_path, monkeypatch):
    """R-1378: the two task-plan calls spent before the question are not lost."""
    import json

    from packages.orchestration.run_log import RunLogWriter
    from packages.orchestration.scope_question import ScopeQuestionRaised
    from tests.orchestration.test_do_sequence_order_digest import _registered_repo, _shape_order

    repo = _registered_repo(tmp_path, monkeypatch)
    checksum_json = json.dumps({"schema_v": "task_plan_v1", "tasks": [
        _task("T001", "Write a checksum manifest of the site", "checksums.json")]})
    _fake_structured_calls(monkeypatch, checksum_json)

    with pytest.raises(ScopeQuestionRaised) as excinfo:
        _shape_order(repo, LAB_OPEN_ORDER)

    log = RunLogWriter(job_id=excinfo.value.job_id)
    trace_path = log.path.parent / "prompt_trace.jsonl"
    assert trace_path.exists()
    rows = [json.loads(line) for line in trace_path.read_text().splitlines() if line.strip()]
    assert len([r for r in rows if r.get("role") == "task_plan"]) >= 2


# ---------------------------------------------------------------------------
# F312 R4 C3 — R-1379: the saved and reloaded answered job reads empty strings, not `None`.
# R-1380: each of `apply_scope_answer`'s two guards gets a test that fails exactly one condition.
# ---------------------------------------------------------------------------


def test_the_saved_and_reloaded_answered_job_reads_empty_strings_not_none(tmp_path, monkeypatch):
    """R-1379: `apply_scope_answer` must leave `JobPlan`'s string fields a string, not `None`,
    or the saved-and-reloaded record carries a value its own type does not allow."""
    from datetime import datetime, timezone

    from packages.core.models import RunState
    from packages.orchestration.escalation import answer_task_decision
    from packages.orchestration.pingpong_job import load_job_plan, save_job_plan
    from packages.orchestration.task_deliverables import task_deliverable

    job, decision_id = _build_stopped_question_job(tmp_path, monkeypatch)

    record = answer_task_decision(
        job, decision_id, answer="style.css", now=datetime.now(timezone.utc))
    assert record is not None and record["status"] == "answered"
    save_job_plan(job)

    reloaded = load_job_plan(job.job_id)
    assert reloaded.stop_reason == ""
    assert reloaded.finished_at == ""
    assert reloaded.state == RunState.PLANNED
    assert [task_deliverable(t) for t in reloaded.tasks] == ["style.css"]


def test_the_stop_reason_guard_alone_leaves_a_non_scope_job_unchanged():
    """R-1380: a job NOT stopped by the scope question, holding a task decision whose question
    happens to start with the marker, is unchanged — only the stop-reason guard is exercised,
    the marker guard holding true throughout."""
    from datetime import datetime, timezone

    from packages.core.models import RunState
    from packages.orchestration.escalation import answer_task_decision, enqueue_task_decision
    from packages.orchestration.pingpong_job import JobPlan, TaskEntry
    from packages.orchestration.scope_question import SCOPE_QUESTION_MARKER

    task = TaskEntry(title="Do a thing")
    job = JobPlan(job_title="t", mission="m", state=RunState.STOPPED,
                 stop_reason="budget_exhausted", tasks=[task])
    record = enqueue_task_decision(
        job, task_id=task.task_id,
        question=f"{SCOPE_QUESTION_MARKER} the planner's last refusal.",
        now=datetime.now(timezone.utc))

    answered = answer_task_decision(
        job, record["decision_id"], answer="style.css", now=datetime.now(timezone.utc))

    assert answered is not None and answered["status"] == "answered"
    assert job.state == RunState.STOPPED
    assert job.stop_reason == "budget_exhausted"
    assert [t.task_id for t in job.tasks] == [task.task_id]


def test_the_marker_guard_alone_leaves_a_scope_stopped_job_unchanged():
    """R-1380: a job stopped BY the scope question, holding a second task decision whose
    question does NOT carry the marker, is unchanged — only the marker guard is exercised, the
    stop-reason guard holding true throughout."""
    from datetime import datetime, timezone

    from packages.core.models import RunState
    from packages.orchestration.escalation import answer_task_decision, enqueue_task_decision
    from packages.orchestration.pingpong_job import JobPlan, TaskEntry
    from packages.orchestration.scope_question import (
        SCOPE_QUESTION_MARKER,
        SCOPE_QUESTION_STOP_REASON,
    )

    task_one = TaskEntry(title="The scope question's own task")
    task_two = TaskEntry(title="A second, unrelated task")
    job = JobPlan(job_title="t", mission="m", state=RunState.STOPPED,
                 stop_reason=SCOPE_QUESTION_STOP_REASON, tasks=[task_one, task_two])
    enqueue_task_decision(
        job, task_id=task_one.task_id,
        question=f"{SCOPE_QUESTION_MARKER} the planner's last refusal.",
        now=datetime.now(timezone.utc))
    second = enqueue_task_decision(
        job, task_id=task_two.task_id, question="Proceed with the risky approach?",
        now=datetime.now(timezone.utc))

    answered = answer_task_decision(
        job, second["decision_id"], answer="style.css", now=datetime.now(timezone.utc))

    assert answered is not None and answered["status"] == "answered"
    assert job.state == RunState.STOPPED
    assert job.stop_reason == SCOPE_QUESTION_STOP_REASON
    assert [t.task_id for t in job.tasks] == [task_one.task_id, task_two.task_id]
