"""The manual evidence producer's per-run verification shape (finding R-1017).

``manual_attestation._vt_run_v11`` and ``job_evidence._build_verification_tests``
both write a run's ``test_files``, and ``scripts/build_review_manifest.py`` rejects
a per-run list that is not sorted. The job path always sorted; the manual path kept
the caller's order, so a closure package built through it was BLOCKED_EVIDENCE
whenever the caller had not sorted. These tests pin the manual path to the
sibling's normalisation: sorted, duplicates collapsed.
"""
from __future__ import annotations

from packages.orchestration.manual_attestation import _vt_run_v11


def _run(test_files: list[str]) -> dict:
    return {"run_id": "r1", "command": "python3 -m pytest", "exit_code": 0, "test_files": test_files}


def test_test_files_are_sorted_whatever_order_the_caller_gave() -> None:
    assert _vt_run_v11(_run(["b.py", "a.py"]))["test_files"] == ["a.py", "b.py"]


def test_duplicate_test_files_collapse_to_one() -> None:
    assert _vt_run_v11(_run(["b.py", "a.py", "b.py"]))["test_files"] == ["a.py", "b.py"]


def test_a_run_without_test_files_keeps_an_empty_list() -> None:
    assert _vt_run_v11({"run_id": "r1", "command": "true"})["test_files"] == []
