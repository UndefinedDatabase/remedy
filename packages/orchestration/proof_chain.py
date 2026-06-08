"""
Proof Chain v2 — "Why did this happen, and is it proven?"

Builds a compact safe chain:
  Goal → Job → Task → Artifact → Patch Intent → Approval → Apply → Test → Proof

Derived from existing structured records — no new persistence layer.
No raw content, diffs, approval reasons, stdout/stderr, or file contents.

Truth guarantee: "verified" requires linked approval + apply + proof + passed
or explicitly not-required test evidence. Test absence is never treated as verified.

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

# Test link types — how test evidence connects to a change
TEST_LINK_NONE = "none"
TEST_LINK_INTENT = "intent_linked"
TEST_LINK_TASK = "task_linked"
TEST_LINK_SOLE_CHANGE = "sole_change"
TEST_LINK_NOT_REQUIRED = "explicit_not_required"


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class NextSafeAction:
    """Structured next action recommendation."""

    label: str
    command: str
    reason: str
    available: bool


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
    test_state: str           # not_tested | passed | failed | not_required
    test_link: str            # none | intent_linked | task_linked | sole_change | explicit_not_required
    proof_status: str         # verified | failed | incomplete | unverified | not_applicable
    safe_summary: str
    next_safe_action: str     # legacy string for text output
    next_safe_action_obj: NextSafeAction | None = None
    missing_links: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ProofChain:
    """Full proof chain for a job, optionally filtered by path."""

    job_id: str
    goal: str
    path_filter: str
    changes: tuple[ProofChange, ...]
    overall_status: str       # verified | failed | incomplete | unverified
    next_safe_action: str     # legacy string
    next_safe_action_obj: NextSafeAction | None = None
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
    test_link: str,
    has_proof: bool,
    has_apply_event: bool,
    task_blocked: bool,
    task_failed: bool,
) -> str:
    """Classify proof status from chain state.

    Truth rules (strict):
    - verified: approved + applied + apply_event + proof + (linked test passed OR explicit not_required)
    - failed: applied + (linked test failed OR task blocked/failed)
    - incomplete: intent exists but chain not complete
    - unverified: change exists but required linkage cannot be established
    - not_applicable: rejected
    """
    if approval_state == "rejected":
        return PROOF_NOT_APPLICABLE

    if task_blocked or task_failed:
        return PROOF_FAILED

    if apply_state == "applied" and test_state == "failed" and test_link != TEST_LINK_NONE:
        return PROOF_FAILED

    # Verified requires full chain with linked evidence
    if (
        approval_state == "approved"
        and apply_state == "applied"
        and has_apply_event
        and has_proof
        and test_state in ("passed", "not_required")
        and test_link != TEST_LINK_NONE
    ):
        return PROOF_VERIFIED

    # Incomplete: some chain present but not all links
    if approval_state == "pending":
        return PROOF_INCOMPLETE
    if approval_state == "approved" and apply_state == "not_applied":
        return PROOF_INCOMPLETE
    if apply_state == "applied" and not has_apply_event:
        return PROOF_INCOMPLETE
    if apply_state == "applied" and not has_proof:
        return PROOF_INCOMPLETE
    if apply_state == "applied" and has_proof and test_state == "not_tested":
        return PROOF_INCOMPLETE
    if apply_state == "applied" and has_proof and test_state in ("passed", "failed") and test_link == TEST_LINK_NONE:
        return PROOF_INCOMPLETE

    return PROOF_UNVERIFIED


def _derive_missing_links(
    *,
    approval_state: str,
    apply_state: str,
    test_state: str,
    test_link: str,
    has_proof: bool,
    has_apply_event: bool,
) -> list[str]:
    """List what's missing from the proof chain."""
    missing: list[str] = []
    if approval_state == "pending":
        missing.append("approval_pending")
    if approval_state == "approved" and apply_state == "not_applied":
        missing.append("not_applied")
    if apply_state == "applied" and not has_apply_event:
        missing.append("no_apply_event")
    if apply_state == "applied" and not has_proof:
        missing.append("no_apply_proof")
    if apply_state == "applied" and test_state == "not_tested":
        missing.append("no_linked_test")
    if apply_state == "applied" and test_state in ("passed", "failed") and test_link == TEST_LINK_NONE:
        missing.append("test_not_linked_to_change")
    return missing


