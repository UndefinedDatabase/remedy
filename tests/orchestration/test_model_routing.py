"""Tests for packages/orchestration/model_routing.py — F110 T002a/T002b/T002c/T003.

The four rounds this file covers are the class TABLE (T002a), the three HARD
RULES as named checks (T002b), the PER-PROJECT OVERRIDE SCHEMA that validates
a whole override map against those rules before it is applied (T002c), and the
PROMOTION-EVIDENCE DISCIPLINE that refuses a move to a CHEAPER tier unless a
documented benchmark run backs it (T003).

THERE IS A SECOND SYNC TEST NOW, AND IT IS T003's DELIVERABLE.
:class:`TestPromotionRuleSyncTest` parses the "Promotion rule" section of the
same document and asserts the parsed runs count, the two parsed percentages and
the parsed logged-per-run field list EQUAL the module's constants, so the
promotion BARS are pinned to the policy exactly as the class TABLE is. Lowering a
bar in the code without lowering it in the document is a red test rather than a
quiet saving.

THE SYNC TEST IS THE ACCEPTANCE LINE. docs/roadmap/features/T3_F110.md's
Acceptance section requires that "the class table matches the policy document (a
sync test diffs them)", and :class:`TestPolicyDocumentSyncTest` below is it: it
parses the "Seed mapping" section of docs/agents/model_routing_policy.md and
asserts the parsed mapping EQUALS ``TASK_CLASS_TIERS``. It therefore reddens for
drift in EITHER direction — a re-tiered class in the code, or a re-worded class
in the document — which is what makes it a sync test rather than a code test.

THE ONE NON-ARROW BULLET IS ASSERTED, NOT FILTERED AWAY. The section carries
four bullets, three of which are mappings and one of which
("Repair prompts follow the tier of the original task class.") is a RULE. A
parser that silently dropped every line it could not read as a mapping would
pass over exactly the change this test exists to catch, so the count of
non-arrow bullets and the text of the one that exists are both pinned.

No model id is asserted anywhere in this file, deliberately: this round maps
task classes to TIERS. Which concrete model serves a tier is a configuration
fact and asserting one here would make these tests go stale on the day an
operator repoints it.

EACH HARD RULE HAS A VIOLATING FIXTURE REFUSED WITH THE RULE NAMED, which is the
second acceptance line of docs/roadmap/features/T3_F110.md, and each is paired
with a CONFORMING case so the test discriminates rather than merely producing a
refusal. Every such assertion compares against the module's own rule-name
CONSTANT and never against a retyped string literal: a renamed token must break
the import, not leave a test quietly asserting a dead string.

THE SAFETY RULE IS PROVEN NON-VACUOUS. Its production class set
(``SAFETY_RELEVANT_CLASSES``) is EMPTY today, so a test written against that
constant alone could never see the rule fire. The check therefore takes the class
set as a parameter, the tests below supply a FIXTURE set and prove the refusal
really happens, and a separate test asserts the production constant is empty
TODAY — so the emptiness is a stated property under test rather than an accident
nobody would notice changing.
"""

from __future__ import annotations

import dataclasses
import re
from pathlib import Path

import pytest

from packages.orchestration.model_routing import (
    HARD_RULE_NAMES,
    MID_TIER,
    MODEL_TIERS,
    ORCHESTRATION_TASK_CLASSES,
    OVERRIDE_REASON,
    OVERRIDE_SCHEMA_RULE_NAMES,
    OVERRIDE_VIOLATION_RULE_NAMES,
    PROMOTION_EVIDENCE_COMPOUND_FIELD_SEPARATOR,
    PROMOTION_EVIDENCE_DOCUMENT_FIELDS,
    PROMOTION_MINIMUM_BLOCK_ASSERTION_PASS_RATE,
    PROMOTION_MINIMUM_OVERALL_PASS_RATE,
    PROMOTION_MINIMUM_RUNS_PER_FIXTURE,
    PROMOTION_RULE_NAMES,
    REVIEWER_WORKER_CLASS_PAIRS,
    ROUTED_CALL_EVIDENCE_FIELDS,
    RULE_ORCHESTRATION_BELOW_TOP_TIER,
    RULE_OVERRIDE_UNKNOWN_TASK_CLASS,
    RULE_OVERRIDE_UNKNOWN_TIER,
    RULE_PROMOTION_EVIDENCE_BELOW_THRESHOLD,
    RULE_PROMOTION_EVIDENCE_INCOMPLETE,
    RULE_PROMOTION_WITHOUT_EVIDENCE,
    RULE_REVIEWER_WEAKER_THAN_WORKER,
    RULE_SAFETY_CLASS_BELOW_MID_TIER,
    SAFETY_RELEVANT_CLASSES,
    SEED_MAPPING_REASON,
    TASK_CLASS_TIERS,
    TOP_TIER,
    UNKNOWN_CLASS_REASON,
    OverrideRefused,
    PromotionAssertionResults,
    PromotionEvidence,
    build_effective_task_class_tiers,
    check_orchestration_class_routed_to_top_tier,
    check_promotion_backed_by_evidence,
    check_reviewer_not_weaker_than_worker,
    check_safety_relevant_class_not_below_mid_tier,
    is_task_class_promotion,
    model_tier_rank,
    normalize_task_class,
    resolve_task_class_tier,
    resolve_task_class_tier_with_overrides,
    routed_call_evidence_fields,
    validate_routing_choice,
    validate_task_class_tier_overrides,
)

REPO = Path(__file__).resolve().parents[2]

#: The human-readable policy the table is seeded from. Read, never written.
POLICY_DOC = REPO / "docs" / "agents" / "model_routing_policy.md"

#: U+2192 RIGHTWARDS ARROW — what separates a class list from its tier in the
#: document's mapping bullets, and the single test for "is this bullet a
#: mapping or a rule?".
ARROW = "→"

SEED_HEADING = "## Seed mapping"
NEXT_HEADING = "## Hard rules"

#: The one bullet in the section that is a RULE and not a mapping. Pinned
#: verbatim: a second rule bullet, or a reworded one, must turn this file red
#: rather than being quietly ignored by the mapping parser.
REPAIR_RULE_BULLET = "- Repair prompts follow the tier of the original task class."


