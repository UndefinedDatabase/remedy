"""
Review Bundle v1 — safe state package for reviewers.

Generates a zip file containing safe summaries only:
manifest, job summary, proof chains, event summary, trust report,
context inspection, changed files, repair summary, command summary,
and a readme.

No raw artifact bodies. No raw diffs. No raw source files.
No stdout/stderr. No secrets. No .env. No __pycache__.

Public API::

    build_review_bundle(job_id, output_path=None) -> ReviewBundleResult
    export_review_bundle_json(result) -> dict
    summarize_review_bundle(result) -> str
"""

from __future__ import annotations

import json
import logging
import re
import zipfile
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID

logger = logging.getLogger(__name__)

BUNDLE_VERSION = 1

REQUIRED_SECTIONS = (
    "manifest.json",
    "job_summary.json",
    "proof_chains.json",
    "event_summary.json",
    "trust_report.json",
    "context_inspection.json",
    "changed_files_safe.json",
    "snapshot_summary.json",
    "continuation_summary.json",
    "repair_summary.json",
    "overnight_readiness_summary.json",
    "overnight_run_summary.json",
    "provider_trust_summary.json",
    "provider_material_summary.json",
    "provider_verification_summary.json",
    "repair_request_summary.json",
    "self_dogfood_summary.json",
    "self_execution_summary.json",
    "orchestrator_decision_summary.json",
    "local_advisor_summary.json",
    "builder_routing_summary.json",
    "local_candidate_summary.json",
    "candidate_quality_summary.json",
    "external_builder_summary.json",
    "worker_registry_summary.json",
    "token_economy_summary.json",
    "model_route_tournament_summary.json",
    "overnight_mission_summary.json",
    "snapshot_rollback_summary.json",
    "repair_loop_summary.json",
    "main_builder_adapter_summary.json",
    "managed_execution_summary.json",
    "dogfood_run_summary.json",
    "command_summary.json",
    "progress_ledger.json",
    "integrity_summary.json",
    "run_contract_summary.json",
    "test_execution_summary.json",
    "config_summary.json",
    "self_repair_proposal_summary.json",
    "execution_approval_policy_summary.json",
    "bundle_readme.md",
)

_UNSAFE_PATTERNS = frozenset({
    "__pycache__", ".pyc", ".pyo", ".env", ".data",
    "node_modules", "dist", "build", ".cache", ".git",
    "secrets", "credentials", "token",
})

_PROTECTED_OUTPUT_DIRS = frozenset({
    ".git", ".env", "node_modules", "__pycache__",
    ".venv", "venv", "dist", "build", ".cache",
})


# ---------------------------------------------------------------------------
# Models (Step 977)
# ---------------------------------------------------------------------------


SECTION_ERROR_CATEGORIES = (
    "section_builder_error",
    "optional_data_unavailable",
    "import_error",
    "validation_error",
    "io_error",
    "permission_error",
    "unknown_error",
)


def _categorize_exception(exc: BaseException) -> str:
    if isinstance(exc, ImportError):
        return "import_error"
    if isinstance(exc, (ValueError, TypeError, KeyError)):
        return "validation_error"
    if isinstance(exc, PermissionError):
        return "permission_error"
    if isinstance(exc, OSError):
        return "io_error"
    return "section_builder_error"


_SAFE_MSG_SECRET_RE: re.Pattern[str] | None = None


def _get_safe_msg_secret_re() -> re.Pattern[str]:
    global _SAFE_MSG_SECRET_RE
    if _SAFE_MSG_SECRET_RE is None:
        from packages.orchestration.redaction_patterns import _SECRET_RE
        _SAFE_MSG_SECRET_RE = _SECRET_RE
    return _SAFE_MSG_SECRET_RE


_HOME_RE = re.compile(r"(/(?:home|Users)/[^\s/]+)")


def _safe_exception_message(exc: BaseException, max_len: int = 240) -> str:
    """Redact secrets and private paths from exception message. No traceback."""
    msg = str(exc)
    if not msg:
        return ""
    msg = _get_safe_msg_secret_re().sub("[REDACTED]", msg)
    msg = _PROTECTED_PATH_RE.sub(lambda m: "[PROTECTED_PATH]", msg)
    msg = _HOME_RE.sub("[PRIVATE_PATH]", msg)
    if len(msg) > max_len:
        msg = msg[:max_len] + "..."
    return msg


@dataclass
class ReviewBundleSectionError:
    """Structured error for a failed review bundle section."""

    section_name: str
    error_type: str
    error_category: str
    safe_message: str
    is_bug: bool = False
    is_optional_dependency: bool = False
    occurred_at: str = ""

    def __post_init__(self) -> None:
        if not self.occurred_at:
            self.occurred_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict[str, Any]:
        return {
            "section_name": self.section_name,
            "error_type": self.error_type,
            "error_category": self.error_category,
            "safe_message": self.safe_message,
            "is_bug": self.is_bug,
            "is_optional_dependency": self.is_optional_dependency,
            "occurred_at": self.occurred_at,
        }


@dataclass
class ReviewBundleSection:
    """One section in the review bundle."""

    filename: str
    status: str = "included"
    error: str = ""
    byte_count: int = 0
    error_type: str = ""
    error_category: str = ""
    error_message: str = ""
    structured_error: ReviewBundleSectionError | None = None


@dataclass
class BundleSafetyReport:
    """Safety check results for the bundle."""

    has_raw_artifacts: bool = False
    has_raw_diffs: bool = False
    has_raw_output: bool = False
    has_secrets: bool = False
    has_pycache: bool = False
    has_env_files: bool = False
    warnings: list[str] = field(default_factory=list)

    @property
    def is_safe(self) -> bool:
        return not any([
            self.has_raw_artifacts,
            self.has_raw_diffs,
            self.has_raw_output,
            self.has_secrets,
            self.has_pycache,
            self.has_env_files,
        ])


@dataclass
class ChangedFileSafe:
    """Safe representation of a changed file."""

    path: str = ""
    status: str = "unknown"
    proof_status: str = ""
    related_task_id: str = ""
    related_intent_id: str = ""
    tested_after_change: bool = False
    safety_flags: list[str] = field(default_factory=list)
    snapshot_verified: bool = False


@dataclass
class ReviewBundleManifest:
    """Bundle manifest."""

    bundle_version: int = BUNDLE_VERSION
    job_id: str = ""
    generated_at: str = ""
    included_sections: list[str] = field(default_factory=list)
    skipped_sections: list[str] = field(default_factory=list)
    safety_warnings: list[str] = field(default_factory=list)


@dataclass
class ReviewBundleResult:
    """Result of building a review bundle."""

    job_id: str = ""
    output_path: str = ""
    bundle_version: int = BUNDLE_VERSION
    generated_at: str = ""
    sections: list[ReviewBundleSection] = field(default_factory=list)
    safety: BundleSafetyReport = field(default_factory=BundleSafetyReport)
    file_count: int = 0
    byte_count: int = 0
    error: str = ""
    diagnostics_version: int = 1
    degraded_section_count: int = 0
    degraded_sections: list[str] = field(default_factory=list)
    section_error_summary: list[dict[str, Any]] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Text redaction (Step 997)
# ---------------------------------------------------------------------------


_PROTECTED_PATH_RE = re.compile(
    r"(?:^|[\s\"'/,;:(\[{])"
    r"("
    r"(?:[a-zA-Z0-9_./-]*/)?"                       # optional directory prefix
    r"(?:\.env(?:\.[a-zA-Z0-9_.-]+)?)"               # .env, .env.secret, .env.local, etc.
    r"|(?:[a-zA-Z0-9_./-]*/)?credentials\.json"      # credentials.json
    r"|(?:[a-zA-Z0-9_./-]*/)?service-account\.json"  # service-account.json
    r"|(?:[a-zA-Z0-9_./-]*/)?secrets\.ya?ml"         # secrets.yaml/yml
    r"|(?:[a-zA-Z0-9_./-]*/)?id_(?:rsa|ed25519|ecdsa)" # SSH keys
    r")"
)


def redact_safe_text(text: str, max_len: int = 200) -> tuple[str, int]:
    """Redact secrets and protected paths from text and bound length.

    Returns (redacted_text, redaction_count).
    """
    from packages.orchestration.redaction_patterns import _SECRET_RE

    redaction_count = 0

    def _replace(m: re.Match[str]) -> str:
        nonlocal redaction_count
        redaction_count += 1
        return "[REDACTED]"

    result = _SECRET_RE.sub(_replace, text)

    def _replace_path(m: re.Match[str]) -> str:
        nonlocal redaction_count
        full = m.group(0)
        path_part = m.group(1)
        prefix = full[: full.index(path_part[0])] if path_part else ""
        redaction_count += 1
        return prefix + "[PROTECTED_PATH]"

    result = _PROTECTED_PATH_RE.sub(_replace_path, result)

    if len(result) > max_len:
        result = result[:max_len] + "..."
        redaction_count += 1

    return result, redaction_count


def _is_protected_path(path: str) -> bool:
    """Check if path is protected — reuses context inspector policy."""
    from packages.orchestration.context_inspector import (
        _PROTECTED_DIRS,
        _PROTECTED_EXACT,
        _PROTECTED_PREFIXES,
        _SECRET_NAMES,
    )
    p = Path(path)
    name = p.name
    if name in _PROTECTED_EXACT:
        return True
    if any(name.startswith(pf) for pf in _PROTECTED_PREFIXES):
        return True
    if name in _SECRET_NAMES:
        return True
    for part in p.parts:
        if part in _PROTECTED_DIRS:
            return True
    return False


# ---------------------------------------------------------------------------
# Path safety (Step 1000)
# ---------------------------------------------------------------------------


def _is_safe_output_path(path: str) -> bool:
    """Reject traversal and protected output destinations. Segment-based."""
    p = Path(path)
    for part in p.parts:
        if part == "..":
            return False
        if part in _PROTECTED_OUTPUT_DIRS:
            return False
        if part.startswith(".env"):
            return False
    return True


def _default_output_path(job_id: str, data_dir: Path) -> Path:
    """Default bundle output path."""
    bundles_dir = data_dir / "review_bundles"
    bundles_dir.mkdir(parents=True, exist_ok=True)
    return bundles_dir / f"{job_id[:8]}-review-bundle.zip"


# ---------------------------------------------------------------------------
# Section spec + registry (Steps 2296-2365)
# ---------------------------------------------------------------------------


@dataclass
class ReviewBundleSectionSpec:
    """Declarative spec for one review bundle section."""

    filename: str
    builder: Callable[..., dict | str]
    required: bool = True
    description: str = ""
    args: tuple[str, ...] = ()


