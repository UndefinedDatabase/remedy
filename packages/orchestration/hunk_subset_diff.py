"""WHICH BYTES an approved selection applies: the subset diff of F033's hunk approval.

WHY this module exists: an operator approves some hunks of a diff and not others, and
something must turn that selection into the exact unified-diff text an applier is handed.
Folding that into the applier would fuse two questions that fail differently — "which hunks
did the operator choose?" and "do those hunks still fit the file?" — so the choice lives
here, as pure text in and pure text out, and the fit stays where the snapshots and the
rollback already are. ``build_approved_subset_diff`` returns an ``ApprovedSubsetDiff``
carrying one ``ApprovedSubsetFile`` per file that kept a hunk, or a ``SubsetRefusal`` naming
one code and every offending id.

NO HEADER ARITHMETIC HAPPENS HERE, and that is measured rather than hoped. The applier
positions every hunk by its OLD-side start, validates context against the ORIGINAL file and
keeps its own running offset for the result; it never reads a hunk header's NEW side at all,
so skewing ``+10,3`` to ``+999,3`` applies byte-identically. Dropping a hunk therefore needs
no renumbering whatsoever, a subset is a pure SELECTION rather than an arithmetic, and every
header is re-emitted VERBATIM. Inventing a renumbering here would be a defect.

DELIBERATE ABSENCE — this module APPLIES NOTHING. It opens no file, runs no subprocess,
touches no network, no logging and no global mutable state, and never learns whether the
subset would land cleanly; a conflict is the applier's answer, not this one's. DELIBERATE
ABSENCE — it also does NOT import the applier, structurally rather than incidentally: this
module decides WHICH bytes, ``apply_structured_patch`` decides whether they land, and
``tests/ui_server/test_command_channel.py`` already names the applier's module one the write
door may never reach, so the subset builder must not become the back door into it. A reader
who wants the apply mechanics wants ``apply_structured_patch``, in the
``packages/orchestration/`` module that test's ``FORBIDDEN_MODULES`` names; one who wants how
a diff becomes hunks wants ``packages/orchestration/diff_parser.py``; one who wants where a
hunk id COMES FROM wants ``packages/orchestration/hunk_identity.py``; one who wants whether a
selection is coherent at all wants ``packages/orchestration/hunk_approval.py``.

The one import of this package is ``parse_unified_diff_to_view``, and it is the POINT of the
module rather than an accident: the ids selected on are the ids that parser already computes
through ``hunk_identity``, so this repository still holds exactly ONE hunk identity —
DECISION F033 D3 — and no second one can drift away from it.

Every public name is TOTAL: it NEVER raises, on any input at all — a non-string diff,
``None``, a non-iterable id set, an id that is not a string. Same reason ``hunk_approval.py``
states: this runs behind an approval screen, and a builder that throws on a strange id takes
down the very screen that exists to show what is strange.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from packages.orchestration.diff_parser import (
    DIFF_LINE_ADDED,
    DIFF_LINE_CONTEXT,
    DIFF_LINE_DELETED,
    DIFF_STATUS_BINARY,
    parse_unified_diff_to_view,
)

# The refusal codes. Each gets its own module-level NAME so a caller matches on the name and
# never on a message. ``build_approved_subset_diff`` checks them in exactly the order declared
# here and returns the FIRST that trips; the order is contract and a test pins it with an
# input tripping two at once. WHY UNTRUSTWORTHY sits before ABSENT, the subtle one: a
# truncated view is missing hunks it never showed, so "this approved id is not in the diff" is
# UNKNOWABLE while the view is untrustworthy, and reporting absence first would blame the
# operator's selection for the parser's ceiling.

#: The approved set names no hunk at all. Landing nothing is not an all-or-nothing apply of
#: nothing, it is a caller mistake: ``decide_hunk_approval`` already refuses an empty decision,
#: and a full-rejection round reaches the repair loop rather than an applier.
SUBSET_REFUSAL_NO_APPROVED_IDS = "no_approved_ids"
#: The view cannot be re-emitted faithfully — it is truncated, or a file the selection touches
#: carries a ``note`` or a ``binary`` status, or a kept line carries a kind this module has no
#: prefix for. Re-emitting from such a view would silently produce a diff that is not the diff.
SUBSET_REFUSAL_UNTRUSTWORTHY_VIEW = "untrustworthy_view"
#: An approved id is not among the ids the view carries. A real integrity check rather than a
#: repeat of ``hunk_approval``'s ``unknown_hunk``: the diff can be re-parsed between the
#: decision and the apply, and an id that has since vanished must STOP the apply rather than
#: silently shrink it.
SUBSET_REFUSAL_ABSENT_HUNK = "absent_hunk"

#: The prefix each view line kind is re-emitted with. LOAD-BEARING, not cosmetic: swapping the
#: ``add`` and ``del`` entries changes what the emitted diff applies to, so a test pins it. A
#: kind absent from this map is an untrustworthy view, never a line to guess at.
_LINE_PREFIXES = {
    DIFF_LINE_CONTEXT: " ",
    DIFF_LINE_DELETED: "-",
    DIFF_LINE_ADDED: "+",
}


@dataclass(frozen=True)
class ApprovedSubsetFile:
    """The approved hunks of ONE file, as the text an applier takes for that file. ``diff`` is
    exactly what ``UnifiedDiff(path=..., diff=...)`` in
    ``packages/orchestration/structured_patch.py`` carries; ``hunk_ids`` are the ids emitted
    into it, in the diff's own order."""

    path: str
    diff: str
    hunk_ids: tuple[str, ...]


