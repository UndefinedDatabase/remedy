"""F042 T001, DECISION F042 D1 — the cockpit's project list and per-project summary.

Written by the reviewer as the acceptance of T001: every number a card shows is
pinned here against the reader it composes, never against a figure this file
invents. Two registered projects, `alpha` and `beta`, each in its own git
folder, own jobs with FIXED creation times. `NOW` lies BEFORE any real run of
this file: a card the decision queue derives on the spot is stamped with the
real clock, so its age under `NOW` is negative and scores 0, and the one urgency
that counts comes from a failed test event whose timestamp is recorded, which
makes the peak exact on every date this file is run.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime, timezone
from uuid import uuid4

import pytest

from packages.core.models import RunState
from packages.orchestration.data_paths import resolve_data_root, run_log_dir
from packages.orchestration.decision_inbox import build_decision_inbox, decision_urgency
from packages.orchestration.job_digest import build_job_digest
from packages.orchestration.pingpong_job import JobPlan, save_job_plan
from packages.orchestration.project_cockpit import (
    MISSING_REPO_FIX_IT,
    NO_REPO_FIX_IT,
    PROJECT_COCKPIT_VERSION,
    find_project,
    job_project_view,
    project_summary,
    projects_view,
)
from packages.orchestration.project_registry import register_project_repo
from packages.orchestration.timeline import load_run_events
from packages.orchestration.token_ledger import (
    COST_BASIS_PROVIDER_REPORTED,
    COST_BASIS_UNKNOWN,
    CallRecord,
    query_cost,
    record_call,
)

NOW = datetime(2026, 9, 1, 12, 0, tzinfo=timezone.utc)

#: The two envelopes' whole key sets, literal on purpose: the point is that the
#: module cannot grow or drop a key without this file saying so.
VIEW_KEYS = {"version", "projects", "default_project", "single_project", "unscoped_jobs", "orphaned_jobs"}
ENTRY_KEYS = {"id", "slug", "name", "repo_path", "repo_reachable", "fix_it"}
SUMMARY_KEYS = {"version", "project_id", "slug", "jobs", "last_result", "cost_today", "decisions", "degraded"}


def _git_folder(path):
    path.mkdir()
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    return path


def _job(project, title, created_at, state=RunState.PLANNED):
    job = JobPlan(job_title=title, project_id=str(project.id) if project else "",
                  created_at=created_at, state=state)
    save_job_plan(job)
    return job


def _failed_test(job, timestamp):
    folder = run_log_dir(str(job.job_id), resolve_data_root())
    folder.mkdir(parents=True, exist_ok=True)
    event = {"event": "test_run_completed", "timestamp": timestamp,
             "metadata": {"status": "failed", "command_safe": "pytest -q", "test_run_id": f"run-{job.job_id}"}}
    (folder / "events.jsonl").write_text(json.dumps(event) + "\n", encoding="utf-8")


def _call(project, call_id, ts_utc, cost_usd, basis):
    assert record_call(CallRecord(call_id=call_id, ts_utc=ts_utc, cost_usd=cost_usd, cost_basis=basis),
                       project_id=project.id)


@pytest.fixture
def world(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.delenv("REMEDY_PROJECT", raising=False)
    alpha = register_project_repo("alpha", _git_folder(tmp_path / "alpha"))
    beta = register_project_repo("beta", _git_folder(tmp_path / "beta"))
    jobs = {
        "a_old": _job(alpha, "alpha finished", "2026-09-01T08:00:00+00:00", RunState.COMPLETED),
        "a_run": _job(alpha, "alpha running", "2026-09-01T10:00:00+00:00", RunState.RUNNING),
        "a_new": _job(alpha, "alpha newest", "2026-09-01T11:00:00+00:00", RunState.BLOCKED),
        "b_one": _job(beta, "beta only", "2026-09-01T09:00:00+00:00", RunState.FAILED),
    }
    _failed_test(jobs["a_run"], "2026-09-01T11:00:00+00:00")
    _failed_test(jobs["b_one"], "2026-09-01T09:00:00+00:00")
    _call(alpha, "a-today", "2026-09-01T08:30:00+00:00", 0.25, COST_BASIS_PROVIDER_REPORTED)
    _call(alpha, "a-yesterday", "2026-08-31T23:59:59+00:00", 1.0, COST_BASIS_PROVIDER_REPORTED)
    _call(alpha, "a-tomorrow", "2026-09-02T00:00:00+00:00", 2.0, COST_BASIS_PROVIDER_REPORTED)
    _call(beta, "b-priced", "2026-09-01T09:30:00+00:00", 0.5, COST_BASIS_PROVIDER_REPORTED)
    _call(beta, "b-unpriced", "2026-09-01T09:31:00+00:00", None, COST_BASIS_UNKNOWN)
    return {"tmp": tmp_path, "alpha": alpha, "beta": beta, "jobs": jobs}


class TestProjectsView:
    def test_the_view_lists_every_project_by_slug_with_its_folder_checked(self, world):
        view = projects_view(str(world["tmp"]))
        assert set(view) == VIEW_KEYS
        assert view["version"] == PROJECT_COCKPIT_VERSION == 1
        assert [set(p) for p in view["projects"]] == [ENTRY_KEYS, ENTRY_KEYS]
        assert view["projects"] == [
            {"id": str(world["alpha"].id), "slug": "alpha", "name": "alpha",
             "repo_path": world["alpha"].canonical_repo_path, "repo_reachable": True, "fix_it": None},
            {"id": str(world["beta"].id), "slug": "beta", "name": "beta",
             "repo_path": world["beta"].canonical_repo_path, "repo_reachable": True, "fix_it": None},
        ]
        assert view["single_project"] is False
        assert (view["unscoped_jobs"], view["orphaned_jobs"]) == (0, 0)

    def test_a_moved_folder_is_unreachable_and_names_the_attach_fix_it(self, world):
        shutil.rmtree(world["tmp"] / "beta")
        beta = projects_view(str(world["tmp"]))["projects"][1]
        assert beta["repo_reachable"] is False
        assert beta["fix_it"] == MISSING_REPO_FIX_IT.format(path=world["beta"].canonical_repo_path, slug="beta")
        assert beta["fix_it"] == (
            f"The folder {world['beta'].canonical_repo_path} is not there any more. If the project moved, "
            "run: remedy project attach --project beta --repo <the new folder>")

    def test_a_project_with_no_folder_names_the_attach_fix_it(self, world, monkeypatch):
        from packages.orchestration import project_registry

        orphan = project_registry.RemyProject(name="loose", slug="loose")
        project_registry.save_project(orphan)
        entry = [p for p in projects_view(str(world["tmp"]))["projects"] if p["slug"] == "loose"][0]
        assert entry == {"id": str(orphan.id), "slug": "loose", "name": "loose", "repo_path": None,
                         "repo_reachable": False, "fix_it": NO_REPO_FIX_IT.format(slug="loose")}
        assert entry["fix_it"] == ("No folder is attached to this project. "
                                   "Run: remedy project attach --project loose --repo <its folder>")

    def test_the_default_project_follows_the_resolution_precedence(self, world, monkeypatch):
        assert projects_view(str(world["tmp"]))["default_project"] is None
        assert projects_view(str(world["tmp"] / "alpha"))["default_project"] == {
            "id": str(world["alpha"].id), "slug": "alpha", "source": "cwd"}
        monkeypatch.setenv("REMEDY_PROJECT", "beta")
        assert projects_view(str(world["tmp"] / "alpha"))["default_project"] == {
            "id": str(world["beta"].id), "slug": "beta", "source": "environment"}
        monkeypatch.setenv("REMEDY_PROJECT", "no-such-project")
        assert projects_view(str(world["tmp"] / "alpha"))["default_project"] is None

    def test_jobs_no_card_can_show_are_counted_not_hidden(self, world):
        _job(None, "legacy job", "2026-09-01T07:00:00+00:00")
        orphan = JobPlan(job_title="orphaned job", project_id=str(uuid4()), created_at="2026-09-01T07:00:00+00:00")
        save_job_plan(orphan)
        view = projects_view(str(world["tmp"]))
        assert (view["unscoped_jobs"], view["orphaned_jobs"]) == (1, 1)

    def test_a_single_project_says_so(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        monkeypatch.delenv("REMEDY_PROJECT", raising=False)
        register_project_repo("solo", _git_folder(tmp_path / "solo"))
        view = projects_view(str(tmp_path))
        assert view["single_project"] is True
        assert [p["slug"] for p in view["projects"]] == ["solo"]

    def test_no_registry_is_an_empty_list_not_an_error(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        monkeypatch.delenv("REMEDY_PROJECT", raising=False)
        assert projects_view(str(tmp_path)) == {
            "version": 1, "projects": [], "default_project": None, "single_project": False,
            "unscoped_jobs": 0, "orphaned_jobs": 0}


class TestFindProject:
    def test_a_slug_and_a_uuid_both_name_the_project(self, world):
        assert find_project("alpha").id == world["alpha"].id
        assert find_project(str(world["beta"].id)).id == world["beta"].id

    def test_an_unknown_selector_is_none(self, world):
        assert find_project("gamma") is None
        assert find_project(str(uuid4())) is None


class TestProjectSummary:
    def test_the_summary_has_exactly_its_keys(self, world):
        summary = project_summary(world["alpha"], now=NOW)
        assert set(summary) == SUMMARY_KEYS
        assert summary["version"] == 1
        assert (summary["project_id"], summary["slug"]) == (str(world["alpha"].id), "alpha")
        assert summary["degraded"] is False

    def test_jobs_count_the_scoped_jobs_and_the_ones_that_can_still_run(self, world):
        assert project_summary(world["alpha"], now=NOW)["jobs"] == {"active": 2, "total": 3}
        assert project_summary(world["beta"], now=NOW)["jobs"] == {"active": 0, "total": 1}

    def test_the_last_result_is_the_newest_jobs_digest(self, world):
        newest = world["jobs"]["a_new"]
        digest = build_job_digest(newest)
        assert project_summary(world["alpha"], now=NOW)["last_result"] == {
            "job_id": str(newest.job_id), "title": "alpha newest",
            "state": digest["state"], "headline": digest["headline"]}
        assert digest["state"] == "blocked"

    def test_a_project_with_no_jobs_has_no_last_result(self, world, tmp_path):
        gamma = register_project_repo("gamma", _git_folder(tmp_path / "gamma"))
        summary = project_summary(gamma, now=NOW)
        assert summary["last_result"] is None
        assert summary["jobs"] == {"active": 0, "total": 0}
        assert summary["decisions"] == {"open_count": 0, "peak_urgency": 0}

    def test_cost_today_is_the_ledgers_utc_day_and_names_its_basis(self, world):
        alpha = project_summary(world["alpha"], now=NOW)["cost_today"]
        assert alpha == {"day": "2026-09-01", "value_usd": 0.25, "basis": "actual", "calls": 1}
        report = query_cost(project_id=world["alpha"].id, since="2026-09-01", until="2026-09-02")
        assert (alpha["value_usd"], alpha["calls"]) == (report.total.cost_usd, report.total.calls)

    def test_an_unpriced_call_makes_cost_today_a_lower_bound(self, world):
        assert project_summary(world["beta"], now=NOW)["cost_today"] == {
            "day": "2026-09-01", "value_usd": 0.5, "basis": "lower_bound", "calls": 2}

    def test_no_ledger_is_an_absent_cost_never_a_zero(self, world, tmp_path):
        gamma = register_project_repo("gamma", _git_folder(tmp_path / "gamma"))
        assert project_summary(gamma, now=NOW)["cost_today"] == {
            "day": "2026-09-01", "value_usd": None, "basis": "absent", "calls": 0}

    def test_the_day_is_the_utc_day_of_the_moment_asked(self, world):
        late = datetime(2026, 9, 2, 0, 30, tzinfo=timezone.utc)
        assert project_summary(world["alpha"], now=late)["cost_today"] == {
            "day": "2026-09-02", "value_usd": 2.0, "basis": "actual", "calls": 1}

    def test_decisions_sum_every_scoped_jobs_open_cards(self, world):
        decisions = project_summary(world["alpha"], now=NOW)["decisions"]
        expected_open, expected_peak = 0, 0
        for key in ("a_old", "a_run", "a_new"):
            job = world["jobs"][key]
            events = load_run_events(resolve_data_root(), str(job.job_id))
            for card in build_decision_inbox(job, events, now=NOW)["decisions"]:
                if card["status"] == "open":
                    expected_open += 1
                    expected_peak = max(expected_peak, decision_urgency(card))
        assert decisions == {"open_count": expected_open, "peak_urgency": expected_peak}
        assert decisions == {"open_count": 5, "peak_urgency": 3600}

    @pytest.mark.parametrize("damage", ["undecodable", "directory"])
    def test_an_unreadable_jobs_run_log_is_skipped_never_the_card(self, world, damage):
        job = world["jobs"]["a_run"]
        events_path = run_log_dir(str(job.job_id), resolve_data_root()) / "events.jsonl"
        if damage == "undecodable":
            events_path.write_bytes(b"\xff\xfe not utf-8\n")
        else:
            events_path.unlink()
            events_path.mkdir()

        expected_open, expected_peak = 0, 0
        for key in ("a_old", "a_new"):
            other = world["jobs"][key]
            events = load_run_events(resolve_data_root(), str(other.job_id))
            for card in build_decision_inbox(other, events, now=NOW)["decisions"]:
                if card["status"] == "open":
                    expected_open += 1
                    expected_peak = max(expected_peak, decision_urgency(card))

        summary = project_summary(world["alpha"], now=NOW)
        assert summary["decisions"] == {"open_count": expected_open, "peak_urgency": expected_peak}
        assert summary["decisions"] != {"open_count": 5, "peak_urgency": 3600}
        assert summary["jobs"]["total"] == 3

    def test_an_unexpected_error_in_the_inbox_is_not_swallowed(self, world, monkeypatch):
        def _raise(job, events, now=None):
            raise RuntimeError("inbox bug")

        monkeypatch.setattr("packages.orchestration.decision_inbox.build_decision_inbox", _raise)
        with pytest.raises(RuntimeError, match="inbox bug"):
            project_summary(world["alpha"], now=NOW)

    def test_the_open_count_is_the_one_remedy_status_prints(self, world, capsys):
        from apps.cli.commands.status_cmd import _cmd_status

        for project in (world["alpha"], world["beta"]):
            _cmd_status(repo=str(world["tmp"]), project_flag=project.slug, json_output=True)
            printed = json.loads(capsys.readouterr().out)
            summary = project_summary(project, now=NOW)
            assert summary["decisions"]["open_count"] == printed["decisions_open"]
            assert summary["jobs"]["total"] == sum(len(group) for group in printed["jobs"].values())

    def test_one_projects_jobs_never_reach_anothers_card(self, world):
        beta = project_summary(world["beta"], now=NOW)
        assert beta["last_result"]["job_id"] == str(world["jobs"]["b_one"].job_id)
        assert beta["decisions"] == {"open_count": 3, "peak_urgency": 10800}

    def test_a_legacy_job_joins_the_card_only_when_one_project_exists(self, world, tmp_path, monkeypatch):
        _job(None, "legacy job", "2026-09-01T11:30:00+00:00")
        assert project_summary(world["alpha"], now=NOW)["jobs"]["total"] == 3
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "solo-data"))
        solo = register_project_repo("solo", _git_folder(tmp_path / "solo"))
        _job(None, "legacy job", "2026-09-01T11:30:00+00:00")
        assert project_summary(solo, now=NOW)["jobs"]["total"] == 1


class TestJobProjectView:
    """F042 T002, DECISION F042 D2: the project a job belongs to, labelled as `remedy job list`
    labels it, so the cockpit opens on the job's own project and says so when it has none."""

    def test_a_scoped_job_names_its_project_entry(self, world):
        job = world["jobs"]["a_run"]
        view = job_project_view(job)
        assert set(view) == {"version", "job_id", "scope", "project"}
        assert view == {
            "version": 1, "job_id": str(job.job_id), "scope": "project",
            "project": projects_view(str(world["tmp"]))["projects"][0]}

    def test_a_job_with_no_project_is_unscoped(self, world):
        legacy = _job(None, "legacy job", "2026-09-01T07:00:00+00:00")
        assert job_project_view(legacy) == {
            "version": 1, "job_id": str(legacy.job_id), "scope": "unscoped", "project": None}

    def test_a_job_whose_project_is_gone_is_orphaned(self, world):
        orphan = JobPlan(job_title="orphaned job", project_id=str(uuid4()),
                         created_at="2026-09-01T07:00:00+00:00")
        save_job_plan(orphan)
        assert job_project_view(orphan) == {
            "version": 1, "job_id": str(orphan.job_id), "scope": "orphaned", "project": None}

    def test_a_moved_folder_travels_with_the_jobs_project(self, world):
        shutil.rmtree(world["tmp"] / "beta")
        entry = job_project_view(world["jobs"]["b_one"])["project"]
        assert (entry["slug"], entry["repo_reachable"]) == ("beta", False)
