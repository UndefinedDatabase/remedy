"""Property tests for F033's hunk-decision ledger.

One test per PROPERTY the record turns on, named for the property rather than for the
function that happens to implement it, so a later change of mechanism does not leave a
misleading test name behind. The properties, in the order they appear below: the ledger is
in the DIFF's order and not the decision's; a repeated known id gets one row; each of the
three decision states lands on the hunk that earned it; a rejection reason arrives VERBATIM
and every other reason is empty; each of the three landing values in the case that produces
it; the two axes coming APART, which is the whole reason this module exists; a failed apply
refusing the ``landed_hunk_ids`` it was handed; an unattempted apply overriding every other
landing argument; a decided id the attempt does not carry being dropped; a ``None`` known set
yielding NO rows where any OTHER unusable value yields one naming it; the export carrying
four keys and nothing else; and TOTALITY — no input raises, in any argument position.

Decisions are built by CALLING ``decide_hunk_approval`` wherever the case allows it, so the
suite pins the two modules AGREEING rather than the ledger's reading of a shape nothing
produces. Only the dropped-id case hand-builds a ``HunkDecision``, because
``decide_hunk_approval`` refuses that input by design and so cannot produce it."""

from __future__ import annotations

import json

import pytest

from packages.orchestration.hunk_approval import (
    HunkDecision,
    HunkRejection,
    decide_hunk_approval,
)
from packages.orchestration.hunk_ledger import (
    HUNK_LANDING_LANDED,
    HUNK_LANDING_NOT_LANDED,
    HUNK_LANDING_UNATTEMPTED,
    HUNK_STATE_APPROVED,
    HUNK_STATE_PENDING,
    HUNK_STATE_REJECTED,
    HunkDecisionLedger,
    build_hunk_ledger,
    export_hunk_ledger,
)

#: The ids one attempt's diff carries, IN THE ORDER IT CARRIES THEM. Short stand-ins for
#: the sixteen hex characters ``hunk_identity`` really produces: nothing in the ledger
#: depends on an id's SHAPE, which is exactly why it compares ids as text.
KNOWN = ["h1", "h2", "h3", "h4"]

#: An operator's reason with surrounding whitespace, so "verbatim" is a testable claim
#: rather than a description. T003 quotes this text into the next repair prompt.
REASON = "  the regex is too greedy  "


def _coherent_decision(approved, rejected, known=KNOWN) -> HunkDecision:
    """A decision built the way production builds one — through the decision core."""
    result = decide_hunk_approval(known, approved, rejected)
    assert isinstance(result, HunkDecision), result
    return result


class _BrokenText:
    """An object whose ``__str__`` raises — the totality guard's worst realistic input."""

    def __str__(self) -> str:
        raise RuntimeError("__str__ is deliberately broken")

    def __repr__(self) -> str:
        return "<BrokenText>"


class _BrokenFlag:
    """An object whose truthiness raises, for the ``applied``/``apply_attempted`` guards."""

    def __bool__(self) -> bool:
        raise RuntimeError("__bool__ is deliberately broken")


class _BrokenAttributes:
    """An object whose attribute access raises, for the decision and entry readers."""

    def __getattr__(self, name: str) -> object:
        raise RuntimeError("__getattr__ is deliberately broken")


class _NotIterable:
    """Neither iterable nor a decision in any accepted spelling."""


def test_the_ledger_is_in_the_diffs_order_and_not_the_decisions() -> None:
    decision = _coherent_decision(["h4", "h1"], [{"id": "h3", "reason": REASON}])
    assert decision.approved == ("h4", "h1")
    ledger = build_hunk_ledger(KNOWN, decision)
    assert [entry.hunk_id for entry in ledger.entries] == KNOWN


def test_a_repeated_known_id_gets_exactly_one_row() -> None:
    decision = _coherent_decision(["h1"], [])
    ledger = build_hunk_ledger(["h2", "h1", "h2", "h1"], decision)
    assert [entry.hunk_id for entry in ledger.entries] == ["h2", "h1"]


def test_each_of_the_three_states_lands_on_the_hunk_that_earned_it() -> None:
    decision = _coherent_decision(["h1"], [{"id": "h2", "reason": REASON}])
    ledger = build_hunk_ledger(KNOWN, decision)
    assert [(entry.hunk_id, entry.state) for entry in ledger.entries] == [
        ("h1", HUNK_STATE_APPROVED),
        ("h2", HUNK_STATE_REJECTED),
        ("h3", HUNK_STATE_PENDING),
        ("h4", HUNK_STATE_PENDING),
    ]


