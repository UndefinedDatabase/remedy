"""
Cockpit v1 — decision-oriented job status view.

Timeline answers: "what happened?"
Cockpit answers: "where are we, what matters, what needs the user,
                  what can continue automatically, what should I do next?"

Read-only: never mutates job state or run logs.
No external dependencies — plain text output only.

Public API::

    summarize_cockpit(job, events, *, data_dir=None) -> str
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from packages.core.models import Job, RunState
from packages.orchestration.approval_queue import (
    APPROVAL_APPROVED,
    APPROVAL_PENDING,
    APPROVAL_REJECTED,
    list_patch_intents,
)
from packages.orchestration.data_paths import run_log_dir
from packages.orchestration.permissions import Capability, is_allowed

if TYPE_CHECKING:
    from packages.orchestration.project_constitution import ProjectConstitution

# ---------------------------------------------------------------------------
# Symbols (consistent with timeline.py)
# ---------------------------------------------------------------------------

from packages.orchestration._symbols import (
    FAIL as _FAIL,
)
from packages.orchestration._symbols import (
    INFO as _INFO,
)
from packages.orchestration._symbols import (
    NEXT as _NEXT,
)
from packages.orchestration._symbols import (
    OK as _OK,
)
from packages.orchestration._symbols import (
    WARN as _WARN,
)
from packages.orchestration._symbols import (
    section,
)

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def summarize_cockpit(
    job: Job,
    events: list[dict[str, Any]],
    *,
    data_dir: Path | None = None,
    constitution: ProjectConstitution | None = None,
) -> str:
    """Return a decision-oriented cockpit string for a job.

    ``data_dir`` is the REMEDY_DATA_DIR root (parent of ``runs/``); when
    provided, the run-log directory path is shown in the artifacts section.
    ``constitution`` is an optional pre-loaded ProjectConstitution; when
    provided, a concise summary line is added to the Important artifacts section.
    """
    signals = _extract_signals(events)
    parts: list[str] = []

    # ── Header ──────────────────────────────────────────────────────────
    short_id = str(job.id)[:8]
    name = job.name if len(job.name) <= 60 else job.name[:60] + "…"
    parts.append("Remedy Cockpit")
    parts.append(f"Job: {short_id} — {name}")
    parts.append(f"State: {job.state.value}")

    total = len(job.tasks)
    completed = sum(1 for t in job.tasks if t.status == RunState.COMPLETED)
    if total:
        parts.append(f"Progress: {completed}/{total} task(s) completed")
    else:
        parts.append("Progress: unplanned (no tasks yet)")

    # ── Situation ────────────────────────────────────────────────────────
    parts.append(section("Situation", width=64))
    parts.extend(_render_situation(job, signals))

    # ── Needs your attention ─────────────────────────────────────────────
    parts.append(section("Needs your attention", width=64))
    attention = _derive_attention(job, signals)
    if attention:
        for item in attention:
            parts.append(f"  {_WARN} {item}")
    else:
        parts.append(f"  {_OK} Nothing needs your attention right now.")

    # ── Can continue automatically ───────────────────────────────────────
    parts.append(section("Can continue automatically", width=64))
    can_auto, auto_reason = _can_auto_continue(job, signals)
    flag = "yes" if can_auto else "no"
    parts.append(f"  {flag} — {auto_reason}")

    # ── Important artifacts ──────────────────────────────────────────────
    artifacts = _collect_artifacts(job, signals, data_dir)
    if constitution is not None:
        n = len(constitution.source_files)
        artifacts.append(("constitution:", f"{n} source file(s)"))
    if artifacts:
        parts.append(section("Important artifacts", width=64))
        for label, value in artifacts:
            parts.append(f"  {label:<16} {value}")

    # ── Next best action ─────────────────────────────────────────────────
    parts.append(section("Next best action", width=64))
    parts.append(_derive_next_action(job, signals))

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Signal extraction
# ---------------------------------------------------------------------------


def _extract_signals(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Scan events once and extract the key decision signals."""
    signals: dict[str, Any] = {
        "last_terminal":           None,   # last task_run_completed/failed/noop
        "last_vfail":              None,   # last verification_failed
        "last_patch":              None,   # last patch_intent_created
        "last_workspace":          None,   # last workspace_materialized
        "last_repo":               None,   # last repo_application_completed
        "has_interrupted":         False,  # task_run_started without terminal
        "interrupted_task_type":   None,
    }

    # Detect interrupted run: task_run_started not closed by a terminal event
    in_task = False
    last_started_type = None
    for ev in events:
        name = ev.get("event", "")
        if name == "task_run_started":
            in_task = True
            last_started_type = ev.get("metadata", {}).get("task_type")
        elif in_task and name in ("task_run_completed", "task_run_failed", "task_run_noop"):
            in_task = False
            last_started_type = None
    if in_task:
        signals["has_interrupted"] = True
        signals["interrupted_task_type"] = last_started_type

    # Collect last occurrence of each relevant event
    for ev in events:
        name = ev.get("event", "")
        if name in ("task_run_completed", "task_run_failed", "task_run_noop"):
            signals["last_terminal"] = ev
        elif name == "verification_failed":
            signals["last_vfail"] = ev
        elif name == "patch_intent_created":
            signals["last_patch"] = ev
        elif name == "workspace_materialized":
            signals["last_workspace"] = ev
        elif name == "repo_application_completed":
            signals["last_repo"] = ev

    return signals


