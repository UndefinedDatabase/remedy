"""Tests for diff_repair.py (F111 T001).

Covers the eight pinned clauses of select_repair_hunks: margin clamping at
both file edges, overlap/adjacency merging, deterministic sort order,
binary omission, missing-path omission, the char budget, margin_lines=0,
empty range lists — plus exact-text fidelity of a carried hunk and the
out-of-bounds omission reason that R-0299 split off from `no_ranges`.

repo_root is a bare tmp_path: no git init, no fixtures beyond tmp_path,
matching tests/orchestration/test_fences.py.
"""

from __future__ import annotations

from packages.orchestration.diff_repair import (
    REPAIR_HUNKS_HEADING,
    REPAIR_HUNKS_OMITTED_INTRO,
    RepairHunk,
    RepairHunkSelection,
    changed_line_ranges_from_patch,
    render_repair_hunks,
    select_repair_hunks,
)
from packages.orchestration.structured_patch import FileOp, StructuredPatch, UnifiedDiff


def _write(tmp_path, name: str, line_count: int) -> list[str]:
    """Write a file of numbered lines and return those lines."""
    lines = [f"line{n:03d}" for n in range(1, line_count + 1)]
    (tmp_path / name).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return lines


# ═══════════════════════════════════════════════════════════════════════════
# Clause 1 — margin expansion is always clamped to the file
# ═══════════════════════════════════════════════════════════════════════════


class TestMarginClamping:
    """Expanded ranges never leave the file's line bounds."""

    def test_start_of_file_clamps_to_line_1(self, tmp_path):
        _write(tmp_path, "a.txt", 5)
        result = select_repair_hunks(tmp_path, {"a.txt": [[1, 1]]}, margin_lines=3)
        assert len(result.hunks) == 1
        assert result.hunks[0].start_line == 1
        assert result.hunks[0].end_line == 4

    def test_end_of_file_clamps_to_last_line(self, tmp_path):
        _write(tmp_path, "a.txt", 5)
        result = select_repair_hunks(tmp_path, {"a.txt": [[5, 5]]}, margin_lines=3)
        assert result.hunks[0].start_line == 2
        assert result.hunks[0].end_line == 5

    def test_margin_wider_than_file_yields_whole_file(self, tmp_path):
        lines = _write(tmp_path, "a.txt", 4)
        result = select_repair_hunks(tmp_path, {"a.txt": [[2, 2]]}, margin_lines=99)
        assert (result.hunks[0].start_line, result.hunks[0].end_line) == (1, 4)
        assert result.hunks[0].text == "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════
# Clause 2 — overlapping or adjacent ranges merge into one hunk
# ═══════════════════════════════════════════════════════════════════════════


class TestMerging:
    """No source line is carried twice within one file."""

    def test_overlapping_ranges_merge(self, tmp_path):
        _write(tmp_path, "a.txt", 20)
        result = select_repair_hunks(
            tmp_path, {"a.txt": [[5, 7], [6, 9]]}, margin_lines=0
        )
        assert len(result.hunks) == 1
        assert (result.hunks[0].start_line, result.hunks[0].end_line) == (5, 9)

    def test_adjacent_ranges_merge(self, tmp_path):
        _write(tmp_path, "a.txt", 20)
        result = select_repair_hunks(
            tmp_path, {"a.txt": [[5, 5], [8, 8]]}, margin_lines=1
        )
        assert len(result.hunks) == 1
        assert (result.hunks[0].start_line, result.hunks[0].end_line) == (4, 9)
        assert len(result.hunks[0].text.split("\n")) == 6

    def test_distant_ranges_stay_separate(self, tmp_path):
        _write(tmp_path, "a.txt", 40)
        result = select_repair_hunks(
            tmp_path, {"a.txt": [[3, 3], [30, 30]]}, margin_lines=1
        )
        assert [(h.start_line, h.end_line) for h in result.hunks] == [(2, 4), (29, 31)]


# ═══════════════════════════════════════════════════════════════════════════
# Clause 3 — deterministic order
# ═══════════════════════════════════════════════════════════════════════════


