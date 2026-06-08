"""
Proof Chain v1 — "Why did this happen, and is it proven?"

Builds a compact safe chain:
  Goal → Job → Task → Artifact → Patch Intent → Approval → Apply → Test → Proof

Derived from existing structured records — no new persistence layer.
No raw content, diffs, approval reasons, stdout/stderr, or file contents.

Public API::

    build_proof_chain(job, events, path=None) -> ProofChain
    export_proof_chain_json(chain) -> dict
    summarize_proof_chain(chain) -> str
    derive_next_safe_action(chain) -> str
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from packages.core.models import Job


# ---------------------------------------------------------------------------
# Proof status enum
# ---------------------------------------------------------------------------

PROOF_VERIFIED = "verified"
PROOF_FAILED = "failed"
PROOF_INCOMPLETE = "incomplete"
PROOF_UNVERIFIED = "unverified"
PROOF_NOT_APPLICABLE = "not_applicable"

_VALID_STATUSES = frozenset({
    PROOF_VERIFIED, PROOF_FAILED, PROOF_INCOMPLETE,
    PROOF_UNVERIFIED, PROOF_NOT_APPLICABLE,
})


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ProofChange:
    """One change with full proof chain linkage."""

    target_path: str
    intent_id: str
    task_id: str
    task_title: str
    artifact_id: str
    patch_intent_id: str
    approval_state: str       # pending | approved | rejected
    apply_state: str          # not_applied | applied | reverted
    test_state: str           # not_tested | passed | failed
    proof_status: str         # verified | failed | incomplete | unverified
    safe_summary: str
    next_safe_action: str
    missing_links: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ProofChain:
    """Full proof chain for a job, optionally filtered by path."""

    job_id: str
    goal: str
    path_filter: str
    changes: tuple[ProofChange, ...]
    overall_status: str       # verified | failed | incomplete | unverified
    next_safe_action: str
    missing_links: list[str] = field(default_factory=list)
    generated_at: str = ""


# ---------------------------------------------------------------------------
# Truth rules
# ---------------------------------------------------------------------------


def _classify_proof_status(
    *,
    approval_state: str,
    apply_state: str,
    test_state: str,
    has_proof: bool,
    task_blocked: bool,
    task_failed: bool,
) -> str:
    """Classify proof status from chain state.

    Truth rules:
    - verified: approved + applied + proof exists + (test passed OR test not required)
    - failed: applied + (test failed OR task blocked/failed)
    - incomplete: intent exists but chain not complete
    - unverified: change exists but cannot link to proof
    """
    if task_blocked or task_failed:
        return PROOF_FAILED

    if apply_state == "applied" and test_state == "failed":
        return PROOF_FAILED

    if (
        approval_state == "approved"
        and apply_state == "applied"
        and has_proof
        and test_state in ("passed", "not_tested")
    ):
        return PROOF_VERIFIED

    if approval_state == "rejected":
        return PROOF_NOT_APPLICABLE

    # Incomplete: some chain present but not all links
    if approval_state == "pending":
        return PROOF_INCOMPLETE
    if approval_state == "approved" and apply_state == "not_applied":
        return PROOF_INCOMPLETE
    if apply_state == "applied" and not has_proof:
        return PROOF_INCOMPLETE
    if apply_state == "applied" and has_proof and test_state == "not_tested":
        # Has proof but no test yet — still verified if test not required
        return PROOF_VERIFIED

    return PROOF_UNVERIFIED


def _derive_missing_links(
    *,
    approval_state: str,
    apply_state: str,
    test_state: str,
    has_proof: bool,
) -> list[str]:
    """List what's missing from the proof chain."""
    missing: list[str] = []
    if approval_state == "pending":
        missing.append("approval_pending")
    if approval_state == "approved" and apply_state == "not_applied":
        missing.append("not_applied")
    if apply_state == "applied" and not has_proof:
        missing.append("no_apply_proof")
    if apply_state == "applied" and test_state == "not_tested":
        missing.append("not_tested")
    return missing


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


