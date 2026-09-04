"""Job group command handlers."""

from __future__ import annotations

import re
import sys
import time
from collections.abc import Callable
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

from packages.core.models import Job, RunState, Task
from packages.orchestration.data_paths import resolve_data_root, resolve_job_id
from packages.orchestration.job_runner import PlanJobResult
from packages.orchestration.storage import JobNotFoundError, load_job, save_job

if TYPE_CHECKING:
    import argparse

    from packages.orchestration.project_scope import ProjectScope

_SAFE_TASK_TYPE_RE = re.compile(r'^[A-Za-z0-9_-]+$')


def _cmd_create_job(
    prompt: str,
    *,
    project_id: str | None = None,
    task_type: str | None = None,
    task_description: str | None = None,
    max_total_tokens: str | None = None,
    max_provider_calls: str | None = None,
    max_wall_clock_minutes: str | None = None,
    max_cost_usd: str | None = None,
    deadline: str | None = None,
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

    from packages.orchestration.project_registry import ProjectNotFoundError, select_project

    project = None
    try:
        project, _src = select_project(project_id, ".")
        project_id = str(project.id)
    except ProjectNotFoundError:
        print(
            "Error: no project found. Run: remedy init\n"
            "  or pass --project <slug-or-id>",
            file=sys.stderr,
        )
        sys.exit(3)

    metadata: dict = {}
    metadata["project_id"] = project_id

    tasks: list[Task] = []
    state = RunState.PENDING
    if task_type is not None:
        description = (task_description or "").strip() or f"Execute {task_type} task."
        tasks = [Task(description=description, inputs={"task_type": task_type})]
        state = RunState.PLANNED

    from packages.orchestration.budget_resolution import BudgetConfigError, resolve_job_budgets
    _project_repo = None
    if project is not None and hasattr(project, "repo_paths") and project.repo_paths:
        _project_repo = project.repo_paths[0]
    try:
        budgets = resolve_job_budgets(
            cli_max_total_tokens=max_total_tokens,
            cli_max_provider_calls=max_provider_calls,
            cli_max_wall_clock_minutes=max_wall_clock_minutes,
            cli_max_cost_usd=max_cost_usd,
            cli_deadline=deadline,
            project_root=_project_repo,
        )
    except (BudgetConfigError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)

    job = Job(
        name=prompt[:50],
        user_prompt=prompt,
        state=state,
        tasks=tasks,
        metadata=metadata,
        budgets=budgets,
        project_id=project_id,
    )
    save_job(job)
    print(job.id)
    log = RunLogWriter(job_id=job.id)
    log.log("job_created", outcome="created")

    if project is not None:
        from packages.orchestration.project_registry import attach_job, save_project
        attach_job(project, str(job.id))
        save_project(project)


def _known_project_ids() -> set[str]:
    """Build set of existing project IDs (one registry read)."""
    from packages.orchestration.project_registry import _list_projects_readonly
    return {str(p.id) for p in _list_projects_readonly()}


def _cmd_list_jobs(
    *,
    project: str | None = None,
    all_projects: bool = False,
    json_output: bool = False,
    sort: str | None = None,
    desc: bool = False,
    since: str | None = None,
    until: str | None = None,
    limit: str | None = None,
) -> None:
    from packages.orchestration.list_options import ListOptionError, apply_list_options
    from packages.orchestration.project_scope import resolve_scope, scoped_jobs

    scope = resolve_scope(project_flag=project, all_projects=all_projects)
    jobs, degraded, skipped = scoped_jobs(scope)
    try:
        jobs = apply_list_options(
            jobs,
            sort=sort, desc=desc, since=since, until=until, limit=limit,
            sort_fields={
                "created_at": lambda j: j.created_at,
                "name": lambda j: j.name,
                "state": lambda j: j.state.value,
            },
            default_sort_field="created_at",
            date_getter=lambda j: j.created_at.isoformat(),
        )
    except ListOptionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    if json_output:
        import json as _json
        print(_json.dumps({
            "version": 1,
            "job_count": len(jobs),
            "jobs": [{"id": str(job.id), "state": job.state.value, "name": job.name,
                     "created_at": job.created_at.isoformat(),
                     "project_id": job.project_id or ""} for job in jobs],
        }, sort_keys=True))
        return
    if not jobs:
        print("No jobs found.")
        return
    known = _known_project_ids()
    for job in jobs:
        label = _scope_label(job, scope, known)
        print(f"{job.id}  {job.state.value:<12}  {job.created_at.isoformat()}  {job.name}{label}")
    if skipped:
        print(f"  ({len(skipped)} unreadable job file(s) skipped)", file=sys.stderr)


def _scope_label(job: Job, scope: ProjectScope, known_ids: set[str]) -> str:
    """Return display suffix for scoped listings."""
    if job.project_id is None:
        return "  (unscoped)"
    if job.project_id not in known_ids:
        return f"  (orphaned: {job.project_id[:8]})"
    if scope.all_projects and scope.project_id and job.project_id != scope.project_id:
        return f"  (project: {job.project_id[:8]})"
    return ""


def _cmd_show_job(job_id_str: str) -> None:
    job_id = resolve_job_id(job_id_str)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    print(job.model_dump_json(indent=2))
    if job.intake:
        _print_intake_block(job.intake)


def _print_intake_block(intake: dict) -> None:
    def p(s: str) -> None:
        print(s, file=sys.stderr)

    p("\n--- Intake ---")
    p(f"  Goal: {intake.get('goal', '')}")
    refs = intake.get("context_refs", [])
    if refs:
        p(f"  Context refs: {', '.join(refs)}")
    constraints = intake.get("constraints", [])
    if constraints:
        for c in constraints:
            p(f"  Constraint: {c}")
    hints = intake.get("acceptance_hints", [])
    if hints:
        for h in hints:
            p(f"  Acceptance: {h}")
    clarifications = intake.get("clarifications", [])
    if clarifications:
        p("  Clarifications:")
        for cl in clarifications:
            q = cl.get("question", "")
            d = cl.get("default_answer", "")
            p(f"    - {q} (default: {d})")
    sv = intake.get("schema_v", "")
    if sv:
        p(f"  Schema: {sv}")
    if intake.get("truncated_input"):
        p("  Truncated input: yes")
    dropped = intake.get("dropped_clarifications", 0)
    if dropped:
        p(f"  Dropped clarifications: {dropped}")


def _cmd_plan_job_local(job_id_str: str) -> None:
    job_id = resolve_job_id(job_id_str)
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
    # F115: `plan_job_with_llm` appends the ComposedPrompt it is about to send,
    # so the recorder below can name the segments of the exact prompt it traces
    # instead of rebuilding a second composition that could drift from it.
    _plan_compositions: list = []

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
            composed_prompt=_plan_compositions[-1] if _plan_compositions else None,
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
        result: PlanJobResult = plan_job_with_llm(
            job, call_planner, on_prompt_composed=_plan_compositions.append,
        )
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
    job_id = resolve_job_id(job_id_str)
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
    job_id = resolve_job_id(job_id_str)
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
    job_id = resolve_job_id(job_id_str)
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
    job_id = resolve_job_id(job_id_str)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    from packages.orchestration.flight_plan import flight_plan_blocks_execution
    block_reason = flight_plan_blocks_execution(job)
    if block_reason == "pending":
        print(
            f"Error: plan awaiting approval. "
            f"Run: remedy decision resolve {job_id_str[:8]} fp:approval --reason approve",
            file=sys.stderr,
        )
        sys.exit(3)
    elif block_reason == "rejected":
        print(
            f"Error: flight plan rejected. "
            f"Run: remedy do replan {job_id_str[:8]}",
            file=sys.stderr,
        )
        sys.exit(3)

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
                        pi_created_at = datetime.now(timezone.utc).isoformat()
                        pi_artifact.metadata["patch_intent_explanations"] = [
                            {"file": r.target_path, "action": r.action, "risk": r.risk_level,
                             "reason": r.reason, "summary": r.summary, "created_at": pi_created_at}
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


def _cmd_job_run_cycles(
    job_id_str: str,
    *,
    cycles: int | None = None,
    unattended: bool = False,
    yes: bool = False,
    json_output: bool = False,
) -> None:
    """Run a job in bounded cycles (F046).

    The rollout rule is enforced here, not in the loop: config value and
    ``--cycles`` flag are both capped by ``CYCLE_SAFETY_CAP`` until the F075
    milestone gate raises it.  While the resolved count is one cycle, this
    command IS today's single pass — it delegates to the existing run-next
    entry point, so single-cycle behavior cannot drift from it.

    ``unattended`` (F051, R-0157) is the product surface for the loop's
    unattended mode: a task decision that carries a safe default is answered
    from that default and recorded in the escalation assumption log, instead of
    pausing the branch until a human answers.  A decision with no safe default
    waits either way.  Default OFF — attended behavior is untouched.
    """
    import json as _json
    from dataclasses import replace

    from packages.orchestration.config import get_config
    from packages.orchestration.long_run_executor import (
        default_task_step,
        limits_from_config,
        run_cycles,
    )

    try:
        limits, resolved = limits_from_config(get_config(), cycles_flag=cycles)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)

    if resolved.capped:
        origin = "--cycles" if resolved.source == "flag" else "cycles.max_cycles"
        print(
            f"Note: {origin} {resolved.requested} capped to {resolved.max_cycles} "
            f"by the F046 rollout default (raised by the F075 milestone gate).",
            file=sys.stderr,
        )

    from apps.cli.cost_preview_confirm import confirm_cost_preview
    from packages.orchestration.cost_preview import (
        ESTIMATE_UNAVAILABLE,
        CostBandEstimate,
        resolve_confirm_above_usd,
    )

    estimate = CostBandEstimate(None, None, ESTIMATE_UNAVAILABLE, {})
    if not confirm_cost_preview(
        estimate,
        confirm_above_usd=resolve_confirm_above_usd(),
        yes=(yes or unattended),
        command_name="job.run",
    ):
        print("Cancelled. Nothing was run.")
        return

    if resolved.max_cycles <= 1:
        # One cycle == today's single pass. Reuse it verbatim rather than
        # reimplementing the task/verify/apply pipeline behind a second door.
        if unattended:
            # Say it rather than swallow it: the single pass does not go through
            # the cycle loop, so it raises no task decisions to auto-answer.
            print(
                "Note: --unattended has no effect while the run resolves to the "
                "single pass (F046 rollout default); task decisions are raised by "
                "the cycle loop, which the F075 milestone gate enables.",
                file=sys.stderr,
            )
        _cmd_run_next_task_local(job_id_str)
        return

    job_id = resolve_job_id(job_id_str)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    from packages.orchestration.flight_plan import flight_plan_blocks_execution
    block_reason = flight_plan_blocks_execution(job)
    if block_reason == "pending":
        print(
            f"Error: plan awaiting approval. "
            f"Run: remedy decision resolve {job_id_str[:8]} fp:approval --reason approve",
            file=sys.stderr,
        )
        sys.exit(3)
    elif block_reason == "rejected":
        print(
            f"Error: flight plan rejected. "
            f"Run: remedy do replan {job_id_str[:8]}",
            file=sys.stderr,
        )
        sys.exit(3)

    from packages.orchestration.permissions import Capability
    from packages.orchestration.permissions import is_allowed as _perm_allowed
    from packages.orchestration.run_log import RunLogWriter
    from packages.providers.ollama_builder.provider import OllamaBuilder

    if not _perm_allowed(job, Capability.workspace_write):
        print(
            f"Error: permission denied — workspace_write is not granted for job {job.id}",
            file=sys.stderr,
        )
        sys.exit(1)

    log = RunLogWriter(job_id=job.id)
    try:
        builder = OllamaBuilder()
    except Exception as exc:
        print(f"Error: builder unavailable — {exc}", file=sys.stderr)
        sys.exit(1)

    limits = replace(limits, budgets=job.budgets)
    result = run_cycles(job, limits, builder.build,
                        task_step=default_task_step, log=log,
                        unattended=unattended)

    if json_output:
        print(_json.dumps(result.to_json(), indent=2, sort_keys=True))
    else:
        print(
            f"Job {job.id} | cycles={result.cycles_run}/{limits.max_cycles} "
            f"terminal={result.terminal_status} status={result.job_status}"
            f"{' reason=' + result.stop_reason if result.stop_reason else ''}"
            f"  log={log.path}"
        )
        # F052: a cycle that did not verify says WHY on the same screen — a
        # reader must not have to open the log to learn that the harness, not a
        # test, is what broke.
        from packages.orchestration.long_run_executor import render_cycle_summary_line
        for record in result.cycles:
            print(f"  {render_cycle_summary_line(record)}")
    if result.terminal_status not in ("all_green", "max_cycles_reached"):
        sys.exit(1)


def _resume_preview(job: Job, jid: str, checkpoint: Any) -> dict[str, Any]:
    """What ``remedy job resume`` WOULD decide — computed without changing anything.

    Every lookup here is read-only.  In particular the stop request is
    *observed* (``stop_requested``), never consumed: a preview that swallowed
    an operator's pending stop would be worse than the bug it replaced
    (R-0146).
    """
    from packages.orchestration.checkpoints import resolve_live_worktree_head
    from packages.orchestration.flight_plan import flight_plan_blocks_execution
    from packages.orchestration.safe_points import stop_requested

    signal = stop_requested(jid)
    stop = {
        "pending": signal is not None,
        "reason": getattr(signal, "reason", "") if signal is not None else "",
    }

    checkpoint_head = getattr(checkpoint, "worktree_head", "") if checkpoint else ""
    live_head = resolve_live_worktree_head(jid) if checkpoint_head else ""
    if not checkpoint_head:
        head_outcome = "not_recorded"
    elif not live_head:
        head_outcome = "unknown"
    elif live_head == checkpoint_head:
        head_outcome = "match"
    else:
        head_outcome = "drift"
    head = {"outcome": head_outcome, "checkpoint_head": checkpoint_head,
            "live_head": live_head}

    gate = flight_plan_blocks_execution(job) or "open"

    pending_tasks = [t for t in job.tasks if t.status != RunState.COMPLETED]
    if job.tasks and not pending_tasks:
        state = "all_green"
    elif checkpoint is None:
        state = "no_checkpoint"
    else:
        state = "from_checkpoint"

    return {
        "job_id": jid,
        "action": "preview",
        "resumed": False,
        "stop_request": stop,
        "worktree_head": head,
        "plan_approval_gate": gate,
        "state": state,
        "checkpoint_index": (
            getattr(checkpoint, "cycle_index", None) if checkpoint else None),
        "pending_tasks": len(pending_tasks),
        "would_run": (
            not stop["pending"] and head_outcome != "drift"
            and gate == "open" and state != "all_green"
        ),
    }


def _print_resume_preview(preview: dict[str, Any]) -> None:
    """Render the preview as text, in the order the checks are evaluated."""
    jid = preview["job_id"]
    print(f"Job {jid} | resume preview (--dry-run) — nothing was consumed, "
          f"nothing was run")

    stop = preview["stop_request"]
    if stop["pending"]:
        print(f"  stop request:  PENDING — would be consumed and the run would "
              f"not start{' (reason: ' + stop['reason'] + ')' if stop['reason'] else ''}")
    else:
        print("  stop request:  none pending")

    head = preview["worktree_head"]
    if head["outcome"] == "drift":
        print("  worktree head: DRIFTED — resume would refuse")
        print(f"                 checkpoint head: {head['checkpoint_head']}")
        print(f"                 worktree head:   {head['live_head']}")
    elif head["outcome"] == "match":
        print(f"  worktree head: matches the checkpoint ({head['live_head']})")
    elif head["outcome"] == "unknown":
        print(f"  worktree head: unknown — checkpoint recorded "
              f"{head['checkpoint_head']}, live head not resolvable")
    else:
        print("  worktree head: not recorded on the checkpoint — not compared")

    gate = preview["plan_approval_gate"]
    print(f"  plan gate:     {'open' if gate == 'open' else gate.upper()}"
          f"{'' if gate == 'open' else ' — resume would refuse'}")

    if preview["state"] == "all_green":
        print("  state:         already all green — resume would be a no-op")
    elif preview["state"] == "no_checkpoint":
        print(f"  state:         no checkpoint found — would continue from the "
              f"persisted job state ({preview['pending_tasks']} task(s) pending)")
    else:
        print(f"  state:         would resume from checkpoint "
              f"{preview['checkpoint_index']} "
              f"({preview['pending_tasks']} task(s) pending)")

    print(f"  would run:     {'yes' if preview['would_run'] else 'no'}")


def _cmd_job_resume(
    job_id_str: str,
    *,
    cycles: int | None = None,
    dry_run: bool = False,
    json_output: bool = False,
) -> None:
    """Continue a job from its newest valid CYCLE checkpoint (F047 T002).

    This is the ``remedy job resume <id>`` path taken when no ``--checkpoint``
    is given.  ``remedy job resume <id> --checkpoint <cid>`` still routes to
    ``_cmd_resume`` — the older event-replay resume — completely unchanged.
    The two are different objects with the same word in their name: an
    event-replay checkpoint is DERIVED from run-log events, an F047 checkpoint
    is WRITTEN at a cycle boundary under the job's evidence area.

    The order of the checks is the contract, not an implementation detail:

      1. a PENDING STOP REQUEST is consumed FIRST and the run does not start.
         An operator who asked a job to stop must not have that request
         silently outlived by a resume.
      2. the WORKTREE HEAD recorded in the checkpoint is compared with the
         head the worktree is standing on now.  A mismatch means a human
         edited the worktree; resume refuses and names BOTH heads.  It never
         rebases silently (P2).
      3. the PLAN-APPROVAL GATE is consulted through the same check
         ``remedy job run`` uses — resume is not a second door around it.

    Only then does it hand off to the multi-cycle executor.

    ``dry_run`` makes the whole thing a READ-ONLY PREVIEW: it reports what
    each of those checks would decide, consumes nothing — a pending stop
    request is still pending afterwards — never reaches the executor, and
    exits 0.  ``remedy job resume --dry-run`` previously dropped the flag on
    this path and executed for real (R-0146).

    Degradations, all honest:
      * no checkpoint at all -> says so and continues from the persisted job
        state (a legacy job that was never checkpointed still resumes);
      * checkpoints exist but none verifies -> refuses, naming the files;
      * an all-green job -> friendly no-op, exit 0.

    Exit codes: 0 ok / no-op / stop consumed · 1 job or checkpoint problem ·
    3 refused by a guard (head drift, plan-approval gate).
    """
    import json as _json

    from packages.orchestration.checkpoints import (
        AllCheckpointsCorruptError,
        load_latest_valid,
        resolve_live_worktree_head,
        worktree_drift_message,
    )
    from packages.orchestration.flight_plan import flight_plan_blocks_execution
    from packages.orchestration.safe_points import consume_stop, stop_requested

    job_id = resolve_job_id(job_id_str)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    jid = str(job.id)

    try:
        checkpoint = load_latest_valid(jid)
    except AllCheckpointsCorruptError as exc:
        print(
            f"Error: no usable checkpoint for job {jid} — "
            f"{len(exc.paths)} checkpoint(s) failed hash verification "
            f"({', '.join(exc.paths)}). They are kept on disk for inspection.",
            file=sys.stderr,
        )
        sys.exit(1)

    # A dry run stops HERE: it reports what the checks below would decide and
    # consumes none of them.  It must never reach the executor (R-0146).
    if dry_run:
        preview = _resume_preview(job, jid, checkpoint)
        if json_output:
            print(_json.dumps(preview, indent=2, sort_keys=True))
        else:
            _print_resume_preview(preview)
        return

    # 1. Pending stop request — consumed first, and it wins.
    if stop_requested(jid) is not None:
        signal = consume_stop(jid)
        reason = getattr(signal, "reason", "") if signal is not None else ""
        message = (
            f"Job {jid} | stop request consumed — not resuming"
            f"{' (reason: ' + reason + ')' if reason else ''}"
        )
        if json_output:
            print(_json.dumps(
                {"job_id": jid, "action": "stopped", "resumed": False,
                 "stop_reason": reason}, indent=2, sort_keys=True))
        else:
            print(message)
        return

    # 2. Worktree drift — refuse, and name both heads.
    if checkpoint is not None and checkpoint.worktree_head:
        live_head = resolve_live_worktree_head(jid)
        if live_head and live_head != checkpoint.worktree_head:
            print(
                "Error: " + worktree_drift_message(
                    checkpoint.worktree_head, live_head),
                file=sys.stderr,
            )
            sys.exit(3)

    # 3. Plan-approval gate — the same check `remedy job run` makes.
    block_reason = flight_plan_blocks_execution(job)
    if block_reason == "pending":
        print(
            f"Error: plan awaiting approval. "
            f"Run: remedy decision resolve {job_id_str[:8]} fp:approval "
            f"--reason approve",
            file=sys.stderr,
        )
        sys.exit(3)
    if block_reason == "rejected":
        print(
            f"Error: flight plan rejected. Run: remedy do replan {job_id_str[:8]}",
            file=sys.stderr,
        )
        sys.exit(3)

    # An all-green job has nothing to resume.
    pending = [t for t in job.tasks if t.status != RunState.COMPLETED]
    if job.tasks and not pending:
        if json_output:
            print(_json.dumps(
                {"job_id": jid, "action": "noop", "resumed": False,
                 "reason": "all_green"}, indent=2, sort_keys=True))
        else:
            print(f"Job {jid} | already all green — nothing to resume")
        return

    if checkpoint is None:
        print(f"Job {jid} | no checkpoint found — continuing from persisted "
              f"job state")
    else:
        print(f"Job {jid} | resuming from checkpoint {checkpoint.cycle_index} "
              f"(spent={checkpoint.budget_spent_tokens} tokens, "
              f"verify={checkpoint.verify_result or 'not_run'})")

    _cmd_job_run_cycles(job_id_str, cycles=cycles, json_output=json_output)


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

    job_id = resolve_job_id(job_id_str)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    from packages.orchestration.flight_plan import flight_plan_blocks_execution
    block_reason = flight_plan_blocks_execution(job)
    if block_reason == "pending":
        print(
            f"Error: plan awaiting approval. "
            f"Run: remedy decision resolve {job_id_str[:8]} fp:approval --reason approve",
            file=sys.stderr,
        )
        sys.exit(3)
    elif block_reason == "rejected":
        print(
            f"Error: flight plan rejected. "
            f"Run: remedy do replan {job_id_str[:8]}",
            file=sys.stderr,
        )
        sys.exit(3)

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


def _cmd_job_assumptions(job_id_str: str) -> None:
    """Print the job's assumption log (F034).

    Rendered from the job's own flight plan, so it tells the truth even
    for a job approved before the evidence file was written. When the
    evidence copy exists, its path is reported alongside.
    """
    job_id = resolve_job_id(job_id_str)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    from packages.orchestration.data_paths import job_evidence_export_dir
    from packages.orchestration.flight_plan import render_assumptions_md

    fp = getattr(job, "flight_plan", None)
    clarifications = fp.get("clarifications_resolved") if isinstance(fp, dict) else None
    print(render_assumptions_md(clarifications))

    log_path = job_evidence_export_dir(str(job.id)) / "assumptions.md"
    if log_path.exists():
        print(f"Evidence copy: {log_path}")


def _cmd_job_summary(job_id_str: str, *, json_output: bool = False) -> None:
    """Print an honest summary of job state — truth contract."""
    import json as _json

    job_id = resolve_job_id(job_id_str)
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

    job_id = resolve_job_id(job_id_str)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    from packages.orchestration.flight_plan import flight_plan_blocks_execution
    block_reason = flight_plan_blocks_execution(job)
    if block_reason == "pending":
        print(
            f"Error: plan awaiting approval. "
            f"Run: remedy decision resolve {job_id_str[:8]} fp:approval --reason approve",
            file=sys.stderr,
        )
        sys.exit(3)
    elif block_reason == "rejected":
        print(
            f"Error: flight plan rejected. "
            f"Run: remedy do replan {job_id_str[:8]}",
            file=sys.stderr,
        )
        sys.exit(3)

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


def _open_decisions_view(job: Job) -> dict:
    """The open-decision block status and report both render FIRST (F051 T003).

    Returns the rendered text lines, the JSON-safe decision dicts, and the one
    command that answers the most urgent open decision.  A decision queue that
    cannot be read must never break a read-only view, so any failure degrades to
    "nothing open" rather than an error.
    """
    try:
        from packages.orchestration.decision_queue import (
            export_decision_json,
            list_decisions,
            open_decisions,
            open_decisions_next_action,
            render_open_decisions_lines,
        )
        from packages.orchestration.timeline import load_run_events

        events = load_run_events(resolve_data_root(), job.id)
        decisions = list_decisions(job, events)
        return {
            'lines': render_open_decisions_lines(decisions),
            'open_decisions': [export_decision_json(d)
                               for d in open_decisions(decisions)],
            'next_action': open_decisions_next_action(decisions),
        }
    except Exception:  # noqa: BLE001 — a read-only view never fails on this
        return {'lines': [], 'open_decisions': [], 'next_action': ''}


def _cmd_job_status(job_id_str: str, *, json_output: bool = False) -> None:
    """Job status -- safe read-only view of current job state."""
    import json as _json

    job_id = resolve_job_id(job_id_str)
    try:
        job = load_job(job_id)
    except JobNotFoundError:
        if json_output:
            print(_json.dumps({'error': 'job_not_found', 'job_id': job_id_str}))
        else:
            print(f'Error: job not found: {job_id_str}', file=sys.stderr)
        sys.exit(1)

    truth = _extract_job_truth(job)
    open_decision_view = _open_decisions_view(job)

    state = job.state.value if hasattr(job.state, 'value') else str(job.state)
    task_count = len(job.tasks)
    done_count = sum(1 for t in job.tasks if (t.status.value if hasattr(t.status, 'value') else str(t.status)) == 'completed')
    pending_count = sum(1 for t in job.tasks if (t.status.value if hasattr(t.status, 'value') else str(t.status)) == 'pending')

    blockers: list[str] = []
    # F051: an open decision comes first — it is what the run needs from a human.
    if open_decision_view['open_decisions']:
        blockers.append('awaiting_decision')
    if truth['approval_required']:
        blockers.append('approval_required')
    elif pending_count > 0 and state == 'pending':
        blockers.append('job_not_started')
    if state == 'blocked':
        blockers.append('job_blocked')
    # Surface fulfillment blockers
    if truth.get('fulfillment_blockers'):
        blockers.extend(truth['fulfillment_blockers'])

    if open_decision_view['next_action']:
        next_action = open_decision_view['next_action']
    elif truth['approval_required']:
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
        # F051: open decisions first, with the exact command that answers each.
        'open_decisions': open_decision_view['open_decisions'],
        'open_decision_count': len(open_decision_view['open_decisions']),
    }

    if json_output:
        print(_json.dumps(status, indent=2))
    else:
        for line in open_decision_view['lines']:
            print(line)
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