class TestOrdering:
    """Hunks come back sorted by (path, start_line)."""

    def test_sorted_by_path_then_start_line(self, tmp_path):
        _write(tmp_path, "b.txt", 40)
        _write(tmp_path, "a.txt", 40)
        result = select_repair_hunks(
            tmp_path,
            {"b.txt": [[30, 30], [4, 4]], "a.txt": [[20, 20], [2, 2]]},
            margin_lines=0,
        )
        assert [(h.path, h.start_line) for h in result.hunks] == [
            ("a.txt", 2),
            ("a.txt", 20),
            ("b.txt", 4),
            ("b.txt", 30),
        ]


# ═══════════════════════════════════════════════════════════════════════════
# Clause 4 — binary files are omitted, never raised on
# ═══════════════════════════════════════════════════════════════════════════


class TestBinaryOmission:
    """A NUL byte or a UTF-8 decode failure omits the file with 'binary'."""

    def test_nul_byte_file_is_omitted(self, tmp_path):
        (tmp_path / "blob.bin").write_bytes(b"abc\x00def\nghi\n")
        result = select_repair_hunks(tmp_path, {"blob.bin": [[1, 1]]})
        assert result.hunks == ()
        assert result.omitted == (("blob.bin", "binary"),)

    def test_undecodable_file_is_omitted(self, tmp_path):
        (tmp_path / "blob.bin").write_bytes(b"\xff\xfe\xfd bad utf8\n")
        result = select_repair_hunks(tmp_path, {"blob.bin": [[1, 1]]})
        assert result.omitted == (("blob.bin", "binary"),)
        assert result.total_chars == 0


# ═══════════════════════════════════════════════════════════════════════════
# Clause 5 — missing paths are omitted
# ═══════════════════════════════════════════════════════════════════════════


class TestMissingOmission:
    """A path that does not exist under repo_root is omitted with 'missing'."""

    def test_missing_path_is_omitted(self, tmp_path):
        result = select_repair_hunks(tmp_path, {"gone.py": [[1, 2]]})
        assert result.hunks == ()
        assert result.omitted == (("gone.py", "missing"),)

    def test_missing_path_does_not_block_present_one(self, tmp_path):
        _write(tmp_path, "a.txt", 5)
        result = select_repair_hunks(
            tmp_path, {"gone.py": [[1, 2]], "a.txt": [[2, 2]]}, margin_lines=0
        )
        assert [h.path for h in result.hunks] == ["a.txt"]
        assert result.omitted == (("gone.py", "missing"),)


# ═══════════════════════════════════════════════════════════════════════════
# Clause 6 — the char budget
# ═══════════════════════════════════════════════════════════════════════════


class TestBudget:
    """Admission stops at the cap and the rest is reported as 'budget'."""

    def test_over_budget_hunk_is_omitted(self, tmp_path):
        (tmp_path / "a.txt").write_text("x" * 100 + "\n", encoding="utf-8")
        (tmp_path / "b.txt").write_text("y" * 100 + "\n", encoding="utf-8")
        result = select_repair_hunks(
            tmp_path,
            {"a.txt": [[1, 1]], "b.txt": [[1, 1]]},
            margin_lines=0,
            max_total_chars=150,
        )
        assert [h.path for h in result.hunks] == ["a.txt"]
        assert result.omitted == (("b.txt", "budget"),)

    def test_total_chars_never_exceeds_cap(self, tmp_path):
        (tmp_path / "a.txt").write_text("x" * 100 + "\n", encoding="utf-8")
        (tmp_path / "b.txt").write_text("y" * 100 + "\n", encoding="utf-8")
        result = select_repair_hunks(
            tmp_path,
            {"a.txt": [[1, 1]], "b.txt": [[1, 1]]},
            margin_lines=0,
            max_total_chars=150,
        )
        assert result.total_chars == 100
        assert result.total_chars <= 150
        assert result.total_chars == sum(len(h.text) for h in result.hunks)

    def test_everything_fits_under_a_wide_cap(self, tmp_path):
        _write(tmp_path, "a.txt", 5)
        result = select_repair_hunks(
            tmp_path, {"a.txt": [[1, 5]]}, margin_lines=0, max_total_chars=20000
        )
        assert result.omitted == ()
        assert result.total_chars == len(result.hunks[0].text)


