"""
Localhost UI Server — read-only HTTP server for the Remedy UI.

Serves a single-page app shell and JSON API endpoints for job inspection.
Binds 127.0.0.1 only.  No mutation endpoints.  No POST/PUT/DELETE.
Token-gated API access via per-run random token in URL.

Scope:
  - Read-only only.
  - No repo mutation, no shell (except optional opener and auto-build).
  - No external network, CDN (auto-build uses local npm only).
  - Serves only safe summaries, counts, statuses, IDs, hashes, next actions.
  - No raw artifact content, file content, diffs, stdout/stderr, approval
    reasons, secrets, or tracebacks in any response.

Public API::

    start_ui_server(job_id, host, port, token, open_browser, info_file)
"""

from __future__ import annotations

import json
import os
import secrets
import sys
from datetime import datetime, timezone
from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse
from uuid import UUID


# ---------------------------------------------------------------------------
# Safe data builders (no raw content leaks)
# ---------------------------------------------------------------------------

def _load_events(job: Any) -> list[dict[str, Any]]:
    """Load run-log events for a job."""
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.timeline import load_run_events
    return load_run_events(resolve_data_root(), job.id)


def _safe_error(code: int, message: str) -> tuple[int, dict[str, Any]]:
    return code, {"error": message}


def _load_job(job_id_str: str) -> Any:
    """Load a Job by UUID string, return (job, error_tuple)."""
    try:
        job_id = UUID(job_id_str)
    except ValueError:
        return None, _safe_error(400, "invalid job_id")
    try:
        from packages.orchestration.storage import JobNotFoundError, load_job
        job = load_job(job_id)
    except (FileNotFoundError, JobNotFoundError):
        return None, _safe_error(404, "job not found")
    return job, None


def _task_test_status(task_id: str, events: list[dict]) -> str:
    """Return scoped test status for a task: 'pass', 'fail', or 'none'."""
    task_tests = [
        e for e in events
        if e.get("event") == "test_run_completed"
        and e.get("metadata", {}).get("task_id") == task_id
    ]
    if not task_tests:
        return "none"
    latest = task_tests[-1]
    return "pass" if latest.get("metadata", {}).get("exit_code") == 0 else "fail"


def _task_outcome_summary(task_id: str, tstat: str, events: list[dict]) -> str:
    """Derive a human-readable outcome for a task from events and status."""
    if tstat == "completed":
        has_proof = any(
            e.get("event") == "proof_collected"
            and e.get("metadata", {}).get("task_id") == task_id
            for e in events
        )
        test = _task_test_status(task_id, events)
        if has_proof and test == "pass":
            return "Completed and verified"
        if has_proof:
            return "Completed with proof"
        if test == "pass":
            return "Completed, tests pass"
        return "Completed"
    if tstat in ("running", "active"):
        return "In progress"
    if tstat in ("blocked", "failed"):
        return "Blocked"
    return ""


def _task_changed_files_count(task_id: str, events: list[dict]) -> int:
    """Count files changed for a task from apply events."""
    applies = [
        e for e in events
        if e.get("event") == "patch_intent_applied"
        and e.get("metadata", {}).get("task_id") == task_id
    ]
    return sum(e.get("metadata", {}).get("file_count", 1) for e in applies)


def _task_changed_files_safe(task_id: str, events: list[dict]) -> list[str]:
    """Return safe filenames changed for a task (no paths with secrets)."""
    applies = [
        e for e in events
        if e.get("event") == "patch_intent_applied"
        and e.get("metadata", {}).get("task_id") == task_id
    ]
    names: list[str] = []
    for e in applies:
        fnames = e.get("metadata", {}).get("files", [])
        for f in fnames[:10]:
            base = str(f).rsplit("/", 1)[-1] if "/" in str(f) else str(f)
            if base and len(base) < 80:
                names.append(base)
    return names[:10]


def _task_blocked_reason(task_id: str, tstat: str, events: list[dict]) -> str:
    """Return human-readable blocked reason if task is blocked."""
    if tstat not in ("blocked", "failed"):
        return ""
    stops = [
        e for e in events
        if e.get("event") == "stop_reason_recorded"
        and e.get("metadata", {}).get("task_id") == task_id
    ]
    if stops:
        reason = stops[-1].get("metadata", {}).get("stop_reason", "")
        return reason.replace("_", " ").capitalize() if reason else "Blocked"
    return "Blocked"


def _task_completed_at(task_id: str, events: list[dict]) -> str:
    """Return completion timestamp if available."""
    proofs = [
        e for e in events
        if e.get("event") == "proof_collected"
        and e.get("metadata", {}).get("task_id") == task_id
    ]
    if proofs:
        return proofs[-1].get("timestamp", "")
    applies = [
        e for e in events
        if e.get("event") == "patch_intent_applied"
        and e.get("metadata", {}).get("task_id") == task_id
    ]
    if applies:
        return applies[-1].get("timestamp", "")
    return ""


def _event_backed_actor(events: list[dict]) -> str:
    """Derive current actor from most recent event, not hardcoded."""
    if not events:
        return ""
    _actor_map = {
        "task_created": "Builder", "patch_intent_created": "Builder",
        "patch_intent_approved": "User", "patch_intent_applied": "Builder",
        "test_run_completed": "Builder", "proof_collected": "Builder",
        "stop_reason_recorded": "System", "human_decision_requested": "User",
    }
    last_event = events[-1].get("event", "")
    return _actor_map.get(last_event, "System")


def _build_timeline_events(events: list[dict]) -> list[dict[str, Any]]:
    """Derive cycle-aware timeline events from the event ledger."""
    _event_to_kind = {
        "task_created": "llm_action",
        "patch_intent_created": "llm_action",
        "patch_intent_approved": "llm_action",
        "patch_intent_applied": "llm_action",
        "test_run_completed": "test",
        "proof_collected": "review",
        "human_decision_requested": "review",
    }
    _event_to_phase = {
        "task_created": "planning",
        "patch_intent_created": "build",
        "patch_intent_approved": "build",
        "patch_intent_applied": "build",
        "test_run_completed": "test",
        "proof_collected": "review",
        "human_decision_requested": "review",
    }
    result: list[dict[str, Any]] = []
    for idx, e in enumerate(events):
        ev = e.get("event", "")
        kind = _event_to_kind.get(ev)
        if kind is None:
            continue
        result.append({
            "id": f"te-{idx}",
            "kind": kind,
            "phase": _event_to_phase.get(ev, "build"),
            "done": True,
            "label": ev.replace("_", " ").capitalize(),
        })
    return result


