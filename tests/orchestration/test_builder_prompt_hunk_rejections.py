"""F033: the operator's rejected hunks reach the NEXT builder prompt, verbatim.

THE ACCEPTANCE PROPERTY, and the reason this file exists: the feature file
``docs/roadmap/features/T5_F033.md`` requires that rejected hunks' reasons
appear "verbatim in the next trace". ``packages/orchestration/hunk_repair_findings.py``
renders them and ``tests/orchestration/test_hunk_repair_findings.py`` pins that
renderer. What is pinned HERE is the next link: that the rendered text survives
``compose_builder_prompt`` — segment registration, the ``"\\n"`` part join, the
one-newline-per-boundary adjustment and the ``PROMPT_SEGMENT_DELIMITER`` join —
BYTE FOR BYTE, so an operator's own words arrive at the next builder unchanged.

WHY A SUBSTRING ASSERTION AND NOT A NORMALISED ONE. Every reason below is chosen
to break under a normalisation: it carries leading spaces, an interior blank
line, a tab indent, a line whose first character is ``#`` and trailing spaces. A
test comparing stripped or re-wrapped forms would pass while composition quietly
rewrote what the operator typed, which is the exact failure the verbatim rule
exists to forbid. So each assertion is ``reason in composed.text`` on the RAW
reason.

THE VOCABULARY IS REFERENCED BY NAME. ``REJECTION_FINDINGS_HEADING``,
``REJECTION_FINDINGS_ENTRY_PREFIX`` and ``REJECTION_FINDINGS_REASON_INTRO`` are
imported and never retyped — the convention ``hunk_repair_findings.py``'s own
docstring states, because a test that retypes a heading passes for the wrong
reason the day the wording is improved.

DELIBERATE ABSENCE — nothing here asserts that the RUN LOOP supplies a ledger.
It does not yet: ``compose_builder_prompt``'s call site in ``run_pingpong`` is
unchanged this round because ``packages/orchestration/hunk_decision_record.py``
persists no decision, so there is no route from a stored decision to the loop to
test. A test asserting an end-to-end that does not exist would be a green gate
over a missing feature.
"""
from __future__ import annotations

import pytest

from packages.orchestration.hunk_ledger import (
    HUNK_LANDING_LANDED,
    HUNK_LANDING_NOT_LANDED,
    HUNK_LANDING_UNATTEMPTED,
    HUNK_STATE_APPROVED,
    HUNK_STATE_PENDING,
    HUNK_STATE_REJECTED,
    HunkDecisionLedger,
    HunkLedgerEntry,
)
from packages.orchestration.hunk_repair_findings import (
    REJECTION_FINDINGS_ENTRY_PREFIX,
    REJECTION_FINDINGS_HEADING,
    REJECTION_FINDINGS_REASON_INTRO,
)
from packages.orchestration.pingpong_loop import (
    _build_builder_prompt,
    compose_builder_prompt,
)
from packages.orchestration.pingpong_provider import ReviewFinding
from packages.orchestration.prompt_segments import SegmentStabilityRank

#: The segment this round adds. Named once so no test retypes it.
_SEGMENT = "builder_hunk_rejections"

_GOAL = "Make the widget resize with its container."
_CONTEXT = "## Repo Facts\nremedy, python, pytest."

#: THE HOSTILE REASON. Every character class that a strip, a re-wrap, an indent
#: or a comment-stripper would damage, in one string: two leading spaces, an
#: interior BLANK line, a tab-indented line, a line opening with ``#``, and two
#: trailing spaces. If composition normalises anything at all, this string stops
#: being a substring of the composed text.
_HOSTILE_REASON = (
    "  the resize helper is the wrong layer\n"
    "\n"
    "\tmove it beside the container instead\n"
    "# and drop the stale comment above it\n"
    "  "
)

_FINDINGS = [
    ReviewFinding(
        id="R-0001",
        severity="high",
        file="packages/widget.py",
        summary="resize ignores the container width",
        required_fix="read the container width before resizing",
    ),
]


def _rejected(hunk_id: str, reason: str) -> HunkLedgerEntry:
    return HunkLedgerEntry(
        hunk_id=hunk_id,
        state=HUNK_STATE_REJECTED,
        reason=reason,
        landing=HUNK_LANDING_NOT_LANDED,
    )


def _ledger(*entries: HunkLedgerEntry) -> HunkDecisionLedger:
    return HunkDecisionLedger(entries=tuple(entries))


def _compose(**kwargs):
    return compose_builder_prompt(_GOAL, _CONTEXT, **kwargs)


