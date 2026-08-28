"""Corpus tests for the F037 unified-diff view parser.

One test per shape the feature file's Task-slicing row for T001 lists, plus the
shapes `docs/roadmap/features/T5_F037.md` amendment A1 and A3 name. Every fixture
carries its diff text INLINE so a reader sees the input beside the expectation
rather than chasing a fixture directory.

The line-number test is the one that matters: it asserts the FULL ordered list of
`(kind, old_ln, new_ln, content)` tuples for a hunk holding context, additions and
deletions. That is the assertion the R1 source inventory showed the existing reader
in `packages/orchestration/review_scope.py` would fail — its hunk regex captures no
old-side line numbers at all — so it is written to catch that specific defect, not
merely to cover the function.
"""

from __future__ import annotations

import difflib
import re
import time

from packages.orchestration.diff_parser import (
    DIFF_INTRALINE_MIN_RATIO,
    DIFF_STATUS_ADDED,
    DIFF_STATUS_BINARY,
    DIFF_STATUS_DELETED,
    DIFF_STATUS_MODIFIED,
    DIFF_STATUS_RENAMED,
    DIFF_VIEW_MAX_BODY_LINES,
    DIFF_VIEW_STATUSES,
    DIFF_VIEW_VERSION,
    parse_unified_diff_to_view,
)

# --------------------------------------------------------------------------- #
# Inline fixtures — one per shape the feature file lists.
# --------------------------------------------------------------------------- #

#: Shape (a): plain modification, `difflib.unified_diff` as `_compute_safe_diff`
#: writes it into `safe.diff`.
MODIFIED_DIFF = (
    "--- a/pkg/app.py\n"
    "+++ b/pkg/app.py\n"
    "@@ -1,4 +1,5 @@ def render():\n"
    " alpha\n"
    "-beta\n"
    "+BETA\n"
    " gamma\n"
    "+inserted\n"
    " delta\n"
)

#: Shape (c): `repair_attest.build_safe_diff_text`'s untracked-file marker — the
#: `--- /dev/null` header and a `#` comment, with no hunk body at all.
ADDED_VIA_DEV_NULL_DIFF = (
    "--- /dev/null\n"
    "+++ b/pkg/brand_new.py\n"
    "# new untracked file (sha256=deadbeef, size=42)\n"
)

#: Shape (a): the SAME logical add, but as `difflib` renders it for a file whose
#: old side is empty — an all-zero old side rather than a `/dev/null` header.
ADDED_VIA_DIFFLIB_DIFF = (
    "--- a/pkg/fresh.py\n"
    "+++ b/pkg/fresh.py\n"
    "@@ -0,0 +1,3 @@\n"
    "+one\n"
    "+two\n"
    "+three\n"
)

DELETED_DIFF = (
    "--- a/pkg/gone.py\n"
    "+++ /dev/null\n"
    "@@ -1,3 +0,0 @@\n"
    "-one\n"
    "-two\n"
    "-three\n"
)

#: Shape (b): real `git diff` output, whose rename is carried by the
#: `rename from`/`rename to` pair and NOT by the header paths alone.
RENAMED_DIFF = (
    "diff --git a/pkg/old_name.py b/pkg/new_name.py\n"
    "similarity index 92%\n"
    "rename from pkg/old_name.py\n"
    "rename to pkg/new_name.py\n"
    "index 1111111..2222222 100644\n"
    "--- a/pkg/old_name.py\n"
    "+++ b/pkg/new_name.py\n"
    "@@ -1,3 +1,3 @@\n"
    " one\n"
    "-two\n"
    "+TWO\n"
    " three\n"
)

#: `pingpong_loop._compute_safe_diff` emits this literal for an extension in
#: `_BINARY_EXTENSIONS`; git's own `Binary files ... differ` is the other spelling.
BINARY_DIFF = (
    "--- a/assets/logo.png\n"
    "+++ b/assets/logo.png\n"
    "[binary file]\n"
)

MULTI_FILE_DIFF = (
    "--- a/first.txt\n"
    "+++ b/first.txt\n"
    "@@ -1,1 +1,1 @@\n"
    "-a\n"
    "+A\n"
    "--- a/second.txt\n"
    "+++ b/second.txt\n"
    "@@ -1,1 +1,1 @@\n"
    "-b\n"
    "+B\n"
)

#: Two hunks in one file: the second hunk's numbering must be seeded from its OWN
#: header, never continued from where the first hunk stopped.
MULTI_HUNK_DIFF = (
    "--- a/pkg/two_hunks.py\n"
    "+++ b/pkg/two_hunks.py\n"
    "@@ -1,2 +1,2 @@\n"
    " head\n"
    "-old-one\n"
    "+new-one\n"
    "@@ -40,2 +40,3 @@ class Far:\n"
    " far-context\n"
    "-far-old\n"
    "+far-new\n"
    "+far-extra\n"
)

#: `pingpong_loop._compute_safe_diff` appends this once its char cap is hit.
TRUNCATED_DIFF = (
    "--- a/pkg/big.py\n"
    "+++ b/pkg/big.py\n"
    "@@ -1,1 +1,1 @@\n"
    "-a\n"
    "+b\n"
    "\n"
    "[DIFF TRUNCATED]\n"
)

NO_NEWLINE_DIFF = (
    "--- a/pkg/tail.py\n"
    "+++ b/pkg/tail.py\n"
    "@@ -1,2 +1,2 @@\n"
    " keep\n"
    "-old\n"
    "\\ No newline at end of file\n"
    "+new\n"
    "\\ No newline at end of file\n"
)


