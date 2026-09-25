"""Handlers for ``remedy job plan-*`` — show and edit a job plan while its approval is open (F015 T002).

Every edit command is a thin wrapper: it turns its arguments into the backend's own
arguments and calls `plan_editing.edit_plan`, the one transaction the write channel
uses too (DECISION F015 D1), so the CLI can do nothing the backend would refuse and
refuses nothing the backend would take. Each edit names `--plan-version`, the version
`remedy job plan-show` prints, and an edit made against an older version is refused with
the current one rather than written over it.

Exit codes follow the CLI contract (docs/guides/exit-codes.md): 2 when the arguments
themselves are wrong — a missing or malformed option, an unknown task — 3 when the job,
its plan or its approval is not in a state to take an edit, and 1 when the edited plan
fails the planner's own checks.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from apps.cli.json_envelope import emit_ok, fail

if TYPE_CHECKING:
    import argparse
    from collections.abc import Callable

EXIT_USAGE = 2
EXIT_NOT_READY = 3

#: The refusals that mean the arguments were wrong, and those that mean the job or its
#: plan cannot take an edit now. Every other refusal is the edited plan failing a check.
_USAGE_REFUSALS = frozenset({"invalid_args", "unknown_task", "unknown_command"})
_NOT_READY_REFUSALS = frozenset({"no_task_plan", "plan_not_editable", "version_conflict",
                                 "lock_timeout"})

#: Who the edit log names for an edit made here; the write door names a token fingerprint.
CLI_ACTOR = "cli"


def _load(job_id_raw: str, *, json_output: bool) -> Any:
    from apps.cli.job_id_arg import resolve_job_id_or_fail
    from packages.orchestration.pingpong_job import load_job_plan

    full_id = resolve_job_id_or_fail((job_id_raw or "").strip(), json_output=json_output,
                                     job_id=job_id_raw)
    job = load_job_plan(full_id)
    if job is None:
        fail("job_not_found", f"The record of job {full_id} cannot be read.",
             json_output=json_output, exit_code=EXIT_NOT_READY, job_id=full_id)
    return job


def _task_entry_for_planned_id(job: Any, planned_id: Any) -> Any | None:
    """The ``TaskEntry`` whose ``inputs["plan"]["planned_id"]`` matches, or ``None``."""
    return next(
        (t for t in job.tasks if (t.inputs.get("plan") or {}).get("planned_id") == planned_id),
        None)


def _cmd_plan_show(job_id_raw: str, *, json_output: bool = False) -> None:
    """Print the job's stored plan. Exits 3 when the job or its plan cannot be read."""
    from packages.orchestration.plan_editing import edit_window_refusal, plan_version

    job = _load(job_id_raw, json_output=json_output)
    body = job.task_plan
    if not isinstance(body, dict) or not body.get("tasks"):
        fail("no_task_plan", f"Job {job.job_id} has no task plan.", json_output=json_output,
             exit_code=EXIT_NOT_READY, job_id=job.job_id)
    version = plan_version(body)
    refusal = edit_window_refusal(job, body)
    tasks = []
    for t in body["tasks"]:
        task = {k: t.get(k) for k in ("id", "title", "goal", "depends_on", "est_tokens_band",
                                       "files_hint", "acceptance")}
        # DECISION F026 D2: the matching task entry's own id, status and spec
        # version — what a runtime edit's `--spec-version` must name.
        entry = _task_entry_for_planned_id(job, t.get("id"))
        task["job_task_id"] = entry.task_id if entry is not None else ""
        task["status"] = entry.status if entry is not None else ""
        task["spec_version"] = entry.spec_version if entry is not None else 1
        tasks.append(task)
    if json_output:
        emit_ok(job_id=job.job_id, version=version, approval=body.get("_approval"),
                editable=refusal is None, not_editable_because=refusal and refusal.detail,
                tasks=tasks)
        return
    print(f"Plan of job {job.job_id} — version {version}, approval {body.get('_approval')}")
    if refusal is None:
        print("The approval is open, so the plan can be edited; name --plan-version "
              f"{version} on each edit.")
    else:
        print(f"The plan cannot be edited: {refusal.detail}.")
    for task in tasks:
        deps = ", ".join(task["depends_on"]) or "nothing"
        print(f"\n{task['id']} — {task['title']} (band {task['est_tokens_band']}; "
              f"waits for {deps})")
        print(f"  goal: {task['goal']}")
        print(f"  spec version {task['spec_version']} · {task['status']}")
        for index, criterion in enumerate(task["acceptance"]):
            print(f"  [{index}] {criterion}")


