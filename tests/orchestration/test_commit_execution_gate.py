"""Tests for commit_execution_gate.py — verdict aggregation."""

from __future__ import annotations

import json
from pathlib import Path

from packages.orchestration.commit_execution_gate import (
    build_commit_execution_gate,
    write_commit_execution_gate,
)


def test_all_pass_commit_ready():
    gate = build_commit_execution_gate("PASS", "PASS", "PASS", "PASS")
    assert gate["verdict"] == "COMMIT_READY"
    assert gate["promote_ready"] is True
    assert gate["blocked_gates"] == []
    assert gate["non_pass_gates"] == []
    assert gate["issues"] == []


def test_blocked_gate_blocks():
    gate = build_commit_execution_gate("BLOCKED", "PASS", "PASS", "PASS")
    assert gate["verdict"] == "BLOCKED"
    assert gate["promote_ready"] is False
    assert "fresh_evidence_gate" in gate["blocked_gates"]
    assert "fresh_evidence_gate" in gate["non_pass_gates"]
    assert gate["issues"]


def test_needs_human_approval():
    gate = build_commit_execution_gate("PASS", "PASS_WITH_RISKS", "PASS", "PASS")
    assert gate["verdict"] == "NEEDS_HUMAN_APPROVAL"
    assert gate["promote_ready"] is False
    assert gate["blocked_gates"] == []
    assert "artifact_contract_gate" in gate["non_pass_gates"]


def test_change_provenance_blocked_blocks():
    gate = build_commit_execution_gate(
        "PASS", "PASS", "PASS", "PASS", change_provenance_verdict="BLOCKED"
    )
    assert gate["verdict"] == "BLOCKED"
    assert "change_provenance_gate" in gate["gate_checks"]
    assert "change_provenance_gate" in gate["blocked_gates"]
    assert gate["promote_ready"] is False


def test_change_provenance_optional_when_empty():
    gate = build_commit_execution_gate("PASS", "PASS", "PASS", "PASS")
    assert "change_provenance_gate" not in gate["gate_checks"]
    assert gate["verdict"] == "COMMIT_READY"

    with_value = build_commit_execution_gate(
        "PASS", "PASS", "PASS", "PASS", change_provenance_verdict="PASS"
    )
    assert "change_provenance_gate" in with_value["gate_checks"]


def test_write_registers_path(tmp_path: Path):
    written: dict[str, str] = {}
    write_commit_execution_gate(
        str(tmp_path),
        written,
        fresh_evidence_verdict="PASS",
        artifact_contract_verdict="PASS",
        runtime_integration_verdict="PASS",
        final_verifier_verdict="PASS",
    )
    out = tmp_path / "commit_execution_gate.json"
    assert out.exists()
    assert written["commit_execution_gate.json"] == str(out)
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["verdict"] == "COMMIT_READY"


def test_write_noop_when_empty_dir():
    written: dict[str, str] = {}
    write_commit_execution_gate("", written)
    assert written == {}


def test_blocked_when_final_verifier_needs_tests():
    gate = build_commit_execution_gate("PASS", "PASS", "PASS", "NEEDS_TESTS")
    assert gate["verdict"] == "BLOCKED"
    assert "final_verifier" in gate["blocked_gates"]
    assert gate["promote_ready"] is False


def test_blocked_when_final_verifier_needs_repair():
    gate = build_commit_execution_gate("PASS", "PASS", "PASS", "NEEDS_REPAIR")
    assert gate["verdict"] == "BLOCKED"
    assert "final_verifier" in gate["blocked_gates"]
    assert gate["promote_ready"] is False


def test_needs_human_approval_only_for_pass_with_risks():
    gate = build_commit_execution_gate("PASS", "PASS", "PASS", "PASS_WITH_RISKS")
    assert gate["verdict"] == "NEEDS_HUMAN_APPROVAL"
    assert gate["blocked_gates"] == []
    assert "final_verifier" in gate["non_pass_gates"]
    assert gate["promote_ready"] is False


def test_blocked_when_empty_verdict():
    gate = build_commit_execution_gate("PASS", "PASS", "PASS", "")
    assert gate["verdict"] == "BLOCKED"
    assert "final_verifier" in gate["blocked_gates"]
