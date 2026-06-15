"""
Provider Trust Verification v1 (Steps 1537-1572).

A SECOND-STAGE check on UNTRUSTED external candidate output, layered on top of the
Provider Trust Gate v0. The Trust Gate answers *is this candidate SAFE to ingest?*
This module answers *is this candidate PLAUSIBLE, RELEVANT, BOUNDED, and WORTHY of
becoming a pending repair intent?* — a candidate may be syntactically safe yet still
solve the wrong problem, touch irrelevant files, overclaim that it applied/tested/
fixed, ignore the request constraints, be too broad, repeat a failed idea, or be
inconsistent with the failure / self-improvement item it claims to address.

Hard rules enforced here (mirroring the Trust Gate):
  - NO provider/model execution, NO network, NO subprocess, NO shell, NO apply, NO
    approval, NO test execution, NO PR/git ops. Verification reads existing entities
    + the PRIVATE quarantine bytes only and emits a SAFE report.
  - Raw provider output / diffs / source / secrets / tracebacks / absolute private
    paths are NEVER exported. Public surfaces carry safe codes / counts / IDs only.
  - Verification NEVER approves, applies, tests, or creates PRs. A PASSED verification
    only marks a candidate *eligible* for materialization into a pending, approval-
    gated intent. Accepted ≠ verified ≠ approved ≠ applied.
  - Model/local-advisor output, if consulted, is critique ONLY and can never pass or
    reject a candidate by itself.

Public API::

    verify_provider_candidate(request, *, data_dir=None) -> ProviderVerificationReport
    run_inline_verification(job, report, candidate, raw_text, request, data_dir, *, request_package_id="")
    load_verification_reports(job) -> dict[str, dict]
    get_verification_report(job, verification_id) -> dict | None
    export_verification_report_json(report) -> dict
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from packages.orchestration.provider_trust import (
    Severity,
    _scrub_public,
    _safe_path_label,
    _is_docs_path,
    _is_test_path,
    scan_secrets,
    _read_quarantined_raw,
    parse_candidate,
    ProviderCandidateRepair,
)


# ---------------------------------------------------------------------------
# Limits
# ---------------------------------------------------------------------------

MAX_TARGET_FILES_VERIFY = 10            # candidate touching more is "too broad"
MAX_OPERATIONS_VERIFY = 20
MAX_LINES_VERIFY = 1500
MAX_GOALS = 1                           # v1 accepts exactly one goal/candidate
ENTROPY_MIN_LEN = 20                    # token length to consider for entropy
ENTROPY_THRESHOLD = 4.0                 # Shannon bits/char threshold
LOOP_REJECT_THRESHOLD = 1              # prior rejected verification for same hash → repeat
LOOP_FAILURE_THRESHOLD = 3            # verifications for same failure → loop risk


# ---------------------------------------------------------------------------
# Vocabularies (Steps 1538/1539/1547)
# ---------------------------------------------------------------------------


class VerificationDecision:
    PASSED = "verification_passed"
    NEEDS_HUMAN_REVIEW = "needs_human_review"
    REJECTED = "verification_rejected"
    INCOMPLETE = "verification_incomplete"


class VerificationStatus:
    VERIFIED = "verified"
    NEEDS_REVIEW = "needs_review"
    REJECTED = "rejected"
    INCOMPLETE = "incomplete"


class VerificationStopReason:
    OK = "ok"
    BLOCKER_OR_HIGH = "blocker_or_high_finding"
    MEDIUM_NEEDS_REVIEW = "medium_finding_needs_review"
    MISSING_TRUST_REPORT = "missing_trust_report"
    MISSING_CANDIDATE = "missing_candidate"
    CONTRACT_DENIED = "contract_denied"
    JOB_NOT_FOUND = "job_not_found"
    LOOP_GUARD = "loop_guard"


class LoopRisk:
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class VerificationImpact:
    ALLOW_MATERIALIZE = "allow_materialize"
    HUMAN_REVIEW = "needs_human_review"
    BLOCK = "block"
    INCOMPLETE = "incomplete"


class VerificationFindingCode:
    # Canonical taxonomy (Step 1539).
    CANDIDATE_NOT_LINKED_TO_FAILURE = "candidate_not_linked_to_failure"
    CANDIDATE_NOT_LINKED_TO_SELF_ITEM = "candidate_not_linked_to_self_item"
    TARGET_FILES_MISMATCH = "target_files_mismatch"
    PATCH_TARGETS_UNEXPECTED_FILE = "patch_targets_unexpected_file"
    CANDIDATE_OVERCLAIMS_APPLY = "candidate_overclaims_apply"
    CANDIDATE_OVERCLAIMS_TESTS = "candidate_overclaims_tests"
    CANDIDATE_OVERCLAIMS_VERIFICATION = "candidate_overclaims_verification"
    CANDIDATE_IGNORES_REQUEST_SCHEMA = "candidate_ignores_request_schema"
    CANDIDATE_MULTIPLE_GOALS = "candidate_multiple_goals"
    CANDIDATE_TOO_BROAD = "candidate_too_broad"
    CANDIDATE_LOW_SPECIFICITY = "candidate_low_specificity"
    CANDIDATE_NOT_TESTABLE = "candidate_not_testable"
    CANDIDATE_DOCS_ONLY_FOR_SOURCE_FAILURE = "candidate_docs_only_for_source_failure"
    CANDIDATE_SOURCE_CHANGE_FOR_DOCS_REQUEST = "candidate_source_change_for_docs_request"
    CANDIDATE_LOOP_RISK = "candidate_loop_risk"
    CANDIDATE_REPEATS_FAILED_ATTEMPT = "candidate_repeats_failed_attempt"
    CANDIDATE_MISSING_RATIONALE = "candidate_missing_rationale"
    CANDIDATE_RATIONALE_INCONSISTENT = "candidate_rationale_inconsistent"
    CANDIDATE_SAFE_BUT_NEEDS_HUMAN_REVIEW = "candidate_safe_but_needs_human_review"
    CANDIDATE_VERIFICATION_INCOMPLETE = "candidate_verification_incomplete"
    # Scanner codes (Step 1546) — secret/entropy material, never echoed.
    CANDIDATE_SECRET_MATERIAL = "candidate_secret_material"
    CANDIDATE_HIGH_ENTROPY_TOKEN = "candidate_high_entropy_token"
    CANDIDATE_CREDENTIAL_ASSIGNMENT = "candidate_credential_assignment"
    CANDIDATE_URL_CREDENTIALS = "candidate_url_credentials"
    CANDIDATE_ABSOLUTE_PATH = "candidate_absolute_path"
    CANDIDATE_TRACEBACK = "candidate_traceback"


CANONICAL_FINDING_CODES: frozenset[str] = frozenset(
    v for k, v in vars(VerificationFindingCode).items()
    if not k.startswith("_") and isinstance(v, str)
)


# ---------------------------------------------------------------------------
# Models (Step 1538) — NO raw output / diff / source fields anywhere.
# ---------------------------------------------------------------------------


@dataclass
class ProviderVerificationFinding:
    code: str
    severity: str
    summary: str
    target: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"code": self.code, "severity": self.severity,
                "summary": self.summary, "target": self.target}


@dataclass
class ProviderVerificationEvidenceRef:
    kind: str               # trust_report | quarantine | material | intent | failure_artifact | request_package | self_attempt | proposed_task
    ref_id: str
    label: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"kind": self.kind, "ref_id": self.ref_id, "label": self.label}


@dataclass
class ProviderVerificationScore:
    value: float = 0.0      # 0.0 (worst) .. 1.0 (best)
    band: str = "low"       # low | medium | high

    def to_dict(self) -> dict[str, Any]:
        return {"value": self.value, "band": self.band}


@dataclass
class ProviderVerificationImpact:
    impact: str = VerificationImpact.INCOMPLETE
    allowed_to_materialize: bool = False
    allowed_to_create_intent: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {"impact": self.impact,
                "allowed_to_materialize": self.allowed_to_materialize,
                "allowed_to_create_intent": self.allowed_to_create_intent}


@dataclass(frozen=True)
class ProviderVerificationRequest:
    job_id: str
    trust_report_id: str = ""
    quarantine_id: str = ""
    material_id: str = ""
    failure_artifact_id: str = ""
    self_attempt_id: str = ""
    proposed_task_id: str = ""
    request_package_id: str = ""
    candidate_hash: str = ""
    new: bool = False


@dataclass
class ProviderVerificationReport:
    verification_id: str
    job_id: str
    trust_report_id: str = ""
    quarantine_id: str = ""
    material_id: str = ""
    failure_artifact_id: str = ""
    self_attempt_id: str = ""
    proposed_task_id: str = ""
    request_package_id: str = ""
    candidate_hash: str = ""
    verification_status: str = VerificationStatus.INCOMPLETE
    decision: str = VerificationDecision.INCOMPLETE
    stop_reason: str = VerificationStopReason.MISSING_TRUST_REPORT
    score: ProviderVerificationScore = field(default_factory=ProviderVerificationScore)
    impact: ProviderVerificationImpact = field(default_factory=ProviderVerificationImpact)
    loop_risk: str = LoopRisk.NONE
    findings: list[ProviderVerificationFinding] = field(default_factory=list)
    evidence_refs: list[ProviderVerificationEvidenceRef] = field(default_factory=list)
    allowed_to_materialize: bool = False
    allowed_to_create_intent: bool = False
    advisor_critique: dict[str, Any] | None = None
    next_safe_action: str = ""
    safe_summary: str = ""
    created_at: str = ""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _finding(code: str, severity: str, summary: str, target: str = "") -> ProviderVerificationFinding:
    return ProviderVerificationFinding(code=code, severity=severity,
                                       summary=_scrub_public(summary)[:200], target=target)


def _dedupe(findings: list[ProviderVerificationFinding]) -> list[ProviderVerificationFinding]:
    seen: set[tuple[str, str]] = set()
    out: list[ProviderVerificationFinding] = []
    for f in findings:
        key = (f.code, f.target)
        if key in seen:
            continue
        seen.add(key)
        out.append(f)
    return out


# ---------------------------------------------------------------------------
# Step 1540 — request / candidate consistency
# ---------------------------------------------------------------------------


def check_request_consistency(
    candidate: ProviderCandidateRepair, request_package: dict | None,
) -> list[ProviderVerificationFinding]:
    """Verify the candidate against the original request package, when available.

    A missing request package is NOT a crash and NOT a hard failure — it surfaces a
    low 'safe but needs review' note (verification can still proceed on other signals)."""
    out: list[ProviderVerificationFinding] = []
    if not request_package:
        out.append(_finding(VerificationFindingCode.CANDIDATE_SAFE_BUT_NEEDS_HUMAN_REVIEW,
                            Severity.LOW, "No request package linked; consistency unverifiable."))
        return out

    # Exactly one candidate / one goal.
    if candidate.patch_block_count > MAX_GOALS:
        out.append(_finding(VerificationFindingCode.CANDIDATE_MULTIPLE_GOALS, Severity.HIGH,
                            f"Candidate carries {candidate.patch_block_count} patch blocks; expected exactly one."))

    # Response format followed: a request package expecting a patch should get a patch.
    target_kind = str(request_package.get("target_kind", "") or "")
    if target_kind in ("source", "docs", "external") and not candidate.has_patch:
        out.append(_finding(VerificationFindingCode.CANDIDATE_IGNORES_REQUEST_SCHEMA, Severity.MEDIUM,
                            "Request expected a patch candidate; none was produced."))

    # docs request vs source change and vice-versa.
    if candidate.has_patch and candidate.target_files:
        docs_only = all(_is_docs_path(f) for f in candidate.target_files)
        source_like = any(not _is_docs_path(f) and not _is_test_path(f) for f in candidate.target_files)
        if target_kind == "docs" and source_like:
            out.append(_finding(VerificationFindingCode.CANDIDATE_SOURCE_CHANGE_FOR_DOCS_REQUEST,
                                Severity.HIGH, "Docs-scoped request but candidate changes source files."))
        if target_kind == "source" and docs_only:
            out.append(_finding(VerificationFindingCode.CANDIDATE_DOCS_ONLY_FOR_SOURCE_FAILURE,
                                Severity.MEDIUM, "Source-scoped request but candidate is docs-only."))

    # Target-file justification: candidate targets should overlap the package's named files.
    pkg_files = _request_package_files(request_package)
    if pkg_files and candidate.target_files:
        pkg_base = {_safe_path_label(f) for f in pkg_files}
        cand_base = {_safe_path_label(f) for f in candidate.target_files}
        if not (pkg_base & cand_base):
            out.append(_finding(VerificationFindingCode.TARGET_FILES_MISMATCH, Severity.MEDIUM,
                                "Candidate targets do not overlap the request package's named files."))
    return out


def _request_package_files(request_package: dict) -> list[str]:
    files: list[str] = []
    for sec in request_package.get("sections", []) or []:
        if not isinstance(sec, dict):
            continue
        for f in sec.get("files", []) or sec.get("target_files", []) or []:
            if isinstance(f, str) and f:
                files.append(f)
    return files[:MAX_TARGET_FILES_VERIFY + 5]


# ---------------------------------------------------------------------------
# Step 1541 — failure / self context relevance
# ---------------------------------------------------------------------------


def check_failure_relevance(
    job: Any, candidate: ProviderCandidateRepair, failure_artifact_id: str,
) -> list[ProviderVerificationFinding]:
    out: list[ProviderVerificationFinding] = []
    if not failure_artifact_id:
        out.append(_finding(VerificationFindingCode.CANDIDATE_NOT_LINKED_TO_FAILURE, Severity.MEDIUM,
                            "Candidate is not linked to a failure artifact."))
        return out
    fa = next((a for a in getattr(job, "artifacts", []) if str(a.id) == failure_artifact_id), None)
    if fa is None:
        out.append(_finding(VerificationFindingCode.CANDIDATE_NOT_LINKED_TO_FAILURE, Severity.HIGH,
                            "Referenced failure artifact does not exist."))
        return out
    meta = getattr(fa, "metadata", None) or {}
    related = [str(f) for f in (meta.get("related_files") or []) if isinstance(f, str)]
    if related and candidate.target_files:
        rel_base = {_safe_path_label(f) for f in related}
        cand_base = {_safe_path_label(f) for f in candidate.target_files}
        if not (rel_base & cand_base):
            out.append(_finding(VerificationFindingCode.TARGET_FILES_MISMATCH, Severity.MEDIUM,
                                "Candidate targets do not overlap the failure's known related files."))
    # Type match: a docs-only candidate answering a failure whose own related files are
    # source code is a MEDIUM mismatch; if the failure's related files are themselves docs
    # the docs candidate is consistent and only surfaced (LOW).
    if candidate.has_patch and candidate.target_files and meta.get("test_failure") \
            and all(_is_docs_path(f) for f in candidate.target_files):
        failure_has_source = any(
            not _is_docs_path(f) and not _is_test_path(f) for f in related)
        sev = Severity.MEDIUM if (failure_has_source or not related) else Severity.LOW
        out.append(_finding(VerificationFindingCode.CANDIDATE_DOCS_ONLY_FOR_SOURCE_FAILURE,
                            sev, "Docs-only candidate for a test failure."))
    return out


def check_self_relevance(
    job: Any, candidate: ProviderCandidateRepair, self_attempt_id: str, proposed_task_id: str,
) -> list[ProviderVerificationFinding]:
    out: list[ProviderVerificationFinding] = []
    if not self_attempt_id and not proposed_task_id:
        out.append(_finding(VerificationFindingCode.CANDIDATE_NOT_LINKED_TO_SELF_ITEM, Severity.MEDIUM,
                            "Self-improvement candidate is not linked to an attempt / proposed task."))
        return out
    # Resolve the proposed task if present and check overlap with its target hint.
    pt = None
    if proposed_task_id:
        for t in getattr(job, "tasks", []) or []:
            if str(getattr(t, "id", "")) == proposed_task_id:
                pt = t
                break
    if proposed_task_id and pt is None:
        out.append(_finding(VerificationFindingCode.CANDIDATE_NOT_LINKED_TO_SELF_ITEM, Severity.HIGH,
                            "Referenced proposed task does not exist."))
    return out


# ---------------------------------------------------------------------------
# Step 1542 — overclaim detector (never echoes raw text)
# ---------------------------------------------------------------------------

_APPLY_CLAIM_RE = re.compile(
    r"\b(applied|i\s+applied|has\s+been\s+applied|merged|deployed|committed|pushed)\b", re.IGNORECASE)
_TEST_CLAIM_RE = re.compile(
    r"\b(tests?\s+pass(ed|ing)?|all\s+tests?\s+pass|test\s+suite\s+pass|ran\s+the\s+tests?)\b",
    re.IGNORECASE)
_VERIFY_CLAIM_RE = re.compile(
    r"\b(verified|confirmed\s+fixed|fix\s+is\s+confirmed|proven|validated\s+the\s+fix|"
    r"successfully\s+fixed|bug\s+is\s+fixed|issue\s+is\s+resolved)\b", re.IGNORECASE)
# Note: "intended to fix" / "should fix" / "will fix" are allowed framing — the claim
# patterns above intentionally do NOT match them, so no whitelist pass is needed.


def check_overclaims(claim_text: str) -> list[ProviderVerificationFinding]:
    """Detect execution/result claims in candidate prose. Reports codes only — never
    echoes the matched text."""
    out: list[ProviderVerificationFinding] = []
    text = claim_text or ""
    if _APPLY_CLAIM_RE.search(text):
        out.append(_finding(VerificationFindingCode.CANDIDATE_OVERCLAIMS_APPLY, Severity.MEDIUM,
                            "Candidate claims it was applied/merged/deployed."))
    if _TEST_CLAIM_RE.search(text):
        out.append(_finding(VerificationFindingCode.CANDIDATE_OVERCLAIMS_TESTS, Severity.MEDIUM,
                            "Candidate claims tests passed."))
    if _VERIFY_CLAIM_RE.search(text):
        out.append(_finding(VerificationFindingCode.CANDIDATE_OVERCLAIMS_VERIFICATION, Severity.MEDIUM,
                            "Candidate claims the fix is verified/confirmed."))
    return out


# ---------------------------------------------------------------------------
# Step 1543 — patch minimality / scope (safe metadata only)
# ---------------------------------------------------------------------------


def check_minimality(candidate: ProviderCandidateRepair) -> list[ProviderVerificationFinding]:
    out: list[ProviderVerificationFinding] = []
    if not candidate.has_patch:
        return out
    n_files = len(candidate.target_files)
    if n_files > MAX_TARGET_FILES_VERIFY:
        out.append(_finding(VerificationFindingCode.CANDIDATE_TOO_BROAD, Severity.HIGH,
                            f"Candidate touches {n_files} files (> {MAX_TARGET_FILES_VERIFY})."))
    if candidate.line_count > MAX_LINES_VERIFY:
        out.append(_finding(VerificationFindingCode.CANDIDATE_TOO_BROAD, Severity.MEDIUM,
                            f"Candidate spans {candidate.line_count} lines (> {MAX_LINES_VERIFY})."))
    # Generated / lock / cache targets are unexpected for a repair candidate.
    for f in candidate.target_files:
        low = (f or "").lower()
        if low.endswith(".lock") or "lock" in low.rsplit("/", 1)[-1] or "__pycache__" in low \
                or low.endswith((".min.js", ".map")):
            out.append(_finding(VerificationFindingCode.PATCH_TARGETS_UNEXPECTED_FILE, Severity.HIGH,
                                "Candidate targets a generated/lock/cache file.",
                                target=_safe_path_label(f)))
    return out


# ---------------------------------------------------------------------------
# Step 1544 — testability (no execution)
# ---------------------------------------------------------------------------


def check_testability(
    job: Any, candidate: ProviderCandidateRepair, failure_artifact_id: str,
) -> list[ProviderVerificationFinding]:
    out: list[ProviderVerificationFinding] = []
    if not candidate.has_patch:
        return out
    docs_only = bool(candidate.target_files) and all(_is_docs_path(f) for f in candidate.target_files)
    has_test_link = False
    if failure_artifact_id:
        fa = next((a for a in getattr(job, "artifacts", []) if str(a.id) == failure_artifact_id), None)
        meta = (getattr(fa, "metadata", None) or {}) if fa is not None else {}
        if meta.get("test_command") or meta.get("test_run_id") or meta.get("test_failure"):
            has_test_link = True
    if not has_test_link:
        sev = Severity.LOW if docs_only else Severity.MEDIUM
        out.append(_finding(VerificationFindingCode.CANDIDATE_NOT_TESTABLE, sev,
                            "No linked test evidence to verify this candidate after apply."))
    return out


# ---------------------------------------------------------------------------
# Step 1545 — loop risk (durable summaries; no execution)
# ---------------------------------------------------------------------------


def check_loop_risk(
    job: Any, candidate_hash: str, failure_artifact_id: str,
) -> tuple[list[ProviderVerificationFinding], str]:
    """Return (findings, loop_risk) from durable verification history in job metadata."""
    out: list[ProviderVerificationFinding] = []
    reports = load_verification_reports(job)
    same_hash_rejected = 0
    same_failure = 0
    for rep in reports.values():
        if candidate_hash and rep.get("candidate_hash") == candidate_hash \
                and rep.get("decision") == VerificationDecision.REJECTED:
            same_hash_rejected += 1
        if failure_artifact_id and rep.get("failure_artifact_id") == failure_artifact_id:
            same_failure += 1
    risk = LoopRisk.NONE
    if same_hash_rejected >= LOOP_REJECT_THRESHOLD:
        out.append(_finding(VerificationFindingCode.CANDIDATE_REPEATS_FAILED_ATTEMPT, Severity.HIGH,
                            "An identical candidate was already rejected by verification."))
        risk = LoopRisk.HIGH
    elif same_failure >= LOOP_FAILURE_THRESHOLD:
        out.append(_finding(VerificationFindingCode.CANDIDATE_LOOP_RISK, Severity.MEDIUM,
                            f"{same_failure} verifications already exist for this failure."))
        risk = LoopRisk.MEDIUM
    elif same_failure >= 1:
        risk = LoopRisk.LOW
    return out, risk


# ---------------------------------------------------------------------------
# Step 1546 — enhanced secret / entropy heuristic (no raw value echo)
# ---------------------------------------------------------------------------

_CRED_ASSIGN_RE = re.compile(
    r"(?i)\b(api[_-]?key|secret|token|password|passwd|pwd|access[_-]?key)\b\s*[:=]\s*\S{6,}")
_URL_CRED_RE = re.compile(r"[a-z][a-z0-9+.\-]*://[^\s/@:]+:[^\s/@]+@")
_PRIVATE_KEY_RE = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")
_DOTENV_RE = re.compile(r"(?m)^[A-Z][A-Z0-9_]{2,}=\S{8,}$")
_TOKEN_RE = re.compile(r"[A-Za-z0-9_\-+/=]{%d,}" % ENTROPY_MIN_LEN)


def _shannon_entropy(s: str) -> float:
    if not s:
        return 0.0
    counts: dict[str, int] = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    n = len(s)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())


def scan_candidate_secrets(raw_text: str) -> list[ProviderVerificationFinding]:
    """Scan the PRIVATE raw candidate for secret / high-entropy / credential material.
    Runs on private bytes; emits SAFE codes/counts only — never echoes a value."""
    out: list[ProviderVerificationFinding] = []
    text = raw_text or ""
    # Reuse the trust-gate base scanner (private-key headers, AKIA/sk-/ghp_, bearer,
    # api-key assignment, abs path, traceback) and re-map to verification codes.
    for tf in scan_secrets(text):
        if tf.code == "raw_secret_detected":
            out.append(_finding(VerificationFindingCode.CANDIDATE_SECRET_MATERIAL, Severity.BLOCKER,
                                "Secret-like material detected in candidate."))
        elif tf.code == "absolute_path":
            out.append(_finding(VerificationFindingCode.CANDIDATE_ABSOLUTE_PATH, Severity.HIGH,
                                "Absolute filesystem path detected in candidate."))
        else:
            out.append(_finding(VerificationFindingCode.CANDIDATE_TRACEBACK, Severity.MEDIUM,
                                "Stack-trace-like block detected in candidate."))
    if _PRIVATE_KEY_RE.search(text):
        out.append(_finding(VerificationFindingCode.CANDIDATE_SECRET_MATERIAL, Severity.BLOCKER,
                            "Private-key header detected in candidate."))
    if _CRED_ASSIGN_RE.search(text) or _DOTENV_RE.search(text):
        out.append(_finding(VerificationFindingCode.CANDIDATE_CREDENTIAL_ASSIGNMENT, Severity.HIGH,
                            "Credential-style assignment / .env-like value detected."))
    if _URL_CRED_RE.search(text):
        out.append(_finding(VerificationFindingCode.CANDIDATE_URL_CREDENTIALS, Severity.HIGH,
                            "URL with embedded credentials detected."))
    # High-entropy token-like strings (novel secret formats).
    for tok in _TOKEN_RE.findall(text):
        if _shannon_entropy(tok) >= ENTROPY_THRESHOLD:
            out.append(_finding(VerificationFindingCode.CANDIDATE_HIGH_ENTROPY_TOKEN, Severity.HIGH,
                                "High-entropy token-like string detected (possible secret)."))
            break
    return _dedupe(out)


# ---------------------------------------------------------------------------
# Step 1547 — decision rules + score/impact
# ---------------------------------------------------------------------------

_SEVERITY_WEIGHT = {Severity.BLOCKER: 1.0, Severity.HIGH: 0.5,
                    Severity.MEDIUM: 0.2, Severity.LOW: 0.05}


def score_findings(findings: list[ProviderVerificationFinding]) -> ProviderVerificationScore:
    penalty = sum(_SEVERITY_WEIGHT.get(f.severity, 0.0) for f in findings)
    value = round(max(0.0, min(1.0, 1.0 - penalty)), 2)
    band = "high" if value >= 0.75 else ("medium" if value >= 0.45 else "low")
    return ProviderVerificationScore(value=value, band=band)


def decide_verification(
    findings: list[ProviderVerificationFinding], *, candidate_present: bool,
) -> tuple[str, str, str]:
    """Return (decision, verification_status, stop_reason)."""
    if not candidate_present:
        return (VerificationDecision.INCOMPLETE, VerificationStatus.INCOMPLETE,
                VerificationStopReason.MISSING_CANDIDATE)
    has_blocker = any(f.severity == Severity.BLOCKER for f in findings)
    has_high = any(f.severity == Severity.HIGH for f in findings)
    has_medium = any(f.severity == Severity.MEDIUM for f in findings)
    if has_blocker or has_high:
        return (VerificationDecision.REJECTED, VerificationStatus.REJECTED,
                VerificationStopReason.BLOCKER_OR_HIGH)
    if has_medium:
        return (VerificationDecision.NEEDS_HUMAN_REVIEW, VerificationStatus.NEEDS_REVIEW,
                VerificationStopReason.MEDIUM_NEEDS_REVIEW)
    return (VerificationDecision.PASSED, VerificationStatus.VERIFIED, VerificationStopReason.OK)


def _impact_for(decision: str) -> ProviderVerificationImpact:
    if decision == VerificationDecision.PASSED:
        return ProviderVerificationImpact(VerificationImpact.ALLOW_MATERIALIZE, True, True)
    if decision == VerificationDecision.NEEDS_HUMAN_REVIEW:
        return ProviderVerificationImpact(VerificationImpact.HUMAN_REVIEW, False, False)
    if decision == VerificationDecision.REJECTED:
        return ProviderVerificationImpact(VerificationImpact.BLOCK, False, False)
    return ProviderVerificationImpact(VerificationImpact.INCOMPLETE, False, False)


# ---------------------------------------------------------------------------
# Persistence (Step 1549) — safe report; raw stays in quarantine only
# ---------------------------------------------------------------------------

_VERIFY_META_KEY = "provider_verifications_v1"


def _verification_root(job_id: str, data_dir: Path) -> Path:
    return data_dir / "workspaces" / job_id / "provider_verification"


def _verification_dir(job_id: str, verification_id: str, data_dir: Path) -> Path:
    return _verification_root(job_id, data_dir) / verification_id


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


def export_verification_report_json(report: ProviderVerificationReport) -> dict[str, Any]:
    return {
        "version": 1,
        "verification_id": report.verification_id,
        "job_id": report.job_id,
        "trust_report_id": report.trust_report_id,
        "quarantine_id": report.quarantine_id,
        "material_id": report.material_id,
        "failure_artifact_id": report.failure_artifact_id,
        "self_attempt_id": report.self_attempt_id,
        "proposed_task_id": report.proposed_task_id,
        "request_package_id": report.request_package_id,
        "candidate_hash": report.candidate_hash,
        "verification_status": report.verification_status,
        "decision": report.decision,
        "stop_reason": report.stop_reason,
        "score": report.score.to_dict(),
        "impact": report.impact.to_dict(),
        "loop_risk": report.loop_risk,
        "findings": [f.to_dict() for f in report.findings],
        "evidence_refs": [e.to_dict() for e in report.evidence_refs],
        "allowed_to_materialize": report.allowed_to_materialize,
        "allowed_to_create_intent": report.allowed_to_create_intent,
        "advisor_critique": report.advisor_critique,
        "next_safe_action": report.next_safe_action,
        "safe_summary": report.safe_summary,
        "created_at": report.created_at,
    }


def save_verification_report(job: Any, report: ProviderVerificationReport,
                             data_dir: Path | None = None) -> None:
    """Persist a SAFE verification report to job metadata + a private report.json.
    Caller persists the job."""
    safe = export_verification_report_json(report)
    store = job.metadata.setdefault(_VERIFY_META_KEY, {})
    store[report.verification_id] = safe
    if data_dir is not None:
        path = _verification_dir(report.job_id, report.verification_id, data_dir) / "report.json"
        _atomic_write(path, json.dumps(safe, indent=2).encode("utf-8"))


def load_verification_reports(job: Any) -> dict[str, dict]:
    return dict((getattr(job, "metadata", None) or {}).get(_VERIFY_META_KEY, {}))


def get_verification_report(job: Any, verification_id: str) -> dict | None:
    return load_verification_reports(job).get(verification_id)


def _find_existing_report(
    job: Any, *, trust_report_id: str, candidate_hash: str,
    request_package_id: str, self_attempt_id: str,
) -> dict | None:
    """Idempotency by (trust_report_id, candidate_hash, request_package_id/self_attempt_id)."""
    for rep in load_verification_reports(job).values():
        if rep.get("trust_report_id") == trust_report_id \
                and rep.get("candidate_hash") == candidate_hash \
                and rep.get("request_package_id", "") == request_package_id \
                and rep.get("self_attempt_id", "") == self_attempt_id:
            return rep
    return None


# ---------------------------------------------------------------------------
# Core verification engine
# ---------------------------------------------------------------------------


def _next_action(job_id: str, decision: str, intent_id: str, verification_id: str) -> str:
    if decision == VerificationDecision.PASSED:
        if intent_id:
            return f"remedy patch approve {job_id} {intent_id} --json"
        return f"remedy provider verification-show {job_id} {verification_id} --json"
    if decision == VerificationDecision.REJECTED:
        return f"remedy repair request {job_id} --json"
    # needs_review / incomplete
    return f"remedy provider verification-show {job_id} {verification_id} --json"


def _run_checks(
    job: Any, candidate: ProviderCandidateRepair, raw_text: str, *,
    failure_artifact_id: str, self_attempt_id: str, proposed_task_id: str,
    request_package: dict | None, candidate_hash: str,
) -> tuple[list[ProviderVerificationFinding], str]:
    findings: list[ProviderVerificationFinding] = []
    findings += check_request_consistency(candidate, request_package)
    if self_attempt_id or proposed_task_id:
        findings += check_self_relevance(job, candidate, self_attempt_id, proposed_task_id)
    else:
        findings += check_failure_relevance(job, candidate, failure_artifact_id)
    claim_text = " ".join([candidate.summary or "", candidate.rationale or "",
                           candidate.risk_notes or ""])
    findings += check_overclaims(claim_text)
    findings += check_minimality(candidate)
    findings += check_testability(job, candidate, failure_artifact_id)
    if not (candidate.rationale or "").strip():
        findings.append(_finding(VerificationFindingCode.CANDIDATE_MISSING_RATIONALE, Severity.LOW,
                                 "Candidate provides no rationale."))
    findings += scan_candidate_secrets(raw_text)
    loop_findings, loop_risk = check_loop_risk(job, candidate_hash, failure_artifact_id)
    findings += loop_findings
    return _dedupe(findings), loop_risk


def _build_report(
    job: Any, *, verification_id: str, request: ProviderVerificationRequest,
    candidate: ProviderCandidateRepair | None, raw_text: str, candidate_hash: str,
    request_package: dict | None, intent_id: str, data_dir: Path | None,
    persist: bool,
) -> ProviderVerificationReport:
    report = ProviderVerificationReport(
        verification_id=verification_id, job_id=request.job_id,
        trust_report_id=request.trust_report_id, quarantine_id=request.quarantine_id,
        material_id=request.material_id, failure_artifact_id=request.failure_artifact_id,
        self_attempt_id=request.self_attempt_id, proposed_task_id=request.proposed_task_id,
        request_package_id=request.request_package_id, candidate_hash=candidate_hash,
        created_at=_now(),
    )
    refs: list[ProviderVerificationEvidenceRef] = []
    if request.trust_report_id:
        refs.append(ProviderVerificationEvidenceRef("trust_report", request.trust_report_id))
    if request.quarantine_id:
        refs.append(ProviderVerificationEvidenceRef("quarantine", request.quarantine_id))
    if request.material_id:
        refs.append(ProviderVerificationEvidenceRef("material", request.material_id))
    if request.failure_artifact_id:
        refs.append(ProviderVerificationEvidenceRef("failure_artifact", request.failure_artifact_id))
    if request.request_package_id:
        refs.append(ProviderVerificationEvidenceRef("request_package", request.request_package_id))
    if request.self_attempt_id:
        refs.append(ProviderVerificationEvidenceRef("self_attempt", request.self_attempt_id))
    if request.proposed_task_id:
        refs.append(ProviderVerificationEvidenceRef("proposed_task", request.proposed_task_id))
    if intent_id:
        refs.append(ProviderVerificationEvidenceRef("intent", intent_id))
    report.evidence_refs = refs

    if candidate is None:
        report.decision = VerificationDecision.INCOMPLETE
        report.verification_status = VerificationStatus.INCOMPLETE
        report.stop_reason = VerificationStopReason.MISSING_CANDIDATE
        report.findings = [_finding(VerificationFindingCode.CANDIDATE_VERIFICATION_INCOMPLETE,
                                    Severity.MEDIUM, "No candidate available to verify.")]
        report.impact = _impact_for(VerificationDecision.INCOMPLETE)
        report.next_safe_action = _next_action(request.job_id, report.decision, "", verification_id)
        report.safe_summary = "Verification incomplete: no candidate."
        if persist:
            save_verification_report(job, report, data_dir)
        return report

    findings, loop_risk = _run_checks(
        job, candidate, raw_text, failure_artifact_id=request.failure_artifact_id,
        self_attempt_id=request.self_attempt_id, proposed_task_id=request.proposed_task_id,
        request_package=request_package, candidate_hash=candidate_hash)
    decision, status, stop_reason = decide_verification(findings, candidate_present=True)
    report.findings = findings
    report.loop_risk = loop_risk
    report.score = score_findings(findings)
    report.decision = decision
    report.verification_status = status
    report.stop_reason = stop_reason
    report.impact = _impact_for(decision)
    report.allowed_to_materialize = report.impact.allowed_to_materialize
    report.allowed_to_create_intent = report.impact.allowed_to_create_intent
    # Loop guard: a high loop risk forces human review even on otherwise-low findings.
    if loop_risk == LoopRisk.HIGH and decision == VerificationDecision.PASSED:
        report.decision = VerificationDecision.NEEDS_HUMAN_REVIEW
        report.verification_status = VerificationStatus.NEEDS_REVIEW
        report.stop_reason = VerificationStopReason.LOOP_GUARD
        report.impact = _impact_for(VerificationDecision.NEEDS_HUMAN_REVIEW)
        report.allowed_to_materialize = False
        report.allowed_to_create_intent = False
    report.next_safe_action = _next_action(request.job_id, report.decision, intent_id, verification_id)
    report.safe_summary = (
        f"Verification {report.decision}: score={report.score.value}, "
        f"{len(findings)} finding(s), loop_risk={report.loop_risk}.")
    if persist:
        save_verification_report(job, report, data_dir)
    return report


# ---------------------------------------------------------------------------
# Public entry — standalone CLI verification (Step 1550)
# ---------------------------------------------------------------------------


def verify_provider_candidate(
    request: ProviderVerificationRequest, *, data_dir: Path | None = None,
) -> ProviderVerificationReport:
    """Verify an existing trust-report candidate. Reads existing entities + the PRIVATE
    quarantine bytes only. NEVER materializes, approves, applies, tests, or executes."""
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.storage import load_job, save_job, JobNotFoundError
    from packages.orchestration.run_contract import (
        ensure_contract, evaluate_run_action, ContractAction,
    )
    from packages.orchestration.provider_trust import get_trust_report
    from packages.orchestration.repair_request_builder import get_request_package

    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    vid = uuid4().hex[:16]

    try:
        job = load_job(UUID(request.job_id), ddir)
    except (ValueError, JobNotFoundError):
        rep = ProviderVerificationReport(verification_id=vid, job_id=request.job_id,
                                         stop_reason=VerificationStopReason.JOB_NOT_FOUND)
        rep.decision = VerificationDecision.INCOMPLETE
        rep.verification_status = VerificationStatus.INCOMPLETE
        rep.impact = _impact_for(VerificationDecision.INCOMPLETE)
        rep.next_safe_action = "remedy job list --json"
        rep.safe_summary = "Job not found."
        return rep

    contract = ensure_contract(job)
    if not evaluate_run_action(contract, ContractAction.PROVIDER_VERIFY_CANDIDATE).allowed:
        rep = ProviderVerificationReport(verification_id=vid, job_id=request.job_id,
                                         stop_reason=VerificationStopReason.CONTRACT_DENIED)
        rep.decision = VerificationDecision.INCOMPLETE
        rep.verification_status = VerificationStatus.INCOMPLETE
        rep.impact = _impact_for(VerificationDecision.INCOMPLETE)
        rep.next_safe_action = f"remedy contract inspect {request.job_id} --json"
        rep.safe_summary = "Contract denies provider verification."
        return rep

    trust = get_trust_report(job, request.trust_report_id) if request.trust_report_id else None
    if trust is None:
        rep = ProviderVerificationReport(
            verification_id=vid, job_id=request.job_id,
            trust_report_id=request.trust_report_id,
            stop_reason=VerificationStopReason.MISSING_TRUST_REPORT)
        rep.decision = VerificationDecision.INCOMPLETE
        rep.verification_status = VerificationStatus.INCOMPLETE
        rep.impact = _impact_for(VerificationDecision.INCOMPLETE)
        rep.findings = [_finding(VerificationFindingCode.CANDIDATE_VERIFICATION_INCOMPLETE,
                                 Severity.MEDIUM, "Trust report not found.")]
        rep.next_safe_action = f"remedy provider trust-show {request.job_id} {request.trust_report_id} --json"
        rep.safe_summary = "Verification incomplete: trust report missing."
        return rep

    quarantine_id = request.quarantine_id or str(trust.get("quarantine_id", ""))
    failure_artifact_id = request.failure_artifact_id or str(trust.get("failure_artifact_id", ""))
    intent_id = str(trust.get("repair_intent_id", ""))
    # Re-read the PRIVATE quarantine bytes to verify the actual candidate text.
    raw_text = _read_quarantined_raw(request.job_id, quarantine_id, ddir) if quarantine_id else ""
    if raw_text:
        candidate, _raw_patch, _f = parse_candidate(raw_text)
    else:
        candidate = _candidate_from_trust_dict(trust)
    candidate_hash = request.candidate_hash or _candidate_hash_from_trust(job, trust)

    request_package = None
    if request.request_package_id:
        request_package = get_request_package(job, request.request_package_id)

    existing = _find_existing_report(
        job, trust_report_id=request.trust_report_id, candidate_hash=candidate_hash,
        request_package_id=request.request_package_id, self_attempt_id=request.self_attempt_id)
    if existing is not None and not request.new:
        return _report_from_dict(existing)

    eff_request = ProviderVerificationRequest(
        job_id=request.job_id, trust_report_id=request.trust_report_id,
        quarantine_id=quarantine_id, material_id=request.material_id or str(trust.get("material_id", "")),
        failure_artifact_id=failure_artifact_id, self_attempt_id=request.self_attempt_id,
        proposed_task_id=request.proposed_task_id, request_package_id=request.request_package_id,
        candidate_hash=candidate_hash, new=request.new)

    report = _build_report(
        job, verification_id=vid, request=eff_request, candidate=candidate, raw_text=raw_text,
        candidate_hash=candidate_hash, request_package=request_package, intent_id=intent_id,
        data_dir=ddir, persist=True)
    save_job(job, root=ddir)
    return report


# ---------------------------------------------------------------------------
# Inline verification — called by intake before materialization (Step 1548)
# ---------------------------------------------------------------------------


def run_inline_verification(
    job: Any, report: Any, candidate: ProviderCandidateRepair, raw_text: str,
    request: Any, data_dir: Path, *, request_package_id: str = "", candidate_hash: str = "",
) -> ProviderVerificationReport:
    """Verify an accepted candidate DURING intake, before any materialization. Does not
    persist the job (the intake caller owns that). Returns a SAFE report."""
    from packages.orchestration.repair_request_builder import get_request_package

    chash = candidate_hash or hashlib.sha256(
        (raw_text or "").encode("utf-8", errors="replace")).hexdigest()
    request_package = get_request_package(job, request_package_id) if request_package_id else None
    # Self-dogfood candidates are self-linked (provider label "self_dogfood:<attempt>"),
    # not failure-linked; route them through the self-relevance check instead.
    provider_name = str(getattr(request, "provider_name", "") or "")
    self_attempt_id = ""
    if provider_name.startswith("self_dogfood:"):
        self_attempt_id = provider_name.split(":", 1)[1]
    eff = ProviderVerificationRequest(
        job_id=str(getattr(job, "id", "")), trust_report_id=getattr(report, "report_id", ""),
        quarantine_id=getattr(report, "quarantine_id", ""),
        failure_artifact_id="" if self_attempt_id else getattr(report, "failure_artifact_id", ""),
        self_attempt_id=self_attempt_id,
        request_package_id=request_package_id, candidate_hash=chash)
    vid = uuid4().hex[:16]
    return _build_report(
        job, verification_id=vid, request=eff, candidate=candidate, raw_text=raw_text or "",
        candidate_hash=chash, request_package=request_package, intent_id="",
        data_dir=data_dir, persist=True)


# ---------------------------------------------------------------------------
# Helpers: reconstruct a candidate from a safe trust report when raw is gone
# ---------------------------------------------------------------------------


def _candidate_from_trust_dict(trust: dict) -> ProviderCandidateRepair:
    c = trust.get("candidate", {}) or {}
    return ProviderCandidateRepair(
        candidate_kind=str(c.get("candidate_kind", "unknown")),
        summary=str(c.get("summary", "")),
        target_files=[str(f) for f in c.get("target_files", []) if isinstance(f, str)],
        patch_format=str(c.get("patch_format", "")),
        has_patch=bool(c.get("has_patch", False)),
        patch_block_count=int(c.get("patch_block_count", 0) or 0),
        hunk_count=int(c.get("hunk_count", 0) or 0),
        line_count=int(c.get("line_count", 0) or 0),
    )


def _candidate_hash_from_trust(job: Any, trust: dict) -> str:
    """Resolve the candidate hash from a linked material, else hash the quarantine id."""
    try:
        from packages.orchestration.provider_patch_material import load_materials
        for m in load_materials(job).values():
            if m.get("trust_report_id") == trust.get("report_id") and m.get("candidate_hash"):
                return str(m["candidate_hash"])
    except (ImportError, AttributeError, TypeError):
        pass
    return hashlib.sha256(str(trust.get("quarantine_id", "")).encode("utf-8")).hexdigest()


def _report_from_dict(d: dict) -> ProviderVerificationReport:
    rep = ProviderVerificationReport(
        verification_id=str(d.get("verification_id", "")), job_id=str(d.get("job_id", "")),
        trust_report_id=str(d.get("trust_report_id", "")),
        quarantine_id=str(d.get("quarantine_id", "")), material_id=str(d.get("material_id", "")),
        failure_artifact_id=str(d.get("failure_artifact_id", "")),
        self_attempt_id=str(d.get("self_attempt_id", "")),
        proposed_task_id=str(d.get("proposed_task_id", "")),
        request_package_id=str(d.get("request_package_id", "")),
        candidate_hash=str(d.get("candidate_hash", "")),
        verification_status=str(d.get("verification_status", VerificationStatus.INCOMPLETE)),
        decision=str(d.get("decision", VerificationDecision.INCOMPLETE)),
        stop_reason=str(d.get("stop_reason", "")),
        loop_risk=str(d.get("loop_risk", LoopRisk.NONE)),
        allowed_to_materialize=bool(d.get("allowed_to_materialize", False)),
        allowed_to_create_intent=bool(d.get("allowed_to_create_intent", False)),
        advisor_critique=d.get("advisor_critique"),
        next_safe_action=str(d.get("next_safe_action", "")),
        safe_summary=str(d.get("safe_summary", "")), created_at=str(d.get("created_at", "")),
    )
    sc = d.get("score", {}) or {}
    rep.score = ProviderVerificationScore(float(sc.get("value", 0.0)), str(sc.get("band", "low")))
    im = d.get("impact", {}) or {}
    rep.impact = ProviderVerificationImpact(
        str(im.get("impact", VerificationImpact.INCOMPLETE)),
        bool(im.get("allowed_to_materialize", False)),
        bool(im.get("allowed_to_create_intent", False)))
    rep.findings = [ProviderVerificationFinding(f.get("code", ""), f.get("severity", ""),
                                                f.get("summary", ""), f.get("target", ""))
                    for f in d.get("findings", []) if isinstance(f, dict)]
    rep.evidence_refs = [ProviderVerificationEvidenceRef(e.get("kind", ""), e.get("ref_id", ""),
                                                         e.get("label", ""))
                         for e in d.get("evidence_refs", []) if isinstance(e, dict)]
    return rep