def _plan_version(raw: Any, *, json_output: bool) -> int:
    if raw is None:
        fail("missing_plan_version", "Name the plan version the edit was made against with "
             "--plan-version, as `remedy job plan-show` prints it.", json_output=json_output,
             exit_code=EXIT_USAGE)
    try:
        return int(str(raw).strip())
    except ValueError:
        fail("invalid_plan_version", f"--plan-version must be a whole number, not {raw!r}.",
             json_output=json_output, exit_code=EXIT_USAGE)


def _ids(raw: str | None) -> list[str]:
    return [part.strip() for part in (raw or "").split(",") if part.strip()]


def _indexes(raw: str, *, json_output: bool) -> list[int]:
    try:
        return [int(part) for part in _ids(raw)]
    except ValueError:
        fail("invalid_index", f"A criterion index is a whole number, not {raw!r}.",
             json_output=json_output, exit_code=EXIT_USAGE)


def _run_edit(job_id_raw: str, command: str, edit_args: dict[str, Any], raw_version: Any, *,
              json_output: bool) -> None:
    """Apply one edit through the backend and report the plan's new version."""
    from packages.orchestration.pingpong_job import JobNotFoundError, JobStoreError
    from packages.orchestration.plan_editing import PlanEditRefused, edit_plan

    version = _plan_version(raw_version, json_output=json_output)
    job = _load(job_id_raw, json_output=json_output)
    try:
        result = edit_plan(str(job.job_id), command, edit_args, expected_version=version,
                           actor=CLI_ACTOR)
    except (JobNotFoundError, JobStoreError) as exc:
        fail("job_not_found", str(exc), json_output=json_output, exit_code=EXIT_NOT_READY,
             job_id=job.job_id)
    except PlanEditRefused as exc:
        message = f"The plan was not changed: {exc.detail}."
        if exc.code in _USAGE_REFUSALS:
            fail(exc.code, message, json_output=json_output, exit_code=EXIT_USAGE,
                 job_id=job.job_id, current_version=exc.current_version)
        if exc.code in _NOT_READY_REFUSALS:
            fail(exc.code, message, json_output=json_output, exit_code=EXIT_NOT_READY,
                 job_id=job.job_id, current_version=exc.current_version)
        fail(exc.code, message, json_output=json_output, job_id=job.job_id,
             current_version=exc.current_version)
    if json_output:
        emit_ok(job_id=job.job_id, command=command, version=result.version,
                tasks=[t.id for t in result.plan.tasks], plan_md=str(result.plan_md))
        return
    print(f"Plan of job {job.job_id} is now at version {result.version}: "
          f"{', '.join(t.id for t in result.plan.tasks)}.")
    print(f"Rendered plan: {result.plan_md}")


#: F026 T002, DECISION F026 D2: the runtime edit's own refusal classes, mirroring
#: `_USAGE_REFUSALS`/`_NOT_READY_REFUSALS` above but widened by the four codes
#: `task_edit_runtime.py` raises that the pre-approval editor never does.
_RUNTIME_USAGE_REFUSALS = frozenset({
    "invalid_args", "unknown_task", "unknown_command", "not_a_plan_task"})
_RUNTIME_NOT_READY_REFUSALS = frozenset({
    "job_not_found", "no_task_plan", "plan_not_editable", "version_conflict",
    "lock_timeout", "job_not_editable", "task_not_editable", "spec_archive_conflict",
})


def _spec_version(raw: Any, *, json_output: bool) -> int:
    if raw is None:
        fail("missing_spec_version", "Name the spec version the edit was made against with "
             "--spec-version, as `remedy job plan-show` prints it.", json_output=json_output,
             exit_code=EXIT_USAGE)
    try:
        return int(str(raw).strip())
    except ValueError:
        fail("invalid_spec_version", f"--spec-version must be a whole number, not {raw!r}.",
             json_output=json_output, exit_code=EXIT_USAGE)


def _resolve_task_arg(job: Any, task_arg: str) -> str:
    """The ``TaskEntry`` id *task_arg* names: its own id, its plan's unique planned id, or itself.

    An argument matching no task entry's id and no entry's unique planned id passes through
    unchanged so the backend refuses it as ``unknown_task``.
    """
    if any(t.task_id == task_arg for t in job.tasks):
        return task_arg
    matches = [t.task_id for t in job.tasks
              if (t.inputs.get("plan") or {}).get("planned_id") == task_arg]
    if len(matches) == 1:
        return matches[0]
    return task_arg