def _cmd_job_run_report(job_id_str: str, *, interim: bool = False,
                        json_output: bool = False) -> None:
    """The F053 run report: one human-readable account of a run.

    `--final` renders the account of a terminal job; `--interim` renders the
    same structure for a run still in progress, headed by a loud snapshot
    label.  Both are strictly READ-ONLY — the interim path in particular never
    writes and never mutates job state, because rendering a progress snapshot
    must not perturb the run it is describing.

    `--final` REFUSES a job that has not reached a reported terminal (R-0161).
    Rendering one anyway would produce an unbannered report of a run that is
    still moving — exactly the mislabeled snapshot the interim banner exists to
    prevent, one typo away. The refusal names the state and points at
    `--interim`; it never renders anyway and never silently switches mode,
    because a command that quietly does something else than asked is how a
    snapshot gets mistaken for a final account.
    """
    import json as _json
    from dataclasses import asdict

    from packages.orchestration.long_run_executor import REPORTED_TERMINALS
    from packages.orchestration.run_report import (
        MODE_FINAL,
        MODE_INTERIM,
        build_report_sources,
        render_report,
    )

    job_id = resolve_job_id(job_id_str)
    try:
        job = load_job(job_id)
    except JobNotFoundError:
        # A clean error, never a traceback: an unknown id is a normal thing for
        # a human to type.
        if json_output:
            print(_json.dumps({'error': 'job_not_found', 'job_id': job_id_str}))
        else:
            print(f'Error: job not found: {job_id_str}', file=sys.stderr)
        sys.exit(1)

    terminal = str((job.metadata or {}).get('cycle_terminal_status', '') or '')
    if not interim and terminal not in REPORTED_TERMINALS:
        state = job.state.value if hasattr(job.state, 'value') else str(job.state)
        if json_output:
            print(_json.dumps({
                'error': 'run_not_terminal',
                'job_id': str(job.id),
                'state': state,
                'terminal_status': terminal,
                'hint': 'use --interim for a snapshot',
            }))
        else:
            print(f'Error: run still in progress (state: {state}) — '
                  'use --interim for a snapshot', file=sys.stderr)
        sys.exit(1)

    sources = build_report_sources(job)
    if json_output:
        print(_json.dumps(asdict(sources), indent=2, sort_keys=True, default=str))
        return
    print(render_report(job, MODE_INTERIM if interim else MODE_FINAL,
                        sources=sources))


