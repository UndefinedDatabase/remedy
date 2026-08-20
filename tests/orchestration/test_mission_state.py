"""F056 T001 — the mission record, its store, and the honesty rules around it.

What the order requires proof of:

  * the record round-trips through disk unchanged, under a project-scoped path;
  * listing order is total and reproducible (newest first, ties broken by id);
  * listings are project-SCOPED — one project never sees another's missions;
  * a record that will not parse is skipped and COUNTED, never fatal;
  * a mission goal is IMMUTABLE — a changed goal is refused, not rewritten.

Every test writes into ``tmp_path``: the mission root is passed explicitly via
``root=``, so the repository's real data root is never touched.
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from packages.core.models import Job, RunState
from packages.orchestration.dag_schedule import blocked_downstream, ready_set
from packages.orchestration.decision_queue import list_decisions
from packages.orchestration.intake import heuristic_intake, mission_candidate_hint
from packages.orchestration.mission_state import (
    MAX_MISSION_GOAL_CHARS,
    MISSING_JOB_LABEL,
    MISSION_ROLE_FOLLOW_UP,
    MISSION_ROLE_INITIAL,
    MISSION_SCHEMA_VERSION,
    MISSION_STATUS_ABANDONED,
    MISSION_STATUS_ACHIEVED,
    MISSION_STATUS_ACTIVE,
    MISSION_VERIFY_PLANNED_ID,
    UNREADABLE_JOB_LABEL,
    VERIFY_RESULT_FAILED,
    VERIFY_RESULT_PASSED,
    VERIFY_RESULT_UNVERIFIABLE,
    Mission,
    MissionError,
    MissionGoalImmutableError,
    MissionJobAlreadyLinkedError,
    MissionLinkRoleError,
    MissionNotFoundError,
    MissionVerifyFirstError,
    assert_verify_first,
    build_follow_up_task,
    build_verify_first_task,
    continue_mission,
    create_mission,
    execute_mission_followup,
    inject_verify_first,
    is_verify_task,
    link_job_to_mission,
    list_missions,
    list_missions_safe,
    load_mission,
    mission_dir_for_project,
    mission_for_job,
    mission_record_path,
    project_ids_with_missions,
    read_mission_verify_record,
    render_mission_chain,
    render_mission_row,
    resolve_mission_id,
    resolve_verify_command,
    run_verify_task,
    save_mission,
    set_mission_status,
)
from packages.orchestration.schemas.models import JobIntake
from packages.orchestration.storage import load_job, save_job

_T0 = datetime(2026, 7, 31, 12, 0, 0, tzinfo=timezone.utc)
_PROJECT = "proj-alpha"
_OTHER_PROJECT = "proj-beta"


def _at(minutes: int) -> datetime:
    return _T0 + timedelta(minutes=minutes)


class TestMissionRecord:

    def test_create_persists_under_a_project_scoped_path(self, tmp_path):
        mission = create_mission(_PROJECT, "Ship the importer", now=_T0,
                                 root=tmp_path)
        path = mission_record_path(_PROJECT, mission.id, root=tmp_path)

        assert path.is_file()
        assert path.parent == mission_dir_for_project(_PROJECT, root=tmp_path)
        assert path.parent.parent.name == "missions"

    def test_created_mission_starts_active_with_no_jobs(self, tmp_path):
        mission = create_mission(_PROJECT, "Ship the importer", now=_T0,
                                 root=tmp_path)

        assert mission.status == MISSION_STATUS_ACTIVE
        assert mission.job_links == ()
        assert mission.created_at == _T0.isoformat()
        assert mission.project_id == _PROJECT

    def test_dossier_reference_is_reserved_but_unfilled(self, tmp_path):
        """The field exists for the later dossier feature; this one never fills it."""
        mission = create_mission(_PROJECT, "Ship the importer", root=tmp_path)

        assert mission.dossier_ref == ""
        body = json.loads(
            mission_record_path(_PROJECT, mission.id, root=tmp_path).read_text())
        assert body["dossier_ref"] == ""

    def test_record_round_trips_through_disk(self, tmp_path):
        mission = create_mission(_PROJECT, "Ship the importer", now=_T0,
                                 root=tmp_path)

        assert load_mission(_PROJECT, mission.id, root=tmp_path) == mission

    def test_stored_json_carries_the_schema_version(self, tmp_path):
        mission = create_mission(_PROJECT, "Ship the importer", root=tmp_path)
        body = json.loads(
            mission_record_path(_PROJECT, mission.id, root=tmp_path).read_text())

        assert body["schema_version"] == MISSION_SCHEMA_VERSION

    def test_an_empty_goal_is_refused(self, tmp_path):
        with pytest.raises(MissionError):
            create_mission(_PROJECT, "   ", root=tmp_path)

    def test_an_oversized_goal_is_refused(self, tmp_path):
        with pytest.raises(MissionError):
            create_mission(_PROJECT, "x" * (MAX_MISSION_GOAL_CHARS + 1),
                           root=tmp_path)

    def test_a_project_id_that_would_escape_its_directory_is_refused(self, tmp_path):
        with pytest.raises(MissionError):
            create_mission("../../etc", "Ship the importer", root=tmp_path)


class TestMissionLoading:

    def test_loading_an_unknown_mission_raises_not_found(self, tmp_path):
        with pytest.raises(MissionNotFoundError):
            load_mission(_PROJECT, "deadbeef" * 4, root=tmp_path)

    def test_loading_a_corrupt_record_raises_rather_than_guessing(self, tmp_path):
        mission = create_mission(_PROJECT, "Ship the importer", root=tmp_path)
        mission_record_path(_PROJECT, mission.id, root=tmp_path).write_text("{ not json")

        with pytest.raises(MissionError):
            load_mission(_PROJECT, mission.id, root=tmp_path)

    def test_an_unknown_schema_version_is_refused(self, tmp_path):
        mission = create_mission(_PROJECT, "Ship the importer", root=tmp_path)
        path = mission_record_path(_PROJECT, mission.id, root=tmp_path)
        body = json.loads(path.read_text())
        body["schema_version"] = MISSION_SCHEMA_VERSION + 99
        path.write_text(json.dumps(body))

        with pytest.raises(MissionError):
            load_mission(_PROJECT, mission.id, root=tmp_path)


class TestMissionListing:

    def test_listing_is_newest_first(self, tmp_path):
        old = create_mission(_PROJECT, "Older goal", now=_at(0), root=tmp_path)
        mid = create_mission(_PROJECT, "Middle goal", now=_at(5), root=tmp_path)
        new = create_mission(_PROJECT, "Newest goal", now=_at(10), root=tmp_path)

        assert [m.id for m in list_missions(_PROJECT, root=tmp_path)] == [
            new.id, mid.id, old.id]

    def test_identical_timestamps_break_the_tie_by_id(self, tmp_path):
        first = create_mission(_PROJECT, "One", now=_T0, root=tmp_path)
        second = create_mission(_PROJECT, "Two", now=_T0, root=tmp_path)
        expected = sorted([first.id, second.id], reverse=True)

        assert [m.id for m in list_missions(_PROJECT, root=tmp_path)] == expected

    def test_listing_is_scoped_to_one_project(self, tmp_path):
        mine = create_mission(_PROJECT, "My goal", root=tmp_path)
        theirs = create_mission(_OTHER_PROJECT, "Their goal", root=tmp_path)

        assert [m.id for m in list_missions(_PROJECT, root=tmp_path)] == [mine.id]
        assert [m.id for m in list_missions(_OTHER_PROJECT, root=tmp_path)] == [
            theirs.id]

    def test_listing_a_project_without_missions_is_empty_not_an_error(self, tmp_path):
        assert list_missions("proj-empty", root=tmp_path) == []

    def test_a_corrupt_record_is_skipped_and_counted(self, tmp_path):
        good = create_mission(_PROJECT, "Readable", now=_at(0), root=tmp_path)
        broken = create_mission(_PROJECT, "About to break", now=_at(1),
                                root=tmp_path)
        broken_path = mission_record_path(_PROJECT, broken.id, root=tmp_path)
        broken_path.write_text("{{{ not json at all")

        missions, degraded, skipped = list_missions_safe(_PROJECT, root=tmp_path)

        assert [m.id for m in missions] == [good.id]
        assert degraded is True
        assert skipped == [broken_path.name]

    def test_a_listing_never_crashes_on_a_bad_record(self, tmp_path):
        create_mission(_PROJECT, "Readable", root=tmp_path)
        (mission_dir_for_project(_PROJECT, root=tmp_path) / "garbage.json").write_text(
            "not even close")

        # No exception: the honest answer is the records that DO parse.
        assert len(list_missions(_PROJECT, root=tmp_path)) == 1

    def test_project_ids_with_missions_reads_disk_not_a_registry(self, tmp_path):
        create_mission(_PROJECT, "A", root=tmp_path)
        create_mission(_OTHER_PROJECT, "B", root=tmp_path)

        assert project_ids_with_missions(root=tmp_path) == sorted(
            [_PROJECT, _OTHER_PROJECT])

    def test_project_ids_with_missions_is_empty_before_anything_exists(self, tmp_path):
        assert project_ids_with_missions(root=tmp_path) == []


class TestMissionGoalImmutability:

    def test_saving_a_changed_goal_is_refused(self, tmp_path):
        mission = create_mission(_PROJECT, "Ship the importer", root=tmp_path)
        rewritten = Mission(
            id=mission.id, project_id=mission.project_id,
            goal="Ship something else entirely", status=mission.status,
            created_at=mission.created_at)

        with pytest.raises(MissionGoalImmutableError):
            save_mission(rewritten, root=tmp_path)

    def test_the_goal_on_disk_survives_a_refused_rewrite(self, tmp_path):
        mission = create_mission(_PROJECT, "Ship the importer", root=tmp_path)
        rewritten = Mission(
            id=mission.id, project_id=mission.project_id, goal="Something else",
            status=mission.status, created_at=mission.created_at)

        with pytest.raises(MissionGoalImmutableError):
            save_mission(rewritten, root=tmp_path)

        assert load_mission(_PROJECT, mission.id,
                            root=tmp_path).goal == "Ship the importer"

    def test_other_fields_still_save_with_the_goal_unchanged(self, tmp_path):
        mission = create_mission(_PROJECT, "Ship the importer", root=tmp_path)
        paused = Mission(
            id=mission.id, project_id=mission.project_id, goal=mission.goal,
            status=MISSION_STATUS_ABANDONED, created_at=mission.created_at)
        save_mission(paused, root=tmp_path)

        assert load_mission(_PROJECT, mission.id,
                            root=tmp_path).status == MISSION_STATUS_ABANDONED

    def test_two_goals_mean_two_missions(self, tmp_path):
        first = create_mission(_PROJECT, "Ship the importer", root=tmp_path)
        second = create_mission(_PROJECT, "Ship the exporter", root=tmp_path)

        assert first.id != second.id
        assert len(list_missions(_PROJECT, root=tmp_path)) == 2


class TestMissionJobLinking:

    def test_the_first_link_is_the_initial_job(self, tmp_path):
        mission = create_mission(_PROJECT, "Ship the importer", root=tmp_path)
        job_id = str(uuid4())

        updated = link_job_to_mission(_PROJECT, mission.id, job_id,
                                      MISSION_ROLE_INITIAL, now=_T0, root=tmp_path)

        assert [(link.job_id, link.role) for link in updated.job_links] == [
            (job_id, MISSION_ROLE_INITIAL)]
        assert updated.job_links[0].created_at == _T0.isoformat()

    def test_the_chain_keeps_link_order(self, tmp_path):
        mission = create_mission(_PROJECT, "Ship the importer", root=tmp_path)
        first, second, third = str(uuid4()), str(uuid4()), str(uuid4())
        link_job_to_mission(_PROJECT, mission.id, first, MISSION_ROLE_INITIAL,
                            now=_at(0), root=tmp_path)
        link_job_to_mission(_PROJECT, mission.id, second, MISSION_ROLE_FOLLOW_UP,
                            now=_at(5), root=tmp_path)
        updated = link_job_to_mission(_PROJECT, mission.id, third,
                                      MISSION_ROLE_FOLLOW_UP, now=_at(10),
                                      root=tmp_path)

        assert list(updated.job_ids()) == [first, second, third]
        assert updated.latest_link().job_id == third

    def test_a_job_belongs_to_at_most_one_mission(self, tmp_path):
        first = create_mission(_PROJECT, "Ship the importer", root=tmp_path)
        second = create_mission(_PROJECT, "Ship the exporter", root=tmp_path)
        job_id = str(uuid4())
        link_job_to_mission(_PROJECT, first.id, job_id, MISSION_ROLE_INITIAL,
                            root=tmp_path)

        with pytest.raises(MissionJobAlreadyLinkedError) as exc:
            link_job_to_mission(_PROJECT, second.id, job_id,
                                MISSION_ROLE_INITIAL, root=tmp_path)

        assert exc.value.mission_id == first.id

    def test_the_one_mission_rule_holds_across_projects(self, tmp_path):
        """Job ids are globally unique, so the validator cannot be project-local."""
        mine = create_mission(_PROJECT, "My goal", root=tmp_path)
        theirs = create_mission(_OTHER_PROJECT, "Their goal", root=tmp_path)
        job_id = str(uuid4())
        link_job_to_mission(_PROJECT, mine.id, job_id, MISSION_ROLE_INITIAL,
                            root=tmp_path)

        with pytest.raises(MissionJobAlreadyLinkedError):
            link_job_to_mission(_OTHER_PROJECT, theirs.id, job_id,
                                MISSION_ROLE_INITIAL, root=tmp_path)

    def test_a_second_initial_job_is_refused(self, tmp_path):
        mission = create_mission(_PROJECT, "Ship the importer", root=tmp_path)
        link_job_to_mission(_PROJECT, mission.id, str(uuid4()),
                            MISSION_ROLE_INITIAL, root=tmp_path)

        with pytest.raises(MissionLinkRoleError):
            link_job_to_mission(_PROJECT, mission.id, str(uuid4()),
                                MISSION_ROLE_INITIAL, root=tmp_path)

    def test_a_chain_cannot_start_with_a_follow_up(self, tmp_path):
        mission = create_mission(_PROJECT, "Ship the importer", root=tmp_path)

        with pytest.raises(MissionLinkRoleError):
            link_job_to_mission(_PROJECT, mission.id, str(uuid4()),
                                MISSION_ROLE_FOLLOW_UP, root=tmp_path)

    def test_an_unknown_role_is_refused(self, tmp_path):
        mission = create_mission(_PROJECT, "Ship the importer", root=tmp_path)

        with pytest.raises(MissionLinkRoleError):
            link_job_to_mission(_PROJECT, mission.id, str(uuid4()), "whatever",
                                root=tmp_path)

    def test_linking_into_an_unknown_mission_raises_not_found(self, tmp_path):
        with pytest.raises(MissionNotFoundError):
            link_job_to_mission(_PROJECT, "0" * 32, str(uuid4()),
                                MISSION_ROLE_INITIAL, root=tmp_path)

    def test_mission_for_job_finds_the_holder(self, tmp_path):
        mission = create_mission(_PROJECT, "Ship the importer", root=tmp_path)
        job_id = str(uuid4())
        link_job_to_mission(_PROJECT, mission.id, job_id, MISSION_ROLE_INITIAL,
                            root=tmp_path)

        assert mission_for_job(job_id, root=tmp_path).id == mission.id

    def test_mission_for_an_unlinked_job_is_none(self, tmp_path):
        create_mission(_PROJECT, "Ship the importer", root=tmp_path)

        assert mission_for_job(str(uuid4()), root=tmp_path) is None


class TestMissionStatusTransitions:

    def test_status_is_set_only_by_an_explicit_call(self, tmp_path):
        mission = create_mission(_PROJECT, "Ship the importer", root=tmp_path)

        updated = set_mission_status(_PROJECT, mission.id,
                                     MISSION_STATUS_ACHIEVED, root=tmp_path)

        assert updated.status == MISSION_STATUS_ACHIEVED
        assert load_mission(_PROJECT, mission.id,
                            root=tmp_path).status == MISSION_STATUS_ACHIEVED

    def test_an_unknown_status_is_refused(self, tmp_path):
        mission = create_mission(_PROJECT, "Ship the importer", root=tmp_path)

        with pytest.raises(MissionError):
            set_mission_status(_PROJECT, mission.id, "finished", root=tmp_path)

    def test_linking_jobs_never_moves_the_status_on_its_own(self, tmp_path):
        """Nothing in this feature auto-transitions a mission."""
        mission = create_mission(_PROJECT, "Ship the importer", root=tmp_path)
        link_job_to_mission(_PROJECT, mission.id, str(uuid4()),
                            MISSION_ROLE_INITIAL, root=tmp_path)
        updated = link_job_to_mission(_PROJECT, mission.id, str(uuid4()),
                                      MISSION_ROLE_FOLLOW_UP, root=tmp_path)

        assert updated.status == MISSION_STATUS_ACTIVE


class TestMissionIdResolution:

    def test_a_unique_prefix_resolves(self, tmp_path):
        mission = create_mission(_PROJECT, "Ship the importer", root=tmp_path)

        assert resolve_mission_id(_PROJECT, mission.id[:8],
                                  root=tmp_path) == mission.id

    def test_an_ambiguous_prefix_is_refused(self, tmp_path):
        first = create_mission(_PROJECT, "One", root=tmp_path)
        second = Mission(id=first.id[:4] + "f" * 28, project_id=_PROJECT,
                         goal="Two", created_at=first.created_at)
        save_mission(second, root=tmp_path)

        with pytest.raises(MissionError):
            resolve_mission_id(_PROJECT, first.id[:4], root=tmp_path)

    def test_an_unknown_prefix_comes_back_unchanged(self, tmp_path):
        assert resolve_mission_id(_PROJECT, "nothing", root=tmp_path) == "nothing"


class TestMissionChainRendering:

    def test_the_chain_renders_each_job_with_its_state(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = Job(name="job one", state=RunState.COMPLETED)
        save_job(job, root=tmp_path)
        mission = create_mission(_PROJECT, "Ship the importer", root=tmp_path)
        linked = link_job_to_mission(_PROJECT, mission.id, str(job.id),
                                     MISSION_ROLE_INITIAL, root=tmp_path)

        rendered = "\n".join(render_mission_chain(linked))

        assert str(job.id) in rendered
        assert "completed" in rendered
        assert MISSING_JOB_LABEL not in rendered

    def test_a_deleted_job_renders_as_missing_and_never_crashes(
            self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = Job(name="job one", state=RunState.COMPLETED)
        save_job(job, root=tmp_path)
        mission = create_mission(_PROJECT, "Ship the importer", root=tmp_path)
        linked = link_job_to_mission(_PROJECT, mission.id, str(job.id),
                                     MISSION_ROLE_INITIAL, root=tmp_path)
        (tmp_path / "jobs" / f"{job.id}.json").unlink()

        rendered = "\n".join(render_mission_chain(linked))

        assert MISSING_JOB_LABEL in rendered

    def test_an_unreadable_job_is_not_reported_as_missing(
            self, tmp_path, monkeypatch):
        """Deleted and corrupt are different facts and get different labels."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = Job(name="job one", state=RunState.COMPLETED)
        save_job(job, root=tmp_path)
        mission = create_mission(_PROJECT, "Ship the importer", root=tmp_path)
        linked = link_job_to_mission(_PROJECT, mission.id, str(job.id),
                                     MISSION_ROLE_INITIAL, root=tmp_path)
        (tmp_path / "jobs" / f"{job.id}.json").write_text("{ not json")

        rendered = "\n".join(render_mission_chain(linked))

        assert UNREADABLE_JOB_LABEL in rendered
        assert MISSING_JOB_LABEL not in rendered

    def test_an_empty_mission_renders_without_a_chain(self, tmp_path):
        mission = create_mission(_PROJECT, "Ship the importer", root=tmp_path)

        rendered = "\n".join(render_mission_chain(mission))

        assert "no jobs linked yet" in rendered
        assert mission.goal in rendered

    def test_the_row_carries_id_status_and_job_count(self, tmp_path):
        mission = create_mission(_PROJECT, "Ship the importer", root=tmp_path)
        linked = link_job_to_mission(_PROJECT, mission.id, str(uuid4()),
                                     MISSION_ROLE_INITIAL, root=tmp_path)

        row = render_mission_row(linked)

        assert mission.id[:12] in row
        assert MISSION_STATUS_ACTIVE in row
        assert "1 job(s)" in row
        assert "Ship the importer" in row