def _build_section_safe(
    spec: ReviewBundleSectionSpec,
    *,
    builder_args: dict[str, Any],
) -> tuple[str, bytes | None, ReviewBundleSection]:
    """Build one section with structured error handling on failure."""
    try:
        positional = [builder_args[a] for a in spec.args]
        raw = spec.builder(*positional)
        if isinstance(raw, str):
            content = raw.encode("utf-8")
        else:
            content = json.dumps(raw, indent=2).encode("utf-8")
        section = ReviewBundleSection(
            spec.filename, status="included", byte_count=len(content),
        )
        return spec.filename, content, section
    except Exception as exc:
        error_type = type(exc).__name__
        error_category = _categorize_exception(exc)
        safe_msg = _safe_exception_message(exc)
        is_optional = error_category == "import_error"
        is_bug = error_category not in ("import_error", "optional_data_unavailable")

        structured_error = ReviewBundleSectionError(
            section_name=spec.filename,
            error_type=error_type,
            error_category=error_category,
            safe_message=safe_msg,
            is_bug=is_bug,
            is_optional_dependency=is_optional,
        )

        logger.warning(
            "Review bundle section %s failed: %s: %s",
            spec.filename, error_type, safe_msg,
            exc_info=True,
        )

        degraded_data = {
            "status": "degraded",
            "reason": f"{spec.filename} build failed",
            "error_type": error_type,
            "error_category": error_category,
            "error_message": safe_msg,
            "section_name": spec.filename,
        }
        degraded_content = json.dumps(degraded_data, indent=2).encode("utf-8")

        section = ReviewBundleSection(
            spec.filename,
            status="degraded",
            error=f"{error_type}: {safe_msg}" if safe_msg else error_type,
            byte_count=len(degraded_content),
            error_type=error_type,
            error_category=error_category,
            error_message=safe_msg,
            structured_error=structured_error,
        )
        return spec.filename, degraded_content, section


# ---------------------------------------------------------------------------
# Section builders (Steps 978-983)
# ---------------------------------------------------------------------------


def _build_job_summary(job: Any) -> dict:
    """Safe job summary — no raw content, no raw prompt."""
    tasks_summary = []
    for t in job.tasks:
        safe_desc, _ = redact_safe_text(t.description, max_len=100)
        tasks_summary.append({
            "task_id": str(t.id)[:8],
            "description": safe_desc,
            "status": t.status.value,
            "task_type": t.inputs.get("task_type", "unknown"),
        })

    artifacts_summary = []
    for a in job.artifacts:
        safe_name, _ = redact_safe_text(a.name, max_len=60)
        artifacts_summary.append({
            "artifact_id": str(a.id)[:8],
            "name": safe_name,
            "kind": a.kind.value if hasattr(a.kind, "value") else str(a.kind),
            "has_patch_intent": bool(a.metadata.get("patch_intent_explanations")),
            "is_test_failure": bool(a.metadata.get("test_failure")),
            "is_repair": bool(a.metadata.get("repair")),
        })

    prompt = job.user_prompt or ""
    safe_prompt, prompt_redactions = redact_safe_text(prompt, max_len=200)

    return {
        "job_id": str(job.id),
        "name": job.name[:60],
        "state": job.state.value,
        "user_prompt_present": bool(prompt),
        "user_prompt_length": len(prompt),
        "user_prompt_safe_summary": safe_prompt if prompt_redactions == 0 else None,
        "user_prompt_redacted": prompt_redactions > 0,
        "task_count": len(job.tasks),
        "artifact_count": len(job.artifacts),
        "tasks": tasks_summary,
        "artifacts": artifacts_summary,
    }


def _build_event_summary(events: list[dict]) -> dict:
    """Safe event summary — counts by type, no raw metadata."""
    counts: dict[str, int] = {}
    latest_ts = ""
    for ev in events:
        etype = ev.get("event", "unknown")
        counts[etype] = counts.get(etype, 0) + 1
        ts = ev.get("timestamp", ev.get("ts", ""))
        if ts > latest_ts:
            latest_ts = ts

    repair_events = sum(v for k, v in counts.items() if "repair" in k or "failure" in k)
    proof_events = counts.get("proof_chain_built", 0)
    apply_events = sum(v for k, v in counts.items() if "apply" in k)
    test_events = sum(v for k, v in counts.items() if "test" in k)

    return {
        "total_events": len(events),
        "event_counts": counts,
        "latest_timestamp": latest_ts,
        "repair_events": repair_events,
        "proof_events": proof_events,
        "apply_events": apply_events,
        "test_events": test_events,
    }


def _build_changed_files_safe(job: Any, events: list[dict]) -> dict:
    """Safe changed file list from available sources. Protected paths excluded."""
    files: dict[str, ChangedFileSafe] = {}
    redacted_count = 0

    for a in job.artifacts:
        explanations = a.metadata.get("patch_intent_explanations", [])
        apply_records = a.metadata.get("patch_intent_apply_records", {})
        for exp in explanations:
            path = exp.get("file", "")
            if not path or path.startswith("/") or ".." in Path(path).parts:
                continue
            if _is_protected_path(path):
                redacted_count += 1
                continue
            if path not in files:
                files[path] = ChangedFileSafe(path=path)
            files[path].status = exp.get("action", "unknown")
            if a.task_id:
                files[path].related_task_id = str(a.task_id)[:8]
            from packages.orchestration.approval_queue import make_intent_id
            iid = make_intent_id(a.id, 0)
            files[path].related_intent_id = iid
            # Snapshot verification status (Step 1149) — safe bool only, no blob content
            rec = apply_records.get(iid, {})
            if rec.get("snapshot_verified", False):
                files[path].snapshot_verified = True

    for ev in events:
        if ev.get("event") == "test_completed" or ev.get("event") == "test_passed":
            tested_path = ev.get("path", "")
            if tested_path in files:
                files[tested_path].tested_after_change = True

    return {
        "files": [
            {
                "path": f.path,
                "status": f.status,
                "proof_status": f.proof_status,
                "related_task_id": f.related_task_id,
                "related_intent_id": f.related_intent_id,
                "tested_after_change": f.tested_after_change,
                "safety_flags": f.safety_flags,
                "snapshot_verified": f.snapshot_verified,
            }
            for f in files.values()
        ],
        "redacted_protected_path_count": redacted_count,
    }


def _build_snapshot_summary(job_id: str, data_dir: Path) -> dict:
    """Safe snapshot/apply-record aggregate summary (Step 1160).

    Sourced from the authoritative snapshot-truth builder. Contains safe counts
    and non-path identifiers only — no recovery blob references, no source
    content, no raw/absolute/protected paths.
    """
    try:
        from packages.orchestration.repository_snapshot import (
            build_snapshot_truth,
            list_durable_apply_ids,
        )

        apply_ids = list_durable_apply_ids(job_id, data_dir)
        snapshot_ids: set[str] = set()
        snapshot_count = 0
        verified_count = 0
        verification_failed_count = 0
        active_apply_count = 0
        reverted_count = 0
        drift_blocked_count = 0
        partial_revert_count = 0
        revert_failed_count = 0
        missing_recovery_count = 0
        evidence_degraded_count = 0
        applies: list[dict] = []

        for aid in apply_ids:
            truth = build_snapshot_truth(job_id, apply_id=aid, data_dir=data_dir)
            if truth.snapshot_id and truth.snapshot_exists:
                if truth.snapshot_id not in snapshot_ids:
                    snapshot_ids.add(truth.snapshot_id)
                    snapshot_count += 1
                if truth.snapshot_verified_now:
                    verified_count += 1
                else:
                    verification_failed_count += 1
                if not truth.recovery_material_available:
                    missing_recovery_count += 1
            if truth.apply_state == "applied":
                active_apply_count += 1
            if truth.apply_state == "reverted" or truth.revert_state == "reverted":
                reverted_count += 1
            if truth.drift_blocked:
                drift_blocked_count += 1
            if truth.revert_state == "partial_revert":
                partial_revert_count += 1
            if truth.revert_state == "revert_failed":
                revert_failed_count += 1
            if truth.evidence_status == "degraded":
                evidence_degraded_count += 1
            applies.append({
                "apply_id": truth.apply_id,
                "snapshot_id": truth.snapshot_id,
                "apply_state": truth.apply_state,
                "revert_state": truth.revert_state,
                "snapshot_verified": truth.snapshot_verified_now,
                "recovery_material_available": truth.recovery_material_available,
                "drift_blocked": truth.drift_blocked,
                "evidence_status": truth.evidence_status,
            })

        return {
            "version": 1,
            "snapshot_count": snapshot_count,
            "verified_count": verified_count,
            "verification_failed_count": verification_failed_count,
            "active_apply_count": active_apply_count,
            "reverted_count": reverted_count,
            "drift_blocked_count": drift_blocked_count,
            "partial_revert_count": partial_revert_count,
            "revert_failed_count": revert_failed_count,
            "missing_recovery_count": missing_recovery_count,
            "evidence_degraded_count": evidence_degraded_count,
            "applies": applies,
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"status": "section_unavailable", "reason": "snapshot summary not available"}


def _build_continuation_summary(job_id: str, data_dir: Path, events: list[dict]) -> dict:
    """Safe `remedy do --continue` summary (Step 1177).

    Current phase, durable checkpoints, apply/test/proof/evidence status, stop
    reason, next-action availability, and safe IDs. No raw prompt, patch, source,
    output, blobs, paths, or secrets.
    """
    try:
        from packages.orchestration.do_continue import (
            CONTINUE_PHASES,
            latest_checkpoint,
            load_checkpoints,
        )
        cps = load_checkpoints(job_id, data_dir)
        if not cps:
            return {"version": 1, "present": False}

        stop_reason = ""
        evidence_status = ""
        proof_status = ""
        test_status = ""
        for ev in events:
            ename = ev.get("event", "")
            m = ev.get("metadata", {}) if isinstance(ev.get("metadata"), dict) else {}
            if ename == "do_continue_stopped":
                stop_reason = m.get("stop_reason", stop_reason)
                evidence_status = m.get("evidence_status", evidence_status)
            elif ename == "do_continue_proof_built":
                proof_status = m.get("proof_status", proof_status)
            elif ename == "do_continue_test_completed":
                test_status = m.get("status", test_status)

        ids: dict[str, str] = {}
        for c in cps:
            ids.update(c.ids or {})

        def _phase_status(p: str) -> str:
            cp = latest_checkpoint(cps, p)
            return cp.status if cp else "pending"

        _NEXT_AVAILABLE = {
            "test_failed_repair_available", "evidence_incomplete", "test_blocked",
            "snapshot_failed", "apply_failed", "blocked_ineligible",
        }
        return {
            "version": 1,
            "present": True,
            "current_phase": cps[-1].phase,
            "phase_status": {p: _phase_status(p) for p in CONTINUE_PHASES},
            "checkpoints": [
                {"phase": c.phase, "status": c.status, "at": c.at,
                 "evidence_status": c.evidence_status}
                for c in cps
            ],
            "apply_status": _phase_status("apply"),
            "test_status": test_status or ids.get("test_status", ""),
            "proof_status": proof_status,
            "evidence_status": evidence_status or cps[-1].evidence_status,
            "stop_reason": stop_reason or ids.get("stop_reason", ""),
            "next_action_available": (stop_reason or ids.get("stop_reason", "")) in _NEXT_AVAILABLE,
            "snapshot_id": ids.get("snapshot_id", ""),
            "apply_id": ids.get("apply_id", ""),
            "test_run_id": ids.get("test_run_id", ""),
            "failure_artifact_id": ids.get("failure_artifact_id", ""),
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"status": "section_unavailable", "reason": "continuation summary not available"}


