"""Project group command handlers."""

from __future__ import annotations

import json as _json
import sys
from typing import TYPE_CHECKING, Callable
from uuid import UUID

from packages.orchestration.storage import JobNotFoundError, list_jobs, load_job, save_job

if TYPE_CHECKING:
    import argparse


def _cmd_create_project(name: str, description: str | None) -> None:
    from packages.orchestration.project_registry import RemyProject, save_project
    project = RemyProject(name=name, description=description)
    save_project(project)
    print(project.id)


def _cmd_list_projects() -> None:
    from packages.orchestration.project_registry import list_projects
    projects = list_projects()
    if not projects:
        print("No projects found.")
        return
    for p in projects:
        desc = f"  {p.description}" if p.description else ""
        print(f"{p.id}  {p.name}{desc}")


def _cmd_show_project(project_id_str: str, *, json_output: bool = False) -> None:
    from packages.orchestration.project_registry import (
        ProjectNotFoundError,
        export_project_json,
        load_project,
        summarize_project,
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
    all_jobs = list_jobs()
    linked_jobs = [j for j in all_jobs if str(j.id) in project.job_ids]
    if json_output:
        print(_json.dumps(export_project_json(project, linked_jobs), indent=2))
    else:
        print(summarize_project(project, linked_jobs))


def _cmd_attach_project_repo(project_id_str: str, repo_path_str: str) -> None:
    from packages.orchestration.project_registry import (
        ProjectNotFoundError,
        attach_repo,
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
    added = attach_repo(project, repo_path_str)
    save_project(project)
    if added:
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
        load_project,
    )
    from packages.orchestration.run_log import RunLogWriter

    try:
        pid = UUID(project_id_str)
    except ValueError:
        print(f"Error: invalid project ID: {project_id_str!r}", file=sys.stderr)
        sys.exit(1)
    try:
        project = load_project(pid)
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

    if linked_jobs:
        log = RunLogWriter(job_id=linked_jobs[0].id)
        log.log(
            "project_context_coverage_inspected",
            outcome="inspected",
            score=snapshot.score,
            present_signal_count=snapshot.present_signal_count,
            missing_signal_count=snapshot.missing_signal_count,
            scope=snapshot.scope,
            repo_count=snapshot.repo_count,
            job_count=snapshot.job_count,
        )


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "project.create": lambda args: _cmd_create_project(args.name, getattr(args, "description", None)),
    "project.list": lambda args: _cmd_list_projects(),
    "project.show": lambda args: _cmd_show_project(args.project_id, json_output=args.json),
    "project.attach-repo": lambda args: _cmd_attach_project_repo(args.project_id, args.repo_path),
    "project.attach-job": lambda args: _cmd_attach_project_job(args.project_id, args.job_id),
    "project.context": lambda args: _cmd_project_context(args.project_id, json_output=args.json),
}
