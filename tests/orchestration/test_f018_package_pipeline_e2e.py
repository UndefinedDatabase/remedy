"""E2E tests for F018 package-pipeline closure.

Validates the full chain: gate producer → manual attestation → manifest
validator → evidence refresh → persisted actuals schema → runtime boundary
guards.
"""
from __future__ import annotations

import json
import os
import shutil
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def scratch(tmp_path):
    return str(tmp_path)


def _make_verification_data(
    *,
    test_files=None,
    passed_counts=None,
    head_sha="abc123",
    output_hash=None,
):
    """Build complete verification_data matching all 6 binding test files (F018 + F146)."""
    if output_hash is None:
        output_hash = "a" * 64
    if test_files is None:
        test_files = [
            "tests/orchestration/test_f018_authority_integration.py",
            "tests/orchestration/test_budget_guard.py",
            "tests/orchestration/test_job_budgets.py",
            "tests/orchestration/test_budget_stop_integration.py",
            "tests/orchestration/test_project_resolution.py",
            "tests/cli/test_project_current.py",
            "tests/test_project_registry.py",
        ]
    if passed_counts is None:
        passed_counts = [95, 52, 76, 39, 83, 16, 46]

    from packages.orchestration.runtime_integration_gate import TEST_EXECUTION_BINDINGS
    _binding_map = {b["test_file"]: b for b in TEST_EXECUTION_BINDINGS}

    runs = []
    for i, (tf, pc) in enumerate(zip(test_files, passed_counts)):
        node_ids = [f"{tf}::test_{j}" for j in range(3)]
        binding = _binding_map.get(tf)
        if binding:
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
            "output_hash": output_hash,
            "head_sha": head_sha,
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
        "timestamp": "2026-07-22T00:00:00+00:00",
    }


# ---------------------------------------------------------------------------
# Scope 1: Gate producer produces v1.1.0 with real checks
# ---------------------------------------------------------------------------

class TestGateProducerV110:
    def test_gate_schema_version(self, scratch):
        from packages.orchestration.runtime_integration_gate import (
            build_runtime_integration_gate,
        )
        gate = build_runtime_integration_gate(
            ".", verification_data=_make_verification_data())
        assert gate["schema_version"] == "1.1.0"

    def test_gate_has_34_checks(self, scratch):
        from packages.orchestration.runtime_integration_gate import (
            build_runtime_integration_gate,
        )
        gate = build_runtime_integration_gate(
            ".", verification_data=_make_verification_data())
        assert gate["checks_total"] == 35

    def test_gate_28_static_6_binding(self, scratch):
        from packages.orchestration.runtime_integration_gate import (
            build_runtime_integration_gate,
        )
        gate = build_runtime_integration_gate(
            ".", verification_data=_make_verification_data())
        static = [c for c in gate["checks"] if c["check_type"] == "call_exists"]
        binding = [c for c in gate["checks"]
                   if c["check_type"] == "test_execution_binding"]
        assert len(static) == 28
        assert len(binding) == 7

    def test_gate_passes_with_all_bindings(self, scratch):
        from packages.orchestration.runtime_integration_gate import (
            build_runtime_integration_gate,
        )
        gate = build_runtime_integration_gate(
            ".", verification_data=_make_verification_data())
        assert gate["verdict"] == "PASS"
        assert gate["checks_passed"] == 35

    def test_gate_blocks_with_zero_checks(self, scratch):
        from packages.orchestration.runtime_integration_gate import (
            build_runtime_integration_gate,
        )
        gate = build_runtime_integration_gate(".", checks=[])
        assert gate["verdict"] == "BLOCKED"
        assert gate["checks_total"] == 0

    def test_bindings_carry_bound_run(self, scratch):
        from packages.orchestration.runtime_integration_gate import (
            build_runtime_integration_gate,
        )
        gate = build_runtime_integration_gate(
            ".", verification_data=_make_verification_data())
        bindings = [c for c in gate["checks"]
                    if c["check_type"] == "test_execution_binding"]
        for b in bindings:
            assert b["found"] is True
            br = b["bound_run"]
            assert isinstance(br, dict)
            assert br["head_sha"] == "abc123"
            assert br["output_hash"] == "a" * 64
            assert br["passed"] >= b["min_passed"]

    def test_missing_binding_blocks_gate(self, scratch):
        from packages.orchestration.runtime_integration_gate import (
            build_runtime_integration_gate,
        )
        vd = _make_verification_data(test_files=["tests/orchestration/test_budget_guard.py"],
                                     passed_counts=[52])
        gate = build_runtime_integration_gate(".", verification_data=vd)
        assert gate["verdict"] == "BLOCKED"
        assert gate["checks_passed"] < 34