# ---------------------------------------------------------------------------
# Test linking
# ---------------------------------------------------------------------------


def _link_test_to_change(
    *,
    intent_id: str,
    task_id: str,
    test_events: list[dict[str, Any]],
    apply_events: dict[str, dict[str, Any]],
    total_applied_changes: int,
) -> tuple[str, str, dict[str, Any]]:
    """Link test evidence to a specific change. Returns (test_state, test_link, test_meta).

    Linking rules (in priority order):
    1. Test event has intent_id matching this change → intent_linked
    2. Test event has task_id matching this change → task_linked
    3. Job has exactly one applied change and test ran after apply → sole_change
    4. Otherwise → no link (test_state="not_tested", test_link="none")
    """
    # Check for explicit not-required evidence
    for te in test_events:
        meta = te.get("metadata", {})
        if meta.get("test_not_required") and meta.get("intent_id") == intent_id:
            return "not_required", TEST_LINK_NOT_REQUIRED, meta

    # 1. Intent-linked test
    for te in test_events:
        meta = te.get("metadata", {})
        if meta.get("intent_id") == intent_id:
            status = "passed" if meta.get("status") == "passed" else "failed"
            return status, TEST_LINK_INTENT, meta

    # 2. Task-linked test
    if task_id:
        for te in test_events:
            meta = te.get("metadata", {})
            if meta.get("task_id") == task_id:
                status = "passed" if meta.get("status") == "passed" else "failed"
                return status, TEST_LINK_TASK, meta

    # 3. Sole change — only if exactly one applied change in job
    if total_applied_changes == 1 and intent_id in apply_events:
        for te in test_events:
            meta = te.get("metadata", {})
            # Generic test (no intent_id/task_id) after apply
            if not meta.get("intent_id") and not meta.get("task_id"):
                status = "passed" if meta.get("status") == "passed" else "failed"
                return status, TEST_LINK_SOLE_CHANGE, meta

    return "not_tested", TEST_LINK_NONE, {}


# ---------------------------------------------------------------------------
# Next safe action (structured)
# ---------------------------------------------------------------------------

# Valid catalog commands referenced by next actions
_CATALOG_COMMANDS = frozenset({
    "patch.approve", "patch.reject", "patch.apply",
    "change.proof", "change.list", "change.show",
    "file.why", "test.run",
})


def _make_next_action(
    *,
    label: str,
    command: str = "",
    reason: str = "",
    available: bool = True,
) -> NextSafeAction:
    """Create structured next action, validating command exists."""
    if command:
        # Extract catalog command from CLI string (e.g., "remedy change proof ..." → "change.proof")
        parts = command.replace("remedy ", "").split()
        if len(parts) >= 2:
            catalog_id = f"{parts[0]}.{parts[1]}"
        elif len(parts) == 1:
            catalog_id = parts[0]
        else:
            catalog_id = ""
        if catalog_id not in _CATALOG_COMMANDS:
            command = ""
            available = False
    return NextSafeAction(label=label, command=command, reason=reason, available=available)


