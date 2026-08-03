"""F071 — the mission dossier: structure and update mechanics.

What the order requires proof of (T001 structure and update mechanics):

  * the five sections render in ONE fixed order, and that order is stable
    across any number of updates — the dossier is a cache-stable prompt
    prefix, so drifting bytes are a defect;
  * the goal is copied once and stays byte-identical across many iterations;
  * update() APPENDS: a fact whose id is already present replaces that line
    (one line per milestone, always), a new id appends, decisions accumulate;
  * a risk that closes moves to DECISIONS with its outcome and leaves the
    open-only RISKS section — one home per fact (A9).

Nothing here touches a provider or the filesystem: the append mechanics are
pure, which is exactly why they are testable without either.
"""
from __future__ import annotations

import pytest

from packages.orchestration.mission_dossier import (
    DOSSIER_SECTIONS,
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
    dossier_sections,
    open_items,
    render_dossier_body,
    resolve_risk,
    start_dossier,
)

GOAL = "The payments API stays releasable while the ledger is rewritten"


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
