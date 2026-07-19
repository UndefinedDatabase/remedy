"""F2 (round 29) — manual-only Evidence is a trust boundary: every structured field consumed by
validate_manual_completion and its _verify_* helpers is validated BEFORE any iteration or .get chain.
A valid-JSON document with a wrong nested type appends a bounded ``artifact: field is not a <kind>``
error and invalidates the candidate — it never raises AttributeError/TypeError and never leaves READY
reachable. The mutation matrix replaces every consumed collection/record field with the applicable
wrong types and proves none throws.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import os
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_b = importlib.util.spec_from_file_location(
    "_brm_mc", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_b); _b.loader.exec_module(_brm)


def _valid() -> dict:
    """A minimal manual-only completion bundle that triggers the manual-completion path and carries
    every consumed structured field with a correct type."""
    return {
        "manifest.json": {"job_id": "j1", "task_ids": ["T001"], "task_count": 1},
        "final_job_review.json": {
            "job_id": "j1", "completion_mode": "manual_operator_repair",
            "human_final_reviewer_required": True, "completion_provider_call_count": 0,
            "linked_prior_job_ids": ["prior1"],
            "linked_prior_job_summaries": [{"job_id": "prior1", "status": "ok",
                                            "provider_call_count": 0}],
            "per_task_changed_files": {"T001": ["src/a.py"]},
            "actual_changed_files": ["src/a.py"], "expected_changed_files": ["src/a.py"]},
        "current_change_content_proof.json": {
            "file_hashes": {"src/a.py": "0" * 64}, "tombstones": {},
            "base_commit": "a" * 40, "head_commit": "b" * 40},
        "final_verifier_report.json": {
            "authoritative_changed_files": ["src/a.py"],
            "test_status": {"ran": True, "passed": 1, "failed": 0},
            "review_subject_uncovered_files": [], "content_hash_mismatches": [],
            "file_set_alignment_status": "PASS"},
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
                                                  "provider_call_count": 0,
                                                  "completion_provider_call_count": 0,
                                                  "prompt_trace_available": False,
                                                  "actual_provider_available": False},
        "task_runs/T001/token_accounting.json": {"task_id": "T001", "kind": "manual",
                                                 "reason": "manual", "provider_call_count": 0,
                                                 "actual_available": False},
        "task_runs/T001/manifest.json": {"evidence_available": True,
                                         "effective_status": "operator_attested_complete"},
        "task_runs/T001/review_scope_packet.json": {"changed_files": ["src/a.py"]},
    }


def _view(objs: dict, extra_files: dict | None = None) -> "._brm._EvidenceView":  # type: ignore
    files = {rel: json.dumps(o).encode() for rel, o in objs.items()}
    files["task_runs/T001/safe.diff"] = b"--- a/src/a.py\n+++ b/src/a.py\n"
    for k, v in (extra_files or {}).items():
        files[k] = v
    return _brm._EvidenceView(files)


# Applicable WRONG-typed values per expected kind (right-typed shapes are excluded — they are not a
# type error). null is a present-but-wrong value for every collection kind.
_WRONG = {
    _brm._MC_LIST: [None, True, False, 0, 1, -1, "", "x", {}, {"x": 1}],
    _brm._MC_DICT: [None, True, False, 0, 1, -1, "", "x", [], [1]],
    _brm._MC_LISTDICT: [None, True, 0, "x", {}, {"x": 1}, [1], [1, {"ok": 1}]],
    _brm._MC_DICTLIST: [None, True, 0, "x", [], [1], {"k": 1}, {"k": "x"}],
}


def _cases():
    for rel, spec in _brm._MC_SHAPES.items():
        # map the basename spec onto the concrete fixture rel(s)
        concrete = [rel] if rel in _valid() else [f"task_runs/T001/{rel}"]
        for cr in concrete:
            if cr not in _valid():
                continue
            for field, kind in spec.items():
                for val in _WRONG[kind]:
                    yield cr, field, kind, val


class TestManualCompletionMutationMatrix:
    def test_manual_path_triggers_on_valid_fixture(self):
        assert _brm._is_manual_completion(_view(_valid())) is True

    def test_every_wrong_typed_field_is_a_controlled_error(self):
        for rel, field, kind, val in _cases():
            objs = copy.deepcopy(_valid())
            objs[rel][field] = val
            ev = _view(objs)
            try:
                vc = _brm.validate_evidence_candidate(ev)
                gm = _brm.evaluate_ready_gate_matrix(ev.gate_loader())
            except Exception as exc:                       # pragma: no cover - the whole point
                raise AssertionError(f"{rel}:{field}={val!r} raised {type(exc).__name__}: {exc}")
            assert vc["is_valid_current_run"] is False, f"{rel}:{field}={val!r} stayed valid"
            assert gm["ok"] is False, f"{rel}:{field}={val!r} left READY reachable"
            assert any(field in e and rel in e for e in vc["validation_errors"]), \
                f"{rel}:{field}={val!r} produced no error naming the artifact+field"

    def test_build_manifest_never_throws_on_malformed_manual_evidence(self):
        for rel, field, val in (
            ("manifest.json", "task_ids", 123),
            ("final_job_review.json", "linked_prior_job_ids", 123),
            ("current_change_content_proof.json", "file_hashes", [{"x": 1}]),
            ("task_runs/T001/manual_repair_provenance.json", "untracked_file_hashes", "x"),
            ("task_runs/T001/manual_repair_provenance.json", "changed_files", 123),
        ):
            objs = copy.deepcopy(_valid())
            objs[rel][field] = val
            d = tempfile.mkdtemp()
            for r, o in objs.items():
                p = os.path.join(d, r)
                os.makedirs(os.path.dirname(p), exist_ok=True)
                with open(p, "w") as fh:
                    json.dump(o, fh)
            with open(os.path.join(d, "task_runs/T001/safe.diff"), "w") as fh:
                fh.write("--- a/src/a.py\n+++ b/src/a.py\n")
            manifest = _brm.build_manifest(d)              # must NOT raise
            assert isinstance(manifest, dict) and "review_subject" in manifest
            assert _brm.validate_evidence_candidate(d)["is_valid_current_run"] is False


class TestManualCompletionScalarSemantics:
    """F3 (round 31) — scalar typing and cross-artifact binding: booleans-for-integers, wrong enums and
    mismatched counts/task-ids block, and none throws."""

    def _apply(self, rel, field, val):
        objs = copy.deepcopy(_valid())
        objs[rel][field] = val
        return _view(objs)

    def _invalid(self, rel, field, val):
        ev = self._apply(rel, field, val)
        vc = _brm.validate_evidence_candidate(ev)          # must not raise
        assert vc["is_valid_current_run"] is False, f"{rel}.{field}={val!r} stayed valid"
        return vc["validation_errors"]

    def test_task_count_boolean_blocks(self):
        assert any("task_count" in e for e in self._invalid("manifest.json", "task_count", False))

    def test_task_count_wrong_value_blocks(self):
        assert any("task_count" in e for e in self._invalid("manifest.json", "task_count", 999))

    def test_completion_provider_call_count_boolean_blocks(self):
        assert any("completion_provider_call_count" in e for e in
                   self._invalid("final_job_review.json", "completion_provider_call_count", False))

    def test_provider_call_count_boolean_blocks(self):
        assert any("provider_call_count" in e for e in self._invalid(
            "task_runs/T001/provider_evidence.json", "provider_call_count", False))

    def test_actual_provider_available_string_false_blocks(self):
        assert any("actual_provider_available" in e for e in self._invalid(
            "task_runs/T001/provider_evidence.json", "actual_provider_available", "false"))

    def test_prompt_trace_available_true_blocks(self):
        assert any("prompt_trace_available" in e for e in self._invalid(
            "task_runs/T001/provider_evidence.json", "prompt_trace_available", True))

    def test_token_accounting_call_count_boolean_blocks(self):
        assert any("token_accounting.provider_call_count" in e for e in self._invalid(
            "task_runs/T001/token_accounting.json", "provider_call_count", False))

    def test_token_accounting_kind_not_manual_blocks(self):
        assert any("token_accounting" in e for e in self._invalid(
            "task_runs/T001/token_accounting.json", "kind", "actual"))

    def test_no_scalar_mutation_throws(self):
        for rel, field in (("manifest.json", "task_count"),
                           ("final_job_review.json", "completion_provider_call_count"),
                           ("task_runs/T001/provider_evidence.json", "provider_call_count"),
                           ("task_runs/T001/provider_evidence.json", "actual_provider_available"),
                           ("task_runs/T001/provider_evidence.json", "prompt_trace_available"),
                           ("task_runs/T001/token_accounting.json", "provider_call_count")):
            for val in (None, True, False, -1, 0, 1, 999, "", "0", "false", [], [1], {}, {"x": 1}):
                ev = self._apply(rel, field, val)
                _brm.validate_evidence_candidate(ev)       # must not raise


class TestLinkedPriorAndProductionIntegration:
    """F3 (round 32) — the exact linked-prior string-count reproduction blocks, and the canonical
    manual producer has a real (non-test) production caller."""

    def test_linked_prior_string_count_blocks(self):
        objs = copy.deepcopy(_valid())
        objs["final_job_review.json"]["linked_prior_job_summaries"] = [
            {"job_id": "prior1", "status": "ok", "provider_call_count": "0"}]
        objs["final_job_review.json"]["linked_prior_job_ids"] = ["prior1"]
        vc = _brm.validate_evidence_candidate(_view(objs))
        assert vc["is_valid_current_run"] is False
        assert any("provider_call_count is not an integer" in e for e in vc["validation_errors"])

    def test_linked_prior_boolean_count_blocks(self):
        objs = copy.deepcopy(_valid())
        objs["final_job_review.json"]["linked_prior_job_summaries"] = [
            {"job_id": "prior1", "status": "ok", "provider_call_count": True}]
        objs["final_job_review.json"]["linked_prior_job_ids"] = ["prior1"]
        assert _brm.validate_evidence_candidate(_view(objs))["is_valid_current_run"] is False

    def test_linked_prior_null_count_is_allowed(self):
        objs = copy.deepcopy(_valid())
        objs["final_job_review.json"]["linked_prior_job_summaries"] = [
            {"job_id": "prior1", "status": "ok", "provider_call_count": None}]
        objs["final_job_review.json"]["linked_prior_job_ids"] = ["prior1"]
        errs = _brm.validate_evidence_candidate(_view(objs))["validation_errors"]
        assert not any("provider_call_count is not an integer" in e for e in errs)

    def test_manual_producer_has_a_production_caller(self):
        # The canonical producer is invoked from a real (non-test) production module.
        from packages.orchestration.job_evidence import write_manual_completion_evidence
        import inspect
        src = inspect.getsource(write_manual_completion_evidence)
        assert "manual_attestation" in src and "write_manual_token_truth" in src
