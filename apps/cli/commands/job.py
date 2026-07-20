"""Job group command handlers."""

from __future__ import annotations

import re
import sys
import time
from collections.abc import Callable
from typing import TYPE_CHECKING
from uuid import UUID

from packages.core.models import Job, RunState, Task
from packages.orchestration.data_paths import resolve_data_root
from packages.orchestration.job_runner import PlanJobResult
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

    # F005: enforce the PlannerPlan schema natively (Ollama format=), with a
    # compact schema_v, one parse retry, and a prompt-trace entry per actual call.
    # Structured mode is the DEFAULT; the legacy planner.plan path is used ONLY
    # when REMEDY_PLANNER_FREETEXT=1. There is no silent fallback: if the planner
    # lacks the structured (plan_raw) capability, structured mode fails clearly.
    from packages.orchestration.prompt_trace import build_trace_entry, write_trace_jsonl
    from packages.orchestration.schemas import PlannerPlan, to_json_schema
    from packages.orchestration.structured_planner import (
        StructuredParseError,
        make_structured_planner,
        planner_structured_enabled,
    )

    _plan_traces: list = []

    def _record_plan_call(
        attempt: int, schema_v: str, is_parse_retry: bool, effective_prompt: str,
    ) -> None:
        # F005 Finding 2: fires IMMEDIATELY BEFORE every real plan_raw() call, so
        # the trace exists even when the provider raises (network down) or returns
        # invalid JSON. Every real structured Planner call logs its schema_v.
        _plan_traces.append(build_trace_entry(
            prompt_text=effective_prompt,
            role="planner",
            job_id=str(job.id),
            provider="ollama",
            provider_kind="ollama",
            prompt_kind="plan-retry" if is_parse_retry else "plan",
            configured_model=planner.model,
            schema_v=schema_v,
            phase="plan-retry" if is_parse_retry else "plan",
            transport_attempt=attempt,
            is_transport_retry=False,
        ))

    _structured_planner = planner_structured_enabled()
    if _structured_planner:
        _raw_plan = getattr(planner, "plan_raw", None)
        if not callable(_raw_plan):
            log.log("planning_failed", provider="ollama", role="planner", model=planner.model,
                    outcome="error", message="structured planner capability missing",
                    error_category="config")
            print(
                "Error: structured planner requires a plan_raw capability the "
                "installed planner does not provide; set REMEDY_PLANNER_FREETEXT=1 "
                "to use the legacy planner.",
                file=sys.stderr,
            )
            sys.exit(1)
        _pp_schema = to_json_schema(PlannerPlan)
        call_planner = make_structured_planner(
            lambda p, _a, _r=_raw_plan, _s=_pp_schema: _r(p, schema=_s),
            on_call=_record_plan_call,
            native_schema=True,
        )
    else:
        call_planner = planner.plan

    def _persist_plan_traces() -> None:
        if _plan_traces:
            try:
                write_trace_jsonl(_plan_traces, log.path.parent / "prompt_trace.jsonl")
            except OSError:
                pass

    start = time.monotonic()
    try:
        result: PlanJobResult = plan_job_with_llm(job, call_planner)
    except StructuredParseError as exc:
        _persist_plan_traces()
        # F005/F010: parse exhaustion is the stable class ``parse``, not the
        # exception's class name.
        log.log("planning_failed", provider="ollama", role="planner", model=planner.model,
                outcome="error", message=str(exc), error_category="parse")
        print(f"Error: planner structured output invalid after one retry: {exc}", file=sys.stderr)
        sys.exit(1)
    except ImportError as exc:
        _persist_plan_traces()
        log.log("planning_failed", provider="ollama", role="planner", model=planner.model,
                outcome="error", message="planning failed", error_category=type(exc).__name__)
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        _persist_plan_traces()
        log.log("planning_failed", provider="ollama", role="planner", model=planner.model,
                outcome="error", message="planning failed", error_category=type(exc).__name__)
        print(f"Error: Ollama planning failed: {exc}", file=sys.stderr)
        sys.exit(1)
    elapsed_ms = (time.monotonic() - start) * 1000
    _persist_plan_traces()

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


