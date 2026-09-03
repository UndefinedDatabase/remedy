"""
Model routing by task class for Remedy (F110).

Owns the CLASS TABLE — which model TIER a declared task class is routed to — the
THREE HARD RULES of docs/agents/model_routing_policy.md as named checks, each
returning ITS OWN rule name when a routing choice violates it, and the PER-PROJECT
OVERRIDE SCHEMA that validates a whole override map against those rules BEFORE it
is applied. Nothing else yet: no config file is read, no model id is named and no
call site routes through it.
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

Remedy deliberately does not READ A CONFIG FILE here, and the per-project override
map is a MAPPING PASSED IN rather than one this module loads. A reader searching
here for the loader that turns a project's TOML table into that mapping will not
find it: it arrives with the resolver-seam round, alongside the per-call-site
class declarations, because the schema is worth pinning BEFORE anything can be
configured to break it. packages/orchestration/config.py is deliberately NOT
imported — every function below stays a pure function of its arguments, which is
what lets the override rules be tested without a config file existing at all.

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
    OVERRIDE_REASON: reason recorded when an OVERRIDE supplied the tier
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
    REVIEWER_WORKER_CLASS_PAIRS: the declared (worker, reviewer) class pairs
    RULE_OVERRIDE_UNKNOWN_TASK_CLASS: schema-rule name, an override naming a
        task class the seed table does not
    RULE_OVERRIDE_UNKNOWN_TIER: schema-rule name, an override naming a tier
        MODEL_TIERS does not
    OVERRIDE_SCHEMA_RULE_NAMES: the two above, in report order
    OVERRIDE_VIOLATION_RULE_NAMES: schema names then HARD_RULE_NAMES — the
        order an override map's violations are reported in
    OverrideViolation: frozen (task_class, rule_name) record of one violation
    OverrideRefused: the exception a refused override map raises
    validate_task_class_tier_overrides(overrides, classes)
        -> tuple[OverrideViolation, ...] of EVERY violation in the map
    build_effective_task_class_tiers(overrides, classes) -> dict[str, str],
        raising OverrideRefused rather than dropping a violating entry
    resolve_task_class_tier_with_overrides(task_class, effective_tiers)
        -> tuple[str, str], the reason DERIVED by comparison with the seed
"""

from __future__ import annotations

from dataclasses import dataclass

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