def _emitter_shaped_workspace_file_diff(
    rel_path: str, repo_lines: list[str], ws_lines: list[str], repeats: int = 1
) -> str:
    """Reproduce one file's emission by `job_evidence._build_workspace_diff`.

    That emitter appends `--- a/<rel>` and `+++ b/<rel>` ITSELF and then appends
    `difflib.unified_diff(..., fromfile="a/<rel>", tofile="b/<rel>", lineterm="")`,
    whose own first two lines are that SAME pair — so every file in `workspace.diff`
    carries the header pair TWICE. That doubling is finding `R-0716`. The fixture is
    GENERATED from `difflib` rather than typed out so it cannot drift away from the
    producer it stands for, and `repeats` lets a test push the echo past two.
    """
    out = [f"--- a/{rel_path}", f"+++ b/{rel_path}"] * repeats
    out.extend(
        line.rstrip()
        for line in difflib.unified_diff(
            repo_lines,
            ws_lines,
            fromfile=f"a/{rel_path}",
            tofile=f"b/{rel_path}",
            lineterm="",
        )
    )
    out.append("")
    return "\n".join(out) + "\n"


#: The `workspace.diff` shape in full: `job_evidence`'s `#` preamble, then one file
#: whose header pair appears twice. `R-0716`: the parser read this as TWO files.
WORKSPACE_DOUBLED_HEADER_DIFF = (
    "# Job workspace diff (workspace vs original target repo)\n"
    "# Workspace: <workspace>\n"
    "# Repo: <repo>\n"
    "\n"
) + _emitter_shaped_workspace_file_diff(
    "pkg/app.py",
    ["alpha\n", "beta\n", "gamma\n"],
    ["alpha\n", "BETA\n", "gamma\n"],
)

#: The same shape with the header pair written THREE times, because the collapse is
#: applied repeatedly rather than exactly once.
WORKSPACE_TRIPLED_HEADER_DIFF = _emitter_shaped_workspace_file_diff(
    "pkg/app.py",
    ["alpha\n", "beta\n", "gamma\n"],
    ["alpha\n", "BETA\n", "gamma\n"],
    repeats=3,
)

#: The `R-0716` guard: `repair_attest.build_safe_diff_text` puts a TRACKED region and
#: an UNTRACKED `--- /dev/null` marker for ONE path into `safe.diff`, and those are
#: two distinct facts. The tracked region here is deliberately hunkless so that every
#: other fold precondition holds and ONLY the header-pair comparison keeps the two
#: entries apart — a collapse written against the resolved PATH would merge them.
SAME_PATH_DIFFERENT_HEADERS_DIFF = (
    "--- a/pkg/thing.py\n"
    "+++ b/pkg/thing.py\n"
    "--- /dev/null\n"
    "+++ b/pkg/thing.py\n"
    "# new untracked file (sha256=cafe, size=7)\n"
)

#: One word changes inside one line — the fixture the feature file's Acceptance names
#: for intraline highlighting. `brown` becomes `blue` and nothing else moves.
INTRALINE_WORD_DIFF = (
    "--- a/pkg/greet.py\n"
    "+++ b/pkg/greet.py\n"
    "@@ -1,1 +1,1 @@\n"
    "-the quick brown fox\n"
    "+the quick blue fox\n"
)

#: A pair with almost nothing in common. Marking every character of both lines says
#: no more than marking none, so the similarity guard emits `[]` on both.
INTRALINE_WHOLE_LINE_REPLACEMENT_DIFF = (
    "--- a/pkg/swap.py\n"
    "+++ b/pkg/swap.py\n"
    "@@ -1,1 +1,1 @@\n"
    "-alpha\n"
    "+zulu\n"
)

#: One deletion against TWO additions: the first addition pairs, the second is
#: surplus with no line to compare against. The `ctx` line is here for the same test.
INTRALINE_UNEVEN_RUNS_DIFF = (
    "--- a/pkg/uneven.py\n"
    "+++ b/pkg/uneven.py\n"
    "@@ -1,2 +1,3 @@\n"
    " head\n"
    "-the quick brown fox\n"
    "+the quick blue fox\n"
    "+tail added line\n"
)

#: `R-0717`: a pair whose token diff is a BARE `delete` opcode — the new line is the
#: old line with an interior run of words removed and nothing else touched. Every
#: other intraline fixture in this file produces only `equal` and `replace`, so
#: before this one the `delete` half of the old-side opcode tuple was unpinned.
INTRALINE_PURE_DELETION_DIFF = (
    "--- a/pkg/pure_del.py\n"
    "+++ b/pkg/pure_del.py\n"
    "@@ -1,1 +1,1 @@\n"
    "-keep the extra words here\n"
    "+keep the words here\n"
)

#: `R-0717`, the mirror: a pair whose token diff is a BARE `insert` opcode, pinning
#: the `insert` half of the new-side tuple.
INTRALINE_PURE_INSERTION_DIFF = (
    "--- a/pkg/pure_add.py\n"
    "+++ b/pkg/pure_add.py\n"
    "@@ -1,1 +1,1 @@\n"
    "-keep the words here\n"
    "+keep the extra words here\n"
)

#: `R-0718`: two MULTI-WORD lines sharing no word at all. Over the full token stream
#: their ratio is 0.400 — floored by the matching separators alone — so the guard
#: could not fire and every word of both lines was marked. The single-word
#: `alpha`/`zulu` pair below is the one shape with no such floor, which is why it
#: passed while the guard it tests was inert for every real line.
INTRALINE_MULTI_WORD_NO_SHARED_WORD_DIFF = (
    "--- a/pkg/nothing_shared.py\n"
    "+++ b/pkg/nothing_shared.py\n"
    "@@ -1,1 +1,1 @@\n"
    "-alpha beta gamma\n"
    "+zzz qqq www\n"
)

#: `R-0718`'s other side: a multi-word pair that SHARES most of its words must still
#: be marked word-by-word. Narrowing the ratio's stream must not narrow what it lets
#: through.
INTRALINE_MULTI_WORD_ONE_WORD_CHANGED_DIFF = (
    "--- a/pkg/one_word.py\n"
    "+++ b/pkg/one_word.py\n"
    "@@ -1,1 +1,1 @@\n"
    "-the fox jumps\n"
    "+the cat jumps\n"
)


