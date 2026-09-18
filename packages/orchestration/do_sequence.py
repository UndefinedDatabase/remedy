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
mission record for the order, plans it and keeps the plan (D4, D5); shape reads
"one job" or "milestones" from that plan, `--force-job` / `--force-mission`
overriding it, and plans the jobs, each bounded by deliverables (D5, D6); run
runs the first job on the chosen providers; ui opens the cockpit for the job
that ran as a detached process unless `--no-ui`; apply stops before apply and
prints the apply command for the job that ran, unless `--apply`, which applies
it (DECISION F268 D9).

DECISION F268 D12 (amending D10): in a walk of two or more jobs only the first
runs. Every other job waits, because a job's workspace is cut from the target's
HEAD commit and an apply does not commit, so a follow-up job run now could not
see its predecessor's output. `do` names the waiting jobs, and for each prints
the `remedy job run` command to use once its predecessor's applied output is
committed. Chaining them inside one `do` needs F270's `--commit` family.

DECISION F268 D11: run mirrors each job it ran into the F103 ledger, as `job run`
does, and `do_cost_summary` reads the measured tokens per role and cost back
through `token_ledger.query_cost`.

DECISION F268 D8: `--step-by-step` halts after every step that did work and,
inside run, before each job — points where no provider call is in flight — and
reads one line through the context's `read_line`; `q` or end of input stops the
walk and asks every job of the walk to stop through `safe_points.request_stop`.
`--plan-only` ends the walk after shape: run reports stopped and runs no job.
"""

from __future__ import annotations

import json
import shlex
import subprocess
import sys
import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from packages.orchestration.pingpong_job import JobPlan, TaskEntry
    from packages.orchestration.project_registry import RemyProject

#: The sequence, as data (DECISION F268 D4). The walker reads nothing else.
DO_SEQUENCE: tuple[str, ...] = ("init", "study", "plan", "shape", "run", "ui", "apply")

#: The two shapes (DECISION F268 D5), and where the one in force came from.
DO_SHAPE_ONE_JOB = "one job"
DO_SHAPE_MILESTONES = "milestones"
DO_SHAPE_SOURCE_PLANNER = "planner"
DO_SHAPE_SOURCE_FORCE_JOB = "--force-job"
DO_SHAPE_SOURCE_FORCE_MISSION = "--force-mission"

DO_STEP_DONE = "done"
DO_STEP_SKIPPED = "skipped"
DO_STEP_STOPPED = "stopped"
DO_STEP_FAILED = "failed"

#: A step reporting one of these ends the walk; later steps are not called.
DO_WALK_ENDING_STATUSES = frozenset({DO_STEP_STOPPED, DO_STEP_FAILED})


@dataclass(frozen=True)
class DoStepResult:
    """What one step did: its name, a status word and a sentence with real ids."""

    name: str
    status: str
    detail: str

    def to_json(self) -> dict[str, str]:
        return {"name": self.name, "status": self.status, "detail": self.detail}


@dataclass
class DoContext:
    """Everything one `remedy do` walk carries from step to step."""

    order: str
    repo: str = "."
    builder_provider: str | None = None
    reviewer_provider: str | None = None
    #: `--project <slug-or-id>`: the init step selects this project instead of
    #: resolving or registering the repository (DECISION F268 D16 (4)).
    project_selector: str | None = None
    #: The resolved `JobBudgets` as a dict, set only when a budget flag was given;
    #: the run step passes it to `run_job` as `job run` does (DECISION F268 D16 (5)).
    budgets: dict[str, Any] | None = None
    builder_model: str | None = None
    reviewer_model: str | None = None
    #: `--planner-model`: `model=` of every structured planner call the plan and
    #: shape steps build (DECISION F268 D16 (7)).
    planner_model: str | None = None
    no_ui: bool = False
    yes: bool = False
    no_llm: bool = False
    force_job: bool = False
    force_mission: bool = False
    step_by_step: bool = False
    plan_only: bool = False
    #: `--apply`: the apply step applies every job instead of stopping (DECISION F268 D9).
    apply: bool = False
    #: Reads one line at a `--step-by-step` halt, raising `EOFError` at end of
    #: input like `input`, which the CLI supplies; ``None`` reads as end of input.
    read_line: Callable[[], str] | None = None
    #: Opens the cockpit for a job id and returns its URL, raising
    #: `DoCockpitLaunchError` when it does not come up; the CLI supplies
    #: `launch_do_cockpit`. ``None`` opens nothing and prints the command.
    ui_launcher: Callable[[str], str] | None = None
    #: Why a `--step-by-step` halt stopped the walk; "" while it has not.
    halt_reason: str = ""
    repo_root: str = ""
    project: RemyProject | None = None
    mission_id: str = ""
    mission_plan: Any = None
    mission_plan_path: str = ""
    shape: str = ""
    shape_source: str = ""
    job_ids: list[str] = field(default_factory=list)
    #: The jobs of a multi-job walk the run step did not run: each waits for its
    #: predecessor's applied output to be committed (DECISION F268 D12).
    waiting_job_ids: list[str] = field(default_factory=list)
    #: Each job the run step ran → `mirror_job_run_into_ledger`'s answer for it (DECISION F268 D11).
    cost_mirrors: dict[str, dict[str, Any]] = field(default_factory=dict)
    results: list[DoStepResult] = field(default_factory=list)
    next_lines: list[str] = field(default_factory=list)

    @property
    def run_job_ids(self) -> list[str]:
        """The walk's jobs that are not waiting, in job order: the ones run, ui and apply act on."""
        return [job_id for job_id in self.job_ids if job_id not in self.waiting_job_ids]

    @property
    def failed(self) -> bool:
        return any(r.status == DO_STEP_FAILED for r in self.results)

    @property
    def stopped_before_apply(self) -> bool:
        """True unless the apply step itself ran to completion."""
        return not any(r.name == "apply" and r.status == DO_STEP_DONE
                       for r in self.results)