def _derive_change_next_action(
    *,
    intent_id: str,
    job_id: str,
    approval_state: str,
    apply_state: str,
    test_state: str,
    test_link: str,
    proof_status: str,
) -> tuple[str, NextSafeAction]:
    """Derive next safe action for a single change. Returns (label_str, NextSafeAction)."""
    if proof_status == PROOF_VERIFIED:
        obj = _make_next_action(label="No action needed.", reason="Change verified.")
        return obj.label, obj
    if proof_status == PROOF_NOT_APPLICABLE:
        obj = _make_next_action(label="No action needed (rejected).", reason="Intent rejected.")
        return obj.label, obj
    if approval_state == "pending":
        cmd = f"remedy patch approve {job_id} {intent_id}"
        obj = _make_next_action(
            label=f"Approve or reject intent.",
            command=cmd, reason="Approval pending.",
        )
        return obj.label, obj
    if approval_state == "approved" and apply_state == "not_applied":
        cmd = f"remedy patch apply {job_id} {intent_id}"
        obj = _make_next_action(
            label="Apply the approved patch intent.",
            command=cmd, reason="Approved but not applied.",
        )
        return obj.label, obj
    if apply_state == "applied" and test_state == "not_tested":
        obj = _make_next_action(
            label="Run tests to verify the change.",
            command=f"remedy test run {job_id}",
            reason="Applied but no linked test evidence.",
        )
        return obj.label, obj
    if apply_state == "applied" and test_link == TEST_LINK_NONE and test_state in ("passed", "failed"):
        obj = _make_next_action(
            label="Run tests linked to this change.",
            command=f"remedy test run {job_id}",
            reason="Test ran but not linked to this change.",
        )
        return obj.label, obj
    if test_state == "failed":
        cmd = f"remedy change proof {job_id}"
        obj = _make_next_action(
            label="Investigate test failure.",
            command=cmd, reason="Linked test failed.",
        )
        return obj.label, obj
    cmd = f"remedy change proof {job_id}"
    obj = _make_next_action(
        label="Review proof chain.",
        command=cmd, reason="Proof chain incomplete or unverified.",
    )
    return obj.label, obj


def derive_next_safe_action_from_changes(
    changes: list[ProofChange],
    job_id: str,
) -> tuple[str, NextSafeAction]:
    """Derive overall next safe action. Returns (label_str, NextSafeAction)."""
    if not changes:
        obj = _make_next_action(label="No changes to verify.", reason="No patch intents found.")
        return obj.label, obj

    pending = [c for c in changes if c.approval_state == "pending"]
    if pending:
        cmd = f"remedy change list {job_id}"
        obj = _make_next_action(
            label=f"Approve {len(pending)} pending intent(s).",
            command=cmd, reason="Intents awaiting approval.",
        )
        return obj.label, obj

    unapplied = [c for c in changes if c.apply_state == "not_applied" and c.approval_state == "approved"]
    if unapplied:
        obj = _make_next_action(
            label=f"Apply {len(unapplied)} approved intent(s).",
            reason="Approved intents not yet applied.",
        )
        return obj.label, obj

    untested = [c for c in changes if c.apply_state == "applied" and c.test_state == "not_tested"]
    if untested:
        obj = _make_next_action(
            label="Run tests to verify applied changes.",
            command=f"remedy test run {job_id}",
            reason="Applied changes with no linked test evidence.",
        )
        return obj.label, obj

    failed = [c for c in changes if c.proof_status == PROOF_FAILED]
    if failed:
        cmd = f"remedy change proof {job_id}"
        obj = _make_next_action(
            label=f"Investigate {len(failed)} failed change(s).",
            command=cmd, reason="Changes with failed tests or blocked tasks.",
        )
        return obj.label, obj

    if all(c.proof_status in (PROOF_VERIFIED, PROOF_NOT_APPLICABLE) for c in changes):
        obj = _make_next_action(label="All changes verified. No action needed.", reason="Full proof chain complete.")
        return obj.label, obj

    cmd = f"remedy change proof {job_id}"
    obj = _make_next_action(
        label="Review proof chain.",
        command=cmd, reason="Some changes unverified or incomplete.",
    )
    return obj.label, obj


