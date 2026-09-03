"""
Model routing by task class for Remedy (F110).

Owns the CLASS TABLE — which model TIER a declared task class is routed to — the
THREE HARD RULES of docs/agents/model_routing_policy.md as named checks, each
returning ITS OWN rule name when a routing choice violates it, the PER-PROJECT
OVERRIDE SCHEMA that validates a whole override map against those rules BEFORE it
is applied, the PROMOTION-EVIDENCE DISCIPLINE that refuses a move to a
CHEAPER tier unless a documented benchmark run backs it, and — new in T001 — the
ROLE-TO-CLASS INVENTORY that gives every role Remedy resolves a runtime
configuration for a DECLARED task class, together with the SINGLE ROUTING SEAM
every provider call site invokes. Nothing else yet: no config file is read and
no model id is named.
The table is SEEDED from the "Seed mapping" section of
docs/agents/model_routing_policy.md, which remains the human-readable policy.
tests/orchestration/test_model_routing.py parses that section and asserts the
parsed mapping EQUALS :data:`TASK_CLASS_TIERS`, so the document and this table
cannot drift apart silently — that sync test is an explicit acceptance line of
docs/roadmap/features/T3_F110.md.

THE PROMOTION BARS ARE SEEDED THE SAME WAY, from that document's "Promotion rule"
section rather than from a hand-typed number, exactly as the table is seeded from
its "Seed mapping" section. The same test file parses that section and asserts the
parsed runs count, the two parsed percentages and the parsed logged-per-run field
list EQUAL the constants below, so lowering a bar in the code without lowering it
in the policy is a RED TEST rather than a quiet saving.

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

Remedy deliberately does not CALL :func:`promotion_evidence_from_mapping` from
anywhere in production yet, and a reader searching for its caller should find
this sentence rather than a silence. The parser turns the raw
``model_routing.promotion_evidence`` config table into
:class:`PromotionEvidence` records, and the call that hands it that table arrives
with the wiring round, in ``packages/orchestration/role_config.py`` beside
``resolve_effective_task_class_tiers`` — the config-reading layer, which is
already where the per-project TIERS table is read. The schema lands a round
BEFORE its reader on purpose, so it is pinned before routing behaviour moves
against it.

THE SEAM IS WIRED IN EXACTLY ONE PLACE, and a reader searching for where a call
routes must go there: ``packages/orchestration/role_config.resolve_role_config``
calls :func:`route_role_call` and carries what it returned on the ``RoleConfig``
it already hands back. That ONE call site reaches all seven entries of
:data:`ROLE_CONFIG_CALL_SITES`, because all seven already funnel through that
resolver — so routing is the DEFAULT for a provider call rather than something
each site has to remember, and a new site that resolves a role is routed the day
it lands. Nothing else calls :func:`route_role_call` in production, which is why
the inventory below is unmoved by the wiring: it changes what that resolver DOES,
not how many times it is called.

Remedy deliberately does not IMPORT packages/orchestration/role_config.py here,
even though this module now declares a task class for every role that module
knows. model_routing is the POLICY layer and role_config the CONFIG layer, and
this docstring already forbids that same inversion for config.py. The coupling is
enforced BY A TEST instead (tests/orchestration/test_model_routing.py), which is
STRONGER than an import would be: an import fails only when something is MISSING,
while the test fails when the two role sets DISAGREE IN EITHER DIRECTION — a role
added to ``KNOWN_ROLES`` with no declared class, or a class declared here for a
role nobody configures.

Remedy deliberately does not give ``mission_compile`` a role or a call site.
It is a declared member of :data:`ORCHESTRATION_TASK_CLASSES`, so a reader who
searches for the call site that declares it will find none: missions are compiled
OUTSIDE the role-config surface, so there is no role to map and no
``resolve_role_config`` call to inventory. That absence is deliberate and stated
here rather than left to be rediscovered.

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
    PROMOTION_MINIMUM_RUNS_PER_FIXTURE: the policy's runs-per-fixture bar
    PROMOTION_MINIMUM_BLOCK_ASSERTION_PASS_RATE: its block-level bar, PERCENT
    PROMOTION_MINIMUM_OVERALL_PASS_RATE: its overall bar, PERCENT
    PROMOTION_EVIDENCE_COMPOUND_FIELD_SEPARATOR: the ONE document-to-code split
    PROMOTION_EVIDENCE_DOCUMENT_FIELDS: the document's own logged-per-run names
    PromotionAssertionResults: frozen (block_level_pass_rate, overall_pass_rate)
    PromotionEvidence: frozen record of ONE documented benchmark run
    RULE_PROMOTION_WITHOUT_EVIDENCE: promotion-rule name, no evidence at all
    RULE_PROMOTION_EVIDENCE_INCOMPLETE: promotion-rule name, a document field
        of PROMOTION_EVIDENCE_DOCUMENT_FIELDS left unset
    RULE_PROMOTION_EVIDENCE_BELOW_THRESHOLD: promotion-rule name, a bar unmet
    PROMOTION_RULE_NAMES: the three above, in report order
    is_task_class_promotion(task_class, tier) -> bool — CHEAPER than the seed
    check_promotion_backed_by_evidence(task_class, tier, evidence)
    PROMOTION_EVIDENCE_NESTED_FIELD: the one field that is itself a table
    PROMOTION_EVIDENCE_ENTRY_FIELD_TYPES: the raw type each other field reads as
    promotion_evidence_from_mapping(raw_evidence) -> dict[str, PromotionEvidence]
        — the PURE parser; a malformed entry is SKIPPED, never guessed at
    OVERRIDE_VIOLATION_RULE_NAMES: schema names, then HARD_RULE_NAMES, then
        PROMOTION_RULE_NAMES — the order an override map's violations are
        reported in
    OverrideViolation: frozen (task_class, rule_name) record of one violation
    OverrideRefused: the exception a refused override map raises
    validate_task_class_tier_overrides(overrides, classes, promotion_evidence)
        -> tuple[OverrideViolation, ...] of EVERY violation in the map
    build_effective_task_class_tiers(overrides, classes, promotion_evidence)
        -> dict[str, str], raising OverrideRefused rather than dropping a
        violating entry
    resolve_task_class_tier_with_overrides(task_class, effective_tiers)
        -> tuple[str, str], the reason DERIVED by comparison with the seed
    ROUTED_CALL_EVIDENCE_FIELDS: the keys a routed call records
    routed_call_evidence_fields(task_class, effective_tiers, promotion_evidence)
        -> dict[str, str | None], the mapping a routed call records
    ROLE_TASK_CLASSES: the T001 inventory — role -> the class its calls declare
    TASK_CLASS_INHERITING_ROLES: the roles that INHERIT the originating class
    UNDECLARED_ROLE_TASK_CLASS: the class a role nobody declared answers with
    OriginatingTaskClassRequired: raised when an inheriting role is given none
    resolve_role_task_class(role, originating_task_class) -> str
    route_role_call(role, originating_task_class, effective_tiers,
        promotion_evidence) -> dict[str, str | None] — THE SEAM
    ROLE_CONFIG_RESOLVER_NAME: the role_config function the inventory swept for
    DYNAMIC_ROLE_MARKER: stands where a call site passes a role VARIABLE
    ROLE_CONFIG_CALL_SITES: the (path, role-or-marker) call-site inventory
"""