# ═══════════════════════════════════════════════════════════════════════════
# Clause 7 — margin_lines=0 returns exactly the requested lines
# ═══════════════════════════════════════════════════════════════════════════


class TestZeroMargin:
    """No margin means the requested span and nothing around it."""

    def test_zero_margin_returns_requested_span(self, tmp_path):
        lines = _write(tmp_path, "a.txt", 10)
        result = select_repair_hunks(tmp_path, {"a.txt": [[4, 6]]}, margin_lines=0)
        assert (result.hunks[0].start_line, result.hunks[0].end_line) == (4, 6)
        assert result.hunks[0].text == "\n".join(lines[3:6])


# ═══════════════════════════════════════════════════════════════════════════
# Clause 8 — an empty range list is omitted
# ═══════════════════════════════════════════════════════════════════════════


class TestNoRanges:
    """A path whose range list is empty is omitted with 'no_ranges'."""

    def test_empty_range_list_is_omitted(self, tmp_path):
        _write(tmp_path, "a.txt", 5)
        result = select_repair_hunks(tmp_path, {"a.txt": []})
        assert result.hunks == ()
        assert result.omitted == (("a.txt", "no_ranges"),)
        assert result.total_chars == 0

    def test_single_empty_range_entry_is_still_no_ranges(self, tmp_path):
        _write(tmp_path, "a.txt", 5)
        result = select_repair_hunks(tmp_path, {"a.txt": [[]]})
        assert result.hunks == ()
        assert result.omitted == (("a.txt", "no_ranges"),)


# ═══════════════════════════════════════════════════════════════════════════
# R-0299 — ranges that name lines the file does not have are 'out_of_bounds'
# ═══════════════════════════════════════════════════════════════════════════


class TestOutOfBounds:
    """Lines were asked for, none exist: a stale range, not an absent one."""

    def test_range_past_eof_is_out_of_bounds(self, tmp_path):
        _write(tmp_path, "a.txt", 5)
        result = select_repair_hunks(tmp_path, {"a.txt": [[50, 51]]})
        assert result.omitted == (("a.txt", "out_of_bounds"),)
        assert [h.path for h in result.hunks] == []
        assert result.total_chars == 0

    def test_out_of_bounds_path_does_not_block_present_one(self, tmp_path):
        _write(tmp_path, "a.txt", 5)
        _write(tmp_path, "b.txt", 5)
        result = select_repair_hunks(
            tmp_path, {"a.txt": [[50, 51]], "b.txt": [[2, 2]]}, margin_lines=0
        )
        assert [h.path for h in result.hunks] == ["b.txt"]
        assert result.omitted == (("a.txt", "out_of_bounds"),)


# ═══════════════════════════════════════════════════════════════════════════
# Text fidelity and shape
# ═══════════════════════════════════════════════════════════════════════════


class TestHunkText:
    """A hunk's text is the exact source lines, newline-joined."""

    def test_text_equals_exact_source_lines(self, tmp_path):
        lines = _write(tmp_path, "a.txt", 12)
        result = select_repair_hunks(tmp_path, {"a.txt": [[5, 6]]}, margin_lines=2)
        hunk = result.hunks[0]
        assert (hunk.start_line, hunk.end_line) == (3, 8)
        assert hunk.text == "\n".join(lines[2:8])
        assert hunk.text.splitlines() == lines[2:8]

    def test_result_types_are_frozen_dataclasses(self, tmp_path):
        _write(tmp_path, "a.txt", 5)
        result = select_repair_hunks(tmp_path, {"a.txt": [[1, 2]]})
        assert isinstance(result, RepairHunkSelection)
        assert isinstance(result.hunks[0], RepairHunk)
        assert isinstance(result.hunks, tuple)