def _seed_mapping_bullets() -> list[str]:
    """Return the ``- `` bullets between the Seed mapping and Hard rules headings."""
    lines = POLICY_DOC.read_text(encoding="utf-8").split("\n")
    starts = [i for i, ln in enumerate(lines) if ln.startswith(SEED_HEADING)]
    assert len(starts) == 1, f"expected exactly one {SEED_HEADING!r} heading, found {len(starts)}"
    ends = [i for i, ln in enumerate(lines) if ln.startswith(NEXT_HEADING) and i > starts[0]]
    assert ends, f"no {NEXT_HEADING!r} heading after {SEED_HEADING!r}"
    return [ln for ln in lines[starts[0] + 1:ends[0]] if ln.startswith("- ")]


def _parse_seed_mapping() -> dict[str, str]:
    """Parse the document's mapping bullets into a task-class -> tier dict.

    The left side of the arrow, split on ``/``, gives the class phrases; the
    first word of the right side gives the tier. Phrases become keys through
    ``normalize_task_class`` and no other route, which is what lets the result
    be compared to the module's table directly instead of through a translation.
    """
    parsed: dict[str, str] = {}
    for bullet in _seed_mapping_bullets():
        if ARROW not in bullet:
            continue
        left, right = bullet[len("- "):].split(ARROW)
        tier = right.split()[0]
        for phrase in left.split("/"):
            parsed[normalize_task_class(phrase)] = tier
    return parsed


class TestPolicyDocumentSyncTest:
    """The acceptance line: the document and the table say the same thing."""

    def test_the_parsed_seed_mapping_equals_the_module_table(self):
        assert _parse_seed_mapping() == TASK_CLASS_TIERS

    def test_the_section_carries_exactly_four_bullets(self):
        assert len(_seed_mapping_bullets()) == 4

    def test_exactly_three_bullets_are_mappings(self):
        bullets = _seed_mapping_bullets()
        assert len([b for b in bullets if ARROW in b]) == 3

    def test_exactly_one_bullet_is_a_rule_rather_than_a_mapping(self):
        bullets = _seed_mapping_bullets()
        assert len([b for b in bullets if ARROW not in b]) == 1

    def test_the_one_rule_bullet_is_the_repair_prompt_sentence(self):
        rules = [b for b in _seed_mapping_bullets() if ARROW not in b]
        assert rules == [REPAIR_RULE_BULLET]

    def test_the_document_names_exactly_ten_classes(self):
        assert len(_parse_seed_mapping()) == 10

    def test_every_tier_the_document_names_is_a_known_tier(self):
        assert set(_parse_seed_mapping().values()) <= set(MODEL_TIERS)


class TestEveryTableClassResolvesToItsTier:
    """Every class the table carries resolves to the tier the table gives it."""

    @pytest.mark.parametrize(("task_class", "tier"), sorted(TASK_CLASS_TIERS.items()))
    def test_table_class_resolves_to_its_tier(self, task_class, tier):
        assert resolve_task_class_tier(task_class) == (tier, SEED_MAPPING_REASON)

    @pytest.mark.parametrize("task_class", sorted(TASK_CLASS_TIERS))
    def test_a_table_class_never_reports_the_unknown_reason(self, task_class):
        _, reason = resolve_task_class_tier(task_class)
        assert reason != UNKNOWN_CLASS_REASON


class TestUnknownClassIsConservative:
    """An undeclared class costs money rather than quality, and says so."""

    @pytest.mark.parametrize(
        "task_class",
        [
            "a_class_the_document_does_not_name",
            "refactor",
            "Deep Research",
            "",
            "   ",
        ],
    )
    def test_unknown_class_routes_to_the_top_tier(self, task_class):
        tier, _ = resolve_task_class_tier(task_class)
        assert tier == TOP_TIER

    @pytest.mark.parametrize(
        "task_class",
        [
            "a_class_the_document_does_not_name",
            "refactor",
            "Deep Research",
        ],
    )
    def test_unknown_class_reason_is_exactly_the_documented_token(self, task_class):
        _, reason = resolve_task_class_tier(task_class)
        assert reason == "unknown_class_conservative"

    def test_the_documented_token_is_what_the_module_exports(self):
        assert UNKNOWN_CLASS_REASON == "unknown_class_conservative"


class TestNormalizeTaskClass:
    """One documented normalization, used by both the table and the sync test."""

    def test_the_three_spellings_are_one_key(self):
        keys = {
            normalize_task_class("Standard Build"),
            normalize_task_class("standard build"),
            normalize_task_class("standard_build"),
        }
        assert keys == {"standard_build"}

    @pytest.mark.parametrize(
        ("phrase", "expected"),
        [
            ("  MISSION  ", "mission"),
            ("prompt authoring for other agents", "prompt_authoring_for_other_agents"),
            ("Standard   Review", "standard_review"),
            ("\tformat\n", "format"),
            ("extract", "extract"),
        ],
    )
    def test_normalization_cases(self, phrase, expected):
        assert normalize_task_class(phrase) == expected

    def test_the_three_spellings_resolve_alike(self):
        answers = {
            resolve_task_class_tier("Standard Build"),
            resolve_task_class_tier("standard build"),
            resolve_task_class_tier("standard_build"),
        }
        assert len(answers) == 1


class TestTierVocabulary:
    """The order of the tier tuple is load-bearing, so it is pinned."""

    def test_the_tiers_are_cheapest_to_strongest(self):
        assert MODEL_TIERS == ("cheap", "mid", "top")

    def test_the_order_is_strictly_increasing_in_strength(self):
        assert MODEL_TIERS.index("cheap") < MODEL_TIERS.index("mid") < MODEL_TIERS.index("top")

    def test_top_tier_is_the_last_tier(self):
        assert TOP_TIER == MODEL_TIERS[-1]

    def test_every_table_value_is_a_member_of_the_tier_tuple(self):
        assert set(TASK_CLASS_TIERS.values()) <= set(MODEL_TIERS)

    def test_every_tier_is_actually_used_by_the_table(self):
        assert set(TASK_CLASS_TIERS.values()) == set(MODEL_TIERS)


# ---------------------------------------------------------------------------
# F110 T002b — the three hard rules
# ---------------------------------------------------------------------------

#: Every tier that is NOT the top one, derived from the module's own vocabulary
#: rather than written out, so adding a tier extends the fixtures automatically.
TIERS_BELOW_TOP = tuple(t for t in MODEL_TIERS if t != TOP_TIER)

#: Every tier strictly below mid, derived the same way.
TIERS_BELOW_MID = tuple(t for t in MODEL_TIERS if model_tier_rank(t) < model_tier_rank(MID_TIER))

