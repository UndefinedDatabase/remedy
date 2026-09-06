"""
Trust Report v1 — auditable, read-only summary of a Remedy job.

Timeline answers: "what happened?"
Cockpit answers:  "where are we and what should I do now?"
Trust Report answers: "what was requested, planned, run, created, verified,
                       decided, and explicitly NOT done?"

Read-only: never mutates job state, run logs, or any filesystem resource.
No external dependencies — plain text output only.
No LLM calls.

Public API::

    summarize_trust_report(job, events, *, data_dir=None) -> str
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from packages.core.models import ArtifactKind, Job, RunState

if TYPE_CHECKING:
    from packages.orchestration.project_constitution import ProjectConstitution
from packages.orchestration._symbols import (
    FAIL as _FAIL,
)
from packages.orchestration._symbols import (
    INFO as _INFO,
)
from packages.orchestration._symbols import (
    NEXT as _NEXT,
)

# ---------------------------------------------------------------------------
# Symbols (consistent with timeline.py / cockpit.py)
# ---------------------------------------------------------------------------
from packages.orchestration._symbols import (
    OK as _OK,
)
from packages.orchestration._symbols import (
    WARN as _WARN,
)
from packages.orchestration._symbols import (
    section,
)
from packages.orchestration.approval_queue import (
    APPROVAL_APPROVED,
    APPROVAL_PENDING,
    APPROVAL_REJECTED,
    list_patch_intents,
)
from packages.orchestration.data_paths import run_log_dir
from packages.orchestration.permissions import Capability, effective_permissions, is_allowed

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def summarize_trust_report(
    job: Job,
    events: list[dict[str, Any]],
    *,
    data_dir: Path | None = None,
    constitution: ProjectConstitution | None = None,
) -> str:
    """Return a full trust/audit report string for a job.

    ``data_dir`` is the REMEDY_DATA_DIR root (parent of ``runs/``); when
    provided, the run-log directory path is included in the report.
    """
    signals = _extract_signals(events)
    parts: list[str] = []

    # ── Header ──────────────────────────────────────────────────────────────
    short_id = str(job.id)[:8]
    name = job.name if len(job.name) <= 60 else job.name[:60] + "…"
    parts.append("Remedy Trust Report")
    parts.append(f"Job: {short_id} — {name}")
    parts.append(f"State: {job.state.value}")
    parts.append("")

    # ── 1. User request ─────────────────────────────────────────────────────
    parts.append(section("1. User request"))
    if job.user_prompt:
        # Truncate very long prompts — raw content cap for display only.
        prompt = job.user_prompt[:400] + "…" if len(job.user_prompt) > 400 else job.user_prompt
        parts.append(f"  {prompt}")
    else:
        parts.append(f"  (no prompt recorded — job name: {job.name!r})")

    # ── 2. Plan ─────────────────────────────────────────────────────────────
    parts.append(section("2. Plan"))
    total = len(job.tasks)
    if not total:
        parts.append("  No tasks planned yet.")
    else:
        n_pending   = sum(1 for t in job.tasks if t.status == RunState.PENDING)
        n_completed = sum(1 for t in job.tasks if t.status == RunState.COMPLETED)
        n_failed    = sum(1 for t in job.tasks if t.status == RunState.FAILED)
        n_other     = total - n_pending - n_completed - n_failed
        summary_parts = [f"{total} total"]
        if n_completed:
            summary_parts.append(f"{n_completed} completed")
        if n_pending:
            summary_parts.append(f"{n_pending} pending")
        if n_failed:
            summary_parts.append(f"{n_failed} failed")
        if n_other:
            summary_parts.append(f"{n_other} other")
        parts.append(f"  Tasks: {', '.join(summary_parts)}")
        for task in job.tasks:
            task_type = task.inputs.get("task_type", "unknown")
            desc = task.description[:60] + "…" if len(task.description) > 60 else task.description
            status_label = task.status.value
            parts.append(f"    [{status_label:<9}] {task_type} — {desc}")

    # ── 3. Execution summary ─────────────────────────────────────────────────
    parts.append(section("3. Execution summary"))
    n_started     = signals["run_invocations"]
    n_completed_r = signals["run_completed"]
    n_failed_r    = signals["run_failed"]
    n_noop        = signals["run_noop"]
    n_interrupted = 1 if signals["has_interrupted"] else 0

    planning_failures = signals["planning_failures"]
    if not events:
        parts.append("  No run logs available.")
    else:
        if n_started:
            parts.append(f"  Run invocations:  {n_started}")
            parts.append(f"  Completed:        {n_completed_r}")
        if n_failed_r:
            parts.append(f"  Failed/blocked:   {n_failed_r}")
        if n_noop:
            parts.append(f"  No-op:            {n_noop}")
        if n_interrupted:
            itype = signals.get("interrupted_task_type")
            itype_str = f" (task_type={itype})" if itype else ""
            parts.append(f"  {_WARN} Interrupted:      {n_interrupted}{itype_str}")
        for error_cat in planning_failures:
            parts.append(f"  {_FAIL} Planning failed:  {error_cat}")
        if not n_started and not n_noop and not n_failed_r and not planning_failures:
            parts.append("  Run logs present but no task_run_started events recorded.")

    # ── 4. Artifacts ─────────────────────────────────────────────────────────
    parts.append(section("4. Artifacts"))
    if not job.artifacts:
        parts.append("  No artifacts recorded.")
    else:
        # Group by kind for readability
        kind_order = [
            ArtifactKind.PLANNING,
            ArtifactKind.BUILDER_PROPOSAL,
            ArtifactKind.WORKSPACE_MATERIALIZATION,
            ArtifactKind.PATCH_INTENT,
            ArtifactKind.REPO_APPLICATION,
            ArtifactKind.VERIFICATION,
            ArtifactKind.UNKNOWN,
        ]
        shown: set[str] = set()
        for kind in kind_order:
            for artifact in job.artifacts:
                if artifact.kind != kind:
                    continue
                a_short = artifact.id.hex[:8]
                a_name  = artifact.name[:60] + "…" if len(artifact.name) > 60 else artifact.name
                label   = kind.value.replace("_", " ")
                parts.append(f"  {label:<28} {a_name} ({a_short})")
                shown.add(str(artifact.id))
        # Any artifacts whose kind wasn't in order (shouldn't happen)
        for artifact in job.artifacts:
            if str(artifact.id) not in shown:
                a_short = artifact.id.hex[:8]
                a_name  = artifact.name[:60] + "…" if len(artifact.name) > 60 else artifact.name
                parts.append(f"  {'unknown':<28} {a_name} ({a_short})")

    # ── 5. Verification ──────────────────────────────────────────────────────
    parts.append(section("5. Verification"))
    vevents = signals["verification_events"]
    if not vevents:
        parts.append("  No verification events recorded.")
    else:
        for vev in vevents:
            task_id_str = vev.get("task_id", "")
            short_task  = task_id_str[:8] if task_id_str else "unknown"
            outcome     = vev.get("outcome", "")
            ev_name     = vev.get("event", "")
            if ev_name == "verification_passed":
                profile = vev.get("metadata", {}).get("verifier_profile") or vev.get("verifier_profile", "")
                profile_str = f"  profile: {profile}" if profile else ""
                parts.append(f"  {_OK} Task {short_task}: passed{profile_str}")
            elif ev_name == "verification_failed":
                meta         = vev.get("metadata", {})
                fail_count   = meta.get("failure_count") or vev.get("failure_count", "?")
                failed_checks = meta.get("failed_checks") or vev.get("failed_checks", [])
                checks_str   = ", ".join(str(c) for c in failed_checks) if failed_checks else ""
                checks_info  = f": {checks_str}" if checks_str else ""
                parts.append(
                    f"  {_FAIL} Task {short_task}: failed — {fail_count} check(s){checks_info}"
                )
            else:
                parts.append(f"  {_INFO} Task {short_task}: {outcome or ev_name}")

    # ── 6. Permissions and safety ─────────────────────────────────────────────
    parts.append(section("6. Permissions and safety"))
    for row in effective_permissions(job):
        cap    = row["capability"]
        eff    = row["effective"]
        status = row["status"]
        reserved_note = "  (reserved — not yet enforced)" if status == "reserved" else ""
        indicator = _OK if eff == "allow" else _INFO
        parts.append(f"  {indicator} {cap:<24} {eff}{reserved_note}")

    denied_events = signals["denied_events"]
    if denied_events:
        parts.append(f"  {_WARN} Blocked run events:")
        for dev in denied_events:
            meta = dev.get("metadata", {})
            cap  = meta.get("capability") or dev.get("capability", "")
            cap_str = f", capability={cap}" if cap else ""
            outcome = dev.get("outcome", "")
            parts.append(f"      task_run_failed(outcome={outcome}{cap_str})")

    # Constitution summary (counts only — no raw content, no raw conventions)
    if constitution is not None:
        # Stale/non-dir repo produces a warning and zero sources
        if constitution.warnings and not constitution.source_files:
            parts.append(
                f"  {_INFO} Project Constitution: unavailable"
                f" (attached repo missing or not a directory)"
            )
        elif constitution.source_files:
            n = len(constitution.source_files)
            parts.append(
                f"  {_INFO} Project Constitution: available from {n} source file(s)"
            )
        else:
            parts.append(f"  {_INFO} Project Constitution: no sources found")
    else:
        target_repo = job.metadata.get("target_repo")
        if target_repo:
            parts.append(
                f"  {_INFO} Project Constitution: not loaded"
                f" (run: remedy constitution {job.id})"
            )
        else:
            parts.append(f"  {_INFO} Project Constitution: no attached repo")

    # ── 7. Patch intents and decisions ────────────────────────────────────────
    parts.append(section("7. Patch intents and decisions"))
    intents = list_patch_intents(job)
    if not intents:
        parts.append("  No patch intents recorded.")
    else:
        n_pending_i  = sum(1 for i in intents if i["state"] == APPROVAL_PENDING)
        n_approved   = sum(1 for i in intents if i["state"] == APPROVAL_APPROVED)
        n_rejected   = sum(1 for i in intents if i["state"] == APPROVAL_REJECTED)
        counts = []
        if n_pending_i:
            counts.append(f"{n_pending_i} pending")
        if n_approved:
            counts.append(f"{n_approved} approved")
        if n_rejected:
            counts.append(f"{n_rejected} rejected")
        parts.append(f"  {len(intents)} intent(s): {', '.join(counts)}")
        parts.append("")
        for intent in intents:
            state     = intent["state"]
            indicator = _OK if state == APPROVAL_APPROVED else (_FAIL if state == APPROVAL_REJECTED else _INFO)
            risk      = intent["risk"]
            action    = intent["action"]
            path      = intent["target_path"]
            iid       = intent["intent_id"]
            decided   = intent.get("decided_at", "")
            decided_str = f"  decided: {decided[:10]}" if decided else ""
            parts.append(
                f"  {indicator} {iid:<14} {state:<8}  risk={risk:<8}  {action:<14}  {path}"
                f"{decided_str}"
            )
            # Show apply status if present (no content / diff text)
            apply_record = _get_apply_record(job, iid)
            if apply_record:
                apply_state = apply_record.get("state", "")
                parts.append(
                    f"      applied: yes  outcome={apply_state}  target={path}"
                )
                proof = apply_record.get("proof", {})
                if proof:
                    before_sha = str(proof.get("before_sha256", ""))
                    after_sha  = str(proof.get("after_sha256", ""))
                    bdelta = int(proof.get("bytes_delta", 0))
                    ldelta = int(proof.get("line_delta", 0))
                    before_str = (before_sha[:16] + "…") if before_sha else "(none)"
                    parts.append(
                        f"      proof:  before={before_str}"
                        f"  after={after_sha[:16]}…"
                        f"  Δbytes={bdelta:+d}  Δlines={ldelta:+d}"
                    )
        parts.append("")
        n_applied = sum(
            1 for i in intents
            if _get_apply_record(job, i["intent_id"]) is not None
            and _get_apply_record(job, i["intent_id"]).get("state") == "applied"
        )
        if n_approved and not n_pending_i and n_applied == n_approved:
            parts.append(f"  {_OK} All approved intents applied ({n_applied}).")
        elif n_approved and not n_pending_i:
            unapplied = n_approved - n_applied
            parts.append(
                f"  {_INFO} {unapplied} approved intent(s) not yet applied. "
                f"Apply with: remedy patch apply <job_id> <intent_id>"
            )
        elif n_approved:
            parts.append(
                f"  {_INFO} Note: pending intents must be decided before apply. "
                f"Apply with: remedy patch apply <job_id> <intent_id>"
            )
        else:
            parts.append(
                "  Note: intents must be approved before apply. "
                "Use: remedy patch approve <job_id> <intent_id>"
            )

    # ── 8. Test runs ──────────────────────────────────────────────────────────
    parts.append(section("8. Test runs"))
    test_run_events = [e for e in events if e.get("event") == "test_run_completed"]
    if not test_run_events:
        parts.append("  No test runs recorded.")
    else:
        for ev in test_run_events:
            meta       = ev.get("metadata", {})
            status     = str(meta.get("status", "unknown"))
            command    = str(meta.get("command", ""))
            exit_code  = meta.get("exit_code")
            dur_ms     = meta.get("duration_ms", 0)
            src_type   = str(meta.get("command_source_type", ""))
            confidence = str(meta.get("command_confidence", ""))
            sym        = _OK if status == "passed" else (_FAIL if status == "failed" else _WARN)
            exit_str   = f"  exit_code={exit_code}" if exit_code is not None else ""
            src_str    = f"  source={src_type}  confidence={confidence}" if src_type else ""
            trunc_str = ""
            if meta.get("output_truncated"):
                orig = meta.get("original_output_bytes", 0)
                kept = meta.get("persisted_output_bytes", 0)
                trunc_str = f"  OUTPUT TRUNCATED ({orig} -> {kept} bytes)"
            parts.append(
                f"  {sym} status={status}  command={command}"
                f"{exit_str}  duration_ms={dur_ms}{src_str}{trunc_str}"
            )
            parts.append("      (raw stdout/stderr not included in this report)")

    # ── 9. Redaction / trust boundary ─────────────────────────────────────────
    parts.append(section("9. Redaction / trust boundary"))
    parts.append(
        "  Raw prompts, artifact content, and full diff text are not included in this report."
    )
    parts.append(
        "  Run logs contain IDs, counts, labels, and outcomes only — no raw exception text."
    )
    parts.append(
        "  This report is generated from persisted Job JSON and JSONL run logs."
    )

    # ── 10. Next safe action ───────────────────────────────────────────────────
    parts.append(section("10. Next safe action"))
    parts.append(_derive_next_action(job, signals))

    # Optional: run log dir path
    if data_dir is not None:
        run_log_path = run_log_dir(job.id, data_dir)
        parts.append("")
        parts.append(f"  Run log dir: {run_log_path}")

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Signal extraction
# ---------------------------------------------------------------------------


def _extract_signals(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Scan events once and extract all signals needed for the trust report."""
    signals: dict[str, Any] = {
        "run_invocations":    0,
        "run_completed":      0,
        "run_failed":         0,
        "run_noop":           0,
        "has_interrupted":    False,
        "interrupted_task_type": None,
        "verification_events": [],   # list of verification_passed/failed events
        "denied_events":       [],   # task_run_failed with outcome=permission_denied
        "planning_failures":   [],   # (error_category,) tuples from planning_failed events
        "last_patch":          None,
        "last_terminal":       None,
    }

    in_task = False
    last_started_type: str | None = None

    for ev in events:
        name = ev.get("event", "")

        if name == "task_run_started":
            signals["run_invocations"] += 1
            in_task = True
            last_started_type = ev.get("metadata", {}).get("task_type") or ev.get("task_type")

        elif name in ("task_run_completed", "task_run_failed", "task_run_noop"):
            signals["last_terminal"] = ev
            in_task = False
            last_started_type = None

            if name == "task_run_completed":
                signals["run_completed"] += 1
            elif name == "task_run_failed":
                signals["run_failed"] += 1
                outcome = ev.get("outcome", "") or ev.get("metadata", {}).get("outcome", "")
                if outcome == "permission_denied":
                    signals["denied_events"].append(ev)
            elif name == "task_run_noop":
                signals["run_noop"] += 1

        elif name == "planning_failed":
            # Safe: use only error_category from metadata; never ev["message"].
            error_cat = ev.get("metadata", {}).get("error_category", "") or ""
            signals["planning_failures"].append(error_cat or "unknown error")

        elif name in ("verification_passed", "verification_failed"):
            signals["verification_events"].append(ev)

        elif name == "patch_intent_created":
            signals["last_patch"] = ev

    if in_task:
        signals["has_interrupted"] = True
        signals["interrupted_task_type"] = last_started_type

    return signals


