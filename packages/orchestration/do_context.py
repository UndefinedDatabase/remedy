"""F268 — what one `remedy do` walk carries from step to step: the context, its statuses and
shapes, and the two sentences every step reads from it;
moved out of `packages/orchestration/do_sequence.py` unchanged, as a step of that file's
boundary on `docs/system/structure-ledger-v1.md` (structure rule 2, DECISION F205 D3);
`do_sequence.py` imports every name back by name, so each import path keeps working.
"""

from __future__ import annotations

import shlex
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from packages.orchestration.project_registry import RemyProject

#: The two shapes (DECISION F268 D5), and where the one in force came from; an order over
#: several projects has a third, one job per repository, from its projects (DECISION F205 D4).
DO_SHAPE_ONE_JOB = "one job"
DO_SHAPE_MILESTONES = "milestones"
DO_SHAPE_REPOSITORIES = "one job per repository"
DO_SHAPE_SOURCE_PLANNER = "planner"
DO_SHAPE_SOURCE_PROJECTS = "the order's projects"
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
    #: The order file's resolved absolute path (DECISION F295 D3); "" for an order given as text.
    order_source_path: str = ""
    #: sha256 (hex) of the order file's exact bytes (DECISION F295 D3); "" for an order given as text.
    order_source_sha256: str = ""
    repo: str = "."
    builder_provider: str | None = None
    reviewer_provider: str | None = None
    #: `--project <slug-or-id>`: the init step selects this project instead of
    #: resolving or registering the repository (DECISION F268 D16 (4)); a tuple is every
    #: project an order file names, one job each (DECISION F205 D4).
    project_selector: str | tuple[str, ...] | None = None
    #: The resolved `JobBudgets` as a dict, set only when a budget flag was given;
    #: the run step passes it to `run_job` as `job run` does (DECISION F268 D16 (5)).
    budgets: dict[str, Any] | None = None
    builder_model: str | None = None
    reviewer_model: str | None = None
    #: `--planner-model`: `model=` of every structured planner call the plan and
    #: shape steps build (DECISION F268 D16 (7)).
    planner_model: str | None = None
    #: `--planner-provider`: which SERVICE plans — `ollama`, `claude-cli`, or
    #: `None` to take the `planner` role's own answer (operator amendment
    #: amend0920-selfuse-real, DECISION D1). It reaches every
    #: `make_structured_call_fn` this walk builds, beside `planner_model`.
    planner_provider: str | None = None
    #: `--contract <name>`: the contract template the plan step writes onto the
    #: new mission; ``None`` applies the one proposed from the order, if any
    #: (DECISION F269 D1 (4)).
    contract_template: str | None = None
    no_ui: bool = False
    yes: bool = False
    no_llm: bool = False
    force_job: bool = False
    force_mission: bool = False
    step_by_step: bool = False
    plan_only: bool = False
    #: `--apply`: the apply step applies every job instead of stopping (DECISION F268 D9).
    apply: bool = False
    #: The commit flag every apply passes to `apply_job`, at most one of the three
    #: set; each implies `--apply` and chains the walk's jobs (DECISION F270 D4 (1), (2)).
    commit_message: str | None = None
    commit_auto: bool = False
    commit_with_history: bool = False
    #: Push the mission ONCE after its last job; `push_source` names why: `--push`
    #: or `apply.push_after_mission`. Never passed to `apply_job` (D4 (4), (5)).
    push: bool = False
    push_source: str = ""
    #: One ``{job_id, sha, branch}`` per commit or merge the walk landed, in job order.
    landed: list[dict[str, str]] = field(default_factory=list)
    #: Each job applied so far → the sentence saying so, in apply order.
    applied: dict[str, str] = field(default_factory=dict)
    #: The mission's one push (D4 (7)); None while the walk has not asked it.
    push_outcome: dict[str, Any] | None = None
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
    #: Every project of an order over several, the first being `project`; empty otherwise.
    projects: list[RemyProject] = field(default_factory=list)
    #: Each of those projects' repository root, by project id (DECISION F205 D4).
    project_repos: dict[str, str] = field(default_factory=dict)
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
    def project_ids(self) -> list[str]:
        """The ids of every project an order over several names, in its order; empty otherwise."""
        return [str(project.id) for project in self.projects]

    @property
    def commit_mode(self) -> str:
        """``message``, ``auto``, ``history`` or ``""``: the walk's commit flag, as `job_apply` names it."""
        if self.commit_message is not None:
            return "message"
        return "auto" if self.commit_auto else "history" if self.commit_with_history else ""

    @property
    def failed(self) -> bool:
        return any(r.status == DO_STEP_FAILED for r in self.results)

    @property
    def stopped_before_apply(self) -> bool:
        """True unless the apply step itself ran to completion."""
        return not any(r.name == "apply" and r.status == DO_STEP_DONE
                       for r in self.results)


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


def do_stopped_walk_note(ctx: DoContext) -> str:
    """The tail of a stopped walk's detail under a commit flag: what stays, and no push (D4 (2))."""
    if not ctx.landed:
        return "; no commit landed and nothing was pushed"
    shas = ", ".join(entry["sha"][:12] for entry in ctx.landed)
    return (f"; the {len(ctx.landed)} commit(s) that landed ({shas}) stay on "
            f"{ctx.landed[-1]['branch']}, and nothing was pushed")