def _cmd_job_report(job_id_str: str, *, json_output: bool = False) -> None:
    """Job report -- safe read-only report of job progress and evidence."""
    import json as _json

    job_id = resolve_job_id(job_id_str)
    try:
        job = load_job(job_id)
    except JobNotFoundError:
        if json_output:
            print(_json.dumps({'error': 'job_not_found', 'job_id': job_id_str}))
        else:
            print(f'Error: job not found: {job_id_str}', file=sys.stderr)
        sys.exit(1)

    truth = _extract_job_truth(job)
    open_decision_view = _open_decisions_view(job)

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
        # F051: a blocked run's next action is the command that answers its
        # most urgent open decision — that is what unblocks it.
        'next_safe_action': (open_decision_view['next_action']
                             or truth.get('fulfillment_next_action', '')),
        'open_decisions': open_decision_view['open_decisions'],
        'open_decision_count': len(open_decision_view['open_decisions']),
        'tasks': task_details,
    }
    if fulfillment_data:
        report['fulfillment'] = fulfillment_data

    if json_output:
        print(_json.dumps(report, indent=2))
    else:
        for line in open_decision_view['lines']:
            print(line)
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
        # The last line a human reads is what to do next.  For a blocked run
        # with open decisions that is the answer command, spelled out (F051).
        if report['next_safe_action']:
            print(f'  Next:      {report["next_safe_action"]}')


