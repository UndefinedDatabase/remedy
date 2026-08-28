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

import pytest

from packages.orchestration import diff_view_source
from packages.orchestration.diff_parser import DIFF_TRUNCATED_SENTINEL, DIFF_VIEW_VERSION
from packages.orchestration.diff_view_source import (
    DIFF_JOB_ARTIFACT_NAME,
    DIFF_REASON_ARTIFACT_MISSING,
    DIFF_REASON_NO_EVIDENCE_DIR,
    DIFF_REASON_UNKNOWN_TASK_RUN,
    DIFF_SCOPE_JOB,
    DIFF_SCOPE_TASK_RUN,
    DIFF_VIEW_MAX_ARTIFACT_BYTES,
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


# --- F037 R14: the READ ceiling (DECISION F037 D7) --------------------------------------
#
# The two parser ceilings bound the view that is BUILT. Everything below bounds what is
# READ, which is a different resource in a different unit, and the two cut hazards — a
# partial line and a split character — each get a test whose fixture is built so the cut
# lands exactly on them.


def _write_job_diff(root: Path, diff_text: str) -> Path:
    """Build an evidence dir under ``root`` whose ``workspace.diff`` is exactly ``diff_text``.

    WHY this exists BESIDE ``_write_evidence_tree``: that helper builds a FIXED pair of
    artifacts, and every test below needs an artifact whose BYTES it chose itself. Callers
    that need two trees in one test pass two different ``root`` directories.
    """
    evidence = root / "evidence"
    evidence.mkdir(parents=True)
    (evidence / DIFF_JOB_ARTIFACT_NAME).write_text(diff_text, encoding="utf-8")
    return evidence


def _contents(view: dict) -> list[str]:
    """Every body line's ``content``, in order, across every file and hunk of the view."""
    return [line["content"] for f in view["files"] for hunk in f["hunks"] for line in hunk["lines"]]


def test_an_artifact_above_the_read_ceiling_is_cut_and_the_envelope_says_so(tmp_path: Path) -> None:
    """The ONLY test here that runs at the REAL ``DIFF_VIEW_MAX_ARTIFACT_BYTES``.

    WHAT IT COSTS: an artifact of more than eight megabytes written to ``tmp_path``. WHY it
    is worth paying: every other test below moves the ceiling, and a moved ceiling proves the
    comparison but never that the SHIPPED constant is the one the read actually uses. The
    cost stays bounded because the parser stops at its own ``DIFF_VIEW_MAX_BODY_LINES``
    early in this text, so what is paid is the read and the split — not a full parse of
    eight megabytes.
    """
    body_line = " " + "x" * 200 + "\n"
    line_count = (DIFF_VIEW_MAX_ARTIFACT_BYTES // len(body_line.encode("utf-8"))) + 200
    text = (
        "--- a/packages/orchestration/huge.py\n"
        "+++ b/packages/orchestration/huge.py\n"
        f"@@ -1,{line_count} +1,{line_count} @@\n"
    ) + body_line * line_count
    assert len(text.encode("utf-8")) > DIFF_VIEW_MAX_ARTIFACT_BYTES
    evidence = _write_job_diff(tmp_path, text)

    view = build_diff_view(evidence)

    assert view["available"] is True
    assert view["truncated"] is True
    # A bound that returned NOTHING at all would satisfy a truncation assertion on its own.
    assert len(view["files"]) >= 1


# WHY the tests below move the ceiling with ``monkeypatch.setattr`` instead of sizing every
# fixture to the real one: a boundary is a property of the COMPARISON, not of the value being
# compared against, so a small ceiling exercises exactly the same branch on exactly the same
# bytes. A fixture per test at the real value would cost tens of megabytes of writes to prove
# the same thing, and the test above already pins that the shipped constant is in the path.
def _set_read_ceiling(monkeypatch: pytest.MonkeyPatch, ceiling: int) -> None:
    monkeypatch.setattr(diff_view_source, "DIFF_VIEW_MAX_ARTIFACT_BYTES", ceiling)


def test_the_read_ceiling_boundary_holds_on_both_of_its_sides(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Both halves in one test, for the reason the parser's two boundary tests already state.

    Each half alone is satisfiable by a bound that is one off in either direction: only the
    pair pins that the comparison is ``>`` and not ``>=``.
    """
    ceiling = 512
    _set_read_ceiling(monkeypatch, ceiling)
    header = "--- a/packages/orchestration/edge.py\n+++ b/packages/orchestration/edge.py\n@@ -1,2 +1,2 @@\n alpha\n"
    padding = ceiling - len(header.encode("utf-8")) - len(b" \n")
    exactly = header + " " + "y" * padding + "\n"
    one_over = header + " " + "y" * (padding + 1) + "\n"
    assert len(exactly.encode("utf-8")) == ceiling
    assert len(one_over.encode("utf-8")) == ceiling + 1

    at_the_ceiling = build_diff_view(_write_job_diff(tmp_path / "exactly", exactly))
    assert at_the_ceiling["available"] is True
    assert at_the_ceiling["truncated"] is False
    assert _contents(at_the_ceiling) == ["alpha", "y" * padding]

    above_the_ceiling = build_diff_view(_write_job_diff(tmp_path / "one_over", one_over))
    assert above_the_ceiling["available"] is True
    assert above_the_ceiling["truncated"] is True


def test_the_cut_never_hands_the_parser_a_partial_line(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A cut landing mid-line must drop that line whole, never half of it."""
    body = [f"line-{index:03d}-" + "y" * 30 for index in range(12)]
    header = (
        "--- a/packages/orchestration/lines.py\n"
        "+++ b/packages/orchestration/lines.py\n"
        f"@@ -1,{len(body)} +1,{len(body)} @@\n"
    )
    text = header + "".join(" " + line + "\n" for line in body)
    data = text.encode("utf-8")
    line_bytes = len((" " + body[0] + "\n").encode("utf-8"))
    surviving = 6
    ceiling = len(header.encode("utf-8")) + surviving * line_bytes + line_bytes // 2
    # Pinned so the fixture cannot silently stop exercising the case: the cut point has a
    # non-newline byte on either side of it, which is what "in the middle of a line" means.
    assert data[ceiling - 1] != 0x0A
    assert data[ceiling] != 0x0A
    _set_read_ceiling(monkeypatch, ceiling)

    view = build_diff_view(_write_job_diff(tmp_path, text))

    # Beside the content assertion so the test cannot pass by the cut never having happened.
    assert view["truncated"] is True
    # Every content the contract carries is a WHOLE generated line, in order. The trailing
    # "" is the parser's reading of the text's own terminating newline while the hunk header
    # still declares lines outstanding — its behaviour on any short hunk, not a cut line.
    assert _contents(view) == body[:surviving] + [""]


def test_the_cut_never_splits_a_multi_byte_character(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Without the newline cut this artifact raises ``UnicodeDecodeError``.

    The module's existing handler would then report a perfectly readable diff as
    ``DIFF_REASON_ARTIFACT_MISSING``, so ``available`` True and ``reason`` None are the
    assertions that fail when the cut goes to an arbitrary byte instead.
    """
    body_line = " " + "→" * 12 + "\n"
    header = (
        "--- a/packages/orchestration/wide.py\n"
        "+++ b/packages/orchestration/wide.py\n"
        "@@ -1,6 +1,6 @@\n"
    )
    text = header + body_line * 6
    data = text.encode("utf-8")
    line_bytes = len(body_line.encode("utf-8"))
    surviving = 3
    # One byte for the context marker, then one byte INTO the three-byte character after it.
    ceiling = len(header.encode("utf-8")) + surviving * line_bytes + 2
    # Pinned so the fixture cannot silently stop exercising the case: the first byte the cut
    # would drop is a UTF-8 CONTINUATION byte, which is only true inside a character.
    assert 0x80 <= data[ceiling] < 0xC0
    _set_read_ceiling(monkeypatch, ceiling)

    view = build_diff_view(_write_job_diff(tmp_path, text))

    assert view["available"] is True
    assert view["reason"] is None
    assert view["truncated"] is True
    # Whole characters and whole lines, plus the terminating newline's own empty entry.
    assert _contents(view) == ["→" * 12] * surviving + [""]


def test_one_enormous_line_is_bounded_though_it_reaches_neither_parser_ceiling(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The shape that motivates this bound: it appends nothing to either parser counter.

    No newline anywhere means no body line and no second file entry, so a diff like this
    passes ``DIFF_VIEW_MAX_BODY_LINES`` and ``DIFF_VIEW_MAX_FILES`` untouched however large
    it grows. Cut to the ceiling and then back to a last newline it does not have, it yields
    the empty text — available, empty and truncated, which is the honest answer.
    """
    text = "packages/orchestration/minified.js:" + "z" * 4000
    assert "\n" not in text
    _set_read_ceiling(monkeypatch, 64)

    view = build_diff_view(_write_job_diff(tmp_path, text))

    assert view["available"] is True
    assert view["truncated"] is True
    assert view["files"] == []


def test_the_parsers_own_truncation_still_reaches_the_envelope(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The discriminator that ``truncated`` is an OR over both sources, not a replacement.

    This artifact stays UNDER the read ceiling, so the read does nothing at all; the flag can
    only come from the upstream ``[DIFF TRUNCATED]`` sentinel the parser reads.
    """
    ceiling = 4096
    text = JOB_DIFF_TEXT + DIFF_TRUNCATED_SENTINEL + "\n"
    assert len(text.encode("utf-8")) < ceiling
    _set_read_ceiling(monkeypatch, ceiling)

    view = build_diff_view(_write_job_diff(tmp_path, text))

    assert view["available"] is True
    assert view["truncated"] is True
    assert _paths(view) == ["packages/orchestration/job_only.py"]
