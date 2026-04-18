"""
Remedy CLI entrypoint.

Usage:
    remedy create-job "<prompt>"
    remedy list-jobs
    remedy show-job <job_id>
    remedy plan-job <job_id>
"""

from __future__ import annotations

import argparse
import sys
from uuid import UUID

from packages.core.models import Job, RunState
from packages.orchestration.job_runner import PlanJobResult, plan_job
from packages.orchestration.storage import JobNotFoundError, list_jobs, load_job, save_job


def _cmd_create_job(prompt: str) -> None:
    job = Job(
        name=prompt[:50],
        user_prompt=prompt,
        state=RunState.PENDING,
    )
    save_job(job)
    print(job.id)


def _cmd_list_jobs() -> None:
    jobs = list_jobs()
    if not jobs:
        print("No jobs found.")
        return
    for job in jobs:
        print(f"{job.id}  {job.state.value:<12}  {job.created_at.isoformat()}  {job.name}")


def _cmd_show_job(job_id_str: str) -> None:
    try:
        job_id = UUID(job_id_str)
    except ValueError:
        print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
        sys.exit(1)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    print(job.model_dump_json(indent=2))


def _cmd_plan_job(job_id_str: str) -> None:
    try:
        job_id = UUID(job_id_str)
    except ValueError:
        print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
        sys.exit(1)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    result: PlanJobResult = plan_job(job)
    save_job(result.job)

    if not result.changed:
        print(f"Job {result.job.id} already planned — no changes made.")
    else:
        print(
            f"Job {result.job.id} planned: "
            f"{len(result.job.tasks)} task(s), {len(result.job.artifacts)} artifact(s)"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="remedy",
        description="Remedy orchestration CLI",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create-job", help="Create and persist a new job")
    create.add_argument("prompt", help="User prompt describing the job")

    subparsers.add_parser("list-jobs", help="List all persisted jobs (newest first)")

    show = subparsers.add_parser("show-job", help="Print full JSON for a job")
    show.add_argument("job_id", help="UUID of the job to show")

    plan = subparsers.add_parser("plan-job", help="Generate planning skeleton for a job")
    plan.add_argument("job_id", help="UUID of the job to plan")

    args = parser.parse_args()

    if args.command == "create-job":
        _cmd_create_job(args.prompt)
    elif args.command == "list-jobs":
        _cmd_list_jobs()
    elif args.command == "show-job":
        _cmd_show_job(args.job_id)
    elif args.command == "plan-job":
        _cmd_plan_job(args.job_id)


if __name__ == "__main__":
    main()
