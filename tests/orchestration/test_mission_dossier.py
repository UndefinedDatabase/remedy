"""F071 — the mission dossier: structure, budget, versioning, compression.

What the order requires proof of (T001 structure and update mechanics):

  * the five sections render in ONE fixed order, and that order is stable
    across any number of updates — the dossier is a cache-stable prompt
    prefix, so drifting bytes are a defect;
  * the goal is copied once and stays byte-identical across many iterations;
  * update() APPENDS: a fact whose id is already present replaces that line
    (one line per milestone, always), a new id appends, decisions accumulate;
  * a risk that closes moves to DECISIONS with its outcome and leaves the
    open-only RISKS section — one home per fact (A9);
  * the budget comes from config with a conservative default, and every count
    carries the basis that produced it (P6) — no invented counter;
  * every version is stored as dossier_v<N>.md and no version is overwritten;
  * the over-budget flag is honest: it is metadata, never counted against the
    budget it reports on, and never a truncation;
  * the compression rules are ASSERTIONS, not prose — open items survive,
    resolved items merge away, the goal stays byte-identical to iteration one;
  * a compression that breaks a rule is REFUSED and returns the dossier
    untouched — the rules are checked, not believed, and checked against the
    REBUILT document so an open item cannot be lost by crossing sections
    (R-0172);
  * a failed compression (no provider, bad answer, broken rule, an exception)
    leaves the previous dossier plus the raw facts and an honest flag.

No provider is contacted: every "LLM" here is a local callable returning
recorded text.

Every test that writes goes to ``tmp_path`` with the mission root passed
explicitly via ``root=``, so the repository's real data root is never touched.
"""
from __future__ import annotations

import json

import pytest

from packages.orchestration.config import get_key_spec
from packages.orchestration.mission_dossier import (
    COMPRESSION_INVALID_ANSWER,
    COMPRESSION_NO_PROVIDER,
    COMPRESSION_OK,
    COMPRESSION_PROVIDER_ERROR,
    COMPRESSION_RULE_VIOLATION,
    COMPRESSION_RULES,
    COMPRESSION_WITHIN_BUDGET,
    CONFIG_KEY_MAX_TOKENS,
    DEFAULT_MAX_TOKENS,
    DOSSIER_COMPRESSION_SCHEMA_V,
    DOSSIER_SECTIONS,
    DOSSIER_TOKEN_BASIS,
    DOSSIER_TOKEN_CONFIDENCE,
    DOSSIER_VERSION_TEMPLATE,
    MAX_RECENT_DECISIONS,
    NO_NEXT_STEP,
    SECTION_DECISIONS,
    SECTION_GOAL,
    SECTION_MILESTONES,
    SECTION_NEXT,
    SECTION_RISKS,
    DossierCompression,
    DossierItem,
    IterationFacts,
    append_facts,
    build_compression_prompt,
    compress_dossier,
    compression_rule_violation,
    count_dossier_tokens,
    dossier_budget_from_config,
    dossier_sections,
    dossier_tokens,
    dossier_version_path,
    dossier_versions,
    latest_dossier_version,
    open_items,
    render_dossier,
    render_dossier_body,
    resolve_risk,
    start_dossier,
    update,
    write_dossier_version,
)

PROJECT = "proj-f071"
MISSION = "mission-f071"
GOAL = "The payments API stays releasable while the ledger is rewritten"


class _Config:
    """The smallest thing that behaves like RemedyConfig for one key."""

    def __init__(self, **values):
        self._values = values

    def get(self, key):
        return self._values.get(key)


def _dossier():
    """A dossier with something in every section."""
    return append_facts(start_dossier(GOAL), IterationFacts(
        milestones=[DossierItem(id="M001", text="the ledger is rewritten"),
                    DossierItem(id="M002", text="the API stays releasable")],
        risks=[DossierItem(id="R001", text="the migration is not reversible"),
               DossierItem(id="R002", text="the smoke has no fixture data")],
        decisions=[DossierItem(id="D001", text="use the existing writer",
                               resolved=True, outcome="no second mechanism")],
        next_step="dispatch the first job for M001",
    ))