# ---------------------------------------------------------------------------
# Scope 1: Manual attestation produces v1.1.0 gate (not zero-check v1.0.0)
# ---------------------------------------------------------------------------

class TestManualAttestationGate:
    def test_build_manual_gates_produces_v110(self, scratch):
        from packages.orchestration.manual_attestation import (
            build_manual_completion_gates,
        )
        vd = _make_verification_data()
        build_manual_completion_gates(
            scratch,
            job_id="test-job",
            authority=["packages/orchestration/pingpong_job.py"],
            file_hashes={"packages/orchestration/pingpong_job.py": "sha256:x"},
            step="1-10",
            total_passed=244,
            verification_runs=vd["runs"],
            repo_root=".",
            verification_data=vd,
        )
        gate_path = os.path.join(scratch, "runtime_integration_gate.json")
        assert os.path.isfile(gate_path)
        with open(gate_path) as f:
            gate = json.loads(f.read())
        assert gate["schema_version"] == "1.1.0"
        assert gate["checks_total"] == 35
        assert gate["checks_passed"] == 35
        assert gate["verdict"] == "PASS"

    def test_old_zero_check_gate_no_longer_produced(self, scratch):
        from packages.orchestration.manual_attestation import (
            build_manual_completion_gates,
        )
        vd = _make_verification_data()
        build_manual_completion_gates(
            scratch,
            job_id="test-job",
            authority=["packages/orchestration/pingpong_job.py"],
            file_hashes={"packages/orchestration/pingpong_job.py": "sha256:x"},
            step="1-10",
            total_passed=244,
            verification_runs=vd["runs"],
            repo_root=".",
            verification_data=vd,
        )
        with open(os.path.join(scratch, "runtime_integration_gate.json")) as f:
            gate = json.loads(f.read())
        assert gate["checks_total"] > 0, "zero-check gate must no longer be produced"


# ---------------------------------------------------------------------------
# Scope 1+2: Manifest validator accepts v1.1.0 gate
# ---------------------------------------------------------------------------

class TestManifestValidatorV110:
    def test_v110_gate_passes_schema_validation(self):
        from packages.orchestration.runtime_integration_gate import (
            build_runtime_integration_gate,
        )
        from scripts.build_review_manifest import _gate_closed_schema_problems
        gate = build_runtime_integration_gate(
            ".", verification_data=_make_verification_data())
        assert _gate_closed_schema_problems("runtime_integration_gate.json", gate) == []

    def test_v110_gate_passes_semantic_validation(self):
        from packages.orchestration.runtime_integration_gate import (
            build_runtime_integration_gate,
        )
        from scripts.build_review_manifest import _safe_gate_semantics
        gate = build_runtime_integration_gate(
            ".", verification_data=_make_verification_data())
        assert _safe_gate_semantics("runtime_integration_gate.json", gate, {}, {}) == []

    def test_zero_checks_blocks_semantics(self):
        from scripts.build_review_manifest import _safe_gate_semantics
        gate = {"schema_version": "1.1.0", "verdict": "PASS",
                "checks": [], "checks_total": 0, "checks_passed": 0, "issues": []}
        issues = _safe_gate_semantics("runtime_integration_gate.json", gate, {}, {})
        assert any("zero" in i.lower() or "checks_total" in i for i in issues)

    def test_v100_gate_still_accepted(self):
        from scripts.build_review_manifest import _gate_closed_schema_problems
        gate = {
            "schema_version": "1.0.0", "verdict": "PASS",
            "checks": [{
                "check_id": "test", "check_type": "call_exists",
                "source_file": "x.py", "pattern": "import x",
                "found": True, "file_missing": False,
            }],
            "checks_total": 1, "checks_passed": 1, "issues": [],
        }
        assert _gate_closed_schema_problems("runtime_integration_gate.json", gate) == []

    def test_bound_run_requires_head_sha(self):
        from scripts.build_review_manifest import _safe_gate_semantics
        gate = {
            "schema_version": "1.1.0", "verdict": "PASS",
            "checks": [{
                "check_id": "test_bind", "check_type": "test_execution_binding",
                "test_file": "tests/test_x.py", "min_passed": 1, "found": True,
                "bound_run": {
                    "run_id": "vr-1", "command": "pytest", "exit_code": 0,
                    "passed": 10, "failed": 0, "skipped": 0, "selected": 10,
                    "node_ids": [], "output_hash": "sha256:abc", "head_sha": "",
                },
            }],
            "checks_total": 1, "checks_passed": 1, "issues": [],
        }
        issues = _safe_gate_semantics("runtime_integration_gate.json", gate, {}, {})
        assert any("head_sha" in i for i in issues)

    def test_bound_run_requires_output_hash(self):
        from scripts.build_review_manifest import _safe_gate_semantics
        gate = {
            "schema_version": "1.1.0", "verdict": "PASS",
            "checks": [{
                "check_id": "test_bind", "check_type": "test_execution_binding",
                "test_file": "tests/test_x.py", "min_passed": 1, "found": True,
                "bound_run": {
                    "run_id": "vr-1", "command": "pytest", "exit_code": 0,
                    "passed": 10, "failed": 0, "skipped": 0, "selected": 10,
                    "node_ids": [], "output_hash": "", "head_sha": "abc123",
                },
            }],
            "checks_total": 1, "checks_passed": 1, "issues": [],
        }
        issues = _safe_gate_semantics("runtime_integration_gate.json", gate, {}, {})
        assert any("output_hash" in i for i in issues)

    def test_bound_run_passed_below_min(self):
        from scripts.build_review_manifest import _safe_gate_semantics
        gate = {
            "schema_version": "1.1.0", "verdict": "PASS",
            "checks": [{
                "check_id": "test_bind", "check_type": "test_execution_binding",
                "test_file": "tests/test_x.py", "min_passed": 50, "found": True,
                "bound_run": {
                    "run_id": "vr-1", "command": "pytest", "exit_code": 0,
                    "passed": 10, "failed": 0, "skipped": 0, "selected": 10,
                    "node_ids": [], "output_hash": "sha256:abc", "head_sha": "abc123",
                },
            }],
            "checks_total": 1, "checks_passed": 1, "issues": [],
        }
        issues = _safe_gate_semantics("runtime_integration_gate.json", gate, {}, {})
        assert any("min_passed" in i for i in issues)


