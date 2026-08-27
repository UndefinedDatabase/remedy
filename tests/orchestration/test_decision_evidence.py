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

from packages.core.models import Artifact, Job
from packages.memory import local_gateway
from packages.memory.models import MemoryEntry
from packages.orchestration import decision_evidence, stop_reasons
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
from packages.orchestration.stop_reasons import StopReason

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


def test_the_shipped_required_type_set_holds_exactly_the_upgraded_producers():
    """The whole safety argument of the opt-in set in one assertion.

    A type joins this set in T002, in the same commit that gives its producer a
    real triple.  If this test goes red because a type was added without that
    commit, every job carrying that type starts raising.  It is pinned to EXACT
    membership rather than to containment, so adding a type ahead of its
    producer's upgrade fails here first.
    """
    assert TRIPLE_REQUIRED_TYPES == frozenset({
        "token_budget", "test_failure", "patch_approval", "stop_reason",
        "repo_dirty", "memory_review",
    })


def test_an_unenforced_tripleless_decision_is_left_alone():
    """An UNENFORCED type is not read, not validated and not altered.

    ``flight_plan_approval`` is the example because it is still outside
    ``TRIPLE_REQUIRED_TYPES`` after T002e.  ``memory_review`` stood here until
    that slice enforced it, which is why this guard is repointed rather than
    deleted: the behaviour it pins is the gate's opt-in, not the type's.
    """
    decision = _decision(decision_type="flight_plan_approval", evidence=None)
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
    """A payload with no ``options`` key is the five-branch case (DECISION F032 D3)."""
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
    wire = export_decision_json(_decision(decision_type="flight_plan_approval"))

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


# ---------------------------------------------------------------------------
# R-0711 — the card states WHY it is in the inbox, not whether it is valid
# ---------------------------------------------------------------------------


def test_a_stale_only_card_reads_as_stale(monkeypatch):
    entry = MemoryEntry(key="deploy-target", validity="stale")
    decisions = _memory_review_decisions(monkeypatch, entry)

    assert [d.safe_summary for d in decisions] == [
        "Memory 'deploy-target' is stale."
    ]


def test_a_flagged_only_card_reads_as_flagged_and_never_as_active(monkeypatch):
    """The half R-0710 surfaced, rendering the one fact that explains nothing.

    ``review_status`` and ``validity`` are independent fields, so a card flagged
    for review normally still carries ``validity`` ``active``.  A summary built
    from the validity therefore told the human that a card raised FOR REVIEW is
    active -- true, and silent about why anyone should look at it.
    """
    entry = MemoryEntry(key="api-contract", review_status="needs_review")
    assert entry.validity == "active"

    decisions = _memory_review_decisions(monkeypatch, entry)

    assert [d.safe_summary for d in decisions] == [
        "Memory 'api-contract' is flagged for review."
    ]
    assert "active" not in decisions[0].safe_summary


def test_a_stale_and_flagged_card_names_both_reasons(monkeypatch):
    entry = MemoryEntry(
        key="db-dsn", validity="stale", review_status="needs_review")
    decisions = _memory_review_decisions(monkeypatch, entry)

    assert [d.safe_summary for d in decisions] == [
        "Memory 'db-dsn' is stale and flagged for review."
    ]


# ---------------------------------------------------------------------------
# F032 T002a — the budget stop, the first producer with a real triple
#
# These drive the REAL branch through `list_decisions` rather than constructing
# a `HumanDecision` by hand: the point of the round is that the SHIPPED producer
# emits the triple, and a hand-built card would pass while the producer stayed
# tripleless.  They assert the RENDERED strings, because the triple's value to a
# human is its wording and a shape-only assertion stays green on filler.
# ---------------------------------------------------------------------------

#: The two downsides do not vary with what the stop event carried, so they are
#: written once and pinned in both cases.
EXTEND_DOWNSIDE = (
    "Spend continues past the ceiling that was set, and the same stop recurs "
    "if the run is not converging."
)
ABANDON_DOWNSIDE = (
    "The work in flight is left unfinished, and a later resume pays again for "
    "the context this run had built."
)


def _budget_events(
    reason: str,
    exhausted_limit: str | None = None,
    request_id: str | None = None,
) -> list[dict]:
    """One `job_stopped` event from the budget guard, as the branch reads it."""
    metadata: dict = {"source": "budget", "reason": reason}
    if exhausted_limit is not None:
        metadata["exhausted_limit"] = exhausted_limit
    if request_id is not None:
        metadata["request_id"] = request_id
    return [{
        "event": "job_stopped",
        "timestamp": "2026-08-27T10:00:00Z",
        "metadata": metadata,
    }]


def _budget_decision(events: list[dict]) -> HumanDecision:
    decisions = [d for d in list_decisions(_StubJob(), events)
                 if d.type == "token_budget"]
    assert len(decisions) == 1
    return decisions[0]


