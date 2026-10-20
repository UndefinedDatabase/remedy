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
