"""Contract tests for packages/orchestration/decision_evidence.py (F032 T001a).

Every test asserts on the PROBLEM SENTENCE ``evidence_triple_problems`` returns,
never merely on the list being non-empty: a test that only counts problems stays
green when a rule fires for the wrong reason, and the whole point of the
validator is that a producer can read why its triple was refused.

Each fixture below is otherwise valid and breaks exactly ONE rule, so the
expected problem list is written out in full rather than searched.
"""

from __future__ import annotations

import pytest

from packages.memory import local_gateway
from packages.memory.models import MemoryEntry
from packages.orchestration import decision_evidence
from packages.orchestration.decision_evidence import (
    DECISION_EVIDENCE_STATUS_LEGACY,
    DECISION_EVIDENCE_STATUS_PRESENT,
    NO_MATERIAL_DOWNSIDE,
    TRIPLE_REQUIRED_TYPES,
    UNKEYED_OPTION,
    DecisionEvidenceError,
    DecisionEvidenceRef,
    DecisionEvidenceTriple,
    DecisionOptionOutcome,
    enforce_decision_evidence,
    evidence_triple_problems,
    export_decision_evidence,
)
from packages.orchestration.decision_queue import (
    HumanDecision,
    export_decision_json,
    list_decisions,
)

OPTIONS = ["postgres", "sqlite"]


def _ref(
    kind: str = "file",
    target: str = "packages/orchestration/decision_queue.py:120",
    label: str = "the derivation point",
) -> DecisionEvidenceRef:
    return DecisionEvidenceRef(kind=kind, target=target, label=label)


def _outcome(
    option: str = "postgres",
    expected_outcome: str = "the queue keeps its rows across a restart",
    downside: str = "one more service to run in development",
) -> DecisionOptionOutcome:
    return DecisionOptionOutcome(
        option=option,
        expected_outcome=expected_outcome,
        downside=downside,
    )


def _sqlite_outcome() -> DecisionOptionOutcome:
    return _outcome(
        option="sqlite",
        expected_outcome="the queue runs with no extra process",
        downside="concurrent writers block each other",
    )


def _triple(refs, outcomes) -> DecisionEvidenceTriple:
    return DecisionEvidenceTriple(refs=tuple(refs), outcomes=tuple(outcomes))


# ---------------------------------------------------------------------------
# The accepting cases — these are what keep the rules below from over-firing
# ---------------------------------------------------------------------------


def test_a_complete_triple_with_options_has_no_problems():
    triple = _triple([_ref()], [_outcome(), _sqlite_outcome()])
    assert evidence_triple_problems(triple, options=OPTIONS) == []


def test_a_complete_triple_with_no_options_has_no_problems():
    triple = _triple([_ref()], [_outcome(option=UNKEYED_OPTION)])
    assert evidence_triple_problems(triple, options=[]) == []


def test_no_material_downside_is_accepted_as_a_downside():
    """The discriminator that keeps rule (f) from swallowing the benign case.

    ``docs/roadmap/features/T5_F032.md:78-80`` permits this literal by name, so
    a denylist that caught it would punish the one honest way to report that a
    choice costs nothing.
    """
    triple = _triple(
        [_ref()],
        [_outcome(downside=NO_MATERIAL_DOWNSIDE), _sqlite_outcome()],
    )
    assert evidence_triple_problems(triple, options=OPTIONS) == []


# ---------------------------------------------------------------------------
# (a) through (h) — one rule per test, each pinned to its own sentence
# ---------------------------------------------------------------------------


def test_a_triple_with_no_refs_is_refused():
    triple = _triple([], [_outcome(), _sqlite_outcome()])
    assert evidence_triple_problems(triple, options=OPTIONS) == [
        "evidence_refs is empty: a decision must cite at least one ref."
    ]


def test_a_ref_kind_outside_the_vocabulary_is_refused():
    triple = _triple([_ref(kind="screenshot")], [_outcome(), _sqlite_outcome()])
    assert evidence_triple_problems(triple, options=OPTIONS) == [
        "evidence ref 0 has kind 'screenshot', which is not one of "
        "coverage, decision, failure, file."
    ]


def test_a_ref_with_a_blank_target_is_refused():
    triple = _triple([_ref(target="   ")], [_outcome(), _sqlite_outcome()])
    assert evidence_triple_problems(triple, options=OPTIONS) == [
        "evidence ref 0 has an empty target and points at nothing."
    ]


def test_an_outcome_with_a_blank_expected_outcome_is_refused():
    triple = _triple(
        [_ref()],
        [_outcome(expected_outcome="  "), _sqlite_outcome()],
    )
    assert evidence_triple_problems(triple, options=OPTIONS) == [
        "outcome for option 'postgres' has an empty expected_outcome."
    ]