def _names(composed) -> list[str]:
    return [entry.name for entry in composed.manifest]


# ---------------------------------------------------------------- B1, B2


def test_a_hostile_reason_reaches_the_composed_prompt_as_an_exact_substring():
    """B1, the acceptance property: verbatim means byte for byte, not modulo whitespace."""
    composed = _compose(hunk_ledger=_ledger(_rejected("h-9c1f", _HOSTILE_REASON)))

    assert _HOSTILE_REASON in composed.text

    # And the vocabulary around it arrived too — by NAME, never by spelling.
    assert REJECTION_FINDINGS_HEADING in composed.text
    assert REJECTION_FINDINGS_ENTRY_PREFIX + "h-9c1f" in composed.text
    assert REJECTION_FINDINGS_REASON_INTRO in composed.text
    # The reason sits BELOW its intro line, which is what "verbatim below" means.
    assert composed.text.index(_HOSTILE_REASON) > composed.text.index(
        REJECTION_FINDINGS_REASON_INTRO
    )


def test_each_hostile_feature_survives_on_its_own():
    """B1 again, one property per reason, so a failure names the damage."""
    cases = {
        "leading_spaces": "   indented by three",
        "interior_blank_line": "first line\n\nthird line",
        "tab_indent": "\tone tab in front",
        "hash_first_character": "# not a heading, an operator's words",
        "trailing_spaces": "trailing two  ",
        "trailing_tab": "trailing tab\t",
        "carriage_return": "a line\r\nand another",
        "internal_run_of_spaces": "kept     five spaces",
    }
    for label, reason in cases.items():
        composed = _compose(hunk_ledger=_ledger(_rejected("h-1", reason)))
        assert reason in composed.text, label


def test_a_reason_ending_in_a_newline_keeps_that_newline():
    """B2: the boundary helper eats the RENDERER's structural newline, not the operator's.

    ``render_rejection_findings`` always terminates a non-empty block with a
    structural newline of its own, and ``_drop_one_newline_per_segment_boundary``
    removes exactly one newline at each boundary. This pins that the byte
    consumed there is the renderer's and never the last byte of a reason.
    """
    reason = "the operator pressed enter at the end\n"
    composed = _compose(hunk_ledger=_ledger(_rejected("h-2", reason)))
    assert reason in composed.text


def test_two_rejections_keep_the_ledger_order_and_both_reasons():
    first = "first rejection, verbatim  "
    second = "\tsecond rejection, verbatim"
    composed = _compose(
        hunk_ledger=_ledger(_rejected("h-a", first), _rejected("h-b", second))
    )
    assert first in composed.text
    assert second in composed.text
    assert composed.text.index(first) < composed.text.index(second)


# ---------------------------------------------------------------- B3


def test_no_rejection_registers_no_segment_and_changes_no_byte():
    """B3: the default, an empty ledger and an approvals-only ledger are all silent."""
    baseline = _compose()
    assert _SEGMENT not in _names(baseline)

    approvals_only = _ledger(
        HunkLedgerEntry(
            hunk_id="h-ok",
            state=HUNK_STATE_APPROVED,
            reason="",
            landing=HUNK_LANDING_LANDED,
        ),
        HunkLedgerEntry(
            hunk_id="h-wait",
            state=HUNK_STATE_PENDING,
            reason="",
            landing=HUNK_LANDING_UNATTEMPTED,
        ),
    )
    for ledger in (None, _ledger(), approvals_only):
        composed = _compose(hunk_ledger=ledger)
        assert _SEGMENT not in _names(composed)
        assert composed.text == baseline.text
        assert _names(composed) == _names(baseline)


def test_the_parameter_is_keyword_only():
    """Positional supply would silently land the ledger in ``round_number``."""
    with pytest.raises(TypeError):
        compose_builder_prompt(_GOAL, _CONTEXT, _ledger())  # type: ignore[misc]


# ---------------------------------------------------------------- B4, B5


def test_the_directive_is_still_the_last_segment_when_rejections_are_present():
    """B4: steering rank is shared, so ORDER here is registration order."""
    composed = _compose(hunk_ledger=_ledger(_rejected("h-3", "reason")))
    names = _names(composed)
    assert _SEGMENT in names
    assert names[-1] == "builder_directive"
    assert names.index(_SEGMENT) < names.index("builder_directive")