# ═══════════════════════════════════════════════════════════════════════════
# R-0300 — a range against a file with no lines at all
# ═══════════════════════════════════════════════════════════════════════════


class TestEmptyFileRanges:
    """A zero-line file has no line the range could name, so it is stale too."""

    def test_empty_file_with_a_non_empty_range_is_out_of_bounds(self, tmp_path):
        (tmp_path / "empty.txt").write_text("", encoding="utf-8")
        result = select_repair_hunks(tmp_path, {"empty.txt": [[1, 1]]})
        assert result.omitted == (("empty.txt", "out_of_bounds"),)
        assert result.hunks == ()
        assert result.total_chars == 0


# ═══════════════════════════════════════════════════════════════════════════
# The range source — a builder patch becomes the ranges selection consumes
# ═══════════════════════════════════════════════════════════════════════════


_ONE_HUNK_DIFF = """--- a/a.py
+++ b/a.py
@@ -1,3 +1,4 @@
 one
+two
 three
"""

_TWO_HUNK_DIFF = """--- a/a.py
+++ b/a.py
@@ -1,2 +1,2 @@
 one
-two
+TWO
@@ -20,3 +20,4 @@
 twenty
+extra
"""


class TestChangedLineRangesFromPatch:
    """Ranges come from the applied patch, never from a timeline event."""

    def test_one_hunk_yields_its_new_file_span(self):
        patch = StructuredPatch(
            intent_kind="unified_diff",
            unified_diffs=(UnifiedDiff(path="a.py", diff=_ONE_HUNK_DIFF),),
        )
        assert changed_line_ranges_from_patch(patch) == {"a.py": [[1, 4]]}

    def test_two_hunks_yield_two_spans_in_order(self):
        patch = StructuredPatch(
            intent_kind="unified_diff",
            unified_diffs=(UnifiedDiff(path="a.py", diff=_TWO_HUNK_DIFF),),
        )
        assert changed_line_ranges_from_patch(patch) == {"a.py": [[1, 2], [20, 23]]}

    def test_two_diffs_yield_both_paths(self):
        patch = StructuredPatch(
            intent_kind="unified_diff",
            unified_diffs=(
                UnifiedDiff(path="a.py", diff=_ONE_HUNK_DIFF),
                UnifiedDiff(
                    path="b.py",
                    diff=_ONE_HUNK_DIFF.replace("a/a.py", "a/b.py").replace(
                        "b/a.py", "b/b.py"
                    ),
                ),
            ),
        )
        assert changed_line_ranges_from_patch(patch) == {
            "a.py": [[1, 4]],
            "b.py": [[1, 4]],
        }

    def test_declared_path_without_a_hunk_header_survives_as_empty(self):
        patch = StructuredPatch(
            intent_kind="unified_diff",
            unified_diffs=(UnifiedDiff(path="lonely.py", diff=""),),
        )
        assert changed_line_ranges_from_patch(patch) == {"lonely.py": []}

    def test_file_ops_paths_carry_no_lines(self):
        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(
                FileOp(path="new.py", action="create", content="x\n"),
                FileOp(path="old.py", action="delete"),
            ),
        )
        assert changed_line_ranges_from_patch(patch) == {"new.py": [], "old.py": []}

    def test_markdown_patch_yields_nothing(self):
        patch = StructuredPatch(intent_kind="markdown", markdown_proposal="prose")
        assert changed_line_ranges_from_patch(patch) == {}

    def test_ranges_feed_selection_end_to_end(self, tmp_path):
        lines = _write(tmp_path, "a.txt", 20)
        diff = "--- a/a.txt\n+++ b/a.txt\n@@ -5,3 +5,3 @@\n line005\n-line006\n+x\n line007\n"
        patch = StructuredPatch(
            intent_kind="unified_diff",
            unified_diffs=(UnifiedDiff(path="a.txt", diff=diff),),
        )
        ranges = changed_line_ranges_from_patch(patch)
        result = select_repair_hunks(tmp_path, ranges, margin_lines=0)
        assert (result.hunks[0].start_line, result.hunks[0].end_line) == (5, 7)
        assert result.hunks[0].text == "\n".join(lines[4:7])

    def test_a_file_ops_path_is_reported_as_no_ranges_by_selection(self, tmp_path):
        _write(tmp_path, "a.txt", 5)
        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(FileOp(path="a.txt", action="modify", content="x\n"),),
        )
        result = select_repair_hunks(tmp_path, changed_line_ranges_from_patch(patch))
        assert result.hunks == ()
        assert result.omitted == (("a.txt", "no_ranges"),)


