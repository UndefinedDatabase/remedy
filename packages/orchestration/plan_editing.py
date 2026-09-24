"""F015 T001 — edit a job's stored task plan while its approval is open.

The human reshapes the plan BEFORE blessing it. Every edit is one transaction on
the STORED plan, the ``task_plan`` body of the job record (DECISION F015 D1):
load it, apply one edit, revalidate the result with the SAME validation the planner's
own path runs, then persist the plan, its version, its edit log and the job's task
list in one write of the record. An edit that fails revalidation changes nothing.
There is no second plan representation: ``job.tasks`` is regenerated from the edited
plan by ``map_task_plan_to_tasks``, the mapping the planner's path uses.

The edit window is the plan approval: an edit is accepted only while
``_approval`` reads ``pending`` and the job is still planned. Concurrent editors are
told apart by the plan's version: every edit names the version it was made
against, and a stale one is refused with the current version rather than written
over it.

Split and merge reuse the granularity module's own mechanics with the human's
parameters: ``_split_task`` over a manual acceptance partition and ``_merge_group``
over the named tasks, with ``_rewire`` pointing dependents at the result.
"""
from __future__ import annotations

import fcntl
import os
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from packages.common.secure_fs import durable_write_json
from packages.core.models import RunState
from packages.orchestration.data_paths import job_dir, job_evidence_export_dir
from packages.orchestration.job_plan import (
    APPROVED_PLAN_HASH_KEY,
    map_task_plan_to_tasks,
    plan_content_hash,
    resolve_task_plan_approval,
    write_plan_md,
)
from packages.orchestration.mission_compiler import PLAN_VERSION_KEY
from packages.orchestration.pingpong_job import require_job_plan, save_job_plan
from packages.orchestration.schemas.models import PlannedTask, TaskPlan
from packages.orchestration.task_deliverables import (
    DeliverablePlanError,
    record_llm_task_deliverables,
    validate_deliverable_plan,
)
from packages.orchestration.task_granularity import (
    _Cluster,
    _merge_group,
    _rewire,
    _split_task,
)

#: The persisted body's edit log: one entry per accepted edit, oldest first.
EDIT_LOG_KEY = "_edits"

#: The evidence file the edit log is exported to after every accepted edit.
EDIT_LOG_EVIDENCE = "user_edited_plan.json"
EDIT_LOG_SCHEMA_V = "user_edited_plan_v1"

#: The fields ``plan_edit_task`` may change. ``id`` and ``depends_on`` are the
#: graph itself and change only through delete, merge and split.
EDITABLE_TASK_FIELDS = ("title", "goal", "acceptance", "est_tokens_band", "files_hint")

ACCEPTANCE_OPS = ("add", "edit", "remove")

_LOCK_NAME = "plan_edit.lock"
_LOCK_TIMEOUT_SEC = 5.0


class PlanEditRefused(ValueError):
    """An edit or approval the backend refused. Nothing was written.

    ``code`` is one of ``no_task_plan``, ``plan_not_editable``, ``version_conflict``,
    ``unknown_command``, ``invalid_args``, ``unknown_task``, ``invalid_plan``,
    ``lock_timeout`` and ``approval_closed``; ``current_version`` is the stored plan's
    version whenever one was read. A ``ValueError``, so the write door's own
    ``rejected_effect`` clause answers any code the door does not handle itself.
    """

    def __init__(self, code: str, detail: str, *, current_version: int | None = None) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail
        self.current_version = current_version


@dataclass(frozen=True)
class PlanEditResult:
    """An accepted edit: the plan's new version, the plan, and the log entry written."""

    version: int
    plan: TaskPlan
    entry: dict[str, Any]
    plan_md: Path


def plan_version(body: dict[str, Any]) -> int:
    """The stored plan's version; a plan no edit has touched is version 1."""
    return int(body.get(PLAN_VERSION_KEY, 1))


def _model_body(body: dict[str, Any]) -> dict[str, Any]:
    # The persisted body carries `_approval`, `_normalization` and the keys this
    # module adds beside the model's own fields, and the model forbids extras.
    return {k: v for k, v in body.items() if not k.startswith("_")}


