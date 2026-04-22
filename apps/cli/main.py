"""
Remedy CLI entrypoint.

Usage:
    remedy create-job "<prompt>"
    remedy list-jobs
    remedy show-job <job_id>
    remedy plan-job <job_id>
    remedy plan-job-local <job_id>
    remedy run-next-task-local <job_id>
"""

from __future__ import annotations

import argparse
import sys
import time
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


def _cmd_plan_job_local(job_id_str: str) -> None:
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

    from packages.orchestration.llm_planner import annotate_planning_result, plan_job_with_llm
    from packages.providers.ollama_planner.provider import OllamaPlanner

    planner = OllamaPlanner()
    start = time.monotonic()
    try:
        result: PlanJobResult = plan_job_with_llm(job, planner.plan)
    except ImportError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"Error: Ollama planning failed: {exc}", file=sys.stderr)
        sys.exit(1)
    elapsed_ms = (time.monotonic() - start) * 1000

    annotate_planning_result(
        result,
        provider="ollama",
        role="planner",
        model=planner.model,
        elapsed_ms=elapsed_ms,
    )
    save_job(result.job)

    if not result.changed:
        print(f"Job {result.job.id} already planned — no changes made.")
    else:
        print(
            f"Job {result.job.id} | role=planner model={planner.model} "
            f"tasks={len(result.job.tasks)} elapsed={round(elapsed_ms)}ms"
        )


def _cmd_run_next_task_local(job_id_str: str) -> None:
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

    from pydantic import ValidationError

    from packages.orchestration.task_runner import RunTaskResult, annotate_task_result, run_next_task
    from packages.providers.ollama_builder.provider import OllamaBuilder

    builder = OllamaBuilder()
    start = time.monotonic()
    try:
        result: RunTaskResult = run_next_task(job, builder.build)
    except ImportError as exc:
        print(f"Error: missing dependency — {exc}", file=sys.stderr)
        sys.exit(1)
    except ValueError as exc:
        print(f"Error: configuration — {exc}", file=sys.stderr)
        sys.exit(1)
    except ValidationError as exc:
        print(f"Error: builder returned invalid output — {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"Error: builder execution failed — {exc}", file=sys.stderr)
        sys.exit(1)
    elapsed_ms = (time.monotonic() - start) * 1000

    if not result.changed:
        print(f"Job {job.id} — no pending tasks.")
        return

    annotate_task_result(
        result,
        provider="ollama",
        role="builder",
        model=builder.model,
        elapsed_ms=elapsed_ms,
    )
    save_job(result.job)

    task = next(t for t in result.job.tasks if t.id == result.task_id)
    task_type = task.inputs.get("task_type", "unknown")
    pending_remaining = sum(1 for t in result.job.tasks if t.status.value == "pending")

    print(
        f"Job {result.job.id} | task={result.task_id} type={task_type} "
        f"role=builder model={builder.model} elapsed={round(elapsed_ms)}ms "
        f"remaining={pending_remaining}"
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

    plan_local = subparsers.add_parser(
        "plan-job-local", help="Plan a job using local Ollama (requires ollama package)"
    )
    plan_local.add_argument("job_id", help="UUID of the job to plan")

    run_task = subparsers.add_parser(
        "run-next-task-local",
        help="Execute the next pending task using local Ollama (requires ollama package)",
    )
    run_task.add_argument("job_id", help="UUID of the job to advance")

    args = parser.parse_args()

    if args.command == "create-job":
        _cmd_create_job(args.prompt)
    elif args.command == "list-jobs":
        _cmd_list_jobs()
    elif args.command == "show-job":
        _cmd_show_job(args.job_id)
    elif args.command == "plan-job":
        _cmd_plan_job(args.job_id)
    elif args.command == "plan-job-local":
        _cmd_plan_job_local(args.job_id)
    elif args.command == "run-next-task-local":
        _cmd_run_next_task_local(args.job_id)


if __name__ == "__main__":
    main()