def test_the_budget_stop_cites_the_reason_the_limit_and_the_request():
    decision = _budget_decision(_budget_events(
        "budget_exhausted: 120000 of 100000 tokens",
        exhausted_limit="100000",
        request_id="req-7f3a",
    ))

    assert [(r.kind, r.target) for r in decision.evidence.refs] == [
        ("failure", "budget_exhausted: 120000 of 100000 tokens"),
        ("failure", "100000"),
        ("decision", "req-7f3a"),
    ]
    assert [r.label for r in decision.evidence.refs] == [
        "the stop reason the budget guard recorded",
        "the budget limit that was exhausted",
        "the request in flight when the budget was exhausted",
    ]


def test_the_budget_stop_keys_one_outcome_to_each_choice_and_names_the_limit():
    decision = _budget_decision(_budget_events(
        "budget_exhausted: 120000 of 100000 tokens",
        exhausted_limit="100000",
        request_id="req-7f3a",
    ))

    assert [(o.option, o.expected_outcome, o.downside)
            for o in decision.evidence.outcomes] == [
        (
            "extend",
            "The job resumes from its last safe point with the exhausted "
            "limit of 100000 raised, and the work already paid for is kept.",
            EXTEND_DOWNSIDE,
        ),
        (
            "abandon",
            "The job stops with the artifacts it has, and nothing further is "
            "spent against the exhausted limit of 100000.",
            ABANDON_DOWNSIDE,
        ),
    ]


def test_the_budget_stop_states_its_options_where_the_gate_reads_them():
    """DECISION F032 D6: the gate reads options from `payload`, not `next_actions`."""
    decision = _budget_decision(_budget_events(
        "budget_exhausted: 120000 of 100000 tokens",
        exhausted_limit="100000",
        request_id="req-7f3a",
    ))

    assert decision.payload == {"options": ["extend", "abandon"]}
    assert decision.next_actions == ("extend", "abandon")


def test_the_budget_stop_exports_the_present_status_not_the_legacy_literal():
    decision = _budget_decision(_budget_events(
        "budget_exhausted: 120000 of 100000 tokens",
        exhausted_limit="100000",
        request_id="req-7f3a",
    ))
    wire = export_decision_json(decision)

    assert wire["evidence_status"] == DECISION_EVIDENCE_STATUS_PRESENT
    assert wire["evidence_status"] != DECISION_EVIDENCE_STATUS_LEGACY
    assert wire["evidence_refs"] != []
    assert [o["option"] for o in wire["outcomes"]] == ["extend", "abandon"]


def test_a_budget_stop_with_only_a_reason_drops_the_refs_it_cannot_fill():
    """The optional two refs are OMITTED, never emitted with an empty target.

    Rule (c) of `evidence_triple_problems` refuses a ref pointing at nothing, so
    a branch that emitted all three unconditionally would raise at the emit gate
    whenever the stop event carried no `exhausted_limit`.
    """
    decision = _budget_decision(
        _budget_events("budget_exhausted: the run passed its ceiling"))

    assert [(r.kind, r.target) for r in decision.evidence.refs] == [
        ("failure", "budget_exhausted: the run passed its ceiling"),
    ]


def test_a_budget_stop_with_only_a_reason_still_names_a_limit_in_english():
    """The fallback is a whole noun phrase, so neither sentence reads as a splice."""
    decision = _budget_decision(
        _budget_events("budget_exhausted: the run passed its ceiling"))

    assert [(o.option, o.expected_outcome, o.downside)
            for o in decision.evidence.outcomes] == [
        (
            "extend",
            "The job resumes from its last safe point with the exhausted "
            "limit raised, and the work already paid for is kept.",
            EXTEND_DOWNSIDE,
        ),
        (
            "abandon",
            "The job stops with the artifacts it has, and nothing further is "
            "spent against the exhausted limit.",
            ABANDON_DOWNSIDE,
        ),
    ]


@pytest.mark.parametrize(
    "events",
    [
        _budget_events(
            "budget_exhausted: 120000 of 100000 tokens",
            exhausted_limit="100000",
            request_id="req-7f3a",
        ),
        _budget_events("budget_exhausted: the run passed its ceiling"),
    ],
    ids=["all-three-present", "reason-only"],
)
def test_no_budget_ref_ever_points_at_nothing(events):
    decision = _budget_decision(events)

    assert decision.evidence.refs
    assert [r for r in decision.evidence.refs if not r.target.strip()] == []


def test_a_token_budget_decision_without_a_triple_is_refused_by_the_gate():
    """`token_budget` is ENFORCED now, so a regression that drops the triple raises."""
    decision = _decision(
        decision_id="budget:regression",
        decision_type="token_budget",
        evidence=None,
        payload={"options": ["extend", "abandon"]},
    )

    with pytest.raises(DecisionEvidenceError) as excinfo:
        enforce_decision_evidence([decision])

    message = str(excinfo.value)
    assert "budget:regression" in message
    assert "token_budget" in message
    assert "evidence_refs is empty: a decision must cite at least one ref." in message


# ---------------------------------------------------------------------------
# F032 T002b — the test-failure card, and R-0712, the key it reads
#
# These drive the REAL branch through `list_decisions` from the event the test
# runner actually emits, for the same reason the budget tests above do: a
# hand-built card would pass while the shipped producer stayed wrong.  R-0712
# was exactly that failure — the branch read a key no producer writes and the
# only guard over the card asserted that it APPEARED.
# ---------------------------------------------------------------------------

