"""Project-level brain summary, patterns, and memory suggestions.

Aggregates across multiple jobs to give project-wide visibility.
All outputs contain safe metadata only — no raw content.

Public API::

    build_project_summary(project, jobs, all_events) -> ProjectBrainSummary
    detect_patterns(jobs, all_events) -> list[ProjectPattern]
    build_project_model_summary(scorecards) -> ProjectModelSummary
    suggest_memory_updates(summary, patterns) -> list[MemorySuggestion]
    export_project_summary_json(summary) -> dict
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


# -- Step 400: Project Brain Summary --

@dataclass
class ProjectBrainSummary:
    """Project-level summary across jobs. Safe metadata only."""

    version: int = 1
    project_id: str = ""
    generated_at: str = ""
    job_count: int = 0
    active_job_count: int = 0
    completed_job_count: int = 0
    blocked_job_count: int = 0
    latest_job_id: str = ""
    latest_event_at: str = ""
    current_focus: str = ""
    open_decisions: int = 0
    blockers: list[str] = field(default_factory=list)
    completed_work: list[str] = field(default_factory=list)
    pending_work: list[str] = field(default_factory=list)
    risky_areas: list[str] = field(default_factory=list)
    changed_file_count: int = 0
    frequently_touched_files: list[str] = field(default_factory=list)
    latest_safe_checkpoint: str = ""
    token_usage_total: int = 0
    model_quality_summary: str = ""
    patterns: list[dict[str, Any]] = field(default_factory=list)
    memory_suggestions: list[dict[str, Any]] = field(default_factory=list)
    suggested_next_step: str = ""
    next_command: str = ""
    redaction: str = "safe_metadata_only"


def build_project_summary(
    project: Any,
    jobs: list[Any],
    all_events: dict[str, list[dict[str, Any]]],
) -> ProjectBrainSummary:
    """Build project summary from real jobs and events."""
    now = datetime.now(timezone.utc).isoformat()
    pid = str(project.id) if hasattr(project, "id") else str(project)

    active = 0
    completed = 0
    blocked = 0
    latest_job_id = ""
    latest_event_at = ""
    all_stop_reasons: list[str] = []
    all_touched_files: list[str] = []
    total_tokens = 0
    open_decisions = 0
    blockers: list[str] = []
    completed_work: list[str] = []
    pending_work: list[str] = []

    for job in jobs:
        jid = str(job.id)
        state = job.state.value if hasattr(job.state, "value") else str(job.state)
        events = all_events.get(jid, [])

        if state in ("completed", "done"):
            completed += 1
            completed_work.append(f"Job {jid[:8]}: {state}")
        elif state in ("blocked", "failed"):
            blocked += 1
        else:
            active += 1
            pending_work.append(f"Job {jid[:8]}: {state}")

        if not latest_job_id:
            latest_job_id = jid

        for ev in events:
            ts = ev.get("timestamp", "")
            if ts > latest_event_at:
                latest_event_at = ts
                latest_job_id = jid

            meta = ev.get("metadata", {})
            event_name = ev.get("event", "")

            if event_name == "stop_reason_recorded":
                sr = meta.get("stop_reason", "")
                if sr:
                    all_stop_reasons.append(sr)

            if event_name == "patch_intent_applied":
                path = meta.get("target_path", "")
                if path:
                    all_touched_files.append(path)

            if event_name == "human_decision_requested" and ev.get("outcome") != "resolved":
                open_decisions += 1

            est = meta.get("estimated_tokens")
            if isinstance(est, int):
                total_tokens += est

    for job in jobs:
        jid = str(job.id)
        events = all_events.get(jid, [])
        stop_events = [e for e in events if e.get("event") == "stop_reason_recorded"]
        for se in stop_events:
            sr = se.get("metadata", {}).get("stop_reason", "")
            if sr in ("approval_required", "permission_denied"):
                blockers.append(f"Job {jid[:8]}: {sr}")

    file_counts: dict[str, int] = {}
    for f in all_touched_files:
        file_counts[f] = file_counts.get(f, 0) + 1
    frequent = sorted(file_counts.items(), key=lambda x: -x[1])[:5]
    frequently_touched = [f for f, _ in frequent]

    current_focus = ""
    if active > 0:
        current_focus = f"{active} active job(s)"
    elif blocked > 0:
        current_focus = f"{blocked} blocked job(s) need attention"
    elif completed > 0:
        current_focus = "All jobs completed"

    suggested = ""
    next_cmd = ""
    if blocked > 0:
        suggested = "Resolve blocked jobs first"
        if blockers:
            next_cmd = f"remedy job show {latest_job_id[:8] if latest_job_id else '<job_id>'}"
    elif active > 0:
        suggested = "Continue active jobs"
        next_cmd = f"remedy job show {latest_job_id[:8] if latest_job_id else '<job_id>'}"
    elif completed > 0:
        suggested = "Start new work or review completed results"
        next_cmd = f"remedy project show {pid[:8]}"

    return ProjectBrainSummary(
        project_id=pid,
        generated_at=now,
        job_count=len(jobs),
        active_job_count=active,
        completed_job_count=completed,
        blocked_job_count=blocked,
        latest_job_id=latest_job_id,
        latest_event_at=latest_event_at,
        current_focus=current_focus,
        open_decisions=open_decisions,
        blockers=blockers[:5],
        completed_work=completed_work[:10],
        pending_work=pending_work[:10],
        changed_file_count=len(set(all_touched_files)),
        frequently_touched_files=frequently_touched,
        token_usage_total=total_tokens,
        suggested_next_step=suggested,
        next_command=next_cmd,
    )


# -- Step 401: Repeated Pattern Detection --

@dataclass
class ProjectPattern:
    """A detected repeated pattern across jobs."""

    pattern_id: str = ""
    kind: str = ""
    count: int = 0
    severity: str = "low"
    summary: str = ""
    related_job_ids: list[str] = field(default_factory=list)
    related_file_paths: list[str] = field(default_factory=list)
    first_seen_at: str = ""
    last_seen_at: str = ""
    suggested_attention: str = ""


def detect_patterns(
    jobs: list[Any],
    all_events: dict[str, list[dict[str, Any]]],
) -> list[ProjectPattern]:
    """Detect repeated patterns across jobs."""
    patterns: list[ProjectPattern] = []

    stop_reasons: dict[str, list[tuple[str, str]]] = {}
    touched_files: dict[str, list[str]] = {}
    parse_failures: dict[str, list[str]] = {}
    test_failures: list[tuple[str, str]] = []
    permission_blocks: list[tuple[str, str]] = []
    provider_issues: list[tuple[str, str]] = []
    repair_exhaustions: list[tuple[str, str]] = []

    for job in jobs:
        jid = str(job.id)
        events = all_events.get(jid, [])

        for ev in events:
            meta = ev.get("metadata", {})
            event_name = ev.get("event", "")
            ts = ev.get("timestamp", "")

            if event_name == "stop_reason_recorded":
                sr = meta.get("stop_reason", "")
                if sr:
                    stop_reasons.setdefault(sr, []).append((jid, ts))

            if event_name == "patch_intent_applied":
                path = meta.get("target_path", "")
                if path:
                    touched_files.setdefault(path, []).append(jid)

            if event_name == "builder_patch_parsed" and not meta.get("parse_success"):
                ek = meta.get("error_kind", "unknown")
                parse_failures.setdefault(ek, []).append(jid)

            if event_name == "test_run_completed" and meta.get("status") == "failed":
                test_failures.append((jid, ts))

            if event_name == "stop_reason_recorded" and meta.get("stop_reason") == "permission_denied":
                permission_blocks.append((jid, ts))

            if event_name == "stop_reason_recorded" and meta.get("stop_reason") == "provider_unavailable":
                provider_issues.append((jid, ts))

            if event_name == "repair_loop_stopped" and meta.get("reason") == "repair_budget_exhausted":
                repair_exhaustions.append((jid, ts))

    pid = 0
    for sr, occurrences in stop_reasons.items():
        if len(occurrences) >= 2:
            timestamps = [t for _, t in occurrences if t]
            job_ids = list({j for j, _ in occurrences})
            pid += 1
            patterns.append(ProjectPattern(
                pattern_id=f"stop_{pid}",
                kind="repeated_stop_reason",
                count=len(occurrences),
                severity="medium" if len(occurrences) >= 3 else "low",
                summary=f"'{sr}' stopped {len(occurrences)} times across {len(job_ids)} job(s)",
                related_job_ids=job_ids[:5],
                first_seen_at=min(timestamps) if timestamps else "",
                last_seen_at=max(timestamps) if timestamps else "",
                suggested_attention=f"Investigate recurring '{sr}' — may indicate a systematic issue",
            ))

    for path, job_ids in touched_files.items():
        if len(job_ids) >= 2:
            unique_jobs = list(set(job_ids))
            pid += 1
            patterns.append(ProjectPattern(
                pattern_id=f"file_{pid}",
                kind="frequently_touched_file",
                count=len(job_ids),
                severity="low",
                summary=f"'{path}' modified {len(job_ids)} times across {len(unique_jobs)} job(s)",
                related_job_ids=unique_jobs[:5],
                related_file_paths=[path],
                suggested_attention=f"File '{path}' may need special attention or testing",
            ))

    for ek, job_ids in parse_failures.items():
        if len(job_ids) >= 2:
            unique_jobs = list(set(job_ids))
            pid += 1
            patterns.append(ProjectPattern(
                pattern_id=f"parse_{pid}",
                kind="repeated_parse_failure",
                count=len(job_ids),
                severity="medium" if len(job_ids) >= 3 else "low",
                summary=f"Parse failure '{ek}' in {len(job_ids)} attempts across {len(unique_jobs)} job(s)",
                related_job_ids=unique_jobs[:5],
                suggested_attention=f"Model may need prompt adjustment for '{ek}' failures",
            ))

    if len(test_failures) >= 2:
        unique_jobs = list({j for j, _ in test_failures})
        pid += 1
        patterns.append(ProjectPattern(
            pattern_id=f"test_{pid}",
            kind="repeated_test_failure",
            count=len(test_failures),
            severity="medium" if len(test_failures) >= 3 else "low",
            summary=f"Tests failed {len(test_failures)} times across {len(unique_jobs)} job(s)",
            related_job_ids=unique_jobs[:5],
            suggested_attention="Check if test failures share a common root cause",
        ))

    if len(permission_blocks) >= 2:
        unique_jobs = list({j for j, _ in permission_blocks})
        pid += 1
        patterns.append(ProjectPattern(
            pattern_id=f"perm_{pid}",
            kind="repeated_permission_block",
            count=len(permission_blocks),
            severity="medium",
            summary=f"Permission denied {len(permission_blocks)} times across {len(unique_jobs)} job(s)",
            related_job_ids=unique_jobs[:5],
            suggested_attention="Grant required permissions or review permission policy",
        ))

    if len(provider_issues) >= 2:
        unique_jobs = list({j for j, _ in provider_issues})
        pid += 1
        patterns.append(ProjectPattern(
            pattern_id=f"prov_{pid}",
            kind="repeated_provider_unavailable",
            count=len(provider_issues),
            severity="medium",
            summary=f"Provider unavailable {len(provider_issues)} times across {len(unique_jobs)} job(s)",
            related_job_ids=unique_jobs[:5],
            suggested_attention="Check if local model is running and accessible",
        ))

    if len(repair_exhaustions) >= 2:
        unique_jobs = list({j for j, _ in repair_exhaustions})
        pid += 1
        patterns.append(ProjectPattern(
            pattern_id=f"repair_{pid}",
            kind="repeated_repair_exhaustion",
            count=len(repair_exhaustions),
            severity="high" if len(repair_exhaustions) >= 3 else "medium",
            summary=f"Repair budget exhausted {len(repair_exhaustions)} times across {len(unique_jobs)} job(s)",
            related_job_ids=unique_jobs[:5],
            suggested_attention="Model may struggle with this type of task — consider prompt changes",
        ))

    return sorted(patterns, key=lambda p: -p.count)


# -- Step 402: Model Quality Rollup --

@dataclass
class ProjectModelSummary:
    """Project-level model quality summary. Safe metadata only."""

    provider: str = ""
    model: str = ""
    prompt_profile: str = ""
    sample_count: int = 0
    usable_patch_rate: float = 0.0
    safe_rejection_rate: float = 0.0
    outcome_accuracy: float = 0.0
    avg_tokens: float = 0.0
    avg_latency_ms: float = 0.0
    confidence: str = "low"
    recommendation: str = ""
    needs_real_model_check: bool = True
    redaction: str = "safe_metadata_only"


def build_project_model_summary(
    scorecards: list[Any],
) -> ProjectModelSummary:
    """Aggregate scorecards into project-level model quality summary."""
    if not scorecards:
        return ProjectModelSummary(
            recommendation="No model quality data — run builder quality check first.",
            confidence="low",
        )

    total_cases = 0
    total_usable = 0
    total_rejected = 0
    total_correct = 0
    total_tokens = 0
    total_latency = 0
    any_real = False

    for sc in scorecards:
        n = sc.total_cases
        total_cases += n
        total_usable += int(sc.usable_patch_rate * n)
        total_rejected += int(sc.safe_rejection_rate * n)
        total_correct += int(sc.outcome_accuracy * n)
        total_tokens += int(sc.average_tokens * n)
        total_latency += int(sc.average_latency_ms * n)
        if not sc.needs_real_model_check:
            any_real = True

    if total_cases == 0:
        return ProjectModelSummary(
            recommendation="No samples — run builder quality check first.",
            confidence="low",
        )

    confidence = "low"
    if any_real and total_cases >= 5:
        confidence = "medium"
    if any_real and total_cases >= 15:
        confidence = "high"

    accuracy = total_correct / total_cases
    if accuracy >= 0.8:
        rec = f"Good accuracy ({accuracy:.0%}). "
    elif accuracy >= 0.5:
        rec = f"Moderate accuracy ({accuracy:.0%}). "
    else:
        rec = f"Low accuracy ({accuracy:.0%}). "

    if not any_real:
        rec += "Needs real model check — only simulated data so far."
    else:
        rec += f"Based on {total_cases} samples."

    best_sc = max(scorecards, key=lambda s: s.outcome_accuracy)

    return ProjectModelSummary(
        provider=best_sc.provider,
        model=best_sc.model,
        prompt_profile=best_sc.prompt_profile,
        sample_count=total_cases,
        usable_patch_rate=total_usable / total_cases,
        safe_rejection_rate=total_rejected / total_cases if total_cases > 0 else 0.0,
        outcome_accuracy=accuracy,
        avg_tokens=total_tokens / total_cases,
        avg_latency_ms=total_latency / total_cases,
        confidence=confidence,
        recommendation=rec,
        needs_real_model_check=not any_real,
    )


# -- Step 403: Safe Memory Suggestions --

@dataclass
class MemorySuggestion:
    """Advisory memory update suggestion. Requires approval before writing."""

    title: str = ""
    summary: str = ""
    evidence_count: int = 0
    related_job_ids: list[str] = field(default_factory=list)
    risk: str = "low"
    recommended_scope: str = "project"
    requires_approval: bool = True


def suggest_memory_updates(
    summary: ProjectBrainSummary,
    patterns: list[ProjectPattern],
) -> list[MemorySuggestion]:
    """Generate safe memory suggestions from project patterns."""
    suggestions: list[MemorySuggestion] = []

    for pattern in patterns:
        if pattern.kind == "frequently_touched_file" and pattern.count >= 3:
            for f in pattern.related_file_paths[:3]:
                suggestions.append(MemorySuggestion(
                    title=f"Frequently modified file: {f}",
                    summary=f"File '{f}' has been modified {pattern.count} times. Consider adding targeted tests.",
                    evidence_count=pattern.count,
                    related_job_ids=pattern.related_job_ids[:3],
                ))

        if pattern.kind == "repeated_stop_reason" and pattern.count >= 3:
            suggestions.append(MemorySuggestion(
                title=f"Recurring blocker: {pattern.summary[:60]}",
                summary=pattern.suggested_attention,
                evidence_count=pattern.count,
                related_job_ids=pattern.related_job_ids[:3],
                risk="medium",
            ))

        if pattern.kind == "repeated_parse_failure" and pattern.count >= 2:
            suggestions.append(MemorySuggestion(
                title=f"Model parse issue: {pattern.summary[:60]}",
                summary=pattern.suggested_attention,
                evidence_count=pattern.count,
                related_job_ids=pattern.related_job_ids[:3],
            ))

    if summary.blocked_job_count >= 2:
        suggestions.append(MemorySuggestion(
            title="Multiple blocked jobs",
            summary=f"{summary.blocked_job_count} jobs are blocked. Approval or permission may be the common issue.",
            evidence_count=summary.blocked_job_count,
            risk="medium",
        ))

    return suggestions[:10]


# -- Export --

def export_project_summary_json(summary: ProjectBrainSummary) -> dict[str, Any]:
    """Export project summary as safe JSON."""
    return {
        "version": summary.version,
        "project_id": summary.project_id,
        "generated_at": summary.generated_at,
        "redaction": summary.redaction,
        "job_count": summary.job_count,
        "active_job_count": summary.active_job_count,
        "completed_job_count": summary.completed_job_count,
        "blocked_job_count": summary.blocked_job_count,
        "latest_job_id": summary.latest_job_id,
        "latest_event_at": summary.latest_event_at,
        "current_focus": summary.current_focus,
        "open_decisions": summary.open_decisions,
        "blockers": summary.blockers,
        "completed_work": summary.completed_work,
        "pending_work": summary.pending_work,
        "changed_file_count": summary.changed_file_count,
        "frequently_touched_files": summary.frequently_touched_files,
        "token_usage_total": summary.token_usage_total,
        "model_quality_summary": summary.model_quality_summary,
        "suggested_next_step": summary.suggested_next_step,
        "next_command": summary.next_command,
        "patterns": summary.patterns,
        "memory_suggestions": summary.memory_suggestions,
    }


def export_patterns_json(patterns: list[ProjectPattern]) -> list[dict[str, Any]]:
    """Export patterns as safe JSON list."""
    return [
        {
            "pattern_id": p.pattern_id,
            "kind": p.kind,
            "count": p.count,
            "severity": p.severity,
            "summary": p.summary,
            "related_job_ids": p.related_job_ids,
            "related_file_paths": p.related_file_paths,
            "suggested_attention": p.suggested_attention,
        }
        for p in patterns
    ]


def export_memory_suggestions_json(suggestions: list[MemorySuggestion]) -> list[dict[str, Any]]:
    """Export memory suggestions as safe JSON list."""
    return [
        {
            "title": s.title,
            "summary": s.summary,
            "evidence_count": s.evidence_count,
            "related_job_ids": s.related_job_ids,
            "risk": s.risk,
            "recommended_scope": s.recommended_scope,
            "requires_approval": s.requires_approval,
        }
        for s in suggestions
    ]
