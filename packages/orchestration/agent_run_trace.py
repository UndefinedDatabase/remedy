"""Agent Run Trace v1 — canonical timeline of the Builder/Reviewer/Repair loop.

Append-only trace of safe, redacted events during a job-flow run. Persisted as
agent_run_trace.jsonl + agent_run_trace_summary.json under job evidence output.

Events never include raw stdout/stderr, raw provider output, full diffs, full
file contents, secrets, or absolute private/staging paths.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TRACE_EVENT_KINDS = frozenset({
    "job_flow_started",
    "job_planned",
    "task_started",
    "builder_prompt_created",
    "builder_output_received",
    "reviewer_prompt_created",
    "reviewer_output_received",
    "review_finding_opened",
    "repair_prompt_created",
    "repair_output_received",
    "review_finding_rechecked",
    "task_gate_evaluated",
    "task_workspace_applied",
    "job_evidence_exported",
    "promotion_dry_run_completed",
    "final_audit_completed",
})


@dataclass
class RunTraceEvent:
    """One event in the agent run trace timeline."""
    event_kind: str = ""
    job_id: str = ""
    task_id: str = ""
    run_id: str = ""
    round: int = 0
    role: str = ""
    provider: str = ""
    provider_kind: str = ""
    prompt_kind: str = ""
    prompt_sha256: str = ""
    prompt_chars: int = 0
    changed_files_safe: list[str] = field(default_factory=list)
    finding_ids: list[str] = field(default_factory=list)
    verdict: str = ""
    status: str = ""
    outcome: str = ""
    safe_summary: str = ""
    trace_source: str = ""
    source_artifact_refs: list[str] = field(default_factory=list)
    created_at: str = ""


def create_trace_event(
    event_kind: str,
    *,
    job_id: str = "",
    task_id: str = "",
    run_id: str = "",
    round_num: int = 0,
    role: str = "",
    provider: str = "",
    provider_kind: str = "",
    prompt_kind: str = "",
    prompt_sha256: str = "",
    prompt_chars: int = 0,
    changed_files_safe: list[str] | None = None,
    finding_ids: list[str] | None = None,
    verdict: str = "",
    status: str = "",
    outcome: str = "",
    safe_summary: str = "",
    trace_source: str = "",
    source_artifact_refs: list[str] | None = None,
) -> RunTraceEvent:
    """Create a safe trace event with timestamp."""
    return RunTraceEvent(
        event_kind=event_kind,
        job_id=job_id,
        task_id=task_id,
        run_id=run_id,
        round=round_num,
        role=role,
        provider=provider,
        provider_kind=provider_kind,
        prompt_kind=prompt_kind,
        prompt_sha256=prompt_sha256,
        prompt_chars=prompt_chars,
        changed_files_safe=list(changed_files_safe or []),
        finding_ids=list(finding_ids or []),
        verdict=verdict,
        status=status,
        outcome=outcome,
        safe_summary=safe_summary[:500] if safe_summary else "",
        trace_source=trace_source,
        source_artifact_refs=list(source_artifact_refs or []),
        created_at=datetime.now(timezone.utc).isoformat(),
    )


def trace_event_to_dict(event: RunTraceEvent) -> dict[str, Any]:
    return asdict(event)


def write_trace_jsonl(events: list[RunTraceEvent], path: Path) -> None:
    """Write trace events as JSONL."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for event in events:
            f.write(json.dumps(trace_event_to_dict(event)) + "\n")


def load_trace_jsonl(path: Path) -> list[dict[str, Any]]:
    """Load trace events from JSONL file."""
    if not path.exists():
        return []
    events = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if line:
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return events


def build_trace_summary(events: list[RunTraceEvent]) -> dict[str, Any]:
    """Build aggregate summary of trace events."""
    by_kind: dict[str, int] = {}
    tasks_seen: set[str] = set()
    providers_seen: set[str] = set()
    rounds_max = 0

    for e in events:
        by_kind[e.event_kind] = by_kind.get(e.event_kind, 0) + 1
        if e.task_id:
            tasks_seen.add(e.task_id)
        if e.provider:
            providers_seen.add(e.provider)
        if e.round > rounds_max:
            rounds_max = e.round

    sources_seen: set[str] = set()
    for e in events:
        if e.trace_source:
            sources_seen.add(e.trace_source)

    return {
        "total_events": len(events),
        "event_counts": by_kind,
        "tasks_traced": sorted(tasks_seen),
        "providers": sorted(providers_seen),
        "max_round": rounds_max,
        "has_builder_events": by_kind.get("builder_prompt_created", 0) > 0,
        "has_reviewer_events": by_kind.get("reviewer_prompt_created", 0) > 0,
        "has_repair_events": by_kind.get("repair_prompt_created", 0) > 0,
        "has_final_audit": by_kind.get("final_audit_completed", 0) > 0,
        "trace_sources": sorted(sources_seen),
        "source_limitations": (
            ["Events reconstructed from persisted run data, not captured live."]
            if "reconstructed" in sources_seen else []
        ),
    }
