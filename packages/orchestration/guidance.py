"""
Human Guidance Rail v1 — derive safe next-action cards from job state.

Each card tells the user what matters, why, and what safe command to run.
No raw content, no secrets, no execution — text suggestions only.

Public API::

    GuidanceCard (frozen dataclass)
    build_guidance_cards(job, events) -> list[GuidanceCard]
    export_guidance_json(job, cards) -> dict[str, Any]
    summarize_guidance(job, cards) -> str
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from packages.core.models import Job, RunState


@dataclass(frozen=True)
class GuidanceCard:
    """One actionable guidance item for the user."""

    id: str
    title: str
    severity: str  # "high", "medium", "low", "info"
    why_it_matters: str
    safe_next_action: str
    command: str
    related_node_type: str = ""


def build_guidance_cards(
    job: Job,
    events: list[dict[str, Any]],
) -> list[GuidanceCard]:
    """Derive guidance cards from current job state. No raw content."""
    cards: list[GuidanceCard] = []
    job_id = str(job.id)[:8]

    # 1. Readiness
    try:
        from packages.orchestration.autonomy_readiness import assess_readiness
        r = assess_readiness(job, events)
        level = r.get("level", 0)
        missing = r.get("missing", [])
        if missing:
            cards.append(GuidanceCard(
                id="readiness",
                title=f"Readiness level {level}",
                severity="medium" if level < 3 else "low",
                why_it_matters=f"{len(missing)} signal(s) missing for higher autonomy.",
                safe_next_action="Check readiness details.",
                command=f"remedy readiness job {job_id}",
                related_node_type="autonomy_readiness",
            ))
    except (ImportError, Exception):
        pass

    # 2. Decision queue
    try:
        from packages.orchestration.decision_queue import list_decisions, build_decision_summary
        decisions = list_decisions(job, events)
        summary = build_decision_summary(decisions)
        open_count = summary.get("open_count", 0)
        if open_count > 0:
            cards.append(GuidanceCard(
                id="decisions",
                title=f"{open_count} open decision(s)",
                severity="high",
                why_it_matters="Open decisions block autonomy progression.",
                safe_next_action="Review and resolve decisions.",
                command=f"remedy decision list {job_id}",
                related_node_type="decision_queue",
            ))
    except (ImportError, Exception):
        pass

    # 3. Stop reasons / blockers
    try:
        from packages.orchestration.stop_reasons import derive_stop_reasons
        reasons = derive_stop_reasons(job, events)
        if reasons:
            cards.append(GuidanceCard(
                id="blockers",
                title=f"{len(reasons)} blocker(s)",
                severity="high",
                why_it_matters="Blockers prevent job completion.",
                safe_next_action="Inspect blockers and resolve.",
                command=f"remedy blocker list {job_id}",
                related_node_type="stop_reason",
            ))
    except (ImportError, Exception):
        pass

    # 4. Token policy
    try:
        from packages.orchestration.token_policy import build_default_token_policy
        tp = build_default_token_policy(job)
        budget = tp.budget.get("expensive_tokens", 100_000)
        cards.append(GuidanceCard(
            id="token_policy",
            title="Token budget active",
            severity="info",
            why_it_matters=f"Budget: {budget:,} tokens.",
            safe_next_action="Review token policy.",
            command=f"remedy policy token {job_id} --json",
            related_node_type="token_policy",
        ))
    except (ImportError, Exception):
        pass

    # 5. Test status
    has_tests = any(t.status == RunState.COMPLETED for t in (job.tasks or []))
    failed_tasks = [t for t in (job.tasks or []) if t.status == RunState.FAILED]
    if failed_tasks:
        cards.append(GuidanceCard(
            id="test_status",
            title=f"{len(failed_tasks)} task(s) blocked",
            severity="high",
            why_it_matters="Blocked tasks need attention.",
            safe_next_action="Inspect blocked tasks.",
            command=f"remedy brain graph {job_id} --json",
            related_node_type="task",
        ))
    elif has_tests:
        cards.append(GuidanceCard(
            id="test_status",
            title="Tasks completed",
            severity="info",
            why_it_matters="All tasks completed successfully.",
            safe_next_action="Review brain graph for proof chain.",
            command=f"remedy brain graph {job_id}",
            related_node_type="task",
        ))

    # 6. Git status
    try:
        from packages.orchestration.git_status import read_job_git_status
        gs = read_job_git_status(job)
        if gs and gs.get("dirty"):
            cards.append(GuidanceCard(
                id="git_status",
                title="Working tree has changes",
                severity="medium",
                why_it_matters="Uncommitted changes may affect reproducibility.",
                safe_next_action="Review repo status.",
                command=f"remedy repo status {job_id}",
                related_node_type="git_status",
            ))
    except (ImportError, Exception):
        pass

    # 7. Dashboard
    cards.append(GuidanceCard(
        id="dashboard",
        title="View dashboard",
        severity="info",
        why_it_matters="Dashboard shows overall job health.",
        safe_next_action="Open job dashboard.",
        command=f"remedy dashboard job {job_id}",
        related_node_type="job",
    ))

    # 8. Brain viewer
    cards.append(GuidanceCard(
        id="viewer",
        title="Open brain viewer",
        severity="info",
        why_it_matters="Visual inspection of proof chain and decisions.",
        safe_next_action="Generate and open viewer.",
        command=f"remedy brain open {job_id}",
        related_node_type="job",
    ))

    return cards


def export_guidance_json(
    job: Job,
    cards: list[GuidanceCard],
) -> dict[str, Any]:
    """Export guidance as JSON-serialisable dict."""
    high = [c for c in cards if c.severity == "high"]
    return {
        "version": 1,
        "scope": "job",
        "job_id": str(job.id),
        "cards": [
            {
                "id": c.id,
                "title": c.title,
                "severity": c.severity,
                "why_it_matters": c.why_it_matters,
                "safe_next_action": c.safe_next_action,
                "command": c.command,
                "related_node_type": c.related_node_type,
            }
            for c in cards
        ],
        "summary": f"{len(cards)} guidance card(s), {len(high)} high severity.",
        "recommended_next_action": cards[0].command if cards else "",
    }


def summarize_guidance(job: Job, cards: list[GuidanceCard]) -> str:
    """Return human-readable guidance summary."""
    lines = [f"Guidance for job {str(job.id)[:8]}:", ""]
    for c in cards:
        marker = {"high": "!!", "medium": " !", "low": " -", "info": "  "}.get(c.severity, "  ")
        lines.append(f"  {marker} {c.title}")
        lines.append(f"     {c.why_it_matters}")
        lines.append(f"     > {c.command}")
        lines.append("")
    if not cards:
        lines.append("  No guidance cards.")
    return "\n".join(lines)