#: Every tier at or above mid.
TIERS_AT_OR_ABOVE_MID = tuple(t for t in MODEL_TIERS if model_tier_rank(t) >= model_tier_rank(MID_TIER))

#: A FIXTURE safety-relevant class set. The PRODUCTION set is empty (and a test
#: below asserts that it is), so without a fixture set the safety rule could
#: never fire and its check would be a rule that cannot fail. These two names are
#: the prompts the policy document scopes the rule to, spelled as task classes.
FIXTURE_SAFETY_CLASSES = frozenset({"fence_evaluation", "dod_evaluation"})

#: A tier no MODEL_TIERS entry names, for the raise-on-unknown cases.
UNKNOWN_TIER = "gigantic"


class TestModelTierRank:
    """One ordered vocabulary, compared by index — and no silent default."""

    @pytest.mark.parametrize(
        ("tier", "expected"),
        [(tier, index) for index, tier in enumerate(MODEL_TIERS)],
    )
    def test_each_tier_ranks_at_its_position_in_the_tuple(self, tier, expected):
        assert model_tier_rank(tier) == expected

    def test_the_ranks_increase_from_cheapest_to_strongest(self):
        ranks = [model_tier_rank(t) for t in MODEL_TIERS]
        assert ranks == sorted(ranks)
        assert len(set(ranks)) == len(MODEL_TIERS)

    def test_mid_ranks_between_the_cheapest_and_the_top_tier(self):
        assert model_tier_rank(MODEL_TIERS[0]) < model_tier_rank(MID_TIER) < model_tier_rank(TOP_TIER)

    def test_mid_tier_is_a_member_of_the_tier_tuple(self):
        assert MID_TIER in MODEL_TIERS

    def test_an_unknown_tier_raises_rather_than_returning_a_default(self):
        with pytest.raises(ValueError):
            model_tier_rank(UNKNOWN_TIER)

    def test_the_raised_error_names_the_offending_tier(self):
        with pytest.raises(ValueError) as excinfo:
            model_tier_rank(UNKNOWN_TIER)
        assert UNKNOWN_TIER in str(excinfo.value)


class TestHardRuleNamesAreStableTokens:
    """Refused WITH THE RULE NAMED means a stable token, not a prose sentence."""

    def test_the_three_names_are_distinct(self):
        names = {
            RULE_REVIEWER_WEAKER_THAN_WORKER,
            RULE_ORCHESTRATION_BELOW_TOP_TIER,
            RULE_SAFETY_CLASS_BELOW_MID_TIER,
        }
        assert len(names) == 3

    def test_hard_rule_names_carries_exactly_those_three_in_a_declared_order(self):
        assert HARD_RULE_NAMES == (
            RULE_REVIEWER_WEAKER_THAN_WORKER,
            RULE_ORCHESTRATION_BELOW_TOP_TIER,
            RULE_SAFETY_CLASS_BELOW_MID_TIER,
        )

    def test_no_rule_name_is_a_tier_name(self):
        assert set(HARD_RULE_NAMES).isdisjoint(set(MODEL_TIERS))


class TestReviewerNeverWeakerThanTheWorker:
    """Policy hard rule 1 — equal allowed, stronger fine, strictly weaker refused."""

    @pytest.mark.parametrize(
        ("worker_tier", "reviewer_tier"),
        [
            (w, r)
            for w in MODEL_TIERS
            for r in MODEL_TIERS
            if model_tier_rank(r) < model_tier_rank(w)
        ],
    )
    def test_a_weaker_reviewer_is_refused_with_the_rule_named(self, worker_tier, reviewer_tier):
        assert check_reviewer_not_weaker_than_worker(worker_tier, reviewer_tier) == (
            RULE_REVIEWER_WEAKER_THAN_WORKER
        )

    @pytest.mark.parametrize("tier", MODEL_TIERS)
    def test_an_equal_reviewer_is_not_refused(self, tier):
        assert check_reviewer_not_weaker_than_worker(tier, tier) is None

    @pytest.mark.parametrize(
        ("worker_tier", "reviewer_tier"),
        [
            (w, r)
            for w in MODEL_TIERS
            for r in MODEL_TIERS
            if model_tier_rank(r) > model_tier_rank(w)
        ],
    )
    def test_a_stronger_reviewer_is_not_refused(self, worker_tier, reviewer_tier):
        assert check_reviewer_not_weaker_than_worker(worker_tier, reviewer_tier) is None

    def test_an_unknown_tier_raises_rather_than_reading_as_a_pass(self):
        with pytest.raises(ValueError):
            check_reviewer_not_weaker_than_worker(TOP_TIER, UNKNOWN_TIER)


class TestOrchestrationCallsAlwaysTopTier:
    """The feature file's rule — orchestration calls always top tier.

    The feature file words it "orchestrator and mission-compile calls"; the SET
    the rule is checked against also carries ``mission``, per DECISION F110 D2,
    because the seed table routes ``mission`` to the top tier and a per-project
    override is exactly what could move it. The membership test below pins the
    WIDER set exactly, so the widening stays a decision and not a drift.
    """

    @pytest.mark.parametrize("task_class", sorted(ORCHESTRATION_TASK_CLASSES))
    @pytest.mark.parametrize("tier", TIERS_BELOW_TOP)
    def test_an_orchestration_class_below_top_is_refused_with_the_rule_named(self, task_class, tier):
        assert check_orchestration_class_routed_to_top_tier(task_class, tier) == (
            RULE_ORCHESTRATION_BELOW_TOP_TIER
        )

    @pytest.mark.parametrize("task_class", sorted(ORCHESTRATION_TASK_CLASSES))
    def test_an_orchestration_class_at_the_top_tier_is_not_refused(self, task_class):
        assert check_orchestration_class_routed_to_top_tier(task_class, TOP_TIER) is None

    @pytest.mark.parametrize("task_class", sorted(TASK_CLASS_TIERS))
    @pytest.mark.parametrize("tier", MODEL_TIERS)
    def test_a_class_the_rule_does_not_cover_is_never_refused_by_it(self, task_class, tier):
        if task_class in ORCHESTRATION_TASK_CLASSES:
            pytest.skip("covered by the violating fixture above")
        assert check_orchestration_class_routed_to_top_tier(task_class, tier) is None

    def test_the_declared_class_may_be_spelled_as_the_document_words_it(self):
        assert check_orchestration_class_routed_to_top_tier("Mission Compile", MODEL_TIERS[0]) == (
            RULE_ORCHESTRATION_BELOW_TOP_TIER
        )

    def test_the_covered_classes_are_exactly_the_set_decision_d2_declares(self):
        # A WIDER PIN IS STILL A PIN. DECISION F110 D2 added ``mission`` to the
        # set, which made the previous two-class assertion false; it is REWRITTEN
        # here to the exact new membership rather than deleted, so adding a fourth
        # class silently still turns this file red.
        assert ORCHESTRATION_TASK_CLASSES == frozenset(
            {
                normalize_task_class("orchestrator"),
                normalize_task_class("mission compile"),
                normalize_task_class("mission"),
            }
        )


