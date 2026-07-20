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
    REQUIRED_F012_VERIFICATION_SUITES,
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


class TestRequiredF012Suites:
    """Round 40 F4: the required suite constant is non-empty and the completeness validator
    enforces it — a verification_tests missing a required suite blocks."""

    def test_required_suites_constant_is_nonempty(self):
        assert len(REQUIRED_F012_VERIFICATION_SUITES) >= 4

    def test_all_required_suites_are_strings(self):
        for s in REQUIRED_F012_VERIFICATION_SUITES:
            assert isinstance(s, str) and s.strip()

    def test_missing_required_suite_detected(self):
        vt = _full([_run(command="pytest tests/orchestration/test_unrelated.py -q")])
        problems = validate_verification_completeness(vt, REQUIRED_F012_VERIFICATION_SUITES)
        assert any("missing required" in p for p in problems)

    def test_all_required_suites_covered_passes(self):
        runs = []
        for i, suite in enumerate(REQUIRED_F012_VERIFICATION_SUITES):
            runs.append(_run(
                run_id=f"vr-{i+1:04d}",
                command=f"pytest tests/orchestration/{suite}.py -q",
                test_files=[f"tests/orchestration/{suite}.py"]))
        vt = _full(runs)
        problems = validate_verification_completeness(vt, REQUIRED_F012_VERIFICATION_SUITES)
        assert not any("missing required" in p for p in problems)


def _diag_view(objs):
    """Build an _EvidenceView from the SAME module as validate_evidence_candidate."""
    import json as _json
    files = {}
    for rel, o in objs.items():
        if isinstance(o, bytes):
            files[rel] = o
        else:
            files[rel] = _json.dumps(o).encode()
    return _brm._EvidenceView(files)


def _diag_valid():
    """Minimal manual bundle for diagnostic tests."""
    return {
        "manifest.json": {"job_id": "j1", "task_ids": ["T001"], "task_count": 1},
        "final_job_review.json": {
            "job_id": "j1", "completion_mode": "manual_operator_repair",
            "human_final_reviewer_required": True, "completion_provider_call_count": 0,
            "linked_prior_job_ids": [], "linked_prior_job_summaries": [],
            "per_task_changed_files": {"T001": ["src/a.py"]},
            "actual_changed_files": ["src/a.py"], "expected_changed_files": ["src/a.py"]},
        "current_change_content_proof.json": {
            "file_hashes": {"src/a.py": "0" * 64}, "tombstones": {},
            "base_commit": "a" * 40, "head_commit": "b" * 40},
        "final_verifier_report.json": {
            "authoritative_changed_files": ["src/a.py"],
            "test_status": {"ran": True, "passed": 1, "failed": 0},
            "review_subject_uncovered_files": [], "content_hash_mismatches": [],
            "file_set_alignment_status": "PASS", "manual_completion": True,
            "human_final_reviewer_required": True,
            "operator_attested_tasks": ["T001"]},
        "change_provenance_gate.json": {
            "covered_files": ["src/a.py"], "hash_mismatches": [], "uncovered_files": []},
        "verification_tests.json": {
            "schema_version": "1.0.0", "verification_type": "explicit_commands",
            "runs": [{"run_id": "vr-0001", "command": "pytest -q", "exit_code": 0, "passed": 1,
                      "failed": 0, "test_files": ["src/a.py"], "stdout_summary": "1 passed"}],
            "command": "pytest -q", "exit_code": 0, "passed": 1, "failed": 0,
            "test_files": ["src/a.py"], "timestamp": "2026-07-19T00:00:00Z"},
        "review_subject.json": {"subject_v": 1, "base_commit": "a" * 40, "head_commit": "b" * 40,
                                "commits": [], "files": []},
        "review_commit_chain.json": {"chain_v": 1, "base_commit": "a" * 40, "head_commit": "b" * 40,
                                     "commits": []},
        "task_runs/T001/manual_repair_provenance.json": {
            "manual_operator_repair": True, "no_provider_calls": True, "job_id": "j1",
            "task_id": "T001", "note": "x", "provenance_sha256": "0" * 64, "diff_sha256": "0" * 64,
            "tracked_diff_sha256": "0" * 64, "changed_files": ["src/a.py"],
            "task_scoped_files": ["src/a.py"], "untracked_file_hashes": []},
        "task_runs/T001/review.json": {"final_verdict": "operator_attested",
                                       "human_final_reviewer_required": True},
        "task_runs/T001/provider_evidence.json": {"execution_mode": "manual_operator_repair",
                                                  "schema_version": "1.0.0",
                                                  "provider_call_count": 0,
                                                  "completion_provider_call_count": 0,
                                                  "prompt_trace_available": False,
                                                  "actual_provider_available": False},
        "task_runs/T001/token_accounting.json": {"task_id": "T001", "kind": "manual",
                                                 "reason": "manual", "provider_call_count": 0,
                                                 "actual_available": False},
        "task_runs/T001/manifest.json": {"evidence_available": True,
                                         "effective_status": "operator_attested_complete"},
        "task_runs/T001/safe.diff": b"--- a/src/a.py\n+++ b/src/a.py\n",
    }


class TestDiagnosticStalenessBlocks:
    """Round 40 F4: validate_evidence_candidate rejects a stale diagnostic_broad_run.json."""

    def test_stale_diagnostic_blocks(self):
        import copy
        objs = copy.deepcopy(_diag_valid())
        objs["diagnostic_broad_run.json"] = {"head_commit": "a" * 40}
        ev = _diag_view(objs)
        vc = _brm.validate_evidence_candidate(ev)
        assert any("stale HEAD" in e for e in vc["validation_errors"])

    def test_matching_diagnostic_has_no_staleness_error(self):
        import copy
        objs = copy.deepcopy(_diag_valid())
        objs["diagnostic_broad_run.json"] = {"head_commit": "b" * 40}
        ev = _diag_view(objs)
        vc = _brm.validate_evidence_candidate(ev)
        assert not any("stale HEAD" in e for e in vc["validation_errors"])
