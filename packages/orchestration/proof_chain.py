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
from pathlib import Path
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
    snapshot_verified: bool = False,
) -> str:
    """Classify proof status from chain state.

    Truth rules (strict):
    - verified: approved + applied + apply_event + proof + snapshot_verified + (linked test passed OR explicit not_required)
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

    # Verified requires full chain with linked evidence and verified snapshot (Step 1145)
    if (
        approval_state == "approved"
        and apply_state == "applied"
        and has_apply_event
        and has_proof
        and snapshot_verified
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
    test_missing_reason: str = "",
    snapshot_verified: bool = False,
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
    if apply_state == "applied" and not snapshot_verified:
        missing.append("no_snapshot_proof")
    if apply_state == "applied" and test_link == TEST_LINK_NONE:
        if test_missing_reason in ("test_order_unknown", "no_test_after_apply"):
            missing.append(test_missing_reason)
        elif test_state in ("not_tested", "passed", "failed"):
            missing.append("no_linked_test")
    return missing


# WHY: one task's folded apply answer travels with the two numbers behind it, so a
# reader can say "3 of 8 applied" instead of only "partial" (finding R-0738).
@dataclass(frozen=True)
class TaskApplyState:
    """One task's apply state, folded from its changes, plus the counts behind it."""

    state: str        # applied | reverted | not_applied | partial
    applied: int      # changes in this task whose apply_state is "applied"
    total: int        # changes in this task, the group size


def fold_task_apply_states(chain: Any) -> dict[str, TaskApplyState]:
    """Fold each task's changes to ONE apply state, keyed by the FULL task id.

    Lives here, beside the `ProofChange.apply_state` field it reads, because more than
    one reader needs the same answer: the cockpit's `_task_truth_maps` in
    `packages/orchestration/ui_server.py` and the run report. A reader importing the
    HTTP server module to learn a task's apply state would be the wrong dependency in
    the wrong direction. When *chain* is None the result is empty, and the caller
    reports "unknown".

    Finding R-0738. The apply fold agrees or it says "partial": unanimity for each
    confident answer, one distinct state reserved for the mixed case, the same shape
    the PROOF fold in the cockpit has. The membership test this replaces —
    `if "applied" in apply_states` — reported "applied" for a task where ONE change of
    eight had applied, indistinguishable from a task where all eight had, and
    hunk-level approval makes that mixed case the normal one. `grouped` is built by
    setdefault(...).append(...), so a task's list is never empty and the all() below
    cannot be vacuously true. ONLY the mixed case moved: the three unanimous inputs
    read exactly what the fold returned for them before the partial state existed, and
    the move out of `ui_server.py` changed no answer at all.
    """
    folded: dict[str, TaskApplyState] = {}
    if chain is None:
        return folded
    try:
        grouped: dict[str, list[Any]] = {}
        for c in chain.changes:
            tid = getattr(c, "task_id", "") or ""
            if not tid:
                continue
            grouped.setdefault(tid, []).append(c)
        state_by_task: dict[str, str] = {}
        for tid, changes in grouped.items():
            apply_states = [getattr(c, "apply_state", "") for c in changes]
            if all(s == "applied" for s in apply_states):
                state_by_task[tid] = "applied"
            elif all(s == "reverted" for s in apply_states):
                state_by_task[tid] = "reverted"
            elif not any(s in ("applied", "reverted") for s in apply_states):
                # Absorbs the getattr default "" exactly as the old `else` did: a
                # change with no apply_state attribute is not evidence of an apply.
                state_by_task[tid] = "not_applied"
            else:
                state_by_task[tid] = "partial"
            folded[tid] = TaskApplyState(
                state=state_by_task[tid],
                applied=sum(1 for s in apply_states if s == "applied"),
                total=len(apply_states),
            )
    except (ImportError, AttributeError, TypeError):
        # The same three classes the cockpit fold guarded, so a malformed chain
        # degrades to "unknown" here exactly as it did there.
        return {}
    return folded


# ---------------------------------------------------------------------------
# Test linking
# ---------------------------------------------------------------------------


_TIMESTAMP_KEYS = ("timestamp", "created_at", "completed_at", "applied_at")


def _parse_iso_timestamp(value: str) -> datetime | None:
    """Parse a timestamp only for ordering; never expose raw values."""
    try:
        normalized = value.replace("Z", "+00:00") if value.endswith("Z") else value
        parsed = datetime.fromisoformat(normalized)
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _event_timestamp(event_or_meta: dict[str, Any]) -> str | None:
    """Return a supported timestamp string from an event or metadata dict, or None."""
    for key in _TIMESTAMP_KEYS:
        value = event_or_meta.get(key)
        if isinstance(value, str) and _parse_iso_timestamp(value) is not None:
            return value
    meta = event_or_meta.get("metadata")
    if isinstance(meta, dict):
        for key in _TIMESTAMP_KEYS:
            value = meta.get(key)
            if isinstance(value, str) and _parse_iso_timestamp(value) is not None:
                return value
    return None


