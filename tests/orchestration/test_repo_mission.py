"""DECISION amend1011b D1-D6: one repository, one lasting mission; each order a batch under it."""

from __future__ import annotations

import subprocess
import threading
from types import SimpleNamespace
from uuid import uuid4

import pytest

from packages.orchestration.mission_state import (
    MISSION_STATUS_ABANDONED,
    MISSION_STATUS_ACHIEVED,
    MISSION_STATUS_PAUSED,
    MissionOrder,
    create_mission,
    list_missions,
    list_missions_safe,
    load_mission,
    mission_for_job,
    project_ids_with_missions,
    save_mission,
    set_mission_status,
)
from packages.orchestration.repo_mission import (
    RepoMissionError,
    accept_order,
    accept_order_in_each,
    ensure_repo_mission,
    link_order_job,
    order_batch_view,
    order_refusal,
    repo_key,
)
from packages.orchestration.repo_mission_reconcile import (
    reconcile_repo_missions,
    restore_reconcile,
)


def _git(path, *args):
    subprocess.run(["git", *args], cwd=path, check=True, capture_output=True)


def _repo(tmp_path, name):
    path = tmp_path / name
    path.mkdir()
    _git(path, "init", "-q")
    _git(path, "-c", "user.email=a@b", "-c", "user.name=n", "commit", "-q", "--allow-empty", "-m", "x")
    return path


def _project(repo, slug=None):
    return SimpleNamespace(id=uuid4(), slug=slug or repo.name, name=repo.name,
                           canonical_repo_path=str(repo), repo_paths=[str(repo)])


def _order(text):
    return MissionOrder(text=text)


def test_three_orders_make_one_mission_with_three_attributed_batches(tmp_path):
    repo = _repo(tmp_path, "app")
    project = _project(repo)
    ids = []
    for index, text in enumerate(("feature", "fix", "extension")):
        mission, batch = accept_order(project, repo, _order(text), root=tmp_path)
        mission = link_order_job(mission.project_id, mission.id, batch.order_id, f"job-{index}",
                                 root=tmp_path)
        ids.append(mission.id)

    assert len(set(ids)) == 1
    [only] = list_missions(str(project.id), tmp_path)
    assert only.goal == "Maintain app"
    assert [link.role for link in only.job_links] == ["initial", "follow_up", "follow_up"]
    view = order_batch_view(only)
    assert [row["text"] for row in view] == ["feature", "fix", "extension"]
    assert [row["job_ids"] for row in view] == [["job-0"], ["job-1"], ["job-2"]]
    assert [bool(row["sealed"]) for row in view] == [True, True, False]
    assert only.order.text == "extension" and only.orders[0].target_commit


def test_a_sealed_order_keeps_its_plan_and_contract_when_the_next_order_arrives(tmp_path):
    repo = _repo(tmp_path, "app")
    project = _project(repo)
    mission, _ = accept_order(project, repo, _order("one"), root=tmp_path)
    save_mission(mission.__class__(**{**mission.__dict__, "contract": {"criteria": ["c"]},
                                      "mission_plan": {"_version": 1, "milestones": []}}), tmp_path)

    later, _ = accept_order(project, repo, _order("two"), root=tmp_path)

    assert later.contract is None
    assert later.orders[0].sealed["contract"] == {"criteria": ["c"]}
    assert later.orders[0].sealed["plan_version"] == 1


def test_a_restart_and_a_linked_worktree_find_the_same_mission(tmp_path):
    repo = _repo(tmp_path, "app")
    project = _project(repo)
    first, _ = accept_order(project, repo, _order("one"), root=tmp_path)
    worktree = tmp_path / "wt"
    _git(repo, "worktree", "add", "-q", str(worktree))

    again, _ = accept_order(project, worktree, _order("two"), root=tmp_path)

    assert again.id == first.id
    assert repo_key(project, worktree) == repo_key(project, repo)


def test_a_repository_the_project_does_not_hold_is_refused(tmp_path):
    project = _project(_repo(tmp_path, "app"))
    with pytest.raises(RepoMissionError):
        accept_order(project, _repo(tmp_path, "other"), _order("x"), root=tmp_path)