def _tuples(hunk: dict) -> list[tuple]:
    """Reduce a hunk's lines to the four fields the viewer actually renders."""
    return [(ln["kind"], ln["old_ln"], ln["new_ln"], ln["content"]) for ln in hunk["lines"]]


# --------------------------------------------------------------------------- #
# One test per shape.
# --------------------------------------------------------------------------- #


def test_parse_unified_diff_to_view_reads_a_plain_modification():
    view = parse_unified_diff_to_view(MODIFIED_DIFF)

    assert view["version"] == DIFF_VIEW_VERSION
    assert view["truncated"] is False
    assert len(view["files"]) == 1
    entry = view["files"][0]
    assert entry["path"] == "pkg/app.py"
    assert entry["old_path"] is None
    assert entry["status"] == DIFF_STATUS_MODIFIED
    assert entry["stats"] == {"added": 2, "deleted": 1}
    assert len(entry["hunks"]) == 1
    # The section heading is part of the header the viewer renders, so it is kept
    # verbatim rather than parsed away.
    assert entry["hunks"][0]["header"] == "@@ -1,4 +1,5 @@ def render():"
    assert entry["hunks"][0]["old_start"] == 1
    assert entry["hunks"][0]["new_start"] == 1


def test_parse_unified_diff_to_view_reads_an_add_via_dev_null_header():
    view = parse_unified_diff_to_view(ADDED_VIA_DEV_NULL_DIFF)

    assert len(view["files"]) == 1
    entry = view["files"][0]
    assert entry["path"] == "pkg/brand_new.py"
    assert entry["status"] == DIFF_STATUS_ADDED
    assert entry["hunks"] == []
    # The `#` marker is the only explanation of an empty region, so it is carried.
    assert entry["note"] == "# new untracked file (sha256=deadbeef, size=42)"


def test_parse_unified_diff_to_view_reads_an_add_with_an_all_zero_old_side():
    view = parse_unified_diff_to_view(ADDED_VIA_DIFFLIB_DIFF)

    entry = view["files"][0]
    assert entry["path"] == "pkg/fresh.py"
    assert entry["status"] == DIFF_STATUS_ADDED
    assert entry["stats"] == {"added": 3, "deleted": 0}
    assert _tuples(entry["hunks"][0]) == [
        ("add", None, 1, "one"),
        ("add", None, 2, "two"),
        ("add", None, 3, "three"),
    ]


def test_parse_unified_diff_to_view_reads_a_deletion():
    view = parse_unified_diff_to_view(DELETED_DIFF)

    entry = view["files"][0]
    assert entry["path"] == "pkg/gone.py"
    assert entry["status"] == DIFF_STATUS_DELETED
    assert entry["stats"] == {"added": 0, "deleted": 3}
    assert _tuples(entry["hunks"][0]) == [
        ("del", 1, None, "one"),
        ("del", 2, None, "two"),
        ("del", 3, None, "three"),
    ]


def test_parse_unified_diff_to_view_reads_a_git_rename_and_keeps_the_old_path():
    view = parse_unified_diff_to_view(RENAMED_DIFF)

    entry = view["files"][0]
    assert entry["status"] == DIFF_STATUS_RENAMED
    assert entry["path"] == "pkg/new_name.py"
    assert entry["old_path"] == "pkg/old_name.py"
    assert entry["stats"] == {"added": 1, "deleted": 1}


def test_parse_unified_diff_to_view_reads_the_binary_sentinel():
    view = parse_unified_diff_to_view(BINARY_DIFF)

    entry = view["files"][0]
    assert entry["path"] == "assets/logo.png"
    assert entry["status"] == DIFF_STATUS_BINARY
    assert entry["note"] == "[binary file]"
    assert entry["hunks"] == []


def test_parse_unified_diff_to_view_reads_empty_input_as_no_files():
    assert parse_unified_diff_to_view("") == {
        "version": 1,
        "truncated": False,
        "files": [],
    }


def test_parse_unified_diff_to_view_reads_non_diff_text_as_no_files():
    view = parse_unified_diff_to_view("hello world\nthis is not a diff at all\n")

    assert view == {"version": 1, "truncated": False, "files": []}


def test_parse_unified_diff_to_view_keeps_input_order_and_distinct_hunk_ids():
    view = parse_unified_diff_to_view(MULTI_FILE_DIFF)

    assert [f["path"] for f in view["files"]] == ["first.txt", "second.txt"]
    ids = [h["id"] for f in view["files"] for h in f["hunks"]]
    assert ids == ["0:0", "1:0"]
    assert len(set(ids)) == len(ids)


def test_parse_unified_diff_to_view_seeds_each_hunk_from_its_own_header():
    view = parse_unified_diff_to_view(MULTI_HUNK_DIFF)

    entry = view["files"][0]
    assert [h["id"] for h in entry["hunks"]] == ["0:0", "0:1"]
    first, second = entry["hunks"]
    assert (first["old_start"], first["new_start"]) == (1, 1)
    assert (second["old_start"], second["new_start"]) == (40, 40)
    assert _tuples(first) == [
        ("ctx", 1, 1, "head"),
        ("del", 2, None, "old-one"),
        ("add", None, 2, "new-one"),
    ]
    # The second hunk restarts at 40/40 rather than continuing the first hunk's
    # counters, which is the whole reason both starts are captured.
    assert _tuples(second) == [
        ("ctx", 40, 40, "far-context"),
        ("del", 41, None, "far-old"),
        ("add", None, 41, "far-new"),
        ("add", None, 42, "far-extra"),
    ]


