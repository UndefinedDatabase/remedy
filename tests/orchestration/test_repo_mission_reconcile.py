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


class TestReconcileRefusesEveryJobThatHasNotEnded:
    def test_a_paused_job_of_a_duplicate_refuses_the_fold_naming_it(self, tmp_path, monkeypatch):
        from packages.orchestration.pingpong_job import JOB_PAUSED, JobPlan, save_job_plan

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        project_id = str(uuid4())
        paused = "c" * 16
        save_job_plan(JobPlan(job_id=paused, job_title="t", project_id=project_id,
                              state=JOB_PAUSED), tmp_path)
        _legacy(project_id, tmp_path, "first", ["j1"], 0)
        _legacy(project_id, tmp_path, "second", [paused], 5)

        report = reconcile_repo_missions(apply=True, root=tmp_path)

        [refusal] = report["refused"]
        assert any(paused in reason and "paused" in reason for reason in refusal["reasons"])
        assert len(list_missions(project_id, tmp_path)) == 2


def _stamped(project_id, root, mission, key):
    """Stamp a saved mission with a repository key, keeping its links."""
    from dataclasses import replace

    from packages.orchestration.mission_state import load_mission, save_mission

    save_mission(replace(load_mission(project_id, mission.id, root), repo=key), root)


class TestReconcileGroupsPerRepository:
    """R-1295: each repository a project holds has its own one mission, so duplicates fold per key."""

    def test_legacy_duplicates_fold_when_a_second_repositorys_mission_is_the_newest(self, tmp_path):
        project_id = str(uuid4())
        first = _legacy(project_id, tmp_path, "first", ["j1"], 0)
        _legacy(project_id, tmp_path, "second", ["j2"], 5)
        other = _legacy(project_id, tmp_path, "other repository", ["j3"], 9)
        _stamped(project_id, tmp_path, other, f"{project_id}:0123456789ab")

        report = reconcile_repo_missions(apply=True, root=tmp_path)

        assert not report["refused"]
        live = {m.id: m for m in list_missions(project_id, tmp_path)}
        assert set(live) == {first.id, other.id}
        assert live[first.id].job_ids() == ("j1", "j2") and live[other.id].job_ids() == ("j3",)

    def test_duplicates_of_two_repositories_each_fold_into_their_own_mission(self, tmp_path):
        project_id = str(uuid4())
        key = f"{project_id}:0123456789ab"
        first = _legacy(project_id, tmp_path, "first", ["j1"], 0)
        second = _legacy(project_id, tmp_path, "second", ["j2"], 5)
        other = _legacy(project_id, tmp_path, "other first", ["j3"], 7)
        other_dup = _legacy(project_id, tmp_path, "other second", ["j4"], 9)
        for mission, stamp in ((first, project_id), (second, project_id), (other, key), (other_dup, key)):
            _stamped(project_id, tmp_path, mission, stamp)

        report = reconcile_repo_missions(apply=True, root=tmp_path)

        assert not report["refused"]
        live = {m.id: m for m in list_missions(project_id, tmp_path)}
        assert set(live) == {first.id, other.id}
        assert live[first.id].job_ids() == ("j1", "j2") and live[other.id].job_ids() == ("j3", "j4")
        assert live[first.id].repo == project_id and live[other.id].repo == key


class TestAFoldedDuplicateKeepsItsCurrentOrder:
    def test_a_duplicates_unsealed_last_batch_keeps_its_plan_and_contract(self, tmp_path):
        """R-1284: a duplicate's current plan and contract live in its slots; the fold seals them
        into its last batch before the batches are merged."""
        from dataclasses import replace

        from packages.orchestration.mission_record import MissionOrderBatch
        from packages.orchestration.mission_state import load_mission, save_mission

        project_id = str(uuid4())
        first = _legacy(project_id, tmp_path, "first", ["j1"], 0)
        dup = _legacy(project_id, tmp_path, "second", ["j2"], 5)
        batch = MissionOrderBatch(order_id="b" * 32, text="second", created_at="2026-01-01T00:05:00+00:00")
        current = load_mission(project_id, dup.id, tmp_path)
        save_mission(replace(
            current, orders=(batch,), mission_plan={"milestones": ["m1"]}, contract={"goal": "second"},
            job_links=tuple(replace(link, order_id=batch.order_id) for link in current.job_links)), tmp_path)

        reconcile_repo_missions(apply=True, root=tmp_path)

        [live] = list_missions(project_id, tmp_path)
        assert live.id == first.id and live.job_ids() == ("j1", "j2")
        sealed = next(b for b in live.orders if b.order_id == batch.order_id).sealed
        assert sealed["plan"] == {"milestones": ["m1"]} and sealed["contract"] == {"goal": "second"}