# ---------------------------------------------------------------------------
# Situation section
# ---------------------------------------------------------------------------


def _render_situation(job: Job, signals: dict[str, Any]) -> list[str]:
    lines: list[str] = []

    # Last run status
    lt = signals["last_terminal"]
    if lt is None:
        if signals["has_interrupted"]:
            lines.append(f"  {_WARN} Last run: interrupted (no terminal event recorded)")
        else:
            lines.append(f"  {_INFO} No task runs recorded yet")
    else:
        ev_name = lt.get("event", "")
        outcome = lt.get("outcome", "")
        if ev_name == "task_run_completed":
            lines.append(f"  {_OK} Last run: passed")
        elif ev_name == "task_run_failed":
            if outcome == "permission_denied":
                cap = lt.get("metadata", {}).get("capability", "")
                lines.append(f"  {_FAIL} Last run: blocked (permission denied: {cap})")
            elif outcome == "fail":
                lv = signals["last_vfail"]
                fc = lv.get("metadata", {}).get("failure_count", "?") if lv else "?"
                lines.append(f"  {_FAIL} Last run: verification failed ({fc} check(s))")
            else:
                lines.append(f"  {_FAIL} Last run: failed ({outcome})")
        elif ev_name == "task_run_noop":
            if outcome == "no_pending_tasks":
                lines.append(f"  {_INFO} Last run: no pending tasks")
            else:
                lines.append(f"  {_INFO} Last run: builder returned no change")

    # Patch intent risk
    lp = signals["last_patch"]
    if lp:
        risks = lp.get("metadata", {}).get("risk_levels", [])
        warn_risks = {"medium", "high", "unknown"}
        if any(r in warn_risks for r in risks):
            risk_str = ", ".join(sorted(set(r for r in risks if r in warn_risks)))
            lines.append(f"  {_WARN} Patch intent risk: {risk_str}")
        else:
            lines.append(f"  {_OK} Patch intent risk: low")

    # Permissions
    ws_ok = is_allowed(job, Capability.workspace_write)
    lines.append(f"  {_OK if ws_ok else _FAIL} Workspace writes: {'allowed' if ws_ok else 'denied'}")

    repo_ok = is_allowed(job, Capability.repo_generated_write)
    lines.append(f"  {_OK if repo_ok else _FAIL} Repo writes: {'allowed' if repo_ok else 'denied'}")

    # Pending task count
    pending = sum(1 for t in job.tasks if t.status == RunState.PENDING)
    if pending:
        lines.append(f"  {_INFO} Pending tasks: {pending}")
    else:
        lines.append(f"  {_OK} Pending tasks: none")

    return lines