class TestMissionCandidateHint:
    """F056 T002 — intake's hint. It offers a choice; it never makes one."""

    def test_a_standing_commitment_is_flagged(self):
        assert mission_candidate_hint(
            "Keep the importer working from now on") is True

    def test_a_multi_stage_effort_is_flagged(self):
        assert mission_candidate_hint(
            "Migrate the database in stages over the next quarter") is True

    def test_a_one_shot_fix_is_not_flagged(self):
        assert mission_candidate_hint("Fix the login bug") is False

    def test_the_hint_is_case_insensitive(self):
        assert mission_candidate_hint("MAINTAIN the CI pipeline") is True

    def test_heuristic_intake_carries_the_hint(self):
        flagged = heuristic_intake("Keep it green, continuously.")
        plain = heuristic_intake("Fix the login bug.")

        assert flagged.value.mission_candidate is True
        assert plain.value.mission_candidate is False

    def test_the_field_defaults_to_false_for_older_payloads(self):
        """Additive field: an intake written before F056 loads unchanged."""
        intake = JobIntake.model_validate({"schema_v": "ji1", "goal": "Ship it"})

        assert intake.mission_candidate is False


class TestMissionOfferInThePlanApproval:
    """The offer rides the existing approval decision and defaults to NO."""

    def test_a_flagged_intake_adds_the_offer_to_the_payload(self):
        job = Job(name="t", flight_plan={"_approval": "pending"},
                  intake={"schema_v": "ji1", "goal": "Keep it green",
                          "mission_candidate": True})

        decision = [d for d in list_decisions(job, [])
                    if d.type == "flight_plan_approval"][0]

        assert decision.payload["mission_offer"]["default"] == "no"
        assert decision.payload["mission_offer"]["goal"] == "Keep it green"

    def test_the_offer_names_the_opt_in_flag(self):
        job = Job(name="t", flight_plan={"_approval": "pending"},
                  intake={"schema_v": "ji1", "goal": "Keep it green",
                          "mission_candidate": True})

        decision = [d for d in list_decisions(job, [])
                    if d.type == "flight_plan_approval"][0]

        assert any("--as-mission" in action for action in decision.next_actions)

    def test_an_unflagged_intake_gets_no_offer(self):
        job = Job(name="t", flight_plan={"_approval": "pending"},
                  intake={"schema_v": "ji1", "goal": "Fix the bug",
                          "mission_candidate": False})

        decision = [d for d in list_decisions(job, [])
                    if d.type == "flight_plan_approval"][0]

        assert "mission_offer" not in decision.payload
        assert not any("--as-mission" in a for a in decision.next_actions)

    def test_a_job_without_intake_gets_no_offer(self):
        job = Job(name="t", flight_plan={"_approval": "pending"})

        decision = [d for d in list_decisions(job, [])
                    if d.type == "flight_plan_approval"][0]

        assert "mission_offer" not in decision.payload

    def test_the_offer_is_one_touchpoint_not_a_second_decision(self):
        """No new human touchpoint: the offer rides the approval that exists."""
        job = Job(name="t", flight_plan={"_approval": "pending"},
                  intake={"schema_v": "ji1", "goal": "Keep it green",
                          "mission_candidate": True})

        approvals = [d for d in list_decisions(job, [])
                     if d.type == "flight_plan_approval"]

        assert len(approvals) == 1