#: Neither half of the one unkeyed outcome varies with what the event carried,
#: so both are written once and pinned wherever the outcome is asserted.
TEST_FAILURE_EXPECTED_OUTCOME = (
    "Reading the named run's output shows which assertion failed, so the "
    "repair targets the real cause instead of a guess."
)
TEST_FAILURE_DOWNSIDE = (
    "The job stays blocked while that output is read, and a failure caused by "
    "the environment rather than by the change spends that time for nothing."
)


def _test_failure_decision(metadata: dict) -> HumanDecision:
    """The card the real branch builds from one failed `test_run_completed`."""
    events = [{
        "event": "test_run_completed",
        "timestamp": "2026-08-27T11:00:00Z",
        "metadata": dict(metadata, status="failed"),
    }]
    decisions = [d for d in list_decisions(_StubJob(), events)
                 if d.type == "test_failure"]
    assert len(decisions) == 1
    return decisions[0]


def test_the_test_failure_card_names_the_command_its_emitter_writes():
    """R-0712: `test_execution_service` writes `command_safe`, never `command`."""
    decision = _test_failure_decision({
        "command_safe": "pytest tests/orchestration -q",
        "test_run_id": "run-abc-123",
    })

    assert decision.safe_summary == "Test 'pytest tests/orchestration -q' failed."


def test_the_test_failure_card_still_reads_the_older_command_key():
    """The fallback is not dead code: the inbox guard's own fixture writes it."""
    decision = _test_failure_decision({
        "command": "pytest -q",
        "test_run_id": "run-def-456",
    })

    assert decision.safe_summary == "Test 'pytest -q' failed."


def test_the_test_failure_card_reads_command_safe_first_never_command():
    """THE R-0712 PIN: an event carrying BOTH keys must render the emitter's.

    Every other test here would stay green if the branch went back to reading
    `command` first, because no other event carries both keys.  This one is the
    discriminator: it fails, and only it fails, on that exact regression.
    """
    decision = _test_failure_decision({
        "command_safe": "pytest tests/orchestration/test_decision_evidence.py -q",
        "command": "the key no producer writes",
        "test_run_id": "run-ghi-789",
    })

    assert decision.safe_summary == (
        "Test 'pytest tests/orchestration/test_decision_evidence.py -q' failed.")
    assert "the key no producer writes" not in decision.safe_summary


def test_a_test_failure_card_with_no_command_at_all_stays_honest():
    """The placeholder is correct here and wrong everywhere else."""
    decision = _test_failure_decision({"test_run_id": "run-jkl-012"})

    assert decision.safe_summary == "Test '?' failed."


def test_the_test_failure_card_cites_the_run_and_the_command():
    decision = _test_failure_decision({
        "command_safe": "pytest tests/orchestration -q",
        "test_run_id": "run-abc-123",
    })

    assert [(r.kind, r.target) for r in decision.evidence.refs] == [
        ("failure", "run-abc-123"),
        ("failure", "pytest tests/orchestration -q"),
    ]
    assert [r.label for r in decision.evidence.refs] == [
        "the test run that failed",
        "the command that was run",
    ]


def test_the_test_failure_card_omits_the_command_ref_it_cannot_fill():
    """A ref to the `?` placeholder would cite a question mark as a command."""
    decision = _test_failure_decision({"test_run_id": "run-jkl-012"})

    assert [(r.kind, r.target) for r in decision.evidence.refs] == [
        ("failure", "run-jkl-012"),
    ]


def test_the_test_failure_card_cites_the_unknown_run_rather_than_nothing():
    """The id's own default is honest; an empty target rule (c) would refuse."""
    decision = _test_failure_decision({"command_safe": "pytest -q"})

    assert decision.id == "tf:unknown"
    assert [(r.kind, r.target) for r in decision.evidence.refs] == [
        ("failure", "unknown"),
        ("failure", "pytest -q"),
    ]
    assert [r for r in decision.evidence.refs if not r.target.strip()] == []


def test_the_test_failure_card_carries_exactly_one_unkeyed_outcome():
    """This branch offers no options, so DECISION F032 D3's rule (h) applies."""
    decision = _test_failure_decision({
        "command_safe": "pytest tests/orchestration -q",
        "test_run_id": "run-abc-123",
    })

    assert decision.payload == {}
    assert [(o.option, o.expected_outcome, o.downside)
            for o in decision.evidence.outcomes] == [
        (UNKEYED_OPTION, TEST_FAILURE_EXPECTED_OUTCOME, TEST_FAILURE_DOWNSIDE),
    ]


def test_the_test_failure_card_exports_the_present_status():
    decision = _test_failure_decision({
        "command_safe": "pytest tests/orchestration -q",
        "test_run_id": "run-abc-123",
    })
    wire = export_decision_json(decision)

    assert wire["evidence_status"] == "present"
    assert wire["evidence_status"] == DECISION_EVIDENCE_STATUS_PRESENT
    assert wire["evidence_status"] != DECISION_EVIDENCE_STATUS_LEGACY