# --------------------------------------------------------------------------- #
# The assertion that matters: both sides of every line, in order.
# --------------------------------------------------------------------------- #


def test_parse_unified_diff_to_view_numbers_both_sides_of_every_line():
    """Assert the FULL ordered tuple list, so a dropped old side cannot pass.

    `review_scope.py`'s reader captures only the new-side start; a parser with the
    same defect would still produce the right `kind` sequence and the right
    `content`, and would still get `new_ln` right. Only the `old_ln` column
    distinguishes it, so every `old_ln` is pinned here explicitly.
    """
    view = parse_unified_diff_to_view(MODIFIED_DIFF)

    assert _tuples(view["files"][0]["hunks"][0]) == [
        ("ctx", 1, 1, "alpha"),
        ("del", 2, None, "beta"),
        ("add", None, 2, "BETA"),
        ("ctx", 3, 3, "gamma"),
        ("add", None, 4, "inserted"),
        ("ctx", 4, 5, "delta"),
    ]


# --------------------------------------------------------------------------- #
# Further pins.
# --------------------------------------------------------------------------- #


def test_diff_view_statuses_holds_exactly_the_five_viewer_statuses():
    assert DIFF_VIEW_STATUSES == frozenset(
        {"added", "modified", "deleted", "renamed", "binary"}
    )
    assert DIFF_STATUS_ADDED == "added"
    assert DIFF_STATUS_MODIFIED == "modified"
    assert DIFF_STATUS_DELETED == "deleted"
    assert DIFF_STATUS_RENAMED == "renamed"
    assert DIFF_STATUS_BINARY == "binary"


def test_parse_unified_diff_to_view_marks_a_truncated_diff():
    view = parse_unified_diff_to_view(TRUNCATED_DIFF)

    assert view["truncated"] is True
    assert view["files"][0]["path"] == "pkg/big.py"


def test_parse_unified_diff_to_view_drops_the_no_newline_marker():
    view = parse_unified_diff_to_view(NO_NEWLINE_DIFF)

    lines = view["files"][0]["hunks"][0]["lines"]
    assert all("No newline" not in ln["content"] for ln in lines)
    assert _tuples(view["files"][0]["hunks"][0]) == [
        ("ctx", 1, 1, "keep"),
        ("del", 2, None, "old"),
        ("add", None, 2, "new"),
    ]


def test_every_file_stats_equal_a_recount_of_its_own_parsed_lines():
    """Assert the PROPERTY across the whole corpus, never a transcribed number."""
    corpus = [
        MODIFIED_DIFF,
        ADDED_VIA_DEV_NULL_DIFF,
        ADDED_VIA_DIFFLIB_DIFF,
        DELETED_DIFF,
        RENAMED_DIFF,
        BINARY_DIFF,
        MULTI_FILE_DIFF,
        MULTI_HUNK_DIFF,
        TRUNCATED_DIFF,
        NO_NEWLINE_DIFF,
        "",
    ]
    seen = 0
    for diff_text in corpus:
        view = parse_unified_diff_to_view(diff_text)
        for entry in view["files"]:
            seen += 1
            kinds = [ln["kind"] for hunk in entry["hunks"] for ln in hunk["lines"]]
            assert entry["stats"]["added"] == kinds.count("add")
            assert entry["stats"]["deleted"] == kinds.count("del")
            assert entry["status"] in DIFF_VIEW_STATUSES
    assert seen > 0


# --------------------------------------------------------------------------- #
# R-0716: the `workspace.diff` doubled header pair, and the guard on the fix.
# --------------------------------------------------------------------------- #


def test_parse_unified_diff_to_view_collapses_the_doubled_workspace_header():
    """`R-0716`: one file emitted with its header pair twice is ONE file entry.

    Before the repair this returned two entries — a phantom with no hunks, zero
    stats and no note, which a sidebar would render as a real changed file holding
    nothing.
    """
    view = parse_unified_diff_to_view(WORKSPACE_DOUBLED_HEADER_DIFF)

    assert len(view["files"]) == 1
    entry = view["files"][0]
    assert entry["path"] == "pkg/app.py"
    assert entry["old_path"] is None
    assert entry["status"] == DIFF_STATUS_MODIFIED
    assert entry["note"] is None
    assert entry["stats"] == {"added": 1, "deleted": 1}
    assert len(entry["hunks"]) == 1
    assert _tuples(entry["hunks"][0]) == [
        ("ctx", 1, 1, "alpha"),
        ("del", 2, None, "beta"),
        ("add", None, 2, "BETA"),
        ("ctx", 3, 3, "gamma"),
    ]


def test_parse_unified_diff_to_view_collapses_three_repeats_as_cleanly_as_two():
    view = parse_unified_diff_to_view(WORKSPACE_TRIPLED_HEADER_DIFF)

    assert len(view["files"]) == 1
    assert view["files"][0]["path"] == "pkg/app.py"
    assert view["files"][0]["stats"] == {"added": 1, "deleted": 1}


def test_parse_unified_diff_to_view_keeps_two_regions_for_one_path():
    """The `R-0716` guard: same resolved path, DIFFERENT header pairs, two entries."""
    view = parse_unified_diff_to_view(SAME_PATH_DIFFERENT_HEADERS_DIFF)

    assert len(view["files"]) == 2
    assert [f["path"] for f in view["files"]] == ["pkg/thing.py", "pkg/thing.py"]
    tracked, untracked = view["files"]
    assert tracked["status"] == DIFF_STATUS_MODIFIED
    assert tracked["note"] is None
    assert untracked["status"] == DIFF_STATUS_ADDED
    assert untracked["note"] == "# new untracked file (sha256=cafe, size=7)"


# --------------------------------------------------------------------------- #
# Intraline spans.
# --------------------------------------------------------------------------- #


