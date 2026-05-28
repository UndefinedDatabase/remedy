"""
Agent Loop Contract v1 — Orchestration contract for external agent workflows.

Defines the data models and state derivation logic for coordinating workflows
such as:

    Remedy planner → builder agent → reviewer agent → fix cycle → verifier

IMPORTANT — Scope limitations (v1):
  No external processes are called.  No Claude Code, Copilot CLI, Git
  commands, shell commands, MCP tools, network requests, or repo mutations
  beyond what already exists in Remedy.  This module is a contract and
  inspection layer only — execution adapters are a future step.

Run-log events (only ``agent_loop_inspected`` is emitted; the rest are
reserved for future adapter steps):
  agent_loop_inspected       — emitted by ``remedy agent-loop <job_id>``
  external_agent_proposed    — future: external agent submitted a proposal
  external_review_recorded   — future: reviewer agent returned findings
  fix_cycle_requested        — future: fixer agent was requested
  agent_loop_completed       — future: loop reached a terminal state

Stale-event policy:
  A historical ``task_run_failed outcome=permission_denied`` event does NOT
  permanently block the loop.  It is ignored when:
    - the same task_id has a later ``task_run_completed`` event, OR
    - the corresponding task is no longer PENDING in job.tasks, OR
    - there are no pending tasks at all.

  A CURRENT block is signalled by:
    - A non-reserved capability that is explicitly denied for the job AND
      pending tasks exist (checked via ``is_allowed``), OR
    - An unresolved ``permission_denied`` event whose task is still PENDING
      with no later successful terminal event.

Public API::

    default_agent_loop_state(job, *, max_cycles=3) -> AgentLoopState
    summarize_agent_loop_state(job, state) -> str
    derive_agent_loop_state(job, events, *, max_cycles=3) -> AgentLoopState
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from packages.core.models import Job, RunState
from packages.orchestration.approval_queue import (
    APPROVAL_APPROVED,
    APPROVAL_PENDING,
    list_patch_intents,
)
from packages.orchestration.patch_intent import RISK_LOW
from packages.orchestration.permissions import Capability, is_allowed, is_reserved


# ---------------------------------------------------------------------------
# Symbols (consistent with other orchestration views)
# ---------------------------------------------------------------------------

_OK   = "✓"
_FAIL = "✕"
_WARN = "!"
_INFO = "○"
_NEXT = "→"
_LINE = "─"


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class AgentRole(str, enum.Enum):
    PLANNER  = "planner"
    BUILDER  = "builder"
    REVIEWER = "reviewer"
    FIXER    = "fixer"
    VERIFIER = "verifier"
    REPORTER = "reporter"


class AgentLoopStage(str, enum.Enum):
    PLANNED   = "planned"
    BUILD     = "build"
    REVIEW    = "review"
    FIX       = "fix"
    VERIFY    = "verify"
    COMPLETED = "completed"
    BLOCKED   = "blocked"
    FAILED    = "failed"


class AgentLoopDecision(str, enum.Enum):
    # Note: "continue" is a Python keyword; CONTINUE is the attribute name.
    CONTINUE       = "continue"
    NEEDS_REVIEW   = "needs_review"
    NEEDS_FIX      = "needs_fix"
    NEEDS_APPROVAL = "needs_approval"
    BLOCKED        = "blocked"
    COMPLETE       = "complete"


# ---------------------------------------------------------------------------
# Immutable data models
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AgentAdapterSpec:
    """Describes an external agent adapter — metadata only, no execution."""

    name: str
    role: AgentRole
    provider: str
    command_hint: str | None = None
    capabilities: frozenset[str] = field(default_factory=frozenset)
    dry_run_only: bool = True
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class AgentLoopState:
    """Immutable snapshot of the current agent loop state for a job."""

    job_id: UUID
    current_stage: AgentLoopStage
    cycle: int
    max_cycles: int
    decision: AgentLoopDecision
    builder: AgentAdapterSpec | None
    reviewer: AgentAdapterSpec | None
    pending_findings: tuple[str, ...]
    completed_cycles: int
    blocked_reason: str | None


# ---------------------------------------------------------------------------
# Public functions
# ---------------------------------------------------------------------------


def default_agent_loop_state(job: Job, *, max_cycles: int = 3) -> AgentLoopState:
    """Return a fresh, zero-cycle loop state for a job."""
    return AgentLoopState(
        job_id=job.id,
        current_stage=AgentLoopStage.PLANNED,
        cycle=0,
        max_cycles=max_cycles,
        decision=AgentLoopDecision.CONTINUE,
        builder=None,
        reviewer=None,
        pending_findings=(),
        completed_cycles=0,
        blocked_reason=None,
    )


def derive_agent_loop_state(
    job: Job,
    events: list[dict[str, Any]],
    *,
    max_cycles: int = 3,
) -> AgentLoopState:
    """Derive current loop state from job model and run-log events.

    Deterministic — no LLM calls, no external processes, no repo access.

    Priority order (highest first):
      1. Current permission denial or unresolved perm_denied event → blocked
      2. Pending medium/high/unknown-risk patch intents              → needs_approval
      3. All tasks done + all non-low intents approved               → complete
      4. Pending tasks                                               → continue / build
      5. No tasks yet                                                → continue / planned

    Historical permission_denied events that have been superseded by a later
    successful task_run_completed (or whose task is no longer PENDING) are
    treated as stale and do not block the loop.
    """
    # ── 1. Blocking check ─────────────────────────────────────────────────
    blocked_reason = _find_current_blocker(job, events)
    if blocked_reason:
        return AgentLoopState(
            job_id=job.id,
            current_stage=AgentLoopStage.BLOCKED,
            cycle=0,
            max_cycles=max_cycles,
            decision=AgentLoopDecision.BLOCKED,
            builder=None,
            reviewer=None,
            pending_findings=(),
            completed_cycles=0,
            blocked_reason=blocked_reason,
        )

    # ── 2. Patch intent analysis ──────────────────────────────────────────
    intents = list_patch_intents(job)
    pending_non_low = [
        i for i in intents
        if i["state"] == APPROVAL_PENDING and i["risk"] != RISK_LOW
    ]
    # Vacuously True when there are no non-low intents.
    all_non_low_approved = all(
        i["state"] == APPROVAL_APPROVED
        for i in intents
        if i["risk"] != RISK_LOW
    )

    if pending_non_low:
        return AgentLoopState(
            job_id=job.id,
            current_stage=AgentLoopStage.REVIEW,
            cycle=0,
            max_cycles=max_cycles,
            decision=AgentLoopDecision.NEEDS_APPROVAL,
            builder=None,
            reviewer=None,
            pending_findings=(),
            completed_cycles=0,
            blocked_reason=None,
        )

    # ── 3. Completion check — requires at least one task and none pending ──
    all_tasks_done = bool(job.tasks) and not any(
        t.status == RunState.PENDING for t in job.tasks
    )
    if all_tasks_done and all_non_low_approved:
        return AgentLoopState(
            job_id=job.id,
            current_stage=AgentLoopStage.COMPLETED,
            cycle=0,
            max_cycles=max_cycles,
            decision=AgentLoopDecision.COMPLETE,
            builder=None,
            reviewer=None,
            pending_findings=(),
            completed_cycles=0,
            blocked_reason=None,
        )

    # ── 4/5. Pending tasks → build; no tasks → planned ────────────────────
    has_pending = any(t.status == RunState.PENDING for t in job.tasks)
    stage = AgentLoopStage.BUILD if has_pending else AgentLoopStage.PLANNED
    return AgentLoopState(
        job_id=job.id,
        current_stage=stage,
        cycle=0,
        max_cycles=max_cycles,
        decision=AgentLoopDecision.CONTINUE,
        builder=None,
        reviewer=None,
        pending_findings=(),
        completed_cycles=0,
        blocked_reason=None,
    )


def summarize_agent_loop_state(job: Job, state: AgentLoopState) -> str:
    """Return a human-readable agent loop state report for a job.

    Read-only: never mutates job, state, or any filesystem resource.
    Redaction: no raw artifact content, approval reasons, event messages,
    prompts, diff previews, or command output are included in the output.
    """
    intents = list_patch_intents(job)
    pending_tasks = [t for t in job.tasks if t.status == RunState.PENDING]

    short_id = str(job.id)[:8]
    name     = job.name if len(job.name) <= 60 else job.name[:60] + "…"

    parts: list[str] = []
    parts.append("Remedy Agent Loop")
    parts.append(f"Job: {short_id} — {name}")
    parts.append(f"Stage: {state.current_stage.value}")
    parts.append(f"Decision: {state.decision.value}")
    parts.append(f"Cycle: {state.cycle}/{state.max_cycles}")

    # ── Agents ──────────────────────────────────────────────────────────────
    parts.append(_section("Agents"))
    parts.append(f"  builder:  {state.builder.name  if state.builder  else 'not configured'}")
    parts.append(f"  reviewer: {state.reviewer.name if state.reviewer else 'not configured'}")

    # ── Loop state ──────────────────────────────────────────────────────────
    parts.append(_section("Loop state"))
    parts.append(f"  pending tasks: {len(pending_tasks)}")

    # Patch intent summary — structured counts/risk labels only.
    pending_non_low = [
        i for i in intents
        if i["state"] == APPROVAL_PENDING and i["risk"] != RISK_LOW
    ]
    pending_low = [
        i for i in intents
        if i["state"] == APPROVAL_PENDING and i["risk"] == RISK_LOW
    ]
    if pending_non_low:
        risks = ", ".join(sorted({i["risk"] for i in pending_non_low}))
        n = len(pending_non_low)
        parts.append(
            f"  patch decisions: {n} pending {risks}-risk"
            f" intent{'s' if n != 1 else ''}"
        )
    elif pending_low:
        parts.append(
            f"  patch decisions: {len(pending_low)} pending low-risk"
            " intent(s) (no approval required)"
        )
    elif intents:
        parts.append(f"  patch decisions: all {len(intents)} intent(s) decided")
    else:
        parts.append("  patch decisions: none")

    # Blocker display — parse "permission_denied:capability" format.
    if state.blocked_reason:
        parts.append(f"  blockers: {_format_blocker(state.blocked_reason)}")
    else:
        parts.append("  blockers: none")

    if state.pending_findings:
        for finding in state.pending_findings:
            parts.append(f"  finding: {finding}")

    # ── Next action ─────────────────────────────────────────────────────────
    parts.append(_section("Next action"))
    parts.append(_next_action(job, state))

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _find_current_blocker(
    job: Job,
    events: list[dict[str, Any]],
) -> str | None:
    """Return a ``blocked_reason`` string if there is a current blocking condition.

    Returns ``None`` when no active blocker exists.  Format of the returned
    string when a blocker is found:

      ``"permission_denied:<capability>"``  — capability name known
      ``"permission_denied"``               — capability unknown (legacy event)

    A historical permission_denied event is considered stale (not blocking) when:
      - There are no pending tasks (all work is done or no work has started).
      - The same task_id has a later ``task_run_completed`` event.
      - The corresponding task is no longer PENDING in job.tasks.
    """
    has_pending = any(t.status == RunState.PENDING for t in job.tasks)

    # Check 1: explicit capability denial in job metadata (no events required).
    # Only capabilities that were explicitly set to "deny" constitute a current
    # block — default-deny states (repo_generated_write etc.) do not block, as
    # those capabilities are simply not granted yet and do not halt pending work.
    if has_pending:
        overrides: dict[str, str] = job.metadata.get("permissions", {})
        for cap in Capability:
            if is_reserved(cap):
                continue
            if overrides.get(cap.value) == "deny":
                return f"permission_denied:{cap.value}"

    # Check 2: unresolved permission_denied events.
    # Historical events whose tasks have since succeeded are treated as stale.
    if not has_pending:
        # No pending tasks → no event-based block possible.
        return None

    # Build latest terminal event per task_id (chronological order → last wins).
    terminal_per_task: dict[str, dict] = {}
    for ev in events:
        task_id = ev.get("task_id")
        if task_id and ev.get("event") in (
            "task_run_completed", "task_run_failed", "task_run_noop"
        ):
            terminal_per_task[task_id] = ev

    for ev in events:
        if ev.get("event") != "task_run_failed":
            continue
        outcome = ev.get("outcome") or ev.get("metadata", {}).get("outcome", "")
        if outcome != "permission_denied":
            continue

        task_id = ev.get("task_id")
        if task_id:
            # Stale if a later successful completion exists for this task.
            latest = terminal_per_task.get(task_id)
            if latest and latest.get("event") == "task_run_completed":
                continue
            # Stale if the task is no longer PENDING in the job model.
            task_still_pending = any(
                str(t.id) == task_id and t.status == RunState.PENDING
                for t in job.tasks
            )
            if not task_still_pending:
                continue
        # No task_id → cannot prove stale → conservative (treat as active).

        capability = ev.get("metadata", {}).get("capability")
        return f"permission_denied:{capability}" if capability else "permission_denied"

    return None


def _format_blocker(blocked_reason: str) -> str:
    """Format blocked_reason for display.

    ``"permission_denied:workspace_write"`` → ``"permission_denied (workspace_write)"``
    ``"permission_denied"``                 → ``"permission_denied"``
    """
    if ":" in blocked_reason:
        prefix, cap = blocked_reason.split(":", 1)
        return f"{prefix} ({cap})"
    return blocked_reason


def _section(title: str) -> str:
    bar = _LINE * (50 - len(title) - 1)
    return f"\n{_LINE}{_LINE} {title} {bar}"


def run_agent_loop(
    job: Job,
    *,
    max_cycles: int = 3,
    auto_approve_low_risk: bool = False,
    run_tests: bool = True,
) -> AgentLoopState:
    """Run the agent execution loop for a job.

    Safe local execution loop. Default does NOT auto-approve.
    Stops on: needs_approval (paused), blocked, complete, max_cycles reached.

    Run-log events emitted:
      agent_loop_started, cycle_started, agent_loop_decision,
      cycle_completed, agent_loop_paused, agent_loop_completed
    """
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.run_log import RunLogWriter
    from packages.orchestration.storage import load_job, save_job
    from packages.orchestration.timeline import load_run_events

    data_dir = resolve_data_root()
    log = RunLogWriter(job_id=job.id)

    log.log("agent_loop_started", outcome="started",
            **{"metadata": {"max_cycles": max_cycles,
                            "auto_approve_low_risk": auto_approve_low_risk,
                            "run_tests": run_tests}})

    state: AgentLoopState | None = None

    for cycle in range(1, max_cycles + 1):
        # Reload job and events each cycle to get latest state
        job = load_job(job.id)
        events = load_run_events(data_dir, job.id)
        state = derive_agent_loop_state(job, events, max_cycles=max_cycles)

        log.log("cycle_started", outcome="cycle_started",
                **{"metadata": {"cycle": cycle, "stage": state.current_stage.value,
                                "decision": state.decision.value}})

        # Terminal conditions
        if state.decision == AgentLoopDecision.COMPLETE:
            log.log("agent_loop_completed", outcome="complete",
                    **{"metadata": {"cycle": cycle, "reason": "all_done"}})
            return state

        if state.decision == AgentLoopDecision.BLOCKED:
            log.log("agent_loop_paused", outcome="blocked",
                    **{"metadata": {"cycle": cycle,
                                    "blocked_reason": state.blocked_reason}})
            return state

        if state.decision == AgentLoopDecision.NEEDS_APPROVAL:
            if auto_approve_low_risk:
                _auto_approve_low_risk_intents(job, log)
                # Re-derive after auto-approval
                job = load_job(job.id)
                events = load_run_events(data_dir, job.id)
                state = derive_agent_loop_state(job, events, max_cycles=max_cycles)
                if state.decision == AgentLoopDecision.NEEDS_APPROVAL:
                    # Still needs approval for non-low-risk intents
                    log.log("agent_loop_paused", outcome="needs_approval",
                            **{"metadata": {"cycle": cycle}})
                    return state
            else:
                log.log("agent_loop_paused", outcome="needs_approval",
                        **{"metadata": {"cycle": cycle}})
                return state

        # Execute: run next task if in BUILD stage
        if state.current_stage == AgentLoopStage.BUILD:
            log.log("agent_loop_decision", outcome="run_next_task",
                    **{"metadata": {"cycle": cycle}})
            try:
                _run_next_task_step(job)
            except SystemExit:
                # run_next_task_local calls sys.exit on failure
                pass

        elif state.current_stage == AgentLoopStage.PLANNED:
            # Need planning first
            log.log("agent_loop_decision", outcome="needs_planning",
                    **{"metadata": {"cycle": cycle}})
            log.log("agent_loop_paused", outcome="needs_planning",
                    **{"metadata": {"cycle": cycle}})
            return state

        log.log("cycle_completed", outcome="cycle_completed",
                **{"metadata": {"cycle": cycle}})

    # Max cycles reached
    if state is None:
        events = load_run_events(data_dir, job.id)
        state = derive_agent_loop_state(job, events, max_cycles=max_cycles)

    log.log("agent_loop_completed", outcome="max_cycles_reached",
            **{"metadata": {"max_cycles": max_cycles}})
    return state


def _auto_approve_low_risk_intents(job: Job, log: Any) -> None:
    """Auto-approve low-risk patch intents."""
    from packages.orchestration.approval_queue import set_approval_state
    from packages.orchestration.storage import save_job

    intents = list_patch_intents(job)
    for intent in intents:
        if intent["state"] == APPROVAL_PENDING and intent["risk"] == RISK_LOW:
            try:
                set_approval_state(job, intent["intent_id"], "approved",
                                   reason="auto-approved (low risk)")
            except ValueError:
                continue
    save_job(job)


def _run_next_task_step(job: Job) -> None:
    """Execute one run-next-task step. Delegates to the job command handler."""
    from apps.cli.commands.job import _cmd_run_next_task_local
    _cmd_run_next_task_local(str(job.id))


def _next_action(job: Job, state: AgentLoopState) -> str:
    full_id = str(job.id)
    d = state.decision

    if d == AgentLoopDecision.BLOCKED:
        # Extract concrete capability from "permission_denied:<cap>" format.
        cap_arg = "<capability>"
        if state.blocked_reason and ":" in state.blocked_reason:
            cap_arg = state.blocked_reason.split(":", 1)[1]
        return (
            f"  {_NEXT} Grant the missing permission:\n"
            f"      remedy job permit {full_id} {cap_arg} allow"
        )
    if d == AgentLoopDecision.NEEDS_APPROVAL:
        return (
            f"  {_NEXT} Review and approve patch intents:\n"
            f"      remedy patch list {full_id}"
        )
    if d == AgentLoopDecision.NEEDS_REVIEW:
        return (
            f"  {_NEXT} Review patch intents:\n"
            f"      remedy patch list {full_id}"
        )
    if d == AgentLoopDecision.NEEDS_FIX:
        return (
            f"  {_NEXT} Request a fix cycle via a new task or manual edit."
        )
    if d == AgentLoopDecision.COMPLETE:
        return (
            f"  {_NEXT} Inspect generated files and open PR,"
            " or review the trust report:\n"
            f"      remedy brain trust {full_id}"
        )
    # CONTINUE
    if state.current_stage == AgentLoopStage.BUILD:
        return (
            f"  {_NEXT} Run next Remedy task:\n"
            f"      remedy job run-next {full_id}"
        )
    return (
        f"  {_NEXT} Plan the job:\n"
        f"      remedy job plan {full_id}"
    )
