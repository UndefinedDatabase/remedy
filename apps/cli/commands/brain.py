"""Brain group command handlers."""

from __future__ import annotations

import json as _json
import sys
from typing import TYPE_CHECKING, Callable
from uuid import UUID

from packages.orchestration.data_paths import resolve_data_root
from packages.orchestration.storage import JobNotFoundError, load_job

if TYPE_CHECKING:
    import argparse


def _cmd_brain(job_id_str: str, *, json_output: bool = False) -> None:
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
        build_project_brain, export_project_brain_json, summarize_project_brain,
    )
    from packages.orchestration.project_constitution import load_project_constitution
    from packages.orchestration.run_log import RunLogWriter
    from packages.orchestration.timeline import load_run_events

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job_id)

    target_repo_str = job.metadata.get("target_repo")
    constitution = load_project_constitution(Path(target_repo_str)) if target_repo_str else None

    graph = build_project_brain(job, events, constitution=constitution)

    if json_output:
        print(_json.dumps(export_project_brain_json(graph), sort_keys=True))
    else:
        print(summarize_project_brain(graph))

    task_count = sum(1 for n in graph.nodes if n.type == "task")
    patch_intent_count = sum(1 for n in graph.nodes if n.type == "patch_intent")

    log = RunLogWriter(job_id=job.id)
    log.log(
        "project_brain_inspected", outcome="inspected",
        node_count=len(graph.nodes), edge_count=len(graph.edges),
        task_count=task_count, patch_intent_count=patch_intent_count,
    )


def _cmd_brain_node(job_id_str: str, node_id: str, *, json_output: bool = False) -> None:
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
        build_brain_node_detail, export_brain_node_detail_json, summarize_brain_node_detail,
    )
    from packages.orchestration.project_brain import build_project_brain
    from packages.orchestration.project_constitution import load_project_constitution
    from packages.orchestration.run_log import RunLogWriter
    from packages.orchestration.timeline import load_run_events

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job_id)

    target_repo_str = job.metadata.get("target_repo")
    constitution = load_project_constitution(Path(target_repo_str)) if target_repo_str else None

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
        "brain_node_inspected", outcome="inspected",
        node_id=detail.node_id, node_type=detail.node_type,
        connected_count=len(detail.connected_to), evidence_count=len(detail.evidence),
    )


def _cmd_brain_view(job_id_str: str) -> None:
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
    from packages.orchestration.brain_viewer import build_brain_viewer_data, write_brain_viewer_files
    from packages.orchestration.project_brain import build_project_brain
    from packages.orchestration.project_constitution import load_project_constitution
    from packages.orchestration.run_log import RunLogWriter
    from packages.orchestration.timeline import load_run_events

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job_id)

    target_repo_str = job.metadata.get("target_repo")
    constitution = None
    if target_repo_str:
        try:
            repo_path = Path(target_repo_str)
            if not repo_path.exists() or not repo_path.is_dir():
                print("Warning: project constitution unavailable for viewer.", file=sys.stderr)
            else:
                constitution = load_project_constitution(repo_path)
        except Exception:
            print("Warning: project constitution unavailable for viewer.", file=sys.stderr)

    graph = build_project_brain(job, events, constitution=constitution)
    viewer_data = build_brain_viewer_data(job, graph, events)

    out_dir = data_dir / "viewers" / str(job_id)
    index_path = write_brain_viewer_files(viewer_data, out_dir)

    print(f"Brain Viewer v0: {index_path}")

    log = RunLogWriter(job_id=job.id)
    log.log(
        "brain_viewer_prepared", outcome="prepared",
        node_count=len(graph.nodes), edge_count=len(graph.edges),
        detail_count=len(viewer_data.node_details),
        detail_fallback_count=viewer_data.detail_fallback_count, mode="static",
    )


def _cmd_context(job_id_str: str, *, json_output: bool = False) -> None:
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
        derive_context_coverage, export_context_coverage_json, summarize_context_coverage,
    )
    from packages.orchestration.project_constitution import load_project_constitution
    from packages.orchestration.run_log import RunLogWriter
    from packages.orchestration.timeline import load_run_events

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job_id)

    target_repo_str = job.metadata.get("target_repo")
    constitution = None
    if target_repo_str:
        try:
            repo_path = Path(target_repo_str)
            if not repo_path.exists() or not repo_path.is_dir():
                print("Warning: project constitution unavailable for context coverage.", file=sys.stderr)
            else:
                constitution = load_project_constitution(repo_path)
        except Exception:
            print("Warning: project constitution unavailable for context coverage.", file=sys.stderr)

    snapshot = derive_context_coverage(job, events, constitution=constitution)

    if json_output:
        print(_json.dumps(export_context_coverage_json(snapshot), sort_keys=True))
    else:
        print(summarize_context_coverage(snapshot))

    log = RunLogWriter(job_id=job.id)
    log.log(
        "context_coverage_inspected", outcome="inspected",
        score=snapshot.score,
        present_signal_count=sum(1 for s in snapshot.signals if s.present),
        missing_signal_count=len(snapshot.missing_keys), scope=snapshot.scope,
    )


