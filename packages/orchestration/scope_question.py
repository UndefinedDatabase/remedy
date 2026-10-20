"""F312, DECISION F312 D3 — an open order whose task plan is refused twice asks which files it
means, and plans no third time.

`do_sequence._first_pass_task_plan` gives an order of the `open` kind
(`do_scope.order_scope_kind`) one more `plan_job_llm` call after its first refusal
(`second_pass_task_plan`); a plan that refusal refuses too stops the walk on one question
(`raise_scope_question`) instead of a third planner call. A fenced or file-naming order already
says which files it means, so only an open order reaches this module.

DECISION F312 D4 — the answer side: `apply_scope_answer`, called by
`escalation.answer_task_decision` after it records every answer, turns the named files into the
job's tasks and the job `planned`, so `remedy job resume` runs it with no further planner call.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from packages.orchestration.project_registry import RemyProject

#: WHY: the question's own text and the walk's detail both name it, so the two never drift apart.
SCOPE_QUESTION_MARKER = "Which files does this order mean?"

#: WHY: the stopped job and the walk's stop reason share one spelling, read by both sides.
SCOPE_QUESTION_STOP_REASON = "scope_question"


# WHY: the decision's options are the planner's own proposal, so answering it only PICKS, never invents.
def scope_question_options(plan: Any) -> list[str]:
    """The first `files_hint` entry of each task of *plan*, stripped, in task order, each once."""
    options: list[str] = []
    for task in plan.tasks:
        if not task.files_hint:
            continue
        hint = str(task.files_hint[0]).strip()
        if hint and hint not in options:
            options.append(hint)
    return options


# WHY: the question carries the planner's own last word, so the person reads why Remedy stopped.
def scope_question_text(refusal: str) -> str:
    """The one question asked after a second refusal, naming *refusal*'s message."""
    trimmed = refusal[:-1] if refusal.endswith(".") else refusal
    return (
        f"{SCOPE_QUESTION_MARKER} Remedy planned it twice and refused both plans; the last refusal was: "
        f"{trimmed}. Answer with the names of the files you mean, separated by commas."
    )


# WHY: the walk's shape step needs the answering command without reaching into escalation itself.
class ScopeQuestionRaised(Exception):
    """A second refusal of an open order's task plan; carries the stopped job's answering command."""

    def __init__(self, *, job_id: str, decision_id: str, answer_command: str) -> None:
        self.job_id = job_id
        self.decision_id = decision_id
        self.answer_command = answer_command
        super().__init__(
            f"the task plan was refused twice, so job {job_id} asks which files the order means "
            f"instead of planning a third time")


# WHY: the second refusal's job never runs, so it is saved stopped with ONE question, not pending.
def raise_scope_question(
        second_refusal: Exception, refused_plan: Any, *, mission: str, job_file_sha256: str,
        project: RemyProject, target_repo_path: str, intake_result: Any, prompt_traces: list,
) -> None:
    """Save the job the second refusal left, ask which files it means, and raise `ScopeQuestionRaised`.

    Never returns normally (DECISION F312 D3). R-1378: *prompt_traces*, the calls spent so far,
    are written to the job's `prompt_trace.jsonl` before it raises, exactly as the end of
    `plan_order_job` writes them for a job that is not stopped on a question.
    """
    from datetime import datetime, timezone

    from packages.orchestration.escalation import enqueue_task_decision, task_decision_answer_command
    from packages.orchestration.job_plan import map_task_plan_to_tasks
    from packages.orchestration.pingpong_job import JOB_STOPPED, JobPlan, save_job_plan
    from packages.orchestration.project_registry import attach_job, save_project

    tasks = map_task_plan_to_tasks(refused_plan)
    job = JobPlan(
        job_title=mission[:80], mission=mission, user_prompt=mission,
        job_file_sha256=job_file_sha256,
        project_id=str(project.id),
        repo_path=target_repo_path,
        intake=intake_result.value.model_dump(),
        task_plan=refused_plan.model_dump(),
        tasks=tasks,
        state=JOB_STOPPED,
        stop_reason=SCOPE_QUESTION_STOP_REASON,
        finished_at=datetime.now(timezone.utc).isoformat(),
    )
    save_job_plan(job)
    attach_job(project, str(job.job_id))
    save_project(project)
    record = enqueue_task_decision(
        job, task_id=tasks[0].task_id, question=scope_question_text(str(second_refusal)),
        options=scope_question_options(refused_plan), safe_default="",
        impact="No further planner call is made until this is answered.",
        now=datetime.now(timezone.utc))
    save_job_plan(job)
    if prompt_traces:
        from packages.orchestration.prompt_trace import write_trace_jsonl
        from packages.orchestration.run_log import RunLogWriter
        log = RunLogWriter(job_id=job.job_id)
        try:
            write_trace_jsonl(prompt_traces, log.path.parent / "prompt_trace.jsonl")
        except OSError:
            pass
    answer_command = task_decision_answer_command(str(job.job_id), str(record["decision_id"]))
    raise ScopeQuestionRaised(
        job_id=str(job.job_id), decision_id=str(record["decision_id"]), answer_command=answer_command)