def _cmd_job_digest(job_id_str: str, *, json_output: bool = False) -> None:
    """`remedy job digest <id>` — the completion digest's CLI parity (F040
    T003), the HTTP route's little sibling. Reuses the SAME two calls
    `_cmd_job_summary` already makes above — `resolve_job_id`/`load_job`
    then `load_run_events` — and prints the SAME `build_job_digest`
    envelope the route builds, so the CLI and the route can never disagree
    about the same job.
    """
    import json as _json

    job_id = resolve_job_id(job_id_str)
    try:
        job = load_job(job_id)
    except JobNotFoundError:
        # A clean error, never a traceback: an unknown id is a normal thing
        # for a human to type (the same shape _cmd_job_report uses above).
        if json_output:
            print(_json.dumps({'error': 'job_not_found', 'job_id': job_id_str}))
        else:
            print(f'Error: job not found: {job_id_str}', file=sys.stderr)
        sys.exit(1)

    from packages.orchestration.timeline import load_run_events

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job.id)

    from packages.orchestration.job_digest import build_job_digest

    # The ONLY call that builds the envelope — no field is recomputed,
    # renamed or filtered before being printed, so this can never drift
    # from what `_build_digest_json` prints for the same job.
    digest = build_job_digest(job, events)

    if json_output:
        print(_json.dumps(digest, indent=2))
        return

    print(f'Job digest: {job.id}')
    print(f'  State:     {digest["state"]}')
    print(f'  Headline:  {digest["headline"]}')
    print(f'  Cost:      {digest["cost"]["value"]} ({digest["cost"]["basis"]})')
    print(f'  Decisions: {digest["decisions"]["open_count"]} open, '
          f'peak urgency {digest["decisions"]["peak_urgency"]}')
    # No `ownership` line this round: the key is always empty (DECISION
    # F040 D3) until F035 ships a producer, so there is no shape to render.
    print(f'  Next:      {digest["primary_action"]["label"]}')