class TestSectionOrdering:
    def test_the_five_sections_are_the_contract(self):
        assert DOSSIER_SECTIONS == (
            SECTION_GOAL, SECTION_MILESTONES, SECTION_RISKS,
            SECTION_DECISIONS, SECTION_NEXT)

    def test_every_section_renders_even_when_empty(self):
        names = [name for name, _ in dossier_sections(start_dossier(GOAL))]
        assert names == list(DOSSIER_SECTIONS)

    def test_the_order_is_stable_across_updates(self):
        dossier = start_dossier(GOAL)
        seen = []
        for index in range(6):
            dossier = append_facts(dossier, IterationFacts(
                milestones=[DossierItem(id=f"M{index:03d}", text="outcome")],
                risks=[DossierItem(id=f"R{index:03d}", text="a risk")],
                decisions=[DossierItem(id=f"D{index:03d}", text="a call",
                                       resolved=True, outcome="held")],
                next_step=f"step {index}"))
            seen.append([name for name, _ in dossier_sections(dossier)])
        assert seen == [list(DOSSIER_SECTIONS)] * 6

    def test_the_body_renders_the_sections_in_that_order(self):
        body = render_dossier_body(_dossier())
        positions = [body.index(f"## {name}") for name in DOSSIER_SECTIONS]
        assert positions == sorted(positions)

    def test_an_empty_next_step_says_so_rather_than_vanishing(self):
        sections = dict(dossier_sections(start_dossier(GOAL)))
        assert sections[SECTION_NEXT] == NO_NEXT_STEP

    def test_a_dossier_needs_a_goal(self):
        with pytest.raises(ValueError):
            start_dossier("   ")


class TestGoalIsImmutable:
    def test_the_goal_survives_many_updates_byte_identical(self):
        first = start_dossier(GOAL)
        dossier = first
        for index in range(20):
            dossier = append_facts(dossier, IterationFacts(
                milestones=[DossierItem(id=f"M{index:03d}", text="x" * 40)],
                next_step=f"step {index}"))
        assert dossier.goal == first.goal
        assert dict(dossier_sections(dossier))[SECTION_GOAL] == \
            dict(dossier_sections(first))[SECTION_GOAL]

    def test_the_goal_is_normalized_once_at_the_start(self):
        assert start_dossier("  a   goal\n  with  space ").goal == \
            "a goal with space"


# ---------------------------------------------------------------------------
# T001 — update() append mechanics
# ---------------------------------------------------------------------------


class TestAppendMechanics:
    def test_a_new_id_appends(self):
        dossier = append_facts(_dossier(), IterationFacts(
            milestones=[DossierItem(id="M003", text="a third outcome")]))
        assert [m.id for m in dossier.milestones] == ["M001", "M002", "M003"]

    def test_a_known_id_replaces_its_line_in_place(self):
        dossier = append_facts(_dossier(), IterationFacts(
            milestones=[DossierItem(id="M001", text="the ledger is rewritten",
                                    resolved=True, outcome="gate released")]))
        assert [m.id for m in dossier.milestones] == ["M001", "M002"]
        assert dossier.milestones[0].resolved is True

    def test_one_line_per_milestone_however_often_it_is_restated(self):
        dossier = _dossier()
        for _ in range(5):
            dossier = append_facts(dossier, IterationFacts(
                milestones=[DossierItem(id="M001", text="restated")]))
        body = dict(dossier_sections(dossier))[SECTION_MILESTONES]
        assert len([line for line in body.splitlines()
                    if line.startswith("- M001 ")]) == 1

    def test_the_next_step_is_single_and_replaced(self):
        dossier = append_facts(_dossier(), IterationFacts(next_step="do M002"))
        assert dict(dossier_sections(dossier))[SECTION_NEXT] == "do M002"

    def test_an_empty_next_step_leaves_the_current_one_alone(self):
        before = _dossier()
        after = append_facts(before, IterationFacts(next_step="  "))
        assert after.next_step == before.next_step

    def test_the_version_advances_on_every_update(self):
        dossier = start_dossier(GOAL)
        assert dossier.version == 1
        assert append_facts(dossier, IterationFacts()).version == 2

    def test_decisions_render_only_the_recent_few(self):
        dossier = _dossier()
        for index in range(MAX_RECENT_DECISIONS + 3):
            dossier = append_facts(dossier, IterationFacts(
                decisions=[DossierItem(id=f"D1{index:02d}", text="a call",
                                       resolved=True, outcome="held")]))
        body = dict(dossier_sections(dossier))[SECTION_DECISIONS]
        assert len(body.splitlines()) == MAX_RECENT_DECISIONS
        # The RECORD keeps them all; only the rendering is the recent few.
        assert len(dossier.decisions) == MAX_RECENT_DECISIONS + 4