from __future__ import annotations

import warnings
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

# ---------------------------------------------------------------------------
# The promotion-evidence discipline — F110 T003
# ---------------------------------------------------------------------------
# docs/agents/model_routing_policy.md, "Promotion rule (evidence over claims, P1)":
# "A model may be promoted into a task class only after a documented benchmark run
# on the F082 corpus (or the class's frozen fixtures)". Everything below is that
# sentence turned into a refusal a caller can branch on. The evidence map, like the
# override map, is PASSED IN; see the module docstring for why no config file is
# read here.

#: MINIMUM RUNS PER FIXTURE. From the policy document's "Promotion rule" bullet
#: "each fixture run 3× (small models are high-variance)". SEEDED from that
#: sentence and pinned to it by the promotion-rule sync test in
#: tests/orchestration/test_model_routing.py — lowering it here without lowering it
#: in the document is a red test, which is the whole point of the bar living in
#: two places.
PROMOTION_MINIMUM_RUNS_PER_FIXTURE: int = 3

#: MINIMUM BLOCK-LEVEL ASSERTION PASS RATE, IN PERCENT. From the same section's
#: bullet "pass thresholds: ≥90% on block-level assertions, ≥75% overall" — this is
#: the first of that bullet's two numbers. Percent and not a fraction because the
#: document writes percent, and the sync test compares the parsed number to this
#: constant directly rather than through a conversion nobody maintains.
PROMOTION_MINIMUM_BLOCK_ASSERTION_PASS_RATE: int = 90

#: MINIMUM OVERALL PASS RATE, IN PERCENT. The second number of that same bullet,
#: "≥75% overall", carried for the same reason and compared the same way.
PROMOTION_MINIMUM_OVERALL_PASS_RATE: int = 75

#: THE ONE TRANSLATION BETWEEN THE DOCUMENT AND THE CODE, DECLARED HERE BECAUSE A
#: SILENT ONE WOULD TURN THE SYNC TEST INTO A TAUTOLOGY. The document's
#: "logged per run" bullet carries one COMPOUND phrase, "model id + quantization",
#: which is two logged names written as one item; the sync test splits on this
#: separator before normalizing, and every other item passes through
#: :func:`normalize_task_class` untouched. A reader who wonders why the document
#: lists six items and this module names seven fields reads exactly this constant.
PROMOTION_EVIDENCE_COMPOUND_FIELD_SEPARATOR: str = " + "

#: THE DOCUMENT'S OWN FIELD LIST — the names the "logged per run" bullet of the
#: "Promotion rule" section carries, normalized through
#: :func:`normalize_task_class` and split on
#: :data:`PROMOTION_EVIDENCE_COMPOUND_FIELD_SEPARATOR`, in the document's order.
#: The sync test asserts the parsed bullet EQUALS this tuple, so a field added to
#: or dropped from the policy is a red test rather than an undetected divergence.
PROMOTION_EVIDENCE_DOCUMENT_FIELDS: tuple[str, ...] = (
    "model_id",
    "quantization",
    "prompt_hash",
    "tokens",
    "cost",
    "assertion_results",
    "reviewer_verdict",
)


# WHY THE TWO RATES LIVE INSIDE "assertion results" AND NOT BESIDE IT: the document
# names "assertion results" as ONE logged field, and its "pass thresholds" bullet
# states two READINGS of that field. Nesting them keeps
# PROMOTION_EVIDENCE_DOCUMENT_FIELDS exactly what the document says, which is what
# lets the sync test be a straight comparison.
@dataclass(frozen=True)
class PromotionAssertionResults:
    """The two pass rates a benchmark run reports, both IN PERCENT.

    ``block_level_pass_rate`` is compared against
    :data:`PROMOTION_MINIMUM_BLOCK_ASSERTION_PASS_RATE` and
    ``overall_pass_rate`` against :data:`PROMOTION_MINIMUM_OVERALL_PASS_RATE`.
    """

    block_level_pass_rate: int
    overall_pass_rate: int


