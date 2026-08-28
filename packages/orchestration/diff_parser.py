"""Turn a unified diff into the versioned view JSON the F037 diff viewer renders.

WHY this module exists at all: this repository does not produce ONE diff shape, it
produces THREE, and a viewer that reads only one of them shows the operator a blank
panel for the other two. The three, named here because the next reader will search
for exactly these words:

* (a) ``difflib.unified_diff`` output carrying ``--- a/<path>`` and ``+++ b/<path>``
  headers and no ``diff --git`` line at all. ``pingpong_loop._compute_safe_diff``
  writes this into ``safe.diff``; ``job_evidence`` writes the same shape into
  ``workspace.diff`` (there with ``lineterm=""`` and every line ``rstrip``-ed, so a
  blank context line arrives as the empty string rather than as a single space).
* (b) real ``git diff`` hunks, complete with ``diff --git``, ``index``,
  ``similarity index`` and ``rename from``/``rename to`` lines.
  ``repair_attest.build_safe_diff_text`` concatenates these as the tracked half of
  ``safe.diff``.
* (c) that same function's untracked-file markers: ``--- /dev/null`` followed by
  ``+++ b/<path>`` followed by a ``#`` comment holding the new file's hash and
  size, with no hunk body whatsoever.

DELIBERATE ABSENCE — this module does NOT reuse the file-status vocabulary of
``packages/orchestration/review_subject.py`` and does not import it. That module
maps the seven ``git diff --name-status`` letters (``added``, ``modified``,
``deleted``, ``renamed``, ``copied``, ``type_changed``, ``dirty``) and has no
concept of ``binary``, because git reports a binary file with the same letter as a
text file: binary-ness is a property of the diff BODY, not of the name-status
letter. Widening that vocabulary would move guards this repository already
enforces over it. The reasoning, the alternatives and the reversal instructions
are amendment A1 of ``docs/roadmap/features/T5_F037.md`` (DECISION F037 D1).
Amendment A3 of the same file rules why this is a NEW module rather than an
extension of ``packages/orchestration/review_scope.py``, whose hunk regex captures
no old-side line numbers.

CONTRACT NOTES a reader will otherwise have to guess at:

* The feature file's contract writes a file's counters as ``stats {+,-}``. This
  module reads that shorthand as the two named integer keys ``stats["added"]`` and
  ``stats["deleted"]``.
* ``truncated`` (top level) and ``note`` (per file) are ADDITIONS to the contract as
  the feature file states it. They are exactly what ``DIFF_VIEW_VERSION`` exists to
  carry: the version field is authoritative over the prose contract, and a consumer
  pinning version 1 gets these two keys.
* Hunk ``id`` values are PROVISIONAL — ``"<file_index>:<hunk_index>"``, both
  zero-based, stable only within a single parse of a single diff text. F033
  replaces them with content-hash ids, and ``DIFF_VIEW_VERSION`` is the seam
  through which it does so.

The parser is PURE and TOTAL: text in, plain data out. No file system, no
subprocess, no network, no logging, no global mutable state, and it NEVER raises on
malformed input. A region it cannot read is reported in the data it returns — as a
``note``, or as a file with an empty hunk list — because this feeds a VIEWER, and a
viewer that crashes on a strange diff is worse than one that says it could not read
the region.
"""

from __future__ import annotations

import re
from typing import Any

#: Bumped whenever the returned shape changes; F033's content-hash hunk ids are the
#: first planned bump, and consumers gate on this rather than on key sniffing.
DIFF_VIEW_VERSION = 1

#: The five viewer statuses. F037's own vocabulary — see the deliberate-absence note
#: in the module docstring and amendment A1 of docs/roadmap/features/T5_F037.md.
DIFF_STATUS_ADDED = "added"
DIFF_STATUS_MODIFIED = "modified"
DIFF_STATUS_DELETED = "deleted"
DIFF_STATUS_RENAMED = "renamed"
DIFF_STATUS_BINARY = "binary"