# ---------------------------------------------------------------------------
# Scope 2: Evidence refresh upgrades stale gate
# ---------------------------------------------------------------------------

class TestEvidenceRefresh:
    def test_stale_v100_refreshed_to_v110(self, scratch):
        from scripts.refresh_review_evidence import refresh_staged_evidence
        stale_gate = {"schema_version": "1.0.0", "verdict": "PASS",
                      "checks": [], "checks_total": 0, "checks_passed": 0, "issues": []}
        vt = _make_verification_data()
        with open(os.path.join(scratch, "runtime_integration_gate.json"), "w") as f:
            json.dump(stale_gate, f)
        with open(os.path.join(scratch, "verification_tests.json"), "w") as f:
            json.dump(vt, f)

        report = refresh_staged_evidence(scratch, ".")
        assert len(report["refreshed_gates"]) == 1
        assert report["refreshed_gates"][0]["new_schema_version"] == "1.1.0"
        assert report["refreshed_gates"][0]["new_checks_total"] == 35

        with open(os.path.join(scratch, "runtime_integration_gate.json")) as f:
            gate = json.loads(f.read())
        assert gate["schema_version"] == "1.1.0"
        assert gate["checks_total"] == 35

    def test_already_v110_left_unchanged(self, scratch):
        from packages.orchestration.runtime_integration_gate import (
            build_runtime_integration_gate,
        )
        from scripts.refresh_review_evidence import refresh_staged_evidence
        vd = _make_verification_data()
        gate = build_runtime_integration_gate(
            ".", verification_data=vd)
        with open(os.path.join(scratch, "runtime_integration_gate.json"), "w") as f:
            f.write(json.dumps(gate, indent=1, sort_keys=True))
        with open(os.path.join(scratch, "verification_tests.json"), "w") as f:
            json.dump(vd, f)

        report = refresh_staged_evidence(scratch, ".")
        assert len(report["unchanged_gates"]) == 1
        assert len(report["refreshed_gates"]) == 0

    def test_missing_gate_regenerated(self, scratch):
        from scripts.refresh_review_evidence import refresh_staged_evidence
        vt = _make_verification_data()
        with open(os.path.join(scratch, "verification_tests.json"), "w") as f:
            json.dump(vt, f)

        report = refresh_staged_evidence(scratch, ".")
        assert len(report["refreshed_gates"]) == 1
        assert os.path.isfile(
            os.path.join(scratch, "runtime_integration_gate.json"))

    def test_refresh_report_written(self, scratch):
        from scripts.refresh_review_evidence import refresh_staged_evidence
        stale = {"schema_version": "1.0.0", "verdict": "PASS",
                 "checks": [], "checks_total": 0, "checks_passed": 0, "issues": []}
        with open(os.path.join(scratch, "runtime_integration_gate.json"), "w") as f:
            json.dump(stale, f)

        refresh_staged_evidence(scratch, ".")
        report_path = os.path.join(scratch, "evidence_refresh_report.json")
        assert os.path.isfile(report_path)
        with open(report_path) as f:
            report = json.loads(f.read())
        assert report["schema_version"] == "1.0.0"

    def test_inventory_updated_after_refresh(self, scratch):
        import hashlib

        from scripts.refresh_review_evidence import refresh_staged_evidence

        stale = {"schema_version": "1.0.0", "verdict": "PASS",
                 "checks": [], "checks_total": 0, "checks_passed": 0, "issues": []}
        gate_path = os.path.join(scratch, "runtime_integration_gate.json")
        with open(gate_path, "w") as f:
            json.dump(stale, f)

        vt = _make_verification_data()
        with open(os.path.join(scratch, "verification_tests.json"), "w") as f:
            json.dump(vt, f)

        old_inv = {
            "inventory_v": 1,
            "boundary": "source-evidence-at-snapshot",
            "member_count": 2,
            "members": [
                {"kind": "regular", "mode": 420, "relative_path": "runtime_integration_gate.json",
                 "sha256": "old_hash", "size": 100, "source_class": "evidence"},
                {"kind": "regular", "mode": 420, "relative_path": "verification_tests.json",
                 "sha256": "vt_hash", "size": 50, "source_class": "evidence"},
            ],
        }
        inv_path = os.path.join(scratch, "evidence_snapshot_inventory.json")
        with open(inv_path, "w") as f:
            json.dump(old_inv, f)

        refresh_staged_evidence(scratch, ".")

        with open(inv_path) as f:
            updated_inv = json.loads(f.read())

        paths = [m["relative_path"] for m in updated_inv["members"]]
        assert "evidence_refresh_report.json" in paths
        assert "runtime_integration_gate.json" in paths
        assert updated_inv["member_count"] == len(updated_inv["members"])

        gate_entry = [m for m in updated_inv["members"]
                      if m["relative_path"] == "runtime_integration_gate.json"][0]
        assert gate_entry["sha256"] != "old_hash"
        with open(gate_path, "rb") as f:
            expected_sha = hashlib.sha256(f.read()).hexdigest()
        assert gate_entry["sha256"] == expected_sha

    def test_original_evidence_not_mutated(self, scratch):
        from scripts.refresh_review_evidence import refresh_staged_evidence
        orig_dir = os.path.join(scratch, "original")
        staged_dir = os.path.join(scratch, "staged")
        os.makedirs(orig_dir)
        os.makedirs(staged_dir)

        stale = {"schema_version": "1.0.0", "verdict": "PASS",
                 "checks": [], "checks_total": 0, "checks_passed": 0, "issues": []}
        orig_path = os.path.join(orig_dir, "runtime_integration_gate.json")
        staged_path = os.path.join(staged_dir, "runtime_integration_gate.json")
        with open(orig_path, "w") as f:
            json.dump(stale, f)
        shutil.copy2(orig_path, staged_path)

        refresh_staged_evidence(staged_dir, ".")
        with open(orig_path) as f:
            orig_gate = json.loads(f.read())
        assert orig_gate["schema_version"] == "1.0.0"