def _cmd_checkpoints(job_id_str: str, *, json_output: bool = False) -> None:
    import json as _json

    from packages.orchestration.event_replay import (
        export_checkpoints_json,
        find_checkpoints,
        replay_job,
    )

    data_dir = resolve_data_root()
    replay = replay_job(job_id_str, data_dir)
    cps = find_checkpoints(replay)

    if json_output:
        print(_json.dumps({
            "version": 1,
            "job_id": job_id_str,
            "checkpoints": export_checkpoints_json(cps),
        }, indent=2))
    else:
        if not cps:
            print(f"No checkpoints for job {job_id_str[:8]}.")
            return
        for cp in cps:
            safe = "safe" if cp.safe_to_resume else "blocked"
            reason = f" ({cp.blocked_reason})" if cp.blocked_reason else ""
            print(f"  [{safe}] {cp.kind}: {cp.label}{reason}")
            if cp.next_command:
                print(f"         next: {cp.next_command}")


def _cmd_resume(
    job_id_str: str,
    *,
    checkpoint_id: str,
    dry_run: bool = False,
    json_output: bool = False,
) -> None:
    import json as _json

    from packages.orchestration.event_replay import (
        export_dry_run_json,
        resume_dry_run,
    )

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

    data_dir = resolve_data_root()

    if dry_run:
        dr = resume_dry_run(job, checkpoint_id, data_dir)
        if json_output:
            print(_json.dumps(export_dry_run_json(dr), indent=2))
        else:
            status = "can resume" if dr.can_resume else "blocked"
            print(f"Resume dry-run: {status}")
            print(f"  Checkpoint: {dr.checkpoint_kind}")
            if dr.would_run_stage:
                print(f"  Would run: {dr.would_run_stage}")
            if dr.blocked_reason:
                print(f"  Blocked: {dr.blocked_reason}")
            if dr.next_command:
                print(f"  Next: {dr.next_command}")
            print(f"  {dr.safety_summary}")
        return

    # Real resume — conservative v1
    from packages.orchestration.event_replay import find_checkpoints, replay_job
    from packages.orchestration.timeline import append_run_event

    replay = replay_job(job_id_str, data_dir)
    cps = find_checkpoints(replay)
    cp = next((c for c in cps if c.id == checkpoint_id), None)

    if not cp:
        print(f"Error: checkpoint not found: {checkpoint_id}", file=sys.stderr)
        sys.exit(1)

    if not cp.safe_to_resume:
        append_run_event(data_dir, job_id, event="resume_blocked", metadata={
            "checkpoint_id": checkpoint_id, "checkpoint_kind": cp.kind,
            "blocked_reason": cp.blocked_reason,
        })
        print(f"Error: checkpoint not safe to resume: {cp.blocked_reason}", file=sys.stderr)
        sys.exit(1)

    # F006 phase 1 (prepare): lock and verify the exact recorded worktree of the
    # interrupted run. Nothing is removed yet — the continuation has to run INSIDE
    # the recovered worktree, so it must still be there.
    #
    # A job owns exactly ONE worktree, so exactly one recoverable worktree may be
    # resumed by one continuation. A legacy record with several recoverable runs is
    # ambiguous: it is blocked honestly (and every worktree retained and unlocked)
    # rather than silently resuming the first one and destroying the rest.
    from packages.orchestration import worktree_resume as _wtr
    prepared = _wtr.prepare_job_worktrees(job_id_str)
    sessions = [s for s, _o in prepared if s is not None]
    wt_outcomes = [o for _s, o in prepared if o.applicable]
    wt_json = [o.to_json() for o in wt_outcomes]

    def _retain_all(reason: str) -> None:
        for s in sessions:
            try:
                _wtr.retain_worktree_resume(s, reason)
            except Exception:                     # one failure must not leak the rest
                _wtr.W.release_lock(s.handle)

    if len(sessions) > 1:
        _retain_all("ambiguous_recoverable_worktrees")
        append_run_event(data_dir, job_id, event="resume_blocked", metadata={
            "checkpoint_id": checkpoint_id, "checkpoint_kind": cp.kind,
            "blocked_reason": "ambiguous_recoverable_worktrees",
            "run_ids": [s.run_id for s in sessions],
        })
        if json_output:
            print(_json.dumps({
                "resumed": False,
                "blocked_reason": "ambiguous_recoverable_worktrees",
                "worktrees": [o.to_json() for o in wt_outcomes],
            }, indent=2))
        else:
            print("Resume blocked: ambiguous_recoverable_worktrees "
                  f"({', '.join(s.run_id for s in sessions)})", file=sys.stderr)
        sys.exit(1)

    wt_blocked = [o for o in wt_outcomes if o.blocked and not o.recovered]
    if wt_blocked:
        _retain_all("resume blocked before continuation")
        append_run_event(data_dir, job_id, event="resume_blocked", metadata={
            "checkpoint_id": checkpoint_id, "checkpoint_kind": cp.kind,
            "blocked_reason": "worktree_recovery_blocked",
            "worktrees": wt_json,
        })
        if json_output:
            print(_json.dumps({
                "resumed": False,
                "blocked_reason": "worktree_recovery_blocked",
                "worktrees": wt_json,
            }, indent=2))
        else:
            for o in wt_blocked:
                print(f"Resume blocked: worktree {o.run_id}: {o.blocked_reason}",
                      file=sys.stderr)
        sys.exit(1)
    for o in wt_outcomes:
        append_run_event(data_dir, job_id, event="worktree_prepared", metadata={
            "run_id": o.run_id, "branch": o.branch,
            "worktree_path": o.worktree_path,
            "result_diff_sha256": o.result_diff_sha256,
        })
        if not json_output:
            print(f"Recovered worktree {o.run_id} on branch {o.branch}; "
                  f"continuing inside it.")

    def _finish_worktrees(ok: bool, reason: str) -> None:
        """Phase 3: finalize ONLY the worktree the continuation actually used, and
        only on success. A failure while finalizing one session must never leave
        another session's lock held."""
        for idx, s in enumerate(sessions):
            try:
                if ok:
                    out = _wtr.finalize_worktree_resume(s)
                    event = "worktree_recovered"
                else:
                    out = _wtr.retain_worktree_resume(s, reason)
                    event = "worktree_retained"
            except Exception as exc:
                _wtr.W.release_lock(s.handle)      # never strand the lock
                append_run_event(data_dir, job_id, event="worktree_retained", metadata={
                    "run_id": s.run_id,
                    "cleanup_status": "failed_recoverable",
                    "cleanup_error": f"{type(exc).__name__}: {exc}",
                })
                continue
            wt_json[idx] = out.to_json()
            append_run_event(data_dir, job_id, event=event, metadata={
                "run_id": out.run_id, "branch": out.branch,
                "cleanup_status": out.cleanup_status,
                "branch_kept": out.branch_kept,
                "result_diff_sha256": out.result_diff_sha256,
            })

    # Resume from_apply: run tests via Remedy's test_runner, inside the recovered
    # worktree when there is one.
    if cp.resume_mode == "from_apply":
        from packages.orchestration.event_replay import (
            execute_resume_from_apply,
            export_resume_result_json,
        )
        workspace_root = str(sessions[0].workspace_root) if sessions else None
        try:
            result = execute_resume_from_apply(
                job, checkpoint_id, data_dir, workspace_root=workspace_root,
            )
        except Exception as exc:
            # The continuation blew up: keep the worktree and its uncommitted
            # changes so a later resume can pick the SAME one up again.
            _finish_worktrees(False, f"continuation raised: {type(exc).__name__}: {exc}")
            raise

        continued_ok = bool(result.resumed) and result.tests_passed is not False
        _finish_worktrees(
            continued_ok,
            result.blocked_reason or "continuation did not complete successfully",
        )

        if json_output:
            _payload = export_resume_result_json(result)
            _payload["worktrees"] = wt_json
            print(_json.dumps(_payload, indent=2))
        else:
            if result.resumed:
                status_str = "passed" if result.tests_passed else "failed"
                print(f"Resumed from {cp.kind}. Tests {status_str}.")
                if result.test_run_id:
                    print(f"  Test run: {result.test_run_id}")
            else:
                print(f"Resume blocked: {result.blocked_reason}")
        return
    _finish_worktrees(False, f"resume mode {cp.resume_mode!r} not implemented")

    # Unimplemented resume mode — do not fake success
    from packages.orchestration.timeline import append_run_event as _emit
    _emit(data_dir, job_id, event="resume_blocked", metadata={
        "checkpoint_id": checkpoint_id, "checkpoint_kind": cp.kind,
        "blocked_reason": "resume_mode_not_implemented",
    })
    if json_output:
        print(_json.dumps({
            "resumed": False,
            "blocked_reason": "resume_mode_not_implemented",
            "checkpoint_kind": cp.kind,
            "resume_mode": cp.resume_mode,
            "worktrees": wt_json,
        }))
    else:
        print(f"Resume blocked: mode '{cp.resume_mode}' not implemented yet.")