def _cmd_job_dod(job_id_str: str, *, json_output: bool = False) -> None:
    """`remedy job dod <id>` — the Definition-of-Done matrix, live (F061 T004).

    Strictly READ-ONLY: it prints the last recorded gate run and never runs a
    check itself. A job with no DoD says so plainly rather than printing an
    empty table, because an empty matrix reads like "nothing failed".
    """
    import json as _json

    from packages.orchestration.dod_gate import (
        MATRIX_HEADER,
        load_dod,
        load_gate_result,
        matrix_rows,
    )

    job_id = resolve_job_id(job_id_str)
    try:
        load_job(job_id)
    except JobNotFoundError:
        if json_output:
            print(_json.dumps({'error': 'job_not_found', 'job_id': job_id_str}))
        else:
            print(f'Error: job not found: {job_id_str}', file=sys.stderr)
        sys.exit(1)

    jid = str(job_id)
    dod = load_dod(jid)
    recorded = load_gate_result(jid)

    if json_output:
        print(_json.dumps({
            'job_id': jid,
            'compiled': None if dod is None else dod.compiled,
            'origin': None if dod is None else dod.origin,
            'check_count': 0 if dod is None else len(dod.checks),
            'gate': recorded,
        }, indent=2, sort_keys=True))
        return

    if dod is None:
        print(f'Job {jid}: no Definition of Done has been compiled.')
        return

    label = 'compiled' if dod.compiled else 'deterministic (compiled=false)'
    print(f'Definition of Done for job {jid} — {label}, '
          f'{len(dod.checks)} check(s), {len(dod.blocking_checks)} blocking')
    print()

    if recorded is None:
        print('The gate has not run yet — no check has produced evidence.')
        for check in dod.checks:
            print(f'  {check.id:<24} {check.kind:<14} '
                  f'{"blocking" if check.blocking else "reported"}  not run')
        return

    rows = matrix_rows(recorded)
    widths = [max(len(MATRIX_HEADER[i]), *(len(r[i]) for r in rows))
              for i in range(len(MATRIX_HEADER))]
    print('  '.join(h.ljust(widths[i]) for i, h in enumerate(MATRIX_HEADER)))
    print('  '.join('-' * w for w in widths))
    for row in rows:
        print('  '.join(cell.ljust(widths[i]) for i, cell in enumerate(row)))
    print()

    if recorded.get('released'):
        print('Gate: RELEASED — every blocking check is green.')
    else:
        blocking = ', '.join(recorded.get('blocking_red') or []) or 'unnamed'
        print(f'Gate: HOLDING — blocking check(s) red: {blocking}')
    reported = recorded.get('reported_red') or []
    if reported:
        print(f'Non-blocking reds (reported, not gating): {", ".join(reported)}')


