"""F3 (round 26) — strict, fail-closed VerificationTestsV1. Missing/invalid/unsupported/type-
mismatched/incoherent verification totals block, with no int() coercion, and the FV total must equal
the recorded verification total."""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_b = importlib.util.spec_from_file_location(
    "_brm_vt", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_b); _b.loader.exec_module(_brm)
_e = importlib.util.spec_from_file_location(
    "_e2e_vt", REPO_ROOT / "tests" / "orchestration" / "test_review_authoritative_e2e.py")
_E2E = importlib.util.module_from_spec(_e); _e.loader.exec_module(_E2E)


def _vt(**over):
    base = {"schema_version": "1.0.0", "verification_type": "explicit_commands",
            "runs": [{"run_id": "vr-0001", "command": "pytest -q", "exit_code": 0, "passed": 3,
                      "failed": 0, "test_files": ["a.py"], "stdout_summary": "3 passed"}],
            "command": "pytest -q", "exit_code": 0, "passed": 3, "failed": 0,
            "test_files": ["a.py"], "timestamp": "t"}
    base.update(over)
    return base


class TestStrictValidator:
    def test_valid_record_passes(self):
        problems, passed = _brm.validate_verification_tests(_vt())
        assert problems == [] and passed == 3

    def test_missing_blocks(self):
        problems, _ = _brm.validate_verification_tests(None)
        assert problems

    def test_string_passed_blocks_no_coercion(self):
        problems, _ = _brm.validate_verification_tests(_vt(passed="9999"))
        assert any("real integer" in p for p in problems)

    def test_bool_passed_blocks(self):
        problems, _ = _brm.validate_verification_tests(_vt(passed=True))
        assert problems

    def test_bad_version_blocks(self):
        assert _brm.validate_verification_tests(_vt(schema_version="2.0.0"))[0]

    def test_nonzero_failed_blocks(self):
        assert _brm.validate_verification_tests(_vt(failed=2))[0]

    def test_nonzero_exit_blocks(self):
        assert _brm.validate_verification_tests(_vt(exit_code=1))[0]

    def test_total_not_sum_of_runs_blocks(self):
        assert _brm.validate_verification_tests(_vt(passed=5))[0]

    def test_unknown_top_field_blocks(self):
        assert _brm.validate_verification_tests(_vt(surprise=1))[0]

    def test_run_wrong_field_set_blocks(self):
        vt = _vt()
        vt["runs"][0]["extra"] = 1
        assert _brm.validate_verification_tests(vt)[0]

    def test_test_files_union_incoherent_blocks(self):
        assert _brm.validate_verification_tests(_vt(test_files=["a.py", "ghost.py"]))[0]

    def test_duplicate_run_id_blocks(self):
        vt = _vt()
        vt["runs"].append(dict(vt["runs"][0]))
        vt["passed"] = 6
        assert _brm.validate_verification_tests(vt)[0]


class TestGateMatrixFailClosed:
    def _gates(self):
        return {k: copy.deepcopy(v) for k, v in _E2E._complete_gates().items()}

    def test_absent_verification_blocks_ready(self):
        g = self._gates()
        del g["verification_tests.json"]
        assert _brm.evaluate_ready_gate_matrix(lambda n: g.get(n))["ok"] is False

    def test_fv_total_mismatch_blocks(self):
        g = self._gates()
        g["final_verifier_report.json"]["test_status"]["passed"] = 999
        assert _brm.evaluate_ready_gate_matrix(lambda n: g.get(n))["ok"] is False

    def test_matching_total_passes(self):
        assert _brm.evaluate_ready_gate_matrix(
            lambda n: self._gates().get(n))["ok"] is True