def _refuse_args(detail: str) -> PlanEditRefused:
    return PlanEditRefused("invalid_args", detail)


def _task_with(task: PlannedTask, update: dict[str, Any]) -> PlannedTask:
    # Built through the model, never `model_copy`, which would skip validation.
    try:
        return PlannedTask.model_validate({**task.model_dump(), **update})
    except ValidationError as exc:
        raise PlanEditRefused("invalid_plan", _reasons(exc)) from exc


def _reasons(exc: ValidationError) -> str:
    return "; ".join(str(e.get("msg", "")) for e in exc.errors())


def _task_index(tasks: list[PlannedTask], task_id: Any) -> int:
    if not isinstance(task_id, str) or not task_id:
        raise _refuse_args("task_id must be a non-empty string")
    for i, task in enumerate(tasks):
        if task.id == task_id:
            return i
    raise PlanEditRefused("unknown_task", f"the plan has no task {task_id!r}")


def _edit_task(tasks: list[PlannedTask], args: dict[str, Any]) -> list[PlannedTask]:
    i = _task_index(tasks, args.get("task_id"))
    fields = args.get("fields")
    if not isinstance(fields, dict) or not fields:
        raise _refuse_args("fields must be a non-empty object")
    for name in fields:
        if name == "clarifications_resolved":
            raise _refuse_args(
                "clarification answers are immutable once resolved and are not edited here")
        if name not in EDITABLE_TASK_FIELDS:
            raise _refuse_args(
                f"field {name!r} is not editable; editable: {', '.join(EDITABLE_TASK_FIELDS)}")
    out = list(tasks)
    out[i] = _task_with(tasks[i], fields)
    return out


def _delete_task(tasks: list[PlannedTask], args: dict[str, Any]) -> list[PlannedTask]:
    i = _task_index(tasks, args.get("task_id"))
    gone = tasks[i]
    out: list[PlannedTask] = []
    for task in tasks[:i] + tasks[i + 1:]:
        if gone.id not in task.depends_on:
            out.append(task)
            continue
        # THE REWIRING RULE: a dependent inherits the deleted task's own
        # dependencies in the deleted task's place, so nothing it waited for
        # through the deleted task is dropped.
        deps: list[str] = []
        for dep in task.depends_on:
            for new_dep in (gone.depends_on if dep == gone.id else [dep]):
                if new_dep not in deps and new_dep != task.id:
                    deps.append(new_dep)
        out.append(task.model_copy(update={"depends_on": deps}))
    return out


def _reorder(tasks: list[PlannedTask], args: dict[str, Any]) -> list[PlannedTask]:
    order = args.get("order")
    if not isinstance(order, list) or not all(isinstance(t, str) for t in order):
        raise _refuse_args("order must be a list of task ids")
    current = [t.id for t in tasks]
    if sorted(order) != sorted(current) or len(set(order)) != len(order):
        missing = sorted(set(current) - set(order))
        extra = sorted(set(order) - set(current))
        raise _refuse_args(
            "order must name every task exactly once; "
            f"missing: {missing or 'none'}, unknown: {extra or 'none'}")
    by_id = {t.id: t for t in tasks}
    return [by_id[tid] for tid in order]


def _merge_tasks(tasks: list[PlannedTask], args: dict[str, Any]) -> list[PlannedTask]:
    ids = args.get("task_ids")
    if not isinstance(ids, list) or len(ids) < 2 or len(set(ids)) != len(ids):
        raise _refuse_args("task_ids must name at least two distinct tasks")
    positions = sorted(_task_index(tasks, tid) for tid in ids)
    group = [tasks[i] for i in positions]
    merged = _merge_group(group)
    replacements = {t.id: merged.id for t in group[1:]}
    out: list[PlannedTask] = []
    for i, task in enumerate(tasks):
        if i == positions[0]:
            out.append(merged)
        elif i not in positions:
            out.append(_rewire(task, replacements))
    return out


