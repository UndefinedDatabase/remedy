"""The rejected half of F033's approval loop: an operator's rejections, as repair findings.

WHY this module exists: ``docs/roadmap/features/T5_F033.md`` requires that "rejected hunks'
reasons appear verbatim in the following repair prompt", and its Design says rejections
"enqueue as repair findings for the next round, quoted with their reasons". The RECORD of
those rejections already exists — ``packages/orchestration/hunk_ledger.py`` holds each one's
``reason`` and says in its own docstring that the reason is "the operator's own words held
VERBATIM, surrounding whitespace included — T003 quotes it into the next repair prompt and
this is not the layer that reformats an operator's words". This is the layer that does the
quoting, and it does not reformat them either.

THE VERBATIM RULE IS THE WHOLE POINT. A reason reaches the rendered text byte for byte: no
strip, no rewrap, no escaping, no truncation, no case change, no collapsing of internal
whitespace. That is why a reason is emitted on its OWN LINES rather than inside a bullet or
a quoted span — a bullet would invite an indent, and an indent applied to the second line of
a two-line reason is a rewrite of what the operator typed. The feature file calls the trace
proof of this property acceptance material; it lives in
``tests/orchestration/test_hunk_repair_findings.py``.

DELIBERATE ABSENCE — this module is PURE: text and data in, text out. It reads no file,
runs no subprocess, opens no socket, reads no environment variable, keeps no state and logs
nothing, and it imports the standard library and ``packages.orchestration.hunk_ledger`` and
nothing else. It also does NOT build the ledger it renders (that is
``packages/orchestration/hunk_ledger.py``), does not decide whether a decision is coherent
(``packages/orchestration/hunk_approval.py``), and has NO CALLER YET — the round that wires
its output into the next builder prompt follows this one.

DELIBERATE ABSENCE — it never renders what was APPROVED. A repair prompt listing what the
operator accepted is a different feature; this one carries only what must change.

Every public name is TOTAL: it NEVER raises, on any input at all — ``None``, a non-iterable,
an object with no ``entries``, an entry with no ``reason``, an id whose ``__str__`` is
broken. ``hunk_ledger.py`` and ``hunk_approval.py`` state the same rule about themselves,
for the same reason: this text is built while an approval screen is on an operator's
display, and a renderer that throws on a strange id takes down the screen that exists to
show the operator what is strange. On anything unreadable this returns the EMPTY STRING
rather than a half-built block — a partial repair prompt is worse than none, because the
missing half is invisible to whoever reads it next.

Public API::

    REJECTION_FINDINGS_HEADING — str, the single heading a rendered findings block opens with
    REJECTION_FINDINGS_ENTRY_PREFIX — str, what precedes a rejected hunk's id on its own line
    REJECTION_FINDINGS_REASON_INTRO — str, the line announcing the verbatim reason below it
    render_rejection_findings — one attempt's rejected hunks as repair-prompt text
"""

from __future__ import annotations

from typing import Any

from packages.orchestration.hunk_ledger import HUNK_STATE_REJECTED

# The rendered vocabulary. Each fixed literal gets its own module-level NAME so a caller and
# a test match on the NAME and never on a spelling — the convention ``hunk_ledger.py`` states
# for its own two vocabularies. A test asserting the heading by retyping it is a test that
# passes for the wrong reason the day the wording is improved.

#: The one heading a non-empty findings block opens with.
REJECTION_FINDINGS_HEADING = "Rejected hunks — repair findings for the next round"
#: What precedes a rejected hunk's id, on a line of its own.
REJECTION_FINDINGS_ENTRY_PREFIX = "Hunk "
#: The line directly above a reason. It says "verbatim" because the lines below it are.
REJECTION_FINDINGS_REASON_INTRO = "The operator's reason, verbatim:"


def _total_text(value: object) -> str:
    """Coerce anything to text without ever raising.

    RE-STATED rather than imported: ``hunk_ledger._total_text`` is PRIVATE to that module,
    and this module follows the rule its siblings follow — ``hunk_approval`` re-states
    ``hunk_identity``'s guard and ``hunk_ledger`` re-states ``hunk_approval``'s, each for the
    same reason. A value whose ``__str__`` is broken contributes its ``repr()``, and one
    whose ``repr()`` is broken too contributes the unoverridable ``object.__repr__``.

    It is applied to the hunk ID and to NOTHING ELSE. An id with a broken ``__str__`` still
    renders — as its repr — so its operator's reason still reaches the repair prompt, which
    is the outcome that matters. A REASON is never coerced: the operator's words are either
    text or this block is not readable, and inventing the string "None" where a reason should
    be would put words in an operator's mouth."""
    try:
        return str(value)
    except Exception:
        try:
            return repr(value)
        except Exception:
            return object.__repr__(value)


# The one entry point: one attempt's ledger, rendered as the next round's repair findings.
def render_rejection_findings(ledger: Any) -> str:
    """The REJECTED hunks of one attempt as repair-prompt text, reasons quoted VERBATIM.

    Returns the EMPTY STRING when the ledger holds no rejection at all — an empty findings
    block is a heading with nothing under it, and a caller concatenating that into a prompt
    would tell the next round it has findings when it has none. An empty ledger and a ledger
    of nothing but approvals are DIFFERENT inputs and both legitimate: this feature's own
    edge-case note says a round in which the operator approves everything is a valid round.

    ORDER IS THE LEDGER'S OWN, which is the order the attempt's diff carries its hunks —
    ``HunkDecisionLedger`` exists in that order precisely so nobody downstream has to
    reconstruct it. Nothing here sorts and nothing here deduplicates.

    Never raises, on any input at all. THE STRUCTURAL GUARD IS THE ONE ``try`` BELOW and
    there is deliberately no second one inside it: a redundant inner layer would make this
    one unobservable, and a guard no test can redden is a guard nobody knows is there.
    Anything unreadable — no ``entries``, a non-iterable one, an entry with no ``state`` or
    no ``reason`` — discards the work in progress and yields ``""``, never a partial block.
    ``_total_text`` is the separate COERCION guard and covers the hunk id alone; its reason
    for existing beside this one is stated on it."""
    try:
        rendered: list[str] = []
        for entry in ledger.entries:
            # A5: only a rejection has a repair finding. An approved or pending entry
            # contributes NOTHING — not a heading, not a blank line, not a placeholder.
            if entry.state != HUNK_STATE_REJECTED:
                continue
            rendered.append(REJECTION_FINDINGS_ENTRY_PREFIX + _total_text(entry.hunk_id))
            rendered.append(REJECTION_FINDINGS_REASON_INTRO)
            # THE VERBATIM LINE. ``entry.reason`` is appended as it was stored and is never
            # stripped, wrapped, escaped, truncated, indented or re-cased. This is not the
            # layer that reformats an operator's words — ``hunk_ledger.py``'s docstring is
            # where that rule comes from, and this is the layer it was written for.
            rendered.append(entry.reason)
            rendered.append("")
        if not rendered:
            return ""
        return "\n".join([REJECTION_FINDINGS_HEADING, ""] + rendered)
    except Exception:
        return ""
