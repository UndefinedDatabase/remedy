"""Round 39 F3 — verification matrix producer/completeness-validator contract tests.

Every producer output conforms to the existing VerificationTestsV1 schema. Top-level
fields are derived from runs, never caller-asserted. Completeness checks detect
missing suites and inconsistent counts.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

from packages.orchestration.verification_matrix import (
    VERIFICATION_TESTS_SCHEMA_VERSION,
    VerificationMatrixError,
    produce_verification_run,
    produce_verification_tests,
    validate_verification_completeness,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
_brm_spec = importlib.util.spec_from_file_location(
    "_brm_vm", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_brm_spec)
_brm_spec.loader.exec_module(_brm)


def _run(run_id="vr-0001", command="pytest tests/a.py -q", exit_code=0,
         passed=10, failed=0, test_files=None, stdout_summary="10 passed"):
    return produce_verification_run(
        run_id=run_id, command=command, exit_code=exit_code,
        passed=passed, failed=failed,
        test_files=test_files or ["tests/a.py"],
        stdout_summary=stdout_summary)


def _full(runs=None, timestamp="2026-07-20T12:00:00+00:00"):
    if runs is None:
        runs = [_run()]
    return produce_verification_tests(runs=runs, timestamp=timestamp)


class TestProducerOutputPassesExistingValidator:
    def test_single_run(self):
        vt = _full()
        problems, passed = _brm.validate_verification_tests(vt)
        assert problems == [] and passed == 10

    def test_multiple_runs(self):
        runs = [
            _run(run_id="vr-0001", command="pytest tests/a.py -q", passed=10,
                 test_files=["tests/a.py"]),
            _run(run_id="vr-0002", command="pytest tests/b.py -q", passed=20,
                 test_files=["tests/b.py"]),
        ]
        vt = _full(runs=runs)
        problems, passed = _brm.validate_verification_tests(vt)
        assert problems == [] and passed == 30

    def test_derived_command_is_join(self):
        runs = [
            _run(run_id="vr-0001", command="cmd1"),
            _run(run_id="vr-0002", command="cmd2"),
        ]
        vt = _full(runs=runs)
        assert vt["command"] == "cmd1 && cmd2"

    def test_derived_exit_code_all_zero(self):
        vt = _full()
        assert vt["exit_code"] == 0

    def test_derived_test_files_union(self):
        runs = [
            _run(run_id="vr-0001", test_files=["a.py", "b.py"]),
            _run(run_id="vr-0002", test_files=["b.py", "c.py"]),
        ]
        vt = _full(runs=runs)
        assert vt["test_files"] == ["a.py", "b.py", "c.py"]


class TestRunProducerRejectsInvalid:
    def test_bad_run_id(self):
        with pytest.raises(VerificationMatrixError, match="run_id"):
            _run(run_id="bad")

    def test_empty_command(self):
        with pytest.raises(VerificationMatrixError, match="command"):
            _run(command="")

    def test_bool_exit_code(self):
        with pytest.raises(VerificationMatrixError, match="exit_code"):
            _run(exit_code=True)

    def test_bool_passed(self):
        with pytest.raises(VerificationMatrixError, match="passed"):
            _run(passed=True)

    def test_negative_passed(self):
        with pytest.raises(VerificationMatrixError, match="passed"):
            _run(passed=-1)

    def test_negative_failed(self):
        with pytest.raises(VerificationMatrixError, match="failed"):
            _run(failed=-1)


class TestTestsProducerRejectsInvalid:
    def test_empty_runs(self):
        with pytest.raises(VerificationMatrixError, match="at least one"):
            produce_verification_tests(runs=[], timestamp="2026-07-20T12:00:00+00:00")

    def test_missing_timestamp(self):
        with pytest.raises(VerificationMatrixError, match="timestamp"):
            produce_verification_tests(runs=[_run()], timestamp="")

    def test_duplicate_run_id(self):
        with pytest.raises(VerificationMatrixError, match="duplicate"):
            produce_verification_tests(
                runs=[_run(run_id="vr-0001"), _run(run_id="vr-0001")],
                timestamp="2026-07-20T12:00:00+00:00")


class TestCompletenessValidator:
    def test_complete_matrix(self):
        runs = [
            _run(run_id="vr-0001", command="pytest tests/a.py"),
            _run(run_id="vr-0002", command="pytest tests/b.py"),
        ]
        vt = _full(runs=runs)
        problems = validate_verification_completeness(vt, ["tests/a.py", "tests/b.py"])
        assert problems == []

    def test_missing_suite(self):
        vt = _full()
        problems = validate_verification_completeness(
            vt, ["tests/a.py", "tests/missing.py"])
        assert any("missing required suites" in p for p in problems)

    def test_count_mismatch(self):
        vt = _full()
        vt["passed"] = 999
        problems = validate_verification_completeness(vt, [])
        assert any("sum of runs" in p for p in problems)

    def test_failed_count_mismatch(self):
        vt = _full()
        vt["failed"] = 999
        problems = validate_verification_completeness(vt, [])
        assert any("sum of runs" in p for p in problems)

    def test_duplicate_run_id_detected(self):
        vt = _full()
        vt["runs"].append(dict(vt["runs"][0]))
        problems = validate_verification_completeness(vt, [])
        assert any("duplicate" in p for p in problems)

    def test_not_a_dict(self):
        problems = validate_verification_completeness("bad", [])
        assert any("not a dict" in p for p in problems)

    def test_runs_not_a_list(self):
        problems = validate_verification_completeness({"runs": "bad"}, [])
        assert any("not a list" in p for p in problems)


class TestSchemaVersion:
    def test_version_is_1_0_0(self):
        assert VERIFICATION_TESTS_SCHEMA_VERSION == "1.0.0"

    def test_producer_emits_version(self):
        vt = _full()
        assert vt["schema_version"] == "1.0.0"