def _extract_job_truth(job: Job) -> dict:
    """Extract safe truth from job model for status/report views."""
    artifact_count = len(job.artifacts) if hasattr(job, 'artifacts') else 0

    # Find patch intents and approval/apply status from artifact metadata
    patch_intent_ids: list[str] = []
    pending_intents = 0
    code_applied = False
    for a in (job.artifacts if hasattr(job, 'artifacts') else []):
        meta = a.metadata if hasattr(a, 'metadata') and a.metadata else {}
        if meta.get('patch_intent_count'):
            intent_id = str(a.id) + '-0'
            patch_intent_ids.append(intent_id)
            # Check if this intent has been applied
            apply_records = meta.get('patch_intent_apply_records', {})
            intent_applied = False
            for rec in apply_records.values():
                if isinstance(rec, dict) and rec.get('state') == 'applied':
                    code_applied = True
                    intent_applied = True
                    break
            # Check approval state
            approvals = meta.get('patch_intent_approvals', {})
            intent_approved = approvals.get(intent_id, {}).get('state') == 'approved'
            # Only pending if not yet applied and not approved
            if not intent_applied and not intent_approved:
                pending_intents += 1

    approval_required = pending_intents > 0
    latest_stop_reason = ''

    # Check timeline for stop reason
    from packages.orchestration.timeline import load_run_events
    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job.id)
    for ev in reversed(events):
        ev_data = ev if isinstance(ev, dict) else (ev.data if hasattr(ev, 'data') else {})
        if isinstance(ev_data, dict):
            sr = ev_data.get('stop_reason', '')
            if sr:
                latest_stop_reason = sr
                break
            phase = ev_data.get('phase', '')
            status_val = ev_data.get('status', '')
            if phase == 'approval_required' or status_val == 'approval_required':
                latest_stop_reason = 'approval_required'
                if not code_applied:
                    approval_required = True
                break

    # Also check fulfillment events for code_applied
    if not code_applied:
        for ev in events:
            ev_data = ev if isinstance(ev, dict) else {}
            if isinstance(ev_data, dict) and ev_data.get('event') == 'fulfillment_applied':
                code_applied = True
                break

    # Load fulfillment record if available
    fulfillment_status = ''
    fulfillment_id = ''
    staging_used = False
    staging_promoted = False
    fulfillment_blockers: list[str] = []
    fulfillment_next_action = ''
    try:
        from packages.orchestration.job_fulfillment import list_fulfillment_records
        records = list_fulfillment_records(str(job.id), data_dir)
        if records:
            latest = records[-1]
            fulfillment_status = latest.status.value
            fulfillment_id = latest.fulfillment_id
            staging_used = latest.staging_used
            staging_promoted = latest.staging_promoted
            fulfillment_blockers = latest.contract_blockers or []
            fulfillment_next_action = latest.next_safe_action or ''
            # Surface fulfillment stop_reason as latest_stop_reason
            if latest.stop_reason and not latest_stop_reason:
                latest_stop_reason = latest.stop_reason
            # Derive blocker from stop_reason if contract_blockers empty
            if latest.status.value == 'blocked' and not fulfillment_blockers:
                sr = latest.stop_reason or 'unknown'
                # Extract first colon-delimited part as safe blocker
                safe_reason = sr.split(':')[0] if ':' in sr else sr
                fulfillment_blockers = [f'fulfillment_blocked:{safe_reason}']
    except Exception:
        pass

    # When staging was used, staging_promoted is authoritative for code_applied
    if staging_used:
        code_applied = staging_promoted

    return {
        'artifact_count': artifact_count,
        'patch_intent_ids': patch_intent_ids,
        'approval_required': approval_required,
        'latest_stop_reason': latest_stop_reason,
        'event_count': len(events),
        'code_applied': code_applied,
        'fulfillment_status': fulfillment_status,
        'fulfillment_id': fulfillment_id,
        'staging_used': staging_used,
        'staging_promoted': staging_promoted,
        'fulfillment_blockers': fulfillment_blockers,
        'fulfillment_next_action': fulfillment_next_action,
    }