class TestVerifyFirstStructure:
    """F056 T003 — verification is a task in the plan, not a request in a prompt."""

    def _previous_job(self, command: str = "true") -> Job:
        return Job(name="previous", metadata={"verify_command": command})

    def test_the_verify_task_is_built_from_the_previous_job(self):
        previous = self._previous_job("pytest tests/importer")
        task = build_verify_first_task(previous)

        assert is_verify_task(task)
        assert task.inputs["verify_command"] == "pytest tests/importer"
        assert task.inputs["previous_job_id"] == str(previous.id)
        assert str(previous.id) in task.description

    def test_a_previous_job_without_a_command_says_so(self):
        task = build_verify_first_task(Job(name="previous"))

        assert task.inputs["verify_command"] == ""
        assert "no verification command recorded" in task.description

    def test_the_command_may_come_from_the_flight_plan(self):
        previous = Job(name="previous",
                       flight_plan={"verify_command": "make smoke"})

        assert resolve_verify_command(previous) == "make smoke"

    def test_injection_puts_verify_first_and_makes_work_depend_on_it(self):
        previous = self._previous_job()
        tasks = inject_verify_first(previous, [build_follow_up_task("Add the CSV path")])

        assert is_verify_task(tasks[0])
        assert tasks[1].inputs["flight"]["depends_on"] == [
            MISSION_VERIFY_PLANNED_ID]

    def test_the_scheduler_withholds_the_work_until_verify_completes(self):
        """The enforcement is the existing DAG scheduler, not a convention."""
        previous = self._previous_job()
        tasks = inject_verify_first(previous, [build_follow_up_task("Add the CSV path")])

        ready = ready_set(tasks)

        assert ready == [tasks[0].id]

    def test_the_work_becomes_ready_once_verify_completed(self):
        previous = self._previous_job()
        tasks = inject_verify_first(previous, [build_follow_up_task("Add the CSV path")])
        tasks[0].status = RunState.COMPLETED

        assert ready_set(tasks) == [tasks[1].id]

    def test_a_failed_verify_blocks_the_work_downstream(self):
        previous = self._previous_job()
        tasks = inject_verify_first(previous, [build_follow_up_task("Add the CSV path")])
        tasks[0].status = RunState.FAILED

        assert blocked_downstream(tasks, [tasks[0].id]) == {tasks[1].id}

    def test_a_plan_that_does_not_start_with_verify_is_refused(self):
        with pytest.raises(MissionVerifyFirstError):
            assert_verify_first([build_follow_up_task("Add the CSV path")])

    def test_an_empty_plan_is_refused(self):
        with pytest.raises(MissionVerifyFirstError):
            assert_verify_first([])

    def test_work_that_does_not_depend_on_verify_is_refused(self):
        previous = self._previous_job()
        verify = build_verify_first_task(previous)
        loose = build_follow_up_task("Add the CSV path")
        loose.inputs["flight"] = {"planned_id": "M001", "depends_on": []}

        with pytest.raises(MissionVerifyFirstError):
            assert_verify_first([verify, loose])