#: Recorded when a PER-PROJECT OVERRIDE, and not the seed mapping, supplied the
#: class's tier. A fixed token for the same reason its two siblings above are:
#: evidence readers GROUP on the reason, so "which of this run's calls were routed
#: by a project's own override rather than by the shipped policy?" is a filter
#: rather than a prose search. :func:`resolve_task_class_tier_with_overrides`
#: DERIVES this reason by comparing against :data:`TASK_CLASS_TIERS` instead of
#: asserting it, so an override that merely restates the seed tier still reports
#: :data:`SEED_MAPPING_REASON`.
OVERRIDE_REASON: str = "per_project_override"


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
#: every job it plans.
#:
#: THIS SET IS DELIBERATELY WIDER THAN THE FEATURE FILE'S TWO LITERAL CALL KINDS,
#: and that is not drift — it is DECISION F110 D2, taken at the F110 R5 gate and
#: recorded in .agent/decisions.md. docs/roadmap/features/T3_F110.md names
#: "orchestrator and mission-compile calls"; ``mission`` is here as well because
#: :data:`TASK_CLASS_TIERS` already routes ``mission`` to the top tier, and THAT
#: SEED ENTRY IS EXACTLY THE PROPERTY A PER-PROJECT OVERRIDE CAN MOVE. Membership
#: here is what turns that top-tier routing from a table entry an override could
#: quietly demote into a CHECKED rule that refuses the override by name. The
#: policy-document sync test cannot reach an override at all — it guards the
#: TABLE against the DOCUMENT — so without this entry the demotion had no guard.
#: A reader comparing this set to the feature file's sentence reads that
#: DECISION, not a rename.
ORCHESTRATION_TASK_CLASSES: frozenset[str] = frozenset(
    {
        normalize_task_class("orchestrator"),
        normalize_task_class("mission compile"),
        normalize_task_class("mission"),
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


# ---------------------------------------------------------------------------
# The per-project override schema — F110 T002c
# ---------------------------------------------------------------------------
# docs/roadmap/features/T3_F110.md: "per-project overrides allowed but hard rules
# always win. Violating overrides fail config validation with the rule named."
# Everything below takes the override map as an ARGUMENT; see the module
# docstring for why no config file is read here.

#: The declared (WORKER class, REVIEWER class) pairs, so policy hard rule 1 —
#: "a reviewer is never routed weaker than the worker it reviews" — is checkable
#: against a TABLE rather than only against a per-call pairing an operator has to
#: remember to supply. An override map names classes, not calls, so without this
#: table nothing could tell that lowering ``standard_review`` alone breaks a pair.
#:
#: Seeded with the ONE pair the seed mapping supports today. EVERY MEMBER OF EVERY
#: PAIR MUST BE A KEY OF :data:`TASK_CLASS_TIERS` — a pair naming a class the seed
#: table does not would be silently unjudgeable, so a test pins that property.
REVIEWER_WORKER_CLASS_PAIRS: tuple[tuple[str, str], ...] = (
    ("standard_build", "standard_review"),
)

#: Violated when an override names a task class :data:`TASK_CLASS_TIERS` does not.
#:
#: WHY THIS IS REFUSED RATHER THAN IGNORED, which is the non-obvious half: the
#: RESOLVER routes an undeclared class conservatively at call time
#: (:data:`UNKNOWN_CLASS_REASON`, to :data:`TOP_TIER`), so nothing is unsafe about
#: an undeclared class arriving at a call. But an OVERRIDE for a class NOBODY
#: DECLARES is dead config: it can never match anything, it silently does nothing,
#: and the operator who wrote it believes a tier moved when no tier moved. That is
#: the casual mapping edit this feature exists to stop, one file over — so the
#: config is refused and the operator is told which key is dead.
RULE_OVERRIDE_UNKNOWN_TASK_CLASS: str = "override_unknown_task_class"

#: Violated when an override names a tier :data:`MODEL_TIERS` does not. A typo'd
#: tier cannot be ranked, and ranking it would RAISE by design
#: (:func:`model_tier_rank`), so it is reported as a schema fault instead.
RULE_OVERRIDE_UNKNOWN_TIER: str = "override_unknown_tier"

#: The two schema-rule names, in the order they are reported.
#:
#: HARD_RULE_NAMES IS DELIBERATELY NOT EXTENDED WITH THESE. A schema fault is a
#: MALFORMED CONFIG — a typo — while a hard-rule violation is a POLICY BREACH by a
#: config that is perfectly well formed. Merging the two vocabularies would let a
#: misspelling be reported as a policy breach, and
#: :data:`HARD_RULE_NAMES` is pinned by its own test at exactly the three names
#: the policy document carries.
OVERRIDE_SCHEMA_RULE_NAMES: tuple[str, ...] = (
    RULE_OVERRIDE_UNKNOWN_TASK_CLASS,
    RULE_OVERRIDE_UNKNOWN_TIER,
)

#: The FIXED, DECLARED order an override map's violations are reported in: the
#: SCHEMA names first, then the hard-rule names. Schema first because a malformed
#: entry is what an operator must fix before any policy reading of it means
#: anything.
#:
#: Like :data:`HARD_RULE_NAMES`, this order is deliberately INDEPENDENT of
#: :data:`MODEL_TIERS`, for the reason that constant already states: re-tiering the
#: model vocabulary must not reshuffle an operator's error list, because a list
#: that reorders itself reads as a different set of problems.
OVERRIDE_VIOLATION_RULE_NAMES: tuple[str, ...] = OVERRIDE_SCHEMA_RULE_NAMES + HARD_RULE_NAMES


# WHY A RECORD AND NOT A MESSAGE: "refused with the rule named"
# (docs/roadmap/features/T3_F110.md, Acceptance) has to be something a CALLER CAN
# BRANCH ON. A prose sentence would have to be parsed back apart by anything that
# wanted to act on it, and would go stale the first time somebody reworded it.
@dataclass(frozen=True)
class OverrideViolation:
    """One violation found in an override map: WHICH class, and WHICH rule.

    ``task_class`` is the normalized key the violation is attributed to, so an
    operator is pointed at the entry to change rather than at the map as a whole.
    ``rule_name`` is one of :data:`OVERRIDE_VIOLATION_RULE_NAMES`.
    """

    task_class: str
    rule_name: str


# WHY: dropping a violating entry would leave the operator believing it took
# effect; see the builder's docstring, which states the reason this exception
# exists at all.
class OverrideRefused(Exception):
    """Raised when an override map violates the schema or a hard rule.

    Carries the :class:`OverrideViolation` records it was raised for on
    ``.violations``, so a caller reads STRUCTURE rather than re-parsing the
    message; the message itself names every violated rule, for the operator who
    only ever sees a traceback.
    """

    def __init__(self, violations: tuple[OverrideViolation, ...]) -> None:
        self.violations = violations
        named = ", ".join(f"{v.task_class}: {v.rule_name}" for v in violations)
        super().__init__(f"per-project model-routing overrides refused — {named}")


# WHY: an operator fixing a config one violation per round trip fixes it four
# times; this returns EVERY violation in the whole map at once, in one declared
# order, so the error list reads the same way twice.
def validate_task_class_tier_overrides(
    overrides: dict[str, str],
    safety_relevant_classes: frozenset[str] = SAFETY_RELEVANT_CLASSES,
) -> tuple[OverrideViolation, ...]:
    """Return EVERY violation in an override map, in :data:`OVERRIDE_VIOLATION_RULE_NAMES` order.

    ``overrides`` maps a task class to the tier a project wants it routed to; the
    keys pass through :func:`normalize_task_class`, so a project may spell a class
    in the policy document's own wording.

    THE HARD RULES ARE JUDGED AGAINST THE **EFFECTIVE** TABLE — the override map
    laid over :data:`TASK_CLASS_TIERS` — and never against the override map alone.
    That is what catches an override lowering only the REVIEWER half of a pair in
    :data:`REVIEWER_WORKER_CLASS_PAIRS`: the worker half is still the seed tier,
    and comparing the two requires both.

    A SCHEMA-FAULTY ENTRY IS REPORTED AND THEN NOT JUDGED against the hard rules.
    Ranking a tier :data:`MODEL_TIERS` does not name RAISES by design
    (:func:`model_tier_rank`), so a typo'd tier would crash a policy check that
    tried to read it; reporting the typo and leaving that entry out of the
    effective table is what makes a malformed config REPORTABLE rather than fatal.

    ``safety_relevant_classes`` defaults to :data:`SAFETY_RELEVANT_CLASSES`, which
    is EMPTY in production today, for exactly the reason
    :func:`check_safety_relevant_class_not_below_mid_tier` states: a rule that
    cannot fail is not a rule, so the parameter lets a test supply a FIXTURE set
    and prove the refusal really happens.

    Each violation's ``rule_name`` is the value a check RETURNED wherever a check
    exists — the three hard-rule checks are called, never re-labelled — which is
    the discipline :func:`validate_routing_choice` already states. The two schema
    names have no check function of their own and are the only names this function
    supplies directly.
    """
    normalized: dict[str, str] = {
        normalize_task_class(task_class): tier for task_class, tier in overrides.items()
    }

    found: list[OverrideViolation] = []
    sound: dict[str, str] = {}
    for task_class, tier in normalized.items():
        faulty = False
        if task_class not in TASK_CLASS_TIERS:
            found.append(OverrideViolation(task_class, RULE_OVERRIDE_UNKNOWN_TASK_CLASS))
            faulty = True
        if tier not in MODEL_TIERS:
            found.append(OverrideViolation(task_class, RULE_OVERRIDE_UNKNOWN_TIER))
            faulty = True
        if not faulty:
            sound[task_class] = tier

    effective = dict(TASK_CLASS_TIERS)
    effective.update(sound)

    for task_class in sorted(effective):
        tier = effective[task_class]
        returned = check_orchestration_class_routed_to_top_tier(task_class, tier)
        if returned is not None:
            found.append(OverrideViolation(task_class, returned))
        returned = check_safety_relevant_class_not_below_mid_tier(
            task_class, tier, safety_relevant_classes
        )
        if returned is not None:
            found.append(OverrideViolation(task_class, returned))

    for worker_class, reviewer_class in REVIEWER_WORKER_CLASS_PAIRS:
        worker_tier = effective.get(worker_class)
        reviewer_tier = effective.get(reviewer_class)
        if worker_tier is None or reviewer_tier is None:
            continue
        returned = check_reviewer_not_weaker_than_worker(worker_tier, reviewer_tier)
        if returned is not None:
            # Attributed to the REVIEWER class: that is the entry an operator must
            # change, because raising the worker to match would spend more money to
            # fix a rule about the reviewer.
            found.append(OverrideViolation(reviewer_class, returned))

    ordered: list[OverrideViolation] = []
    for rule_name in OVERRIDE_VIOLATION_RULE_NAMES:
        ordered.extend(
            sorted(
                (v for v in found if v.rule_name == rule_name),
                key=lambda v: v.task_class,
            )
        )
    return tuple(ordered)


# WHY: this is the ONE place an override map becomes a routing table, so it is the
# one place the hard rules can still win before anything routes.
def build_effective_task_class_tiers(
    overrides: dict[str, str],
    safety_relevant_classes: frozenset[str] = SAFETY_RELEVANT_CLASSES,
) -> dict[str, str]:
    """Return :data:`TASK_CLASS_TIERS` overlaid with ``overrides``, or REFUSE the map.

    The override keys are normalized through :func:`normalize_task_class`, the
    whole map is validated by :func:`validate_task_class_tier_overrides`, and if
    there is ANY violation at all this raises :class:`OverrideRefused` carrying
    every one of them.

    WHY IT RAISES RATHER THAN DROPPING THE OFFENDING ENTRY: a silently dropped
    override leaves the operator believing it took effect, which is the silent
    downgrade policy hard rule 2 forbids. The hard rules win by REFUSING the
    config, not by quietly editing it.

    The returned table is a NEW dict; :data:`TASK_CLASS_TIERS` is never mutated,
    so the shipped seed mapping stays the one thing the policy-document sync test
    can compare the document against.
    """
    normalized: dict[str, str] = {
        normalize_task_class(task_class): tier for task_class, tier in overrides.items()
    }
    violations = validate_task_class_tier_overrides(normalized, safety_relevant_classes)
    if violations:
        raise OverrideRefused(violations)
    effective = dict(TASK_CLASS_TIERS)
    effective.update(normalized)
    return effective


# WHY A SIBLING AND NOT A FLAG ON resolve_task_class_tier: that function answers
# from the SHIPPED table and its behaviour is pinned by round 4's tests; this one
# answers from a table a project built, and the two reasons differ.
def resolve_task_class_tier_with_overrides(
    task_class: str,
    effective_tiers: dict[str, str],
) -> tuple[str, str]:
    """Return ``(tier, reason)`` for ``task_class`` against an EFFECTIVE table.

    ``effective_tiers`` is what :func:`build_effective_task_class_tiers` returned.

    THE REASON IS DERIVED BY COMPARISON, NEVER ASSERTED. A class the effective
    table does not name answers ``(TOP_TIER, UNKNOWN_CLASS_REASON)``, exactly as
    :func:`resolve_task_class_tier` does. A class it does name answers
    :data:`OVERRIDE_REASON` only when the tier DIFFERS from
    :data:`TASK_CLASS_TIERS`, and :data:`SEED_MAPPING_REASON` when it agrees — so
    an override that merely restates the seed tier is honestly reported as the
    seed mapping rather than as a project decision nobody actually made.
    """
    key = normalize_task_class(task_class)
    tier = effective_tiers.get(key)
    if tier is None:
        return TOP_TIER, UNKNOWN_CLASS_REASON
    if tier != TASK_CLASS_TIERS.get(key):
        return tier, OVERRIDE_REASON
    return tier, SEED_MAPPING_REASON