def _cmd_job_status(job_id_str: str, *, json_output: bool = False) -> None:
    """Job status -- safe read-only view of current job state."""
    import json as _json

    try:
        job_id = UUID(job_id_str)
    except ValueError:
        if json_output:
            print(_json.dumps({'error': 'invalid_job_id', 'job_id': job_id_str}))
        else:
            print(f'Error: invalid job ID: {job_id_str!r}', file=sys.stderr)
        sys.exit(1)
    try:
        job = load_job(job_id)
    except JobNotFoundError:
        if json_output:
            print(_json.dumps({'error': 'job_not_found', 'job_id': job_id_str}))
        else:
            print(f'Error: job not found: {job_id_str}', file=sys.stderr)
        sys.exit(1)

    truth = _extract_job_truth(job)

    state = job.state.value if hasattr(job.state, 'value') else str(job.state)
    task_count = len(job.tasks)
    done_count = sum(1 for t in job.tasks if (t.status.value if hasattr(t.status, 'value') else str(t.status)) == 'completed')
    pending_count = sum(1 for t in job.tasks if (t.status.value if hasattr(t.status, 'value') else str(t.status)) == 'pending')

    blockers: list[str] = []
    if truth['approval_required']:
        blockers.append('approval_required')
    elif pending_count > 0 and state == 'pending':
        blockers.append('job_not_started')
    if state == 'blocked':
        blockers.append('job_blocked')
    # Surface fulfillment blockers
    if truth.get('fulfillment_blockers'):
        blockers.extend(truth['fulfillment_blockers'])

    if truth['approval_required']:
        next_action = 'remedy patch approve <job_id> <patch_intent_id>'
    elif truth.get('fulfillment_next_action'):
        next_action = truth['fulfillment_next_action']
    elif state == 'completed' and truth.get('fulfillment_status') == 'completed_verified':
        next_action = f'remedy propose list {job_id_str} --json'
    elif pending_count > 0:
        next_action = 'remedy job run-loop <job_id> --json'
    elif state in ('completed', 'failed'):
        next_action = f'remedy job report {job_id_str} --json'
    else:
        next_action = f'remedy job report {job_id_str} --json'

    status = {
        'job_id': str(job.id),
        'name': job.name,
        'state': state,
        'task_count': task_count,
        'done_count': done_count,
        'pending_count': pending_count,
        'event_count': truth['event_count'],
        'artifact_count': truth['artifact_count'],
        'patch_intent_ids': truth['patch_intent_ids'],
        'approval_required': truth['approval_required'],
        'code_applied': truth['code_applied'],
        'latest_stop_reason': truth['latest_stop_reason'],
        'fulfillment_status': truth.get('fulfillment_status', ''),
        'staging_used': truth.get('staging_used', False),
        'staging_promoted': truth.get('staging_promoted', False),
        'blockers': blockers,
        'next_safe_action': next_action,
    }

    if json_output:
        print(_json.dumps(status, indent=2))
    else:
        print(f'Job {job.id}')
        print(f'  Name:      {job.name}')
        print(f'  State:     {state}')
        print(f'  Tasks:     {done_count}/{task_count} done, {pending_count} pending')
        print(f'  Events:    {truth["event_count"]}')
        print(f'  Artifacts: {truth["artifact_count"]}')
        if truth['approval_required']:
            print('  Approval:  REQUIRED')
        if blockers:
            bl = ', '.join(blockers)
            print(f'  Blockers:  {bl}')
        print(f'  Next:      {next_action}')


