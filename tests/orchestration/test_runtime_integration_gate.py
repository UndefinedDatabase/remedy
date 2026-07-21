"""Tests for runtime_integration_gate.py — static wiring + test execution bindings."""

from __future__ import annotations

import json
from pathlib import Path

from packages.orchestration.runtime_integration_gate import (
    INTEGRATION_CHECKS,
    TEST_EXECUTION_BINDINGS,
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
    assert gate["schema_version"] == "1.1.0"


def test_missing_call_blocks(tmp_path):
    _seed_source(tmp_path, "pkg/pipeline.py", "write_gate_a()\n")

    gate = build_runtime_integration_gate(str(tmp_path), checks=_CHECKS)

    assert gate["verdict"] == "BLOCKED"
    assert gate["checks_passed"] == 1
    assert any("write_gate_b" in issue for issue in gate["issues"])
    b = next(c for c in gate["checks"] if c["check_id"] == "calls_b")
    assert b["found"] is False


def test_missing_source_file_blocks(tmp_path):
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


def _seed_all_static_checks(tmp_path):
    """Seed every source file referenced by INTEGRATION_CHECKS with its patterns."""
    by_file: dict[str, list[str]] = {}
    for c in INTEGRATION_CHECKS:
        by_file.setdefault(c["source_file"], []).append(c["pattern"])
    for rel, patterns in by_file.items():
        _seed_source(tmp_path, rel, "\n".join(f"{p}(...)" for p in patterns) + "\n")


def test_default_static_checks_pass_with_patterns(tmp_path):
    _seed_all_static_checks(tmp_path)

    gate = build_runtime_integration_gate(str(tmp_path))

    static_checks = [c for c in gate["checks"] if c["check_type"] == "call_exists"]
    assert len(static_checks) == len(INTEGRATION_CHECKS)
    assert all(c["found"] for c in static_checks)

    binding_checks = [c for c in gate["checks"] if c["check_type"] == "test_execution_binding"]
    assert len(binding_checks) == len(TEST_EXECUTION_BINDINGS)
    assert all(not c["found"] for c in binding_checks)
    assert gate["verdict"] == "BLOCKED"


def test_execution_binding_passes_with_matching_data(tmp_path):
    _seed_all_static_checks(tmp_path)

    vdata = {"runs": []}
    for b in TEST_EXECUTION_BINDINGS:
        vdata["runs"].append({
            "run_id": f"vr-{b['check_id']}",
            "command": f"pytest {b['test_file']}",
            "exit_code": 0,
            "passed": b["min_passed"] + 10,
            "failed": 0,
            "skipped": 0,
            "selected": b["min_passed"] + 10,
            "node_ids": [f"{b['test_file']}::test_{i}" for i in range(3)],
            "output_hash": "sha256:abc123",
            "head_sha": "deadbeef",
            "test_files": [b["test_file"]],
        })

    gate = build_runtime_integration_gate(
        str(tmp_path), verification_data=vdata,
    )
    assert gate["verdict"] == "PASS"
    assert gate["checks_total"] == len(INTEGRATION_CHECKS) + len(TEST_EXECUTION_BINDINGS)
    assert gate["issues"] == []

    for c in gate["checks"]:
        if c["check_type"] == "test_execution_binding":
            assert c["found"] is True
            assert "bound_run" in c
            assert c["bound_run"]["exit_code"] == 0
            assert c["bound_run"]["head_sha"] == "deadbeef"


def test_execution_binding_fails_without_data(tmp_path):
    _seed_all_static_checks(tmp_path)

    gate = build_runtime_integration_gate(str(tmp_path))

    bindings = [c for c in gate["checks"] if c["check_type"] == "test_execution_binding"]
    assert len(bindings) == len(TEST_EXECUTION_BINDINGS)
    assert all(not c["found"] for c in bindings)
    assert gate["verdict"] == "BLOCKED"


def test_execution_binding_fails_insufficient_passes(tmp_path):
    _seed_all_static_checks(tmp_path)

    b = TEST_EXECUTION_BINDINGS[0]
    vdata = {"runs": [{
        "run_id": "vr-1",
        "command": f"pytest {b['test_file']}",
        "exit_code": 0,
        "passed": 1,
        "failed": 0,
        "test_files": [b["test_file"]],
    }]}

    gate = build_runtime_integration_gate(
        str(tmp_path), verification_data=vdata,
    )
    target = next(c for c in gate["checks"]
                  if c["check_id"] == b["check_id"])
    assert target["found"] is False
    assert gate["verdict"] == "BLOCKED"


def test_execution_binding_fails_nonzero_exit(tmp_path):
    _seed_all_static_checks(tmp_path)

    b = TEST_EXECUTION_BINDINGS[0]
    vdata = {"runs": [{
        "run_id": "vr-1",
        "command": f"pytest {b['test_file']}",
        "exit_code": 1,
        "passed": 200,
        "failed": 1,
        "test_files": [b["test_file"]],
    }]}

    gate = build_runtime_integration_gate(
        str(tmp_path), verification_data=vdata,
    )
    target = next(c for c in gate["checks"]
                  if c["check_id"] == b["check_id"])
    assert target["found"] is False


def test_zero_checks_blocks(tmp_path):
    gate = build_runtime_integration_gate(str(tmp_path), checks=[])

    assert gate["verdict"] == "BLOCKED"
    assert gate["checks_total"] == 0
    assert "zero checks" in gate["issues"][0]


def test_write_registers_output(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    by_file: dict[str, list[str]] = {}
    for c in INTEGRATION_CHECKS:
        by_file.setdefault(c["source_file"], []).append(c["pattern"])
    for rel, patterns in by_file.items():
        _seed_source(repo, rel, "\n".join(f"{p}(...)" for p in patterns) + "\n")

    evidence = tmp_path / "evidence"
    written: dict[str, str] = {}
    write_runtime_integration_gate(str(evidence), str(repo), written)

    assert "runtime_integration_gate.json" in written
    on_disk = json.loads((evidence / "runtime_integration_gate.json").read_text())
    assert on_disk["schema_version"] == "1.1.0"


def test_write_with_verification_data(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    by_file: dict[str, list[str]] = {}
    for c in INTEGRATION_CHECKS:
        by_file.setdefault(c["source_file"], []).append(c["pattern"])
    for rel, patterns in by_file.items():
        _seed_source(repo, rel, "\n".join(f"{p}(...)" for p in patterns) + "\n")

    vdata = {"runs": []}
    for b in TEST_EXECUTION_BINDINGS:
        vdata["runs"].append({
            "run_id": f"vr-{b['check_id']}",
            "command": f"pytest {b['test_file']}",
            "exit_code": 0,
            "passed": b["min_passed"] + 5,
            "failed": 0,
            "test_files": [b["test_file"]],
        })

    evidence = tmp_path / "evidence"
    written: dict[str, str] = {}
    write_runtime_integration_gate(
        str(evidence), str(repo), written, verification_data=vdata,
    )

    on_disk = json.loads((evidence / "runtime_integration_gate.json").read_text())
    assert on_disk["verdict"] == "PASS"


def test_write_noop_when_no_evidence_dir(tmp_path):
    written: dict[str, str] = {}
    write_runtime_integration_gate("", str(tmp_path), written)
    assert written == {}


def test_custom_checks_skip_execution_bindings(tmp_path):
    _seed_source(tmp_path, "pkg/pipeline.py", "write_gate_a()\nwrite_gate_b()\n")

    gate = build_runtime_integration_gate(str(tmp_path), checks=_CHECKS)

    assert gate["checks_total"] == 2
    assert not any(c["check_type"] == "test_execution_binding" for c in gate["checks"])
