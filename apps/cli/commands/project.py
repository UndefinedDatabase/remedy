"""Project group command handlers."""

from __future__ import annotations

import json as _json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING
from uuid import UUID

from packages.orchestration.storage import JobNotFoundError, list_jobs, load_job, save_job

if TYPE_CHECKING:
    import argparse


def _cmd_create_project(name: str, description: str | None) -> None:
    from packages.orchestration.project_registry import (
        RemyProject,
        _unique_slug,
        save_project,
        slugify,
    )
    slug = _unique_slug(slugify(name))
    project = RemyProject(name=name, slug=slug, description=description)
    save_project(project)
    print(project.id)


def _cmd_list_projects(
    *,
    json_output: bool = False,
    sort: str | None = None,
    desc: bool = False,
    since: str | None = None,
    until: str | None = None,
    limit: str | None = None,
) -> None:
    from packages.orchestration.list_options import ListOptionError, apply_list_options
    from packages.orchestration.project_registry import _list_projects_readonly
    projects = _list_projects_readonly()
    try:
        projects = apply_list_options(
            projects,
            sort=sort, desc=desc, since=since, until=until, limit=limit,
            sort_fields={
                "created_at": lambda p: p.created_at,
                "name": lambda p: p.name,
            },
            default_sort_field="created_at",
            date_getter=lambda p: p.created_at.isoformat(),
        )
    except ListOptionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    if json_output:
        print(_json.dumps({
            "version": 1,
            "project_count": len(projects),
            "projects": [{"id": str(p.id), "slug": p.slug or "", "name": p.name,
                          "description": p.description or "",
                          "created_at": p.created_at.isoformat()} for p in projects],
        }, sort_keys=True))
        return
    if not projects:
        print("No projects found.")
        return
    for p in projects:
        slug = p.slug or "-"
        desc = f"  {p.description}" if p.description else ""
        print(f"{p.id}  {slug:<20s}  {p.name}  (created={p.created_at.isoformat()}){desc}")


def _cmd_show_project(project_id_str: str, *, json_output: bool = False) -> None:
    from packages.orchestration.project_registry import (
        ProjectNotFoundError,
        _load_project_readonly,
        _projects_dir,
        export_project_json,
        summarize_project,
    )

    try:
        pid = UUID(project_id_str)
    except ValueError:
        print(f"ERROR: invalid project UUID: {project_id_str}", file=sys.stderr)
        sys.exit(1)
    try:
        path = _projects_dir() / f"{pid}.json"
        if not path.exists():
            raise ProjectNotFoundError(pid)
        project = _load_project_readonly(path)
    except ProjectNotFoundError:
        print(f"ERROR: project not found: {project_id_str}", file=sys.stderr)
        sys.exit(1)
    all_jobs = list_jobs()
    linked_jobs = [j for j in all_jobs if str(j.id) in project.job_ids]
    if json_output:
        print(_json.dumps(export_project_json(project, linked_jobs), indent=2))
    else:
        print(summarize_project(project, linked_jobs))


def _cmd_attach_project_repo(project_id_str: str, repo_path_str: str) -> None:
    from packages.orchestration.project_registry import (
        NotAGitRepoError,
        ProjectNotFoundError,
        RepoOwnershipConflictError,
        attach_repo_canonical,
        load_project,
    )

    try:
        pid = UUID(project_id_str)
    except ValueError:
        print(f"ERROR: invalid project UUID: {project_id_str}", file=sys.stderr)
        sys.exit(1)
    try:
        project = load_project(pid)
    except ProjectNotFoundError:
        print(f"ERROR: project not found: {project_id_str}", file=sys.stderr)
        sys.exit(1)
    try:
        changed, repo_real = attach_repo_canonical(project, repo_path_str)
    except NotAGitRepoError:
        print(f"ERROR: {repo_path_str!r} is not a git repository.", file=sys.stderr)
        sys.exit(2)
    except RepoOwnershipConflictError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
    if changed:
        print(f"Attached repo to project {str(pid)[:8]}")
    else:
        print(f"Repo already attached to project {str(pid)[:8]} (no-op)")


