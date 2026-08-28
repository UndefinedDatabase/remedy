"""Tests for the F037 evidence-to-diff resolver.

Every evidence tree is built under pytest's `tmp_path`, never under the repository, so a
test can neither read nor be fooled by a real run's artifacts.

The test that matters most is the refusal test. It does not merely assert that a traversal
id produces the right `reason` — a stubbed field would satisfy that. It plants a marker
file OUTSIDE the evidence directory and asserts the marker appears nowhere in any returned
envelope, so the pin is that nothing was READ, not that a string was set.
"""

from __future__ import annotations

from pathlib import Path

from packages.orchestration.diff_parser import DIFF_VIEW_VERSION
from packages.orchestration.diff_view_source import (
    DIFF_JOB_ARTIFACT_NAME,
    DIFF_REASON_ARTIFACT_MISSING,
    DIFF_REASON_NO_EVIDENCE_DIR,
    DIFF_REASON_UNKNOWN_TASK_RUN,
    DIFF_SCOPE_JOB,
    DIFF_SCOPE_TASK_RUN,
    build_diff_view,
    list_task_run_ids,
)

# The two fixtures name DIFFERENT paths on purpose: every happy-path assertion below is
# written so that serving one artifact where the other was asked for is a red.
JOB_DIFF_TEXT = """--- a/packages/orchestration/job_only.py
+++ b/packages/orchestration/job_only.py
@@ -1,3 +1,3 @@
 alpha
-beta
+gamma
 delta
"""

TASK_DIFF_TEXT = """--- a/packages/orchestration/task_only.py
+++ b/packages/orchestration/task_only.py
@@ -1,3 +1,3 @@
 one
-two
+three
 four
"""


def _write_evidence_tree(tmp_path: Path) -> Path:
    """Build an evidence dir carrying a job diff and one task run's safe diff."""
    evidence = tmp_path / "evidence"
    (evidence / "task_runs" / "T001").mkdir(parents=True)
    (evidence / DIFF_JOB_ARTIFACT_NAME).write_text(JOB_DIFF_TEXT, encoding="utf-8")
    (evidence / "task_runs" / "T001" / "safe.diff").write_text(TASK_DIFF_TEXT, encoding="utf-8")
    return evidence


def _paths(view: dict) -> list[str]:
    return [f["path"] for f in view["files"]]


def test_job_scope_reads_the_workspace_diff(tmp_path: Path) -> None:
    evidence = _write_evidence_tree(tmp_path)

    view = build_diff_view(evidence)

    assert view["scope"] == DIFF_SCOPE_JOB
    assert view["task_id"] is None
    assert view["source"] == "workspace.diff"
    assert view["available"] is True
    assert view["reason"] is None
    assert view["truncated"] is False
    assert _paths(view) == ["packages/orchestration/job_only.py"]


def test_task_run_scope_reads_that_runs_safe_diff(tmp_path: Path) -> None:
    evidence = _write_evidence_tree(tmp_path)

    view = build_diff_view(evidence, task_id="T001")

    assert view["scope"] == DIFF_SCOPE_TASK_RUN
    assert view["task_id"] == "T001"
    assert view["source"] == "task_runs/T001/safe.diff"
    assert view["available"] is True
    assert view["reason"] is None
    # ONLY the task-run artifact names this path, so a swapped artifact is a red here.
    assert _paths(view) == ["packages/orchestration/task_only.py"]
    assert view["task_run_ids"] == ["T001"]


def test_version_is_the_parsers_imported_contract_version(tmp_path: Path) -> None:
    evidence = _write_evidence_tree(tmp_path)

    assert build_diff_view(evidence)["version"] == DIFF_VIEW_VERSION
    assert build_diff_view(evidence, task_id="T001")["version"] == DIFF_VIEW_VERSION
    assert build_diff_view(None)["version"] == DIFF_VIEW_VERSION


def test_absent_evidence_dir_is_named_rather_than_raised(tmp_path: Path) -> None:
    view = build_diff_view(None)

    assert view["reason"] == DIFF_REASON_NO_EVIDENCE_DIR
    assert view["available"] is False
    assert view["files"] == []
    assert view["source"] is None
    assert view["task_run_ids"] == []

    gone = build_diff_view(tmp_path / "never_created")
    assert gone["reason"] == DIFF_REASON_NO_EVIDENCE_DIR
    assert gone["available"] is False
    assert gone["files"] == []


def test_missing_job_artifact_still_names_the_path_it_looked_for(tmp_path: Path) -> None:
    evidence = tmp_path / "evidence"
    evidence.mkdir()

    view = build_diff_view(evidence)

    assert view["reason"] == DIFF_REASON_ARTIFACT_MISSING
    assert view["available"] is False
    assert view["files"] == []
    assert view["truncated"] is False
    # The absence is debuggable: it says WHAT was looked for.
    assert view["source"] == "workspace.diff"


def test_unknown_task_run_is_refused_and_reports_the_real_runs(tmp_path: Path) -> None:
    evidence = _write_evidence_tree(tmp_path)

    view = build_diff_view(evidence, task_id="T404")

    assert view["reason"] == DIFF_REASON_UNKNOWN_TASK_RUN
    assert view["available"] is False
    assert view["files"] == []
    assert view["source"] is None
    assert view["task_run_ids"] == ["T001"]


def test_traversal_task_ids_are_refused_without_reading_anything(tmp_path: Path) -> None:
    evidence = _write_evidence_tree(tmp_path)
    marker = "SECRET_OUTSIDE_THE_EVIDENCE_DIR_9f2b"
    outside = tmp_path / "outside.diff"
    outside.write_text(TASK_DIFF_TEXT.replace("task_only.py", marker), encoding="utf-8")
    (tmp_path / "safe.diff").write_text(TASK_DIFF_TEXT.replace("task_only.py", marker), encoding="utf-8")

    for hostile in ("../../../etc", "T001/../../..", "/etc", ".", ""):
        view = build_diff_view(evidence, task_id=hostile)

        assert view["reason"] == DIFF_REASON_UNKNOWN_TASK_RUN, hostile
        assert view["source"] is None, hostile
        assert view["available"] is False, hostile
        assert view["files"] == [], hostile
        # Nothing was READ: the marker planted outside the evidence dir reaches no field.
        assert marker not in repr(view), hostile


def test_list_task_run_ids_sorts_and_filters_the_listing(tmp_path: Path) -> None:
    evidence = tmp_path / "evidence"
    runs = evidence / "task_runs"
    for name in ("T001", "T010", "T002", "nope"):
        (runs / name).mkdir(parents=True)
    (runs / "T999").write_text("a file, not a task run", encoding="utf-8")

    assert list_task_run_ids(evidence) == ["T001", "T002", "T010"]
    assert list_task_run_ids(None) == []
    assert list_task_run_ids(tmp_path / "never_created") == []
    assert list_task_run_ids(tmp_path) == []


def test_an_empty_diff_artifact_is_available_with_no_files(tmp_path: Path) -> None:
    evidence = tmp_path / "evidence"
    evidence.mkdir()
    (evidence / DIFF_JOB_ARTIFACT_NAME).write_text("", encoding="utf-8")

    view = build_diff_view(evidence)

    # "nothing changed" is not "no diff was written": an empty artifact is AVAILABLE.
    assert view["available"] is True
    assert view["reason"] is None
    assert view["files"] == []
    assert view["source"] == "workspace.diff"
