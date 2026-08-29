"""Property tests for F033's approved-subset diff builder.

One test per PROPERTY the subset turns on, named for the property rather than for the
function that implements it. The properties, in the order below: the ROUND TRIP — a subset
of every hunk applies byte-identically to applying the raw diff, and each hunk alone changes
only its own lines; the prefix map is load-bearing; headers come through verbatim; each of
the three refusal codes alone and the ORDER between them; a multi-FILE diff keeping file
order and dropping untouched files; a duplicate approval emitting once; and TOTALITY.

WHY ``_apply_hunks`` is imported despite the leading underscore: the round-trip property is
about the APPLIER's real behaviour, and only the real splicer can witness it. The public
``apply_structured_patch`` needs a repository, a job and a data directory that a pure text
test has no business building, so reaching for it would trade the property being tested for
a fixture. The private name is the smallest thing that proves the claim."""

from __future__ import annotations

import difflib

from packages.orchestration.diff_parser import parse_unified_diff_to_view
from packages.orchestration.hunk_subset_diff import (
    SUBSET_REFUSAL_ABSENT_HUNK,
    SUBSET_REFUSAL_NO_APPROVED_IDS,
    SUBSET_REFUSAL_UNTRUSTWORTHY_VIEW,
    ApprovedSubsetDiff,
    SubsetRefusal,
    build_approved_subset_diff,
)
from packages.orchestration.source_apply import _apply_hunks

ORIGINAL = "\n".join(f"line {number:02d}" for number in range(1, 21)) + "\n"


def _edited(*replacements: tuple[str, str]) -> str:
    """``ORIGINAL`` with each ``(old, new)`` whole line replaced."""
    text = ORIGINAL
    for old, new in replacements:
        text = text.replace(old + "\n", new + "\n")
    return text


def _diff_of(new_text: str, path: str = "f.txt", old_text: str = ORIGINAL) -> str:
    """A ``difflib`` unified diff carrying ``---``/``+++`` headers, the shape (a) the parser
    documents. Two well-separated edits give two hunks."""
    return "".join(
        difflib.unified_diff(
            old_text.splitlines(True), new_text.splitlines(True),
            fromfile=f"a/{path}", tofile=f"b/{path}",
        )
    )


TWO_EDITS = _edited(("line 03", "line 03 CHANGED"), ("line 15", "line 15 CHANGED"))
TWO_HUNK_DIFF = _diff_of(TWO_EDITS)


def _ids(diff_text: str, file_index: int = 0) -> list[str]:
    """The hunk ids of one file of ``diff_text``, in the diff's own order."""
    return [h["id"] for h in parse_unified_diff_to_view(diff_text)["files"][file_index]["hunks"]]


TWO_HUNK_IDS = _ids(TWO_HUNK_DIFF)


def test_a_subset_of_every_hunk_applies_exactly_as_the_raw_diff_does():
    result = build_approved_subset_diff(TWO_HUNK_DIFF, TWO_HUNK_IDS)
    assert isinstance(result, ApprovedSubsetDiff)
    assert [f.path for f in result.files] == ["f.txt"]
    assert result.selected == tuple(TWO_HUNK_IDS)
    assert _apply_hunks(ORIGINAL, result.files[0].diff) == _apply_hunks(ORIGINAL, TWO_HUNK_DIFF)
    assert _apply_hunks(ORIGINAL, result.files[0].diff) == TWO_EDITS


def test_one_approved_hunk_changes_its_own_lines_and_leaves_the_others_alone():
    for index, expected in (
        (0, _edited(("line 03", "line 03 CHANGED"))),
        (1, _edited(("line 15", "line 15 CHANGED"))),
    ):
        result = build_approved_subset_diff(TWO_HUNK_DIFF, [TWO_HUNK_IDS[index]])
        assert isinstance(result, ApprovedSubsetDiff)
        assert result.selected == (TWO_HUNK_IDS[index],)
        assert _apply_hunks(ORIGINAL, result.files[0].diff) == expected


