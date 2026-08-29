"""The pure decision core of F033's hunk-level approval: is this selection coherent?

WHY this module exists: the approval screen must say that a selection is wrong, and WHICH
hunks are wrong, BEFORE anything is applied. Folding that judgement into the applier or the
write-door handler would make "is this decision coherent?" a question you can only ask by
attempting the change, so it lives here, in something that decides and does nothing else.
It is also the piece every later T002 commit validates against, which is why it lands first
and alone. It decides ONE thing: whether an operator's ``approved`` and ``rejected`` sets
are a coherent decision over the hunks an attempt's diff actually carries — one that names
something, contradicts neither itself nor the diff, and carries a reason on every
rejection. The answer is a ``HunkDecision`` (approved, normalised rejections, and the
PENDING remainder) or a ``HunkApprovalRefusal`` carrying one named code and every offending
id.

DELIBERATE ABSENCE — this module applies NOTHING. It does not read a diff, holds no hunk
header regex, does not know what a hunk's CONTENT is, and never learns whether the approved
set would apply cleanly; a conflict is the applier's answer, not this one's. It touches no
file system, no subprocess, no network, no logging and no global mutable state, uses the
standard library only, and imports no other module of this package. A reader who wants the
apply mechanics wants ``packages/orchestration/source_apply.py``; one who wants where a
hunk id COMES FROM wants ``packages/orchestration/hunk_identity.py``; one who wants how a
diff becomes hunks at all wants ``packages/orchestration/diff_parser.py``.

Every public name is TOTAL: it NEVER raises, on any input at all — a non-iterable,
``None``, a non-string id, or an object whose ``__str__`` is broken. Totality is not
politeness: this runs while rendering the approval screen, and a validator that throws on a
strange id takes down the very screen that exists to show the operator what is strange.
``hunk_identity.py`` states the same rule, and its ``_total_text`` is the shape the guard
below follows — re-stated rather than imported, because that name is private there and this
module deliberately imports nothing but the standard library.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

# The refusal codes. Each gets its own module-level NAME so a caller matches on the name
# and never on a message. ``decide_hunk_approval`` checks them in exactly the order
# declared here and returns the FIRST that trips; that order is contract, and tests pin it
# with inputs tripping two at once, because an unpinned order is one a later refactor
# changes silently. It is not arbitrary: a decision naming nothing at all is not malformed
# but ABSENT; a set contradicting ITSELF is reported before one contradicting the DIFF; and
# a missing reason is last because it is the only fault an operator repairs by typing.

#: The operator approved nothing and rejected nothing — there is no decision to check.
REFUSAL_EMPTY_DECISION = "empty_decision"
#: An id appears more than once WITHIN ``approved``, or more than once WITHIN ``rejected``.
REFUSAL_DUPLICATE_HUNK = "duplicate_hunk"
#: An id appears in BOTH sets, so the operator both approved and rejected it.
REFUSAL_OVERLAPPING_SETS = "overlapping_sets"
#: An id is not among the hunks the attempt's diff actually carries.
REFUSAL_UNKNOWN_HUNK = "unknown_hunk"
#: A rejection carries no reason, or only whitespace where a reason should be.
REFUSAL_MISSING_REASON = "missing_reason"

#: Keys a wire-form rejection may spell its id with. The feature file writes the wire form
#: as ``rejected[{id, reason}]``; ``hunk_id`` is accepted too so a caller that dumps a
#: ``HunkRejection`` to a dict round-trips through here unchanged.
_ID_KEYS = ("id", "hunk_id")
#: Key a wire-form rejection spells its reason with.
_REASON_KEYS = ("reason",)


@dataclass(frozen=True)
class HunkRejection:
    """One rejected hunk and the operator's reason for rejecting it. ``reason`` is held
    VERBATIM, surrounding whitespace included: T003 quotes it into the next repair prompt
    and this is not the layer that reformats an operator's words."""

    hunk_id: str
    reason: str