def _split_task_edit(tasks: list[PlannedTask], args: dict[str, Any]) -> list[PlannedTask]:
    i = _task_index(tasks, args.get("task_id"))
    task = tasks[i]
    partition = args.get("partition")
    if (not isinstance(partition, list) or len(partition) < 2
            or not all(isinstance(g, list) and g for g in partition)):
        raise _refuse_args("partition must hold at least two non-empty groups")
    flat = [n for group in partition for n in group]
    if (not all(isinstance(n, int) and not isinstance(n, bool) for n in flat)
            or sorted(flat) != list(range(len(task.acceptance)))):
        raise _refuse_args(
            f"partition must place each acceptance index 0..{len(task.acceptance) - 1} "
            "of the task in exactly one group")
    clusters = [_Cluster(acceptance=[task.acceptance[n] for n in group]) for group in partition]
    children = _split_task(task, clusters, {t.id for t in tasks})
    # As the automatic split does: whatever waited for the task waits for the chain's end.
    replacements = {task.id: children[-1].id}
    return ([_rewire(t, replacements) for t in tasks[:i]] + children
            + [_rewire(t, replacements) for t in tasks[i + 1:]])


def _edit_acceptance(tasks: list[PlannedTask], args: dict[str, Any]) -> list[PlannedTask]:
    i = _task_index(tasks, args.get("task_id"))
    op = args.get("op")
    if op not in ACCEPTANCE_OPS:
        raise _refuse_args(f"op must be one of {', '.join(ACCEPTANCE_OPS)}")
    acceptance = list(tasks[i].acceptance)
    index = args.get("index")
    text = args.get("text")
    if op != "add" or index is not None:
        upper = len(acceptance) if op == "add" else len(acceptance) - 1
        if not isinstance(index, int) or isinstance(index, bool) or not 0 <= index <= upper:
            raise _refuse_args(f"index must be an integer from 0 to {upper}")
    if op != "remove" and not isinstance(text, str):
        raise _refuse_args("text must be a string")
    if op == "add":
        acceptance.insert(len(acceptance) if index is None else index, text)
    elif op == "edit":
        acceptance[index] = text
    else:
        # Removing the last criterion is left to the schema, which refuses an
        # empty acceptance list: the rule stays in one place.
        del acceptance[index]
    out = list(tasks)
    out[i] = _task_with(tasks[i], {"acceptance": acceptance})
    return out


_EDITS: dict[str, Callable[[list[PlannedTask], dict[str, Any]], list[PlannedTask]]] = {
    "plan_edit_task": _edit_task,
    "plan_delete_task": _delete_task,
    "plan_reorder": _reorder,
    "plan_merge_tasks": _merge_tasks,
    "plan_split_task": _split_task_edit,
    "plan_edit_acceptance": _edit_acceptance,
}

#: The edit commands, in the order the feature file names them.
PLAN_EDIT_COMMANDS: tuple[str, ...] = tuple(_EDITS)


def revalidate(plan: TaskPlan, tasks: list[dict[str, Any]]) -> TaskPlan:
    """The plan with *tasks*, validated exactly as the planner's own path validates one.

    Constructing the model runs ``TaskPlan``'s schema and its DAG check (cycles,
    unknown and therefore dangling dependencies, duplicate ids, the task cap);
    the task list it maps to must then pass ``validate_deliverable_plan``, as
    ``do_sequence`` requires of a fresh plan. Raises ``PlanEditRefused``
    (``invalid_plan``) naming the violation.
    """
    data = plan.model_dump()
    data["tasks"] = tasks
    try:
        new_plan = TaskPlan.model_validate(data)
    except ValidationError as exc:
        raise PlanEditRefused("invalid_plan", _reasons(exc)) from exc
    # DECISION F015 D4: a job runs its tasks in plan order and never reads `depends_on`,
    # so an edited plan may not put a task before one it waits for.
    position = {task.id: n for n, task in enumerate(new_plan.tasks)}
    for task in new_plan.tasks:
        later = [dep for dep in task.depends_on if position[dep] > position[task.id]]
        if later:
            raise PlanEditRefused(
                "invalid_plan", f"task {task.id!r} comes before {later[0]!r}, which it waits "
                "for; a job runs its tasks in plan order")
    try:
        validate_deliverable_plan(_mapped_tasks(new_plan))
    except DeliverablePlanError as exc:
        raise PlanEditRefused("invalid_plan", str(exc)) from exc
    return new_plan