def _cmd_attach_project_job(project_id_str: str, job_id_str: str) -> None:
    from packages.orchestration.project_registry import (
        ProjectNotFoundError,
        attach_job,
        load_project,
        save_project,
    )

    try:
        pid = UUID(project_id_str)
    except ValueError:
        print(f"ERROR: invalid project UUID: {project_id_str}", file=sys.stderr)
        sys.exit(1)
    try:
        project = load_project(pid)
    except ProjectNotFoundError:
        print(f"ERROR: project not found: {project_id_str}", file=sys.stderr)
        sys.exit(1)
    try:
        job = load_job(UUID(job_id_str))
    except (ValueError, JobNotFoundError):
        print(f"ERROR: job not found: {job_id_str}", file=sys.stderr)
        sys.exit(1)
    added = attach_job(project, job_id_str)
    save_project(project)
    if job.metadata.get("project_id") != project_id_str:
        job.metadata["project_id"] = project_id_str
        save_job(job)
    if added:
        print(f"Attached job {job_id_str[:8]} to project {str(pid)[:8]}")
    else:
        print(f"Job already attached to project {str(pid)[:8]} (no-op)")


def _cmd_project_context(project_id_str: str, *, json_output: bool = False) -> None:
    from packages.orchestration.project_context_coverage import (
        derive_project_context_coverage,
        export_project_context_coverage_json,
        summarize_project_context_coverage,
    )
    from packages.orchestration.project_registry import (
        ProjectNotFoundError,
        _load_project_readonly,
        _projects_dir,
    )

    try:
        pid = UUID(project_id_str)
    except ValueError:
        print(f"Error: invalid project ID: {project_id_str!r}", file=sys.stderr)
        sys.exit(1)
    try:
        path = _projects_dir() / f"{pid}.json"
        if not path.exists():
            raise ProjectNotFoundError(pid)
        project = _load_project_readonly(path)
    except ProjectNotFoundError:
        print(f"Error: project not found: {project_id_str}", file=sys.stderr)
        sys.exit(1)

    all_jobs = list_jobs()
    linked_jobs = [j for j in all_jobs if str(j.id) in project.job_ids]
    snapshot = derive_project_context_coverage(project, linked_jobs)

    if json_output:
        print(_json.dumps(export_project_context_coverage_json(snapshot), sort_keys=True))
    else:
        print(summarize_project_context_coverage(snapshot))


def _cmd_project_brain(project_id_str: str, *, json_output: bool = False) -> None:
    from pathlib import Path

    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.project_brain_aggregate import (
        build_project_brain_aggregate,
        export_project_brain_aggregate_json,
        summarize_project_brain_aggregate,
    )
    from packages.orchestration.project_constitution import load_project_constitution
    from packages.orchestration.project_registry import (
        ProjectNotFoundError,
        _load_project_readonly,
        _projects_dir,
    )
    from packages.orchestration.timeline import load_run_events

    try:
        pid = UUID(project_id_str)
    except ValueError:
        print(f"Error: invalid project ID: {project_id_str!r}", file=sys.stderr)
        sys.exit(1)
    try:
        path = _projects_dir() / f"{pid}.json"
        if not path.exists():
            raise ProjectNotFoundError(pid)
        project = _load_project_readonly(path)
    except ProjectNotFoundError:
        print(f"Error: project not found: {project_id_str}", file=sys.stderr)
        sys.exit(1)

    all_jobs = list_jobs()
    linked_jobs = [j for j in all_jobs if str(j.id) in project.job_ids]

    data_dir = resolve_data_root()
    all_events: dict[str, list[dict]] = {}
    consts: dict[str, object | None] = {}
    for job in linked_jobs:
        jid = str(job.id)
        all_events[jid] = load_run_events(data_dir, job.id)
        target_repo = job.metadata.get("target_repo")
        if target_repo:
            try:
                consts[jid] = load_project_constitution(Path(target_repo))
            except Exception:
                consts[jid] = None

    agg = build_project_brain_aggregate(
        project, linked_jobs, all_events, constitutions=consts,
    )

    if json_output:
        print(_json.dumps(export_project_brain_aggregate_json(agg), sort_keys=True))
    else:
        print(summarize_project_brain_aggregate(agg))