def test_two_clones_with_one_remote_are_two_identities(tmp_path):
    a, b = _repo(tmp_path, "a"), _repo(tmp_path, "b")
    for repo in (a, b):
        _git(repo, "remote", "add", "origin", "https://example.invalid/x.git")
    project = SimpleNamespace(id=uuid4(), slug="p", name="p", canonical_repo_path=str(a),
                              repo_paths=[str(a), str(b)])
    assert repo_key(project, a) != repo_key(project, b)
    first, _ = accept_order(project, a, _order("x"), root=tmp_path)
    second, _ = accept_order(project, b, _order("y"), root=tmp_path)
    assert first.id != second.id


def test_different_repositories_get_different_missions(tmp_path):
    one, two = _project(_repo(tmp_path, "one")), _project(_repo(tmp_path, "two"))
    a, _ = accept_order(one, one.canonical_repo_path, _order("x"), root=tmp_path)
    b, _ = accept_order(two, two.canonical_repo_path, _order("x"), root=tmp_path)
    assert a.id != b.id


def test_simultaneous_orders_become_batches_of_one_mission(tmp_path):
    repo = _repo(tmp_path, "app")
    project = _project(repo)
    results, errors = [], []

    def start(index):
        try:
            mission, batch = accept_order(project, repo, _order(f"o{index}"), root=tmp_path)
            link_order_job(mission.project_id, mission.id, batch.order_id, f"job-{index}",
                           root=tmp_path)
            results.append(mission.id)
        except Exception as exc:  # noqa: BLE001
            errors.append(exc)

    threads = [threading.Thread(target=start, args=(i,)) for i in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert not errors
    [only] = list_missions(str(project.id), tmp_path)
    assert len(only.orders) == 8 and len(only.job_links) == 8
    assert [link.role for link in only.job_links].count("initial") == 1


def test_an_achieved_mission_is_reopened_and_says_so_while_paused_and_abandoned_wait(tmp_path):
    repo = _repo(tmp_path, "app")
    project = _project(repo)
    first, _ = accept_order(project, repo, _order("one"), root=tmp_path)
    set_mission_status(first.project_id, first.id, MISSION_STATUS_ACHIEVED, tmp_path)

    reopened, batch = accept_order(project, repo, _order("two"), root=tmp_path)
    assert reopened.id == first.id and reopened.status == "active"
    assert batch.reopened_from == MISSION_STATUS_ACHIEVED

    for status in (MISSION_STATUS_PAUSED, MISSION_STATUS_ABANDONED):
        set_mission_status(first.project_id, first.id, status, tmp_path)
        with pytest.raises(RepoMissionError, match="mission resume"):
            accept_order(project, repo, _order("three"), root=tmp_path)
        assert len(list_missions(str(project.id), tmp_path)) == 1


def test_an_order_is_accepted_by_no_repositorys_mission_unless_every_one_can_take_it(tmp_path):
    """R-1250: every target's mission is asked before any accepts, so a paused second repository
    leaves the first repository's mission without a new batch."""
    one, two = _project(_repo(tmp_path, "one")), _project(_repo(tmp_path, "two"))
    targets = [(one, one.canonical_repo_path), (two, two.canonical_repo_path)]
    first, _ = accept_order(one, one.canonical_repo_path, _order("before"), root=tmp_path)
    second, _ = accept_order(two, two.canonical_repo_path, _order("before"), root=tmp_path)
    set_mission_status(second.project_id, second.id, MISSION_STATUS_PAUSED, tmp_path)

    assert order_refusal(one, one.canonical_repo_path, tmp_path) == ""
    assert "mission resume" in order_refusal(two, two.canonical_repo_path, tmp_path)
    with pytest.raises(RepoMissionError, match="mission resume"):
        accept_order_in_each(targets, _order("both"), root=tmp_path)

    assert len(load_mission(first.project_id, first.id, tmp_path).orders) == 1
    assert len(load_mission(second.project_id, second.id, tmp_path).orders) == 1


def test_an_order_every_mission_can_take_becomes_a_batch_in_each_with_one_correlation(tmp_path):
    one, two = _project(_repo(tmp_path, "one")), _project(_repo(tmp_path, "two"))
    accepted = accept_order_in_each([(one, one.canonical_repo_path), (two, two.canonical_repo_path)],
                                    _order("both"), root=tmp_path)

    batches = [load_mission(str(project.id), accepted[str(project.id)][0], tmp_path).orders[-1]
               for project in (one, two)]
    assert [batch.order_id for batch in batches] == [accepted[str(p.id)][1] for p in (one, two)]
    assert batches[0].correlation_id == batches[1].correlation_id != ""


def test_order_refusal_creates_no_mission(tmp_path):
    project = _project(_repo(tmp_path, "app"))
    assert order_refusal(project, project.canonical_repo_path, tmp_path) == ""
    assert list_missions(str(project.id), tmp_path) == []


def test_ensure_repo_mission_creates_once(tmp_path):
    repo = _repo(tmp_path, "app")
    project = _project(repo)
    first, created = ensure_repo_mission(project, repo, root=tmp_path)
    second, again = ensure_repo_mission(project, repo, root=tmp_path)
    assert (created, again, first.id) == (True, False, second.id)


def test_two_hundred_historical_jobs_stay_listable(tmp_path):
    repo = _repo(tmp_path, "app")
    project = _project(repo)
    for index in range(200):
        mission, batch = accept_order(project, repo, _order(f"o{index}"), root=tmp_path)
        link_order_job(mission.project_id, mission.id, batch.order_id, f"job-{index}", root=tmp_path)
    [only] = list_missions(str(project.id), tmp_path)
    assert len(only.job_links) == 200 and len(order_batch_view(only)) == 200
    assert mission_for_job("job-199", tmp_path).id == only.id


# -- reconcile -------------------------------------------------------------


def _legacy(project_id, tmp_path, goal, jobs, minute):
    from datetime import datetime, timedelta, timezone

    mission = create_mission(project_id, goal, root=tmp_path,
                             now=datetime(2026, 1, 1, tzinfo=timezone.utc) + timedelta(minutes=minute))
    for index, job in enumerate(jobs):
        from packages.orchestration.mission_state import link_job_to_mission

        link_job_to_mission(project_id, mission.id, job, "initial" if index == 0 else "follow_up",
                            root=tmp_path)
    return mission


def test_reconcile_dry_run_changes_nothing_then_folds_losslessly_and_idempotently(tmp_path):
    project_id = str(uuid4())
    old = _legacy(project_id, tmp_path, "first", ["j1", "j2"], 0)
    dup = _legacy(project_id, tmp_path, "second", ["j3"], 5)
    empty = _legacy(project_id, tmp_path, "third", [], 9)
    evidence = tmp_path / "missions" / project_id / dup.id / "evidence"
    evidence.mkdir(parents=True)
    (evidence / "plan.md").write_text("kept")

    report = reconcile_repo_missions(root=tmp_path)
    assert report["projects"][0]["groups"][0]["canonical"] == old.id
    assert len(list_missions(project_id, tmp_path)) == 3

    done = reconcile_repo_missions(apply=True, root=tmp_path)
    assert not done["refused"]
    [live] = list_missions(project_id, tmp_path)
    assert live.id == old.id and live.job_ids() == ("j1", "j2", "j3")
    assert [link.role for link in live.job_links] == ["initial", "follow_up", "follow_up"]
    assert {b.order_id for b in live.orders} == {f"legacy-{m.id[:12]}" for m in (old, dup, empty)}
    sealed = next(b for b in live.orders if b.order_id == f"legacy-{dup.id[:12]}").sealed
    assert sealed["goal"] == "second" and sealed["legacy_roles"] == {"j3": "initial"}
    assert (tmp_path / "missions" / project_id / old.id / "evidence" / "legacy" / dup.id
            / "plan.md").read_text() == "kept"
    assert load_mission(project_id, dup.id, tmp_path).id == old.id
    assert len(list_missions_safe(project_id, tmp_path, include_aliases=True)[0]) == 3
    assert mission_for_job("j3", tmp_path).id == old.id
    assert project_ids_with_missions(tmp_path) == [project_id]

    assert not reconcile_repo_missions(apply=True, root=tmp_path)["projects"]
    assert len(list_missions(project_id, tmp_path)) == 1


def test_reconcile_rolls_back_from_its_backup(tmp_path):
    project_id = str(uuid4())
    _legacy(project_id, tmp_path, "first", ["j1"], 0)
    _legacy(project_id, tmp_path, "second", ["j2"], 5)
    backup = reconcile_repo_missions(apply=True, root=tmp_path)["projects"][0]["backup"]

    restore_reconcile(backup, tmp_path)

    assert len(list_missions(project_id, tmp_path)) == 2


def test_reconcile_refuses_an_unreadable_record(tmp_path):
    project_id = str(uuid4())
    _legacy(project_id, tmp_path, "first", ["j1"], 0)
    _legacy(project_id, tmp_path, "second", ["j2"], 5)
    (tmp_path / "missions" / project_id / "broken.json").write_text("{")

    report = reconcile_repo_missions(apply=True, root=tmp_path)

    assert report["refused"] and len(list_missions(project_id, tmp_path)) == 2


def test_reconcile_gives_each_job_of_a_cross_repository_mission_to_its_own_project(tmp_path):
    lead, other = str(uuid4()), str(uuid4())
    _legacy(lead, tmp_path, "lead own", ["l0"], 0)
    umbrella = create_mission(lead, "both", project_ids=[lead, other], root=tmp_path)
    from packages.orchestration.mission_state import link_job_to_mission
    from packages.orchestration.pingpong_job import JobPlan, save_job_plan

    for job_id, project in (("a" * 16, lead), ("b" * 16, other)):
        save_job_plan(JobPlan(job_id=job_id, job_title="t", project_id=project), tmp_path)
    link_job_to_mission(lead, umbrella.id, "a" * 16, "initial", root=tmp_path)
    link_job_to_mission(lead, umbrella.id, "b" * 16, "follow_up", root=tmp_path)

    reconcile_repo_missions(apply=True, root=tmp_path)

    [mission_lead] = list_missions(lead, tmp_path)
    [mission_other] = list_missions(other, tmp_path)
    assert mission_lead.job_ids() == ("l0", "a" * 16) and mission_other.job_ids() == ("b" * 16,)
    assert mission_for_job("b" * 16, tmp_path).id == mission_other.id


def test_no_production_code_creates_a_mission_except_through_the_repository_mission():
    """DECISION amend1011b D5: `create_mission` is the store's primitive, not an entry point."""
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    allowed = {"packages/orchestration/mission_state.py", "packages/orchestration/repo_mission.py",
               "packages/orchestration/repo_mission_reconcile.py",
               "packages/orchestration/gauntlet_runner.py"}   # a throwaway data root of its own
    found = {path.relative_to(root).as_posix()
             for base in ("packages", "apps") for path in (root / base).rglob("*.py")
             if "create_mission(" in path.read_text(encoding="utf-8")}

    assert found <= allowed, sorted(found - allowed)


# -- the plan chain stays flat (operator amendment amend1014-luna-mission-fixes A.1) --------


class TestThePlanChainStaysFlat:
    """Each planned order adds ONE flat version; nothing nests, nothing doubles."""

    def test_six_planned_orders_keep_one_flat_chain_and_flat_sealed_plans(self, tmp_path):
        import json

        from packages.orchestration.mission_compiler import PLAN_VERSIONS_KEY, plan_mission
        from packages.orchestration.mission_state import mission_dir_for_project

        repo = _repo(tmp_path, "app")
        project = _project(repo)
        sizes = {}
        for plans_so_far in range(1, 7):
            mission, _ = accept_order(project, repo, _order(f"order {plans_so_far}"), root=tmp_path)
            planned = plan_mission(mission.project_id, mission.id, None, root=tmp_path).mission
            versions = planned.mission_plan[PLAN_VERSIONS_KEY]
            assert not [v for v in versions if PLAN_VERSIONS_KEY in v]
            assert len(versions) == plans_so_far - 1
            for batch in planned.orders:
                if batch.sealed is not None and batch.sealed.get("plan") is not None:
                    assert PLAN_VERSIONS_KEY not in batch.sealed["plan"]
            record = mission_dir_for_project(mission.project_id, tmp_path) / f"{mission.id}.json"
            sizes[plans_so_far] = len(json.dumps(json.loads(record.read_text())))
        assert sizes[6] < 3 * sizes[3]

    def test_reconcile_flattens_a_nested_chain_and_keeps_every_other_field(self, tmp_path):
        import json
        from dataclasses import replace as dc_replace

        from packages.orchestration.mission_record import PLAN_VERSION_KEY, PLAN_VERSIONS_KEY
        from packages.orchestration.mission_state import mission_dir_for_project

        repo = _repo(tmp_path, "app")
        project = _project(repo)
        mission, _ = accept_order(project, repo, _order("one"), root=tmp_path)
        v1 = {"milestones": ["a"], PLAN_VERSION_KEY: 1, PLAN_VERSIONS_KEY: []}
        v2 = {"milestones": ["b"], PLAN_VERSION_KEY: 2, PLAN_VERSIONS_KEY: [v1]}
        v3 = {"milestones": ["c"], PLAN_VERSION_KEY: 3, PLAN_VERSIONS_KEY: [v1, v2]}
        current = {"milestones": ["d"], PLAN_VERSION_KEY: 4, PLAN_VERSIONS_KEY: [v1, v2, v3]}
        sealed = dc_replace(mission.orders[0], sealed={"plan": v3, "contract": None,
                                                       "plan_version": 3, "sealed_at": "t"})
        save_mission(dc_replace(mission, mission_plan=current,
                                orders=(sealed, *mission.orders[1:])), tmp_path)
        record = mission_dir_for_project(mission.project_id, tmp_path) / f"{mission.id}.json"
        before = json.loads(record.read_text())

        report = reconcile_repo_missions(root=tmp_path)
        assert [row["mission"] for row in report["flatten"]] == [mission.id]
        assert report["flatten"][0]["bytes_after"] < report["flatten"][0]["bytes_before"]
        assert json.loads(record.read_text()) == before

        done = reconcile_repo_missions(apply=True, root=tmp_path)
        assert done["flatten"][0]["backup"]
        after = json.loads(record.read_text())
        chain = after["mission_plan"][PLAN_VERSIONS_KEY]
        assert [v[PLAN_VERSION_KEY] for v in chain] == [1, 2, 3]
        assert not [v for v in chain if PLAN_VERSIONS_KEY in v]
        assert PLAN_VERSIONS_KEY not in after["orders"][0]["sealed"]["plan"]
        for key in set(before) - {"mission_plan", "orders"}:
            assert json.dumps(after[key], sort_keys=True) == json.dumps(before[key], sort_keys=True)
        assert not reconcile_repo_missions(apply=True, root=tmp_path)["flatten"]


def test_a_follow_up_job_belongs_to_the_current_order_batch(tmp_path, monkeypatch):
    """Operator amendment amend1014-luna-mission-fixes A.4."""
    from packages.orchestration.mission_state import continue_mission
    from packages.orchestration.pingpong_job import JobPlan, save_job_plan
    from packages.orchestration.repo_mission import _unfinished_jobs

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    repo = _repo(tmp_path, "app")
    project = _project(repo)
    mission, batch = accept_order(project, repo, _order("feature"), root=tmp_path)
    first = JobPlan(job_title="first", project_id=str(project.id))
    save_job_plan(first)
    link_order_job(mission.project_id, mission.id, batch.order_id, str(first.job_id), root=tmp_path)

    follow = continue_mission(mission.project_id, mission.id, "next step", root=tmp_path)

    mission = load_mission(mission.project_id, mission.id, tmp_path)
    [link] = [link for link in mission.job_links if link.job_id == str(follow.job_id)]
    assert link.order_id == batch.order_id
    [row] = order_batch_view(mission)
    assert row["order_id"] == batch.order_id and str(follow.job_id) in row["job_ids"]
    assert _unfinished_jobs(mission, batch.order_id)
