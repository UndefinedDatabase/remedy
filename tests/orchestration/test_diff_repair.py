"""Tests for diff_repair.py (F111 T001).

Covers the eight pinned clauses of select_repair_hunks: margin clamping at
both file edges, overlap/adjacency merging, deterministic sort order,
binary omission, missing-path omission, the char budget, margin_lines=0,
empty range lists — plus exact-text fidelity of a carried hunk.

repo_root is a bare tmp_path: no git init, no fixtures beyond tmp_path,
matching tests/orchestration/test_fences.py.
"""

from __future__ import annotations

from packages.orchestration.diff_repair import (
    RepairHunk,
    RepairHunkSelection,
    select_repair_hunks,
)


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
