"""Tests for artifact_contract_gate.py — required artifact contract checks."""

from __future__ import annotations

import json
from pathlib import Path

from packages.orchestration.artifact_contract_gate import (
    CORE_ARTIFACTS,
    CRITICAL_FV_REFERENCES,
    build_artifact_contract_gate,
    write_artifact_contract_gate,
)


def _write(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data) + "\n", encoding="utf-8")


def _seed_core(tmp_path: Path, job_id: str = "job-abc", completeness: dict | None = None) -> str:
    for name in CORE_ARTIFACTS:
        if name == "manifest.json":
            _write(tmp_path / name, {"job_id": job_id})
        elif name == "final_verifier_report.json":
            _write(tmp_path / name, {"evidence_completeness": completeness or {}})
        else:
            _write(tmp_path / name, {"ok": True})
    return str(tmp_path)


def test_all_present_passes(tmp_path):
    evidence = _seed_core(tmp_path)
    gate = build_artifact_contract_gate(evidence)

    assert gate["verdict"] == "PASS"
    assert gate["missing_required"] == []
    assert gate["issues"] == []
    assert all(gate["required_artifacts"].values())
    assert gate["schema_version"] == "1.0.0"


def test_missing_core_blocks(tmp_path):
    evidence = _seed_core(tmp_path)
    (tmp_path / "token_truth.json").unlink()

    gate = build_artifact_contract_gate(evidence)

    assert gate["verdict"] == "BLOCKED"
    assert "token_truth.json" in gate["missing_required"]
    assert any("token_truth.json" in issue for issue in gate["issues"])


def test_critical_fv_referenced_missing_blocks(tmp_path):
    evidence = _seed_core(
        tmp_path,
        completeness={"token_truth": False, "safe_diff": True},
    )
    gate = build_artifact_contract_gate(evidence)

    assert gate["verdict"] == "BLOCKED"
    assert "token_truth" in gate["fv_referenced_missing"]
    assert "token_truth" in gate["critical_fv_missing"]


def test_noncritical_fv_referenced_missing_not_blocked(tmp_path):
    evidence = _seed_core(
        tmp_path,
        completeness={"review_scope_packet": False, "spec_compliance_check": False},
    )
    gate = build_artifact_contract_gate(evidence)

    assert gate["verdict"] == "PASS"
    assert "review_scope_packet" in gate["fv_referenced_missing"]
    assert gate["critical_fv_missing"] == []


def test_change_provenance_gate_missing_blocks(tmp_path):
    evidence = _seed_core(tmp_path)
    (tmp_path / "change_provenance_gate.json").unlink(missing_ok=True)

    gate = build_artifact_contract_gate(evidence)

    assert gate["verdict"] == "BLOCKED"
    assert "change_provenance_gate.json" in gate["missing_required"]


def test_stale_job_id_blocks(tmp_path):
    evidence = _seed_core(tmp_path, job_id="job-old")
    gate = build_artifact_contract_gate(evidence, current_job_id="job-new")

    assert gate["verdict"] == "BLOCKED"
    assert gate["job_id_fresh"] is False
    assert gate["evidence_job_id"] == "job-old"
    assert any("job_id" in issue for issue in gate["issues"])


def test_commit_execution_gate_missing_blocks(tmp_path):
    evidence = _seed_core(tmp_path)
    (tmp_path / "commit_execution_gate.json").unlink(missing_ok=True)

    gate = build_artifact_contract_gate(evidence)

    assert gate["verdict"] == "BLOCKED"
    assert "commit_execution_gate.json" in gate["missing_required"]


def test_fv_referenced_missing_tests_txt_blocks(tmp_path):
    evidence = _seed_core(
        tmp_path,
        completeness={"tests_txt": False},
    )
    gate = build_artifact_contract_gate(evidence)

    assert gate["verdict"] == "BLOCKED"
    assert "tests_txt" in gate["critical_fv_missing"]


def test_fv_referenced_missing_safe_diff_blocks(tmp_path):
    evidence = _seed_core(
        tmp_path,
        completeness={"safe_diff": False},
    )
    gate = build_artifact_contract_gate(evidence)

    assert gate["verdict"] == "BLOCKED"
    assert "safe_diff" in gate["critical_fv_missing"]


def test_critical_references_include_all_gates(tmp_path):
    expected = {"token_truth", "fresh_evidence_gate", "artifact_contract_gate",
                "runtime_integration_gate", "commit_execution_gate",
                "change_provenance_gate", "safe_diff", "review_json", "tests_txt"}
    assert CRITICAL_FV_REFERENCES == expected


def test_write_registers_output(tmp_path):
    evidence = _seed_core(tmp_path)
    written: dict[str, str] = {}
    write_artifact_contract_gate(evidence, written)

    assert "artifact_contract_gate.json" in written
    on_disk = json.loads((tmp_path / "artifact_contract_gate.json").read_text())
    assert on_disk["verdict"] == "PASS"
    assert on_disk["schema_version"] == "1.0.0"
