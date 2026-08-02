"""F069 — the MissionPlan schema, the compiler, and the DoD hand-off.

What the order requires proof of (T001 schema/compiler, T002 hand-off,
T003 version retention and the in-progress refusal):

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
  * every milestone carries a DoD reference compiled by the F061 compiler —
    no second mechanism — and the plan persists on the mission record as an
    ADDITIVE optional field that pre-F069 records survive unchanged;
  * compiling has ZERO side effects and planning end to end creates ZERO jobs,
    starts no process and touches no worktree;
  * a recompile keeps every prior version, and is REFUSED — changing nothing on
    disk — once any milestone counts as in progress.

No provider is contacted: every "LLM" here is a local callable returning
recorded text.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from packages.orchestration.data_paths import jobs_dir
from packages.orchestration.dod_compiler import DoDCompileResult
from packages.orchestration.dod_schema import DOD_SCHEMA_V, DoD
from packages.orchestration.mission_compiler import (
    DETERMINISTIC_MILESTONE_ID,
    MISSION_PLAN_FILENAME,
    PLAN_VERSION_KEY,
    PLAN_VERSIONS_KEY,
    MissionPlanInProgressError,
    attach_milestone_dods,
    build_mission_prompt,
    compile_milestone_dod,
    compile_mission_plan,
    deterministic_mission_plan,
    milestone_flight_plan,
    milestones_in_progress,
    mission_plan_of,
    plan_mission,
    plan_version_of,
    render_mission_plan_md,
    write_mission_plan_md,
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
from packages.orchestration.mission_state import (
    MISSION_SCHEMA_VERSION,
    Mission,
    MissionError,
    create_mission,
    link_job_to_mission,
    list_missions,
    load_mission,
    mission_evidence_dir,
    mission_record_path,
    set_mission_plan,
)
from packages.orchestration.storage import list_jobs_safe
from packages.orchestration.worktrees import WORKTREE_DIRNAME

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


# ---------------------------------------------------------------------------
# T002 — the per-milestone DoD hand-off
# ---------------------------------------------------------------------------

def compiled_fixture_plan(name: str = "payments_platform"):
    fixture = load_fixture(name)
    result = compile_mission_plan(
        fixture["mission"], replaying(fixture["provider_draft"]))
    return fixture, result.plan


class TestMilestoneFlightPlanView:
    def test_one_task_per_outline_plus_the_outcome_task(self):
        _fixture, plan = compiled_fixture_plan()
        ms = plan.milestones[0]

        view = milestone_flight_plan(ms)

        assert len(view.tasks) == len(ms.jobs_draft) + 1
        assert [t.id for t in view.tasks] == [
            "M001-J001", "M001-J002", "M001-DONE"]

    def test_the_outcome_task_carries_the_milestone_goal_and_waits_for_all(self):
        _fixture, plan = compiled_fixture_plan()
        ms = plan.milestones[0]

        outcome = milestone_flight_plan(ms).tasks[-1]

        assert outcome.acceptance == [ms.goal]
        assert outcome.depends_on == ["M001-J001", "M001-J002"]

    def test_a_milestone_with_no_outlines_still_projects_a_valid_plan(self):
        ms = Milestone.model_validate(milestone("M009"))
        view = milestone_flight_plan(ms)
        assert [t.id for t in view.tasks] == ["M009-DONE"]
        assert view.tasks[0].depends_on == []


class TestMilestoneDodHandoff:
    def test_every_milestone_gets_a_dod_reference_and_a_file(self, tmp_path):
        fixture, plan = compiled_fixture_plan()
        assert plan.milestones_without_dod  # nothing referenced yet

        attached = attach_milestone_dods(
            plan, goal=fixture["mission"]["goal"], evidence_dir=tmp_path)

        assert attached.milestones_without_dod == ()
        for ms in attached.milestones:
            assert ms.dod_ref == f"dod_{ms.id}.json"
            assert (tmp_path / ms.dod_ref).is_file()

    def test_the_reference_is_relative_so_a_moved_data_root_still_resolves(
            self, tmp_path):
        fixture, plan = compiled_fixture_plan()
        attached = attach_milestone_dods(
            plan, goal=fixture["mission"]["goal"], evidence_dir=tmp_path)
        for ms in attached.milestones:
            assert not Path(ms.dod_ref).is_absolute()
            assert "/" not in ms.dod_ref

    def test_the_written_dod_is_a_real_dod_v1_artifact(self, tmp_path):
        fixture, plan = compiled_fixture_plan()
        attached = attach_milestone_dods(
            plan, goal=fixture["mission"]["goal"], evidence_dir=tmp_path)

        body = json.loads(
            (tmp_path / attached.milestones[0].dod_ref).read_text(encoding="utf-8"))
        dod = DoD.model_validate(body)
        assert dod.schema_v == DOD_SCHEMA_V
        assert dod.checks

    def test_the_dod_comes_from_the_f061_compiler_not_a_second_mechanism(self):
        """Rule A6: the milestone DoD is compiled, and its traceability holds."""
        fixture, plan = compiled_fixture_plan()
        ms = plan.milestones[0]

        result = compile_milestone_dod(fixture["mission"]["goal"], ms)

        assert isinstance(result, DoDCompileResult)
        assert result.traceability is not None
        assert result.traceability.ok
        assert result.dod.origin == "deterministic"

    def test_a_provider_backed_milestone_dod_is_labeled_compiled(self):
        fixture, plan = compiled_fixture_plan()
        ms = plan.milestones[0]
        draft = {
            "schema_v": "dod_draft_v1",
            "checks": [{
                "id": "contract", "kind": "pytest",
                "spec": {"selector": "tests/payments"},
                "blocking": True, "acceptance_refs": [], "description": "d",
            }],
        }

        result = compile_milestone_dod(
            fixture["mission"]["goal"], ms, replaying(draft))

        assert result.source == "llm"
        assert result.dod.compiled is True


class TestRendering:
    def test_the_rendering_is_deterministic(self, tmp_path):
        fixture, plan = compiled_fixture_plan()
        attached = attach_milestone_dods(
            plan, goal=fixture["mission"]["goal"], evidence_dir=tmp_path)

        first = render_mission_plan_md(attached, fixture["mission"]["goal"])
        second = render_mission_plan_md(attached, fixture["mission"]["goal"])
        assert first == second

    def test_the_rendering_names_every_milestone_and_its_dod(self, tmp_path):
        fixture, plan = compiled_fixture_plan()
        attached = attach_milestone_dods(
            plan, goal=fixture["mission"]["goal"], evidence_dir=tmp_path)

        text = render_mission_plan_md(attached, fixture["mission"]["goal"])
        for ms in attached.milestones:
            assert ms.id in text
            assert ms.goal in text
            assert ms.dod_ref in text

    def test_the_rendering_says_draft_jobs_are_not_runnable(self):
        _fixture, plan = compiled_fixture_plan()
        text = render_mission_plan_md(plan)
        assert "nothing is runnable" in text or "nothing here is" in text
        assert "not compiled yet" in text  # dod_ref still empty

    def test_a_deterministic_plan_is_rendered_as_the_degraded_route_it_is(self):
        text = render_mission_plan_md(deterministic_mission_plan("keep it green"))
        assert "degraded route" in text

    def test_the_file_lands_in_the_evidence_area_and_keeps_prior_versions(
            self, tmp_path):
        _fixture, plan = compiled_fixture_plan()

        first = write_mission_plan_md(plan, tmp_path)
        second = write_mission_plan_md(plan, tmp_path, version=2)

        assert first.name == MISSION_PLAN_FILENAME
        assert second.name == "mission_plan_v2.md"
        assert first.is_file() and second.is_file()


# ---------------------------------------------------------------------------
# T002 — persistence on the mission record (additive, optional)
# ---------------------------------------------------------------------------

class TestPersistence:
    def test_a_plan_round_trips_through_the_mission_record(self, tmp_path,
                                                           monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        fixture, plan = compiled_fixture_plan()
        mission = create_mission("proj", fixture["mission"]["goal"])

        set_mission_plan("proj", mission.id, plan.model_dump())

        again = load_mission("proj", mission.id)
        assert again.mission_plan is not None
        assert MissionPlan.model_validate(again.mission_plan) == plan

    def test_the_field_is_additive_a_record_without_it_still_loads(self):
        """Every mission written before F069 must load unchanged."""
        pre_f069 = {
            "schema_version": 1, "id": "m1", "project_id": "p1",
            "goal": "keep it green", "status": "active", "job_links": [],
            "dossier_ref": "", "created_at": "2026-01-01T00:00:00+00:00",
        }
        mission = Mission.from_json(pre_f069)
        assert mission.mission_plan is None
        # ...and writing it back produces the SAME bytes it came in with.
        assert mission.to_json() == pre_f069

    def test_the_schema_version_did_not_move_for_an_additive_field(self):
        assert MISSION_SCHEMA_VERSION == 1

    def test_a_non_object_plan_body_is_refused(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        mission = create_mission("proj", "keep it green")
        with pytest.raises(MissionError):
            set_mission_plan("proj", mission.id, ["not", "an", "object"])

    def test_a_corrupt_plan_body_on_disk_is_refused_not_guessed(self):
        with pytest.raises(ValueError) as exc:
            Mission.from_json({
                "schema_version": 1, "id": "m1", "project_id": "p1",
                "goal": "g", "status": "active", "job_links": [],
                "mission_plan": "a string, not a plan",
            })
        assert "mission_plan must be an object" in str(exc.value)

    def test_the_evidence_dir_is_a_sibling_that_cannot_disturb_listings(
            self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        mission = create_mission("proj", "keep it green")

        evidence = mission_evidence_dir("proj", mission.id)
        evidence.mkdir(parents=True, exist_ok=True)
        (evidence / MISSION_PLAN_FILENAME).write_text("x", encoding="utf-8")

        assert [m.id for m in list_missions("proj")] == [mission.id]
        assert mission_record_path("proj", mission.id).is_file()


# ---------------------------------------------------------------------------
# T002 — the no-autostart guarantee
# ---------------------------------------------------------------------------

class TestNoAutostart:
    """Compiling a mission plan starts NOTHING. Pinned, not promised."""

    def test_planning_a_mission_end_to_end_creates_zero_jobs(
            self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        fixture = load_fixture("payments_platform")
        mission = create_mission("proj", fixture["mission"]["goal"])

        result = compile_mission_plan(
            mission, replaying(fixture["provider_draft"]))
        attached = attach_milestone_dods(
            result.plan, goal=mission.goal,
            evidence_dir=mission_evidence_dir("proj", mission.id))
        write_mission_plan_md(
            attached, mission_evidence_dir("proj", mission.id), mission.goal)
        set_mission_plan("proj", mission.id, attached.model_dump())

        jobs, _degraded, _skipped = list_jobs_safe()
        assert jobs == []
        assert not jobs_dir().exists() or list(jobs_dir().iterdir()) == []
        assert load_mission("proj", mission.id).job_links == ()

    def test_planning_touches_no_worktree(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        monkeypatch.chdir(tmp_path)
        fixture = load_fixture("payments_platform")
        mission = create_mission("proj", fixture["mission"]["goal"])

        result = compile_mission_plan(
            mission, replaying(fixture["provider_draft"]))
        attach_milestone_dods(
            result.plan, goal=mission.goal,
            evidence_dir=mission_evidence_dir("proj", mission.id))

        assert not (tmp_path / WORKTREE_DIRNAME).exists()

    def test_planning_starts_no_process(self, tmp_path, monkeypatch):
        """The process fact, not an inference from the absence of imports."""
        import subprocess

        def refuse(*args, **kwargs):
            raise AssertionError(
                "compiling a mission plan must not start a process")

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        monkeypatch.setattr(subprocess, "run", refuse)
        monkeypatch.setattr(subprocess, "Popen", refuse)
        monkeypatch.setattr(subprocess, "call", refuse)
        monkeypatch.setattr(os, "system", refuse)

        fixture = load_fixture("payments_platform")
        mission = create_mission("proj", fixture["mission"]["goal"])
        result = compile_mission_plan(
            mission, replaying(fixture["provider_draft"]))
        attached = attach_milestone_dods(
            result.plan, goal=mission.goal,
            evidence_dir=mission_evidence_dir("proj", mission.id))
        set_mission_plan("proj", mission.id, attached.model_dump())

    def test_a_draft_outline_never_becomes_a_task(self):
        """The one-way door: an outline has no shape a scheduler could run."""
        _fixture, plan = compiled_fixture_plan()
        for ms in plan.milestones:
            for draft in ms.jobs_draft:
                assert set(draft.model_dump()) == {"title", "goal", "est_band"}


# ---------------------------------------------------------------------------
# T003 — planning a persisted mission: version retention and the refusal
# ---------------------------------------------------------------------------

@pytest.fixture
def planned_mission(tmp_path, monkeypatch):
    """A persisted mission plus the recorded provider answer for its goal."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    fixture = load_fixture("payments_platform")
    mission = create_mission("proj", fixture["mission"]["goal"])
    return mission, replaying(fixture["provider_draft"])