def test_a_test_failure_decision_without_a_triple_is_refused_by_the_gate():
    """`test_failure` is ENFORCED from this round, so a dropped triple raises."""
    decision = _decision(
        decision_id="tf:regression",
        decision_type="test_failure",
        evidence=None,
    )

    with pytest.raises(DecisionEvidenceError) as excinfo:
        enforce_decision_evidence([decision])

    message = str(excinfo.value)
    assert "tf:regression" in message
    assert "test_failure" in message
    assert "evidence_refs is empty: a decision must cite at least one ref." in message


# ---------------------------------------------------------------------------
# F032 T002c — the patch-approval card, the richest evidence in the queue
#
# These drive the REAL branch through `list_decisions` from a job built the way
# `approval_queue.list_patch_intents` requires — an `Artifact` whose metadata
# carries `patch_intent_explanations` — for the same reason the budget and
# test-failure tests above do: a hand-built card would pass while the shipped
# producer stayed wrong.
# ---------------------------------------------------------------------------

#: Neither half of the one unkeyed outcome varies with what the intent carried,
#: so both are written once and pinned wherever the outcome is asserted.
PATCH_APPROVAL_EXPECTED_OUTCOME = (
    "The named file's pending change is settled either way: approving applies "
    "the patch and unblocks the task that produced it, while rejecting leaves "
    "the working tree untouched."
)
PATCH_APPROVAL_DOWNSIDE = (
    "The judgement is made from the intent's summary and target path rather "
    "than from the applied diff, so a patch that is wrong in a way the summary "
    "does not reveal is approved as easily as a correct one."
)


def _patch_approval_decision(explanation: dict) -> HumanDecision:
    """The card the real branch builds from one pending patch intent."""
    artifact = Artifact(
        name="patch",
        content="",
        metadata={"patch_intent_explanations": [explanation]},
    )
    job = Job(
        name="f032-t002c-job",
        user_prompt="Drive the patch-approval branch",
        tasks=[],
        artifacts=[artifact],
        metadata={"target_repo": "/tmp/repo"},
    )
    decisions = [d for d in list_decisions(job, []) if d.type == "patch_approval"]
    assert len(decisions) == 1
    return decisions[0]


def _named_target_explanation() -> dict:
    return {
        "file": "README.md",
        "action": "modify",
        "risk": "low",
        "reason": "docs",
        "summary": "touch the readme",
    }


def _no_target_explanation() -> dict:
    """The same intent with NO `file` key — `target_path` comes back empty."""
    return {
        "action": "preview-only",
        "risk": "unknown",
        "reason": "no path could be derived",
        "summary": "a patch whose target was never resolved",
    }


def test_the_patch_approval_card_cites_the_intent_and_the_file():
    decision = _patch_approval_decision(_named_target_explanation())

    assert [(r.kind, r.target, r.label) for r in decision.evidence.refs] == [
        ("decision", decision.related_intent_id,
         "the patch intent awaiting approval"),
        ("file", "README.md", "the file this patch would change"),
    ]


def test_the_patch_approval_card_omits_the_file_ref_when_no_path_was_named():
    """PINS THE CONDITIONAL: made unconditional, this ref targets the empty
    string, which rule (c) of ``evidence_triple_problems`` refuses outright.
    """
    decision = _patch_approval_decision(_no_target_explanation())

    assert [(r.kind, r.target, r.label) for r in decision.evidence.refs] == [
        ("decision", decision.related_intent_id,
         "the patch intent awaiting approval"),
    ]


@pytest.mark.parametrize(
    "explanation",
    [_named_target_explanation(), _no_target_explanation()],
    ids=["target-named", "no-target"],
)
def test_no_patch_approval_ref_ever_points_at_nothing(explanation):
    decision = _patch_approval_decision(explanation)

    assert decision.evidence.refs
    assert all(r.target for r in decision.evidence.refs)
    assert evidence_triple_problems(decision.evidence, options=[]) == []


@pytest.mark.parametrize(
    "explanation",
    [_named_target_explanation(), _no_target_explanation()],
    ids=["target-named", "no-target"],
)
def test_the_patch_approval_card_carries_exactly_one_unkeyed_outcome(explanation):
    """DECISION F032 D3 rule (h): this branch offers no options at all.

    Its ``next_actions`` are two ``remedy patch`` command lines rather than two
    option words, and amendment A3 puts growing an options list out of scope, so
    the card keeps an EMPTY payload and owes one outcome for the decision.
    """
    decision = _patch_approval_decision(explanation)

    assert decision.payload == {}
    assert [(o.option, o.expected_outcome, o.downside)
            for o in decision.evidence.outcomes] == [
        (UNKEYED_OPTION, PATCH_APPROVAL_EXPECTED_OUTCOME, PATCH_APPROVAL_DOWNSIDE),
    ]


@pytest.mark.parametrize(
    "explanation",
    [_named_target_explanation(), _no_target_explanation()],
    ids=["target-named", "no-target"],
)
def test_the_patch_approval_card_exports_the_present_status(explanation):
    wire = export_decision_json(_patch_approval_decision(explanation))

    assert wire["evidence_status"] == "present"
    assert wire["evidence_status"] == DECISION_EVIDENCE_STATUS_PRESENT
    assert wire["evidence_status"] != DECISION_EVIDENCE_STATUS_LEGACY


