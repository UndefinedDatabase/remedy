"""
External Builder Sandbox v0 (Steps 1681-1716).

The first SAFE ingress for EXTERNAL builder work. Remedy can export a safe request package to an
external worker (another agent / a human) and ingest the worker's result — but that result stays
fully UNTRUSTED until it traverses the same quarantine → Trust Gate → Verification →
Materialization → human Approval → ``do continue`` path as a local candidate.

  Worker execute. Remedy governs.

Hard rules enforced here:
  - NO provider/model calls, NO network, NO browser, NO subprocess, NO shell, NO git/PR.
  - NO apply / approve / reject / test-run / automatic generation / automatic materialization
    outside the existing approval+intent gates.
  - External candidate output is ALWAYS untrusted: the raw bytes go straight into the existing
    private quarantine via ``intake_provider_repair`` (provider label ``external_builder:<src>``);
    this module never renders the raw candidate. Public surfaces carry safe IDs / counts / statuses.
  - Bounded, protected intake: candidate files are size-capped; symlink / path-traversal /
    protected-path / binary / unreadable inputs are rejected with safe structured errors.

Public API::

    create_external_builder_request_package(job_id, *, task_id="", route_id="", objective="",
        max_context_items=20, max_bytes=..., data_dir=None, new=False) -> ExternalBuilderRequestPackage
    submit_external_candidate(package_id, candidate_path, source_label, *, job_id="",
        data_dir=None, new=False) -> ExternalBuilderCandidateSubmission
    load_external_packages(job_id=None, data_dir=None) -> list[dict]
    get_external_package(package_id, data_dir=None) -> dict | None
    load_external_submissions(job_id=None, data_dir=None) -> list[dict]
    get_external_submission(submission_id, data_dir=None) -> dict | None
    external_builder_integrity(data_dir=None) -> dict
    export_external_package_json(pkg) / export_external_submission_json(sub) -> dict
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from packages.orchestration.provider_trust import _safe_path_label, _scrub_public

# ---------------------------------------------------------------------------
# Limits / constants
# ---------------------------------------------------------------------------

SCHEMA_VERSION = "external-builder-v0"
MAX_CANDIDATE_BYTES = 256 * 1024          # hard cap (aligns with provider intake)
DEFAULT_MAX_CONTEXT_ITEMS = 20
_PROVIDER_LABEL_PREFIX = "external_builder"
_EB_DIRNAME = "external_builder"
_PROTECTED_SUBSTRINGS = (".env", ".ssh", ".aws", ".git/", "/.data", "credentials", "id_rsa",
                         "secrets", "node_modules", "__pycache__")

_ALLOWED_OUTPUT_CONTRACT = (
    "Return EXACTLY ONE candidate as JSON or a single fenced unified diff. Repository-relative "
    "paths only. No secrets/tokens/.env values. No protected/generated/lock files. Do NOT claim "
    "the change was applied/tested/verified/merged. Output is UNTRUSTED: it will be quarantined, "
    "trust-checked, verified, and may be rejected; it is NEVER applied automatically."
)
_FORBIDDEN_CONTENT_POLICY = [
    "no_secrets", "no_absolute_paths", "no_raw_logs", "no_protected_paths",
    "no_apply_test_proof_claims", "single_candidate_only",
]


# ---------------------------------------------------------------------------
# Status vocabulary
# ---------------------------------------------------------------------------


class ExternalSubmissionState:
    QUARANTINED = "quarantined"
    TRUST_REJECTED = "trust_rejected"
    VERIFICATION_REJECTED = "verification_rejected"
    NEEDS_REVIEW = "needs_review"
    MATERIALIZATION_FAILED = "materialization_failed"
    PENDING_APPROVAL = "pending_approval"
    BLOCKED = "blocked"


class ExternalSubmissionStopReason:
    OK = "ok"
    PACKAGE_NOT_FOUND = "package_not_found"
    JOB_NOT_FOUND = "job_not_found"
    CONTRACT_DENIED = "contract_denied"
    FILE_NOT_FOUND = "candidate_file_not_found"
    NOT_REGULAR_FILE = "candidate_not_regular_file"
    SYMLINK_REJECTED = "candidate_symlink_rejected"
    PROTECTED_PATH = "candidate_protected_path"
    OVERSIZED = "candidate_oversized"
    UNREADABLE = "candidate_unreadable"


# ---------------------------------------------------------------------------
# Models (Step 1683) — no raw candidate/context in public fields.
# ---------------------------------------------------------------------------


@dataclass
class ExternalBuilderRequestPackage:
    package_id: str
    job_id: str = ""
    task_id: str = ""
    route_id: str = ""
    created_at: str = ""
    schema_version: str = SCHEMA_VERSION
    objective: str = ""
    safe_context_refs: list[dict[str, str]] = field(default_factory=list)
    allowed_output_contract: str = _ALLOWED_OUTPUT_CONTRACT
    forbidden_content_policy: list[str] = field(default_factory=lambda: list(_FORBIDDEN_CONTENT_POLICY))
    max_candidate_bytes: int = MAX_CANDIDATE_BYTES
    risk_profile: str = "untrusted_external"
    expected_response_schema: dict[str, Any] = field(default_factory=dict)
    evidence_refs: list[dict[str, str]] = field(default_factory=list)
    failure_artifact_id: str = ""
    content_sha256: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "package_id": self.package_id, "job_id": self.job_id, "task_id": self.task_id,
            "route_id": self.route_id, "created_at": self.created_at,
            "schema_version": self.schema_version, "objective": self.objective,
            "safe_context_refs": self.safe_context_refs,
            "allowed_output_contract": self.allowed_output_contract,
            "forbidden_content_policy": self.forbidden_content_policy,
            "max_candidate_bytes": self.max_candidate_bytes, "risk_profile": self.risk_profile,
            "expected_response_schema": self.expected_response_schema,
            "evidence_refs": self.evidence_refs, "failure_artifact_id": self.failure_artifact_id,
            "content_sha256": self.content_sha256,
        }


@dataclass
class ExternalBuilderCandidateSubmission:
    submission_id: str
    package_id: str = ""
    job_id: str = ""
    task_id: str = ""
    route_id: str = ""
    received_at: str = ""
    source_label: str = ""
    candidate_ref: str = ""              # opaque submission id; never raw
    metadata: dict[str, Any] = field(default_factory=dict)
    declared_capabilities: list[str] = field(default_factory=list)
    declared_files_touched: list[str] = field(default_factory=list)
    declared_tests: list[str] = field(default_factory=list)
    raw_storage_ref: str = ""            # private raw-storage hint (in-memory only; NEVER serialized
                                         # or exported — R-0091). Equals quarantine_id; use that
                                         # public field instead.
    public_summary: str = ""
    # Pipeline linkage (all safe IDs).
    quarantine_id: str = ""
    trust_report_id: str = ""
    verification_id: str = ""
    material_id: str = ""
    intent_id: str = ""
    trust_status: str = ""
    verification_decision: str = ""
    state: str = ExternalSubmissionState.QUARANTINED
    stop_reason: str = ExternalSubmissionStopReason.OK
    next_safe_action: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "submission_id": self.submission_id, "package_id": self.package_id,
            "job_id": self.job_id, "task_id": self.task_id, "route_id": self.route_id,
            "received_at": self.received_at, "source_label": self.source_label,
            "candidate_ref": self.candidate_ref, "metadata": self.metadata,
            "declared_capabilities": self.declared_capabilities,
            "declared_files_touched": [_safe_path_label(f) for f in self.declared_files_touched],
            "declared_tests": self.declared_tests,
            "public_summary": self.public_summary, "quarantine_id": self.quarantine_id,
            "trust_report_id": self.trust_report_id, "verification_id": self.verification_id,
            "material_id": self.material_id, "intent_id": self.intent_id,
            "trust_status": self.trust_status, "verification_decision": self.verification_decision,
            "state": self.state, "stop_reason": self.stop_reason,
            "next_safe_action": self.next_safe_action,
        }


def export_external_package_json(pkg: ExternalBuilderRequestPackage) -> dict[str, Any]:
    return pkg.to_dict()


def export_external_submission_json(sub: ExternalBuilderCandidateSubmission) -> dict[str, Any]:
    return sub.to_dict()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _scope(job_id: str) -> str:
    return f"job:{job_id}" if job_id else "repository"


def _sanitize_label(label: str) -> str:
    """A safe, bounded source/route label (no path/secret-ish chars)."""
    s = re.sub(r"[^A-Za-z0-9_.:-]", "-", (label or "").strip())[:48]
    return s or "external"


# ---------------------------------------------------------------------------
# Private storage (Step 1685)
# ---------------------------------------------------------------------------


def _eb_root(job_id: str, data_dir: Path) -> Path:
    base = job_id if job_id else "orchestrator"
    return data_dir / "workspaces" / base / _EB_DIRNAME


def _pkg_path(job_id: str, package_id: str, data_dir: Path) -> Path:
    return _eb_root(job_id, data_dir) / "packages" / package_id / "package.json"


def _sub_path(job_id: str, submission_id: str, data_dir: Path) -> Path:
    return _eb_root(job_id, data_dir) / "submissions" / submission_id / "submission.json"


def _atomic_write(path: Path, data: bytes, mode: int = 0o600) -> bool:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(path.parent, 0o700)
        except OSError:
            pass
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_bytes(data)
        try:
            os.chmod(tmp, mode)
        except OSError:
            pass
        os.replace(tmp, path)
        try:
            os.chmod(path, mode)
        except OSError:
            pass
        return True
    except OSError:
        return False


def _load_all(kind: str, job_id: str | None, data_dir: Path) -> list[dict]:
    """kind ∈ {'packages','submissions'}. Corruption-aware; never raises."""
    fname = "package.json" if kind == "packages" else "submission.json"
    roots: list[Path] = []
    ws = data_dir / "workspaces"
    if job_id:
        roots.append(_eb_root(job_id, data_dir) / kind)
    else:
        try:
            for child in ws.iterdir():
                roots.append(child / _EB_DIRNAME / kind)
        except OSError:
            pass
    out: list[dict] = []
    for root in roots:
        try:
            for child in sorted(root.iterdir()):
                f = child / fname
                if not f.is_file():
                    continue
                try:
                    out.append(json.loads(f.read_text(encoding="utf-8")))
                except (OSError, ValueError):
                    continue
        except OSError:
            continue
    out.sort(key=lambda r: r.get("created_at", r.get("received_at", "")))
    return out


def load_external_packages(job_id: str | None = None, data_dir: Path | None = None) -> list[dict]:
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    return _load_all("packages", job_id, ddir)


def load_external_submissions(job_id: str | None = None, data_dir: Path | None = None) -> list[dict]:
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    return _load_all("submissions", job_id, ddir)


def get_external_package(package_id: str, data_dir: Path | None = None) -> dict | None:
    return next((p for p in load_external_packages(data_dir=data_dir)
                 if p.get("package_id") == package_id), None)


def get_external_submission(submission_id: str, data_dir: Path | None = None) -> dict | None:
    return next((s for s in load_external_submissions(data_dir=data_dir)
                 if s.get("submission_id") == submission_id), None)


# ---------------------------------------------------------------------------
# Safe request package export (Step 1684)
# ---------------------------------------------------------------------------


def _gather_safe_context(job: Any, max_items: int) -> tuple[list[dict], str]:
    """Build SAFE context refs from a job: failure artifact ids + scrubbed safe_summary labels
    only. Never raw source/diff/logs/secrets/paths. Returns (refs, failure_artifact_id)."""
    refs: list[dict[str, str]] = []
    failure_id = ""
    for a in getattr(job, "artifacts", [])[: max_items * 3]:
        meta = getattr(a, "metadata", None) or {}
        if meta.get("test_failure"):
            label = _scrub_public(str(meta.get("safe_summary", "")))[:120]
            refs.append({"kind": "failure_artifact", "ref_id": str(a.id), "label": label})
            if not failure_id and not meta.get("failure_resolved"):
                failure_id = str(a.id)
        if len(refs) >= max_items:
            break
    return refs, failure_id


def _package_fingerprint(job_id: str, task_id: str, route_id: str, refs: list[dict]) -> str:
    parts = [job_id, task_id, route_id] + sorted(r.get("ref_id", "") for r in refs)
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:16]


def create_external_builder_request_package(
    job_id: str, *, task_id: str = "", route_id: str = "", objective: str = "",
    max_context_items: int = DEFAULT_MAX_CONTEXT_ITEMS, max_bytes: int = MAX_CANDIDATE_BYTES,
    data_dir: Path | None = None, new: bool = False,
) -> ExternalBuilderRequestPackage:
    """Export a SAFE request package for an external worker. Idempotent by
    (job, task, route, safe-evidence fingerprint) unless ``new``. Never leaks secrets / raw logs /
    private paths / unbounded context."""
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.storage import JobNotFoundError, load_job
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()

    try:
        job = load_job(UUID(job_id), ddir)
    except (ValueError, JobNotFoundError):
        # Return an empty, clearly-unbacked package record (job-not-found is surfaced by CLI).
        pkg = ExternalBuilderRequestPackage(package_id="", job_id=job_id, created_at=_now())
        return pkg

    refs, failure_id = _gather_safe_context(job, max(1, min(max_context_items, 100)))
    fp = _package_fingerprint(job_id, task_id, route_id, refs)
    if not new:
        existing = next((p for p in load_external_packages(job_id=job_id, data_dir=ddir)
                         if p.get("content_sha256") == fp), None)
        if existing is not None:
            return _pkg_from_dict(existing)

    pkg = ExternalBuilderRequestPackage(
        package_id=uuid4().hex[:16], job_id=job_id, task_id=task_id, route_id=route_id,
        created_at=_now(), objective=_scrub_public(objective or "Repair the linked failure safely.")[:300],
        safe_context_refs=refs, max_candidate_bytes=max(1024, min(max_bytes, MAX_CANDIDATE_BYTES)),
        expected_response_schema={
            "one_of": ["json_candidate", "single_unified_diff"],
            "json_candidate": {"summary": "str", "rationale": "str", "target_files": ["str"],
                               "unified_diff|structured_operations": "str|list"},
        },
        evidence_refs=list(refs), failure_artifact_id=failure_id, content_sha256=fp)
    _atomic_write(_pkg_path(job_id, pkg.package_id, ddir),
                  json.dumps(pkg.to_dict(), indent=2).encode("utf-8"))
    return pkg


def _pkg_from_dict(d: dict) -> ExternalBuilderRequestPackage:
    return ExternalBuilderRequestPackage(
        package_id=str(d.get("package_id", "")), job_id=str(d.get("job_id", "")),
        task_id=str(d.get("task_id", "")), route_id=str(d.get("route_id", "")),
        created_at=str(d.get("created_at", "")), schema_version=str(d.get("schema_version", SCHEMA_VERSION)),
        objective=str(d.get("objective", "")), safe_context_refs=list(d.get("safe_context_refs", [])),
        allowed_output_contract=str(d.get("allowed_output_contract", _ALLOWED_OUTPUT_CONTRACT)),
        forbidden_content_policy=list(d.get("forbidden_content_policy", _FORBIDDEN_CONTENT_POLICY)),
        max_candidate_bytes=int(d.get("max_candidate_bytes", MAX_CANDIDATE_BYTES)),
        risk_profile=str(d.get("risk_profile", "untrusted_external")),
        expected_response_schema=dict(d.get("expected_response_schema", {})),
        evidence_refs=list(d.get("evidence_refs", [])),
        failure_artifact_id=str(d.get("failure_artifact_id", "")),
        content_sha256=str(d.get("content_sha256", "")))


# ---------------------------------------------------------------------------
# Candidate submission intake (Steps 1687 / 1688)
# ---------------------------------------------------------------------------


def _validate_candidate_path(candidate_path: str, max_bytes: int) -> tuple[bool, str]:
    """Bounded + protected pre-checks BEFORE reading content. Returns (ok, stop_reason)."""
    raw = (candidate_path or "")
    low = raw.replace("\\", "/").lower()
    if ".." in low.split("/"):
        return False, ExternalSubmissionStopReason.PROTECTED_PATH
    if any(sub in low for sub in _PROTECTED_SUBSTRINGS):
        return False, ExternalSubmissionStopReason.PROTECTED_PATH
    p = Path(raw)
    try:
        if p.is_symlink():
            return False, ExternalSubmissionStopReason.SYMLINK_REJECTED
        if not p.exists():
            return False, ExternalSubmissionStopReason.FILE_NOT_FOUND
        if not p.is_file():
            return False, ExternalSubmissionStopReason.NOT_REGULAR_FILE
        if p.stat().st_size > max_bytes:
            return False, ExternalSubmissionStopReason.OVERSIZED
    except OSError:
        return False, ExternalSubmissionStopReason.UNREADABLE
    return True, ExternalSubmissionStopReason.OK


def _blocked_submission(job_id, package_id, source_label, stop_reason, summary,
                        data_dir: Path | None = None) -> ExternalBuilderCandidateSubmission:
    """Build a BLOCKED submission record. When the package + job are valid (data_dir given and
    job_id set) the blocked record is PERSISTED so the rejection stays in the safe history
    (R-0092); a missing/invalid package stays ephemeral (no raw candidate is ever stored here)."""
    sub = ExternalBuilderCandidateSubmission(
        submission_id=uuid4().hex[:16], package_id=package_id, job_id=job_id,
        source_label=_sanitize_label(source_label), received_at=_now(),
        state=ExternalSubmissionState.BLOCKED, stop_reason=stop_reason,
        public_summary=_scrub_public(summary)[:200],
        next_safe_action=(f"remedy external-builder package-show {package_id} --json"
                          if package_id else "remedy external-builder package-list --json"))
    sub.candidate_ref = sub.submission_id
    # Persist evidence-backed blocked submissions (package+job valid). No raw candidate is read or
    # stored for blocked cases. Missing/invalid package → ephemeral (not persisted).
    if data_dir is not None and job_id and package_id:
        _atomic_write(_sub_path(job_id, sub.submission_id, data_dir),
                      json.dumps(sub.to_dict(), indent=2).encode("utf-8"))
    return sub


def _state_from_intake(intake: Any) -> str:
    if getattr(intake, "repair_intent_id", ""):
        return ExternalSubmissionState.PENDING_APPROVAL
    trust = getattr(intake, "trust_status", "")
    vdec = getattr(intake, "verification_decision", "")
    if trust == "rejected":
        return ExternalSubmissionState.TRUST_REJECTED
    if vdec == "verification_rejected":
        return ExternalSubmissionState.VERIFICATION_REJECTED
    if vdec == "needs_human_review" or trust == "needs_human_review":
        return ExternalSubmissionState.NEEDS_REVIEW
    if getattr(intake, "material_state", "") == "materialization_failed":
        return ExternalSubmissionState.MATERIALIZATION_FAILED
    return ExternalSubmissionState.QUARANTINED


def submit_external_candidate(
    package_id: str, candidate_path: str, source_label: str, *,
    job_id: str = "", data_dir: Path | None = None, new: bool = False,
) -> ExternalBuilderCandidateSubmission:
    """Ingest an UNTRUSTED external candidate file: bounded/protected pre-checks → existing
    quarantine + Trust Gate + Verification + Materialization (via intake_provider_repair). Never
    applies/approves/tests; never renders the raw candidate. A submission is NOT an approved intent."""
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.run_contract import ContractAction, ensure_contract, evaluate_run_action
    from packages.orchestration.storage import JobNotFoundError, load_job
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    label = _sanitize_label(source_label)

    pkg_d = get_external_package(package_id, data_dir=ddir)
    if pkg_d is None:
        return _blocked_submission(job_id, package_id, label,
                                   ExternalSubmissionStopReason.PACKAGE_NOT_FOUND,
                                   "Request package not found.")
    pkg = _pkg_from_dict(pkg_d)
    job_id = job_id or pkg.job_id

    try:
        job = load_job(UUID(job_id), ddir)
    except (ValueError, JobNotFoundError):
        # Job missing → cannot scope a persisted record safely; stays ephemeral.
        return _blocked_submission(job_id, package_id, label,
                                   ExternalSubmissionStopReason.JOB_NOT_FOUND, "Job not found.")
    contract = ensure_contract(job)
    if not evaluate_run_action(contract, ContractAction.EXTERNAL_BUILDER_SUBMIT).allowed:
        return _blocked_submission(job_id, package_id, label,
                                   ExternalSubmissionStopReason.CONTRACT_DENIED,
                                   "Contract denies external builder submission.", data_dir=ddir)

    ok, sr = _validate_candidate_path(candidate_path, pkg.max_candidate_bytes)
    if not ok:
        # Evidence-backed: a rejected (oversized/protected/symlink/traversal/…) submission stays
        # in the safe history. No raw candidate is read for blocked cases.
        return _blocked_submission(job_id, package_id, label, sr,
                                   f"Candidate rejected: {sr}.", data_dir=ddir)

    # Untrusted ingress through the EXISTING pipeline. The raw file is read + quarantined by
    # intake_provider_repair; this module never reads the raw content itself.
    from packages.orchestration.provider_trust import (
        ProviderOutputIntakeRequest,
        SourceKind,
        intake_provider_repair,
    )
    intake = intake_provider_repair(
        ProviderOutputIntakeRequest(
            job_id=job_id, failure_artifact_id=pkg.failure_artifact_id,
            provider_name=f"{_PROVIDER_LABEL_PREFIX}:{label}", source_kind=SourceKind.FILE),
        input_path=candidate_path, data_dir=ddir)

    sub = ExternalBuilderCandidateSubmission(
        submission_id=uuid4().hex[:16], package_id=package_id, job_id=job_id,
        task_id=pkg.task_id, route_id=pkg.route_id, received_at=_now(), source_label=label,
        raw_storage_ref=getattr(intake, "quarantine_id", ""),
        quarantine_id=getattr(intake, "quarantine_id", ""),
        trust_report_id=getattr(intake, "trust_report_id", ""),
        verification_id=getattr(intake, "verification_id", ""),
        material_id=getattr(intake, "material_id", ""),
        intent_id=getattr(intake, "repair_intent_id", ""),
        trust_status=getattr(intake, "trust_status", ""),
        verification_decision=getattr(intake, "verification_decision", ""))
    sub.candidate_ref = sub.submission_id
    sub.state = _state_from_intake(intake)
    sub.public_summary = (f"External candidate ({label}): trust={sub.trust_status}, "
                          f"verification={sub.verification_decision}, "
                          f"intent={'yes' if sub.intent_id else 'no'} (untrusted; pending review).")
    sub.next_safe_action = _submission_next_action(sub)
    _atomic_write(_sub_path(job_id, sub.submission_id, ddir),
                  json.dumps(sub.to_dict(), indent=2).encode("utf-8"))
    return sub


def _submission_next_action(sub: ExternalBuilderCandidateSubmission) -> str:
    if sub.intent_id:
        return f"remedy patch approve {sub.job_id} {sub.intent_id} --json"
    if sub.verification_id:
        return f"remedy provider verification-show {sub.job_id} {sub.verification_id} --json"
    if sub.trust_report_id:
        return f"remedy provider trust-show {sub.job_id} {sub.trust_report_id} --json"
    return f"remedy external-builder package-show {sub.package_id} --json"


# ---------------------------------------------------------------------------
# Integrity (Step 1695)
# ---------------------------------------------------------------------------

_RAW_MARKERS = ("diff --git", "-----BEGIN", "Traceback (most recent call last)", "sk-")


def external_builder_integrity(data_dir: Path | None = None) -> dict[str, Any]:
    """Read-only invariant check over external packages + submissions. No mutation."""
    pkgs = load_external_packages(data_dir=data_dir)
    subs = load_external_submissions(data_dir=data_dir)
    pkg_ids = {p.get("package_id") for p in pkgs}
    violations: list[dict] = []
    for s in subs:
        if s.get("package_id") not in pkg_ids:
            violations.append({"submission_id": s.get("submission_id"), "code": "submission_without_package"})
        blob = json.dumps({k: v for k, v in s.items() if k != "raw_storage_ref"})
        if any(m in blob for m in _RAW_MARKERS):
            violations.append({"submission_id": s.get("submission_id"), "code": "raw_marker_in_public"})
        if "/home/" in blob or "/Users/" in blob:
            violations.append({"submission_id": s.get("submission_id"), "code": "absolute_path_in_public"})
    return {"version": 1, "package_count": len(pkgs), "submission_count": len(subs),
            "violation_count": len(violations), "passed": not violations, "violations": violations[:50]}