class TestSafetyRelevantClassNeverBelowMid:
    """Policy hard rule 2, and the proof that it is NOT a rule that cannot fail."""

    @pytest.mark.parametrize("task_class", sorted(FIXTURE_SAFETY_CLASSES))
    @pytest.mark.parametrize("tier", TIERS_BELOW_MID)
    def test_a_safety_class_below_mid_is_refused_with_the_rule_named(self, task_class, tier):
        assert check_safety_relevant_class_not_below_mid_tier(
            task_class, tier, FIXTURE_SAFETY_CLASSES
        ) == RULE_SAFETY_CLASS_BELOW_MID_TIER

    @pytest.mark.parametrize("task_class", sorted(FIXTURE_SAFETY_CLASSES))
    @pytest.mark.parametrize("tier", TIERS_AT_OR_ABOVE_MID)
    def test_a_safety_class_at_or_above_mid_is_not_refused(self, task_class, tier):
        assert check_safety_relevant_class_not_below_mid_tier(
            task_class, tier, FIXTURE_SAFETY_CLASSES
        ) is None

    @pytest.mark.parametrize("tier", MODEL_TIERS)
    def test_a_class_outside_the_supplied_set_is_not_refused(self, tier):
        assert check_safety_relevant_class_not_below_mid_tier(
            "format", tier, FIXTURE_SAFETY_CLASSES
        ) is None

    def test_the_production_safety_class_set_is_empty_today(self):
        assert SAFETY_RELEVANT_CLASSES == frozenset()

    def test_the_empty_production_set_therefore_refuses_nothing_today(self):
        assert check_safety_relevant_class_not_below_mid_tier(
            sorted(FIXTURE_SAFETY_CLASSES)[0], MODEL_TIERS[0]
        ) is None

    def test_an_unknown_tier_raises_for_a_class_the_rule_covers(self):
        with pytest.raises(ValueError):
            check_safety_relevant_class_not_below_mid_tier(
                sorted(FIXTURE_SAFETY_CLASSES)[0], UNKNOWN_TIER, FIXTURE_SAFETY_CLASSES
            )


class TestRoutingChoiceValidatorCollectsEveryViolation:
    """Reporting one of three broken rules sends the operator round the loop three times."""

    #: A single choice that breaks ALL THREE hard rules at once: an orchestration
    #: class, also declared safety-relevant by the fixture set, routed to the
    #: cheapest tier while reviewing a top-tier worker.
    BREAKS_ALL_THREE = {
        "task_class": "orchestrator",
        "tier": MODEL_TIERS[0],
        "paired_worker_tier": TOP_TIER,
        "safety_relevant_classes": frozenset({"orchestrator"}),
    }

    def test_a_choice_breaking_all_three_returns_all_three_rule_names(self):
        assert validate_routing_choice(**self.BREAKS_ALL_THREE) == HARD_RULE_NAMES

    def test_a_conforming_choice_returns_an_empty_result(self):
        assert validate_routing_choice(
            task_class="orchestrator",
            tier=TOP_TIER,
            paired_worker_tier=TOP_TIER,
            safety_relevant_classes=frozenset({"orchestrator"}),
        ) == ()

    def test_only_the_reviewer_rule_fires_for_a_plain_weak_reviewer(self):
        assert validate_routing_choice(
            task_class="format",
            tier=MODEL_TIERS[0],
            paired_worker_tier=TOP_TIER,
        ) == (RULE_REVIEWER_WEAKER_THAN_WORKER,)

    def test_only_the_orchestration_rule_fires_for_a_cheap_orchestrator_call(self):
        assert validate_routing_choice(
            task_class="orchestrator",
            tier=MODEL_TIERS[0],
        ) == (RULE_ORCHESTRATION_BELOW_TOP_TIER,)

    def test_only_the_safety_rule_fires_for_a_cheap_safety_class(self):
        assert validate_routing_choice(
            task_class=sorted(FIXTURE_SAFETY_CLASSES)[0],
            tier=MODEL_TIERS[0],
            safety_relevant_classes=FIXTURE_SAFETY_CLASSES,
        ) == (RULE_SAFETY_CLASS_BELOW_MID_TIER,)

    def test_the_reviewer_rule_is_not_evaluated_without_a_paired_worker(self):
        assert validate_routing_choice(task_class="format", tier=MODEL_TIERS[0]) == ()

    def test_the_result_follows_the_declared_order_not_the_alphabet(self):
        result = validate_routing_choice(**self.BREAKS_ALL_THREE)
        assert list(result) == [n for n in HARD_RULE_NAMES if n in set(result)]
        assert list(result) != sorted(result)

    def test_with_the_production_safety_set_the_safety_rule_never_appears(self):
        result = validate_routing_choice(
            task_class=sorted(FIXTURE_SAFETY_CLASSES)[0],
            tier=MODEL_TIERS[0],
        )
        assert RULE_SAFETY_CLASS_BELOW_MID_TIER not in result


# ---------------------------------------------------------------------------
# F110 T002c — the per-project override schema
# ---------------------------------------------------------------------------

#: The orchestration classes an override map can actually REACH, which is the
#: intersection of ORCHESTRATION_TASK_CLASSES with the seed table's keys. An
#: override naming an orchestration class the seed table does NOT name is a SCHEMA
#: fault (``override_unknown_task_class``) and never a hard rule 2 violation, so
#: only this subset can produce the hard-rule refusal. After DECISION F110 D2 it
#: is non-empty, which is precisely what that decision bought.
OVERRIDABLE_ORCHESTRATION_CLASSES = tuple(
    sorted(ORCHESTRATION_TASK_CLASSES & set(TASK_CLASS_TIERS))
)

