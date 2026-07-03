"""Commit execution gate — aggregate all gate verdicts into commit readiness.

Deterministic, read-only orchestration logic: no provider calls, no target-repo
mutation, no job state mutation. Given the same set of gate verdicts, the same
gate is produced every time.

This is the terminal gate: it collects the verdicts of the upstream gates
(fresh evidence, artifact contract, runtime integration, final verifier, and the
optional change provenance gate) and reduces them to a single commit-readiness
verdict. Any BLOCKED upstream gate blocks the commit; any non-PASS upstream gate
demotes the run to NEEDS_HUMAN_APPROVAL; only an all-PASS set is COMMIT_READY.

Public API:
    build_commit_execution_gate(fresh_evidence_verdict, artifact_contract_verdict, runtime_integration_verdict, final_verifier_verdict, change_provenance_verdict="") -> dict
    write_commit_execution_gate(evidence_dir, written, fresh_evidence_verdict="", ...) -> None
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0.0"


def build_commit_execution_gate(
    fresh_evidence_verdict: str,
    artifact_contract_verdict: str,
    runtime_integration_verdict: str,
    final_verifier_verdict: str,
    change_provenance_verdict: str = "",
) -> dict[str, Any]:
    """Aggregate upstream gate verdicts into a commit-readiness verdict.

    ``change_provenance_verdict`` is optional: it is only included in the
    aggregated ``gate_checks`` when it is a non-empty string. A BLOCKED gate
    forces an overall BLOCKED verdict; any other non-PASS gate forces
    NEEDS_HUMAN_APPROVAL; an all-PASS set is COMMIT_READY. Never mutates any file.
    """
    _HARD_BLOCK = frozenset({"BLOCKED", "NEEDS_TESTS", "NEEDS_REPAIR", ""})

    gate_checks: dict[str, str] = {
        "fresh_evidence_gate": str(fresh_evidence_verdict or ""),
        "artifact_contract_gate": str(artifact_contract_verdict or ""),
        "runtime_integration_gate": str(runtime_integration_verdict or ""),
        "final_verifier": str(final_verifier_verdict or ""),
    }
    if change_provenance_verdict:
        gate_checks["change_provenance_gate"] = str(change_provenance_verdict)

    blocked_gates = sorted(
        name for name, verdict in gate_checks.items()
        if verdict in _HARD_BLOCK
    )
    non_pass_gates = sorted(
        name for name, verdict in gate_checks.items() if verdict != "PASS"
    )

    if blocked_gates:
        verdict = "BLOCKED"
    elif non_pass_gates:
        verdict = "NEEDS_HUMAN_APPROVAL"
    else:
        verdict = "COMMIT_READY"

    issues: list[str] = []
    for name in blocked_gates:
        issues.append(f"gate {name!r} is BLOCKED")
    for name in non_pass_gates:
        if name in blocked_gates:
            continue
        issues.append(f"gate {name!r} is not PASS (verdict {gate_checks[name]!r})")

    promote_ready = verdict == "COMMIT_READY"

    return {
        "schema_version": SCHEMA_VERSION,
        "verdict": verdict,
        "gate_checks": gate_checks,
        "blocked_gates": blocked_gates,
        "non_pass_gates": non_pass_gates,
        "promote_ready": promote_ready,
        "issues": issues,
    }


def write_commit_execution_gate(
    evidence_dir: str,
    written: dict[str, str],
    fresh_evidence_verdict: str = "",
    artifact_contract_verdict: str = "",
    runtime_integration_verdict: str = "",
    final_verifier_verdict: str = "",
    change_provenance_verdict: str = "",
) -> None:
    """Build and write ``commit_execution_gate.json`` into ``evidence_dir``.

    Registers the written path in ``written`` when provided. No-op when
    ``evidence_dir`` is empty.
    """
    if not evidence_dir:
        return

    gate = build_commit_execution_gate(
        fresh_evidence_verdict,
        artifact_contract_verdict,
        runtime_integration_verdict,
        final_verifier_verdict,
        change_provenance_verdict,
    )

    out_dir = Path(evidence_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "commit_execution_gate.json"
    json_path.write_text(json.dumps(gate, indent=2) + "\n", encoding="utf-8")

    if written is not None:
        written["commit_execution_gate.json"] = str(json_path)
