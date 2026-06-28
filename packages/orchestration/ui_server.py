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
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse
from uuid import UUID

# ---------------------------------------------------------------------------
# Safe data builders (no raw content leaks)
# ---------------------------------------------------------------------------

class _JobPlanTaskAdapter:
    """Minimal adapter so JobPlan tasks look like core Job tasks to the dashboard."""

    def __init__(self, task: Any) -> None:
        self._t = task
        self.id = task.task_id
        self.description = task.title
        status_map = {
            "applied_to_job_workspace": "completed",
            "passed": "completed",
            "blocked": "blocked",
            "failed": "failed",
            "skipped": "pending",
            "pending": "pending",
            "running": "running",
        }
        raw = task.status or "pending"

        class _Status:
            def __init__(self, val: str) -> None:
                self.value = val
            def __str__(self) -> str:
                return self.value

        self.status = _Status(status_map.get(raw, raw))
        self.metadata = {}


class _JobPlanAdapter:
    """Adapter that makes a JobPlan look enough like a core Job for the dashboard."""

    def __init__(self, plan: Any) -> None:
        self._plan = plan
        self.id = plan.job_id
        self.name = plan.job_title

        class _State:
            def __init__(self, val: str) -> None:
                self.value = val
            def __str__(self) -> str:
                return self.value

        state_map = {
            "completed": "completed",
            "blocked": "blocked",
            "running": "running",
            "planned": "active",
            "paused": "blocked",
        }
        self.state = _State(state_map.get(plan.status, plan.status))
        self.tasks = [_JobPlanTaskAdapter(t) for t in plan.tasks]
        self.artifacts = []
        self.metadata = {"source": "job_plan", "job_plan_id": plan.job_id}
        self._is_job_plan = True


def _load_events(job: Any) -> list[dict[str, Any]]:
    """Load run-log events for a job."""
    if getattr(job, "_is_job_plan", False):
        return _load_job_plan_events(job)
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.timeline import load_run_events
    return load_run_events(resolve_data_root(), job.id)


def _load_job_plan_events(job: Any) -> list[dict[str, Any]]:
    """Load agent run trace events as dashboard events for a JobPlan."""
    from packages.orchestration.agent_run_trace import load_trace_jsonl

    plan = job._plan
    events: list[dict[str, Any]] = []

    # Try to load agent_run_trace from evidence directories
    for evidence_dir_name in [f"remedy-job-evidence-{plan.job_id}"]:
        trace_path = Path(evidence_dir_name) / "agent_run_trace.jsonl"
        if trace_path.exists():
            for te in load_trace_jsonl(trace_path):
                events.append({
                    "event": te.get("event_kind", ""),
                    "timestamp": te.get("created_at", ""),
                    "metadata": {
                        "task_id": te.get("task_id", ""),
                        "run_id": te.get("run_id", ""),
                        "verdict": te.get("verdict", ""),
                        "status": te.get("status", ""),
                    },
                })
            break

    return events


def _safe_error(code: int, message: str) -> tuple[int, dict[str, Any]]:
    return code, {"error": message}


def _load_job(job_id_str: str) -> Any:
    """Load a Job by UUID or JobPlan hex ID, return (job, error_tuple)."""
    import re

    uuid_was_valid = False
    # Try core UUID job first
    try:
        job_id = UUID(job_id_str)
        uuid_was_valid = True
        from packages.orchestration.storage import JobNotFoundError, JobStoreError, load_job
        job = load_job(job_id)
        return job, None
    except ValueError:
        pass
    except (FileNotFoundError, ImportError, JobNotFoundError, JobStoreError):
        pass

    # Valid UUID that wasn't found — 404 not 400
    if uuid_was_valid:
        return None, _safe_error(404, "job not found")

    # Try job-flow JobPlan short hex ID (must look like hex)
    if re.fullmatch(r"[0-9a-fA-F]+", job_id_str):
        try:
            from packages.orchestration.pingpong_job import load_job_plan
            plan = load_job_plan(job_id_str)
            if plan is not None:
                return _JobPlanAdapter(plan), None
        except (ImportError, OSError):
            pass
        return None, _safe_error(404, "job not found")

    return None, _safe_error(400, "invalid job id")


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
    """Derive cycle-aware timeline events from the event ledger.

    Only real ledger events. No task fallback. No raw content.
    Cycle increments each time a build-phase event follows a test/review event.
    """
    _event_map: dict[str, tuple[str, str, str]] = {
        # event_type: (kind, phase, safe_title)
        "task_created": ("llm_action", "planning", "Task created"),
        "patch_intent_created": ("llm_action", "build", "Change proposed"),
        "patch_intent_approved": ("llm_action", "build", "Change approved"),
        "patch_intent_applied": ("llm_action", "build", "Change applied"),
        "test_run_completed": ("test", "test", "Tests run"),
        "proof_collected": ("review", "review", "Proof collected"),
        "human_decision_requested": ("review", "review", "Decision requested"),
    }
    result: list[dict[str, Any]] = []
    cycle = 1
    last_phase = ""
    for idx, e in enumerate(events):
        ev = e.get("event", "")
        mapped = _event_map.get(ev)
        if mapped is None:
            continue
        kind, phase, safe_title = mapped
        # Cycle increments when build-phase event follows test/review
        if phase in ("planning", "build") and last_phase in ("test", "review"):
            cycle += 1
        last_phase = phase
        ts = e.get("timestamp", "")
        time_label = ts[:16].replace("T", " ") if ts else ""
        result.append({
            "id": f"te-{idx}",
            "kind": kind,
            "phase": phase,
            "title": safe_title,
            "state": "done",
            "cycle": cycle,
            "time_label": time_label if time_label else None,
        })
    return result


def _resolve_dashboard_data_dir() -> Path | None:
    """Resolve the data root for authoritative truth, or None if unavailable.

    None means snapshot/proof/continuation truth must be reported as "unknown"
    rather than faked as zero.
    """
    try:
        from packages.orchestration.data_paths import resolve_data_root
        root = resolve_data_root()
        return Path(root) if root is not None else None
    except (ImportError, OSError, ValueError, TypeError):
        return None


def _test_exit_state(meta: dict[str, Any]) -> str:
    """Classify a test_run_completed event: 'pass' | 'fail' | 'none'.

    A missing or non-integer exit_code is 'none' (uncounted) — never folded into
    failures, so a real pass is never mislabeled.
    """
    code = meta.get("exit_code")
    if code == 0:
        return "pass"
    if isinstance(code, int):
        return "fail"
    return "none"