def test_an_outcome_with_a_blank_downside_is_refused():
    triple = _triple([_ref()], [_outcome(downside=""), _sqlite_outcome()])
    assert evidence_triple_problems(triple, options=OPTIONS) == [
        "outcome for option 'postgres' has an empty downside."
    ]


def test_a_boilerplate_phrase_is_refused_case_insensitively():
    triple = _triple(
        [_ref()],
        [_outcome(expected_outcome=" TBD "), _sqlite_outcome()],
    )
    assert evidence_triple_problems(triple, options=OPTIONS) == [
        "outcome for option 'postgres' has the boilerplate "
        "expected_outcome ' TBD '."
    ]


def test_an_option_with_no_outcome_is_refused():
    triple = _triple([_ref()], [_outcome()])
    assert evidence_triple_problems(triple, options=OPTIONS) == [
        "no outcome is given for option 'sqlite'."
    ]


def test_an_outcome_for_an_unoffered_option_is_refused():
    triple = _triple(
        [_ref()],
        [_outcome(), _sqlite_outcome(), _outcome(option="mysql")],
    )
    assert evidence_triple_problems(triple, options=OPTIONS) == [
        "outcome names option 'mysql', which this decision does not offer."
    ]


def test_an_optionless_decision_must_carry_exactly_one_outcome():
    second = _outcome(
        option=UNKEYED_OPTION,
        expected_outcome="a second answer to a question with one answer",
        downside="the reader cannot tell which one was chosen",
    )
    triple = _triple([_ref()], [_outcome(option=UNKEYED_OPTION), second])
    assert evidence_triple_problems(triple, options=[]) == [
        "a decision with no options must carry exactly one outcome, "
        "but it carries 2."
    ]


def test_an_optionless_decision_keys_its_outcome_as_unkeyed():
    triple = _triple([_ref()], [_outcome(option="postgres")])
    assert evidence_triple_problems(triple, options=[]) == [
        "a decision with no options must key its outcome as UNKEYED_OPTION, "
        "but it uses 'postgres'."
    ]


def test_a_malformed_triple_produces_problems_rather_than_raising():
    """T001b calls this on every card, so a raise here would lose the decision."""

    class _NotATriple:
        refs = None
        outcomes = "postgres"

    problems = evidence_triple_problems(_NotATriple(), options=[])
    assert "evidence_refs is empty: a decision must cite at least one ref." in problems
    assert (
        "a decision with no options must carry exactly one outcome, "
        "but it carries 0." in problems
    )


# ---------------------------------------------------------------------------
# The wire form
# ---------------------------------------------------------------------------


def test_export_round_trips_every_field_under_exactly_two_keys():
    triple = _triple(
        [_ref(kind="failure", target="pytest::test_x", label="the red run")],
        [_outcome(), _sqlite_outcome()],
    )
    wire = export_decision_evidence(triple)

    assert sorted(wire) == ["evidence_refs", "outcomes"]
    assert wire["evidence_refs"] == [
        {"kind": "failure", "target": "pytest::test_x", "label": "the red run"}
    ]
    assert wire["outcomes"] == [
        {
            "option": "postgres",
            "expected_outcome": "the queue keeps its rows across a restart",
            "downside": "one more service to run in development",
        },
        {
            "option": "sqlite",
            "expected_outcome": "the queue runs with no extra process",
            "downside": "concurrent writers block each other",
        },
    ]


# ---------------------------------------------------------------------------
# The emit gate (F032 T001b) — opt-in per type, and the opt-in set starts EMPTY
# ---------------------------------------------------------------------------

#: The decision type that exists ONLY for the canary below.  It is never added
#: to the shipped ``TRIPLE_REQUIRED_TYPES``; each test that needs it enforced
#: patches the module constant for its own duration, so the gate is proven live
#: without any producer being opted in.
CANARY_TYPE = "canary_producer"


def _decision(
    decision_id: str = "canary:1",
    decision_type: str = CANARY_TYPE,
    evidence: DecisionEvidenceTriple | None = None,
    payload: dict | None = None,
) -> HumanDecision:
    return HumanDecision(
        id=decision_id,
        type=decision_type,
        status="open",
        severity="blocker",
        source="test",
        related_node_id="",
        related_intent_id="",
        related_file="",
        safe_summary="A decision raised by the canary producer.",
        next_actions=(),
        created_at="",
        resolved_at=None,
        payload=payload or {},
        evidence=evidence,
    )


def test_the_shipped_required_type_set_is_empty():
    """The whole safety argument of T001b in one assertion.

    A type joins this set in T002, in the same commit that gives its producer a
    real triple.  If this test goes red because a type was added without that
    commit, every job carrying that type starts raising.
    """
    assert TRIPLE_REQUIRED_TYPES == frozenset()


def test_an_unenforced_tripleless_decision_is_left_alone():
    """No existing producer changes behaviour: none of their types is enforced."""
    decision = _decision(decision_type="memory_review", evidence=None)
    assert enforce_decision_evidence([decision]) is None