@dataclass(frozen=True)
class HunkDecision:
    """A coherent decision over the hunks one attempt's diff carries.

    ``pending`` is the ids the attempt carries that the operator decided NEITHER way, in
    the order the known set gave them. It is computed here rather than by a caller because
    the feature's report line — "partially approved (5/8 hunks)" — and T003's viewer badges
    both need it, and two derivations of one number drift apart. An undecided hunk is a
    legitimate state, not an error: ``docs/roadmap/features/T5_F033.md`` rules that new
    hunks appearing in a later round render PENDING with no inherited decision."""

    approved: tuple[str, ...]
    rejected: tuple[HunkRejection, ...]
    pending: tuple[str, ...]


@dataclass(frozen=True)
class HunkApprovalRefusal:
    """Why a decision was refused, and which ids are at fault. ``hunk_ids`` carries every
    offending id, DEDUPLICATED and in first-appearance order, so the operator sees all of
    them at once rather than one per round-trip; it is empty when no single id is at fault,
    which is the ``REFUSAL_EMPTY_DECISION`` case."""

    code: str
    message: str
    hunk_ids: tuple[str, ...]


def _total_text(value: object) -> str:
    """Coerce anything to text without ever raising — the totality guard everything below
    leans on. A value whose ``__str__`` is broken contributes its ``repr()``, and one whose
    ``repr()`` is broken too contributes the unoverridable ``object.__repr__``."""
    try:
        return str(value)
    except Exception:
        try:
            return repr(value)
        except Exception:
            return object.__repr__(value)


def _entries(value: Any) -> list[Any]:
    """The entries of an argument that is SUPPOSED to be an iterable, without raising. A
    ``str``, a bytes-like value, a ``Mapping`` and a ``HunkRejection`` each count as ONE
    entry, never an iterable of characters, keys or fields: a caller passing a single id, or
    a single wire-form rejection it forgot to wrap in a list, must get that one thing back
    and not fragments reported as several strange ids. Anything not iterable at all is
    likewise one entry, so a wrong-typed call surfaces as a refusal NAMING what it saw."""
    if isinstance(value, (str, bytes, bytearray, Mapping, HunkRejection)):
        return [value]
    try:
        return list(value)
    except Exception:
        return [value]


def _id_list(value: Any) -> list[str]:
    """Every entry of ``value`` as text, in the order given. An id is compared as text."""
    return [_total_text(entry) for entry in _entries(value)]


def _unique(ids: Iterable[str]) -> list[str]:
    """``ids`` with repeats removed, keeping FIRST-appearance order."""
    seen: set[str] = set()
    unique: list[str] = []
    for identifier in ids:
        if identifier not in seen:
            seen.add(identifier)
            unique.append(identifier)
    return unique


def _repeated(ids: list[str]) -> list[str]:
    """The ids appearing more than once in ``ids``, once each, in first-appearance order."""
    counts = Counter(ids)
    return [identifier for identifier in _unique(ids) if counts[identifier] > 1]


def _mapping_value(entry: Mapping, keys: tuple[str, ...]) -> Any:
    """The first present key's value, or ``None``. A mapping whose ``__contains__`` or
    ``__getitem__`` raises contributes nothing rather than propagating the exception."""
    for key in keys:
        try:
            if key in entry:
                return entry[key]
        except Exception:
            continue
    return None


def _reason_text(value: Any) -> str:
    """A reason as text, kept VERBATIM — leading and trailing whitespace and all. An ABSENT
    reason and an explicit ``None`` are the same thing, no reason, so both become the empty
    string and trip ``REFUSAL_MISSING_REASON`` rather than becoming the literal text
    ``"None"``, which would sail straight past the emptiness check that code names."""
    if value is None:
        return ""
    return _total_text(value)


