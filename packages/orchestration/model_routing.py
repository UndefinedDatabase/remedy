"""
Model routing by task class for Remedy (F110).

Owns the CLASS TABLE — which model TIER a declared task class is routed to — and
the THREE HARD RULES of docs/agents/model_routing_policy.md as named checks, each
returning ITS OWN rule name when a routing choice violates it. Nothing else yet:
no config file is read, no model id is named and no call site routes through it.
The table is SEEDED from the "Seed mapping" section of
docs/agents/model_routing_policy.md, which remains the human-readable policy.
tests/orchestration/test_model_routing.py parses that section and asserts the
parsed mapping EQUALS :data:`TASK_CLASS_TIERS`, so the document and this table
cannot drift apart silently — that sync test is an explicit acceptance line of
docs/roadmap/features/T3_F110.md.

:data:`MODEL_TIERS` is ordered CHEAPEST TO STRONGEST and that ORDER IS
SIGNIFICANT: the hard rules of the policy document are comparisons along it
("reviewer never weaker than the paired worker", "never below mid"), so the
vocabulary is stated exactly once, here, and compared by index.

Remedy deliberately does not map a task class to a MODEL ID in this module. A
tier is the policy-level answer; which concrete model serves a tier is a
configuration question, and mixing the two would put the promotion discipline
(policy document, "Promotion rule") behind a casual table edit.

Nothing in production imports this module yet: the per-call-site task-class
declarations come after the resolver seam work, so the table lands and is
pinned before anything routes through it.

THE WORD "TIER" MEANS SOMETHING ELSE ONE MODULE OVER, and nothing is renamed:
packages/orchestration/orchestrator_brain.py's ``OrchestratorModelRoutingPlan``
carries a field ``tier`` whose vocabulary is HUMAN_REVIEW_REQUIRED /
EXTERNAL_BUILDER_NEEDED / local_advisor_preferred — it answers WHEN a job must
escalate to a human or an external builder, and it surfaces as
``model_routing_plan.tier`` and ``model_routing_tier`` in the ledger, the review
bundle, the UI server and the CLI — whereas :data:`MODEL_TIERS` here answers
WHICH STRENGTH OF MODEL a declared task class is routed to. AGENTS.md's
discoverability section forbids mass renames of existing code as their own
activity, so the counter-measure is this sentence rather than a rename: a reader
who searches for "tier" and lands in the wrong vocabulary reads here which is
which.

Public API::

    MODEL_TIERS: tiers CHEAPEST FIRST — the order is significant
    TOP_TIER: the strongest tier, i.e. MODEL_TIERS[-1]
    MID_TIER: the middle tier, i.e. MODEL_TIERS[len(MODEL_TIERS) // 2]
    TASK_CLASS_TIERS: the seeded task-class -> tier table
    SEED_MAPPING_REASON: reason recorded for a class the seed mapping names
    UNKNOWN_CLASS_REASON: reason recorded for a class it does not
    normalize_task_class(phrase) -> str
    resolve_task_class_tier(task_class) -> tuple[str, str]
    model_tier_rank(tier) -> int, raising on a tier MODEL_TIERS does not name
    RULE_REVIEWER_WEAKER_THAN_WORKER: hard-rule name, policy hard rule 1
    RULE_ORCHESTRATION_BELOW_TOP_TIER: hard-rule name, the feature file's
        "orchestrator and mission-compile calls always top tier"
    RULE_SAFETY_CLASS_BELOW_MID_TIER: hard-rule name, policy hard rule 2
    HARD_RULE_NAMES: the three above, in the order violations are reported
    ORCHESTRATION_TASK_CLASSES: the classes pinned to the top tier
    SAFETY_RELEVANT_CLASSES: the safety-relevant classes — EMPTY today
    check_reviewer_not_weaker_than_worker(worker_tier, reviewer_tier)
    check_orchestration_class_routed_to_top_tier(task_class, tier)
    check_safety_relevant_class_not_below_mid_tier(task_class, tier, classes)
    validate_routing_choice(...) -> tuple[str, ...] of every violated rule name
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# The tier vocabulary
# ---------------------------------------------------------------------------

#: The three tiers docs/agents/model_routing_policy.md names, CHEAPEST FIRST.
#: The ORDER is load-bearing, not cosmetic: the policy's hard rules are
#: comparisons along this tuple, so they are index comparisons on it rather
#: than a second, rival ranking.
MODEL_TIERS: tuple[str, ...] = ("cheap", "mid", "top")

#: The strongest tier, derived from MODEL_TIERS so the order stays the one
#: source of truth. An unknown class routes here — over-spending beats
#: under-thinking (docs/roadmap/features/T3_F110.md, "Edge cases").
TOP_TIER: str = MODEL_TIERS[-1]

# ---------------------------------------------------------------------------
# Routing reasons — recorded beside the routed model on every routed call
# ---------------------------------------------------------------------------

#: Recorded when the seed mapping names the class outright.
SEED_MAPPING_REASON: str = "seed_mapping"

#: Recorded when it does not. The exact string
#: docs/roadmap/features/T3_F110.md's "Edge cases & assumption defaults"
#: section specifies; it is a fixed token because evidence readers group on it.
UNKNOWN_CLASS_REASON: str = "unknown_class_conservative"


# The doc writes its classes as English phrases ("standard build", "prompt
# authoring for other agents"); this is the ONE normalization that turns such a
# phrase into a table key, so the sync test can be a straight set comparison
# rather than a translation table nobody maintains.
def normalize_task_class(phrase: str) -> str:
    """Return the table key for a task-class ``phrase``.

    Strips, lowercases, and collapses each run of whitespace to a single
    underscore, so ``"Standard Build"``, ``"standard build"`` and
    ``"standard_build"`` are all the one key ``"standard_build"``.

    Both the seeded table below and the policy-document sync test use this
    function and no other, which is what makes the two directly comparable.
    """
    return "_".join(phrase.lower().split())


# ---------------------------------------------------------------------------
# The class table
# ---------------------------------------------------------------------------

#: Task class -> model tier, SEEDED from the "Seed mapping" section of
#: docs/agents/model_routing_policy.md and kept equal to it by the sync test in
#: tests/orchestration/test_model_routing.py. Adding, renaming or re-tiering an
#: entry HERE without the same change in the document turns that test red, and
#: vice versa — which is the whole point of the table living in two places.
TASK_CLASS_TIERS: dict[str, str] = {
    # format / extract / summarize / boilerplate -> cheap tier (local allowed)
    "format": "cheap",
    "extract": "cheap",
    "summarize": "cheap",
    "boilerplate": "cheap",
    # standard build / standard review -> mid tier
    "standard_build": "mid",
    "standard_review": "mid",
    # architecture / mission / vision / prompt authoring for other agents -> top tier
    "architecture": "top",
    "mission": "top",
    "vision": "top",
    "prompt_authoring_for_other_agents": "top",
}


# A call site asks HERE which tier its declared class gets, and gets the REASON
# with it, because the routed model without its reason is an unauditable claim
# (docs/agents/model_routing_policy.md hard rule 3).
def resolve_task_class_tier(task_class: str) -> tuple[str, str]:
    """Return ``(tier, reason)`` for a declared ``task_class``.

    The argument is normalized through :func:`normalize_task_class` first, so
    a call site may declare its class in the document's own wording.

    A class the seed mapping names resolves to its documented tier with the
    reason :data:`SEED_MAPPING_REASON`. Any other class resolves to
    :data:`TOP_TIER` with the reason :data:`UNKNOWN_CLASS_REASON`: routing
    conservatively means a new class costs money rather than quality until it
    is declared, and the reason string is what makes the omission visible in
    evidence instead of silent.
    """
    key = normalize_task_class(task_class)
    tier = TASK_CLASS_TIERS.get(key)
    if tier is None:
        return TOP_TIER, UNKNOWN_CLASS_REASON
    return tier, SEED_MAPPING_REASON


# ---------------------------------------------------------------------------
# Tier comparison — one ordered vocabulary, compared by index and nothing else
# ---------------------------------------------------------------------------

#: The MIDDLE tier, derived from MODEL_TIERS so the order stays the one source of
#: truth. The policy's "never below mid" rule compares against THIS, never
#: against a re-spelled literal that a re-tiering would leave behind.
MID_TIER: str = MODEL_TIERS[len(MODEL_TIERS) // 2]


# Every hard rule below is an index comparison along MODEL_TIERS rather than a
# second, rival ranking — this function is the ONE place a tier becomes a number.
def model_tier_rank(tier: str) -> int:
    """Return the RANK of ``tier`` along :data:`MODEL_TIERS`, cheapest first.

    ``model_tier_rank("cheap")`` is 0 and ``model_tier_rank(TOP_TIER)`` is the
    largest rank, so "weaker than" and "below mid" are ``<`` on the result.

    AN UNKNOWN TIER IS A PROGRAMMING ERROR, NOT A ROUTING DECISION, so this
    RAISES :class:`ValueError` instead of returning a silent default. A default
    of 0 would make every rule refuse the unknown tier and a default of
    ``len(MODEL_TIERS)`` would make every rule pass it; both are invisible, and
    both would let a typo in a config file decide policy. The caller is made to
    fix its vocabulary instead.
    """
    try:
        return MODEL_TIERS.index(tier)
    except ValueError:
        raise ValueError(
            f"unknown model tier {tier!r}; MODEL_TIERS names {MODEL_TIERS!r}"
        ) from None


# ---------------------------------------------------------------------------
# The three hard rules, as NAMED tokens
# ---------------------------------------------------------------------------
# "Refused with the rule named" (docs/roadmap/features/T3_F110.md, Acceptance)
# means the caller receives a STABLE TOKEN it can branch on, log and group by —
# never a prose sentence. Prose is rewritten by the next editor; a token is not.

#: Violated when a reviewer is routed STRICTLY WEAKER than the worker it reviews.
#: Policy hard rule 1: equal is allowed and stronger is preferred, because a weak
#: reviewer passing a weak worker compounds errors instead of catching them.
RULE_REVIEWER_WEAKER_THAN_WORKER: str = "reviewer_weaker_than_worker"

#: Violated when an orchestration-class call is routed BELOW the top tier. From
#: docs/roadmap/features/T3_F110.md's Design section: orchestrator and
#: mission-compile calls always top tier.
RULE_ORCHESTRATION_BELOW_TOP_TIER: str = "orchestration_below_top_tier"

#: Violated when a SAFETY-RELEVANT class is routed BELOW the mid tier. Policy
#: hard rule 2: no silent downgrade of security-relevant roles.
RULE_SAFETY_CLASS_BELOW_MID_TIER: str = "safety_class_below_mid_tier"

#: The three rule names in a FIXED, DECLARED order — the order
#: :func:`validate_routing_choice` reports violations in. It is deliberately
#: INDEPENDENT of MODEL_TIERS: re-tiering the model vocabulary must not reshuffle
#: an operator's error list, because a list that reorders itself reads as a
#: different set of problems.
HARD_RULE_NAMES: tuple[str, ...] = (
    RULE_REVIEWER_WEAKER_THAN_WORKER,
    RULE_ORCHESTRATION_BELOW_TOP_TIER,
    RULE_SAFETY_CLASS_BELOW_MID_TIER,
)

#: The task classes that ALWAYS route to :data:`TOP_TIER`. These are the calls
#: that decide what every other call does, so under-thinking one is paid for by
#: every job it plans. Note that the seed table already routes ``mission`` to the
#: top tier; this set is what makes the guarantee a CHECKED rule rather than a
#: property of one table entry an override could quietly move.
ORCHESTRATION_TASK_CLASSES: frozenset[str] = frozenset(
    {
        normalize_task_class("orchestrator"),
        normalize_task_class("mission compile"),
    }
)

#: The safety-relevant task classes, for the policy document's hard rule 2.
#:
#: REMEDY DELIBERATELY SHIPS THIS SET EMPTY. The policy scopes the rule to
#: "fence/DoD evaluation prompts, if any become LLM calls", and none of them is
#: an LLM call today — the fence and the DoD evaluation are deterministic Python.
#: A reader who searches for why the safety rule never fires in production must
#: land HERE: it does not fire because there is nothing yet for it to fire ON,
#: not because it is broken or unreachable.
#:
#: That emptiness is exactly why
#: :func:`check_safety_relevant_class_not_below_mid_tier` takes the class set as
#: a PARAMETER defaulting to this constant. A check written against an empty
#: constant alone could never refuse anything, and a rule that cannot fail is not
#: a rule; the parameter lets the test supply a FIXTURE set and prove the refusal
#: really happens. A separate test asserts this constant is empty TODAY, so the
#: day it stops being empty is a day somebody notices.
SAFETY_RELEVANT_CLASSES: frozenset[str] = frozenset()


# ---------------------------------------------------------------------------
# The three checks — each returns ITS OWN rule name when violated, else None
# ---------------------------------------------------------------------------
# Every check below is a PURE FUNCTION of the values passed to it: it reads no
# config file, no environment and no global routing state. The config schema that
# feeds them is F110 T002c.


# WHY: policy hard rule 1 — a reviewer weaker than the worker it reviews
# compounds errors rather than catching them, so equal passes, stronger passes,
# and only STRICTLY weaker refuses.
def check_reviewer_not_weaker_than_worker(worker_tier: str, reviewer_tier: str) -> str | None:
    """Return :data:`RULE_REVIEWER_WEAKER_THAN_WORKER` if the rule is VIOLATED.

    Returns ``None`` when it is not, which is the shape every check in this
    module shares: a rule name is a refusal, ``None`` is a pass.

    Both tiers are ranked through :func:`model_tier_rank`, so a tier
    :data:`MODEL_TIERS` does not name raises instead of being read as a pass.
    """
    if model_tier_rank(reviewer_tier) < model_tier_rank(worker_tier):
        return RULE_REVIEWER_WEAKER_THAN_WORKER
    return None


# WHY: docs/roadmap/features/T3_F110.md — orchestrator and mission-compile calls
# always top tier, because these are the calls whose output every later call
# obeys, and over-spending on them beats under-thinking them.
def check_orchestration_class_routed_to_top_tier(task_class: str, tier: str) -> str | None:
    """Return :data:`RULE_ORCHESTRATION_BELOW_TOP_TIER` if the rule is VIOLATED.

    Returns ``None`` for any class outside :data:`ORCHESTRATION_TASK_CLASSES` —
    the rule simply does not speak about those — and ``None`` for an
    orchestration class routed to :data:`TOP_TIER`.

    ``task_class`` passes through :func:`normalize_task_class`, so a call site
    may declare "Mission Compile" or "mission_compile" alike.
    """
    if normalize_task_class(task_class) not in ORCHESTRATION_TASK_CLASSES:
        return None
    if model_tier_rank(tier) < model_tier_rank(TOP_TIER):
        return RULE_ORCHESTRATION_BELOW_TOP_TIER
    return None


# WHY: policy hard rule 2 — no silent downgrade of security-relevant roles; a
# fence evaluation answered by the cheapest available model is a fence that
# agrees with whatever it is shown.
def check_safety_relevant_class_not_below_mid_tier(
    task_class: str,
    tier: str,
    safety_relevant_classes: frozenset[str] = SAFETY_RELEVANT_CLASSES,
) -> str | None:
    """Return :data:`RULE_SAFETY_CLASS_BELOW_MID_TIER` if the rule is VIOLATED.

    Returns ``None`` for any class outside ``safety_relevant_classes``, and
    ``None`` for a safety-relevant class routed at or above :data:`MID_TIER`.

    ``safety_relevant_classes`` DEFAULTS to :data:`SAFETY_RELEVANT_CLASSES`,
    which is EMPTY in production today, so this check refuses nothing in
    production today — deliberately, and documented at that constant. The
    parameter exists so the rule can be exercised against a fixture set and shown
    to refuse, rather than shipping as a check that could never fail.
    """
    if normalize_task_class(task_class) not in safety_relevant_classes:
        return None
    if model_tier_rank(tier) < model_tier_rank(MID_TIER):
        return RULE_SAFETY_CLASS_BELOW_MID_TIER
    return None


# WHY: a validation that reports ONE of three broken rules sends its operator
# round the loop three times; this collects EVERY violated rule name at once.
def validate_routing_choice(
    task_class: str,
    tier: str,
    paired_worker_tier: str | None = None,
    safety_relevant_classes: frozenset[str] = SAFETY_RELEVANT_CLASSES,
) -> tuple[str, ...]:
    """Return every hard-rule name a candidate routing choice VIOLATES.

    The choice routes ``task_class`` to ``tier``. ``paired_worker_tier`` is
    supplied ONLY when the choice is a REVIEWER call, and is then the tier of the
    worker being reviewed; ``None`` means the choice is not a reviewer call and
    hard rule 1 has nothing to compare it against.

    The result is a tuple in :data:`HARD_RULE_NAMES` order — stable, and
    independent of :data:`MODEL_TIERS`, so re-tiering the model vocabulary cannot
    reshuffle the list an operator reads. An EMPTY tuple means the choice breaks
    no hard rule; it does not mean the choice is a good one, only a legal one.

    Each name in the result is the value a check actually RETURNED, not a label
    this function attached, so a check that stops refusing drops out of the
    result rather than being reported on its behalf.
    """
    returned = [
        check_orchestration_class_routed_to_top_tier(task_class, tier),
        check_safety_relevant_class_not_below_mid_tier(task_class, tier, safety_relevant_classes),
    ]
    if paired_worker_tier is not None:
        returned.append(check_reviewer_not_weaker_than_worker(paired_worker_tier, tier))
    refused = {name for name in returned if name is not None}
    return tuple(name for name in HARD_RULE_NAMES if name in refused)
