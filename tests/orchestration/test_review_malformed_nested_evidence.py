"""F4 (round 28) — a document that decodes to valid JSON but carries a MALFORMED nested shape must
append controlled validation errors, never raise AttributeError/TypeError from a ``.get`` on a
non-dict. The manifest builder always returns a valid root manifest; ``validate_evidence_candidate``
always returns a result whose candidate is invalid."""
from __future__ import annotations

import importlib.util
import json
import os
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_b = importlib.util.spec_from_file_location(
    "_brm_malformed", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_b); _b.loader.exec_module(_brm)


def _view(job_flow):
    return _brm._EvidenceView({"job_flow.json": json.dumps(job_flow).encode()})


class TestJobFlowShapeProblems:
    def test_final_audit_list_is_a_problem_not_a_crash(self):
        p = _brm._job_flow_shape_problems({"job_id": "e2e", "final_audit": []})
        assert any("final_audit is not an object" in x for x in p)

    def test_target_guard_list_is_a_problem(self):
        p = _brm._job_flow_shape_problems(
            {"job_id": "e2e", "final_audit": {"status": "pass"}, "target_guard": []})
        assert any("target_guard is not an object" in x for x in p)

    def test_non_bool_mutated_target_is_a_problem(self):
        p = _brm._job_flow_shape_problems(
            {"job_id": "e2e", "final_audit": {"status": "pass"},
             "target_guard": {"mutated_target": "yes"}})
        assert any("mutated_target is not a boolean" in x for x in p)

    def test_empty_job_id_and_status(self):
        p = _brm._job_flow_shape_problems({"job_id": "", "final_audit": {"status": ""}})
        assert any("job_id is not a non-empty string" in x for x in p)
        assert any("final_audit.status is not a non-empty string" in x for x in p)

    def test_missing_obs_not_a_list(self):
        p = _brm._job_flow_shape_problems(
            {"job_id": "e2e", "final_audit": {"status": "p", "missing_observability_artifacts": "x"}})
        assert any("missing_observability_artifacts is not a list" in x for x in p)

    def test_non_object_root(self):
        assert _brm._job_flow_shape_problems([]) == ["job_flow.json: root is not a JSON object"]

    def test_well_formed_has_no_problems(self):
        assert _brm._job_flow_shape_problems(
            {"job_id": "e2e", "final_audit": {"status": "PASS"}}) == []


class TestCandidateNeverThrows:
    REPRO = [
        {"job_id": "e2e", "final_audit": []},
        {"job_id": "e2e", "final_audit": {"status": "pass"}, "target_guard": []},
        {"job_id": "e2e", "final_audit": {"status": "pass"},
         "target_guard": {"mutated_target": "yes"}},
        {"job_id": "e2e", "final_audit": {"status": "p", "missing_observability_artifacts": "x"}},
    ]

    def test_each_reproduction_blocks_without_raising(self):
        for jf in self.REPRO:
            r = _brm.validate_evidence_candidate(_view(jf))
            assert r["is_valid_current_run"] is False, jf

    def test_manifest_builder_returns_valid_root_on_malformed_disk(self):
        for jf in self.REPRO:
            d = tempfile.mkdtemp()
            with open(os.path.join(d, "job_flow.json"), "w") as fh:
                json.dump(jf, fh)
            os.makedirs(os.path.join(d, "task_runs", "T001"))
            manifest = _brm.build_manifest(d)              # must NOT raise
            assert isinstance(manifest, dict)
            assert "review_subject" in manifest
            assert _brm.validate_evidence_candidate(d)["is_valid_current_run"] is False
