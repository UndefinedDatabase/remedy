"""
Timeline v1 — human-readable cockpit layer over run-log events.

Public API::

    load_run_events(data_dir, job_id)  → list[dict]
    summarize_timeline(job, events)    → str

Read-only: never mutates job state or run logs.
No external dependencies — plain text output only.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from uuid import UUID

from packages.core.models import Job, RunState
from packages.orchestration._symbols import (
    FAIL as _FAIL,
)
from packages.orchestration._symbols import (
    INFO as _INFO,
)
from packages.orchestration._symbols import (
    NEXT as _NEXT,
)

# ---------------------------------------------------------------------------
# Symbols
# ---------------------------------------------------------------------------
from packages.orchestration._symbols import (
    OK as _OK,
)
from packages.orchestration._symbols import (
    WARN as _WARN,
)
from packages.orchestration._symbols import (
    section,
)
from packages.orchestration.data_paths import run_log_dir
from packages.orchestration.run_log import RunLogWriter, new_run_id

# One run per PROCESS: every event one invocation appends to a job belongs to the
# same run, which is what RunLogWriter's docstring promises and what DECISION F260
# D1's run-keyed layout needs to stay bounded.
_PROCESS_RUN_ID = new_run_id()

# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------


def append_run_event(
    data_dir: str | Path,
    job_id: UUID | str,
    *,
    event: str,
    metadata: dict[str, Any] | None = None,
) -> None:
    """Append a single event to the run log for a job.

    Convenience wrapper around RunLogWriter for one-shot event recording.
    ``data_dir`` is the Remedy data root (e.g. ``.data/``).
    """
    jid = job_id if isinstance(job_id, UUID) else UUID(str(job_id))
    writer = RunLogWriter(jid, run_id=_PROCESS_RUN_ID, data_root=Path(data_dir))
    writer.log(event, **(metadata or {}))


def load_run_events(data_dir: Path, job_id: UUID | str) -> list[dict[str, Any]]:
    """Load all run log events for a job, sorted by timestamp.

    Reads every ``*.jsonl`` file under ``<data_dir>/runs/<job_id>/``.
    Returns ``[]`` if the directory does not exist.
    Skips empty lines and silently ignores malformed JSON lines.
    """
    run_log_path = run_log_dir(job_id, data_dir)
    if not run_log_path.exists():
        return []
    events: list[dict[str, Any]] = []
    for jsonl_file in sorted(run_log_path.glob("*.jsonl")):
        for raw in jsonl_file.read_text(encoding="utf-8").splitlines():
            raw = raw.strip()
            if not raw:
                continue
            try:
                events.append(json.loads(raw))
            except json.JSONDecodeError:
                pass
    events.sort(key=lambda e: e.get("timestamp", ""))
    return events


# ---------------------------------------------------------------------------
# Summarise
# ---------------------------------------------------------------------------


def summarize_timeline(job: Job, events: list[dict[str, Any]]) -> str:
    """Return a human-readable multiline string summarising the job timeline."""
    parts: list[str] = []

    # ── Header ──────────────────────────────────────────────────────────
    parts.append("Remedy Timeline")
    short_id = str(job.id)[:8]
    name = job.name if len(job.name) <= 60 else job.name[:60] + "…"
    parts.append(f"Job: {short_id} — {name}")
    parts.append(f"State: {job.state.value}")

    completed = sum(1 for t in job.tasks if t.status == RunState.COMPLETED)
    pending = sum(1 for t in job.tasks if t.status == RunState.PENDING)
    running = sum(1 for t in job.tasks if t.status == RunState.RUNNING)
    parts.append(f"Tasks: {completed} completed, {pending} pending, {running} running")

    # ── Events ──────────────────────────────────────────────────────────
    parts.append(section("Events", width=64))
    if not events:
        parts.append(f"  {_INFO} No run log events found.")
    else:
        parts.extend(_render_events(events))

    # ── Status ──────────────────────────────────────────────────────────
    parts.append(section("Current status", width=64))
    parts.append(_derive_status(job))

    # ── Next action ─────────────────────────────────────────────────────
    parts.append(section("Next suggested action", width=64))
    parts.append(_derive_next_action(job, events))

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Internal: event rendering
# ---------------------------------------------------------------------------


def _render_events(events: list[dict[str, Any]]) -> list[str]:
    """Process events in order; accumulate task blocks for compact rendering."""
    lines: list[str] = []
    in_task: list[dict[str, Any]] | None = None

    for ev in events:
        name = ev.get("event", "")

        if name == "task_run_started":
            in_task = [ev]
            continue

        if in_task is not None:
            in_task.append(ev)
            if name in ("task_run_completed", "task_run_failed", "task_run_noop"):
                lines.extend(_render_task_block(in_task))
                in_task = None
            continue

        # Non-task (or pre-task noop) event
        rendered = _render_single_event(ev)
        if rendered is not None:
            lines.append(rendered)

    # Unclosed task block — process was interrupted
    if in_task:
        lines.extend(_render_task_block(in_task))

    return lines


def _render_single_event(ev: dict[str, Any]) -> str | None:
    """Render one standalone (non-task-block) event to a single line.

    Returns ``None`` for events that should be silently skipped.
    Unknown events are rendered as an info line rather than crashing.
    """
    name = ev.get("event", "")
    meta = ev.get("metadata", {})
    outcome = ev.get("outcome")
    model = ev.get("model", "")

    if name == "job_created":
        return f"  {_OK} Job created"

    if name == "planning_started":
        return None  # planning_completed/failed is the useful signal

    if name == "planning_completed":
        if outcome == "noop":
            return f"  {_INFO} Planning: already planned (no change)"
        task_count = meta.get("task_count", "?")
        elapsed = _fmt_elapsed(meta)
        model_str = f"  model={model}" if model else ""
        return f"  {_OK} Planning completed  tasks={task_count}{model_str}{elapsed}"

    if name == "planning_failed":
        # Prefer error_category (structured, redaction-safe).
        # Never use ev["message"] — it may contain raw exception text from older logs.
        detail = meta.get("error_category", "") or "unknown error"
        return f"  {_FAIL} Planning failed: {detail}"

    if name == "task_run_noop":
        # Pre-start noop (no pending tasks) — occurs outside a task block.
        if outcome == "no_pending_tasks":
            return f"  {_INFO} No pending tasks"
        if outcome == "no_change":
            return f"  {_INFO} Builder returned no change"
        return f"  {_INFO} No-op ({outcome})"

    if name == "project_constitution_loaded":
        src   = meta.get("source_count", "?")
        warn  = meta.get("warning_count", 0)
        tests = meta.get("has_test_commands", False)
        tests_str = "yes" if tests else "no"
        warn_str  = f"  warnings={warn}" if warn else ""
        return (
            f"  {_OK} Project Constitution loaded"
            f"  sources={src}  tests={tests_str}{warn_str}"
        )

    if name == "patch_intent_applied":
        intent_id   = meta.get("intent_id", "")[:14]
        target_path = meta.get("target_path", "")
        ev_outcome  = meta.get("outcome") or outcome or ""
        sym = _OK if ev_outcome == "applied" else _INFO
        return (
            f"  {sym} patch intent applied  {intent_id}  {target_path}"
            f"  outcome={ev_outcome}"
        )

    if name == "patch_apply_proof_recorded":
        intent_id   = meta.get("intent_id", "")[:14]
        after_sha   = str(meta.get("after_sha256", ""))
        bdelta      = meta.get("bytes_delta", 0)
        ldelta      = meta.get("line_delta", 0)
        sha_str     = (after_sha[:16] + "…") if after_sha else "?"
        return (
            f"  {_OK} patch apply proof  {intent_id}"
            f"  after_sha={sha_str}"
            f"  Δbytes={bdelta:+d}  Δlines={ldelta:+d}"
        )

    if name == "test_run_completed":
        status    = str(meta.get("status", "unknown"))
        command   = str(meta.get("command", ""))
        exit_code = meta.get("exit_code")
        dur_ms    = meta.get("duration_ms", 0)
        sym       = _OK if status == "passed" else (_FAIL if status == "failed" else _WARN)
        exit_str  = f"  exit={exit_code}" if exit_code is not None else ""
        dur_str   = _fmt_elapsed({"elapsed_ms": dur_ms}) if dur_ms else ""
        return (
            f"  {sym} test run  status={status}  cmd={command}"
            f"{exit_str}{dur_str}"
            f"  (raw output not shown)"
        )

    # All other events outside a task block: render as informational.
    return f"  {_INFO} {name}"


def _render_task_block(task_events: list[dict[str, Any]]) -> list[str]:
    """Render a compact block for one task run (from started to terminal)."""
    lines: list[str] = []

    started = task_events[0]
    task_type = started.get("metadata", {}).get("task_type", "unknown")

    def _find(ev_name: str) -> dict[str, Any] | None:
        return next((e for e in task_events if e.get("event") == ev_name), None)

    terminal = next(
        (e for e in reversed(task_events)
         if e.get("event") in ("task_run_completed", "task_run_failed", "task_run_noop")),
        None,
    )

    builder_ev = _find("builder_started")
    completed_ev = _find("builder_completed")
    workspace_ev = _find("workspace_materialized")
    vpass_ev = _find("verification_passed")
    vfail_ev = _find("verification_failed")
    repo_done_ev = _find("repo_application_completed")
    repo_skip_ev = _find("repo_application_skipped")
    patch_ev = _find("patch_intent_created")

    model = builder_ev.get("model", "") if builder_ev else ""
    elapsed = _fmt_elapsed(completed_ev.get("metadata", {})) if completed_ev else ""

    # ── Primary outcome line ─────────────────────────────────────────────
    if terminal is None:
        lines.append(f"  {_WARN} {task_type}  interrupted (no terminal event recorded)")
        return lines

    ev_name = terminal.get("event", "")
    outcome = terminal.get("outcome", "")
    term_meta = terminal.get("metadata", {})

    if ev_name == "task_run_completed":
        model_str = f"  model={model}" if model else ""
        verified = "  verified=pass" if vpass_ev else ""
        lines.append(f"  {_OK} {task_type}{model_str}{elapsed}{verified}")
    elif ev_name == "task_run_failed":
        if outcome == "permission_denied":
            cap = term_meta.get("capability", "")
            lines.append(f"  {_FAIL} {task_type}  blocked: permission denied ({cap})")
        elif outcome == "fail":
            if vfail_ev:
                fc = vfail_ev.get("metadata", {}).get("failure_count", "?")
                lines.append(f"  {_FAIL} {task_type}  verification failed ({fc} check(s))")
            else:
                lines.append(f"  {_FAIL} {task_type}  failed")
        else:
            lines.append(f"  {_FAIL} {task_type}  failed: {outcome}")
    elif ev_name == "task_run_noop":
        if outcome == "no_change":
            lines.append(f"  {_INFO} {task_type}  builder returned no change")
        else:
            lines.append(f"  {_INFO} {task_type}  noop ({outcome})")

    # ── Sub-detail lines ─────────────────────────────────────────────────
    if workspace_ev:
        ws = workspace_ev.get("metadata", {}).get("workspace_file", "")
        if ws:
            lines.append(f"      workspace: {ws}")

    if repo_done_ev:
        files = repo_done_ev.get("metadata", {}).get("files", [])
        if files:
            lines.append(f"      repo:      {files[0]}")
            for extra in files[1:]:
                lines.append(f"                 {extra}")

    if repo_skip_ev:
        reason = repo_skip_ev.get("metadata", {}).get("reason", "")
        lines.append(f"      {_WARN} repo write skipped: {reason}")

    if patch_ev:
        pm = patch_ev.get("metadata", {})
        count = pm.get("intent_count", 0)
        risks = pm.get("risk_levels", [])
        risk_str = ", ".join(sorted(set(str(r) for r in risks))) if risks else ""
        risk_part = f"  risk={risk_str}" if risk_str else ""
        lines.append(f"      intents:   {count}{risk_part}")

    if vfail_ev:
        failed_checks = vfail_ev.get("metadata", {}).get("failed_checks", [])
        for check in failed_checks[:3]:
            lines.append(f"      {_FAIL} check: {check}")
        if len(failed_checks) > 3:
            lines.append(f"      … {len(failed_checks) - 3} more check(s)")

    return lines


def _fmt_elapsed(meta: dict[str, Any]) -> str:
    ms = meta.get("elapsed_ms")
    if ms is None:
        return ""
    if ms >= 1000:
        return f"  {ms / 1000:.1f}s"
    return f"  {ms}ms"


# ---------------------------------------------------------------------------
# Internal: status + next action
# ---------------------------------------------------------------------------


def _derive_status(job: Job) -> str:
    total = len(job.tasks)
    completed = sum(1 for t in job.tasks if t.status == RunState.COMPLETED)
    pending = sum(1 for t in job.tasks if t.status == RunState.PENDING)
    running = sum(1 for t in job.tasks if t.status == RunState.RUNNING)

    if total == 0:
        return "  Unplanned: no tasks in job."
    if running:
        return f"  Running: {running} task(s) in progress."
    if pending:
        return f"  Pending: {pending} of {total} task(s) awaiting execution."
    if completed == total:
        return f"  Complete: all {total} task(s) completed."
    return f"  {job.state.value.capitalize()}."


def _derive_next_action(job: Job, events: list[dict[str, Any]]) -> str:
    pending = sum(1 for t in job.tasks if t.status == RunState.PENDING)
    job_id_str = str(job.id)

    # Most recent terminal event
    terminal_events = [
        e for e in events
        if e.get("event") in ("task_run_completed", "task_run_failed", "task_run_noop")
    ]
    last_terminal = terminal_events[-1] if terminal_events else None

    # Permission denied: suggest granting before running again
    if (
        last_terminal
        and last_terminal.get("event") == "task_run_failed"
        and last_terminal.get("outcome") == "permission_denied"
    ):
        cap = last_terminal.get("metadata", {}).get("capability", "workspace_write")
        return (
            f"  {_NEXT} Grant permission if appropriate:\n"
            f"      remedy job permit {job_id_str} {cap} allow"
        )

    # Patch intent risk: flag review if any medium/high/unknown risk present
    patch_events = [e for e in events if e.get("event") == "patch_intent_created"]
    if patch_events:
        risks = set(patch_events[-1].get("metadata", {}).get("risk_levels", []))
        if risks & {"medium", "high", "unknown"}:
            return (
                f"  {_NEXT} Review patch intent risk levels before applying future changes."
            )

    # Pending tasks
    if pending:
        return (
            f"  {_NEXT} Run the next pending task:\n"
            f"      remedy job run-next {job_id_str}"
        )

    return (
        f"  {_NEXT} No pending tasks. Inspect generated repo/workspace files\n"
        f"      or create a new job: remedy job create \"<prompt>\""
    )
