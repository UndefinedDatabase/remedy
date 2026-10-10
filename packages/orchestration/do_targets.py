"""F268 — where a `remedy do` walk's jobs go: the project and repository the init step selects,
and the orders, one per job, the shape step plans;
moved out of `packages/orchestration/do_sequence.py` unchanged, as a step of that file's
boundary on `docs/system/structure-ledger-v1.md` (structure rule 2, DECISION F205 D3);
`do_sequence.py` imports every name back by name, so each import path keeps working.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import TYPE_CHECKING, Any

from packages.orchestration.do_context import (
    DO_SHAPE_MILESTONES,
    DO_SHAPE_ONE_JOB,
    DO_SHAPE_SOURCE_FORCE_JOB,
    DO_SHAPE_SOURCE_FORCE_MISSION,
    DO_SHAPE_SOURCE_PLANNER,
    DO_STEP_DONE,
    DO_STEP_FAILED,
    DoContext,
)

if TYPE_CHECKING:
    from packages.orchestration.pingpong_job import TaskEntry

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


def _shape_job_orders(
        ctx: DoContext, shape: str,
) -> list[tuple[str, list[TaskEntry] | None, str | None]]:
    """What to plan, one ``(order, deterministic_tasks, milestone_id)`` per job.

    ``None`` tasks let the planner choose.  ``milestone_id`` is the milestone
    whose ``jobs_draft`` outline the job came from (R-0977); a job planned
    from the order itself serves the plan's milestone when the plan has
    exactly one, and no milestone when it has several.
    """
    from packages.orchestration.task_deliverables import (
        deliverable_check_task,
        deliverable_task,
        deterministic_job_plans,
        extract_order_deliverables,
    )

    order = ctx.order
    milestones = list(ctx.mission_plan.milestones) if ctx.mission_plan is not None else []
    sole = str(milestones[0].id) if len(milestones) == 1 else None
    if shape == DO_SHAPE_ONE_JOB:
        slices = deterministic_job_plans(order)
        if len(slices) == 1:
            return [(order, None, sole)]
        return [(order, tasks, sole) for tasks in slices]
    outlines = [(outline, str(milestone.id)) for milestone in milestones
                for outline in milestone.jobs_draft]
    if len(outlines) >= 2:
        return [(outline.goal, None, milestone_id) for outline, milestone_id in outlines]
    deliverables = extract_order_deliverables(order)
    if len(deliverables) >= 2:
        return [(order, [deliverable_task(d, order)], sole) for d in deliverables]
    [only] = deliverables
    return [(order, [deliverable_task(only, order)], sole),
            (order, [deliverable_check_task(only, order)], sole)]