@dataclass(frozen=True)
class ApprovedSubsetDiff:
    """Every file that kept a hunk, in the diff's own file order. ``selected`` is every id
    emitted ACROSS all files, in the diff's own order, so a caller reporting "applied 5 of 8
    hunks" counts one tuple rather than summing the files."""

    files: tuple[ApprovedSubsetFile, ...]
    selected: tuple[str, ...]


@dataclass(frozen=True)
class SubsetRefusal:
    """Why no subset was built, and which ids are at fault. The same SHAPE as
    ``HunkApprovalRefusal`` on purpose, so a caller handles both alike, but a DISTINCT type:
    these codes are about the DIFF, those about the SELECTION, and one type carrying both sets
    would let a caller match a code that cannot reach it. ``hunk_ids`` is empty when no single
    id is at fault."""

    code: str
    message: str
    hunk_ids: tuple[str, ...]


def _total_text(value: object) -> str:
    """Coerce anything to text without ever raising — the totality guard everything below leans
    on. A broken ``__str__`` contributes ``repr()``, a broken ``repr()`` too the unoverridable
    ``object.__repr__``. Re-stated rather than imported from ``hunk_approval.py``, because that
    name is private there."""
    try:
        return str(value)
    except Exception:
        try:
            return repr(value)
        except Exception:
            return object.__repr__(value)


def _entries(value: Any) -> list[Any]:
    """The entries of an argument SUPPOSED to be an iterable, without raising. A ``str``, a
    bytes-like value and a ``Mapping`` each count as ONE entry, never an iterable of characters
    or keys: a caller passing a single id must get that one id back, not fragments reported as
    several strange ones. Anything not iterable at all is likewise one entry, so a wrong-typed
    call surfaces as a refusal NAMING what it saw."""
    if isinstance(value, (str, bytes, bytearray, Mapping)):
        return [value]
    try:
        return list(value)
    except Exception:
        return [value]


def _unique(ids: Iterable[str]) -> list[str]:
    """``ids`` with repeats removed, keeping FIRST-appearance order."""
    seen: set[str] = set()
    unique: list[str] = []
    for identifier in ids:
        if identifier not in seen:
            seen.add(identifier)
            unique.append(identifier)
    return unique


def _hunk_id(hunk: dict[str, Any]) -> str:
    """One hunk's id as text — the ONE identity, computed by ``hunk_identity`` upstream."""
    return _total_text(hunk.get("id"))


def _kept_hunks(file_entry: dict[str, Any], approved: set[str]) -> list[dict[str, Any]]:
    """This file's approved hunks, in the diff's own order. Membership is a SET test, so an id
    the caller listed twice keeps its hunk exactly once."""
    return [hunk for hunk in file_entry["hunks"] if _hunk_id(hunk) in approved]


