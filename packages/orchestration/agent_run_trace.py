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
            if any(str(s).startswith("reconstructed") for s in sources_seen) else []
        ),
    }


# ---------------------------------------------------------------------------
# F004 — normalized raw stream as a trace source
# ---------------------------------------------------------------------------

#: Explicit trace-source labels. A reader can always tell where events came from.
TRACE_SOURCE_STREAM = "normalized_raw_stream"
TRACE_SOURCE_LEGACY = "reconstructed_legacy_evidence"

#: Stream event types that become trace events, and their trace event_kind.
_STREAM_EVENT_KINDS = {
    "tool_use": "tool_use",
    "tool_result": "tool_result",
    "api_retry": "api_retry",
    "result": "provider_result",
    "provider_error": "provider_error",
    "stream_cap_reached": "stream_cap_reached",
}

#: Reconstruction must not duplicate these once normalized events exist.
STREAM_OWNED_EVENT_KINDS = frozenset(_STREAM_EVENT_KINDS.values())


def has_normalized_stream(task_dir: Path | str) -> bool:
    """True when a task has normalized F004 stream events available."""
    from packages.orchestration.stream_evidence import RUN_EVENTS_FILENAME
    return (Path(task_dir) / RUN_EVENTS_FILENAME).is_file()


def trace_events_from_run_events(
    task_dir: Path | str,
    *,
    job_id: str = "",
    task_id: str = "",
    run_id: str = "",
    provider: str = "",
) -> list[RunTraceEvent]:
    """Build trace events from a task's normalized ``run_events.jsonl``.

    Each trace event keeps the raw byte offset backreference in
    ``source_artifact_refs`` so a reader can jump to the exact raw stream bytes.
    API retries stay visible. No model text is copied.
    """
    from packages.orchestration.stream_evidence import (
        RAW_STREAM_FILENAME,
        RUN_EVENTS_FILENAME,
        read_run_events,
    )

    base = Path(task_dir)
    events: list[RunTraceEvent] = []
    for ev in read_run_events(base / RUN_EVENTS_FILENAME):
        kind = _STREAM_EVENT_KINDS.get(str(ev.get("event_type", "")))
        if not kind:
            continue
        parts: list[str] = []
        if ev.get("event_type") == "tool_use" and ev.get("tool_name"):
            parts.append(f"tool={ev['tool_name']}")
        if ev.get("event_type") == "api_retry":
            parts.append(f"attempt={ev.get('attempt', '')} reason={ev.get('reason', '')}")
        if ev.get("event_type") == "provider_error":
            parts.append(str(ev.get("error", ""))[:200])
        offset = ev.get("raw_byte_offset")
        length = ev.get("raw_byte_length")
        refs = [
            f"{RUN_EVENTS_FILENAME}#seq={ev.get('seq', '')}",
            f"{RAW_STREAM_FILENAME}#line={ev.get('raw_line_number', '')}"
            f",offset={offset},length={length}",
        ]
        events.append(create_trace_event(
            event_kind=kind,
            job_id=job_id,
            task_id=task_id,
            run_id=run_id,
            provider=provider,
            safe_summary=" ".join(parts)[:200],
            trace_source=TRACE_SOURCE_STREAM,
            source_artifact_refs=refs,
        ))
    return events


def resolve_trace_source(task_dir: Path | str) -> str:
    """Return the trace source that will be used for a task.

    Normalized raw stream events win when present; otherwise the existing
    reconstruction from persisted run data remains the fallback.
    """
    return TRACE_SOURCE_STREAM if has_normalized_stream(task_dir) else TRACE_SOURCE_LEGACY


#: Where per-call stream artifacts live under a task's evidence directory.
STREAMS_DIRNAME = "streams"


def iter_task_stream_calls(task_dir: Path | str):
    """Yield ``(stream_call_id, call_dir)`` for every per-call stream directory.

    Deterministic order: role, then round, then attempt. Absent streams yield
    nothing, so a task without F004 evidence simply falls back to reconstruction.
    """
    from packages.orchestration.stream_evidence import RUN_EVENTS_FILENAME

    root = Path(task_dir) / STREAMS_DIRNAME
    if not root.is_dir():
        return
    for events_file in sorted(root.rglob(RUN_EVENTS_FILENAME)):
        call_dir = events_file.parent
        rel = call_dir.relative_to(Path(task_dir)).as_posix()
        yield rel, call_dir


def task_has_stream_evidence(task_dir: Path | str) -> bool:
    return any(True for _ in iter_task_stream_calls(task_dir))


def trace_events_from_task_streams(
    task_dir: Path | str,
    *,
    job_id: str = "",
    task_id: str = "",
    run_id: str = "",
) -> list[RunTraceEvent]:
    """Build normalized provider/tool trace events for every call of a task.

    Each event keeps a relative reference to the exact raw artifact line, byte
    offset and length. Returns [] when the task has no stream artifacts, so the
    caller keeps its existing reconstruction.
    """
    from packages.orchestration.stream_evidence import (
        RAW_STREAM_FILENAME,
        RUN_EVENTS_FILENAME,
        read_run_events,
    )

    events: list[RunTraceEvent] = []
    for rel, call_dir in iter_task_stream_calls(task_dir):
        role = "builder" if "/builder/" in f"/{rel}/" else (
            "reviewer" if "/reviewer/" in f"/{rel}/" else ""
        )
        for ev in read_run_events(call_dir / RUN_EVENTS_FILENAME):
            kind = _STREAM_EVENT_KINDS.get(str(ev.get("event_type", "")))
            if not kind:
                continue
            parts: list[str] = [f"call={rel}"]
            if ev.get("tool_name"):
                parts.append(f"tool={ev['tool_name']}")
            if ev.get("event_type") == "api_retry":
                parts.append(f"attempt={ev.get('attempt', '')} reason={ev.get('reason', '')}")
            if ev.get("event_type") == "provider_error":
                parts.append(str(ev.get("error", ""))[:150])
            if ev.get("event_type") == "stream_cap_reached":
                parts.append("provider terminated at stream cap")
            refs = [
                f"{rel}/{RUN_EVENTS_FILENAME}#seq={ev.get('seq', '')}",
                f"{rel}/{RAW_STREAM_FILENAME}#line={ev.get('raw_line_number', '')}"
                f",offset={ev.get('raw_byte_offset')},length={ev.get('raw_byte_length')}",
            ]
            events.append(create_trace_event(
                event_kind=kind,
                job_id=job_id,
                task_id=task_id,
                run_id=run_id,
                role=role,
                safe_summary=" ".join(parts)[:200],
                trace_source=TRACE_SOURCE_STREAM,
                source_artifact_refs=refs,
            ))
    return events