def _build_dashboard(job: Any) -> dict[str, Any]:
    """Build safe dashboard payload for a job."""
    events = _load_events(job)

    # Status
    state = job.state.value if hasattr(job.state, "value") else str(job.state)
    task_count = len(job.tasks)
    artifact_count = len(job.artifacts)

    # Lifecycle counts from events
    apply_count = sum(1 for e in events if e.get("event") == "patch_intent_applied")
    proof_count = sum(1 for e in events if e.get("event") == "proof_collected")
    test_count = sum(1 for e in events if e.get("event") == "test_run_completed")
    revert_count = sum(1 for e in events if e.get("event") == "patch_intent_reverted")

    # Approvals
    pending_approvals = 0
    for art in job.artifacts:
        meta = art.metadata or {}
        explanations = meta.get("patch_intent_explanations", [])
        for _idx, intent in enumerate(explanations):
            approval = intent.get("approval_state", "pending")
            if approval == "pending":
                pending_approvals += 1

    # Blockers / decisions
    blocker_count = sum(1 for e in events if e.get("event") == "stop_reason_recorded"
                        and e.get("outcome") != "resolved")
    decision_count = sum(1 for e in events if e.get("event") == "human_decision_requested"
                         and e.get("outcome") != "resolved")

    # Latest proof
    proof_events = [e for e in events if e.get("event") == "proof_collected"]
    latest_proof = None
    if proof_events:
        pe = proof_events[-1]
        pm = pe.get("metadata", {})
        latest_proof = {
            "hash": pm.get("content_hash", "")[:16],
            "intent_id": pm.get("intent_id", ""),
            "timestamp": pe.get("timestamp", ""),
        }

    # Latest test
    test_events = [e for e in events if e.get("event") == "test_run_completed"]
    latest_test = None
    if test_events:
        te = test_events[-1]
        tm = te.get("metadata", {})
        latest_test = {
            "exit_code": tm.get("exit_code"),
            "command_hash": tm.get("command_hash", "")[:16],
            "timestamp": te.get("timestamp", ""),
        }

    # Token budget
    token_mode = "compact"
    for e in reversed(events):
        if e.get("event") == "context_pack_created":
            token_mode = e.get("metadata", {}).get("mode", "compact")
            break

    # Guidance
    guidance_cards: list[dict[str, str]] = []
    try:
        from packages.orchestration.guidance import build_guidance_cards
        cards = build_guidance_cards(job, events)
        guidance_cards = [
            {
                "id": c.id,
                "title": c.title,
                "severity": c.severity,
                "why": c.why_it_matters,
                "action": c.safe_next_action,
                "command": c.command,
            }
            for c in cards
        ]
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        pass

    # Primary next action
    next_action = ""
    if guidance_cards:
        next_action = guidance_cards[0].get("command", "")

    # What-happened lifecycle
    lifecycle: list[dict[str, str]] = []
    lifecycle_types = [
        ("task_created", "Task created"),
        ("patch_intent_created", "Patch proposed"),
        ("patch_intent_approved", "Patch approved"),
        ("patch_intent_applied", "Patch applied"),
        ("proof_collected", "Proof collected"),
        ("test_run_completed", "Tests run"),
    ]
    for etype, label in lifecycle_types:
        matching = [e for e in events if e.get("event") == etype]
        if matching:
            lifecycle.append({
                "step": label,
                "count": len(matching),
                "latest": matching[-1].get("timestamp", ""),
            })

    # Truth contract
    has_real_events = len(events) > 0
    has_real_tasks = task_count > 0
    # Demo mode only with explicit flag — normal empty jobs are NOT demo
    demo_mode = os.environ.get("REMEDY_UI_DEMO_MODE") == "1"
    synthetic_count = 0
    missing_sources: list[str] = []
    if not has_real_events:
        missing_sources.append("events")
    if not has_real_tasks:
        missing_sources.append("tasks")

    # Build tasks list for dashboard
    task_items: list[dict[str, Any]] = []
    for idx, t in enumerate(job.tasks):
        tstat = t.status.value if hasattr(t.status, "value") else str(t.status)
        tid = str(t.id)
        task_items.append({
            "id": tid,
            "title": t.description[:80] if t.description else f"Task {idx + 1}",
            "status": tstat,
            "verified": tstat == "completed",
            "source": "real",
            "accepted": tstat == "completed",
            "rank": idx,
            "related_node_id": tid,
            "short_reason": "",
            "proof_status": "verified" if any(
                e.get("event") == "proof_collected" and e.get("metadata", {}).get("task_id") == tid
                for e in events
            ) else "none",
            "test_status": _task_test_status(tid, events),
            "outcome_summary": _task_outcome_summary(tid, tstat, events),
            "changed_files_count": _task_changed_files_count(tid, events),
            "changed_files_safe": _task_changed_files_safe(tid, events),
            "blocked_reason": _task_blocked_reason(tid, tstat, events),
            "completed_at": _task_completed_at(tid, events),
            "is_current": tstat in ("running", "active"),
            "is_future": tstat == "pending",
            "is_reviewer_suggested": False,
        })

    # Build activity from events
    activity_items: list[dict[str, Any]] = []
    _event_actors = {
        "task_created": "Builder", "patch_intent_created": "Builder",
        "patch_intent_approved": "User", "patch_intent_applied": "Builder",
        "test_run_completed": "Builder", "proof_collected": "Builder",
        "stop_reason_recorded": "System", "human_decision_requested": "System",
    }
    for e in events[-8:]:
        ev = e.get("event", "")
        activity_items.append({
            "id": f"evt-{e.get('timestamp', '')[:19]}",
            "time": e.get("timestamp", ""),
            "actor": _event_actors.get(ev, "System"),
            "event_kind": ev,
            "summary": ev.replace("_", " ").capitalize(),
            "related_node_id": "",
            "severity": "info",
            "source": "event_ledger",
        })

    # Phases — full 6-phase canonical set
    is_finalized = state in ("completed", "done", "finalized")
    phases = [
        {"id": "job", "title": "Job", "status": "done", "rank": 0, "started_at": "", "completed_at": "", "current": False, "source": "derived"},
        {"id": "planning", "title": "Planning", "status": "done" if has_real_tasks else "current", "rank": 1, "started_at": "", "completed_at": "", "current": not has_real_tasks, "source": "derived"},
        {"id": "build", "title": "Build", "status": "done" if is_finalized else ("current" if apply_count > 0 else "pending"), "rank": 2, "started_at": "", "completed_at": "", "current": apply_count > 0 and not is_finalized, "source": "derived"},
        {"id": "test", "title": "Test", "status": "done" if test_count > 0 else "pending", "rank": 3, "started_at": "", "completed_at": "", "current": False, "source": "derived"},
        {"id": "review", "title": "Review", "status": "done" if proof_count > 0 else "pending", "rank": 4, "started_at": "", "completed_at": "", "current": False, "source": "derived"},
        {"id": "finalized", "title": "Finalized", "status": "done" if is_finalized else "pending", "rank": 5, "started_at": "", "completed_at": "", "current": False, "source": "derived"},
    ]

    # Timeline events — cycle-aware from event ledger
    timeline_events = _build_timeline_events(events)

    # Live state
    running = state in ("active", "running")
    last_event_at = events[-1].get("timestamp", "") if events else ""

    # Graph summary from actual brain data
    try:
        from packages.orchestration.project_brain import build_project_brain
        brain = build_project_brain(job, events)
        graph_node_count = len(brain.nodes)
        graph_edge_count = len(brain.edges)
    except (ImportError, TypeError, ValueError, KeyError, AttributeError):
        graph_node_count = task_count + artifact_count
        graph_edge_count = max(0, graph_node_count - 1)

    # Next action
    na_label = next_action if next_action else "Review project state"
    na_command = next_action if next_action else "remedy dev status"

    generated_at = datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return {
        "version": 3,
        "job_id": str(job.id),
        "generated_at": generated_at,
        "source": "server",
        "live": {
            "running": running,
            "state": state,
            "current_actor": _event_backed_actor(events) if running else "",
            "current_action": "",
            "current_task_id": "",
            "last_event_at": last_event_at,
            "stale": not has_real_events,
            "source": "event_ledger",
            "confidence": "high" if has_real_events else "none",
        },
        "metrics": {
            "open": blocker_count + decision_count,
            "planned": sum(1 for t in job.tasks if (t.status.value if hasattr(t.status, "value") else "") == "pending"),
            "done": sum(1 for t in job.tasks if (t.status.value if hasattr(t.status, "value") else "") == "completed"),
            "progress_percent": round((sum(1 for t in job.tasks if (t.status.value if hasattr(t.status, "value") else "") == "completed") / max(task_count, 1)) * 100),
            "source_counts": {"tasks": task_count, "events": len(events), "artifacts": artifact_count},
            "computed_from": "job_tasks_and_events",
        },
        "token_usage": _build_token_usage(events),
        "tasks": task_items,
        "activity": activity_items,
        "phases": phases,
        "graph_summary": {
            "node_count": graph_node_count,
            "edge_count": graph_edge_count,
            "visible_node_count": graph_node_count,
            "visible_edge_count": graph_edge_count,
            "source": "project_brain",
            "mode": "force_graph",
            "full_graph_requires_explicit_toggle": True,
        },
        "next_action": {
            "kind": "guidance",
            "label": na_label,
            "command": na_command,
            "reason": "Next recommended step",
            "requires_user": True,
            "related_node_id": "",
        },
        "truth": {
            "fallback_count": 0 if has_real_events else 1,
            "synthetic_count": synthetic_count,
            "demo_mode": demo_mode,
            "stale_sources": [] if has_real_events else ["events"],
            "missing_sources": missing_sources,
            "computed_from": "job_model_and_event_ledger",
        },
        "timeline_events": timeline_events,
        "pipeline": _build_pipeline_section(job, events),
        "resume": _build_resume_section(job, events),
        "project_summary": _build_project_summary_section(job),
        "worker": _build_worker_section(),
        "redaction": {
            "policy": "safe_summaries_only",
            "raw_content_exposed": False,
            "unsafe_fields_blocked": True,
        },
        # Legacy fields — classified under "legacy" key.
        # Primary truth is in metrics, tasks, phases, truth, live.
        # Do not use legacy fields as core truth in new consumers.
        "legacy": {
            "job_name": job.name,
            "task_count": task_count,
            "guidance": guidance_cards,
            "lifecycle": lifecycle,
        },
    }