# WHY A RECORD AND NOT A DICT: "with evidence logged"
# (docs/roadmap/features/T3_F110.md, T003) has to be something a check can read
# field by field; a dict would let a typo'd key read as an absent field and turn a
# missing measurement into a silent pass.
@dataclass(frozen=True)
class PromotionEvidence:
    """ONE documented benchmark run, as the policy's "Promotion rule" describes it.

    The first seven fields are EXACTLY :data:`PROMOTION_EVIDENCE_DOCUMENT_FIELDS`,
    every one of them defaulting to ``None`` so that "unset" is a state the
    completeness check can see rather than a constructor error a caller routes
    around.

    ``runs_per_fixture`` AND ``corpus`` ARE DELIBERATELY NOT IN THAT TUPLE. The
    document names both in the PROSE of the section — "each fixture run 3×" and
    "on the F082 corpus (or the class's frozen fixtures)" — and NOT in its
    "logged per run" bullet, so listing them among the document's field names
    would make the sync test assert something the document does not say. They are
    carried here because the promotion check needs the run count and the run
    reference needs the corpus, and they are checked and reported on their own
    terms.
    """

    model_id: str | None = None
    quantization: str | None = None
    prompt_hash: str | None = None
    tokens: int | None = None
    cost: float | None = None
    assertion_results: PromotionAssertionResults | None = None
    reviewer_verdict: str | None = None
    runs_per_fixture: int = 0
    corpus: str | None = None

    def promotion_run_reference(self) -> str:
        """Return a short reference LOCATING this benchmark run.

        A routed call records this string and not the record itself: evidence
        readers need to find the run, not to carry a copy of it, and a copy would
        grow every routed call by the whole measurement.
        """
        return (
            f"{self.model_id}{PROMOTION_EVIDENCE_COMPOUND_FIELD_SEPARATOR}"
            f"{self.quantization}@{self.prompt_hash} on {self.corpus}"
        )


#: Violated when a class is promoted to a CHEAPER tier with NO evidence at all.
#: The plainest form of the policy's "evidence over claims": the mapping edit this
#: feature exists to stop is the one nobody measured.
RULE_PROMOTION_WITHOUT_EVIDENCE: str = "promotion_without_evidence"

#: Violated when evidence is present but a field of
#: :data:`PROMOTION_EVIDENCE_DOCUMENT_FIELDS` is unset. Reported apart from the
#: name above because the two ask different things of an operator: one says
#: "measure it", the other says "you measured it and did not log all of it".
RULE_PROMOTION_EVIDENCE_INCOMPLETE: str = "promotion_evidence_incomplete"

#: Violated when evidence is complete but a bar is unmet — the runs count, the
#: block-level pass rate or the overall pass rate. The document's own consequence:
#: "Below threshold, the class stays on the stronger tier."
RULE_PROMOTION_EVIDENCE_BELOW_THRESHOLD: str = "promotion_evidence_below_threshold"

#: The three promotion-rule names, in the order violations are reported.
#:
#: WHY THEY ARE THEIR OWN CLASS AND NOT HARD RULES. A HARD RULE IS NEVER
#: SATISFIABLE BY EVIDENCE — no benchmark buys a reviewer weaker than the worker it
#: reviews — while a PROMOTION RULE is precisely a rule that EVIDENCE DISCHARGES.
#: Merging the two vocabularies would let a measured, documented promotion read as
#: a policy breach, and would let an operator believe a benchmark could rescue an
#: entry no benchmark can rescue. :data:`HARD_RULE_NAMES` and
#: :data:`OVERRIDE_SCHEMA_RULE_NAMES` are therefore left exactly as they are, each
#: pinned by its own test.
PROMOTION_RULE_NAMES: tuple[str, ...] = (
    RULE_PROMOTION_WITHOUT_EVIDENCE,
    RULE_PROMOTION_EVIDENCE_INCOMPLETE,
    RULE_PROMOTION_EVIDENCE_BELOW_THRESHOLD,
)


# WHY ONLY CHEAPER: the policy's promotion rule is about SPENDING LESS, and a move
# to a STRONGER tier costs money rather than quality, so it needs no benchmark to
# justify it.
def is_task_class_promotion(task_class: str, tier: str) -> bool:
    """Return whether routing ``task_class`` to ``tier`` is a PROMOTION.

    True only when ``tier`` ranks STRICTLY BELOW the tier
    :data:`TASK_CLASS_TIERS` seeds for that class — cheaper, in the vocabulary
    :data:`MODEL_TIERS` orders.

    False for a class the seed table does not name: that is a SCHEMA fault
    (:data:`RULE_OVERRIDE_UNKNOWN_TASK_CLASS`) and never a promotion, and reading
    it as one would report a dead config key as an unmeasured saving. False, too,
    for a move to an equal or stronger tier.
    """
    key = normalize_task_class(task_class)
    seeded = TASK_CLASS_TIERS.get(key)
    if seeded is None:
        return False
    return model_tier_rank(tier) < model_tier_rank(seeded)