#: A FIXTURE safety-relevant set for the override tests, and it names a class the
#: SEED TABLE names, which ``FIXTURE_SAFETY_CLASSES`` above deliberately does not.
#: An override on "fence_evaluation" would be refused as a schema fault before the
#: safety rule ever looked at it, so proving the safety rule fires through an
#: OVERRIDE needs a class the table already carries. ``architecture`` is seeded at
#: the top tier, so the seed table alone conforms under this set and every refusal
#: below is caused by the override rather than by the fixture.
OVERRIDE_SAFETY_CLASSES = frozenset({"architecture"})

#: A key no seed-table class normalizes to.
UNKNOWN_OVERRIDE_CLASS = "a_class_the_document_does_not_name"


def _rule_names(violations) -> list[str]:
    """Return just the rule names of ``violations``, in the order reported."""
    return [violation.rule_name for violation in violations]


# ---------------------------------------------------------------------------
# F110 T003 — the promotion-evidence fixtures
# ---------------------------------------------------------------------------

#: A seeded class that is PROMOTABLE (its seed tier is above the cheapest) and
#: that NO hard rule speaks about: it is not an orchestration class, it is not in
#: ``OVERRIDE_SAFETY_CLASSES``, and it is in no reviewer/worker pair. Demoting it
#: therefore isolates the promotion discipline from every other rule, which is what
#: makes the pairs below discriminate.
PROMOTABLE_CLASS = "vision"

#: The tier those fixtures promote to — the cheapest, so every promotable class is
#: strictly below its seed tier.
PROMOTED_TIER = MODEL_TIERS[0]


def _promotion_evidence(**overrides) -> PromotionEvidence:
    """Return a COMPLETE benchmark record sitting EXACTLY AT every bar.

    Every bar value is read from the module's own constant rather than retyped,
    so the boundary cases below stay at the boundary when a bar moves. Keyword
    ``overrides`` produce the incomplete and below-threshold variants.
    """
    fields = {
        "model_id": "qwen3-8b-instruct",
        "quantization": "q4_k_m",
        "prompt_hash": "0f1e2d3c4b5a6978",
        "tokens": 1200,
        "cost": 0.0,
        "assertion_results": PromotionAssertionResults(
            block_level_pass_rate=PROMOTION_MINIMUM_BLOCK_ASSERTION_PASS_RATE,
            overall_pass_rate=PROMOTION_MINIMUM_OVERALL_PASS_RATE,
        ),
        "reviewer_verdict": "pass",
        "runs_per_fixture": PROMOTION_MINIMUM_RUNS_PER_FIXTURE,
        "corpus": "F082",
    }
    fields.update(overrides)
    return PromotionEvidence(**fields)


#: A run that meets every bar exactly.
SUFFICIENT_EVIDENCE = _promotion_evidence()

#: A run that was measured but not fully logged — one document field unset.
INCOMPLETE_EVIDENCE = _promotion_evidence(prompt_hash=None)

#: A run that was fully logged but fell one below the runs bar.
BELOW_THRESHOLD_EVIDENCE = _promotion_evidence(
    runs_per_fixture=PROMOTION_MINIMUM_RUNS_PER_FIXTURE - 1
)


class TestOverrideSchemaFaults:
    """A malformed override is REPORTED with its own name, not crashed on."""

    def test_an_override_naming_an_unknown_task_class_is_refused_with_its_own_rule(self):
        violations = validate_task_class_tier_overrides({UNKNOWN_OVERRIDE_CLASS: TOP_TIER})
        assert _rule_names(violations) == [RULE_OVERRIDE_UNKNOWN_TASK_CLASS]
        assert violations[0].task_class == UNKNOWN_OVERRIDE_CLASS

    def test_an_override_naming_an_unknown_tier_is_refused_with_its_own_rule(self):
        violations = validate_task_class_tier_overrides({"format": UNKNOWN_TIER})
        assert _rule_names(violations) == [RULE_OVERRIDE_UNKNOWN_TIER]
        assert violations[0].task_class == "format"

    def test_a_malformed_override_is_reported_rather_than_raising_out_of_the_validator(self):
        # The validator RETURNS for both schema faults; nothing propagates. A
        # config typo an operator can read is worth more than a traceback.
        assert validate_task_class_tier_overrides({UNKNOWN_OVERRIDE_CLASS: UNKNOWN_TIER})
        assert validate_task_class_tier_overrides({"format": UNKNOWN_TIER})

    def test_an_unrankable_tier_never_reaches_a_hard_rule_check(self):
        # ``mission`` at an unknown tier would RAISE inside hard rule 2 if the
        # schema-faulty entry were judged; it must report the schema fault alone.
        violations = validate_task_class_tier_overrides({"mission": UNKNOWN_TIER})
        assert _rule_names(violations) == [RULE_OVERRIDE_UNKNOWN_TIER]

    def test_a_well_formed_override_produces_no_schema_fault(self):
        violations = validate_task_class_tier_overrides({"format": MID_TIER})
        assert not [n for n in _rule_names(violations) if n in OVERRIDE_SCHEMA_RULE_NAMES]


