"""
Memory Context Summary — bounded, redacted, approved-only memory for injection.

Produces a safe summary of project memory that can be injected into planner
or execution context without leaking raw content.

Public API::

    build_memory_context(*, project_id, job_id, budget) -> MemoryContextSummary
"""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from typing import Any

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class MemoryContextItem:
    """One approved memory item, summarized for injection."""

    id: str
    title: str
    scope: str
    relevance_reason: str
    confidence: str
    approved: bool
    created_at: str
    token_estimate: int
    source_kind: str


@dataclass(frozen=True)
class MemoryContextSummary:
    """Bounded, redacted memory context ready for planner/builder injection."""

    version: int
    project_id: str | None
    job_id: str | None
    scope: str
    items: tuple[MemoryContextItem, ...]
    item_count: int
    token_budget: int
    estimated_tokens: int
    truncated: bool
    source: str
    redaction: str
    context_hash: str


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_MAX_SUMMARY_CHARS = 200
_DEFAULT_BUDGET = 1000
_DEFAULT_SOURCE = "local_gateway"
_DEFAULT_REDACTION = "redact_secrets"


# ---------------------------------------------------------------------------
# Token estimation
# ---------------------------------------------------------------------------

def _estimate_tokens(text: str) -> int:
    return math.ceil(len(text) / 4) if text else 0


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def build_memory_context(
    *,
    project_id: str | None = None,
    job_id: str | None = None,
    budget: int = _DEFAULT_BUDGET,
) -> MemoryContextSummary:
    """Build bounded, approved-only memory context for injection.

    Rules:
    - Only approved, active memory items included.
    - Summaries bounded to _MAX_SUMMARY_CHARS.
    - Deterministic ordering (newest first, then by key).
    - Truncates at budget.
    - Empty when no memory exists.
    """
    from packages.memory.local_gateway import list_memory

    all_entries = list_memory(project_id=project_id, job_id=job_id)

    # Filter: approved + active only
    approved = [
        e for e in all_entries
        if e.approved and e.validity == "active"
    ]

    # Deterministic sort: newest first, break ties by key
    approved.sort(key=lambda e: (-len(e.created_at), e.created_at, e.key), reverse=False)
    approved.sort(key=lambda e: e.created_at, reverse=True)

    # Build items with budget enforcement
    items: list[MemoryContextItem] = []
    total_tokens = 0
    truncated = False
    hash_parts: list[str] = []

    for entry in approved:
        # Bounded summary: use entry.summary or truncated value
        title = entry.summary[:_MAX_SUMMARY_CHARS] if entry.summary else entry.key[:_MAX_SUMMARY_CHARS]
        relevance = f"scope={entry.scope}, tags={','.join(entry.tags[:5])}"

        item = MemoryContextItem(
            id=str(entry.id),
            title=title,
            scope=entry.scope,
            relevance_reason=relevance,
            confidence=entry.confidence_source,
            approved=True,
            created_at=entry.created_at,
            token_estimate=_estimate_tokens(title + relevance),
            source_kind=entry.source_type,
        )

        if total_tokens + item.token_estimate > budget:
            truncated = True
            break

        items.append(item)
        total_tokens += item.token_estimate
        hash_parts.append(f"{entry.id}:{entry.key}:{entry.created_at}")

    # Context hash: deterministic fingerprint of included items
    hash_input = "|".join(hash_parts) if hash_parts else "empty"
    context_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

    scope = "project" if project_id else ("job" if job_id else "global")

    return MemoryContextSummary(
        version=1,
        project_id=project_id,
        job_id=job_id,
        scope=scope,
        items=tuple(items),
        item_count=len(items),
        token_budget=budget,
        estimated_tokens=total_tokens,
        truncated=truncated,
        source=_DEFAULT_SOURCE,
        redaction=_DEFAULT_REDACTION,
        context_hash=context_hash,
    )


def export_memory_context_json(summary: MemoryContextSummary) -> dict[str, Any]:
    """Export memory context as safe JSON dict (no raw memory content)."""
    return {
        "version": summary.version,
        "project_id": summary.project_id,
        "job_id": summary.job_id,
        "scope": summary.scope,
        "item_count": summary.item_count,
        "token_budget": summary.token_budget,
        "estimated_tokens": summary.estimated_tokens,
        "truncated": summary.truncated,
        "source": summary.source,
        "redaction": summary.redaction,
        "context_hash": summary.context_hash,
        "items": [
            {
                "id": item.id,
                "title": item.title,
                "scope": item.scope,
                "confidence": item.confidence,
                "approved": item.approved,
                "token_estimate": item.token_estimate,
                "source_kind": item.source_kind,
            }
            for item in summary.items
        ],
    }


def emit_memory_recalled_event(
    summary: MemoryContextSummary,
    *,
    data_dir: str | None = None,
    job_id: str | None = None,
    stage: str = "unknown",
) -> None:
    """Emit a project_memory_recalled event with safe metadata only.

    No-op if data_dir or job_id is missing, or if no memory items.
    """
    if not data_dir or not job_id or summary.item_count == 0:
        return
    try:
        from uuid import UUID

        from packages.orchestration.timeline import append_run_event
        append_run_event(data_dir, UUID(job_id), event="project_memory_recalled", metadata={
            "stage": stage,
            "item_count": summary.item_count,
            "estimated_tokens": summary.estimated_tokens,
            "truncated": summary.truncated,
            "scope": summary.scope,
            "source": summary.source,
            "context_hash": summary.context_hash,
            "approved_only": True,
        })
    except (ImportError, OSError, ValueError):
        pass


def format_memory_section(summary: MemoryContextSummary) -> str:
    """Format memory context as a compact text section for injection.

    Returns empty string when no memory items exist.
    """
    if not summary.items:
        return ""

    lines = [f"Project Memory ({summary.item_count} items, ~{summary.estimated_tokens} tokens):"]
    for item in summary.items:
        lines.append(f"  - [{item.scope}] {item.title}")
    if summary.truncated:
        lines.append("  (truncated — more items available)")
    return "\n".join(lines)