def _mapped_tasks(plan: TaskPlan) -> list[Any]:
    tasks = map_task_plan_to_tasks(plan)
    record_llm_task_deliverables(tasks)
    return tasks


def apply_edit(plan: TaskPlan, command: str, args: dict[str, Any]) -> TaskPlan:
    """Apply one edit to *plan* and return the revalidated result. Pure: no I/O."""
    edit = _EDITS.get(command)
    if edit is None:
        raise PlanEditRefused(
            "unknown_command", f"{command!r}; known: {', '.join(PLAN_EDIT_COMMANDS)}")
    if not isinstance(args, dict):
        raise _refuse_args("args must be an object")
    after = [t.model_dump() for t in edit(list(plan.tasks), args)]
    if after == [t.model_dump() for t in plan.tasks]:
        raise _refuse_args("the edit changes nothing")
    return revalidate(plan, after)


def edit_window_refusal(job: Any, body: dict[str, Any]) -> PlanEditRefused | None:
    """Why *job*'s stored plan *body* cannot be edited now, or None while it can."""
    approval = body.get("_approval")
    if approval != "pending":
        return PlanEditRefused(
            "plan_not_editable",
            f"the plan is {approval or 'not awaiting approval'}; a plan is edited only "
            "while its approval is open", current_version=plan_version(body))
    if job.state != RunState.PLANNED:
        return PlanEditRefused(
            "plan_not_editable",
            f"the job is {job.state.value}; a plan is edited only before its job starts",
            current_version=plan_version(body))
    return None


@contextmanager
def plan_edit_lock(job_id: str, root: Path | None = None) -> Iterator[None]:
    """Hold the job's plan-edit lock: one read-check-write of the plan at a time."""
    directory = job_dir(job_id, root)
    directory.mkdir(parents=True, exist_ok=True)
    fd = os.open(str(directory / _LOCK_NAME), os.O_CREAT | os.O_RDWR, 0o600)
    try:
        deadline = time.monotonic() + _LOCK_TIMEOUT_SEC
        while True:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise PlanEditRefused(
                        "lock_timeout",
                        f"another edit of job {job_id} held the plan for "
                        f"{_LOCK_TIMEOUT_SEC:g}s") from None
                time.sleep(0.05)
        try:
            yield
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
    finally:
        os.close(fd)