class TestOneHomePerFact:
    def test_a_resolved_risk_leaves_the_open_only_risks_section(self):
        dossier = resolve_risk(_dossier(), "R001", "the migration is reversible")
        risks = dict(dossier_sections(dossier))[SECTION_RISKS]
        assert "R001" not in risks
        assert "R002" in risks

    def test_a_resolved_risk_is_recorded_once_in_decisions_with_its_outcome(self):
        dossier = resolve_risk(_dossier(), "R001", "rollback proven")
        decisions = dict(dossier_sections(dossier))[SECTION_DECISIONS]
        assert decisions.count("R001") == 1
        assert "outcome: rollback proven" in decisions

    def test_resolving_through_iteration_facts_does_the_same(self):
        dossier = append_facts(_dossier(), IterationFacts(
            resolved_risks=[("R002", "fixture data landed")]))
        assert "R002" not in dict(dossier_sections(dossier))[SECTION_RISKS]
        assert "fixture data landed" in \
            dict(dossier_sections(dossier))[SECTION_DECISIONS]

    def test_resolving_an_unknown_risk_changes_nothing(self):
        before = _dossier()
        assert resolve_risk(before, "R999", "n/a") == before

    def test_open_items_are_the_not_done_milestones_and_open_risks(self):
        dossier = resolve_risk(_dossier(), "R001", "closed")
        assert {i.id for i in open_items(dossier)} == {"M001", "M002", "R002"}


# ---------------------------------------------------------------------------
# T001 — the budget: config seam, labeled counting basis (P6)
# ---------------------------------------------------------------------------


class TestBudget:
    def test_the_config_key_exists_with_the_conservative_default(self):
        spec = get_key_spec(CONFIG_KEY_MAX_TOKENS)
        assert spec is not None
        assert spec.env_var == "REMEDY_DOSSIER_MAX_TOKENS"
        assert spec.value_type is int
        assert spec.default == DEFAULT_MAX_TOKENS == 3000

    def test_config_supplies_the_budget(self):
        config = _Config(**{CONFIG_KEY_MAX_TOKENS: 1234})
        assert dossier_budget_from_config(config) == 1234

    def test_an_explicit_value_beats_config(self):
        config = _Config(**{CONFIG_KEY_MAX_TOKENS: 1234})
        assert dossier_budget_from_config(config, max_tokens=42) == 42

    def test_an_unset_key_falls_back_to_the_default(self):
        assert dossier_budget_from_config(_Config()) == DEFAULT_MAX_TOKENS

    def test_a_nonsense_budget_is_refused_rather_than_clamped(self):
        with pytest.raises(ValueError):
            dossier_budget_from_config(_Config(), max_tokens=0)


class TestCountingBasisIsLabeled:
    def test_every_count_says_what_produced_it(self):
        count = count_dossier_tokens("some dossier text")
        assert count.basis == DOSSIER_TOKEN_BASIS
        assert count.confidence == DOSSIER_TOKEN_CONFIDENCE == "low"
        assert count.to_json()["basis"] == DOSSIER_TOKEN_BASIS

    def test_the_basis_names_the_existing_seam_it_reuses(self):
        assert "token_economy.estimate_text_tokens" in DOSSIER_TOKEN_BASIS

    def test_the_count_is_the_existing_seams_own_number(self):
        from packages.orchestration.token_economy import estimate_text_tokens

        text = render_dossier_body(_dossier())
        assert dossier_tokens(_dossier()).tokens == estimate_text_tokens(text)

    def test_a_bigger_dossier_counts_higher(self):
        small = _dossier()
        big = append_facts(small, IterationFacts(
            risks=[DossierItem(id=f"R1{i:02d}", text="x" * 200)
                   for i in range(20)]))
        assert dossier_tokens(big).tokens > dossier_tokens(small).tokens