def _cmd_job_report(job_id_str: str, *, json_output: bool = False) -> None:
    """Job report -- safe read-only report of job progress and evidence."""
    import json as _json

    try:
        job_id = UUID(job_id_str)
    except ValueError:
        if json_output:
            print(_json.dumps({'error': 'invalid_job_id', 'job_id': job_id_str}))
        else:
            print(f'Error: invalid job ID: {job_id_str!r}', file=sys.stderr)
        sys.exit(1)
    try:
        job = load_job(job_id)
    except JobNotFoundError:
        if json_output:
            print(_json.dumps({'error': 'job_not_found', 'job_id': job_id_str}))
        else:
            print(f'Error: job not found: {job_id_str}', file=sys.stderr)
        sys.exit(1)

    truth = _extract_job_truth(job)

    state = job.state.value if hasattr(job.state, 'value') else str(job.state)
    task_count = len(job.tasks)
    done_count = sum(1 for t in job.tasks if (t.status.value if hasattr(t.status, 'value') else str(t.status)) == 'completed')
    pending_count = sum(1 for t in job.tasks if (t.status.value if hasattr(t.status, 'value') else str(t.status)) == 'pending')

    task_details = []
    for t in job.tasks:
        t_state = t.status.value if hasattr(t.status, 'value') else str(t.status)
        task_details.append({
            'task_id': str(t.id),
            'status': t_state,
            'description': t.description[:120] if t.description else '',
            'type': t.inputs.get('task_type', 'unknown') if t.inputs else 'unknown',
        })

    # Include fulfillment data if available
    fulfillment_data: dict = {}
    try:
        from packages.orchestration.job_fulfillment import (
            export_job_fulfillment_json,
            list_fulfillment_records,
        )
        data_dir = resolve_data_root()
        records = list_fulfillment_records(str(job.id), data_dir)
        if records:
            fulfillment_data = export_job_fulfillment_json(records[-1])
    except Exception:
        pass

    report = {
        'job_id': str(job.id),
        'name': job.name,
        'state': state,
        'task_count': task_count,
        'done_count': done_count,
        'pending_count': pending_count,
        'event_count': truth['event_count'],
        'artifact_count': truth['artifact_count'],
        'patch_intent_ids': truth['patch_intent_ids'],
        'approval_required': truth['approval_required'],
        'latest_stop_reason': truth['latest_stop_reason'],
        'code_applied': truth['code_applied'],
        'fulfillment_status': truth.get('fulfillment_status', ''),
        'staging_used': truth.get('staging_used', False),
        'staging_promoted': truth.get('staging_promoted', False),
        'fulfillment_blockers': truth.get('fulfillment_blockers', []),
        'next_safe_action': truth.get('fulfillment_next_action', ''),
        'tasks': task_details,
    }
    if fulfillment_data:
        report['fulfillment'] = fulfillment_data

    if json_output:
        print(_json.dumps(report, indent=2))
    else:
        print(f'Job Report: {job.id}')
        print(f'  Name:      {job.name}')
        print(f'  State:     {state}')
        print(f'  Tasks:     {done_count}/{task_count} done, {pending_count} pending')
        print(f'  Events:    {truth["event_count"]}')
        print(f'  Artifacts: {truth["artifact_count"]}')
        if truth['approval_required']:
            print('  Approval:  REQUIRED')
        if truth['latest_stop_reason']:
            print(f'  Stop:      {truth["latest_stop_reason"]}')
        print(f'  Applied:   {"Yes" if truth["code_applied"] else "No"}')
        if task_details:
            print('  Task details:')
            for td in task_details:
                s = td['status']
                ty = td['type']
                desc = td['description']
                print(f'    [{s:<10}] {ty}: {desc}')