def _cmd_edit_task(args: argparse.Namespace) -> None:
    """``job edit-task`` — edit one task of an approved plan at runtime (DECISION F026 D2)."""
    from packages.orchestration.pingpong_job import JobNotFoundError, JobStoreError
    from packages.orchestration.plan_editing import PlanEditRefused
    from packages.orchestration.task_edit_runtime import edit_task_at_runtime

    json_output = getattr(args, "json", False)
    version = _spec_version(getattr(args, "spec_version", None), json_output=json_output)
    job = _load(getattr(args, "job_id", ""), json_output=json_output)
    task_id = _resolve_task_arg(job, getattr(args, "task_id", ""))
    fields = _edit_task_args(args)["fields"]
    try:
        result = edit_task_at_runtime(
            str(job.job_id), task_id, fields, expected_spec_version=version, actor=CLI_ACTOR)
    except (JobNotFoundError, JobStoreError) as exc:
        fail("job_not_found", str(exc), json_output=json_output, exit_code=EXIT_NOT_READY,
             job_id=job.job_id, current_version=None)
    except PlanEditRefused as exc:
        message = f"The task was not changed: {exc.detail}."
        if exc.code in _RUNTIME_USAGE_REFUSALS:
            fail(exc.code, message, json_output=json_output, exit_code=EXIT_USAGE,
                 job_id=job.job_id, current_version=exc.current_version)
        if exc.code in _RUNTIME_NOT_READY_REFUSALS:
            fail(exc.code, message, json_output=json_output, exit_code=EXIT_NOT_READY,
                 job_id=job.job_id, current_version=exc.current_version)
        fail(exc.code, message, json_output=json_output, job_id=job.job_id,
             current_version=exc.current_version)
    if json_output:
        emit_ok(job_id=result.job_id, task_id=result.task_id, planned_id=result.planned_id,
                state=result.state, spec_version=result.spec_version,
                plan_version=result.plan_version, restored=list(result.restored))
        return
    print(f"Task {result.planned_id} of job {result.job_id} is now at spec version "
          f"{result.spec_version}.")
    if result.state == "failed":
        print(f"Relaunch with: remedy job run {result.job_id}")


def _edit_task_args(args: argparse.Namespace) -> dict[str, Any]:
    fields: dict[str, Any] = {}
    for option, field in (("title", "title"), ("goal", "goal"), ("acceptance", "acceptance"),
                          ("band", "est_tokens_band"), ("files_hint", "files_hint")):
        value = getattr(args, option, None)
        if value is not None:
            fields[field] = value
    return {"task_id": getattr(args, "task_id", ""), "fields": fields}


def _split_args(args: argparse.Namespace) -> dict[str, Any]:
    json_output = getattr(args, "json", False)
    groups = [_indexes(group, json_output=json_output) for group in getattr(args, "group", None) or []]
    return {"task_id": getattr(args, "task_id", ""), "partition": groups}


def _acceptance_args(args: argparse.Namespace) -> dict[str, Any]:
    edit_args: dict[str, Any] = {"task_id": getattr(args, "task_id", ""),
                                 "op": getattr(args, "op", "")}
    raw_index = getattr(args, "index", None)
    if raw_index is not None:
        try:
            edit_args["index"] = int(str(raw_index).strip())
        except ValueError:
            fail("invalid_index", f"A criterion index is a whole number, not {raw_index!r}.",
                 json_output=getattr(args, "json", False), exit_code=EXIT_USAGE)
    text = getattr(args, "text", None)
    if text is not None:
        edit_args["text"] = text
    return edit_args


def _edit(command: str, build: Callable[[argparse.Namespace], dict[str, Any]]):
    return lambda args: _run_edit(
        getattr(args, "job_id", ""), command, build(args), getattr(args, "plan_version", None),
        json_output=getattr(args, "json", False))


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "job.plan-show": lambda args: _cmd_plan_show(
        getattr(args, "job_id", ""), json_output=getattr(args, "json", False)),
    "job.plan-edit-task": _edit("plan_edit_task", _edit_task_args),
    "job.edit-task": _cmd_edit_task,
    "job.plan-delete-task": _edit("plan_delete_task", lambda args: {
        "task_id": getattr(args, "task_id", "")}),
    "job.plan-reorder": _edit("plan_reorder", lambda args: {
        "order": _ids(getattr(args, "sequence", ""))}),
    "job.plan-merge-tasks": _edit("plan_merge_tasks", lambda args: {
        "task_ids": _ids(getattr(args, "task_ids", ""))}),
    "job.plan-split-task": _edit("plan_split_task", _split_args),
    "job.plan-edit-acceptance": _edit("plan_edit_acceptance", _acceptance_args),
}