class TestVerifyTaskExecution:

    def _task(self, command: str):
        return build_verify_first_task(
            Job(name="previous", metadata={"verify_command": command}))

    def test_a_passing_command_lets_the_follow_up_start(self):
        outcome = run_verify_task(self._task("check the thing"),
                                  runner=lambda argv, cwd: (0, "all good"))

        assert outcome.result == VERIFY_RESULT_PASSED
        assert outcome.follow_up_may_start is True
        assert outcome.exit_code == 0

    def test_a_failing_command_names_what_broke(self):
        outcome = run_verify_task(self._task("check the thing"),
                                  runner=lambda argv, cwd: (1, "2 tests failed"))

        assert outcome.result == VERIFY_RESULT_FAILED
        assert outcome.follow_up_may_start is False
        assert "check the thing" in outcome.detail
        assert "exited 1" in outcome.detail
        assert "2 tests failed" in outcome.output_tail

    def test_a_command_that_cannot_run_is_a_failure_not_a_pass(self):
        def _explode(argv, cwd):
            raise FileNotFoundError("no such command: check")

        outcome = run_verify_task(self._task("check"), runner=_explode)

        assert outcome.result == VERIFY_RESULT_FAILED
        assert outcome.follow_up_may_start is False
        assert "could not run" in outcome.detail

    def test_no_recorded_command_is_reported_unverified_never_passed(self):
        outcome = run_verify_task(build_verify_first_task(Job(name="previous")))

        assert outcome.result == VERIFY_RESULT_UNVERIFIABLE
        assert outcome.result != VERIFY_RESULT_PASSED
        assert "nothing was verified" in outcome.detail

    def test_the_command_is_split_into_argv_not_handed_to_a_shell(self):
        seen: list[list[str]] = []

        def _record(argv, cwd):
            seen.append(argv)
            return (0, "")

        run_verify_task(self._task("pytest tests/importer -q"), runner=_record)

        assert seen == [["pytest", "tests/importer", "-q"]]

    def test_the_default_runner_goes_through_the_guarded_seam(self, monkeypatch):
        import subprocess

        from packages.orchestration import mission_state

        seen: dict[str, object] = {}

        def _fake_guarded(cmd, *, timeout_sec, cwd, extra_env_keys=()):
            seen.update(cmd=list(cmd), timeout_sec=timeout_sec, cwd=cwd)
            return subprocess.CompletedProcess(
                list(cmd), 0, b"ok-\xff-undecodable\n", b"warn\n")

        monkeypatch.setattr(mission_state, "run_guarded_test_command", _fake_guarded)
        outcome = run_verify_task(self._task("pytest tests/importer -q"))

        assert seen == {
            "cmd": ["pytest", "tests/importer", "-q"],
            "timeout_sec": 900,
            "cwd": None,
        }
        assert outcome.result == VERIFY_RESULT_PASSED
        assert outcome.exit_code == 0
        assert "ok-" in outcome.output_tail
        assert "undecodable" in outcome.output_tail
        assert "warn" in outcome.output_tail