#: Exactly the five values above; the client renders nothing outside this set.
DIFF_VIEW_STATUSES = frozenset(
    {
        DIFF_STATUS_ADDED,
        DIFF_STATUS_MODIFIED,
        DIFF_STATUS_DELETED,
        DIFF_STATUS_RENAMED,
        DIFF_STATUS_BINARY,
    }
)

#: Line kinds inside a hunk body.
DIFF_LINE_CONTEXT = "ctx"
DIFF_LINE_ADDED = "add"
DIFF_LINE_DELETED = "del"

#: Sentinels this repository really emits, quoted from their producers so a grep for
#: the literal lands both on the emitter and on the reader.
#: pingpong_loop._compute_safe_diff writes these three.
DIFF_BINARY_SENTINEL = "[binary file]"
DIFF_TRUNCATED_SENTINEL = "[DIFF TRUNCATED]"
DIFF_UNSAFE_ARTIFACT_PREFIX = "[unsafe staged artifact skipped:"

_NO_NEWLINE_PREFIX = "\\ No newline"
_DEV_NULL = "/dev/null"

_HUNK_HEADER_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")
_GIT_HEADER_RE = re.compile(r"^diff --git a/(.+) b/(.+)$")


def _strip_side_prefix(raw_path: str) -> str:
    """Drop ONE leading ``a/`` or ``b/`` from a diff header path.

    Follows ``repair_attest.parse_safe_diff_paths``, which already reads
    ``+++ b/<path>`` headers this way, so the repository keeps one spelling of the
    concept rather than two that drift.
    """
    path = raw_path.strip()
    if path.startswith("a/") or path.startswith("b/"):
        return path[2:]
    return path


class _FileRegion:
    """Mutable accumulator for one file's region; converted to plain data on flush."""

    __slots__ = (
        "git_path",
        "minus_header",
        "plus_header",
        "rename_from",
        "rename_to",
        "binary",
        "note",
        "hunks",
        "hunks_refused",
    )

    def __init__(self, git_path: str | None = None) -> None:
        self.git_path: str | None = git_path
        self.minus_header: str | None = None
        self.plus_header: str | None = None
        self.rename_from: str | None = None
        self.rename_to: str | None = None
        self.binary: bool = False
        self.note: str | None = None
        self.hunks: list[dict[str, Any]] = []
        self.hunks_refused: bool = False

    def set_note(self, text: str, force: bool = False) -> None:
        """Record the FIRST unreadable-region marker, or overwrite when forced.

        First-come rather than last-wins so that the marker nearest the file's own
        header — which is where every producer in this repository puts it — is the
        one the viewer shows.
        """
        if force or self.note is None:
            self.note = text

    def resolve_path(self) -> tuple[str, str | None]:
        """Return ``(path, old_path)``; ``old_path`` is non-None only for a rename."""
        if self.rename_to is not None or self.rename_from is not None:
            path = self.rename_to
            if path is None:
                path = _header_path(self.plus_header) or self.git_path or ""
            return path, self.rename_from
        path = _header_path(self.plus_header)
        if path is None or path == _DEV_NULL:
            # A deleted file's `+++` side is /dev/null, so the real name is on the
            # `---` side. Same fallback repair_attest.parse_safe_diff_paths relies on.
            path = _header_path(self.minus_header)
        if path is None or path == _DEV_NULL:
            path = self.git_path
        return (path or ""), None

    def derive_status(self) -> str:
        """First match wins, in the order amendment A1's five-value vocabulary implies."""
        if self.rename_from is not None and self.rename_to is not None:
            return DIFF_STATUS_RENAMED
        if self.binary:
            return DIFF_STATUS_BINARY
        minus_is_null = _header_path(self.minus_header) == _DEV_NULL
        plus_is_null = _header_path(self.plus_header) == _DEV_NULL
        if minus_is_null or (self.hunks and all(h["_old_count"] == 0 for h in self.hunks)):
            return DIFF_STATUS_ADDED
        if plus_is_null or (self.hunks and all(h["_new_count"] == 0 for h in self.hunks)):
            return DIFF_STATUS_DELETED
        # No hunks and no other signal: a readable file entry with nothing to show,
        # never an error.
        return DIFF_STATUS_MODIFIED


