"""`remedy job inject`, `job inject-confirm` and `job inject-answer` — F028 T003,
DECISION F028 D4.

Drafts a new task from the operator's own words into a running job's plan, confirms a
drafted task, and answers a shortfall the draft's budget check raised. Modelled on
`job_veto_cmd.py`: the same job-id resolution, the same usage/not-ready/other exit-code
split, and the same write channel the browser will share in round 5 —
`task_injection.injection_budget_inputs` and `task_injection.injection_call_fn` are the
one pair of helpers both doors read, per DECISION F028 D4 (3).

Exit codes follow the CLI contract (docs/guides/exit-codes.md): 2 when the invocation
itself is wrong — `text_required`, `text_too_long`, `text_invalid`, `unknown_task`,
`unknown_option` and `cannot_shrink` — 3 when the job, the plan or the draft is not in a
state that admits the request — `job_terminal`, `no_task_plan`, `plan_full`,
`planner_unavailable`, `budget_unreadable`, `draft_unknown`, `draft_expired`,
`draft_needs_decision`, `already_confirmed`, `draft_stale`, `draft_not_in_shortfall` and
`already_answered` — and 1, `fail()`'s own default, for every other refusal and for a job
that does not exist.
"""
from __future__ import annotations

from typing import Any

from apps.cli.job_id_arg import resolve_job_id_or_fail
from apps.cli.json_envelope import emit_ok, fail

EXIT_USAGE = 2
EXIT_NOT_READY = 3

#: The refusals that mean the invocation itself was wrong.
_USAGE_CODES = frozenset({
    "text_required", "text_too_long", "text_invalid", "unknown_task",
    "unknown_option", "cannot_shrink",
})
#: The refusals that mean the job, the plan or the draft cannot take the request right now.
_NOT_READY_CODES = frozenset({
    "job_terminal", "no_task_plan", "plan_full", "planner_unavailable",
    "budget_unreadable", "draft_unknown", "draft_expired", "draft_needs_decision",
    "already_confirmed", "draft_stale", "draft_not_in_shortfall", "already_answered",
})

#: Who the injection's audit line names for a request made here; DECISION F027 D5 (2)'s
#: same reasoning: the write door names a token fingerprint instead.
CLI_ACTOR = "cli"


def _resolve_after(job: Any, after_arg: str | None) -> str | None:
    """The plan's own id `--after` names, or *after_arg* unchanged.

    `job_plan_cmd._resolve_task_arg` resolves *after_arg* to a `TaskEntry`'s own id (its
    own id or its plan's unique planned id); the plan `draft_task_injection` places
    against is keyed by PLANNED ids (`T001`, ...), not that runtime id, so this looks the
    matched entry back up and answers its `inputs["plan"]["planned_id"]`. *after_arg* is
    returned unchanged when nothing matched it, or when the matched entry carries no
    planned id — the draft pass then refuses it as `unknown_task` itself.
    """
    if after_arg is None:
        return None
    from apps.cli.commands.job_plan_cmd import _resolve_task_arg

    resolved = _resolve_task_arg(job, after_arg)
    entry = next((t for t in job.tasks if t.task_id == resolved), None)
    if entry is None:
        return after_arg
    planned_id = (entry.inputs.get("plan") or {}).get("planned_id")
    return planned_id if planned_id else after_arg


def _print_draft(job_id: str, answer: dict) -> None:
    task = answer["task"]
    placement = answer["placement"]
    check = answer["budget_check"]
    print(f"Drafted task {task['id']}: {task['title']}")
    print(f"  goal: {task['goal']}")
    for item in task["acceptance"]:
        print(f"  acceptance: {item}")
    print(f"  band: {task['est_tokens_band']}")
    print(f"  placement: {placement['rationale']}")
    print(f"  budget: {check['arithmetic']}")
    for conflict in answer.get("fence_conflicts") or []:
        glob = conflict.get("glob") or ""
        suffix = f" ({glob})" if glob else ""
        print(f"  fence flag: {conflict['path']} [{conflict['rule']}]{suffix}")
    print(f"  expires: {answer['expires_at']}")
    token = answer["confirm_token"]
    print(f"Confirm it with: remedy job inject-confirm {job_id} {token}")


def _print_shortfall(job_id: str, answer: dict) -> None:
    seed = answer["decision_seed"]
    check = answer["budget_check"]
    draft_id = answer["draft_id"]
    print(seed["question"])
    print(f"  {check['arithmetic']}")
    for option in seed["options"]:
        print(f"  {option}: {seed['option_labels'][option]}")
        print(f"  remedy job inject-answer {job_id} {draft_id} --option {option}")


def _print_confirmation(job_id: str, confirmation: dict) -> None:
    print(f"Task {confirmation['task_id']} confirmed for job {job_id}.")
    print(f"  draft: {confirmation['draft_id']}")
    print(f"  placement: {confirmation['placement']['rationale']}")
    print(f"  confirmed at: {confirmation['confirmed_at']}")