def _line_at(view: dict, kind: str, file_index: int = 0, hunk_index: int = 0) -> dict:
    """First line of the given kind in one hunk, so a test names what it means."""
    for line in view["files"][file_index]["hunks"][hunk_index]["lines"]:
        if line["kind"] == kind:
            return line
    raise AssertionError(f"no {kind} line in file {file_index} hunk {hunk_index}")


def test_intraline_spans_mark_only_the_word_that_changed():
    """The exact spans AND the text they slice out, because numbers alone hide drift."""
    view = parse_unified_diff_to_view(INTRALINE_WORD_DIFF)

    deleted = _line_at(view, "del")
    added = _line_at(view, "add")
    assert deleted["content"] == "the quick brown fox"
    assert added["content"] == "the quick blue fox"
    assert deleted["intraline"] == [[10, 5]]
    assert added["intraline"] == [[10, 4]]
    assert [deleted["content"][s:s + n] for s, n in deleted["intraline"]] == ["brown"]
    assert [added["content"][s:s + n] for s, n in added["intraline"]] == ["blue"]


def test_intraline_spans_are_empty_below_the_similarity_threshold():
    """Named against the exported constant, not against a transcribed 0.3."""
    view = parse_unified_diff_to_view(INTRALINE_WHOLE_LINE_REPLACEMENT_DIFF)

    deleted = _line_at(view, "del")
    added = _line_at(view, "add")
    ratio = difflib.SequenceMatcher(
        a=re.findall(r"\w+|\W", deleted["content"]),
        b=re.findall(r"\w+|\W", added["content"]),
    ).ratio()
    assert ratio < DIFF_INTRALINE_MIN_RATIO
    assert deleted["intraline"] == []
    assert added["intraline"] == []


def test_intraline_spans_are_empty_on_a_context_line():
    view = parse_unified_diff_to_view(INTRALINE_UNEVEN_RUNS_DIFF)

    context = _line_at(view, "ctx")
    assert context["content"] == "head"
    assert context["intraline"] == []


def test_intraline_spans_are_empty_on_a_surplus_unpaired_line():
    """One deletion, two additions: the second addition has no partner."""
    view = parse_unified_diff_to_view(INTRALINE_UNEVEN_RUNS_DIFF)

    lines = view["files"][0]["hunks"][0]["lines"]
    added = [ln for ln in lines if ln["kind"] == "add"]
    assert [ln["content"] for ln in added] == ["the quick blue fox", "tail added line"]
    assert added[0]["intraline"] == [[10, 4]]
    assert added[1]["intraline"] == []


def test_intraline_spans_mark_a_pure_deletion_on_the_del_side_only():
    """`R-0717`: a bare `delete` opcode marks the OLD side and leaves the NEW side bare.

    The old-side opcode tuple carries `delete` beside `replace`, and until this
    fixture existed nothing in the corpus produced a `delete` at all: narrowing that
    tuple to `("replace",)` left the whole suite green. The `[]` on the `add` entry
    is the other half of the pin — a mapping that let `delete` reach the new side
    would mark text that was never added.
    """
    view = parse_unified_diff_to_view(INTRALINE_PURE_DELETION_DIFF)

    deleted = _line_at(view, "del")
    added = _line_at(view, "add")
    assert deleted["content"] == "keep the extra words here"
    assert added["content"] == "keep the words here"
    assert deleted["intraline"] == [[9, 6]]
    assert [deleted["content"][s:s + n] for s, n in deleted["intraline"]] == ["extra "]
    assert added["intraline"] == []


def test_intraline_spans_mark_a_pure_insertion_on_the_add_side_only():
    """`R-0717`, mirrored: a bare `insert` opcode marks the NEW side only."""
    view = parse_unified_diff_to_view(INTRALINE_PURE_INSERTION_DIFF)

    deleted = _line_at(view, "del")
    added = _line_at(view, "add")
    assert deleted["content"] == "keep the words here"
    assert added["content"] == "keep the extra words here"
    assert added["intraline"] == [[9, 6]]
    assert [added["content"][s:s + n] for s, n in added["intraline"]] == ["extra "]
    assert deleted["intraline"] == []


def _significant_tokens(content: str) -> list[str]:
    """The test's own reading of "not pure whitespace", written out rather than imported.

    A test that imported the module's helper would agree with the module by
    construction and could never notice it drifting.
    """
    return [token for token in re.findall(r"\w+|\W", content) if token.strip() != ""]


def test_intraline_spans_are_empty_for_multi_word_lines_that_share_no_word():
    """`R-0718`: the guard fires for a MULTI-WORD pair, not only for a one-word one.

    Named against the exported constant, not against a transcribed 0.3, and computed
    over the significant tokens because that is the stream the guard now reads.
    """
    view = parse_unified_diff_to_view(INTRALINE_MULTI_WORD_NO_SHARED_WORD_DIFF)

    deleted = _line_at(view, "del")
    added = _line_at(view, "add")
    assert deleted["content"] == "alpha beta gamma"
    assert added["content"] == "zzz qqq www"
    ratio = difflib.SequenceMatcher(
        a=_significant_tokens(deleted["content"]),
        b=_significant_tokens(added["content"]),
    ).ratio()
    assert ratio < DIFF_INTRALINE_MIN_RATIO
    assert deleted["intraline"] == []
    assert added["intraline"] == []


def test_intraline_spans_still_mark_a_multi_word_pair_that_shares_its_other_words():
    """`R-0718`'s regression guard: a real one-word edit is still marked word-by-word."""
    view = parse_unified_diff_to_view(INTRALINE_MULTI_WORD_ONE_WORD_CHANGED_DIFF)

    deleted = _line_at(view, "del")
    added = _line_at(view, "add")
    ratio = difflib.SequenceMatcher(
        a=_significant_tokens(deleted["content"]),
        b=_significant_tokens(added["content"]),
    ).ratio()
    assert ratio >= DIFF_INTRALINE_MIN_RATIO
    assert deleted["intraline"] == [[4, 3]]
    assert added["intraline"] == [[4, 3]]
    assert [deleted["content"][s:s + n] for s, n in deleted["intraline"]] == ["fox"]
    assert [added["content"][s:s + n] for s, n in added["intraline"]] == ["cat"]


