"""
Change Set / Review Board v0 — derived review surface for proof chains.

Groups patch_intent + approval + apply + proof + test + revert + memory
into a single reviewable change object per intent.

Derived from existing structured records — no new persistence layer.
No raw content, diffs, approval reasons, stdout/stderr, or file contents.

Public API::

    derive_change_set(job, events) -> list[ChangeEntry]
    export_change_list_json(job_id, changes) -> dict
    export_change_show_json(job_id, entry) -> dict
    summarize_change_list(changes) -> str
    summarize_change_show(entry) -> str
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from packages.core.models import Job


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ChangeEntry:
    """One reviewable change — groups all proof chain data for an intent."""

    intent_id: str
    target_path: str
    risk: str
    status: str  # pending | approved | applied | reverted | rejected
    approval: dict[str, Any]
    apply: dict[str, Any]
    proof: dict[str, Any]
    test: dict[str, Any]
    revert: dict[str, Any]
    memory: list[str]  # related memory keys


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def derive_change_set(
    job: Job,
    events: list[dict[str, Any]],
) -> list[ChangeEntry]:
    """Derive change entries from job artifacts and run-log events.

    Deterministic, read-only. No LLM, no network, no filesystem.
    """
    from packages.orchestration.approval_queue import list_patch_intents

    intents = list_patch_intents(job)
    if not intents:
        return []

    # Index events by intent_id
    apply_events: dict[str, dict] = {}
    apply_event_records: dict[str, dict] = {}
    proof_events: dict[str, dict] = {}
    test_events: list[dict] = []
    revert_events: dict[str, dict] = {}

    for ev in events:
        meta = ev.get("metadata", {})
        ename = ev.get("event", "")
        iid = meta.get("intent_id", "")
        if ename == "patch_intent_applied" and iid:
            apply_events[iid] = meta
            apply_event_records[iid] = ev
        elif ename == "patch_apply_proof_recorded" and iid:
            proof_events[iid] = meta
        elif ename == "test_run_completed":
            test_events.append(ev)
        elif ename == "patch_intent_reverted" and iid:
            revert_events[iid] = meta

    # Memory keys from events
    memory_keys: list[str] = []
    for ev in events:
        if ev.get("event") == "memory_learned":
            k = ev.get("metadata", {}).get("key", "")
            if k:
                memory_keys.append(k)

    total_applied = len(apply_events)

    entries: list[ChangeEntry] = []
    for intent in intents:
        iid = intent["intent_id"]
        state = intent.get("state", "pending")
        target_path = intent.get("target_path", "")
        risk = intent.get("risk", "unknown")

        # Determine overall status
        if iid in revert_events:
            status = "reverted"
        elif iid in apply_events:
            status = "applied"
        elif state == "approved":
            status = "approved"
        elif state == "rejected":
            status = "rejected"
        else:
            status = "pending"

        # Approval info (safe only)
        approval = {
            "state": state,
            "decided": state in ("approved", "rejected"),
        }

        # Apply info (safe only)
        ae = apply_events.get(iid, {})
        apply_info = {
            "applied": bool(ae),
            "outcome": ae.get("outcome", ""),
            "bytes_written": ae.get("bytes_written", 0),
            "line_count": ae.get("line_count", 0),
        }

        # Proof info (safe only)
        pe = proof_events.get(iid, {})
        proof_info = {
            "recorded": bool(pe),
            "before_sha256": pe.get("before_sha256", ""),
            "after_sha256": pe.get("after_sha256", ""),
            "bytes_delta": pe.get("bytes_delta", 0),
        }

        # Test info — only linked evidence, never the latest unrelated global test.
        from packages.orchestration.proof_chain import TEST_LINK_NONE, _link_test_to_change

        test_state, test_link, test_meta = _link_test_to_change(
            intent_id=iid,
            task_id=str(intent.get("task_id", "") or ""),
            test_events=test_events,
            apply_events=apply_event_records,
            total_applied_changes=total_applied,
        )
        if test_link == TEST_LINK_NONE:
            test_info = {"ran": False, "linked": False}
        else:
            test_info = {
                "ran": test_state != "not_required",
                "linked": True,
                "status": test_state,
                "link": test_link,
                "exit_code": test_meta.get("exit_code", -1),
            }

        # Revert info
        re = revert_events.get(iid, {})
        revert_info = {
            "reverted": bool(re),
            "outcome": re.get("outcome", ""),
            "existed_before": re.get("existed_before", False),
        }

        entries.append(ChangeEntry(
            intent_id=iid,
            target_path=target_path,
            risk=risk,
            status=status,
            approval=approval,
            apply=apply_info,
            proof=proof_info,
            test=test_info,
            revert=revert_info,
            memory=memory_keys,
        ))

    return entries


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------


def export_change_list_json(
    job_id: str,
    changes: list[ChangeEntry],
) -> dict[str, Any]:
    """Export change list as safe JSON dict."""
    return {
        "version": 1,
        "job_id": job_id,
        "changes": [
            {
                "intent_id": c.intent_id,
                "target_path": c.target_path,
                "risk": c.risk,
                "status": c.status,
            }
            for c in changes
        ],
    }


def export_change_show_json(
    job_id: str,
    entry: ChangeEntry,
) -> dict[str, Any]:
    """Export single change entry as safe JSON dict."""
    return {
        "version": 1,
        "job_id": job_id,
        "intent_id": entry.intent_id,
        "status": entry.status,
        "target_path": entry.target_path,
        "risk": entry.risk,
        "approval": entry.approval,
        "apply": entry.apply,
        "proof": entry.proof,
        "test": entry.test,
        "revert": entry.revert,
        "memory": entry.memory,
    }


# ---------------------------------------------------------------------------
# Summaries
# ---------------------------------------------------------------------------


def summarize_change_list(changes: list[ChangeEntry]) -> str:
    """Human-readable change list."""
    if not changes:
        return "No changes."
    lines = ["Changes:"]
    for c in changes:
        lines.append(
            f"  {c.intent_id}  {c.target_path}  "
            f"risk={c.risk}  status={c.status}"
        )
    return "\n".join(lines)


def summarize_change_show(entry: ChangeEntry) -> str:
    """Human-readable single change detail."""
    lines = [
        f"Change: {entry.intent_id}",
        f"  Target: {entry.target_path}",
        f"  Risk: {entry.risk}",
        f"  Status: {entry.status}",
        f"  Approval: {entry.approval['state']}",
        f"  Applied: {entry.apply['applied']}",
        f"  Proof: {'yes' if entry.proof['recorded'] else 'no'}",
        f"  Test: {'ran' if entry.test['ran'] else 'not yet'}",
        f"  Reverted: {entry.revert['reverted']}",
    ]
    if entry.memory:
        lines.append(f"  Memory: {', '.join(entry.memory[:5])}")
    return "\n".join(lines)