def _build_repair_summary(job: Any, events: list[dict]) -> dict:
    """Safe repair summary — no raw test output."""
    failure_count = 0
    fix_task_count = 0
    repair_intent_count = 0
    pending_intents = 0
    latest_failure_kind = ""
    next_safe_action = None

    for a in job.artifacts:
        if a.metadata.get("test_failure"):
            failure_count += 1
            kind = a.metadata.get("failure_kind", "")
            if kind:
                latest_failure_kind = kind
        if a.metadata.get("repair"):
            repair_intent_count += 1
            approvals = a.metadata.get("patch_intent_approvals", {})
            explanations = a.metadata.get("patch_intent_explanations", [])
            for idx, _exp in enumerate(explanations):
                from packages.orchestration.approval_queue import make_intent_id
                iid = make_intent_id(a.id, idx)
                state = approvals.get(iid, {}).get("state", "pending")
                if state == "pending":
                    pending_intents += 1

    for t in job.tasks:
        if t.inputs.get("failure_artifact_id"):
            fix_task_count += 1

    for ev in events:
        if ev.get("event") == "repair_loop_stopped":
            meta = ev
            if meta.get("stop_reason") == "awaiting_approval":
                next_safe_action = f"remedy patch approve {str(job.id)} {meta.get('fix_task_id', '?')[:8]}"

    # Repair Loop v1 attempt counts (Step 1208) — safe statuses only, no body.
    repair_attempt_count = 0
    v1_intent_count = 0
    pending_approval_count = 0
    blocked_count = 0
    unavailable_count = 0
    # Approved Repair Apply Cycle counts (Step 1231).
    applied_count = 0
    tested_passed_count = 0
    tested_failed_count = 0
    resolved_failure_count = 0
    evidence_incomplete_count = 0
    attempts = (job.metadata or {}).get("repair_attempts_v1", {})
    if isinstance(attempts, dict):
        for v in attempts.values():
            if not isinstance(v, dict):
                continue
            repair_attempt_count += 1
            status = v.get("status", "")
            stop_reason = v.get("stop_reason", "")
            if v.get("repair_intent_id"):
                v1_intent_count += 1
            if status == "approval_required":
                pending_approval_count += 1
            if status == "blocked":
                blocked_count += 1
            if stop_reason == "repair_builder_unavailable":
                unavailable_count += 1
            if status in ("applied", "tested_passed", "tested_failed"):
                applied_count += 1
            if status == "tested_passed":
                tested_passed_count += 1
            if status == "tested_failed":
                tested_failed_count += 1
            if status == "evidence_incomplete":
                evidence_incomplete_count += 1
            if v.get("resolved_failure"):
                resolved_failure_count += 1

    return {
        "failure_artifact_count": failure_count,
        "repair_attempt_count": repair_attempt_count,
        "fix_task_count": fix_task_count,
        "repair_patch_intent_count": repair_intent_count + v1_intent_count,
        "repair_intent_count": v1_intent_count,
        "pending_repair_intents": pending_intents,
        "pending_approval_count": pending_approval_count,
        "blocked_count": blocked_count,
        "unavailable_count": unavailable_count,
        # Approved Repair Apply Cycle (Step 1231).
        "applied_count": applied_count,
        "tested_passed_count": tested_passed_count,
        "tested_failed_count": tested_failed_count,
        "resolved_failure_count": resolved_failure_count,
        "unresolved_failure_count": max(0, failure_count - resolved_failure_count),
        "evidence_incomplete_count": evidence_incomplete_count,
        "latest_failure_kind": latest_failure_kind,
        "next_safe_action": next_safe_action,
    }


def _build_overnight_readiness_summary(job: Any, data_dir: Path) -> dict:
    """Safe Bounded Overnight Prep summary (Step 1261). Counts/labels only."""
    try:
        from packages.orchestration.overnight_readiness import (
            build_overnight_readiness,
            export_readiness_json,
        )
        report = build_overnight_readiness(str(job.id), data_dir)
        d = export_readiness_json(report)
        caps = d.get("capabilities", [])
        checklist = d.get("checklist", [])
        na = d.get("next_action")
        return {
            "ready": d.get("ready"),
            "can_run_unattended": d.get("can_run_unattended"),
            "readiness_level": d.get("readiness_level"),
            "recommended_mode": d.get("recommended_mode"),
            "blocker_count": len(d.get("blockers", [])),
            "risk_count": len(d.get("risks", [])),
            "capability_counts": {
                "available": sum(1 for c in caps if c["status"] == "available"),
                "blocked": sum(1 for c in caps if c["status"] == "blocked"),
                "unknown": sum(1 for c in caps if c["status"] == "unknown"),
                "not_supported": sum(1 for c in caps if c["status"] == "not_supported"),
            },
            "checklist_counts": {
                "done": sum(1 for i in checklist if i["status"] == "done"),
                "pending": sum(1 for i in checklist if i["status"] == "pending"),
                "blocked": sum(1 for i in checklist if i["status"] == "blocked"),
            },
            "next_action_label": na["label"] if na else "",
            "next_action_command": na["command"] if na else "",
            "budget_summary": d.get("budget_summary", {}),
            "evidence_summary": d.get("evidence_summary", {}),
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"ready": False, "can_run_unattended": False, "readiness_level": "unknown",
                "blocker_count": 0, "risk_count": 0, "error": "overnight_readiness_unavailable"}


def _build_overnight_run_summary(job: Any, data_dir: Path) -> dict:
    """Safe Bounded Overnight Executor run summary (Step 1291). Counts/labels only."""
    try:
        from packages.orchestration.overnight_executor import (
            latest_run_record,
            list_run_records,
        )
        records = list_run_records(str(job.id), data_dir)
        latest = latest_run_record(str(job.id), data_dir)
        if not latest:
            return {"run_count": 0, "latest_status": "none", "selected_action": "",
                    "executed_action": "", "stop_reason": "", "evidence_status": "",
                    "checkpoint_count": 0, "policy_summary": {}, "next_safe_action": ""}
        na = latest.get("next_safe_action") or {}
        return {
            "run_count": len(records),
            "latest_status": latest.get("stop_reason", ""),
            "mode": latest.get("mode", ""),
            "selected_action": (latest.get("selected_action") or {}).get("kind", ""),
            "executed_action": (latest.get("executed_action") or {}).get("kind", ""),
            "stop_reason": latest.get("stop_reason", ""),
            "evidence_status": latest.get("evidence_status", ""),
            "checkpoint_count": len(latest.get("checkpoints", [])),
            "policy_summary": latest.get("policy_summary", {}),
            "review_findings": latest.get("review_findings", {}),
            "next_safe_action": na.get("command", "") if isinstance(na, dict) else "",
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"run_count": 0, "latest_status": "unknown",
                "error": "overnight_run_unavailable"}


def _build_provider_trust_summary(job: Any) -> dict:
    """Safe Provider Trust Gate summary (Step 1324). Counts/codes/IDs only — no raw
    provider output, no diff, no source, no secrets, no absolute paths."""
    try:
        from packages.orchestration.provider_trust import load_trust_reports
        reports = list(load_trust_reports(job).values())
        by_status = {"accepted": 0, "rejected": 0, "needs_human_review": 0}
        finding_codes: dict[str, int] = {}
        finding_sev: dict[str, int] = {}
        pending = 0
        for r in reports:
            st = r.get("trust_status", "")
            if st in by_status:
                by_status[st] += 1
            if st == "accepted" and r.get("repair_intent_id"):
                pending += 1
            for f in r.get("findings", []):
                finding_codes[f.get("code", "")] = finding_codes.get(f.get("code", ""), 0) + 1
                finding_sev[f.get("severity", "")] = finding_sev.get(f.get("severity", ""), 0) + 1
        return {
            "report_count": len(reports),
            "accepted": by_status["accepted"],
            "rejected": by_status["rejected"],
            "needs_review": by_status["needs_human_review"],
            "pending_provider_repair_intents": pending,
            "finding_counts_by_code": finding_codes,
            "finding_counts_by_severity": finding_sev,
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"report_count": 0, "accepted": 0, "rejected": 0, "needs_review": 0,
                "error": "provider_trust_unavailable"}


def _build_provider_verification_summary(job: Any) -> dict:
    """Safe Provider Trust Verification v1 summary (Step 1558). Counts/codes/IDs only —
    no raw candidate, no diff, no source, no secrets, no absolute paths."""
    try:
        from packages.orchestration.provider_trust_verification import load_verification_reports
        reports = list(load_verification_reports(job).values())
        by_decision = {"verification_passed": 0, "needs_human_review": 0,
                       "verification_rejected": 0, "verification_incomplete": 0}
        loop_counts = {"none": 0, "low": 0, "medium": 0, "high": 0}
        finding_codes: dict[str, int] = {}
        finding_sev: dict[str, int] = {}
        pending = 0
        linked_ids: list[str] = []
        for r in reports:
            dec = r.get("decision", "")
            if dec in by_decision:
                by_decision[dec] += 1
            lr = r.get("loop_risk", "none")
            if lr in loop_counts:
                loop_counts[lr] += 1
            if dec == "verification_passed" and r.get("allowed_to_create_intent"):
                pending += 1
            if r.get("verification_id"):
                linked_ids.append(str(r.get("verification_id")))
            for f in r.get("findings", []):
                finding_codes[f.get("code", "")] = finding_codes.get(f.get("code", ""), 0) + 1
                finding_sev[f.get("severity", "")] = finding_sev.get(f.get("severity", ""), 0) + 1
        return {
            "verification_count": len(reports),
            "passed": by_decision["verification_passed"],
            "needs_review": by_decision["needs_human_review"],
            "rejected": by_decision["verification_rejected"],
            "incomplete": by_decision["verification_incomplete"],
            "pending_verification_passed_count": pending,
            "loop_risk_counts": loop_counts,
            "finding_counts_by_code": finding_codes,
            "finding_counts_by_severity": finding_sev,
            "verification_ids": linked_ids[:50],
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"verification_count": 0, "passed": 0, "needs_review": 0, "rejected": 0,
                "incomplete": 0, "error": "provider_verification_unavailable"}