# ═══════════════════════════════════════════════════════════════════════════
# Rendering — a selection becomes repair-prompt text (T002b-ii step 2 prep,
# DECISION F106 D1(b)'s rendering-convention obligation). No production
# caller wires this in yet; that is a later round's own work.
# ═══════════════════════════════════════════════════════════════════════════


class TestRenderRepairHunks:
    """The frozen prompt-text convention for a RepairHunkSelection."""

    def test_empty_selection_renders_nothing(self):
        selection = RepairHunkSelection(hunks=(), omitted=(), total_chars=0)
        assert render_repair_hunks(selection) == ""

    def test_empty_selection_with_only_omissions_still_renders_nothing(self):
        selection = RepairHunkSelection(
            hunks=(), omitted=(("a.py", "missing"),), total_chars=0
        )
        assert render_repair_hunks(selection) == ""

    def test_single_hunk_frozen_render(self):
        hunk = RepairHunk(path="a.py", start_line=1, end_line=3, text="one\ntwo\nthree")
        selection = RepairHunkSelection(hunks=(hunk,), omitted=(), total_chars=13)
        assert render_repair_hunks(selection) == (
            "## Resumed Session — Changed Regions Only\n"
            "\n"
            "### a.py (lines 1-3)\n"
            "```\n"
            "one\ntwo\nthree\n"
            "```\n"
        )

    def test_two_hunks_render_in_selection_order_with_a_blank_line_between(self):
        hunk_a = RepairHunk(path="a.py", start_line=1, end_line=1, text="one")
        hunk_b = RepairHunk(path="b.py", start_line=9, end_line=9, text="nine")
        selection = RepairHunkSelection(
            hunks=(hunk_a, hunk_b), omitted=(), total_chars=7
        )
        rendered = render_repair_hunks(selection)
        assert rendered == (
            "## Resumed Session — Changed Regions Only\n"
            "\n"
            "### a.py (lines 1-1)\n"
            "```\n"
            "one\n"
            "```\n"
            "\n"
            "### b.py (lines 9-9)\n"
            "```\n"
            "nine\n"
            "```\n"
        )
        assert rendered.index("a.py") < rendered.index("b.py")

    def test_omitted_paths_render_as_a_trailing_bulleted_list(self):
        hunk = RepairHunk(path="a.py", start_line=1, end_line=1, text="one")
        selection = RepairHunkSelection(
            hunks=(hunk,),
            omitted=(("b.py", "budget"), ("c.py", "missing")),
            total_chars=3,
        )
        rendered = render_repair_hunks(selection)
        assert rendered.endswith(
            "Omitted from this selection:\n"
            "- b.py (budget)\n"
            "- c.py (missing)\n"
        )
        assert REPAIR_HUNKS_OMITTED_INTRO in rendered

    def test_rendered_text_starts_with_the_heading_constant(self):
        hunk = RepairHunk(path="a.py", start_line=1, end_line=1, text="one")
        selection = RepairHunkSelection(hunks=(hunk,), omitted=(), total_chars=3)
        assert render_repair_hunks(selection).startswith(REPAIR_HUNKS_HEADING)

    def test_end_to_end_with_select_repair_hunks(self, tmp_path):
        _write(tmp_path, "a.txt", 5)
        result = select_repair_hunks(tmp_path, {"a.txt": [[2, 2]]}, margin_lines=0)
        rendered = render_repair_hunks(result)
        assert "a.txt" in rendered
        assert result.hunks[0].text in rendered
