"""F268 — `remedy do "<order>"` as DATA: the step names, the step table, one walker.

DECISION F268 D4. `DO_SEQUENCE` is the one ordered list of step names; the
table maps each name to its step function; `walk_do_sequence` calls steps only
through that table, only in that order, and ends the walk at the first step
that stops or fails. No step is called from prose-order code, so a later
feature can add a second named list as a lookup rather than a rewrite
(DECISION amend0911-feedback D3).

The module sits under `packages/` rather than `apps/cli/commands/` because its
steps call package functions and must be testable without the CLI.

Scope: init registers and ignores and writes no file into the repository
(D2); study runs once, on a non-empty repository only (D3); plan creates the
mission record for the order, writes the contract template forced or proposed
onto it (DECISION F269 D1 (4)), plans it and keeps the plan (D4, D5); shape reads
"one job" or "milestones" from that plan, `--force-job` / `--force-mission`
overriding it, and plans the jobs, each bounded by deliverables (D5, D6); the ui
step that opened the old cockpit is gone and `--no-ui` does nothing (operator amendment
amend1015-face-migration, DECISIONs amend1015f D21, D22); run runs the first job on
the chosen providers; apply stops before apply and prints the apply command for
the job that ran, unless `--apply`, which applies it (DECISION F268 D9).

Operator amendment amend1014-do-golden-path-now D1: a bounded one-deliverable order walks the
bounded lane of `do_lane.py` (no planning provider call; only the builder and the reviewer
run), anything else the full lane, and a human-facing walk says what it is doing through
`do_progress.py` (D4).

DECISION F268 D12 (amending D10): in a walk of two or more jobs only the first
runs. Every other job waits, because a job's workspace is cut from the target's
HEAD commit and an apply does not commit, so a follow-up job run now could not
see its predecessor's output. `do` names the waiting jobs, and for each prints
the `remedy job run` command to use once its predecessor's applied output is
committed.

DECISION F270 D4: under a commit flag (`--commit "<message>"`, `--commit-auto`
or `--commit-with-history`) no job waits: the run step applies and commits (or
merges) each job before the next job's worktree is cut, and the apply step
applies the last. The apply step never passes `--push` to `apply_job`; with
`--push`, or `apply.push_after_mission` and a commit flag, it pushes the last
landed commit ONCE after the last job, through `job_apply.push_to_upstream`.
Only a blocking criterion of the mission that is `unmet` refuses that push;
each one still `open` is named. A walk that stops keeps what it committed and
pushes nothing.

DECISION F268 D11: run mirrors each job it ran into the F103 ledger, as `job run`
does, and `do_cost_summary` reads the measured tokens per role and cost back
through `token_ledger.query_cost`.

DECISION F310 D6, continuing F269 D9 (2): a job the run step ran that its budget stopped names
its budget decision as its one open question, the Next lines name the command that answers it
`extend`, and the remainder decision waits until that stop is answered `abandon`.

DECISION F268 D8: `--step-by-step` halts after every step that did work and,
inside run, before each job — points where no provider call is in flight — and
reads one line through the context's `read_line`; `q` or end of input stops the
walk and asks every job of the walk to stop through `safe_points.request_stop`.
`--plan-only` ends the walk after shape: run reports stopped and runs no job.
`--rehearse` stops where `--plan-only` stops, through `stop_walk_for_rehearsal` (DECISION F055 D1).
"""

from __future__ import annotations

import hashlib
import logging
import sys
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from packages.orchestration.pingpong_job import JobPlan, TaskEntry
    from packages.orchestration.project_registry import RemyProject

from packages.orchestration.budget_stop import budget_stop_walk_note

# DECISION F205 D3: the walk's context, its targets, its apply and push and its summaries
# live in modules of their own; this module imports the names it uses, and every other
# consumer imports each name from its own module (operator amendment amend1014-luna-mission-fixes D.2).
from packages.orchestration.do_apply import (
    _step_apply,
    do_apply_one_job,
)
from packages.orchestration.do_context import (
    DO_STEP_DONE,
    DO_STEP_FAILED,
    DO_STEP_STOPPED,
    DO_WALK_ENDING_STATUSES,
    DoContext,
    DoStepResult,
    _job_run_role_flags,
    do_stopped_walk_note,
)
from packages.orchestration.do_lane import settle_do_lane
from packages.orchestration.do_plan_confirm import approve_confirmed_plan
from packages.orchestration.do_progress import do_step_intro
from packages.orchestration.do_rehearsal import stop_walk_for_rehearsal
from packages.orchestration.do_study import do_step_study
from packages.orchestration.do_targets import (
    _shape_job_orders,
    _step_init,
    name_do_job,
    resolve_do_shape,
)
from packages.orchestration.order_cancel import cancellable_walk
from packages.orchestration.order_jobs import record_job_waits
from packages.orchestration.order_ledger import (
    OrderCallLedger,
    bind_order_ledger,
    reserve_waiting_budgets,
)
from packages.orchestration.review_reports import capture_review_report

#: The sequence, as data (DECISION F268 D4). The walker reads nothing else.
DO_SEQUENCE: tuple[str, ...] = ("init", "study", "plan", "shape", "run", "apply")


#: A step takes the context and returns ``(status, detail)``; the walker names it.
DoStep = Callable[[DoContext], tuple[str, str]]