def _build_provider_material_summary(job: Any) -> dict:
    """Safe Provider Patch Materialization summary (Step 1350). Counts/IDs/states
    only — no raw diff, no source, no secrets, no private/absolute paths."""
    try:
        from packages.orchestration.provider_patch_material import load_materials
        materials = list(load_materials(job).values())
        materialized = [m for m in materials if m.get("material_state") == "materialized"]
        failed = [m for m in materials if m.get("material_state") == "materialization_failed"]
        verified = [m for m in materials if m.get("verified")]
        pending = [m for m in materialized if m.get("linked_intent_id")]
        return {
            "material_count": len(materials),
            "materialized_count": len(materialized),
            "verified_count": len(verified),
            "materialization_failed_count": len(failed),
            "provider_repair_intent_count": len(pending),
            "pending_approval_count": len(pending),
            "operation_count": sum(m.get("operation_count", 0) for m in materials),
            "target_file_count": sum(m.get("target_path_count", 0) for m in materials),
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"material_count": 0, "materialized_count": 0, "verified_count": 0,
                "materialization_failed_count": 0, "error": "provider_material_unavailable"}


def _build_repair_request_summary(job: Any) -> dict:
    """Safe Repair Request Builder summary (Step 1380). Counts/labels/IDs only — no
    raw request text, no source, no diffs, no secrets, no absolute paths."""
    try:
        from packages.orchestration.provider_patch_material import load_materials
        from packages.orchestration.repair_request_builder import load_request_packages
        packages = list(load_request_packages(job).values())
        materialized_failures = {m.get("failure_artifact_id") for m in load_materials(job).values()
                                 if m.get("material_state") == "materialized"}
        imported = [p for p in packages if p.get("failure_artifact_id") in materialized_failures]
        pending = [p for p in packages if p.get("failure_artifact_id") not in materialized_failures]
        labels: dict[str, int] = {}
        for p in packages:
            labels[p.get("target_kind", "external")] = labels.get(p.get("target_kind", "external"), 0) + 1
        return {
            "request_package_count": len(packages),
            "target_labels": labels,
            "pending_response_count": len(pending),
            "imported_response_count": len(imported),
            "failure_artifact_ids": sorted({p.get("failure_artifact_id", "") for p in packages if p.get("failure_artifact_id")}),
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"request_package_count": 0, "pending_response_count": 0,
                "imported_response_count": 0, "error": "repair_request_unavailable"}


def _build_self_dogfood_summary(job: Any) -> dict:
    """Safe Self-Dogfood summary (Step 1417). Counts/IDs only — no raw finding body,
    source, diffs, logs, secrets, or absolute paths. Derived from durable self-dogfood
    ProposedTasks (no .agent re-scan in the bundle)."""
    try:
        from packages.orchestration.proposed_tasks import load_proposed_tasks_safe
        tasks, _ = load_proposed_tasks_safe(str(job.id))
        sd = [t for t in tasks if getattr(t, "task_type", "") == "self_dogfood"]
        by_priority: dict[str, int] = {}
        by_status: dict[str, int] = {}
        for t in sd:
            by_priority[t.priority] = by_priority.get(t.priority, 0) + 1
            st = str(t.status.value if hasattr(t.status, "value") else t.status)
            by_status[st] = by_status.get(st, 0) + 1
        return {
            "proposed_task_count": len(sd),
            "by_priority": by_priority,
            "by_status": by_status,
            "high_priority_count": by_priority.get("high", 0),
            "top_item_ids": [t.id for t in sd[:5]],
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"proposed_task_count": 0, "by_priority": {}, "by_status": {},
                "error": "self_dogfood_unavailable"}


def _build_self_execution_summary(job: Any) -> dict:
    """Safe Self-Dogfood Execution summary (Step 1444). Counts/states/IDs only — no
    raw request/candidate content, no diff/source/logs/secrets/paths."""
    try:
        from packages.orchestration.self_dogfood_execution import list_attempts
        attempts = [a for a in list_attempts() if a.get("job_id") == str(job.id)]
        by_state: dict[str, int] = {}
        for a in attempts:
            by_state[a.get("state", "")] = by_state.get(a.get("state", ""), 0) + 1
        return {
            "attempt_count": len(attempts),
            "by_state": by_state,
            "pending_external_candidate": by_state.get("awaiting_external_candidate", 0),
            "pending_approval": by_state.get("intent_pending_approval", 0),
            "applied": by_state.get("applied", 0),
            "tested_passed": by_state.get("tested_passed", 0),
            "tested_failed": by_state.get("tested_failed", 0),
            "completed": by_state.get("completed", 0),
            "blocked": by_state.get("blocked", 0),
            "attempt_ids": [a.get("attempt_id", "") for a in attempts[:10]],
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"attempt_count": 0, "by_state": {}, "error": "self_execution_unavailable"}


def _build_orchestrator_decision_summary(job: Any) -> dict:
    """Safe Orchestrator Brain summary (Step 1483). Latest decision counts/labels/IDs
    only — no raw ideas, source, diffs, logs, secrets, or absolute paths."""
    try:
        from packages.orchestration.orchestrator_brain import list_decisions
        scope = f"job:{job.id}"
        decisions = list_decisions(scope)
        if not decisions:
            return {"decision_count": 0, "latest_selected_option": "", "stop_reason": "none",
                    "confidence": "", "model_routing_tier": "", "loop_guard_status": "",
                    "blocker_count": 0, "risk_count": 0, "next_safe_action": ""}
        latest = decisions[-1]
        sel = latest.get("selected_option") or {}
        return {
            "decision_count": len(decisions),
            "latest_selected_option": sel.get("kind", ""),
            "stop_reason": latest.get("stop_reason", ""),
            "confidence": latest.get("confidence", ""),
            "model_routing_tier": (latest.get("model_routing_plan") or {}).get("tier", ""),
            "loop_guard_status": latest.get("loop_guard_status", ""),
            "blocker_count": len(latest.get("blockers", [])),
            "risk_count": len(latest.get("risks", [])),
            "next_safe_action": latest.get("next_safe_action", ""),
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"decision_count": 0, "stop_reason": "unknown", "error": "orchestrator_unavailable"}


def _build_context_inspection_safe(job: Any, events: list[dict]) -> dict:
    """Safe context inspection summary — no file bodies."""
    try:
        from packages.orchestration.context_inspector import inspect_context
        inspection = inspect_context(job, events)
        return {
            "included_count": len(inspection.included_paths),
            "excluded_count": len(inspection.excluded_paths),
            "protected_count": len(inspection.protected_paths),
            "unsupported_count": len(inspection.unsupported_paths),
            "budget_tokens": inspection.budget_tokens,
            "budget_used_tokens": inspection.budget_used_tokens,
            "budget_remaining_tokens": inspection.budget_remaining_tokens,
            "policy_gates": [
                {"name": g.name, "status": g.status, "reason": g.reason[:100]}
                for g in inspection.policy_gates
            ],
            "tooling": {
                "has_mcp": inspection.tooling.has_mcp,
                "mcp_server_count": inspection.tooling.mcp_server_count,
            } if inspection.tooling else {},
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"status": "section_unavailable", "reason": "context inspection not available"}


def _build_trust_report_safe(job: Any, events: list[dict], data_dir: Path) -> dict:
    """Safe trust report — redacted text summary only."""
    try:
        from packages.orchestration.trust_report import summarize_trust_report
        text = summarize_trust_report(job, events, data_dir=data_dir)
        safe_text, redactions = redact_safe_text(text, max_len=5000)
        return {
            "status": "available",
            "summary_text": safe_text,
            "summary_length": len(safe_text),
            "redaction_count": redactions,
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"status": "section_unavailable", "reason": "trust report not available"}


def _build_proof_chains_safe(job: Any, events: list[dict]) -> dict:
    """Safe proof chains — no raw diffs, no raw goal text."""
    try:
        from packages.orchestration.proof_chain import build_proof_chain, export_proof_chain_json
        chain = build_proof_chain(job, events)
        exported = export_proof_chain_json(chain)
        if "goal" in exported:
            safe_goal, _ = redact_safe_text(str(exported["goal"]), max_len=200)
            exported["goal"] = safe_goal
        safe_changes = []
        redacted_path_count = 0
        for change in exported.get("changes", []):
            path = change.get("target_path", change.get("path", change.get("file", "")))
            if _is_protected_path(path):
                redacted_path_count += 1
                continue
            change.pop("diff_preview", None)
            change.pop("content", None)
            change.pop("raw_diff", None)
            for field in ("reason", "summary", "description"):
                if field in change:
                    change[field], _ = redact_safe_text(str(change[field]), max_len=300)
            safe_changes.append(change)
        exported["changes"] = safe_changes
        exported["redacted_protected_path_count"] = redacted_path_count
        return exported
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"status": "section_unavailable", "reason": "proof chains not available"}


def _build_local_advisor_summary(job: Any) -> dict:
    """Safe Local Model Advisor summary (Step 1519). Run counts / latest status /
    availability / model label / finding+impact counts / durations / safe IDs only — no raw
    prompt/response, source, diffs, logs, secrets, or absolute paths."""
    try:
        from packages.orchestration.local_model_advisor import (
            list_local_advisor_runs,
            load_local_advisor_usage,
        )
        scope = f"job:{job.id}"
        runs = [r for r in list_local_advisor_runs() if r.get("scope") == scope]
        usage = load_local_advisor_usage(scope)
        if not runs:
            return {"run_count": 0, "latest_status": "none", "available": False,
                    "model_name": "", "impact_counts": {}, "finding_severity_counts": {},
                    "duration_ms_total": 0}
        latest = runs[-1]
        impact_counts: dict[str, int] = {}
        sev_counts: dict[str, int] = {}
        for r in runs:
            impact_counts[r.get("decision_impact", "")] = impact_counts.get(r.get("decision_impact", ""), 0) + 1
            for sev, n in (r.get("finding_severity_counts") or {}).items():
                sev_counts[sev] = sev_counts.get(sev, 0) + int(n)
        return {
            "run_count": len(runs),
            "completed_count": usage.get("completed_count", 0),
            "latest_status": latest.get("status", ""),
            "latest_stop_reason": latest.get("stop_reason", ""),
            "latest_decision_impact": latest.get("decision_impact", ""),
            "available": latest.get("status") in ("completed", "reused"),
            "model_name": latest.get("model_name", ""),
            "endpoint_label": latest.get("endpoint_label", ""),
            "impact_counts": impact_counts,
            "finding_severity_counts": sev_counts,
            "duration_ms_total": usage.get("duration_ms_total", 0),
            "prompt_chars_total": usage.get("prompt_chars_total", 0),
            "response_chars_total": usage.get("response_chars_total", 0),
            "latest_run_id": latest.get("advisor_run_id", ""),
            "tokens_used": "unknown",
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"run_count": 0, "latest_status": "unknown", "error": "local_advisor_unavailable"}


