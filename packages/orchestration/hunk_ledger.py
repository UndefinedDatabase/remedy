"""The durable record of what an operator decided about each hunk, and what became of it.

WHY this module exists: rounds 6 through 9 of F033 decide whether a selection is coherent,
which bytes it means, how it lands and how a failure to land is told truthfully. None of
them produces the RECORD — the thing ``docs/roadmap/features/T5_F033.md`` calls "the ledger
of hunk decisions in evidence" and the thing T003's viewer badges, node glyph and report
line all read. It lands here, in something that records and does nothing else.

TWO AXES, NEVER ONE. A hunk carries a DECISION — approved, rejected or pending — and
SEPARATELY a LANDING: did those bytes reach the branch. They come apart in exactly the
state this feature exists to render honestly. An approved hunk whose apply failed is still
APPROVED and did NOT land, and collapsing the two axes into one would make a failed apply
indistinguishable from a rejection, which is the single most misleading thing this feature
could tell an operator. So every entry carries both, and neither is derived from the other.

THE ORDER IS THE DIFF'S ORDER, which is why ``known_hunk_ids`` is the first argument. A
``HunkDecision`` gives ``approved`` in the order the operator gave it, ``rejected`` in the
order the operator gave it, and ``pending`` in the known set's order — three orders, none of
them the one a viewer renders in. Rather than recover an order it was never given, this
module is handed the attempt's full hunk list and walks IT. That list is also what makes
"5 of 8" answerable at all: the decision alone does not carry the 8.

DELIBERATE ABSENCE — this module does NOT import ``packages/orchestration/hunk_apply.py``,
and that is a constraint rather than an oversight. That module imports
``packages/orchestration/source_apply.py``, which is the first entry of ``FORBIDDEN_MODULES``
in ``tests/ui_server/test_command_channel.py``: nothing reachable from the HTTP write door
may drag the applier behind it. The ledger is precisely what the write door will write, so
it must stay importable from anywhere. It therefore takes PLAIN VALUES — a bool and a list
of ids — where a ``HunkApplyOutcome`` would otherwise have been the obvious argument. A
reader who wants the apply seam itself wants ``packages/orchestration/hunk_apply.py``; one
who wants whether a decision is coherent at all wants
``packages/orchestration/hunk_approval.py``; one who wants which bytes an approved selection
means wants ``packages/orchestration/hunk_subset_diff.py``; one who wants where a hunk id
COMES FROM wants ``packages/orchestration/hunk_identity.py``.

DELIBERATE ABSENCE — it decides nothing, applies nothing, reads no diff, opens no file,
runs no subprocess, writes no log and keeps no state. It imports the standard library and
``packages.orchestration.hunk_approval`` and nothing else.

Every public name is TOTAL: it NEVER raises, on any input at all — a non-iterable, ``None``,
a non-string id, or an object whose ``__str__`` is broken. Totality is not politeness: this
runs while rendering the approval screen and while writing evidence, and a recorder that
throws on a strange id takes down the very screen that exists to show the operator what is
strange. ``hunk_approval.py`` states the same rule, and its ``_total_text`` is the shape the
guard below follows — RE-STATED rather than imported, because that name is private there and
this module follows the rule its siblings do.

Public API::

    HUNK_STATE_APPROVED — str, the decision badge for an approved hunk
    HUNK_STATE_REJECTED — str, the decision badge for a rejected hunk
    HUNK_STATE_PENDING — str, the decision badge for an undecided hunk
    HUNK_LANDING_LANDED — str, the landing value for bytes that reached the branch
    HUNK_LANDING_NOT_LANDED — str, the landing value for an attempt that did not land them
    HUNK_LANDING_UNATTEMPTED — str, the landing value for bytes never submitted at all
    HunkLedgerEntry — one hunk's id, decision state, verbatim reason and landing
    HunkDecisionLedger — the ordered entries of one attempt
    build_hunk_ledger — known ids plus a decision plus what became of it, as a ledger
    export_hunk_ledger — that ledger as a JSON-safe dict
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from packages.orchestration.hunk_approval import HunkDecision

# The DECISION vocabulary — one closed set of three, the viewer's three badges, named in the
# Partial-state-truth bullet of ``docs/roadmap/features/T5_F033.md``. Each gets its own
# module-level NAME so a caller matches on the name and never on a spelling.

#: The operator approved this hunk.
HUNK_STATE_APPROVED = "approved"
#: The operator rejected this hunk, and the entry carries the reason verbatim.
HUNK_STATE_REJECTED = "rejected"
#: The operator decided this hunk NEITHER way. A legitimate state, not an error.
HUNK_STATE_PENDING = "pending"

# The LANDING vocabulary — the SECOND axis, and the reason this module exists as a pair
# rather than as a single status. ``unattempted`` is NOT a synonym for ``not_landed`` and
# the distinction is load-bearing: it separates "we tried and it did not land" from "no
# apply has run", which is exactly what a viewer must not conflate before the operator has
# pressed anything.

#: These bytes reached the branch.
HUNK_LANDING_LANDED = "landed"
#: An apply ran and these bytes did NOT reach the branch.
HUNK_LANDING_NOT_LANDED = "not_landed"
#: These bytes were never submitted to an apply at all.
HUNK_LANDING_UNATTEMPTED = "unattempted"

#: The four keys ``export_hunk_ledger`` writes per entry, and the only ones it writes.
_EXPORT_ENTRY_KEYS = ("id", "state", "reason", "landing")
#: The single top-level key the exported dict carries.
_EXPORT_ROOT_KEY = "hunks"


@dataclass(frozen=True)
class HunkLedgerEntry:
    """One hunk of one attempt, on BOTH axes.

    ``state`` is one of the three ``HUNK_STATE_*`` values and ``landing`` one of the three
    ``HUNK_LANDING_*`` values; they are independent, and an approved hunk that did not land
    is the whole reason they are two fields. ``reason`` is the operator's own words held
    VERBATIM, surrounding whitespace included — T003 quotes it into the next repair prompt
    and this is not the layer that reformats an operator's words. It is ``""`` for every
    state but ``rejected``, because only a rejection has one."""

    hunk_id: str
    state: str
    reason: str
    landing: str


@dataclass(frozen=True)
class HunkDecisionLedger:
    """The entries of ONE attempt, in the order the attempt's diff carries its hunks.

    It deliberately holds NO counts. The feature's report line — "partially approved (5/8
    hunks)" — is derived from ``entries`` by whoever renders it, for the same reason
    ``HunkDecision.pending`` is computed once in ``hunk_approval`` rather than by each
    caller: two derivations of one number drift apart, and a stored count is a third."""

    entries: tuple[HunkLedgerEntry, ...]


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


def _total_flag(value: object) -> bool:
    """A flag read without ever raising. An object whose ``__bool__`` is broken reads FALSE,
    never TRUE: a flag we cannot read is not a claim we are entitled to make, and both flags
    here only ever WIDEN what this module asserts about disk."""
    try:
        return bool(value)
    except Exception:
        return False


def _total_attr(value: object, name: str) -> Any:
    """One attribute, or ``None``, without ever raising — an object with a broken
    ``__getattr__`` contributes nothing rather than propagating its exception."""
    try:
        return getattr(value, name, None)
    except Exception:
        return None


def _entries(value: Any) -> list[Any]:
    """The entries of an argument that is SUPPOSED to be an iterable, without raising. A
    ``str``, a bytes-like value and a ``Mapping`` each count as ONE entry, never an iterable
    of characters or keys: a caller passing a single id must get that one thing back and not
    fragments reported as several strange ids. Anything not iterable at all is likewise one
    entry, so a wrong-typed call surfaces as a row NAMING what it saw. This mirrors
    ``hunk_approval._entries``; the two are re-stated rather than shared for the reason the
    module docstring gives. ONE DELIBERATE DIVERGENCE from that sibling: ``None`` yields NO
    entries here rather than one. A validator reports the strange value it was handed, but a
    LEDGER would render it as a row, and a fabricated hunk called "None" in the operator's
    record is worse than an empty record that says nothing is known."""
    if value is None:
        return []
    if isinstance(value, (str, bytes, bytearray, Mapping)):
        return [value]
    try:
        return list(value)
    except Exception:
        return [value]


def _id_list(value: Any) -> list[str]:
    """Every entry of ``value`` as text, in the order given. An id is compared AS TEXT,
    exactly as ``hunk_approval`` compares one."""
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


def _rejection_reasons(decision: Any) -> dict[str, str]:
    """Every rejected id mapped to its reason, VERBATIM. FIRST appearance wins, matching the
    first-appearance rule ``_unique`` applies to ids; ``decide_hunk_approval`` refuses a
    decision that names one id twice, so a repeat can only arrive from a hand-built
    ``HunkDecision`` and this fixes what such a value means rather than leaving it open."""
    reasons: dict[str, str] = {}
    for entry in _entries(_total_attr(decision, "rejected")):
        hunk_id = _total_text(_total_attr(entry, "hunk_id"))
        if hunk_id not in reasons:
            reasons[hunk_id] = _total_text(_total_attr(entry, "reason"))
    return reasons


def _entry_state(hunk_id: str, approved: set[str], reasons: Mapping[str, str]) -> str:
    """The DECISION axis for one hunk.

    APPROVED IS CHECKED FIRST, and the order is stated here rather than left to chance. An
    id in BOTH sets cannot reach this module — ``decide_hunk_approval`` refuses that decision
    with ``REFUSAL_OVERLAPPING_SETS`` before a ``HunkDecision`` can exist — so the branch
    order is unobservable through the supported path. It is fixed anyway because a
    hand-built ``HunkDecision`` can reach here, and an unpinned order is one a later refactor
    changes silently in the exact case a reader would most want defined."""
    if hunk_id in approved:
        return HUNK_STATE_APPROVED
    if hunk_id in reasons:
        return HUNK_STATE_REJECTED
    return HUNK_STATE_PENDING


def _entry_landing(state: str, applied: bool, landed: set[str], hunk_id: str) -> str:
    """The LANDING axis for one hunk, given that an apply WAS attempted.

    Only an approved hunk was ever submitted, so a rejected or pending one is
    ``unattempted`` even here — it was not tried, which is a different fact from "it was
    tried and did not land".

    A DELIBERATE REFUSAL, and this is its ONLY site: while ``applied`` is false, ``landed``
    is not consulted at all. A caller passing ids alongside ``applied=False`` is
    contradicting ``HunkApplyOutcome``'s own contract, which keeps ``landed`` empty whenever
    ``applied`` is false, and this module will not mint a landing out of that contradiction
    — it refuses the ids rather than trusting the caller, so the worst a confused caller
    produces is an understated ledger. The refusal is stated HERE and nowhere else: a rule
    enforced in two places is a rule whose two copies are free to drift apart, and a second
    copy would also make this one unobservable to the test that pins it."""
    if state != HUNK_STATE_APPROVED:
        return HUNK_LANDING_UNATTEMPTED
    if not applied:
        return HUNK_LANDING_NOT_LANDED
    return HUNK_LANDING_LANDED if hunk_id in landed else HUNK_LANDING_NOT_LANDED


# The one entry point: the attempt's hunks, the operator's decision, and what became of it.
def build_hunk_ledger(
    known_hunk_ids: Iterable[str],
    decision: HunkDecision,
    *,
    applied: bool = False,
    landed_hunk_ids: Iterable[str] = (),
    apply_attempted: bool = False,
) -> HunkDecisionLedger:
    """The ordered record of every hunk in one attempt, on both axes.

    ``known_hunk_ids`` is the attempt's full hunk list in the DIFF's order and is what this
    walks: one entry per known hunk, repeats removed keeping first appearance. An id that
    ``decision`` names but ``known_hunk_ids`` does not is DROPPED rather than appended — the
    ledger is the record of THIS attempt's hunks and an id outside it has no row to render.
    ``decide_hunk_approval`` already refuses such a decision with ``REFUSAL_UNKNOWN_HUNK``,
    so that is a guard rather than a path.

    ``apply_attempted`` is the outer switch: while it is false EVERY entry is
    ``unattempted``, whatever ``applied`` and ``landed_hunk_ids`` say, because no apply has
    run and a viewer must not show a landing verdict before the operator has pressed
    anything. Never raises, on any input at all."""
    known_ids = _unique(_id_list(known_hunk_ids))
    approved = set(_id_list(_total_attr(decision, "approved")))
    reasons = _rejection_reasons(decision)
    attempted = _total_flag(apply_attempted)
    did_apply = _total_flag(applied)

    # ``landed_hunk_ids`` is coerced here and JUDGED in ``_entry_landing``, which is the one
    # place that decides whether it may be consulted at all. Coercing it unconditionally is
    # deliberate: the refusal belongs to the landing rule, not to this assignment.
    landed = set(_id_list(landed_hunk_ids))

    entries: list[HunkLedgerEntry] = []
    for hunk_id in known_ids:
        state = _entry_state(hunk_id, approved, reasons)
        if attempted:
            landing = _entry_landing(state, did_apply, landed, hunk_id)
        else:
            landing = HUNK_LANDING_UNATTEMPTED
        reason = reasons.get(hunk_id, "") if state == HUNK_STATE_REJECTED else ""
        entries.append(HunkLedgerEntry(hunk_id, state, reason, landing))
    return HunkDecisionLedger(tuple(entries))


def export_hunk_ledger(ledger: HunkDecisionLedger) -> dict:
    """``ledger`` as a JSON-safe dict: plain ``str`` and ``list`` throughout, one object per
    entry under the single key ``hunks``, with exactly the keys ``id``, ``state``, ``reason``
    and ``landing``. It adds NOTHING the entries do not already hold — no counts, no summary
    and no derived badge — for the reason ``HunkDecisionLedger`` holds no counts either.
    Never raises, on any input at all."""
    hunks = []
    for entry in _entries(_total_attr(ledger, "entries")):
        values = (
            _total_text(_total_attr(entry, "hunk_id")),
            _total_text(_total_attr(entry, "state")),
            _total_text(_total_attr(entry, "reason")),
            _total_text(_total_attr(entry, "landing")),
        )
        hunks.append(dict(zip(_EXPORT_ENTRY_KEYS, values)))
    return {_EXPORT_ROOT_KEY: hunks}