def walk_do_sequence(ctx: DoContext,
                     table: Mapping[str, DoStep] | None = None) -> DoContext:
    """Call each step of `DO_SEQUENCE` through the table, in order, until one ends the walk.

    With `--step-by-step`, a step that did work is followed by a halt before the
    next step (DECISION F268 D8); a halt that stops reports the next step stopped.
    """
    ctx.ledger = ctx.ledger or OrderCallLedger(caps=ctx.budgets)
    with cancellable_walk(DO_STEP_TABLE if table is None else table) as steps, \
            bind_order_ledger(ctx.ledger), capture_review_report(ctx):   # exec-1017c, R-1356; exec-1017 D5
        return _walk_steps(ctx, steps)


def _walk_steps(ctx: DoContext, steps: Mapping[str, DoStep]) -> DoContext:
    for index, name in enumerate(DO_SEQUENCE):
        status, detail = _announced_step(ctx, name, steps[name])
        ctx.results.append(DoStepResult(name=name, status=status, detail=detail))
        if status in DO_WALK_ENDING_STATUSES:
            break
        if status != DO_STEP_DONE or index + 1 == len(DO_SEQUENCE):
            continue
        coming = DO_SEQUENCE[index + 1]
        if not do_step_by_step_halt(ctx, f"{name}: {detail}", f"the {coming} step"):
            # DECISION F270 D4 (2): a stopped walk under a commit flag says what stays.
            note = do_stopped_walk_note(ctx) if ctx.commit_mode else ""
            ctx.results.append(DoStepResult(
                name=coming, status=DO_STEP_STOPPED,
                detail=f"not run: {ctx.halt_reason}{note}"))
            break
    return ctx


def _announced_step(ctx: DoContext, name: str, step: DoStep) -> tuple[str, str]:
    """Call *step*, and when the walk has a progress sink say it started, beat while it runs, say it ended.

    Operator amendment amend1014-do-golden-path-now D4: the start line is written, flushed, before
    the step's first line of work, so a step that blocks is never silent.
    """
    if ctx.progress is None:
        return step(ctx)
    intro = do_step_intro(name, ctx)
    with ctx.progress.step(name, intro) as end:
        status, detail = step(ctx)
        end(status, detail)
    return status, detail


#: The answer at a `--step-by-step` halt that stops the walk; end of input stops it too.
DO_HALT_STOP_ANSWER = "q"


def do_step_by_step_halt(ctx: DoContext, done: str, coming: str) -> bool:
    """One `--step-by-step` halt: print what happened and what comes next, read one line.

    Returns True to go on. Without `--step-by-step` it returns True at once. `q`
    or end of input returns False, records the reason on the context and asks
    every job of the walk to stop through the F011 kill switch (DECISION F268 D8).
    No provider call is in flight here: every caller halts between whole steps
    or between whole jobs.
    """
    if not ctx.step_by_step:
        return True
    print(f"[step-by-step] done: {done}", file=sys.stderr)  # noqa: T201 — the step-by-step prompt the person answers
    print(f"[step-by-step] next: {coming}. Enter continues, "  # noqa: T201 — the step-by-step prompt the person answers
          f"{DO_HALT_STOP_ANSWER} stops.", file=sys.stderr)
    try:
        answer = ctx.read_line() if ctx.read_line is not None else None
    except EOFError:
        answer = None
    if answer is not None and answer.strip().lower() != DO_HALT_STOP_ANSWER:
        return True

    from packages.orchestration.safe_points import StopControlError, request_stop

    said = "end of input" if answer is None else f"{DO_HALT_STOP_ANSWER!r}"
    reason = f"stopped by {said} at the --step-by-step halt before {coming}"
    failures = []
    for job_id in ctx.job_ids:
        try:
            request_stop(job_id, reason=reason, source="do")
        except (StopControlError, OSError) as exc:
            failures.append(f"job {job_id}: {exc}")
    if ctx.job_ids:
        reason += f"; a stop was requested for job(s) {', '.join(ctx.job_ids)}"
    if failures:
        reason += f" (not recorded for {'; '.join(failures)})"
    ctx.halt_reason = reason
    return False


# ---------------------------------------------------------------------------
# The shape step's job planning — moved here from `_cmd_do_mission` in
# apps/cli/commands/do_cmd.py (the F147 golden path), not copied.
# ---------------------------------------------------------------------------


#: The audit reason of a task plan that `--run-unattended` approved.
DO_UNATTENDED_REASON = "auto-approved via --run-unattended"

#: The plan label of a job planned without an LLM task plan (DECISION F268 D6).
DO_DETERMINISTIC_PLAN_LABEL = "deterministic, one task per deliverable"


class OrderJobPlanError(Exception):
    """The task plan for an order could not be generated; the job is left unplanned."""


# A plan's limits either hold or refuse the order. A budget or fence set that does not
# validate is never dropped, because a job without it runs unbounded or unfenced (R-1037).
def order_job_limits(merged_budgets: dict[str, Any] | None,
                     merged_fences: dict[str, Any] | None) -> tuple[Any, Any]:
    """The job's ``JobBudgets`` and ``JobFences`` from the merged plan values, or None for each.

    Raises :class:`OrderJobPlanError` naming the set that failed to validate.
    """
    from packages.core.models import JobBudgets, JobFences

    job_budgets = job_fences = None
    if merged_budgets:
        try:
            job_budgets = JobBudgets(**{
                k: v for k, v in merged_budgets.items() if k in JobBudgets.model_fields})
        except (TypeError, ValueError) as exc:
            raise OrderJobPlanError(f"job budgets rejected: {exc}") from exc
    if merged_fences:
        try:
            job_fences = JobFences(**{
                k: v for k, v in merged_fences.items() if k in JobFences.model_fields})
        except (TypeError, ValueError) as exc:
            raise OrderJobPlanError(f"job fences rejected: {exc}") from exc
    return job_budgets, job_fences


