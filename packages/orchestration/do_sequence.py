"""F268 — `remedy do "<order>"` as DATA: the step names, the step table, one walker.

DECISION F268 D4. `DO_SEQUENCE` is the one ordered list of step names; the
table maps each name to its step function; `walk_do_sequence` calls steps only
through that table, only in that order, and ends the walk at the first step
that stops or fails. No step is called from prose-order code, so a later
feature can add a second named list as a lookup rather than a rewrite
(DECISION amend0911-feedback D3).

The module sits under `packages/` rather than `apps/cli/commands/` because its
steps call package functions and must be testable without the CLI.

T001 scope: init registers and ignores and writes no file into the repository
(D2); study runs once, on a non-empty repository only (D3); plan creates the
mission record for the order and plans it (D4); shape yields ONE job linked to
the mission; run runs it on the chosen providers; ui prints the real
`remedy ui start` command unless `--no-ui`; apply always stops before apply.
"""

from __future__ import annotations

import shlex
import subprocess
import sys
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from packages.orchestration.pingpong_job import JobPlan
    from packages.orchestration.project_registry import RemyProject

#: The sequence, as data (DECISION F268 D4). The walker reads nothing else.
DO_SEQUENCE: tuple[str, ...] = ("init", "study", "plan", "shape", "run", "ui", "apply")

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
    no_ui: bool = False
    yes: bool = False
    no_llm: bool = False
    repo_root: str = ""
    project: RemyProject | None = None
    mission_id: str = ""
    job_ids: list[str] = field(default_factory=list)
    results: list[DoStepResult] = field(default_factory=list)
    next_lines: list[str] = field(default_factory=list)

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
    """Call each step of `DO_SEQUENCE` through the table, in order, until one ends the walk."""
    steps = DO_STEP_TABLE if table is None else table
    for name in DO_SEQUENCE:
        status, detail = steps[name](ctx)
        ctx.results.append(DoStepResult(name=name, status=status, detail=detail))
        if status in DO_WALK_ENDING_STATUSES:
            break
    return ctx


# ---------------------------------------------------------------------------
# The shape step's job planning — moved here from `_cmd_do_mission` in
# apps/cli/commands/do_cmd.py (the F147 golden path), not copied.
# ---------------------------------------------------------------------------


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
) -> OrderJobPlan:
    """Plan ONE job for an order: intake, then an LLM task plan or the deterministic skeleton.

    ``repo_path`` is the job's target repository. ``yes`` auto-approves an LLM
    task plan through ``job_plan.auto_approve_task_plan`` (F034). The job is
    saved and attached to ``project``. Raises :class:`OrderJobPlanError` when
    an LLM task plan cannot be parsed, after writing the job's post-mortem.
    """
    from packages.core.models import RunState
    from packages.orchestration.intake import (
        compose_intake_prompt,
        heuristic_intake,
        make_intake_call_recorder,
        make_provider_call_fn,
        run_intake,
    )
    from packages.orchestration.job_runner import plan_job
    from packages.orchestration.pingpong_job import JobPlan, save_job_plan

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
    plan_label = "deterministic skeleton"

    plan_call_fn = None
    if call_fn is not None and not no_llm:
        from packages.orchestration.intake import make_structured_call_fn
        from packages.orchestration.schemas.models import TaskPlan
        # Planning needs a call_fn bound to TaskPlan: the intake one binds
        # the provider's native schema to JobIntake, so the provider would
        # answer in intake shape and every plan attempt would fail validation.
        # There is deliberately NO fallback to it — without a TaskPlan-bound
        # provider we skip LLM planning and take the deterministic skeleton
        # below, exactly as the no-provider path does.
        plan_call_fn = make_structured_call_fn(TaskPlan)

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
        job = JobPlan(
            job_title=mission[:80], mission=mission, user_prompt=mission,
            project_id=str(project.id),
            repo_path=target_repo_path,
            intake=intake_result.value.model_dump(),
        )
        plan_result = plan_job(job)
        job = plan_result.job
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
    """Register the repository if it is not, and add the ignore entries (D2). Nothing else."""
    from packages.orchestration.project_registry import (
        register_project_repo,
        resolve_project,
    )
    from packages.orchestration.repo_ignore import ensure_ignore_entry, ignore_entries
    from packages.orchestration.worktrees import WorktreeError, repo_root

    try:
        root = repo_root(ctx.repo)
    except (WorktreeError, OSError, subprocess.SubprocessError):
        return DO_STEP_FAILED, (
            f"{Path(ctx.repo).resolve()} is not a git repository — run `git init` first")
    ctx.repo_root = str(root)

    project = resolve_project(root)
    if project is None:
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

        call_fn = make_structured_call_fn(MissionPlanDraft)
    try:
        # Named exactly as `mission plan` names it: `make_structured_call_fn` is
        # Ollama-backed. Without a provider the compiler plans deterministically.
        outcome = plan_mission(project_id, mission.id, call_fn,
                               provider="ollama", provider_kind="ollama")
    except (MissionPlanInProgressError, MissionError) as exc:
        return DO_STEP_FAILED, f"mission {mission.id} was not planned: {exc}"
    return DO_STEP_DONE, (
        f"mission {mission.id} plan v{outcome.version} ({outcome.source}, "
        f"{len(outcome.plan.milestones)} milestone(s)): {outcome.plan_path}")