def _build_metrics_tests(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Safe test counters from the event ledger. Counts only, no output."""
    test_events = [e for e in events if e.get("event") == "test_run_completed"]
    runs = len(test_events)
    states = [_test_exit_state(e.get("metadata", {})) for e in test_events]
    passed = sum(1 for s in states if s == "pass")
    failed = sum(1 for s in states if s == "fail")
    latest_state = states[-1] if states else "none"
    return {"runs": runs, "passed": passed, "failed": failed, "latest_state": latest_state}


def _safe_build_proof_chain(job: Any, events: list[dict[str, Any]], data_dir: Path | None) -> Any:
    """Build the authoritative proof chain, or None when unavailable.

    The proof chain consults `build_snapshot_truth` (durable apply records +
    verified manifest/blobs) when *data_dir* is provided, so proof/apply state is
    authoritative — never derived from event presence. None means "unknown".
    """
    if data_dir is None:
        return None
    try:
        from packages.orchestration.proof_chain import build_proof_chain
        return build_proof_chain(job, events, data_dir=data_dir)
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return None


def _metrics_proof_from_chain(chain: Any) -> dict[str, Any]:
    """Safe proof counters from a prebuilt authoritative proof chain.

    Counts only (total changes vs verified). "unknown" when the chain is None.
    """
    if chain is None:
        return {"total_changes": "unknown", "verified": "unknown", "state": "unknown"}
    try:
        from packages.orchestration.proof_chain import PROOF_VERIFIED
        total = len(chain.changes)
        verified = sum(1 for c in chain.changes if c.proof_status == PROOF_VERIFIED)
        if total == 0:
            state = "none"
        elif verified == total:
            state = "verified"
        elif verified > 0:
            state = "partial"
        else:
            state = "none"
        return {"total_changes": total, "verified": verified, "state": state}
    except (ImportError, AttributeError, TypeError):
        return {"total_changes": "unknown", "verified": "unknown", "state": "unknown"}


def _task_truth_maps(chain: Any) -> tuple[dict[str, str], dict[str, str]]:
    """Authoritative per-task proof + apply labels from the proof chain.

    Returns (proof_by_task, apply_by_task). A task is "verified" only when every
    applicable change for that task is verified (fail-closed). Apply state comes
    from the durable apply record, never inferred from changed-file counts. When
    the chain is None both maps are empty (caller reports "unknown").
    """
    proof_by_task: dict[str, str] = {}
    apply_by_task: dict[str, str] = {}
    if chain is None:
        return proof_by_task, apply_by_task
    try:
        from packages.orchestration.proof_chain import PROOF_FAILED, PROOF_NOT_APPLICABLE, PROOF_VERIFIED
        grouped: dict[str, list[Any]] = {}
        for c in chain.changes:
            tid = getattr(c, "task_id", "") or ""
            if not tid:
                continue
            grouped.setdefault(tid, []).append(c)
        for tid, changes in grouped.items():
            proofs = [c.proof_status for c in changes]
            if any(p == PROOF_FAILED for p in proofs):
                proof_by_task[tid] = "failed"
            else:
                applicable = [p for p in proofs if p != PROOF_NOT_APPLICABLE]
                if applicable and all(p == PROOF_VERIFIED for p in applicable):
                    proof_by_task[tid] = "verified"
                elif not applicable:
                    proof_by_task[tid] = "not_applicable"
                else:
                    proof_by_task[tid] = "incomplete"
            apply_states = [getattr(c, "apply_state", "") for c in changes]
            if "applied" in apply_states:
                apply_by_task[tid] = "applied"
            elif "reverted" in apply_states:
                apply_by_task[tid] = "reverted"
            else:
                apply_by_task[tid] = "not_applied"
    except (ImportError, AttributeError, TypeError):
        return {}, {}
    return proof_by_task, apply_by_task


def _build_test_execution_section(job: Any) -> dict[str, Any]:
    """Safe read-only Real Test Execution v1 cockpit summary (Step 1892). Latest test status + run id
    + failure artifact only. No raw output, no mutation, no fake live."""
    try:
        from packages.orchestration.real_test_execution import list_test_runs
        runs = list_test_runs(str(job.id))
        latest = runs[-1] if runs else None
        return {
            "latest_test_status": (latest or {}).get("status", "none"),
            "latest_test_run_id": (latest or {}).get("test_run_id", ""),
            "failure_artifact_id": (latest or {}).get("failure_artifact_id", ""),
            "test_run_count": len(runs),
            "next_safe_action": (f"remedy test result {(latest or {}).get('test_run_id')} --json"
                                 if latest else f"remedy test run {str(job.id)} --json"),
            "live": False, "source": "real_test_execution",
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"latest_test_status": "none", "latest_test_run_id": "", "failure_artifact_id": "",
                "test_run_count": "unknown", "next_safe_action": "", "live": False,
                "source": "unavailable"}


def _build_snapshot_rollback_section(job: Any) -> dict[str, Any]:
    """Safe read-only Snapshot/Rollback Proof v1 cockpit summary (Step 1892). Honest restore flags;
    no fake rollback-ready; no mutation; no raw data."""
    try:
        from packages.orchestration.real_test_execution import (
            list_rollback_proofs,
            list_snapshot_proofs,
        )
        snaps = list_snapshot_proofs(job_id=str(job.id))
        rbs = list_rollback_proofs(job_id=str(job.id))
        return {
            "snapshot_recorded": bool(snaps),
            "snapshot_proof_count": len(snaps),
            "restore_available": any(r.get("restore_available") for r in rbs),
            "restore_tested": False,
            "rollback_proof_count": len(rbs),
            "next_safe_action": f"remedy snapshot create {str(job.id)} --json",
            "live": False, "source": "real_test_execution",
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"snapshot_recorded": False, "restore_available": False, "restore_tested": False,
                "next_safe_action": "", "live": False, "source": "unavailable"}


def _build_repair_loop_section(job: Any) -> dict[str, Any]:
    """Safe read-only Token-Aware Repair Loop v1/v2 cockpit summary (Step 1935). Counts/status/IDs +
    next safe action only; no mutation buttons; no fake live repair; no raw/private data."""
    try:
        from packages.orchestration.repair_loop_v2 import (
            list_repair_attempts,
            list_repair_work_items,
            load_latest_repair_evaluation,
        )
        items = list_repair_work_items(job_id=str(job.id))
        open_count = sum(1 for i in items if i.get("status") not in ("repaired", "abandoned"))
        blocked = sum(1 for i in items if i.get("status") in ("blocked", "abandoned"))
        latest = items[-1] if items else {}
        latest_id = latest.get("repair_id", "")
        attempts = list_repair_attempts(latest_id, str(job.id)) if latest_id else []
        ev = (load_latest_repair_evaluation(latest_id) or {}) if latest_id else {}
        token_band = attempts[-1].get("token_estimate_band", "unknown") if attempts else "unknown"
        route = attempts[-1].get("route_id", "") if attempts else ""
        retest = attempts[-1].get("retest_status", "unknown") if attempts else "unknown"
        return {
            "open_repair_count": open_count,
            "blocked_repair_count": blocked,
            "latest_status": latest.get("status", "none"),
            "latest_repair_id": latest_id,
            "token_band": token_band,
            "route_recommendation": route,
            "retest_status": retest,
            "user_decision_required": bool(blocked) or latest.get("status") == "abandoned",
            "next_safe_action": (ev.get("required_next_actions", []) or
                                 [f"remedy repair item-list {str(job.id)} --json"])[0],
            "live": False, "source": "repair_loop_v2",
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"open_repair_count": 0, "blocked_repair_count": 0, "latest_status": "none",
                "user_decision_required": False, "next_safe_action": "", "live": False,
                "source": "unavailable"}


def _build_main_builder_adapter_section(job: Any) -> dict[str, Any]:
    """Safe read-only Main Builder Adapter v0 cockpit summary (Step 1993). Counts/status + next safe
    action only; no mutation buttons; no fake live builder; no raw/private data."""
    try:
        from packages.orchestration.main_builder_adapter import (
            list_builder_adapter_specs,
            list_builder_sessions,
        )
        specs = list_builder_adapter_specs()
        sessions = list_builder_sessions(str(job.id))
        enabled = sum(1 for s in specs if s.get("enabled", False))
        latest = sessions[-1] if sessions else {}
        blocked = sum(1 for s in sessions if s.get("status") == "blocked")
        pkg_ready = sum(1 for s in sessions if s.get("status") in ("package_ready", "waiting_for_operator"))
        candidate = sum(1 for s in sessions if s.get("status") == "candidate_received")
        intake = sum(1 for s in sessions if s.get("status") == "completed_intake_only")
        running = sum(1 for s in sessions if s.get("status") == "running")
        return {
            "enabled_adapter_count": enabled,
            "latest_session_status": latest.get("status", "none"),
            "latest_adapter_kind": latest.get("adapter_id", ""),
            "package_ready_count": pkg_ready,
            "blocked_session_count": blocked,
            "candidate_intake_status": "candidate_received" if candidate else (
                "intake_complete" if intake else "none"),
            "token_warning": "",
            "next_safe_action": latest.get("next_safe_action", ""),
            "live": bool(running),
            "source": "main_builder_adapter",
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"enabled_adapter_count": 0, "latest_session_status": "none",
                "blocked_session_count": 0, "next_safe_action": "", "live": False,
                "source": "unavailable"}


def _build_managed_execution_section(job: Any) -> dict[str, Any]:
    """Safe read-only Managed Builder Execution v1.1 cockpit summary. Counts/status/approval state +
    next safe action only; no mutation buttons; no raw output; no fake live execution."""
    try:
        from packages.orchestration.managed_builder_execution import (
            list_command_templates,
            list_execution_approvals,
            list_execution_results,
        )
        templates = list_command_templates()
        results = list_execution_results(str(job.id))
        approvals = list_execution_approvals()
        enabled = sum(1 for t in templates if t.get("enabled", False))
        latest = results[-1] if results else {}
        running = sum(1 for r in results if r.get("status") == "running")
        completed = sum(1 for r in results if r.get("status") == "completed")
        failed = sum(1 for r in results if r.get("status") == "failed")
        blocked = sum(1 for r in results if r.get("status") in ("blocked", "approval_required"))
        # v1.1: approval state.
        active_approvals = 0
        for a in approvals:
            max_runs = int(a.get("max_runs", 0))
            used = int(a.get("used_count", 0))
            if max_runs <= 0 or used < max_runs:
                active_approvals += 1
        return {
            "enabled_template_count": enabled,
            "execution_count": len(results),
            "completed_count": completed,
            "failed_count": failed,
            "blocked_count": blocked,
            "approval_count": len(approvals),
            "active_approval_count": active_approvals,
            "latest_status": latest.get("status", "none"),
            "next_safe_action": latest.get("next_safe_action", ""),
            "live": bool(running),
            "source": "managed_builder_execution",
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"enabled_template_count": 0, "execution_count": 0,
                "latest_status": "none", "next_safe_action": "", "live": False,
                "source": "unavailable"}


def _build_snapshot_section(job: Any, data_dir: Path | None) -> dict[str, Any]:
    """Safe snapshot/apply-record summary from the authoritative builder.

    Aggregate counts and bools only — no snapshot blobs, paths, hashes, or IDs.
    Returns "unknown" values when the data root or durable records are unavailable.
    """
    unknown = {
        "apply_records": "unknown", "verified": "unknown",
        "reverted": "unknown", "drift_detected": "unknown",
        "source": "unavailable",
    }
    if data_dir is None:
        return unknown
    try:
        from packages.orchestration.repository_snapshot import (
            build_snapshot_truth,
            list_durable_apply_ids,
        )
        apply_ids = list_durable_apply_ids(str(job.id), data_dir)
        verified = 0
        reverted = 0
        drift = False
        for aid in apply_ids:
            truth = build_snapshot_truth(str(job.id), apply_id=aid, data_dir=data_dir)
            if (truth.apply_state == "applied"
                    and truth.snapshot_verified_now
                    and truth.recovery_material_available
                    and truth.evidence_status == "complete"):
                verified += 1
            if truth.revert_state in ("reverted",):
                reverted += 1
            if truth.drift_blocked:
                drift = True
        return {
            "apply_records": len(apply_ids),
            "verified": verified,
            "reverted": reverted,
            "drift_detected": drift,
            "source": "durable_apply_records",
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return unknown


def _build_continuation_section(
    job: Any, events: list[dict[str, Any]], data_dir: Path | None,
) -> dict[str, Any]:
    """Safe continuation summary from do_continue events + approved intents.

    available: eligibility-light — at least one approved patch intent exists.
    last_result / last_stop_reason: from the most recent do_continue_stopped
    event metadata (safe enum labels only — no raw content).
    """
    unknown = {"available": "unknown", "last_result": "unknown", "last_stop_reason": "unknown"}
    if data_dir is None:
        return unknown
    # available — light approved-intent check (not the full eligibility gate)
    available = False
    try:
        from packages.orchestration.approval_queue import (
            APPROVAL_APPROVED,
            list_patch_intents,
        )
        intents = list_patch_intents(job)
        available = any(i.get("state") == APPROVAL_APPROVED for i in intents)
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        available = False

    # last result — most recent do_continue_stopped event
    _RESULT_REASONS = {
        "completed_verified", "test_failed_repair_available", "evidence_incomplete",
    }
    last_result = "none"
    last_stop_reason = "none"
    stopped = [e for e in events if e.get("event") == "do_continue_stopped"]
    if stopped:
        reason = str(stopped[-1].get("metadata", {}).get("stop_reason", ""))
        last_stop_reason = reason or "none"
        last_result = reason if reason in _RESULT_REASONS else "none"
    return {
        "available": available,
        "last_result": last_result,
        "last_stop_reason": last_stop_reason,
    }


def _build_repair_section(job: Any) -> dict[str, Any]:
    """Safe read-only Repair Loop v1 summary for the cockpit (Step 1210).

    Counts + safe statuses only — no failure output, no patch body, no source.
    No mutation affordance: a pending approval surfaces a copyable CLI command,
    never an Approve button.
    """
    attempts = (job.metadata or {}).get("repair_attempts_v1", {})
    attempt_count = 0
    pending_approval = 0
    applied_count = 0
    tested_passed_count = 0
    tested_failed_count = 0
    resolved_failure_count = 0
    pending_intent_id = ""
    if isinstance(attempts, dict):
        for v in attempts.values():
            if not isinstance(v, dict):
                continue
            attempt_count += 1
            status = v.get("status")
            if status == "approval_required":
                pending_approval += 1
                if not pending_intent_id and v.get("repair_intent_id"):
                    pending_intent_id = str(v.get("repair_intent_id"))
            if status in ("applied", "tested_passed", "tested_failed"):
                applied_count += 1
            if status == "tested_passed":
                tested_passed_count += 1
            if status == "tested_failed":
                tested_failed_count += 1
            if v.get("resolved_failure"):
                resolved_failure_count += 1
    next_action = ""
    if pending_intent_id:
        next_action = f"remedy patch approve {job.id} {pending_intent_id}"
    return {
        "attempt_count": attempt_count,
        "pending_approval_count": pending_approval,
        "applied_count": applied_count,
        "tested_passed_count": tested_passed_count,
        "tested_failed_count": tested_failed_count,
        "resolved_failure_count": resolved_failure_count,
        "next_safe_action": next_action,
        "source": "repair_attempts_v1",
    }


def _build_overnight_section(job: Any, data_dir: Path | None) -> dict[str, Any]:
    """Safe read-only Bounded Overnight Prep summary for the cockpit (Step 1262).

    Readiness state + counts + next-action label only — no mutation, no buttons,
    no fabricated "ready". "unknown" when the data root or builder is unavailable.
    """
    unknown = {"readiness_level": "unknown", "ready": "unknown",
               "can_run_unattended": "unknown", "blocker_count": "unknown",
               "next_action_label": "", "checklist_done": "unknown",
               "checklist_total": "unknown", "source": "unavailable"}
    if data_dir is None:
        return unknown
    try:
        from packages.orchestration.overnight_readiness import (
            build_overnight_readiness,
            export_readiness_json,
        )
        d = export_readiness_json(build_overnight_readiness(str(job.id), data_dir))
        checklist = d.get("checklist", [])
        na = d.get("next_action")
        return {
            "readiness_level": d.get("readiness_level"),
            "ready": d.get("ready"),
            "can_run_unattended": d.get("can_run_unattended"),
            "blocker_count": len(d.get("blockers", [])),
            "next_action_label": na["label"] if na else "",
            "checklist_done": sum(1 for i in checklist if i["status"] == "done"),
            "checklist_total": len(checklist),
            "source": "overnight_readiness",
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return unknown


def _build_overnight_run_section(job: Any, data_dir: Path | None) -> dict[str, Any]:
    """Safe read-only Bounded Overnight Executor run summary for the cockpit (Step
    1292).

    Latest run status + stop reason + selected-action label + checkpoint count +
    morning-report availability. Read-only: no buttons, no mutation, no fabricated
    running state. "none"/"unknown" when no run or the data root is unavailable.
    """
    unknown = {"run_count": "unknown", "latest_status": "unknown",
               "selected_action": "", "executed_action": "", "stop_reason": "",
               "checkpoint_count": "unknown", "report_available": "unknown",
               "source": "unavailable"}
    if data_dir is None:
        return unknown
    try:
        from packages.orchestration.overnight_executor import (
            latest_run_record,
            list_run_records,
        )
        records = list_run_records(str(job.id), data_dir)
        latest = latest_run_record(str(job.id), data_dir)
        if not latest:
            return {"run_count": 0, "latest_status": "none", "selected_action": "",
                    "executed_action": "", "stop_reason": "", "checkpoint_count": 0,
                    "report_available": False, "source": "overnight_executor"}
        return {
            "run_count": len(records),
            "latest_status": latest.get("stop_reason", ""),
            "mode": latest.get("mode", ""),
            "selected_action": (latest.get("selected_action") or {}).get("kind", ""),
            "executed_action": (latest.get("executed_action") or {}).get("kind", ""),
            "stop_reason": latest.get("stop_reason", ""),
            "evidence_status": latest.get("evidence_status", ""),
            "checkpoint_count": len(latest.get("checkpoints", [])),
            "report_available": bool(latest.get("run_id")),
            "source": "overnight_executor",
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return unknown


def _build_provider_trust_section(job: Any) -> dict[str, Any]:
    """Safe read-only Provider Trust Gate summary for the cockpit (Step 1325).

    Counts only (reports / accepted / rejected / needs_review / pending intents).
    No buttons, no provider execution, no mutation, no raw output."""
    try:
        from packages.orchestration.provider_trust import load_trust_reports
        reports = list(load_trust_reports(job).values())
        accepted = sum(1 for r in reports if r.get("trust_status") == "accepted")
        rejected = sum(1 for r in reports if r.get("trust_status") == "rejected")
        needs = sum(1 for r in reports if r.get("trust_status") == "needs_human_review")
        pending = sum(1 for r in reports
                      if r.get("trust_status") == "accepted" and r.get("repair_intent_id"))
        materialized = failed = 0
        try:
            from packages.orchestration.provider_patch_material import load_materials
            mats = list(load_materials(job).values())
            materialized = sum(1 for m in mats if m.get("material_state") == "materialized")
            failed = sum(1 for m in mats if m.get("material_state") == "materialization_failed")
        except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
            materialized = failed = 0
        return {
            "report_count": len(reports),
            "accepted": accepted,
            "rejected": rejected,
            "needs_review": needs,
            "pending_provider_repair_approval": pending,
            "materialized_count": materialized,
            "materialization_failed_count": failed,
            "source": "provider_trust",
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"report_count": "unknown", "accepted": "unknown", "rejected": "unknown",
                "needs_review": "unknown", "pending_provider_repair_approval": "unknown",
                "materialized_count": "unknown", "materialization_failed_count": "unknown",
                "source": "unavailable"}


def _build_external_builder_section(job: Any) -> dict[str, Any]:
    """Safe read-only External Builder Sandbox v0 summary for the cockpit (Step 1693).

    Counts + latest state only. No buttons, no mutation, no "run external builder", no raw.
    LIVE only with real running evidence — in this block normally false (ingress only)."""
    try:
        from packages.orchestration.external_builder_sandbox import (
            load_external_packages,
            load_external_submissions,
        )
        pkgs = load_external_packages(job_id=str(job.id))
        subs = load_external_submissions(job_id=str(job.id))
        latest = subs[-1] if subs else None
        return {
            "external_packages": len(pkgs),
            "external_submissions": len(subs),
            "pending_external_reviews": sum(1 for s in subs if s.get("state") == "needs_review"),
            "rejected_external_candidates": sum(
                1 for s in subs if s.get("state") in ("trust_rejected", "verification_rejected")),
            "verified_external_candidates": sum(1 for s in subs if s.get("state") == "pending_approval"),
            "latest_state": (latest or {}).get("state", ""),
            "live": False,
            "source": "external_builder",
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"external_packages": "unknown", "external_submissions": "unknown",
                "pending_external_reviews": "unknown", "rejected_external_candidates": "unknown",
                "verified_external_candidates": "unknown", "latest_state": "", "live": False,
                "source": "unavailable"}


def _build_token_economy_section(job: Any) -> dict[str, Any]:
    """Safe read-only Token Economy + Context Budget v0 summary for the cockpit (Step 1770).

    Estimated bands + budget status + context pack recommendation + warning count only. No mutation
    buttons, no fake provider readiness, no raw context, no exact pricing, no "savings verified"
    claim. LIVE is always false — estimates + metadata only."""
    try:
        from packages.orchestration.token_economy import token_economy_report
        rep = token_economy_report(str(job.id))
        est = rep.get("context_budget_estimate", {}) or {}
        pack = rep.get("context_pack_recommendation", {}) or {}
        decision = rep.get("decision", {}) or {}
        from packages.orchestration.worker_registry import get_worker_spec, is_placeholder
        oll = get_worker_spec("ollama.placeholder")
        return {
            "budget_status": decision.get("budget_status", "unknown_budget"),
            "estimated_token_band": decision.get("estimated_token_band", "unknown"),
            "estimated_context_tokens": est.get("estimated_input_tokens", 0),
            "context_pack_recommendation": pack.get("recommended_pack_kind", ""),
            "estimated_token_savings_band": (pack.get("estimated_token_savings", {}) or {}).get("band", "unknown"),
            "local_first_recommended": (decision.get("estimated_cost_band") in ("free", "cheap")
                                        and not decision.get("requires_human_approval")),
            "ollama_placeholder_available": bool(oll is not None and is_placeholder(oll)),
            "requires_human_approval": decision.get("requires_human_approval", True),
            "warning_count": len(est.get("warnings", [])),
            "next_safe_action": decision.get("next_safe_action", ""),
            "live": False,
            "source": "token_economy",
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"budget_status": "unknown_budget", "estimated_token_band": "unknown",
                "estimated_context_tokens": "unknown", "context_pack_recommendation": "",
                "estimated_token_savings_band": "unknown", "local_first_recommended": False,
                "ollama_placeholder_available": "unknown", "requires_human_approval": True,
                "warning_count": "unknown", "next_safe_action": "", "live": False,
                "source": "unavailable"}


def _build_overnight_mission_section(job: Any) -> dict[str, Any]:
    """Safe read-only Overnight Mission Contract v0 summary for the cockpit (Step 1849).

    Status + satisfied + open finding/gate counts + required next actions + optional ideas + next
    safe action only. No mutation buttons, no fake live overnight run, no raw/private data. LIVE is
    false unless real active evidence exists — in this metadata-only block it stays false."""
    try:
        from packages.orchestration.overnight_mission import (
            _contract_from_dict,
            evaluate_mission_contract,
            list_mission_contracts,
        )
        contracts = list_mission_contracts(job_id=str(job.id))
        if not contracts:
            return {"status": "not_started", "satisfied": False, "open_findings_count": 0,
                    "missing_gates_count": 0, "required_next_actions": [], "optional_next_ideas": [],
                    "user_decision_required": False,
                    "next_safe_action": f"remedy overnight contract-create {str(job.id)} --json",
                    "live": False, "source": "overnight_mission"}
        ev = evaluate_mission_contract(_contract_from_dict(contracts[-1]), persist=False)
        return {
            "status": ev.status,
            "satisfied": ev.satisfied,
            "open_findings_count": ev.open_review_findings,
            "missing_gates_count": len(ev.missing_proofs),
            "required_next_actions": [a.get("command") for a in ev.required_next_actions],
            "optional_next_ideas": [i.get("title") for i in ev.optional_next_ideas],
            "user_decision_required": ev.user_decision_required,
            "next_safe_action": (ev.next_safe_actions or [""])[0],
            "live": False,
            "source": "overnight_mission",
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"status": "not_started", "satisfied": False, "open_findings_count": "unknown",
                "missing_gates_count": "unknown", "required_next_actions": [], "optional_next_ideas": [],
                "user_decision_required": False, "next_safe_action": "", "live": False,
                "source": "unavailable"}


def _build_model_route_tournament_section(job: Any) -> dict[str, Any]:
    """Safe read-only Model/Route Tournament v0 summary for the cockpit (Step 1811).

    Latest status + competitor count + evidence status + recommended route + confidence + warning
    count + next action only. No mutation buttons, no fake live tournament, no raw data, no provider
    readiness claim. LIVE is always false — evidence/reporting only."""
    try:
        from packages.orchestration.model_route_tournament import generate_tournament_report
        rep = generate_tournament_report(str(job.id), persist=False)
        d = rep.to_dict()
        winner = next((c for c in d.get("competitors", [])
                       if c.get("competitor_id") == d.get("winner_competitor_id")), None)
        ev_status = "complete" if any(
            e.get("evidence_status") == "complete" for e in d.get("evidence", [])) else (
            "partial" if any(e.get("evidence_status") == "partial" for e in d.get("evidence", []))
            else "insufficient_evidence")
        return {
            "latest_status": d.get("status"),
            "competitor_count": len(d.get("competitors", [])),
            "evidence_status": ev_status,
            "recommended_route": (winner or {}).get("worker_id", ""),
            "confidence": d.get("confidence"),
            "warning_count": len(d.get("warnings", [])),
            "next_safe_action": (d.get("next_safe_actions") or [""])[0],
            "live": False,
            "source": "model_route_tournament",
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"latest_status": "insufficient_evidence", "competitor_count": "unknown",
                "evidence_status": "insufficient_evidence", "recommended_route": "",
                "confidence": "low", "warning_count": "unknown", "next_safe_action": "",
                "live": False, "source": "unavailable"}


def _build_worker_registry_section(job: Any) -> dict[str, Any]:
    """Safe read-only Worker Registry + Route Policy v0 summary for the cockpit (Step 1730).

    Counts + active route policy + recommended route only. No buttons, no mutation, no "run worker",
    no fake provider/Ollama status. LIVE is always false — this block is metadata + policy only."""
    try:
        from packages.orchestration.worker_registry import (
            WorkerSelectionRequest,
            evaluate_worker_selection,
            is_placeholder,
            load_route_policy,
            load_worker_registry,
        )
        specs = load_worker_registry()
        policy = load_route_policy(str(job.id))
        selection = evaluate_worker_selection(
            WorkerSelectionRequest(job_id=str(job.id), task_type="repair"), policy=policy,
            registry=specs)
        return {
            "available_workers_count": len(specs),
            "enabled_workers_count": sum(1 for s in specs if s.enabled),
            "placeholder_workers_count": sum(1 for s in specs if is_placeholder(s)),
            "selected_workers": list(policy.user_selected_worker_ids),
            "preferred_workers": list(policy.preferred_worker_ids),
            "blocked_workers": list(policy.blocked_worker_ids),
            "local_first_enabled": policy.prefer_local_for_cheap_tasks,
            "ollama_preference_enabled": policy.prefer_ollama_for_cheap_tasks,
            "max_cost_tier": policy.max_cost_tier,
            "max_risk_tier": policy.max_risk_tier,
            "token_budget_hint": policy.token_budget_hint,
            "recommended_worker_id": selection.recommended_worker_id,
            "requires_human_approval": selection.requires_human_approval,
            "recommended_next_action": selection.next_safe_action,
            "live": False,
            "source": "worker_registry",
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"available_workers_count": "unknown", "selected_workers": [],
                "preferred_workers": [], "blocked_workers": [], "local_first_enabled": "unknown",
                "ollama_preference_enabled": "unknown", "recommended_worker_id": "",
                "recommended_next_action": "", "live": False, "source": "unavailable"}


def _build_candidate_quality_section(job: Any) -> dict[str, Any]:
    """Safe read-only Local Candidate Quality Evaluation v1 summary for the cockpit (Step 1664).

    Status + latest outcome + pending-with-quality + best route + loop-risk counts only.
    No buttons, no mutation, no raw content."""
    try:
        from packages.orchestration.candidate_quality import (
            build_candidate_scorecards,
            load_candidate_quality_evaluations,
        )
        evals = load_candidate_quality_evaluations(job_id=str(job.id))
        latest = evals[-1] if evals else None
        pending = sum(1 for e in evals if e.get("outcome") == "pending_approval")
        loop = sum(1 for e in evals
                   if (e.get("score", {}) or {}).get("dimensions", {}).get("loop_risk") == "fail")
        cards = build_candidate_scorecards(job_id=str(job.id))
        ranked = sorted((cards.get("by_route_tier", {}) or {}).items(),
                        key=lambda kv: kv[1].get("average_score", 0.0), reverse=True)
        return {
            "evaluation_count": len(evals),
            "latest_outcome": (latest or {}).get("outcome", ""),
            "latest_score_band": ((latest or {}).get("score", {}) or {}).get("band", ""),
            "pending_with_quality_count": pending,
            "best_route": ranked[0][0] if ranked else "",
            "loop_risk_count": loop,
            "source": "candidate_quality",
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"evaluation_count": "unknown", "latest_outcome": "", "latest_score_band": "",
                "pending_with_quality_count": "unknown", "best_route": "",
                "loop_risk_count": "unknown", "source": "unavailable"}


def _build_local_candidate_section(job: Any) -> dict[str, Any]:
    """Safe read-only Automated Local Candidate Generator v0 summary for the cockpit (Step 1627).

    Status + latest generation state + pending-approval + trust/verification rejection counts only.
    No buttons, no mutation, no model execution, no raw output."""
    try:
        from packages.orchestration.local_candidate_generator import (
            list_local_candidate_runs,
            load_local_candidate_config,
        )
        cfg = load_local_candidate_config()
        runs = [r for r in list_local_candidate_runs() if r.get("job_id") == str(job.id)]
        latest = runs[-1] if runs else None
        pending = sum(1 for r in runs
                      if r.get("status") == "intent_pending_approval" and r.get("intent_id"))
        return {
            "enabled": cfg.enabled,
            "run_count": len(runs),
            "latest_status": (latest or {}).get("status", ""),
            "pending_approval_count": pending,
            "trust_rejected_count": sum(1 for r in runs if r.get("status") == "trust_rejected"),
            "verification_rejected_count": sum(1 for r in runs if r.get("status") == "verification_rejected"),
            "needs_review_count": sum(1 for r in runs if r.get("status") == "needs_review"),
            "source": "local_candidate",
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"enabled": False, "run_count": "unknown", "latest_status": "",
                "pending_approval_count": "unknown", "trust_rejected_count": "unknown",
                "verification_rejected_count": "unknown", "needs_review_count": "unknown",
                "source": "unavailable"}


def _build_builder_routing_section(job: Any) -> dict[str, Any]:
    """Safe read-only Expensive Builder Routing v0 summary for the cockpit (Step 1595).

    Latest tier + budget/loop status + external-recommended flag + next-action label only.
    No buttons, no mutation, no execution, no raw content."""
    try:
        from packages.orchestration.builder_routing import load_builder_routing_traces
        scope = f"job:{job.id}"
        traces = load_builder_routing_traces(scope=scope)
        latest = traces[-1] if traces else None
        external_recommended = any(
            t.get("selected_tier") == "external_candidate_generator" for t in traces)
        return {
            "routing_decision_count": len(traces),
            "latest_tier": (latest or {}).get("selected_tier", ""),
            "loop_guard_status": (latest or {}).get("loop_guard_status", ""),
            "risk_level": ((latest or {}).get("risk_summary", {}) or {}).get("level", ""),
            "external_builder_recommended": external_recommended,
            "next_safe_action_label": (latest or {}).get("next_safe_action", ""),
            "source": "builder_routing",
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"routing_decision_count": "unknown", "latest_tier": "",
                "loop_guard_status": "", "external_builder_recommended": False,
                "next_safe_action_label": "", "source": "unavailable"}


def _build_provider_verification_section(job: Any) -> dict[str, Any]:
    """Safe read-only Provider Trust Verification v1 summary for the cockpit (Step 1559).

    Counts + latest status only. No buttons, no mutation, no provider execution, no raw."""
    try:
        from packages.orchestration.provider_trust_verification import load_verification_reports
        reports = list(load_verification_reports(job).values())
        passed = sum(1 for r in reports if r.get("decision") == "verification_passed")
        needs = sum(1 for r in reports if r.get("decision") == "needs_human_review")
        rejected = sum(1 for r in reports if r.get("decision") == "verification_rejected")
        incomplete = sum(1 for r in reports if r.get("decision") == "verification_incomplete")
        pending = sum(1 for r in reports
                      if r.get("decision") == "verification_passed" and r.get("allowed_to_create_intent"))
        latest = reports[-1] if reports else None
        return {
            "verification_count": len(reports),
            "passed": passed,
            "needs_review": needs,
            "rejected": rejected,
            "incomplete": incomplete,
            "pending_approval_after_verification": pending,
            "latest_status": (latest or {}).get("verification_status", ""),
            "latest_decision": (latest or {}).get("decision", ""),
            "source": "provider_verification",
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"verification_count": "unknown", "passed": "unknown", "needs_review": "unknown",
                "rejected": "unknown", "incomplete": "unknown",
                "pending_approval_after_verification": "unknown", "latest_status": "",
                "latest_decision": "", "source": "unavailable"}


def _build_repair_request_section(job: Any) -> dict[str, Any]:
    """Safe read-only Repair Request Builder summary for the cockpit (Step 1381).

    Counts + latest target only. No buttons, no mutation, no external execution,
    no raw request content."""
    try:
        from packages.orchestration.provider_patch_material import load_materials
        from packages.orchestration.repair_request_builder import load_request_packages
        packages = list(load_request_packages(job).values())
        materialized = {m.get("failure_artifact_id") for m in load_materials(job).values()
                        if m.get("material_state") == "materialized"}
        pending = sum(1 for p in packages if p.get("failure_artifact_id") not in materialized)
        latest = packages[-1].get("target_kind", "") if packages else "none"
        return {
            "request_package_count": len(packages),
            "pending_response_count": pending,
            "latest_request_target": latest,
            "source": "repair_request_builder",
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"request_package_count": "unknown", "pending_response_count": "unknown",
                "latest_request_target": "unknown", "source": "unavailable"}


def _build_self_dogfood_section(job: Any) -> dict[str, Any]:
    """Safe read-only Self-Dogfood summary for the cockpit (Step 1418). Counts +
    latest status only. No buttons, no mutation, no raw findings."""
    try:
        from packages.orchestration.proposed_tasks import load_proposed_tasks_safe
        tasks, _ = load_proposed_tasks_safe(str(job.id))
        sd = [t for t in tasks if getattr(t, "task_type", "") == "self_dogfood"]
        def _st(t):
            s = getattr(t, "status", "")
            return str(getattr(s, "value", s)).lower()
        high = sum(1 for t in sd if t.priority == "high")
        pending = sum(1 for t in sd if _st(t) in ("proposed", "evaluated"))
        return {
            "self_improvement_item_count": len(sd),
            "high_priority_count": high,
            "pending_evaluation_count": pending,
            "latest_status": (_st(sd[-1]) if sd else "none"),
            "source": "self_dogfood",
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"self_improvement_item_count": "unknown", "high_priority_count": "unknown",
                "pending_evaluation_count": "unknown", "latest_status": "unknown",
                "source": "unavailable"}


def _build_self_execution_section(job: Any) -> dict[str, Any]:
    """Safe read-only Self-Dogfood Execution summary for the cockpit (Step 1445).
    Counts + latest state only. No buttons, no mutation, no raw content."""
    try:
        from packages.orchestration.self_dogfood_execution import list_attempts
        attempts = [a for a in list_attempts() if a.get("job_id") == str(job.id)]
        by_state: dict[str, int] = {}
        for a in attempts:
            by_state[a.get("state", "")] = by_state.get(a.get("state", ""), 0) + 1
        return {
            "attempt_count": len(attempts),
            "pending_candidate_count": by_state.get("awaiting_external_candidate", 0),
            "pending_approval_count": by_state.get("intent_pending_approval", 0),
            "completed_count": by_state.get("completed", 0),
            "latest_state": (attempts[-1].get("state", "") if attempts else "none"),
            "source": "self_dogfood_execution",
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"attempt_count": "unknown", "pending_candidate_count": "unknown",
                "pending_approval_count": "unknown", "completed_count": "unknown",
                "latest_state": "unknown", "source": "unavailable"}


def _build_orchestrator_section(job: Any) -> dict[str, Any]:
    """Safe read-only Orchestrator Brain summary for the cockpit (Step 1484). Latest
    decision only. No buttons, no mutation, no raw content."""
    try:
        from packages.orchestration.orchestrator_brain import list_decisions
        decisions = list_decisions(f"job:{job.id}")
        if not decisions:
            return {"decision_count": 0, "latest_stop_reason": "none", "confidence": "",
                    "next_safe_action": "", "loop_guard_status": "", "model_routing_tier": "",
                    "source": "orchestrator_brain"}
        latest = decisions[-1]
        return {
            "decision_count": len(decisions),
            "latest_stop_reason": latest.get("stop_reason", ""),
            "confidence": latest.get("confidence", ""),
            "next_safe_action": latest.get("next_safe_action", ""),
            "loop_guard_status": latest.get("loop_guard_status", ""),
            "model_routing_tier": (latest.get("model_routing_plan") or {}).get("tier", ""),
            "source": "orchestrator_brain",
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"decision_count": "unknown", "latest_stop_reason": "unknown", "confidence": "unknown",
                "next_safe_action": "", "loop_guard_status": "unknown",
                "model_routing_tier": "unknown", "source": "unavailable"}


def _build_local_advisor_section(job: Any) -> dict[str, Any]:
    """Safe read-only Local Model Advisor summary for the cockpit (Step 1520). Latest
    advisor critique + counts only. No buttons, no mutation, no raw prompt/response."""
    try:
        from packages.orchestration.local_model_advisor import list_local_advisor_runs
        from packages.orchestration.orchestrator_brain import list_decisions
        scope = f"job:{job.id}"
        runs = [r for r in list_local_advisor_runs() if r.get("scope") == scope]
        decisions = list_decisions(scope)
        adv = ((decisions[-1].get("advisor") if decisions else None) or {}) if decisions else {}
        latest = runs[-1] if runs else {}
        return {
            "run_count": len(runs),
            "enabled": bool(adv.get("enabled", False)),
            "available": bool(adv.get("available", False)),
            "latest_status": latest.get("status", "none"),
            "latest_decision_impact": adv.get("decision_impact", latest.get("decision_impact", "")),
            "concern_count": len(adv.get("suggested_concerns", []) or []),
            "model_routing_tier": ((decisions[-1].get("model_routing_plan") or {}).get("tier", "")
                                   if decisions else ""),
            "source": "local_model_advisor",
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"run_count": "unknown", "enabled": "unknown", "available": "unknown",
                "latest_status": "unknown", "source": "unavailable"}


def _build_dashboard(job: Any) -> dict[str, Any]:
    """Build safe dashboard payload for a job."""
    events = _load_events(job)
    truth_data_dir = _resolve_dashboard_data_dir()
    # Authoritative proof chain (durable snapshot truth) — built once, reused for
    # metrics.proof and per-task proof/apply truth. Never event-presence-derived.
    proof_chain = _safe_build_proof_chain(job, events, truth_data_dir)
    task_proof_map, task_apply_map = _task_truth_maps(proof_chain)

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
            # Authoritative proof/apply truth from the proof chain (durable
            # snapshot truth), never from proof_collected event presence. When the
            # data root is unavailable the value is "unknown", never "verified".
            "proof_status": task_proof_map.get(tid, "unknown" if proof_chain is None else "none"),
            "apply_status": task_apply_map.get(tid, "unknown" if proof_chain is None else "not_applied"),
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
    # Finalized gate: strict — only if job state says done AND no blockers remain
    pending_task_count = sum(
        1 for t in job.tasks
        if (t.status.value if hasattr(t.status, "value") else str(t.status)) in ("pending", "planned")
    )
    blocked_task_count = sum(
        1 for t in job.tasks
        if (t.status.value if hasattr(t.status, "value") else str(t.status)) in ("blocked", "failed")
    )
    # Finalized gate — centralized via can_finalize
    try:
        from packages.orchestration.proposed_tasks import can_finalize
        finalize_ok, finalize_reason = can_finalize(
            str(job.id),
            pending_task_count=pending_task_count,
            blocked_task_count=blocked_task_count,
            pending_approvals=pending_approvals,
        )
    except ImportError:
        finalize_ok = (pending_task_count == 0 and blocked_task_count == 0 and pending_approvals == 0)
        finalize_reason = "ready" if finalize_ok else "pending_work"

    job_says_done = state in ("completed", "done", "finalized")
    is_finalized = job_says_done and finalize_ok
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
            "tests": _build_metrics_tests(events),
            "proof": _metrics_proof_from_chain(proof_chain),
        },
        "snapshot": _build_snapshot_section(job, truth_data_dir),
        "continuation": _build_continuation_section(job, events, truth_data_dir),
        "repair": _build_repair_section(job),
        "overnight": _build_overnight_section(job, truth_data_dir),
        "overnight_run": _build_overnight_run_section(job, truth_data_dir),
        "provider_trust": _build_provider_trust_section(job),
        "provider_verification": _build_provider_verification_section(job),
        "builder_routing": _build_builder_routing_section(job),
        "local_candidate": _build_local_candidate_section(job),
        "candidate_quality": _build_candidate_quality_section(job),
        "external_builder": _build_external_builder_section(job),
        "worker_registry": _build_worker_registry_section(job),
        "token_economy": _build_token_economy_section(job),
        "model_route_tournament": _build_model_route_tournament_section(job),
        "overnight_mission": _build_overnight_mission_section(job),
        "test_execution": _build_test_execution_section(job),
        "snapshot_rollback": _build_snapshot_rollback_section(job),
        "repair_loop": _build_repair_loop_section(job),
        "main_builder_adapter": _build_main_builder_adapter_section(job),
        "managed_execution": _build_managed_execution_section(job),
        "repair_request": _build_repair_request_section(job),
        "self_dogfood": _build_self_dogfood_section(job),
        "self_execution": _build_self_execution_section(job),
        "orchestrator": _build_orchestrator_section(job),
        "local_advisor": _build_local_advisor_section(job),
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
        "proposed_tasks": _build_proposed_tasks_section(str(job.id)),
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


def _build_proposed_tasks_section(job_id: str) -> dict[str, Any]:
    """Build proposed task counts for dashboard v2."""
    empty: dict[str, Any] = {
        "total": 0, "proposed": 0, "evaluated": 0, "approved": 0,
        "rejected": 0, "deferred": 0, "unresolved": 0,
        "approved_not_materialized": 0, "materialized": 0,
        "degraded": False, "blocking_finalized": False, "blocking_build": False,
        "summaries": [],
    }
    try:
        from packages.orchestration.proposed_tasks import (
            ProposedTaskStatus,
            load_proposed_tasks_safe,
        )
        tasks, degraded = load_proposed_tasks_safe(job_id)
        if degraded:
            return {**empty, "degraded": True, "blocking_finalized": True, "blocking_build": True}
        unresolved = sum(1 for t in tasks if t.status in (ProposedTaskStatus.PROPOSED, ProposedTaskStatus.EVALUATED))
        approved = [t for t in tasks if t.status == ProposedTaskStatus.APPROVED_FOR_BUILD]
        materialized = sum(1 for t in approved if t.materialized_task_id)
        not_materialized = len(approved) - materialized
        summaries = [
            {
                "id": t.id,
                "title": t.title[:80],
                "status": t.status.value,
                "risk": t.risk,
                "priority": t.priority,
                "source": t.source.value,
                "materialized_task_id": t.materialized_task_id or None,
                "is_materialized": bool(t.materialized_task_id),
            }
            for t in tasks
        ]
        return {
            "total": len(tasks),
            "proposed": sum(1 for t in tasks if t.status == ProposedTaskStatus.PROPOSED),
            "evaluated": sum(1 for t in tasks if t.status == ProposedTaskStatus.EVALUATED),
            "approved": len(approved),
            "rejected": sum(1 for t in tasks if t.status == ProposedTaskStatus.REJECTED),
            "deferred": sum(1 for t in tasks if t.status == ProposedTaskStatus.DEFERRED),
            "unresolved": unresolved,
            "approved_not_materialized": not_materialized,
            "materialized": materialized,
            "degraded": False,
            "blocking_finalized": unresolved > 0,
            "blocking_build": unresolved > 0,
            "summaries": summaries,
        }
    except ImportError:
        return empty


def _build_resume_section(job: Any, events: list[dict[str, Any]]) -> dict[str, Any]:
    """Build safe resume/checkpoint visibility for dashboard."""
    try:
        from packages.orchestration.data_paths import resolve_data_root
        from packages.orchestration.event_replay import (
            find_checkpoints,
            replay_job,
        )
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
        return "remedy do \"<goal>\" --repo . --builder-provider fixture --json"
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
    print("Press Ctrl-C to stop.\n")

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
