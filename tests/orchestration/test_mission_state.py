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

import pytest

from packages.orchestration.mission_state import (
    MAX_MISSION_GOAL_CHARS,
    MISSION_SCHEMA_VERSION,
    MISSION_STATUS_ABANDONED,
    MISSION_STATUS_ACTIVE,
    Mission,
    MissionError,
    MissionGoalImmutableError,
    MissionNotFoundError,
    create_mission,
    list_missions,
    list_missions_safe,
    load_mission,
    mission_dir_for_project,
    mission_record_path,
    project_ids_with_missions,
    save_mission,
)

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
