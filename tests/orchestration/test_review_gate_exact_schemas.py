"""F1 (round 24) — every READY gate is validated by an EXACT, closed recursive schema.

The round-23 validator was a partial field checklist: it confirmed a handful of fields were present
and equal, but it neither rejected UNKNOWN fields (so an injected field rode through), nor enforced
the complete internal truth of the fresh/artifact/runtime gates. This suite pins the closed schema:
an unknown field blocks, the version is closed to {"1.0.0"}, required_artifacts must all be true,
and each runtime check must carry exactly its field set with found/not-missing/known type and a
unique, path-safe id.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_b = importlib.util.spec_from_file_location(
    "_brm_exact", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_b); _b.loader.exec_module(_brm)
_e = importlib.util.spec_from_file_location(
    "_e2e_exact", REPO_ROOT / "tests" / "orchestration" / "test_review_authoritative_e2e.py")
_E2E = importlib.util.module_from_spec(_e); _e.loader.exec_module(_E2E)


def _gates(fname=None, **patch):
    g = {k: dict(v) for k, v in _E2E._complete_gates().items()}
    if fname is not None:
        g[fname] = {**g[fname], **patch}
    return g


def _ok(g):
    return _brm.evaluate_ready_gate_matrix(lambda name: g.get(name))["ok"]


def test_the_complete_closed_matrix_passes():
    assert _ok(_gates()) is True


class TestUnknownFieldsBlock:
    def test_unknown_field_on_fresh_blocks(self):
        assert _ok(_gates("fresh_evidence_gate.json", injected_secret_field=1)) is False

    def test_unknown_field_on_final_verifier_blocks(self):
        assert _ok(_gates("final_verifier_report.json", surprise="x")) is False

    def test_unknown_field_on_artifact_blocks(self):
        assert _ok(_gates("artifact_contract_gate.json", extra=True)) is False

    def test_unknown_field_on_runtime_blocks(self):
        assert _ok(_gates("runtime_integration_gate.json", extra=[])) is False

    def test_unknown_field_on_commit_blocks(self):
        assert _ok(_gates("commit_execution_gate.json", extra=1)) is False


class TestVersionClosed:
    def test_wrong_version_blocks_each_gate(self):
        for name in ("final_verifier_report.json", "fresh_evidence_gate.json",
                     "artifact_contract_gate.json", "change_provenance_gate.json",
                     "runtime_integration_gate.json", "manifest_integrity.json",
                     "postmortem_integrity.json", "commit_execution_gate.json"):
            assert _ok(_gates(name, schema_version="2.0.0")) is False, name


class TestFreshEvidenceComplete:
    def test_job_id_match_false_blocks(self):
        assert _ok(_gates("fresh_evidence_gate.json", job_id_match=False)) is False

    def test_nested_step_range_false_blocks(self):
        assert _ok(_gates("fresh_evidence_gate.json",
                          evidence_freshness={"is_fresh": True, "job_id_match": True,
                                              "step_range_match": False})) is False

    def test_validity_current_run_false_blocks(self):
        assert _ok(_gates("fresh_evidence_gate.json",
                          evidence_validity={"has_job_id": True, "has_manifest": True,
                                             "is_valid_current_run": False})) is False


class TestArtifactRequiredArtifacts:
    def test_a_false_required_artifact_blocks(self):
        assert _ok(_gates("artifact_contract_gate.json",
                          required_artifacts={"manifest.json": False,
                                              "final_verifier_report.json": True})) is False

    def test_job_id_not_fresh_blocks(self):
        assert _ok(_gates("artifact_contract_gate.json", job_id_fresh=False)) is False


class TestRuntimeChecksExact:
    def _checks(self, **over):
        base = {"check_id": "c0", "check_type": "call_exists", "source_file": "src/app.py",
                "pattern": "add(", "found": True, "file_missing": False}
        base.update(over)
        return [base]

    def test_found_false_blocks(self):
        g = _gates("runtime_integration_gate.json", checks=self._checks(found=False),
                   checks_total=1, checks_passed=1)
        assert _ok(g) is False

    def test_file_missing_true_blocks(self):
        g = _gates("runtime_integration_gate.json", checks=self._checks(file_missing=True),
                   checks_total=1, checks_passed=1)
        assert _ok(g) is False

    def test_unknown_check_type_blocks(self):
        g = _gates("runtime_integration_gate.json", checks=self._checks(check_type="eval_code"),
                   checks_total=1, checks_passed=1)
        assert _ok(g) is False

    def test_absolute_source_file_blocks(self):
        g = _gates("runtime_integration_gate.json",
                   checks=self._checks(source_file="/etc/passwd"), checks_total=1, checks_passed=1)
        assert _ok(g) is False

    def test_duplicate_check_id_blocks(self):
        dup = [dict(self._checks()[0]), dict(self._checks()[0])]
        g = _gates("runtime_integration_gate.json", checks=dup, checks_total=2, checks_passed=2)
        assert _ok(g) is False

    def test_count_disagreement_blocks(self):
        g = _gates("runtime_integration_gate.json", checks=self._checks(),
                   checks_total=3, checks_passed=3)
        assert _ok(g) is False

    def test_extra_check_field_blocks(self):
        g = _gates("runtime_integration_gate.json", checks=self._checks(bogus=1),
                   checks_total=1, checks_passed=1)
        assert _ok(g) is False