def _cmd_project_summary(project_id_str: str, *, json_output: bool = False) -> None:
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.project_registry import (
        ProjectNotFoundError,
        _load_project_readonly,
        _projects_dir,
    )
    from packages.orchestration.project_summary import (
        build_project_summary,
        detect_patterns,
        export_patterns_json,
        export_project_summary_json,
        suggest_memory_updates,
    )
    from packages.orchestration.timeline import load_run_events

    try:
        pid = UUID(project_id_str)
    except ValueError:
        print(f"Error: invalid project ID: {project_id_str!r}", file=sys.stderr)
        sys.exit(1)
    try:
        path = _projects_dir() / f"{pid}.json"
        if not path.exists():
            raise ProjectNotFoundError(pid)
        project = _load_project_readonly(path)
    except ProjectNotFoundError:
        print(f"Error: project not found: {project_id_str}", file=sys.stderr)
        sys.exit(1)

    all_jobs = list_jobs()
    linked_jobs = [j for j in all_jobs if str(j.id) in project.job_ids]

    data_dir = resolve_data_root()
    all_events: dict[str, list[dict]] = {}
    for job in linked_jobs:
        jid = str(job.id)
        all_events[jid] = load_run_events(data_dir, job.id)

    summary = build_project_summary(project, linked_jobs, all_events)
    patterns = detect_patterns(linked_jobs, all_events)
    suggestions = suggest_memory_updates(summary, patterns)

    summary.patterns = export_patterns_json(patterns)
    summary.memory_suggestions = [
        {"title": s.title, "summary": s.summary, "evidence_count": s.evidence_count,
         "requires_approval": s.requires_approval}
        for s in suggestions
    ]

    if json_output:
        print(_json.dumps(export_project_summary_json(summary), sort_keys=True))
    else:
        print(f"Project: {project.name} ({project_id_str[:8]})")
        print(f"Jobs: {summary.job_count} (active={summary.active_job_count}, completed={summary.completed_job_count}, blocked={summary.blocked_job_count})")
        print(f"Focus: {summary.current_focus}")
        if summary.blockers:
            print(f"Blockers: {', '.join(summary.blockers[:3])}")
        if summary.frequently_touched_files:
            print(f"Frequently touched: {', '.join(summary.frequently_touched_files[:3])}")
        if patterns:
            print(f"Patterns: {len(patterns)} detected")
            for p in patterns[:3]:
                print(f"  - [{p.severity}] {p.summary}")
        if suggestions:
            print(f"Memory suggestions: {len(suggestions)} (approval required)")
            for s in suggestions[:3]:
                print(f"  - {s.title}")
        if summary.suggested_next_step:
            print(f"Next step: {summary.suggested_next_step}")
        if summary.next_command:
            print(f"Command: {summary.next_command}")