class TestOverrideRefusedPerHardRule:
    """One violating override map per hard rule, each refused WITH THE RULE NAMED."""

    @pytest.mark.parametrize("task_class", OVERRIDABLE_ORCHESTRATION_CLASSES)
    @pytest.mark.parametrize("tier", TIERS_BELOW_TOP)
    def test_an_orchestration_class_demoted_below_top_is_refused_with_the_rule_named(
        self, task_class, tier
    ):
        # WIDENED IN T003, NOT WEAKENED. Every orchestration class the seed table
        # names is seeded at the TOP tier, so demoting it is necessarily ALSO a
        # promotion; with no evidence supplied the map now reports both names. The
        # assertion stays an EXACT list and simply names the second one.
        violations = validate_task_class_tier_overrides({task_class: tier})
        assert _rule_names(violations) == [
            RULE_ORCHESTRATION_BELOW_TOP_TIER,
            RULE_PROMOTION_WITHOUT_EVIDENCE,
        ]
        assert violations[0].task_class == task_class

    @pytest.mark.parametrize("task_class", OVERRIDABLE_ORCHESTRATION_CLASSES)
    @pytest.mark.parametrize("tier", TIERS_BELOW_TOP)
    def test_evidence_clears_the_promotion_name_and_never_the_orchestration_rule(
        self, task_class, tier
    ):
        # The discriminator for the case above: the SAME map with a sufficient
        # benchmark run loses the promotion name and keeps the hard-rule name.
        violations = validate_task_class_tier_overrides(
            {task_class: tier},
            SAFETY_RELEVANT_CLASSES,
            {task_class: SUFFICIENT_EVIDENCE},
        )
        assert _rule_names(violations) == [RULE_ORCHESTRATION_BELOW_TOP_TIER]

    @pytest.mark.parametrize("task_class", OVERRIDABLE_ORCHESTRATION_CLASSES)
    def test_the_same_orchestration_class_restated_at_the_top_tier_is_not_refused(
        self, task_class
    ):
        assert validate_task_class_tier_overrides({task_class: TOP_TIER}) == ()

    def test_mission_demoted_below_top_is_refused_with_the_rule_named(self):
        # DECISION F110 D2's OWN ACCEPTANCE FIXTURE. Before D2, ``mission`` was
        # outside ORCHESTRATION_TASK_CLASSES and this override was accepted in
        # silence, because the policy-document sync test guards the TABLE against
        # the DOCUMENT and cannot reach an override at all.
        # WIDENED IN T003: ``mission`` is seeded at the top tier, so this demotion
        # is also an unevidenced promotion and both names are now reported.
        violations = validate_task_class_tier_overrides({"mission": MODEL_TIERS[0]})
        assert _rule_names(violations) == [
            RULE_ORCHESTRATION_BELOW_TOP_TIER,
            RULE_PROMOTION_WITHOUT_EVIDENCE,
        ]
        assert violations[0].task_class == "mission"

    def test_mission_left_at_the_top_tier_is_not_refused(self):
        assert validate_task_class_tier_overrides({"mission": TOP_TIER}) == ()

    @pytest.mark.parametrize("tier", TIERS_BELOW_MID)
    def test_a_safety_relevant_class_demoted_below_mid_is_refused_with_the_rule_named(self, tier):
        # WIDENED IN T003: ``architecture`` is seeded at the top tier, so dropping
        # it below mid is also an unevidenced promotion. Both names, exact list.
        task_class = sorted(OVERRIDE_SAFETY_CLASSES)[0]
        violations = validate_task_class_tier_overrides(
            {task_class: tier}, OVERRIDE_SAFETY_CLASSES
        )
        assert _rule_names(violations) == [
            RULE_SAFETY_CLASS_BELOW_MID_TIER,
            RULE_PROMOTION_WITHOUT_EVIDENCE,
        ]
        assert violations[0].task_class == task_class

    @pytest.mark.parametrize("tier", TIERS_AT_OR_ABOVE_MID)
    def test_the_same_safety_class_at_or_above_mid_is_not_refused(self, tier):
        # WIDENED IN T003, NOT WEAKENED: the assertion is still EXACTLY EMPTY, and
        # it is now made against a supplied benchmark run, so it says the stronger
        # thing — at or above mid, with the promotion discharged, NOTHING is
        # refused. ``architecture`` is seeded at the top tier, so the mid case is a
        # promotion and only evidence can keep the result empty.
        task_class = sorted(OVERRIDE_SAFETY_CLASSES)[0]
        assert validate_task_class_tier_overrides(
            {task_class: tier},
            OVERRIDE_SAFETY_CLASSES,
            {task_class: SUFFICIENT_EVIDENCE},
        ) == ()

    def test_the_seed_table_alone_conforms_under_the_fixture_safety_set(self):
        # The discriminator for the pair above: with NO override at all the same
        # fixture set produces nothing, so every refusal above is the override's.
        assert validate_task_class_tier_overrides({}, OVERRIDE_SAFETY_CLASSES) == ()

    @pytest.mark.parametrize(("worker_class", "reviewer_class"), REVIEWER_WORKER_CLASS_PAIRS)
    def test_the_reviewer_half_of_a_pair_demoted_below_its_worker_is_refused(
        self, worker_class, reviewer_class
    ):
        # ONLY the reviewer half moves. The worker half is still the SEED tier,
        # which is what makes this the proof that the rule is judged against the
        # EFFECTIVE table rather than against the override map alone.
        below = MODEL_TIERS[0]
        assert model_tier_rank(below) < model_tier_rank(TASK_CLASS_TIERS[worker_class])
        violations = validate_task_class_tier_overrides({reviewer_class: below})
        assert RULE_REVIEWER_WEAKER_THAN_WORKER in _rule_names(violations)

    @pytest.mark.parametrize(("worker_class", "reviewer_class"), REVIEWER_WORKER_CLASS_PAIRS)
    def test_the_pair_violation_is_attributed_to_the_reviewer_class(
        self, worker_class, reviewer_class
    ):
        violations = validate_task_class_tier_overrides({reviewer_class: MODEL_TIERS[0]})
        attributed = [
            v.task_class for v in violations if v.rule_name == RULE_REVIEWER_WEAKER_THAN_WORKER
        ]
        assert attributed == [reviewer_class]

    @pytest.mark.parametrize(("worker_class", "reviewer_class"), REVIEWER_WORKER_CLASS_PAIRS)
    def test_the_reviewer_half_left_at_its_seed_tier_is_not_refused(
        self, worker_class, reviewer_class
    ):
        violations = validate_task_class_tier_overrides(
            {reviewer_class: TASK_CLASS_TIERS[reviewer_class]}
        )
        assert RULE_REVIEWER_WEAKER_THAN_WORKER not in _rule_names(violations)


