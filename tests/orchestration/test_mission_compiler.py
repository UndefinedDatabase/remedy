"""F069 T001 — the MissionPlan schema and the compiler that fills it.

What the order requires proof of:

  * the schema round-trips through JSON unchanged, and refuses a plan that
    claims to be compiled when it was not;
  * the milestone DAG is validated with the same discipline as the flight
    plan's task DAG — duplicate ids, unknown deps, cycles, hard cap;
  * an over-cap plan is refused as hallucinated scope, and a milestone written
    as a task list is refused by the documented outcome lint;
  * three long-goal fixture missions compile to their golden milestone
    structures — on the provider path AND on the no-provider path;
  * a fallback plan is labeled ``compiled=false`` / ``origin="deterministic"``
    on every route into it — no provider, provider error, unparseable answer;
  * compiling has ZERO side effects: nothing is written, nothing is started.

No provider is contacted: every "LLM" here is a local callable returning
recorded text.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration.mission_compiler import (
    DETERMINISTIC_MILESTONE_ID,
    build_mission_prompt,
    compile_mission_plan,
    deterministic_mission_plan,
)
from packages.orchestration.mission_plan_schema import (
    MAX_MISSION_MILESTONES,
    MISSION_PLAN_DRAFT_SCHEMA_V,
    MISSION_PLAN_SCHEMA_V,
    Milestone,
    MissionPlan,
    MissionPlanDraft,
    looks_like_task_list,
)

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "mission"
#: Plain identifiers — they become pytest parametrize ids, and an id carrying a
#: path separator is not package-safe (F062 lesson).
FIXTURE_NAMES = ("payments_platform", "docs_portal", "cli_onboarding")


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURE_DIR / f"{name}.json").read_text(encoding="utf-8"))


def replaying(payload: dict):
    """A call_fn that hands back one recorded provider answer."""
    text = json.dumps(payload)

    def _call(prompt: str, attempt: int) -> str:
        return text

    return _call


def milestone(ident: str, **over) -> dict:
    body = {
        "id": ident,
        "goal": f"the {ident} outcome holds",
        "rationale": "",
        "depends_on": [],
        "jobs_draft": [],
    }
    body.update(over)
    return body


def plan_body(*milestones: dict, **over) -> dict:
    body = {
        "schema_v": MISSION_PLAN_SCHEMA_V,
        "milestones": list(milestones),
        "compiled": False,
        "origin": "deterministic",
    }
    body.update(over)
    return body


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

class TestSchema:
    def test_round_trip_through_json_is_unchanged(self):
        plan = MissionPlan.model_validate(plan_body(
            milestone("M001", jobs_draft=[
                {"title": "t", "goal": "g", "est_band": "M"}], dod_ref="d.json"),
            risks=["r"], assumptions=["a"],
        ))
        again = MissionPlan.model_validate(json.loads(json.dumps(plan.model_dump())))
        assert again == plan
        assert again.model_dump() == plan.model_dump()

    def test_schema_v_is_required_not_defaulted(self):
        with pytest.raises(Exception) as exc:
            MissionPlan.model_validate({"milestones": [milestone("M001")]})
        assert "schema_v" in str(exc.value)

    def test_unknown_field_is_refused(self):
        with pytest.raises(Exception):
            MissionPlan.model_validate(plan_body(
                milestone("M001", surprise=1)))

    def test_at_least_one_milestone_is_required(self):
        with pytest.raises(Exception):
            MissionPlan.model_validate(plan_body())

    @pytest.mark.parametrize("compiled,origin", [
        (True, "deterministic"),
        (False, "provider"),
    ])
    def test_compiled_flag_and_origin_must_agree(self, compiled, origin):
        """A deterministic plan cannot be dressed up as a compiled one."""
        with pytest.raises(Exception) as exc:
            MissionPlan.model_validate(plan_body(
                milestone("M001"), compiled=compiled, origin=origin))
        assert "compiled" in str(exc.value)

    def test_the_draft_contract_cannot_carry_a_dod_ref(self):
        """The DoD hand-off is the compiler's to make, not the provider's."""
        with pytest.raises(Exception):
            MissionPlanDraft.model_validate({
                "schema_v": MISSION_PLAN_DRAFT_SCHEMA_V,
                "milestones": [milestone("M001", dod_ref="smuggled.json")],
            })

    def test_milestones_without_dod_names_the_unreferenced_ones(self):
        plan = MissionPlan.model_validate(plan_body(
            milestone("M001", dod_ref="a.json"),
            milestone("M002"),
            milestone("M003", dod_ref="   "),
        ))
        assert plan.milestones_without_dod == ("M002", "M003")

    @pytest.mark.parametrize("ident", [
        pytest.param("", id="empty"),
        pytest.param("   ", id="blank"),
        pytest.param(" M001", id="padded"),
        pytest.param("M 001", id="inner_space"),
        pytest.param("M" * 65, id="too_long"),
    ])
    def test_unusable_milestone_ids_are_refused(self, ident):
        with pytest.raises(Exception):
            Milestone.model_validate(milestone(ident))

    def test_a_milestone_needs_a_goal(self):
        with pytest.raises(Exception) as exc:
            Milestone.model_validate(milestone("M001", goal="   "))
        assert "no goal" in str(exc.value)


# ---------------------------------------------------------------------------
# The milestone DAG — same discipline as FlightPlan._validate_dag
# ---------------------------------------------------------------------------

class TestMilestoneDag:
    def test_duplicate_ids_are_refused(self):
        with pytest.raises(Exception) as exc:
            MissionPlan.model_validate(plan_body(
                milestone("M001"), milestone("M001")))
        assert "duplicate milestone id" in str(exc.value)

    def test_an_unknown_dependency_is_refused(self):
        with pytest.raises(Exception) as exc:
            MissionPlan.model_validate(plan_body(
                milestone("M001", depends_on=["M404"])))
        assert "unknown id" in str(exc.value)

    def test_a_self_dependency_is_refused(self):
        with pytest.raises(Exception) as exc:
            MissionPlan.model_validate(plan_body(
                milestone("M001", depends_on=["M001"])))
        assert "depends on itself" in str(exc.value)

    def test_a_cycle_is_refused(self):
        with pytest.raises(Exception) as exc:
            MissionPlan.model_validate(plan_body(
                milestone("M001", depends_on=["M003"]),
                milestone("M002", depends_on=["M001"]),
                milestone("M003", depends_on=["M002"]),
            ))
        assert "cycle" in str(exc.value)

    def test_a_diamond_is_a_valid_dag(self):
        plan = MissionPlan.model_validate(plan_body(
            milestone("M001"),
            milestone("M002", depends_on=["M001"]),
            milestone("M003", depends_on=["M001"]),
            milestone("M004", depends_on=["M002", "M003"]),
        ))
        assert [m.id for m in plan.milestones] == ["M001", "M002", "M003", "M004"]

    def test_the_cap_admits_exactly_twelve(self):
        plan = MissionPlan.model_validate(plan_body(
            *(milestone(f"M{i:03d}") for i in range(1, MAX_MISSION_MILESTONES + 1))))
        assert len(plan.milestones) == MAX_MISSION_MILESTONES

    def test_over_the_cap_is_refused_as_hallucinated_scope(self):
        with pytest.raises(Exception) as exc:
            MissionPlan.model_validate(plan_body(
                *(milestone(f"M{i:03d}")
                  for i in range(1, MAX_MISSION_MILESTONES + 2))))
        assert "hallucinated scope" in str(exc.value)


# ---------------------------------------------------------------------------
# The outcome lint (documented heuristic)
# ---------------------------------------------------------------------------

class TestOutcomeLint:
    @pytest.mark.parametrize("goal", [
        pytest.param("Add tests, refactor the parser and update the docs",
                     id="comma_list"),
        pytest.param("Update the docs; run the suite", id="semicolon_list"),
        pytest.param("Write the runbook then run the rehearsal", id="then_list"),
        pytest.param("Fix onboarding and add a first-run check", id="and_list"),
    ])
    def test_a_task_list_is_not_a_milestone(self, goal):
        assert looks_like_task_list(goal) is True
        with pytest.raises(Exception) as exc:
            Milestone.model_validate(milestone("M001", goal=goal))
        assert "task list" in str(exc.value)

    @pytest.mark.parametrize("goal", [
        pytest.param("the payments service is releasable on any weekday",
                     id="outcome"),
        pytest.param("Refactor the parser", id="single_imperative"),
        pytest.param("Documentation and support agree on the install steps",
                     id="and_without_second_verb"),
        pytest.param("the build fails on a page the code has outgrown",
                     id="outcome_with_verbs_inside"),
    ])
    def test_an_outcome_survives_the_lint(self, goal):
        """Conservative on purpose: one imperative is terse, not a to-do list."""
        assert looks_like_task_list(goal) is False
        assert Milestone.model_validate(milestone("M001", goal=goal)).goal == goal

    def test_the_known_limit_of_the_heuristic_is_stated_not_hidden(self):
        """A task list built from UNLISTED verbs passes — by construction.

        The verb list is closed and small on purpose: a lint that guesses at
        what counts as an imperative would reject real outcomes. This test
        exists so the gap is a documented property rather than a surprise —
        "rehearse" is not in the list, so this list is not caught.
        """
        assert looks_like_task_list("Rehearse the rollback then brief the team") is False


# ---------------------------------------------------------------------------
# The prompt
# ---------------------------------------------------------------------------

class TestPrompt:
    def test_the_prompt_carries_the_goal_the_cap_and_the_outcome_rule(self):
        prompt = build_mission_prompt(
            "keep the docs honest", project_facts="Top-level dirs: packages")
        assert "keep the docs honest" in prompt
        assert str(MAX_MISSION_MILESTONES) in prompt
        assert "OUTCOME, not a step" in prompt
        assert "NOT runnable jobs" in prompt
        assert MISSION_PLAN_DRAFT_SCHEMA_V in prompt
        assert "Top-level dirs: packages" in prompt

    def test_repo_facts_come_from_the_shared_helper_not_a_copy(self):
        """A9/A6: one repo-facts block, used by the planner and by this one."""
        from packages.orchestration import flight_plan, mission_compiler
        from packages.orchestration.prompt_facts import repo_facts_block

        assert mission_compiler.repo_facts_block is repo_facts_block
        assert flight_plan.repo_facts_block is repo_facts_block


# ---------------------------------------------------------------------------
# The deterministic fallback
# ---------------------------------------------------------------------------

class TestDeterministicFallback:
    def test_one_milestone_wrapping_the_whole_goal_labeled_deterministic(self):
        plan = deterministic_mission_plan("keep the payments service releasable")
        assert len(plan.milestones) == 1
        assert plan.milestones[0].id == DETERMINISTIC_MILESTONE_ID
        assert "keep the payments service releasable" in plan.milestones[0].goal
        assert plan.compiled is False
        assert plan.origin == "deterministic"

    def test_an_imperative_list_goal_still_produces_a_valid_plan(self):
        """The user's prose is not edited — it is wrapped in an outcome."""
        goal = "Add tests, refactor the parser and update the docs"
        assert looks_like_task_list(goal) is True
        plan = deterministic_mission_plan(goal)
        assert goal in plan.milestones[0].goal
        assert plan.milestones[0].jobs_draft[0].goal == goal

    def test_the_draft_outline_is_not_a_runnable_job(self):
        plan = deterministic_mission_plan("keep the docs honest")
        draft = plan.milestones[0].jobs_draft[0]
        assert draft.est_band == "XL"
        assert not hasattr(draft, "id")
        assert not hasattr(draft, "acceptance")
        assert not hasattr(draft, "status")

    @pytest.mark.parametrize("call_fn,hint_needle", [
        pytest.param(None, "no provider", id="no_provider"),
        pytest.param(lambda p, a: "not json at all", "no JSON", id="unparseable"),
    ])
    def test_every_route_into_the_fallback_is_labeled(self, call_fn, hint_needle):
        result = compile_mission_plan("keep the docs honest", call_fn)
        assert result.source == "deterministic"
        assert result.plan.compiled is False
        assert result.plan.origin == "deterministic"
        assert hint_needle in result.error_hint

    def test_a_raising_provider_falls_back_rather_than_propagating(self):
        def boom(prompt: str, attempt: int) -> str:
            raise RuntimeError("provider is down")

        result = compile_mission_plan("keep the docs honest", boom)
        assert result.source == "deterministic"
        assert "provider is down" in result.error_hint

    def test_an_unparseable_answer_costs_exactly_one_parse_retry(self):
        calls: list[int] = []

        def bad(prompt: str, attempt: int) -> str:
            calls.append(attempt)
            return "{"

        result = compile_mission_plan("keep the docs honest", bad)
        assert calls == [0, 1]
        assert result.calls == 2

    def test_a_compiled_plan_that_fails_validation_falls_back(self):
        """A draft can validate while the compiled artifact cannot."""
        over_cap = {
            "schema_v": MISSION_PLAN_DRAFT_SCHEMA_V,
            "milestones": [milestone(f"M{i:03d}")
                           for i in range(1, MAX_MISSION_MILESTONES + 2)],
        }
        result = compile_mission_plan(
            "keep the docs honest", replaying(over_cap))
        assert result.source == "deterministic"
        assert result.plan.origin == "deterministic"

    def test_a_mission_without_a_goal_is_refused_rather_than_guessed(self):
        with pytest.raises(ValueError) as exc:
            compile_mission_plan("   ")
        assert "needs a goal" in str(exc.value)