class TestOverBudgetFlagIsHonest:
    def test_the_flag_is_metadata_and_is_not_counted_against_the_budget(self):
        import dataclasses

        clean = _dossier()
        flagged = dataclasses.replace(
            clean, over_budget=True, budget_note="over by 400 tokens")
        assert dossier_tokens(flagged).tokens == dossier_tokens(clean).tokens
        assert "OVER BUDGET" not in render_dossier_body(flagged)

    def test_the_written_document_shows_the_flag_and_says_nothing_was_cut(self):
        import dataclasses

        flagged = dataclasses.replace(
            _dossier(), over_budget=True, budget_note="compression failed")
        text = render_dossier(flagged)
        assert "OVER BUDGET — compression failed" in text
        assert "Nothing was truncated" in text

    def test_a_dossier_within_budget_carries_no_flag(self):
        assert "OVER BUDGET" not in render_dossier(_dossier())


# ---------------------------------------------------------------------------
# T001 — versioning
# ---------------------------------------------------------------------------


class TestVersioning:
    def test_a_version_is_stored_under_its_own_name(self, tmp_path):
        path = write_dossier_version(PROJECT, MISSION, _dossier(), tmp_path)
        assert path.name == DOSSIER_VERSION_TEMPLATE.format(version=2)
        assert path.read_text(encoding="utf-8") == render_dossier(_dossier())

    def test_versions_live_in_the_missions_own_evidence_area(self, tmp_path):
        path = dossier_version_path(PROJECT, MISSION, 3, tmp_path)
        assert path.parent.name == "evidence"
        assert MISSION in path.parts

    def test_no_version_is_ever_overwritten(self, tmp_path):
        first = _dossier()
        write_dossier_version(PROJECT, MISSION, first, tmp_path)
        before = dossier_version_path(
            PROJECT, MISSION, first.version, tmp_path).read_text()
        second = append_facts(first, IterationFacts(next_step="something else"))
        write_dossier_version(PROJECT, MISSION, second, tmp_path)
        after = dossier_version_path(
            PROJECT, MISSION, first.version, tmp_path).read_text()
        assert after == before
        assert dossier_versions(PROJECT, MISSION, tmp_path) == [2, 3]

    def test_the_newest_version_is_findable(self, tmp_path):
        assert latest_dossier_version(PROJECT, MISSION, tmp_path) == 0
        dossier = _dossier()
        for _ in range(3):
            write_dossier_version(PROJECT, MISSION, dossier, tmp_path)
            dossier = append_facts(dossier, IterationFacts())
        assert latest_dossier_version(PROJECT, MISSION, tmp_path) == 4

    def test_the_layout_is_diff_friendly_one_item_per_line(self, tmp_path):
        text = write_dossier_version(
            PROJECT, MISSION, _dossier(), tmp_path).read_text(encoding="utf-8")
        milestone_lines = [line for line in text.splitlines()
                           if line.startswith("- M")]
        assert milestone_lines == [
            "- M001 [open] the ledger is rewritten",
            "- M002 [open] the API stays releasable",
        ]

    def test_a_foreign_file_in_the_area_is_not_read_as_a_version(self, tmp_path):
        write_dossier_version(PROJECT, MISSION, _dossier(), tmp_path)
        stray = dossier_version_path(PROJECT, MISSION, 2, tmp_path).parent
        (stray / "dossier_vNEXT.md").write_text("not a version", encoding="utf-8")
        assert dossier_versions(PROJECT, MISSION, tmp_path) == [2]


# ---------------------------------------------------------------------------
# T002 — the compression call, its rules, and the honest failure path
# ---------------------------------------------------------------------------


def _answer(dossier, *, milestones=None, risks=None, decisions=None,
            next_step="keep going"):
    """A compression answer as a provider would return it: JSON text.

    Defaults to the well-behaved rewrite — every open item kept, every
    resolved risk merged away — so each test only has to state its own
    deviation from the rules.
    """
    if milestones is None:
        milestones = [{"id": m.id, "text": "short"} for m in dossier.milestones]
    if risks is None:
        risks = [{"id": r.id, "text": "short"}
                 for r in dossier.risks if not r.resolved]
    if decisions is None:
        decisions = [{"id": d.id, "text": "short"}
                     for d in dossier.decisions[-1:]]
    return json.dumps({
        "schema_v": DOSSIER_COMPRESSION_SCHEMA_V,
        "milestones": milestones,
        "risks": risks,
        "decisions": decisions,
        "next_step": next_step,
    })