def _untrustworthy_refusal(view: dict[str, Any], approved: set[str]) -> SubsetRefusal | None:
    """The ``SUBSET_REFUSAL_UNTRUSTWORTHY_VIEW`` refusal this view earns, or ``None``. All three
    untrustworthy shapes are decided HERE, in one place, so a caller reads one branch and a
    test disables one behaviour. The top-level ceiling names no id, because the ids it lost are
    exactly the ones it cannot report. The view is this package's own total parser's output, so
    its shape is a given here and only its CONTENT is in question."""
    if view["truncated"]:
        return SubsetRefusal(
            SUBSET_REFUSAL_UNTRUSTWORTHY_VIEW,
            "The diff was truncated before it was fully parsed, so which hunks it does not "
            "show is unknown and no subset of it can be trusted.",
            (),
        )
    tainted: list[str] = []
    unrenderable: list[str] = []
    for file_entry in view["files"]:
        kept = _kept_hunks(file_entry, approved)
        if not kept:
            # A file the selection does not touch cannot make the selection wrong.
            continue
        if file_entry["note"] is not None or file_entry["status"] == DIFF_STATUS_BINARY:
            tainted.extend(_hunk_id(hunk) for hunk in kept)
            continue
        for hunk in kept:
            if any(line["kind"] not in _LINE_PREFIXES for line in hunk["lines"]):
                unrenderable.append(_hunk_id(hunk))
    if tainted:
        return SubsetRefusal(
            SUBSET_REFUSAL_UNTRUSTWORTHY_VIEW,
            "These approved hunks are in a file the parser could not read faithfully: "
            + ", ".join(_unique(tainted)) + ".",
            tuple(_unique(tainted)),
        )
    if unrenderable:
        return SubsetRefusal(
            SUBSET_REFUSAL_UNTRUSTWORTHY_VIEW,
            "These approved hunks carry a line this module has no prefix for: "
            + ", ".join(_unique(unrenderable)) + ".",
            tuple(_unique(unrenderable)),
        )
    return None


def _emit(hunks: list[dict[str, Any]]) -> str:
    """The unified-diff text of ``hunks``: each header VERBATIM, then one line per view line as
    its kind's prefix followed by its content. No ``diff --git``, ``---`` or ``+++`` header is
    written — the applier takes the path from ``UnifiedDiff.path`` and reads only ``@@`` lines,
    so a header here would be noise it skips. Ends in exactly one newline."""
    out: list[str] = []
    for hunk in hunks:
        out.append(_total_text(hunk["header"]))
        for line in hunk["lines"]:
            out.append(_LINE_PREFIXES[line["kind"]] + _total_text(line["content"]))
    return "\n".join(out) + "\n"


# The one entry point: the diff of exactly the approved hunks, or a named refusal.
def build_approved_subset_diff(
    diff_text: str,
    approved_hunk_ids: Iterable[str],
) -> ApprovedSubsetDiff | SubsetRefusal:
    """Build the unified diff holding EXACTLY the approved hunks of ``diff_text``.

    Returns an ``ApprovedSubsetDiff`` — one ``ApprovedSubsetFile`` per file that kept a hunk, in
    the diff's own file order, a file with no kept hunk absent entirely — or the FIRST
    ``SubsetRefusal`` that trips, in the order the codes are declared above. Duplicate approved
    ids are harmless and never a refusal: asking for a hunk twice is the same request, and the
    hunk is emitted once. Never raises, on any input at all."""
    approved_ids = [_total_text(entry) for entry in _entries(approved_hunk_ids)]
    if not approved_ids:
        return SubsetRefusal(
            SUBSET_REFUSAL_NO_APPROVED_IDS,
            "The approved set names no hunk — there is no subset to build.",
            (),
        )

    # From here down the ids in play are plain ``str`` produced by ``_total_text``, and the
    # parser is itself total, so nothing below can raise: the guards sit at the BOUNDARY and the
    # rules need no catch-all that would swallow a real defect along with a hostile input.
    view = parse_unified_diff_to_view(_total_text(diff_text))
    approved = set(approved_ids)

    untrustworthy = _untrustworthy_refusal(view, approved)
    if untrustworthy is not None:
        return untrustworthy

    present = {_hunk_id(hunk) for entry in view["files"] for hunk in entry["hunks"]}
    absent = _unique([identifier for identifier in approved_ids if identifier not in present])
    if absent:
        return SubsetRefusal(
            SUBSET_REFUSAL_ABSENT_HUNK,
            "These approved hunks are not in this diff: " + ", ".join(absent) + ".",
            tuple(absent),
        )

    subset_files: list[ApprovedSubsetFile] = []
    selected: list[str] = []
    for file_entry in view["files"]:
        kept = _kept_hunks(file_entry, approved)
        if not kept:
            continue
        kept_ids = tuple(_hunk_id(hunk) for hunk in kept)
        subset_files.append(ApprovedSubsetFile(file_entry["path"], _emit(kept), kept_ids))
        selected.extend(kept_ids)
    return ApprovedSubsetDiff(tuple(subset_files), tuple(selected))
