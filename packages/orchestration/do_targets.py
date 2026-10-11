"""F268 — where a `remedy do` walk's jobs go: the project and repository the init step selects,
and the orders, one per job, the shape step plans;
moved out of `packages/orchestration/do_sequence.py` unchanged, as a step of that file's
boundary on `docs/system/structure-ledger-v1.md` (structure rule 2, DECISION F205 D3);
`do_sequence.py` imports every name back by name, so each import path keeps working.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import TYPE_CHECKING, Any, NamedTuple

from packages.orchestration.do_context import (
    DO_SHAPE_MILESTONES,
    DO_SHAPE_ONE_JOB,
    DO_SHAPE_REPOSITORIES,
    DO_SHAPE_SOURCE_FORCE_JOB,
    DO_SHAPE_SOURCE_FORCE_MISSION,
    DO_SHAPE_SOURCE_PLANNER,
    DO_SHAPE_SOURCE_PROJECTS,
    DO_STEP_DONE,
    DO_STEP_FAILED,
    DoContext,
)

if TYPE_CHECKING:
    from packages.orchestration.pingpong_job import TaskEntry


class DoJobTarget(NamedTuple):
    """The project one job of the walk is planned for, and the repository it runs in."""

    project: Any
    repo: str


def _step_init(ctx: DoContext) -> tuple[str, str]:
    """Register the repository if it is not, and add the ignore entries (D2). Nothing else.

    With `--project` the project is selected through `select_project` instead,
    and an unknown one fails the step (DECISION F268 D16 (4)). An order file that
    names several projects selects each of them (DECISION F205 D4).
    """
    if isinstance(ctx.project_selector, tuple):
        return _init_several_projects(ctx, ctx.project_selector)
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


# WHY: an order over several projects runs each job in its own project's repository, so each
# project it names must be one registered project with a git repository (DECISION F205 D4).
def _init_several_projects(ctx: DoContext, selectors: tuple[str, ...]) -> tuple[str, str]:
    """Select every project the order names, the first as the walk's own; fail on one that does not fit.

    Nothing is registered here: each project is selected as `--project` selects one, and
    each one's registered repository must be a git repository.
    """
    from packages.orchestration.project_registry import (
        AmbiguousProjectError,
        InvalidProjectSelectorError,
        ProjectNotFoundError,
        select_project,
    )
    from packages.orchestration.repo_ignore import ensure_ignore_entry, ignore_entries
    from packages.orchestration.worktrees import WorktreeError, repo_root

    projects, roots = [], []
    for selector in selectors:
        try:
            project, _source = select_project(selector, ctx.repo)
        except (AmbiguousProjectError, ProjectNotFoundError, InvalidProjectSelectorError):
            return DO_STEP_FAILED, (
                f"no single project matches {selector!r}, which the order names; nothing "
                f"was planned; list them with: remedy project list")
        if any(str(chosen.id) == str(project.id) for chosen in projects):
            return DO_STEP_FAILED, f"the order names project {project.slug} twice; nothing was planned"
        try:
            root = repo_root(project.canonical_repo_path or "")
        except (WorktreeError, OSError, subprocess.SubprocessError):
            return DO_STEP_FAILED, (
                f"project {project.slug}'s repository {project.canonical_repo_path or '(none)'} "
                f"is not a git repository; nothing was planned")
        projects.append(project)
        roots.append(str(root))
    ctx.projects, ctx.project, ctx.repo_root = projects, projects[0], roots[0]
    ctx.project_repos = {str(project.id): root for project, root in zip(projects, roots)}
    for root in roots:
        for entry in ignore_entries(Path(root)):
            ensure_ignore_entry(Path(root), entry)
    named = ", ".join(f"{project.slug} ({project.id}) in {root}"
                      for project, root in zip(projects, roots))
    return DO_STEP_DONE, f"projects {named}, selected by the order, one job each"


def mission_plan_outlines(plan: Any) -> list[Any]:
    """Every `jobs_draft` outline across the plan's milestones, in milestone order."""
    if plan is None:
        return []
    return [outline for milestone in plan.milestones for outline in milestone.jobs_draft]


def do_shape_of_plan(plan: Any) -> str:
    """The planner's shape (DECISION F268 D5): two or more outlines are milestones."""
    return DO_SHAPE_MILESTONES if len(mission_plan_outlines(plan)) >= 2 else DO_SHAPE_ONE_JOB


def resolve_do_shape(plan: Any, *, force_job: bool = False, force_mission: bool = False,
                     projects: int = 1) -> tuple[str, str]:
    """``(shape, shape_source)``: a force flag wins over the plan; both at once is refused.

    An order over several *projects* plans one job per repository, and refuses a force
    flag (DECISION F205 D4).
    """
    if force_job and force_mission:
        raise ValueError("--force-job and --force-mission cannot be given together")
    if projects > 1:
        if force_job or force_mission:
            raise ValueError("an order naming several projects plans one job per repository; "
                             "--force-job and --force-mission do not apply to it")
        return DO_SHAPE_REPOSITORIES, DO_SHAPE_SOURCE_PROJECTS
    if force_job:
        return DO_SHAPE_ONE_JOB, DO_SHAPE_SOURCE_FORCE_JOB
    if force_mission:
        return DO_SHAPE_MILESTONES, DO_SHAPE_SOURCE_FORCE_MISSION
    return do_shape_of_plan(plan), DO_SHAPE_SOURCE_PLANNER


def do_project_order(order: str, slug: str, slugs: list[str]) -> str:
    """The order one job of an order over several projects is planned from (DECISION F205 D4)."""
    return (f"{order}\n\nThis job does the part of this order that belongs to project {slug}; "
            f"the order names these projects, one job each, in this order: {', '.join(slugs)}.")


def _shape_job_orders(
        ctx: DoContext, shape: str,
) -> list[tuple[str, list[TaskEntry] | None, str | None, DoJobTarget]]:
    """What to plan, one ``(order, deterministic_tasks, milestone_id, target)`` per job.

    ``None`` tasks let the planner choose.  ``milestone_id`` is the milestone
    whose ``jobs_draft`` outline the job came from (R-0977); a job planned
    from the order itself serves the plan's milestone when the plan has
    exactly one, and no milestone when it has several. ``target`` is the
    walk's own project and repository, or, one job per repository, each
    project the order names in its own (DECISION F205 D4).
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
    own = DoJobTarget(ctx.project, ctx.repo_root)
    if shape == DO_SHAPE_REPOSITORIES:
        slugs = [project.slug for project in ctx.projects]
        return [(do_project_order(order, project.slug, slugs), None, sole,
                 DoJobTarget(project, ctx.project_repos[str(project.id)]))
                for project in ctx.projects]
    if shape == DO_SHAPE_ONE_JOB:
        slices = deterministic_job_plans(order)
        if len(slices) == 1:
            return [(order, None, sole, own)]
        return [(order, tasks, sole, own) for tasks in slices]
    outlines = [(outline, str(milestone.id)) for milestone in milestones
                for outline in milestone.jobs_draft]
    if len(outlines) >= 2:
        return [(outline.goal, None, milestone_id, own) for outline, milestone_id in outlines]
    deliverables = extract_order_deliverables(order)
    if len(deliverables) >= 2:
        return [(order, [deliverable_task(d, order)], sole, own) for d in deliverables]
    [only] = deliverables
    return [(order, [deliverable_task(only, order)], sole, own),
            (order, [deliverable_check_task(only, order)], sole, own)]