# ---------------------------------------------------------------------------
# Approval helpers
# ---------------------------------------------------------------------------


def _approval_counts(job: Job) -> dict[str, int]:
    """Count approval states across all patch intents in the job.

    Returns a dict with keys APPROVAL_PENDING, APPROVAL_APPROVED, APPROVAL_REJECTED.
    Reads directly from job.artifacts metadata — no event scanning.
    """
    counts = {APPROVAL_PENDING: 0, APPROVAL_APPROVED: 0, APPROVAL_REJECTED: 0}
    for item in list_patch_intents(job):
        state = item["state"]
        if state in counts:
            counts[state] += 1
    return counts


# ---------------------------------------------------------------------------
# Attention items
# ---------------------------------------------------------------------------


def _derive_attention(job: Job, signals: dict[str, Any]) -> list[str]:
    items: list[str] = []
    pending = sum(1 for t in job.tasks if t.status == RunState.PENDING)

    # Interrupted run — mention first (most alarming)
    if signals["has_interrupted"]:
        tt = signals["interrupted_task_type"] or "unknown"
        items.append(
            f"Interrupted task detected (type: {tt}) — inspect with: remedy timeline <job_id>"
        )

    # workspace_write denied blocks all task execution
    if pending and not is_allowed(job, Capability.workspace_write):
        items.append(
            "workspace_write is required to run tasks — "
            "grant with: remedy job permit <job_id> workspace_write allow"
        )

    # Patch intent risk and approval state
    lp = signals["last_patch"]
    if lp:
        ac = _approval_counts(job)
        risks = lp.get("metadata", {}).get("risk_levels", [])
        if any(r in {"medium", "high", "unknown"} for r in risks):
            if ac[APPROVAL_PENDING] > 0:
                items.append(
                    f"Review patch intent risk — {ac[APPROVAL_PENDING]} pending "
                    "decision(s): remedy patch list <job_id>"
                )
            else:
                items.append("Review patch intent risk levels before applying future changes.")
        # Show rejected count as a separate item regardless of risk level.
        if ac[APPROVAL_REJECTED] > 0:
            items.append(
                f"{ac[APPROVAL_REJECTED]} patch intent(s) rejected — review or re-evaluate: "
                "remedy patch list <job_id>"
            )

    # Verification failure on the most recent failed task run
    lv = signals["last_vfail"]
    lt = signals["last_terminal"]
    if lv and lt and lt.get("event") == "task_run_failed" and lt.get("outcome") == "fail":
        meta = lv.get("metadata", {})
        fc = meta.get("failure_count", "?")
        failed_checks = meta.get("failed_checks", [])
        check_preview = ", ".join(failed_checks[:3])
        if len(failed_checks) > 3:
            check_preview += f" … +{len(failed_checks) - 3} more"
        items.append(f"Verification failed: {fc} check(s) — {check_preview}")

    # Repo write explicitly denied but patch/repo output already exists (optional action).
    # Only fires when the user has explicitly denied repo_generated_write (not the default).
    repo_explicitly_denied = (
        job.metadata.get("permissions", {}).get("repo_generated_write") == "deny"
    )
    if (signals["last_patch"] or signals["last_repo"]) and repo_explicitly_denied:
        items.append(
            "Repo writes are denied — allow with: "
            "remedy job permit <job_id> repo_generated_write allow"
        )

    return items


# ---------------------------------------------------------------------------
# Auto-continue
# ---------------------------------------------------------------------------


