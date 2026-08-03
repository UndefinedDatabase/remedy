"""F071 — the mission dossier: structure, budget and versioning.

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
    budget it reports on, and never a truncation.

Every test that writes goes to ``tmp_path`` with the mission root passed
explicitly via ``root=``, so the repository's real data root is never touched.
"""
from __future__ import annotations

import pytest

from packages.orchestration.config import get_key_spec
from packages.orchestration.mission_dossier import (
    CONFIG_KEY_MAX_TOKENS,
    DEFAULT_MAX_TOKENS,
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
    DossierItem,
    IterationFacts,
    append_facts,
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
