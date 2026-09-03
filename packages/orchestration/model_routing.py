"""
Model routing by task class for Remedy (F110).

Owns the CLASS TABLE and nothing else yet: which model TIER a declared task
class is routed to. The table is SEEDED from the "Seed mapping" section of
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

Public API::

    MODEL_TIERS: tiers CHEAPEST FIRST — the order is significant
    TOP_TIER: the strongest tier, i.e. MODEL_TIERS[-1]
    TASK_CLASS_TIERS: the seeded task-class -> tier table
    SEED_MAPPING_REASON: reason recorded for a class the seed mapping names
    UNKNOWN_CLASS_REASON: reason recorded for a class it does not
    normalize_task_class(phrase) -> str
    resolve_task_class_tier(task_class) -> tuple[str, str]
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