def test_a_patch_approval_decision_without_a_triple_is_refused_by_the_gate():
    """`patch_approval` is ENFORCED from this round, so a dropped triple raises."""
    decision = _decision(
        decision_id="pa:regression",
        decision_type="patch_approval",
        evidence=None,
    )

    with pytest.raises(DecisionEvidenceError) as excinfo:
        enforce_decision_evidence([decision])

    message = str(excinfo.value)
    assert "pa:regression" in message
    assert "patch_approval" in message
    assert "evidence_refs is empty: a decision must cite at least one ref." in message


# ---------------------------------------------------------------------------
# R-0713 — the patch-approval summary's placeholder, which could never fire
#
# `list_patch_intents` ALWAYS sets `target_path`, to the empty string when the
# explanation named no `file`, so the key is present-and-empty and the old
# `pi.get('target_path', '?')` default was unreachable.  Both cases are pinned
# below: the summary is the only half of the card R-0713 touched, so the
# no-file case is asserted on the RENDERED sentence rather than on the value it
# was built from.
# ---------------------------------------------------------------------------


def test_the_patch_approval_summary_shows_the_placeholder_and_not_an_empty_gap():
    """FAILS IF THE FIX IS REVERTED to ``pi.get('target_path', '?')``.

    With that form the card rendered ``Patch intent for  awaits approval.`` —
    two spaces and no subject — because the default only fires on an ABSENT
    key and this key is present-and-empty.
    """
    decision = _patch_approval_decision(_no_target_explanation())

    assert decision.safe_summary == "Patch intent for ? awaits approval."


def test_the_patch_approval_summary_still_names_the_file_when_there_is_one():
    """The discriminator: the case that already worked must keep working."""
    decision = _patch_approval_decision(_named_target_explanation())

    assert decision.safe_summary == "Patch intent for README.md awaits approval."


# ---------------------------------------------------------------------------
# F032 T002d — the stop-reason card, which copied a record and cited none of it
#
# These drive the REAL branch through `list_decisions`.  The no-target-repo
# case comes from `derive_stop_reasons` itself and has an EMPTY `related_file`,
# which is what makes the file ref's guard load-bearing; the related-file case
# substitutes the record source the same way the memory-review tests above
# substitute `local_gateway.list_memory`, because no derived arm sets that
# field and the branch under test is the queue's, not the deriver's.
# ---------------------------------------------------------------------------

#: Neither half of the one unkeyed outcome varies with the record, so both are
#: written once and pinned wherever the outcome is asserted.
STOP_REASON_EXPECTED_OUTCOME = (
    "Clearing the named blocker lets the run continue from where it stopped, "
    "with the work already done still in place."
)
STOP_REASON_DOWNSIDE = (
    "Until it is cleared the run makes no further progress, and a blocker "
    "cleared without understanding why it fired can fire again."
)


def _no_repo_stop_decision() -> HumanDecision:
    """The card the real branch builds from the derived no-target-repo stop."""
    job = Job(
        name="f032-t002d-job",
        user_prompt="Drive the stop-reason branch",
        tasks=[],
        metadata={},
    )
    decisions = [d for d in list_decisions(job, []) if d.type == "stop_reason"]
    assert len(decisions) == 1
    return decisions[0]


def _stop_record_naming_a_file() -> StopReason:
    return StopReason(
        id="derived_dirty_repo",
        job_id="0123456789abcdef",
        source="git_status",
        reason_code="dirty_repo_blocks_level",
        severity="warning",
        status="active",
        created_at="2026-08-28T00:00:00+00:00",
        resolved_at=None,
        related_node_id="",
        related_intent_id="",
        related_file="packages/core/models.py",
        safe_summary="Target repository has uncommitted changes.",
        next_actions=("Commit or stash changes in target repo.",),
    )


def _related_file_stop_decision(monkeypatch) -> HumanDecision:
    monkeypatch.setattr(
        stop_reasons,
        "derive_stop_reasons",
        lambda job, events: [_stop_record_naming_a_file()],
    )
    decisions = [d for d in list_decisions(_StubJob(), []) if d.type == "stop_reason"]
    assert len(decisions) == 1
    return decisions[0]


def test_the_stop_reason_card_cites_the_record_and_its_reason_code():
    """PINS THE CONDITIONAL: this record's ``related_file`` is EMPTY.

    Made unconditional, the file ref of T002d would appear here targeting the
    empty string, which rule (c) of ``evidence_triple_problems`` refuses
    outright — and `_fixture_stop_reason` in the decision-inbox guard drives
    exactly this record, so the whole inbox would raise instead of rendering.
    """
    decision = _no_repo_stop_decision()

    assert decision.id == "sr:derived_no_repo"
    assert [(r.kind, r.target, r.label) for r in decision.evidence.refs] == [
        ("failure", "derived_no_repo",
         "the stop record that raised this decision"),
        ("failure", "no_target_repo", "the reason code the run recorded"),
    ]


def test_the_stop_reason_card_cites_the_file_when_the_record_names_one(monkeypatch):
    decision = _related_file_stop_decision(monkeypatch)

    assert [(r.kind, r.target, r.label) for r in decision.evidence.refs] == [
        ("failure", "derived_dirty_repo",
         "the stop record that raised this decision"),
        ("failure", "dirty_repo_blocks_level",
         "the reason code the run recorded"),
        ("file", "packages/core/models.py", "the file this stop is about"),
    ]