def _build_resume_section(job: Any, events: list[dict[str, Any]]) -> dict[str, Any]:
    """Build safe resume/checkpoint visibility for dashboard."""
    try:
        from packages.orchestration.event_replay import (
            find_checkpoints,
            replay_job,
        )
        from packages.orchestration.data_paths import resolve_data_root
        data_dir = resolve_data_root()
        replay = replay_job(str(job.id), data_dir)
        cps = find_checkpoints(replay)

        safe_cps = [c for c in cps if c.safe_to_resume]
        latest_safe = safe_cps[-1] if safe_cps else None

        return {
            "replay_available": not replay.degraded,
            "replay_degraded": replay.degraded,
            "latest_checkpoint": {
                "id": latest_safe.id,
                "kind": latest_safe.kind,
                "label": latest_safe.label,
                "next_command": latest_safe.next_command,
            } if latest_safe else None,
            "checkpoint_count": len(cps),
            "safe_checkpoint_count": len(safe_cps),
            "can_resume": bool(safe_cps),
            "blocked_reason": "" if safe_cps else (
                cps[-1].blocked_reason if cps else "no_checkpoints"
            ),
            "last_event_at": replay.last_event_at,
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {
            "replay_available": False,
            "replay_degraded": True,
            "latest_checkpoint": None,
            "checkpoint_count": 0,
            "safe_checkpoint_count": 0,
            "can_resume": False,
            "blocked_reason": "replay_error",
            "last_event_at": "",
        }


def _build_project_summary_section(job: Any) -> dict[str, Any] | None:
    """Build project-level summary for dashboard. Returns None if no project."""
    try:
        from packages.orchestration.data_paths import resolve_data_root
        from packages.orchestration.project_registry import load_project
        from packages.orchestration.project_summary import (
            build_project_summary,
            detect_patterns,
            export_project_summary_json,
        )
        from packages.orchestration.storage import list_jobs
        from packages.orchestration.timeline import load_run_events

        project_id = job.metadata.get("project_id")
        if not project_id:
            return None

        from uuid import UUID
        project = load_project(UUID(project_id))
        all_jobs = list_jobs()
        linked_jobs = [j for j in all_jobs if str(j.id) in project.job_ids]

        data_dir = resolve_data_root()
        all_events: dict[str, list[dict]] = {}
        for j in linked_jobs:
            all_events[str(j.id)] = load_run_events(data_dir, j.id)

        summary = build_project_summary(project, linked_jobs, all_events)
        patterns = detect_patterns(linked_jobs, all_events)

        model_confidence = "low"
        needs_real_check = True
        real_builder_count = sum(
            1 for evs in all_events.values() for ev in evs
            if ev.get("event") == "autorun_builder_completed"
            and ev.get("metadata", {}).get("provider") not in (None, "", "fixture", "mock")
        )
        if real_builder_count >= 15:
            model_confidence = "high"
            needs_real_check = False
        elif real_builder_count >= 5:
            model_confidence = "medium"
            needs_real_check = False

        return {
            "project_id": summary.project_id,
            "job_count": summary.job_count,
            "active_job_count": summary.active_job_count,
            "blocked_job_count": summary.blocked_job_count,
            "current_focus": summary.current_focus,
            "top_blocker": summary.blockers[0] if summary.blockers else "",
            "repeated_pattern_count": len(patterns),
            "model_quality_confidence": model_confidence,
            "needs_real_model_check": needs_real_check,
            "suggested_next_step": summary.suggested_next_step,
            "next_command": summary.next_command,
            "redaction": "safe_metadata_only",
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return None


def _build_worker_section() -> dict[str, Any] | None:
    """Build safe worker status for dashboard."""
    try:
        from packages.orchestration.data_paths import resolve_data_root
        from packages.orchestration.worker_queue import get_worker_status, list_queued

        data_dir = resolve_data_root()
        status = get_worker_status(data_dir)
        queue = list_queued(data_dir)
        queued_count = sum(1 for e in queue if e.lifecycle_state == "queued")

        return {
            "worker_available": bool(status.worker_id),
            "worker_id": status.worker_id,
            "lifecycle_state": status.lifecycle_state,
            "current_job_id": status.current_job_id,
            "queue_count": queued_count,
            "heartbeat_at": status.heartbeat_at,
            "stale": status.stale,
            "why_it_stopped": status.why_it_stopped,
            "next_command": "remedy worker run --once" if not status.worker_id else "",
            "redaction": "safe_metadata_only",
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return None


def _build_token_usage(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Build safe token usage summary from events. Estimated only — no exact billing."""
    by_role: dict[str, int] = {}
    total = 0
    sources_seen: set[str] = set()

    for e in events:
        meta = e.get("metadata", {})
        tokens = meta.get("estimated_tokens", 0)
        if not isinstance(tokens, (int, float)) or tokens <= 0:
            continue
        tokens = int(tokens)
        total += tokens

        ev = e.get("event", "")
        if ev == "source_context_injected":
            by_role["context"] = by_role.get("context", 0) + tokens
            sources_seen.add("source_context")
        elif ev == "project_memory_recalled":
            by_role["memory"] = by_role.get("memory", 0) + tokens
            sources_seen.add("memory")
        elif ev == "repair_context_created":
            by_role["repair"] = by_role.get("repair", 0) + tokens
            sources_seen.add("repair_context")
        elif ev in ("context_pack_created",):
            by_role["planner"] = by_role.get("planner", 0) + tokens
            sources_seen.add("context_pack")
        else:
            by_role["other"] = by_role.get("other", 0) + tokens

    known = total > 0
    missing: list[str] = []
    if "source_context" not in sources_seen:
        missing.append("source_context")
    if "memory" not in sources_seen:
        missing.append("memory")

    return {
        "total_tokens": total if known else None,
        "known": known,
        "estimated": True,
        "source": "event_metadata",
        "by_role": by_role if by_role else {},
        "missing_sources": missing,
    }


def _build_pipeline_section(job: Any, events: list[dict[str, Any]]) -> dict[str, Any]:
    """Build structured autocoder pipeline status for dashboard v4.

    All fields derived from real events/job state. Unknown = null.
    No raw provider output, diffs, test output, or approval reasons.
    """
    # Provider
    started_events = [e for e in events if e.get("event") == "autorun_started"]
    builder_events = [e for e in events if e.get("event") == "autorun_builder_completed"]
    provider_error_events = [e for e in events if e.get("event") == "autorun_provider_error"]

    provider = None
    provider_mode = "none"
    if builder_events:
        provider = builder_events[-1].get("metadata", {}).get("provider")
        provider_mode = provider or "unknown"
    elif provider_error_events:
        provider = provider_error_events[-1].get("metadata", {}).get("provider")
        provider_mode = provider or "unknown"

    # Source context
    ctx_events = [e for e in events if e.get("event") == "source_context_injected"]
    source_context_injected = bool(ctx_events)
    source_context_meta: dict[str, Any] = {}
    if ctx_events:
        cm = ctx_events[-1].get("metadata", {})
        source_context_meta = {
            "file_count": cm.get("file_count", 0),
            "test_file_count": cm.get("test_file_count", 0),
            "estimated_tokens": cm.get("estimated_tokens", 0),
            "truncated": cm.get("truncated", False),
            "selection_hash": str(cm.get("selection_hash", ""))[:12],
        }

    # Memory
    mem_events = [e for e in events if e.get("event") == "project_memory_recalled"]
    memory_used = bool(mem_events)
    memory_item_count = mem_events[-1].get("metadata", {}).get("item_count", 0) if mem_events else 0
    memory_truncated = mem_events[-1].get("metadata", {}).get("truncated", False) if mem_events else False
    memory_context_hash = str(mem_events[-1].get("metadata", {}).get("context_hash", ""))[:12] if mem_events else ""

    # Parse
    parse_events = [e for e in events if e.get("event") == "builder_patch_parsed"]
    structured_patch_attempted = bool(builder_events or parse_events)
    parse_success = None
    parse_error_kind = ""
    if parse_events:
        pm = parse_events[-1].get("metadata", {})
        parse_success = pm.get("parse_success", False)
        if not parse_success:
            parse_error_kind = pm.get("error_kind", "")

    # Intent / approval
    intent_events = [e for e in events if e.get("event") in (
        "structured_patch_intent_created", "builder_bridge_intent_approved")]
    intent_id = ""
    intent_status = "none"
    approval_required = False
    approval_status = "none"
    if intent_events:
        intent_id = intent_events[-1].get("metadata", {}).get("intent_id", "")
        if any(e.get("event") == "builder_bridge_intent_approved" for e in intent_events):
            intent_status = "approved"
            approval_status = "approved"
        else:
            intent_status = "created"
            approval_required = True
            approval_status = "pending"

    # Check job artifacts for pending approvals
    for art in job.artifacts:
        meta = art.metadata or {}
        explanations = meta.get("patch_intent_explanations", [])
        for expl in explanations:
            ast = expl.get("approval_state", "")
            if ast == "pending":
                approval_required = True
                approval_status = "pending"
            elif ast == "approved" and approval_status == "none":
                approval_status = "approved"

    # Source apply
    apply_events = [e for e in events if e.get("event") == "patch_intent_applied"]
    source_apply_status = "applied" if apply_events else "none"

    # Tests
    test_events = [e for e in events if e.get("event") in (
        "test_run_completed", "builder_bridge_test_completed")]
    tests_status = "none"
    tests_passed = None
    if test_events:
        last_test = test_events[-1].get("metadata", {})
        tests_passed = last_test.get("passed", last_test.get("exit_code") == 0)
        tests_status = "pass" if tests_passed else "fail"

    # Repair loop
    repair_cycle_events = [e for e in events if e.get("event") == "repair_loop_cycle_started"]
    repair_loop_used = bool(repair_cycle_events) or any(
        e.get("event") == "repair_context_created" for e in events)
    repair_cycle_count = repair_cycle_events[-1].get("metadata", {}).get("cycle", 0) if repair_cycle_events else 0
    repair_max_cycles = repair_cycle_events[-1].get("metadata", {}).get("max_cycles", 0) if repair_cycle_events else 0

    # Stop reason
    stop_reason = ""
    stop_events = [e for e in events if e.get("event") in (
        "repair_loop_stopped", "repair_loop_succeeded")]
    if stop_events:
        stop_reason = stop_events[-1].get("metadata", {}).get("reason", "")
    elif parse_events and not parse_success:
        pm = parse_events[-1].get("metadata", {})
        stop_reason = pm.get("stop_reason", "") or pm.get("error_kind", "")
    elif provider_error_events:
        stop_reason = provider_error_events[-1].get("metadata", {}).get("stop_reason", "")
    elif test_events and tests_passed is False:
        stop_reason = "test_failed_after_apply"

    _STOP_LABELS = {
        "provider_output_prose_only": "Model returned prose, not a patch",
        "provider_output_malformed": "Model output could not be parsed",
        "provider_unavailable": "Provider not reachable",
        "unsafe_shell_command": "Output contained shell commands",
        "validation_failed": "Patch structure invalid",
        "unsafe_path": "Absolute path not allowed",
        "path_traversal": "Path traversal not allowed",
        "approval_required": "Human approval required",
        "source_apply_failed": "Patch could not be applied",
        "test_failed_after_apply": "Tests failed after apply",
        "repair_budget_exhausted": "Repair budget exhausted",
        "repeated_patch_detected": "Same patch produced twice",
        "no_structured_patch_text": "No patch in builder output",
        "test_timeout": "Test execution timed out",
    }
    stop_reason_label = _STOP_LABELS.get(stop_reason, stop_reason.replace("_", " ").capitalize() if stop_reason else "")

    # Next command
    next_command = _pipeline_next_command(
        str(job.id), stop_reason, approval_required, intent_id,
        source_apply_status, tests_status,
    )

    # Staleness
    stale = not bool(events)

    return {
        "version": 1,
        "provider": provider,
        "provider_mode": provider_mode,
        "source_context": {
            "injected": source_context_injected,
            **source_context_meta,
        },
        "memory": {
            "used": memory_used,
            "item_count": memory_item_count,
            "truncated": memory_truncated,
            "context_hash": memory_context_hash,
        },
        "structured_patch_attempted": structured_patch_attempted,
        "parse_success": parse_success,
        "parse_error_kind": parse_error_kind,
        "intent_id": intent_id,
        "intent_status": intent_status,
        "approval_required": approval_required,
        "approval_status": approval_status,
        "source_apply_status": source_apply_status,
        "tests_status": tests_status,
        "tests_passed": tests_passed,
        "repair_loop": {
            "used": repair_loop_used,
            "cycle_count": repair_cycle_count,
            "max_cycles": repair_max_cycles,
        },
        "stop_reason": stop_reason,
        "stop_reason_label": stop_reason_label,
        "next_command": next_command,
        "stale": stale,
        "source": "event_ledger",
    }


def _pipeline_next_command(
    job_id: str, stop_reason: str, approval_required: bool,
    intent_id: str, source_apply_status: str, tests_status: str,
) -> str:
    """Generate next safe catalog-valid command based on pipeline state."""
    if stop_reason == "approval_required" and intent_id:
        return f"remedy patch approve {job_id} {intent_id}"
    if stop_reason == "provider_unavailable":
        return "remedy worker resources --json"
    if stop_reason in ("provider_output_prose_only", "provider_output_malformed"):
        return f"remedy do \"<goal>\" --repo . --builder-provider fixture --json"
    if stop_reason == "test_failed_after_apply":
        return f"remedy job summary {job_id} --json"
    if stop_reason == "repair_budget_exhausted":
        return f"remedy job summary {job_id} --json"
    if approval_required and intent_id:
        return f"remedy patch show {job_id} {intent_id}"
    if source_apply_status == "applied" and tests_status == "none":
        return f"remedy test discover {job_id} --json"
    if tests_status == "pass":
        return f"remedy job summary {job_id} --json"
    return "remedy dev status --json"


def _build_brain_json(job: Any) -> dict[str, Any]:
    """Build safe brain graph payload."""
    from packages.orchestration.brain_detail import (
        build_brain_node_detail,
        export_brain_node_detail_json,
    )
    from packages.orchestration.project_brain import (
        build_project_brain,
        export_project_brain_json,
    )

    events = _load_events(job)
    graph = build_project_brain(job, events)
    brain_json = export_project_brain_json(graph)

    details = {}
    for node in graph.nodes:
        try:
            detail = build_brain_node_detail(job, graph, node.id, events)
            details[node.id] = export_brain_node_detail_json(detail)
        except (ValueError, KeyError):
            details[node.id] = {"title": node.type, "id": node.id}

    return {
        "version": 1,
        "graph": brain_json,
        "details": details,
    }


def _build_events_json(job: Any) -> dict[str, Any]:
    """Build safe events timeline."""

    events = _load_events(job)
    safe_events = []
    for e in events[-100:]:
        safe_events.append({
            "event": e.get("event", ""),
            "timestamp": e.get("timestamp", ""),
            "outcome": e.get("outcome", ""),
        })
    return {"version": 1, "events": safe_events, "total": len(events)}


def _build_readiness_json(job: Any) -> dict[str, Any]:
    """Build safe readiness payload from autonomy_readiness module."""
    try:
        from packages.orchestration.autonomy_readiness import (
            assess_job_readiness,
            export_readiness_json,
        )

        events = _load_events(job)
        report = assess_job_readiness(job, events)
        return export_readiness_json(report)
    except (ImportError, OSError, ValueError) as exc:
        return {"version": 2, "error": f"readiness unavailable: {type(exc).__name__}"}


def _build_guide_json(job: Any) -> dict[str, Any]:
    """Build safe guidance payload."""
    try:
        from packages.orchestration.guidance import (
            build_guidance_cards,
            export_guidance_json,
        )

        events = _load_events(job)
        cards = build_guidance_cards(job, events)
        return export_guidance_json(job, cards)
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {
            "version": 1, "cards": [],
            "error": "guidance unavailable",
            "degraded": True, "error_kind": "guidance_build_failed", "source": "server",
        }


def _build_brain_view_model_json(job: Any) -> dict[str, Any]:
    """Build semantic zoom view-model for the PixiJS brain canvas."""
    from packages.orchestration.ui_view_model import build_brain_view_model
    events = _load_events(job)
    return build_brain_view_model(job, events)


def _build_story_json(job: Any) -> dict[str, Any]:
    """Build human story model — Step 164."""
    from packages.orchestration.ui_view_model import build_story
    events = _load_events(job)
    return build_story(job, events)


def _build_human_node_detail_json(job: Any, node_id: str) -> dict[str, Any]:
    """Build human-only node detail — Step 165."""
    from packages.orchestration.ui_view_model import build_human_node_detail
    events = _load_events(job)
    return build_human_node_detail(job, events, node_id)


def _build_layers_json() -> dict[str, Any]:
    """Build layer definitions — Step 167."""
    from packages.orchestration.ui_view_model import build_layers
    return build_layers()


def _build_diagnostics_json(job: Any) -> dict[str, Any]:
    """Build diagnostics-only nodes — Step 167."""
    from packages.orchestration.ui_view_model import build_diagnostics_nodes
    events = _load_events(job)
    return build_diagnostics_nodes(job, events)


def _build_checklist_json(job: Any) -> dict[str, Any]:
    """Build task checklist — Step 168."""
    from packages.orchestration.ui_view_model import build_checklist
    events = _load_events(job)
    return build_checklist(job, events)


def _build_node_detail_json(job: Any, node_id: str) -> dict[str, Any]:
    """Build compact node detail for the floating card."""
    from packages.orchestration.ui_view_model import build_node_detail
    events = _load_events(job)
    return build_node_detail(job, events, node_id)


def _build_live_state_json(job: Any) -> dict[str, Any]:
    """Build live state for polling — lightweight check for UI updates."""
    import hashlib as _hl

    events = _load_events(job)
    state = job.state.value if hasattr(job.state, "value") else str(job.state)

    # Compute view-model hash for change detection
    node_count = len(events)
    raw = f"{job.id}:{state}:{node_count}"
    vm_hash = _hl.md5(raw.encode()).hexdigest()[:12]

    # Latest event
    latest_at = ""
    if events:
        latest_at = events[-1].get("timestamp", "")

    # Cursor = event count
    cursor = str(len(events))

    # Stage detection
    stage = "idle"
    if events:
        last_event = events[-1].get("event", "")
        stage_map = {
            "task_created": "planning",
            "patch_intent_created": "proposing",
            "patch_intent_approved": "approved",
            "patch_intent_applied": "applying",
            "test_run_completed": "testing",
            "proof_collected": "proving",
            "stop_reason_recorded": "stopped",
            "builder_patch_parsed": "parsing",
            "builder_bridge_intent_approved": "approved",
            "builder_bridge_test_completed": "testing",
            "repair_loop_cycle_started": "repairing",
            "repair_loop_succeeded": "proving",
            "repair_loop_stopped": "stopped",
        }
        stage = stage_map.get(last_event, "active")

    # Open decisions
    open_decisions = sum(
        1 for e in events
        if e.get("event") == "human_decision_requested"
        and e.get("outcome") != "resolved"
    )

    # Test status
    test_events = [e for e in events if e.get("event") == "test_run_completed"]
    test_status = "none"
    if test_events:
        last_exit = test_events[-1].get("metadata", {}).get("exit_code")
        test_status = "pass" if last_exit == 0 else "fail"

    # Active/latest completed task
    active_task_id = ""
    latest_completed_task_id = ""
    for t in job.tasks:
        tstat = t.status.value if hasattr(t.status, "value") else str(t.status)
        if tstat == "running":
            active_task_id = str(t.id)
        if tstat == "completed":
            latest_completed_task_id = str(t.id)

    # Repair loop detection
    repair_loop_used = any(
        e.get("event") == "repair_context_created" for e in events
    )

    # Builder bridge pipeline visibility
    bridge_parse_events = [e for e in events if e.get("event") == "builder_patch_parsed"]
    bridge_parse_success = bridge_parse_events[-1].get("metadata", {}).get("parse_success", False) if bridge_parse_events else None
    bridge_parse_error = bridge_parse_events[-1].get("metadata", {}).get("error_kind", "") if bridge_parse_events and not bridge_parse_success else ""

    loop_cycle_events = [e for e in events if e.get("event") == "repair_loop_cycle_started"]
    repair_loop_cycle = loop_cycle_events[-1].get("metadata", {}).get("cycle", 0) if loop_cycle_events else 0
    repair_loop_max = loop_cycle_events[-1].get("metadata", {}).get("max_cycles", 0) if loop_cycle_events else 0

    # Stop reason from latest stop event, parse failure, or test failure
    stop_events = [e for e in events if e.get("event") in ("repair_loop_stopped", "repair_loop_succeeded")]
    bridge_stop_reason = ""
    if stop_events:
        bridge_stop_reason = stop_events[-1].get("metadata", {}).get("reason", "")
    elif bridge_parse_events and not bridge_parse_success:
        last_parse = bridge_parse_events[-1].get("metadata", {})
        bridge_stop_reason = last_parse.get("stop_reason", "") or last_parse.get("error_kind", "")
    else:
        test_events = [e for e in events if e.get("event") == "builder_bridge_test_completed"]
        if test_events and not test_events[-1].get("metadata", {}).get("passed", True):
            bridge_stop_reason = "test_failed_after_apply"

    # Reviewer pending count
    recs = (job.metadata or {}).get("reviewer_recommendations", [])
    reviewer_pending = sum(1 for r in recs if r.get("status") == "pending")

    # Memory candidate count
    candidates = (job.metadata or {}).get("memory_candidates", [])
    memory_candidate_count = len(candidates)

    # Approved memory usage from events
    mem_events = [e for e in events if e.get("event") == "project_memory_recalled"]
    memory_used_count = mem_events[-1].get("metadata", {}).get("item_count", 0) if mem_events else 0

    has_real_events = len(events) > 0

    return {
        "version": 3,
        "job_id": str(job.id),
        "cursor": cursor,
        "stage": stage,
        "running": state in ("active", "running"),
        "latest_event_at": latest_at,
        "node_count": node_count,
        "edge_count": 0,
        "open_decision_count": open_decisions,
        "active_task_id": active_task_id,
        "latest_completed_task_id": latest_completed_task_id,
        "test_status": test_status,
        "token_mode": "compact",
        "view_model_hash": vm_hash,
        "repair_loop_used": repair_loop_used,
        "repair_loop_cycle": repair_loop_cycle,
        "repair_loop_max_cycles": repair_loop_max,
        "builder_patch_parsed": bridge_parse_success,
        "builder_patch_error": bridge_parse_error,
        "stop_reason": bridge_stop_reason,
        "reviewer_pending_count": reviewer_pending,
        "memory_candidate_count": memory_candidate_count,
        "memory_used_count": memory_used_count,
        # Truth contract
        "demo_mode": os.environ.get("REMEDY_UI_DEMO_MODE") == "1",
        "idle": not has_real_events or stage == "idle",
        "stale": not has_real_events,
    }


def _build_task_progress_json(job: Any) -> dict[str, Any]:
    """Build task progress ribbon data."""
    from packages.orchestration.ui_view_model import build_task_progress
    events = _load_events(job)
    return build_task_progress(job, events)


def _build_next_action_json(job: Any) -> dict[str, Any]:
    """Build next-action suggestion."""
    from packages.orchestration.ui_view_model import build_next_action
    events = _load_events(job)
    return build_next_action(job, events)


def _build_events_since_json(job: Any, cursor: str) -> dict[str, Any]:
    """Return safe event summaries since cursor position."""
    events = _load_events(job)
    start = 0
    if cursor.isdigit():
        start = int(cursor)
    new_events = events[start:]
    safe = []
    for e in new_events[:50]:
        safe.append({
            "event": e.get("event", ""),
            "timestamp": e.get("timestamp", ""),
            "outcome": e.get("outcome", ""),
        })
    return {
        "version": 1,
        "job_id": str(job.id),
        "cursor": str(len(events)),
        "events": safe,
    }


def _get_frontend_dist() -> Path | None:
    """Return path to built React frontend dist/ if it exists."""
    dist = Path(__file__).resolve().parent.parent.parent / "apps" / "ui" / "dist"
    index = dist / "index.html"
    if index.is_file():
        return dist
    return None


def _frontend_is_stale() -> bool:
    """Return True if any source file in apps/ui/src/ is newer than dist/index.html."""
    ui_root = Path(__file__).resolve().parent.parent.parent / "apps" / "ui"
    index = ui_root / "dist" / "index.html"
    if not index.is_file():
        return True
    dist_mtime = index.stat().st_mtime
    src_dir = ui_root / "src"
    if not src_dir.is_dir():
        return False
    for f in src_dir.rglob("*"):
        if f.is_file() and f.stat().st_mtime > dist_mtime:
            return True
    return False


def _auto_build_frontend(reason: str = "missing") -> Path | None:
    """Build the React frontend via npm. Returns dist Path or None.

    Runs automatically when dist/ is missing or stale (source newer than build).
    Disable with REMEDY_UI_NO_AUTO_BUILD=1 if you manage builds yourself.
    """
    import subprocess

    if os.environ.get("REMEDY_UI_NO_AUTO_BUILD") == "1":
        return None

    ui_root = Path(__file__).resolve().parent.parent.parent / "apps" / "ui"
    if not (ui_root / "package.json").is_file():
        return None

    print(f"[remedy-ui] auto-build ({reason})…", file=sys.stderr)

    # npm install (skip if node_modules fresh)
    node_modules = ui_root / "node_modules"
    pkg_mtime = (ui_root / "package.json").stat().st_mtime
    need_install = not node_modules.is_dir() or node_modules.stat().st_mtime < pkg_mtime
    if need_install:
        try:
            subprocess.run(
                ["npm", "install", "--no-audit", "--no-fund"],
                cwd=str(ui_root),
                check=True,
                capture_output=True,
                timeout=120,
            )
        except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
            print(f"[remedy-ui] npm install failed: {exc}", file=sys.stderr)
            return None

    # npm run build
    try:
        subprocess.run(
            ["npm", "run", "build"],
            cwd=str(ui_root),
            check=True,
            capture_output=True,
            timeout=120,
        )
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        print(f"[remedy-ui] build failed: {exc}", file=sys.stderr)
        return None

    dist = _get_frontend_dist()
    if dist is not None:
        print("[remedy-ui] build done.", file=sys.stderr)
    return dist


def _load_frontend(job_id: str, token: str) -> str:
    """Load frontend HTML — auto-builds when dist/ is missing or stale.

    Behavior:
      1. If apps/ui/dist/ exists and is fresh → serve it.
      2. If missing or stale (source newer) → auto-build.
      3. If auto-build fails → fail loudly.
      4. Disable auto-build: REMEDY_UI_NO_AUTO_BUILD=1.
    """
    dist = _get_frontend_dist()

    # Auto-build if missing
    if dist is None:
        dist = _auto_build_frontend("dist missing")
    # Auto-build if stale
    elif _frontend_is_stale():
        dist = _auto_build_frontend("source changed")

    if dist is not None:
        html = (dist / "index.html").read_text(encoding="utf-8")
        # Inject job/token as URL params for the React app
        html = html.replace("__JOB_ID__", job_id).replace("__TOKEN__", token)
        return html

    # Legacy fallback — only if explicitly allowed
    if os.environ.get("REMEDY_UI_ALLOW_LEGACY_FALLBACK") == "1":
        print("[remedy-ui] WARNING: serving legacy fallback (REMEDY_UI_ALLOW_LEGACY_FALLBACK=1)",
              file=sys.stderr)
        from packages.orchestration.ui_app_shell import build_app_shell
        return build_app_shell(job_id, token)

    # Fail loudly
    print(
        "\n"
        "ERROR: React UI not built.\n"
        "\n"
        "  To fix, run:\n"
        "    cd apps/ui && npm install && npm run build\n"
        "\n"
        "  Or check npm is installed and retry.\n"
        "  Disable auto-build: REMEDY_UI_NO_AUTO_BUILD=1\n",
        file=sys.stderr,
    )
    sys.exit(1)


def _build_context_budget_json(job: Any) -> dict[str, Any]:
    """Build safe context budget payload."""
    try:
        from packages.orchestration.context_pack import build_context_pack, export_context_pack_json

        events = _load_events(job)
        pack = build_context_pack(job, events, budget=2000, mode="compact")
        data = export_context_pack_json(pack)
        # Strip section content — only return structure
        for s in data.get("sections", []):
            s.pop("content", None)
        return data
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {
            "version": 1,
            "error": "context budget unavailable",
            "degraded": True, "error_kind": "context_budget_build_failed", "source": "server",
        }


# ---------------------------------------------------------------------------
# HTTP Request Handler
# ---------------------------------------------------------------------------

class _RemedyHandler(BaseHTTPRequestHandler):
    """Read-only handler. No POST/PUT/DELETE. Token-gated API."""

    server_token: str = ""
    target_job_id: str = ""
    app_html: str = ""

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        """Suppress default stderr logging."""

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        qs = parse_qs(parsed.query)

        # App shell — no token required
        if path == "/":
            self._send_html(200, self.app_html)
            return

        # Static assets from React dist/ (JS/CSS bundles)
        if path.startswith("/assets/"):
            self._serve_static(path)
            return

        # API routes — token required
        token = (qs.get("token") or [""])[0]
        if token != self.server_token:
            self._send_json(*_safe_error(403, "invalid token"))
            return

        # Route dispatch
        if path == "/api/state":
            job_id = (qs.get("job_id") or [self.target_job_id])[0]
            job, err = _load_job(job_id)
            if err:
                self._send_json(*err)
                return
            self._send_json(200, _build_dashboard(job))
            return

        # /api/jobs/<job_id>/<endpoint>
        parts = path.split("/")
        if len(parts) == 5 and parts[1] == "api" and parts[2] == "jobs":
            job_id_str = parts[3]
            endpoint = parts[4]
            job, err = _load_job(job_id_str)
            if err:
                self._send_json(*err)
                return
            handlers = {
                "dashboard": _build_dashboard,
                "brain": _build_brain_json,
                "brain-view-model": _build_brain_view_model_json,
                "live-state": _build_live_state_json,
                "task-progress": _build_task_progress_json,
                "next-action": _build_next_action_json,
                "guide": _build_guide_json,
                "events": _build_events_json,
                "readiness": _build_readiness_json,
                "context-budget": _build_context_budget_json,
                "story": _build_story_json,
                "checklist": _build_checklist_json,
                "diagnostics": _build_diagnostics_json,
            }
            handler = handlers.get(endpoint)
            if handler:
                self._send_json(200, handler(job))
                return

            # events-since with cursor param
            if endpoint == "events-since":
                cursor = (qs.get("cursor") or ["0"])[0]
                self._send_json(200, _build_events_since_json(job, cursor))
                return

        # /api/layers
        if path == "/api/layers":
            self._send_json(200, _build_layers_json())
            return

        # /api/jobs/<job_id>/nodes/<node_id>/detail
        if (len(parts) == 7 and parts[1] == "api" and parts[2] == "jobs"
                and parts[4] == "nodes" and parts[6] == "detail"):
            job_id_str = parts[3]
            node_id = parts[5]
            job, err = _load_job(job_id_str)
            if err:
                self._send_json(*err)
                return
            self._send_json(200, _build_node_detail_json(job, node_id))
            return

        # /api/jobs/<job_id>/nodes/<node_id>/human-detail (Step 165)
        if (len(parts) == 7 and parts[1] == "api" and parts[2] == "jobs"
                and parts[4] == "nodes" and parts[6] == "human-detail"):
            job_id_str = parts[3]
            node_id = parts[5]
            job, err = _load_job(job_id_str)
            if err:
                self._send_json(*err)
                return
            self._send_json(200, _build_human_node_detail_json(job, node_id))
            return

        # /api/jobs/<job_id>/nodes/<node_id>/debug-detail (Step 165 — advanced)
        if (len(parts) == 7 and parts[1] == "api" and parts[2] == "jobs"
                and parts[4] == "nodes" and parts[6] == "debug-detail"):
            job_id_str = parts[3]
            node_id = parts[5]
            job, err = _load_job(job_id_str)
            if err:
                self._send_json(*err)
                return
            self._send_json(200, _build_node_detail_json(job, node_id))
            return

        self._send_json(*_safe_error(404, "not found"))

    def do_POST(self) -> None:  # noqa: N802
        self._send_json(*_safe_error(405, "method not allowed"))

    def do_PUT(self) -> None:  # noqa: N802
        self._send_json(*_safe_error(405, "method not allowed"))

    def do_DELETE(self) -> None:  # noqa: N802
        self._send_json(*_safe_error(405, "method not allowed"))

    def _send_json(self, code: int, data: dict[str, Any]) -> None:
        body = json.dumps(data, default=str).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, code: int, html: str) -> None:
        body = html.encode()
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    _MIME_TYPES: dict[str, str] = {
        ".js": "application/javascript",
        ".css": "text/css",
        ".svg": "image/svg+xml",
        ".png": "image/png",
        ".woff2": "font/woff2",
        ".json": "application/json",
    }

    def _serve_static(self, url_path: str) -> None:
        """Serve static files from React dist/assets/. Path-traversal safe."""
        dist = _get_frontend_dist()
        if dist is None:
            self._send_json(*_safe_error(404, "not found"))
            return
        # Resolve and ensure within dist/
        try:
            target = (dist / url_path.lstrip("/")).resolve()
            if not str(target).startswith(str(dist.resolve())):
                self._send_json(*_safe_error(403, "forbidden"))
                return
            if not target.is_file():
                self._send_json(*_safe_error(404, "not found"))
                return
        except (ValueError, OSError):
            self._send_json(*_safe_error(404, "not found"))
            return
        suffix = target.suffix.lower()
        content_type = self._MIME_TYPES.get(suffix, "application/octet-stream")
        body = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "public, max-age=31536000, immutable")
        self.end_headers()
        self.wfile.write(body)


# ---------------------------------------------------------------------------
# Server lifecycle
# ---------------------------------------------------------------------------

def start_ui_server(
    job_id: str,
    *,
    host: str = "127.0.0.1",
    port: int = 8787,
    token: str | None = None,
    open_browser: bool = False,
    info_file: str | None = None,
) -> None:
    """Start the read-only UI server. Blocks until Ctrl-C."""
    # Security: refuse non-localhost
    if host not in ("127.0.0.1", "localhost", "::1"):
        print(f"Error: refusing to bind {host} — only 127.0.0.1 allowed", file=sys.stderr)
        sys.exit(1)
    # Normalize to 127.0.0.1
    host = "127.0.0.1"

    # Validate job exists
    job, err = _load_job(job_id)
    if err:
        print(f"Error: {err[1]['error']}", file=sys.stderr)
        sys.exit(1)

    if token is None:
        token = secrets.token_urlsafe(24)

    # Load React frontend (auto-builds if dist/ missing)
    app_html = _load_frontend(job_id, token)

    # Create handler class with bound state
    handler_class = type(
        "_BoundHandler",
        (_RemedyHandler,),
        {
            "server_token": token,
            "target_job_id": job_id,
            "app_html": app_html,
        },
    )

    server = HTTPServer((host, port), handler_class)
    actual_port = server.server_address[1]
    url = f"http://127.0.0.1:{actual_port}/?job={job_id}&token={token}"

    # Write info file
    if info_file:
        info = {
            "version": 1,
            "url": url,
            "host": host,
            "port": actual_port,
            "token": token,
            "job_id": job_id,
            "pid": os.getpid(),
            "started_at": datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        Path(info_file).write_text(json.dumps(info, indent=2))

    print(f"\nRemedy UI: {url}\n")
    print(f"Press Ctrl-C to stop.\n")

    # Optional browser open
    if open_browser:
        _try_open_browser(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def _try_open_browser(url: str) -> None:
    """Best-effort platform opener. Failure does not raise."""
    import platform
    import subprocess

    system = platform.system()
    try:
        if system == "Darwin":
            subprocess.Popen(["open", url])
        elif system == "Linux":
            subprocess.Popen(["xdg-open", url])
        elif system == "Windows":
            os.startfile(url)  # type: ignore[attr-defined]
    except (OSError, FileNotFoundError):
        pass