def test_a_rejection_reason_arrives_verbatim_and_every_other_reason_is_empty() -> None:
    decision = _coherent_decision(["h1"], [{"id": "h2", "reason": REASON}])
    ledger = build_hunk_ledger(KNOWN, decision)
    assert [entry.reason for entry in ledger.entries] == [""] + [REASON] + ["", ""]


def test_each_of_the_three_landings_appears_in_the_case_that_produces_it() -> None:
    decision = _coherent_decision(["h1", "h2"], [{"id": "h3", "reason": REASON}])
    ledger = build_hunk_ledger(
        KNOWN,
        decision,
        applied=True,
        landed_hunk_ids=["h1"],
        apply_attempted=True,
    )
    assert [(entry.hunk_id, entry.landing) for entry in ledger.entries] == [
        ("h1", HUNK_LANDING_LANDED),
        ("h2", HUNK_LANDING_NOT_LANDED),
        ("h3", HUNK_LANDING_UNATTEMPTED),
        ("h4", HUNK_LANDING_UNATTEMPTED),
    ]


def test_an_approved_hunk_whose_apply_failed_is_still_approved_and_did_not_land() -> None:
    # The two axes coming apart is the reason this module exists: collapsing them would
    # make a failed apply indistinguishable from a rejection.
    decision = _coherent_decision(["h1"], [{"id": "h2", "reason": REASON}])
    ledger = build_hunk_ledger(KNOWN, decision, applied=False, apply_attempted=True)
    approved_entry = ledger.entries[0]
    rejected_entry = ledger.entries[1]
    assert (approved_entry.state, approved_entry.landing) == (
        HUNK_STATE_APPROVED,
        HUNK_LANDING_NOT_LANDED,
    )
    assert (rejected_entry.state, rejected_entry.landing) == (
        HUNK_STATE_REJECTED,
        HUNK_LANDING_UNATTEMPTED,
    )


def test_a_failed_apply_does_not_honour_the_landed_ids_it_was_handed() -> None:
    decision = _coherent_decision(["h1", "h2"], [{"id": "h3", "reason": REASON}])
    ledger = build_hunk_ledger(
        KNOWN,
        decision,
        applied=False,
        landed_hunk_ids=["h1", "h2"],
        apply_attempted=True,
    )
    assert [(entry.hunk_id, entry.landing) for entry in ledger.entries] == [
        ("h1", HUNK_LANDING_NOT_LANDED),
        ("h2", HUNK_LANDING_NOT_LANDED),
        ("h3", HUNK_LANDING_UNATTEMPTED),
        ("h4", HUNK_LANDING_UNATTEMPTED),
    ]


def test_an_unattempted_apply_overrides_every_other_landing_argument() -> None:
    decision = _coherent_decision(["h1", "h2"], [{"id": "h3", "reason": REASON}])
    ledger = build_hunk_ledger(
        KNOWN,
        decision,
        applied=True,
        landed_hunk_ids=["h1", "h2"],
        apply_attempted=False,
    )
    assert {entry.landing for entry in ledger.entries} == {HUNK_LANDING_UNATTEMPTED}
    assert [entry.state for entry in ledger.entries] == [
        HUNK_STATE_APPROVED,
        HUNK_STATE_APPROVED,
        HUNK_STATE_REJECTED,
        HUNK_STATE_PENDING,
    ]


def test_a_decided_id_the_attempt_does_not_carry_is_dropped() -> None:
    # ``decide_hunk_approval`` refuses this decision with ``REFUSAL_UNKNOWN_HUNK``, so it is
    # hand-built here: the ledger's rule is a guard against a hand-built value, not a path.
    decision = HunkDecision(
        approved=("h1", "ghost"),
        rejected=(HunkRejection("phantom", REASON),),
        pending=(),
    )
    ledger = build_hunk_ledger(
        ["h1", "h2"],
        decision,
        applied=True,
        landed_hunk_ids=["h1", "ghost"],
        apply_attempted=True,
    )
    assert [entry.hunk_id for entry in ledger.entries] == ["h1", "h2"]
    assert [entry.state for entry in ledger.entries] == [
        HUNK_STATE_APPROVED,
        HUNK_STATE_PENDING,
    ]


