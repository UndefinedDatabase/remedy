"""Tests for packages/orchestration/model_routing.py — F110 T002a, the class table, and T002b, the three hard rules.

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

from pathlib import Path

import pytest

from packages.orchestration.model_routing import (
    HARD_RULE_NAMES,
    MID_TIER,
    MODEL_TIERS,
    ORCHESTRATION_TASK_CLASSES,
    RULE_ORCHESTRATION_BELOW_TOP_TIER,
    RULE_REVIEWER_WEAKER_THAN_WORKER,
    RULE_SAFETY_CLASS_BELOW_MID_TIER,
    SAFETY_RELEVANT_CLASSES,
    SEED_MAPPING_REASON,
    TASK_CLASS_TIERS,
    TOP_TIER,
    UNKNOWN_CLASS_REASON,
    check_orchestration_class_routed_to_top_tier,
    check_reviewer_not_weaker_than_worker,
    check_safety_relevant_class_not_below_mid_tier,
    model_tier_rank,
    normalize_task_class,
    resolve_task_class_tier,
    validate_routing_choice,
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
    """The feature file's rule — orchestrator and mission-compile calls always top tier."""

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

    def test_the_covered_classes_are_the_two_the_feature_file_names(self):
        assert ORCHESTRATION_TASK_CLASSES == frozenset(
            {normalize_task_class("orchestrator"), normalize_task_class("mission compile")}
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