@dataclass
class OrderJobPlan:
    """The one job planned for an order, and how its intake and plan were made."""

    job: JobPlan
    intake_result: Any
    intake_fallback_reason: str
    plan_label: str

    @property
    def intake_label(self) -> str:
        if self.intake_result.source == "llm":
            return "intake: llm"
        if self.intake_fallback_reason == "forced":
            return "intake: heuristic (forced by --no-llm)"
        if self.intake_fallback_reason == "bounded":
            return "intake: heuristic (bounded lane, no provider call)"
        if self.intake_fallback_reason == "provider_unavailable":
            return "intake: heuristic fallback (provider unavailable)"
        if self.intake_fallback_reason == "provider_error":
            return "intake: heuristic fallback (provider error)"
        return f"intake: {self.intake_result.source}"

    def to_json(self) -> dict[str, Any]:
        return {
            "job_id": str(self.job.job_id),
            "state": self.job.state.value,
            "order": self.job.mission,
            "intake": {
                "source": self.intake_result.source,
                "goal": self.intake_result.value.goal,
                "fallback_reason": self.intake_fallback_reason,
            },
            "tasks": [
                {"task_id": str(t.task_id), "description": t.title}
                for t in self.job.tasks
            ],
            "plan_label": self.plan_label,
        }


def _deliverable_task_plan(plan: Any, order: str = "", repo: str = "") -> tuple[Any, list[Any]]:
    """The plan and its job tasks, every task a deliverable; raises :class:`OrderJobPlanError` otherwise.

    DECISION amend1011 D1 and operator amendment amend1014-do-golden-path-now D2: a plan is
    normalized before it may run, each inspection task folded into the task that needs it and
    the tasks serving one file merged into one; the planner's own plan is the last candidate,
    and a plan still rejected afterwards fails. exec-1017 D2: first, a task whose deliverable the
    *order* did not put in scope is left out, and a plan of nothing else fails. DECISION F312 D1:
    for an order whose `do_scope.order_scope_kind` is open, that refusal names a checking artifact
    instead of a foreign file.
    """
    if order:
        from packages.orchestration.do_lane import tracked_repo_files
        from packages.orchestration.do_scope import ORDER_SCOPE_OPEN, order_scope_kind, out_of_scope_task_ids

        outside = set(out_of_scope_task_ids(order, list(plan.tasks), tracked_repo_files(repo)))
        if outside and outside == {task.id for task in plan.tasks}:
            if order_scope_kind(order) == ORDER_SCOPE_OPEN:
                raise OrderJobPlanError(
                    "task plan rejected: every task only makes a checking artifact the order did not ask for "
                    f"({', '.join(sorted(outside))})")
            raise OrderJobPlanError("task plan rejected: every task delivers a file the order did not ask "
                                    f"for ({', '.join(sorted(outside))})")
        plan = plan.model_copy(update={"tasks": [
            task.model_copy(update={"depends_on": [d for d in task.depends_on if d not in outside]})
            for task in plan.tasks if task.id not in outside]})
    from packages.orchestration.job_plan import map_task_plan_to_tasks
    from packages.orchestration.task_deliverables import (
        DeliverablePlanError,
        coalesce_deliverable_tasks,
        fold_inspection_tasks,
        record_llm_task_deliverables,
        validate_deliverable_plan,
    )

    folded = fold_inspection_tasks(plan)
    candidates = (coalesce_deliverable_tasks(folded or plan), folded, plan)
    error: DeliverablePlanError | None = None
    for attempt in candidates:
        if attempt is None:
            continue
        tasks = map_task_plan_to_tasks(attempt)
        record_llm_task_deliverables(tasks)
        try:
            validate_deliverable_plan(tasks)
        except DeliverablePlanError as exc:
            error = error or exc
            continue
        return attempt, tasks
    raise OrderJobPlanError(f"task plan rejected: {error}") from error


# Step (1) of `plan_order_job`'s boundary on docs/system/structure-ledger-v1.md (F297): the
# record a task plan that could not be parsed leaves. The job is saved stopped, never pending,
# because nothing will run it (R-1247).
def _record_unparsed_plan(job: JobPlan, error_hint: str | None) -> None:
    from datetime import datetime, timezone

    from packages.orchestration.data_paths import job_evidence_export_dir
    from packages.orchestration.failure_postmortem import (
        FailureSignals,
        build_job_rollup,
        write_postmortem,
    )
    from packages.orchestration.pingpong_job import JOB_STOPPED, save_job_plan

    job.state, job.stop_reason = JOB_STOPPED, "plan_parse_failed"
    job.finished_at = datetime.now(timezone.utc).isoformat()
    save_job_plan(job)
    signals = FailureSignals(error_class="parse", error_text=error_hint or "task plan parse failure")
    pm = build_job_rollup(job_id=str(job.job_id), signals=signals)
    ev_dir = job_evidence_export_dir(str(job.job_id))
    ev_dir.mkdir(parents=True, exist_ok=True)
    try:
        write_postmortem(ev_dir, pm, root=ev_dir)
    except Exception as exc:  # noqa: BLE001 — postmortem write failure is only warned about, not fatal
        logging.getLogger(__name__).warning("Warning: postmortem write failed: %s", exc)