def test_every_intraline_span_lies_inside_its_own_content():
    """The property over EVERY `*_DIFF` fixture in this file, gathered so it cannot go stale."""
    fixtures = sorted(
        name
        for name, value in list(globals().items())
        if name.endswith("_DIFF") and isinstance(value, str)
    )
    assert len(fixtures) >= 15
    spans_seen = 0
    lines_seen = 0
    for name in fixtures:
        view = parse_unified_diff_to_view(globals()[name])
        for entry in view["files"]:
            for hunk in entry["hunks"]:
                for line in hunk["lines"]:
                    lines_seen += 1
                    assert "intraline" in line, name
                    assert isinstance(line["intraline"], list), name
                    if line["kind"] == "ctx":
                        assert line["intraline"] == [], name
                    previous_end = -1
                    for span in line["intraline"]:
                        assert isinstance(span, list) and len(span) == 2, (name, span)
                        start, length = span
                        assert start >= 0, (name, span)
                        assert length > 0, (name, span)
                        assert start + length <= len(line["content"]), (name, span)
                        # Sorted by start, and merged: touching spans cannot survive.
                        assert start > previous_end, (name, span)
                        previous_end = start + length
                        spans_seen += 1
    assert lines_seen > 0
    assert spans_seen > 0


def test_parse_unified_diff_to_view_reads_real_difflib_output():
    """The generator itself, not a hand-typed imitation of it."""
    old = ["alpha\n", "beta\n", "gamma\n"]
    new = ["alpha\n", "BETA\n", "gamma\n"]
    diff_text = "".join(
        difflib.unified_diff(old, new, fromfile="a/real.txt", tofile="b/real.txt")
    )

    view = parse_unified_diff_to_view(diff_text)

    assert [f["path"] for f in view["files"]] == ["real.txt"]
    assert view["files"][0]["status"] == DIFF_STATUS_MODIFIED
    assert _tuples(view["files"][0]["hunks"][0]) == [
        ("ctx", 1, 1, "alpha"),
        ("del", 2, None, "beta"),
        ("add", None, 2, "BETA"),
        ("ctx", 3, 3, "gamma"),
    ]


# --------------------------------------------------------------------------- #
# The huge shape — the last row of T001's task slicing, and Acceptance's budget.
# --------------------------------------------------------------------------- #

#: Acceptance in `docs/roadmap/features/T5_F037.md` names a "10k-line fixture within
#: the perf budget (recorded)". This is that fixture's BODY-line count. It must be
#: even: the body is written as alternating deletion/addition PAIRS.
HUGE_DIFF_BODY_LINE_COUNT = 10_000

#: The many-FILES dimension of the same shape, kept separate from the many-LINES one
#: because the parser opens a region per file and a hunk per header, and a defect can
#: live in either loop alone.
MANY_FILE_DIFF_FILE_COUNT = 400

#: The GENEROUS absolute ceiling the budget test below asserts against. The measured
#: figure it is set against, and why it is deliberately NOT that figure, are recorded
#: in `test_the_huge_diff_parses_inside_the_recorded_perf_budget`.
HUGE_DIFF_PARSE_CEILING_SECONDS = 0.5


def _generated_huge_single_file_diff(
    body_line_count: int, path: str = "pkg/huge_module.py"
) -> str:
    """One file with `body_line_count` body lines, as alternating `-`/`+` pairs.

    GENERATED rather than typed out — the one exception to this module's docstring
    rule that every fixture carries its diff text INLINE — because ten thousand
    literal body lines would bury every other fixture in the file and show a reader
    nothing the fourth line does not already show.
    """
    pair_count = body_line_count // 2
    lines = [
        f"diff --git a/{path} b/{path}",
        f"--- a/{path}",
        f"+++ b/{path}",
        f"@@ -1,{pair_count} +1,{pair_count} @@",
    ]
    for index in range(pair_count):
        lines.append(f"-old body line {index}")
        lines.append(f"+new body line {index}")
    return "\n".join(lines) + "\n"


def _generated_many_file_diff(file_count: int) -> str:
    """`file_count` files, one one-line hunk each, in a single diff text.

    Generated for the same reason as the single-file builder above: several hundred
    header pairs written out inline are unreadable, and the shape they stand for —
    many small files rather than one enormous one — is the other half of what a real
    `workspace.diff` looks like.
    """
    lines: list[str] = []
    for index in range(file_count):
        path = f"pkg/module_{index:04d}.py"
        lines.extend(
            [
                f"diff --git a/{path} b/{path}",
                f"--- a/{path}",
                f"+++ b/{path}",
                "@@ -1,1 +1,1 @@",
                f"-old line in {path}",
                f"+new line in {path}",
            ]
        )
    return "\n".join(lines) + "\n"


def test_the_huge_single_file_diff_parses_to_one_complete_file():
    """Every generated body line survives into exactly one file entry.

    Asserted as a PROPERTY against the generated size, never against a transcribed
    literal, the way `test_every_file_stats_equal_a_recount_of_its_own_parsed_lines`
    does it. A parser that silently stopped appending after some internal cap would
    pass every other test in this file, all of whose fixtures are a few dozen lines
    at most; this is the only assertion in the corpus that can see such a cap.
    """
    diff_text = _generated_huge_single_file_diff(HUGE_DIFF_BODY_LINE_COUNT)

    view = parse_unified_diff_to_view(diff_text)

    assert view["truncated"] is False
    assert len(view["files"]) == 1
    entry = view["files"][0]
    assert entry["path"] == "pkg/huge_module.py"
    assert entry["status"] == DIFF_STATUS_MODIFIED
    lines = [line for hunk in entry["hunks"] for line in hunk["lines"]]
    assert len(lines) == HUGE_DIFF_BODY_LINE_COUNT
    kinds = [line["kind"] for line in lines]
    assert entry["stats"]["added"] == kinds.count("add")
    assert entry["stats"]["deleted"] == kinds.count("del")
    assert entry["stats"]["added"] == HUGE_DIFF_BODY_LINE_COUNT // 2
    assert entry["stats"]["deleted"] == HUGE_DIFF_BODY_LINE_COUNT // 2
    hunk_ids = [hunk["id"] for hunk in entry["hunks"]]
    assert len(set(hunk_ids)) == len(hunk_ids)