# ---------------------------------------------------------------------------
# Next safe action
# ---------------------------------------------------------------------------


def _derive_next_action(job: Job, signals: dict[str, Any]) -> str:
    if not job.tasks:
        return (
            f"  {_NEXT} Plan this job:\n"
            f"      remedy job plan {job.id}"
        )

    pending = sum(1 for t in job.tasks if t.status == RunState.PENDING)
    ws_allowed = is_allowed(job, Capability.workspace_write)

    if not ws_allowed and pending:
        return (
            f"  {_NEXT} Grant workspace permission, then run:\n"
            f"      remedy job permit {job.id} workspace_write allow\n"
            f"      remedy job run-next {job.id}"
        )

    if signals["has_interrupted"] and pending:
        return (
            f"  {_NEXT} Inspect the timeline, then resume:\n"
            f"      remedy brain timeline {job.id}\n"
            f"      remedy job run-next {job.id}"
        )

    intents = list_patch_intents(job)
    n_pending_intents = sum(1 for i in intents if i["state"] == APPROVAL_PENDING)
    n_approved        = sum(1 for i in intents if i["state"] == APPROVAL_APPROVED)
    high_risk_pending = any(
        i["risk"] in ("medium", "high", "unknown") and i["state"] == APPROVAL_PENDING
        for i in intents
    )

    if high_risk_pending and pending:
        return (
            f"  {_NEXT} Review and decide on patch intents, then continue:\n"
            f"      remedy patch list {job.id}\n"
            f"      remedy job run-next {job.id}"
        )

    if n_approved and not pending and not n_pending_intents:
        return (
            f"  {_NEXT} All patch intents approved. Apply with:\n"
            f"      remedy patch apply {job.id} <intent_id>"
        )

    if pending:
        return (
            f"  {_NEXT} Continue execution:\n"
            f"      remedy job run-next {job.id}"
        )

    return (
        f"  {_NEXT} No pending tasks. Inspect generated files\n"
        f"      or create a new job: remedy job create \"<prompt>\""
    )


# ---------------------------------------------------------------------------
# Apply record lookup (for trust report section 7)
# ---------------------------------------------------------------------------


def _get_apply_record(job: Job, intent_id: str) -> dict | None:
    """Return the apply record for intent_id from artifact metadata, or None."""
    for artifact in job.artifacts:
        records = artifact.metadata.get("patch_intent_apply_records", {})
        if intent_id in records:
            return records[intent_id]
    return None
