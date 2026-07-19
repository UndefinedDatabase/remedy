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
            "test_files": ["a.py"], "timestamp": "2026-07-18T00:00:00Z"}
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


class TestProducerCoherence:
    """F2 (round 28) — VerificationTestsV1 is the exact job_evidence._run_verifications contract:
    repeated commands are legitimate, the top-level command/exit are producer-derived views of the
    runs, and the timestamp must be a timezone-aware datetime."""

    def _produce(self, commands, runner=None):
        from packages.orchestration.job_evidence import _run_verifications
        runner = runner or (lambda c: {"exit_code": 0, "passed": 1, "failed": 0,
                                       "test_files": ["a.py"], "stdout_summary": "1 passed"})
        return _run_verifications(commands, repo=".", runner=runner)

    def test_duplicate_commands_distinct_run_ids_pass(self):
        vt = self._produce(["pytest -q a.py", "pytest -q a.py"])
        assert vt["runs"][0]["run_id"] != vt["runs"][1]["run_id"]
        assert _brm.validate_verification_tests(vt)[0] == []

    def test_duplicate_run_id_blocks(self):
        vt = self._produce(["pytest -q a.py", "pytest -q b.py"])
        vt["runs"][1]["run_id"] = vt["runs"][0]["run_id"]
        assert _brm.validate_verification_tests(vt)[0]

    def test_forged_top_command_blocks(self):
        vt = self._produce(["pytest -q a.py", "pytest -q b.py"])
        vt["command"] = "echo harmless"
        assert _brm.validate_verification_tests(vt)[0]

    def test_reordered_distinct_run_commands_break_derived_top(self):
        vt = self._produce(["pytest -q a.py", "pytest -q b.py"])
        vt["runs"].reverse()                                # top-level command now stale
        assert _brm.validate_verification_tests(vt)[0]

    def test_date_only_timestamp_blocks(self):
        vt = self._produce(["pytest -q a.py"])
        vt["timestamp"] = "2026-07-19"
        assert _brm.validate_verification_tests(vt)[0]

    def test_naive_datetime_blocks(self):
        vt = self._produce(["pytest -q a.py"])
        vt["timestamp"] = "2026-07-19T00:00:00"
        assert _brm.validate_verification_tests(vt)[0]

    def test_z_timestamp_passes(self):
        vt = self._produce(["pytest -q a.py"])
        vt["timestamp"] = "2026-07-19T00:00:00Z"
        assert _brm.validate_verification_tests(vt)[0] == []

    def test_explicit_offsets_pass(self):
        for ts in ("2026-07-19T00:00:00+00:00", "2026-07-19T00:00:00+05:30"):
            vt = self._produce(["pytest -q a.py"])
            vt["timestamp"] = ts
            assert _brm.validate_verification_tests(vt)[0] == [], ts

    def test_zero_test_utility_command_valid_with_real_tests_elsewhere(self):
        # A static command (0 passed) is legitimate as long as the aggregate proves >= 1 test.
        def runner(c):
            if "compileall" in c:
                return {"exit_code": 0, "passed": 0, "failed": 0, "test_files": [],
                        "stdout_summary": ""}
            return {"exit_code": 0, "passed": 3, "failed": 0, "test_files": ["a.py"],
                    "stdout_summary": "3 passed"}
        vt = self._produce(["pytest -q a.py", "python -m compileall -q ."], runner)
        assert _brm.validate_verification_tests(vt)[0] == []