def test_no_stop_reason_ref_ever_points_at_nothing(monkeypatch):
    for decision in (_no_repo_stop_decision(), _related_file_stop_decision(monkeypatch)):
        assert decision.evidence.refs
        assert all(r.target for r in decision.evidence.refs)
        assert evidence_triple_problems(decision.evidence, options=[]) == []


def test_the_stop_reason_card_carries_exactly_one_unkeyed_outcome(monkeypatch):
    """DECISION F032 D3 rule (h): this branch offers no options at all.

    It copies the record's own ``next_actions``, which are command lines rather
    than option words, and amendment A3 puts growing an options list out of
    scope, so the card keeps an EMPTY payload and owes one outcome.
    """
    for decision in (_no_repo_stop_decision(), _related_file_stop_decision(monkeypatch)):
        assert decision.payload == {}
        assert [(o.option, o.expected_outcome, o.downside)
                for o in decision.evidence.outcomes] == [
            (UNKEYED_OPTION, STOP_REASON_EXPECTED_OUTCOME, STOP_REASON_DOWNSIDE),
        ]


def test_the_stop_reason_card_exports_the_present_status(monkeypatch):
    for decision in (_no_repo_stop_decision(), _related_file_stop_decision(monkeypatch)):
        wire = export_decision_json(decision)
        assert wire["evidence_status"] == "present"
        assert wire["evidence_status"] == DECISION_EVIDENCE_STATUS_PRESENT
        assert wire["evidence_status"] != DECISION_EVIDENCE_STATUS_LEGACY


def test_a_stop_reason_decision_without_a_triple_is_refused_by_the_gate():
    """`stop_reason` is ENFORCED from this round, so a dropped triple raises."""
    decision = _decision(
        decision_id="sr:regression",
        decision_type="stop_reason",
        evidence=None,
    )

    with pytest.raises(DecisionEvidenceError) as excinfo:
        enforce_decision_evidence([decision])

    message = str(excinfo.value)
    assert "sr:regression" in message
    assert "stop_reason" in message
    assert "evidence_refs is empty: a decision must cite at least one ref." in message


# ---------------------------------------------------------------------------
# F032 T002e — the dirty-repo card, whose whole evidence is one run-log event
#
# These drive the REAL branch through `list_decisions` from BOTH shapes the
# `git_status_read` event actually takes.  The thin one is the metadata
# `_fixture_repo_dirty` in `tests/orchestration/test_decision_inbox.py` writes —
# `dirty` and nothing else — and the full one is what the only non-test emitter,
# `apps/cli/commands/repo.py`, writes.  Pinning both is the point: `repo_dirty`
# is ENFORCED from this round, so an unguarded fingerprint ref would refuse the
# card on the thin event and take the inbox's per-type parametrization with it.
# ---------------------------------------------------------------------------

#: Neither half of the one unkeyed outcome varies with what the event carried,
#: so both are written once and pinned wherever the outcome is asserted.
REPO_DIRTY_EXPECTED_OUTCOME = (
    "Committing or stashing the target repository's changes leaves a clean "
    "tree, so a later diff shows only what this job did."
)
REPO_DIRTY_DOWNSIDE = (
    "The job waits while that happens, and stashing work that is not this "
    "job's can hide changes their author still needs."
)

#: The two event shapes, named after where each one comes from.
THIN_GIT_STATUS_METADATA = {"dirty": True}
FULL_GIT_STATUS_METADATA = {
    "is_git_repo": True,
    "git_available": True,
    "branch": "feature/f032-evidence-triple",
    "head_sha": "0216c5bb9d48",
    "dirty": True,
    "changed_file_count": 3,
    "status_hash": "6f1c2d3e4a5b6c7d",
}


def _repo_dirty_decision(metadata: dict) -> HumanDecision:
    """The card the real branch builds from one dirty `git_status_read`."""
    events = [{
        "event": "git_status_read",
        "timestamp": "2026-08-28T09:00:00+00:00",
        "metadata": metadata,
    }]
    decisions = [d for d in list_decisions(_StubJob(), events)
                 if d.type == "repo_dirty"]
    assert len(decisions) == 1
    return decisions[0]


def test_the_thin_git_status_event_still_yields_a_valid_repo_dirty_card():
    """PINS THE CONDITIONAL: this event carries NO `status_hash`.

    Made unconditional, the fingerprint ref would appear here targeting the
    empty string, which rule (c) of ``evidence_triple_problems`` refuses
    outright — and this is `_fixture_repo_dirty`'s own metadata, so the whole
    inbox would raise instead of rendering.  The event NAME is the receipt that
    keeps rule (a) satisfied with nothing else on the record.
    """
    decision = _repo_dirty_decision(THIN_GIT_STATUS_METADATA)

    assert [(r.kind, r.target, r.label) for r in decision.evidence.refs] == [
        ("failure", "git_status_read",
         "the run-log event that reported the working tree dirty"),
    ]
    assert evidence_triple_problems(decision.evidence, options=[]) == []