def test_the_line_prefix_map_is_load_bearing():
    """Would fail if ``add`` and ``del`` were swapped: the deletion must quote the ORIGINAL
    line and the addition the NEW one, and a swapped emission no longer matches the file, so
    the applier refuses it outright."""
    emitted = build_approved_subset_diff(TWO_HUNK_DIFF, [TWO_HUNK_IDS[0]]).files[0].diff
    assert "-line 03\n" in emitted
    assert "+line 03 CHANGED\n" in emitted
    assert " line 04\n" in emitted
    assert "+line 03\n" not in emitted
    assert "-line 03 CHANGED\n" not in emitted
    swapped = emitted.replace("-line 03", "\x00").replace("+line 03 CHANGED", "-line 03 CHANGED")
    swapped = swapped.replace("\x00", "+line 03")
    assert _apply_hunks(ORIGINAL, swapped) is None


def test_a_header_is_re_emitted_character_for_character():
    source_headers = [line for line in TWO_HUNK_DIFF.split("\n") if line.startswith("@@")]
    emitted = build_approved_subset_diff(TWO_HUNK_DIFF, TWO_HUNK_IDS).files[0].diff
    assert [line for line in emitted.split("\n") if line.startswith("@@")] == source_headers
    # No renumbering: dropping the FIRST hunk leaves the second's header untouched.
    second = build_approved_subset_diff(TWO_HUNK_DIFF, [TWO_HUNK_IDS[1]]).files[0].diff
    assert second.split("\n")[0] == source_headers[1]


def test_an_emitted_file_carries_only_hunks_and_one_trailing_newline():
    emitted = build_approved_subset_diff(TWO_HUNK_DIFF, TWO_HUNK_IDS).files[0].diff
    assert emitted.endswith("\n") and not emitted.endswith("\n\n")
    assert "diff --git" not in emitted
    assert "--- " not in emitted and "+++ " not in emitted


def test_an_empty_approved_set_is_refused_rather_than_applying_nothing():
    result = build_approved_subset_diff(TWO_HUNK_DIFF, [])
    assert isinstance(result, SubsetRefusal)
    assert result.code == SUBSET_REFUSAL_NO_APPROVED_IDS
    assert result.hunk_ids == ()


def test_a_truncated_view_is_refused_and_blames_no_hunk():
    truncated = TWO_HUNK_DIFF + "[DIFF TRUNCATED]\n"
    assert parse_unified_diff_to_view(truncated)["truncated"] is True
    result = build_approved_subset_diff(truncated, [TWO_HUNK_IDS[0]])
    assert isinstance(result, SubsetRefusal)
    assert result.code == SUBSET_REFUSAL_UNTRUSTWORTHY_VIEW
    assert result.hunk_ids == ()


def test_a_hunk_in_a_file_the_parser_could_not_read_is_refused_by_name():
    noted = TWO_HUNK_DIFF + "# a marker the parser records as this file's note\n"
    assert parse_unified_diff_to_view(noted)["files"][0]["note"] is not None
    result = build_approved_subset_diff(noted, [TWO_HUNK_IDS[0]])
    assert isinstance(result, SubsetRefusal)
    assert result.code == SUBSET_REFUSAL_UNTRUSTWORTHY_VIEW
    assert result.hunk_ids == (TWO_HUNK_IDS[0],)


def test_a_hunk_in_a_binary_file_is_refused():
    binary = TWO_HUNK_DIFF + "Binary files a/f.txt and b/f.txt differ\n"
    assert parse_unified_diff_to_view(binary)["files"][0]["status"] == "binary"
    result = build_approved_subset_diff(binary, [TWO_HUNK_IDS[0]])
    assert isinstance(result, SubsetRefusal)
    assert result.code == SUBSET_REFUSAL_UNTRUSTWORTHY_VIEW


