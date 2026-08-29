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
* ``intraline`` joined the per-line shape while version 1 was still PRIVATE — nothing
  outside this repository could observe it — so it completed v1 rather than changing a
  shipped shape. Version 1 stopped being private when F256 landed the diff endpoint:
  ``packages/orchestration/ui_server.py`` builds the envelope through
  ``packages/orchestration/diff_view_source.py``'s ``build_diff_view``, which carries
  ``DIFF_VIEW_VERSION`` straight out to a consumer. Version 1 WAS served. That is why
  F033's id change took a real bump to 2 rather than riding in unversioned, and any
  later shape change must take one too — the private-shape argument is spent.
* Hunk ``id`` values are CONTENT-DERIVED and carry no position at all. The identity is
  computed by ``hunk_identity`` in ``packages/orchestration/hunk_identity.py`` over the
  file's resolved ``path``, the hunk's normalised OLD side — its ``ctx`` and ``del``
  lines in order, never its ``add`` lines — and the hunk's occurrence rank among
  byte-identical old sides within the SAME file. An id is ``HUNK_ID_LENGTH`` lowercase
  hex characters. THE STABILITY PROPERTY a reader may rely on: a hunk keeps its id when
  anything else in its file moves — another hunk gains, loses or rewrites lines, or
  hunks appear before it — and when its OWN added lines change, because a second
  proposed fix for the same original text is the same hunk. It changes only when the
  path changes or when the hunk's own old side does. This shape arrived with
  ``DIFF_VIEW_VERSION`` 2.