def _header_path(header: str | None) -> str | None:
    """Return a ``---``/``+++`` header's path, ``/dev/null`` preserved as itself."""
    if header is None:
        return None
    raw = header.strip()
    # difflib appends a tab-separated timestamp field to its headers when given one.
    raw = raw.split("\t", 1)[0].strip()
    if raw == _DEV_NULL:
        return _DEV_NULL
    return _strip_side_prefix(raw)


def parse_unified_diff_to_view(diff_text: str) -> dict:
    """Parse ``diff_text`` into the F037 diff-view JSON.

    Returns ``{"version": DIFF_VIEW_VERSION, "truncated": bool, "files": [...]}``.
    A file is ``{"path", "old_path", "status", "stats": {"added", "deleted"},
    "note", "hunks"}``; a hunk is ``{"id", "header", "old_start", "new_start",
    "lines"}``; a line is ``{"kind", "old_ln", "new_ln", "content"}``.

    Never raises. Empty text, and text that is not a diff at all, both return the
    empty-files shape.
    """
    files: list[dict[str, Any]] = []
    regions: list[_FileRegion] = []
    truncated = False

    current: _FileRegion | None = None
    hunk: dict[str, Any] | None = None
    old_ln = 0
    new_ln = 0
    old_left = 0
    new_left = 0

    def close_hunk() -> None:
        nonlocal hunk, old_left, new_left
        hunk = None
        old_left = 0
        new_left = 0

    def open_region(git_path: str | None = None) -> _FileRegion:
        nonlocal current
        close_hunk()
        current = _FileRegion(git_path)
        regions.append(current)
        return current

    if not isinstance(diff_text, str):
        # Total by contract: a non-string is an unreadable region, not an exception.
        return {"version": DIFF_VIEW_VERSION, "truncated": False, "files": []}

    for line in diff_text.split("\n"):
        stripped = line.strip()

        # --- sentinels first ------------------------------------------------
        # None of these can be a hunk body line (a body line starts with " ", "+",
        # "-", "\\", or is the empty string), so testing them ahead of the body
        # keeps them unambiguous.
        if stripped == DIFF_TRUNCATED_SENTINEL:
            truncated = True
            close_hunk()
            current = None
            continue
        if stripped == DIFF_BINARY_SENTINEL:
            if current is None:
                current = open_region()
            close_hunk()
            current.binary = True
            current.set_note(DIFF_BINARY_SENTINEL, force=True)
            continue
        if stripped.startswith(DIFF_UNSAFE_ARTIFACT_PREFIX):
            if current is None:
                current = open_region()
            close_hunk()
            current.set_note(line, force=True)
            current.hunks = []
            current.hunks_refused = True
            continue

        # --- hunk body ------------------------------------------------------
        if hunk is not None and (old_left > 0 or new_left > 0):
            if line.startswith(_NO_NEWLINE_PREFIX):
                # Metadata about the previous line. Belongs to no entry, advances
                # no counter, and is dropped.
                continue
            # Classify first, then advance in ONE place per side. Two copies of
            # "advance the old counter" is how a viewer ends up numbering the old
            # side correctly in context lines and wrongly in deletions.
            kind: str | None = None
            if (line.startswith(" ") or line == "") and old_left > 0 and new_left > 0:
                kind = DIFF_LINE_CONTEXT
            elif line.startswith("+") and new_left > 0:
                kind = DIFF_LINE_ADDED
            elif line.startswith("-") and old_left > 0:
                kind = DIFF_LINE_DELETED
            if kind is not None:
                on_old = kind in (DIFF_LINE_CONTEXT, DIFF_LINE_DELETED)
                on_new = kind in (DIFF_LINE_CONTEXT, DIFF_LINE_ADDED)
                hunk["lines"].append(
                    {
                        "kind": kind,
                        "old_ln": old_ln if on_old else None,
                        "new_ln": new_ln if on_new else None,
                        # The leading marker character is dropped; a `rstrip`-ed blank
                        # context line arrives as "" and has no marker to drop.
                        "content": line[1:] if line else "",
                    }
                )
                if on_old:
                    old_ln += 1
                    old_left -= 1
                if on_new:
                    new_ln += 1
                    new_left -= 1
                continue
            # Anything else ends the hunk early and is re-read as structure below.
            close_hunk()
        elif hunk is not None:
            close_hunk()

        # --- structure ------------------------------------------------------
        git_match = _GIT_HEADER_RE.match(line)
        if git_match is not None:
            current = open_region(git_match.group(2).strip())
            continue

        if line.startswith("--- "):
            # S4: a `--- ` line outside a hunk body starts a new file, UNLESS it is
            # the header pair of the `diff --git` region just opened.
            if current is None or current.minus_header is not None or current.hunks:
                current = open_region()
            current.minus_header = line[4:]
            continue

        if line.startswith("+++ "):
            if current is None:
                current = open_region()
            current.plus_header = line[4:]
            continue

        if line.startswith("rename from "):
            if current is None:
                current = open_region()
            current.rename_from = line[len("rename from "):].strip()
            continue

        if line.startswith("rename to "):
            if current is None:
                current = open_region()
            current.rename_to = line[len("rename to "):].strip()
            continue

        if line.startswith("Binary files ") or line.startswith("GIT binary patch"):
            if current is None:
                current = open_region()
            current.binary = True
            current.set_note(stripped)
            continue

        if line.startswith("@@"):
            match = _HUNK_HEADER_RE.match(line)
            if match is None:
                # Not a hunk header. Record it rather than guess at it.
                if current is not None:
                    current.set_note(stripped)
                continue
            if current is None:
                current = open_region()
            if current.hunks_refused:
                continue
            old_start = int(match.group(1))
            old_count = 1 if match.group(2) is None else int(match.group(2))
            new_start = int(match.group(3))
            new_count = 1 if match.group(4) is None else int(match.group(4))
            hunk = {
                "id": "",  # assigned on flush, when the file index is known
                "header": line,  # VERBATIM, section heading included; the viewer renders it
                "old_start": old_start,
                "new_start": new_start,
                "lines": [],
                "_old_count": old_count,
                "_new_count": new_count,
            }
            current.hunks.append(hunk)
            old_ln = old_start
            new_ln = new_start
            old_left = old_count
            new_left = new_count
            continue

        if line.startswith("#"):
            # job_evidence's workspace preamble and repair_attest's untracked-file
            # marker both emit these. Outside a file they are prose; inside one they
            # are the only explanation of an empty region.
            if current is not None:
                current.set_note(stripped)
            continue

        # Everything else outside a hunk (`index `, `new file mode `, `similarity
        # index `, ordinary prose) carries nothing the viewer renders.

    for file_index, region in enumerate(regions):
        path, old_path = region.resolve_path()
        status = region.derive_status()
        hunks_out: list[dict[str, Any]] = []
        added = 0
        deleted = 0
        for hunk_index, raw in enumerate(region.hunks):
            for entry in raw["lines"]:
                # Counted from the PARSED entries, never from a second walk of the
                # text, so stats can never disagree with the rendered lines.
                if entry["kind"] == DIFF_LINE_ADDED:
                    added += 1
                elif entry["kind"] == DIFF_LINE_DELETED:
                    deleted += 1
            hunks_out.append(
                {
                    "id": f"{file_index}:{hunk_index}",
                    "header": raw["header"],
                    "old_start": raw["old_start"],
                    "new_start": raw["new_start"],
                    "lines": raw["lines"],
                }
            )
        files.append(
            {
                "path": path,
                "old_path": old_path if status == DIFF_STATUS_RENAMED else None,
                "status": status,
                "stats": {"added": added, "deleted": deleted},
                "note": region.note,
                "hunks": hunks_out,
            }
        )

    return {"version": DIFF_VIEW_VERSION, "truncated": truncated, "files": files}
