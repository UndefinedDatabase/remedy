"""
Repair Loop v0 — structured failure → fix task → optional fixture patch intent.

No real provider. No automatic apply. No test execution.
Stops before any risky action.

Public API::

    start_repair_loop_v0(job_id, failure_artifact_id, ...) -> RepairLoopResult
    export_repair_loop_json(result) -> dict
    summarize_repair_loop(result) -> str
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID

from packages.orchestration.do_run import (
    DoRunNextAction,
    validate_next_safe_action_command,
)


# ---------------------------------------------------------------------------
# Result model (Step 946)
# ---------------------------------------------------------------------------


@dataclass
class RepairLoopResult:
    """Result of a repair loop v0 run."""

    version: int = 1
    job_id: str = ""
    failure_artifact_id: str = ""
    fix_task_id: str = ""
    repair_artifact_id: str = ""
    repair_patch_intent_id: str = ""
    stop_reason: str = ""
    stop_detail: str = ""
    next_safe_action: DoRunNextAction | None = None
    proof_status: str = "incomplete"
    phases: list[dict[str, str]] = field(default_factory=list)
    error: str = ""
    generated_at: str = ""


# ---------------------------------------------------------------------------
# Orchestrator (Step 946)
# ---------------------------------------------------------------------------


def start_repair_loop_v0(
    job_id: str,
    failure_artifact_id: str,
    *,
    create_patch_intent: bool = False,
) -> RepairLoopResult:
    """Run repair loop v0 — creates fix task, optionally fixture patch intent.

    No real provider. No apply. No test execution. Stops before risky action.
    """
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.storage import load_job, save_job
    from packages.orchestration.test_failure_artifact import (
        TestFailureArtifact,
        create_fix_task_from_failure,
        emit_failure_events,
    )
    from packages.orchestration.timeline import append_run_event

    result = RepairLoopResult(
        job_id=job_id,
        failure_artifact_id=failure_artifact_id,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )

    data_dir = resolve_data_root()

    # --- Phase: load ---
    try:
        job = load_job(job_id)
    except Exception:
        result.stop_reason = "job_not_found"
        result.stop_detail = f"Job {job_id[:8]} not found"
        result.error = result.stop_detail
        result.phases.append({"phase": "load", "status": "failed", "safe_summary": result.stop_detail})
        return result

    result.phases.append({"phase": "load", "status": "completed", "safe_summary": f"Job {job_id[:8]} loaded"})

    # --- Contract enforcement (Step 1071: central contract) ---
    from packages.orchestration.run_contract import (
        ensure_contract,
        evaluate_run_action,
        load_usage,
        save_usage,
    )

    repair_contract = ensure_contract(job)
    save_job(job)  # persist contract if newly created

    fix_decision = evaluate_run_action(repair_contract, "create_fix_task")
    if not fix_decision.allowed:
        result.stop_reason = "contract_blocked"
        result.stop_detail = fix_decision.reason
        result.phases.append({"phase": "contract", "status": "blocked", "safe_summary": fix_decision.reason})
        return result

    if create_patch_intent:
        pi_decision = evaluate_run_action(repair_contract, "create_patch_intent")
        if not pi_decision.allowed:
            result.stop_reason = "contract_blocked"
            result.stop_detail = pi_decision.reason
            result.phases.append({"phase": "contract", "status": "blocked", "safe_summary": pi_decision.reason})
            return result

    result.phases.append({"phase": "contract", "status": "completed", "safe_summary": "Contract checks passed"})

    # --- Phase: validate failure artifact ---
    failure_art = None
    failure_meta = None
    for art in job.artifacts:
        if str(art.id) == failure_artifact_id and art.metadata.get("test_failure"):
            failure_art = art
            failure_meta = art.metadata
            break

    if not failure_art or not failure_meta:
        result.stop_reason = "failure_artifact_not_found"
        result.stop_detail = f"Failure artifact {failure_artifact_id[:8]} not found in job"
        result.error = result.stop_detail
        result.phases.append({"phase": "validate", "status": "failed", "safe_summary": result.stop_detail})
        return result

    result.phases.append({"phase": "validate", "status": "completed",
                          "safe_summary": f"Failure artifact validated: {failure_meta.get('failure_kind', 'unknown')}"})

    # Reconstruct minimal TestFailureArtifact from metadata
    failure = TestFailureArtifact(
        artifact_id=failure_artifact_id,
        job_id=job_id,
        task_id=failure_meta.get("related_task_id", ""),
        related_intent_id=failure_meta.get("related_intent_id", ""),
        related_apply_id=failure_meta.get("related_apply_id", ""),
        related_test_run_id=failure_meta.get("related_test_run_id", ""),
        failing_phase=failure_meta.get("failing_phase", "test"),
        command_safe=failure_meta.get("command_safe", ""),
        exit_code=failure_meta.get("exit_code"),
        safe_summary=failure_meta.get("safe_summary", ""),
        output_ref=failure_meta.get("output_ref", ""),
        failure_kind=failure_meta.get("failure_kind", "unknown"),
    )

    # --- Phase: create fix task ---
    # Check if fix task already exists for this failure
    existing_fix = None
    for task in job.tasks:
        if task.inputs.get("failure_artifact_id") == failure_artifact_id:
            existing_fix = task
            break

    if existing_fix:
        fix_task = existing_fix
        result.phases.append({"phase": "fix_task", "status": "completed",
                              "safe_summary": f"Fix task already exists: {str(fix_task.id)[:8]}"})
    else:
        fix_task = create_fix_task_from_failure(job, failure)
        result.phases.append({"phase": "fix_task", "status": "completed",
                              "safe_summary": f"Fix task created: {str(fix_task.id)[:8]}"})

    result.fix_task_id = str(fix_task.id)

    # --- Phase: optional fixture patch intent ---
    if create_patch_intent:
        from packages.core.models import Artifact, ArtifactKind
        from packages.orchestration.approval_queue import make_intent_id

        repair_art = Artifact(
            name=f"fixture-repair-{failure.artifact_id[:8]}",
            content=f"Fixture repair proposal for: {failure.safe_summary[:100]}",
            kind=ArtifactKind.BUILDER_PROPOSAL,
            task_id=fix_task.id,
            metadata={
                "fixture": True,
                "repair": True,
                "failure_artifact_id": failure_artifact_id,
                "safe_summary": f"Fixture repair for {failure.failure_kind}",
                "patch_intent_explanations": [
                    {
                        "file": "docs/REPAIR.md",
                        "action": "create",
                        "risk": "low",
                        "reason": f"Fixture repair proposal for {failure.failure_kind}",
                        "summary": f"Fixture repair for: {failure.safe_summary[:100]}",
                    },
                ],
                "patch_intent_approvals": {},
            },
        )
        job.artifacts.append(repair_art)
        save_job(job)

        intent_id = make_intent_id(repair_art.id, 0)
        result.repair_artifact_id = str(repair_art.id)
        result.repair_patch_intent_id = intent_id

        result.phases.append({"phase": "repair_intent", "status": "completed",
                              "safe_summary": f"Repair patch intent {intent_id} created"})
    else:
        result.phases.append({"phase": "repair_intent", "status": "skipped",
                              "safe_summary": "No patch intent requested"})

    # --- Phase: emit events (idempotent — skip if already emitted for this failure) ---
    from packages.orchestration.timeline import load_run_events
    existing_events = load_run_events(data_dir, UUID(job_id))
    already_emitted = any(
        e.get("event") == "test_failure_artifact_created"
        and e.get("artifact_id") == failure_artifact_id
        for e in existing_events
    )
    if not already_emitted:
        emit_failure_events(data_dir, UUID(job_id), failure, fix_task_id=str(fix_task.id))

    append_run_event(data_dir, UUID(job_id), event="repair_loop_stopped", metadata={
        "job_id": job_id,
        "fix_task_id": str(fix_task.id),
        "failure_artifact_id": failure_artifact_id,
        "stop_reason": "awaiting_approval" if create_patch_intent else "fix_task_created",
    })

    result.phases.append({"phase": "events", "status": "completed", "safe_summary": "Events emitted"})

    # Step 1077: Record usage
    usage = load_usage(job)
    usage.loops_used += 1
    save_usage(job, usage)

    append_run_event(data_dir, UUID(job_id), event="contract_decision", metadata={
        "action": "repair_loop_complete",
        "loops_used": usage.loops_used,
        "contract_id": repair_contract.contract_id,
    })

    save_job(job)

    # --- Stop ---
    if create_patch_intent and result.repair_patch_intent_id:
        from packages.orchestration.approval_queue import get_patch_intent
        reloaded = load_job(job_id)
        verified_intent = get_patch_intent(reloaded, result.repair_patch_intent_id)
        if verified_intent is not None:
            result.stop_reason = "approval_required"
            result.stop_detail = "Repair patch intent awaiting approval"
            result.next_safe_action = DoRunNextAction(
                label="Approve repair patch",
                command=f"remedy patch approve {job_id} {result.repair_patch_intent_id}",
                reason="Review and approve the repair patch intent.",
            )
        else:
            result.stop_reason = "intent_not_verified"
            result.stop_detail = "Repair intent created but not verifiable — skipping next_safe_action"
            result.repair_patch_intent_id = ""
            result.next_safe_action = DoRunNextAction(
                label="Show job",
                command=f"remedy job show {job_id} --json",
                reason="Review the fix task and failure artifact.",
            )
    else:
        result.stop_reason = "fix_task_created"
        result.stop_detail = "Fix task created from failure evidence"
        result.next_safe_action = DoRunNextAction(
            label="Show job",
            command=f"remedy job show {job_id} --json",
            reason="Review the fix task and failure artifact.",
        )

    result.phases.append({"phase": "stop", "status": "stopped",
                          "safe_summary": f"Stopped: {result.stop_reason}"})

    return result


# ---------------------------------------------------------------------------
# Export / summary
# ---------------------------------------------------------------------------


def export_repair_loop_json(result: RepairLoopResult) -> dict[str, Any]:
    """Export RepairLoopResult as safe JSON dict."""
    out: dict[str, Any] = {
        "version": result.version,
        "job_id": result.job_id,
        "failure_artifact_id": result.failure_artifact_id,
        "fix_task_id": result.fix_task_id,
        "repair_artifact_id": result.repair_artifact_id,
        "repair_patch_intent_id": result.repair_patch_intent_id,
        "stop_reason": result.stop_reason,
        "stop_detail": result.stop_detail,
        "proof_status": result.proof_status,
        "phases": result.phases,
        "generated_at": result.generated_at,
        "next_safe_action": None,
    }
    if result.next_safe_action:
        out["next_safe_action"] = {
            "label": result.next_safe_action.label,
            "command": result.next_safe_action.command,
            "reason": result.next_safe_action.reason,
        }
    if result.error:
        out["error"] = result.error
    return out


def summarize_repair_loop(result: RepairLoopResult) -> str:
    """Human-readable repair loop summary."""
    lines = [
        f"Repair Loop: {result.job_id[:8]}",
        f"Failure: {result.failure_artifact_id[:8] if result.failure_artifact_id else 'none'}",
    ]
    if result.fix_task_id:
        lines.append(f"Fix task: {result.fix_task_id[:8]}")

    lines.append("")
    lines.append("Phases:")
    for p in result.phases:
        lines.append(f"  [{p.get('status', '?')}] {p.get('phase', '?')}: {p.get('safe_summary', '')}")

    lines.append(f"\nStop: {result.stop_reason}")
    if result.stop_detail:
        lines.append(f"  {result.stop_detail}")

    if result.next_safe_action:
        lines.append(f"\nNext: {result.next_safe_action.label}")
        lines.append(f"  $ {result.next_safe_action.command}")

    return "\n".join(lines)


# ===========================================================================
# Repair Loop v1 — Failure Artifact → Repair Context → Fix Task → Repair
# Artifact → Fix Patch Intent → approval_required → safe stop. (Steps 1194-1200)
#
# Creates a PROPOSAL only. No source_apply, no apply, no test execution, no
# provider. Apply stays separate + approval-gated (do continue --intent-id).
# ===========================================================================


class RepairStatus:
    """Repair attempt lifecycle status (1194; apply states added 1225)."""

    BLOCKED = "blocked"
    CONTEXT_READY = "context_ready"
    FIX_TASK_CREATED = "fix_task_created"
    REPAIR_ARTIFACT_CREATED = "repair_artifact_created"
    PATCH_INTENT_CREATED = "patch_intent_created"
    APPROVAL_REQUIRED = "approval_required"
    # Approved Repair Apply Cycle states (Step 1225).
    APPROVED = "approved"
    APPLYING = "applying"
    APPLIED = "applied"
    TESTED_PASSED = "tested_passed"
    TESTED_FAILED = "tested_failed"
    SUPERSEDED = "superseded"
    FAILED = "failed"
    EVIDENCE_INCOMPLETE = "evidence_incomplete"


_REPAIR_STATUSES = frozenset({
    RepairStatus.BLOCKED, RepairStatus.CONTEXT_READY, RepairStatus.FIX_TASK_CREATED,
    RepairStatus.REPAIR_ARTIFACT_CREATED, RepairStatus.PATCH_INTENT_CREATED,
    RepairStatus.APPROVAL_REQUIRED, RepairStatus.APPROVED, RepairStatus.APPLYING,
    RepairStatus.APPLIED, RepairStatus.TESTED_PASSED, RepairStatus.TESTED_FAILED,
    RepairStatus.SUPERSEDED, RepairStatus.FAILED, RepairStatus.EVIDENCE_INCOMPLETE,
})

# Resumable (non-terminal-error) states: a repeated propose returns the existing
# attempt rather than creating duplicates.
_RESUMABLE_STATUSES = frozenset({
    RepairStatus.FIX_TASK_CREATED, RepairStatus.REPAIR_ARTIFACT_CREATED,
    RepairStatus.PATCH_INTENT_CREATED, RepairStatus.APPROVAL_REQUIRED,
    RepairStatus.CONTEXT_READY,
})

# Repair kind / expected effect classification (Step 1221).
REPAIR_KIND_DOCS_FIXTURE = "docs_fixture"
REPAIR_KIND_SOURCE_FIXTURE = "source_fixture"
REPAIR_KIND_PROVIDER = "provider"  # future
EXPECT_DOCUMENTATION_ONLY = "documentation_only"
EXPECT_SOURCE_FIX = "source_fix"
EXPECT_UNKNOWN = "unknown"


class RepairStopReason:
    """Safe stop reasons for a repair attempt (1194)."""

    APPROVAL_REQUIRED = "approval_required"
    FIX_TASK_CREATED = "fix_task_created"
    REPAIR_BUILDER_UNAVAILABLE = "repair_builder_unavailable"
    BLOCKED_INELIGIBLE = "blocked_ineligible"
    EVIDENCE_INCOMPLETE = "evidence_incomplete"
    FAILED = "failed"
    ERROR = "error"


# Fixture repair builder supports only these deterministic failure kinds in v1.
_SUPPORTED_FIXTURE_KINDS = frozenset({
    "test_failed", "command_failed", "assertion",
})


@dataclass
class RepairContextSummary:
    """Safe failure context for a repair proposal (1195). No raw output."""

    version: int = 1
    job_id: str = ""
    failure_artifact_id: str = ""
    status: str = ""               # context_ready | blocked
    blocker: str = ""
    test_run_id: str = ""
    task_id: str = ""
    intent_id: str = ""
    apply_id: str = ""
    command_display: str = ""
    exit_code: int | None = None
    failure_kind: str = ""
    safe_summary: str = ""
    changed_files_safe: list[str] = field(default_factory=list)
    proof_status: str = "unknown"
    snapshot_status: str = "unknown"
    hints: list[str] = field(default_factory=list)
    fixture_supported: bool = False
    # Optional opt-in deterministic source-fixture descriptor (Step 1233): a safe
    # repo-relative target path supplied on the failure artifact metadata
    # (`repair_fixture_target`). When present and the source-fixture builder is
    # requested, a `source_fix` repair intent is proposed instead of docs-only.
    source_fixture_target: str = ""


@dataclass
class RepairEligibility:
    """Outcome of evaluate_repair_eligibility (1196). No raw content."""

    eligible: bool = False
    job_id: str = ""
    failure_artifact_id: str = ""
    test_run_id: str = ""
    task_id: str = ""
    intent_id: str = ""
    apply_id: str = ""
    blockers: list[str] = field(default_factory=list)
    next_safe_action: DoRunNextAction | None = None
    existing_repair_intent_id: str = ""
    safe_summary: str = ""


@dataclass
class RepairAttempt:
    """Durable repair attempt record (1197). Safe IDs/status only."""

    attempt_id: str = ""
    job_id: str = ""
    failure_artifact_id: str = ""
    test_run_id: str = ""
    task_id: str = ""
    intent_id: str = ""
    apply_id: str = ""
    repair_task_id: str = ""
    repair_artifact_id: str = ""
    repair_intent_id: str = ""
    status: str = ""
    stop_reason: str = ""
    evidence_status: str = "complete"
    source: str = "cli_v1"
    # Classification (Step 1221). repair_kind: docs_fixture | source_fixture |
    # provider. expected_effect: documentation_only | source_fix | unknown.
    repair_kind: str = ""
    expected_effect: str = ""
    # Apply-cycle linkage (Step 1223-1225) — repair apply / post-repair test.
    repair_apply_id: str = ""
    post_repair_test_run_id: str = ""
    resolved_failure: bool = False
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "attempt_id": self.attempt_id, "job_id": self.job_id,
            "failure_artifact_id": self.failure_artifact_id,
            "test_run_id": self.test_run_id, "task_id": self.task_id,
            "intent_id": self.intent_id, "apply_id": self.apply_id,
            "repair_task_id": self.repair_task_id,
            "repair_artifact_id": self.repair_artifact_id,
            "repair_intent_id": self.repair_intent_id,
            "status": self.status, "stop_reason": self.stop_reason,
            "evidence_status": self.evidence_status, "source": self.source,
            "repair_kind": self.repair_kind, "expected_effect": self.expected_effect,
            "repair_apply_id": self.repair_apply_id,
            "post_repair_test_run_id": self.post_repair_test_run_id,
            "resolved_failure": self.resolved_failure,
            "created_at": self.created_at, "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "RepairAttempt":
        return cls(**{k: d.get(k, getattr(cls(), k)) for k in cls().__dict__})


@dataclass
class RepairPatchIntentResult:
    """Outcome of repair patch intent creation (1200). No patch body."""

    repair_artifact_id: str = ""
    repair_intent_id: str = ""
    approval_state: str = ""
    risk: str = ""
    target_paths: list[str] = field(default_factory=list)
    resolvable: bool = False
    repair_kind: str = ""
    expected_effect: str = ""


@dataclass
class RepairAttemptResult:
    """Full result of one repair proposal cycle (1194). No raw content."""

    version: int = 1
    job_id: str = ""
    failure_artifact_id: str = ""
    attempt_id: str = ""
    test_run_id: str = ""
    task_id: str = ""
    intent_id: str = ""
    apply_id: str = ""
    repair_task_id: str = ""
    repair_artifact_id: str = ""
    repair_intent_id: str = ""
    status: str = ""
    stop_reason: str = ""
    evidence_status: str = "complete"
    resumed: bool = False
    phases: list[dict[str, str]] = field(default_factory=list)
    next_safe_action: DoRunNextAction | None = None
    safe_summary: str = ""
    created_at: str = ""
    source: str = "cli_v1"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Repair context builder (Step 1195)
# ---------------------------------------------------------------------------


def _find_failure_artifact(job: Any, failure_artifact_id: str) -> Any:
    for art in job.artifacts:
        if str(art.id) == failure_artifact_id and (art.metadata or {}).get("test_failure"):
            return art
    return None


def _safe_changed_files(meta: dict[str, Any]) -> list[str]:
    """Basenames only, bounded — never absolute paths."""
    out: list[str] = []
    for f in (meta.get("related_files") or [])[:10]:
        base = str(f).rsplit("/", 1)[-1]
        if base and len(base) < 80:
            out.append(base)
    return out


def _safe_rel_target(value: Any) -> str:
    """Validate an opt-in source-fixture target: a safe repo-relative path.

    Rejects absolute paths, parent traversal, and over-long values. Returns ""
    when unsafe or absent.
    """
    p = str(value or "").strip()
    if not p or len(p) > 200:
        return ""
    if p.startswith("/") or p.startswith("~") or ".." in p.split("/"):
        return ""
    return p


def build_repair_context(
    job_id: str,
    failure_artifact_id: str,
    data_dir: "Path | None" = None,
) -> RepairContextSummary:
    """Build a safe repair context for a failure (Step 1195).

    Read-only. Includes safe summaries only — never raw stdout/stderr, source,
    diff, artifact body, absolute paths, secrets, or tracebacks. Missing or stale
    failure artifacts return status="blocked" with a safe blocker code.
    """
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.storage import load_job, JobNotFoundError

    ctx = RepairContextSummary(job_id=job_id, failure_artifact_id=failure_artifact_id)
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()

    try:
        job = load_job(UUID(job_id), ddir)
    except (ValueError, JobNotFoundError):
        ctx.status = "blocked"
        ctx.blocker = "job_not_found"
        return ctx

    art = _find_failure_artifact(job, failure_artifact_id)
    if art is None:
        ctx.status = "blocked"
        ctx.blocker = "failure_artifact_not_found"
        return ctx

    meta = art.metadata or {}
    test_run_id = str(meta.get("related_test_run_id", "") or "")
    # Stale link: failure references a test run that no later passing run resolves.
    # If the failure claims a test_run_id but the recorded exit_code is success,
    # the link is inconsistent → block safely.
    exit_code = meta.get("exit_code")
    if exit_code == 0:
        ctx.status = "blocked"
        ctx.blocker = "stale_failure_link"
        return ctx

    ctx.test_run_id = test_run_id
    ctx.task_id = str(meta.get("related_task_id", "") or "")
    ctx.intent_id = str(meta.get("related_intent_id", "") or "")
    ctx.apply_id = str(meta.get("related_apply_id", "") or "")
    ctx.command_display = str(meta.get("command_safe", "") or "")[:200]
    ctx.exit_code = exit_code if isinstance(exit_code, int) else None
    ctx.failure_kind = str(meta.get("failure_kind", "unknown") or "unknown")
    ctx.safe_summary = str(meta.get("safe_summary", "") or "")[:200]
    ctx.changed_files_safe = _safe_changed_files(meta)
    ctx.fixture_supported = ctx.failure_kind in _SUPPORTED_FIXTURE_KINDS
    ctx.source_fixture_target = _safe_rel_target(meta.get("repair_fixture_target", ""))

    # Authoritative proof + snapshot status (best-effort, never raw).
    try:
        from packages.orchestration.proof_chain import build_proof_chain, PROOF_VERIFIED
        chain = build_proof_chain(job, _load_events_safe(ddir, job_id), data_dir=ddir)
        verified = sum(1 for c in chain.changes if c.proof_status == PROOF_VERIFIED)
        ctx.proof_status = "verified" if (chain.changes and verified == len(chain.changes)) else (
            "partial" if verified else "none")
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        ctx.proof_status = "unknown"

    if ctx.apply_id:
        try:
            from packages.orchestration.repository_snapshot import build_snapshot_truth
            truth = build_snapshot_truth(job_id, apply_id=ctx.apply_id, data_dir=ddir)
            ctx.snapshot_status = truth.apply_state or "unknown"
        except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
            ctx.snapshot_status = "unknown"

    # Bounded, safe hints (no raw output).
    hints: list[str] = []
    if ctx.failure_kind == "test_failed":
        hints.append("A test assertion failed after the apply — review the linked task.")
    elif ctx.failure_kind == "timeout":
        hints.append("The test command timed out — repair builder cannot propose a fix.")
    elif ctx.failure_kind in ("collection_failed",):
        hints.append("Tests could not be collected — likely an import/setup error.")
    if not ctx.fixture_supported:
        hints.append("No deterministic fixture repair is available for this failure kind.")
    ctx.hints = hints[:5]

    ctx.status = "context_ready"
    return ctx


def _load_events_safe(data_dir: Path, job_id: str) -> list[dict[str, Any]]:
    try:
        from packages.orchestration.timeline import load_run_events
        return load_run_events(data_dir, UUID(job_id))
    except (ImportError, OSError, ValueError, KeyError, TypeError):
        return []


# ---------------------------------------------------------------------------
# Repair attempt persistence (Step 1197)
# ---------------------------------------------------------------------------


_ATTEMPTS_KEY = "repair_attempts_v1"


def _attempt_key(failure_artifact_id: str, source: str) -> str:
    return f"{failure_artifact_id}::{source}"


def load_repair_attempts(job: Any) -> dict[str, RepairAttempt]:
    """Load all v1 repair attempts from job metadata."""
    raw = (job.metadata or {}).get(_ATTEMPTS_KEY, {})
    out: dict[str, RepairAttempt] = {}
    if isinstance(raw, dict):
        for k, v in raw.items():
            if isinstance(v, dict):
                out[k] = RepairAttempt.from_dict(v)
    return out


def find_repair_attempt(job: Any, failure_artifact_id: str, source: str = "cli_v1") -> RepairAttempt | None:
    return load_repair_attempts(job).get(_attempt_key(failure_artifact_id, source))


def save_repair_attempt(job: Any, attempt: RepairAttempt) -> None:
    """Persist a repair attempt into job.metadata (atomic dict update)."""
    from packages.orchestration.storage import save_job

    if job.metadata is None:
        job.metadata = {}
    attempts = job.metadata.get(_ATTEMPTS_KEY, {})
    if not isinstance(attempts, dict):
        attempts = {}
    attempt.updated_at = _now()
    attempts[_attempt_key(attempt.failure_artifact_id, attempt.source)] = attempt.to_dict()
    job.metadata[_ATTEMPTS_KEY] = attempts
    save_job(job)


# ---------------------------------------------------------------------------
# Events (Step 1205)
# ---------------------------------------------------------------------------


REPAIR_EVENTS = frozenset({
    "repair_attempt_requested",
    "repair_context_built",
    "repair_fix_task_created",
    "repair_artifact_created",
    "repair_patch_intent_created",
    "repair_approval_required",
    "repair_attempt_blocked",
    "repair_attempt_failed",
})


def _emit_repair(data_dir: Path, job_id: str, event: str, metadata: dict[str, Any]) -> str:
    """Emit a safe repair event; returns persistence status (degradation visible)."""
    from packages.orchestration.event_persistence import emit_important_event
    r = emit_important_event(data_dir, job_id, event, metadata, eligible=REPAIR_EVENTS)
    return r.status


# ---------------------------------------------------------------------------
# Eligibility (Step 1196)
# ---------------------------------------------------------------------------


def _na(label: str, command: str, reason: str) -> DoRunNextAction:
    return DoRunNextAction(label=label, command=command, reason=reason)


def evaluate_repair_eligibility(
    job_id: str,
    failure_artifact_id: str,
    data_dir: "Path | None" = None,
    *,
    source: str = "cli_v1",
) -> RepairEligibility:
    """Decide whether a repair proposal may proceed (Step 1196). Read-only.

    Gates: job exists; failure artifact exists; linked to a real test run (or a
    safe legacy fallback with a related apply); failure not already resolved by a
    later passing linked test; RunContract allows metadata repair actions; an
    existing resumable attempt / unresolved repair intent yields an idempotent
    return (eligible, with the existing intent id). Every block returns a
    catalog-backed next safe action.
    """
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.storage import load_job, JobNotFoundError
    from packages.orchestration.run_contract import (
        ensure_contract, evaluate_run_action, ContractAction,
    )
    from packages.orchestration.approval_queue import get_patch_intent

    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    elig = RepairEligibility(job_id=job_id, failure_artifact_id=failure_artifact_id)

    # 1. Job exists.
    try:
        job = load_job(UUID(job_id), ddir)
    except (ValueError, JobNotFoundError):
        elig.blockers.append("job_not_found")
        elig.next_safe_action = _na("List jobs", "remedy job list --json", "Job not found.")
        elig.safe_summary = "Job not found."
        return elig

    # 2. Failure artifact exists.
    art = _find_failure_artifact(job, failure_artifact_id)
    if art is None:
        elig.blockers.append("failure_artifact_not_found")
        elig.next_safe_action = _na("Show job", f"remedy job show {job_id} --json",
                                    "Failure artifact not found in job.")
        elig.safe_summary = "Failure artifact not found."
        return elig

    meta = art.metadata or {}
    elig.test_run_id = str(meta.get("related_test_run_id", "") or "")
    elig.task_id = str(meta.get("related_task_id", "") or "")
    elig.intent_id = str(meta.get("related_intent_id", "") or "")
    elig.apply_id = str(meta.get("related_apply_id", "") or "")
    exit_code = meta.get("exit_code")

    # 3. Linkage: a real test run, or a safe legacy fallback (a related apply).
    if not elig.test_run_id and not elig.apply_id:
        elig.blockers.append("unlinked_failure")
        elig.next_safe_action = _na("Show job", f"remedy job show {job_id} --json",
                                    "Failure is not linked to a test run or apply.")
        elig.safe_summary = "Unlinked failure."
        return elig

    # 4. Already resolved? exit_code success, or a later passing run for the task.
    if exit_code == 0:
        elig.blockers.append("failure_already_resolved")
        elig.next_safe_action = _na("Show job", f"remedy job show {job_id} --json",
                                    "Failure exit code is success — no repair needed.")
        elig.safe_summary = "Failure already resolved."
        return elig
    if _later_passing_test(ddir, job_id, elig.task_id, art):
        elig.blockers.append("failure_already_resolved")
        elig.next_safe_action = _na("Show job", f"remedy job show {job_id} --json",
                                    "A later passing test resolved this failure.")
        elig.safe_summary = "Failure resolved by later passing test."
        return elig

    # 5. Idempotent return for an existing resumable attempt / unresolved intent.
    existing = find_repair_attempt(job, failure_artifact_id, source)
    if existing is not None and existing.status in _RESUMABLE_STATUSES:
        if existing.repair_intent_id and get_patch_intent(job, existing.repair_intent_id):
            elig.existing_repair_intent_id = existing.repair_intent_id
        elig.eligible = True
        elig.safe_summary = "Existing repair attempt resumable."
        return elig

    # 6. RunContract allows metadata repair actions.
    contract = ensure_contract(job)
    decision = evaluate_run_action(contract, ContractAction.CREATE_FIX_TASK)
    if not decision.allowed:
        elig.blockers.append("contract_repair_denied")
        elig.next_safe_action = _na("Review contract", f"remedy contract inspect {job_id} --json",
                                    "RunContract denies repair metadata actions.")
        elig.safe_summary = "Contract denies repair."
        return elig

    elig.eligible = True
    elig.safe_summary = "Eligible for repair proposal."
    return elig


def _later_passing_test(data_dir: Path, job_id: str, task_id: str, failure_art: Any) -> bool:
    """True if a passing test for the same task occurred after this failure."""
    if not task_id:
        return False
    fa_created = (failure_art.metadata or {}).get("created_at") or getattr(failure_art, "created_at", "") or ""
    for e in _load_events_safe(data_dir, job_id):
        if e.get("event") != "test_run_completed":
            continue
        m = e.get("metadata", {})
        if str(m.get("task_id", "")) == task_id and m.get("exit_code") == 0:
            ts = e.get("timestamp", "")
            if not fa_created or (ts and str(ts) > str(fa_created)):
                return True
    return False


# ---------------------------------------------------------------------------
# Fix task (Step 1198)
# ---------------------------------------------------------------------------


def _find_fix_task(job: Any, failure_artifact_id: str) -> Any:
    for task in job.tasks:
        if (task.inputs or {}).get("failure_artifact_id") == failure_artifact_id:
            return task
    return None


def create_or_reuse_fix_task(job: Any, ctx: RepairContextSummary, attempt_id: str) -> Any:
    """Create (or reuse) a Fix Task linked to the failure (Step 1198). Idempotent."""
    from packages.core.models import Task
    from packages.orchestration.storage import save_job

    existing = _find_fix_task(job, ctx.failure_artifact_id)
    if existing is not None:
        return existing

    run_short = (ctx.test_run_id or ctx.failure_artifact_id)[:8]
    task = Task(
        description=f"Fix failing test from {run_short}"[:200],
        inputs={
            "failure_artifact_id": ctx.failure_artifact_id,
            "test_run_id": ctx.test_run_id,
            "original_task_id": ctx.task_id,
            "original_intent_id": ctx.intent_id,
            "apply_id": ctx.apply_id,
            "repair_attempt_id": attempt_id,
            "failure_kind": ctx.failure_kind,
            "safe_summary": ctx.safe_summary[:200],
            "repair_fix_task": True,
        },
    )
    job.tasks.append(task)
    save_job(job)
    return task


# ---------------------------------------------------------------------------
# Fixture repair builder + repair patch intent (Steps 1199-1200)
# ---------------------------------------------------------------------------


def _find_repair_artifact(job: Any, attempt_id: str) -> Any:
    for art in job.artifacts:
        m = art.metadata or {}
        if m.get("repair_v1") and m.get("repair_attempt_id") == attempt_id:
            return art
    return None


def build_fixture_repair(
    job: Any, ctx: RepairContextSummary, fix_task: Any, attempt_id: str,
    *, source_fixture: bool = False,
) -> RepairPatchIntentResult | None:
    """Deterministic fixture repair builder v1 (Steps 1199-1200; classified 1221/1233).

    Produces a real, safe Repair Artifact that yields a pending Patch Intent for
    supported deterministic failure kinds. By default the proposed change is a
    docs-only repair note (`expected_effect=documentation_only`) — it never
    touches source. When `source_fixture` is requested AND the failure carries a
    safe opt-in `repair_fixture_target`, a `source_fix` intent targeting that
    repo-relative path is proposed instead (Step 1233). Either way: never applies,
    never runs a command, no raw output. Unsupported failures return None.
    """
    if not ctx.fixture_supported:
        return None

    from packages.core.models import Artifact, ArtifactKind
    from packages.orchestration.approval_queue import get_patch_intent, make_intent_id
    from packages.orchestration.storage import save_job

    existing = _find_repair_artifact(job, attempt_id)
    if existing is not None:
        intent_id = make_intent_id(existing.id, 0)
        intent = get_patch_intent(job, intent_id)
        if intent is not None:
            em = existing.metadata or {}
            return RepairPatchIntentResult(
                repair_artifact_id=str(existing.id), repair_intent_id=intent_id,
                approval_state=intent.get("state", "pending"), risk=intent.get("risk", "low"),
                target_paths=[intent.get("target_path", "")], resolvable=True,
                repair_kind=em.get("repair_kind", REPAIR_KIND_DOCS_FIXTURE),
                expected_effect=em.get("expected_effect", EXPECT_DOCUMENTATION_ONLY),
            )

    fa_short = ctx.failure_artifact_id[:8]
    # Classification: opt-in source fixture only when a safe target is supplied.
    if source_fixture and ctx.source_fixture_target:
        repair_kind = REPAIR_KIND_SOURCE_FIXTURE
        expected_effect = EXPECT_SOURCE_FIX
        target = ctx.source_fixture_target
        action = "modify"
        reason = f"Apply the deterministic source fixture repair for failure {fa_short}."
    else:
        repair_kind = REPAIR_KIND_DOCS_FIXTURE
        expected_effect = EXPECT_DOCUMENTATION_ONLY
        target = f"docs/repairs/{fa_short}.md"
        action = "create"
        reason = f"Document the repair plan for failure {fa_short} ({ctx.failure_kind})."

    repair_art = Artifact(
        name=f"repair-v1-{fa_short}",
        content=f"Repair proposal for failure {fa_short} ({ctx.failure_kind}).",
        kind=ArtifactKind.BUILDER_PROPOSAL,
        task_id=fix_task.id,
        metadata={
            "repair_v1": True,
            "fixture": True,
            "repair_attempt_id": attempt_id,
            "failure_artifact_id": ctx.failure_artifact_id,
            "repair_kind": repair_kind,
            "expected_effect": expected_effect,
            # Classification linkage (Step 1221) — original failure context IDs.
            "original_test_run_id": ctx.test_run_id,
            "original_apply_id": ctx.apply_id,
            "original_intent_id": ctx.intent_id,
            "original_task_id": ctx.task_id,
            "safe_summary": f"Fixture repair ({expected_effect}) for {ctx.failure_kind}",
            "patch_intent_explanations": [
                {
                    "file": target,
                    "action": action,
                    "risk": "low",
                    "reason": reason,
                    "summary": f"Repair for: {ctx.safe_summary[:100]}",
                },
            ],
            "patch_intent_approvals": {},
        },
    )
    job.artifacts.append(repair_art)
    save_job(job)

    intent_id = make_intent_id(repair_art.id, 0)
    # Verify the intent is real + resolvable before claiming it exists.
    reloaded_intent = get_patch_intent(job, intent_id)
    if reloaded_intent is None:
        return None
    return RepairPatchIntentResult(
        repair_artifact_id=str(repair_art.id), repair_intent_id=intent_id,
        approval_state=reloaded_intent.get("state", "pending"),
        risk=reloaded_intent.get("risk", "low"),
        target_paths=[target], resolvable=True,
        repair_kind=repair_kind, expected_effect=expected_effect,
    )


# ---------------------------------------------------------------------------
# Orchestrator (Steps 1194/1199/1200/1205) — repair propose
# ---------------------------------------------------------------------------


def _approve_action(job_id: str, intent_id: str) -> DoRunNextAction:
    return _na("Approve repair patch", f"remedy patch approve {job_id} {intent_id}",
               "Review and approve the repair patch intent. Apply runs separately.")


def _show_action(job_id: str) -> DoRunNextAction:
    return _na("Show job", f"remedy job show {job_id} --json",
               "Review the fix task and failure evidence.")


def _result_from_attempt(attempt: RepairAttempt, *, resumed: bool, phases: list, na: DoRunNextAction | None, summary: str) -> RepairAttemptResult:
    return RepairAttemptResult(
        job_id=attempt.job_id, failure_artifact_id=attempt.failure_artifact_id,
        attempt_id=attempt.attempt_id, test_run_id=attempt.test_run_id,
        task_id=attempt.task_id, intent_id=attempt.intent_id, apply_id=attempt.apply_id,
        repair_task_id=attempt.repair_task_id, repair_artifact_id=attempt.repair_artifact_id,
        repair_intent_id=attempt.repair_intent_id, status=attempt.status,
        stop_reason=attempt.stop_reason, evidence_status=attempt.evidence_status,
        resumed=resumed, phases=phases, next_safe_action=na, safe_summary=summary,
        created_at=attempt.created_at, source=attempt.source,
    )


def run_repair_attempt(
    job_id: str,
    failure_artifact_id: str,
    *,
    fixture_builder: bool = False,
    source_fixture_builder: bool = False,
    data_dir: "Path | None" = None,
    source: str = "cli_v1",
) -> RepairAttemptResult:
    """One repair proposal cycle (Steps 1194-1200). Creates a Patch Intent only.

    Idempotent: a repeated call returns the same attempt without duplicating the
    Fix Task, Repair Artifact, or Patch Intent. No apply, no test execution, no
    provider, no revert. Stops at approval_required (intent created) or
    repair_builder_unavailable.
    """
    from uuid import uuid4
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.storage import load_job, JobNotFoundError
    from packages.orchestration.run_contract import (
        ensure_contract, evaluate_run_action, ContractAction,
    )
    from packages.orchestration.approval_queue import get_patch_intent

    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    phases: list[dict[str, str]] = []
    _emit_repair(ddir, job_id, "repair_attempt_requested",
                 {"failure_artifact_id": failure_artifact_id, "source": source})

    # --- Eligibility ---
    elig = evaluate_repair_eligibility(job_id, failure_artifact_id, ddir, source=source)
    phases.append({"phase": "eligibility", "status": "completed" if elig.eligible else "blocked",
                   "safe_summary": elig.safe_summary})
    if not elig.eligible:
        _emit_repair(ddir, job_id, "repair_attempt_blocked",
                     {"failure_artifact_id": failure_artifact_id, "blockers": elig.blockers})
        return RepairAttemptResult(
            job_id=job_id, failure_artifact_id=failure_artifact_id,
            status=RepairStatus.BLOCKED, stop_reason=RepairStopReason.BLOCKED_INELIGIBLE,
            phases=phases, next_safe_action=elig.next_safe_action,
            safe_summary=elig.safe_summary, created_at=_now(), source=source,
        )

    try:
        job = load_job(UUID(job_id), ddir)
    except (ValueError, JobNotFoundError):
        return RepairAttemptResult(
            job_id=job_id, failure_artifact_id=failure_artifact_id,
            status=RepairStatus.FAILED, stop_reason=RepairStopReason.ERROR,
            phases=phases, created_at=_now(), source=source,
        )

    # --- Idempotent resume ---
    existing = find_repair_attempt(job, failure_artifact_id, source)
    if existing is not None and existing.status in _RESUMABLE_STATUSES:
        na = None
        if existing.repair_intent_id and get_patch_intent(job, existing.repair_intent_id):
            na = _approve_action(job_id, existing.repair_intent_id)
        else:
            na = _show_action(job_id)
        phases.append({"phase": "resume", "status": "resumed",
                       "safe_summary": f"Existing attempt {existing.attempt_id[:8]} ({existing.status})"})
        return _result_from_attempt(existing, resumed=True, phases=phases, na=na,
                                    summary="Resumed existing repair attempt — no duplicates created.")

    # --- Context ---
    ctx = build_repair_context(job_id, failure_artifact_id, ddir)
    if ctx.status != "context_ready":
        _emit_repair(ddir, job_id, "repair_attempt_blocked",
                     {"failure_artifact_id": failure_artifact_id, "blocker": ctx.blocker})
        phases.append({"phase": "context", "status": "blocked", "safe_summary": ctx.blocker})
        return RepairAttemptResult(
            job_id=job_id, failure_artifact_id=failure_artifact_id,
            status=RepairStatus.BLOCKED, stop_reason=RepairStopReason.BLOCKED_INELIGIBLE,
            phases=phases, next_safe_action=_show_action(job_id),
            safe_summary=f"Context blocked: {ctx.blocker}", created_at=_now(), source=source,
        )
    _emit_repair(ddir, job_id, "repair_context_built",
                 {"failure_artifact_id": failure_artifact_id, "failure_kind": ctx.failure_kind,
                  "fixture_supported": ctx.fixture_supported})
    phases.append({"phase": "context", "status": "completed", "safe_summary": "Repair context ready"})

    # --- New attempt ---
    attempt = RepairAttempt(
        attempt_id=uuid4().hex[:12], job_id=job_id, failure_artifact_id=failure_artifact_id,
        test_run_id=ctx.test_run_id, task_id=ctx.task_id, intent_id=ctx.intent_id,
        apply_id=ctx.apply_id, status=RepairStatus.CONTEXT_READY,
        stop_reason="", source=source, created_at=_now(),
    )

    # --- Fix task ---
    fix_task = create_or_reuse_fix_task(job, ctx, attempt.attempt_id)
    attempt.repair_task_id = str(fix_task.id)
    attempt.status = RepairStatus.FIX_TASK_CREATED
    _emit_repair(ddir, job_id, "repair_fix_task_created",
                 {"fix_task_id": attempt.repair_task_id, "failure_artifact_id": failure_artifact_id})
    phases.append({"phase": "fix_task", "status": "completed",
                   "safe_summary": f"Fix task {attempt.repair_task_id[:8]}"})

    # --- Fixture repair builder (optional) ---
    if fixture_builder:
        contract = ensure_contract(job)
        art_decision = evaluate_run_action(contract, ContractAction.CREATE_REPAIR_ARTIFACT)
        pi_decision = evaluate_run_action(contract, ContractAction.CREATE_REPAIR_PATCH_INTENT)
        if not art_decision.allowed or not pi_decision.allowed:
            attempt.stop_reason = RepairStopReason.BLOCKED_INELIGIBLE
            save_repair_attempt(job, attempt)
            _emit_repair(ddir, job_id, "repair_attempt_blocked",
                         {"failure_artifact_id": failure_artifact_id, "blocker": "contract_patch_intent_denied"})
            phases.append({"phase": "patch_intent", "status": "blocked",
                           "safe_summary": "Contract denies patch intent creation"})
            return _result_from_attempt(attempt, resumed=False, phases=phases,
                                        na=_na("Review contract", f"remedy contract inspect {job_id} --json",
                                               "RunContract denies repair patch intent."),
                                        summary="Blocked: contract denies repair patch intent.")

        intent_result = build_fixture_repair(
            job, ctx, fix_task, attempt.attempt_id,
            source_fixture=source_fixture_builder,
        )
        if intent_result is not None and intent_result.resolvable:
            attempt.repair_artifact_id = intent_result.repair_artifact_id
            attempt.repair_intent_id = intent_result.repair_intent_id
            attempt.repair_kind = intent_result.repair_kind
            attempt.expected_effect = intent_result.expected_effect
            attempt.status = RepairStatus.APPROVAL_REQUIRED
            attempt.stop_reason = RepairStopReason.APPROVAL_REQUIRED
            save_repair_attempt(job, attempt)
            _emit_repair(ddir, job_id, "repair_artifact_created",
                         {"repair_artifact_id": attempt.repair_artifact_id, "failure_artifact_id": failure_artifact_id})
            _emit_repair(ddir, job_id, "repair_patch_intent_created",
                         {"repair_intent_id": attempt.repair_intent_id, "risk": intent_result.risk})
            _emit_repair(ddir, job_id, "repair_approval_required",
                         {"repair_intent_id": attempt.repair_intent_id, "failure_artifact_id": failure_artifact_id})
            phases.append({"phase": "patch_intent", "status": "completed",
                           "safe_summary": f"Repair intent {attempt.repair_intent_id} pending approval"})
            return _result_from_attempt(attempt, resumed=False, phases=phases,
                                        na=_approve_action(job_id, attempt.repair_intent_id),
                                        summary="Repair patch intent created — approval required. No apply.")
        # Unsupported failure for fixture builder.
        attempt.stop_reason = RepairStopReason.REPAIR_BUILDER_UNAVAILABLE
        save_repair_attempt(job, attempt)
        phases.append({"phase": "patch_intent", "status": "skipped",
                       "safe_summary": "Repair builder unavailable for this failure kind"})
        return _result_from_attempt(attempt, resumed=False, phases=phases, na=_show_action(job_id),
                                    summary="Fix task created. Repair builder unavailable — manual or provider repair needed.")

    # --- No fixture builder: fix task only ---
    attempt.stop_reason = RepairStopReason.FIX_TASK_CREATED
    save_repair_attempt(job, attempt)
    phases.append({"phase": "stop", "status": "stopped", "safe_summary": "Fix task created"})
    return _result_from_attempt(attempt, resumed=False, phases=phases, na=_show_action(job_id),
                                summary="Fix task created from failure evidence. No patch intent requested.")


# ---------------------------------------------------------------------------
# Export / summary for v1 (no raw content)
# ---------------------------------------------------------------------------


def export_repair_attempt_json(result: RepairAttemptResult) -> dict[str, Any]:
    """Export RepairAttemptResult as safe JSON (stable schema, no raw content)."""
    out: dict[str, Any] = {
        "version": result.version,
        "job_id": result.job_id,
        "failure_artifact_id": result.failure_artifact_id,
        "attempt_id": result.attempt_id,
        "test_run_id": result.test_run_id,
        "task_id": result.task_id,
        "intent_id": result.intent_id,
        "apply_id": result.apply_id,
        "repair_task_id": result.repair_task_id,
        "repair_artifact_id": result.repair_artifact_id,
        "repair_intent_id": result.repair_intent_id,
        "status": result.status,
        "stop_reason": result.stop_reason,
        "evidence_status": result.evidence_status,
        "resumed": result.resumed,
        "phases": result.phases,
        "safe_summary": result.safe_summary,
        "created_at": result.created_at,
        "source": result.source,
        "next_safe_action": None,
    }
    if result.next_safe_action:
        out["next_safe_action"] = {
            "label": result.next_safe_action.label,
            "command": result.next_safe_action.command,
            "reason": result.next_safe_action.reason,
        }
    return out


def summarize_repair_attempt(result: RepairAttemptResult) -> str:
    """Human-readable repair attempt summary (no raw content)."""
    lines = [
        f"Repair attempt: {result.job_id[:8]}",
        f"Failure: {result.failure_artifact_id[:8] if result.failure_artifact_id else 'none'}",
        f"Status: {result.status}   Stop: {result.stop_reason}",
    ]
    if result.resumed:
        lines.append("(resumed existing attempt — no duplicates)")
    if result.repair_task_id:
        lines.append(f"Fix task: {result.repair_task_id[:8]}")
    if result.repair_intent_id:
        lines.append(f"Repair intent: {result.repair_intent_id} (pending approval)")
    lines.append("")
    for p in result.phases:
        lines.append(f"  [{p.get('status', '?')}] {p.get('phase', '?')}: {p.get('safe_summary', '')}")
    if result.next_safe_action:
        lines.append(f"\nNext: {result.next_safe_action.label}")
        lines.append(f"  $ {result.next_safe_action.command}")
    return "\n".join(lines)


def export_repair_context_json(ctx: RepairContextSummary) -> dict[str, Any]:
    """Export RepairContextSummary as safe JSON (no raw output)."""
    return {
        "version": ctx.version, "job_id": ctx.job_id,
        "failure_artifact_id": ctx.failure_artifact_id, "status": ctx.status,
        "blocker": ctx.blocker, "test_run_id": ctx.test_run_id, "task_id": ctx.task_id,
        "intent_id": ctx.intent_id, "apply_id": ctx.apply_id,
        "command_display": ctx.command_display, "exit_code": ctx.exit_code,
        "failure_kind": ctx.failure_kind, "safe_summary": ctx.safe_summary,
        "changed_files_safe": ctx.changed_files_safe, "proof_status": ctx.proof_status,
        "snapshot_status": ctx.snapshot_status, "hints": ctx.hints,
        "fixture_supported": ctx.fixture_supported,
    }


# ===========================================================================
# Approved Repair Apply Cycle (Steps 1221-1226) — reconcile a repair intent
# AFTER it flows through the existing `do continue` apply/test/proof path.
# This module never applies code itself; it only records repair truth.
# ===========================================================================


REPAIR_APPLY_EVENTS = frozenset({
    "repair_apply_reconciled",
    "repair_failure_resolved",
    "repair_tested_failed",
})


@dataclass
class RepairReconcileResult:
    """Outcome of reconciling a repair intent after a continue cycle (1225)."""

    is_repair: bool = False
    repair_attempt_id: str = ""
    failure_artifact_id: str = ""
    repair_intent_id: str = ""
    status: str = ""
    resolved_failure: bool = False
    new_failure_artifact_id: str = ""
    expected_effect: str = ""


def find_attempt_by_repair_intent(job: Any, intent_id: str) -> RepairAttempt | None:
    """Classify a patch intent as a repair intent (Step 1221). None if normal."""
    if not intent_id:
        return None
    for attempt in load_repair_attempts(job).values():
        if attempt.repair_intent_id == intent_id:
            return attempt
    return None


def resolve_failure_if_repaired(
    job: Any,
    failure_artifact_id: str,
    repair_attempt_id: str,
    test_run_id: str,
    *,
    expected_effect: str,
    snapshot_verified: bool,
    proof_status: str,
    evidence_status: str,
) -> bool:
    """Mark the original failure resolved ONLY with full proven evidence (1226).

    Requires: a verified snapshot, a linked post-repair test that PASSED
    (test_run_id present), complete evidence, proof verified, and a repair whose
    expected_effect is a source fix. A documentation_only / unknown repair never
    resolves a source failure (no overclaim). Mutates + saves the job. Returns
    True only when the failure was newly resolved.
    """
    from packages.orchestration.storage import save_job

    if expected_effect != EXPECT_SOURCE_FIX:
        return False
    if not test_run_id or not snapshot_verified:
        return False
    if evidence_status != "complete" or proof_status != "verified":
        return False

    target = None
    for art in job.artifacts:
        if str(art.id) == failure_artifact_id and (art.metadata or {}).get("test_failure"):
            target = art
            break
    if target is None:
        return False
    if (target.metadata or {}).get("failure_resolved"):
        return False  # already resolved — idempotent

    target.metadata["failure_resolved"] = True
    target.metadata["resolved_by_repair_attempt_id"] = repair_attempt_id
    target.metadata["resolved_by_test_run_id"] = test_run_id
    target.metadata["resolved_at"] = _now()
    save_job(job)
    return True


def _link_new_failure(job: Any, new_failure_artifact_id: str, attempt: RepairAttempt) -> None:
    """Link a post-repair failure to its repair attempt + the prior failure."""
    from packages.orchestration.storage import save_job
    for art in job.artifacts:
        if str(art.id) == new_failure_artifact_id and (art.metadata or {}).get("test_failure"):
            art.metadata["repair_attempt_id"] = attempt.attempt_id
            art.metadata["supersedes_failure_artifact_id"] = attempt.failure_artifact_id
            save_job(job)
            return


def reconcile_repair_after_continue(
    job_id: str,
    intent_id: str,
    *,
    apply_id: str,
    test_status: str,
    test_run_id: str,
    failure_artifact_id: str,
    snapshot_verified: bool,
    evidence_status: str,
    proof_status: str,
    data_dir: "Path | None" = None,
) -> RepairReconcileResult:
    """Record repair truth after `do continue` applied + tested a repair intent.

    Idempotent: re-running for the same test_run_id does not re-resolve or
    duplicate. Returns is_repair=False for normal (non-repair) intents — a no-op.
    Never applies code, never runs tests; it only reflects the outcome.
    """
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.storage import load_job, JobNotFoundError

    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    out = RepairReconcileResult()
    try:
        job = load_job(UUID(job_id), ddir)
    except (ValueError, JobNotFoundError):
        return out

    attempt = find_attempt_by_repair_intent(job, intent_id)
    if attempt is None:
        return out  # not a repair intent — no-op

    out.is_repair = True
    out.repair_attempt_id = attempt.attempt_id
    out.failure_artifact_id = attempt.failure_artifact_id
    out.repair_intent_id = attempt.repair_intent_id
    out.expected_effect = attempt.expected_effect

    # Idempotency: already reconciled for this test run.
    if attempt.post_repair_test_run_id == test_run_id and attempt.status in (
        RepairStatus.TESTED_PASSED, RepairStatus.TESTED_FAILED
    ):
        out.status = attempt.status
        out.resolved_failure = attempt.resolved_failure
        return out

    attempt.repair_apply_id = apply_id
    attempt.post_repair_test_run_id = test_run_id

    if test_status == "passed":
        attempt.status = RepairStatus.TESTED_PASSED
        resolved = resolve_failure_if_repaired(
            job, attempt.failure_artifact_id, attempt.attempt_id, test_run_id,
            expected_effect=attempt.expected_effect, snapshot_verified=snapshot_verified,
            proof_status=proof_status, evidence_status=evidence_status,
        )
        attempt.resolved_failure = resolved
        out.resolved_failure = resolved
        if resolved:
            _emit_repair(ddir, job_id, "repair_failure_resolved", {
                "failure_artifact_id": attempt.failure_artifact_id,
                "repair_attempt_id": attempt.attempt_id, "test_run_id": test_run_id,
            })
    elif test_status in ("failed", "timeout"):
        attempt.status = RepairStatus.TESTED_FAILED
        if failure_artifact_id and failure_artifact_id != attempt.failure_artifact_id:
            _link_new_failure(job, failure_artifact_id, attempt)
            out.new_failure_artifact_id = failure_artifact_id
        _emit_repair(ddir, job_id, "repair_tested_failed", {
            "repair_attempt_id": attempt.attempt_id,
            "new_failure_artifact_id": out.new_failure_artifact_id,
        })
    elif evidence_status not in ("complete",):
        attempt.status = RepairStatus.EVIDENCE_INCOMPLETE
    else:
        attempt.status = RepairStatus.APPLIED

    out.status = attempt.status
    save_repair_attempt(job, attempt)
    _emit_repair(ddir, job_id, "repair_apply_reconciled", {
        "repair_attempt_id": attempt.attempt_id, "status": attempt.status,
        "resolved_failure": out.resolved_failure,
    })
    return out