The parser is PURE and TOTAL: text in, plain data out. No file system, no
subprocess, no network, no logging, no global mutable state, and it NEVER raises on
malformed input. A region it cannot read is reported in the data it returns — as a
``note``, or as a file with an empty hunk list — because this feeds a VIEWER, and a
viewer that crashes on a strange diff is worse than one that says it could not read
the region.
"""

from __future__ import annotations

import difflib
import re
from typing import Any

from packages.orchestration.hunk_identity import hunk_identity, normalise_old_side

#: Bumped whenever the returned shape changes; consumers gate on this rather than on key
#: sniffing. Version 2 IS F033's bump, and it happened: a hunk's ``id`` is now derived
#: from that hunk's own content by ``packages/orchestration/hunk_identity.py`` instead of
#: from its position in the diff. No other key of the view moved with it.
DIFF_VIEW_VERSION = 2

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

#: A paired deletion/addition whose SIGNIFICANT-token
#: ``difflib.SequenceMatcher.ratio()`` is STRICTLY BELOW this gets no intraline spans
#: at all: two lines with almost nothing in common are a whole-line replacement, and
#: marking every character of both is the same as marking none. Exported so a test can
#: name the threshold rather than transcribe it. Which token stream the ratio is taken
#: over is the whole of finding ``R-0718`` — see ``_intraline_pair_is_similar``.
DIFF_INTRALINE_MIN_RATIO = 0.3

#: Ceiling on the hunk BODY LINES ``parse_unified_diff_to_view`` appends across the
#: WHOLE diff; above it the walk stops and ``truncated`` is set. DECISION F037 D5 fixes
#: the value at twice the 10,000-line fixture the Acceptance of
#: ``docs/roadmap/features/T5_F037.md`` names, so that fixture still renders in full.
#: DELIBERATE ABSENCE — Remedy does NOT bound the artifact READ here, because this
#: module touches no filesystem at all; that bound belongs to
#: ``packages/orchestration/diff_view_source.py``, which is where the file is read.
DIFF_VIEW_MAX_BODY_LINES = 20_000

#: Ceiling on the FILE ENTRIES ``parse_unified_diff_to_view`` carries; above it the file
#: list is cut to this length and ``truncated`` is set. DECISION F037 D6 fixes the value
#: at five times the 400-file corpus shape ``MANY_FILE_DIFF_FILE_COUNT`` names in
#: ``tests/orchestration/test_diff_parser.py``, so that fixture still renders in full.
#: WHY a SECOND ceiling exists (finding ``R-0722``): ``DIFF_VIEW_MAX_BODY_LINES`` counts
#: BODY LINES, and a file can carry none — a mode change, a binary marker, a pure rename
#: each add a file entry and append nothing to that counter — so a diff made only of such
#: files reached no bound at all however large it grew.
#: DELIBERATE ABSENCE — these two ceilings bound the OUTPUT this module BUILDS, and
#: neither bounds what is READ. The INPUT is bounded separately, by
#: ``DIFF_VIEW_MAX_ARTIFACT_BYTES`` in ``packages/orchestration/diff_view_source.py`` under
#: DECISION F037 D7, which is where the file is read. Neither bound subsumes the other:
#: these two count file entries and body lines, that one counts bytes, and they are
#: different resources in different units.
DIFF_VIEW_MAX_FILES = 2_000

_NO_NEWLINE_PREFIX = "\\ No newline"
_DEV_NULL = "/dev/null"

#: Word-or-single-other-character tokens for the intraline diff. It keeps the
#: SEPARATORS, so every character of the input lands in exactly one token and the
#: concatenation of the tokens is the original string again — that identity is what
#: makes a token index convertible into a character offset without drift.
_INTRALINE_TOKEN_RE = re.compile(r"\w+|\W")

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


def _region_is_redundant_header_echo(earlier: _FileRegion, later: _FileRegion) -> bool:
    """True when ``earlier`` is nothing but a repeat of ``later``'s header pair.

    Every condition is on the EARLIER region: it carries no hunks, no ``note``, no
    binary flag and no rename, both of its own headers are present, and its
    ``(minus_header, plus_header)`` pair equals the later region's pair.

    The comparison is on the HEADER PAIR and NEVER on the resolved path.
    ``repair_attest.build_safe_diff_text`` legitimately puts a tracked region and an
    untracked ``--- /dev/null`` marker for ONE path into ``safe.diff``, and those are
    two distinct facts a viewer must keep apart. A region carrying a ``note`` is
    never dropped either, because the note is the only explanation an empty region
    has.
    """
    if earlier.hunks or earlier.note is not None or earlier.binary:
        return False
    if earlier.rename_from is not None or earlier.rename_to is not None:
        return False
    if earlier.minus_header is None or earlier.plus_header is None:
        return False
    return (earlier.minus_header, earlier.plus_header) == (
        later.minus_header,
        later.plus_header,
    )


def _collapse_doubled_header_regions(regions: list[_FileRegion]) -> list[_FileRegion]:
    """Fold each redundant header-echo region into the region that FOLLOWS it.

    WHY this exists (finding ``R-0716``): ``job_evidence._build_workspace_diff``
    appends ``--- a/<rel>`` and ``+++ b/<rel>`` itself and then appends
    ``difflib.unified_diff(..., fromfile="a/<rel>", tofile="b/<rel>")``, whose own
    first two lines are that same pair. Every file in ``workspace.diff`` therefore
    carries the header pair TWICE, and the ``--- `` rule in the walk opens a second,
    empty region on the repeat — one file rendered as two, the first with no hunks
    and zero stats.

    Done at flush time rather than as a lookahead in the walk, so the walk keeps its
    one-line-at-a-time shape. Walking backwards makes the fold IDEMPOTENT over runs:
    three repeats of a header pair collapse as cleanly as two, because each dropped
    region is compared against the region that SURVIVED to its right. File order is
    preserved; nothing is reordered and nothing is merged.
    """
    kept: list[_FileRegion] = []
    for region in reversed(regions):
        if kept and _region_is_redundant_header_echo(region, kept[0]):
            continue
        kept.insert(0, region)
    return kept


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


def _intraline_token_offsets(tokens: list[str]) -> list[int]:
    """Character offset at which each token starts, with the total length appended.

    Length ``len(tokens) + 1`` so a half-open token range ``[i1, i2)`` converts to the
    character span ``(offsets[i1], offsets[i2] - offsets[i1])`` with no special case
    for the last token.
    """
    offsets = [0]
    position = 0
    for token in tokens:
        position += len(token)
        offsets.append(position)
    return offsets


def _normalise_intraline_spans(
    raw_spans: list[tuple[int, int]], content_length: int
) -> list[list[int]]:
    """Clamp, drop empties, merge touching or overlapping spans, sort by ``start``.

    Every returned span satisfies ``0 <= start`` and ``start + length <=
    content_length``; a span that indexes past its own content is exactly the defect
    this normalisation exists to make impossible.
    """
    bounds: list[tuple[int, int]] = []
    for start, length in raw_spans:
        low = max(0, start)
        high = min(content_length, start + length)
        if high > low:
            bounds.append((low, high))
    bounds.sort()
    merged: list[list[int]] = []
    for low, high in bounds:
        if merged and low <= merged[-1][1]:
            if high > merged[-1][1]:
                merged[-1][1] = high
        else:
            merged.append([low, high])
    return [[low, high - low] for low, high in merged]


def _significant_intraline_tokens(tokens: list[str]) -> list[str]:
    """The tokens of one line that carry WORD evidence: everything not pure whitespace.

    ``_INTRALINE_TOKEN_RE`` deliberately keeps the separators, because the offset
    arithmetic needs every character in exactly one token. A separator says nothing
    about whether two lines are the same sentence, so the similarity DECISION reads
    this reduced stream while the span mapping keeps reading the full one.
    """
    return [token for token in tokens if token.strip() != ""]


def _intraline_pair_is_similar(old_tokens: list[str], new_tokens: list[str]) -> bool:
    """True when a changed-line pair is close enough to mark word-by-word.

    WHY the ratio is taken over the SIGNIFICANT tokens rather than over the stream the
    spans are mapped from (finding ``R-0718``): two space-separated lines with the same
    word count always match on their separator tokens, which puts a FLOOR under the
    full-stream ratio even when the lines share no word at all — 0.333 at two words,
    0.400 at three, 0.444 at five, 0.474 at ten, rising toward 0.5. Measured against
    ``DIFF_INTRALINE_MIN_RATIO`` that floor made the guard UNREACHABLE for every
    multi-word line, so the only shape it could ever refuse was a single-word one, and
    ``alpha beta gamma`` against ``zzz qqq www`` had every word of both sides marked —
    exactly the all-marked noise the guard exists to prevent.

    Two lines carrying no significant token at all give no word evidence either way.
    That pair is treated as SIMILAR and gets spans from the full stream, because
    marking is the recoverable half of a choice this rule cannot make honestly.
    """
    old_significant = _significant_intraline_tokens(old_tokens)
    new_significant = _significant_intraline_tokens(new_tokens)
    if not old_significant and not new_significant:
        return True
    ratio = difflib.SequenceMatcher(a=old_significant, b=new_significant).ratio()
    return ratio >= DIFF_INTRALINE_MIN_RATIO


def _intraline_spans_for_pair(
    old_content: str, new_content: str
) -> tuple[list[list[int]], list[list[int]]]:
    """Return ``(old_spans, new_spans)`` marking what differs INSIDE one changed line.

    ``replace`` and ``delete`` opcodes mark the OLD side, ``replace`` and ``insert``
    mark the NEW side, and ``equal`` marks neither. A pair ``_intraline_pair_is_similar``
    rejects comes back empty on both sides — see that function and
    ``DIFF_INTRALINE_MIN_RATIO``.
    """
    old_tokens = _INTRALINE_TOKEN_RE.findall(old_content)
    new_tokens = _INTRALINE_TOKEN_RE.findall(new_content)
    if "".join(old_tokens) != old_content or "".join(new_tokens) != new_content:
        # The offset arithmetic below is sound only while the tokens rejoin to the
        # original string. They always do for this regex; refusing rather than
        # guessing keeps the parser total if that ever stops being true.
        return [], []

    if not _intraline_pair_is_similar(old_tokens, new_tokens):
        return [], []

    # The MAPPING runs over the FULL token stream: offsets must stay exact.
    matcher = difflib.SequenceMatcher(a=old_tokens, b=new_tokens)
    old_offsets = _intraline_token_offsets(old_tokens)
    new_offsets = _intraline_token_offsets(new_tokens)
    old_raw: list[tuple[int, int]] = []
    new_raw: list[tuple[int, int]] = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag in ("replace", "delete"):
            old_raw.append((old_offsets[i1], old_offsets[i2] - old_offsets[i1]))
        if tag in ("replace", "insert"):
            new_raw.append((new_offsets[j1], new_offsets[j2] - new_offsets[j1]))
    return (
        _normalise_intraline_spans(old_raw, len(old_content)),
        _normalise_intraline_spans(new_raw, len(new_content)),
    )


def _apply_intraline_spans(lines: list[dict[str, Any]]) -> None:
    """Give every line of ONE hunk its ``intraline`` key, in place.

    The key is set to ``[]`` on every entry FIRST, so a client never has to test for
    its presence: a ``ctx`` line, an unpaired line and a pair below the ratio
    threshold all carry an empty list rather than nothing.

    PAIRING: each maximal run of consecutive ``del`` entries IMMEDIATELY followed by a
    maximal run of consecutive ``add`` entries is one replacement block, and within it
    the i-th deletion is paired with the i-th addition. The surplus entries of the
    longer run keep ``[]`` — there is no line to compare them against, and inventing
    one is how an intraline highlighter starts marking unrelated text.
    """
    for entry in lines:
        entry["intraline"] = []

    index = 0
    total = len(lines)
    while index < total:
        if lines[index]["kind"] != DIFF_LINE_DELETED:
            index += 1
            continue
        del_start = index
        while index < total and lines[index]["kind"] == DIFF_LINE_DELETED:
            index += 1
        add_start = index
        while index < total and lines[index]["kind"] == DIFF_LINE_ADDED:
            index += 1
        paired = min(add_start - del_start, index - add_start)
        for offset in range(paired):
            old_entry = lines[del_start + offset]
            new_entry = lines[add_start + offset]
            old_spans, new_spans = _intraline_spans_for_pair(
                old_entry["content"], new_entry["content"]
            )
            old_entry["intraline"] = old_spans
            new_entry["intraline"] = new_spans


def parse_unified_diff_to_view(diff_text: str) -> dict:
    """Parse ``diff_text`` into the F037 diff-view JSON.

    Returns ``{"version": DIFF_VIEW_VERSION, "truncated": bool, "files": [...]}``.
    A file is ``{"path", "old_path", "status", "stats": {"added", "deleted"},
    "note", "hunks"}``; a hunk is ``{"id", "header", "old_start", "new_start",
    "lines"}``; a line is ``{"kind", "old_ln", "new_ln", "content", "intraline"}``,
    where ``intraline`` is a possibly empty list of ``[start, length]`` character
    spans into that line's OWN ``content``. Two ceilings bound what is returned —
    ``DIFF_VIEW_MAX_BODY_LINES`` on the body lines appended across the whole diff and
    ``DIFF_VIEW_MAX_FILES`` on the file entries — and ``truncated`` is True whenever
    either of them bites.

    Never raises. Empty text, and text that is not a diff at all, both return the
    empty-files shape.
    """
    files: list[dict[str, Any]] = []
    regions: list[_FileRegion] = []
    truncated = False
    # Counted across the WHOLE diff, not per file or per hunk: the payload is the sum,
    # and a per-file ceiling would leave a diff of many small files unbounded.
    body_lines_appended = 0

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
                # WHY the walk may stop here: ``truncated`` is the contract's OWN
                # top-level field, so reaching ``DIFF_VIEW_MAX_BODY_LINES`` is a
                # deliberate stop that is REPORTED in the data, never an error raised.
                # The boundary is inclusive: exactly the ceiling parses in full. Above
                # it the LAST file in the view may carry a partial hunk or a hunk
                # holding no lines at all, and files after it do not appear.
                if body_lines_appended >= DIFF_VIEW_MAX_BODY_LINES:
                    truncated = True
                    break
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
                body_lines_appended += 1
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
                "id": "",  # assigned on flush, from this hunk's own old side
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

    # R-0716: fold the `workspace.diff` header echo away BEFORE regions become files, so
    # the view carries one entry per real file rather than a phantom beside each of them.
    regions = _collapse_doubled_header_regions(regions)

    # WHY the file ceiling is applied HERE, after the collapse rather than during the
    # walk: `workspace.diff` carries every file's header pair TWICE (finding `R-0716`),
    # so a count taken during the walk would bound that shape at half the files a reader
    # sees. The collapsed list is the list that becomes `files`, so it is the list the
    # ceiling belongs to. WHY the comparison is `>` and not `>=`: exactly the ceiling
    # parses in full and is NOT marked truncated, which is the same inclusive boundary
    # `DIFF_VIEW_MAX_BODY_LINES` already has.
    if len(regions) > DIFF_VIEW_MAX_FILES:
        truncated = True
        regions = regions[:DIFF_VIEW_MAX_FILES]

    for region in regions:
        path, old_path = region.resolve_path()
        status = region.derive_status()
        hunks_out: list[dict[str, Any]] = []
        added = 0
        deleted = 0
        # The occurrence rank `hunk_identity` takes, counted PER FILE and reset with it:
        # two hunks of one file whose normalised old sides are byte-identical would
        # otherwise share a name. Keyed on that normalised text rather than on the
        # finished id, so the rank is a property of the content and not of the digest.
        old_side_ranks: dict[str, int] = {}
        for raw in region.hunks:
            # Intraline pairing is a WITHIN-HUNK relation, so it runs here, once per
            # hunk, rather than during the walk where a run is not yet complete.
            _apply_intraline_spans(raw["lines"])
            # The hunk's OLD side, in order — exactly the membership the walk calls
            # `on_old`. Added lines are EXCLUDED so that re-proposing a different fix
            # for the same original text keeps the hunk's id, which is the stability
            # property the module docstring's contract note promises.
            old_side_lines: list[str] = []
            for entry in raw["lines"]:
                # Counted from the PARSED entries, never from a second walk of the
                # text, so stats can never disagree with the rendered lines.
                if entry["kind"] == DIFF_LINE_ADDED:
                    added += 1
                elif entry["kind"] == DIFF_LINE_DELETED:
                    deleted += 1
                if entry["kind"] in (DIFF_LINE_CONTEXT, DIFF_LINE_DELETED):
                    old_side_lines.append(entry["content"])
            normalised_old_side = normalise_old_side(old_side_lines)
            occurrence = old_side_ranks.get(normalised_old_side, 0)
            old_side_ranks[normalised_old_side] = occurrence + 1
            hunks_out.append(
                {
                    "id": hunk_identity(path, old_side_lines, occurrence),
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