def test_the_repo_dirty_card_cites_the_event_and_the_status_fingerprint():
    """The full metadata `apps/cli/commands/repo.py` writes yields both refs."""
    decision = _repo_dirty_decision(FULL_GIT_STATUS_METADATA)

    assert [(r.kind, r.target, r.label) for r in decision.evidence.refs] == [
        ("failure", "git_status_read",
         "the run-log event that reported the working tree dirty"),
        ("failure", "6f1c2d3e4a5b6c7d",
         "the status fingerprint that reading recorded"),
    ]


def test_the_repo_dirty_card_cites_no_branch_no_commit_and_no_count():
    """A2 forbids inventing vocabulary, so three metadata keys stay uncited.

    No kind in ``DECISION_EVIDENCE_REF_KINDS`` types a branch name, a commit or
    a file count, and a ``file`` or ``failure`` ref pointing at one would lie
    about what it is.  This fails if a later round cites them anyway.
    """
    decision = _repo_dirty_decision(FULL_GIT_STATUS_METADATA)
    targets = [r.target for r in decision.evidence.refs]

    assert "feature/f032-evidence-triple" not in targets
    assert "0216c5bb9d48" not in targets
    assert "3" not in targets


@pytest.mark.parametrize(
    "metadata",
    [THIN_GIT_STATUS_METADATA, FULL_GIT_STATUS_METADATA],
    ids=["thin-event", "full-metadata"],
)
def test_no_repo_dirty_ref_ever_points_at_nothing(metadata):
    decision = _repo_dirty_decision(metadata)

    assert decision.evidence.refs
    assert all(r.target for r in decision.evidence.refs)
    assert evidence_triple_problems(decision.evidence, options=[]) == []


@pytest.mark.parametrize(
    "metadata",
    [THIN_GIT_STATUS_METADATA, FULL_GIT_STATUS_METADATA],
    ids=["thin-event", "full-metadata"],
)
def test_the_repo_dirty_card_carries_exactly_one_unkeyed_outcome(metadata):
    """DECISION F032 D3 rule (h): this branch offers no options at all.

    Its one ``next_action`` is an instruction rather than an option word, so the
    card keeps an EMPTY payload and owes exactly one outcome for the decision.
    """
    decision = _repo_dirty_decision(metadata)

    assert decision.payload == {}
    assert [(o.option, o.expected_outcome, o.downside)
            for o in decision.evidence.outcomes] == [
        (UNKEYED_OPTION, REPO_DIRTY_EXPECTED_OUTCOME, REPO_DIRTY_DOWNSIDE),
    ]
    outcome = decision.evidence.outcomes[0]
    assert outcome.expected_outcome.strip()
    assert outcome.downside.strip()


def test_the_repo_dirty_card_exports_the_present_status():
    wire = export_decision_json(_repo_dirty_decision(FULL_GIT_STATUS_METADATA))

    assert wire["evidence_status"] == "present"
    assert wire["evidence_status"] == DECISION_EVIDENCE_STATUS_PRESENT
    assert wire["evidence_status"] != DECISION_EVIDENCE_STATUS_LEGACY


def test_a_repo_dirty_decision_without_a_triple_is_refused_by_the_gate():
    """`repo_dirty` is ENFORCED from this round, so a dropped triple raises."""
    decision = _decision(
        decision_id="dirty_repo",
        decision_type="repo_dirty",
        evidence=None,
    )

    with pytest.raises(DecisionEvidenceError) as excinfo:
        enforce_decision_evidence([decision])

    message = str(excinfo.value)
    assert "dirty_repo" in message
    assert "repo_dirty" in message
    assert "evidence_refs is empty: a decision must cite at least one ref." in message


# ---------------------------------------------------------------------------
# F032 T002e — the memory-review card, which names a key and cites neither it
# nor the field the reason was read off
#
# All three of its refs are guarded, so each is pinned in BOTH directions: the
# stale-only card, the flagged-only card, the card that is both, and the card
# with no key at all.  The last one is the argument the key's guard rests on —
# rule (a) stays satisfied with no key, because the branch's own selecting
# predicate guarantees at least one of the two field refs fires.
# ---------------------------------------------------------------------------

#: Neither half of the one unkeyed outcome varies with the card, so both are
#: written once and pinned wherever the outcome is asserted.
MEMORY_REVIEW_EXPECTED_OUTCOME = (
    "Opening the named card shows what it claims and when that was last "
    "confirmed, so it can be re-approved, corrected or superseded instead of "
    "trusted blind."
)
MEMORY_REVIEW_DOWNSIDE = (
    "Reading it takes time now, and a card left in place while it is checked "
    "keeps feeding whatever already reads it."
)


def _stale_only_entry() -> MemoryEntry:
    return MemoryEntry(key="deploy-target", validity="stale")


def _flagged_only_entry() -> MemoryEntry:
    return MemoryEntry(key="api-contract", review_status="needs_review")


def _stale_and_flagged_entry() -> MemoryEntry:
    return MemoryEntry(
        key="db-dsn", validity="stale", review_status="needs_review")


def _keyless_entry() -> MemoryEntry:
    """``MemoryEntry.key`` defaults to the empty string, so this is reachable."""
    return MemoryEntry(validity="stale")