class TestReconcileBackupsAreAClassOfTheirOwn:
    """R-1283: a backup holds only the projects a step writes, in a registered class it prunes."""

    def test_a_fold_backs_up_only_its_own_project_into_the_registered_class(self, tmp_path):
        from packages.orchestration.data_paths import classify_data_child, reconcile_backups_dir

        project_id, bystander = str(uuid4()), str(uuid4())
        _legacy(project_id, tmp_path, "first", ["j1"], 0)
        _legacy(project_id, tmp_path, "second", ["j2"], 5)
        _legacy(bystander, tmp_path, "alone", ["j3"], 0)

        backup = Path(reconcile_repo_missions(apply=True, root=tmp_path)["projects"][0]["backup"])

        assert backup.parent == reconcile_backups_dir(tmp_path)
        assert classify_data_child(backup.parent.name) == "durable"
        assert sorted(p.name for p in backup.iterdir()) == [project_id]

    def test_a_new_backup_removes_the_backups_older_than_the_kept_span(self, tmp_path):
        from packages.orchestration.data_paths import reconcile_backups_dir

        folder = reconcile_backups_dir(tmp_path)
        made = datetime.now(timezone.utc)
        old, young, foreign = (folder / (made - timedelta(days=31)).strftime("%Y%m%dT%H%M%S%fZ"),
                               folder / (made - timedelta(days=1)).strftime("%Y%m%dT%H%M%S%fZ"),
                               folder / "kept-by-hand")
        for path in (old, young, foreign):
            path.mkdir(parents=True)
        project_id = str(uuid4())
        _legacy(project_id, tmp_path, "first", ["j1"], 0)
        _legacy(project_id, tmp_path, "second", ["j2"], 5)

        reconcile_repo_missions(apply=True, root=tmp_path)

        assert not old.exists() and young.is_dir() and foreign.is_dir()

    def test_a_restore_puts_back_the_projects_it_holds_and_leaves_the_others(self, tmp_path):
        project_id, bystander = str(uuid4()), str(uuid4())
        _legacy(project_id, tmp_path, "first", ["j1"], 0)
        _legacy(project_id, tmp_path, "second", ["j2"], 5)
        backup = reconcile_repo_missions(apply=True, root=tmp_path)["projects"][0]["backup"]
        _legacy(bystander, tmp_path, "made after the fold", ["j3"], 0)

        restore_reconcile(Path(backup), tmp_path)

        assert len(list_missions(project_id, tmp_path)) == 2
        assert [m.goal for m in list_missions(bystander, tmp_path)] == ["made after the fold"]

    def test_a_backup_holding_a_name_that_is_no_project_is_refused(self, tmp_path):
        from packages.orchestration.data_paths import reconcile_backups_dir

        project_id = str(uuid4())
        _legacy(project_id, tmp_path, "first", ["j1"], 0)
        backup = reconcile_backups_dir(tmp_path) / "20260101T000000000000Z"
        (backup / "not a project").mkdir(parents=True)
        (backup / "not a project" / "x.json").write_text("{}")

        with pytest.raises(MissionError, match="which is not a project's mission directory"):
            restore_reconcile(backup, tmp_path)

        assert len(list_missions(project_id, tmp_path)) == 1


def _umbrella(tmp_path):
    """A lead project with a mission of its own and a legacy umbrella over it and one other."""
    from packages.orchestration.pingpong_job import JobPlan, save_job_plan

    lead, other = str(uuid4()), str(uuid4())
    _legacy(lead, tmp_path, "lead own", ["l0"], 0)
    umbrella = create_mission(lead, "both", project_ids=[lead, other], root=tmp_path)
    for job_id, project in (("a" * 16, lead), ("b" * 16, other)):
        save_job_plan(JobPlan(job_id=job_id, job_title="t", project_id=project), tmp_path)
    link_job_to_mission(lead, umbrella.id, "a" * 16, "initial", root=tmp_path)
    link_job_to_mission(lead, umbrella.id, "b" * 16, "follow_up", root=tmp_path)
    return lead, other, umbrella


class TestAHandOverWritesTheTargetUnderItsOwnLock:
    """R-1296: the job of a legacy umbrella goes to its project's one mission, under that project's
    lock, and a mission made for it is named after the project."""

    def test_the_target_mission_is_named_after_the_project_and_saved_under_its_lock(
            self, tmp_path, monkeypatch):
        from types import SimpleNamespace

        from packages.orchestration import repo_mission, repo_mission_reconcile
        from packages.orchestration.mission_state import (
            LOCK_FILENAME,
            _held_mission_lock_paths,
            mission_dir_for_project,
        )

        lead, other, _umbrella_mission = _umbrella(tmp_path)
        monkeypatch.setattr(repo_mission, "project_by_id", lambda project_id: SimpleNamespace(
            id=project_id, slug=f"slug-{project_id[:8]}", name="n", canonical_repo_path=None,
            repo_paths=[]))
        held: dict[str, bool] = {}
        real_save = repo_mission_reconcile.save_mission

        def save(mission, root=None):
            lock = str(mission_dir_for_project(mission.project_id, root) / LOCK_FILENAME)
            held[mission.project_id] = held.get(mission.project_id, True) and lock in _held_mission_lock_paths()
            return real_save(mission, root)

        monkeypatch.setattr(repo_mission_reconcile, "save_mission", save)

        reconcile_repo_missions(apply=True, root=tmp_path)

        [mission_other] = list_missions(other, tmp_path)
        assert mission_other.goal == f"Maintain slug-{other[:8]}"
        assert mission_other.job_ids() == ("b" * 16,)
        assert held == {lead: True, other: True}

    def test_a_restore_of_a_hand_over_takes_back_the_mission_it_made(self, tmp_path):
        lead, other, umbrella = _umbrella(tmp_path)
        backup = reconcile_repo_missions(apply=True, root=tmp_path)["projects"][0]["backup"]
        assert len(list_missions(other, tmp_path)) == 1

        restore_reconcile(Path(backup), tmp_path)

        assert list_missions(other, tmp_path) == []
        assert umbrella.id in {m.id for m in list_missions(lead, tmp_path)}