#: A step takes the context and returns ``(status, detail)``; the walker names it.
DoStep = Callable[[DoContext], tuple[str, str]]


def walk_do_sequence(ctx: DoContext,
                     table: Mapping[str, DoStep] | None = None) -> DoContext:
    """Call each step of `DO_SEQUENCE` through the table, in order, until one ends the walk.

    With `--step-by-step`, a step that did work is followed by a halt before the
    next step (DECISION F268 D8); a halt that stops reports the next step stopped.
    """
    steps = DO_STEP_TABLE if table is None else table
    for index, name in enumerate(DO_SEQUENCE):
        status, detail = steps[name](ctx)
        ctx.results.append(DoStepResult(name=name, status=status, detail=detail))
        if status in DO_WALK_ENDING_STATUSES:
            break
        if status != DO_STEP_DONE or index + 1 == len(DO_SEQUENCE):
            continue
        coming = DO_SEQUENCE[index + 1]
        if not do_step_by_step_halt(ctx, f"{name}: {detail}", f"the {coming} step"):
            ctx.results.append(DoStepResult(
                name=coming, status=DO_STEP_STOPPED,
                detail=f"not run: {ctx.halt_reason}"))
            break
    return ctx


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
    print(f"[step-by-step] done: {done}", file=sys.stderr)
    print(f"[step-by-step] next: {coming}. Enter continues, "
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


#: The plan label of a job planned without an LLM task plan (DECISION F268 D6).
DO_DETERMINISTIC_PLAN_LABEL = "deterministic, one task per deliverable"


class OrderJobPlanError(Exception):
    """The task plan for an order could not be generated; the job is left unplanned."""


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


def plan_order_job(
    order: str,
    *,
    project: RemyProject,
    repo_path: str = "",
    no_llm: bool = False,
    yes: bool = False,
    deterministic_tasks: list[TaskEntry] | None = None,
    planner_model: str | None = None,
) -> OrderJobPlan:
    """Plan ONE job for an order: intake, then an LLM task plan or the deterministic one.

    ``repo_path`` is the job's target repository. ``yes`` auto-approves an LLM
    task plan through ``job_plan.auto_approve_task_plan`` (F034). The job is
    saved and attached to ``project``. The deterministic plan is one task per
    deliverable of the order (DECISION F268 D6); ``deterministic_tasks`` names
    the job's tasks outright and skips the LLM task plan, which is how the
    shape step plans a job per deliverable or per job-sized slice of them.
    Every plan, LLM or deterministic, passes the deliverable validator.
    ``planner_model`` is ``model=`` of the intake and task-plan calls
    (DECISION F268 D16 (7)); omitted, the planner's configured model serves.
    Raises :class:`OrderJobPlanError` when an LLM task plan cannot be parsed
    (after writing the job's post-mortem), when a plan fails the validator,
    or when the order names more deliverables than one job holds.
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
        record_llm_task_deliverables,
        validate_deliverable_plan,
    )

    mission = order
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
        if planner_model:
            from packages.orchestration.intake import make_structured_call_fn
            from packages.orchestration.schemas import JobIntake
            call_fn = make_structured_call_fn(JobIntake, model=planner_model)
        else:
            call_fn = make_provider_call_fn()
        if call_fn is not None:
            intake_composed = compose_intake_prompt(mission)
            intake_result = run_intake(
                mission,
                call_fn,
                composed=intake_composed,
                on_call=make_intake_call_recorder(
                    prompt_traces,
                    intake_composed,
                    provider="ollama",
                    provider_kind="ollama",
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
        plan_call_fn = make_structured_call_fn(TaskPlan, model=planner_model)

    if plan_call_fn is not None:
        from packages.orchestration.job_plan import (
            apply_plan_budgets,
            apply_plan_fences,
            compose_task_plan_prompt,
            make_task_plan_call_recorder,
            map_task_plan_to_tasks,
            plan_job_llm,
            write_plan_md,
        )
        plan_intake_dict = intake_result.value.model_dump()
        # Composed exactly ONCE here and handed to `plan_job_llm`, so the bytes
        # the provider receives and the manifest the trace records come from the
        # same composition — `prompt_chars` and `segment_manifest_chars` can no
        # longer describe two different prompts (R-0256).
        plan_composed = compose_task_plan_prompt(plan_intake_dict)
        fp_result = plan_job_llm(
            plan_intake_dict,
            plan_call_fn,
            composed=plan_composed,
            on_call=make_task_plan_call_recorder(
                prompt_traces,
                plan_composed,
                provider="ollama",
                provider_kind="ollama",
            ),
        )
        if fp_result.plan is not None:
            fp_dict = fp_result.plan.model_dump()
            fp_dict["_approval"] = "pending"
            fp_dict["_normalization"] = fp_result.transformations
            tasks = map_task_plan_to_tasks(fp_result.plan)
            record_llm_task_deliverables(tasks)
            try:
                validate_deliverable_plan(tasks)
            except DeliverablePlanError as exc:
                raise OrderJobPlanError(f"task plan rejected: {exc}") from exc
            from packages.core.models import JobBudgets, JobFences
            from packages.orchestration.budget_resolution import resolve_job_budgets
            config_budgets = resolve_job_budgets(project_root=repo)
            config_budgets_dict = config_budgets.model_dump(exclude_none=True) if config_budgets else None
            merged_budgets = apply_plan_budgets(config_budgets_dict, fp_result.plan.budgets)
            merged_fences = apply_plan_fences(None, fp_result.plan.fences)
            job_budgets = None
            if merged_budgets:
                try:
                    job_budgets = JobBudgets(**{
                        k: v for k, v in merged_budgets.items()
                        if k in JobBudgets.model_fields})
                except Exception:
                    pass
            job_fences = None
            if merged_fences:
                try:
                    job_fences = JobFences(**{
                        k: v for k, v in merged_fences.items()
                        if k in JobFences.model_fields})
                except Exception:
                    pass
            job = JobPlan(
                job_title=mission[:80], mission=mission, user_prompt=mission,
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
            if yes:
                # F034: --yes covers approval AND clarifications. Every open
                # question runs on its documented default, recorded in the
                # assumption log — unattended, but never silent. The semantics
                # live in job_plan.auto_approve_task_plan so the
                # orchestrator loop runs the SAME approval, not a copy of it.
                from packages.orchestration.job_plan import auto_approve_task_plan
                fp_dict = auto_approve_task_plan(
                    fp_dict, job_evidence_export_dir(str(job.job_id)))
                job.task_plan = fp_dict
                save_job_plan(job)
                plan_label = (
                    f"task plan {fp_result.plan.schema_v} (approved via --yes)"
                )
            else:
                plan_label = (
                    f"task plan {fp_result.plan.schema_v} (awaiting approval)"
                )
        else:
            job = JobPlan(
                job_title=mission[:80], mission=mission, user_prompt=mission,
                project_id=str(project.id),
                repo_path=target_repo_path,
                intake=intake_result.value.model_dump(),
                state=RunState.PENDING,
            )
            save_job_plan(job)
            from packages.orchestration.data_paths import job_evidence_export_dir
            from packages.orchestration.failure_postmortem import (
                FailureSignals,
                build_job_rollup,
                write_postmortem,
            )
            signals = FailureSignals(
                error_class="parse",
                error_text=fp_result.error_hint or "task plan parse failure",
            )
            pm = build_job_rollup(job_id=str(job.job_id), signals=signals)
            ev_dir = job_evidence_export_dir(str(job.job_id))
            ev_dir.mkdir(parents=True, exist_ok=True)
            try:
                write_postmortem(ev_dir, pm, root=ev_dir)
            except Exception as exc:
                print(f"Warning: postmortem write failed: {exc}", file=sys.stderr)
            raise OrderJobPlanError(
                f"task plan generation failed: "
                f"{fp_result.error_hint or 'parse failure'}"
            )

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
            validate_deliverable_plan(tasks)
        except DeliverablePlanError as exc:
            raise OrderJobPlanError(f"task plan rejected: {exc}") from exc
        job = JobPlan(
            job_title=mission[:80], mission=mission, user_prompt=mission,
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


def _step_init(ctx: DoContext) -> tuple[str, str]:
    """Register the repository if it is not, and add the ignore entries (D2). Nothing else.

    With `--project` the project is selected through `select_project` instead,
    and an unknown one fails the step (DECISION F268 D16 (4)).
    """
    from packages.orchestration.project_registry import (
        InvalidProjectSelectorError,
        ProjectNotFoundError,
        register_project_repo,
        resolve_project,
        select_project,
    )
    from packages.orchestration.repo_ignore import ensure_ignore_entry, ignore_entries
    from packages.orchestration.worktrees import WorktreeError, repo_root

    try:
        root = repo_root(ctx.repo)
    except (WorktreeError, OSError, subprocess.SubprocessError):
        return DO_STEP_FAILED, (
            f"{Path(ctx.repo).resolve()} is not a git repository — run `git init` first")
    ctx.repo_root = str(root)

    if ctx.project_selector is not None:
        try:
            project, _source = select_project(ctx.project_selector, root)
        except (ProjectNotFoundError, InvalidProjectSelectorError):
            return DO_STEP_FAILED, (
                f"no project matches --project {ctx.project_selector!r}; "
                f"list them with: remedy project list")
        detail = f"project {project.slug} ({project.id}) selected by --project"
    elif (project := resolve_project(root)) is None:
        project = register_project_repo(root.name, root)
        detail = f"registered {root} as project {project.slug} ({project.id})"
    else:
        detail = f"project {project.slug} ({project.id}) already registered for {root}"
    ctx.project = project
    for entry in ignore_entries(root):
        ensure_ignore_entry(root, entry)
    return DO_STEP_DONE, detail


def _repo_has_committed_file(repo_root: str) -> bool:
    """At least one commit exists and HEAD holds at least one tracked file."""
    proc = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", "HEAD"],
        cwd=repo_root, capture_output=True, text=True, timeout=30,
    )
    return proc.returncode == 0 and bool(proc.stdout.strip())


def _step_study(ctx: DoContext) -> tuple[str, str]:
    """Study the repository exactly once, and only when it is non-empty (D3)."""
    from packages.orchestration.study import (
        record_study_pass,
        run_study,
        study_call_fn,
    )

    metadata = ctx.project.metadata
    if metadata.get("studied_at"):
        return DO_STEP_SKIPPED, (
            f"already studied at {metadata['studied_at']} "
            f"(head {metadata.get('studied_head') or 'none'}); study again by hand: "
            f"remedy study run --path {shlex.quote(ctx.repo_root)}")
    if not _repo_has_committed_file(ctx.repo_root):
        return DO_STEP_SKIPPED, (
            f"{ctx.repo_root} has no commit holding a tracked file — nothing to study")

    call_fn = None if ctx.no_llm else study_call_fn()
    result = run_study(ctx.repo_root, project_id=str(ctx.project.id), call_fn=call_fn)
    updated = record_study_pass(str(ctx.project.id), ctx.repo_root)
    if updated is not None:
        ctx.project = updated
    detail = f"{len(result.cards_written)} memory card(s) written for project {ctx.project.slug}"
    if result.partial:
        detail += f" (PARTIAL — {result.stopped_reason})"
    return DO_STEP_DONE, detail


def _step_plan(ctx: DoContext) -> tuple[str, str]:
    """Create the mission record for the order, record the order, and plan it (D4)."""
    from packages.orchestration.mission_compiler import (
        MissionPlanInProgressError,
        plan_mission,
    )
    from packages.orchestration.mission_state import (
        MissionError,
        MissionOrder,
        create_mission,
        set_mission_order,
    )

    project_id = str(ctx.project.id)
    try:
        mission = create_mission(project_id, ctx.order)
        set_mission_order(project_id, mission.id, MissionOrder(text=ctx.order))
    except MissionError as exc:
        return DO_STEP_FAILED, f"no mission created: {exc}"
    ctx.mission_id = mission.id

    call_fn = None
    if not ctx.no_llm:
        from packages.orchestration.intake import make_structured_call_fn
        from packages.orchestration.mission_plan_schema import MissionPlanDraft

        call_fn = make_structured_call_fn(MissionPlanDraft, model=ctx.planner_model)
    try:
        # Named exactly as `mission plan` names it: `make_structured_call_fn` is
        # Ollama-backed. Without a provider the compiler plans deterministically.
        outcome = plan_mission(project_id, mission.id, call_fn,
                               provider="ollama", provider_kind="ollama")
    except (MissionPlanInProgressError, MissionError) as exc:
        return DO_STEP_FAILED, f"mission {mission.id} was not planned: {exc}"
    ctx.mission_plan = outcome.plan
    ctx.mission_plan_path = str(outcome.plan_path)
    return DO_STEP_DONE, (
        f"mission {mission.id} plan v{outcome.version} ({outcome.source}, "
        f"{len(outcome.plan.milestones)} milestone(s)): {outcome.plan_path}")


def mission_plan_outlines(plan: Any) -> list[Any]:
    """Every `jobs_draft` outline across the plan's milestones, in milestone order."""
    if plan is None:
        return []
    return [outline for milestone in plan.milestones for outline in milestone.jobs_draft]


def do_shape_of_plan(plan: Any) -> str:
    """The planner's shape (DECISION F268 D5): two or more outlines are milestones."""
    return DO_SHAPE_MILESTONES if len(mission_plan_outlines(plan)) >= 2 else DO_SHAPE_ONE_JOB


def resolve_do_shape(plan: Any, *, force_job: bool = False,
                     force_mission: bool = False) -> tuple[str, str]:
    """``(shape, shape_source)``: a force flag wins over the plan; both at once is refused."""
    if force_job and force_mission:
        raise ValueError("--force-job and --force-mission cannot be given together")
    if force_job:
        return DO_SHAPE_ONE_JOB, DO_SHAPE_SOURCE_FORCE_JOB
    if force_mission:
        return DO_SHAPE_MILESTONES, DO_SHAPE_SOURCE_FORCE_MISSION
    return do_shape_of_plan(plan), DO_SHAPE_SOURCE_PLANNER


def _shape_job_orders(ctx: DoContext, shape: str) -> list[tuple[str, list[TaskEntry] | None]]:
    """What to plan, one ``(order, deterministic_tasks)`` per job; ``None`` lets the planner choose."""
    from packages.orchestration.task_deliverables import (
        deliverable_check_task,
        deliverable_task,
        deterministic_job_plans,
        extract_order_deliverables,
    )

    order = ctx.order
    if shape == DO_SHAPE_ONE_JOB:
        slices = deterministic_job_plans(order)
        if len(slices) == 1:
            return [(order, None)]
        return [(order, tasks) for tasks in slices]
    outlines = mission_plan_outlines(ctx.mission_plan)
    if len(outlines) >= 2:
        return [(outline.goal, None) for outline in outlines]
    deliverables = extract_order_deliverables(order)
    if len(deliverables) >= 2:
        return [(order, [deliverable_task(d, order)]) for d in deliverables]
    [only] = deliverables
    return [(order, [deliverable_task(only, order)]),
            (order, [deliverable_check_task(only, order)])]


def _step_shape(ctx: DoContext) -> tuple[str, str]:
    """Read the shape from the plan (or a force flag) and plan its jobs, linked to the mission (D5)."""
    from packages.orchestration.mission_state import (
        MISSION_ROLE_FOLLOW_UP,
        MISSION_ROLE_INITIAL,
        link_job_to_mission,
    )

    try:
        shape, source = resolve_do_shape(ctx.mission_plan, force_job=ctx.force_job,
                                         force_mission=ctx.force_mission)
    except ValueError as exc:
        return DO_STEP_FAILED, str(exc)
    ctx.shape, ctx.shape_source = shape, source

    shaped_jobs: list[OrderJobPlan] = []
    for order, tasks in _shape_job_orders(ctx, shape):
        try:
            shaped = plan_order_job(
                order,
                project=ctx.project,
                repo_path=ctx.repo_root,
                no_llm=ctx.no_llm,
                yes=ctx.yes,
                deterministic_tasks=tasks,
                planner_model=ctx.planner_model,
            )
        except OrderJobPlanError as exc:
            return DO_STEP_FAILED, str(exc)
        job_id = str(shaped.job.job_id)
        role = MISSION_ROLE_FOLLOW_UP if ctx.job_ids else MISSION_ROLE_INITIAL
        link_job_to_mission(str(ctx.project.id), ctx.mission_id, job_id, role=role)
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


def do_job_task_listing(ctx: DoContext) -> list[dict[str, Any]]:
    """Every job of the walk in job order: ``{job_id, tasks: [{title, deliverable}]}``."""
    from packages.orchestration.pingpong_job import load_job_plan
    from packages.orchestration.task_deliverables import task_deliverable

    listing: list[dict[str, Any]] = []
    for job_id in ctx.job_ids:
        job = load_job_plan(job_id)
        tasks = [] if job is None else [
            {"title": task.title, "deliverable": task_deliverable(task)}
            for task in job.tasks]
        listing.append({"job_id": job_id, "tasks": tasks})
    return listing


def _job_run_role_flags(ctx: DoContext) -> str:
    """The role flags every `remedy job run` Next line carries: providers, then models (D16 (6))."""
    flags = ""
    for flag, value in (("--builder-provider", ctx.builder_provider),
                        ("--reviewer-provider", ctx.reviewer_provider),
                        ("--builder-model", ctx.builder_model),
                        ("--reviewer-model", ctx.reviewer_model)):
        if value:
            flags += f" {flag} {shlex.quote(value)}"
    return flags


def _step_run(ctx: DoContext) -> tuple[str, str]:
    """Run the walk's first job on the chosen builder and reviewer; the rest wait (DECISION F268 D12).

    A follow-up job's workspace would be cut from the target's HEAD, which an
    apply does not move, so it runs only once its predecessor's applied output
    is committed; the apply step prints how.
    """
    from packages.orchestration.job_plan import task_plan_blocks_execution
    from packages.orchestration.pingpong_job import JOB_COMPLETED, load_job_plan, run_job

    if ctx.plan_only:
        ctx.next_lines.extend(f"remedy job run {job_id}{_job_run_role_flags(ctx)}"
                              for job_id in ctx.job_ids)
        return DO_STEP_STOPPED, (
            f"--plan-only: no job was run; {len(ctx.job_ids)} job(s) planned, "
            f"mission plan: {ctx.mission_plan_path}")

    ctx.waiting_job_ids = list(ctx.job_ids[1:])
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

        blocked = task_plan_blocks_execution(job)
        if blocked is not None:
            approve = f"remedy decision resolve {job_id} plan:approval --reason approve"
            ctx.next_lines.append(approve)
            ctx.next_lines.append(f"remedy job run {job_id}{_job_run_role_flags(ctx)}")
            return DO_STEP_STOPPED, (
                f"job {job_id}'s task plan is {blocked}, not approved; it was not run "
                f"(--yes approves it unattended). Approve it with: {approve}")

        done = run_job(job_id, builder_name=ctx.builder_provider,
                       reviewer_name=ctx.reviewer_provider,
                       builder_model=ctx.builder_model,
                       reviewer_model=ctx.reviewer_model,
                       budgets=ctx.budgets)
        # DECISION F268 D11: the job's cost reaches the F103 ledger exactly as
        # `job run` sends it there; never fatal, a failure is named in the summary.
        from packages.orchestration.job_evidence import mirror_job_run_into_ledger
        ctx.cost_mirrors[job_id] = mirror_job_run_into_ledger(job_id)
        ctx.next_lines.append(f"remedy job show {job_id}")
        if done.state != JOB_COMPLETED:
            reason = f": {done.error}" if done.error else ""
            return DO_STEP_FAILED, f"job {job_id} ended {done.state.value}{reason}"
        ran.append(f"job {job_id} ran {len(done.tasks)} task(s) to {done.state.value}")
    if ctx.waiting_job_ids:
        ran.append(
            f"job(s) {', '.join(ctx.waiting_job_ids)} wait: each runs only once the job "
            f"before it is applied and committed, because a job's workspace is cut from "
            f"{ctx.repo_root}'s HEAD commit (DECISION F268 D12)")
    return DO_STEP_DONE, "; ".join(ran)


# ---------------------------------------------------------------------------
# The cockpit, opened detached (DECISION F268 D9 (1)).
# ---------------------------------------------------------------------------


#: How long the ui step waits for the detached cockpit to write its info file.
DO_COCKPIT_WAIT_SECONDS = 15.0

#: The stop command the ui step reports; it stops every running UI session.
DO_COCKPIT_STOP_COMMAND = "remedy ui stop"


class DoCockpitLaunchError(Exception):
    """The detached cockpit did not come up; the message says why and where its log is."""


def do_cockpit_argv(job_id: str, info_file: Path | str) -> list[str]:
    """The detached cockpit's command line: `remedy ui start` on an automatic port."""
    return [sys.executable, "-m", "apps.cli.grouped", "ui", "start", job_id,
            "--port", "0", "--info-file", str(info_file)]


def do_cockpit_paths(job_id: str) -> tuple[Path, Path]:
    """``(info_file, log_file)`` under the data root, which init keeps out of `git status`.

    The info file sits in the UI session registry `remedy ui start` itself
    writes to, so `remedy ui status` and `remedy ui stop` see the cockpit.
    """
    from packages.orchestration.data_paths import resolve_data_root

    ui_root = Path(resolve_data_root()) / "ui"
    return ui_root / "sessions" / f"do-{job_id}.json", ui_root / "do_logs" / f"{job_id}.log"


def launch_do_cockpit(
    job_id: str,
    *,
    wait_seconds: float = DO_COCKPIT_WAIT_SECONDS,
    spawn: Callable[..., Any] = subprocess.Popen,
    sleep: Callable[[float], None] = time.sleep,
) -> str:
    """Start the cockpit for *job_id* in its own session and return its URL.

    The child outlives `remedy do`: it runs in a new session with its output in
    a log file. Waits at most ``wait_seconds`` for the info file; a child that
    exits first or does not come up in time raises `DoCockpitLaunchError`
    (a child still starting is terminated, so no half-started server is left).
    """
    info_file, log_file = do_cockpit_paths(job_id)
    info_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    info_file.unlink(missing_ok=True)
    with open(log_file, "ab") as log:
        child = spawn(do_cockpit_argv(job_id, info_file), stdin=subprocess.DEVNULL,
                      stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    deadline = time.monotonic() + wait_seconds
    while True:
        try:
            url = json.loads(info_file.read_text(encoding="utf-8")).get("url", "")
        except (OSError, ValueError):
            url = ""
        if url:
            return url
        code = child.poll()
        if code is not None:
            raise DoCockpitLaunchError(
                f"the cockpit exited with code {code} before it came up; its log: {log_file}")
        if time.monotonic() >= deadline:
            child.terminate()
            raise DoCockpitLaunchError(
                f"the cockpit did not come up within {wait_seconds:g}s; its log: {log_file}")
        sleep(0.1)


def _step_ui(ctx: DoContext) -> tuple[str, str]:
    """Open the cockpit for the last job that ran, detached, unless `--no-ui` (DECISIONs F268 D9, D12)."""
    if ctx.no_ui:
        return DO_STEP_SKIPPED, "--no-ui given; the cockpit was not opened"
    job_id = ctx.run_job_ids[-1]
    command = f"remedy ui start {job_id}"
    if ctx.ui_launcher is None:
        ctx.next_lines.append(command)
        return DO_STEP_SKIPPED, f"no cockpit launcher on this walk; open it with: {command}"
    try:
        url = ctx.ui_launcher(job_id)
    except (DoCockpitLaunchError, OSError) as exc:
        ctx.next_lines.append(command)
        return DO_STEP_SKIPPED, f"the cockpit was not opened: {exc}; open it with: {command}"
    ctx.next_lines.append(DO_COCKPIT_STOP_COMMAND)
    return DO_STEP_DONE, (
        f"the cockpit for job {job_id} is open at {url}; "
        f"stop it with: {DO_COCKPIT_STOP_COMMAND}")


def do_waiting_job_next_lines(ctx: DoContext) -> list[str]:
    """One line per waiting job, with real ids: commit its predecessor's applied output, then run it.

    DECISION F268 D12: a job's workspace is cut from the target's HEAD commit,
    so a waiting job runs only once the job before it is applied AND committed.
    """
    repo = shlex.quote(ctx.repo_root)
    lines = []
    for position, job_id in enumerate(ctx.job_ids):
        if job_id not in ctx.waiting_job_ids:
            continue
        before = ctx.job_ids[position - 1]
        lines.append(f"commit job {before}'s applied output in {repo}, then: "
                     f"remedy job run {job_id}{_job_run_role_flags(ctx)}")
    return lines


def _step_apply(ctx: DoContext) -> tuple[str, str]:
    """Stop before apply, printing the apply command per job that ran; `--apply` applies them.

    With `--apply` each job that ran goes through `job_apply.apply_job(...,
    approve=True)` in run order, and the walk fails at the first job that is not
    applied, naming it and why (DECISION F268 D9 (2)). The apply gate is
    `job_apply`'s own. A waiting job is never applied here; the Next lines say
    how it runs (DECISION F268 D12).
    """
    if not ctx.apply:
        commands = [f"remedy job apply {job_id} --repo {shlex.quote(ctx.repo_root)} --approve"
                    for job_id in ctx.run_job_ids]
        ctx.next_lines.extend(commands)
        ctx.next_lines.extend(do_waiting_job_next_lines(ctx))
        return DO_STEP_STOPPED, (
            f"stopped before apply; {ctx.repo_root} is untouched. "
            f"Apply the reviewed result with: {'; then '.join(commands)}")

    from packages.orchestration.job_apply import apply_job

    applied: list[str] = []
    for job_id in ctx.run_job_ids:
        result = apply_job(job_id, ctx.repo_root, approve=True)
        if result.status != "applied":
            why = result.blocked_reason or "; ".join(result.blocked_reasons) or "no reason given"
            ctx.next_lines.append(f"remedy job apply {job_id} --repo "
                                  f"{shlex.quote(ctx.repo_root)} --dry-run")
            before = f"; applied before it: {'; '.join(applied)}" if applied else ""
            return DO_STEP_FAILED, (
                f"job {job_id} was not applied to {ctx.repo_root} "
                f"(status {result.status}): {why}{before}")
        applied.append(f"job {job_id} applied {len(result.files_applied)} file(s)")
    ctx.next_lines.extend(do_waiting_job_next_lines(ctx))
    return DO_STEP_DONE, f"{'; '.join(applied)} to {ctx.repo_root}"


# ---------------------------------------------------------------------------
# The measured cost of the walk, read from the F103 ledger (DECISION F268 D11).
# ---------------------------------------------------------------------------


def _add_measured(total: float | int | None, value: float | int | None) -> float | int | None:
    """Sum two ledger figures as the ledger's own SUM does: None only when both are None."""
    if value is None:
        return total
    return value if total is None else total + value


def do_mission_contract(ctx: DoContext) -> dict[str, Any] | None:
    """The walk's mission contract body as its record holds it, or None.

    None when the walk created no mission or the mission has no contract
    (DECISION F269 D4 (6)); read from the record, so it is the contract as
    the walk left it.
    """
    if not ctx.mission_id or ctx.project is None:
        return None
    from packages.orchestration.mission_state import load_mission

    body = load_mission(str(ctx.project.id), ctx.mission_id).contract
    return body if isinstance(body, dict) else None


def do_cost_summary(ctx: DoContext) -> dict[str, Any] | None:
    """The walk's measured tokens per role and cost, or None when no job ran.

    Read through `token_ledger.query_cost(..., job_id=<id>, by="role")` for each
    job the run step mirrored, and summed over them; a figure no call reported
    stays None, never 0. A job whose mirror failed is named in
    `mirror_failed_job_ids`, with its error, and contributes nothing.
    """
    if not ctx.cost_mirrors:
        return None
    from packages.orchestration.token_ledger import query_cost

    failed = {job_id: str(mirror.get("error") or "")
              for job_id, mirror in ctx.cost_mirrors.items()
              if not mirror.get("ledger_mirrored")}
    roles: dict[str | None, dict[str, Any]] = {}
    for job_id in ctx.cost_mirrors:
        if job_id in failed:
            continue
        report = query_cost(project_id=str(ctx.project.id), job_id=job_id, by="role")
        for row in report.rows:
            role = roles.setdefault(row.bucket, {
                "role": row.bucket, "calls": 0, "tokens_in": None, "tokens_out": None,
                "cache_read": None, "cost_usd": None})
            role["calls"] += row.calls
            for key in ("tokens_in", "tokens_out", "cache_read", "cost_usd"):
                role[key] = _add_measured(role[key], getattr(row, key))
    cost_usd = None
    for role in roles.values():
        cost_usd = _add_measured(cost_usd, role["cost_usd"])
    return {
        "roles": sorted(roles.values(), key=lambda r: str(r["role"])),
        "cost_usd": cost_usd,
        "job_ids": [job_id for job_id in ctx.cost_mirrors if job_id not in failed],
        "mirror_failed_job_ids": list(failed),
        "mirror_errors": failed,
    }


def _measured(value: float | int | None) -> str:
    return "not reported" if value is None else f"{value}"


def do_cost_summary_lines(summary: dict[str, Any] | None) -> list[str]:
    """The text lines of `do_cost_summary`: one per role, one for the cost, one per failed mirror."""
    if summary is None:
        return []
    lines = [f"Tokens {role['role'] or '(role not named)'}: input {_measured(role['tokens_in'])}, "
             f"output {_measured(role['tokens_out'])}, "
             f"cache read {_measured(role['cache_read'])} ({role['calls']} call(s))"
             for role in summary["roles"]]
    cost = summary["cost_usd"]
    lines.append("Cost: not reported by the provider" if cost is None
                 else f"Cost: ${cost:.6f} (measured, from the ledger)")
    lines.extend(f"Cost NOT recorded to the ledger for job {job_id}: {error}"
                 for job_id, error in summary["mirror_errors"].items())
    return lines


#: The step table. `walk_do_sequence` reaches a step only through this mapping.
DO_STEP_TABLE: dict[str, DoStep] = {
    "init": _step_init,
    "study": _step_study,
    "plan": _step_plan,
    "shape": _step_shape,
    "run": _step_run,
    "ui": _step_ui,
    "apply": _step_apply,
}
