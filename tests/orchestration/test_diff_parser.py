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

from packages.orchestration.diff_parser import (
    DIFF_STATUS_ADDED,
    DIFF_STATUS_BINARY,
    DIFF_STATUS_DELETED,
    DIFF_STATUS_MODIFIED,
    DIFF_STATUS_RENAMED,
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