# WHY: this is the one second call `_first_pass_task_plan` may make; a third call is never reachable.
def second_pass_task_plan(
        refusal: Exception, scope_order: str, plan_intake_dict: dict[str, Any], plan_call_fn: Any,
        composed: Any, on_call: Any, mission: str, job_file_sha256: str, project: RemyProject,
        target_repo_path: str, intake_result: Any, prompt_traces: list,
) -> tuple[Any, list[Any]]:
    """The order's second-attempt LLM task plan: ``(fp_result, tasks)``, or raises.

    *refusal* propagates unchanged for a scope order that is not `open`
    (`do_scope.order_scope_kind`). For an open order, `plan_job_llm` is called once more with the
    same *composed* prompt and *on_call* trace recorder; a plan it cannot parse fails as a
    first-pass parse failure does; a plan `_deliverable_task_plan` refuses again reaches
    `raise_scope_question`, which never returns.
    """
    from packages.orchestration.do_scope import ORDER_SCOPE_OPEN, order_scope_kind

    if order_scope_kind(scope_order) != ORDER_SCOPE_OPEN:
        raise refusal
    from packages.core.models import RunState
    from packages.orchestration.do_sequence import (
        OrderJobPlanError,
        _deliverable_task_plan,
        _record_unparsed_plan,
    )
    from packages.orchestration.job_plan import plan_job_llm
    from packages.orchestration.pingpong_job import JobPlan

    fp_result = plan_job_llm(plan_intake_dict, plan_call_fn, composed=composed, on_call=on_call)
    if fp_result.plan is None:
        job = JobPlan(
            job_title=mission[:80], mission=mission, user_prompt=mission,
            job_file_sha256=job_file_sha256,
            project_id=str(project.id),
            repo_path=target_repo_path,
            intake=intake_result.value.model_dump(),
            state=RunState.PENDING,
        )
        _record_unparsed_plan(job, fp_result.error_hint)
        raise OrderJobPlanError(
            f"task plan generation failed: {fp_result.error_hint or 'parse failure'}")
    try:
        fp_result.plan, tasks = _deliverable_task_plan(fp_result.plan, scope_order, target_repo_path)
    except OrderJobPlanError as second_refusal:
        raise_scope_question(
            second_refusal, fp_result.plan, mission=mission, job_file_sha256=job_file_sha256,
            project=project, target_repo_path=target_repo_path, intake_result=intake_result,
            prompt_traces=prompt_traces)
    return fp_result, tasks


# WHY: DECISION F312 D4 — an answer naming files makes them the job's tasks, so `job resume` runs
# them with no further planner call; an answer that names nothing usable changes nothing.
def apply_scope_answer(job: Any, record: Mapping[str, Any]) -> bool:
    """Turn a scope question's answer into the job's tasks (DECISION F312 D4); `True` iff it did.

    Acts only when *job*'s `stop_reason` is `SCOPE_QUESTION_STOP_REASON` and *record*'s question
    starts with `SCOPE_QUESTION_MARKER`; otherwise returns `False`, unchanged. The answer is read
    as comma-separated file names, each stripped, blank and repeated ones left out; of those, a
    name is kept only when it is a relative path that stays inside the repository (no leading
    `/`, no `..` segment). When at least one name is kept, the job's tasks become one
    `task_deliverables.deliverable_task` per kept name, in the order given; its task plan is
    cleared, its state becomes `RunState.PLANNED`, and its stop reason and finish time are
    cleared, so `remedy job resume <job>` runs it with no planner call. Never saves *job* and
    never calls a planner: both answer doors save the job after `answer_task_decision`.
    """
    if getattr(job, "stop_reason", "") != SCOPE_QUESTION_STOP_REASON:
        return False
    if not str(record.get("question", "")).startswith(SCOPE_QUESTION_MARKER):
        return False
    seen: list[str] = []
    for raw in str(record.get("answer", "")).split(","):
        name = raw.strip()
        if name and name not in seen:
            seen.append(name)
    names = [name for name in seen
             if not name.startswith("/") and ".." not in name.split("/")]
    if not names:
        return False
    from packages.core.models import RunState
    from packages.orchestration.task_deliverables import deliverable_task

    job.tasks = [deliverable_task(name, job.mission) for name in names]
    job.task_plan = None
    job.state = RunState.PLANNED
    job.stop_reason = ""
    job.finished_at = ""
    return True