def test_an_untouched_unreadable_file_does_not_refuse_a_clean_selection():
    """The check is scoped to the files the SELECTION touches: a note on some other file is
    not this selection's problem, and refusing on it would make one bad region unapprovable."""
    other = _diff_of(_edited(("line 07", "line 07 CHANGED")), path="g.txt")
    combined = TWO_HUNK_DIFF + other + "# a marker on the SECOND file only\n"
    view = parse_unified_diff_to_view(combined)
    assert view["files"][0]["note"] is None and view["files"][1]["note"] is not None
    result = build_approved_subset_diff(combined, TWO_HUNK_IDS)
    assert isinstance(result, ApprovedSubsetDiff)
    assert [f.path for f in result.files] == ["f.txt"]


def test_an_id_the_diff_no_longer_carries_stops_the_apply():
    result = build_approved_subset_diff(TWO_HUNK_DIFF, ["deadbeefdeadbeef", TWO_HUNK_IDS[0]])
    assert isinstance(result, SubsetRefusal)
    assert result.code == SUBSET_REFUSAL_ABSENT_HUNK
    assert result.hunk_ids == ("deadbeefdeadbeef",)


def test_absent_ids_are_deduplicated_in_the_order_the_caller_gave_them():
    result = build_approved_subset_diff(TWO_HUNK_DIFF, ["zz", "aa", "zz"])
    assert result.hunk_ids == ("zz", "aa")


def test_an_untrustworthy_view_is_reported_before_an_absent_hunk():
    """Both codes trip at once. A truncated view is missing hunks it never showed, so absence
    is UNKNOWABLE while it is untrustworthy; reporting absence first would blame the
    operator's selection for the parser's ceiling."""
    truncated = TWO_HUNK_DIFF + "[DIFF TRUNCATED]\n"
    result = build_approved_subset_diff(truncated, ["deadbeefdeadbeef"])
    assert result.code == SUBSET_REFUSAL_UNTRUSTWORTHY_VIEW


def test_only_files_with_a_kept_hunk_appear_and_in_the_diffs_own_order():
    second = _diff_of(_edited(("line 07", "line 07 CHANGED")), path="g.txt")
    third = _diff_of(_edited(("line 09", "line 09 CHANGED")), path="h.txt")
    combined = TWO_HUNK_DIFF + second + third
    view = parse_unified_diff_to_view(combined)
    assert [f["path"] for f in view["files"]] == ["f.txt", "g.txt", "h.txt"]
    approved = [_ids(combined, 2)[0], _ids(combined, 0)[0]]
    result = build_approved_subset_diff(combined, approved)
    assert isinstance(result, ApprovedSubsetDiff)
    # The DIFF's order, never the caller's: h.txt was approved first and appears last.
    assert [f.path for f in result.files] == ["f.txt", "h.txt"]
    assert result.selected == (_ids(combined, 0)[0], _ids(combined, 2)[0])
    assert [f.hunk_ids for f in result.files] == [(result.selected[0],), (result.selected[1],)]


def test_a_hunk_approved_twice_is_emitted_once_and_is_not_a_refusal():
    once = build_approved_subset_diff(TWO_HUNK_DIFF, [TWO_HUNK_IDS[0]])
    twice = build_approved_subset_diff(TWO_HUNK_DIFF, [TWO_HUNK_IDS[0]] * 3)
    assert isinstance(twice, ApprovedSubsetDiff)
    assert twice == once


def test_no_input_raises_in_either_argument_position():
    hostile = (None, object(), 7, 3.5, b"bytes", {"a": 1}, "not a diff at all")
    for diff_argument in hostile + (TWO_HUNK_DIFF,):
        for ids_argument in hostile + (TWO_HUNK_IDS,):
            result = build_approved_subset_diff(diff_argument, ids_argument)
            assert isinstance(result, (ApprovedSubsetDiff, SubsetRefusal))


def test_an_id_that_is_not_a_string_is_compared_as_text():
    class Named:
        def __str__(self):
            return TWO_HUNK_IDS[0]

    result = build_approved_subset_diff(TWO_HUNK_DIFF, [Named()])
    assert isinstance(result, ApprovedSubsetDiff)
    assert result.selected == (TWO_HUNK_IDS[0],)