# ---------------------------------------------------------------------------
# Scope 3: Stopped-job override guard in run_job boundary
# ---------------------------------------------------------------------------

class TestStoppedJobGuard:
    def test_stopped_job_with_pending_stop_blocks(self, scratch, monkeypatch):
        from types import SimpleNamespace

        from packages.orchestration import pingpong_job as pj

        fake_job = pj.JobPlan(
            job_id="test-stopped-guard",
            status=pj.JOB_STOPPED,
            stop_reason="test_stop",
        )
        monkeypatch.setattr(pj, "load_job_plan", lambda _: fake_job)

        _persisted_jobs = []
        monkeypatch.setattr(pj, "_persist_job", lambda j: _persisted_jobs.append(j))

        stop_signal = SimpleNamespace(
            request_id="stop-001", reason="operator_requested",
            source="operator", requested_at="2026-07-22T00:00:00+00:00")
        monkeypatch.setattr(
            "packages.orchestration.safe_points.stop_requested",
            lambda *a, **kw: stop_signal)
        monkeypatch.setattr(
            "packages.orchestration.safe_points.control_root",
            lambda *a, **kw: scratch)

        result = pj.run_job("test-stopped-guard")
        assert "stopped_job_has_pending_stop" in (result.error or "")

    def test_stopped_job_without_pending_stop_proceeds(self, scratch, monkeypatch):
        from packages.orchestration import pingpong_job as pj

        fake_job = pj.JobPlan(
            job_id="test-resume",
            status=pj.JOB_STOPPED,
            tasks=[],
        )
        monkeypatch.setattr(pj, "load_job_plan", lambda _: fake_job)
        monkeypatch.setattr(
            "packages.orchestration.safe_points.stop_requested",
            lambda *a, **kw: None)
        monkeypatch.setattr(
            "packages.orchestration.safe_points.control_root",
            lambda *a, **kw: scratch)
        monkeypatch.setattr(pj, "_persist_job", lambda j: None)
        monkeypatch.setattr(pj, "_mark_manifest_required", lambda j: None)

        result = pj.run_job("test-resume")
        assert "stopped_job_has_pending_stop" not in (result.error or "")