class TestPlanMission:
    def test_the_first_compilation_is_version_one(self, planned_mission):
        mission, call_fn = planned_mission

        outcome = plan_mission("proj", mission.id, call_fn)

        assert outcome.version == 1
        assert outcome.source == "llm"
        assert plan_version_of(outcome.mission) == 1
        assert outcome.plan_path.name == MISSION_PLAN_FILENAME

    def test_the_persisted_body_round_trips_back_into_the_model(
            self, planned_mission):
        mission, call_fn = planned_mission

        outcome = plan_mission("proj", mission.id, call_fn)

        stored = mission_plan_of(load_mission("proj", mission.id))
        assert stored == outcome.plan

    def test_a_recompile_retains_every_prior_version(self, planned_mission):
        mission, call_fn = planned_mission

        plan_mission("proj", mission.id, call_fn)
        plan_mission("proj", mission.id, call_fn)
        third = plan_mission("proj", mission.id, call_fn)

        assert third.version == 3
        versions = third.mission.mission_plan[PLAN_VERSIONS_KEY]
        assert [v[PLAN_VERSION_KEY] for v in versions] == [1, 2]

    def test_a_retained_version_is_still_a_valid_plan(self, planned_mission):
        mission, call_fn = planned_mission
        plan_mission("proj", mission.id, call_fn)
        second = plan_mission("proj", mission.id, call_fn)

        prior = second.mission.mission_plan[PLAN_VERSIONS_KEY][0]
        assert MissionPlan.model_validate(
            {k: v for k, v in prior.items() if not k.startswith("_")})

    def test_each_version_renders_its_own_file_and_keeps_the_earlier_one(
            self, planned_mission):
        mission, call_fn = planned_mission

        first = plan_mission("proj", mission.id, call_fn)
        second = plan_mission("proj", mission.id, call_fn)

        assert first.plan_path.is_file()
        assert second.plan_path.name == "mission_plan_v2.md"
        assert second.plan_path.is_file()

    def test_planning_without_a_provider_persists_the_degraded_route(
            self, planned_mission):
        mission, _call_fn = planned_mission

        outcome = plan_mission("proj", mission.id, None)

        assert outcome.source == "deterministic"
        assert outcome.plan.compiled is False
        assert len(outcome.plan.milestones) == 1
        assert outcome.plan.milestones[0].dod_ref