# ---------------------------------------------------------------------------
# Golden fixtures — three long goals
# ---------------------------------------------------------------------------

class TestGoldenFixtures:
    @pytest.mark.parametrize("name", FIXTURE_NAMES)
    def test_provider_path_matches_the_golden_plan(self, name):
        fixture = load_fixture(name)
        result = compile_mission_plan(
            fixture["mission"], replaying(fixture["provider_draft"]),
            project_facts="(fixture: repo facts are pinned, not collected)")

        assert result.plan.model_dump() == fixture["golden_plan"]
        assert result.source == "llm"
        assert result.calls == 1
        assert result.error_hint == ""

    @pytest.mark.parametrize("name", FIXTURE_NAMES)
    def test_no_provider_matches_the_golden_fallback_plan(self, name):
        fixture = load_fixture(name)
        result = compile_mission_plan(fixture["mission"], None)

        assert result.plan.model_dump() == fixture["golden_fallback_plan"]
        assert result.source == "deterministic"

    @pytest.mark.parametrize("name", FIXTURE_NAMES)
    def test_every_fixture_goal_is_a_long_prose_goal(self, name):
        """These are mission goals, not one-liners — that is the point."""
        assert len(load_fixture(name)["mission"]["goal"]) > 400

    @pytest.mark.parametrize("name", FIXTURE_NAMES)
    def test_no_milestone_carries_a_dod_reference_yet(self, name):
        """T001 compiles the structure; the DoD hand-off is T002's step."""
        fixture = load_fixture(name)
        result = compile_mission_plan(
            fixture["mission"], replaying(fixture["provider_draft"]))
        assert result.plan.milestones_without_dod == tuple(
            m.id for m in result.plan.milestones)

    def test_the_fixture_dags_are_real_dags_not_flat_lists(self):
        """At least one fixture fans in — a plan with no edges proves nothing."""
        edges = 0
        for name in FIXTURE_NAMES:
            for m in load_fixture(name)["golden_plan"]["milestones"]:
                edges += len(m["depends_on"])
        assert edges >= 4


# ---------------------------------------------------------------------------
# No side effects
# ---------------------------------------------------------------------------

class TestCompilingChangesNothing:
    def test_compiling_writes_no_file_anywhere_under_the_data_root(
            self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        fixture = load_fixture("payments_platform")

        compile_mission_plan(
            fixture["mission"], replaying(fixture["provider_draft"]))

        assert list(tmp_path.rglob("*")) == []

    def test_compiling_leaves_the_mission_record_untouched(self):
        fixture = load_fixture("payments_platform")
        before = json.dumps(fixture["mission"], sort_keys=True)

        compile_mission_plan(
            fixture["mission"], replaying(fixture["provider_draft"]))

        assert json.dumps(fixture["mission"], sort_keys=True) == before