def test_rejections_sit_between_the_repair_findings_and_the_directive():
    """B4: with reviewer findings supplied too, all three steering segments order."""
    composed = _compose(
        findings=_FINDINGS,
        hunk_ledger=_ledger(_rejected("h-4", "reason")),
    )
    names = _names(composed)
    assert names.index("builder_repair") < names.index(_SEGMENT)
    assert names.index(_SEGMENT) < names.index("builder_directive")
    assert names[-1] == "builder_directive"


def test_the_segment_is_registered_at_steering_rank():
    composed = _compose(hunk_ledger=_ledger(_rejected("h-5", "reason")))
    entry = next(e for e in composed.manifest if e.name == _SEGMENT)
    assert entry.rank == SegmentStabilityRank.STEERING


def test_manifest_ranks_stay_non_decreasing_with_the_segment_present():
    """B5."""
    for kwargs in (
        dict(hunk_ledger=_ledger(_rejected("h-6", "reason"))),
        dict(findings=_FINDINGS, hunk_ledger=_ledger(_rejected("h-7", "reason"))),
        dict(
            findings=_FINDINGS,
            staged_state="M packages/widget.py",
            safe_diff="--- a/w.py\n+++ b/w.py\n+    resize()",
            task_body="Resize the widget.",
            scope_contract="## Scope Contract\nTouch only packages/widget.py.",
            test_result="3 passed in 0.10s",
            hunk_ledger=_ledger(_rejected("h-8", _HOSTILE_REASON)),
        ),
    ):
        composed = _compose(**kwargs)
        assert _SEGMENT in _names(composed)
        ranks = [entry.rank for entry in composed.manifest]
        assert ranks == sorted(ranks)


def test_the_segment_hash_and_span_agree_with_the_composed_text():
    """The manifest is not decoration: slice the segment back out and hash it."""
    import hashlib

    from packages.orchestration.prompt_segments import PROMPT_SEGMENT_DELIMITER

    composed = _compose(hunk_ledger=_ledger(_rejected("h-9", _HOSTILE_REASON)))
    position = 0
    span = None
    for entry in composed.manifest:
        if entry.name == _SEGMENT:
            span = (position, position + entry.chars)
        position += entry.chars + len(PROMPT_SEGMENT_DELIMITER)
    assert span is not None
    chunk = composed.text[span[0]:span[1]]
    segment = next(e for e in composed.manifest if e.name == _SEGMENT)
    assert hashlib.sha256(chunk.encode("utf-8")).hexdigest() == segment.sha256
    assert _HOSTILE_REASON in chunk


# ---------------------------------------------------------------- B6


def test_a_malformed_ledger_composes_without_raising_and_registers_nothing():
    """B6: the renderer is TOTAL, so composition inherits totality — it never throws here."""

    class _NoEntries:
        pass

    class _EntryWithoutReason:
        state = HUNK_STATE_REJECTED
        hunk_id = "h-broken"

    class _EntriesNotIterable:
        entries = 7

    class _BadEntryHolder:
        entries = (_EntryWithoutReason(),)

    baseline = _compose()
    for ledger in (
        _NoEntries(),
        _EntriesNotIterable(),
        _BadEntryHolder(),
        object(),
        "not a ledger at all",
        42,
    ):
        composed = _compose(hunk_ledger=ledger)
        assert _SEGMENT not in _names(composed)
        assert composed.text == baseline.text


def test_a_ledger_whose_second_entry_is_broken_registers_nothing_at_all():
    """A PARTIAL block is worse than none: the renderer discards work in progress."""
    baseline = _compose()

    class _EntryWithoutReason:
        state = HUNK_STATE_REJECTED
        hunk_id = "h-broken"

    class _Mixed:
        entries = (_rejected("h-good", "a readable reason"), _EntryWithoutReason())

    composed = _compose(hunk_ledger=_Mixed())
    assert _SEGMENT not in _names(composed)
    assert composed.text == baseline.text
    assert "a readable reason" not in composed.text


# ---------------------------------------------------------------- B7


def test_build_builder_prompt_forwards_the_parameter_unchanged():
    """B7."""
    ledger = _ledger(_rejected("h-10", _HOSTILE_REASON))
    built = _build_builder_prompt(_GOAL, _CONTEXT, hunk_ledger=ledger)
    assert built == _compose(hunk_ledger=ledger).text
    assert _HOSTILE_REASON in built
    # And with no ledger it is byte-equal to the call that omits the parameter.
    assert _build_builder_prompt(_GOAL, _CONTEXT) == _build_builder_prompt(
        _GOAL, _CONTEXT, hunk_ledger=None
    )
