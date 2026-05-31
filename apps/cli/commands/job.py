"""Job group command handlers."""

from __future__ import annotations

import re
import sys
import time
from typing import TYPE_CHECKING, Callable
from uuid import UUID

from packages.core.models import Job, RunState, Task
from packages.orchestration.data_paths import resolve_data_root
from packages.orchestration.job_runner import PlanJobResult, plan_job
from packages.orchestration.storage import JobNotFoundError, list_jobs, load_job, save_job

if TYPE_CHECKING:
    import argparse

_SAFE_TASK_TYPE_RE = re.compile(r'^[A-Za-z0-9_-]+$')


def _cmd_create_job(
    prompt: str,
    *,
    project_id: str | None = None,
    task_type: str | None = None,
    task_description: str | None = None,
) -> None:
    from packages.orchestration.run_log import RunLogWriter

    if task_description is not None and task_type is None:
        print("Error: --task-description requires --task-type", file=sys.stderr)
        sys.exit(1)

    if task_type is not None:
        task_type = task_type.strip()
        if not task_type:
            print("Error: --task-type must not be empty", file=sys.stderr)
            sys.exit(1)
        if not _SAFE_TASK_TYPE_RE.match(task_type):
            print(
                "Error: --task-type contains invalid characters; "
                "allowed: letters, digits, underscores, hyphens",
                file=sys.stderr,
            )
            sys.exit(1)

    project = None
    if project_id:
        from packages.orchestration.project_registry import (
            ProjectNotFoundError,
            load_project,
        )
        try:
            project = load_project(UUID(project_id))
        except (ProjectNotFoundError, ValueError):
            print("Warning: project unavailable; job created without project link.", file=sys.stderr)
            project_id = None

    metadata: dict = {}
    if project_id:
        metadata["project_id"] = project_id

    tasks: list[Task] = []
    state = RunState.PENDING
    if task_type is not None:
        description = (task_description or "").strip() or f"Execute {task_type} task."
        tasks = [Task(description=description, inputs={"task_type": task_type})]
        state = RunState.PLANNED

    job = Job(
        name=prompt[:50],
        user_prompt=prompt,
        state=state,
        tasks=tasks,
        metadata=metadata,
    )
    save_job(job)
    print(job.id)
    log = RunLogWriter(job_id=job.id)
    log.log("job_created", outcome="created")

    if project is not None:
        from packages.orchestration.project_registry import attach_job, save_project
        attach_job(project, str(job.id))
        save_project(project)


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
    from packages.orchestration.run_log import RunLogWriter
    from packages.providers.ollama_planner.provider import OllamaPlanner

    log = RunLogWriter(job_id=job.id)
    planner = OllamaPlanner()
    log.log("planning_started", provider="ollama", role="planner", model=planner.model)

    start = time.monotonic()
    try:
        result: PlanJobResult = plan_job_with_llm(job, planner.plan)
    except ImportError as exc:
        log.log("planning_failed", provider="ollama", role="planner", model=planner.model,
                outcome="error", message="planning failed", error_category=type(exc).__name__)
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        log.log("planning_failed", provider="ollama", role="planner", model=planner.model,
                outcome="error", message="planning failed", error_category=type(exc).__name__)
        print(f"Error: Ollama planning failed: {exc}", file=sys.stderr)
        sys.exit(1)
    elapsed_ms = (time.monotonic() - start) * 1000

    annotate_planning_result(result, provider="ollama", role="planner", model=planner.model, elapsed_ms=elapsed_ms)
    save_job(result.job)

    if not result.changed:
        log.log("planning_completed", provider="ollama", role="planner", model=planner.model, outcome="noop")
        print(f"Job {result.job.id} already planned — no changes made.  log={log.path}")
    else:
        from packages.orchestration.artifact_index import planning_artifact
        pa = planning_artifact(result.job.artifacts)
        artifact_id_str = str(pa.id) if pa is not None else None
        log.log(
            "planning_completed", provider="ollama", role="planner", model=planner.model,
            artifact_id=artifact_id_str, outcome="changed", elapsed_ms=round(elapsed_ms),
            task_count=len(result.job.tasks),
        )
        print(
            f"Job {result.job.id} | role=planner model={planner.model} "
            f"tasks={len(result.job.tasks)} elapsed={round(elapsed_ms)}ms  log={log.path}"
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


def _cmd_set_permission(job_id_str: str, action: str, capability_str: str) -> None:
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

    if action not in ("allow", "deny"):
        print(f"Error: action must be 'allow' or 'deny', got {action!r}", file=sys.stderr)
        sys.exit(1)

    from packages.orchestration.permissions import Capability, is_reserved, set_permission
    try:
        cap = Capability(capability_str)
    except ValueError:
        valid = ", ".join(c.value for c in Capability)
        print(f"Error: unknown capability {capability_str!r}. Valid: {valid}", file=sys.stderr)
        sys.exit(1)

    set_permission(job, cap, allow=(action == "allow"))
    save_job(job)
    print(f"Job {job.id} | permission {cap.value}={action}")
    if is_reserved(cap):
        print(
            f"note: {cap.value} is reserved and has no effect in this version "
            "(setting is persisted but not enforced at runtime)"
        )


def _cmd_show_permissions(job_id_str: str) -> None:
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

    from packages.orchestration.permissions import effective_permissions
    rows = effective_permissions(job)
    print(f"Job {job.id} | permissions:")
    for row in rows:
        print(f"  {row['capability']:<24} {row['effective']:<6}  [{row['status']}]")


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

    from pathlib import Path
    from pydantic import ValidationError
    from packages.orchestration.permissions import Capability
    from packages.orchestration.permissions import is_allowed as _perm_allowed
    from packages.orchestration.repo_applicator import check_and_apply_to_repo
    from packages.orchestration.run_log import RunLogWriter
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

    log = RunLogWriter(job_id=job.id)

    if not any(t.status == RunState.PENDING for t in job.tasks):
        log.log("task_run_noop", outcome="no_pending_tasks")
        print(f"Job {job.id} — no pending tasks.  log={log.path}")
        return

    pending_task = next((t for t in job.tasks if t.status == RunState.PENDING), None)
    pending_task_type = pending_task.inputs.get("task_type", "unknown") if pending_task else None
    log.log("task_run_started", task_id=str(pending_task.id) if pending_task else None, task_type=pending_task_type)

    def _fail(outcome: str, **meta: object) -> None:
        log.log(
            "task_run_failed",
            task_id=str(pending_task.id) if pending_task else None,
            outcome=outcome, task_type=pending_task_type, **meta,
        )

    if not _perm_allowed(job, Capability.workspace_write):
        _fail("permission_denied", capability="workspace_write")
        print(f"Error: permission denied — workspace_write is not granted for job {job.id}", file=sys.stderr)
        sys.exit(1)

    start = time.monotonic()
    try:
        builder = OllamaBuilder()
        log.log(
            "builder_started", task_id=str(pending_task.id) if pending_task else None,
            provider="ollama", role="builder", model=builder.model, task_type=pending_task_type,
        )
        result: RunTaskResult = run_next_task(job, builder.build)
    except ImportError as exc:
        _fail("missing_dependency", error_category="ImportError")
        print(f"Error: missing dependency — {exc}", file=sys.stderr)
        sys.exit(1)
    except ValidationError as exc:
        _fail("invalid_builder_output", error_category="ValidationError")
        print(f"Error: builder returned invalid output — {exc}", file=sys.stderr)
        sys.exit(1)
    except ValueError as exc:
        _fail("configuration_error", error_category="ValueError")
        print(f"Error: configuration — {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        _fail("builder_error", error_category=type(exc).__name__)
        print(f"Error: builder execution failed — {exc}", file=sys.stderr)
        sys.exit(1)
    elapsed_ms = (time.monotonic() - start) * 1000

    if not result.changed:
        log.log(
            "task_run_noop", task_id=str(pending_task.id) if pending_task else None,
            outcome="no_change", task_type=pending_task_type, reason="builder_returned_no_change",
        )
        print(f"Job {job.id} — builder returned no change.  log={log.path}")
        return

    _task_obj_for_log = next((t for t in result.job.tasks if t.id == result.task_id), None)
    _artifact_id_for_log = (
        str(_task_obj_for_log.output_artifact_ids[0])
        if _task_obj_for_log and _task_obj_for_log.output_artifact_ids
        else None
    )
    log.log("builder_completed", task_id=str(result.task_id), artifact_id=_artifact_id_for_log,
            outcome="changed", elapsed_ms=round(elapsed_ms))

    annotate_task_result(result, provider="ollama", role="builder", model=builder.model, elapsed_ms=elapsed_ms)

    runtime = LocalWorkspaceRuntime(job_id=job.id)
    mf = materialize_task_output(result, runtime)
    log.log("workspace_materialized", task_id=str(result.task_id), workspace_file=str(mf.path))

    vr = verify_task_output(result.job, result.task_id)

    _task_type_for_log = (
        next(t for t in result.job.tasks if t.id == result.task_id).inputs.get("task_type", "unknown")
    )
    if vr.passed:
        from packages.orchestration.task_registry import get_task_type_spec as _get_spec
        _spec = _get_spec(_task_type_for_log)
        log.log("verification_passed", task_id=str(result.task_id), outcome="pass", verifier_profile=_spec.verifier_profile)
    else:
        _failed_checks = [c.check for c in vr.failures]
        log.log("verification_failed", task_id=str(result.task_id), outcome="fail",
                failure_count=len(vr.failures), failed_checks=_failed_checks)

    finalize_task(result, vr)

    repo_applied: list[str] = []
    if vr.passed and job.metadata.get("target_repo"):
        repo_root = Path(job.metadata["target_repo"])
        if not repo_root.exists() or not repo_root.is_dir():
            print(
                f"  warning: attached repo {str(repo_root)!r} no longer exists or is not a "
                "directory; skipping repo application", file=sys.stderr,
            )
        else:
            task_obj = next(t for t in result.job.tasks if t.id == result.task_id)
            if task_obj.output_artifact_ids:
                artifact_id = task_obj.output_artifact_ids[0]
                artifact = next((a for a in result.job.artifacts if a.id == artifact_id), None)
                if artifact is not None:
                    repo_applied = check_and_apply_to_repo(job, artifact, repo_root)
                    if repo_applied:
                        artifact.metadata["repo_applied_files"] = repo_applied
                        log.log("repo_application_completed", task_id=str(result.task_id),
                                outcome="applied", file_count=len(repo_applied), files=repo_applied)
                    else:
                        _skip_reason = artifact.metadata.get("repo_application_skipped_reason")
                        if _skip_reason:
                            log.log("repo_application_skipped", task_id=str(result.task_id),
                                    outcome="skipped", reason=_skip_reason)

    patch_intent_count = 0
    dry_run_block = ""
    if vr.passed:
        from packages.orchestration.patch_intent import (
            derive_patch_intents,
            format_dry_run_explanations,
            generate_dry_run_preview,
            materialize_patch_intents,
            truncate_preview,
            verify_patch_intent_set,
        )
        pi_task_obj = next(t for t in result.job.tasks if t.id == result.task_id)
        if pi_task_obj.output_artifact_ids:
            pi_artifact_id = pi_task_obj.output_artifact_ids[0]
            pi_artifact = next((a for a in result.job.artifacts if a.id == pi_artifact_id), None)
            if pi_artifact is not None:
                pi_task_type = pi_artifact.metadata.get("task_type", "unknown")
                pi_task_index = next(i for i, t in enumerate(result.job.tasks) if t.id == result.task_id)
                pis = derive_patch_intents(pi_artifact, pi_task_type)
                pi_errors = verify_patch_intent_set(pis)
                if pi_errors:
                    print(
                        f"  warning: patch intent verification failed "
                        f"({len(pi_errors)} error(s)) — not materialized", file=sys.stderr,
                    )
                    pi_artifact.metadata["patch_intent_errors"] = pi_errors
                    log.log("patch_intent_failed", task_id=str(result.task_id),
                            outcome="failed", error_count=len(pi_errors))
                elif pis.intents:
                    pi_mf = materialize_patch_intents(pis, runtime, pi_task_index, pi_task_type)
                    if pi_mf is not None:
                        pi_artifact.metadata["patch_intent_file"] = str(pi_mf.path)
                        pi_artifact.metadata["patch_intent_count"] = len(pis.intents)
                        patch_intent_count = len(pis.intents)

                    pi_repo_root = (
                        Path(job.metadata["target_repo"]) if job.metadata.get("target_repo") else None
                    )
                    dry_run_results = generate_dry_run_preview(
                        pis, pi_artifact.content or "", pi_task_type, pi_repo_root,
                    )
                    if dry_run_results:
                        pi_artifact.metadata["patch_intent_explanations"] = [
                            {"file": r.target_path, "action": r.action, "risk": r.risk_level,
                             "reason": r.reason, "summary": r.summary}
                            for r in dry_run_results
                        ]
                        pi_artifact.metadata["patch_intent_risks"] = [r.risk_level for r in dry_run_results]
                        combined_preview = "\n\n".join(r.diff_preview for r in dry_run_results)
                        pi_artifact.metadata["patch_intent_diff_preview"] = truncate_preview(combined_preview)
                        dry_run_block = format_dry_run_explanations(dry_run_results)

                    risk_levels = pi_artifact.metadata.get("patch_intent_risks", [])
                    log.log("patch_intent_created", task_id=str(result.task_id),
                            outcome="created", intent_count=len(pis.intents), risk_levels=risk_levels)
                else:
                    log.log("patch_intent_skipped", task_id=str(result.task_id), outcome="no_intents")

    save_job(result.job)

    task = next(t for t in result.job.tasks if t.id == result.task_id)
    task_type = task.inputs.get("task_type", "unknown")
    pending_remaining = sum(1 for t in result.job.tasks if t.status.value == "pending")

    if vr.passed:
        log.log("task_run_completed", task_id=str(result.task_id), outcome="pass")
    else:
        log.log("task_run_failed", task_id=str(result.task_id), outcome="fail")

    file_info = f" file={mf.path}"
    repo_info = f" repo={repo_applied[0]}" if repo_applied else ""
    pi_info = f" patch_intents={patch_intent_count}" if patch_intent_count > 0 else ""
    verified_info = "verified=pass" if vr.passed else f"verified=FAIL({len(vr.failures)} check(s))"
    print(
        f"Job {result.job.id} | task={result.task_id} type={task_type} "
        f"role=builder model={builder.model} elapsed={round(elapsed_ms)}ms "
        f"remaining={pending_remaining}{file_info}{repo_info}{pi_info} {verified_info}"
        f"  log={log.path}"
    )
    if dry_run_block:
        print(dry_run_block)
    if not vr.passed:
        for failure in vr.failures:
            print(f"  verification failure: {failure.check}: {failure.message}", file=sys.stderr)
        sys.exit(1)


def _cmd_run_loop(
    job_id_str: str,
    *,
    max_cycles: int = 3,
    autonomy_level: int = 1,
    auto_approve_low_risk: bool = False,
    no_tests: bool = False,
    json_output: bool = False,
) -> None:
    import json as _json

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

    from packages.orchestration.autonomy_loop import (
        export_loop_result_json,
        run_autonomy_loop,
        summarize_loop_result,
    )
    from packages.orchestration.run_log import RunLogWriter
    from packages.orchestration.timeline import load_run_events

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job_id)

    result = run_autonomy_loop(
        job, events,
        max_cycles=max_cycles,
        autonomy_level=autonomy_level,
    )

    # Emit run-log events
    log = RunLogWriter(job_id=job.id)
    for c in result.cycles:
        log.log(
            "agent_loop_cycle_decision",
            cycle=c.cycle,
            decision=c.decision,
            reason=c.reason,
            next_action=c.next_action,
            blocked_by=c.blocked_by,
            token_mode=c.token_mode,
            selected_worker=c.selected_worker,
            readiness_level=c.readiness_level,
        )
    log.log(
        "agent_loop_stopped",
        final_decision=result.final_decision,
        stop_reason=result.stop_reasons[0] if result.stop_reasons else "",
        cycles_run=len(result.cycles),
        unresolved_blocker_count=len(result.stop_reasons),
    )

    if json_output:
        print(_json.dumps(export_loop_result_json(result), sort_keys=True))
    else:
        print(summarize_loop_result(result))


def _cmd_job_summary(job_id_str: str, *, json_output: bool = False) -> None:
    """Print an honest summary of job state — truth contract."""
    import json as _json

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

    from packages.orchestration.timeline import load_run_events

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job.id)

    state = job.state.value if hasattr(job.state, "value") else str(job.state)
    task_count = len(job.tasks)
    done_count = sum(1 for t in job.tasks if (t.status.value if hasattr(t.status, "value") else str(t.status)) == "completed")
    pending_count = sum(1 for t in job.tasks if (t.status.value if hasattr(t.status, "value") else str(t.status)) == "pending")
    event_count = len(events)
    has_real_events = event_count > 0

    summary = {
        "job_id": str(job.id),
        "name": job.name,
        "state": state,
        "task_count": task_count,
        "done_count": done_count,
        "pending_count": pending_count,
        "event_count": event_count,
        "demo_mode": not has_real_events,
        "data_honest": True,
        "synthetic_fields": 0 if has_real_events else 1,
    }

    if json_output:
        print(_json.dumps(summary, indent=2))
    else:
        mode_label = "LIVE" if has_real_events else "DEMO (no events yet)"
        print(f"Job {job.id}")
        print(f"  Name:    {job.name}")
        print(f"  State:   {state}")
        print(f"  Mode:    {mode_label}")
        print(f"  Tasks:   {done_count}/{task_count} done, {pending_count} pending")
        print(f"  Events:  {event_count}")


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "job.create": lambda args: _cmd_create_job(
        args.prompt,
        project_id=getattr(args, "project", None),
        task_type=getattr(args, "task_type", None),
        task_description=getattr(args, "task_description", None),
    ),
    "job.list": lambda args: _cmd_list_jobs(),
    "job.show": lambda args: _cmd_show_job(args.job_id),
    "job.attach-repo": lambda args: _cmd_attach_repo(args.job_id, args.repo_path),
    "job.permit": lambda args: _cmd_set_permission(args.job_id, args.action, args.permission),
    "job.permissions": lambda args: _cmd_show_permissions(args.job_id),
    "job.run-next": lambda args: _cmd_run_next_task_local(args.job_id),
    "job.plan": lambda args: _cmd_plan_job_local(args.job_id),
    "job.run-loop": lambda args: _cmd_run_loop(
        args.job_id,
        max_cycles=int(getattr(args, "max_cycles", "3")),
        autonomy_level=int(getattr(args, "autonomy_level", "1")),
        auto_approve_low_risk=getattr(args, "auto_approve_low_risk", False),
        no_tests=getattr(args, "no_tests", False),
        json_output=getattr(args, "json", False),
    ),
    "job.summary": lambda args: _cmd_job_summary(
        args.job_id,
        json_output=getattr(args, "json", False),
    ),
}