def test_the_canary_producer_missing_a_field_is_refused(monkeypatch):
    """THE CANARY: an enforced type that omits a downside fails, by name.

    The message must carry the decision id and the problem sentence for the
    field that is actually missing — an error that only said "invalid triple"
    would leave the producer's author guessing which of six rules fired.
    """
    monkeypatch.setattr(
        decision_evidence, "TRIPLE_REQUIRED_TYPES", frozenset({CANARY_TYPE})
    )
    decision = _decision(
        decision_id="canary:missing-downside",
        evidence=_triple([_ref()], [_outcome(downside=""), _sqlite_outcome()]),
        payload={"options": OPTIONS},
    )

    with pytest.raises(DecisionEvidenceError) as excinfo:
        enforce_decision_evidence([decision])

    message = str(excinfo.value)
    assert "canary:missing-downside" in message
    assert CANARY_TYPE in message
    assert "outcome for option 'postgres' has an empty downside." in message


def test_an_enforced_decision_with_a_complete_triple_raises_nothing(monkeypatch):
    monkeypatch.setattr(
        decision_evidence, "TRIPLE_REQUIRED_TYPES", frozenset({CANARY_TYPE})
    )
    decision = _decision(
        evidence=_triple([_ref()], [_outcome(), _sqlite_outcome()]),
        payload={"options": OPTIONS},
    )
    assert enforce_decision_evidence([decision]) is None


def test_an_enforced_optionless_decision_reads_no_options_from_the_payload(
    monkeypatch,
):
    """A payload with no ``options`` key is the six-branch case (DECISION F032 D3)."""
    monkeypatch.setattr(
        decision_evidence, "TRIPLE_REQUIRED_TYPES", frozenset({CANARY_TYPE})
    )
    decision = _decision(
        evidence=_triple(
            [_ref()],
            [_outcome(option=UNKEYED_OPTION, downside=NO_MATERIAL_DOWNSIDE)],
        ),
    )
    assert enforce_decision_evidence([decision]) is None


# ---------------------------------------------------------------------------
# The legacy rendering — always present, always empty, never fabricated
# ---------------------------------------------------------------------------


def test_a_tripleless_decision_exports_empty_lists_and_the_legacy_status():
    wire = export_decision_json(_decision(decision_type="memory_review"))

    assert wire["evidence_refs"] == []
    assert wire["outcomes"] == []
    assert wire["evidence_status"] == "recorded_before_evidence_requirements"
    assert wire["evidence_status"] == DECISION_EVIDENCE_STATUS_LEGACY


def test_a_decision_with_a_triple_exports_the_present_status_and_the_real_refs():
    decision = _decision(
        evidence=_triple(
            [_ref(kind="failure", target="pytest::test_x", label="the red run")],
            [_outcome(option=UNKEYED_OPTION)],
        ),
    )
    wire = export_decision_json(decision)

    assert wire["evidence_status"] == "present"
    assert wire["evidence_status"] == DECISION_EVIDENCE_STATUS_PRESENT
    assert wire["evidence_refs"] == [
        {"kind": "failure", "target": "pytest::test_x", "label": "the red run"}
    ]
    assert wire["outcomes"] == [
        {
            "option": UNKEYED_OPTION,
            "expected_outcome": "the queue keeps its rows across a restart",
            "downside": "one more service to run in development",
        }
    ]


# ---------------------------------------------------------------------------
# R-0710 — `validity` and `review_status` are two fields, not one
# ---------------------------------------------------------------------------


class _StubJob:
    """The least a job can be and still reach the memory branch of the queue."""

    job_id = "0123456789abcdef"


def _memory_review_decisions(monkeypatch, entry: MemoryEntry) -> list[HumanDecision]:
    monkeypatch.setattr(local_gateway, "list_memory", lambda *a, **k: [entry])
    return [d for d in list_decisions(_StubJob(), []) if d.type == "memory_review"]


def test_a_stale_memory_card_raises_a_memory_review_decision(monkeypatch):
    entry = MemoryEntry(key="deploy-target", validity="stale")
    decisions = _memory_review_decisions(monkeypatch, entry)

    assert [d.id for d in decisions] == ["mem:deploy-target"]


def test_a_needs_review_memory_card_raises_a_memory_review_decision(monkeypatch):
    """The half of the predicate that was dead before R-0710's fix.

    ``needs_review`` is a value of ``review_status``
    (``packages/memory/models.py:45``) and never of ``validity`` (``:44``), so a
    test over the stale card alone would have stayed green while this case
    selected nothing.
    """
    entry = MemoryEntry(key="api-contract", review_status="needs_review")
    decisions = _memory_review_decisions(monkeypatch, entry)

    assert [d.id for d in decisions] == ["mem:api-contract"]