def _build_builder_routing_summary(job: Any) -> dict:
    """Safe Expensive Builder Routing v0 summary (Step 1594). Decision counts / selected-tier
    counts / loop+budget block counts / latest tier / safe next action only — no raw prompt/
    response, provider output, source, diffs, logs, secrets, or absolute paths."""
    try:
        from packages.orchestration.builder_routing import load_builder_routing_traces
        scope = f"job:{job.id}"
        traces = load_builder_routing_traces(scope=scope)
        tier_counts: dict[str, int] = {}
        loop_counts: dict[str, int] = {}
        external_recommended = 0
        local_recommended = 0
        blocked = 0
        budget_blocked = 0
        for t in traces:
            tier = t.get("selected_tier", "")
            tier_counts[tier] = tier_counts.get(tier, 0) + 1
            loop_counts[t.get("loop_guard_status", "")] = loop_counts.get(t.get("loop_guard_status", ""), 0) + 1
            if tier == "external_candidate_generator":
                external_recommended += 1
            if tier == "local_candidate_generator":
                local_recommended += 1
            if tier == "no_safe_route":
                blocked += 1
            if t.get("stop_reason") == "budget_exhausted":
                budget_blocked += 1
        latest = traces[-1] if traces else None
        return {
            "routing_decision_count": len(traces),
            "selected_tier_counts": tier_counts,
            "external_recommended_count": external_recommended,
            "local_recommended_count": local_recommended,
            "blocked_count": blocked,
            "budget_block_count": budget_blocked,
            "loop_guard_counts": loop_counts,
            "latest_selected_tier": (latest or {}).get("selected_tier", ""),
            "latest_next_safe_action": (latest or {}).get("next_safe_action", ""),
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"routing_decision_count": 0, "selected_tier_counts": {},
                "error": "builder_routing_unavailable"}


def _build_local_candidate_summary(job: Any) -> dict:
    """Safe Automated Local Candidate Generator v0 summary (Step 1626). Run counts / statuses /
    trust+verification outcomes / materialized-intent count / model label / duration / safe IDs
    only — no raw prompt/output, source, diff, logs, secrets, or absolute paths."""
    try:
        from packages.orchestration.local_candidate_generator import (
            list_local_candidate_runs,
            load_local_candidate_usage,
        )
        runs = [r for r in list_local_candidate_runs() if r.get("job_id") == str(job.id)]
        usage = load_local_candidate_usage(f"job:{job.id}")
        if not runs:
            return {"run_count": 0, "latest_status": "none", "status_counts": {},
                    "materialized_intent_count": 0, "pending_approval_count": 0,
                    "model_name": "", "duration_ms_total": 0}
        status_counts: dict[str, int] = {}
        for r in runs:
            status_counts[r.get("status", "")] = status_counts.get(r.get("status", ""), 0) + 1
        pending = [r for r in runs if r.get("status") == "intent_pending_approval" and r.get("intent_id")]
        latest = runs[-1]
        return {
            "run_count": len(runs),
            "latest_status": latest.get("status", ""),
            "latest_stop_reason": latest.get("stop_reason", ""),
            "status_counts": status_counts,
            "trust_rejected_count": status_counts.get("trust_rejected", 0),
            "verification_rejected_count": status_counts.get("verification_rejected", 0),
            "needs_review_count": status_counts.get("needs_review", 0),
            "materialized_intent_count": len(pending),
            "pending_approval_count": len(pending),
            "model_name": latest.get("model_name", ""),
            "endpoint_label": latest.get("endpoint_label", ""),
            "duration_ms_total": usage.get("duration_ms_total", 0),
            "latest_generation_id": latest.get("generation_id", ""),
            "tokens_used": "unknown",
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"run_count": 0, "latest_status": "unknown", "error": "local_candidate_unavailable"}


def _build_candidate_quality_summary(job: Any) -> dict:
    """Safe Local Candidate Quality Evaluation v1 summary (Step 1663). Evaluation/outcome counts /
    score distribution / model+route scorecards / pending+loop counts / safe IDs only — no raw
    prompt/output/candidate/diff/source/logs/secrets/absolute paths."""
    try:
        from packages.orchestration.candidate_quality import (
            build_candidate_scorecards,
            load_candidate_quality_evaluations,
        )
        evals = load_candidate_quality_evaluations(job_id=str(job.id))
        if not evals:
            return {"evaluation_count": 0, "outcome_counts": {}, "score_band_counts": {},
                    "pending_approval_count": 0, "loop_risk_count": 0}
        outcome_counts: dict[str, int] = {}
        band_counts: dict[str, int] = {}
        pending = loop = 0
        for e in evals:
            outcome_counts[e.get("outcome", "")] = outcome_counts.get(e.get("outcome", ""), 0) + 1
            band = (e.get("score", {}) or {}).get("band", "")
            band_counts[band] = band_counts.get(band, 0) + 1
            if e.get("outcome") == "pending_approval":
                pending += 1
            if (e.get("score", {}) or {}).get("dimensions", {}).get("loop_risk") == "fail":
                loop += 1
        cards = build_candidate_scorecards(job_id=str(job.id))
        return {
            "evaluation_count": len(evals),
            "outcome_counts": outcome_counts,
            "score_band_counts": band_counts,
            "pending_approval_count": pending,
            "loop_risk_count": loop,
            "by_model": cards.get("by_model", {}),
            "by_route_tier": cards.get("by_route_tier", {}),
            "latest_outcome": evals[-1].get("outcome", ""),
            "evaluation_ids": [e.get("evaluation_id", "") for e in evals][:50],
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"evaluation_count": 0, "outcome_counts": {}, "error": "candidate_quality_unavailable"}


def _build_external_builder_summary(job: Any) -> dict:
    """Safe External Builder Sandbox v0 summary (Step 1692). Package/submission counts, states,
    latest safe outcome, related quality evaluations, safe route/source labels, known risks only —
    no raw candidate/package context/output/diff/secrets/absolute paths."""
    try:
        from packages.orchestration.external_builder_sandbox import (
            load_external_packages,
            load_external_submissions,
        )
        pkgs = load_external_packages(job_id=str(job.id))
        subs = load_external_submissions(job_id=str(job.id))
        by_state: dict[str, int] = {}
        sources: set[str] = set()
        for s in subs:
            by_state[s.get("state", "")] = by_state.get(s.get("state", ""), 0) + 1
            if s.get("source_label"):
                sources.add(str(s.get("source_label")))
        latest = subs[-1] if subs else None
        risks = []
        if by_state.get("trust_rejected"):
            risks.append("trust_rejected")
        if by_state.get("verification_rejected"):
            risks.append("verification_rejected")
        return {
            "package_count": len(pkgs),
            "submission_count": len(subs),
            "submissions_by_state": by_state,
            "pending_approval_count": by_state.get("pending_approval", 0),
            "latest_state": (latest or {}).get("state", ""),
            "latest_trust_status": (latest or {}).get("trust_status", ""),
            "latest_verification_decision": (latest or {}).get("verification_decision", ""),
            "source_labels": sorted(sources)[:20],
            "known_risks": risks,
            "submission_ids": [s.get("submission_id", "") for s in subs][:50],
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"package_count": 0, "submission_count": 0, "submissions_by_state": {},
                "error": "external_builder_unavailable"}


def _build_worker_registry_summary(job: Any) -> dict:
    """Safe Worker Registry + Route Policy v0 summary (Step 1729). Worker/kind/cost/risk counts,
    the active route policy summary, local/Ollama preference flags, token-budget warning if present,
    and safe next actions only — no secrets/keys/raw prompts/raw output/absolute paths. Metadata
    only — never indicates a running worker or an available provider."""
    try:
        from packages.orchestration.worker_registry import (
            WorkerSelectionRequest,
            evaluate_worker_selection,
            is_placeholder,
            load_route_policy,
            load_worker_registry,
        )
        specs = load_worker_registry()
        by_kind: dict[str, int] = {}
        by_cost: dict[str, int] = {}
        by_risk: dict[str, int] = {}
        for s in specs:
            by_kind[s.kind] = by_kind.get(s.kind, 0) + 1
            by_cost[s.cost_tier] = by_cost.get(s.cost_tier, 0) + 1
            by_risk[s.risk_tier] = by_risk.get(s.risk_tier, 0) + 1
        policy = load_route_policy(str(job.id))
        selection = evaluate_worker_selection(
            WorkerSelectionRequest(job_id=str(job.id), task_type="repair"), policy=policy,
            registry=specs)
        return {
            "enabled_workers": sum(1 for s in specs if s.enabled),
            "user_selectable_workers": sum(1 for s in specs if s.user_selectable),
            "disabled_workers": sum(1 for s in specs if not s.enabled),
            "placeholder_workers": sum(1 for s in specs if is_placeholder(s)),
            "workers_by_kind": by_kind,
            "cost_distribution": by_cost,
            "risk_distribution": by_risk,
            "route_policy": {
                "policy_id": policy.policy_id,
                "user_selected_worker_ids": list(policy.user_selected_worker_ids),
                "blocked_worker_ids": list(policy.blocked_worker_ids),
                "max_cost_tier": policy.max_cost_tier,
                "max_risk_tier": policy.max_risk_tier,
                "prefer_local_for_cheap_tasks": policy.prefer_local_for_cheap_tasks,
                "prefer_ollama_for_cheap_tasks": policy.prefer_ollama_for_cheap_tasks,
            },
            "recommended_worker_id": selection.recommended_worker_id,
            "requires_human_approval": selection.requires_human_approval,
            "token_budget_warning": selection.token_budget_warning,
            "safe_next_actions": [
                f"remedy route-policy show {str(job.id)} --json",
                f"remedy route-policy evaluate {str(job.id)} --task-type repair --json",
                "remedy worker registry-list --json",
            ],
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"enabled_workers": 0, "user_selectable_workers": 0, "workers_by_kind": {},
                "error": "worker_registry_unavailable"}


def _build_token_economy_summary(job: Any) -> dict:
    """Safe Token Economy + Context Budget v0 summary (Step 1769). Budget profile + estimated band +
    context pack recommendation + warnings + memory-candidate COUNT + safe next actions only — no raw
    prompts/context/source dumps, no secrets, no absolute paths, no provider pricing claims. All
    estimates labeled estimated."""
    try:
        from packages.orchestration.token_economy import token_economy_report
        rep = token_economy_report(str(job.id))
        profile = rep.get("budget_profile", {}) or {}
        est = rep.get("context_budget_estimate", {}) or {}
        pack = rep.get("context_pack_recommendation", {}) or {}
        decision = rep.get("decision", {}) or {}
        return {
            "budget_profile": {
                "max_context_tokens": profile.get("max_context_tokens"),
                "max_total_estimated_tokens": profile.get("max_total_estimated_tokens"),
                "prefer_local_under_tokens": profile.get("prefer_local_under_tokens"),
                "require_human_approval_over_tokens": profile.get("require_human_approval_over_tokens"),
            },
            "estimated_token_band": decision.get("estimated_token_band"),
            "estimated_cost_band": decision.get("estimated_cost_band"),
            "estimated_total_tokens": est.get("estimated_total_tokens"),
            "budget_status": decision.get("budget_status"),
            "context_pack_recommendation": pack.get("recommended_pack_kind"),
            "estimated_token_savings_band": (pack.get("estimated_token_savings", {}) or {}).get("band"),
            "local_first_recommended": (decision.get("estimated_cost_band") in ("free", "cheap")
                                        and not decision.get("requires_human_approval")),
            "requires_human_approval": decision.get("requires_human_approval"),
            "warnings": est.get("warnings", []),
            "memory_candidates_count": len(pack.get("memory_candidates", [])),
            "memory_candidates_persisted": False,
            "estimated": True,
            "verified": False,
            "safe_next_actions": [
                f"remedy token budget-show {str(job.id)} --json",
                f"remedy token economy-report {str(job.id)} --json",
                f"remedy context-pack recommend {str(job.id)} --json",
            ],
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"budget_status": "unknown_budget", "estimated": True,
                "error": "token_economy_unavailable"}