def _cmd_job_fulfill(
    job_id_str: str,
    *,
    fixture_demo: bool = False,
    json_output: bool = False,
) -> None:
    """Run job fulfillment spine — fixture-demo mode only in v0."""
    import json as _json

    try:
        job_id = UUID(job_id_str)
    except ValueError:
        if json_output:
            print(_json.dumps({'error': 'invalid_job_id', 'job_id': job_id_str}))
        else:
            print(f'Error: invalid job ID: {job_id_str!r}', file=sys.stderr)
        sys.exit(1)

    if not fixture_demo:
        if json_output:
            print(_json.dumps({'error': 'fixture_demo_required',
                               'message': 'v0 fulfillment requires --fixture-demo flag'}))
        else:
            print('Error: v0 fulfillment requires --fixture-demo flag', file=sys.stderr)
        sys.exit(1)

    try:
        job = load_job(job_id)
    except JobNotFoundError:
        if json_output:
            print(_json.dumps({'error': 'job_not_found', 'job_id': job_id_str}))
        else:
            print(f'Error: job not found: {job_id_str}', file=sys.stderr)
        sys.exit(1)

    repo_str = job.metadata.get('target_repo', '')
    if not repo_str:
        if json_output:
            print(_json.dumps({'error': 'no_repo_attached',
                               'message': 'Attach a repo first: remedy job attach-repo <id> <path>'}))
        else:
            print('Error: no repo attached to job', file=sys.stderr)
        sys.exit(1)

    from pathlib import Path as _Path
    repo_root = _Path(repo_str)

    from packages.orchestration.job_fulfillment import (
        export_job_fulfillment_json,
        run_job_fulfill,
        summarize_job_fulfillment,
    )

    record = run_job_fulfill(str(job_id), repo_root, data_dir=resolve_data_root())

    if json_output:
        print(_json.dumps(export_job_fulfillment_json(record), indent=2))
    else:
        print(summarize_job_fulfillment(record))