# WHY: "a promotion without evidence refused, with evidence logged"
# (docs/roadmap/features/T3_F110.md, T003) — and the three ways evidence can fail
# ask three different things of an operator, so each gets its own name.
def check_promotion_backed_by_evidence(
    task_class: str,
    tier: str,
    evidence: PromotionEvidence | None = None,
) -> str | None:
    """Return the promotion-rule name a promotion VIOLATES, or ``None``.

    ``None`` outright when :func:`is_task_class_promotion` says the change is not
    a promotion — the rule simply does not speak about a move that costs more.

    Otherwise, in order: no evidence at all is
    :data:`RULE_PROMOTION_WITHOUT_EVIDENCE`; evidence with ANY field of
    :data:`PROMOTION_EVIDENCE_DOCUMENT_FIELDS` unset is
    :data:`RULE_PROMOTION_EVIDENCE_INCOMPLETE`; and evidence whose
    ``runs_per_fixture`` or either pass rate falls below its bar is
    :data:`RULE_PROMOTION_EVIDENCE_BELOW_THRESHOLD`. ``None`` when the run meets
    every bar, which is the shape every check in this module shares: a rule name
    is a refusal, ``None`` is a pass.

    THE BARS ARE ``>=`` AND NOT ``>``, because the document writes "≥90%" and
    "≥75%" and "run 3×": a run exactly AT a bar is a run that met it.
    """
    if not is_task_class_promotion(task_class, tier):
        return None
    if evidence is None:
        return RULE_PROMOTION_WITHOUT_EVIDENCE
    for field_name in PROMOTION_EVIDENCE_DOCUMENT_FIELDS:
        if getattr(evidence, field_name) is None:
            return RULE_PROMOTION_EVIDENCE_INCOMPLETE
    if evidence.runs_per_fixture < PROMOTION_MINIMUM_RUNS_PER_FIXTURE:
        return RULE_PROMOTION_EVIDENCE_BELOW_THRESHOLD
    results = evidence.assertion_results
    if results.block_level_pass_rate < PROMOTION_MINIMUM_BLOCK_ASSERTION_PASS_RATE:
        return RULE_PROMOTION_EVIDENCE_BELOW_THRESHOLD
    if results.overall_pass_rate < PROMOTION_MINIMUM_OVERALL_PASS_RATE:
        return RULE_PROMOTION_EVIDENCE_BELOW_THRESHOLD
    return None


# ---------------------------------------------------------------------------
# Reading promotion evidence out of a RAW MAPPING — F110 T003
# ---------------------------------------------------------------------------
# A project WRITES DOWN the benchmark run that licenses a cheaper tier, and a
# config table hands it here as plain strings, numbers and nested tables. This
# section is the ONE place such a mapping becomes PromotionEvidence records. It
# stays a pure function of its argument for the reason the module docstring
# gives: it reads no config file and imports nothing that does.

#: The field of :class:`PromotionEvidence` that is itself a NESTED TABLE, read
#: into a :class:`PromotionAssertionResults` of its own rather than into a scalar.
#: Named as a constant because :func:`promotion_evidence_from_mapping` and the
#: tests both need it, and a retyped literal in either would let a rename land
#: with a test still passing against the dead spelling.
PROMOTION_EVIDENCE_NESTED_FIELD: str = "assertion_results"

#: THE RAW TYPE EACH FIELD OF :class:`PromotionEvidence` IS READ FROM,
#: :data:`PROMOTION_EVIDENCE_NESTED_FIELD` excepted because it is a table and not
#: a reading. DECLARED RATHER THAN DERIVED FROM THE DATACLASS: this module runs
#: under ``from __future__ import annotations``, so a field's annotation is the
#: STRING ``"int | None"`` and deriving the type would mean evaluating annotations
#: back into types at import time. tests/orchestration/test_model_routing.py
#: asserts these names are EXACTLY the record's own fields minus that one, so a
#: field added to :class:`PromotionEvidence` without a reading here is a red test
#: rather than a value silently dropped on the floor.
PROMOTION_EVIDENCE_ENTRY_FIELD_TYPES: dict[str, type] = {
    "model_id": str,
    "quantization": str,
    "prompt_hash": str,
    "tokens": int,
    "cost": float,
    "reviewer_verdict": str,
    "runs_per_fixture": int,
    "corpus": str,
}


# WHY A BOOLEAN IS NEVER A READING: ``bool`` is a subclass of ``int`` in Python,
# so a TOML ``tokens = true`` would pass a bare isinstance check and land in the
# record as 1. An int is accepted where a float is wanted — TOML writes ``0`` for
# a free run and that is a cost — and widened, so the record carries the number
# the mapping carried.
def _promotion_evidence_reading(value: object, expected: type) -> object | None:
    """Return ``value`` as ``expected``, or ``None`` when it is not readable as one."""
    if isinstance(value, bool):
        return None
    if expected is float and isinstance(value, int):
        return float(value)
    if isinstance(value, expected):
        return value
    return None


def _promotion_assertion_results_from_mapping(
    raw: dict[str, object],
) -> PromotionAssertionResults | None:
    """Return the two readings ``raw`` carries, or ``None`` if it carries neither shape.

    THE FIELD NAMES ARE READ FROM :class:`PromotionAssertionResults` ITSELF and
    never spelled here, so renaming a reading moves this parser with it. They are
    read off ``__dataclass_fields__`` rather than through ``dataclasses.fields``
    because this module imports nothing beyond ``dataclass`` itself and stays
    that way. Both fields are required because the record has no defaults for
    them: a table missing one is not half a measurement, it is an unreadable one.
    """
    read: dict[str, object] = {}
    for field_name in PromotionAssertionResults.__dataclass_fields__:
        if field_name not in raw:
            return None
        reading = _promotion_evidence_reading(raw[field_name], int)
        if reading is None:
            return None
        read[field_name] = reading
    return PromotionAssertionResults(**read)  # type: ignore[arg-type]