class _Provider:
    """A fake provider: returns recorded text and counts how often it is called."""

    def __init__(self, *replies):
        self.replies = list(replies)
        self.prompts = []

    def __call__(self, prompt, attempt):
        self.prompts.append(prompt)
        return self.replies[min(attempt, len(self.replies) - 1)]


def _bloated():
    """A dossier well past any small budget, with one risk already resolved."""
    dossier = append_facts(_dossier(), IterationFacts(
        risks=[DossierItem(id=f"R1{i:02d}", text="a long standing risk " * 12)
               for i in range(10)],
        decisions=[DossierItem(id=f"D1{i:02d}", text="a recorded call " * 12,
                               resolved=True, outcome="held")
                   for i in range(4)]))
    return resolve_risk(dossier, "R001", "the migration is reversible")


class TestCompressionRulesAreTheContract:
    def test_the_three_rules_are_recorded_verbatim(self):
        assert COMPRESSION_RULES == (
            "merge resolved risks away",
            "keep every open item",
            "never drop the goal",
        )

    def test_every_rule_is_quoted_into_the_prompt(self):
        prompt = build_compression_prompt(_bloated())
        for rule in COMPRESSION_RULES:
            assert rule in prompt

    def test_the_prompt_names_the_ids_that_must_survive(self):
        dossier = _bloated()
        prompt = build_compression_prompt(dossier)
        for item in open_items(dossier):
            assert item.id in prompt

    def test_never_drop_the_goal_is_the_shape_of_the_schema(self):
        # Not a prompt request: the provider has no field to answer with.
        assert "goal" not in DossierCompression.model_fields

    def test_the_draft_contract_is_not_registered(self):
        from packages.orchestration.schemas.models import SCHEMA_REGISTRY

        # A compression answer is never persisted under its tag — what reaches
        # disk is the rewritten dossier markdown.
        assert DOSSIER_COMPRESSION_SCHEMA_V not in SCHEMA_REGISTRY


class TestCompressionHoldsToTheRules:
    def test_open_items_survive_compression(self):
        dossier = _bloated()
        expected = {item.id for item in open_items(dossier)}
        result = compress_dossier(dossier, _Provider(_answer(dossier)))
        assert result.status == COMPRESSION_OK
        assert {item.id for item in open_items(result.dossier)} == expected

    def test_resolved_items_merge_away(self):
        dossier = _bloated()
        result = compress_dossier(dossier, _Provider(_answer(dossier)))
        assert "R001" not in {r.id for r in result.dossier.risks}
        assert "R001" not in dict(dossier_sections(result.dossier))[SECTION_RISKS]
        # Merged away, not lost: its outcome is still on the record.
        assert "R001" in {d.id for d in result.dossier.decisions}

    def test_the_goal_is_byte_identical_to_iteration_one(self):
        first = start_dossier(GOAL)
        dossier = _bloated()
        result = compress_dossier(dossier, _Provider(_answer(dossier)))
        assert result.dossier.goal == first.goal
        assert dict(dossier_sections(result.dossier))[SECTION_GOAL] == \
            dict(dossier_sections(first))[SECTION_GOAL]

    def test_compression_is_exactly_one_provider_call(self):
        dossier = _bloated()
        provider = _Provider(_answer(dossier))
        result = compress_dossier(dossier, provider)
        assert len(provider.prompts) == 1
        assert result.calls == 1

    def test_even_an_unparseable_answer_is_not_retried(self):
        provider = _Provider("not json at all")
        result = compress_dossier(_bloated(), provider)
        assert len(provider.prompts) == 1
        assert result.status == COMPRESSION_INVALID_ANSWER

    def test_the_document_actually_gets_smaller(self):
        dossier = _bloated()
        result = compress_dossier(dossier, _Provider(_answer(dossier)))
        assert dossier_tokens(result.dossier).tokens < dossier_tokens(dossier).tokens

    def test_a_compression_cannot_promote_a_milestone_to_done(self):
        dossier = _bloated()
        result = compress_dossier(dossier, _Provider(_answer(dossier)))
        # The answer carries text only; state is carried over, not granted.
        assert [m.resolved for m in result.dossier.milestones] == [False, False]