def test_line_numbering_survives_the_whole_huge_file():
    """Both counters stay monotonic over ten thousand lines, and land where they must.

    The shapes already in the corpus are three or four lines long, so a counter that
    drifts only after thousands of lines — an off-by-one that compounds, a reset on
    some interior condition — is invisible to all of them. Here the old-side numbers
    of the deletions and the new-side numbers of the additions are each checked for
    STRICT increase across the entire file, and the final line is checked against the
    number its own position implies.
    """
    pair_count = HUGE_DIFF_BODY_LINE_COUNT // 2
    diff_text = _generated_huge_single_file_diff(HUGE_DIFF_BODY_LINE_COUNT)

    view = parse_unified_diff_to_view(diff_text)

    lines = [line for hunk in view["files"][0]["hunks"] for line in hunk["lines"]]
    old_numbers = [line["old_ln"] for line in lines if line["kind"] == "del"]
    new_numbers = [line["new_ln"] for line in lines if line["kind"] == "add"]
    assert len(old_numbers) == pair_count
    assert len(new_numbers) == pair_count
    assert all(later > earlier for earlier, later in zip(old_numbers, old_numbers[1:]))
    assert all(later > earlier for earlier, later in zip(new_numbers, new_numbers[1:]))
    assert (old_numbers[0], new_numbers[0]) == (1, 1)
    assert (old_numbers[-1], new_numbers[-1]) == (pair_count, pair_count)
    last = lines[-1]
    assert (last["kind"], last["old_ln"], last["new_ln"]) == ("add", None, pair_count)
    assert last["content"] == f"new body line {pair_count - 1}"


def test_the_many_file_diff_keeps_every_file_distinct_and_in_input_order():
    """Several hundred files stay several hundred file entries, in order, none empty.

    Worth asserting at scale because of the doubled-header collapse `R-0716` added:
    that fold walks the region list backwards and drops entries, so a mistake in it
    costs FILES rather than lines, and the corpus's other multi-file fixtures hold
    two or three.
    """
    diff_text = _generated_many_file_diff(MANY_FILE_DIFF_FILE_COUNT)
    # Read the expectation back out of the generated TEXT rather than out of the
    # builder's own formatting, so it is not true by construction.
    expected_paths = [
        line[len("+++ b/"):]
        for line in diff_text.split("\n")
        if line.startswith("+++ b/")
    ]
    assert len(expected_paths) == MANY_FILE_DIFF_FILE_COUNT
    assert len(set(expected_paths)) == MANY_FILE_DIFF_FILE_COUNT

    view = parse_unified_diff_to_view(diff_text)

    assert len(view["files"]) == MANY_FILE_DIFF_FILE_COUNT
    assert [entry["path"] for entry in view["files"]] == expected_paths
    # No phantom entries: every file carries the one hunk it was generated with.
    assert all(len(entry["hunks"]) == 1 for entry in view["files"])
    assert all(entry["stats"] == {"added": 1, "deleted": 1} for entry in view["files"])
    hunk_ids = [hunk["id"] for entry in view["files"] for hunk in entry["hunks"]]
    assert len(set(hunk_ids)) == len(hunk_ids)


def test_the_huge_diff_parses_inside_the_recorded_perf_budget():
    """The perf figure Acceptance asks to have RECORDED, and a complexity guard on it.

    MEASURED 2026-08-28 on the machine this feature is being built on — a Linux
    x86-64 development workstation, CPython 3, unloaded — as the median of fifteen
    parses of this exact fixture: 0.105 s for 10,000 body lines, against 0.010 s for
    1,000 and 0.021 s for 2,000. The cost is LINEAR at roughly 10 microseconds per
    body line, and a 400-file shape scales the same way.

    THE CEILING IS NOT THAT FIGURE. `HUGE_DIFF_PARSE_CEILING_SECONDS` is 0.5 s, about
    five times the measured median, so a runner five times slower than this one still
    passes and this assertion never becomes a report on machine speed. What it is
    for is a change of COMPLEXITY CLASS: a parser scaling as N squared while matching
    today's cost at 1,000 body lines would need about 1.0 s at 10,000 — a hundred
    times the 1,000-line figure — which is twice the ceiling. The ceiling therefore
    sits BETWEEN the two cases rather than merely above the good one.

    It is deliberately not a full order of magnitude above the measurement: 1.0 s is
    exactly where the quadratic case lands, so a ten-times ceiling would pass both
    and record nothing. Anyone tightening this below about 0.35 s is policing a
    machine rather than a complexity class, and should not.
    """
    diff_text = _generated_huge_single_file_diff(HUGE_DIFF_BODY_LINE_COUNT)

    started = time.perf_counter()
    view = parse_unified_diff_to_view(diff_text)
    elapsed = time.perf_counter() - started

    # A budget met by parsing nothing is not a budget: pin the work first.
    assert len(view["files"]) == 1
    parsed_lines = sum(len(hunk["lines"]) for hunk in view["files"][0]["hunks"])
    assert parsed_lines == HUGE_DIFF_BODY_LINE_COUNT
    assert elapsed < HUGE_DIFF_PARSE_CEILING_SECONDS, (
        f"parsing {HUGE_DIFF_BODY_LINE_COUNT} body lines took {elapsed:.3f}s, "
        f"ceiling {HUGE_DIFF_PARSE_CEILING_SECONDS}s"
    )


