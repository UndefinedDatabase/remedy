"""Property tests for F033's hunk-approval decision core.

One test per PROPERTY the decision turns on, named for the property rather than for the
function that happens to implement it, so a later change of mechanism does not leave a
misleading test name behind. The properties, in the order they appear below: each of the
five refusal codes on its own; the refusal ORDER, pinned with inputs that trip two codes at
once; a mixed decision's approved, rejected and pending tuples; pending EMPTY when every
known hunk is decided, and otherwise in the known set's own order; a full-rejection round
with an empty approved set accepted as VALID, the edge case
``docs/roadmap/features/T5_F033.md`` names; a reason kept VERBATIM including surrounding
whitespace; the three ``rejected`` spellings agreeing; the offending-id list deduplicated
in first-appearance order; and TOTALITY — no input raises, in any argument position. Every
input is built inline: they are short lists of short ids, and a reader should see them
beside the expectation."""

from __future__ import annotations

import pytest

from packages.orchestration.hunk_approval import (
    REFUSAL_DUPLICATE_HUNK,
    REFUSAL_EMPTY_DECISION,
    REFUSAL_MISSING_REASON,
    REFUSAL_OVERLAPPING_SETS,
    REFUSAL_UNKNOWN_HUNK,
    HunkApprovalRefusal,
    HunkDecision,
    HunkRejection,
    decide_hunk_approval,
)

#: The ids one attempt's diff carries, in the order it carries them. Short stand-ins for
#: the sixteen hex characters ``hunk_identity`` really produces: nothing in the decision
#: core depends on an id's SHAPE, which is exactly why it compares ids as text.
KNOWN = ["h1", "h2", "h3", "h4"]


class _BrokenText:
    """An object whose ``__str__`` raises — the totality guard's worst realistic input."""

    def __str__(self) -> str:
        raise RuntimeError("__str__ is deliberately broken")

    def __repr__(self) -> str:
        return "<BrokenText>"


class _NotIterable:
    """Neither iterable nor a rejection in any accepted spelling."""


def test_a_decision_naming_no_hunk_is_refused_as_absent() -> None:
    result = decide_hunk_approval(KNOWN, [], [])
    assert isinstance(result, HunkApprovalRefusal)
    assert result.code == REFUSAL_EMPTY_DECISION
    assert result.hunk_ids == ()
    assert result.message


@pytest.mark.parametrize(
    ("approved", "rejected", "offending"),
    [
        (["h1", "h2", "h1"], [], ("h1",)),
        (["h1"], [("h2", "no"), ("h2", "still no")], ("h2",)),
    ],
    ids=["within-approved", "within-rejected"],
)
def test_an_id_repeated_inside_one_set_is_refused_as_a_duplicate(approved, rejected, offending) -> None:
    result = decide_hunk_approval(KNOWN, approved, rejected)
    assert isinstance(result, HunkApprovalRefusal)
    assert result.code == REFUSAL_DUPLICATE_HUNK
    assert result.hunk_ids == offending


def test_an_id_in_both_sets_is_refused_as_overlapping() -> None:
    result = decide_hunk_approval(KNOWN, ["h1", "h2"], [("h2", "not this one")])
    assert isinstance(result, HunkApprovalRefusal)
    assert result.code == REFUSAL_OVERLAPPING_SETS
    assert result.hunk_ids == ("h2",)


def test_an_id_the_diff_does_not_carry_is_refused_as_unknown() -> None:
    result = decide_hunk_approval(KNOWN, ["h1", "nope"], [])
    assert isinstance(result, HunkApprovalRefusal)
    assert result.code == REFUSAL_UNKNOWN_HUNK
    assert result.hunk_ids == ("nope",)


@pytest.mark.parametrize(
    "rejected",
    [
        [("h2", "")],
        [("h2", "   ")],
        [("h2", "\t\n ")],
        ["h2"],
        [{"id": "h2", "reason": None}],
        [{"id": "h2"}],
    ],
    ids=["empty", "spaces", "tab-newline", "bare-string", "null-reason", "no-reason-key"],
)
def test_a_rejection_without_a_real_reason_is_refused(rejected) -> None:
    """A bare string and a null reason land here too: they name a hunk and carry no reason,
    so they are that fault and not an exception. Every id here is KNOWN, so the earlier
    UNKNOWN_HUNK check cannot mask the code under test."""
    result = decide_hunk_approval(KNOWN, ["h1"], rejected)
    assert isinstance(result, HunkApprovalRefusal)
    assert result.code == REFUSAL_MISSING_REASON
    assert result.hunk_ids == ("h2",)


@pytest.mark.parametrize(
    ("known", "approved", "rejected", "expected", "also_trips"),
    [
        (["h1"], ["h1", "h1"], [("h1", "why")], REFUSAL_DUPLICATE_HUNK, REFUSAL_OVERLAPPING_SETS),
        ([], ["gone"], [("gone", "why")], REFUSAL_OVERLAPPING_SETS, REFUSAL_UNKNOWN_HUNK),
        (["h1"], ["h1"], [("gone", "")], REFUSAL_UNKNOWN_HUNK, REFUSAL_MISSING_REASON),
    ],
    ids=["duplicate-first", "overlapping-first", "unknown-first"],
)
def test_the_earlier_refusal_wins_when_one_input_trips_two(
    known, approved, rejected, expected, also_trips
) -> None:
    result = decide_hunk_approval(known, approved, rejected)
    assert isinstance(result, HunkApprovalRefusal)
    assert result.code == expected
    assert result.code != also_trips