def _promotion_evidence_from_entry(entry: dict[str, object]) -> PromotionEvidence | None:
    """Return the record ``entry`` describes, or ``None`` when it cannot be read."""
    read: dict[str, object] = {}
    for field_name, expected in PROMOTION_EVIDENCE_ENTRY_FIELD_TYPES.items():
        if field_name not in entry:
            continue
        reading = _promotion_evidence_reading(entry[field_name], expected)
        if reading is None:
            return None
        read[field_name] = reading
    if PROMOTION_EVIDENCE_NESTED_FIELD in entry:
        raw_results = entry[PROMOTION_EVIDENCE_NESTED_FIELD]
        if not isinstance(raw_results, dict):
            return None
        results = _promotion_assertion_results_from_mapping(raw_results)
        if results is None:
            return None
        read[PROMOTION_EVIDENCE_NESTED_FIELD] = results
    return PromotionEvidence(**read)  # type: ignore[arg-type]


# WHY A MALFORMED ENTRY IS SKIPPED HERE AND A MALFORMED OVERRIDE IS REFUSED
# LOUDLY, WHICH LOOKS LIKE TWO ANSWERS TO ONE QUESTION AND IS NOT. A missing
# evidence record means the promotion it would have licensed is REFUSED by
# check_promotion_backed_by_evidence with RULE_PROMOTION_WITHOUT_EVIDENCE, so a
# malformed record FAILS CLOSED — the class keeps its seeded, stronger tier and
# the project pays money rather than quality. A malformed OVERRIDE fails the
# other way: dropping it would leave the operator believing a re-tier took
# effect, which is the silent downgrade policy hard rule 2 forbids, so
# build_effective_task_class_tiers raises instead. Both refuse to act on input
# they do not understand; they differ only in which direction is conservative.
def promotion_evidence_from_mapping(
    raw_evidence: dict[str, object],
) -> dict[str, PromotionEvidence]:
    """Return the :class:`PromotionEvidence` records ``raw_evidence`` describes.

    ``raw_evidence`` is the RAW mapping a config table produces — task class to
    a table of readings — and this function is a PURE function of it: no config
    file is read here, exactly as the module docstring promises for everything
    in this module. The returned mapping is keyed by NORMALIZED task class,
    through :func:`normalize_task_class`, precisely as
    :func:`validate_task_class_tier_overrides` normalizes the keys of an override
    map, so a project may spell a class in the policy document's own wording in
    both tables.

    AN ENTRY THAT CANNOT BE READ PRODUCES NO RECORD, and skipping is PER ENTRY:
    a well-formed sibling in the same mapping is still parsed. An entry that is
    not a table, an entry whose ``assertion_results`` is present but is not a
    table or is missing a reading, and an entry carrying a field of the wrong
    type are all unreadable. An ABSENT field is not: it stays ``None`` on the
    record, which is the state
    :data:`RULE_PROMOTION_EVIDENCE_INCOMPLETE` exists to report.

    NOTHING IN PRODUCTION CALLS THIS YET, and a reader searching for the caller
    should find this sentence rather than a silence. The call arrives with the
    wiring round, in ``packages/orchestration/role_config.py`` — the
    config-reading layer, beside ``resolve_effective_task_class_tiers``, which is
    already where the per-project TIERS table is read. It is deliberately a round
    apart: the schema is pinned before routing behaviour moves against it.
    """
    parsed: dict[str, PromotionEvidence] = {}
    for name, entry in raw_evidence.items():
        if not isinstance(entry, dict):
            continue
        record = _promotion_evidence_from_entry(entry)
        if record is None:
            continue
        parsed[normalize_task_class(name)] = record
    return parsed


