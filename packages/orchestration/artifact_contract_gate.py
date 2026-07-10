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

When a task ran with ``--stream-evidence``, the F004 raw stream artifacts it
references must be present in the bundle; without the flag they are not
applicable and never block. Only the current bundle is scanned, so history
bundles staged alongside it cannot influence this verdict.

Public API:
    build_artifact_contract_gate(evidence_dir, required_artifacts=None, current_job_id=None) -> dict
    write_artifact_contract_gate(evidence_dir, written, required_artifacts=None, current_job_id=None) -> None
"""
from __future__ import annotations

import hashlib
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


def _is_safe_relative(ref: str) -> bool:
    """Reject absolute paths and any ref that walks out of its task directory."""
    r = str(ref or "").strip()
    if not r or r.startswith("/") or r.startswith("~"):
        return False
    parts = r.replace("\\", "/").split("/")
    return ".." not in parts and "" not in parts[:-1]


def _sha256_and_size(path: Path) -> tuple[str, int]:
    """Stream the file so a large raw_stream.jsonl is never held in memory."""
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
            size += len(chunk)
    return h.hexdigest(), size


def check_stream_artifacts(evidence_dir: str) -> dict[str, Any]:
    """Verify the F004 stream artifacts each task's provider evidence references.

    Existence is not integrity. Every referenced artifact is re-hashed and
    re-measured and compared against the ``stream_artifacts.json`` listing the
    export wrote, so a mutated ``raw_stream.jsonl`` or ``run_events.jsonl`` can
    never be presented as verified evidence. The listing and the provider
    references must describe exactly the same set of files.

    Stream artifacts are REQUIRED only for tasks whose ``provider_evidence.json``
    records ``stream_evidence_present: true`` — i.e. the run was made with
    ``--stream-evidence``. Without the flag there are no refs and nothing to
    require, so the check is simply not applicable and never blocks.
    """
    base = Path(evidence_dir) if evidence_dir else Path(".")
    tasks_with_streams: list[str] = []
    missing: list[str] = []              # referenced file absent from the bundle
    missing_metadata: list[str] = []     # referenced file absent from the listing
    hash_mismatches: list[dict[str, str]] = []
    size_mismatches: list[dict[str, Any]] = []
    unexpected: list[str] = []           # listed but not referenced, or out of tree
    duplicates: list[str] = []
    unsafe: list[str] = []
    missing_listing: list[str] = []      # task has refs but no stream_artifacts.json
    verified_count = 0

    task_runs = base / "task_runs"
    if task_runs.is_dir():
        for run_dir in sorted(p for p in task_runs.iterdir() if p.is_dir()):
            pe = _read_json(run_dir / "provider_evidence.json")
            if not pe or not pe.get("stream_evidence_present"):
                continue
            task = run_dir.name
            tasks_with_streams.append(task)

            listing_doc = _read_json(run_dir / "stream_artifacts.json")
            if listing_doc is None:
                missing_listing.append(f"task_runs/{task}/stream_artifacts.json")
                listing: dict[str, Any] = {}
            else:
                raw_listing = listing_doc.get("artifacts")
                listing = raw_listing if isinstance(raw_listing, dict) else {}

            # --- provider references -> recompute and compare ------------------
            task_prefix = f"task_runs/{task}/streams/"
            seen: set[str] = set()
            referenced: set[str] = set()

            for ref in pe.get("stream_artifact_refs") or []:
                ref = str(ref)
                key = f"task_runs/{task}/{ref}"
                if not _is_safe_relative(ref):
                    unsafe.append(key)
                    continue
                if key in seen:
                    duplicates.append(key)
                    continue
                seen.add(key)
                referenced.add(key)

                target = run_dir / ref
                if not target.is_file():
                    missing.append(key)
                    continue
                meta = listing.get(key)
                if not isinstance(meta, dict):
                    missing_metadata.append(key)
                    continue

                actual_hash, actual_size = _sha256_and_size(target)
                recorded_hash = str(meta.get("sha256") or "")
                recorded_size = meta.get("size_bytes")

                ok = True
                if actual_hash != recorded_hash:
                    hash_mismatches.append({
                        "path": key, "recorded": recorded_hash, "actual": actual_hash,
                    })
                    ok = False
                if actual_size != recorded_size:
                    size_mismatches.append({
                        "path": key, "recorded": recorded_size, "actual": actual_size,
                    })
                    ok = False
                if ok:
                    verified_count += 1

            # --- listing entries with no provider reference --------------------
            for key in listing:
                k = str(key)
                if not _is_safe_relative(k) or not k.startswith(task_prefix):
                    unexpected.append(k)
                elif k not in referenced:
                    unexpected.append(k)

    if not tasks_with_streams:
        applicable = False
        verdict = "NOT_APPLICABLE"
    else:
        applicable = True
        blocked = (
            missing or missing_metadata or hash_mismatches or size_mismatches
            or unexpected or duplicates or unsafe or missing_listing
        )
        verdict = "BLOCKED" if blocked else "PASS"

    return {
        "applicable": applicable,
        "verdict": verdict,
        "tasks_with_stream_evidence": tasks_with_streams,
        "artifacts_verified": verified_count,
        # Kept for readers of the previous shape.
        "artifacts_present": verified_count,
        "missing_stream_artifact_listing": missing_listing,
        "missing_stream_artifacts": missing,
        "missing_stream_artifact_metadata": missing_metadata,
        "stream_artifact_hash_mismatches": hash_mismatches,
        "stream_artifact_size_mismatches": size_mismatches,
        "unexpected_stream_artifacts": unexpected,
        "duplicate_stream_artifact_refs": duplicates,
        "unsafe_stream_artifact_refs": unsafe,
    }


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

    streams = check_stream_artifacts(str(base))

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
    for ref in streams["missing_stream_artifact_listing"]:
        issues.append(f"stream artifact listing {ref!r} is missing")
    for ref in streams["missing_stream_artifacts"]:
        issues.append(f"referenced stream artifact {ref!r} is missing from the bundle")
    for ref in streams["missing_stream_artifact_metadata"]:
        issues.append(f"stream artifact {ref!r} has no recorded hash/size")
    for m in streams["stream_artifact_hash_mismatches"]:
        issues.append(
            f"stream artifact {m['path']!r} sha256 mismatch: "
            f"recorded {m['recorded']!r}, actual {m['actual']!r}"
        )
    for m in streams["stream_artifact_size_mismatches"]:
        issues.append(
            f"stream artifact {m['path']!r} size mismatch: "
            f"recorded {m['recorded']!r}, actual {m['actual']!r}"
        )
    for ref in streams["unexpected_stream_artifacts"]:
        issues.append(f"stream artifact listing entry {ref!r} is not referenced by provider evidence")
    for ref in streams["duplicate_stream_artifact_refs"]:
        issues.append(f"duplicate stream artifact reference {ref!r}")
    for ref in streams["unsafe_stream_artifact_refs"]:
        issues.append(f"stream artifact ref {ref!r} is not a safe relative path")

    verdict = (
        "BLOCKED"
        if (missing_required or critical_fv_missing or stale_job_id
            or streams["verdict"] == "BLOCKED")
        else "PASS"
    )

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
        "stream_artifacts": streams,
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