class TestRuleViolationsAreRefused:
    def test_dropping_an_open_item_is_refused(self):
        dossier = _bloated()
        kept = [{"id": r.id, "text": "short"}
                for r in dossier.risks if not r.resolved][1:]
        result = compress_dossier(
            dossier, _Provider(_answer(dossier, risks=kept)))
        assert result.status == COMPRESSION_RULE_VIOLATION
        assert "keep every open item" in result.detail

    def test_keeping_a_resolved_risk_in_risks_is_refused(self):
        dossier = _bloated()
        risks = [{"id": r.id, "text": "short"} for r in dossier.risks]
        result = compress_dossier(
            dossier, _Provider(_answer(dossier, risks=risks)))
        assert result.status == COMPRESSION_RULE_VIOLATION
        assert "merge resolved risks away" in result.detail

    def test_an_invented_fact_is_refused(self):
        dossier = _bloated()
        risks = [{"id": r.id, "text": "short"}
                 for r in dossier.risks if not r.resolved]
        risks.append({"id": "R999", "text": "a risk nobody recorded"})
        result = compress_dossier(
            dossier, _Provider(_answer(dossier, risks=risks)))
        assert result.status == COMPRESSION_RULE_VIOLATION
        assert "R999" in result.detail

    def test_a_refused_compression_returns_the_dossier_untouched(self):
        dossier = _bloated()
        result = compress_dossier(dossier, _Provider(_answer(dossier, risks=[])))
        assert result.ok is False
        assert result.dossier == dossier

    def test_a_provider_that_raises_is_a_status_not_an_exception(self):
        def explode(prompt, attempt):
            raise RuntimeError("the provider is down")

        result = compress_dossier(_bloated(), explode)
        assert result.status == COMPRESSION_PROVIDER_ERROR
        assert "the provider is down" in result.detail
        assert result.dossier == _bloated()


class TestOpenItemsCannotBeLostAcrossSections:
    """R-0172: the rule check judges the REBUILT document, not the answer.

    ``_rebuild`` carries items per SECTION, so an open item returned under the
    wrong section is present in the answer and absent from the rebuild.
    Checking the answer would pass it and then silently drop the item.
    """

    def test_an_open_risk_returned_under_milestones_is_refused(self):
        dossier = _bloated()
        risks = [{"id": r.id, "text": "short"}
                 for r in dossier.risks if not r.resolved]
        moved, kept = risks[0], risks[1:]
        milestones = [{"id": m.id, "text": "short"} for m in dossier.milestones]
        result = compress_dossier(dossier, _Provider(_answer(
            dossier, milestones=[*milestones, moved], risks=kept)))
        assert result.status == COMPRESSION_RULE_VIOLATION
        assert "keep every open item" in result.detail
        assert moved["id"] in result.detail

    def test_an_open_milestone_returned_under_risks_is_refused(self):
        dossier = _bloated()
        milestones = [{"id": m.id, "text": "short"} for m in dossier.milestones]
        risks = [{"id": r.id, "text": "short"}
                 for r in dossier.risks if not r.resolved]
        result = compress_dossier(dossier, _Provider(_answer(
            dossier, milestones=milestones[1:],
            risks=[*risks, milestones[0]])))
        assert result.status == COMPRESSION_RULE_VIOLATION
        assert "keep every open item" in result.detail
        assert milestones[0]["id"] in result.detail

    def test_a_section_crossing_answer_leaves_the_dossier_untouched(self):
        dossier = _bloated()
        risks = [{"id": r.id, "text": "short"}
                 for r in dossier.risks if not r.resolved]
        milestones = [{"id": m.id, "text": "short"} for m in dossier.milestones]
        result = compress_dossier(dossier, _Provider(_answer(
            dossier, milestones=[*milestones, risks[0]], risks=risks[1:])))
        assert result.ok is False
        assert result.dossier == dossier
        assert {i.id for i in open_items(result.dossier)} == \
            {i.id for i in open_items(dossier)}

    def test_the_rule_check_judges_what_would_reach_disk(self):
        # The public predicate and the compressed result agree, because both
        # go through the same rebuild.
        dossier = _bloated()
        answer = DossierCompression(
            schema_v=DOSSIER_COMPRESSION_SCHEMA_V,
            milestones=[{"id": m.id, "text": "short"}
                        for m in dossier.milestones],
            risks=[{"id": r.id, "text": "short"}
                   for r in dossier.risks if not r.resolved],
            decisions=[], next_step="onwards")
        assert compression_rule_violation(dossier, answer) == ""
        result = compress_dossier(dossier, _Provider(_answer(dossier)))
        assert result.status == COMPRESSION_OK