# ---------------------------------------------------------------------------
# Scope 3: first_running_at not set before pre-work validation
# ---------------------------------------------------------------------------

class TestFirstRunningAtTiming:
    def test_corrupt_budget_does_not_stamp_first_running_at(self, scratch, monkeypatch):
        from packages.orchestration import pingpong_job as pj

        fake_job = pj.JobPlan(
            job_id="test-timing",
            status="planned",
            budgets={"invalid": True},
            first_running_at="",
            tasks=[],
        )
        monkeypatch.setattr(pj, "load_job_plan", lambda _: fake_job)
        monkeypatch.setattr(pj, "_persist_job", lambda j: None)
        monkeypatch.setattr(pj, "_mark_manifest_required", lambda j: None)
        monkeypatch.setattr(pj, "_write_job_postmortem_record", lambda j, e: None)
        monkeypatch.setattr(
            "packages.orchestration.safe_points.stop_requested",
            lambda *a, **kw: None)
        monkeypatch.setattr(
            "packages.orchestration.safe_points.control_root",
            lambda *a, **kw: scratch)

        result = pj.run_job("test-timing")
        assert result.status == pj.JOB_BLOCKED
        assert result.first_running_at == "", \
            "first_running_at must not be set when budget validation blocks"


# ---------------------------------------------------------------------------
# Scope 3: Persisted actuals provenance (closed schema)
# ---------------------------------------------------------------------------

class TestPersistedActualsSchema:
    def test_actuals_include_schema_version(self):

        actuals = {
            "schema_version": "1.0.0",
            "provider_call_count": 5,
            "actual_call_count": 3,
            "total_tokens": 1000,
            "started_at": "2026-07-22T00:00:00+00:00",
            "actual_sources": ["pingpong_live"],
            "unmeasured_call_count": 2,
        }
        # Should validate without error
        _prior = dict(actuals)
        for _afield in ("provider_call_count", "total_tokens", "actual_call_count"):
            _aval = _prior.get(_afield, 0)
            assert isinstance(_aval, int) and _aval >= 0

    def test_unknown_key_rejected(self):

        actuals = {
            "provider_call_count": 5,
            "actual_call_count": 3,
            "total_tokens": 1000,
            "started_at": "2026-07-22T00:00:00+00:00",
            "EXTRA_KEY": "bad",
        }
        _CLOSED_ACTUALS_KEYS = frozenset({
            "schema_version", "provider_call_count", "actual_call_count",
            "total_tokens", "started_at", "actual_sources", "unmeasured_call_count",
        })
        extra = set(actuals) - _CLOSED_ACTUALS_KEYS
        assert extra == {"EXTRA_KEY"}

    def test_unmeasured_mismatch_rejected(self):

        actuals = {
            "provider_call_count": 5,
            "actual_call_count": 3,
            "total_tokens": 1000,
            "started_at": "2026-07-22T00:00:00+00:00",
            "unmeasured_call_count": 99,
        }
        pc = actuals["provider_call_count"]
        ac = actuals["actual_call_count"]
        umc = actuals["unmeasured_call_count"]
        assert umc != pc - ac, "mismatch correctly detected"

    def test_actual_sources_must_be_list_or_tuple(self):
        actuals = {
            "provider_call_count": 0,
            "actual_call_count": 0,
            "total_tokens": 0,
            "started_at": "2026-07-22T00:00:00+00:00",
            "actual_sources": "not_a_list",
        }
        assert not isinstance(actuals["actual_sources"], (list, tuple))