# Step (2) of `plan_order_job`'s boundary on docs/system/structure-ledger-v1.md (F312): the
# first-pass task plan and its approval.
def _first_pass_task_plan(
        mission: str, intake_result: Any, plan_call_fn: Any, prompt_traces: list,
        project: RemyProject, repo: str, target_repo_path: str, job_file_sha256: str,
        run_unattended: bool, scope_order: str,
) -> tuple[Any, str]:
    """The order's first-pass LLM task plan, approved or left pending: ``(job, plan_label)``.

    DECISION F312 D3: a plan `_deliverable_task_plan` refuses, for a *scope_order* of the `open`
    kind, gets one more attempt through `scope_question.second_pass_task_plan`; a plan refused
    again stops the walk on one question instead of a third planner call.
    """
    from packages.core.models import RunState
    from packages.orchestration.job_plan import (
        apply_plan_fences,
        compose_task_plan_prompt,
        make_task_plan_call_recorder,
        plan_job_llm,
        write_plan_md,
    )
    from packages.orchestration.pingpong_job import JobPlan, save_job_plan
    plan_intake_dict = intake_result.value.model_dump()
    # Composed exactly ONCE here and handed to `plan_job_llm`, so the bytes
    # the provider receives and the manifest the trace records come from the
    # same composition — `prompt_chars` and `segment_manifest_chars` can no
    # longer describe two different prompts (R-0256).
    plan_composed = compose_task_plan_prompt(plan_intake_dict, repo_root=target_repo_path)
    on_call = make_task_plan_call_recorder(
        prompt_traces, plan_composed, provider="ollama", provider_kind="ollama")
    fp_result = plan_job_llm(plan_intake_dict, plan_call_fn, composed=plan_composed, on_call=on_call)
    if fp_result.plan is not None:
        try:
            fp_result.plan, tasks = _deliverable_task_plan(fp_result.plan, scope_order, target_repo_path)
        except OrderJobPlanError as refusal:
            from packages.orchestration.scope_question import second_pass_task_plan
            fp_result, tasks = second_pass_task_plan(
                refusal, scope_order, plan_intake_dict, plan_call_fn, plan_composed, on_call,
                mission, job_file_sha256, project, target_repo_path, intake_result)
        fp_dict = fp_result.plan.model_dump()
        fp_dict["_approval"] = "pending"
        fp_dict["_normalization"] = fp_result.transformations
        from packages.orchestration.budget_resolution import resolve_job_budgets
        config_budgets = resolve_job_budgets(project_root=repo)
        config_budgets_dict = config_budgets.model_dump(exclude_none=True) if config_budgets else None
        # DECISION F310 D2: the plan's suggested budgets are its estimate, never a limit.
        merged_fences = apply_plan_fences(None, fp_result.plan.fences)
        job_budgets, job_fences = order_job_limits(config_budgets_dict, merged_fences)
        job = JobPlan(
            job_title=mission[:80], mission=mission, user_prompt=mission,
            job_file_sha256=job_file_sha256,
            project_id=str(project.id),
            repo_path=target_repo_path,
            intake=intake_result.value.model_dump(),
            task_plan=fp_dict,
            tasks=tasks,
            state=RunState.PLANNED,
            budgets=job_budgets.model_dump(mode="json") if job_budgets is not None else None,
            fences=job_fences,
        )
        save_job_plan(job)
        from packages.orchestration.data_paths import job_evidence_export_dir
        write_plan_md(
            fp_result.plan, job_evidence_export_dir(str(job.job_id)),
            transformations=fp_result.transformations)
        if run_unattended:
            # F034: --run-unattended covers approval AND clarifications: every open question
            # runs on its documented default, in the assumption log, never silent. The semantics
            # live in job_plan.auto_approve_task_plan, which the orchestrator loop runs too.
            from packages.orchestration.job_plan import (
                AUTO_APPROVAL_MODE,
                announce_plan_approval,
                auto_approve_task_plan,
            )
            fp_dict = auto_approve_task_plan(
                fp_dict, job_evidence_export_dir(str(job.job_id)), reason=DO_UNATTENDED_REASON)
            job.task_plan = fp_dict
            save_job_plan(job)
            announce_plan_approval(job, mode=AUTO_APPROVAL_MODE)
            plan_label = (
                f"task plan {fp_result.plan.schema_v} (approved via --run-unattended)"
            )
        else:
            plan_label = (
                f"task plan {fp_result.plan.schema_v} (awaiting approval)"
            )
    else:
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
            f"task plan generation failed: "
            f"{fp_result.error_hint or 'parse failure'}"
        )
    return job, plan_label


