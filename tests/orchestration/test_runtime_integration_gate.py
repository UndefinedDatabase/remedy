"""Tests for runtime_integration_gate.py — static wiring verification."""

from __future__ import annotations

import json
from pathlib import Path

from packages.orchestration.runtime_integration_gate import (
    INTEGRATION_CHECKS,
    build_runtime_integration_gate,
    write_runtime_integration_gate,
)


def _seed_source(repo_root: Path, rel: str, text: str) -> None:
    target = repo_root / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


_CHECKS = [
    {
        "check_id": "calls_a",
        "source_file": "pkg/pipeline.py",
        "check_type": "call_exists",
        "pattern": "write_gate_a",
    },
    {
        "check_id": "calls_b",
        "source_file": "pkg/pipeline.py",
        "check_type": "call_exists",
        "pattern": "write_gate_b",
    },
]


def test_all_calls_present_passes(tmp_path):
    _seed_source(tmp_path, "pkg/pipeline.py", "write_gate_a()\nwrite_gate_b()\n")

    gate = build_runtime_integration_gate(str(tmp_path), checks=_CHECKS)

    assert gate["verdict"] == "PASS"
    assert gate["checks_passed"] == 2
    assert gate["checks_total"] == 2
    assert gate["issues"] == []
    assert all(c["found"] for c in gate["checks"])
    assert gate["schema_version"] == "1.0.0"


def test_missing_call_blocks(tmp_path):
    _seed_source(tmp_path, "pkg/pipeline.py", "write_gate_a()\n")

    gate = build_runtime_integration_gate(str(tmp_path), checks=_CHECKS)

    assert gate["verdict"] == "BLOCKED"
    assert gate["checks_passed"] == 1
    assert any("write_gate_b" in issue for issue in gate["issues"])
    b = next(c for c in gate["checks"] if c["check_id"] == "calls_b")
    assert b["found"] is False


def test_missing_source_file_blocks(tmp_path):
    # No file created at all.
    gate = build_runtime_integration_gate(str(tmp_path), checks=_CHECKS)

    assert gate["verdict"] == "BLOCKED"
    assert gate["checks_passed"] == 0
    assert all(c["file_missing"] for c in gate["checks"])
    assert any("not found" in issue for issue in gate["issues"])


def test_default_checks_cover_all_gate_writers():
    patterns = {c["pattern"] for c in INTEGRATION_CHECKS}
    assert {
        "write_fresh_evidence_gate",
        "write_artifact_contract_gate",
        "write_runtime_integration_gate",
        "write_change_provenance_gate",
        "write_commit_execution_gate",
    } <= patterns


def test_default_checks_target_job_evidence(tmp_path):
    # A repo whose job_evidence.py wires every writer passes the default checks.
    body = "\n".join(
        f"{c['pattern']}(...)" for c in INTEGRATION_CHECKS
    )
    _seed_source(tmp_path, "packages/orchestration/job_evidence.py", body + "\n")

    gate = build_runtime_integration_gate(str(tmp_path))

    assert gate["verdict"] == "PASS"
    assert gate["checks_total"] == len(INTEGRATION_CHECKS)


def test_write_registers_output(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    body = "\n".join(f"{c['pattern']}(...)" for c in INTEGRATION_CHECKS)
    _seed_source(repo, "packages/orchestration/job_evidence.py", body + "\n")

    evidence = tmp_path / "evidence"
    written: dict[str, str] = {}
    write_runtime_integration_gate(str(evidence), str(repo), written)

    assert "runtime_integration_gate.json" in written
    on_disk = json.loads((evidence / "runtime_integration_gate.json").read_text())
    assert on_disk["verdict"] == "PASS"
    assert on_disk["schema_version"] == "1.0.0"


def test_write_noop_when_no_evidence_dir(tmp_path):
    written: dict[str, str] = {}
    write_runtime_integration_gate("", str(tmp_path), written)
    assert written == {}