class TestTwoJobFixtureEndToEnd:
    """The acceptance fixture: job 1 green -> continue -> verify runs FIRST.

    The ordering claim is asserted from the evidence record the run writes,
    not from prose: ``steps[0]`` is the verification, and the work only ever
    appears after it.
    """

    def _mission_with_a_green_first_job(self, tmp_path, command: str):
        job_one = Job(name="job one", state=RunState.COMPLETED,
                      project_id=_PROJECT, metadata={"verify_command": command})
        save_job(job_one)
        mission = create_mission(_PROJECT, "Keep the importer working",
                                 root=tmp_path)
        link_job_to_mission(_PROJECT, mission.id, str(job_one.id),
                            MISSION_ROLE_INITIAL, root=tmp_path)
        return mission, job_one

    @pytest.fixture(autouse=True)
    def _data_root(self, tmp_path, monkeypatch):
        """continue_mission and the executor use the default data root."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))

    def test_verify_runs_first_and_then_the_follow_up_work_runs(self, tmp_path):
        mission, job_one = self._mission_with_a_green_first_job(
            tmp_path, "check the importer")
        job_two = continue_mission(_PROJECT, mission.id, "Add the CSV path",
                                   root=tmp_path)
        ran: list[str] = []

        run = execute_mission_followup(
            job_two,
            runner=lambda argv, cwd: (0, "importer still fine"),
            work_runner=lambda task: (ran.append(task.description), True)[1],
        )

        assert run.steps[0] == f"verify:{VERIFY_RESULT_PASSED}"
        assert run.steps[1] == "work:Add the CSV path"
        assert ran == ["Add the CSV path"]
        assert run.follow_up_started is True

    def test_a_broken_previous_state_stops_the_follow_up_before_it_starts(
            self, tmp_path):
        mission, job_one = self._mission_with_a_green_first_job(
            tmp_path, "check the importer")
        job_two = continue_mission(_PROJECT, mission.id, "Add the CSV path",
                                   root=tmp_path)
        ran: list[str] = []

        run = execute_mission_followup(
            job_two,
            runner=lambda argv, cwd: (1, "ImporterError: schema drifted"),
            work_runner=lambda task: (ran.append(task.description), True)[1],
        )

        assert run.steps == [f"verify:{VERIFY_RESULT_FAILED}"]
        assert ran == []
        assert run.follow_up_started is False

    def test_the_failure_message_names_what_broke(self, tmp_path):
        mission, _job_one = self._mission_with_a_green_first_job(
            tmp_path, "check the importer")
        job_two = continue_mission(_PROJECT, mission.id, "Add the CSV path",
                                   root=tmp_path)

        run = execute_mission_followup(
            job_two, runner=lambda argv, cwd: (1, "ImporterError: schema drifted"),
            work_runner=lambda task: True)

        assert "check the importer" in run.message
        assert "exited 1" in run.message
        assert "the follow-up never started" in run.message
        assert "ImporterError: schema drifted" in run.verify.output_tail

    def test_the_ordering_is_readable_from_the_evidence_record(self, tmp_path):
        mission, _job_one = self._mission_with_a_green_first_job(
            tmp_path, "check the importer")
        job_two = continue_mission(_PROJECT, mission.id, "Add the CSV path",
                                   root=tmp_path)

        execute_mission_followup(
            job_two, runner=lambda argv, cwd: (0, "fine"),
            work_runner=lambda task: True)

        record = read_mission_verify_record(str(job_two.id))
        assert record["steps"][0].startswith("verify:")
        assert record["verify"]["command"] == "check the importer"
        assert record["verify"]["follow_up_may_start"] is True

    def test_a_failed_verify_leaves_the_work_task_unstarted_on_the_job(
            self, tmp_path):
        mission, _job_one = self._mission_with_a_green_first_job(
            tmp_path, "check the importer")
        job_two = continue_mission(_PROJECT, mission.id, "Add the CSV path",
                                   root=tmp_path)

        execute_mission_followup(job_two, runner=lambda argv, cwd: (1, "broken"),
                                 work_runner=lambda task: True)

        reloaded = load_job(job_two.id)
        assert reloaded.tasks[0].status == RunState.FAILED
        assert reloaded.tasks[1].status == RunState.PENDING

    def test_the_lineage_is_correct_in_the_chain(self, tmp_path):
        mission, job_one = self._mission_with_a_green_first_job(
            tmp_path, "check the importer")
        job_two = continue_mission(_PROJECT, mission.id, "Add the CSV path",
                                   root=tmp_path)

        chain = load_mission(_PROJECT, mission.id, root=tmp_path)

        assert [(link.job_id, link.role) for link in chain.job_links] == [
            (str(job_one.id), MISSION_ROLE_INITIAL),
            (str(job_two.id), MISSION_ROLE_FOLLOW_UP),
        ]
        rendered = "\n".join(render_mission_chain(chain))
        assert rendered.index(str(job_one.id)) < rendered.index(str(job_two.id))

    def test_the_follow_up_plan_is_verify_first(self, tmp_path):
        mission, job_one = self._mission_with_a_green_first_job(
            tmp_path, "check the importer")

        job_two = continue_mission(_PROJECT, mission.id, "Add the CSV path",
                                   root=tmp_path)

        assert is_verify_task(job_two.tasks[0])
        assert job_two.tasks[0].inputs["previous_job_id"] == str(job_one.id)
        assert job_two.tasks[1].description == "Add the CSV path"

    def test_the_first_job_of_an_empty_mission_has_nothing_to_verify(self, tmp_path):
        mission = create_mission(_PROJECT, "Keep the importer working",
                                 root=tmp_path)

        job = continue_mission(_PROJECT, mission.id, "Write the importer",
                               root=tmp_path)

        assert not is_verify_task(job.tasks[0])
        assert job.metadata["mission_role"] == MISSION_ROLE_INITIAL

    def test_a_gone_previous_job_refuses_rather_than_verifying_blind(self, tmp_path):
        mission, job_one = self._mission_with_a_green_first_job(
            tmp_path, "check the importer")
        (tmp_path / "jobs" / f"{job_one.id}.json").unlink()

        with pytest.raises(MissionError) as exc:
            continue_mission(_PROJECT, mission.id, "Add the CSV path",
                             root=tmp_path)

        assert "starting blind" in str(exc.value)

    def test_an_empty_next_step_is_refused(self, tmp_path):
        mission, _job_one = self._mission_with_a_green_first_job(
            tmp_path, "check the importer")

        with pytest.raises(MissionError):
            continue_mission(_PROJECT, mission.id, "   ", root=tmp_path)

    def test_an_unverifiable_previous_job_is_reported_not_claimed_green(
            self, tmp_path):
        """A9: nothing to verify does not block, and is never called a pass."""
        job_one = Job(name="job one", state=RunState.COMPLETED,
                      project_id=_PROJECT)
        save_job(job_one)
        mission = create_mission(_PROJECT, "Keep it working", root=tmp_path)
        link_job_to_mission(_PROJECT, mission.id, str(job_one.id),
                            MISSION_ROLE_INITIAL, root=tmp_path)
        job_two = continue_mission(_PROJECT, mission.id, "Add the CSV path",
                                   root=tmp_path)

        run = execute_mission_followup(job_two, work_runner=lambda task: True)

        assert run.verify.result == VERIFY_RESULT_UNVERIFIABLE
        assert "nothing was verified" in run.message
        assert run.follow_up_started is True