def derive_next_safe_action(chain: ProofChain) -> str:
    """Convenience wrapper for ProofChain."""
    return chain.next_safe_action


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

    # Index events
    task_exec_events: dict[str, dict] = {}
    all_test_events: list[dict] = []
    apply_event_map: dict[str, dict] = {}

    for ev in events:
        ename = ev.get("event", "")
        meta = ev.get("metadata", {})
        tid = meta.get("task_id", "")
        iid = meta.get("intent_id", "")
        if ename in ("task_execution_completed", "task_execution_blocked", "task_execution_failed"):
            if tid:
                task_exec_events[tid] = {"event": ename, "meta": meta}
        elif ename == "test_run_completed":
            all_test_events.append(ev)
        elif ename == "patch_intent_applied" and iid:
            apply_event_map[iid] = meta

    # Build intent → task/artifact mapping
    intents = list_patch_intents(job)
    intent_map: dict[str, dict] = {}
    for i in intents:
        intent_map[i["intent_id"]] = i

    # Build task title map
    task_titles: dict[str, str] = {}
    for t in job.tasks:
        task_titles[str(t.id)] = t.description[:100] if t.description else ""

    # Count total applied changes for sole_change linking
    total_applied = sum(1 for c in changes_raw if c.apply.get("applied"))

    proof_changes: list[ProofChange] = []
    for c in changes_raw:
        intent_info = intent_map.get(c.intent_id, {})
        task_id = intent_info.get("task_id", "") or ""
        artifact_id = intent_info.get("artifact_id", "")
        task_title = task_titles.get(task_id, "")

        # Derive states
        approval_state = c.approval.get("state", "pending")
        apply_state = "applied" if c.apply.get("applied") else "not_applied"
        if c.revert.get("reverted"):
            apply_state = "reverted"

        has_proof = c.proof.get("recorded", False)
        has_apply_event = c.intent_id in apply_event_map

        # Link test to this specific change
        test_state, test_link, _test_meta = _link_test_to_change(
            intent_id=c.intent_id,
            task_id=task_id,
            test_events=all_test_events,
            apply_events=apply_event_map,
            total_applied_changes=total_applied,
        )

        # Task execution state
        task_ev = task_exec_events.get(task_id, {})
        task_blocked = task_ev.get("event") == "task_execution_blocked"
        task_failed = task_ev.get("event") == "task_execution_failed"

        proof_status = _classify_proof_status(
            approval_state=approval_state,
            apply_state=apply_state,
            test_state=test_state,
            test_link=test_link,
            has_proof=has_proof,
            has_apply_event=has_apply_event,
            task_blocked=task_blocked,
            task_failed=task_failed,
        )
        missing = _derive_missing_links(
            approval_state=approval_state,
            apply_state=apply_state,
            test_state=test_state,
            test_link=test_link,
            has_proof=has_proof,
            has_apply_event=has_apply_event,
        )

        # Safe summary
        safe_summary = f"{c.target_path}: {proof_status}"
        if missing:
            safe_summary += f" (missing: {', '.join(missing)})"

        # Per-change next action
        next_label, next_obj = _derive_change_next_action(
            intent_id=c.intent_id,
            job_id=job_id_str,
            approval_state=approval_state,
            apply_state=apply_state,
            test_state=test_state,
            test_link=test_link,
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
            test_link=test_link,
            proof_status=proof_status,
            safe_summary=safe_summary,
            next_safe_action=next_label,
            next_safe_action_obj=next_obj,
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

    overall_label, overall_obj = derive_next_safe_action_from_changes(proof_changes, job_id_str)

    return ProofChain(
        job_id=job_id_str,
        goal=goal,
        path_filter=path or "",
        changes=tuple(proof_changes),
        overall_status=overall,
        next_safe_action=overall_label,
        next_safe_action_obj=overall_obj,
        missing_links=all_missing,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------


def _export_next_action(obj: NextSafeAction | None) -> dict[str, Any]:
    """Export NextSafeAction as safe dict."""
    if obj is None:
        return {"label": "", "command": "", "reason": "", "available": False}
    return {
        "label": obj.label,
        "command": obj.command,
        "reason": obj.reason,
        "available": obj.available,
    }


def export_proof_chain_json(chain: ProofChain) -> dict[str, Any]:
    """Export proof chain as safe JSON dict."""
    return {
        "version": 2,
        "job_id": chain.job_id,
        "goal": chain.goal,
        "path_filter": chain.path_filter,
        "overall_status": chain.overall_status,
        "next_safe_action": chain.next_safe_action,
        "next_safe_action_obj": _export_next_action(chain.next_safe_action_obj),
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
                "test_link": c.test_link,
                "proof_status": c.proof_status,
                "safe_summary": c.safe_summary,
                "next_safe_action": c.next_safe_action,
                "next_safe_action_obj": _export_next_action(c.next_safe_action_obj),
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
            lines.append(f"       intent={c.intent_id}  approval={c.approval_state}  apply={c.apply_state}  test={c.test_state}  test_link={c.test_link}")
            if c.missing_links:
                lines.append(f"       missing: {', '.join(c.missing_links)}")
            lines.append(f"       next: {c.next_safe_action}")
    else:
        lines.append("\nNo changes found.")

    return "\n".join(lines)
