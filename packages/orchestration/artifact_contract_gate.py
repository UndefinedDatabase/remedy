"""Artifact contract gate — verify required evidence artifacts exist.

Deterministic, read-only orchestration logic: no provider calls, no target-repo
mutation, no job state mutation. Given the same evidence directory, the same gate
is produced every time.

The gate checks that every required (core) artifact exists in the evidence
directory, records which optional artifacts are present (informational), and
cross-checks the ``final_verifier_report.json`` ``evidence_completeness`` map for
references it names as missing. Missing references that are job-level gates
(``CRITICAL_FV_REFERENCES``) are blocking; the rest are advisory. The evidence
``job_id`` (from ``manifest.json``) is also checked for freshness against the
current job id when one is supplied.

Public API:
    build_artifact_contract_gate(evidence_dir, required_artifacts=None, current_job_id=None) -> dict
    write_artifact_contract_gate(evidence_dir, written, required_artifacts=None, current_job_id=None) -> None
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0.0"

CORE_ARTIFACTS = (
    "manifest.json",
    "job_report.json",
    "token_truth.json",
    "fresh_evidence_gate.json",
    "artifact_contract_gate.json",
    "runtime_integration_gate.json",
    "change_provenance_gate.json",
    "commit_execution_gate.json",
    "final_verifier_report.json",
)

OPTIONAL_ARTIFACTS = (
    "scratch_file_guard.json",
    "prompt_trace_summary.json",
)

CRITICAL_FV_REFERENCES = frozenset({
    "token_truth",
    "fresh_evidence_gate",
    "artifact_contract_gate",
    "runtime_integration_gate",
    "commit_execution_gate",
    "change_provenance_gate",
    "safe_diff",
    "review_json",
    "tests_txt",
})


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def build_artifact_contract_gate(
    evidence_dir: str,
    required_artifacts: list[str] | None = None,
    current_job_id: str | None = None,
) -> dict[str, Any]:
    """Check that all required artifacts exist in ``evidence_dir``.

    ``required_artifacts`` overrides ``CORE_ARTIFACTS`` when provided. Reads the
    final verifier report's ``evidence_completeness`` map to surface references it
    names as missing, and checks the evidence ``job_id`` (from ``manifest.json``)
    against ``current_job_id`` when supplied. Never mutates any file.
    """
    base = Path(evidence_dir) if evidence_dir else Path(".")
    required = list(required_artifacts) if required_artifacts is not None else list(CORE_ARTIFACTS)

    required_present: dict[str, bool] = {
        name: (base / name).exists() for name in required
    }
    missing_required = [name for name, present in required_present.items() if not present]

    optional_present: dict[str, bool] = {
        name: (base / name).exists() for name in OPTIONAL_ARTIFACTS
    }

    fv = _read_json(base / "final_verifier_report.json")
    completeness = {}
    if fv and isinstance(fv.get("evidence_completeness"), dict):
        completeness = fv["evidence_completeness"]
    fv_referenced_missing = sorted(
        name for name, present in completeness.items() if not present
    )
    critical_fv_missing = sorted(
        name for name in fv_referenced_missing if name in CRITICAL_FV_REFERENCES
    )

    manifest = _read_json(base / "manifest.json")
    evidence_job_id = ""
    if manifest and manifest.get("job_id"):
        evidence_job_id = str(manifest.get("job_id") or "")
    # A stale job_id is a present-but-different id; a missing id is not a mismatch.
    stale_job_id = bool(current_job_id) and bool(evidence_job_id) and evidence_job_id != current_job_id
    job_id_fresh = (not current_job_id) or (not evidence_job_id) or (evidence_job_id == current_job_id)

    issues: list[str] = []
    for name in missing_required:
        issues.append(f"required artifact {name!r} is missing")
    for name in critical_fv_missing:
        issues.append(f"final verifier references missing critical gate {name!r}")
    if stale_job_id:
        issues.append(
            f"evidence job_id {evidence_job_id!r} does not match "
            f"current job_id {current_job_id!r}"
        )

    verdict = "BLOCKED" if (missing_required or critical_fv_missing or stale_job_id) else "PASS"

    return {
        "schema_version": SCHEMA_VERSION,
        "verdict": verdict,
        "required_artifacts": required_present,
        "optional_artifacts": optional_present,
        "missing_required": missing_required,
        "fv_referenced_missing": fv_referenced_missing,
        "critical_fv_missing": critical_fv_missing,
        "evidence_job_id": evidence_job_id,
        "job_id_fresh": job_id_fresh,
        "issues": issues,
    }


def write_artifact_contract_gate(
    evidence_dir: str,
    written: dict[str, str],
    required_artifacts: list[str] | None = None,
    current_job_id: str | None = None,
) -> None:
    """Build and write ``artifact_contract_gate.json`` into ``evidence_dir``.

    Registers the written path in ``written`` when provided. No-op when
    ``evidence_dir`` is empty.
    """
    if not evidence_dir:
        return

    gate = build_artifact_contract_gate(evidence_dir, required_artifacts, current_job_id)

    out_dir = Path(evidence_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "artifact_contract_gate.json"
    json_path.write_text(json.dumps(gate, indent=2) + "\n", encoding="utf-8")

    if written is not None:
        written["artifact_contract_gate.json"] = str(json_path)