def plan_order_job(
    order: str,
    *,
    project: RemyProject,
    repo_path: str = "",
    no_llm: bool = False,
    run_unattended: bool = False,
    deterministic_tasks: list[TaskEntry] | None = None,
    planner_model: str | None = None,
    planner_provider: str | None = None,
    scope_order: str = "",
) -> OrderJobPlan:
    """Plan ONE job for an order: intake, then an LLM task plan or the deterministic one.

    ``repo_path`` is the job's target repository. ``run_unattended`` auto-approves an LLM task plan
    through ``job_plan.auto_approve_task_plan`` (F034). The job is saved and attached to
    ``project``. The deterministic plan is one task per deliverable of the order (DECISION F268 D6);
    ``deterministic_tasks`` names the job's tasks outright and skips the LLM task plan, which is how
    the shape step plans a job per deliverable or per job-sized slice of them. Every plan, LLM or
    deterministic, passes the deliverable validator. ``planner_model`` is ``model=`` of the intake
    and task-plan calls (DECISION F268 D16 (7)); omitted, the planner's configured model serves.
    ``planner_provider`` is ``provider=`` of those same calls — which planning SERVICE runs them
    (operator amendment amend0920-selfuse-real, DECISION D1); omitted, the ``planner`` role answers,
    and its default is Ollama. ``scope_order`` is the person's order whose kind the task-plan guard
    reads (DECISION F312 D2); omitted, *order* serves.
    Raises :class:`OrderJobPlanError` when an LLM task plan cannot be parsed (after writing the
    job's post-mortem), when a plan fails the validator, or when the order names more deliverables
    than one job holds.
    """
    from packages.core.models import RunState
    from packages.orchestration.intake import (
        compose_intake_prompt,
        heuristic_intake,
        make_intake_call_recorder,
        make_provider_call_fn,
        run_intake,
    )
    from packages.orchestration.pingpong_job import JobPlan, save_job_plan
    from packages.orchestration.task_deliverables import (
        DeliverablePlanError,
        deterministic_job_plans,
        validate_deliverable_plan,
    )

    mission = order
    # The run manifest's job-input check requires job_file_sha256 as a REQUIRED
    # fact (DECISION F295 D10): a job planned from an order is defined by that
    # order text, so its digest is taken once, here, from that text.
    job_file_sha256 = hashlib.sha256(mission.encode("utf-8")).hexdigest()
    repo = repo_path
    target_repo_path = str(Path(repo_path).resolve()) if repo_path else ""

    call_fn = None
    intake_result = None
    # One list, one write: it carries every prompt trace this command produces,
    # intake and task plan alike, because `write_trace_jsonl` opens its path
    # with mode "w" and a second write would truncate the first.
    prompt_traces: list = []
    intake_fallback_reason = ""
    if no_llm:
        intake_result = heuristic_intake(mission)
        intake_fallback_reason = "forced"
    else:
        from packages.orchestration.intake import resolve_planner_target

        planner_name, _ = resolve_planner_target(planner_provider, planner_model)
        if planner_model or planner_provider:
            from packages.orchestration.intake import make_structured_call_fn
            from packages.orchestration.schemas import JobIntake
            call_fn = make_structured_call_fn(
                JobIntake, model=planner_model, provider=planner_provider,
            )
        else:
            call_fn = make_provider_call_fn()
        if call_fn is not None:
            intake_composed = compose_intake_prompt(mission)
            intake_result = run_intake(
                mission,
                call_fn,
                composed=intake_composed,
                # The evidence names the planner that ACTUALLY ran, resolved
                # through the one function that decides it. A trace that says
                # "ollama" while the Claude CLI planned is a trace that lies
                # about its own run (amend0920-selfuse-real, DECISION D1).
                on_call=make_intake_call_recorder(
                    prompt_traces,
                    intake_composed,
                    provider=planner_name,
                    provider_kind=planner_name,
                ),
            )
            if intake_result.source == "heuristic":
                intake_fallback_reason = "provider_error"

        if intake_result is None:
            intake_result = heuristic_intake(mission)
            intake_fallback_reason = "provider_unavailable"

    # --- Task Plan (LLM) or deterministic fallback ---
    job = None
    plan_label = DO_DETERMINISTIC_PLAN_LABEL

    plan_call_fn = None
    if call_fn is not None and not no_llm and deterministic_tasks is None:
        from packages.orchestration.intake import make_structured_call_fn
        from packages.orchestration.schemas.models import TaskPlan
        # Planning needs a call_fn bound to TaskPlan: the intake one binds
        # the provider's native schema to JobIntake, so the provider would
        # answer in intake shape and every plan attempt would fail validation.
        # There is deliberately NO fallback to it — without a TaskPlan-bound
        # provider we skip LLM planning and take the deterministic skeleton
        # below, exactly as the no-provider path does.
        plan_call_fn = make_structured_call_fn(
            TaskPlan, model=planner_model, provider=planner_provider,
        )

    if plan_call_fn is not None:
        job, plan_label = _first_pass_task_plan(
            mission, intake_result, plan_call_fn, prompt_traces, project, repo,
            target_repo_path, job_file_sha256, run_unattended, scope_order or mission)

    if job is None:
        if deterministic_tasks is not None:
            tasks = list(deterministic_tasks)
        else:
            plans = deterministic_job_plans(mission)
            if len(plans) > 1:
                raise OrderJobPlanError(
                    f"the order names {sum(len(p) for p in plans)} deliverables, more than "
                    f"one job holds; `remedy do` plans them as {len(plans)} jobs")
            [tasks] = plans
        try:
            validate_deliverable_plan(tasks, allow_empty=deterministic_tasks is not None)
        except DeliverablePlanError as exc:
            raise OrderJobPlanError(f"task plan rejected: {exc}") from exc
        job = JobPlan(
            job_title=mission[:80], mission=mission, user_prompt=mission,
            job_file_sha256=job_file_sha256,
            project_id=str(project.id),
            repo_path=target_repo_path,
            intake=intake_result.value.model_dump(),
            tasks=tasks,
            state=RunState.PLANNED,
        )
        save_job_plan(job)

    if prompt_traces:
        from packages.orchestration.prompt_trace import write_trace_jsonl
        from packages.orchestration.run_log import RunLogWriter
        log = RunLogWriter(job_id=job.job_id)
        try:
            write_trace_jsonl(prompt_traces, log.path.parent / "prompt_trace.jsonl")
        except OSError:
            pass

    from packages.orchestration.project_registry import attach_job, save_project
    attach_job(project, str(job.job_id))
    save_project(project)

    return OrderJobPlan(
        job=job,
        intake_result=intake_result,
        intake_fallback_reason=intake_fallback_reason,
        plan_label=plan_label,
    )


# ---------------------------------------------------------------------------
# The steps. Each returns (status, detail); a skipped or stopped step says why.
# ---------------------------------------------------------------------------