def _is_after_or_same(test_ts: str | None, apply_ts: str | None) -> bool | None:
    """Return whether test_ts >= apply_ts, or None when ordering is unknown."""
    if not test_ts or not apply_ts:
        return None
    test_time = _parse_iso_timestamp(test_ts)
    apply_time = _parse_iso_timestamp(apply_ts)
    if test_time is None or apply_time is None:
        return None
    return test_time >= apply_time


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

    # 3. Sole change — only if exactly one applied change and test is after apply
    saw_generic = False
    saw_unknown_order = False
    saw_before_apply = False
    if total_applied_changes == 1 and intent_id in apply_events:
        apply_event = apply_events[intent_id]
        apply_ts = _event_timestamp(apply_event)
        for te in test_events:
            meta = te.get("metadata", {})
            # Generic test (no intent_id/task_id) must be demonstrably after apply
            if not meta.get("intent_id") and not meta.get("task_id"):
                saw_generic = True
                ordering = _is_after_or_same(_event_timestamp(te), apply_ts)
                if ordering is True:
                    status = "passed" if meta.get("status") == "passed" else "failed"
                    return status, TEST_LINK_SOLE_CHANGE, meta
                if ordering is None:
                    saw_unknown_order = True
                else:
                    saw_before_apply = True

    if saw_generic and saw_unknown_order:
        return "not_tested", TEST_LINK_NONE, {"missing_link": "test_order_unknown"}
    if saw_generic and saw_before_apply:
        return "not_tested", TEST_LINK_NONE, {"missing_link": "no_test_after_apply"}

    return "not_tested", TEST_LINK_NONE, {}


# ---------------------------------------------------------------------------
# Next safe action (structured)
# ---------------------------------------------------------------------------

def _catalog_command_ids() -> frozenset[str]:
    """Return command ids from the actual CLI command catalog."""
    from apps.cli.command_catalog import CATALOG

    return frozenset(cmd.command_id for cmd in CATALOG)


# Backward-compatible constant for tests and callers; derived from actual catalog.
_CATALOG_COMMANDS = _catalog_command_ids()


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
        if catalog_id not in _catalog_command_ids():
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
            label="Approve or reject intent.",
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
    data_dir: Path | None = None,
) -> ProofChain:
    """Build proof chain from job and events.

    Deterministic, read-only. No LLM, no network.

    When *data_dir* is provided, apply/revert state and snapshot verification are
    taken from the authoritative snapshot-truth builder (build_snapshot_truth)
    rather than artifact metadata or events (Step 1158). Artifact metadata is a
    compatibility fallback only; event presence is never authoritative for the
    snapshot fact. A reverted apply is not "currently applied"; a drift-blocked
    revert leaves the apply active and provable; a partial/failed revert blocks
    the verified state.
    """
    from packages.orchestration.approval_queue import list_patch_intents
    from packages.orchestration.change_set import derive_change_set

    job_id_str = str(job.id)
    goal = job.user_prompt or job.name or ""
    if len(goal) > 200:
        goal = goal[:200] + "…"

    changes_all = derive_change_set(job, events)
    total_applied = sum(1 for c in changes_all if c.apply.get("applied"))
    changes_raw = changes_all
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
        elif ename in ("test_run_completed", "test_run_timed_out"):
            all_test_events.append(ev)
        elif ename == "patch_intent_applied" and iid:
            apply_event_map[iid] = ev

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
        test_state, test_link, test_meta = _link_test_to_change(
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

        # Snapshot fact: artifact metadata is the fallback; the durable
        # snapshot-truth builder is authoritative when data_dir is available.
        _snap_ver = c.proof.get("snapshot_verified", False)
        if data_dir is not None:
            from packages.orchestration.repository_snapshot import build_snapshot_truth
            truth = build_snapshot_truth(job_id_str, intent_id=c.intent_id, data_dir=data_dir)
            if truth.apply_state != "unknown":
                # Reverted apply is not currently applied.
                if truth.apply_state == "reverted":
                    apply_state = "reverted"
                elif truth.apply_state == "applied":
                    apply_state = "applied"
                # Verified snapshot fact comes from live manifest/blob check.
                _snap_ver = truth.snapshot_verified_now
                # Partial/failed revert can never back a verified state.
                if truth.revert_state in ("partial_revert", "revert_failed"):
                    _snap_ver = False
                # Degraded recovery evidence cannot back a verified state.
                if truth.evidence_status == "degraded":
                    _snap_ver = False
            elif apply_state == "applied" or "no_apply_record" in truth.blockers:
                # The authority has no durable record while the artifact claims an
                # apply occurred. Asking and getting "no record" is evidence loss —
                # never trust the artifact's snapshot_verified claim here (R-0066).
                _snap_ver = False

        proof_status = _classify_proof_status(
            approval_state=approval_state,
            apply_state=apply_state,
            test_state=test_state,
            test_link=test_link,
            has_proof=has_proof,
            has_apply_event=has_apply_event,
            task_blocked=task_blocked,
            task_failed=task_failed,
            snapshot_verified=_snap_ver,
        )
        missing = _derive_missing_links(
            approval_state=approval_state,
            apply_state=apply_state,
            test_state=test_state,
            test_link=test_link,
            has_proof=has_proof,
            has_apply_event=has_apply_event,
            test_missing_reason=str(test_meta.get("missing_link", "")),
            snapshot_verified=_snap_ver,
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