def _memory_review_decision(monkeypatch, entry: MemoryEntry) -> HumanDecision:
    decisions = _memory_review_decisions(monkeypatch, entry)
    assert len(decisions) == 1
    return decisions[0]


def test_the_memory_review_card_cites_the_card_and_its_staleness(monkeypatch):
    decision = _memory_review_decision(monkeypatch, _stale_only_entry())

    assert [(r.kind, r.target, r.label) for r in decision.evidence.refs] == [
        ("decision", "deploy-target", "the memory card this review is about"),
        ("failure", "stale", "the validity the card carries"),
    ]


def test_the_memory_review_card_cites_the_card_and_its_review_flag(monkeypatch):
    """PINS THE VALIDITY GUARD: this card's ``validity`` is ``active``.

    Made unconditional, the validity ref would appear here citing ``active`` as
    a reason to look at a card — the same wrong fact R-0711 removed from the
    summary, restated as a receipt.
    """
    entry = _flagged_only_entry()
    assert entry.validity == "active"

    decision = _memory_review_decision(monkeypatch, entry)

    assert [(r.kind, r.target, r.label) for r in decision.evidence.refs] == [
        ("decision", "api-contract", "the memory card this review is about"),
        ("failure", "needs_review", "the review status the card carries"),
    ]


def test_the_memory_review_card_cites_both_flags_when_both_fired(monkeypatch):
    """PINS THE REVIEW-STATUS GUARD from the other side: both arms fired here."""
    decision = _memory_review_decision(monkeypatch, _stale_and_flagged_entry())

    assert [(r.kind, r.target, r.label) for r in decision.evidence.refs] == [
        ("decision", "db-dsn", "the memory card this review is about"),
        ("failure", "stale", "the validity the card carries"),
        ("failure", "needs_review", "the review status the card carries"),
    ]


def test_the_memory_review_card_stays_valid_with_no_key_at_all(monkeypatch):
    """PINS THE KEY GUARD, and the argument it rests on.

    ``MemoryEntry.key`` defaults to the empty string, so an unconditional key
    ref would point at nothing and rule (c) would refuse the card.  Rule (a) is
    still satisfied because the selecting predicate admits a card only when it
    is stale or flagged, so at least one field ref always fires.
    """
    decision = _memory_review_decision(monkeypatch, _keyless_entry())

    assert [(r.kind, r.target, r.label) for r in decision.evidence.refs] == [
        ("failure", "stale", "the validity the card carries"),
    ]
    assert evidence_triple_problems(decision.evidence, options=[]) == []


@pytest.mark.parametrize(
    "make_entry",
    [
        _stale_only_entry,
        _flagged_only_entry,
        _stale_and_flagged_entry,
        _keyless_entry,
    ],
    ids=["stale-only", "flagged-only", "stale-and-flagged", "no-key"],
)
def test_no_memory_review_ref_ever_points_at_nothing(monkeypatch, make_entry):
    decision = _memory_review_decision(monkeypatch, make_entry())

    assert decision.evidence.refs
    assert all(r.target for r in decision.evidence.refs)
    assert evidence_triple_problems(decision.evidence, options=[]) == []


@pytest.mark.parametrize(
    "make_entry",
    [
        _stale_only_entry,
        _flagged_only_entry,
        _stale_and_flagged_entry,
        _keyless_entry,
    ],
    ids=["stale-only", "flagged-only", "stale-and-flagged", "no-key"],
)
def test_the_memory_review_card_carries_exactly_one_unkeyed_outcome(
    monkeypatch, make_entry,
):
    """DECISION F032 D3 rule (h): this branch offers no options at all.

    Its one ``next_action`` is a ``remedy memory card-show`` command rather than
    an option word, so the card keeps an EMPTY payload and owes one outcome.
    """
    decision = _memory_review_decision(monkeypatch, make_entry())

    assert decision.payload == {}
    assert [(o.option, o.expected_outcome, o.downside)
            for o in decision.evidence.outcomes] == [
        (UNKEYED_OPTION, MEMORY_REVIEW_EXPECTED_OUTCOME, MEMORY_REVIEW_DOWNSIDE),
    ]
    outcome = decision.evidence.outcomes[0]
    assert outcome.expected_outcome.strip()
    assert outcome.downside.strip()


def test_the_memory_review_card_exports_the_present_status(monkeypatch):
    wire = export_decision_json(
        _memory_review_decision(monkeypatch, _stale_only_entry()))

    assert wire["evidence_status"] == "present"
    assert wire["evidence_status"] == DECISION_EVIDENCE_STATUS_PRESENT
    assert wire["evidence_status"] != DECISION_EVIDENCE_STATUS_LEGACY


def test_a_memory_review_decision_without_a_triple_is_refused_by_the_gate():
    """`memory_review` is ENFORCED from this round, so a dropped triple raises."""
    decision = _decision(
        decision_id="mem:regression",
        decision_type="memory_review",
        evidence=None,
    )

    with pytest.raises(DecisionEvidenceError) as excinfo:
        enforce_decision_evidence([decision])

    message = str(excinfo.value)
    assert "mem:regression" in message
    assert "memory_review" in message
    assert "evidence_refs is empty: a decision must cite at least one ref." in message
