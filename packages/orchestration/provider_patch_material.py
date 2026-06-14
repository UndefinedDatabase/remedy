"""
Trusted Provider Patch Materialization v0 (Steps 1335-1364).

Turns an ACCEPTED ProviderTrustReport candidate into a REAL, applyable pending
Repair Patch Intent — one that flows through the existing approval-gated path:

    approval → remedy do continue <job> --intent-id <id> → snapshot → apply → test → proof

while the raw provider diff/source stays in **private** workspace storage only.

Apply-path reality: ``apply_patch_intent`` is ``.md``-only (create writes a markdown
file from a "Proposed Changes:" section; modify appends one). So a materialized
intent is genuinely apply-compatible ONLY for a single ``.md`` target with
create/modify semantics. Anything else (source files, multiple files, delete,
rename, binary) is reported as ``unsupported_patch_shape`` and NO intent is created.

Hard rules: no provider execution, no network, no subprocess, no auto-apply, no
auto-approval. Raw diff never leaves the private material dir. Public surfaces carry
safe metadata (counts/IDs/state) only. accepted ≠ materialized ≠ applied ≠ verified.

Public API::

    materialize_accepted_candidate(job, report, candidate, raw_patch, request, data_dir) -> ProviderPatchMaterializationResult
    verify_provider_patch_material(job_id, material_id, data_dir=None) -> ProviderPatchMaterialVerification
    load_materials(job) -> dict[str, dict]
    get_material(job, material_id) -> dict | None
    export_materialization_result_json(result) -> dict
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

from packages.orchestration.provider_trust import (
    Severity, TrustStatus, _safe_path_label, _scrub_public, validate_paths,
)


# ---------------------------------------------------------------------------
# Limits (mirror the trust gate; materialization stays conservative)
# ---------------------------------------------------------------------------

MAX_MATERIAL_LINES = 2000
MAX_MATERIAL_BYTES = 256 * 1024


class MaterialState:
    MATERIALIZED = "materialized"
    UNSUPPORTED = "unsupported_patch_shape"
    FAILED = "materialization_failed"
    REVOKED = "revoked"


# ---------------------------------------------------------------------------
# Models (Step 1336) — no raw diff/source in any public field.
# ---------------------------------------------------------------------------


@dataclass
class ProviderPatchMaterialEntry:
    target_path: str
    action: str            # create | modify
    line_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {"target_path": _safe_path_label(self.target_path),
                "action": self.action, "line_count": self.line_count}


@dataclass
class ProviderPatchMaterial:
    material_id: str
    job_id: str
    quarantine_id: str = ""
    trust_report_id: str = ""
    failure_artifact_id: str = ""
    repair_attempt_id: str = ""
    candidate_hash: str = ""
    patch_format: str = ""
    target_path_count: int = 0
    operation_count: int = 0
    total_line_count: int = 0
    material_state: str = MaterialState.MATERIALIZED
    verified: bool = False
    linked_intent_id: str = ""
    repair_artifact_id: str = ""
    evidence_status: str = "complete"
    entries: list[ProviderPatchMaterialEntry] = field(default_factory=list)
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "material_id": self.material_id, "job_id": self.job_id,
            "quarantine_id": self.quarantine_id, "trust_report_id": self.trust_report_id,
            "failure_artifact_id": self.failure_artifact_id,
            "repair_attempt_id": self.repair_attempt_id,
            "candidate_hash": self.candidate_hash, "patch_format": self.patch_format,
            "target_path_count": self.target_path_count,
            "operation_count": self.operation_count,
            "total_line_count": self.total_line_count,
            "material_state": self.material_state, "verified": self.verified,
            "linked_intent_id": self.linked_intent_id,
            "repair_artifact_id": self.repair_artifact_id,
            "evidence_status": self.evidence_status,
            "entries": [e.to_dict() for e in self.entries],
            "created_at": self.created_at,
        }


@dataclass
class ProviderPatchIntentLink:
    intent_id: str = ""
    material_id: str = ""
    trust_report_id: str = ""
    quarantine_id: str = ""
    failure_artifact_id: str = ""
    repair_attempt_id: str = ""
    repair_artifact_id: str = ""


@dataclass
class ProviderPatchMaterializationResult:
    job_id: str
    material_id: str = ""
    state: str = MaterialState.UNSUPPORTED
    linked_intent_id: str = ""
    repair_artifact_id: str = ""
    target_path_count: int = 0
    operation_count: int = 0
    reason: str = ""
    safe_summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "job_id": self.job_id, "material_id": self.material_id, "state": self.state,
            "linked_intent_id": self.linked_intent_id,
            "repair_artifact_id": self.repair_artifact_id,
            "target_path_count": self.target_path_count,
            "operation_count": self.operation_count,
            "reason": self.reason, "safe_summary": self.safe_summary,
        }


@dataclass
class ProviderPatchMaterialVerification:
    material_id: str
    ok: bool = False
    reason: str = ""
    checks: dict[str, bool] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {"material_id": self.material_id, "ok": self.ok,
                "reason": self.reason, "checks": self.checks}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


_MATERIALS_META_KEY = "provider_patch_materials_v0"


# ---------------------------------------------------------------------------
# Private material storage (Step 1337)
# ---------------------------------------------------------------------------


def _material_root(job_id: str, data_dir: Path) -> Path:
    return data_dir / "workspaces" / job_id / "provider_patch_material"


def _material_dir(job_id: str, material_id: str, data_dir: Path) -> Path:
    return _material_root(job_id, data_dir) / material_id


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


def store_material(job_id: str, data_dir: Path, material: ProviderPatchMaterial,
                   raw_patch: str) -> bool:
    """Persist raw patch material privately. Returns True if stored. The raw diff
    lives ONLY here (0o600); the manifest carries safe metadata + a content hash."""
    mdir = _material_dir(job_id, material.material_id, data_dir)
    encoded = raw_patch.encode("utf-8", errors="replace")
    if len(encoded) > MAX_MATERIAL_BYTES:
        return False
    sha = hashlib.sha256(encoded).hexdigest()
    try:
        mdir.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(mdir, 0o700)
        except OSError:
            pass
    except OSError:
        return False
    if not _atomic_write(mdir / "patch.diff", encoded):
        return False
    if not _atomic_write(mdir / "manifest.sha256", sha.encode("utf-8")):
        return False
    if not _atomic_write(mdir / "material.json",
                         json.dumps(material.to_dict(), indent=2, sort_keys=True).encode("utf-8")):
        return False
    return True


def _read_material_patch(job_id: str, material_id: str, data_dir: Path) -> str:
    """PRIVATE: read the raw patch material. Never call from a public export path."""
    p = _material_dir(job_id, material_id, data_dir) / "patch.diff"
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def load_material_manifest(job_id: str, material_id: str, data_dir: Path) -> dict | None:
    p = _material_dir(job_id, material_id, data_dir) / "material.json"
    try:
        return json.loads(p.read_bytes())
    except (OSError, json.JSONDecodeError):
        return None


def save_material(job: Any, material: ProviderPatchMaterial) -> None:
    """Persist a SAFE material manifest in job metadata. Caller persists the job."""
    store = job.metadata.setdefault(_MATERIALS_META_KEY, {})
    store[material.material_id] = material.to_dict()


def load_materials(job: Any) -> dict[str, dict]:
    return dict((job.metadata or {}).get(_MATERIALS_META_KEY, {}))


def get_material(job: Any, material_id: str) -> dict | None:
    return load_materials(job).get(material_id)


def _find_material_by_hash(job: Any, candidate_hash: str) -> dict | None:
    for m in load_materials(job).values():
        if m.get("candidate_hash") == candidate_hash:
            return m
    return None


# ---------------------------------------------------------------------------
# Conversion (Steps 1339-1340) — conservative, single .md target only.
# ---------------------------------------------------------------------------


@dataclass
class _Extracted:
    ok: bool
    reason: str = ""
    target_path: str = ""
    action: str = "modify"          # create | modify
    added_lines: list[str] = field(default_factory=list)


def _is_md(path: str) -> bool:
    return path.lower().endswith(".md")


def materialize_unified_diff_to_structured_patch(raw_patch: str) -> _Extracted:
    """Conservative unified-diff conversion (Step 1339). v0: exactly one ``.md``
    target, create or modify, no delete/rename/binary/mode-change."""
    if "GIT binary patch" in raw_patch or re.search(r"^Binary files ", raw_patch, re.MULTILINE):
        return _Extracted(False, "binary_patch")
    if re.search(r"^rename (from|to) ", raw_patch, re.MULTILINE):
        return _Extracted(False, "rename_unsupported")
    if re.search(r"^deleted file mode", raw_patch, re.MULTILINE) or "+++ /dev/null" in raw_patch:
        return _Extracted(False, "delete_unsupported")

    minus = [ln[4:].strip().split("\t")[0] for ln in raw_patch.splitlines() if ln.startswith("--- ")]
    plus = [ln[4:].strip().split("\t")[0] for ln in raw_patch.splitlines() if ln.startswith("+++ ")]
    targets: list[str] = []
    for p in plus:
        path = p[2:] if p.startswith(("a/", "b/")) else p
        if path and path != "/dev/null" and path not in targets:
            targets.append(path)
    if len(targets) != 1:
        return _Extracted(False, "not_single_target")
    target = targets[0]
    if not _is_md(target):
        return _Extracted(False, "non_markdown_target")

    is_create = any(m.strip() in ("/dev/null", "a//dev/null") for m in minus) or \
        re.search(r"^new file mode", raw_patch, re.MULTILINE) is not None
    added: list[str] = []
    for ln in raw_patch.splitlines():
        if ln.startswith("+++"):
            continue
        if ln.startswith("+"):
            added.append(ln[1:])
    if not added:
        return _Extracted(False, "no_added_lines")
    if len(added) > MAX_MATERIAL_LINES:
        return _Extracted(False, "too_many_lines")
    return _Extracted(True, "", target, "create" if is_create else "modify", added)


def materialize_structured_operations(ops: list[dict]) -> _Extracted:
    """Conservative structured-operations conversion (Step 1340). v0: exactly one
    ``.md`` create/modify op with bounded line content."""
    if not isinstance(ops, list) or len(ops) != 1:
        return _Extracted(False, "not_single_operation")
    op = ops[0]
    if not isinstance(op, dict):
        return _Extracted(False, "bad_operation")
    path = str(op.get("path", ""))
    kind = str(op.get("op", op.get("action", ""))).lower()
    if kind not in ("create", "modify"):
        return _Extracted(False, f"unsupported_operation:{kind or 'none'}")
    if not path or not _is_md(path):
        return _Extracted(False, "non_markdown_target")
    content = op.get("content")
    if isinstance(content, list):
        lines = [str(x) for x in content]
    elif isinstance(content, str):
        lines = content.splitlines()
    else:
        return _Extracted(False, "no_content")
    if not lines:
        return _Extracted(False, "no_added_lines")
    if len(lines) > MAX_MATERIAL_LINES:
        return _Extracted(False, "too_many_lines")
    return _Extracted(True, "", path, kind, lines)


# ---------------------------------------------------------------------------
# Applyable artifact builder (Step 1341) — emits the format apply_patch_intent reads.
# ---------------------------------------------------------------------------


def _build_apply_artifact_content(summary: str, added_lines: list[str]) -> str:
    """Build artifact content in the builder format `apply_patch_intent` extracts:
    a "Proposed Changes:" section with `  - <line>` entries. Lines are scrubbed
    (defense-in-depth — accepted candidates already passed secret scanning)."""
    safe_lines = [_scrub_public(ln) for ln in added_lines[:MAX_MATERIAL_LINES]]
    body = "\n".join(f"  - {ln}" for ln in safe_lines)
    return f"Summary:\n{_scrub_public(summary)[:200]}\nProposed Changes:\n{body}\n"


# ---------------------------------------------------------------------------
# Materialize (Step 1341) — accepted candidate → applyable pending intent.
# ---------------------------------------------------------------------------


def materialize_accepted_candidate(
    job: Any, report: Any, candidate: Any, raw_patch: str, request: Any, data_dir: Path,
) -> ProviderPatchMaterializationResult:
    """Materialize an ACCEPTED candidate into a real pending Repair Patch Intent.

    Idempotent by candidate hash. Supported shapes (single .md create/modify) yield
    an applyable intent; everything else returns ``unsupported_patch_shape`` with no
    intent. Never applies, never approves, never executes a provider."""
    from packages.core.models import Artifact, ArtifactKind
    from packages.orchestration.approval_queue import get_patch_intent, make_intent_id

    result = ProviderPatchMaterializationResult(job_id=str(job.id))
    candidate_hash = hashlib.sha256(raw_patch.encode("utf-8", errors="replace")).hexdigest()

    # Idempotency: same candidate hash → return the existing material/intent.
    existing = _find_material_by_hash(job, candidate_hash)
    if existing is not None:
        result.material_id = existing.get("material_id", "")
        result.state = existing.get("material_state", MaterialState.MATERIALIZED)
        result.linked_intent_id = existing.get("linked_intent_id", "")
        result.repair_artifact_id = existing.get("repair_artifact_id", "")
        result.target_path_count = existing.get("target_path_count", 0)
        result.operation_count = existing.get("operation_count", 0)
        result.safe_summary = "Existing material reused (idempotent)."
        return result

    # Convert per format.
    if candidate.patch_format == "unified_diff":
        ext = materialize_unified_diff_to_structured_patch(raw_patch)
    elif candidate.patch_format == "structured_operations":
        try:
            ops = json.loads(raw_patch)
        except (json.JSONDecodeError, ValueError):
            ops = []
        ext = materialize_structured_operations(ops if isinstance(ops, list) else [])
    else:
        ext = _Extracted(False, "unsupported_format")

    if not ext.ok:
        result.state = MaterialState.UNSUPPORTED
        result.reason = ext.reason
        result.safe_summary = f"Candidate accepted but not materializable: {ext.reason}."
        return result

    material_id = uuid4().hex[:16]
    entry = ProviderPatchMaterialEntry(target_path=ext.target_path, action=ext.action,
                                       line_count=len(ext.added_lines))
    material = ProviderPatchMaterial(
        material_id=material_id, job_id=str(job.id), quarantine_id=report.quarantine_id,
        trust_report_id=report.report_id, failure_artifact_id=report.failure_artifact_id,
        repair_attempt_id=report.repair_attempt_id, candidate_hash=candidate_hash,
        patch_format=candidate.patch_format, target_path_count=1, operation_count=1,
        total_line_count=len(ext.added_lines), material_state=MaterialState.MATERIALIZED,
        entries=[entry], created_at=_now(),
    )

    if not store_material(str(job.id), data_dir, material, raw_patch):
        result.state = MaterialState.FAILED
        result.reason = "material_store_failed"
        result.safe_summary = "Patch material could not be stored privately."
        return result

    # Build the applyable repair artifact (.md create/modify via existing apply path).
    art = Artifact(
        name=f"provider-material-{material_id[:8]}",
        content=_build_apply_artifact_content(getattr(candidate, "summary", ""), ext.added_lines),
        kind=ArtifactKind.BUILDER_PROPOSAL,
        task_id=None,
        metadata={
            "provider_repair_v0": True,
            "provider_material_v0": True,
            "kind": "provider_repair",
            "material_id": material_id,
            "provider_trust_report_id": report.report_id,
            "quarantine_id": report.quarantine_id,
            "failure_artifact_id": report.failure_artifact_id,
            "repair_attempt_id": report.repair_attempt_id,
            "provider_name": getattr(request, "provider_name", ""),
            "model_name": getattr(request, "model_name", ""),
            "patch_format": candidate.patch_format,
            "candidate_hash": candidate_hash,
            "safe_summary": f"Provider repair materialized ({ext.action} {_safe_path_label(ext.target_path)}); pending approval.",
            "patch_intent_explanations": [
                {
                    "file": ext.target_path,
                    "action": ext.action,
                    "risk": "medium",
                    "reason": f"Provider-sourced repair (trust-gated, materialized) for "
                              f"failure {report.failure_artifact_id[:8] or 'n/a'}.",
                    "summary": f"Provider repair: {_scrub_public(getattr(candidate, 'summary', ''))[:100]}",
                },
            ],
            "patch_intent_approvals": {},
        },
    )
    job.artifacts.append(art)
    intent_id = make_intent_id(art.id, 0)
    if get_patch_intent(job, intent_id) is None:
        material.material_state = MaterialState.FAILED
        save_material(job, material)
        result.state = MaterialState.FAILED
        result.reason = "intent_not_resolvable"
        result.safe_summary = "Materialized intent could not be verified."
        return result

    material.linked_intent_id = intent_id
    material.repair_artifact_id = str(art.id)
    save_material(job, material)

    result.material_id = material_id
    result.state = MaterialState.MATERIALIZED
    result.linked_intent_id = intent_id
    result.repair_artifact_id = str(art.id)
    result.target_path_count = 1
    result.operation_count = 1
    result.safe_summary = (
        f"Materialized provider repair ({ext.action} {_safe_path_label(ext.target_path)}); "
        f"pending approval.")
    return result


# ---------------------------------------------------------------------------
# Verification (Step 1338)
# ---------------------------------------------------------------------------


def verify_provider_patch_material(
    job_id: str, material_id: str, data_dir: Path | None = None,
) -> ProviderPatchMaterialVerification:
    """Verify private patch material against its manifest + trust report. Safe."""
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.storage import load_job, JobNotFoundError
    from packages.orchestration.provider_trust import get_trust_report

    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    v = ProviderPatchMaterialVerification(material_id=material_id)
    checks: dict[str, bool] = {}

    mdir = _material_dir(job_id, material_id, ddir)
    manifest = load_material_manifest(job_id, material_id, ddir)
    checks["manifest_exists"] = manifest is not None
    patch_path = mdir / "patch.diff"
    checks["patch_exists"] = patch_path.exists()
    sha_path = mdir / "manifest.sha256"

    if not (checks["manifest_exists"] and checks["patch_exists"] and sha_path.exists()):
        v.checks = checks
        v.reason = "material_files_missing"
        return v

    try:
        stored_sha = sha_path.read_text(encoding="utf-8").strip()
        actual_sha = hashlib.sha256(patch_path.read_bytes()).hexdigest()
        checks["hash_matches"] = (stored_sha == actual_sha)
    except OSError:
        checks["hash_matches"] = False

    checks["not_revoked"] = manifest.get("material_state") != MaterialState.REVOKED
    checks["single_candidate"] = manifest.get("target_path_count", 0) == 1

    # Target paths still safe.
    targets = [e.get("target_path", "") for e in manifest.get("entries", [])]
    checks["paths_safe"] = not any(
        f.severity in (Severity.BLOCKER, Severity.HIGH) for f in validate_paths(targets))

    # Trust report exists + accepted/materialized.
    report_ok = False
    try:
        job = load_job(UUID(job_id), ddir)
        rep = get_trust_report(job, manifest.get("trust_report_id", ""))
        report_ok = rep is not None and rep.get("trust_status") in (
            TrustStatus.ACCEPTED, "materialized", "intent_pending_approval")
    except (ValueError, JobNotFoundError):
        report_ok = False
    checks["trust_report_accepted"] = report_ok

    v.checks = checks
    v.ok = all(checks.values())
    v.reason = "" if v.ok else "verification_failed:" + ",".join(k for k, ok in checks.items() if not ok)
    return v


def export_materialization_result_json(result: ProviderPatchMaterializationResult) -> dict[str, Any]:
    return result.to_dict()