def edit_plan(
    job_id: str,
    command: str,
    args: dict[str, Any],
    *,
    expected_version: int,
    actor: str,
    root: Path | None = None,
) -> PlanEditResult:
    """Apply one edit to job *job_id*'s stored plan as one transaction.

    Under the job's plan-edit lock: load the record, refuse unless the approval is
    open and *expected_version* is the stored version, apply and revalidate the
    edit, then write the plan, its bumped version, the appended log entry and the
    regenerated task list in ONE write of the job record. Only after that write
    are the derived files regenerated: ``plan_v<n>.md`` and the edit log's
    evidence export. Any refusal raises ``PlanEditRefused`` before the record is
    written, so a refused edit changes nothing.
    """
    with plan_edit_lock(job_id, root):
        job = require_job_plan(job_id, root)
        body = job.task_plan
        if not isinstance(body, dict) or not body.get("tasks"):
            raise PlanEditRefused("no_task_plan", f"job {job_id} has no task plan to edit")
        refusal = edit_window_refusal(job, body)
        if refusal is not None:
            raise refusal
        version = plan_version(body)
        if expected_version != version:
            raise PlanEditRefused(
                "version_conflict",
                f"the edit was made against version {expected_version}; the plan is at "
                f"version {version}", current_version=version)
        plan = TaskPlan.model_validate(_model_body(body))
        try:
            new_plan = apply_edit(plan, command, args)
        except PlanEditRefused as exc:
            exc.current_version = version
            raise
        entry = {
            "version": version + 1,
            "ts": datetime.now(timezone.utc).isoformat(),
            "actor": actor,
            "command": command,
            "args": args,
            "before": [t.model_dump() for t in plan.tasks],
            "after": [t.model_dump() for t in new_plan.tasks],
        }
        new_body = new_plan.model_dump()
        new_body.update({k: v for k, v in body.items() if k.startswith("_")})
        new_body[PLAN_VERSION_KEY] = version + 1
        new_body[EDIT_LOG_KEY] = [*body.get(EDIT_LOG_KEY, []), entry]
        job.task_plan = new_body
        job.tasks = _mapped_tasks(new_plan)
        save_job_plan(job, root)
    evidence = job_evidence_export_dir(job_id, root)
    plan_md = write_plan_md(new_plan, evidence, version=version + 1,
                            transformations=body.get("_normalization"),
                            edits=new_body[EDIT_LOG_KEY])
    durable_write_json(evidence / EDIT_LOG_EVIDENCE, {
        "schema_v": EDIT_LOG_SCHEMA_V,
        "job_id": job_id,
        "version": version + 1,
        "edits": new_body[EDIT_LOG_KEY],
    })
    return PlanEditResult(version=version + 1, plan=new_plan, entry=entry, plan_md=plan_md)


def consume_plan_approval(
    job: Any,
    *,
    reason: str,
    answers: dict[str, str],
    questions: list[dict[str, Any]],
    root: Path | None = None,
) -> Path | None:
    """Approve or reject the job's pending plan, closing the edit window atomically.

    Both approval doors load the job before they consume its approval, so an edit
    accepted in between would be written over by the door's older copy, and the
    approval would name a plan the record no longer holds. Here the record is read
    again under the plan-edit lock: the approval is refused ``approval_closed`` when
    the record no longer awaits one, and otherwise the plan and task list the record
    holds NOW are carried into *job* and ``resolve_task_plan_approval`` runs
    unchanged, so the approval covers exactly the stored plan. An edit that arrives
    afterwards finds the approval closed and is refused ``plan_not_editable``.

    Returns what ``resolve_task_plan_approval`` returns: the assumption-log path on
    an approval, None on a rejection.
    """
    job_id = str(job.job_id)
    with plan_edit_lock(job_id, root):
        stored = require_job_plan(job_id, root)
        body = stored.task_plan
        if not isinstance(body, dict) or body.get("_approval") != "pending":
            approval = body.get("_approval") if isinstance(body, dict) else None
            raise PlanEditRefused(
                "approval_closed",
                f"the plan is {approval or 'not awaiting approval'}; there is no open "
                "approval to answer")
        job.task_plan = body
        job.tasks = stored.tasks
        if reason == "approve":
            # DECISION F015 D4: the approval records exactly what it covers.
            body[APPROVED_PLAN_HASH_KEY] = plan_content_hash(body)
        return resolve_task_plan_approval(
            job, reason=reason, answers=answers, questions=questions)


def replay_edits(original: TaskPlan, edits: list[dict[str, Any]]) -> TaskPlan:
    """Rebuild the plan's evolution from *original* by re-applying every logged edit.

    Each entry's ``before`` must equal the plan it is replayed on and its ``after``
    the replay's result; a log that does not reconstruct the plan raises
    ``ValueError`` naming the first entry that diverges.
    """
    plan = original
    for n, entry in enumerate(edits):
        if [t.model_dump() for t in plan.tasks] != entry["before"]:
            raise ValueError(f"edit {n} (version {entry.get('version')}) does not start "
                             "from the plan the log reached")
        plan = apply_edit(plan, entry["command"], entry["args"])
        if [t.model_dump() for t in plan.tasks] != entry["after"]:
            raise ValueError(f"edit {n} (version {entry.get('version')}) does not replay "
                             "to the plan it logged")
    return plan
