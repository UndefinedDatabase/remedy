"""F312 T001 (DECISION F312 D2): `plan_order_job`'s `scope_order` keyword, not the milestone outline
it is handed as its own `order`, is what the task-plan guard reads.

Drives the real `plan_order_job` with a mocked planner, exactly as
`tests/orchestration/test_order_shape_repair.py`'s `_shape_with_plan` does, over a milestone
outline that fences ("Change only README.md …") and a plan whose two tasks deliver files the
outline never named.
"""
from __future__ import annotations

import pytest

#: A planner-written job outline: it fences, but it is never the person's order (DECISION F312 D2).
OUTLINE_ORDER = "Change only README.md and describe the new design there."

#: The second lab order of 2026-10-20 (R-1369): no file name, no fence.
LAB_OPEN_ORDER = "Super, jetzt mach ein schickes design"

#: The lab's README fence (amend1016p D1): a fenced person's order still fences an outline job.
LAB_FENCED_ORDER = "Ändere nur die README. Verändere sonst nichts."


def _task(tid: str, title: str, hint: str):
    return {"id": tid, "title": title, "goal": title, "acceptance": [f"{title} is done"],
            "depends_on": [], "est_tokens_band": "S", "files_hint": [hint]}


def _two_file_plan():
    from packages.orchestration.schemas.models import TaskPlan

    return TaskPlan.model_validate({"schema_v": "task_plan_v1", "tasks": [
        _task("T002", "Add a modern colour scheme", "style.css"),
        _task("T003", "Restructure the page layout", "index.html")]})


def _shape_outline_with_plan(repo, monkeypatch, plan, **kwargs):
    """`plan_order_job(OUTLINE_ORDER, ...)` with a mocked planner, as `_shape_with_plan` does."""
    from packages.orchestration.job_plan import TaskPlanResult
    from tests.orchestration.test_do_sequence_order_digest import _shape_order

    monkeypatch.setattr(
        "packages.orchestration.intake.make_provider_call_fn",
        lambda: (lambda p, a: '{"schema_v": "ji1", "goal": "g", "context_refs": [], '
                 '"constraints": [], "acceptance_hints": [], "truncated_input": false, '
                 '"clarifications": []}'))
    monkeypatch.setattr(
        "packages.orchestration.intake.make_structured_call_fn",
        lambda model_cls, **kw: (lambda p, a: ""))
    monkeypatch.setattr(
        "packages.orchestration.job_plan.plan_job_llm",
        lambda intake, call_fn, **kw: TaskPlanResult(plan=plan, source="llm", calls=1, transformations=[]))
    return _shape_order(repo, OUTLINE_ORDER, **kwargs)


def test_an_open_scope_order_lets_both_outline_tasks_through(tmp_path, monkeypatch):
    from packages.orchestration.task_deliverables import task_deliverable
    from tests.orchestration.test_do_sequence_order_digest import _registered_repo

    repo = _registered_repo(tmp_path, monkeypatch)

    shaped = _shape_outline_with_plan(repo, monkeypatch, _two_file_plan(), scope_order=LAB_OPEN_ORDER)

    assert [task_deliverable(t) for t in shaped.job.tasks] == ["style.css", "index.html"]


def test_without_a_scope_order_the_outlines_own_fence_still_refuses_its_foreign_files(
        tmp_path, monkeypatch):
    from packages.orchestration.do_sequence import OrderJobPlanError
    from tests.orchestration.test_do_sequence_order_digest import _registered_repo

    repo = _registered_repo(tmp_path, monkeypatch)

    with pytest.raises(OrderJobPlanError,
                       match=r"every task delivers a file the order did not ask for \(T002, T003\)"):
        _shape_outline_with_plan(repo, monkeypatch, _two_file_plan())


def test_a_fenced_scope_order_fences_the_outline_job_too(tmp_path, monkeypatch):
    from packages.orchestration.do_sequence import OrderJobPlanError
    from tests.orchestration.test_do_sequence_order_digest import _registered_repo

    repo = _registered_repo(tmp_path, monkeypatch)

    with pytest.raises(OrderJobPlanError,
                       match=r"every task delivers a file the order did not ask for \(T002, T003\)"):
        _shape_outline_with_plan(repo, monkeypatch, _two_file_plan(), scope_order=LAB_FENCED_ORDER)