def _can_auto_continue(job: Job, signals: dict[str, Any]) -> tuple[bool, str]:
    pending = sum(1 for t in job.tasks if t.status == RunState.PENDING)

    if not pending:
        return False, "no pending tasks"
    if not is_allowed(job, Capability.workspace_write):
        return False, "workspace_write permission not granted"
    if signals["has_interrupted"]:
        # Conservative: interrupted runs must never be treated as auto-continue=True
        # by a future autonomy controller, even though pending tasks exist.
        return False, "interrupted run detected — inspect timeline before continuing"
    return True, "pending tasks and workspace_write allowed"


# ---------------------------------------------------------------------------
# Artifacts
# ---------------------------------------------------------------------------


def _collect_artifacts(
    job: Job,
    signals: dict[str, Any],
    data_dir: Path | None,
) -> list[tuple[str, str]]:
    items: list[tuple[str, str]] = []

    lw = signals["last_workspace"]
    if lw:
        ws = lw.get("metadata", {}).get("workspace_file", "")
        if ws:
            items.append(("workspace:", ws))

    lr = signals["last_repo"]
    if lr:
        files = lr.get("metadata", {}).get("files", [])
        if files:
            items.append(("repo:", files[0]))

    lp = signals["last_patch"]
    if lp:
        count = lp.get("metadata", {}).get("intent_count", 0)
        risks = lp.get("metadata", {}).get("risk_levels", [])
        risk_str = ", ".join(sorted(set(str(r) for r in risks))) if risks else "none"
        items.append(("patch intents:", f"{count}  risk={risk_str}"))

    if data_dir is not None:
        items.append(("run log dir:", str(run_log_dir(job.id, data_dir))))

    return items


# ---------------------------------------------------------------------------
# Next best action
# ---------------------------------------------------------------------------


def _derive_next_action(job: Job, signals: dict[str, Any]) -> str:
    pending = sum(1 for t in job.tasks if t.status == RunState.PENDING)
    ws_ok = is_allowed(job, Capability.workspace_write)
    job_id_str = str(job.id)

    # Hard blocker: workspace permission denied
    if pending and not ws_ok:
        return (
            f"  {_NEXT} Grant workspace_write permission:\n"
            f"      remedy job permit {job_id_str} workspace_write allow"
        )

    # Interrupted run with pending tasks: inspect first
    if signals["has_interrupted"] and pending:
        return (
            f"  {_NEXT} Inspect the interrupted run:\n"
            f"      remedy timeline {job_id_str}\n"
            f"  Then resume:\n"
            f"      remedy job run-next {job_id_str}"
        )

    # Patch risk with pending tasks: direct to approval queue if any decisions pending
    lp = signals["last_patch"]
    if lp and pending:
        risks = lp.get("metadata", {}).get("risk_levels", [])
        if any(r in {"medium", "high", "unknown"} for r in risks):
            ac = _approval_counts(job)
            if ac[APPROVAL_PENDING] > 0:
                return (
                    f"  {_NEXT} Approve or reject pending patch intents, then run next task:\n"
                    f"      remedy patch list {job_id_str}\n"
                    f"      remedy patch approve {job_id_str} <intent_id>\n"
                    f"      remedy job run-next {job_id_str}"
                )
            return (
                f"  {_NEXT} Review patch intent risk levels, then run next task:\n"
                f"      remedy job run-next {job_id_str}"
            )

    # Normal: pending tasks and all permissions OK
    if pending:
        return (
            f"  {_NEXT} Run the next pending task:\n"
            f"      remedy job run-next {job_id_str}"
        )

    # All patch intents approved and no pending tasks
    ac = _approval_counts(job)
    total_intents = sum(ac.values())
    if total_intents > 0 and ac[APPROVAL_APPROVED] == total_intents:
        return (
            f"  {_NEXT} All patch intents approved — apply step is not implemented in v1.\n"
            f"      Use: remedy patch show {job_id_str} <intent_id> to review."
        )

    # Nothing left to run
    return (
        f"  {_NEXT} No pending tasks. Inspect generated files\n"
        f"      or create a new job: remedy job create \"<prompt>\""
    )
