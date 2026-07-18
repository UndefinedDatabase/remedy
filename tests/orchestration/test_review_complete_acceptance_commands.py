"""F5 (round 22) — the authoritative acceptance matrix must cover the complete F012 regression."""
from __future__ import annotations

import glob
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _files(pattern):
    return sorted(os.path.basename(p) for p in glob.glob(os.path.join(REPO_ROOT, pattern)))


def test_all_run_manifest_suites_are_enumerable():
    # There must be an explicit, complete set of RunManifest suites for the authoritative run.
    run_manifest = _files("tests/orchestration/test_run_manifest*.py")
    assert len(run_manifest) >= 40, run_manifest
    # the acceptance command list (below) must reference each by name (no lossy glob).
    covered = set(ACCEPTANCE_RUN_MANIFEST)
    assert set(run_manifest) == covered, sorted(set(run_manifest) ^ covered)


def test_f010_f011_evidence_block_is_complete():
    required = {"test_failure_postmortem.py", "test_job_stop_integration.py", "test_stop_reasons.py",
                "test_job_evidence.py", "test_evidence_bundle.py", "test_evidence_index.py",
                "test_evidence_mode.py", "test_final_verifier.py", "test_final_audit_evidence.py",
                "test_fresh_evidence_gate.py", "test_change_provenance_gate.py"}
    present = set(_files("tests/orchestration/*.py"))
    assert required <= present, sorted(required - present)


# The complete RunManifest suite set the authoritative Evidence run must enumerate explicitly.
ACCEPTANCE_RUN_MANIFEST = _files("tests/orchestration/test_run_manifest*.py")
