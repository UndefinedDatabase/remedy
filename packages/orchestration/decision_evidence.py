"""Decision evidence triple — the receipts a decision must carry (F032 T001a).

A decision a human is asked to answer arrives with three things or it does not
arrive at all: the REFS that let a reader check the claim, the EXPECTED OUTCOME
of each option, and that option's DOWNSIDE.  This module holds the shape of
those receipts and the one function that says why a given set of them is not
acceptable.  It is the schema half of T001; the emit gate that refuses a
tripleless decision is T001b (DECISION F032 D1) and its CALL SITE is the
derivation point ``decision_queue.list_decisions``, not here — this module only
supplies ``enforce_decision_evidence`` for that call site to use, and never
reaches back into the queue.

This module is PURE: it performs no I/O, opens no path, keeps no state and
imports nothing from ``decision_queue`` — so when ``list_decisions`` starts
calling it in T001b there is no import cycle to break.

Remedy deliberately does NOT resolve a ref or render a staleness badge here,
because the resolver is F066 and is unbuilt — a badge with no resolver behind
it would be a false live indicator, claiming a ref had been checked when
nothing checked it.  A reader searching this module for ``resolve`` should stop
at this paragraph: the resolution layer is a later feature, not a missing piece
of this one.

Public API::

    DECISION_EVIDENCE_REF_KINDS — frozenset[str], the four accepted ref kinds
    NO_MATERIAL_DOWNSIDE — str, the one permitted benign downside literal
    UNKEYED_OPTION — str, the option key an optionless decision uses
    BOILERPLATE_PHRASES — frozenset[str], the anti-boilerplate denylist
    DECISION_EVIDENCE_STATUS_PRESENT — str, the per-card marker for a real triple
    DECISION_EVIDENCE_STATUS_LEGACY — str, the per-card honest placeholder
    TRIPLE_REQUIRED_TYPES — frozenset[str], the decision types the gate enforces
    DecisionEvidenceRef(kind, target, label)
    DecisionOptionOutcome(option, expected_outcome, downside)
    DecisionEvidenceTriple(refs, outcomes)
    evidence_triple_problems(triple, *, options) -> list[str]
    export_decision_evidence(triple) -> dict
    DecisionEvidenceError — ValueError, raised by the emit gate
    enforce_decision_evidence(decisions) -> None
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

#: The ref vocabulary, DELIBERATELY F066's own
#: (``docs/roadmap/features/T3_F066.md:24-29``) rather than a fresh one, per
#: DECISION F032 D2: when F066 lands its resolver, the migration is a rename
#: onto F066's constant instead of a re-typing of four strings scattered
#: through producers.  It is a real constant and not a comment on purpose —
#: the two nearest existing types,
#: ``provider_trust_verification.ProviderVerificationEvidenceRef`` and
#: ``orchestrator_brain.OrchestratorEvidenceRef``, both state their vocabulary
#: only in a trailing ``#`` comment, so nothing can validate against either.
#: That is exactly the failure this constant exists to avoid.
DECISION_EVIDENCE_REF_KINDS = frozenset({"file", "failure", "coverage", "decision"})

#: The one downside literal a genuinely benign case may use, permitted by name
#: in ``docs/roadmap/features/T5_F032.md:78-80``: honesty includes benign
#: cases, so a producer that has truly found no downside says so in these exact
#: words rather than inventing a risk or leaving the field blank.
NO_MATERIAL_DOWNSIDE = "no material downside identified"

#: The option key of a decision that offers no options at all — five of the
#: eight producing branches carry no options list (DECISION F032 D3), and they
#: still owe one outcome.  The empty string keeps the wire shape identical for
#: keyed and unkeyed decisions instead of making ``option`` nullable.
UNKEYED_OPTION = ""

#: The anti-boilerplate denylist the feature file makes ACCEPTANCE material
#: (``docs/roadmap/features/T5_F032.md:71-75``): generic filler that may never
#: stand as an expected outcome or a downside, because filler is how a producer
#: satisfies the shape of the triple while carrying none of its truth.
#: Matching is case-insensitive on the STRIPPED string, so ``  N/A  `` is
#: caught.  ``NO_MATERIAL_DOWNSIDE`` is deliberately NOT a member: the feature
#: file permits that literal by name, and a denylist that swallowed it would
#: punish the one honest way to report a benign case.
BOILERPLATE_PHRASES = frozenset({
    "-",
    "?",
    "n/a",
    "na",
    "none",
    "nothing",
    "same as above",
    "see above",
    "see below",
    "tbd",
    "to be determined",
    "unknown",
})

#: The two values of a card's own ``evidence_status``.  THIS IS A PER-CARD
#: MARKER AND NOT A BUMP OF ``DECISION_INBOX_VERSION`` (DECISION F032 D5):
#: that constant has no reader anywhere in ``packages/`` or ``apps/`` — the
#: only code comparing it compares it against the value the same process just
#: wrote — and a migration story built on a stamp nothing reads is a story
#: nothing tells.  A single job can also hold legacy and upgraded decisions
#: side by side, which a document-level stamp cannot express at all.
DECISION_EVIDENCE_STATUS_PRESENT = "present"

#: The honest placeholder ``docs/roadmap/features/T5_F032.md:28-31`` asks for,
#: in those words: a decision recorded before F032 says so, rather than
#: carrying a fabricated triple that no producer ever wrote.
DECISION_EVIDENCE_STATUS_LEGACY = "recorded_before_evidence_requirements"

#: The decision types the emit gate actually enforces.  It held ``token_budget``
#: alone from T002a, which is the commit that gave the budget stop of
#: ``decision_queue`` a real triple — it was EMPTY at T001b, and that emptiness
#: stopped being true the moment a producer was upgraded.  THE RULE BY WHICH A
#: TYPE JOINS IS UNCHANGED (DECISION F032 D5): a type is added here ONLY in the
#: same commit that gives its producer a real triple, never ahead of one, so the
#: gate can fire on a regression and never on a card nobody has upgraded yet.
#: When all eight types are in the set the gate is fully live and this constant
#: has become a formality, which is when it can be deleted.
TRIPLE_REQUIRED_TYPES: frozenset[str] = frozenset({
    "token_budget", "test_failure", "patch_approval", "stop_reason",
})


# One checkable reference behind a decision: WHAT kind of thing, WHICH one, and
# how to name it to a human.  ``target`` is left as an opaque string because
# each kind addresses its subject differently (a path, a failure class, a queue
# id) and F066 owns the per-kind parsing.
@dataclass(frozen=True)
class DecisionEvidenceRef:
    kind: str
    target: str
    label: str


# What one option is expected to do, and what it costs.  Both halves are
# required: an expected outcome with no downside reads as a recommendation
# rather than as a choice.
@dataclass(frozen=True)
class DecisionOptionOutcome:
    option: str
    expected_outcome: str
    downside: str


# The triple itself.  Its Python name carries a domain word because
# ``EvidenceRef`` alone would not grep to its own definition — both bare
# spellings are already taken in this repository for other concepts
# (DECISION F032 D4).  The WIRE key stays ``evidence_refs``; see
# ``export_decision_evidence``.
@dataclass(frozen=True)
class DecisionEvidenceTriple:
    refs: tuple[DecisionEvidenceRef, ...]
    outcomes: tuple[DecisionOptionOutcome, ...]


def _members(value: Any) -> list[Any]:
    """Read a triple field as a list of members, tolerating whatever is there.

    Anything that is not a tuple or a list — ``None``, a bare string, an int —
    reads as NO members, which surfaces downstream as a stated problem rather
    than as an exception.  A bare string is excluded on purpose: iterating one
    would yield characters and invent members that no producer wrote.
    """
    if isinstance(value, (tuple, list)):
        return list(value)
    return []


def _text(value: Any) -> str:
    """Read a triple field as text; a non-string reads as absent, never raises.

    Coercing with ``str()`` would turn ``None`` into the four-character string
    ``"None"`` and hide the defect; reading it as absent makes the empty-field
    rule report it instead.
    """
    return value if isinstance(value, str) else ""


def _is_boilerplate(value: str) -> bool:
    """Whether a field is generic filler — case-insensitive on the stripped string."""
    return value.strip().lower() in BOILERPLATE_PHRASES


def evidence_triple_problems(
    triple: Any,
    *,
    options: Sequence[str],
) -> list[str]:
    """Every reason this triple is not acceptable, one plain sentence each.

    Returns the EMPTY list when the triple is acceptable, so a caller reads it
    as a gate.  ``options`` is the decision's own options list and may be
    empty — five of the eight producing branches carry none (DECISION F032 D3).

    NO INPUT MAKES THIS RAISE, and that is load-bearing rather than defensive
    politeness: T001b calls it on every card in the inbox, and an exception
    there would lose the decision it was asked to check.  A malformed triple
    therefore produces problems, never a traceback.
    """
    problems: list[str] = []
    refs = _members(getattr(triple, "refs", None))
    outcomes = _members(getattr(triple, "outcomes", None))
    option_keys = [_text(option) for option in _members(options)]

    # (a) no refs at all
    if not refs:
        problems.append(
            "evidence_refs is empty: a decision must cite at least one ref."
        )

    for index, ref in enumerate(refs):
        kind = _text(getattr(ref, "kind", None))
        # (b) a kind outside the vocabulary
        if kind not in DECISION_EVIDENCE_REF_KINDS:
            problems.append(
                f"evidence ref {index} has kind {kind!r}, which is not one of "
                f"{', '.join(sorted(DECISION_EVIDENCE_REF_KINDS))}."
            )
        # (c) a ref that points at nothing
        if not _text(getattr(ref, "target", None)).strip():
            problems.append(
                f"evidence ref {index} has an empty target and points at nothing."
            )

    for outcome in outcomes:
        option = _text(getattr(outcome, "option", None))
        expected = _text(getattr(outcome, "expected_outcome", None))
        downside = _text(getattr(outcome, "downside", None))
        # (d) and (e) a required half left blank
        if not expected.strip():
            problems.append(
                f"outcome for option {option!r} has an empty expected_outcome."
            )
        if not downside.strip():
            problems.append(
                f"outcome for option {option!r} has an empty downside."
            )
        # (f) filler standing in for either half
        for field_name, field_value in (
            ("expected_outcome", expected),
            ("downside", downside),
        ):
            if _is_boilerplate(field_value):
                problems.append(
                    f"outcome for option {option!r} has the boilerplate "
                    f"{field_name} {field_value!r}."
                )

    outcome_keys = [_text(getattr(outcome, "option", None)) for outcome in outcomes]
    if option_keys:
        # (g) the outcome keys must be the options exactly, both ways
        for option in option_keys:
            if option not in outcome_keys:
                problems.append(
                    f"no outcome is given for option {option!r}."
                )
        for option in outcome_keys:
            if option not in option_keys:
                problems.append(
                    f"outcome names option {option!r}, which this decision does "
                    f"not offer."
                )
    else:
        # (h) an optionless decision owes exactly one outcome, keyed unkeyed
        if len(outcomes) != 1:
            problems.append(
                f"a decision with no options must carry exactly one outcome, "
                f"but it carries {len(outcomes)}."
            )
        for option in outcome_keys:
            if option != UNKEYED_OPTION:
                problems.append(
                    f"a decision with no options must key its outcome as "
                    f"UNKEYED_OPTION, but it uses {option!r}."
                )

    return problems


def export_decision_evidence(triple: Any) -> dict[str, Any]:
    """The wire form of a triple: ``evidence_refs`` and ``outcomes``, nothing else.

    THE WIRE SPELLING IS ``evidence_refs`` AND THAT IS DELIBERATE, which is
    exactly the question a reader arrives with, since the Python type is
    ``DecisionEvidenceRef``.  Two reasons.  It is the name
    ``docs/roadmap/features/T5_F032.md`` uses throughout, and diverging from
    the one document a later reader treats as the specification costs more than
    it buys.  And a key INSIDE a decision card is namespaced by the card, so it
    cannot collide with the unrelated Python attribute
    ``orchestrator_brain.OrchestratorEvidenceRef`` the way a bare type name
    would (DECISION F032 D4).
    """
    return {
        "evidence_refs": [
            {
                "kind": ref.kind,
                "target": ref.target,
                "label": ref.label,
            }
            for ref in _members(getattr(triple, "refs", None))
        ],
        "outcomes": [
            {
                "option": outcome.option,
                "expected_outcome": outcome.expected_outcome,
                "downside": outcome.downside,
            }
            for outcome in _members(getattr(triple, "outcomes", None))
        ],
    }


# The one exception this subsystem raises: an ENFORCED decision type reached the
# emit point without an acceptable triple.  A ``ValueError`` subclass because the
# offending value is the decision itself, and because callers that already catch
# ``ValueError`` around the derivation keep catching this.
class DecisionEvidenceError(ValueError):
    """An enforced decision type carried no acceptable evidence triple."""


def enforce_decision_evidence(decisions: Sequence[Any]) -> None:
    """Raise on any ENFORCED decision whose triple is missing or unacceptable.

    WHY IT RAISES RATHER THAN DROPPING THE DECISION, which is the question a
    reader arrives with.  Dropping a tripleless decision would LOSE A HUMAN
    QUESTION, and not losing one is exactly what ``decision_inbox.py`` says this
    subsystem will not do.  A producer that ships an ENFORCED type with no
    triple is a programming error, which is what
    ``docs/roadmap/features/T5_F032.md:25`` means by "a canary producer missing
    a field fails CI" — a statement about CI, not about runtime refusal.  And
    because ``TRIPLE_REQUIRED_TYPES`` only ever holds types whose producer has
    already been upgraded (DECISION F032 D5), the raise can fire only on a
    regression, never on a record that predates the requirement.

    A decision whose type is NOT in ``TRIPLE_REQUIRED_TYPES`` is left entirely
    alone: it is not read, not validated and not altered.
    """
    for decision in decisions:
        if _text(getattr(decision, "type", None)) not in TRIPLE_REQUIRED_TYPES:
            continue
        payload = getattr(decision, "payload", None)
        options = payload.get("options", []) if isinstance(payload, dict) else []
        problems = evidence_triple_problems(
            getattr(decision, "evidence", None),
            options=_members(options),
        )
        if problems:
            decision_id = _text(getattr(decision, "id", None))
            decision_type = _text(getattr(decision, "type", None))
            raise DecisionEvidenceError(
                f"decision {decision_id!r} of type {decision_type!r} carries no "
                f"acceptable evidence triple: {' '.join(problems)}"
            )