def _step_plan(ctx: DoContext) -> tuple[str, str]:
    """Accept the order as a batch of the repository's one mission, and plan it (D4).

    The mission is the repository's lasting one (DECISION amend1011b D1), found or created
    once; the order is a new batch in it. Before the plan, the contract template forced by
    `--contract`, or else the one proposed from the order, is written onto the mission's
    current-order contract, so the
    planner's criteria are added after it and none of its criteria are dropped
    (DECISION F269 D1 (4)); the detail says whether it was forced or proposed.
    """
    from packages.orchestration.contract_templates import (
        ContractTemplateError,
        propose_contract_template,
        write_template_contract,
    )
    from packages.orchestration.mission_compiler import (
        MissionPlanInProgressError,
        plan_mission,
    )
    from packages.orchestration.mission_contract import ContractError
    from packages.orchestration.mission_state import MissionError, MissionOrder
    from packages.orchestration.repo_mission import accept_order_in_each

    project_id = str(ctx.project.id)
    order = MissionOrder(text=ctx.order, source_path=ctx.order_source_path,
                         source_sha256=ctx.order_source_sha256)
    # DECISION amend1011b D4: the order becomes a batch in the ONE mission of each repository it
    # touches, and in none unless every one can take it (R-1250).
    targets = ctx.projects or [ctx.project]
    try:
        ctx.project_missions.update(accept_order_in_each(
            [(target, ctx.project_repos.get(str(target.id), ctx.repo_root)) for target in targets],
            order, budgets=ctx.budgets))
    except MissionError as exc:
        return DO_STEP_FAILED, f"no order accepted: {exc}"
    ctx.mission_id, ctx.order_id = ctx.project_missions[project_id]

    template, how = ctx.contract_template, "forced by --contract"
    try:
        if template is None:
            template, how = propose_contract_template(ctx.order), "proposed from the order"
        if template is not None:
            for target in targets:
                write_template_contract(str(target.id), ctx.project_missions[str(target.id)][0],
                                        template)
    except (ContractTemplateError, ContractError, MissionError) as exc:
        return DO_STEP_FAILED, f"mission {ctx.mission_id} was not planned: {exc}"
    contract_note = (f"contract template {template}, {how}" if template is not None
                     else "no contract template, none proposed from the order")

    call_fn = None
    from packages.orchestration.intake import resolve_planner_target

    planner_name, _ = resolve_planner_target(ctx.planner_provider, ctx.planner_model)
    lane = settle_do_lane(ctx)
    if not ctx.no_llm and not lane.bounded:
        from packages.orchestration.intake import make_structured_call_fn
        from packages.orchestration.mission_plan_schema import MissionPlanDraft

        call_fn = make_structured_call_fn(
            MissionPlanDraft, model=ctx.planner_model,
            provider=ctx.planner_provider,
        )
    try:
        # Named exactly as `mission plan` names it, and named HONESTLY: the
        # planner that actually served is resolved through the one function
        # that decides it, so the record cannot say "ollama" of a Claude CLI
        # run (amend0920-selfuse-real, DECISION D1). Without a provider the
        # compiler plans deterministically.
        outcome = plan_mission(project_id, ctx.mission_id, call_fn, repo_root=ctx.repo_root,
                               provider=planner_name, provider_kind=planner_name)
    except (MissionPlanInProgressError, MissionError) as exc:
        return DO_STEP_FAILED, f"mission {ctx.mission_id} was not planned: {exc}"
    kept_note = ""
    if call_fn is not None:
        outcome, kept_note = _deterministic_plan_for_invented_scope(ctx, project_id, outcome, planner_name)
    ctx.mission_plan = outcome.plan
    ctx.mission_plan_path = str(outcome.plan_path)
    return DO_STEP_DONE, (
        f"mission {ctx.mission_id} plan v{outcome.version} ({outcome.source}, "
        f"{len(outcome.plan.milestones)} milestone(s)): {outcome.plan_path}; "
        f"lane: {lane.lane} ({lane.reason}){kept_note}; {contract_note}")


def _deterministic_plan_for_invented_scope(
        ctx: DoContext, project_id: str, outcome: Any, planner_name: str) -> tuple[Any, str]:
    """``(outcome, note)``: the planner's plan, or the deterministic one when it names files the order did not.

    Amend1014 D6: the guard is this comparison, not the prompt's wording. The plan that invented
    scope stays on disk as the previous version; the deterministic plan names only the order's
    own deliverables. ``note`` is "" when the planner's plan is kept.
    """
    from packages.orchestration.do_lane import tracked_repo_files
    from packages.orchestration.do_scope import mission_plan_text, order_scope_violations
    from packages.orchestration.mission_compiler import plan_mission

    invented = order_scope_violations(
        ctx.order, mission_plan_text(outcome.plan), tracked_repo_files(ctx.repo_root))
    if not invented:
        return outcome, ""
    kept = plan_mission(project_id, ctx.mission_id, None, provider=planner_name, provider_kind=planner_name,
                        repo_root=ctx.repo_root)
    return kept, (f"; the planner's plan named files the order did not request ({', '.join(invented)}), "
                  f"so the deterministic plan of the order's own deliverables was kept")


def _stop_unrun_shape_jobs(ctx: DoContext) -> str:
    """Stop the jobs a failed shape step already planned; the note for the step's detail.

    DECISION amend1011 D2: an order whose shape step fails leaves no job
    ``planned``. Each job the step saved before the failure is stopped, and the
    walk no longer lists it among its ``job_ids``, so a client that follows the
    first job never waits on a job that will not run. The stopped jobs stay on
    disk and leave their missions' chains (R-1247); the note names them.
    """
    from datetime import datetime, timezone

    from packages.orchestration.pingpong_job import JOB_STOPPED, load_job_plan, save_job_plan
    from packages.orchestration.repo_mission import unlink_order_jobs

    stopped: list[str] = []
    for job_id in ctx.job_ids:
        job = load_job_plan(job_id)
        if job is None:
            continue
        job.state = JOB_STOPPED
        job.stop_reason = "shape_failed"
        job.finished_at = datetime.now(timezone.utc).isoformat()
        save_job_plan(job)
        stopped.append(job_id)
    for project_id, (mission_id, _order_id) in ctx.project_missions.items():
        unlink_order_jobs(project_id, mission_id, stopped)
    ctx.job_ids.clear()
    if not stopped:
        return ""
    return f"; stopped the job(s) planned before it failed, none of them runs: {', '.join(stopped)}"