def _build_model_route_tournament_summary(job: Any) -> dict:
    """Safe Model/Route Tournament v0 summary (Step 1810). Reports count, latest status, competitor
    count, evidence status, winner (only if evidence-backed), score-band distribution, token/cost
    tradeoff, next actions — no raw prompts/candidates/diffs/logs/secrets/absolute paths."""
    try:
        from packages.orchestration.model_route_tournament import (
            generate_tournament_report,
            list_tournament_reports,
        )
        reports = list_tournament_reports(job_id=str(job.id))
        rep = generate_tournament_report(str(job.id), persist=False)
        d = rep.to_dict()
        band_dist: dict[str, int] = {}
        for s in d.get("scores", []):
            band_dist[s.get("score_band", "")] = band_dist.get(s.get("score_band", ""), 0) + 1
        winner = next((c for c in d.get("competitors", [])
                       if c.get("competitor_id") == d.get("winner_competitor_id")), None)
        ev_status = "complete" if any(
            e.get("evidence_status") == "complete" for e in d.get("evidence", [])) else (
            "partial" if any(e.get("evidence_status") == "partial" for e in d.get("evidence", []))
            else "insufficient_evidence")
        return {
            "reports_count": len(reports),
            "latest_status": d.get("status"),
            "competitor_count": len(d.get("competitors", [])),
            "evidence_status": ev_status,
            "winner_worker_id": (winner or {}).get("worker_id", ""),
            "confidence": d.get("confidence"),
            "score_band_distribution": band_dist,
            "token_cost_tradeoff": {c.get("worker_id"): c.get("cost_tier")
                                    for c in d.get("competitors", [])},
            "warnings": d.get("warnings", []),
            "next_safe_actions": [
                f"remedy tournament report {str(job.id)} --json",
                f"remedy tournament list {str(job.id)} --json",
            ],
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"reports_count": 0, "latest_status": "insufficient_evidence",
                "error": "model_route_tournament_unavailable"}


def _build_overnight_mission_summary(job: Any) -> dict:
    """Safe Overnight Mission Contract v0 summary (Step 1848). Contract id + status + satisfied flag +
    unsatisfied/finding/gate counts + next actions + user summary only — no raw prompts (beyond a
    scrubbed user_goal), logs, diffs, secrets, or absolute paths."""
    try:
        from packages.orchestration.overnight_mission import (
            _contract_from_dict,
            evaluate_mission_contract,
            list_mission_contracts,
        )
        contracts = list_mission_contracts(job_id=str(job.id))
        if not contracts:
            return {"has_contract": False, "status": "not_started", "satisfied": False,
                    "next_safe_actions": [f"remedy overnight contract-create {str(job.id)} --json"]}
        contract = _contract_from_dict(contracts[-1])
        ev = evaluate_mission_contract(contract, persist=False)
        return {
            "has_contract": True,
            "contract_id": ev.contract_id,
            "status": ev.status,
            "satisfied": ev.satisfied,
            "unsatisfied_criteria_count": len(ev.unsatisfied_criteria),
            "open_findings_count": ev.open_review_findings,
            "open_tasks": ev.open_tasks,
            "failed_tests": ev.failed_tests,
            "missing_gates": ev.missing_proofs,
            "user_decision_required": ev.user_decision_required,
            "required_next_actions": [a.get("command") for a in ev.required_next_actions],
            "next_safe_actions": ev.next_safe_actions,
            "user_summary": ev.user_summary,
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"has_contract": False, "status": "not_started", "satisfied": False,
                "error": "overnight_mission_unavailable"}


def _build_snapshot_rollback_summary(job: Any) -> dict:
    """Safe Snapshot/Rollback Proof v1 summary (Step 1891). Latest test status + snapshot proof count
    + honest rollback restore availability + failure-artifact count + safe next actions only — no raw
    stdout/stderr/logs/secrets/paths. Never claims restore_available for a metadata snapshot."""
    try:
        from packages.orchestration.real_test_execution import (
            list_rollback_proofs,
            list_snapshot_proofs,
            list_test_runs,
        )
        runs = list_test_runs(str(job.id))
        snaps = list_snapshot_proofs(job_id=str(job.id))
        rbs = list_rollback_proofs(job_id=str(job.id))
        latest = runs[-1] if runs else None
        restore_available = any(r.get("restore_available") for r in rbs)
        return {
            "latest_test_status": (latest or {}).get("status", "none"),
            "latest_test_run_id": (latest or {}).get("test_run_id", ""),
            "test_run_count": len(runs),
            "snapshot_proof_count": len(snaps),
            "snapshot_recorded": bool(snaps),
            "rollback_proof_count": len(rbs),
            "rollback_restore_available": restore_available,
            "rollback_restore_tested": False,
            "failure_artifact_count": sum(1 for r in runs if r.get("status") in ("failed", "timeout")),
            "next_safe_actions": [
                f"remedy test list {str(job.id)} --json",
                f"remedy snapshot create {str(job.id)} --json",
            ],
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"latest_test_status": "none", "snapshot_recorded": False,
                "rollback_restore_available": False, "error": "real_test_execution_unavailable"}


def _build_repair_loop_summary(job: Any) -> dict:
    """Safe Token-Aware Repair Loop v1/v2 summary (Step 1934). Open/blocked/repaired counts + latest
    status + attempts + token band + route + review/retest gate + next safe action only — never raw
    stdout/stderr/logs/candidates/diffs/secrets/paths. Honest (no fake repaired)."""
    try:
        from packages.orchestration.repair_loop_v2 import (
            list_repair_attempts,
            list_repair_work_items,
            load_latest_repair_evaluation,
        )
        items = list_repair_work_items(job_id=str(job.id))
        open_count = sum(1 for i in items if i.get("status") not in ("repaired", "abandoned"))
        blocked = sum(1 for i in items if i.get("status") in ("blocked", "abandoned"))
        repaired = sum(1 for i in items if i.get("status") == "repaired")
        latest = items[-1] if items else {}
        latest_id = latest.get("repair_id", "")
        attempts = list_repair_attempts(latest_id, str(job.id)) if latest_id else []
        ev = load_latest_repair_evaluation(latest_id) or {} if latest_id else {}
        token_band = attempts[-1].get("token_estimate_band", "unknown") if attempts else "unknown"
        return {
            "open_repair_count": open_count,
            "blocked_repair_count": blocked,
            "repaired_count": repaired,
            "total_repair_items": len(items),
            "latest_repair_id": latest_id,
            "latest_status": latest.get("status", "none"),
            "attempts_count": len(attempts),
            "token_estimate_band": token_band,
            "review_gate": "see_evaluation",
            "retest_gate": "see_evaluation",
            "satisfied": bool(ev.get("satisfied", False)),
            "next_safe_action": (ev.get("required_next_actions", []) or
                                 [f"remedy repair item-list {str(job.id)} --json"])[0],
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"open_repair_count": 0, "blocked_repair_count": 0, "repaired_count": 0,
                "latest_status": "none", "error": "repair_loop_v2_unavailable"}


def _build_main_builder_adapter_summary(job: Any) -> dict:
    """Safe Main Builder Adapter v0 summary (Step 1991). Configured/enabled adapter counts + latest
    session status + candidate intake + token warning + next safe actions only — never raw prompts/
    transcripts/candidates/diffs/secrets/paths. Honest (no fake running/done)."""
    try:
        from packages.orchestration.main_builder_adapter import (
            list_builder_adapter_specs,
            list_builder_sessions,
        )
        specs = list_builder_adapter_specs()
        sessions = list_builder_sessions(str(job.id))
        enabled = sum(1 for s in specs if s.get("enabled", False))
        latest = sessions[-1] if sessions else {}
        blocked = sum(1 for s in sessions if s.get("status") == "blocked")
        candidate = sum(1 for s in sessions if s.get("status") == "candidate_received")
        intake = sum(1 for s in sessions if s.get("status") == "completed_intake_only")
        return {
            "configured_adapter_count": len(specs),
            "enabled_adapter_count": enabled,
            "session_count": len(sessions),
            "blocked_session_count": blocked,
            "candidate_received_count": candidate,
            "intake_complete_count": intake,
            "latest_session_status": latest.get("status", "none"),
            "latest_adapter_id": latest.get("adapter_id", ""),
            "next_safe_action": latest.get("next_safe_action", ""),
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"configured_adapter_count": 0, "enabled_adapter_count": 0,
                "latest_session_status": "none", "error": "main_builder_adapter_unavailable"}


def _build_dogfood_run_summary(job: Any) -> dict:
    """Safe Dogfood Run Orchestrator v0 summary. Run counts + status + lanes — never raw
    logs/secrets/paths. Honest (no fake satisfied)."""
    try:
        from packages.orchestration.dogfood_run import list_dogfood_runs
        runs = list_dogfood_runs(job_id=str(job.id))
        active = sum(1 for r in runs if r.get("status") not in (
            "satisfied", "blocked", "stopped_by_operator", "budget_exhausted", "error"))
        satisfied = sum(1 for r in runs if r.get("status") == "satisfied")
        blocked = sum(1 for r in runs if r.get("status") in ("blocked", "error"))
        total_steps = sum(r.get("step_count", 0) for r in runs)
        latest = runs[-1] if runs else {}
        latest_stop = latest.get("stop_reason", "") if latest else ""
        latest_next = latest.get("next_suggested_action", "") if latest else ""
        return {
            "run_count": len(runs), "active_count": active,
            "satisfied_count": satisfied, "blocked_count": blocked,
            "total_steps": total_steps,
            "latest_status": latest.get("status", "none"),
            "latest_run_id": latest.get("run_id", ""),
            "latest_stop_reason": latest_stop,
            "latest_next_safe_action": latest_next,
            "morning_report_available": len(runs) > 0,
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"run_count": 0, "latest_status": "none", "error": "dogfood_run_unavailable"}