def test_a_none_known_set_yields_no_rows_where_another_unusable_value_yields_one() -> None:
    # ``_entries`` diverges from ``hunk_approval._entries`` here ON PURPOSE — its docstring
    # calls it "ONE DELIBERATE DIVERGENCE" — and this is what pins it: a fabricated hunk
    # called "None" in the operator's record is worse than an empty record that says nothing
    # is known. The SECOND half is the discriminator: without it this passes under an
    # ``_entries`` that returns ``[]`` for everything, which is not the shipped rule.
    decision = _coherent_decision(["h1"], [{"id": "h2", "reason": REASON}])
    assert build_hunk_ledger(None, decision).entries == ()
    unusable = build_hunk_ledger(7, decision)
    assert [entry.hunk_id for entry in unusable.entries] == ["7"]


def test_the_export_carries_the_four_keys_and_nothing_else() -> None:
    decision = _coherent_decision(["h1", "h2"], [{"id": "h3", "reason": REASON}])
    ledger = build_hunk_ledger(
        KNOWN,
        decision,
        applied=True,
        landed_hunk_ids=["h1"],
        apply_attempted=True,
    )
    exported = export_hunk_ledger(ledger)
    assert list(exported) == ["hunks"]
    assert len(exported["hunks"]) == len(ledger.entries)
    for row, entry in zip(exported["hunks"], ledger.entries):
        assert list(row) == ["id", "state", "reason", "landing"]
        assert row == {
            "id": entry.hunk_id,
            "state": entry.state,
            "reason": entry.reason,
            "landing": entry.landing,
        }
        assert all(isinstance(value, str) for value in row.values())
    assert json.loads(json.dumps(exported)) == exported


@pytest.mark.parametrize(
    ("known_hunk_ids", "keywords"),
    [
        (None, {}),
        (_NotIterable(), {}),
        ([1, 2.5, None], {}),
        ([_BrokenText()], {}),
        (_BrokenText(), {}),
        (KNOWN, {"applied": _BrokenFlag(), "apply_attempted": _BrokenFlag()}),
        (KNOWN, {"apply_attempted": True, "applied": True, "landed_hunk_ids": _NotIterable()}),
        (KNOWN, {"apply_attempted": True, "applied": True, "landed_hunk_ids": None}),
    ],
    ids=[
        "none-known",
        "non-iterable-known",
        "non-string-ids",
        "broken-str-id",
        "broken-str-known",
        "broken-flags",
        "non-iterable-landed",
        "none-landed",
    ],
)
def test_no_hostile_argument_makes_the_ledger_raise(known_hunk_ids, keywords) -> None:
    decision = _coherent_decision(["h1"], [{"id": "h2", "reason": REASON}])
    ledger = build_hunk_ledger(known_hunk_ids, decision, **keywords)
    assert isinstance(ledger, HunkDecisionLedger)
    assert all(isinstance(entry.hunk_id, str) for entry in ledger.entries)
    assert isinstance(export_hunk_ledger(ledger), dict)


@pytest.mark.parametrize(
    "decision",
    [None, _NotIterable(), _BrokenText(), _BrokenAttributes(), "h1", 7],
    ids=["none", "non-iterable", "broken-str", "broken-attributes", "bare-string", "int"],
)
def test_no_hostile_decision_makes_the_ledger_raise(decision) -> None:
    ledger = build_hunk_ledger(KNOWN, decision, apply_attempted=True, applied=True)
    assert isinstance(ledger, HunkDecisionLedger)
    assert [entry.hunk_id for entry in ledger.entries] == KNOWN
    assert {entry.state for entry in ledger.entries} == {HUNK_STATE_PENDING}
    assert isinstance(export_hunk_ledger(ledger), dict)


@pytest.mark.parametrize(
    "ledger",
    [None, _NotIterable(), _BrokenAttributes(), HunkDecisionLedger(entries=())],
    ids=["none", "non-iterable", "broken-attributes", "empty"],
)
def test_no_hostile_ledger_makes_the_export_raise(ledger) -> None:
    exported = export_hunk_ledger(ledger)
    assert list(exported) == ["hunks"]
    assert isinstance(exported["hunks"], list)
    assert json.loads(json.dumps(exported)) == exported