def _step_shape(ctx: DoContext) -> tuple[str, str]:
    """Read the shape from the plan (or a force flag) and plan its jobs, linked to the mission (D5).

    As each job is linked, it records the milestone whose ``jobs_draft`` it
    came from (``_shape_job_orders``), and its contract slice is merged into
    its DoD (DECISION F269 D6 (3)): the whole-mission criteria and that
    milestone's criteria, whose checks the job's gate reports and never holds
    on (D6 (1); ``hold_on_milestone=False``) — so the job's own gate evaluates
    the planner's criterion of the milestone it serves and reads it `met` or
    `unmet` onto the contract (R-0977).  A job of a plan with several
    milestones that came from no outline (``--force-job``) serves none, and
    its milestones' criteria stay `open`.
    Beside that merge, the contract binds the job to its repository and
    grants it (DECISION F269 D7).
    """
    from packages.orchestration.mission_contract import (
        grant_contract_job_repository,
        merge_contract_slice_into_dod,
        record_job_milestone,
    )
    from packages.orchestration.order_verification import require_order_tests
    from packages.orchestration.repo_mission import link_order_job
    from packages.orchestration.scope_question import ScopeQuestionRaised

    lane = settle_do_lane(ctx)
    try:
        shape, source = resolve_do_shape(ctx.mission_plan, force_job=ctx.force_job,
                                         force_mission=ctx.force_mission,
                                         projects=len(ctx.projects), bounded=lane.bounded)
    except ValueError as exc:
        return DO_STEP_FAILED, str(exc)
    ctx.shape, ctx.shape_source = shape, source

    shaped_jobs: list[OrderJobPlan] = []
    planned = _shape_job_orders(ctx, shape)
    for order, tasks, milestone_id, target in planned:
        try:
            shaped = plan_order_job(
                order,
                project=target.project,
                repo_path=target.repo,
                no_llm=ctx.no_llm or lane.bounded,
                run_unattended=ctx.run_unattended,
                deterministic_tasks=tasks,
                planner_model=ctx.planner_model,
                planner_provider=ctx.planner_provider,
                scope_order=ctx.order,
            )
        except ScopeQuestionRaised as exc:
            ctx.next_lines.append(exc.answer_command)
            return DO_STEP_STOPPED, str(exc) + _stop_unrun_shape_jobs(ctx)
        except OrderJobPlanError as exc:
            return DO_STEP_FAILED, str(exc) + _stop_unrun_shape_jobs(ctx)
        if lane.bounded and not ctx.no_llm:
            shaped.intake_fallback_reason = "bounded"
        job_id = str(shaped.job.job_id)
        name_do_job(shaped.job, order, ctx.order, target, several=len(planned) > 1)
        # DECISION amend1011b D4: the job joins the mission of ITS repository, under this order.
        target_mission, target_order = ctx.project_missions[str(target.project.id)]
        mission = link_order_job(str(target.project.id), target_mission, target_order, job_id)
        if milestone_id is not None and str(target.project.id) == str(ctx.project.id):
            record_job_milestone(job_id, milestone_id)
        merge_contract_slice_into_dod(mission, milestone_id, job_id, hold_on_milestone=False)
        require_order_tests(job_id, ctx.order)     # exec-1017 D2: a test run the order asks for blocks
        grant_contract_job_repository(mission, job_id)
        ctx.job_ids.append(job_id)
        shaped_jobs.append(shaped)

    first = shaped_jobs[0]
    if len(shaped_jobs) == 1:
        return DO_STEP_DONE, (
            f"one job {ctx.job_ids[0]} linked to mission {ctx.mission_id} "
            f"(shape: {shape}, from {source}): {len(first.job.tasks)} task(s), "
            f"plan: {first.plan_label}, {first.intake_label}")
    jobs = ", ".join(f"{str(s.job.job_id)} ({len(s.job.tasks)} task(s))" for s in shaped_jobs)
    return DO_STEP_DONE, (
        f"{len(shaped_jobs)} jobs linked to mission {ctx.mission_id} "
        f"(shape: {shape}, from {source}): {jobs}; "
        f"plan: {first.plan_label}, {first.intake_label}")

def _step_run(ctx: DoContext) -> tuple[str, str]:
    """Run the walk's jobs; without a commit flag only the first, and the rest wait (F268 D12).

    Without a commit flag a follow-up job's workspace would be cut from the
    target's HEAD, which an apply does not move, so it runs only once its
    predecessor's applied output is committed; the apply step prints how.
    Under a commit flag every job runs, and each job before the last is
    applied and committed before the next is cut (DECISION F270 D4 (2)); a
    walk that stops here says what it committed and that nothing was pushed.
    """
    status, detail = _run_the_walks_jobs(ctx)
    if status in DO_WALK_ENDING_STATUSES and ctx.commit_mode and not ctx.plan_only:
        detail += do_stopped_walk_note(ctx)
    return status, detail


