"""Operator amendment amend1014-luna-mission-fixes A.2, A.3, A.5: reconcile's restore, its
interrupted fold and its refusal of jobs that have not ended."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

import pytest

from packages.orchestration.mission_record import MissionError
from packages.orchestration.mission_state import (
    create_mission,
    link_job_to_mission,
    list_missions,
)
from packages.orchestration.repo_mission_reconcile import (
    reconcile_repo_missions,
    restore_reconcile,
)


def _legacy(project_id, root, goal, jobs, minute):
    mission = create_mission(project_id, goal, root=root,
                             now=datetime(2026, 1, 1, tzinfo=timezone.utc) + timedelta(minutes=minute))
    for index, job in enumerate(jobs):
        link_job_to_mission(project_id, mission.id, job, "initial" if index == 0 else "follow_up",
                            root=root)
    return mission


class TestRestoreValidatesFirst:
    def test_a_path_that_does_not_exist_is_refused_and_the_area_is_untouched(self, tmp_path):
        project_id = str(uuid4())
        _legacy(project_id, tmp_path, "first", ["j1"], 0)

        with pytest.raises(MissionError, match="/nowhere/that/exists"):
            restore_reconcile(Path("/nowhere/that/exists"), tmp_path)

        assert len(list_missions(project_id, tmp_path)) == 1

    def test_a_directory_outside_the_backup_folder_is_refused(self, tmp_path):
        project_id = str(uuid4())
        _legacy(project_id, tmp_path, "first", ["j1"], 0)
        elsewhere = tmp_path / "elsewhere"
        elsewhere.mkdir()
        (elsewhere / "x.json").write_text("{}")

        with pytest.raises(MissionError, match="reconcile-backups"):
            restore_reconcile(elsewhere, tmp_path)

        assert len(list_missions(project_id, tmp_path)) == 1

    def test_an_empty_backup_is_refused(self, tmp_path):
        project_id = str(uuid4())
        _legacy(project_id, tmp_path, "first", ["j1"], 0)
        empty = tmp_path / "reconcile-backups" / "20260101T000000Z"
        empty.mkdir(parents=True)

        with pytest.raises(MissionError, match="no mission file"):
            restore_reconcile(empty, tmp_path)

        assert len(list_missions(project_id, tmp_path)) == 1

    def test_a_real_backup_is_restored_and_no_swap_copy_stays(self, tmp_path):
        project_id = str(uuid4())
        _legacy(project_id, tmp_path, "first", ["j1"], 0)
        _legacy(project_id, tmp_path, "second", ["j2"], 5)
        backup = reconcile_repo_missions(apply=True, root=tmp_path)["projects"][0]["backup"]

        restore_reconcile(Path(backup), tmp_path)

        assert len(list_missions(project_id, tmp_path)) == 2
        assert not [p.name for p in tmp_path.iterdir()
                    if ".restoring-" in p.name or ".replaced-" in p.name]


class TestAFoldInterruptedHalfWayStaysRepairable:
    def test_a_canonical_saved_with_the_duplicates_links_is_folded_not_refused(self, tmp_path):
        from dataclasses import replace

        from packages.orchestration.mission_state import load_mission, save_mission

        project_id = str(uuid4())
        old = _legacy(project_id, tmp_path, "first", ["j1"], 0)
        dup = _legacy(project_id, tmp_path, "second", ["j2"], 5)
        # The crash: the canonical was saved with the duplicate's link, the duplicate not aliased yet.
        canonical = load_mission(project_id, old.id, tmp_path)
        dup_links = load_mission(project_id, dup.id, tmp_path).job_links
        save_mission(replace(canonical, job_links=(*canonical.job_links, *dup_links)), tmp_path)

        report = reconcile_repo_missions(apply=True, root=tmp_path)

        assert not report["refused"]
        [live] = list_missions(project_id, tmp_path)
        assert sorted(live.job_ids()) == ["j1", "j2"]