def _cmd_job_fulfill(
    job_id_str: str,
    *,
    fixture_demo: bool = False,
    json_output: bool = False,
) -> None:
    """Run job fulfillment spine — fixture-demo mode only in v0."""
    import json as _json

    job_id = resolve_job_id(job_id_str)

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

    from packages.orchestration.scope_fences import (
        FenceConfigError,
        resolve_fence_spec_effective,
    )

    try:
        job = load_job(resolve_job_id(job_id_str))
    except JobNotFoundError:
        print(f"Job not found: {job_id_str}", file=sys.stderr)
        sys.exit(1)

    repo_str = job.metadata.get("target_repo", "") or ""
    if not repo_str:
        print(f"Job {job_id_str[:8]} has no target_repo attached", file=sys.stderr)
        sys.exit(2)
    repo_root = Path(repo_str)
    if not repo_root.is_dir():
        print(f"Target repo does not exist: {repo_str}", file=sys.stderr)
        sys.exit(2)

    job_fences_dict = None
    if job.fences is not None:
        job_fences_dict = {"allow": job.fences.allow, "deny": job.fences.deny}

    try:
        eff = resolve_fence_spec_effective(repo_root, job_fences=job_fences_dict)
    except FenceConfigError as exc:
        print(f"Fence config error: {exc}", file=sys.stderr)
        sys.exit(3)
    except RuntimeError as exc:
        print(f"Builtin resolution failed: {exc}", file=sys.stderr)
        sys.exit(4)
    spec = eff.spec

    warnings: list[str] = list(eff.warnings)
    if not spec.allow_globs and not spec.deny_globs:
        warnings.append("no configured allow/deny globs — defaults apply (allow all, builtin denies only)")

    def _rule_dict(r):
        return {"pattern": r.pattern, "kind": r.kind, "source": r.source, "reason": r.reason}

    result = {
        "job_id": job_id_str,
        "source": eff.source,
        "case_sensitivity": eff.case_sensitivity,
        "allow_rules": [_rule_dict(r) for r in eff.allow_rules],
        "deny_rules": [_rule_dict(r) for r in eff.deny_rules],
        "builtin_rules": [_rule_dict(r) for r in eff.builtin_rules],
        "allow_globs": list(spec.allow_globs),
        "deny_globs": list(spec.deny_globs),
        "warnings": warnings,
    }

    if json_output:
        print(_json.dumps(result, indent=2))
    else:
        print(f"Scope fences for job {job_id_str[:8]}:")
        print(f"  Source: {eff.source}")
        print(f"  Case:   {eff.case_sensitivity}")
        if eff.allow_rules:
            print("  Allow rules:")
            for r in eff.allow_rules:
                print(f"    {r.pattern:30s} [{r.source}]")
        else:
            print("  Allow:  (all — no restrictions)")
        if eff.deny_rules:
            print("  Deny rules:")
            for r in eff.deny_rules:
                print(f"    {r.pattern:30s} [{r.source}]")
        else:
            print("  Deny:   (none beyond builtins)")
        print("  Builtin rules:")
        for r in eff.builtin_rules:
            print(f"    {r.pattern:30s} [{r.source}] {r.reason}")
        if warnings:
            print("  Warnings:")
            for w in warnings:
                print(f"    {w}")


# Renders a money figure for `remedy job budget`, or says out loud that there is
# none. An unmeasured figure is NEVER rendered as a measured zero (P6) — the
# text mirror of the null that `BudgetPrediction.to_json` keeps in JSON.
def _format_budget_usd(value: float | None) -> str:
    return "not-measured" if value is None else f"${value:.4f}"


# Renders what is left of a money limit. Unknown spend has an unknown remainder;
# a spend that is only a FLOOR (some calls unpriced) leaves a remainder that is
# only a CEILING, and says `<= ` for the same reason `cost_description()` says
# `>= `. Never "$0.0000" for an unmeasured spend — that is the P6 failure this
# whole feature exists to avoid.
def _format_remaining_usd(limit_usd: float, counters) -> str:
    spent = counters.measured_cost_usd
    if spent is None:
        return "not-measured"
    prefix = "<= " if counters.has_unpriced else ""
    return f"{prefix}${max(0.0, limit_usd - spent):.4f}"