def _build_managed_execution_summary(job: Any) -> dict:
    """Safe Managed Builder Execution v1.1 summary. Template/execution/approval counts + latest
    status + next safe actions — never raw output/commands/secrets. Honest (no fake done)."""
    try:
        from packages.orchestration.managed_builder_execution import (
            list_command_templates,
            list_execution_approvals,
            list_execution_results,
        )
        templates = list_command_templates()
        results = list_execution_results(str(job.id))
        approvals = list_execution_approvals()
        enabled = sum(1 for t in templates if t.get("enabled", False))
        latest = results[-1] if results else {}
        completed = sum(1 for r in results if r.get("status") == "completed")
        failed = sum(1 for r in results if r.get("status") == "failed")
        blocked = sum(1 for r in results if r.get("status") in ("blocked", "approval_required"))
        # v1.1: approval state summary.
        expired_approvals = 0
        exhausted_approvals = 0
        for a in approvals:
            max_runs = int(a.get("max_runs", 0))
            used = int(a.get("used_count", 0))
            if max_runs > 0 and used >= max_runs:
                exhausted_approvals += 1
            exp = a.get("expires_at", "")
            if exp:
                try:
                    from datetime import datetime, timezone
                    if datetime.now(timezone.utc) > datetime.fromisoformat(exp):
                        expired_approvals += 1
                except (ValueError, TypeError):
                    expired_approvals += 1
        claude_tmpl = next((t for t in templates if t.get("template_id") == "claude-code-repair-v0"), None)
        claude_readiness = {
            "template_exists": claude_tmpl is not None,
            "template_enabled": bool(claude_tmpl and claude_tmpl.get("enabled", False)),
        }
        try:
            from packages.orchestration.main_builder_adapter import get_builder_adapter_spec
            claude_adapter = get_builder_adapter_spec("claude-code-v0")
            claude_readiness["adapter_exists"] = claude_adapter is not None
            claude_readiness["adapter_enabled"] = bool(claude_adapter and claude_adapter.get("enabled", False))
        except (ImportError, OSError):
            claude_readiness["adapter_exists"] = False
            claude_readiness["adapter_enabled"] = False
        return {
            "template_count": len(templates),
            "enabled_template_count": enabled,
            "execution_count": len(results),
            "completed_count": completed,
            "failed_count": failed,
            "blocked_count": blocked,
            "approval_count": len(approvals),
            "expired_approval_count": expired_approvals,
            "exhausted_approval_count": exhausted_approvals,
            "latest_status": latest.get("status", "none"),
            "latest_template_id": latest.get("template_id", ""),
            "next_safe_action": latest.get("next_safe_action", ""),
            "claude_code_readiness": claude_readiness,
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"template_count": 0, "execution_count": 0,
                "latest_status": "none", "error": "managed_execution_unavailable"}


def _build_command_summary(job: Any) -> dict:
    """Safe command summary — commands available for this job."""
    from apps.cli.command_catalog import CATALOG
    relevant_groups = {"repair", "patch", "job", "change", "brain", "review"}
    commands = []
    for cmd in CATALOG:
        if cmd.group_id in relevant_groups:
            commands.append({
                "command_id": cmd.command_id,
                "description": cmd.description[:80],
                "action_class": cmd.action_class,
                "supports_json": cmd.supports_json,
            })
    return {"available_commands": commands, "command_count": len(commands)}


def _build_progress_ledger_safe(job: Any, events: list[dict]) -> dict:
    """Safe progress ledger section — no raw content."""
    try:
        from packages.orchestration.progress_ledger import (
            build_progress_ledger,
            export_progress_ledger_json,
        )
        plan_text = ""
        live_review_text = ""
        context_text = ""
        agent_dir = Path(".agent")
        if agent_dir.exists():
            for name, target_ref in [("plan.md", "plan"), ("live_review.md", "review"), ("context.md", "ctx")]:
                p = agent_dir / name
                if p.exists():
                    text = p.read_text(encoding="utf-8", errors="replace")
                    if target_ref == "plan":
                        plan_text = text
                    elif target_ref == "review":
                        live_review_text = text
                    else:
                        context_text = text

        ledger = build_progress_ledger(
            plan_text=plan_text,
            live_review_text=live_review_text,
            context_text=context_text,
            job=job,
            events=events,
        )
        exported = export_progress_ledger_json(ledger)
        for item in exported.get("items", []):
            if item.get("safe_summary"):
                item["safe_summary"], _ = redact_safe_text(item["safe_summary"], max_len=200)
        return exported
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"status": "section_unavailable", "reason": "progress ledger not available"}


def _build_integrity_summary() -> dict:
    """Safe integrity summary — no raw command output."""
    try:
        from packages.orchestration.integrity_gate import (
            export_integrity_json,
            run_integrity_checks,
        )
        result = run_integrity_checks(collect_only=False)
        exported = export_integrity_json(result)
        # Strip any message content that might leak paths/secrets
        for check in exported.get("checks", []):
            msg = check.get("message", "")
            safe_msg, _ = redact_safe_text(msg, max_len=200)
            check["message"] = safe_msg
        return exported
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"status": "section_unavailable", "reason": "integrity gate not available"}


def _build_contract_summary(job_id: str) -> dict:
    """Safe run contract summary for the review bundle."""
    try:
        from packages.orchestration.run_contract import (
            ensure_contract,
            export_run_contract_json,
            export_usage_json,
            load_usage,
        )
        from packages.orchestration.storage import load_job

        job = load_job(job_id)
        contract = ensure_contract(job)
        exported = export_run_contract_json(contract)
        # Strip fields that might trigger safety scanners
        exported.pop("notes", None)
        exported.pop("denied_paths", None)
        exported.pop("allowed_paths", None)
        exported["denied_paths_count"] = len(contract.denied_paths)
        exported["allowed_paths_count"] = len(contract.allowed_paths)
        exported["usage"] = export_usage_json(load_usage(job))
        return exported
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"status": "section_unavailable", "reason": "run contract not available"}


def _build_test_execution_summary(job: Any, events: list[dict]) -> dict:
    """Safe test execution summary for the review bundle. No raw output."""
    try:
        from packages.orchestration.run_contract import export_usage_json, load_usage

        # Collect test run records from job metadata
        test_runs = job.metadata.get("test_runs") or []
        safe_runs = []
        for r in test_runs[-20:]:  # last 20 only
            safe_runs.append({
                "test_run_id": r.get("test_run_id", ""),
                "contract_id": r.get("contract_id", ""),
                "status": r.get("status", ""),
                "exit_code": r.get("exit_code"),
                "duration_ms": r.get("duration_ms", 0),
                "command_safe": r.get("command_safe", ""),
                "linked_intent_id": r.get("linked_intent_id", ""),
                "linked_task_id": r.get("linked_task_id", ""),
                "linked_apply_id": r.get("linked_apply_id", ""),
                "created_at": r.get("created_at", ""),
            })

        # Count results from events
        passed = sum(1 for e in events if e.get("event") == "test_run_completed"
                     and e.get("metadata", {}).get("status") == "passed")
        failed = sum(1 for e in events if e.get("event") in ("test_run_completed", "test_run_timed_out")
                     and e.get("metadata", {}).get("status") in ("failed", "timeout"))

        # Find failure artifact IDs
        artifact_ids = [
            e.get("metadata", {}).get("failure_artifact_id", "")
            for e in events
            if e.get("event") == "test_failure_artifact_created"
            and e.get("metadata", {}).get("failure_artifact_id")
        ]

        usage = load_usage(job)

        return {
            "version": 1,
            "run_count": len(safe_runs),
            "passed_count": passed,
            "failed_count": failed,
            "failure_artifact_ids": artifact_ids,
            "usage": export_usage_json(usage),
            "recent_runs": safe_runs,
        }
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"status": "section_unavailable", "reason": "test execution data not available"}


def _build_bundle_readme(job_id: str, sections: list[str]) -> str:
    """Generate bundle readme."""
    lines = [
        "# Remedy Review Bundle",
        "",
        f"Job: {job_id[:8]}",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Contents",
        "",
    ]
    for s in sections:
        lines.append(f"- {s}")
    lines.extend([
        "",
        "## Safety",
        "",
        "This bundle contains safe summaries only.",
        "No raw artifact bodies, diffs, source files, stdout/stderr, or secrets.",
        "No __pycache__, .pyc, .env, .data, node_modules, or .git content.",
        "",
        "## How to review",
        "",
        "1. Start with `manifest.json` for overview",
        "2. Check `job_summary.json` for task/artifact state",
        "3. Review `proof_chains.json` for change verification",
        "4. Check `trust_report.json` for audit trail",
        "5. Review `repair_summary.json` for failure/fix status",
        "6. Check `event_summary.json` for timeline",
    ])
    return "\n".join(lines)


def _build_config_summary() -> dict:
    from packages.orchestration.config import get_config
    return get_config().to_summary_dict()


def _build_self_repair_proposal_summary() -> dict:
    from packages.orchestration.self_repair_proposal import (
        self_repair_proposal_summary_for_bundle,
    )
    return self_repair_proposal_summary_for_bundle()


def _build_approval_policy_summary() -> dict:
    """Safe execution approval policy summary for the review bundle."""
    try:
        from packages.orchestration.execution_approval_policy import (
            execution_approval_policy_summary,
        )
        return execution_approval_policy_summary()
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return {"status": "section_unavailable", "reason": "approval policy not available"}


# ---------------------------------------------------------------------------
# Section registry — deterministic, ordered list of all bundle sections.
# Each spec maps a filename to its builder function and argument keys.
# Argument keys are resolved against a context dict at build time.
# ---------------------------------------------------------------------------