def _run_the_walks_jobs(ctx: DoContext) -> tuple[str, str]:
    from packages.orchestration.job_plan import task_plan_blocks_execution
    from packages.orchestration.pingpong_job import JOB_COMPLETED, JOB_STOPPED, load_job_plan, run_job

    if ctx.plan_only:
        if ctx.rehearse:
            return stop_walk_for_rehearsal(ctx)
        ctx.next_lines.extend(f"remedy job run {job_id}{_job_run_role_flags(ctx)}"
                              for job_id in ctx.job_ids)
        return DO_STEP_STOPPED, (
            f"--plan-only: no job was run; {len(ctx.job_ids)} job(s) planned, "
            f"mission plan: {ctx.mission_plan_path}")

    # DECISION F270 D4 (2): a commit flag lets every job run, each cut from a HEAD
    # that holds its predecessor's committed output.
    chain = bool(ctx.commit_mode)
    ledger = ctx.ledger = ctx.ledger or OrderCallLedger(caps=ctx.budgets)
    ctx.waiting_job_ids = [] if chain else list(ctx.job_ids[1:])
    record_job_waits(ctx.job_ids, ctx.waiting_job_ids)    # a client reads what each one waits for
    ran: list[str] = []
    for position, job_id in enumerate(ctx.run_job_ids, start=1):
        done_so_far = "; ".join(ran) or "no job has run yet"
        if not do_step_by_step_halt(
                ctx, done_so_far, f"run job {job_id} ({position} of {len(ctx.job_ids)})"):
            return DO_STEP_STOPPED, f"{ctx.halt_reason}; ran before the halt: {done_so_far}"
        job = load_job_plan(job_id)
        if job is None:
            return DO_STEP_FAILED, f"job {job_id} was not found in the job store"
        if not job.repo_path:
            # Without a target a run would fall back to copying the process's
            # working directory, which is never the repository `do` was asked about.
            return DO_STEP_FAILED, f"job {job_id} has no target repository; nothing was run"
        if job.state == JOB_STOPPED:
            # amend1016s D1: a stop ends a job that never started at once; the walk never resumes it.
            return DO_STEP_STOPPED, f"job {job_id} was stopped before it ran; ran before it: {done_so_far}"

        blocked = task_plan_blocks_execution(job)
        if blocked == "pending" and ctx.confirm_plan is not None and ctx.confirm_plan(job):
            approve_confirmed_plan(job)
            blocked = task_plan_blocks_execution(job)
        if blocked is not None:
            approve = f"remedy decision resolve {job_id} plan:approval --reason approve"
            ctx.next_lines.append(approve)
            ctx.next_lines.append(f"remedy job run {job_id}{_job_run_role_flags(ctx)}")
            return DO_STEP_STOPPED, (
                f"job {job_id}'s task plan is {blocked}, not approved; it was not run "
                f"(--run-unattended runs a generated plan without asking). Approve it with: {approve}")

        # Scale audit P1-4: the caps are the ORDER's. A job runs with what the planning calls and the
        # jobs before it left, and none starts once nothing is left.
        if (spent := ledger.exhausted()):
            ctx.next_lines.append(f"remedy job run {job_id}{_job_run_role_flags(ctx)}")
            return DO_STEP_STOPPED, (f"job {job_id} was not run: {spent}; "
                                     f"ran before it: {done_so_far}")
        done = run_job(job_id, builder_name=ctx.builder_provider,
                       reviewer_name=ctx.reviewer_provider,
                       builder_model=ctx.builder_model,
                       reviewer_model=ctx.reviewer_model,
                       budgets=ledger.remaining())
        ledger.record_job(done)
        # DECISION F268 D11: the job's cost reaches the F103 ledger exactly as
        # `job run` sends it there; never fatal, a failure is named in the summary.
        from packages.orchestration.job_evidence import mirror_job_run_into_ledger
        ctx.cost_mirrors[job_id] = mirror_job_run_into_ledger(job_id)
        ctx.next_lines.append(f"remedy job show {job_id}")
        # amend1015f D22: the face reads a job through the serve supervisor's public API.
        if "remedy serve start" not in ctx.next_lines:
            ctx.next_lines.append("remedy serve start")
        ctx.next_lines.append(f"remedy client story {job_id}")
        if done.state != JOB_COMPLETED:
            reason = f": {done.error}" if done.error else ""
            return DO_STEP_FAILED, (f"job {job_id} ended {done.state.value}{reason}"
                                    f"{budget_stop_walk_note(ctx, done)}")
        ran.append(f"job {job_id} ran {len(done.tasks)} task(s) to {done.state.value}")
        if chain and position < len(ctx.job_ids):
            failure = do_apply_one_job(ctx, job_id)
            if failure:
                return DO_STEP_FAILED, f"{failure}; ran before it: {'; '.join(ran)}"
            ran.append(f"{ctx.applied[job_id]} before the next job ran")
    if ctx.waiting_job_ids:
        reserve_waiting_budgets(ctx.waiting_job_ids, ledger.remaining(), ledger.exhausted())
        ran.append(
            f"job(s) {', '.join(ctx.waiting_job_ids)} wait: each runs only once the job "
            f"before it is applied and committed, because a job's workspace is cut from "
            f"{'its own repository' if ctx.projects else ctx.repo_root}'s HEAD commit "
            f"(DECISION F268 D12)")
    return DO_STEP_DONE, "; ".join(ran)


#: The step table. `walk_do_sequence` reaches a step only through this mapping.
DO_STEP_TABLE: dict[str, DoStep] = {
    "init": _step_init,
    "study": do_step_study,
    "plan": _step_plan,
    "shape": _step_shape,
    "run": _step_run,
    "apply": _step_apply,
}