def _cmd_job_fences(job_id_str: str, *, json_output: bool = False) -> None:
    """Show effective scope fences for a job (F017 T003)."""
    import json as _json
    from pathlib import Path

    from packages.orchestration.config import get_config
    from packages.orchestration.scope_fences import (
        BUILTIN_DENY,
        FenceConfigError,
        resolve_effective_builtins,
        resolve_fence_spec_effective,
    )

    try:
        job = load_job(UUID(job_id_str))
    except (ValueError, JobNotFoundError):
        print(f"Job not found: {job_id_str}", file=sys.stderr)
        sys.exit(1)

    repo_str = job.metadata.get("target_repo", "") or "."
    repo_root = Path(repo_str)

    job_fences_dict = None
    if job.fences is not None:
        job_fences_dict = {"allow": job.fences.allow, "deny": job.fences.deny}

    try:
        eff = resolve_fence_spec_effective(repo_root, job_fences=job_fences_dict)
    except FenceConfigError as exc:
        print(f"Fence config error: {exc}", file=sys.stderr)
        sys.exit(1)
    spec = eff.spec
    source = eff.source

    cfg = get_config()
    scope_allow = cfg.get("scope.allow")
    scope_deny = cfg.get("scope.deny")

    warnings: list[str] = list(eff.warnings)
    if not spec.allow_globs and not spec.deny_globs:
        warnings.append("no configured allow/deny globs — defaults apply (allow all, builtin denies only)")

    builtins = list(BUILTIN_DENY)
    extra = []
    if repo_root.is_dir():
        try:
            extra_t = resolve_effective_builtins(repo_root)
            extra = [e for e in extra_t]
        except RuntimeError as exc:
            warnings.append(f"builtin resolution failed: {exc}")

    result = {
        "job_id": job_id_str,
        "source": source,
        "allow_globs": list(spec.allow_globs),
        "deny_globs": list(spec.deny_globs),
        "builtin_denies": [
            {"pattern": p, "reason": r} for p, r in builtins
        ],
        "extra_builtin_denies": [
            {"pattern": p, "reason": r} for p, r in extra
        ],
        "config_scope_allow": scope_allow,
        "config_scope_deny": scope_deny,
        "warnings": warnings,
    }

    if json_output:
        print(_json.dumps(result, indent=2))
    else:
        print(f"Scope fences for job {job_id_str[:8]}:")
        print(f"  Source: {source}")
        if spec.allow_globs:
            print(f"  Allow:  {', '.join(spec.allow_globs)}")
        else:
            print("  Allow:  (all — no restrictions)")
        if spec.deny_globs:
            print(f"  Deny:   {', '.join(spec.deny_globs)}")
        else:
            print("  Deny:   (none beyond builtins)")
        print("  Builtin denies:")
        for p, r in builtins:
            print(f"    {p:30s} — {r}")
        for p, r in extra:
            print(f"    {p:30s} — {r}")
        if warnings:
            print("  Warnings:")
            for w in warnings:
                print(f"    ⚠ {w}")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
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
    "job.checkpoints": lambda args: _cmd_checkpoints(
        args.job_id,
        json_output=getattr(args, "json", False),
    ),
    "job.resume": lambda args: _cmd_resume(
        args.job_id,
        checkpoint_id=getattr(args, "checkpoint", ""),
        dry_run=getattr(args, "dry_run", False),
        json_output=getattr(args, "json", False),
    ),
    "job.status": lambda args: _cmd_job_status(
        args.job_id,
        json_output=getattr(args, "json", False),
    ),
    "job.report": lambda args: _cmd_job_report(
        args.job_id,
        json_output=getattr(args, "json", False),
    ),
    "job.fences": lambda args: _cmd_job_fences(
        args.job_id,
        json_output=getattr(args, "json", False),
    ),
    "job.fulfill": lambda args: _cmd_job_fulfill(
        args.job_id,
        fixture_demo=getattr(args, "fixture_demo", False),
        json_output=getattr(args, "json", False),
    ),
    "job.enqueue": lambda args: _cmd_enqueue(args.job_id),
    "job.pause": lambda args: _cmd_pause(args.job_id),
    "job.cancel": lambda args: _cmd_cancel(args.job_id),
    "job.resume-queue": lambda args: _cmd_resume_queue(args.job_id),
}