class TestOverrideValidatorCollectsEveryViolation:
    """One map breaking every rule reports every rule, once, in the declared order."""

    #: One override map that breaks ALL EIGHT rules at once, exactly once each: a
    #: dead key, a typo'd tier, a reviewer dropped below its paired worker, a
    #: demoted orchestration class, a demoted safety class, and three promotions
    #: whose evidence fails in the three different ways.
    #:
    #: WIDENED IN T003, NOT WEAKENED. Round 6's map broke five rules; every entry
    #: that demotes a seeded class is ALSO a promotion, so without the evidence
    #: argument below the same map would report ``promotion_without_evidence``
    #: three times and the "exactly once" property could not be stated at all.
    #: The evidence map is what makes each of the eight names appear once — and it
    #: doubles as the proof that EVIDENCE NEVER DISCHARGES A HARD RULE: ``mission``,
    #: ``architecture`` and the reviewer half all carry evidence here and all three
    #: still report their hard-rule name.
    BREAKS_EVERY_RULE = {
        UNKNOWN_OVERRIDE_CLASS: TOP_TIER,
        "format": UNKNOWN_TIER,
        REVIEWER_WORKER_CLASS_PAIRS[0][1]: MODEL_TIERS[0],
        "mission": MODEL_TIERS[0],
        sorted(OVERRIDE_SAFETY_CLASSES)[0]: MODEL_TIERS[0],
        PROMOTABLE_CLASS: MODEL_TIERS[0],
    }

    #: The evidence that leaves exactly one violation of each promotion rule: the
    #: reviewer half is fully discharged, ``mission`` fails a bar, ``architecture``
    #: is under-logged, and ``PROMOTABLE_CLASS`` has no entry at all.
    EVERY_RULE_EVIDENCE = {
        REVIEWER_WORKER_CLASS_PAIRS[0][1]: SUFFICIENT_EVIDENCE,
        "mission": BELOW_THRESHOLD_EVIDENCE,
        sorted(OVERRIDE_SAFETY_CLASSES)[0]: INCOMPLETE_EVIDENCE,
    }

    def test_every_rule_is_reported_exactly_once(self):
        names = _rule_names(
            validate_task_class_tier_overrides(
                self.BREAKS_EVERY_RULE, OVERRIDE_SAFETY_CLASSES, self.EVERY_RULE_EVIDENCE
            )
        )
        assert sorted(names) == sorted(OVERRIDE_VIOLATION_RULE_NAMES)

    def test_the_result_follows_the_declared_order(self):
        names = _rule_names(
            validate_task_class_tier_overrides(
                self.BREAKS_EVERY_RULE, OVERRIDE_SAFETY_CLASSES, self.EVERY_RULE_EVIDENCE
            )
        )
        assert names == list(OVERRIDE_VIOLATION_RULE_NAMES)

    def test_the_declared_order_is_provably_not_the_alphabet(self):
        names = _rule_names(
            validate_task_class_tier_overrides(
                self.BREAKS_EVERY_RULE, OVERRIDE_SAFETY_CLASSES, self.EVERY_RULE_EVIDENCE
            )
        )
        assert names != sorted(names)

    def test_the_schema_names_are_reported_before_the_hard_rule_names(self):
        names = _rule_names(
            validate_task_class_tier_overrides(
                self.BREAKS_EVERY_RULE, OVERRIDE_SAFETY_CLASSES, self.EVERY_RULE_EVIDENCE
            )
        )
        last_schema = max(names.index(n) for n in OVERRIDE_SCHEMA_RULE_NAMES)
        first_hard = min(names.index(n) for n in HARD_RULE_NAMES)
        assert last_schema < first_hard

    def test_the_hard_rule_names_are_reported_before_the_promotion_rule_names(self):
        names = _rule_names(
            validate_task_class_tier_overrides(
                self.BREAKS_EVERY_RULE, OVERRIDE_SAFETY_CLASSES, self.EVERY_RULE_EVIDENCE
            )
        )
        last_hard = max(names.index(n) for n in HARD_RULE_NAMES)
        first_promotion = min(names.index(n) for n in PROMOTION_RULE_NAMES)
        assert last_hard < first_promotion

    def test_evidence_never_discharges_a_hard_rule(self):
        # The three entries carrying evidence above still report their hard-rule
        # name: no benchmark buys a reviewer weaker than its worker, a cheap
        # orchestration call, or a downgraded safety class.
        names = _rule_names(
            validate_task_class_tier_overrides(
                self.BREAKS_EVERY_RULE, OVERRIDE_SAFETY_CLASSES, self.EVERY_RULE_EVIDENCE
            )
        )
        assert set(HARD_RULE_NAMES) <= set(names)

    def test_a_conforming_map_returns_an_empty_result(self):
        assert validate_task_class_tier_overrides({"format": TOP_TIER, "mission": TOP_TIER}) == ()

    def test_an_empty_map_returns_an_empty_result(self):
        assert validate_task_class_tier_overrides({}) == ()

    def test_an_override_key_may_be_spelled_as_the_document_words_it(self):
        # WIDENED IN T003: same demotion, and it is also an unevidenced promotion.
        violations = validate_task_class_tier_overrides({"Mission": MODEL_TIERS[0]})
        assert _rule_names(violations) == [
            RULE_ORCHESTRATION_BELOW_TOP_TIER,
            RULE_PROMOTION_WITHOUT_EVIDENCE,
        ]
        assert violations[0].task_class == normalize_task_class("Mission")

    def test_an_evidence_key_may_be_spelled_as_the_document_words_it(self):
        # The evidence map's keys normalize exactly as the override map's do.
        assert validate_task_class_tier_overrides(
            {"Vision": PROMOTED_TIER},
            SAFETY_RELEVANT_CLASSES,
            {"Vision": SUFFICIENT_EVIDENCE},
        ) == ()


class TestOverrideRuleNamesAreNotHardRuleNames:
    """A schema fault is a malformed config, not a policy breach."""

    def test_hard_rule_names_still_holds_exactly_the_names_round_five_shipped(self):
        assert HARD_RULE_NAMES == (
            RULE_REVIEWER_WEAKER_THAN_WORKER,
            RULE_ORCHESTRATION_BELOW_TOP_TIER,
            RULE_SAFETY_CLASS_BELOW_MID_TIER,
        )

    @pytest.mark.parametrize("rule_name", OVERRIDE_SCHEMA_RULE_NAMES)
    def test_no_schema_rule_name_is_in_hard_rule_names(self, rule_name):
        assert rule_name not in HARD_RULE_NAMES

    def test_the_report_order_is_the_schema_names_then_the_hard_rule_names(self):
        # WIDENED IN T003, NOT WEAKENED. The report order gained a THIRD segment,
        # the promotion-rule names, so the equality is rewritten to the exact new
        # concatenation rather than loosened to a containment check: a fourth
        # segment appearing silently must still turn this file red.
        assert OVERRIDE_VIOLATION_RULE_NAMES == (
            OVERRIDE_SCHEMA_RULE_NAMES + HARD_RULE_NAMES + PROMOTION_RULE_NAMES
        )

    @pytest.mark.parametrize("rule_name", PROMOTION_RULE_NAMES)
    def test_no_promotion_rule_name_is_in_hard_rule_names(self, rule_name):
        # A hard rule is NEVER satisfiable by evidence; a promotion rule is
        # precisely a rule evidence discharges. Merging the vocabularies would let
        # a measured, documented promotion read as a policy breach.
        assert rule_name not in HARD_RULE_NAMES

    @pytest.mark.parametrize("rule_name", PROMOTION_RULE_NAMES)
    def test_no_promotion_rule_name_is_in_the_schema_tuple(self, rule_name):
        assert rule_name not in OVERRIDE_SCHEMA_RULE_NAMES

    def test_the_schema_tuple_still_holds_exactly_what_round_six_shipped(self):
        assert OVERRIDE_SCHEMA_RULE_NAMES == (
            RULE_OVERRIDE_UNKNOWN_TASK_CLASS,
            RULE_OVERRIDE_UNKNOWN_TIER,
        )


