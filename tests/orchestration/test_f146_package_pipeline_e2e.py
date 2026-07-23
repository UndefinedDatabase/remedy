"""E2E tests for F146 package-pipeline closure.

Validates the F146-scoped gate: feature-aware check selection, feature_id
propagation through Evidence refresh, registry test binding, and read-only
command guarantees.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

REPO_ROOT = str(Path(__file__).resolve().parents[2])


def _make_f146_verification_data(*, passed_counts=None):
    """Build verification_data covering only F146 test bindings."""
    from packages.orchestration.runtime_integration_gate import TEST_EXECUTION_BINDINGS

    f146_bindings = [b for b in TEST_EXECUTION_BINDINGS
                     if b["check_id"].startswith("f146_")]

    test_files = [b["test_file"] for b in f146_bindings]
    if passed_counts is None:
        passed_counts = [83, 18, 46]

    runs = []
    for i, (tf, pc) in enumerate(zip(test_files, passed_counts)):
        node_ids = [f"{tf}::test_{j}" for j in range(3)]
        binding = f146_bindings[i]
        for crit in binding.get("critical_node_ids", []):
            node_ids.append(f"{tf}::{crit}")
        runs.append({
            "run_id": f"vr-{i + 1:04d}",
            "command": f"pytest {tf}",
            "exit_code": 0,
            "passed": pc,
            "failed": 0,
            "test_files": [tf],
            "stdout_summary": f"{pc} passed",
            "skipped": 0,
            "selected": pc,
            "node_ids": node_ids,
            "output_hash": "a" * 64,
            "head_sha": "abc123",
        })
    return {
        "schema_version": "1.0.0",
        "verification_type": "explicit_commands",
        "runs": runs,
        "command": " && ".join(f"pytest {tf}" for tf in test_files),
        "exit_code": 0,
        "passed": sum(passed_counts),
        "failed": 0,
        "test_files": sorted(test_files),
        "timestamp": "2026-07-23T00:00:00+00:00",
    }


class TestF146GateScope:
    """F146-scoped gate includes only F146 and generic checks, no F018."""

    def test_f146_gate_excludes_f018(self):
        from packages.orchestration.runtime_integration_gate import (
            build_runtime_integration_gate,
        )
        gate = build_runtime_integration_gate(REPO_ROOT, feature_id="f146")
        f018 = [c for c in gate["checks"] if c["check_id"].startswith("f018_")]
        assert len(f018) == 0

    def test_f146_gate_includes_f146_checks(self):
        from packages.orchestration.runtime_integration_gate import (
            build_runtime_integration_gate,
        )
        gate = build_runtime_integration_gate(REPO_ROOT, feature_id="f146")
        f146 = [c for c in gate["checks"] if c["check_id"].startswith("f146_")]
        assert len(f146) > 0

    def test_f146_gate_has_feature_id(self):
        from packages.orchestration.runtime_integration_gate import (
            build_runtime_integration_gate,
        )
        gate = build_runtime_integration_gate(REPO_ROOT, feature_id="f146")
        assert gate["feature_id"] == "f146"

    def test_f146_gate_passes_with_verification(self):
        from packages.orchestration.runtime_integration_gate import (
            build_runtime_integration_gate,
        )
        vd = _make_f146_verification_data()
        gate = build_runtime_integration_gate(
            REPO_ROOT, verification_data=vd, feature_id="f146")
        assert gate["verdict"] == "PASS"
        assert gate["feature_id"] == "f146"


class TestF146RegistryBinding:
    """F146 gate includes test_project_registry.py binding."""

    def test_registry_binding_exists(self):
        from packages.orchestration.runtime_integration_gate import (
            TEST_EXECUTION_BINDINGS,
        )
        registry = [b for b in TEST_EXECUTION_BINDINGS
                     if b["check_id"] == "f146_test_registry_execution"]
        assert len(registry) == 1
        assert registry[0]["test_file"] == "tests/test_project_registry.py"
        assert registry[0]["min_passed"] >= 40

    def test_registry_binding_selected_for_f146(self):
        from packages.orchestration.runtime_integration_gate import (
            _select_checks_for_feature,
        )
        _static, bindings = _select_checks_for_feature("f146")
        ids = [b["check_id"] for b in bindings]
        assert "f146_test_registry_execution" in ids

    def test_registry_binding_not_selected_for_f018(self):
        from packages.orchestration.runtime_integration_gate import (
            _select_checks_for_feature,
        )
        _static, bindings = _select_checks_for_feature("f018")
        ids = [b["check_id"] for b in bindings]
        assert "f146_test_registry_execution" not in ids


class TestF146FeatureIdPropagation:
    """feature_id survives Evidence refresh cycle."""

    def test_refresh_preserves_f146(self, tmp_path):
        from packages.orchestration.runtime_integration_gate import (
            build_runtime_integration_gate,
        )
        gate = build_runtime_integration_gate(REPO_ROOT, feature_id="f146")
        gate_path = tmp_path / "runtime_integration_gate.json"
        gate_path.write_text(json.dumps(gate, indent=1, sort_keys=True))

        from scripts.refresh_review_evidence import refresh_staged_evidence
        report = refresh_staged_evidence(str(tmp_path), REPO_ROOT)

        refreshed = json.loads(gate_path.read_text())
        assert refreshed["feature_id"] == "f146"
        assert not report["issues"]

    def test_refresh_no_feature_id_stays_absent(self, tmp_path):
        from packages.orchestration.runtime_integration_gate import (
            build_runtime_integration_gate,
        )
        gate = build_runtime_integration_gate(REPO_ROOT)
        gate_path = tmp_path / "runtime_integration_gate.json"
        gate_path.write_text(json.dumps(gate, indent=1, sort_keys=True))

        from scripts.refresh_review_evidence import refresh_staged_evidence
        refresh_staged_evidence(str(tmp_path), REPO_ROOT)

        refreshed = json.loads(gate_path.read_text())
        assert "feature_id" not in refreshed


class TestF146ReadOnlyInvariant:
    """Read-only commands never write to project files."""

    def test_list_readonly_no_write(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_registry import (
            RemyProject,
            _list_projects_readonly,
            save_project,
        )
        p = RemyProject(name="Test", slug="test")
        save_project(p)

        f = tmp_path / "projects" / f"{p.id}.json"
        before = f.read_bytes()
        mtime = f.stat().st_mtime_ns

        _list_projects_readonly()

        assert f.read_bytes() == before
        assert f.stat().st_mtime_ns == mtime

    def test_project_set_readonly_no_write(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_registry import (
            RemyProject,
            _project_set_readonly,
            save_project,
        )
        p = RemyProject(name="Test", slug="test")
        save_project(p)

        f = tmp_path / "projects" / f"{p.id}.json"
        before = f.read_bytes()
        mtime = f.stat().st_mtime_ns

        _project_set_readonly()

        assert f.read_bytes() == before
        assert f.stat().st_mtime_ns == mtime
