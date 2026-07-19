"""F1 (round 30) — the final verifier report is producer-derived, staged-byte-bound authority. The
packaged report must equal a fresh run of the REAL producer over the exact Evidence bytes; a
hand-written or edited verdict / manual-completion flag / attested-task list / completeness map /
commit-execution status / recommended action makes the package non-reproducible and BLOCKS.
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
    "_brm_fvr", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_b); _b.loader.exec_module(_brm)
_e = importlib.util.spec_from_file_location(
    "_e2e_fvr", REPO_ROOT / "tests" / "orchestration" / "test_review_authoritative_e2e.py")
_E2E = importlib.util.module_from_spec(_e); _e.loader.exec_module(_E2E)

import pytest

pytestmark = pytest.mark.skipif(
    __import__("shutil").which("git") is None, reason="git required")


def _bundle(tmp_path):
    """A real authoritative manual-completion Evidence dir whose final_verifier_report was produced by
    the actual producer (no hand-written report)."""
    repo, base, head = _E2E._build_repo(tmp_path)
    ev, _subject, _authority = _E2E._write_evidence(repo, base, head, tmp_path / "evidence")
    return repo, ev


def _view(ev):
    return _brm._view_from_dir(str(ev))


class TestFinalVerifierReproducible:
    def test_packaged_report_equals_a_fresh_producer_rebuild(self, tmp_path):
        repo, ev = _bundle(tmp_path)
        os.chdir(repo)
        packaged = json.loads((ev / "final_verifier_report.json").read_text())
        regenerated = _brm.regenerate_final_verifier(_view(ev))
        assert regenerated is not None
        assert packaged == regenerated
        ok, reasons, _ = _brm._final_verifier_reproducibility(_view(ev))
        assert ok is True and reasons == []

    @pytest.mark.parametrize("field,newval", [
        ("verdict", "PASS"),
        ("manual_completion", False),
        ("operator_attested_tasks", ["T001", "T999"]),
        ("commit_execution_gate", "PROMOTE_READY"),
        ("recommended_action", "Approve, no human review needed"),
        ("human_final_reviewer_required", False),
    ])
    def test_editing_the_packaged_report_blocks(self, tmp_path, field, newval):
        repo, ev = _bundle(tmp_path)
        os.chdir(repo)
        report = json.loads((ev / "final_verifier_report.json").read_text())
        report[field] = newval
        (ev / "final_verifier_report.json").write_text(json.dumps(report))
        ok, reasons, _ = _brm._final_verifier_reproducibility(_view(ev))
        assert ok is False
        assert reasons and "not reproducible" in reasons[0]

    def test_editing_the_completeness_map_blocks(self, tmp_path):
        repo, ev = _bundle(tmp_path)
        os.chdir(repo)
        report = json.loads((ev / "final_verifier_report.json").read_text())
        report["evidence_completeness"] = dict(report["evidence_completeness"])
        report["evidence_completeness"]["spec_compliance_check"] = True  # already true -> flip a real one
        report["evidence_completeness"]["token_truth"] = not report["evidence_completeness"]["token_truth"]
        (ev / "final_verifier_report.json").write_text(json.dumps(report))
        ok, _reasons, _ = _brm._final_verifier_reproducibility(_view(ev))
        assert ok is False

    def test_stale_report_from_a_different_bundle_blocks(self, tmp_path):
        repo, ev = _bundle(tmp_path)
        os.chdir(repo)
        # An old report whose attested set / verdict no longer matches the Evidence.
        stale = {"verdict": "PASS", "manual_completion": True,
                 "operator_attested_tasks": ["T001", "T002", "T003"]}
        (ev / "final_verifier_report.json").write_text(json.dumps(stale))
        ok, reasons, _ = _brm._final_verifier_reproducibility(_view(ev))
        assert ok is False and reasons

    def test_regeneration_is_pure_over_the_snapshot(self, tmp_path):
        repo, ev = _bundle(tmp_path)
        os.chdir(repo)
        a = _brm.regenerate_final_verifier(_view(ev))
        b = _brm.regenerate_final_verifier(_view(ev))
        assert a == b