#: The FIXED, DECLARED order an override map's violations are reported in: the
#: SCHEMA names first, then the hard-rule names, then the promotion-rule names.
#: Schema first because a malformed entry is what an operator must fix before any
#: policy reading of it means anything; the promotion names LAST because they are
#: the only ones evidence can discharge, so they are the cheapest of the three to
#: clear and the least urgent to read.
#:
#: Like :data:`HARD_RULE_NAMES`, this order is deliberately INDEPENDENT of
#: :data:`MODEL_TIERS`, for the reason that constant already states: re-tiering the
#: model vocabulary must not reshuffle an operator's error list, because a list
#: that reorders itself reads as a different set of problems.
OVERRIDE_VIOLATION_RULE_NAMES: tuple[str, ...] = (
    OVERRIDE_SCHEMA_RULE_NAMES + HARD_RULE_NAMES + PROMOTION_RULE_NAMES
)


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
    promotion_evidence: dict[str, PromotionEvidence] | None = None,
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

    ``promotion_evidence`` maps a task class to the :class:`PromotionEvidence`
    record backing a move to a CHEAPER tier, and DEFAULTS TO NO EVIDENCE. It is
    OPTIONAL so that every caller written before the promotion discipline existed
    — including one passing only the two positional arguments — gets exactly the
    answers it always got for a map that promotes nothing. Promotion violations
    are reported AFTER the hard rules and attributed to the PROMOTED CLASS, which
    is the entry whose evidence is missing.

    A HARD RULE IS NOT DISCHARGED BY EVIDENCE. An override that both promotes a
    class and breaks a hard rule reports BOTH names: the promotion name goes away
    when a benchmark is supplied, the hard-rule name never does, and reporting
    only one of them would tell the operator either that a measurement can rescue
    an entry it cannot, or that a rule is broken when only the paperwork is.

    Each violation's ``rule_name`` is the value a check RETURNED wherever a check
    exists — the three hard-rule checks and the promotion check are called, never
    re-labelled — which is the discipline :func:`validate_routing_choice` already
    states. The two schema names have no check function of their own and are the
    only names this function supplies directly.
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

    # The evidence map's keys are normalized exactly as the override map's are, so
    # a project may spell a class in the policy document's own wording in both.
    evidence_by_class: dict[str, PromotionEvidence] = {
        normalize_task_class(name): record
        for name, record in (promotion_evidence or {}).items()
    }
    for task_class in sorted(effective):
        returned = check_promotion_backed_by_evidence(
            task_class,
            effective[task_class],
            evidence_by_class.get(task_class),
        )
        if returned is not None:
            found.append(OverrideViolation(task_class, returned))

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
    promotion_evidence: dict[str, PromotionEvidence] | None = None,
) -> dict[str, str]:
    """Return :data:`TASK_CLASS_TIERS` overlaid with ``overrides``, or REFUSE the map.

    The override keys are normalized through :func:`normalize_task_class`, the
    whole map is validated by :func:`validate_task_class_tier_overrides`, and if
    there is ANY violation at all this raises :class:`OverrideRefused` carrying
    every one of them.

    ``promotion_evidence`` is passed straight through and DEFAULTS TO NO EVIDENCE,
    so A PROMOTION WITHOUT EVIDENCE IS REFUSED BY THE SAME EXCEPTION that already
    refuses a hard-rule breach. The hard rules and the promotion discipline win the
    same way — by refusing the config, not by editing it — and a caller that
    supplies no evidence map gets exactly the answers it got before the discipline
    existed for any map that promotes nothing.

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
    violations = validate_task_class_tier_overrides(
        normalized, safety_relevant_classes, promotion_evidence
    )
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


# ---------------------------------------------------------------------------
# What a routed call RECORDS — F110's evidence line
# ---------------------------------------------------------------------------

#: The keys :func:`routed_call_evidence_fields` returns, DECLARED as a tuple so a
#: renamed, dropped or added key is a red test rather than a quietly different
#: evidence record. docs/roadmap/features/T3_F110.md's Evidence line is
#: "routed_model, tier, reason on every call"; the routed MODEL is a configuration
#: fact this module deliberately does not know (see the module docstring), so what
#: it records is the declared CLASS, the tier, the reason — and, new in T003, WHAT
#: PROMOTED IT.
ROUTED_CALL_EVIDENCE_FIELDS: tuple[str, ...] = (
    "task_class",
    "tier",
    "reason",
    "promoted_by",
)


# WHY THE TIER AND THE REASON ARE NOT RECOMPUTED HERE: they come from
# resolve_task_class_tier_with_overrides and nowhere else, so the tier a call is
# routed to and the tier its evidence claims can never disagree.
def routed_call_evidence_fields(
    task_class: str,
    effective_tiers: dict[str, str],
    promotion_evidence: dict[str, PromotionEvidence] | None = None,
) -> dict[str, str | None]:
    """Return the mapping a routed call RECORDS for ``task_class``.

    The keys are exactly :data:`ROUTED_CALL_EVIDENCE_FIELDS`. ``tier`` and
    ``reason`` are whatever :func:`resolve_task_class_tier_with_overrides`
    answered against ``effective_tiers``.

    ``promoted_by`` is ``None`` when the class was NOT promoted — the ordinary
    case, and the honest answer for a class routed at or above its seed tier.
    When it WAS promoted it is a REFERENCE LOCATING THE BENCHMARK RUN
    (:meth:`PromotionEvidence.promotion_run_reference`) and never a copy of the
    whole record, because an evidence reader needs to find the run, not to carry
    the measurement on every call.

    A PROMOTED CLASS WITH NO EVIDENCE IN THE MAP ALSO ANSWERS ``None``, and that
    state cannot arise from a table :func:`build_effective_task_class_tiers`
    produced: that builder REFUSES such a map with
    :data:`RULE_PROMOTION_WITHOUT_EVIDENCE`. It is reachable only from a table
    assembled by hand, and answering ``None`` there is the truthful reading —
    nothing located that run because nothing was recorded.
    """
    key = normalize_task_class(task_class)
    tier, reason = resolve_task_class_tier_with_overrides(task_class, effective_tiers)
    promoted_by: str | None = None
    if is_task_class_promotion(key, tier):
        evidence_by_class = {
            normalize_task_class(name): record
            for name, record in (promotion_evidence or {}).items()
        }
        evidence = evidence_by_class.get(key)
        if evidence is not None:
            promoted_by = evidence.promotion_run_reference()
    return {
        "task_class": key,
        "tier": tier,
        "reason": reason,
        "promoted_by": promoted_by,
    }


# ---------------------------------------------------------------------------
# The role inventory and the routing seam — F110 T001
# ---------------------------------------------------------------------------
# docs/roadmap/features/T3_F110.md, T001: the call-site and role inventory, and
# ONE seam every provider call routes through. Everything below is a pure
# function of its arguments for the reason the module docstring gives — this
# module reads no config file and imports neither config.py nor role_config.py.

#: THE T001 INVENTORY IN EXECUTABLE FORM: every orchestration ROLE Remedy
#: resolves a runtime configuration for, mapped to the TASK CLASS that role's
#: calls DECLARE. Until this constant existed the inventory was a list in a
#: feature file, and a list in a feature file rots; here it is read by
#: :func:`resolve_role_task_class` on every routed call, so a wrong entry is a
#: wrong route rather than a stale sentence.
#:
#: EVERY VALUE IS A KEY OF :data:`TASK_CLASS_TIERS`, pinned by its own test — a
#: role declaring a class the seed table does not name would route conservatively
#: while LOOKING declared, which is the worst of both answers.
#:
#: ``orchestrator`` maps to ``mission`` per DECISION F110 D3 (.agent/decisions.md,
#: 2026-09-03), which measured that ``orchestrator`` is a CALL KIND the hard rule
#: guards rather than a seed-table key, and rejected both seeding a new class into
#: the policy document and letting the role fall through to the conservative
#: unknown-class path. ``mission`` is seeded at :data:`TOP_TIER` AND is in
#: :data:`ORCHESTRATION_TASK_CLASSES`, so this role's tier is held by a CHECKED
#: hard rule and not merely by a table entry.
#:
#: ``repair`` IS DELIBERATELY ABSENT from this map: it INHERITS, and is declared in
#: :data:`TASK_CLASS_INHERITING_ROLES` instead. A role in NEITHER is a role nobody
#: declared a task class for — it answers :data:`UNDECLARED_ROLE_TASK_CLASS` with a
#: warning, and the inventory test in tests/orchestration/test_model_routing.py
#: asserts this map and that set together cover EVERY member of
#: ``role_config.KNOWN_ROLES``, so a new role cannot be added quietly.
ROLE_TASK_CLASSES: dict[str, str] = {
    "builder": "standard_build",
    "reviewer": "standard_review",
    "design_worker": "architecture",
    "test_worker": "standard_build",
    "final_verifier": "standard_review",
    "teacher": "summarize",
    "summary": "summarize",
    "orchestrator": "mission",
}

#: THE INHERITING ROLES — roles whose task class is not their own but the class of
#: the work that PROVOKED the call. Exactly one today: ``repair``.
#:
#: THIS IS THE POLICY DOCUMENT'S OWN RULE BULLET, "Repair prompts follow the tier
#: of the original task class.", turned from a CHECKED STRING into a CHECKED
#: BEHAVIOUR. Round 4's policy-document sync test has PINNED that sentence
#: VERBATIM since it landed — ``REPAIR_RULE_BULLET`` in
#: tests/orchestration/test_model_routing.py — and until this constant nothing
#: EXECUTED it: the wording was guarded while the rule itself was inert.
#:
#: THE TWO GUARDS ARE BOTH LOAD-BEARING AND NEITHER REPLACES THE OTHER. The sync
#: test stops the DOCUMENT and the code drifting apart — reword the bullet and it
#: reddens; :func:`resolve_role_task_class` stops the BEHAVIOUR drifting away from
#: the wording — return a fixed class instead of the originating one and the
#: inheritance tests redden. A reworded rule with an unchanged implementation and
#: an unchanged rule with a broken implementation are different failures, so they
#: get different guards.
TASK_CLASS_INHERITING_ROLES: frozenset[str] = frozenset({"repair"})

#: The task class answered for a role neither :data:`ROLE_TASK_CLASSES` nor
#: :data:`TASK_CLASS_INHERITING_ROLES` names. It is deliberately NOT a key of
#: :data:`TASK_CLASS_TIERS`, so it flows through the existing resolver to
#: :data:`TOP_TIER` with :data:`UNKNOWN_CLASS_REASON` — the conservative answer
#: this module already gives an undeclared class, reached by the same code path
#: rather than by a second, rival one.
UNDECLARED_ROLE_TASK_CLASS: str = "undeclared_role"


# WHY AN EXCEPTION AND NOT A DEFAULT: an inheriting role with no originating class
# is a CALLER BUG, not a routing decision. Guessing a class would route a repair
# prompt to a tier nobody chose, which is exactly the silent downgrade
# docs/agents/model_routing_policy.md forbids — and it would be invisible, because
# the evidence line would name a class that was never declared.
class OriginatingTaskClassRequired(Exception):
    """Raised when a role in :data:`TASK_CLASS_INHERITING_ROLES` is given none.

    Carries the role on ``.role`` so a caller reads STRUCTURE rather than
    re-parsing the message; the message names the role and the rule, for the
    operator who only ever sees a traceback.
    """

    def __init__(self, role: str) -> None:
        self.role = role
        super().__init__(
            f"role {role!r} inherits its task class and no originating task class "
            f"was supplied; docs/agents/model_routing_policy.md: "
            f"'Repair prompts follow the tier of the original task class.'"
        )


# WHY THE ORIGINATING CLASS IS IGNORED FOR A DECLARED ROLE: a declared class IS
# the declaration. Letting a caller-supplied class win would make the inventory
# above advisory, and an inventory a caller can override silently is a comment.
def resolve_role_task_class(
    role: str,
    originating_task_class: str | None = None,
) -> str:
    """Return the TASK CLASS a call by ``role`` declares.

    A role in :data:`ROLE_TASK_CLASSES` returns its DECLARED class and
    ``originating_task_class`` is IGNORED — not merged, not preferred, ignored.

    A role in :data:`TASK_CLASS_INHERITING_ROLES` returns
    ``originating_task_class``, normalized through
    :func:`normalize_task_class`, and RAISES :class:`OriginatingTaskClassRequired`
    when none is supplied.

    A role in NEITHER emits a :class:`UserWarning` and returns
    :data:`UNDECLARED_ROLE_TASK_CLASS`, which routes conservatively to
    :data:`TOP_TIER` with :data:`UNKNOWN_CLASS_REASON`.

    WHICH BEHAVIOUR THE UNKNOWN-ROLE PATH MATCHED, AND WHY: it WARNS AND
    CONTINUES, exactly as ``packages/orchestration/role_config.resolve_role_config``
    does for a role its ``KNOWN_ROLES`` does not name. That module warns rather
    than raising, and TWO LAYERS DISAGREEING ABOUT ONE UNKNOWN ROLE — one
    resolving it, the other refusing to route it — would be worse than either
    choice alone: the same call would half-succeed. The disagreement is the
    problem, so this layer follows the layer that already made the choice.
    """
    if role in ROLE_TASK_CLASSES:
        return ROLE_TASK_CLASSES[role]
    if role in TASK_CLASS_INHERITING_ROLES:
        if originating_task_class is None:
            raise OriginatingTaskClassRequired(role)
        return normalize_task_class(originating_task_class)
    warnings.warn(
        f"Role {role!r} declares no task class; routing conservatively as "
        f"{UNDECLARED_ROLE_TASK_CLASS!r}. Declared roles: "
        f"{', '.join(sorted(ROLE_TASK_CLASSES))}; inheriting roles: "
        f"{', '.join(sorted(TASK_CLASS_INHERITING_ROLES))}.",
        stacklevel=2,
    )
    return UNDECLARED_ROLE_TASK_CLASS


# WHY: this is THE SINGLE SEAM docs/roadmap/features/T3_F110.md asks for — every
# provider call site routes through it once the wiring round lands, so the class,
# the tier, the reason and what promoted it come from ONE place and cannot
# disagree.
def route_role_call(
    role: str,
    originating_task_class: str | None = None,
    effective_tiers: dict[str, str] | None = None,
    promotion_evidence: dict[str, PromotionEvidence] | None = None,
) -> dict[str, str | None]:
    """Return the routed-call evidence mapping for a call made by ``role``.

    ``originating_task_class`` is supplied ONLY for a role in
    :data:`TASK_CLASS_INHERITING_ROLES`, and is ignored for every other role.

    ``effective_tiers`` is what :func:`build_effective_task_class_tiers` returned,
    and DEFAULTS to :data:`TASK_CLASS_TIERS` — a call site with no per-project
    overrides configured routes against the shipped policy without having to build
    a table first. ``promotion_evidence`` is passed straight through.

    The keys are exactly :data:`ROUTED_CALL_EVIDENCE_FIELDS`. THIS FUNCTION
    RECOMPUTES NOTHING: it resolves the class through
    :func:`resolve_role_task_class` and then DELEGATES to
    :func:`routed_call_evidence_fields`, so the tier a role's call is routed to and
    the tier its evidence claims are the same value read once.
    """
    task_class = resolve_role_task_class(role, originating_task_class)
    table = TASK_CLASS_TIERS if effective_tiers is None else effective_tiers
    return routed_call_evidence_fields(task_class, table, promotion_evidence)


#: The ``role_config`` function whose calls ARE the call-site inventory below.
#: Named as a constant so the AST sweep in tests/orchestration/test_model_routing.py
#: does not retype it: renaming that function must move the sweep and this
#: constant together, not leave a sweep quietly matching nothing.
ROLE_CONFIG_RESOLVER_NAME: str = "resolve_role_config"

#: Stands in :data:`ROLE_CONFIG_CALL_SITES` where a call site passes a role
#: VARIABLE rather than a literal. Angle brackets because no role name can contain
#: them, so the marker can never be mistaken for a role.
DYNAMIC_ROLE_MARKER: str = "<dynamic>"

#: THE CALL-SITE INVENTORY: every production call that resolves a role's runtime
#: configuration, as a MULTISET of ``(repository path, role-or-marker)`` pairs.
#: A tuple and not a set because ``teacher_model.py`` calls the resolver TWICE and
#: a set would silently collapse the two into one.
#:
#: NO LINE NUMBERS, DELIBERATELY. A line number moves under any edit ABOVE the
#: call, so an inventory keyed on them would go red for edits that changed no call
#: site at all — and a gate that cries wolf gets widened until it stops meaning
#: anything. The pair identifies the call; the sweep finds where it is.
#:
#: WHY THE INVENTORY PINS CALL SITES AND NOT ROLE STRINGS: only TWO of these seven
#: calls pass a role LITERAL. The other five pass a variable, so a sweep keyed on
#: literal roles would reach two of seven and report a clean bill for the five it
#: never looked at. Pinning the SITES makes the missing five visible as
#: :data:`DYNAMIC_ROLE_MARKER` entries — declared unknowns rather than absences.
#:
#: CHECKED, NOT DECLARED: tests/orchestration/test_model_routing.py re-runs the AST
#: sweep over ``packages/`` and ``apps/`` and asserts the multiset EQUALS this
#: constant, so a new provider call site cannot land without that test going red.
ROLE_CONFIG_CALL_SITES: tuple[tuple[str, str], ...] = (
    ("apps/cli/commands/do_cmd.py", DYNAMIC_ROLE_MARKER),
    ("packages/orchestration/artifact_summary.py", "summary"),
    ("packages/orchestration/pingpong_job.py", DYNAMIC_ROLE_MARKER),
    ("packages/orchestration/role_config.py", "orchestrator"),
    ("packages/orchestration/self_use_runner.py", DYNAMIC_ROLE_MARKER),
    ("packages/orchestration/teacher_model.py", DYNAMIC_ROLE_MARKER),
    ("packages/orchestration/teacher_model.py", DYNAMIC_ROLE_MARKER),
)