def _cmd_inject(job_id_str: str, text: str, *, after: str | None = None, yes: bool = False,
                json_output: bool = False) -> None:
    from packages.orchestration import task_injection as ti
    from packages.orchestration.pingpong_job import JobNotFoundError, require_job_plan

    job_id = resolve_job_id_or_fail(job_id_str, json_output=json_output)
    try:
        job = require_job_plan(job_id)
    except JobNotFoundError as exc:
        fail("job_not_found", str(exc), json_output=json_output)

    resolved_after = _resolve_after(job, after)

    try:
        budgets, counters, config = ti.injection_budget_inputs(job)
    except ti.TaskInjectionRefused as exc:
        code = exc.code
        refusal_exit = EXIT_USAGE if code in _USAGE_CODES else (
            EXIT_NOT_READY if code in _NOT_READY_CODES else 1)
        fail(code, exc.detail, json_output=json_output, exit_code=refusal_exit, job_id=job_id)
        return

    call_fn = ti.injection_call_fn()
    answer = ti.draft_task_injection(
        job, text, call_fn=call_fn, budgets=budgets, counters=counters, config=config,
        actor=CLI_ACTOR, after=resolved_after)

    if answer["outcome"] == "refused":
        code = answer["code"]
        refusal_exit = EXIT_USAGE if code in _USAGE_CODES else (
            EXIT_NOT_READY if code in _NOT_READY_CODES else 1)
        fail(code, answer["detail"], json_output=json_output, exit_code=refusal_exit,
             job_id=job_id)
        return

    if answer["outcome"] == "shortfall":
        if json_output:
            emit_ok(**answer)
        else:
            _print_shortfall(job_id, answer)
        if yes:
            fail("draft_needs_decision",
                 "a shortfall draft needs its decision answered before it can be confirmed",
                 json_output=json_output, exit_code=EXIT_NOT_READY, job_id=job_id)
        return

    # outcome == "drafted"
    if yes:
        confirmation = ti.confirm_task_injection(
            job, answer["confirm_token"], actor=CLI_ACTOR, unseen=True)
        if confirmation["outcome"] == "refused":
            code = confirmation["code"]
            refusal_exit = EXIT_USAGE if code in _USAGE_CODES else (
                EXIT_NOT_READY if code in _NOT_READY_CODES else 1)
            fail(code, confirmation["detail"], json_output=json_output,
                 exit_code=refusal_exit, job_id=job_id)
            return
        if json_output:
            emit_ok(job_id=job_id, draft=answer, confirmation=confirmation)
            return
        _print_confirmation(job_id, confirmation)
        return

    if json_output:
        emit_ok(**answer)
        return
    _print_draft(job_id, answer)


def _cmd_inject_confirm(job_id_str: str, token: str, *, json_output: bool = False) -> None:
    from packages.orchestration import task_injection as ti
    from packages.orchestration.pingpong_job import JobNotFoundError, require_job_plan

    job_id = resolve_job_id_or_fail(job_id_str, json_output=json_output)
    try:
        job = require_job_plan(job_id)
    except JobNotFoundError as exc:
        fail("job_not_found", str(exc), json_output=json_output)

    result = ti.confirm_task_injection(job, token, actor=CLI_ACTOR)

    if result["outcome"] == "refused":
        code = result["code"]
        refusal_exit = EXIT_USAGE if code in _USAGE_CODES else (
            EXIT_NOT_READY if code in _NOT_READY_CODES else 1)
        fail(code, result["detail"], json_output=json_output, exit_code=refusal_exit,
             job_id=job_id)
        return

    if json_output:
        emit_ok(**result)
        return
    _print_confirmation(job_id, result)


def _cmd_inject_answer(job_id_str: str, draft_id: str, *, option: str = "",
                       json_output: bool = False) -> None:
    from packages.orchestration import task_injection as ti
    from packages.orchestration.pingpong_job import JobNotFoundError, require_job_plan

    job_id = resolve_job_id_or_fail(job_id_str, json_output=json_output)
    try:
        job = require_job_plan(job_id)
    except JobNotFoundError as exc:
        fail("job_not_found", str(exc), json_output=json_output)

    try:
        budgets, counters, config = ti.injection_budget_inputs(job)
    except ti.TaskInjectionRefused as exc:
        code = exc.code
        refusal_exit = EXIT_USAGE if code in _USAGE_CODES else (
            EXIT_NOT_READY if code in _NOT_READY_CODES else 1)
        fail(code, exc.detail, json_output=json_output, exit_code=refusal_exit, job_id=job_id)
        return

    answer = ti.answer_injection_shortfall(
        job, draft_id, option, actor=CLI_ACTOR, budgets=budgets, counters=counters,
        config=config)

    if answer["outcome"] == "refused":
        code = answer["code"]
        refusal_exit = EXIT_USAGE if code in _USAGE_CODES else (
            EXIT_NOT_READY if code in _NOT_READY_CODES else 1)
        fail(code, answer["detail"], json_output=json_output, exit_code=refusal_exit,
             job_id=job_id)
        return

    if answer["outcome"] == "dropped":
        if json_output:
            emit_ok(**answer)
            return
        print(f"Injection draft {draft_id} dropped for job {job_id}; nothing added.")
        return

    if answer["outcome"] == "shortfall":
        if json_output:
            emit_ok(**answer)
        else:
            _print_shortfall(job_id, answer)
        return

    # outcome == "drafted" — a derived draft, prints as `job inject` prints a draft.
    if json_output:
        emit_ok(**answer)
        return
    _print_draft(job_id, answer)


COMMAND_HANDLERS = {
    "job.inject": lambda args: _cmd_inject(
        getattr(args, "job_id", "") or "",
        getattr(args, "text", "") or "",
        after=getattr(args, "after", None) or None,
        yes=bool(getattr(args, "yes", False)),
        json_output=bool(getattr(args, "json", False)),
    ),
    "job.inject-confirm": lambda args: _cmd_inject_confirm(
        getattr(args, "job_id", "") or "",
        getattr(args, "token", "") or "",
        json_output=bool(getattr(args, "json", False)),
    ),
    "job.inject-answer": lambda args: _cmd_inject_answer(
        getattr(args, "job_id", "") or "",
        getattr(args, "draft", "") or "",
        option=getattr(args, "option", None) or "",
        json_output=bool(getattr(args, "json", False)),
    ),
}