def _step_shape(ctx: DoContext) -> tuple[str, str]:
    """T001: ONE job for the order, targeting the repository, linked to the mission."""
    from packages.orchestration.mission_state import (
        MISSION_ROLE_INITIAL,
        link_job_to_mission,
    )

    try:
        shaped = plan_order_job(
            ctx.order,
            project=ctx.project,
            repo_path=ctx.repo_root,
            no_llm=ctx.no_llm,
            yes=ctx.yes,
        )
    except OrderJobPlanError as exc:
        return DO_STEP_FAILED, str(exc)
    job_id = str(shaped.job.job_id)
    link_job_to_mission(str(ctx.project.id), ctx.mission_id, job_id,
                        role=MISSION_ROLE_INITIAL)
    ctx.job_ids.append(job_id)
    return DO_STEP_DONE, (
        f"one job {job_id} linked to mission {ctx.mission_id}: "
        f"{len(shaped.job.tasks)} task(s), plan: {shaped.plan_label}, "
        f"{shaped.intake_label}")


def _provider_flags(ctx: DoContext) -> str:
    flags = ""
    if ctx.builder_provider:
        flags += f" --builder-provider {ctx.builder_provider}"
    if ctx.reviewer_provider:
        flags += f" --reviewer-provider {ctx.reviewer_provider}"
    return flags


def _step_run(ctx: DoContext) -> tuple[str, str]:
    """Run the job on the chosen builder and reviewer; stop at an open plan approval."""
    from packages.orchestration.job_plan import task_plan_blocks_execution
    from packages.orchestration.pingpong_job import JOB_COMPLETED, load_job_plan, run_job

    job_id = ctx.job_ids[-1]
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
        ctx.next_lines.append(f"remedy job run {job_id}{_provider_flags(ctx)}")
        return DO_STEP_STOPPED, (
            f"job {job_id}'s task plan is {blocked}, not approved; nothing was run "
            f"(--yes approves it unattended). Approve it with: {approve}")

    done = run_job(job_id, builder_name=ctx.builder_provider,
                   reviewer_name=ctx.reviewer_provider)
    ctx.next_lines.append(f"remedy job show {job_id}")
    if done.state != JOB_COMPLETED:
        reason = f": {done.error}" if done.error else ""
        return DO_STEP_FAILED, f"job {job_id} ended {done.state.value}{reason}"
    return DO_STEP_DONE, f"job {job_id} ran {len(done.tasks)} task(s) to {done.state.value}"


def _step_ui(ctx: DoContext) -> tuple[str, str]:
    """Until T004 the cockpit does not open by itself: print its real command, or skip."""
    if ctx.no_ui:
        return DO_STEP_SKIPPED, "--no-ui given; the cockpit was not opened"
    command = f"remedy ui start {ctx.job_ids[-1]}"
    ctx.next_lines.append(command)
    return DO_STEP_SKIPPED, f"the cockpit does not open by itself yet; open it with: {command}"


def _step_apply(ctx: DoContext) -> tuple[str, str]:
    """T001 always stops before apply; nothing is written to the repository."""
    command = (f"remedy job apply {ctx.job_ids[-1]} "
               f"--repo {shlex.quote(ctx.repo_root)} --approve")
    ctx.next_lines.append(command)
    return DO_STEP_STOPPED, (
        f"stopped before apply; {ctx.repo_root} is untouched. "
        f"Apply the reviewed result with: {command}")


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
