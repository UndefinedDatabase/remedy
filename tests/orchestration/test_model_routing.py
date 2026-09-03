"""Tests for packages/orchestration/model_routing.py — F110 T002a, the class table.

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
"""

from __future__ import annotations

from pathlib import Path

import pytest

from packages.orchestration.model_routing import (
    MODEL_TIERS,
    SEED_MAPPING_REASON,
    TASK_CLASS_TIERS,
    TOP_TIER,
    UNKNOWN_CLASS_REASON,
    normalize_task_class,
    resolve_task_class_tier,
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