def build_proof_chain(
    job: Job,
    events: list[dict[str, Any]],
    path: str | None = None,
) -> ProofChain:
    """Build proof chain from job and events.

    Deterministic, read-only. No LLM, no network, no filesystem.
    """
    from packages.orchestration.approval_queue import list_patch_intents
    from packages.orchestration.change_set import derive_change_set

    job_id_str = str(job.id)
    goal = job.user_prompt or job.name or ""
    if len(goal) > 200:
        goal = goal[:200] + "…"

    changes_raw = derive_change_set(job, events)
    if path:
        changes_raw = [c for c in changes_raw if c.target_path == path]

    # Index events for task/execution state
    task_exec_events: dict[str, dict] = {}
    for ev in events:
        ename = ev.get("event", "")
        meta = ev.get("metadata", {})
        tid = meta.get("task_id", "")
        if ename in ("task_execution_completed", "task_execution_blocked", "task_execution_failed"):
            if tid:
                task_exec_events[tid] = {"event": ename, "meta": meta}

    # Build intent → task/artifact mapping
    intents = list_patch_intents(job)
    intent_map: dict[str, dict] = {}
    for i in intents:
        intent_map[i["intent_id"]] = i

    # Build task title map
    task_titles: dict[str, str] = {}
    for t in job.tasks:
        task_titles[str(t.id)] = t.description[:100] if t.description else ""

    proof_changes: list[ProofChange] = []
    for c in changes_raw:
        intent_info = intent_map.get(c.intent_id, {})
        task_id = intent_info.get("task_id", "")
        artifact_id = intent_info.get("artifact_id", "")
        task_title = task_titles.get(task_id, "")

        # Derive states
        approval_state = c.approval.get("state", "pending")
        apply_state = "applied" if c.apply.get("applied") else "not_applied"
        if c.revert.get("reverted"):
            apply_state = "reverted"

        has_proof = c.proof.get("recorded", False)

        # Test state
        if c.test.get("ran"):
            test_status = c.test.get("status", "")
            test_state = "passed" if test_status == "passed" else "failed"
        else:
            test_state = "not_tested"

        # Task execution state
        task_ev = task_exec_events.get(task_id, {})
        task_blocked = task_ev.get("event") == "task_execution_blocked"
        task_failed = task_ev.get("event") == "task_execution_failed"

        proof_status = _classify_proof_status(
            approval_state=approval_state,
            apply_state=apply_state,
            test_state=test_state,
            has_proof=has_proof,
            task_blocked=task_blocked,
            task_failed=task_failed,
        )
        missing = _derive_missing_links(
            approval_state=approval_state,
            apply_state=apply_state,
            test_state=test_state,
            has_proof=has_proof,
        )

        # Safe summary
        safe_summary = f"{c.target_path}: {proof_status}"
        if missing:
            safe_summary += f" (missing: {', '.join(missing)})"

        # Per-change next action
        next_action = _derive_change_next_action(
            intent_id=c.intent_id,
            job_id=job_id_str,
            approval_state=approval_state,
            apply_state=apply_state,
            test_state=test_state,
            proof_status=proof_status,
        )

        proof_changes.append(ProofChange(
            target_path=c.target_path,
            intent_id=c.intent_id,
            task_id=task_id,
            task_title=task_title,
            artifact_id=artifact_id,
            patch_intent_id=c.intent_id,
            approval_state=approval_state,
            apply_state=apply_state,
            test_state=test_state,
            proof_status=proof_status,
            safe_summary=safe_summary,
            next_safe_action=next_action,
            missing_links=missing,
        ))

    # Overall status
    if not proof_changes:
        overall = PROOF_NOT_APPLICABLE
    elif any(c.proof_status == PROOF_FAILED for c in proof_changes):
        overall = PROOF_FAILED
    elif all(c.proof_status in (PROOF_VERIFIED, PROOF_NOT_APPLICABLE) for c in proof_changes):
        overall = PROOF_VERIFIED
    elif any(c.proof_status == PROOF_INCOMPLETE for c in proof_changes):
        overall = PROOF_INCOMPLETE
    else:
        overall = PROOF_UNVERIFIED

    all_missing: list[str] = []
    for c in proof_changes:
        for m in c.missing_links:
            if m not in all_missing:
                all_missing.append(m)

    return ProofChain(
        job_id=job_id_str,
        goal=goal,
        path_filter=path or "",
        changes=tuple(proof_changes),
        overall_status=overall,
        next_safe_action=derive_next_safe_action_from_changes(proof_changes, job_id_str),
        missing_links=all_missing,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )


# ---------------------------------------------------------------------------
# Next safe action
# ---------------------------------------------------------------------------


