"""amend1011-order-shape — the four failing orders of 2026-10-11, as order texts.

The real texts live in the operator's data root, which a session may not read;
these are written from the amendment's description of them (finding R-1246).
"""
from __future__ import annotations

import pytest

from packages.orchestration.job_plan import compose_task_plan_prompt
from packages.orchestration.schemas.models import TaskPlan
from packages.orchestration.task_deliverables import (
    INSPECTION_VERBS,
    fold_inspection_tasks,
    validate_deliverable_plan,
)

ORDERS = {
    "luna-t5twkd": "In universe-gate change one sentence, adjust one test and add one CHANGELOG line.",
    "luna-tugwqu": "Make the gate refuse an empty order and document it in docs/gate.md.",
    "luna-t9qzgu": "Split the loader into src/loader.py and src/parse.py, update tests/test_loader.py and README.md.",
    "luna-tfdvf5": "Rename the export flag in apps/cli/export.py and update CHANGELOG.md.",
}


def _task(tid, title, deps=(), hint=()):
    return {"id": tid, "title": title, "goal": f"goal of {tid}", "acceptance": ["done"],
            "depends_on": list(deps), "est_tokens_band": "S", "files_hint": list(hint)}


def _plan(*tasks):
    return TaskPlan.model_validate({"schema_v": "task_plan_v1", "tasks": list(tasks)})


def test_the_prompt_names_every_verb_the_validator_rejects():
    text = compose_task_plan_prompt({"goal": ORDERS["luna-t5twkd"]}, project_facts="x").text
    assert all(verb in text for verb in INSPECTION_VERBS)
    assert "deliverable" in text


def test_an_inspection_task_is_folded_into_the_task_that_depends_on_it():
    plan = _plan(_task("T001", "Analyze candidates"),
                 _task("T002", "Edit gate", deps=["T001"], hint=["gate.py"]),
                 _task("T003", "Add test", deps=["T001", "T002"], hint=["t.py"]))
    folded = fold_inspection_tasks(plan)
    assert [t.id for t in folded.tasks] == ["T002", "T003"]
    assert "Analyze candidates" in folded.tasks[0].goal
    assert folded.tasks[0].depends_on == []
    assert folded.tasks[1].depends_on == ["T002"]


def test_no_inspection_task_or_nothing_to_fold_into_is_not_repairable():
    assert fold_inspection_tasks(_plan(_task("T001", "Edit gate"))) is None
    assert fold_inspection_tasks(_plan(_task("T001", "Edit gate"),
                                       _task("T002", "Review result", deps=["T001"]))) is None


def _shape_with_plan(repo, monkeypatch, order, plan):
    from packages.orchestration.job_plan import TaskPlanResult
    from tests.orchestration.test_do_sequence_order_digest import _shape_order
    monkeypatch.setattr("packages.orchestration.intake.make_provider_call_fn",
                        lambda: (lambda p, a: '{"schema_v": "ji1", "goal": "g", "context_refs": [], '
                                 '"constraints": [], "acceptance_hints": [], "truncated_input": false, '
                                 '"clarifications": []}'))
    monkeypatch.setattr("packages.orchestration.intake.make_structured_call_fn",
                        lambda model_cls, **kw: (lambda p, a: ""))
    monkeypatch.setattr("packages.orchestration.job_plan.plan_job_llm",
                        lambda intake, call_fn, **kw: TaskPlanResult(
                            plan=plan, source="llm", calls=1, transformations=[]))
    return _shape_order(repo, order)


@pytest.mark.parametrize("key", sorted(ORDERS))
def test_an_order_whose_plan_has_an_inspection_task_is_repaired_once(
        key, tmp_path, monkeypatch):
    from tests.orchestration.test_do_sequence_order_digest import _registered_repo
    repo = _registered_repo(tmp_path, monkeypatch)
    plan = _plan(_task("T001", "Analyze candidates", hint=["a.py"]),
                 _task("T002", "Change sentence", deps=["T001"], hint=["README.md"]))
    shaped = _shape_with_plan(repo, monkeypatch, ORDERS[key], plan)
    assert len(shaped.job.tasks) == 1
    validate_deliverable_plan(shaped.job.tasks)
    assert [t["id"] for t in shaped.job.task_plan["tasks"]] == ["T002"]


def test_a_plan_of_only_inspection_still_fails_the_order(tmp_path, monkeypatch):
    from packages.orchestration.do_sequence import OrderJobPlanError
    from tests.orchestration.test_do_sequence_order_digest import _registered_repo
    repo = _registered_repo(tmp_path, monkeypatch)
    plan = _plan(_task("T001", "Read the code"), _task("T002", "Explore options", deps=["T001"]))
    with pytest.raises(OrderJobPlanError, match="task plan rejected"):
        _shape_with_plan(repo, monkeypatch, ORDERS["luna-t9qzgu"], plan)


def test_a_failed_shape_step_leaves_no_planned_job_and_lists_none(tmp_path, monkeypatch):
    from packages.core.models import RunState
    from packages.orchestration import do_sequence
    from packages.orchestration.do_context import DoContext
    from packages.orchestration.pingpong_job import JobPlan, load_job_plan, save_job_plan

    _registered = __import__("tests.orchestration.test_do_sequence_order_digest",
                             fromlist=["_registered_repo"])._registered_repo
    _registered(tmp_path, monkeypatch)
    job = JobPlan(job_title="t", mission="m", user_prompt="m", state=RunState.PLANNED)
    save_job_plan(job)
    ctx = DoContext.__new__(DoContext)
    ctx.job_ids = [str(job.job_id)]
    note = do_sequence._stop_unrun_shape_jobs(ctx)
    assert load_job_plan(str(job.job_id)).state == RunState.STOPPED
    assert ctx.job_ids == []
    assert str(job.job_id) in note
