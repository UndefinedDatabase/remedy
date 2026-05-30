"""
Context Pack v0 — deterministic compact context generator for future LLM/provider calls.

Produces a token-budget-aware context pack from structured job/project data.
No LLM calls, no network, no embeddings, no raw artifact content.

Modes:
  compact  — readable concise text sections
  caveman  — ultra-short fragments, minimal prose

Public API::

    build_context_pack(job, events, *, budget, mode) -> ContextPack
    export_context_pack_json(pack) -> dict
    summarize_context_pack(pack) -> str
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from packages.core.models import Job, RunState


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PackSection:
    """A single section in the context pack."""

    name: str
    priority: int  # lower = higher priority
    content: str
    estimated_tokens: int


@dataclass(frozen=True)
class ContextPack:
    """Complete context pack."""

    version: int
    job_id: str
    mode: str
    budget: int
    estimated_tokens: int
    truncated: bool
    sections: tuple[PackSection, ...]


# ---------------------------------------------------------------------------
# Token estimation
# ---------------------------------------------------------------------------

def _estimate_tokens(text: str) -> int:
    """Simple deterministic token estimate: ceil(chars / 4)."""
    return math.ceil(len(text) / 4) if text else 0


# ---------------------------------------------------------------------------
# Section builders
# ---------------------------------------------------------------------------

def _build_job_summary(job: Job, mode: str) -> PackSection:
    """Priority 1: job overview."""
    prompt = job.user_prompt or ""
    if mode == "caveman":
        content = (
            f"job:{str(job.id)[:8]} state:{job.state.value} "
            f"tasks:{len(job.tasks)} prompt:{prompt[:60]}"
        )
    elif mode == "standard":
        content = (
            f"Job: {str(job.id)} ({job.name})\n"
            f"State: {job.state.value}\n"
            f"Prompt: {prompt[:200]}\n"
            f"Tasks: {len(job.tasks)}\n"
            f"Artifacts: {len(job.artifacts)}"
        )
    else:
        content = (
            f"Job: {str(job.id)[:8]} ({job.name})\n"
            f"State: {job.state.value}\n"
            f"Prompt: {prompt[:100]}\n"
            f"Tasks: {len(job.tasks)}"
        )
    return PackSection(name="job_summary", priority=1, content=content,
                        estimated_tokens=_estimate_tokens(content))


def _build_task_state(job: Job, mode: str) -> PackSection:
    """Priority 2: current task statuses."""
    lines = []
    for i, t in enumerate(job.tasks):
        tt = t.inputs.get("task_type", "unknown")
        if mode == "caveman":
            lines.append(f"t{i}:{tt}={t.status.value}")
        else:
            lines.append(f"  Task {i}: {tt} — {t.status.value}")
    content = "\n".join(lines) if lines else "(no tasks)"
    return PackSection(name="task_state", priority=2, content=content,
                        estimated_tokens=_estimate_tokens(content))


def _build_blockers(job: Job, mode: str) -> PackSection:
    """Priority 3: permissions and blockers."""
    perms = job.metadata.get("permissions", {})
    lines = []
    for p, v in sorted(perms.items()):
        if mode == "caveman":
            lines.append(f"{p}={v}")
        else:
            lines.append(f"  {p}: {v}")
    content = "\n".join(lines) if lines else "(no permissions set)"
    return PackSection(name="blockers_permissions", priority=3, content=content,
                        estimated_tokens=_estimate_tokens(content))


def _build_apply_proof(events: list[dict[str, Any]], mode: str) -> PackSection:
    """Priority 4: apply/test proof summaries."""
    proofs = [e for e in events if e.get("event") == "patch_apply_proof_recorded"]
    tests = [e for e in events if e.get("event") == "test_run_completed"]
    lines = []
    for p in proofs[-3:]:  # last 3
        meta = p.get("metadata", {})
        if mode == "caveman":
            lines.append(f"apply:{meta.get('target_path', '?')} Δ{meta.get('bytes_delta', 0)}b")
        else:
            lines.append(
                f"  Applied: {meta.get('target_path', '?')} "
                f"(sha:{meta.get('after_sha256', '?')[:12]}.. Δ{meta.get('bytes_delta', 0)}b)"
            )
    for t in tests[-3:]:
        meta = t.get("metadata", {})
        if mode == "caveman":
            lines.append(f"test:{meta.get('command', '?')} rc={meta.get('exit_code', '?')}")
        else:
            lines.append(
                f"  Test: {meta.get('command', '?')} → {meta.get('status', '?')} "
                f"(exit={meta.get('exit_code', '?')}, {meta.get('duration_ms', 0)}ms)"
            )
    content = "\n".join(lines) if lines else "(no apply/test proofs)"
    return PackSection(name="apply_test_proof", priority=4, content=content,
                        estimated_tokens=_estimate_tokens(content))


def _build_readiness_summary(job: Job, events: list[dict[str, Any]], mode: str) -> PackSection:
    """Priority 5: readiness missing actions."""
    try:
        from packages.orchestration.autonomy_readiness import assess_job_readiness
        report = assess_job_readiness(job, events)
        if mode == "caveman":
            content = f"readiness:L{report.highest_eligible_level} missing:{len(report.next_actions)}"
        else:
            content = (
                f"Readiness: Level {report.highest_eligible_level}\n"
                + ("\n".join(f"  → {a}" for a in report.next_actions) if report.next_actions else "  (no missing actions)")
            )
    except (ImportError, ValueError, OSError):
        content = "(readiness unavailable)"
    return PackSection(name="readiness_summary", priority=5, content=content,
                        estimated_tokens=_estimate_tokens(content))


def _build_memory_keys(mode: str) -> PackSection:
    """Priority 6: approved active memory summaries (no raw values)."""
    try:
        from packages.memory.local_gateway import list_memory
        all_entries = list_memory()
        entries = [e for e in all_entries if e.approved and e.validity == "active"]
        lines = []
        if mode == "caveman":
            lines.append(f"mem:{len(entries)}/{len(all_entries)}")
            for e in entries[:10]:
                lines.append(f"  {e.key}")
        elif mode == "standard":
            for e in entries[:10]:
                summary = e.summary[:80] if e.summary else "(no summary)"
                lines.append(
                    f"  {e.key}: {summary}\n"
                    f"    scope={e.scope} review={e.review_status} "
                    f"evidence={len(e.evidence_refs)} src={e.source_type}"
                )
        else:
            for e in entries[:10]:
                summary = e.summary[:60] if e.summary else ""
                lines.append(f"  {e.key}: {summary}" if summary else f"  {e.key}")
        content = "\n".join(lines) if lines else "(no approved memory)"
    except (ImportError, ValueError, OSError):
        content = "(memory unavailable)"
    return PackSection(name="memory_keys", priority=6, content=content,
                        estimated_tokens=_estimate_tokens(content))


def _build_command_candidates(events: list[dict[str, Any]], mode: str) -> PackSection:
    """Priority 7: command discovery summary."""
    disc = [e for e in events if e.get("event") == "command_discovery_completed"]
    if disc:
        meta = disc[-1].get("metadata", {})
        count = meta.get("candidate_count", 0)
        selected = meta.get("selected_command", "?")
        if mode == "caveman":
            content = f"cmds:{count} sel:{selected}"
        else:
            content = f"Discovered commands: {count}, selected: {selected}"
    else:
        content = "(no command discovery)" if mode != "caveman" else "cmds:none"
    return PackSection(name="command_candidates", priority=7, content=content,
                        estimated_tokens=_estimate_tokens(content))


def _build_run_events(events: list[dict[str, Any]], mode: str) -> PackSection:
    """Priority 8: secondary run events summary."""
    # Count by event type, skip already-covered types
    covered = {
        "patch_apply_proof_recorded", "test_run_completed",
        "command_discovery_completed",
    }
    counts: dict[str, int] = {}
    for e in events:
        name = e.get("event", "")
        if name not in covered:
            counts[name] = counts.get(name, 0) + 1
    top = sorted(counts.items(), key=lambda x: -x[1])[:8]
    if mode == "caveman":
        content = " ".join(f"{n}:{c}" for n, c in top) if top else "events:0"
    else:
        lines = [f"  {n}: {c}" for n, c in top]
        content = "\n".join(lines) if lines else "(no additional events)"
    return PackSection(name="run_events", priority=8, content=content,
                        estimated_tokens=_estimate_tokens(content))


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def build_context_pack(
    job: Job,
    events: list[dict[str, Any]],
    *,
    budget: int = 2000,
    mode: str = "compact",
) -> ContextPack:
    """Build a token-budget-aware context pack."""
    if mode not in ("compact", "caveman", "standard"):
        mode = "compact"

    # Build all sections
    all_sections: list[PackSection] = []
    all_sections.append(_build_job_summary(job, mode))
    all_sections.append(_build_task_state(job, mode))
    all_sections.append(_build_blockers(job, mode))
    all_sections.append(_build_apply_proof(events, mode))
    all_sections.append(_build_readiness_summary(job, events, mode))
    all_sections.append(_build_memory_keys(mode))
    all_sections.append(_build_command_candidates(events, mode))
    all_sections.append(_build_run_events(events, mode))

    # Sort by priority and enforce budget
    all_sections.sort(key=lambda s: s.priority)
    included: list[PackSection] = []
    total_tokens = 0
    truncated = False
    for s in all_sections:
        if total_tokens + s.estimated_tokens <= budget:
            included.append(s)
            total_tokens += s.estimated_tokens
        else:
            truncated = True
            break

    return ContextPack(
        version=1,
        job_id=str(job.id),
        mode=mode,
        budget=budget,
        estimated_tokens=total_tokens,
        truncated=truncated,
        sections=tuple(included),
    )


def export_context_pack_json(pack: ContextPack) -> dict[str, Any]:
    """Export context pack as safe JSON dict."""
    return {
        "version": pack.version,
        "job_id": pack.job_id,
        "mode": pack.mode,
        "budget": pack.budget,
        "estimated_tokens": pack.estimated_tokens,
        "truncated": pack.truncated,
        "sections": [
            {
                "name": s.name,
                "priority": s.priority,
                "content": s.content,
                "estimated_tokens": s.estimated_tokens,
            }
            for s in pack.sections
        ],
    }


def summarize_context_pack(pack: ContextPack) -> str:
    """Human-readable text summary of context pack."""
    lines = [f"Context Pack ({pack.mode}, budget={pack.budget}, est={pack.estimated_tokens} tokens)"]
    if pack.truncated:
        lines.append("  [TRUNCATED — budget exceeded]")
    lines.append("")
    for s in pack.sections:
        lines.append(f"--- {s.name} (priority={s.priority}, ~{s.estimated_tokens} tokens) ---")
        lines.append(s.content)
        lines.append("")
    return "\n".join(lines)