def _cmd_job_budget(
    job_id: str,
    *,
    json_output: bool = False,
) -> None:
    """Show budget limits and current counters for a job.

    Supports both Core Job UUIDs and JobPlan hex IDs.
    """
    import json as _json

    from packages.orchestration.budget_guard import evaluate_budget
    from packages.orchestration.pingpong_job import load_job_plan

    _job_display_id = job_id
    _budgets = None
    _budgets_dict = None
    counters = None
    evaluation = None
    _counter_status = "no_runs"
    _counter_diagnostic = ""
    _found_as = None
    # The JobPlan the F104 money figures are read from, whichever id form was
    # given. A Core Job UUID reaches the same plan through _plan_for_core below.
    _plan = None

    job_plan = load_job_plan(job_id)
    if job_plan is not None:
        _plan = job_plan
        _found_as = "job_plan"
        _job_display_id = job_plan.job_id
        if job_plan.budgets is not None:
            from packages.core.models import JobBudgets
            try:
                _budgets = JobBudgets.model_validate(job_plan.budgets)
                _budgets_dict = job_plan.budgets
            except Exception:
                _budgets_dict = job_plan.budgets

        if getattr(job_plan, "budget_actuals", None) is not None:
            from packages.orchestration.budget_guard import (
                BudgetCounterError,
                counters_from_persisted,
                decode_persisted_budget_actuals,
            )
            _fra = getattr(job_plan, "first_running_at", "") or None
            try:
                _validated = decode_persisted_budget_actuals(
                    job_plan.budget_actuals, first_running_at=_fra)
                counters = counters_from_persisted(_validated)
                if _budgets is not None:
                    evaluation = evaluate_budget(_budgets, counters)
                _counter_status = "evaluated"
            except (BudgetCounterError, Exception) as _budget_exc:
                _counter_status = "corrupt"
                _counter_diagnostic = str(_budget_exc)
                counters = None
                evaluation = None
        else:
            has_runs = any(
                t.run_id and t.status in ("applied", "passed", "stopped")
                for t in getattr(job_plan, "tasks", [])
            )
            if has_runs:
                _counter_status = "actuals_not_persisted"

    if _found_as is None:
        try:
            job = load_job(job_id)
        except JobNotFoundError:
            print(f"Error: job {job_id!r} not found.", file=sys.stderr)
            sys.exit(1)
        _found_as = "core_job"
        _job_display_id = str(job.id)
        _budgets = job.budgets

        if _budgets is None:
            if json_output:
                print(_json.dumps({"job_id": _job_display_id, "budgets": None}, indent=2))
            else:
                print(f"Job {_job_display_id[:8]}: no budgets configured.")
            return

        _plan_for_core = load_job_plan(_job_display_id)
        _plan = _plan_for_core
        if _plan_for_core is not None and getattr(_plan_for_core, "budget_actuals", None) is not None:
            from packages.orchestration.budget_guard import (
                BudgetCounterError,
                counters_from_persisted,
                decode_persisted_budget_actuals,
            )
            _fra = getattr(_plan_for_core, "first_running_at", "") or None
            try:
                _validated = decode_persisted_budget_actuals(
                    _plan_for_core.budget_actuals, first_running_at=_fra)
                counters = counters_from_persisted(_validated)
                evaluation = evaluate_budget(_budgets, counters)
                _counter_status = "evaluated"
            except (BudgetCounterError, Exception) as _budget_exc:
                _counter_status = "corrupt"
                _counter_diagnostic = str(_budget_exc)
                counters = None
                evaluation = None

    if _budgets is None and _budgets_dict is None:
        if json_output:
            print(_json.dumps({"job_id": _job_display_id, "budgets": None}, indent=2))
        else:
            print(f"Job {_job_display_id[:8]}: no budgets configured.")
        return

    _has_cost_limit = _budgets is not None and _budgets.max_cost_usd is not None

    # F104 money actuals. The persisted budget-actuals record carries NO cost
    # field — the F103 ledger is the only place a real provider cost lives — so
    # a money-limited job reads it here, exactly as run_job's safe point does.
    # READ-ONLY: `query_cost` never creates a ledger and never writes one, which
    # is what keeps `remedy job budget` action_class="read_only". Any failure
    # leaves the cost UNMEASURED (None, never 0.0 — P6) and every other limit
    # still reports; an inspection command must not fail because a mirror is
    # unreadable.
    # R-0227: a read that FAILED and a job nobody priced both leave the cost
    # UNMEASURED, but only one of them is a broken mirror — and that is the
    # diagnosis an operator who just hit a cost limit most needs. This holds the
    # failure so both surfaces can say it out loud; it stays None when the read
    # succeeded or was never attempted, which is what keeps the two cases apart.
    _cost_read_error = None
    if _has_cost_limit and counters is not None and counters.measured_cost_usd is None:
        try:
            from dataclasses import replace as _replace

            from packages.orchestration.budget_guard import collect_ledger_cost_for_job
            from packages.orchestration.job_evidence import (
                _resolve_job_ledger_project_id,
            )
            _ledger_project = _resolve_job_ledger_project_id(_plan)
            if _ledger_project is not None:
                _cost, _priced, _unpriced = collect_ledger_cost_for_job(
                    job_id=_job_display_id, project_id=_ledger_project)
                counters = _replace(
                    counters,
                    measured_cost_usd=_cost,
                    priced_call_count=_priced,
                    unpriced_call_count=_unpriced,
                )
                evaluation = evaluate_budget(_budgets, counters)
        except Exception as _cost_exc:
            # Recorded BEFORE the log call, so a logging subsystem that is itself
            # broken cannot cost the operator the diagnosis. The displayed cost is
            # unchanged — still not-measured, never 0.0 (P6).
            _cost_read_error = f"{type(_cost_exc).__name__}: {_cost_exc}"[:160]
            try:
                import logging as _logging
                _logging.getLogger(__name__).error(
                    "budget ledger cost read FAILED for job %r; the cost stays "
                    "unmeasured for this read and the other limits still report "
                    "(the evidence files remain the source of truth)",
                    _job_display_id, exc_info=True,
                )
            except Exception:
                # An inspection command never dies because a log handler died.
                pass

    # F104: what the NEXT task is expected to cost, with the label that says
    # where the number came from. Computed LIVE and PURELY — both engine
    # functions are side-effect free and the selection helper only reads the
    # plan — so nothing here writes, persists or mutates the job. The whole
    # computation is wrapped for the same reason run_job's predictive block is:
    # a broken estimate must never take down a healthy read.
    _prediction = None
    _prediction_note = ""
    if _has_cost_limit:
        try:
            from packages.orchestration.budget_guard import (
                BudgetCounters,
                derive_next_task_token_band,
                predict_next_task_cost,
            )
            from packages.orchestration.budget_resolution import (
                resolve_predictive_budget_config,
            )
            from packages.orchestration.pingpong_job import (
                select_next_predictable_task,
            )
            if _plan is None:
                _prediction_note = "unavailable (no job plan on disk)"
            else:
                _next_task, _prev_summaries = select_next_predictable_task(_plan)
                if _next_task is None:
                    _prediction_note = "none (no pending task)"
                else:
                    _prediction = predict_next_task_cost(
                        _budgets,
                        counters if counters is not None else BudgetCounters(),
                        band=derive_next_task_token_band(_next_task, _prev_summaries),
                        config=resolve_predictive_budget_config(
                            project_root=(getattr(_plan, "repo_path", "") or None)),
                    )
        except Exception as _pred_exc:
            _prediction = None
            _prediction_note = (
                f"unavailable ({type(_pred_exc).__name__}: {_pred_exc})"[:160])

    # The arithmetic a predictive stop already recorded, if this job took one.
    _recorded_prediction = (
        getattr(_plan, "budget_prediction", None) if _plan is not None else None)

    if json_output:
        out: dict = {
            "job_id": _job_display_id,
            "found_as": _found_as,
            "limits": (_budgets.model_dump(mode="json") if _budgets else _budgets_dict),
            "counters": counters.to_json() if counters else None,
            "evaluation": evaluation.to_json() if evaluation else None,
            "status": _counter_status,
            "diagnostic": _counter_diagnostic or None,
            # R-0227: the LEDGER READ's own failure. Deliberately its own key —
            # `diagnostic` belongs to the counters decode, and one field standing
            # for two unrelated failures is the defect this fix exists to end.
            "cost_read_error": _cost_read_error,
            # Null, never an invented number, when no prediction could be made.
            "prediction": _prediction.to_json() if _prediction is not None else None,
            "recorded_prediction": _recorded_prediction,
        }
        print(_json.dumps(out, indent=2))
    else:
        print(f"Budget for job {_job_display_id[:8]} ({_found_as}):")
        if _budgets is not None:
            if _budgets.max_total_tokens is not None:
                print(f"  max_total_tokens:      {_budgets.max_total_tokens}")
            if _budgets.max_provider_calls is not None:
                print(f"  max_provider_calls:    {_budgets.max_provider_calls}")
            if _budgets.max_cost_usd is not None:
                print(f"  max_cost_usd:          ${_budgets.max_cost_usd:.4f}")
            if _budgets.max_wall_clock_minutes is not None:
                print(f"  max_wall_clock_minutes: {_budgets.max_wall_clock_minutes}")
            if _budgets.deadline is not None:
                print(f"  deadline:              {_budgets.deadline.isoformat()}")
        elif _budgets_dict is not None:
            for k, v in _budgets_dict.items():
                if v is not None:
                    print(f"  {k}: {v}")
        if _has_cost_limit and counters is not None:
            print(f"  spent:                 {counters.cost_description()}")
            print(f"  remaining:             "
                  f"{_format_remaining_usd(_budgets.max_cost_usd, counters)}")
            # Only when a read actually broke. A genuinely unpriced job prints
            # no such line, which is what keeps the two cases distinguishable.
            if _cost_read_error:
                print(f"  cost_read:             unavailable ({_cost_read_error})")
        if _has_cost_limit:
            if _prediction is not None:
                print(f"  next_task_expected:    "
                      f"{_format_budget_usd(_prediction.expected_cost_usd)}")
                print(f"  estimate_basis:        {_prediction.estimate_basis}")
                print(f"  arithmetic:            {_prediction.arithmetic}")
            elif _prediction_note:
                print(f"  next_task_expected:    {_prediction_note}")
        if isinstance(_recorded_prediction, dict):
            print("  recorded stop prediction:")
            print(f"    estimate_basis:      "
                  f"{_recorded_prediction.get('estimate_basis', '')}")
            print(f"    arithmetic:          "
                  f"{_recorded_prediction.get('arithmetic', '')}")
        if evaluation is not None:
            print(f"  exhausted:             {evaluation.exhausted}")
            if evaluation.first_exhausted_limit:
                print(f"  first_exhausted:       {evaluation.first_exhausted_limit}")
            for src in evaluation.source_descriptions:
                print(f"  {src}")
            for warn in evaluation.warnings:
                print(f"  WARNING: {warn}")
        else:
            print(f"  counters:              {_counter_status}")
            if _counter_diagnostic:
                print(f"  diagnostic:            {_counter_diagnostic}")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "job.create": lambda args: _cmd_create_job(
        args.prompt,
        project_id=getattr(args, "project", None),
        task_type=getattr(args, "task_type", None),
        task_description=getattr(args, "task_description", None),
        max_total_tokens=getattr(args, "max_total_tokens", None),
        max_provider_calls=getattr(args, "max_provider_calls", None),
        max_wall_clock_minutes=getattr(args, "max_wall_clock_minutes", None),
        max_cost_usd=getattr(args, "max_cost_usd", None),
        deadline=getattr(args, "deadline", None),
    ),
    "job.list": lambda args: _cmd_list_jobs(
        project=getattr(args, "project", None),
        all_projects=getattr(args, "all_projects", False),
        json_output=args.json,
        sort=getattr(args, "sort", None),
        desc=getattr(args, "desc", False),
        since=getattr(args, "since", None),
        until=getattr(args, "until", None),
        limit=getattr(args, "limit", None),
    ),
    "job.show": lambda args: _cmd_show_job(args.job_id),
    "job.attach-repo": lambda args: _cmd_attach_repo(args.job_id, args.repo_path),
    "job.permit": lambda args: _cmd_set_permission(args.job_id, args.action, args.permission),
    "job.permissions": lambda args: _cmd_show_permissions(args.job_id),
    "job.budget": lambda args: _cmd_job_budget(
        args.job_id,
        json_output=getattr(args, "json", False),
    ),
    "job.run-next": lambda args: _cmd_run_next_task_local(args.job_id),
    "job.run": lambda args: _cmd_job_run_cycles(
        args.job_id,
        cycles=(int(args.cycles) if getattr(args, "cycles", None) else None),
        unattended=getattr(args, "unattended", False),
        yes=getattr(args, "yes", False),
        json_output=getattr(args, "json", False),
    ),
    "job.plan": lambda args: _cmd_plan_job_local(args.job_id),
    "job.run-loop": lambda args: _cmd_run_loop(
        args.job_id,
        max_cycles=int(getattr(args, "max_cycles", "3")),
        autonomy_level=int(getattr(args, "autonomy_level", "1")),
        auto_approve_low_risk=getattr(args, "auto_approve_low_risk", False),
        no_tests=getattr(args, "no_tests", False),
        json_output=getattr(args, "json", False),
    ),
    "job.assumptions": lambda args: _cmd_job_assumptions(args.job_id),
    "job.summary": lambda args: _cmd_job_summary(
        args.job_id,
        json_output=getattr(args, "json", False),
    ),
    "job.checkpoints": lambda args: _cmd_checkpoints(
        args.job_id,
        json_output=getattr(args, "json", False),
    ),
    # `remedy job resume` has two modes and ONE name (see _cmd_job_resume).
    # --checkpoint <id> keeps the event-replay resume exactly as it was;
    # without it, the F047 cycle-checkpoint resume runs.
    "job.resume": lambda args: (
        _cmd_resume(
            args.job_id,
            checkpoint_id=getattr(args, "checkpoint", ""),
            dry_run=getattr(args, "dry_run", False),
            json_output=getattr(args, "json", False),
        )
        if getattr(args, "checkpoint", "")
        else _cmd_job_resume(
            args.job_id,
            cycles=(int(args.cycles) if getattr(args, "cycles", None) else None),
            dry_run=getattr(args, "dry_run", False),
            json_output=getattr(args, "json", False),
        )
    ),
    "job.status": lambda args: _cmd_job_status(
        args.job_id,
        json_output=getattr(args, "json", False),
    ),
    # `remedy job report` has three modes and ONE name (the F047 `job resume`
    # pattern, see .agent/decisions.md): --final/--interim render the F053 run
    # report; without either flag the existing progress view runs UNCHANGED, so
    # no existing invocation changes behavior.
    "job.report": lambda args: (
        _cmd_job_run_report(
            args.job_id,
            interim=getattr(args, "interim", False),
            json_output=getattr(args, "json", False),
        )
        if (getattr(args, "final", False) or getattr(args, "interim", False))
        else _cmd_job_report(
            args.job_id,
            json_output=getattr(args, "json", False),
        )
    ),
    "job.digest": lambda args: _cmd_job_digest(args.job_id,
        json_output=getattr(args, "json", False)),
    "job.fences": lambda args: _cmd_job_fences(
        args.job_id,
        json_output=getattr(args, "json", False),
    ),
    "job.dod": lambda args: _cmd_job_dod(
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
