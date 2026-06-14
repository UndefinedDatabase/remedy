"""
Provider Trust Gate + External Repair Intake v0 (Steps 1305-1334).

External model/agent output (Claude / Fable / Sonnet / Opus / Pi / Ollama) is
produced OUTSIDE Remedy and is treated as **untrusted**. This module takes a local
file or stdin containing a candidate repair, quarantines the raw bytes privately,
parses/normalizes a conservative v0 format, runs trust validation (secret scan,
path safety, patch shape, failure linkage), emits a safe ``ProviderTrustReport``,
and ONLY when accepted creates a Repair Artifact + a pending Repair Patch Intent.

Hard rules enforced here:
  - NO provider/Ollama/Claude API execution, NO model invocation, NO network, NO
    subprocess. Input is a local file or stdin only.
  - Raw provider output is stored ONLY under a private 0o700 quarantine dir (0o600
    file) and is NEVER exported to any public surface (CLI/events/Job metadata/
    review bundle/cockpit). Public surfaces carry safe summaries / counts / IDs only.
  - No raw source, diffs, secrets, tracebacks, or absolute private paths in public.
  - Patch Intent creation ONLY; approval_required; apply stays via ``do continue``.
    Accepted ≠ applied ≠ approved ≠ verified.

Public API::

    intake_provider_repair(request, *, input_path=None, stdin_text=None, data_dir=None)
        -> ProviderRepairIntakeResult
    load_trust_reports(job) -> dict[str, dict]
    get_trust_report(job, report_id) -> dict | None
    export_trust_report_json(report) -> dict
    export_intake_result_json(result) -> dict
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


# ---------------------------------------------------------------------------
# Limits (Step 1308 / 1313)
# ---------------------------------------------------------------------------

MAX_INPUT_BYTES = 256 * 1024        # 256 KiB hard cap on intake input
MAX_TARGET_FILES = 10
MAX_HUNKS = 50
MAX_PATCH_LINES = 2000
_QUARANTINE_RAW_NAME = "raw_input.txt"


# ---------------------------------------------------------------------------
# Vocabularies (Steps 1306 / 1310)
# ---------------------------------------------------------------------------


class TrustStatus:
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    NEEDS_HUMAN_REVIEW = "needs_human_review"


class CandidateKind:
    PATCH = "patch"
    EXPLANATION = "explanation"
    MIXED = "mixed"
    UNKNOWN = "unknown"


class SourceKind:
    FILE = "file"
    STDIN = "stdin"
    MANUAL = "manual"


class Severity:
    BLOCKER = "blocker"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TrustFindingCode:
    PROVIDER_OUTPUT_UNPARSEABLE = "provider_output_unparseable"
    MULTIPLE_PATCH_CANDIDATES = "multiple_patch_candidates"
    RAW_SECRET_DETECTED = "raw_secret_detected"
    PROTECTED_PATH_TARGETED = "protected_path_targeted"
    PATH_TRAVERSAL = "path_traversal"
    ABSOLUTE_PATH = "absolute_path"
    UNKNOWN_FILE_TARGET = "unknown_file_target"
    GENERATED_FILE_TOO_LARGE = "generated_file_too_large"
    PATCH_TOO_LARGE = "patch_too_large"
    UNSUPPORTED_PATCH_OPERATION = "unsupported_patch_operation"
    DELETES_FILE = "deletes_file"
    BINARY_FILE_CHANGE = "binary_file_change"
    TEST_FILE_ONLY_CHANGE = "test_file_only_change"
    DOCS_ONLY_CHANGE = "docs_only_change"
    NO_FAILURE_LINK = "no_failure_link"
    NO_REPAIR_ATTEMPT_LINK = "no_repair_attempt_link"
    LOW_CONFIDENCE = "low_confidence"
    REQUIRES_HUMAN_REVIEW = "requires_human_review"
    # Input intake (Step 1308) — surfaced as findings, never tracebacks.
    INPUT_NOT_FOUND = "input_not_found"
    INPUT_TOO_LARGE = "input_too_large"
    INPUT_BINARY = "input_binary"
    INPUT_NUL_BYTE = "input_nul_byte"
    INPUT_EMPTY = "input_empty"


# ---------------------------------------------------------------------------
# Models (Step 1306) — no raw output fields in any public model.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ProviderOutputIntakeRequest:
    job_id: str
    failure_artifact_id: str = ""
    repair_attempt_id: str = ""
    provider_name: str = "unknown"
    model_name: str = ""
    source_kind: str = SourceKind.FILE


@dataclass
class ProviderOutputQuarantineRecord:
    quarantine_id: str
    job_id: str
    received_at: str
    source_kind: str
    byte_count: int
    content_sha256: str
    provider_name: str
    model_name: str = ""
    stored: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "quarantine_id": self.quarantine_id, "job_id": self.job_id,
            "received_at": self.received_at, "source_kind": self.source_kind,
            "byte_count": self.byte_count, "content_sha256": self.content_sha256,
            "provider_name": self.provider_name, "model_name": self.model_name,
            "stored": self.stored,
        }


@dataclass
class ProviderCandidateRepair:
    """Safe, public candidate metadata. NEVER carries the raw diff/source."""

    candidate_kind: str = CandidateKind.UNKNOWN
    summary: str = ""
    target_files: list[str] = field(default_factory=list)
    patch_format: str = ""              # unified_diff | structured_operations | none
    rationale: str = ""
    risk_notes: str = ""
    has_patch: bool = False
    patch_block_count: int = 0
    hunk_count: int = 0
    line_count: int = 0


@dataclass
class ProviderTrustFinding:
    code: str
    severity: str
    summary: str
    target: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"code": self.code, "severity": self.severity,
                "summary": self.summary, "target": self.target}


@dataclass
class ProviderTrustDecision:
    trust_status: str
    confidence: float
    reason: str = ""


@dataclass
class ProviderTrustReport:
    report_id: str
    job_id: str
    quarantine_id: str
    provider_name: str
    model_name: str = ""
    failure_artifact_id: str = ""
    repair_attempt_id: str = ""
    candidate_kind: str = CandidateKind.UNKNOWN
    trust_status: str = TrustStatus.NEEDS_HUMAN_REVIEW
    confidence: float = 0.0
    findings: list[ProviderTrustFinding] = field(default_factory=list)
    candidate: ProviderCandidateRepair | None = None
    repair_artifact_id: str = ""
    repair_intent_id: str = ""
    next_safe_action: str = ""
    received_at: str = ""
    safe_summary: str = ""


@dataclass
class ProviderRepairIntakeResult:
    job_id: str
    quarantine_id: str = ""
    trust_report_id: str = ""
    trust_status: str = TrustStatus.REJECTED
    candidate_kind: str = CandidateKind.UNKNOWN
    confidence: float = 0.0
    findings: list[ProviderTrustFinding] = field(default_factory=list)
    repair_artifact_id: str = ""
    repair_intent_id: str = ""
    next_safe_action: str = ""
    safe_summary: str = ""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _finding(code: str, severity: str, summary: str, target: str = "") -> ProviderTrustFinding:
    return ProviderTrustFinding(code=code, severity=severity, summary=summary, target=target)


def _dedupe_findings(findings: list[ProviderTrustFinding]) -> list[ProviderTrustFinding]:
    seen: set[tuple[str, str]] = set()
    out: list[ProviderTrustFinding] = []
    for f in findings:
        key = (f.code, f.target)
        if key in seen:
            continue
        seen.add(key)
        out.append(f)
    return out


# ---------------------------------------------------------------------------
# Input reading + limits (Step 1308)
# ---------------------------------------------------------------------------


def read_intake_input(
    *, input_path: str | None = None, stdin_text: str | None = None
) -> tuple[str, ProviderTrustFinding | None]:
    """Read intake input safely. Returns (text, finding|None).

    A non-None finding means the input is rejected (oversized/binary/NUL/missing/
    empty); the text is "" in that case. Never raises on bad input, never echoes a
    traceback or an absolute path.
    """
    if stdin_text is not None:
        data = stdin_text.encode("utf-8", errors="surrogatepass") if isinstance(stdin_text, str) else b""
        return _decode_bytes(data)

    if not input_path:
        return "", _finding(TrustFindingCode.INPUT_NOT_FOUND, Severity.BLOCKER,
                            "No input path or stdin provided.")
    try:
        p = Path(input_path)
        if not p.is_file():
            return "", _finding(TrustFindingCode.INPUT_NOT_FOUND, Severity.BLOCKER,
                                "Input file not found.")
        size = p.stat().st_size
        if size > MAX_INPUT_BYTES:
            return "", _finding(TrustFindingCode.INPUT_TOO_LARGE, Severity.BLOCKER,
                                f"Input exceeds {MAX_INPUT_BYTES} bytes.")
        data = p.read_bytes()
    except OSError:
        return "", _finding(TrustFindingCode.INPUT_NOT_FOUND, Severity.BLOCKER,
                            "Input file could not be read.")
    return _decode_bytes(data)


def _decode_bytes(data: bytes) -> tuple[str, ProviderTrustFinding | None]:
    if len(data) > MAX_INPUT_BYTES:
        return "", _finding(TrustFindingCode.INPUT_TOO_LARGE, Severity.BLOCKER,
                            f"Input exceeds {MAX_INPUT_BYTES} bytes.")
    if not data.strip():
        return "", _finding(TrustFindingCode.INPUT_EMPTY, Severity.BLOCKER, "Input is empty.")
    if b"\x00" in data:
        return "", _finding(TrustFindingCode.INPUT_NUL_BYTE, Severity.BLOCKER,
                            "Input contains NUL bytes (binary).")
    # Binary heuristic: a high ratio of non-text control bytes → reject.
    sample = data[:8192]
    text_bytes = sum(1 for b in sample if b in (9, 10, 13) or 32 <= b <= 126 or b >= 128)
    if sample and (text_bytes / len(sample)) < 0.70:
        return "", _finding(TrustFindingCode.INPUT_BINARY, Severity.BLOCKER,
                            "Input appears to be binary.")
    # Invalid UTF-8 is decoded with replacement (safe), never raised.
    return data.decode("utf-8", errors="replace"), None


# ---------------------------------------------------------------------------
# Private quarantine storage (Step 1307)
# ---------------------------------------------------------------------------


def _quarantine_root(job_id: str, data_dir: Path) -> Path:
    return data_dir / "workspaces" / job_id / "provider_quarantine"


def _quarantine_dir(job_id: str, quarantine_id: str, data_dir: Path) -> Path:
    return _quarantine_root(job_id, data_dir) / quarantine_id


def store_quarantine(
    job_id: str, data_dir: Path, raw_text: str, request: ProviderOutputIntakeRequest
) -> ProviderOutputQuarantineRecord:
    """Persist raw provider output privately. Returns a SAFE quarantine record
    (hash + counts only). The raw bytes never leave this directory."""
    qid = uuid4().hex[:16]
    qdir = _quarantine_dir(job_id, qid, data_dir)
    encoded = raw_text.encode("utf-8", errors="replace")
    sha = hashlib.sha256(encoded).hexdigest()
    record = ProviderOutputQuarantineRecord(
        quarantine_id=qid, job_id=job_id, received_at=_now(),
        source_kind=request.source_kind, byte_count=len(encoded),
        content_sha256=sha, provider_name=request.provider_name,
        model_name=request.model_name, stored=False,
    )
    try:
        qdir.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(qdir, 0o700)
        except OSError:
            pass
        raw_path = qdir / _QUARANTINE_RAW_NAME
        # No overwrite: a fresh uuid dir means this never collides.
        tmp = raw_path.with_suffix(".txt.tmp")
        tmp.write_bytes(encoded)
        try:
            os.chmod(tmp, 0o600)
        except OSError:
            pass
        os.replace(tmp, raw_path)
        try:
            os.chmod(raw_path, 0o600)
        except OSError:
            pass
        (qdir / "meta.json").write_bytes(
            json.dumps(record.to_dict(), indent=2, sort_keys=True).encode("utf-8"))
        record.stored = True
    except OSError:
        record.stored = False
    return record


def _read_quarantined_raw(job_id: str, quarantine_id: str, data_dir: Path) -> str:
    """PRIVATE: read quarantined raw input. Never call from a public export path."""
    p = _quarantine_dir(job_id, quarantine_id, data_dir) / _QUARANTINE_RAW_NAME
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


# ---------------------------------------------------------------------------
# Candidate parser (Step 1309)
# ---------------------------------------------------------------------------

_FENCE_RE = re.compile(r"```[ \t]*([A-Za-z0-9_+-]*)[ \t]*\n(.*?)```", re.DOTALL)
_DIFF_HEADER_RE = re.compile(r"^\+\+\+ ", re.MULTILINE)
_HUNK_RE = re.compile(r"^@@ ", re.MULTILINE)


def parse_candidate(raw_text: str) -> tuple[ProviderCandidateRepair, str, list[ProviderTrustFinding]]:
    """Parse a conservative v0 candidate. Returns (candidate, raw_patch, findings).

    ``raw_patch`` is the private diff text (kept out of the public candidate). v0
    accepts: a structured JSON object, OR markdown containing exactly one fenced
    unified diff. Explanations without a patch → needs_human_review (no patch);
    multiple patch blocks → finding; unknown → unparseable.
    """
    findings: list[ProviderTrustFinding] = []
    stripped = raw_text.strip()

    # 1. Structured JSON.
    if stripped.startswith("{"):
        try:
            obj = json.loads(stripped)
        except (json.JSONDecodeError, ValueError):
            obj = None
        if isinstance(obj, dict):
            return _parse_json_candidate(obj, findings)

    # 2. Markdown fenced blocks → find diff blocks.
    blocks = _FENCE_RE.findall(raw_text)
    diff_blocks = [body for (lang, body) in blocks
                   if lang.lower() == "diff" or _looks_like_diff(body)]
    if len(diff_blocks) > 1:
        findings.append(_finding(TrustFindingCode.MULTIPLE_PATCH_CANDIDATES, Severity.HIGH,
                                 f"{len(diff_blocks)} patch candidates found; v0 accepts exactly one."))
        cand = ProviderCandidateRepair(candidate_kind=CandidateKind.MIXED,
                                       summary=_safe_first_line(raw_text), patch_block_count=len(diff_blocks))
        return cand, "", findings
    if len(diff_blocks) == 1:
        raw_patch = diff_blocks[0]
        cand = _candidate_from_diff(raw_patch, summary=_safe_first_line(raw_text))
        cand.patch_block_count = 1
        return cand, raw_patch, findings

    # 3. Prose only / unknown.
    if _looks_like_prose(stripped):
        cand = ProviderCandidateRepair(candidate_kind=CandidateKind.EXPLANATION,
                                       summary=_safe_first_line(raw_text), patch_format="none")
        findings.append(_finding(TrustFindingCode.REQUIRES_HUMAN_REVIEW, Severity.MEDIUM,
                                 "Explanation only — no patch candidate to validate."))
        return cand, "", findings

    findings.append(_finding(TrustFindingCode.PROVIDER_OUTPUT_UNPARSEABLE, Severity.HIGH,
                             "Provider output is not a recognized v0 candidate format."))
    return ProviderCandidateRepair(candidate_kind=CandidateKind.UNKNOWN), "", findings


def _parse_json_candidate(
    obj: dict, findings: list[ProviderTrustFinding]
) -> tuple[ProviderCandidateRepair, str, list[ProviderTrustFinding]]:
    summary = _safe_text(obj.get("summary", ""), 200)
    rationale = _safe_text(obj.get("rationale", ""), 300)
    risk_notes = _safe_text(obj.get("risk_notes", ""), 300)
    target_files = [str(f) for f in obj.get("target_files", []) if isinstance(f, str)][:MAX_TARGET_FILES + 5]
    unified = obj.get("unified_diff")
    structured = obj.get("structured_operations")
    raw_patch = ""
    if isinstance(unified, str) and unified.strip():
        raw_patch = unified
        cand = _candidate_from_diff(unified, summary=summary)
        cand.patch_format = "unified_diff"
        if not cand.target_files:
            cand.target_files = target_files
    elif isinstance(structured, list) and structured:
        files = [str(op.get("path", "")) for op in structured if isinstance(op, dict)]
        raw_patch = json.dumps(structured)
        cand = ProviderCandidateRepair(
            candidate_kind=CandidateKind.PATCH, summary=summary,
            target_files=[f for f in files if f][:MAX_TARGET_FILES + 5] or target_files,
            patch_format="structured_operations", has_patch=True,
            line_count=len(structured),
        )
    else:
        cand = ProviderCandidateRepair(candidate_kind=CandidateKind.EXPLANATION,
                                       summary=summary, target_files=target_files, patch_format="none")
        findings.append(_finding(TrustFindingCode.REQUIRES_HUMAN_REVIEW, Severity.MEDIUM,
                                 "Structured output has no patch — explanation only."))
    cand.rationale = rationale
    cand.risk_notes = risk_notes
    cand.patch_block_count = 1 if cand.has_patch else 0
    return cand, raw_patch, findings


def _candidate_from_diff(raw_patch: str, *, summary: str) -> ProviderCandidateRepair:
    targets = _targets_from_diff(raw_patch)
    return ProviderCandidateRepair(
        candidate_kind=CandidateKind.PATCH, summary=summary,
        target_files=targets, patch_format="unified_diff", has_patch=True,
        hunk_count=len(_HUNK_RE.findall(raw_patch)),
        line_count=raw_patch.count("\n") + 1,
    )


def _targets_from_diff(raw_patch: str) -> list[str]:
    targets: list[str] = []
    for line in raw_patch.splitlines():
        if line.startswith("+++ ") or line.startswith("--- "):
            path = line[4:].strip().split("\t")[0]
            if path in ("/dev/null", ""):
                continue
            if path.startswith(("a/", "b/")):
                path = path[2:]
            if path not in targets:
                targets.append(path)
    return targets[:MAX_TARGET_FILES + 5]


def _looks_like_diff(text: str) -> bool:
    return bool(_DIFF_HEADER_RE.search(text)) or "@@ " in text or text.lstrip().startswith("diff --git")


def _looks_like_prose(text: str) -> bool:
    return len(text.split()) >= 3


def _safe_first_line(text: str) -> str:
    for line in text.splitlines():
        s = line.strip().lstrip("#").strip()
        if s:
            return _safe_text(s, 200)
    return ""


def _safe_text(text: str, limit: int) -> str:
    """Collapse whitespace + truncate; strip anything that could be a secret/path
    is handled separately — this only bounds length and removes control chars."""
    out = re.sub(r"\s+", " ", str(text)).strip()
    return out[:limit]


# ---------------------------------------------------------------------------
# Secret / raw-leak scanner (Step 1311)
# ---------------------------------------------------------------------------

_SECRET_PATTERNS = [
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bsk-[A-Za-z0-9]{16,}\b"),
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._\-]{12,}"),
    re.compile(r"(?i)\b(api[_-]?key|secret|token|password|passwd|pwd)\b\s*[:=]\s*\S{6,}"),
    re.compile(r"(?i)\bAWS_SECRET_ACCESS_KEY\b\s*[:=]\s*\S+"),
]
_ABS_PATH_RE = re.compile(r"(?:^|[\s\"'=(])(/(?:home|Users|root|etc|var|opt|private)/[^\s\"':]+)")
_TRACEBACK_RE = re.compile(r"Traceback \(most recent call last\)")


def scan_secrets(text: str) -> list[ProviderTrustFinding]:
    """Detect secret-like / raw-leak material. NEVER echoes the matched value."""
    findings: list[ProviderTrustFinding] = []
    if any(p.search(text) for p in _SECRET_PATTERNS):
        findings.append(_finding(TrustFindingCode.RAW_SECRET_DETECTED, Severity.BLOCKER,
                                 "Secret-like material detected in provider output."))
    if _ABS_PATH_RE.search(text):
        findings.append(_finding(TrustFindingCode.ABSOLUTE_PATH, Severity.HIGH,
                                 "Absolute filesystem path detected in provider output."))
    if _TRACEBACK_RE.search(text):
        findings.append(_finding(TrustFindingCode.REQUIRES_HUMAN_REVIEW, Severity.MEDIUM,
                                 "Traceback-like block detected — needs human review."))
    return findings


# ---------------------------------------------------------------------------
# Path safety validation (Step 1312)
# ---------------------------------------------------------------------------

_PROTECTED_SUBSTRINGS = (
    ".env", ".data", ".git", "node_modules", "__pycache__", ".cache",
    "credentials", "secrets", "id_rsa", ".ssh", ".aws",
)
_GENERATED_FILES = (
    "package-lock.json", "poetry.lock", "yarn.lock", "pnpm-lock.yaml",
    "Pipfile.lock", "Cargo.lock", "go.sum",
)


def validate_paths(target_files: list[str]) -> list[ProviderTrustFinding]:
    findings: list[ProviderTrustFinding] = []
    for path in target_files:
        p = (path or "").strip()
        if not p:
            findings.append(_finding(TrustFindingCode.UNKNOWN_FILE_TARGET, Severity.HIGH,
                                     "Empty target path."))
            continue
        if p.startswith("/") or re.match(r"^[A-Za-z]:[\\/]", p):
            findings.append(_finding(TrustFindingCode.ABSOLUTE_PATH, Severity.BLOCKER,
                                     "Target path is absolute.", target=_safe_path_label(p)))
            continue
        parts = p.replace("\\", "/").split("/")
        if ".." in parts:
            findings.append(_finding(TrustFindingCode.PATH_TRAVERSAL, Severity.BLOCKER,
                                     "Target path contains traversal.", target=_safe_path_label(p)))
            continue
        low = p.lower()
        if any(sub in low for sub in _PROTECTED_SUBSTRINGS):
            findings.append(_finding(TrustFindingCode.PROTECTED_PATH_TARGETED, Severity.BLOCKER,
                                     "Target path is protected.", target=_safe_path_label(p)))
            continue
        if any(p.endswith(g) or low.endswith(".lock") for g in _GENERATED_FILES):
            findings.append(_finding(TrustFindingCode.UNSUPPORTED_PATCH_OPERATION, Severity.HIGH,
                                     "Generated/lock file change not allowed in v0.",
                                     target=_safe_path_label(p)))
    return findings


def _safe_path_label(path: str) -> str:
    """A repo-relative-ish, length-bounded label. Never an absolute path."""
    p = (path or "").replace("\\", "/")
    if p.startswith("/"):
        p = p.rsplit("/", 1)[-1]
    return p[:80]


# ---------------------------------------------------------------------------
# Patch shape validation (Step 1313)
# ---------------------------------------------------------------------------


def validate_patch_shape(candidate: ProviderCandidateRepair, raw_patch: str) -> list[ProviderTrustFinding]:
    findings: list[ProviderTrustFinding] = []
    if not candidate.has_patch:
        return findings
    if len(candidate.target_files) > MAX_TARGET_FILES:
        findings.append(_finding(TrustFindingCode.PATCH_TOO_LARGE, Severity.HIGH,
                                 f"Patch touches {len(candidate.target_files)} files (> {MAX_TARGET_FILES})."))
    if candidate.hunk_count > MAX_HUNKS:
        findings.append(_finding(TrustFindingCode.PATCH_TOO_LARGE, Severity.HIGH,
                                 f"Patch has {candidate.hunk_count} hunks (> {MAX_HUNKS})."))
    if candidate.line_count > MAX_PATCH_LINES:
        findings.append(_finding(TrustFindingCode.PATCH_TOO_LARGE, Severity.HIGH,
                                 f"Patch has {candidate.line_count} lines (> {MAX_PATCH_LINES})."))
    if "GIT binary patch" in raw_patch or re.search(r"^Binary files ", raw_patch, re.MULTILINE):
        findings.append(_finding(TrustFindingCode.BINARY_FILE_CHANGE, Severity.BLOCKER,
                                 "Patch contains a binary file change."))
    if "+++ /dev/null" in raw_patch or re.search(r"^deleted file mode", raw_patch, re.MULTILINE):
        findings.append(_finding(TrustFindingCode.DELETES_FILE, Severity.HIGH,
                                 "Patch deletes a file (blocked in v0)."))
    if re.search(r"^rename (from|to) ", raw_patch, re.MULTILINE):
        findings.append(_finding(TrustFindingCode.UNSUPPORTED_PATCH_OPERATION, Severity.HIGH,
                                 "Patch renames a file (unsupported in v0)."))
    # Classification (informational severity).
    files = candidate.target_files
    if files and all(_is_test_path(f) for f in files):
        findings.append(_finding(TrustFindingCode.TEST_FILE_ONLY_CHANGE, Severity.MEDIUM,
                                 "Candidate changes test files only."))
    elif files and all(_is_docs_path(f) for f in files):
        findings.append(_finding(TrustFindingCode.DOCS_ONLY_CHANGE, Severity.LOW,
                                 "Candidate changes documentation only."))
    return findings


def _is_test_path(p: str) -> bool:
    low = p.lower()
    return low.startswith("tests/") or "/tests/" in low or "/test_" in low or low.startswith("test_") or low.endswith("_test.py")


def _is_docs_path(p: str) -> bool:
    low = p.lower()
    return low.startswith("docs/") or low.endswith(".md") or low.endswith(".rst")


# ---------------------------------------------------------------------------
# Failure link validation (Step 1314)
# ---------------------------------------------------------------------------


def validate_failure_link(
    job: Any, candidate: ProviderCandidateRepair,
    failure_artifact_id: str, repair_attempt_id: str,
) -> tuple[list[ProviderTrustFinding], str]:
    """Validate / resolve the failure linkage. Returns (findings, linked_attempt_id)."""
    findings: list[ProviderTrustFinding] = []
    linked_attempt = repair_attempt_id

    if not failure_artifact_id:
        findings.append(_finding(TrustFindingCode.NO_FAILURE_LINK, Severity.LOW,
                                 "No failure artifact linked — confidence reduced."))
        return findings, linked_attempt

    fa = next((a for a in job.artifacts if str(a.id) == failure_artifact_id), None)
    if fa is None:
        findings.append(_finding(TrustFindingCode.NO_FAILURE_LINK, Severity.HIGH,
                                 "Referenced failure artifact does not exist."))
        return findings, linked_attempt
    meta = fa.metadata or {}
    if not meta.get("test_failure"):
        findings.append(_finding(TrustFindingCode.NO_FAILURE_LINK, Severity.HIGH,
                                 "Referenced artifact is not a test failure."))
        return findings, linked_attempt
    if meta.get("failure_resolved"):
        findings.append(_finding(TrustFindingCode.REQUIRES_HUMAN_REVIEW, Severity.MEDIUM,
                                 "Referenced failure is already resolved."))

    # Link an existing repair attempt if present.
    if not linked_attempt:
        try:
            from packages.orchestration.repair_loop import find_repair_attempt
            att = find_repair_attempt(job, failure_artifact_id)
            if att is not None:
                linked_attempt = att.attempt_id
        except (ImportError, ValueError, KeyError, TypeError, AttributeError):
            pass
    if not linked_attempt:
        findings.append(_finding(TrustFindingCode.NO_REPAIR_ATTEMPT_LINK, Severity.LOW,
                                 "No prior repair attempt linked."))

    # Overlap heuristic between candidate targets and known related files.
    related = [str(f) for f in (meta.get("related_files") or []) if isinstance(f, str)]
    if related and candidate.target_files:
        rel_base = {_safe_path_label(f) for f in related}
        cand_base = {_safe_path_label(f) for f in candidate.target_files}
        if not (rel_base & cand_base):
            findings.append(_finding(TrustFindingCode.LOW_CONFIDENCE, Severity.MEDIUM,
                                     "Candidate targets do not overlap the failure's known files."))
    # A docs-only candidate must not claim a source fix.
    if candidate.has_patch and all(_is_docs_path(f) for f in candidate.target_files):
        claim = f"{candidate.summary} {candidate.risk_notes} {candidate.rationale}".lower()
        if "source fix" in claim or "fixes the bug" in claim or "resolves the failure" in claim:
            findings.append(_finding(TrustFindingCode.REQUIRES_HUMAN_REVIEW, Severity.MEDIUM,
                                     "Docs-only candidate claims a source fix."))
    return findings, linked_attempt


# ---------------------------------------------------------------------------
# Trust decision (Step 1315)
# ---------------------------------------------------------------------------

_SEVERITY_WEIGHT = {Severity.BLOCKER: 1.0, Severity.HIGH: 0.6,
                    Severity.MEDIUM: 0.25, Severity.LOW: 0.08}


def decide_trust(candidate: ProviderCandidateRepair,
                 findings: list[ProviderTrustFinding]) -> ProviderTrustDecision:
    """Map findings + candidate shape to a trust status + confidence (Step 1315)."""
    has_blocker = any(f.severity == Severity.BLOCKER for f in findings)
    has_high = any(f.severity == Severity.HIGH for f in findings)
    has_medium = any(f.severity == Severity.MEDIUM for f in findings)

    penalty = sum(_SEVERITY_WEIGHT.get(f.severity, 0.0) for f in findings)
    confidence = round(max(0.0, min(1.0, 0.85 - penalty)), 2)

    if has_blocker or has_high:
        return ProviderTrustDecision(TrustStatus.REJECTED, confidence,
                                     "Blocker/high finding present.")
    if not candidate.has_patch:
        return ProviderTrustDecision(TrustStatus.NEEDS_HUMAN_REVIEW, confidence,
                                     "No parseable patch candidate.")
    if has_medium:
        return ProviderTrustDecision(TrustStatus.NEEDS_HUMAN_REVIEW, confidence,
                                     "Medium finding present.")
    return ProviderTrustDecision(TrustStatus.ACCEPTED, confidence,
                                 "Low-only findings; eligible for a pending intent.")


# ---------------------------------------------------------------------------
# Report persistence (safe; no raw) + exports
# ---------------------------------------------------------------------------

_REPORTS_META_KEY = "provider_trust_reports_v0"


def export_trust_report_json(report: ProviderTrustReport) -> dict[str, Any]:
    cand = report.candidate or ProviderCandidateRepair()
    return {
        "version": 1,
        "report_id": report.report_id,
        "job_id": report.job_id,
        "quarantine_id": report.quarantine_id,
        "provider_name": report.provider_name,
        "model_name": report.model_name,
        "failure_artifact_id": report.failure_artifact_id,
        "repair_attempt_id": report.repair_attempt_id,
        "candidate_kind": report.candidate_kind,
        "trust_status": report.trust_status,
        "confidence": report.confidence,
        "findings": [f.to_dict() for f in report.findings],
        "candidate": {
            "candidate_kind": cand.candidate_kind,
            "summary": cand.summary,
            "target_files": [_safe_path_label(f) for f in cand.target_files],
            "patch_format": cand.patch_format,
            "has_patch": cand.has_patch,
            "patch_block_count": cand.patch_block_count,
            "hunk_count": cand.hunk_count,
            "line_count": cand.line_count,
        },
        "repair_artifact_id": report.repair_artifact_id,
        "repair_intent_id": report.repair_intent_id,
        "next_safe_action": report.next_safe_action,
        "received_at": report.received_at,
        "safe_summary": report.safe_summary,
    }


def save_trust_report(job: Any, report: ProviderTrustReport) -> None:
    """Persist a SAFE trust report dict in job metadata. Caller persists the job."""
    store = job.metadata.setdefault(_REPORTS_META_KEY, {})
    store[report.report_id] = export_trust_report_json(report)


def load_trust_reports(job: Any) -> dict[str, dict]:
    return dict((job.metadata or {}).get(_REPORTS_META_KEY, {}))


def get_trust_report(job: Any, report_id: str) -> dict | None:
    return load_trust_reports(job).get(report_id)


def export_intake_result_json(result: ProviderRepairIntakeResult) -> dict[str, Any]:
    return {
        "version": 1,
        "job_id": result.job_id,
        "quarantine_id": result.quarantine_id,
        "trust_report_id": result.trust_report_id,
        "trust_status": result.trust_status,
        "candidate_kind": result.candidate_kind,
        "confidence": result.confidence,
        "findings": [f.to_dict() for f in result.findings],
        "repair_artifact_id": result.repair_artifact_id,
        "repair_intent_id": result.repair_intent_id,
        "next_safe_action": result.next_safe_action,
        "safe_summary": result.safe_summary,
    }


# ---------------------------------------------------------------------------
# Repair Artifact + Patch Intent from an accepted candidate (Steps 1316-1317)
# ---------------------------------------------------------------------------


def _create_repair_artifact_and_intent(
    job: Any, report: ProviderTrustReport, candidate: ProviderCandidateRepair,
    request: ProviderOutputIntakeRequest,
) -> tuple[str, str]:
    """Create a Repair Artifact yielding ONE pending Patch Intent. Returns
    (artifact_id, intent_id) or ("","") if the intent could not be verified.

    No raw patch/source is stored on the artifact's public-facing fields — only a
    reference to the private quarantine + the safe trust report."""
    from packages.core.models import Artifact, ArtifactKind
    from packages.orchestration.approval_queue import get_patch_intent, make_intent_id

    primary = _safe_path_label(candidate.target_files[0]) if candidate.target_files else \
        f"docs/provider_repairs/{report.quarantine_id}.md"
    action = "modify" if candidate.target_files else "create"
    extra = f" (+{len(candidate.target_files) - 1} more files)" if len(candidate.target_files) > 1 else ""
    risk = "medium"  # provider-sourced; never auto-low

    art = Artifact(
        name=f"provider-repair-{report.quarantine_id[:8]}",
        content=f"Provider-sourced repair proposal (trust={report.trust_status}, "
                f"provider={request.provider_name}). Raw output quarantined privately.",
        kind=ArtifactKind.BUILDER_PROPOSAL,
        task_id=None,
        metadata={
            "provider_repair_v0": True,
            "provider_trust_report_id": report.report_id,
            "quarantine_id": report.quarantine_id,
            "failure_artifact_id": report.failure_artifact_id,
            "repair_attempt_id": report.repair_attempt_id,
            "provider_name": request.provider_name,
            "model_name": request.model_name,
            "candidate_kind": candidate.candidate_kind,
            "patch_format": candidate.patch_format,
            "trust_status": report.trust_status,
            "trust_confidence": report.confidence,
            "trust_findings": [f.to_dict() for f in report.findings],
            "safe_summary": f"Provider repair ({candidate.patch_format}) pending approval.",
            "patch_intent_explanations": [
                {
                    "file": primary,
                    "action": action,
                    "risk": risk,
                    "reason": f"Provider-sourced repair (untrusted, trust-gated) for "
                              f"failure {report.failure_artifact_id[:8] or 'n/a'}{extra}.",
                    "summary": f"Provider repair: {candidate.summary[:100]}",
                },
            ],
            "patch_intent_approvals": {},
        },
    )
    job.artifacts.append(art)

    intent_id = make_intent_id(art.id, 0)
    # Verify the intent is real + resolvable before claiming it exists.
    if get_patch_intent(job, intent_id) is None:
        return "", ""
    return str(art.id), intent_id


# ---------------------------------------------------------------------------
# Top-level orchestrator (Steps 1306-1317)
# ---------------------------------------------------------------------------


def intake_provider_repair(
    request: ProviderOutputIntakeRequest,
    *,
    input_path: str | None = None,
    stdin_text: str | None = None,
    data_dir: Path | None = None,
) -> ProviderRepairIntakeResult:
    """Ingest untrusted external provider output and, only when accepted, create a
    pending Repair Patch Intent. No provider execution, no apply, no approval."""
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.storage import load_job, save_job, JobNotFoundError
    from packages.orchestration.run_contract import (
        ensure_contract, evaluate_run_action, ContractAction,
    )

    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    result = ProviderRepairIntakeResult(job_id=request.job_id)

    # 1. Job exists.
    try:
        job = load_job(UUID(request.job_id), ddir)
    except (ValueError, JobNotFoundError):
        result.trust_status = TrustStatus.REJECTED
        result.next_safe_action = "remedy job list --json"
        result.safe_summary = "Job not found."
        return result

    # 2. Contract gate: provider intake is metadata-level; provider EXECUTION stays denied.
    contract = ensure_contract(job)
    if not evaluate_run_action(contract, ContractAction.PROVIDER_INTAKE).allowed:
        result.trust_status = TrustStatus.REJECTED
        result.next_safe_action = f"remedy contract inspect {request.job_id} --json"
        result.safe_summary = "Contract denies provider intake."
        return result

    # 3. Read input under limits.
    raw_text, input_finding = read_intake_input(input_path=input_path, stdin_text=stdin_text)
    if input_finding is not None:
        result.findings = [input_finding]
        result.trust_status = TrustStatus.REJECTED
        result.next_safe_action = f"remedy provider trust-show {request.job_id} <report_id> --json"
        result.safe_summary = f"Input rejected: {input_finding.code}."
        return result

    # 4. Quarantine raw input privately.
    qrec = store_quarantine(request.job_id, ddir, raw_text, request)
    result.quarantine_id = qrec.quarantine_id

    # 5. Parse candidate (raw_patch kept private).
    candidate, raw_patch, findings = parse_candidate(raw_text)

    # 6. Trust validation.
    findings += scan_secrets(raw_text)
    if raw_patch:
        findings += scan_secrets(raw_patch)
    findings += validate_paths(candidate.target_files)
    findings += validate_patch_shape(candidate, raw_patch)
    link_findings, linked_attempt = validate_failure_link(
        job, candidate, request.failure_artifact_id, request.repair_attempt_id)
    findings += link_findings
    findings = _dedupe_findings(findings)

    decision = decide_trust(candidate, findings)

    # 7. Build the safe report.
    report = ProviderTrustReport(
        report_id=uuid4().hex[:16], job_id=request.job_id, quarantine_id=qrec.quarantine_id,
        provider_name=request.provider_name, model_name=request.model_name,
        failure_artifact_id=request.failure_artifact_id, repair_attempt_id=linked_attempt,
        candidate_kind=candidate.candidate_kind, trust_status=decision.trust_status,
        confidence=decision.confidence, findings=findings, candidate=candidate,
        received_at=_now(),
    )

    # 8. Accepted → create Repair Artifact + pending Patch Intent (still needs approval).
    if decision.trust_status == TrustStatus.ACCEPTED:
        if not evaluate_run_action(contract, ContractAction.CREATE_PROVIDER_REPAIR_INTENT).allowed:
            report.trust_status = TrustStatus.NEEDS_HUMAN_REVIEW
            report.findings.append(_finding(TrustFindingCode.REQUIRES_HUMAN_REVIEW, Severity.MEDIUM,
                                            "Contract denies provider repair intent creation."))
        else:
            art_id, intent_id = _create_repair_artifact_and_intent(job, report, candidate, request)
            if intent_id:
                report.repair_artifact_id = art_id
                report.repair_intent_id = intent_id
                report.next_safe_action = f"remedy patch approve {request.job_id} {intent_id} --json"
            else:
                report.trust_status = TrustStatus.NEEDS_HUMAN_REVIEW
                report.findings.append(_finding(TrustFindingCode.REQUIRES_HUMAN_REVIEW, Severity.MEDIUM,
                                                "Patch intent could not be created — manual review."))

    if not report.next_safe_action:
        report.next_safe_action = (
            f"remedy provider trust-show {request.job_id} {report.report_id} --json")
    report.safe_summary = (
        f"Provider intake: trust={report.trust_status}, kind={report.candidate_kind}, "
        f"{len(report.findings)} finding(s), confidence={report.confidence}.")

    # 9. Persist the safe report (raw stays in quarantine only).
    save_trust_report(job, report)
    save_job(job, root=ddir)

    result.trust_report_id = report.report_id
    result.trust_status = report.trust_status
    result.candidate_kind = report.candidate_kind
    result.confidence = report.confidence
    result.findings = report.findings
    result.repair_artifact_id = report.repair_artifact_id
    result.repair_intent_id = report.repair_intent_id
    result.next_safe_action = report.next_safe_action
    result.safe_summary = report.safe_summary
    return result
