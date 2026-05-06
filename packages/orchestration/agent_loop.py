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
      1. ``task_run_failed`` with ``outcome=permission_denied`` → blocked
      2. Pending medium/high/unknown-risk patch intents  → needs_approval
      3. All tasks done + all non-low intents approved   → complete
      4. Pending tasks                                   → continue / build
      5. No tasks yet                                    → continue / planned
    """
    # 1. Blocking event — most urgent; checked before any other signal.
    for ev in reversed(events):
        if ev.get("event") == "task_run_failed":
            # outcome may live at top level or in metadata (both sites exist)
            outcome = ev.get("outcome") or ev.get("metadata", {}).get("outcome", "")
            if outcome == "permission_denied":
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
                    blocked_reason="permission_denied",
                )

    # 2. Patch intent analysis.
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

    # 3. Completion check — requires at least one task and none pending.
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

    # 4/5. Pending tasks → build; no tasks → planned.
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
    prompts, or diff previews are included in the output.
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

    if state.blocked_reason:
        parts.append(f"  blockers: {state.blocked_reason}")
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
# Helpers
# ---------------------------------------------------------------------------


def _section(title: str) -> str:
    bar = _LINE * (50 - len(title) - 1)
    return f"\n{_LINE}{_LINE} {title} {bar}"


def _next_action(job: Job, state: AgentLoopState) -> str:
    full_id = str(job.id)
    d = state.decision

    if d == AgentLoopDecision.BLOCKED:
        return (
            f"  {_NEXT} Grant the missing permission:\n"
            f"      remedy set-permission {full_id} allow <capability>"
        )
    if d == AgentLoopDecision.NEEDS_APPROVAL:
        return (
            f"  {_NEXT} Review and approve patch intents:\n"
            f"      remedy list-patch-intents {full_id}"
        )
    if d == AgentLoopDecision.NEEDS_REVIEW:
        return (
            f"  {_NEXT} Review patch intents:\n"
            f"      remedy list-patch-intents {full_id}"
        )
    if d == AgentLoopDecision.NEEDS_FIX:
        return (
            f"  {_NEXT} Request a fix cycle via a new task or manual edit."
        )
    if d == AgentLoopDecision.COMPLETE:
        return (
            f"  {_NEXT} Inspect generated files and open PR,"
            " or review the trust report:\n"
            f"      remedy trust-report {full_id}"
        )
    # CONTINUE
    if state.current_stage == AgentLoopStage.BUILD:
        return (
            f"  {_NEXT} Run next Remedy task:\n"
            f"      remedy run-next-task-local {full_id}"
        )
    return (
        f"  {_NEXT} Plan the job:\n"
        f"      remedy plan-job-local {full_id}"
    )