def _cmd_enqueue(job_id_str: str) -> None:
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.worker_queue import enqueue_job
    entry = enqueue_job(job_id_str, resolve_data_root())
    print(f"Job {job_id_str[:8]}: {entry.lifecycle_state}")


def _cmd_pause(job_id_str: str) -> None:
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.worker_queue import pause_job
    entry = pause_job(job_id_str, resolve_data_root())
    if entry:
        print(f"Job {job_id_str[:8]}: {entry.lifecycle_state}")
    else:
        print(f"Cannot pause job {job_id_str[:8]}", file=sys.stderr)
        sys.exit(1)


def _cmd_cancel(job_id_str: str) -> None:
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.worker_queue import cancel_job
    entry = cancel_job(job_id_str, resolve_data_root())
    if entry:
        print(f"Job {job_id_str[:8]}: {entry.lifecycle_state}")
    else:
        print(f"Cannot cancel job {job_id_str[:8]}", file=sys.stderr)
        sys.exit(1)


def _cmd_resume_queue(job_id_str: str) -> None:
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.worker_queue import resume_queued
    entry = resume_queued(job_id_str, resolve_data_root())
    if entry:
        print(f"Job {job_id_str[:8]}: {entry.lifecycle_state}")
    else:
        print(f"Cannot resume job {job_id_str[:8]} (not paused)", file=sys.stderr)
        sys.exit(1)
