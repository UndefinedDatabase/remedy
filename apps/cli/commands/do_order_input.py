"""F295, F304 — what `remedy do` reads before any step: the order file's header, and the
repository the order runs in.

Moved out of `apps/cli/commands/do_cmd.py` unchanged, as step (1) of that file's boundary on
`docs/system/structure-ledger-v1.md` (structure rule 2, DECISION F205 D3); `do_cmd.py` imports
both names back by name, so each import path keeps working.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass

from apps.cli.json_envelope import fail


@dataclass(frozen=True)
class DoOrderInput:
    """What `_cmd_do` reads from its order argument before any step (DECISION F295 D2)."""

    goal: str
    project: str | tuple[str, ...] | None
    contract: str | None
    max_cost_usd: str | None
    max_total_tokens: str | None
    max_provider_calls: str | None
    max_wall_clock_minutes: str | None
    order_source_kwargs: dict[str, str]


def read_do_order(goal: str, *, project: str | tuple[str, ...] | None, contract: str | None,
                  max_cost_usd: str | None, max_total_tokens: str | None,
                  max_provider_calls: str | None, max_wall_clock_minutes: str | None,
                  json_output: bool) -> DoOrderInput:
    """The order text, its project, contract and caps, and its source, or exit 2 before any step.

    An argument that names no order file comes back as it was given, with the flags' values.
    """
    # DECISION F295 D2: an order argument naming a `.md` file is read before any
    # other step, and a file without a cap is refused before any step; DECISION F304 D14 lets the
    # cap be any one of the four job budgets an order file's header or the flags can set.
    from packages.orchestration.order_file import (
        OrderFileError,
        order_argument_names_file,
        read_order_file,
    )

    order_source_kwargs: dict[str, str] = {}
    if order_argument_names_file(goal):
        try:
            order_file = read_order_file(goal.strip())
        except OrderFileError as exc:
            fail(exc.error, f"{exc} Nothing was run.",
                 json_output=json_output, exit_code=2)
        if max_cost_usd is None:
            max_cost_usd = order_file.max_cost_usd
        if max_total_tokens is None:
            max_total_tokens = order_file.max_total_tokens
        if max_provider_calls is None:
            max_provider_calls = order_file.max_provider_calls
        if max_wall_clock_minutes is None:
            max_wall_clock_minutes = order_file.max_wall_clock_minutes
        if all(cap is None for cap in (max_cost_usd, max_total_tokens, max_provider_calls,
                                       max_wall_clock_minutes)):
            fail("order_file_no_cost_cap",
                 f"{goal.strip()}: an unattended order without a cap is refused; set "
                 "`max-cost-usd:`, `max-total-tokens:`, `max-provider-calls:` or "
                 "`max-wall-clock-minutes:` in the header, or pass --max-cost-usd, "
                 "--max-total-tokens, --max-provider-calls or --max-wall-clock-minutes. "
                 "Nothing was run.",
                 json_output=json_output, exit_code=2)
        goal = order_file.text
        if project is not None and len(order_file.projects) > 1:
            fail("invalid_argument",
                 f"{goal.strip()} names several projects in its header "
                 f"({', '.join(order_file.projects)}), and --project names one; leave "
                 "--project out, and each job runs in its own project. Nothing was run.",
                 json_output=json_output, exit_code=2)
        if project is None:
            project = order_file.project_selector
        if contract is None:
            contract = order_file.contract
        order_source_kwargs = {
            "order_source_path": order_file.source_path,
            "order_source_sha256": order_file.source_sha256,
        }
    return DoOrderInput(goal, project, contract, max_cost_usd, max_total_tokens,
                        max_provider_calls, max_wall_clock_minutes, order_source_kwargs)


# WHY: the project an order names files its records, so the work must happen in that project's
# repository too, wherever the client stands (F298's claim measurement, DECISION F304 D2).
def _order_repo(project: str | tuple[str, ...] | None, repo: str | None, *,
                json_output: bool) -> str:
    """The repository an order runs in, or exit 2 before any step.

    Without a project, `--repo` or else the current directory, as before. With one, that
    project's registered repository: a project with none is refused with
    `project_has_no_repo` and exit 3 (R-1183), and a `--repo` that is not one of its
    repositories with `repo_not_in_project` and exit 2. A selector that names no single
    project is left to the init step, which fails on it as it always has (DECISION F268
    D16 (4)). With several, their first's registered repository (DECISION F205 D4).
    """
    if project is None:
        return repo or "."
    if isinstance(project, tuple):
        return _several_projects_repo(project, repo, json_output=json_output)
    from pathlib import Path

    from packages.orchestration.project_registry import (
        AmbiguousProjectError,
        InvalidProjectSelectorError,
        ProjectNotFoundError,
        select_project,
    )
    from packages.orchestration.worktrees import WorktreeError, repo_root

    try:
        selected, _source = select_project(project, ".")
    except (AmbiguousProjectError, InvalidProjectSelectorError, ProjectNotFoundError):
        return repo or "."
    registered = selected.canonical_repo_path
    if not registered:
        fail("project_has_no_repo",
             f"project {selected.slug} has no registered repository, so the order has "
             f"nowhere to run; attach one with `remedy project attach --project "
             f"{selected.slug} --repo <path>`. Nothing was run.",
             json_output=json_output, exit_code=3)
    if repo is None:
        return registered
    try:
        root = str(Path(repo_root(repo)).resolve())
    except (WorktreeError, OSError, subprocess.SubprocessError):
        root = str(Path(repo).resolve())
    if root not in {registered, *selected.repo_paths}:
        fail("repo_not_in_project",
             f"--repo {repo} is not a repository of project {selected.slug}, whose "
             f"repository is {registered}; leave --repo out to run there. Nothing was "
             "run.", json_output=json_output, exit_code=2)
    return repo


# WHY: an order over several projects runs each job in its own project's repository, so each
# project must have one before any step, and one `--repo` cannot name them all (DECISION F205 D4).
def _several_projects_repo(projects: tuple[str, ...], repo: str | None, *,
                           json_output: bool) -> str:
    """The first project's registered repository, or exit before any step.

    `--repo` is refused with `repo_not_in_project` and exit 2, and a project without a
    registered repository with `project_has_no_repo` and exit 3, as for one project. A
    selector that names no single project is left to the init step, which fails on it.
    """
    from packages.orchestration.project_registry import (
        AmbiguousProjectError,
        InvalidProjectSelectorError,
        ProjectNotFoundError,
        select_project,
    )

    if repo is not None:
        fail("repo_not_in_project",
             f"--repo {repo} names one repository, and the order names several projects "
             f"({', '.join(projects)}), each of whose jobs runs in its own project's "
             "repository; leave --repo out. Nothing was run.",
             json_output=json_output, exit_code=2)
    lead = "."
    for position, selector in enumerate(projects):
        try:
            selected, _source = select_project(selector, ".")
        except (AmbiguousProjectError, InvalidProjectSelectorError, ProjectNotFoundError):
            continue
        if not selected.canonical_repo_path:
            fail("project_has_no_repo",
                 f"project {selected.slug} has no registered repository, so its job has "
                 f"nowhere to run; attach one with `remedy project attach --project "
                 f"{selected.slug} --repo <path>`. Nothing was run.",
                 json_output=json_output, exit_code=3)
        if position == 0:
            lead = selected.canonical_repo_path
    return lead
