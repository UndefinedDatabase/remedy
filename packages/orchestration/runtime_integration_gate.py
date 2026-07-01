"""Runtime integration gate — verify gate writers are wired into the pipeline.

Deterministic, read-only orchestration logic: no provider calls, no target-repo
mutation, no job state mutation. Uses static analysis (source-text search) to
confirm that the evidence-pipeline module actually *calls* each gate writer.
A gate module that exists but is never invoked produces no evidence — this gate
catches that class of silent regression.

Public API:
    build_runtime_integration_gate(repo_root, checks=None) -> dict
    write_runtime_integration_gate(evidence_dir, repo_root, written=None) -> None
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0.0"

_JOB_EVIDENCE = "packages/orchestration/job_evidence.py"

# Each check: the evidence pipeline must reference the given pattern in the
# named source file. ``call_exists`` asserts a writer function is invoked;
# ``artifact_written`` asserts an artifact filename is registered.
INTEGRATION_CHECKS: tuple[dict[str, str], ...] = (
    {
        "check_id": "job_evidence_calls_fresh_evidence_gate",
        "source_file": _JOB_EVIDENCE,
        "check_type": "call_exists",
        "pattern": "write_fresh_evidence_gate",
    },
    {
        "check_id": "job_evidence_calls_artifact_contract_gate",
        "source_file": _JOB_EVIDENCE,
        "check_type": "call_exists",
        "pattern": "write_artifact_contract_gate",
    },
    {
        "check_id": "job_evidence_calls_runtime_integration_gate",
        "source_file": _JOB_EVIDENCE,
        "check_type": "call_exists",
        "pattern": "write_runtime_integration_gate",
    },
    {
        "check_id": "job_evidence_calls_change_provenance_gate",
        "source_file": _JOB_EVIDENCE,
        "check_type": "call_exists",
        "pattern": "write_change_provenance_gate",
    },
    {
        "check_id": "job_evidence_calls_commit_execution_gate",
        "source_file": _JOB_EVIDENCE,
        "check_type": "call_exists",
        "pattern": "write_commit_execution_gate",
    },
)


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except (OSError, ValueError):
        return None


def build_runtime_integration_gate(
    repo_root: str,
    checks: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    """Statically verify each integration check against ``repo_root``.

    ``checks`` overrides ``INTEGRATION_CHECKS`` when provided. For each check the
    named ``source_file`` (relative to ``repo_root``) is read and searched for
    ``pattern``. A check passes when the pattern is present. A missing or
    unreadable source file fails the check. Never mutates any file.
    """
    root = Path(repo_root) if repo_root else Path(".")
    active = list(checks) if checks is not None else [dict(c) for c in INTEGRATION_CHECKS]

    results: list[dict[str, Any]] = []
    issues: list[str] = []

    for check in active:
        check_id = str(check.get("check_id", ""))
        source_file = str(check.get("source_file", ""))
        check_type = str(check.get("check_type", "call_exists"))
        pattern = str(check.get("pattern", ""))

        text = _read_text(root / source_file)
        found = bool(pattern) and text is not None and pattern in text
        file_missing = text is None

        results.append({
            "check_id": check_id,
            "source_file": source_file,
            "check_type": check_type,
            "pattern": pattern,
            "found": found,
            "file_missing": file_missing,
        })

        if not found:
            if file_missing:
                issues.append(f"{check_id}: source file {source_file!r} not found")
            else:
                issues.append(
                    f"{check_id}: pattern {pattern!r} not found in {source_file!r}"
                )

    all_passed = all(r["found"] for r in results) and bool(results)
    verdict = "PASS" if all_passed else "BLOCKED"

    return {
        "schema_version": SCHEMA_VERSION,
        "verdict": verdict,
        "checks": results,
        "checks_total": len(results),
        "checks_passed": sum(1 for r in results if r["found"]),
        "issues": issues,
    }


def write_runtime_integration_gate(
    evidence_dir: str,
    repo_root: str,
    written: dict[str, str] | None = None,
) -> None:
    """Build and write ``runtime_integration_gate.json`` into ``evidence_dir``.

    Registers the written path in ``written`` when provided. No-op when
    ``evidence_dir`` is empty.
    """
    if not evidence_dir:
        return

    gate = build_runtime_integration_gate(repo_root)

    out_dir = Path(evidence_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "runtime_integration_gate.json"
    json_path.write_text(json.dumps(gate, indent=2) + "\n", encoding="utf-8")

    if written is not None:
        written["runtime_integration_gate.json"] = str(json_path)
