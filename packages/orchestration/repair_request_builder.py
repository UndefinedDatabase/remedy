"""
Provider-Agnostic Repair Request Builder v0 (Steps 1365-1398).

Given a TestFailureArtifact, produce a SAFE, structured request package that can be
handed to ANY external worker / model / human — Remedy stays provider-, worker-,
model-, subscription-, IDE-, and account-AGNOSTIC. The external actor produces a
candidate repair OUTSIDE Remedy; that output re-enters ONLY through the existing
path:

    remedy provider intake-repair <job> --failure-artifact-id <id> --input <file> --provider <label>
      → Trust Gate → Patch Materialization → Approval → remedy do continue

This module never calls a provider/model/network/subprocess/browser/IDE, never
applies, never creates a Patch Intent, and never calls provider intake itself. It
only prepares a safe request package + records an offline candidate-generator record.

A candidate-generator adapter BOUNDARY is defined here as an interface only: the
manual/offline adapter's ``execute()`` raises ``CandidateGeneratorExecutionUnavailable``.

Public API::

    build_repair_request_package(job_id, failure_artifact_id, ...) -> RepairRequestBuildResult
    load_request_packages(job) -> dict[str, dict]
    get_request_package(job, request_package_id) -> dict | None
    render_request_markdown(package) -> str
    export_build_result_json(result) -> dict
    ManualCandidateGeneratorAdapter
    CandidateGeneratorExecutionUnavailable
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4


MAX_REQUEST_BYTES = 256 * 1024
_REQUESTS_META_KEY = "repair_request_packages_v0"
_GENERATORS_META_KEY = "external_candidate_generators_v0"


# ---------------------------------------------------------------------------
# Vocabularies (Step 1366)
# ---------------------------------------------------------------------------


class RepairRequestStopReason:
    READY = "ready"
    JOB_NOT_FOUND = "job_not_found"
    FAILURE_NOT_FOUND = "failure_not_found"
    CONTEXT_BLOCKED = "context_blocked"
    CONTRACT_BLOCKED = "contract_blocked"


class CandidateGeneratorCapability:
    """Execution capability of a candidate generator. v0 is manual/offline only."""

    MANUAL = "manual"
    UNAVAILABLE = "unavailable"
    FUTURE = "future"


# ---------------------------------------------------------------------------
# Models (Step 1366) — no raw source/output/diff fields.
# ---------------------------------------------------------------------------


@dataclass
class RepairRequestSection:
    title: str
    body: str

    def to_dict(self) -> dict[str, Any]:
        return {"title": self.title, "body": self.body}


@dataclass
class CandidateGeneratorDescriptor:
    label: str
    execution_mode: str = CandidateGeneratorCapability.MANUAL
    supports_execution: bool = False
    description: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"label": self.label, "execution_mode": self.execution_mode,
                "supports_execution": self.supports_execution, "description": self.description}


@dataclass
class ExternalCandidateGeneratorRecord:
    generator_record_id: str
    generator_label: str
    job_id: str
    failure_artifact_id: str = ""
    request_package_id: str = ""
    status: str = "repair_request_prepared"
    created_at: str = ""
    execution_mode: str = CandidateGeneratorCapability.MANUAL
    trust_report_id: str = ""
    intake_result_id: str = ""
    evidence_status: str = "complete"

    def to_dict(self) -> dict[str, Any]:
        return {
            "generator_record_id": self.generator_record_id,
            "generator_label": self.generator_label, "job_id": self.job_id,
            "failure_artifact_id": self.failure_artifact_id,
            "request_package_id": self.request_package_id, "status": self.status,
            "created_at": self.created_at, "execution_mode": self.execution_mode,
            "trust_report_id": self.trust_report_id, "intake_result_id": self.intake_result_id,
            "evidence_status": self.evidence_status,
        }


@dataclass
class RepairRequestPackage:
    request_package_id: str
    job_id: str
    failure_artifact_id: str = ""
    repair_attempt_id: str = ""
    test_run_id: str = ""
    apply_id: str = ""
    intent_id: str = ""
    task_id: str = ""
    target_kind: str = "external"
    model_hint: str = ""
    generator_label: str = "external"
    failure_kind: str = ""
    sections: list[RepairRequestSection] = field(default_factory=list)
    output_intake_command: str = ""
    trust_gate_command: str = ""
    content_sha256: str = ""
    created_at: str = ""
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_package_id": self.request_package_id, "job_id": self.job_id,
            "failure_artifact_id": self.failure_artifact_id,
            "repair_attempt_id": self.repair_attempt_id, "test_run_id": self.test_run_id,
            "apply_id": self.apply_id, "intent_id": self.intent_id, "task_id": self.task_id,
            "target_kind": self.target_kind, "model_hint": self.model_hint,
            "generator_label": self.generator_label, "failure_kind": self.failure_kind,
            "sections": [s.to_dict() for s in self.sections],
            "output_intake_command": self.output_intake_command,
            "trust_gate_command": self.trust_gate_command,
            "content_sha256": self.content_sha256, "created_at": self.created_at,
            "warnings": self.warnings,
        }


@dataclass
class RepairRequestBuildResult:
    job_id: str
    failure_artifact_id: str = ""
    repair_attempt_id: str = ""
    request_package_id: str = ""
    request_file_id: str = ""
    generator_record_id: str = ""
    target_kind: str = "external"
    model_hint: str = ""
    generator_label: str = "external"
    stop_reason: str = RepairRequestStopReason.READY
    evidence_status: str = "complete"
    output_intake_command: str = ""
    trust_gate_command: str = ""
    next_steps: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    safe_summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "job_id": self.job_id, "failure_artifact_id": self.failure_artifact_id,
            "repair_attempt_id": self.repair_attempt_id,
            "request_package_id": self.request_package_id,
            "request_file_id": self.request_file_id,
            "generator_record_id": self.generator_record_id,
            "target_kind": self.target_kind, "model_hint": self.model_hint,
            "generator_label": self.generator_label, "stop_reason": self.stop_reason,
            "evidence_status": self.evidence_status,
            "output_intake_command": self.output_intake_command,
            "trust_gate_command": self.trust_gate_command,
            "next_steps": self.next_steps, "warnings": self.warnings,
            "safe_summary": self.safe_summary,
        }


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _scrub(text: str) -> str:
    """Scrub secret-like / absolute-path / traceback material from any text that
    will be shared with an untrusted external actor (defense-in-depth)."""
    from packages.orchestration.provider_trust import _scrub_public
    return _scrub_public(str(text))


# ---------------------------------------------------------------------------
# Candidate output schema + request templates (Steps 1368/1387)
# ---------------------------------------------------------------------------

CANDIDATE_OUTPUT_SCHEMA = {
    "summary": "<one-line safe summary>",
    "target_files": ["relative/path.md"],
    "patch_format": "unified_diff",
    "unified_diff": "<a single unified diff>",
    "rationale": "<why this fixes the failure>",
    "risk_notes": "<risks/uncertainty>",
}


# Target-kind templates (Step 1387) — extra constraint lines, NOT execution.
_TEMPLATES: dict[str, list[str]] = {
    "external": [
        "Return exactly ONE candidate repair (no alternatives).",
        "Prefer the smallest safe change that addresses the failure.",
    ],
    "docs_only": [
        "Only documentation (.md) changes are accepted by this request.",
        "Do not modify source or test files.",
    ],
    "test_failure": [
        "Target the documented cause of the test failure.",
        "Do not weaken or delete tests to make them pass.",
    ],
    "markdown_only": [
        "v0 can only apply a SINGLE Markdown (.md) create or modify automatically.",
        "Non-.md changes will be accepted-but-not-materialized (no auto-apply).",
    ],
}


def request_template_labels() -> list[str]:
    return sorted(_TEMPLATES.keys())


def _template_lines(target_kind: str) -> list[str]:
    return _TEMPLATES.get(target_kind, _TEMPLATES["external"])


# ---------------------------------------------------------------------------
# Private storage (Step 1369)
# ---------------------------------------------------------------------------


def _request_root(job_id: str, data_dir: Path) -> Path:
    return data_dir / "workspaces" / job_id / "repair_request_packages"


def _request_dir(job_id: str, rpid: str, data_dir: Path) -> Path:
    return _request_root(job_id, data_dir) / rpid


def _atomic_write(path: Path, data: bytes, mode: int = 0o600) -> bool:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
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


def store_request_package(job_id: str, data_dir: Path, package: RepairRequestPackage,
                          rendered: str) -> bool:
    """Persist the request package privately (workspace-local). The text is safe-to-
    share but still stored under the job workspace. Atomic, hashed, no overwrite."""
    rdir = _request_dir(job_id, package.request_package_id, data_dir)
    encoded = rendered.encode("utf-8", errors="replace")
    if len(encoded) > MAX_REQUEST_BYTES:
        return False
    try:
        rdir.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(rdir, 0o700)
        except OSError:
            pass
    except OSError:
        return False
    ok = _atomic_write(rdir / "request.md", encoded)
    ok = _atomic_write(rdir / "request_manifest.json",
                       json.dumps(package.to_dict(), indent=2, sort_keys=True).encode("utf-8")) and ok
    ok = _atomic_write(rdir / "manifest.sha256", package.content_sha256.encode("utf-8")) and ok
    return ok


def save_request_package(job: Any, package: RepairRequestPackage) -> None:
    store = job.metadata.setdefault(_REQUESTS_META_KEY, {})
    store[package.request_package_id] = package.to_dict()


def load_request_packages(job: Any) -> dict[str, dict]:
    return dict((job.metadata or {}).get(_REQUESTS_META_KEY, {}))


def get_request_package(job: Any, request_package_id: str) -> dict | None:
    return load_request_packages(job).get(request_package_id)


def load_generator_records(job: Any) -> dict[str, dict]:
    return dict((job.metadata or {}).get(_GENERATORS_META_KEY, {}))


def save_generator_record(job: Any, record: ExternalCandidateGeneratorRecord) -> None:
    store = job.metadata.setdefault(_GENERATORS_META_KEY, {})
    store[record.generator_record_id] = record.to_dict()


def _find_existing_package(job: Any, failure_artifact_id: str, target_kind: str,
                           model_hint: str) -> dict | None:
    for p in load_request_packages(job).values():
        if (p.get("failure_artifact_id") == failure_artifact_id
                and p.get("target_kind") == target_kind
                and (p.get("model_hint") or "") == (model_hint or "")):
            return p
    return None


# ---------------------------------------------------------------------------
# Request sections + render (Steps 1367/1368/1377)
# ---------------------------------------------------------------------------


def _build_sections(ctx: Any, target_kind: str, model_hint: str) -> list[RepairRequestSection]:
    files = ", ".join(_scrub(f) for f in (ctx.changed_files_safe or [])[:10]) or "(none known)"
    schema = json.dumps(CANDIDATE_OUTPUT_SCHEMA, indent=2)
    constraints = [
        "Return EXACTLY ONE candidate repair. No alternatives, no multiple patches.",
        "Use ONLY relative repo paths. No absolute paths, no path traversal.",
        "Do NOT include secrets, tokens, credentials, keys, or .env values.",
        "Do NOT target protected files (.env, .git, node_modules, caches, lock files).",
        "Do NOT claim the change was applied or tested — it was not.",
        "Do NOT include raw stdout/stderr, tracebacks, or unrelated prose.",
    ] + _template_lines(target_kind)
    forbidden = [
        "secrets / tokens / private keys / credentials",
        "absolute or private filesystem paths",
        "raw program output, tracebacks, or logs",
        "multiple candidate patches or alternatives",
        "claims of having applied or run tests",
    ]
    sections = [
        RepairRequestSection("Problem summary", _scrub(ctx.safe_summary or "Test failure to repair.")),
        RepairRequestSection(
            "Test failure",
            f"kind: {_scrub(ctx.failure_kind or 'unknown')}\n"
            f"exit_code: {ctx.exit_code if ctx.exit_code is not None else 'unknown'}\n"
            f"command: {_scrub(ctx.command_display or 'unknown')}"),
        RepairRequestSection(
            "Linked entities",
            f"task_id: {ctx.task_id or 'n/a'}\nfailure_artifact_id: {ctx.failure_artifact_id}\n"
            f"test_run_id: {ctx.test_run_id or 'n/a'}\napply_id: {ctx.apply_id or 'n/a'}\n"
            f"intent_id: {ctx.intent_id or 'n/a'}"),
        RepairRequestSection("Relevant files (names only)", files),
        RepairRequestSection(
            "Proof / snapshot status",
            f"proof_status: {ctx.proof_status}\nsnapshot_status: {ctx.snapshot_status}"),
        RepairRequestSection("Constraints", "\n".join(f"- {c}" for c in constraints)),
        RepairRequestSection(
            "Required response format",
            "Return either:\n"
            "(A) a single JSON object:\n```json\n" + schema + "\n```\n"
            "OR (B) a single fenced unified diff:\n```diff\n<one unified diff>\n```\n"
            "If JSON is used, output JSON only — no prose outside it."),
        RepairRequestSection("Forbidden content", "\n".join(f"- {f}" for f in forbidden)),
        RepairRequestSection(
            "How Remedy will handle your output",
            "Your output is treated as UNTRUSTED. Remedy will quarantine it privately, "
            "validate it (secrets, protected paths, patch shape), and REJECT unsafe "
            "candidates. An accepted candidate becomes a PENDING patch intent that a "
            "human must approve before anything is applied."),
        RepairRequestSection(
            "Model hint (optional, non-binding)",
            _scrub(model_hint) if model_hint else "(none — any capable external actor may respond)"),
    ]
    return sections


def render_request_markdown(package: RepairRequestPackage) -> str:
    lines = [f"# Repair request — failure {package.failure_artifact_id[:8]} "
             f"(job {package.job_id[:8]})", ""]
    lines.append("You are an EXTERNAL candidate generator. Produce a safe repair "
                 "candidate per the contract below. You are untrusted; your output will "
                 "be validated before any use.")
    lines.append("")
    for s in package.sections:
        lines.append(f"## {s.title}")
        lines.append(s.body)
        lines.append("")
    return "\n".join(lines)


def _import_next_steps(job_id: str, failure_artifact_id: str, label: str) -> list[str]:
    return [
        "1. Send this request to any external model / worker / human.",
        "2. Save their candidate response to a local file.",
        f"3. Import it: remedy provider intake-repair {job_id} "
        f"--failure-artifact-id {failure_artifact_id} --input <response_file> "
        f"--provider {label} --json",
        f"4. If needed, inspect the trust report: remedy provider trust-show {job_id} <report_id> --json",
        f"5. If a patch intent is created, approve it: remedy patch approve {job_id} <intent_id> --json",
        f"6. Apply it through the normal path: remedy do continue {job_id} --intent-id <intent_id> --json",
    ]


# ---------------------------------------------------------------------------
# Top-level builder (Step 1367)
# ---------------------------------------------------------------------------


def build_repair_request_package(
    job_id: str,
    failure_artifact_id: str,
    *,
    target_kind: str = "external",
    model_hint: str | None = None,
    generator_label: str | None = None,
    new: bool = False,
    data_dir: Path | None = None,
) -> RepairRequestBuildResult:
    """Build a safe, provider-agnostic repair request package from a FailureArtifact.

    Never calls a provider/network/subprocess, never applies, never creates a Patch
    Intent. Idempotent per (failure, target_kind, model_hint) unless ``new=True``."""
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.storage import load_job, save_job, JobNotFoundError
    from packages.orchestration.run_contract import (
        ensure_contract, evaluate_run_action, ContractAction,
    )
    from packages.orchestration.repair_loop import build_repair_context, find_repair_attempt

    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    label = (generator_label or "external").strip() or "external"
    hint = (model_hint or "").strip()
    result = RepairRequestBuildResult(
        job_id=job_id, failure_artifact_id=failure_artifact_id, target_kind=target_kind,
        model_hint=hint, generator_label=label)

    try:
        job = load_job(UUID(job_id), ddir)
    except (ValueError, JobNotFoundError):
        result.stop_reason = RepairRequestStopReason.JOB_NOT_FOUND
        result.evidence_status = "unknown"
        result.safe_summary = "Job not found."
        return result

    contract = ensure_contract(job)
    if not evaluate_run_action(contract, ContractAction.PREPARE_REPAIR_REQUEST).allowed:
        result.stop_reason = RepairRequestStopReason.CONTRACT_BLOCKED
        result.safe_summary = "Contract denies repair request preparation."
        result.warnings.append("contract_denied")
        return result

    ctx = build_repair_context(job_id, failure_artifact_id, ddir)
    if ctx.status != "context_ready":
        blocker = (ctx.blocker or "").lower()
        result.stop_reason = (RepairRequestStopReason.FAILURE_NOT_FOUND
                              if "not_found" in blocker or "no_failure" in blocker
                              else RepairRequestStopReason.CONTEXT_BLOCKED)
        result.evidence_status = "unknown"
        result.safe_summary = f"Repair context unavailable: {_scrub(ctx.blocker)[:80]}"
        return result

    attempt = find_repair_attempt(job, failure_artifact_id)
    attempt_id = attempt.attempt_id if attempt is not None else ""
    result.repair_attempt_id = attempt_id

    # Idempotency: reuse an existing package unless --new.
    if not new:
        existing = _find_existing_package(job, failure_artifact_id, target_kind, hint)
        if existing is not None:
            result.request_package_id = existing["request_package_id"]
            result.request_file_id = existing["request_package_id"]
            result.output_intake_command = existing.get("output_intake_command", "")
            result.trust_gate_command = existing.get("trust_gate_command", "")
            result.next_steps = _import_next_steps(job_id, failure_artifact_id,
                                                   existing.get("generator_label", label))
            result.safe_summary = "Existing repair request reused (idempotent)."
            return result

    rpid = uuid4().hex[:16]
    intake_cmd = (f"remedy provider intake-repair {job_id} "
                  f"--failure-artifact-id {failure_artifact_id} --input <response_file> "
                  f"--provider {label} --json")
    trust_cmd = f"remedy provider trust-show {job_id} <report_id> --json"
    package = RepairRequestPackage(
        request_package_id=rpid, job_id=job_id, failure_artifact_id=failure_artifact_id,
        repair_attempt_id=attempt_id, test_run_id=ctx.test_run_id, apply_id=ctx.apply_id,
        intent_id=ctx.intent_id, task_id=ctx.task_id, target_kind=target_kind,
        model_hint=hint, generator_label=label, failure_kind=ctx.failure_kind,
        sections=_build_sections(ctx, target_kind, hint),
        output_intake_command=intake_cmd, trust_gate_command=trust_cmd, created_at=_now(),
        warnings=[],
    )
    rendered = render_request_markdown(package)
    package.content_sha256 = hashlib.sha256(rendered.encode("utf-8", errors="replace")).hexdigest()

    if not store_request_package(job_id, ddir, package, rendered):
        result.stop_reason = RepairRequestStopReason.CONTEXT_BLOCKED
        result.evidence_status = "degraded"
        result.safe_summary = "Request package could not be stored."
        result.warnings.append("request_store_failed")
        return result

    save_request_package(job, package)

    grid = uuid4().hex[:16]
    record = ExternalCandidateGeneratorRecord(
        generator_record_id=grid, generator_label=label, job_id=job_id,
        failure_artifact_id=failure_artifact_id, request_package_id=rpid,
        status="repair_request_prepared", created_at=_now(),
        execution_mode=CandidateGeneratorCapability.MANUAL,
    )
    save_generator_record(job, record)
    save_job(job, root=ddir)

    result.request_package_id = rpid
    result.request_file_id = rpid
    result.generator_record_id = grid
    result.output_intake_command = intake_cmd
    result.trust_gate_command = trust_cmd
    result.next_steps = _import_next_steps(job_id, failure_artifact_id, label)
    result.safe_summary = (
        f"Repair request prepared ({target_kind}); hand to an external actor, then "
        f"import the response via provider intake-repair.")
    return result


def export_build_result_json(result: RepairRequestBuildResult) -> dict[str, Any]:
    return result.to_dict()


# ---------------------------------------------------------------------------
# Candidate generator adapter boundary (Steps 1374-1375) — interface only.
# ---------------------------------------------------------------------------


class CandidateGeneratorExecutionUnavailable(RuntimeError):
    """Raised when an adapter cannot execute a generator in-process. v0 is offline:
    candidate output must be produced externally and imported via provider intake."""


class CandidateGeneratorAdapter:
    """Boundary for FUTURE automated candidate generators. v0 has NO executing
    implementation — execute() must raise. No network/SDK/subprocess/browser here."""

    label: str = "external"
    execution_mode: str = CandidateGeneratorCapability.MANUAL

    def describe(self) -> CandidateGeneratorDescriptor:
        raise NotImplementedError

    def build_request(self, job_id: str, failure_artifact_id: str, **kwargs: Any) -> RepairRequestBuildResult:
        raise NotImplementedError

    def supports_execution(self) -> bool:
        return False

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        raise CandidateGeneratorExecutionUnavailable(
            "Automated candidate generation is not available in v0; produce the "
            "candidate externally and import it via 'remedy provider intake-repair'.")


class ManualCandidateGeneratorAdapter(CandidateGeneratorAdapter):
    """The only adapter in v0: offline/manual. Builds a request package; never executes."""

    def __init__(self, label: str = "external") -> None:
        self.label = label or "external"
        self.execution_mode = CandidateGeneratorCapability.MANUAL

    def describe(self) -> CandidateGeneratorDescriptor:
        return CandidateGeneratorDescriptor(
            label=self.label, execution_mode=CandidateGeneratorCapability.MANUAL,
            supports_execution=False,
            description="Manual/offline: produces a safe request package; the human "
                        "relays it to any external actor and imports the response.")

    def build_request(self, job_id: str, failure_artifact_id: str, **kwargs: Any) -> RepairRequestBuildResult:
        return build_repair_request_package(
            job_id, failure_artifact_id, generator_label=self.label, **kwargs)

    def supports_execution(self) -> bool:
        return False
