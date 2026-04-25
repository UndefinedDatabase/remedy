"""
Remedy CLI entrypoint.

Usage:
    remedy create-job "<prompt>"
    remedy list-jobs
    remedy show-job <job_id>
    remedy plan-job <job_id>
    remedy plan-job-local <job_id>
    remedy attach-repo <job_id> <repo_path>
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


def _cmd_attach_repo(job_id_str: str, repo_path_str: str) -> None:
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

    from pathlib import Path

    repo_path = Path(repo_path_str)
    if not repo_path.exists():
        print(f"Error: repo_path does not exist: {repo_path_str!r}", file=sys.stderr)
        sys.exit(1)
    if not repo_path.is_dir():
        print(f"Error: repo_path is not a directory: {repo_path_str!r}", file=sys.stderr)
        sys.exit(1)

    resolved = repo_path.resolve()
    job.metadata["target_repo"] = str(resolved)
    save_job(job)
    print(f"Job {job.id} | repo={resolved}")


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

    from pathlib import Path

    from packages.orchestration.repo_applicator import apply_task_output_to_repo
    from packages.orchestration.task_runner import (
        RunTaskResult,
        annotate_task_result,
        finalize_task,
        materialize_task_output,
        run_next_task,
    )
    from packages.orchestration.verifier import verify_task_output
    from packages.orchestration.workspace import LocalWorkspaceRuntime
    from packages.providers.ollama_builder.provider import OllamaBuilder

    start = time.monotonic()
    try:
        builder = OllamaBuilder()
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

    # Annotate timing metadata onto the builder artifact.
    annotate_task_result(
        result,
        provider="ollama",
        role="builder",
        model=builder.model,
        elapsed_ms=elapsed_ms,
    )

    # Materialize builder output to workspace file.
    runtime = LocalWorkspaceRuntime(job_id=job.id)
    mf = materialize_task_output(result, runtime)

    # Verify: run Task Contract v1 checks (deterministic, local-only).
    vr = verify_task_output(result.job, result.task_id)

    # Finalize: mark COMPLETED on pass, PENDING on failure.
    finalize_task(result, vr)

    # Apply to attached repo (only on pass, only if repo is attached and eligible).
    repo_applied: list[str] = []
    if vr.passed and job.metadata.get("target_repo"):
        repo_root = Path(job.metadata["target_repo"])
        if not repo_root.exists() or not repo_root.is_dir():
            print(
                f"  warning: attached repo {str(repo_root)!r} no longer exists or is not a "
                "directory; skipping repo application",
                file=sys.stderr,
            )
        else:
            task_obj = next(t for t in result.job.tasks if t.id == result.task_id)
            if task_obj.output_artifact_ids:
                artifact_id = task_obj.output_artifact_ids[0]
                artifact = next((a for a in result.job.artifacts if a.id == artifact_id), None)
                if artifact is not None:
                    repo_applied = apply_task_output_to_repo(artifact, repo_root)
                    if repo_applied:
                        artifact.metadata["repo_applied_files"] = repo_applied

    # Persist after verification (and optional repo application) so the saved
    # state is authoritative.
    save_job(result.job)

    task = next(t for t in result.job.tasks if t.id == result.task_id)
    task_type = task.inputs.get("task_type", "unknown")
    pending_remaining = sum(1 for t in result.job.tasks if t.status.value == "pending")

    file_info = f" file={mf.path}" if mf is not None else ""
    repo_info = f" repo={repo_applied[0]}" if repo_applied else ""
    verified_info = "verified=pass" if vr.passed else f"verified=FAIL({len(vr.failures)} check(s))"
    print(
        f"Job {result.job.id} | task={result.task_id} type={task_type} "
        f"role=builder model={builder.model} elapsed={round(elapsed_ms)}ms "
        f"remaining={pending_remaining}{file_info}{repo_info} {verified_info}"
    )
    if not vr.passed:
        for failure in vr.failures:
            print(f"  verification failure: {failure.check}: {failure.message}", file=sys.stderr)
        sys.exit(1)


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

    attach = subparsers.add_parser(
        "attach-repo",
        help="Attach a target repository directory to a job for safe file application",
    )
    attach.add_argument("job_id", help="UUID of the job")
    attach.add_argument("repo_path", help="Path to the target repository directory")

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
    elif args.command == "attach-repo":
        _cmd_attach_repo(args.job_id, args.repo_path)
    elif args.command == "run-next-task-local":
        _cmd_run_next_task_local(args.job_id)


if __name__ == "__main__":
    main()
