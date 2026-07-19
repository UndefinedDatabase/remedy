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
                                                  "actual_provider_available": False},
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