def _cmd_trust_report(job_id_str: str) -> None:
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

    data_dir = resolve_data_root()
    target_repo_str = job.metadata.get("target_repo")
    constitution = load_project_constitution(Path(target_repo_str)) if target_repo_str else None
    events = load_run_events(data_dir, job_id)
    print(summarize_trust_report(job, events, data_dir=data_dir, constitution=constitution))


def _cmd_timeline(job_id_str: str) -> None:
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

    from packages.orchestration.timeline import load_run_events, summarize_timeline
    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job_id)
    if not events:
        print(f"No run logs found for job {job_id}.")
        return
    print(summarize_timeline(job, events))


def _cmd_cockpit(job_id_str: str) -> None:
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

    data_dir = resolve_data_root()
    target_repo_str = job.metadata.get("target_repo")
    constitution = load_project_constitution(Path(target_repo_str) if target_repo_str else None)
    events = load_run_events(data_dir, job_id)
    print(summarize_cockpit(job, events, data_dir=data_dir, constitution=constitution))


def _cmd_constitution(job_id_str: str) -> None:
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
    from packages.orchestration.project_constitution import load_project_constitution, render_constitution
    from packages.orchestration.run_log import RunLogWriter

    target_repo_str = job.metadata.get("target_repo")
    repo_root = Path(target_repo_str) if target_repo_str else None

    constitution = load_project_constitution(repo_root)
    print(render_constitution(constitution, repo_root))

    log = RunLogWriter(job_id=job.id)
    log.log(
        "project_constitution_loaded", outcome="loaded",
        source_count=len(constitution.source_files),
        warning_count=len(constitution.warnings),
        has_test_commands=bool(constitution.test_commands),
    )


def _cmd_brain_continue(
    job_id_str: str, node_id: str, prompt: str,
    *, task_type: str | None = None, json_output: bool = False,
) -> None:
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
    from packages.orchestration.continue_from_node import (
        continue_from_node, export_continue_result_json,
    )
    from packages.orchestration.project_brain import build_project_brain
    from packages.orchestration.project_constitution import load_project_constitution
    from packages.orchestration.timeline import load_run_events

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job_id)

    target_repo_str = job.metadata.get("target_repo")
    constitution = load_project_constitution(Path(target_repo_str)) if target_repo_str else None

    graph = build_project_brain(job, events, constitution=constitution)

    try:
        result = continue_from_node(job, graph, node_id, prompt, task_type=task_type)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if json_output:
        print(_json.dumps(export_continue_result_json(result), sort_keys=True))
    else:
        print(f"Created child job: {result.child_job_id}")
        print(f"  Parent: {result.parent_job_id[:8]}")
        print(f"  Origin: {result.origin_node_type} ({result.origin_node_id})")
        if result.inherited_project:
            print("  Project: inherited")
        if result.inherited_repo:
            print("  Repo: inherited")


def _cmd_agent_loop(job_id_str: str) -> None:
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

    from packages.orchestration.agent_loop import derive_agent_loop_state, summarize_agent_loop_state
    from packages.orchestration.run_log import RunLogWriter
    from packages.orchestration.timeline import load_run_events

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job_id)
    state = derive_agent_loop_state(job, events)

    print(summarize_agent_loop_state(job, state))

    log = RunLogWriter(job_id=job.id)
    log.log(
        "agent_loop_inspected", outcome="inspected",
        stage=state.current_stage.value, decision=state.decision.value,
        cycle=state.cycle, max_cycles=state.max_cycles,
        pending_finding_count=len(state.pending_findings),
    )


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "brain.graph": lambda args: _cmd_brain(args.job_id, json_output=args.json),
    "brain.node": lambda args: _cmd_brain_node(args.job_id, args.node_id, json_output=args.json),
    "brain.view": lambda args: _cmd_brain_view(args.job_id),
    "brain.context": lambda args: _cmd_context(args.job_id, json_output=args.json),
    "brain.trust": lambda args: _cmd_trust_report(args.job_id),
    "brain.timeline": lambda args: _cmd_timeline(args.job_id),
    "brain.cockpit": lambda args: _cmd_cockpit(args.job_id),
    "brain.continue": lambda args: _cmd_brain_continue(
        args.job_id, args.node_id, args.prompt,
        task_type=getattr(args, "task_type", None),
        json_output=args.json,
    ),
    "brain.constitution": lambda args: _cmd_constitution(args.job_id),
}