class TestInProgressRule:
    def test_nothing_is_in_progress_before_a_plan_exists(self, planned_mission):
        mission, _call_fn = planned_mission
        link_job_to_mission("proj", mission.id, "job-a", "initial")

        assert milestones_in_progress(load_mission("proj", mission.id)) == ()

    def test_nothing_is_in_progress_while_no_job_is_linked(self, planned_mission):
        mission, call_fn = planned_mission
        outcome = plan_mission("proj", mission.id, call_fn)

        assert milestones_in_progress(outcome.mission) == ()

    def test_one_linked_job_puts_every_milestone_in_progress(self, planned_mission):
        """The conservative rule: the record attributes jobs to the MISSION."""
        mission, call_fn = planned_mission
        outcome = plan_mission("proj", mission.id, call_fn)
        link_job_to_mission("proj", mission.id, "job-a", "initial")

        in_progress = milestones_in_progress(load_mission("proj", mission.id))
        assert in_progress == tuple(m.id for m in outcome.plan.milestones)

    def test_a_recompile_is_refused_once_a_milestone_is_in_progress(
            self, planned_mission):
        mission, call_fn = planned_mission
        plan_mission("proj", mission.id, call_fn)
        link_job_to_mission("proj", mission.id, "job-a", "initial")

        with pytest.raises(MissionPlanInProgressError) as exc:
            plan_mission("proj", mission.id, call_fn)
        assert "cannot be replanned" in str(exc.value)
        assert "already in progress" in str(exc.value)

    def test_the_refusal_changes_nothing_on_disk(self, planned_mission):
        mission, call_fn = planned_mission
        plan_mission("proj", mission.id, call_fn)
        link_job_to_mission("proj", mission.id, "job-a", "initial")
        record = mission_record_path("proj", mission.id)
        before = record.read_text(encoding="utf-8")
        evidence_before = sorted(
            p.name for p in mission_evidence_dir("proj", mission.id).iterdir())

        with pytest.raises(MissionPlanInProgressError):
            plan_mission("proj", mission.id, call_fn)

        assert record.read_text(encoding="utf-8") == before
        assert sorted(
            p.name for p in mission_evidence_dir("proj", mission.id).iterdir()
        ) == evidence_before