def _derive_change_next_action(
    *,
    intent_id: str,
    job_id: str,
    approval_state: str,
    apply_state: str,
    test_state: str,
    proof_status: str,
) -> str:
    """Derive next safe action for a single change."""
    if proof_status == PROOF_VERIFIED:
        return "No action needed."
    if proof_status == PROOF_NOT_APPLICABLE:
        return "No action needed (rejected)."
    if approval_state == "pending":
        return f"Approve or reject: remedy patch approve {job_id} {intent_id}"
    if approval_state == "approved" and apply_state == "not_applied":
        return "Apply the approved patch intent."
    if apply_state == "applied" and test_state == "not_tested":
        return "Run tests to verify the change."
    if test_state == "failed":
        return f"Investigate test failure: remedy change proof {job_id}"
    return f"Review proof chain: remedy change proof {job_id}"


def derive_next_safe_action_from_changes(
    changes: list[ProofChange],
    job_id: str,
) -> str:
    """Derive overall next safe action from proof chain changes."""
    if not changes:
        return "No changes to verify."

    pending = [c for c in changes if c.approval_state == "pending"]
    if pending:
        return f"Approve {len(pending)} pending intent(s): remedy change list {job_id}"

    unapplied = [c for c in changes if c.apply_state == "not_applied" and c.approval_state == "approved"]
    if unapplied:
        return f"Apply {len(unapplied)} approved intent(s)."

    untested = [c for c in changes if c.apply_state == "applied" and c.test_state == "not_tested"]
    if untested:
        return "Run tests to verify applied changes."

    failed = [c for c in changes if c.proof_status == PROOF_FAILED]
    if failed:
        return f"Investigate {len(failed)} failed change(s): remedy change proof {job_id}"

    if all(c.proof_status in (PROOF_VERIFIED, PROOF_NOT_APPLICABLE) for c in changes):
        return "All changes verified. No action needed."

    return f"Review proof chain: remedy change proof {job_id}"


def derive_next_safe_action(chain: ProofChain) -> str:
    """Convenience wrapper for ProofChain."""
    return chain.next_safe_action


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------


def export_proof_chain_json(chain: ProofChain) -> dict[str, Any]:
    """Export proof chain as safe JSON dict."""
    return {
        "version": 1,
        "job_id": chain.job_id,
        "goal": chain.goal,
        "path_filter": chain.path_filter,
        "overall_status": chain.overall_status,
        "next_safe_action": chain.next_safe_action,
        "missing_links": chain.missing_links,
        "generated_at": chain.generated_at,
        "changes": [
            {
                "target_path": c.target_path,
                "intent_id": c.intent_id,
                "task_id": c.task_id,
                "task_title": c.task_title,
                "artifact_id": c.artifact_id,
                "approval_state": c.approval_state,
                "apply_state": c.apply_state,
                "test_state": c.test_state,
                "proof_status": c.proof_status,
                "safe_summary": c.safe_summary,
                "next_safe_action": c.next_safe_action,
                "missing_links": c.missing_links,
            }
            for c in chain.changes
        ],
    }


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------


def summarize_proof_chain(chain: ProofChain) -> str:
    """Human-readable proof chain summary."""
    lines: list[str] = []
    lines.append(f"Proof Chain: {chain.job_id[:8]}")
    if chain.goal:
        lines.append(f"Goal: {chain.goal[:120]}")
    if chain.path_filter:
        lines.append(f"Path filter: {chain.path_filter}")
    lines.append(f"Overall: {chain.overall_status}")
    lines.append(f"Next: {chain.next_safe_action}")

    if chain.missing_links:
        lines.append(f"Missing: {', '.join(chain.missing_links)}")

    if chain.changes:
        lines.append(f"\nChanges ({len(chain.changes)}):")
        for c in chain.changes:
            status_icon = {
                PROOF_VERIFIED: "[OK]",
                PROOF_FAILED: "[FAIL]",
                PROOF_INCOMPLETE: "[...]",
                PROOF_UNVERIFIED: "[?]",
                PROOF_NOT_APPLICABLE: "[N/A]",
            }.get(c.proof_status, "[?]")
            lines.append(f"  {status_icon} {c.target_path}")
            lines.append(f"       intent={c.intent_id}  approval={c.approval_state}  apply={c.apply_state}  test={c.test_state}")
            if c.missing_links:
                lines.append(f"       missing: {', '.join(c.missing_links)}")
            lines.append(f"       next: {c.next_safe_action}")
    else:
        lines.append("\nNo changes found.")

    return "\n".join(lines)
