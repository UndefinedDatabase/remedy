"""
Memory Learn v0 — convert structured run evidence into memory entries.

Reads existing structured evidence (apply proofs, test results, command
discovery, readiness) and creates/updates memory entries. No raw content
stored — only safe structured summaries.

Idempotent: same key+source_id → update, not duplicate.

Public API::

    learn_from_job(job, events, *, approved) -> LearnResult
    export_learn_json(result) -> dict
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from packages.core.models import Job


@dataclass(frozen=True)
class LearnResult:
    """Result of a memory learn operation."""

    version: int
    job_id: str
    learned_count: int
    skipped_count: int
    entries: tuple[dict[str, str], ...]


def learn_from_job(
    job: Job,
    events: list[dict[str, Any]],
    *,
    approved: bool = False,
) -> LearnResult:
    """Extract structured evidence from job events and store as memory entries.

    Each extracted fact is stored via upsert_memory with source_id = job_id,
    ensuring idempotency.
    """
    from packages.memory.local_gateway import upsert_memory

    job_id = str(job.id)
    project_id = job.metadata.get("project_id")
    learned = 0
    skipped = 0
    entry_summaries: list[dict[str, str]] = []

    def _store(key: str, value: str, tags: list[str]) -> None:
        nonlocal learned, skipped
        try:
            _entry, created = upsert_memory(
                key, value,
                source_id=job_id,
                project_id=project_id,
                job_id=job_id if not project_id else None,
                tags=tags,
                source_type="system",
                approved=approved,
            )
            if created:
                learned += 1
            else:
                skipped += 1
            entry_summaries.append({"key": key, "value": value, "status": "created" if created else "updated"})
        except Exception:
            skipped += 1

    # 1. Test run completed → repo.test_command.primary, repo.last_verified_test
    test_runs = [e for e in events if e.get("event") == "test_run_completed"]
    if test_runs:
        last = test_runs[-1].get("metadata", {})
        cmd = last.get("command", "")
        status = last.get("status", "")
        if cmd:
            _store("repo.test_command.primary", cmd, ["test", "command"])
        if status:
            _store("repo.last_verified_test", status, ["test", "status"])

    # 2. Apply proof → patch.last_applied_target
    proofs = [e for e in events if e.get("event") == "patch_apply_proof_recorded"]
    if proofs:
        last = proofs[-1].get("metadata", {})
        target = last.get("target_path", "")
        if target:
            _store("patch.last_applied_target", target, ["patch", "apply"])

    # 3. Command discovery → context.command_discovery.sources
    disc = [e for e in events if e.get("event") == "command_discovery_completed"]
    if disc:
        meta = disc[-1].get("metadata", {})
        sources = meta.get("source_types", "")
        if isinstance(sources, list):
            sources = ", ".join(sources)
        count = meta.get("candidate_count", 0)
        if sources:
            _store("context.command_discovery.sources", str(sources), ["discovery", "command"])
        if count:
            _store("context.command_discovery.count", str(count), ["discovery", "count"])

    # 4. Readiness → project.autonomy_readiness.level
    try:
        from packages.orchestration.autonomy_readiness import assess_job_readiness
        report = assess_job_readiness(job, events)
        _store(
            "project.autonomy_readiness.level",
            str(report.highest_eligible_level),
            ["readiness", "autonomy"],
        )
    except Exception:
        pass

    # 5. Context coverage score
    try:
        from packages.orchestration.context_coverage import derive_context_coverage
        snap = derive_context_coverage(job, events)
        _store("context.coverage_score", str(snap.score), ["context", "coverage"])
    except Exception:
        pass

    # 6. Target repo basename
    target_repo = job.metadata.get("target_repo", "")
    if target_repo:
        import os
        basename = os.path.basename(target_repo.rstrip("/"))
        if basename:
            _store("repo.basename", basename, ["repo", "project"])

    return LearnResult(
        version=1,
        job_id=job_id,
        learned_count=learned,
        skipped_count=skipped,
        entries=tuple(entry_summaries),
    )


def export_learn_json(result: LearnResult) -> dict[str, Any]:
    """Export learn result as safe JSON dict."""
    return {
        "version": result.version,
        "job_id": result.job_id,
        "learned_count": result.learned_count,
        "skipped_count": result.skipped_count,
        "entries": list(result.entries),
    }
