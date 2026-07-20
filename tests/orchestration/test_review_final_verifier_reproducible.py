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
        report, problem = _brm.regenerate_final_verifier(_view(ev))
        assert report is not None and problem is None
        assert packaged == report
        r = _brm._final_verifier_reproducibility(_view(ev))
        assert r == {"checked": True, "reproducible": True, "status": "VERIFIED_EQUAL", "problems": []}

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
        r = _brm._final_verifier_reproducibility(_view(ev))
        assert r["reproducible"] is False and r["status"] == "VERIFIED_MISMATCH"
        assert r["problems"] and "not reproducible" in r["problems"][0]

    def test_editing_the_completeness_map_blocks(self, tmp_path):
        repo, ev = _bundle(tmp_path)
        os.chdir(repo)
        report = json.loads((ev / "final_verifier_report.json").read_text())
        report["evidence_completeness"] = dict(report["evidence_completeness"])
        report["evidence_completeness"]["token_truth"] = not report["evidence_completeness"]["token_truth"]
        (ev / "final_verifier_report.json").write_text(json.dumps(report))
        assert _brm._final_verifier_reproducibility(_view(ev))["status"] == "VERIFIED_MISMATCH"

    def test_stale_report_from_a_different_bundle_blocks(self, tmp_path):
        repo, ev = _bundle(tmp_path)
        os.chdir(repo)
        stale = {"verdict": "PASS", "manual_completion": True,
                 "operator_attested_tasks": ["T001", "T002", "T003"]}
        (ev / "final_verifier_report.json").write_text(json.dumps(stale))
        r = _brm._final_verifier_reproducibility(_view(ev))
        assert r["reproducible"] is False and r["status"] == "VERIFIED_MISMATCH"

    def test_missing_report_blocks(self, tmp_path):
        repo, ev = _bundle(tmp_path)
        os.chdir(repo)
        (ev / "final_verifier_report.json").unlink()
        r = _brm._final_verifier_reproducibility(_view(ev))
        assert r["reproducible"] is False and r["status"] == "VERIFIED_MISMATCH"

    def test_regeneration_is_pure_over_the_snapshot(self, tmp_path):
        repo, ev = _bundle(tmp_path)
        os.chdir(repo)
        assert _brm.regenerate_final_verifier(_view(ev)) == _brm.regenerate_final_verifier(_view(ev))


class TestProducerFailureNeverReportsReproducible:
    """F1B (round 31) — a producer that is unavailable / imports-fail / raises / returns None /
    returns a non-object, or a materialization failure, is PRODUCER_ERROR — never translated into
    success. No failure path reports reproducible=true."""

    def test_producer_module_unavailable(self, tmp_path, monkeypatch):
        repo, ev = _bundle(tmp_path)
        os.chdir(repo)
        import builtins
        real_import = builtins.__import__

        def blocked(name, *a, **k):
            if name == "packages.orchestration.final_verifier":
                raise ImportError("blocked for test")
            return real_import(name, *a, **k)
        monkeypatch.setattr(builtins, "__import__", blocked)
        r = _brm._final_verifier_reproducibility(_view(ev))
        assert r["reproducible"] is False and r["status"] == "PRODUCER_ERROR"

    def test_producer_raises_runtime_error(self, tmp_path, monkeypatch):
        repo, ev = _bundle(tmp_path)
        os.chdir(repo)
        import packages.orchestration.final_verifier as fv

        def boom(_dir):
            raise RuntimeError("producer exploded")
        monkeypatch.setattr(fv, "build_final_verifier_report", boom)
        r = _brm._final_verifier_reproducibility(_view(ev))
        assert r["reproducible"] is False and r["status"] == "PRODUCER_ERROR"
        assert r["problems"] and "RuntimeError" in r["problems"][0]

    def test_producer_returns_none(self, tmp_path, monkeypatch):
        repo, ev = _bundle(tmp_path)
        os.chdir(repo)
        import packages.orchestration.final_verifier as fv
        monkeypatch.setattr(fv, "build_final_verifier_report", lambda _d: None)
        r = _brm._final_verifier_reproducibility(_view(ev))
        assert r["reproducible"] is False and r["status"] == "PRODUCER_ERROR"

    def test_producer_returns_non_object(self, tmp_path, monkeypatch):
        repo, ev = _bundle(tmp_path)
        os.chdir(repo)
        import packages.orchestration.final_verifier as fv
        monkeypatch.setattr(fv, "build_final_verifier_report", lambda _d: ["not", "an", "object"])
        r = _brm._final_verifier_reproducibility(_view(ev))
        assert r["reproducible"] is False and r["status"] == "PRODUCER_ERROR"

    def test_no_evidence_is_not_checked_not_reproducible(self):
        r = _brm._final_verifier_reproducibility(None)
        assert r == {"checked": False, "reproducible": None, "status": "NOT_CHECKED", "problems": []}
        r2 = _brm._final_verifier_reproducibility(_brm._EvidenceView({}))
        assert r2["status"] == "NOT_CHECKED" and r2["reproducible"] is None


class TestStandaloneManifestNeverFalselyClaims:
    """F1A (round 31) — the standalone/default build_manifest never claims reproducibility it did not
    perform: a tampered report yields VERIFIED_MISMATCH and cannot be READY_FOR_REVIEW."""

    def test_valid_bundle_is_verified_equal(self, tmp_path):
        repo, ev = _bundle(tmp_path)
        os.chdir(repo)
        man = _brm.build_manifest(str(ev), selection_mode="explicit")
        r = man["final_verifier_reproducibility"]
        assert r["checked"] is True and r["status"] == "VERIFIED_EQUAL"
        assert man["final_verifier_reproducible"] is True

    def test_tampered_report_is_verified_mismatch_and_not_ready(self, tmp_path):
        repo, ev = _bundle(tmp_path)
        os.chdir(repo)
        report = json.loads((ev / "final_verifier_report.json").read_text())
        report["recommended_action"] = "FORGED"
        (ev / "final_verifier_report.json").write_text(json.dumps(report))
        man = _brm.build_manifest(str(ev), selection_mode="explicit")
        assert man["final_verifier_reproducibility"]["status"] == "VERIFIED_MISMATCH"
        assert man["final_verifier_reproducible"] is False
        assert man["package_status"] != "READY_FOR_REVIEW"

    def test_no_evidence_is_not_checked(self, tmp_path):
        repo, _ev = _bundle(tmp_path)
        os.chdir(repo)
        man = _brm.build_manifest(None)
        r = man["final_verifier_reproducibility"]
        assert r["status"] == "NOT_CHECKED" and r["reproducible"] is None
        assert man["final_verifier_reproducible"] is False