def _normalise_rejection(entry: Any) -> HunkRejection:
    """One rejection in any of its three spellings, as a ``HunkRejection``: the wire form is
    a mapping (``{"id": ..., "reason": ...}``), the test form a tuple, the internal form the
    dataclass, and they are normalised once, here, so no caller has to. An entry that is
    NONE of the three — a bare string, ``None``, an arbitrary object — yields its id as far
    as one can be recovered and an EMPTY reason, so it is reported as a fault about its
    reason rather than as an exception."""
    if isinstance(entry, HunkRejection):
        return HunkRejection(_total_text(entry.hunk_id), _reason_text(entry.reason))
    if isinstance(entry, Mapping):
        return HunkRejection(
            _total_text(_mapping_value(entry, _ID_KEYS)),
            _reason_text(_mapping_value(entry, _REASON_KEYS)),
        )
    if isinstance(entry, Sequence) and not isinstance(entry, (str, bytes, bytearray)):
        try:
            parts = list(entry)
        except Exception:
            parts = []
        return HunkRejection(
            _total_text(parts[0]) if parts else "",
            _reason_text(parts[1]) if len(parts) > 1 else "",
        )
    return HunkRejection(_total_text(entry), "")


# The one entry point: a coherent decision, or a named refusal naming the offending ids.
def decide_hunk_approval(
    known_hunk_ids: Iterable[str],
    approved: Iterable[str],
    rejected: Iterable[HunkRejection | tuple[str, str] | Mapping[str, str]],
) -> HunkDecision | HunkApprovalRefusal:
    """Decide whether ``approved`` and ``rejected`` are coherent over ``known_hunk_ids`` —
    the ids the attempt's diff really carries, in the order it carries them. Returns a
    ``HunkDecision`` (``approved`` in the order given, ``rejected`` normalised in the order
    given with reasons kept verbatim, and the pending remainder) or the FIRST
    ``HunkApprovalRefusal`` that trips, in the order the refusal codes are declared above.
    Never raises, on any input at all."""
    known_ids = _unique(_id_list(known_hunk_ids))
    approved_ids = _id_list(approved)
    rejections = [_normalise_rejection(entry) for entry in _entries(rejected)]
    rejected_ids = [rejection.hunk_id for rejection in rejections]

    # From here down every value in play is a plain ``str`` produced by ``_total_text``, so
    # nothing below can raise: the totality guards sit at the BOUNDARY, and the rules need
    # no catch-all that would swallow a real defect along with a hostile input.
    both_sets = approved_ids + rejected_ids

    if not approved_ids and not rejections:
        return HunkApprovalRefusal(
            REFUSAL_EMPTY_DECISION,
            "The decision names no hunk at all — approve or reject at least one hunk.",
            (),
        )

    duplicates = _unique(_repeated(approved_ids) + _repeated(rejected_ids))
    if duplicates:
        return HunkApprovalRefusal(
            REFUSAL_DUPLICATE_HUNK,
            "These hunks are named more than once within one set: " + ", ".join(duplicates) + ".",
            tuple(duplicates),
        )

    approved_set = set(approved_ids)
    rejected_set = set(rejected_ids)
    overlapping = _unique([i for i in both_sets if i in approved_set and i in rejected_set])
    if overlapping:
        return HunkApprovalRefusal(
            REFUSAL_OVERLAPPING_SETS,
            "These hunks are both approved and rejected: " + ", ".join(overlapping) + ".",
            tuple(overlapping),
        )

    known_set = set(known_ids)
    unknown = _unique([i for i in both_sets if i not in known_set])
    if unknown:
        return HunkApprovalRefusal(
            REFUSAL_UNKNOWN_HUNK,
            "These hunks are not in this attempt's diff: " + ", ".join(unknown) + ".",
            tuple(unknown),
        )

    unreasoned = _unique([r.hunk_id for r in rejections if not r.reason.strip()])
    if unreasoned:
        return HunkApprovalRefusal(
            REFUSAL_MISSING_REASON,
            "These rejected hunks carry no reason: " + ", ".join(unreasoned) + ".",
            tuple(unreasoned),
        )

    decided = approved_set | rejected_set
    return HunkDecision(
        tuple(approved_ids),
        tuple(rejections),
        tuple(i for i in known_ids if i not in decided),
    )