def _cmd_project_current(
    *,
    project_flag: str | None = None,
    json_output: bool = False,
) -> None:
    import os

    from packages.orchestration.project_registry import (
        AmbiguousProjectError,
        InvalidProjectSelectorError,
        ProjectNotFoundError,
        select_project,
    )
    cwd = os.getcwd()
    try:
        project, source = select_project(project_flag, cwd)
    except AmbiguousProjectError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
    except (ProjectNotFoundError, InvalidProjectSelectorError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(3)

    if json_output:
        print(_json.dumps({
            "project_id": str(project.id),
            "slug": project.slug,
            "repo": project.canonical_repo_path,
            "job_count": len(project.job_ids),
            "selection_source": source,
        }, indent=2))
    else:
        print(f"slug  : {project.slug}")
        print(f"id    : {project.id}")
        print(f"repo  : {project.canonical_repo_path or '(none)'}")
        print(f"jobs  : {len(project.job_ids)}")
        print(f"source: {source}")


def _cmd_project_attach_repo(
    repo_path_str: str,
    *,
    project_flag: str | None = None,
) -> None:
    import os

    from packages.orchestration.project_registry import (
        AmbiguousProjectError,
        InvalidProjectSelectorError,
        NotAGitRepoError,
        ProjectNotFoundError,
        RepoOwnershipConflictError,
        attach_repo_canonical,
        select_project,
    )

    cwd = os.getcwd()
    try:
        project, _source = select_project(project_flag, cwd)
    except AmbiguousProjectError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
    except (ProjectNotFoundError, InvalidProjectSelectorError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(3)

    old_canonical = project.canonical_repo_path
    try:
        changed, repo_real = attach_repo_canonical(project, repo_path_str)
    except NotAGitRepoError:
        print(
            f"ERROR: {repo_path_str!r} is not a git repository.",
            file=sys.stderr,
        )
        sys.exit(2)
    except RepoOwnershipConflictError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    print(_json.dumps({
        "project_id": str(project.id),
        "slug": project.slug,
        "old_repo": old_canonical if changed else repo_real,
        "new_repo": repo_real,
        "changed": changed,
    }, indent=2))


def _cmd_project_adopt(
    job_id_str: str,
    *,
    project_flag: str | None = None,
) -> None:
    from packages.orchestration.data_paths import resolve_job_id
    from packages.orchestration.project_registry import (
        ProjectNotFoundError,
        attach_job,
        save_project,
        select_project,
    )

    try:
        project, _src = select_project(project_flag, ".")
    except ProjectNotFoundError:
        print(
            "Error: no project found. Run: remedy init\n"
            "  or pass --project <slug-or-id>",
            file=sys.stderr,
        )
        sys.exit(3)

    resolved_id = str(resolve_job_id(job_id_str))

    try:
        job = load_job(UUID(resolved_id))
    except JobNotFoundError:
        print(f"Error: job not found: {resolved_id[:8]}", file=sys.stderr)
        sys.exit(3)

    if job.project_id is not None:
        print(
            f"Error: job {resolved_id[:8]} already belongs to project {job.project_id[:8]}",
            file=sys.stderr,
        )
        sys.exit(2)

    job.project_id = str(project.id)
    save_job(job)
    attach_job(project, str(job.id))
    save_project(project)
    print(f"Adopted {resolved_id[:8]} into project {project.slug or project.id}.")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "project.create": lambda args: _cmd_create_project(args.name, getattr(args, "description", None)),
    "project.list": lambda args: _cmd_list_projects(
        json_output=args.json,
        sort=getattr(args, "sort", None),
        desc=getattr(args, "desc", False),
        since=getattr(args, "since", None),
        until=getattr(args, "until", None),
        limit=getattr(args, "limit", None),
    ),
    "project.show": lambda args: _cmd_show_project(args.project_id, json_output=args.json),
    "project.attach-repo": lambda args: _cmd_attach_project_repo(args.project_id, args.repo_path),
    "project.attach-job": lambda args: _cmd_attach_project_job(args.project_id, args.job_id),
    "project.brain": lambda args: _cmd_project_brain(args.project_id, json_output=args.json),
    "project.context": lambda args: _cmd_project_context(args.project_id, json_output=args.json),
    "project.summary": lambda args: _cmd_project_summary(args.project_id, json_output=args.json),
    "project.current": lambda args: _cmd_project_current(
        project_flag=getattr(args, "project", None),
        json_output=args.json,
    ),
    "project.attach": lambda args: _cmd_project_attach_repo(
        args.repo,
        project_flag=getattr(args, "project", None),
    ),
    "project.adopt": lambda args: _cmd_project_adopt(
        args.job_id,
        project_flag=getattr(args, "project", None),
    ),
}