def test_a_mixed_decision_reports_approved_rejected_and_the_pending_remainder() -> None:
    result = decide_hunk_approval(KNOWN, ["h3", "h1"], [("h2", "wrong constant")])
    assert isinstance(result, HunkDecision)
    assert result.approved == ("h3", "h1")
    assert result.rejected == (HunkRejection("h2", "wrong constant"),)
    assert result.pending == ("h4",)


def test_pending_follows_the_order_the_known_set_gave() -> None:
    result = decide_hunk_approval(["h4", "h3", "h2", "h1"], ["h2"], [])
    assert isinstance(result, HunkDecision)
    assert result.pending == ("h4", "h3", "h1")


def test_pending_is_empty_when_every_known_hunk_is_decided() -> None:
    result = decide_hunk_approval(KNOWN, ["h1", "h2"], [("h3", "no"), ("h4", "no")])
    assert isinstance(result, HunkDecision)
    assert result.pending == ()
    assert result.approved == ("h1", "h2")
    assert tuple(r.hunk_id for r in result.rejected) == ("h3", "h4")


def test_rejecting_everything_is_a_valid_decision_with_an_empty_approved_set() -> None:
    """The feature file's edge case: a full-rejection round is valid, and the repair gets
    every hunk back as a finding."""
    result = decide_hunk_approval(KNOWN, [], [(hunk_id, "not this") for hunk_id in KNOWN])
    assert isinstance(result, HunkDecision)
    assert result.approved == ()
    assert tuple(r.hunk_id for r in result.rejected) == tuple(KNOWN)
    assert result.pending == ()


def test_a_rejection_reason_is_kept_verbatim_including_its_whitespace() -> None:
    """T003 quotes the reason into the next repair prompt, so nothing here reformats it."""
    reason = "  leading and trailing space,\n and a newline  "
    result = decide_hunk_approval(KNOWN, ["h1"], [("h2", reason)])
    assert isinstance(result, HunkDecision)
    assert result.rejected[0].reason == reason


def test_the_three_rejection_spellings_produce_the_same_decision() -> None:
    dataclass_form = decide_hunk_approval(KNOWN, ["h1"], [HunkRejection("h2", "why")])
    tuple_form = decide_hunk_approval(KNOWN, ["h1"], [("h2", "why")])
    mapping_form = decide_hunk_approval(KNOWN, ["h1"], [{"id": "h2", "reason": "why"}])
    assert isinstance(dataclass_form, HunkDecision)
    assert dataclass_form == tuple_form == mapping_form
    assert dataclass_form.rejected == (HunkRejection("h2", "why"),)


def test_offending_ids_are_deduplicated_in_first_appearance_order() -> None:
    result = decide_hunk_approval(KNOWN, ["zz", "yy", "zz", "h1", "yy"], [])
    assert isinstance(result, HunkApprovalRefusal)
    assert result.code == REFUSAL_DUPLICATE_HUNK
    assert result.hunk_ids == ("zz", "yy")


def test_every_offending_id_is_reported_at_once_rather_than_one_per_round_trip() -> None:
    result = decide_hunk_approval(KNOWN, ["nope", "h1"], [("also-nope", "why")])
    assert isinstance(result, HunkApprovalRefusal)
    assert result.code == REFUSAL_UNKNOWN_HUNK
    assert result.hunk_ids == ("nope", "also-nope")


@pytest.mark.parametrize(
    "hostile",
    [None, _NotIterable(), [7], [_BrokenText()], _BrokenText(), 7],
    ids=["none", "not-iterable", "non-string-id", "broken-str", "bare-broken-str", "bare-int"],
)
def test_no_hostile_input_raises_in_any_position(hostile) -> None:
    """A validator that throws takes down the screen that exists to show the operator what
    is strange, so each of these must RETURN a decision or a refusal."""
    results = (
        decide_hunk_approval(KNOWN, hostile, []),
        decide_hunk_approval(KNOWN, ["h1"], hostile),
        decide_hunk_approval(hostile, ["h1"], []),
    )
    for result in results:
        assert isinstance(result, (HunkDecision, HunkApprovalRefusal))


def test_a_broken_object_is_named_by_its_repr_rather_than_crashing() -> None:
    result = decide_hunk_approval(KNOWN, [_BrokenText()], [])
    assert isinstance(result, HunkApprovalRefusal)
    assert result.code == REFUSAL_UNKNOWN_HUNK
    assert result.hunk_ids == ("<BrokenText>",)


def test_a_non_string_id_is_compared_as_text() -> None:
    result = decide_hunk_approval([7, "h1"], [7], [])
    assert isinstance(result, HunkDecision)
    assert result.approved == ("7",)
    assert result.pending == ("h1",)