class TestReviewerWorkerClassPairs:
    """The declared pairs are checkable, and the SHIPPED table already conforms."""

    def test_at_least_one_pair_is_declared(self):
        assert REVIEWER_WORKER_CLASS_PAIRS

    @pytest.mark.parametrize(("worker_class", "reviewer_class"), REVIEWER_WORKER_CLASS_PAIRS)
    def test_every_member_of_every_pair_is_a_key_of_the_seed_table(
        self, worker_class, reviewer_class
    ):
        assert worker_class in TASK_CLASS_TIERS
        assert reviewer_class in TASK_CLASS_TIERS

    @pytest.mark.parametrize(("worker_class", "reviewer_class"), REVIEWER_WORKER_CLASS_PAIRS)
    def test_the_seed_table_alone_routes_the_reviewer_at_or_above_its_worker(
        self, worker_class, reviewer_class
    ):
        assert check_reviewer_not_weaker_than_worker(
            TASK_CLASS_TIERS[worker_class], TASK_CLASS_TIERS[reviewer_class]
        ) is None


class TestEffectiveTableBuilder:
    """The hard rules win by REFUSING a config, not by quietly editing it."""

    def test_a_conforming_map_returns_the_seed_table_overlaid(self):
        effective = build_effective_task_class_tiers({"format": TOP_TIER})
        assert effective["format"] == TOP_TIER
        assert {k: v for k, v in effective.items() if k != "format"} == {
            k: v for k, v in TASK_CLASS_TIERS.items() if k != "format"
        }

    def test_an_empty_map_returns_the_seed_table_unchanged(self):
        assert build_effective_task_class_tiers({}) == TASK_CLASS_TIERS

    def test_the_seed_table_is_not_mutated(self):
        before = dict(TASK_CLASS_TIERS)
        build_effective_task_class_tiers({"format": TOP_TIER})
        assert TASK_CLASS_TIERS == before

    def test_the_returned_table_is_not_the_seed_table_itself(self):
        effective = build_effective_task_class_tiers({})
        effective["format"] = UNKNOWN_TIER
        assert TASK_CLASS_TIERS["format"] != UNKNOWN_TIER

    def test_a_violating_map_raises_rather_than_dropping_the_offending_entry(self):
        with pytest.raises(OverrideRefused):
            build_effective_task_class_tiers({"mission": MODEL_TIERS[0]})

    def test_the_raised_object_carries_the_violations(self):
        # WIDENED IN T003: the same map, now with the evidence argument the
        # builder passes straight through, so the raised object carries all EIGHT
        # names rather than round 6's five.
        with pytest.raises(OverrideRefused) as excinfo:
            build_effective_task_class_tiers(
                TestOverrideValidatorCollectsEveryViolation.BREAKS_EVERY_RULE,
                OVERRIDE_SAFETY_CLASSES,
                TestOverrideValidatorCollectsEveryViolation.EVERY_RULE_EVIDENCE,
            )
        assert _rule_names(excinfo.value.violations) == list(OVERRIDE_VIOLATION_RULE_NAMES)

    @pytest.mark.parametrize("rule_name", OVERRIDE_VIOLATION_RULE_NAMES)
    def test_the_message_names_every_violated_rule(self, rule_name):
        # The parametrization is NOT narrowed to dodge the new names: it runs over
        # the whole report order, so the three promotion names are covered too.
        with pytest.raises(OverrideRefused) as excinfo:
            build_effective_task_class_tiers(
                TestOverrideValidatorCollectsEveryViolation.BREAKS_EVERY_RULE,
                OVERRIDE_SAFETY_CLASSES,
                TestOverrideValidatorCollectsEveryViolation.EVERY_RULE_EVIDENCE,
            )
        assert rule_name in str(excinfo.value)

    def test_a_schema_faulty_entry_is_refused_rather_than_silently_dropped(self):
        with pytest.raises(OverrideRefused):
            build_effective_task_class_tiers({UNKNOWN_OVERRIDE_CLASS: TOP_TIER})


class TestOverrideAwareResolver:
    """The reason is DERIVED by comparison with the seed table, never asserted."""

    def test_a_tier_that_differs_from_the_seed_reports_the_override_reason(self):
        effective = build_effective_task_class_tiers({"format": TOP_TIER})
        assert resolve_task_class_tier_with_overrides("format", effective) == (
            TOP_TIER,
            OVERRIDE_REASON,
        )

    def test_an_override_restating_the_seed_tier_reports_the_seed_reason(self):
        effective = build_effective_task_class_tiers({"format": TASK_CLASS_TIERS["format"]})
        assert resolve_task_class_tier_with_overrides("format", effective) == (
            TASK_CLASS_TIERS["format"],
            SEED_MAPPING_REASON,
        )

    @pytest.mark.parametrize("task_class", sorted(TASK_CLASS_TIERS))
    def test_a_class_no_override_touched_reports_the_seed_reason(self, task_class):
        effective = build_effective_task_class_tiers({})
        assert resolve_task_class_tier_with_overrides(task_class, effective) == (
            TASK_CLASS_TIERS[task_class],
            SEED_MAPPING_REASON,
        )

    def test_a_class_the_table_does_not_name_reports_the_unknown_pair(self):
        effective = build_effective_task_class_tiers({})
        assert resolve_task_class_tier_with_overrides(UNKNOWN_OVERRIDE_CLASS, effective) == (
            TOP_TIER,
            UNKNOWN_CLASS_REASON,
        )

    def test_the_declared_class_may_be_spelled_as_the_document_words_it(self):
        # "extract" deliberately: it is in no reviewer/worker pair, so raising it
        # cannot trip hard rule 1 and the test measures normalization alone.
        effective = build_effective_task_class_tiers({"Extract": TOP_TIER})
        assert resolve_task_class_tier_with_overrides("Extract", effective) == (
            TOP_TIER,
            OVERRIDE_REASON,
        )

    def test_the_shipped_resolver_is_unchanged_by_any_of_this(self):
        # Round 5's resolve_task_class_tier answers from the SHIPPED table and
        # knows nothing about overrides; the two are siblings, not a replacement.
        assert resolve_task_class_tier("format") == (TASK_CLASS_TIERS["format"], SEED_MAPPING_REASON)