_REVIEW_BUNDLE_SECTION_SPECS: tuple[ReviewBundleSectionSpec, ...] = (
    ReviewBundleSectionSpec("job_summary.json", _build_job_summary, True, "Safe job summary", ("job",)),
    ReviewBundleSectionSpec("proof_chains.json", _build_proof_chains_safe, True, "Proof chains", ("job", "events")),
    ReviewBundleSectionSpec("event_summary.json", _build_event_summary, True, "Event counts", ("events",)),
    ReviewBundleSectionSpec("trust_report.json", _build_trust_report_safe, True, "Trust report", ("job", "events", "data_dir")),
    ReviewBundleSectionSpec("context_inspection.json", _build_context_inspection_safe, True, "Context inspection", ("job", "events")),
    ReviewBundleSectionSpec("changed_files_safe.json", _build_changed_files_safe, True, "Changed files", ("job", "events")),
    ReviewBundleSectionSpec("snapshot_summary.json", _build_snapshot_summary, True, "Snapshot summary", ("job_id", "data_dir")),
    ReviewBundleSectionSpec("continuation_summary.json", _build_continuation_summary, True, "Continuation summary", ("job_id", "data_dir", "events")),
    ReviewBundleSectionSpec("repair_summary.json", _build_repair_summary, True, "Repair summary", ("job", "events")),
    ReviewBundleSectionSpec("overnight_readiness_summary.json", _build_overnight_readiness_summary, True, "Overnight readiness", ("job", "data_dir")),
    ReviewBundleSectionSpec("overnight_run_summary.json", _build_overnight_run_summary, True, "Overnight run", ("job", "data_dir")),
    ReviewBundleSectionSpec("provider_trust_summary.json", _build_provider_trust_summary, True, "Provider trust", ("job",)),
    ReviewBundleSectionSpec("provider_material_summary.json", _build_provider_material_summary, True, "Provider material", ("job",)),
    ReviewBundleSectionSpec("provider_verification_summary.json", _build_provider_verification_summary, True, "Provider verification", ("job",)),
    ReviewBundleSectionSpec("repair_request_summary.json", _build_repair_request_summary, True, "Repair request", ("job",)),
    ReviewBundleSectionSpec("self_dogfood_summary.json", _build_self_dogfood_summary, True, "Self-dogfood", ("job",)),
    ReviewBundleSectionSpec("self_execution_summary.json", _build_self_execution_summary, True, "Self-execution", ("job",)),
    ReviewBundleSectionSpec("orchestrator_decision_summary.json", _build_orchestrator_decision_summary, True, "Orchestrator decisions", ("job",)),
    ReviewBundleSectionSpec("local_advisor_summary.json", _build_local_advisor_summary, True, "Local advisor", ("job",)),
    ReviewBundleSectionSpec("builder_routing_summary.json", _build_builder_routing_summary, True, "Builder routing", ("job",)),
    ReviewBundleSectionSpec("local_candidate_summary.json", _build_local_candidate_summary, True, "Local candidate", ("job",)),
    ReviewBundleSectionSpec("candidate_quality_summary.json", _build_candidate_quality_summary, True, "Candidate quality", ("job",)),
    ReviewBundleSectionSpec("external_builder_summary.json", _build_external_builder_summary, True, "External builder", ("job",)),
    ReviewBundleSectionSpec("worker_registry_summary.json", _build_worker_registry_summary, True, "Worker registry", ("job",)),
    ReviewBundleSectionSpec("token_economy_summary.json", _build_token_economy_summary, True, "Token economy", ("job",)),
    ReviewBundleSectionSpec("model_route_tournament_summary.json", _build_model_route_tournament_summary, True, "Model/route tournament", ("job",)),
    ReviewBundleSectionSpec("overnight_mission_summary.json", _build_overnight_mission_summary, True, "Overnight mission", ("job",)),
    ReviewBundleSectionSpec("snapshot_rollback_summary.json", _build_snapshot_rollback_summary, True, "Snapshot/rollback", ("job",)),
    ReviewBundleSectionSpec("repair_loop_summary.json", _build_repair_loop_summary, True, "Repair loop", ("job",)),
    ReviewBundleSectionSpec("main_builder_adapter_summary.json", _build_main_builder_adapter_summary, True, "Main builder adapter", ("job",)),
    ReviewBundleSectionSpec("managed_execution_summary.json", _build_managed_execution_summary, True, "Managed execution", ("job",)),
    ReviewBundleSectionSpec("dogfood_run_summary.json", _build_dogfood_run_summary, True, "Dogfood run", ("job",)),
    ReviewBundleSectionSpec("command_summary.json", _build_command_summary, True, "Command catalog", ("job",)),
    ReviewBundleSectionSpec("progress_ledger.json", _build_progress_ledger_safe, True, "Progress ledger", ("job", "events")),
    ReviewBundleSectionSpec("integrity_summary.json", _build_integrity_summary, True, "Integrity checks", ()),
    ReviewBundleSectionSpec("run_contract_summary.json", _build_contract_summary, True, "Run contract", ("job_id",)),
    ReviewBundleSectionSpec("test_execution_summary.json", _build_test_execution_summary, True, "Test execution", ("job", "events")),
    ReviewBundleSectionSpec("config_summary.json", _build_config_summary, True, "Config system state", ()),
    ReviewBundleSectionSpec("self_repair_proposal_summary.json", _build_self_repair_proposal_summary, True, "Self-repair proposal state", ()),
    ReviewBundleSectionSpec("execution_approval_policy_summary.json", _build_approval_policy_summary, True, "Execution approval policy", ()),
)


# ---------------------------------------------------------------------------
# Bundle builder (Step 978, refactored Steps 2296-2365)
# ---------------------------------------------------------------------------


def build_review_bundle(
    job_id: str,
    output_path: str | None = None,
) -> ReviewBundleResult:
    """Build safe review bundle zip for a job."""
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.storage import load_job
    from packages.orchestration.timeline import load_run_events

    result = ReviewBundleResult(
        job_id=job_id,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )

    data_dir = resolve_data_root()

    if output_path:
        if not _is_safe_output_path(output_path):
            result.error = "Unsafe output path — contains traversal or protected directory"
            return result
        out_path = Path(output_path)
    else:
        out_path = _default_output_path(job_id, data_dir)

    result.output_path = str(out_path)

    try:
        job = load_job(job_id)
    except Exception as exc:
        # Broad catch intentional: load_job raises JobNotFoundError/JobStoreError
        # but job_id string-to-UUID conversion can also fail with ValueError.
        result.error = f"Job {job_id[:8]} not found"
        logger.warning("Job load failed for bundle: %s", _safe_exception_message(exc))
        return result

    events = load_run_events(data_dir, UUID(job_id))

    builder_args = {
        "job": job,
        "events": events,
        "data_dir": data_dir,
        "job_id": job_id,
    }

    section_data: dict[str, bytes] = {}

    for spec in _REVIEW_BUNDLE_SECTION_SPECS:
        filename, content, section = _build_section_safe(spec, builder_args=builder_args)
        if content is not None:
            section_data[filename] = content
        result.sections.append(section)
        if section.status == "degraded":
            result.degraded_section_count += 1
            result.degraded_sections.append(filename)
            if section.structured_error is not None:
                result.section_error_summary.append(section.structured_error.to_dict())
            else:
                result.section_error_summary.append({
                    "section_name": filename,
                    "error_type": section.error_type,
                    "error_category": section.error_category,
                    "error_message": section.error_message,
                })

    # manifest.json
    included = [s.filename for s in result.sections if s.status == "included"]
    skipped = [s.filename for s in result.sections if s.status != "included"]
    manifest = ReviewBundleManifest(
        job_id=job_id,
        generated_at=result.generated_at,
        included_sections=included,
        skipped_sections=skipped,
        safety_warnings=result.safety.warnings,
    )
    manifest_content = json.dumps({
        "bundle_version": manifest.bundle_version,
        "job_id": manifest.job_id,
        "generated_at": manifest.generated_at,
        "included_sections": manifest.included_sections,
        "skipped_sections": manifest.skipped_sections,
        "safety_warnings": manifest.safety_warnings,
        "diagnostics_version": result.diagnostics_version,
        "degraded_section_count": result.degraded_section_count,
        "degraded_sections": result.degraded_sections,
        "section_error_summary": result.section_error_summary,
    }, indent=2).encode()
    section_data["manifest.json"] = manifest_content
    result.sections.insert(0, ReviewBundleSection("manifest.json", byte_count=len(manifest_content)))

    # bundle_readme.md
    readme = _build_bundle_readme(job_id, list(section_data.keys()))
    readme_content = readme.encode()
    section_data["bundle_readme.md"] = readme_content
    result.sections.append(ReviewBundleSection("bundle_readme.md", byte_count=len(readme_content)))

    # Write zip
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in sorted(section_data.items()):
            zf.writestr(name, data)

    result.file_count = len(section_data)
    result.byte_count = sum(len(d) for d in section_data.values())

    _audit_bundle_safety(result, section_data)

    return result


def _audit_bundle_safety(result: ReviewBundleResult, section_data: dict[str, bytes]) -> None:
    """Post-build safety audit — scans all sections for forbidden content."""
    from packages.orchestration.redaction_patterns import (
        _SECRET_RE,
    )

    _SAFE_MENTION_FILES = {"bundle_readme.md", "manifest.json"}

    for name, data in section_data.items():
        text = data.decode("utf-8", errors="replace")
        text_lower = text.lower()

        # Secret pattern detection
        if _SECRET_RE.search(text):
            result.safety.has_secrets = True
            result.safety.warnings.append(f"Secret-like pattern in {name}")

        # Traceback detection
        if "traceback (most recent" in text_lower and name not in _SAFE_MENTION_FILES:
            result.safety.has_raw_output = True
            result.safety.warnings.append(f"Traceback in {name}")

        # Raw output field names
        for field in ("command_output", "raw_stdout", "raw_stderr"):
            if f'"{field}"' in text_lower:
                result.safety.has_raw_output = True
                result.safety.warnings.append(f"Raw output field '{field}' in {name}")

        # __pycache__ / .pyc detection
        if name not in _SAFE_MENTION_FILES:
            if "__pycache__" in text or ".pyc" in text_lower:
                result.safety.has_pycache = True
                result.safety.warnings.append(f"Cache reference in {name}")

        # .env file reference detection (not category word "environment")
        if name not in _SAFE_MENTION_FILES:
            if '".env"' in text_lower or '".env.' in text_lower or "/.env" in text_lower:
                result.safety.has_env_files = True
                result.safety.warnings.append(f".env reference in {name}")

        # Raw diff markers
        if name not in _SAFE_MENTION_FILES:
            if "\n--- a/" in text or "\n+++ b/" in text:
                result.safety.has_raw_diffs = True
                result.safety.warnings.append(f"Raw diff markers in {name}")


# ---------------------------------------------------------------------------
# Export / summary
# ---------------------------------------------------------------------------


def export_review_bundle_json(result: ReviewBundleResult) -> dict[str, Any]:
    """Export bundle result as safe JSON dict."""
    section_dicts = []
    for s in result.sections:
        d: dict[str, Any] = {"filename": s.filename, "status": s.status, "byte_count": s.byte_count}
        if s.status == "degraded":
            d["error_type"] = s.error_type
            d["error_category"] = s.error_category
            d["error_message"] = s.error_message
        section_dicts.append(d)
    return {
        "job_id": result.job_id,
        "output_path": result.output_path,
        "bundle_version": result.bundle_version,
        "generated_at": result.generated_at,
        "file_count": result.file_count,
        "byte_count": result.byte_count,
        "diagnostics_version": result.diagnostics_version,
        "degraded_section_count": result.degraded_section_count,
        "degraded_sections": result.degraded_sections,
        "section_error_summary": result.section_error_summary,
        "sections": section_dicts,
        "safety": {
            "is_safe": result.safety.is_safe,
            "warnings": result.safety.warnings,
        },
        "error": result.error or None,
    }


def summarize_review_bundle(result: ReviewBundleResult) -> str:
    """Human-readable bundle summary."""
    if result.error:
        return f"Review Bundle: ERROR — {result.error}"

    lines = [
        f"Review Bundle: {result.job_id[:8]}",
        f"Output: {result.output_path}",
        f"Sections: {result.file_count}",
        f"Size: {result.byte_count} bytes",
        "",
    ]

    for s in result.sections:
        if s.status == "included":
            lines.append(f"  [+] {s.filename} ({s.byte_count}B)")
        else:
            lines.append(f"  [!] {s.filename} — {s.error_type or 'error'}: {s.error_message or s.error or 'unknown'}")

    if result.degraded_section_count > 0:
        lines.append(f"\nDegraded sections: {result.degraded_section_count}")
        for name in result.degraded_sections:
            lines.append(f"  - {name}")

    if result.safety.warnings:
        lines.append("\nWarnings:")
        for w in result.safety.warnings:
            lines.append(f"  - {w}")
    else:
        lines.append("\nSafety: PASS — no unsafe content detected")

    return "\n".join(lines)
