"""
Remedy CLI entrypoint.

Usage:
    remedy create-job "<prompt>"
    remedy list-jobs
    remedy show-job <job_id>
    remedy plan-job <job_id>
    remedy plan-job-local <job_id>
    remedy attach-repo <job_id> <repo_path>
    remedy set-permission <job_id> <allow|deny> <capability>
    remedy show-permissions <job_id>
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


def _cmd_create_job(prompt: str, *, project_id: str | None = None) -> None:
    from packages.orchestration.run_log import RunLogWriter

    metadata: dict = {}
    if project_id:
        metadata["project_id"] = project_id
    job = Job(
        name=prompt[:50],
        user_prompt=prompt,
        state=RunState.PENDING,
        metadata=metadata,
    )
    save_job(job)
    print(job.id)
    log = RunLogWriter(job_id=job.id)
    log.log("job_created", outcome="created")
    if project_id:
        from packages.orchestration.project_registry import (
            ProjectNotFoundError,
            attach_job,
            load_project,
            save_project,
        )
        from uuid import UUID
        try:
            project = load_project(UUID(project_id))
            attach_job(project, str(job.id))
            save_project(project)
        except (ProjectNotFoundError, ValueError):
            pass  # --project refers to a non-existent project; job still created


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
    from packages.orchestration.run_log import RunLogWriter
    from packages.providers.ollama_planner.provider import OllamaPlanner

    log = RunLogWriter(job_id=job.id)

    planner = OllamaPlanner()
    log.log(
        "planning_started",
        provider="ollama",
        role="planner",
        model=planner.model,
    )

    start = time.monotonic()
    try:
        result: PlanJobResult = plan_job_with_llm(job, planner.plan)
    except ImportError as exc:
        log.log("planning_failed", provider="ollama", role="planner", model=planner.model,
                outcome="error", message="planning failed",
                error_category=type(exc).__name__)
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        log.log("planning_failed", provider="ollama", role="planner", model=planner.model,
                outcome="error", message="planning failed",
                error_category=type(exc).__name__)
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
        log.log(
            "planning_completed",
            provider="ollama",
            role="planner",
            model=planner.model,
            outcome="noop",
        )
        print(f"Job {result.job.id} already planned — no changes made.  log={log.path}")
    else:
        from packages.orchestration.artifact_index import planning_artifact

        pa = planning_artifact(result.job.artifacts)
        artifact_id_str = str(pa.id) if pa is not None else None
        log.log(
            "planning_completed",
            provider="ollama",
            role="planner",
            model=planner.model,
            artifact_id=artifact_id_str,
            outcome="changed",
            elapsed_ms=round(elapsed_ms),
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
        print(
            f"Error: unknown capability {capability_str!r}. Valid: {valid}",
            file=sys.stderr,
        )
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


def _cmd_cockpit(job_id_str: str) -> None:
    import os

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

    from packages.orchestration.cockpit import summarize_cockpit
    from packages.orchestration.project_constitution import load_project_constitution
    from packages.orchestration.timeline import load_run_events

    env = os.environ.get("REMEDY_DATA_DIR")
    if env:
        data_dir = Path(env)
    else:
        data_dir = Path(__file__).resolve().parent.parent.parent / ".data"

    target_repo_str = job.metadata.get("target_repo")
    constitution = load_project_constitution(Path(target_repo_str) if target_repo_str else None)

    events = load_run_events(data_dir, job_id)
    print(summarize_cockpit(job, events, data_dir=data_dir, constitution=constitution))


def _cmd_list_patch_intents(job_id_str: str) -> None:
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

    from packages.orchestration.approval_queue import format_intent_list, list_patch_intents

    intents = list_patch_intents(job)
    print(format_intent_list(intents))


def _cmd_show_patch_intent(job_id_str: str, intent_id: str) -> None:
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

    from packages.orchestration.approval_queue import (
        _find_artifact_for_intent,
        format_intent_detail,
        get_patch_intent,
    )

    item = get_patch_intent(job, intent_id)
    if item is None:
        print(f"Error: patch intent {intent_id!r} not found in job {job_id}.", file=sys.stderr)
        print("Use 'remedy list-patch-intents <job_id>' to see available intent IDs.", file=sys.stderr)
        sys.exit(1)

    # Pull truncated diff preview from artifact metadata (safe — never full content).
    diff_preview: str | None = None
    found = _find_artifact_for_intent(job, intent_id)
    if found is not None:
        artifact, _ = found
        diff_preview = artifact.metadata.get("patch_intent_diff_preview")

    print(format_intent_detail(item, diff_preview))


def _cmd_approve_patch_intent(job_id_str: str, intent_id: str, reason: str | None) -> None:
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

    from packages.orchestration.approval_queue import set_approval_state
    from packages.orchestration.run_log import RunLogWriter

    try:
        entry = set_approval_state(job, intent_id, "approved", reason=reason)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    save_job(job)

    log = RunLogWriter(job_id=job.id)
    log.log(
        "patch_intent_approved",
        outcome="approved",
        intent_id=entry["intent_id"],
        target_path=entry["target_path"],
        risk=entry["risk"],
        reason_present=reason is not None,
    )

    print(f"Approved: {entry['intent_id']} ({entry['target_path']})")
    print(f"  reason: {'recorded' if reason else 'none'}")
    print("Note: approval is metadata only — no files have been modified.")


def _cmd_reject_patch_intent(job_id_str: str, intent_id: str, reason: str | None) -> None:
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

    from packages.orchestration.approval_queue import set_approval_state
    from packages.orchestration.run_log import RunLogWriter

    try:
        entry = set_approval_state(job, intent_id, "rejected", reason=reason)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    save_job(job)

    log = RunLogWriter(job_id=job.id)
    log.log(
        "patch_intent_rejected",
        outcome="rejected",
        intent_id=entry["intent_id"],
        target_path=entry["target_path"],
        risk=entry["risk"],
        reason_present=reason is not None,
    )

    print(f"Rejected: {entry['intent_id']} ({entry['target_path']})")
    print(f"  reason: {'recorded' if reason else 'none'}")
    print("Note: rejection is metadata only — no files have been modified.")


def _cmd_constitution(job_id_str: str) -> None:
    import os

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

    from packages.orchestration.project_constitution import (
        load_project_constitution,
        render_constitution,
    )
    from packages.orchestration.run_log import RunLogWriter

    target_repo_str = job.metadata.get("target_repo")
    repo_root = Path(target_repo_str) if target_repo_str else None

    constitution = load_project_constitution(repo_root)
    print(render_constitution(constitution, repo_root))

    log = RunLogWriter(job_id=job.id)
    log.log(
        "project_constitution_loaded",
        outcome="loaded",
        source_count=len(constitution.source_files),
        warning_count=len(constitution.warnings),
        has_test_commands=bool(constitution.test_commands),
    )


def _cmd_agent_loop(job_id_str: str) -> None:
    import os

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

    from packages.orchestration.agent_loop import (
        derive_agent_loop_state,
        summarize_agent_loop_state,
    )
    from packages.orchestration.run_log import RunLogWriter
    from packages.orchestration.timeline import load_run_events

    env = os.environ.get("REMEDY_DATA_DIR")
    data_dir = Path(env) if env else Path(__file__).resolve().parent.parent.parent / ".data"

    events = load_run_events(data_dir, job_id)
    state = derive_agent_loop_state(job, events)

    print(summarize_agent_loop_state(job, state))

    log = RunLogWriter(job_id=job.id)
    log.log(
        "agent_loop_inspected",
        outcome="inspected",
        stage=state.current_stage.value,
        decision=state.decision.value,
        cycle=state.cycle,
        max_cycles=state.max_cycles,
        pending_finding_count=len(state.pending_findings),
    )


def _cmd_brain(job_id_str: str, *, json_output: bool = False) -> None:
    import json as _json
    import os

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

    from packages.orchestration.project_brain import (
        build_project_brain,
        export_project_brain_json,
        summarize_project_brain,
    )
    from packages.orchestration.project_constitution import load_project_constitution
    from packages.orchestration.run_log import RunLogWriter
    from packages.orchestration.timeline import load_run_events

    env = os.environ.get("REMEDY_DATA_DIR")
    data_dir = Path(env) if env else Path(__file__).resolve().parent.parent.parent / ".data"

    events = load_run_events(data_dir, job_id)

    target_repo_str = job.metadata.get("target_repo")
    constitution = (
        load_project_constitution(Path(target_repo_str))
        if target_repo_str
        else None
    )

    graph = build_project_brain(job, events, constitution=constitution)

    if json_output:
        print(_json.dumps(export_project_brain_json(graph), sort_keys=True))
    else:
        print(summarize_project_brain(graph))

    task_count = sum(1 for n in graph.nodes if n.type == "task")
    patch_intent_count = sum(1 for n in graph.nodes if n.type == "patch_intent")

    log = RunLogWriter(job_id=job.id)
    log.log(
        "project_brain_inspected",
        outcome="inspected",
        node_count=len(graph.nodes),
        edge_count=len(graph.edges),
        task_count=task_count,
        patch_intent_count=patch_intent_count,
    )


def _cmd_brain_node(job_id_str: str, node_id: str, *, json_output: bool = False) -> None:
    import json as _json
    import os

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

    from packages.orchestration.brain_detail import (
        build_brain_node_detail,
        export_brain_node_detail_json,
        summarize_brain_node_detail,
    )
    from packages.orchestration.project_brain import build_project_brain
    from packages.orchestration.project_constitution import load_project_constitution
    from packages.orchestration.run_log import RunLogWriter
    from packages.orchestration.timeline import load_run_events

    env = os.environ.get("REMEDY_DATA_DIR")
    data_dir = Path(env) if env else Path(__file__).resolve().parent.parent.parent / ".data"

    events = load_run_events(data_dir, job_id)

    target_repo_str = job.metadata.get("target_repo")
    constitution = (
        load_project_constitution(Path(target_repo_str))
        if target_repo_str
        else None
    )

    graph = build_project_brain(job, events, constitution=constitution)

    try:
        detail = build_brain_node_detail(job, graph, node_id, events)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if json_output:
        print(_json.dumps(export_brain_node_detail_json(detail), sort_keys=True))
    else:
        print(summarize_brain_node_detail(detail))

    log = RunLogWriter(job_id=job.id)
    log.log(
        "brain_node_inspected",
        outcome="inspected",
        node_id=detail.node_id,
        node_type=detail.node_type,
        connected_count=len(detail.connected_to),
        evidence_count=len(detail.evidence),
    )


def _cmd_context(job_id_str: str, *, json_output: bool = False) -> None:
    import json as _json
    import os

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

    from packages.orchestration.context_coverage import (
        derive_context_coverage,
        export_context_coverage_json,
        summarize_context_coverage,
    )
    from packages.orchestration.project_constitution import load_project_constitution
    from packages.orchestration.run_log import RunLogWriter
    from packages.orchestration.timeline import load_run_events

    env = os.environ.get("REMEDY_DATA_DIR")
    data_dir = Path(env) if env else Path(__file__).resolve().parent.parent.parent / ".data"

    events = load_run_events(data_dir, job_id)

    target_repo_str = job.metadata.get("target_repo")
    constitution = None
    if target_repo_str:
        try:
            repo_path = Path(target_repo_str)
            if not repo_path.exists() or not repo_path.is_dir():
                print(
                    "Warning: project constitution unavailable for context coverage.",
                    file=sys.stderr,
                )
            else:
                constitution = load_project_constitution(repo_path)
        except Exception:
            print(
                "Warning: project constitution unavailable for context coverage.",
                file=sys.stderr,
            )

    snapshot = derive_context_coverage(job, events, constitution=constitution)

    if json_output:
        print(_json.dumps(export_context_coverage_json(snapshot), sort_keys=True))
    else:
        print(summarize_context_coverage(snapshot))

    log = RunLogWriter(job_id=job.id)
    log.log(
        "context_coverage_inspected",
        outcome="inspected",
        score=snapshot.score,
        present_signal_count=sum(1 for s in snapshot.signals if s.present),
        missing_signal_count=len(snapshot.missing_keys),
        scope=snapshot.scope,
    )


def _cmd_brain_view(job_id_str: str) -> None:
    import os

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

    from packages.orchestration.brain_viewer import (
        build_brain_viewer_data,
        write_brain_viewer_files,
    )
    from packages.orchestration.project_brain import build_project_brain
    from packages.orchestration.project_constitution import load_project_constitution
    from packages.orchestration.run_log import RunLogWriter
    from packages.orchestration.timeline import load_run_events

    env = os.environ.get("REMEDY_DATA_DIR")
    data_dir = Path(env) if env else Path(__file__).resolve().parent.parent.parent / ".data"

    events = load_run_events(data_dir, job_id)

    target_repo_str = job.metadata.get("target_repo")
    constitution = None
    if target_repo_str:
        try:
            repo_path = Path(target_repo_str)
            if not repo_path.exists() or not repo_path.is_dir():
                print(
                    "Warning: project constitution unavailable for viewer.",
                    file=sys.stderr,
                )
            else:
                constitution = load_project_constitution(repo_path)
        except Exception:
            print(
                "Warning: project constitution unavailable for viewer.",
                file=sys.stderr,
            )

    graph = build_project_brain(job, events, constitution=constitution)
    viewer_data = build_brain_viewer_data(job, graph, events)

    out_dir = data_dir / "viewers" / str(job_id)
    index_path = write_brain_viewer_files(viewer_data, out_dir)

    print(f"Brain Viewer v0: {index_path}")

    log = RunLogWriter(job_id=job.id)
    log.log(
        "brain_viewer_prepared",
        outcome="prepared",
        node_count=len(graph.nodes),
        edge_count=len(graph.edges),
        detail_count=len(viewer_data.node_details),
        detail_fallback_count=viewer_data.detail_fallback_count,
        mode="static",
    )


def _cmd_trust_report(job_id_str: str) -> None:
    import os

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

    from packages.orchestration.project_constitution import load_project_constitution
    from packages.orchestration.timeline import load_run_events
    from packages.orchestration.trust_report import summarize_trust_report

    env = os.environ.get("REMEDY_DATA_DIR")
    data_dir = Path(env) if env else Path(__file__).resolve().parent.parent.parent / ".data"

    target_repo_str = job.metadata.get("target_repo")
    constitution = (
        load_project_constitution(Path(target_repo_str))
        if target_repo_str
        else None
    )

    events = load_run_events(data_dir, job_id)
    print(summarize_trust_report(job, events, data_dir=data_dir, constitution=constitution))


def _cmd_timeline(job_id_str: str) -> None:
    import os

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

    from packages.orchestration.timeline import load_run_events, summarize_timeline

    env = os.environ.get("REMEDY_DATA_DIR")
    if env:
        data_dir = Path(env)
    else:
        # apps/cli/main.py is at <repo_root>/apps/cli/main.py
        data_dir = Path(__file__).resolve().parent.parent.parent / ".data"

    events = load_run_events(data_dir, job_id)
    if not events:
        print(f"No run logs found for job {job_id}.")
        return

    print(summarize_timeline(job, events))


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

    # Fast path: no pending tasks — exit cleanly regardless of permissions.
    if not any(t.status == RunState.PENDING for t in job.tasks):
        log.log("task_run_noop", outcome="no_pending_tasks")
        print(f"Job {job.id} — no pending tasks.  log={log.path}")
        return

    # Log task_run_started with the first pending task's context.
    pending_task = next((t for t in job.tasks if t.status == RunState.PENDING), None)
    pending_task_type = pending_task.inputs.get("task_type", "unknown") if pending_task else None
    log.log(
        "task_run_started",
        task_id=str(pending_task.id) if pending_task else None,
        task_type=pending_task_type,
    )

    def _fail(outcome: str, **meta: object) -> None:
        """Emit task_run_failed, preserving the terminal-event invariant."""
        log.log(
            "task_run_failed",
            task_id=str(pending_task.id) if pending_task else None,
            outcome=outcome,
            task_type=pending_task_type,
            **meta,
        )

    # Guard: deny workspace_write before the builder is called.
    # This prevents wasting an LLM call when the permission is not granted.
    if not _perm_allowed(job, Capability.workspace_write):
        _fail("permission_denied", capability="workspace_write")
        print(
            f"Error: permission denied — workspace_write is not granted for job {job.id}",
            file=sys.stderr,
        )
        sys.exit(1)

    start = time.monotonic()
    try:
        builder = OllamaBuilder()
        log.log(
            "builder_started",
            task_id=str(pending_task.id) if pending_task else None,
            provider="ollama",
            role="builder",
            model=builder.model,
            task_type=pending_task_type,
        )
        result: RunTaskResult = run_next_task(job, builder.build)
    except ImportError as exc:
        _fail("missing_dependency", error_category="ImportError")
        print(f"Error: missing dependency — {exc}", file=sys.stderr)
        sys.exit(1)
    except ValidationError as exc:
        # Must precede ValueError: pydantic.ValidationError inherits from ValueError.
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
            "task_run_noop",
            task_id=str(pending_task.id) if pending_task else None,
            outcome="no_change",
            task_type=pending_task_type,
            reason="builder_returned_no_change",
        )
        print(f"Job {job.id} — builder returned no change.  log={log.path}")
        return

    # Resolve the task artifact for logging context.
    _task_obj_for_log = next(
        (t for t in result.job.tasks if t.id == result.task_id), None
    )
    _artifact_id_for_log = (
        str(_task_obj_for_log.output_artifact_ids[0])
        if _task_obj_for_log and _task_obj_for_log.output_artifact_ids
        else None
    )
    log.log(
        "builder_completed",
        task_id=str(result.task_id),
        artifact_id=_artifact_id_for_log,
        outcome="changed",
        elapsed_ms=round(elapsed_ms),
    )

    # Annotate timing metadata onto the builder artifact.
    annotate_task_result(
        result,
        provider="ollama",
        role="builder",
        model=builder.model,
        elapsed_ms=elapsed_ms,
    )

    # Materialize builder output to workspace file.
    # workspace_write was confirmed above — no conditional needed here.
    runtime = LocalWorkspaceRuntime(job_id=job.id)
    mf = materialize_task_output(result, runtime)
    log.log(
        "workspace_materialized",
        task_id=str(result.task_id),
        workspace_file=str(mf.path),
    )

    # Verify: run Task Contract v1 checks (deterministic, local-only).
    vr = verify_task_output(result.job, result.task_id)

    # Log verification outcome.
    _task_type_for_log = (
        next(t for t in result.job.tasks if t.id == result.task_id)
        .inputs.get("task_type", "unknown")
    )
    if vr.passed:
        from packages.orchestration.task_registry import get_task_type_spec as _get_spec

        _spec = _get_spec(_task_type_for_log)
        log.log(
            "verification_passed",
            task_id=str(result.task_id),
            outcome="pass",
            verifier_profile=_spec.verifier_profile,
        )
    else:
        _failed_checks = [c.check for c in vr.failures]
        log.log(
            "verification_failed",
            task_id=str(result.task_id),
            outcome="fail",
            failure_count=len(vr.failures),
            failed_checks=_failed_checks,
        )

    # Finalize: mark COMPLETED on pass, PENDING on failure.
    finalize_task(result, vr)

    # Apply to attached repo (only on pass, repo attached, permission granted).
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
                    repo_applied = check_and_apply_to_repo(job, artifact, repo_root)
                    if repo_applied:
                        artifact.metadata["repo_applied_files"] = repo_applied
                        log.log(
                            "repo_application_completed",
                            task_id=str(result.task_id),
                            outcome="applied",
                            file_count=len(repo_applied),
                            files=repo_applied,
                        )
                    else:
                        _skip_reason = artifact.metadata.get(
                            "repo_application_skipped_reason"
                        )
                        if _skip_reason:
                            log.log(
                                "repo_application_skipped",
                                task_id=str(result.task_id),
                                outcome="skipped",
                                reason=_skip_reason,
                            )

    # Derive and materialize patch intents (only on verification pass).
    patch_intent_count = 0
    dry_run_block = ""  # formatted explanation text for CLI output after main line
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
            pi_artifact = next(
                (a for a in result.job.artifacts if a.id == pi_artifact_id), None
            )
            if pi_artifact is not None:
                pi_task_type = pi_artifact.metadata.get("task_type", "unknown")
                pi_task_index = next(
                    i for i, t in enumerate(result.job.tasks) if t.id == result.task_id
                )
                pis = derive_patch_intents(pi_artifact, pi_task_type)
                pi_errors = verify_patch_intent_set(pis)
                if pi_errors:
                    print(
                        f"  warning: patch intent verification failed "
                        f"({len(pi_errors)} error(s)) — not materialized",
                        file=sys.stderr,
                    )
                    pi_artifact.metadata["patch_intent_errors"] = pi_errors
                    log.log(
                        "patch_intent_failed",
                        task_id=str(result.task_id),
                        outcome="failed",
                        error_count=len(pi_errors),
                    )
                elif pis.intents:
                    pi_mf = materialize_patch_intents(pis, runtime, pi_task_index, pi_task_type)
                    if pi_mf is not None:
                        pi_artifact.metadata["patch_intent_file"] = str(pi_mf.path)
                        pi_artifact.metadata["patch_intent_count"] = len(pis.intents)
                        patch_intent_count = len(pis.intents)

                    # Dry-run preview: read target file (read-only), produce explanation.
                    # Uses the attached repo if one is configured; otherwise preview-only.
                    pi_repo_root = (
                        Path(job.metadata["target_repo"])
                        if job.metadata.get("target_repo")
                        else None
                    )
                    dry_run_results = generate_dry_run_preview(
                        pis,
                        pi_artifact.content or "",
                        pi_task_type,
                        pi_repo_root,
                    )
                    if dry_run_results:
                        pi_artifact.metadata["patch_intent_explanations"] = [
                            {
                                "file": r.target_path,
                                "action": r.action,
                                "risk": r.risk_level,
                                "reason": r.reason,
                                "summary": r.summary,
                            }
                            for r in dry_run_results
                        ]
                        pi_artifact.metadata["patch_intent_risks"] = [
                            r.risk_level for r in dry_run_results
                        ]
                        combined_preview = "\n\n".join(
                            r.diff_preview for r in dry_run_results
                        )
                        # diff_preview is stored in metadata but not printed to the
                        # terminal — avoids noisy output; guarded mode can surface it.
                        pi_artifact.metadata["patch_intent_diff_preview"] = (
                            truncate_preview(combined_preview)
                        )
                        dry_run_block = format_dry_run_explanations(dry_run_results)

                    risk_levels = pi_artifact.metadata.get("patch_intent_risks", [])
                    log.log(
                        "patch_intent_created",
                        task_id=str(result.task_id),
                        outcome="created",
                        intent_count=len(pis.intents),
                        risk_levels=risk_levels,
                    )
                else:
                    log.log(
                        "patch_intent_skipped",
                        task_id=str(result.task_id),
                        outcome="no_intents",
                    )

    # Persist after verification, repo application, and patch intent materialization
    # so the saved state is authoritative.
    save_job(result.job)

    task = next(t for t in result.job.tasks if t.id == result.task_id)
    task_type = task.inputs.get("task_type", "unknown")
    pending_remaining = sum(1 for t in result.job.tasks if t.status.value == "pending")

    # Final run log event before printing summary.
    if vr.passed:
        log.log("task_run_completed", task_id=str(result.task_id), outcome="pass")
    else:
        log.log("task_run_failed", task_id=str(result.task_id), outcome="fail")

    # mf is always set here: result.changed=True and workspace_write was confirmed above.
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


def _cmd_attach_project_repo(project_id_str: str, repo_path_str: str) -> None:
    from packages.orchestration.project_registry import (
        ProjectNotFoundError,
        attach_repo,
        load_project,
        save_project,
    )
    from uuid import UUID

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
    from uuid import UUID

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


def _cmd_show_project(project_id_str: str, *, json_output: bool = False) -> None:
    import json as _json

    from packages.orchestration.project_registry import (
        ProjectNotFoundError,
        export_project_json,
        load_project,
        summarize_project,
    )
    from packages.orchestration.storage import list_jobs
    from uuid import UUID

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


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="remedy",
        description="Remedy orchestration CLI",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create-job", help="Create and persist a new job")
    create.add_argument("prompt", help="User prompt describing the job")
    create.add_argument("--project", default=None, help="Project UUID to attach the job to")

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

    perm = subparsers.add_parser(
        "set-permission",
        help="Grant or deny an execution capability for a job",
    )
    perm.add_argument("job_id", help="UUID of the job")
    perm.add_argument("action", choices=["allow", "deny"], help="allow or deny")
    perm.add_argument(
        "capability",
        help="Capability name (workspace_write, repo_generated_write, repo_overwrite, shell_exec)",
    )

    show_perms = subparsers.add_parser(
        "show-permissions",
        help="Show effective permission state for all capabilities on a job",
    )
    show_perms.add_argument("job_id", help="UUID of the job")

    run_task = subparsers.add_parser(
        "run-next-task-local",
        help="Execute the next pending task using local Ollama (requires ollama package)",
    )
    run_task.add_argument("job_id", help="UUID of the job to advance")

    brain_node_p = subparsers.add_parser(
        "brain-node",
        help="Print detail for a single Project Brain node",
    )
    brain_node_p.add_argument("job_id", help="UUID of the job")
    brain_node_p.add_argument("node_id", help="Node ID from the brain graph")
    brain_node_p.add_argument(
        "--json",
        action="store_true",
        default=False,
        help="Output detail as JSON instead of text",
    )

    context_p = subparsers.add_parser(
        "context",
        help="Show Context Coverage signal for a job (what context Remedy currently has)",
    )
    context_p.add_argument("job_id", help="UUID of the job")
    context_p.add_argument(
        "--json",
        action="store_true",
        default=False,
        help="Output coverage snapshot as JSON",
    )

    brain_view_p = subparsers.add_parser(
        "brain-view",
        help="Generate a read-only local Brain Viewer (static HTML) for a job",
    )
    brain_view_p.add_argument("job_id", help="UUID of the job")

    brain_p = subparsers.add_parser(
        "brain",
        help="Print the Project Brain Graph (node/edge graph) for a job",
    )
    brain_p.add_argument("job_id", help="UUID of the job to inspect")
    brain_p.add_argument(
        "--json",
        action="store_true",
        default=False,
        help="Output graph as JSON instead of text summary (future frontend data source)",
    )

    agent_loop_p = subparsers.add_parser(
        "agent-loop",
        help="Inspect the external agent loop state for a job",
    )
    agent_loop_p.add_argument("job_id", help="UUID of the job to inspect")

    constitution_p = subparsers.add_parser(
        "constitution",
        help="Print the Project Constitution extracted from the attached repo",
    )
    constitution_p.add_argument("job_id", help="UUID of the job to show")

    trust_report = subparsers.add_parser(
        "trust-report",
        help="Print a full read-only audit/trust report for a job",
    )
    trust_report.add_argument("job_id", help="UUID of the job to show")

    timeline = subparsers.add_parser(
        "timeline",
        help="Print a human-readable timeline of all run-log events for a job",
    )
    timeline.add_argument("job_id", help="UUID of the job to show")

    cockpit = subparsers.add_parser(
        "cockpit",
        help="Print a decision-oriented status overview for a job",
    )
    cockpit.add_argument("job_id", help="UUID of the job to show")

    list_pi = subparsers.add_parser(
        "list-patch-intents",
        help="List all patch intents for a job with their approval state",
    )
    list_pi.add_argument("job_id", help="UUID of the job")

    show_pi = subparsers.add_parser(
        "show-patch-intent",
        help="Show details for a specific patch intent",
    )
    show_pi.add_argument("job_id", help="UUID of the job")
    show_pi.add_argument("intent_id", help="Intent ID (e.g. a1b2c3d4-0)")

    approve_pi = subparsers.add_parser(
        "approve-patch-intent",
        help="Record an approval decision for a patch intent (metadata only, no files changed)",
    )
    approve_pi.add_argument("job_id", help="UUID of the job")
    approve_pi.add_argument("intent_id", help="Intent ID (e.g. a1b2c3d4-0)")
    approve_pi.add_argument("--reason", default=None, help="Optional note about this decision")

    reject_pi = subparsers.add_parser(
        "reject-patch-intent",
        help="Record a rejection decision for a patch intent (metadata only, no files changed)",
    )
    reject_pi.add_argument("job_id", help="UUID of the job")
    reject_pi.add_argument("intent_id", help="Intent ID (e.g. a1b2c3d4-0)")
    reject_pi.add_argument("--reason", default=None, help="Optional note about this decision")

    create_project = subparsers.add_parser("create-project", help="Create a new project")
    create_project.add_argument("name", help="Project name")
    create_project.add_argument("--description", default=None, help="Optional project description")

    subparsers.add_parser("list-projects", help="List all projects (newest first)")

    attach_proj_repo = subparsers.add_parser(
        "attach-project-repo", help="Attach a repo path to a project"
    )
    attach_proj_repo.add_argument("project_id", help="UUID of the project")
    attach_proj_repo.add_argument("repo_path", help="Path to the repository")

    attach_proj_job = subparsers.add_parser(
        "attach-project-job", help="Link a job to a project"
    )
    attach_proj_job.add_argument("project_id", help="UUID of the project")
    attach_proj_job.add_argument("job_id", help="UUID of the job")

    show_project = subparsers.add_parser("show-project", help="Show project summary")
    show_project.add_argument("project_id", help="UUID of the project")
    show_project.add_argument(
        "--json", action="store_true", dest="json", help="Output as JSON"
    )

    args = parser.parse_args()

    if args.command == "create-job":
        _cmd_create_job(args.prompt, project_id=getattr(args, "project", None))
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
    elif args.command == "set-permission":
        _cmd_set_permission(args.job_id, args.action, args.capability)
    elif args.command == "show-permissions":
        _cmd_show_permissions(args.job_id)
    elif args.command == "run-next-task-local":
        _cmd_run_next_task_local(args.job_id)
    elif args.command == "brain-node":
        _cmd_brain_node(args.job_id, args.node_id, json_output=args.json)
    elif args.command == "brain":
        _cmd_brain(args.job_id, json_output=args.json)
    elif args.command == "context":
        _cmd_context(args.job_id, json_output=args.json)
    elif args.command == "brain-view":
        _cmd_brain_view(args.job_id)
    elif args.command == "agent-loop":
        _cmd_agent_loop(args.job_id)
    elif args.command == "constitution":
        _cmd_constitution(args.job_id)
    elif args.command == "trust-report":
        _cmd_trust_report(args.job_id)
    elif args.command == "timeline":
        _cmd_timeline(args.job_id)
    elif args.command == "cockpit":
        _cmd_cockpit(args.job_id)
    elif args.command == "list-patch-intents":
        _cmd_list_patch_intents(args.job_id)
    elif args.command == "show-patch-intent":
        _cmd_show_patch_intent(args.job_id, args.intent_id)
    elif args.command == "approve-patch-intent":
        _cmd_approve_patch_intent(args.job_id, args.intent_id, args.reason)
    elif args.command == "reject-patch-intent":
        _cmd_reject_patch_intent(args.job_id, args.intent_id, args.reason)
    elif args.command == "create-project":
        _cmd_create_project(args.name, args.description)
    elif args.command == "list-projects":
        _cmd_list_projects()
    elif args.command == "attach-project-repo":
        _cmd_attach_project_repo(args.project_id, args.repo_path)
    elif args.command == "attach-project-job":
        _cmd_attach_project_job(args.project_id, args.job_id)
    elif args.command == "show-project":
        _cmd_show_project(args.project_id, json_output=args.json)


if __name__ == "__main__":
    main()