# --------------------------------------------------------------------------- #
# The parse ceiling — DECISION F037 D5, the parser half of finding `R-0721`.
# --------------------------------------------------------------------------- #

#: A file count whose TOTAL body lines exceed the ceiling. `_generated_many_file_diff`
#: writes one deletion and one addition per file, so half the ceiling's own value is
#: exactly the ceiling, and the extra files are the ones that must not appear at all in
#: the truncated view. Expressed in the two constants rather than as a literal so it
#: follows the ceiling if DECISION F037 D5 is ever re-decided.
TRUNCATING_MANY_FILE_COUNT = DIFF_VIEW_MAX_BODY_LINES // 2 + MANY_FILE_DIFF_FILE_COUNT


def _total_parsed_body_lines(view: dict) -> int:
    """Body lines the view actually carries, summed across every file and hunk.

    The ceiling is a property of the WHOLE payload, so the quantity every ceiling
    assertion below reads is this total and never one file's share of it.
    """
    return sum(len(hunk["lines"]) for entry in view["files"] for hunk in entry["hunks"])


def test_a_diff_far_above_the_ceiling_stops_at_exactly_the_ceiling():
    """The bound bites, and it bites at its own value rather than near it.

    WHAT A TRUNCATED VIEW LOOKS LIKE, so a reader meeting the shape does not file it
    as a defect: the walk stops mid-input, so the LAST file in the list may carry a
    partial hunk or a hunk holding no lines at all, and files after it do not appear
    at all. `truncated` True is the client's signal that the list is a prefix.
    """
    diff_text = _generated_huge_single_file_diff(DIFF_VIEW_MAX_BODY_LINES * 2)

    view = parse_unified_diff_to_view(diff_text)

    assert view["truncated"] is True
    assert _total_parsed_body_lines(view) == DIFF_VIEW_MAX_BODY_LINES


def test_the_ceiling_boundary_holds_on_both_of_its_sides():
    """Exactly the ceiling parses in full; exactly two more is cut to the ceiling.

    Both halves live in one test because an off-by-one in the comparison moves the
    boundary by one line and leaves each half alone still satisfiable: a `>` instead
    of a `>=` still truncates the larger input, and a bound one line lower still
    parses a smaller one in full. Only the pair pins the value.
    """
    at_ceiling = parse_unified_diff_to_view(
        _generated_huge_single_file_diff(DIFF_VIEW_MAX_BODY_LINES)
    )
    above_ceiling = parse_unified_diff_to_view(
        _generated_huge_single_file_diff(DIFF_VIEW_MAX_BODY_LINES + 2)
    )

    assert at_ceiling["truncated"] is False
    assert _total_parsed_body_lines(at_ceiling) == DIFF_VIEW_MAX_BODY_LINES

    assert above_ceiling["truncated"] is True
    assert _total_parsed_body_lines(above_ceiling) == DIFF_VIEW_MAX_BODY_LINES


def test_many_small_files_are_bounded_by_the_same_total_counter():
    """Thousands of one-line files hit the ceiling on their SUM, not per file.

    This is the case a per-file ceiling would miss entirely, and it is a realistic
    `workspace.diff` shape rather than a contrived one. The last file present may hold
    an empty hunk — the walk stopped inside it — and the files generated after it are
    absent from the view.
    """
    diff_text = _generated_many_file_diff(TRUNCATING_MANY_FILE_COUNT)
    generated_body_lines = 2 * TRUNCATING_MANY_FILE_COUNT
    assert generated_body_lines > DIFF_VIEW_MAX_BODY_LINES

    view = parse_unified_diff_to_view(diff_text)

    assert view["truncated"] is True
    assert _total_parsed_body_lines(view) == DIFF_VIEW_MAX_BODY_LINES
    assert len(view["files"]) < TRUNCATING_MANY_FILE_COUNT


def test_the_acceptance_fixture_stays_below_the_ceiling_and_is_not_truncated():
    """The 10k-line fixture the feature is accepted against renders in FULL.

    A ceiling at or below `HUGE_DIFF_BODY_LINE_COUNT` would truncate the very fixture
    Acceptance names, satisfying every other assertion here while breaking the feature,
    so the relationship between the two constants is asserted directly and not merely
    implied by the parse.
    """
    assert HUGE_DIFF_BODY_LINE_COUNT < DIFF_VIEW_MAX_BODY_LINES

    view = parse_unified_diff_to_view(
        _generated_huge_single_file_diff(HUGE_DIFF_BODY_LINE_COUNT)
    )

    assert view["truncated"] is False
    assert _total_parsed_body_lines(view) == HUGE_DIFF_BODY_LINE_COUNT


def test_every_file_stats_still_recount_its_own_lines_under_truncation():
    """Truncation never leaves `stats` describing lines the payload does not carry.

    `test_every_file_stats_equal_a_recount_of_its_own_parsed_lines` asserts this for
    the untruncated corpus; a bound that cut the lines but kept the counters would be
    worse than no bound, because the sidebar would then promise content the viewer
    cannot show. Checked over the many-files shape so the file whose hunk the walk
    stopped inside — the partial or empty one — is covered too.
    """
    view = parse_unified_diff_to_view(
        _generated_many_file_diff(TRUNCATING_MANY_FILE_COUNT)
    )

    assert view["truncated"] is True
    for entry in view["files"]:
        kinds = [line["kind"] for hunk in entry["hunks"] for line in hunk["lines"]]
        assert entry["stats"]["added"] == kinds.count("add")
        assert entry["stats"]["deleted"] == kinds.count("del")
