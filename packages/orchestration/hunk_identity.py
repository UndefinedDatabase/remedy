"""The ONE stable, content-derived hunk identity F033's hunk-level approval turns on.

WHY this module exists: approving a hunk is a promise about a piece of CONTENT, and
``packages/orchestration/diff_parser.py`` currently names hunks
``"<file_index>:<hunk_index>"`` — both zero-based, both POSITIONAL. Those ids are stable
only within a single parse of a single diff text: insert one hunk near the top of a file
and every hunk after it is renumbered, so an operator who approved hunk ``0:3`` in one
round would be approving a different piece of content in the next. An id computed from
the hunk's own old-side text does not move when something else in the file moves.

This IS the module ``diff_parser.py``'s docstring points at when it says its hunk ``id``
values are PROVISIONAL, that "F033 replaces them with content-hash ids", and that
``DIFF_VIEW_VERSION`` is the seam through which it does so. The parser is not wired to
this module yet — that wiring and the version bump are their own change — and the
identity is proved alone here first. The diff-repair side will share this same function
rather than keep a local hunk helper, so that "the same hunk" means one thing repo-wide.

DELIBERATE ABSENCE — this module does NOT parse diffs and does not know what a diff is.
There is no hunk header regex here, no ``@@`` handling, no file-status vocabulary and no
notion of an added or deleted line. It takes the lines a caller has ALREADY identified as
one hunk's old side, and a path, and returns a name for them. A reader who arrives here
searching for diff parsing wants ``packages/orchestration/diff_parser.py``; a reader who
wants the repair-side hunk handling wants ``packages/orchestration/diff_repair.py``.

Both functions are PURE and TOTAL, in the same sense the parser's docstring uses those
words: no file system, no subprocess, no network, no logging, no global mutable state,
standard library only, and they NEVER raise — on any input at all. Totality is not
politeness here. These ids are computed while rendering a viewer and while attributing an
operator's approval, and a naming function that throws on a strange line would take down
the very screen that exists to show the operator what is strange.
"""

from __future__ import annotations

import hashlib
from collections.abc import Iterable
from typing import Any

#: Characters kept from the hex digest. Sixteen hex characters are 64 bits — long enough
#: that a collision inside one review is not a practical concern, short enough to read in
#: a log line or a URL. Consumers MUST NOT assume any other length.
HUNK_ID_LENGTH = 16

#: The digest's field separator. A NUL can never appear in a source line that reached us
#: as text, so it cannot be confused with content — see ``hunk_identity``.
_FIELD_SEPARATOR = "\x00"


def _total_text(value: object) -> str:
    """Coerce anything to text without ever raising — the totality guard both public
    functions lean on. A value whose ``__str__`` is broken contributes its ``repr()``."""
    try:
        return str(value)
    except Exception:
        try:
            return repr(value)
        except Exception:
            return object.__repr__(value)


def _occurrence_text(occurrence: Any) -> str:
    """The decimal spelling of ``occurrence``, or its ``repr()`` when it is not a number
    at all. Returning the repr rather than raising is what keeps ``hunk_identity`` total
    for a caller that passes a string, ``None`` or an object by mistake."""
    try:
        return str(int(occurrence))
    except Exception:
        return _total_text(occurrence)


# The canonical text of a hunk's old side: trailing whitespace is noise, leading
# whitespace is meaning, so exactly one of the two is removed.
def normalise_old_side(lines: Iterable[str]) -> str:
    """Join a hunk's old-side lines into the canonical text its id is computed over.

    Each line loses its TRAILING whitespace only — spaces, tabs and a trailing ``\\r``, so
    that the same hunk arriving with CRLF endings, or via a writer that pads line ends,
    normalises to one text. The results are joined with ``\\n``.

    LEADING whitespace is preserved exactly, and internal whitespace runs are NOT
    collapsed, because indentation is meaning in every language this repository handles:
    two hunks that differ only in how their body is indented are DIFFERENT hunks, and an
    id that could not tell them apart would let an operator approve the wrong one.

    Total, like the rest of the module: a non-``str`` entry is coerced with ``str()``
    rather than rejected, and an empty iterable normalises to the empty string.
    """
    items: list[Any]
    try:
        items = list(lines)
    except Exception:
        # Not iterable at all. Treat the argument as a single line rather than raising:
        # a wrong-typed call must still get a usable id back.
        items = [lines]
    return "\n".join(_total_text(line).rstrip() for line in items)


# The public name of one hunk: the first HUNK_ID_LENGTH hex characters of a SHA-256 over
# the path, the canonical old side and the occurrence rank — never over a position.
def hunk_identity(path: str, old_side_lines: Iterable[str], occurrence: int = 0) -> str:
    """Return the stable content id of one hunk: ``HUNK_ID_LENGTH`` lowercase hex chars.

    The digest covers, in this order, ``path``, a NUL byte, ``normalise_old_side(
    old_side_lines)``, a NUL byte, and the decimal string of ``occurrence``. The NUL
    separators are load-bearing rather than decorative: without them a path ending in what
    happens to be the hunk's first context line would digest identically to a shorter path
    with a longer context, and two different hunks would share one name.

    ``occurrence`` disambiguates EXACT duplicates and nothing else. Two hunks in the SAME
    file whose normalised old sides are byte-identical would otherwise collide, so the
    caller passes 0 for the first such hunk, 1 for the second, and so on. It is the
    minimal disambiguator that keeps the id independent of POSITION: an unrelated edit
    elsewhere in the file changes neither a hunk's context nor its rank among its
    identical siblings, so neither changes its id.

    The joined text is encoded UTF-8 with ``errors="replace"``, so input no encoder can
    represent — a lone surrogate such as ``"\\ud800"`` pasted out of a broken tool, which
    a strict encode raises ``UnicodeEncodeError`` on — becomes ``b"?"`` and still yields
    an id. ``path`` and ``occurrence`` go through the same totality guards.

    Uses ``hashlib.sha256`` and deliberately never the builtin ``hash``: PEP 456 salts
    that builtin per process, so an id built on it would differ between two runs of the
    same program. ``tests/orchestration/test_hunk_identity.py`` pins this module's
    behaviour across a subprocess started with a different ``PYTHONHASHSEED``.
    """
    material = _FIELD_SEPARATOR.join((
        _total_text(path),
        normalise_old_side(old_side_lines),
        _occurrence_text(occurrence),
    ))
    digest = hashlib.sha256(material.encode("utf-8", errors="replace")).hexdigest()
    return digest[:HUNK_ID_LENGTH]