class TestFailedCompressionLeavesTheHonestFlag:
    NEW_FACT = "the smoke needs a second fixture project"

    def _facts(self):
        return IterationFacts(
            risks=[DossierItem(id="R500", text=self.NEW_FACT)])

    def _assert_honest(self, result):
        assert result.over_budget is True
        text = render_dossier(result.dossier)
        # The raw facts are there, the flag is there, nothing was cut.
        assert self.NEW_FACT in text
        assert "OVER BUDGET" in text
        assert "Nothing was truncated" in text
        assert str(result.budget) in result.dossier.budget_note
        assert result.tokens.basis in result.dossier.budget_note

    def test_no_provider_leaves_the_flag(self):
        result = update(_bloated(), self._facts(), budget=50)
        assert result.status == COMPRESSION_NO_PROVIDER
        self._assert_honest(result)

    def test_an_unparseable_answer_leaves_the_flag(self):
        result = update(_bloated(), self._facts(), budget=50,
                        call_fn=_Provider("not json at all"))
        assert result.status == COMPRESSION_INVALID_ANSWER
        self._assert_honest(result)

    def test_a_broken_rule_leaves_the_flag(self):
        dossier = _bloated()
        result = update(dossier, self._facts(), budget=50,
                        call_fn=_Provider(_answer(dossier, risks=[])))
        assert result.status == COMPRESSION_RULE_VIOLATION
        self._assert_honest(result)

    def test_a_provider_that_raises_leaves_the_flag(self):
        def explode(prompt, attempt):
            raise RuntimeError("the provider is down")

        result = update(_bloated(), self._facts(), budget=50, call_fn=explode)
        assert result.status == COMPRESSION_PROVIDER_ERROR
        assert "the provider is down" in result.detail
        self._assert_honest(result)

    def test_a_compression_that_did_not_free_enough_room_still_says_so(self):
        dossier = _bloated()
        result = update(dossier, IterationFacts(), budget=1,
                        call_fn=_Provider(_answer(dossier)))
        assert result.status == COMPRESSION_OK
        assert result.over_budget is True
        assert "still over budget" in result.dossier.budget_note

    def test_the_failure_path_never_truncates_the_open_items(self):
        dossier = _bloated()
        result = update(dossier, self._facts(), budget=50,
                        call_fn=_Provider("not json at all"))
        surviving = {item.id for item in open_items(result.dossier)}
        assert {item.id for item in open_items(dossier)} <= surviving
        assert "R500" in surviving


class TestUpdateWithinBudget:
    def test_a_dossier_that_fits_makes_no_call_and_carries_no_flag(self):
        provider = _Provider("should never be called")
        result = update(_dossier(), IterationFacts(next_step="do M001"),
                        budget=DEFAULT_MAX_TOKENS, call_fn=provider)
        assert result.status == COMPRESSION_WITHIN_BUDGET
        assert provider.prompts == []
        assert result.over_budget is False
        assert result.calls == 0

    def test_the_budget_still_comes_from_config_when_none_is_passed(self):
        config = _Config(**{CONFIG_KEY_MAX_TOKENS: 4242})
        result = update(_dossier(), IterationFacts(), config=config)
        assert result.budget == 4242

    def test_an_update_advances_exactly_one_version(self):
        dossier = _bloated()
        result = update(dossier, IterationFacts(), budget=50,
                        call_fn=_Provider(_answer(dossier)))
        assert result.dossier.version == dossier.version + 1
