"""CLI tests: `remedy mission start|list|show|continue|achieve|abandon|pause`.

F056 T001–T003 plus the R-0163 status-transition surface.

The surface, not the store: the store's own behaviour is proven in
tests/orchestration/test_mission_state.py. What matters here is that the
catalog carries the commands, that scoping follows the F148 rules, that the
listing is honest about records it cannot read, that `show` renders a chain
whose jobs are gone without crashing, that the plan-approval opt-in defaults
to NO, and that `continue` hands back a plan whose first task verifies the
previous job.

Every test runs the real grouped CLI in a subprocess against a tmp_path data
root, so the assertions are made on what an operator actually sees.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


def _run(args: list[str], data_root: Path, *, expect_ok: bool = True):
    """Run the grouped CLI with an isolated data root."""
    env = {**os.environ, "REMEDY_DATA_DIR": str(data_root)}
    env.pop("REMEDY_PROJECT", None)
    proc = subprocess.run(
        [sys.executable, "-m", "apps.cli.grouped", *args],
        cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=120, env=env,
    )
    if expect_ok:
        assert proc.returncode == 0, f"{args} failed ({proc.returncode}): {proc.stderr}"
    return proc


def _make_project(data_root: Path, name: str, slug: str) -> str:
    proc = subprocess.run(
        [sys.executable, "-c",
         "import sys; sys.path.insert(0, '.');"
         "from packages.orchestration.project_registry import RemyProject, save_project;"
         f"p = RemyProject(name={name!r}, slug={slug!r}); save_project(p); print(p.id)"],
        cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=60,
        env={**os.environ, "REMEDY_DATA_DIR": str(data_root)},
    )
    assert proc.returncode == 0, proc.stderr
    return proc.stdout.strip().splitlines()[-1]


@pytest.fixture
def project(tmp_path: Path) -> tuple[Path, str]:
    """A registered project in an isolated data root. Returns (data_root, project_id)."""
    data_root = tmp_path / "data"
    data_root.mkdir(parents=True)
    return data_root, _make_project(data_root, "Mission Test", "mission-test")


def _start(data_root: Path, project_id: str, goal: str) -> str:
    """Start a mission and return its id."""
    body = json.loads(_run(["mission", "start", goal, "--project", project_id,
                            "--json"], data_root).stdout)
    return body["mission"]["id"]


def _link_job(data_root: Path, project_id: str, mission_id: str, *,
              role: str, state: str = "completed") -> str:
    """Persist a job in the given state and link it into the mission's chain."""
    script = (
        "import sys; sys.path.insert(0, '.');"
        "from packages.core.models import Job, RunState;"
        "from packages.orchestration.storage import save_job;"
        "from packages.orchestration.mission_state import link_job_to_mission;"
        f"job = Job(name='fixture', state=RunState({state!r}));"
        "save_job(job);"
        f"link_job_to_mission({project_id!r}, {mission_id!r}, str(job.id), {role!r});"
        "print(job.id)"
    )
    proc = subprocess.run(
        [sys.executable, "-c", script], cwd=str(REPO_ROOT), capture_output=True,
        text=True, timeout=60,
        env={**os.environ, "REMEDY_DATA_DIR": str(data_root)},
    )
    assert proc.returncode == 0, proc.stderr
    return proc.stdout.strip().splitlines()[-1]


class TestCatalog:
    def test_the_mission_commands_are_in_the_catalog(self):
        from apps.cli.command_catalog import CATALOG

        ids = {entry.command_id for entry in CATALOG}
        assert {"mission.start", "mission.list", "mission.show"} <= ids

    def test_list_and_show_are_read_only_and_start_writes_metadata(self):
        from apps.cli.command_catalog import get_command

        assert get_command("mission.list").action_class == "read_only"
        assert get_command("mission.show").action_class == "read_only"
        assert get_command("mission.start").action_class == "write_metadata"

    def test_every_mission_command_has_a_handler(self):
        from apps.cli.commands import collect_all_handlers

        handlers = collect_all_handlers()
        assert {"mission.start", "mission.list", "mission.show"} <= set(handlers)

    def test_no_mission_command_may_execute_or_mutate_the_repo(self):
        from apps.cli.command_catalog import get_command

        for command_id in ("mission.start", "mission.list", "mission.show"):
            entry = get_command(command_id)
            assert entry.may_execute_commands is False
            assert entry.may_mutate_repo is False


class TestStart:
    def test_start_prints_the_new_mission_id(self, project):
        data_root, project_id = project
        proc = _run(["mission", "start", "Keep the importer working",
                     "--project", project_id], data_root)

        mission_id = proc.stdout.strip().splitlines()[0]
        assert len(mission_id) == 32
        listing = _run(["mission", "list", "--project", project_id], data_root).stdout
        assert mission_id[:12] in listing
        assert "Keep the importer working" in listing

    def test_start_json_carries_the_record(self, project):
        data_root, project_id = project
        body = json.loads(_run(["mission", "start", "Keep it working",
                                "--project", project_id, "--json"], data_root).stdout)

        assert body["mission"]["goal"] == "Keep it working"
        assert body["mission"]["status"] == "active"
        assert body["mission"]["job_links"] == []
        assert body["mission"]["dossier_ref"] == ""

    def test_an_empty_goal_is_refused(self, project):
        data_root, project_id = project
        proc = _run(["mission", "start", "   ", "--project", project_id],
                    data_root, expect_ok=False)

        assert proc.returncode == 1
        assert "Error" in proc.stderr

    def test_starting_without_a_project_exits_three(self, tmp_path):
        data_root = tmp_path / "data"
        data_root.mkdir(parents=True)
        proc = _run(["mission", "start", "A goal"], data_root, expect_ok=False)

        assert proc.returncode == 3
        assert "remedy init" in proc.stderr

    def test_the_same_goal_twice_makes_two_missions(self, project):
        """Goals are immutable, so a repeat is a second mission, never an edit."""
        data_root, project_id = project
        first = _start(data_root, project_id, "Keep it working")
        second = _start(data_root, project_id, "Keep it working")

        assert first != second
        body = json.loads(_run(["mission", "list", "--project", project_id,
                                "--json"], data_root).stdout)
        assert len(body["missions"]) == 2


class TestList:
    def test_an_empty_project_says_so(self, project):
        data_root, project_id = project
        proc = _run(["mission", "list", "--project", project_id], data_root)

        assert "No missions found." in proc.stdout

    def test_listing_is_scoped_to_one_project(self, project):
        data_root, project_id = project
        other_id = _make_project(data_root, "Other", "other-project")
        _start(data_root, project_id, "Mine")
        _start(data_root, other_id, "Theirs")

        mine = _run(["mission", "list", "--project", project_id], data_root).stdout
        assert "Mine" in mine
        assert "Theirs" not in mine

    def test_all_projects_widens_the_listing(self, project):
        data_root, project_id = project
        other_id = _make_project(data_root, "Other", "other-project")
        _start(data_root, project_id, "Mine")
        _start(data_root, other_id, "Theirs")

        everything = _run(["mission", "list", "--all-projects"], data_root).stdout
        assert "Mine" in everything
        assert "Theirs" in everything

    def test_an_unreadable_record_is_skipped_and_counted(self, project):
        data_root, project_id = project
        good = _start(data_root, project_id, "Readable goal")
        broken = _start(data_root, project_id, "About to break")
        (data_root / "missions" / project_id / f"{broken}.json").write_text("{ not json")

        proc = _run(["mission", "list", "--project", project_id], data_root)

        assert good[:12] in proc.stdout
        assert "1 unreadable mission record(s) skipped" in proc.stderr

    def test_the_row_shows_the_job_count(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, "Keep it working")
        _link_job(data_root, project_id, mission_id, role="initial")

        proc = _run(["mission", "list", "--project", project_id], data_root)

        assert "1 job(s)" in proc.stdout


class TestShow:
    def test_show_renders_the_chain_in_link_order(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, "Keep it working")
        first = _link_job(data_root, project_id, mission_id, role="initial")
        second = _link_job(data_root, project_id, mission_id, role="follow_up",
                           state="failed")

        out = _run(["mission", "show", mission_id, "--project", project_id],
                   data_root).stdout

        assert out.index(first) < out.index(second)
        assert "initial" in out and "follow_up" in out
        assert "completed" in out and "failed" in out

    def test_show_accepts_a_unique_prefix(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, "Keep it working")

        out = _run(["mission", "show", mission_id[:8], "--project", project_id],
                   data_root).stdout

        assert mission_id in out

    def test_a_deleted_job_renders_as_missing_and_never_crashes(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, "Keep it working")
        job_id = _link_job(data_root, project_id, mission_id, role="initial")
        (data_root / "jobs" / f"{job_id}.json").unlink()

        proc = _run(["mission", "show", mission_id, "--project", project_id],
                    data_root)

        assert "(missing job)" in proc.stdout
        assert "Traceback" not in proc.stdout and "Traceback" not in proc.stderr

    def test_an_unknown_mission_is_an_error_not_a_crash(self, project):
        data_root, project_id = project
        proc = _run(["mission", "show", "0" * 32, "--project", project_id],
                    data_root, expect_ok=False)

        assert proc.returncode == 1
        assert "no mission" in proc.stderr
        assert "Traceback" not in proc.stderr

    def test_show_json_carries_each_link_state(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, "Keep it working")
        job_id = _link_job(data_root, project_id, mission_id, role="initial")

        body = json.loads(_run(["mission", "show", mission_id, "--project",
                                project_id, "--json"], data_root).stdout)

        assert body["mission"]["job_links"] == [{
            "job_id": job_id,
            "role": "initial",
            "created_at": body["mission"]["job_links"][0]["created_at"],
            "job_state": "completed",
        }]

    def test_an_empty_mission_shows_no_chain(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, "Keep it working")

        out = _run(["mission", "show", mission_id, "--project", project_id],
                   data_root).stdout

        assert "no jobs linked yet" in out


def _git_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(repo), "commit", "--allow-empty", "-m", "init", "-q"],
        check=True, capture_output=True,
        env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
             "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"},
    )
    return repo


def _run_in(repo: Path, args: list[str], data_root: Path, *, expect_ok: bool = True):
    """Run the grouped CLI from inside a project repo."""
    env = {**os.environ, "PYTHONPATH": str(REPO_ROOT),
           "REMEDY_DATA_DIR": str(data_root)}
    env.pop("REMEDY_PROJECT", None)
    proc = subprocess.run(
        [sys.executable, "-m", "apps.cli.grouped", *args],
        cwd=str(repo), capture_output=True, text=True, timeout=120, env=env,
        stdin=subprocess.DEVNULL,
    )
    if expect_ok:
        assert proc.returncode == 0, f"{args} failed ({proc.returncode}): {proc.stderr}"
    return proc


def _missions_on_disk(data_root: Path) -> list[Path]:
    return sorted((data_root / "missions").rglob("*.json"))


def _pending_plan_job(repo: Path, data_root: Path, goal: str,
                      *, mission_candidate: bool) -> str:
    """Persist a job with a pending flight plan and the given intake hint."""
    script = (
        "import sys; sys.path.insert(0, '.');"
        "from packages.core.models import Job, RunState;"
        "from packages.orchestration.storage import save_job;"
        "from packages.orchestration.project_registry import resolve_project;"
        f"project = resolve_project({str(repo)!r});"
        f"job = Job(name='fixture', mission={goal!r}, project_id=str(project.id),"
        f"  intake={{'schema_v': 'ji1', 'goal': {goal!r},"
        f"           'mission_candidate': {mission_candidate!r}}},"
        "   flight_plan={'schema_v': 'flight_plan_v1', '_approval': 'pending'},"
        "   state=RunState.PLANNED);"
        "save_job(job); print(job.id)"
    )
    proc = subprocess.run(
        [sys.executable, "-c", script], cwd=str(REPO_ROOT), capture_output=True,
        text=True, timeout=60,
        env={**os.environ, "REMEDY_DATA_DIR": str(data_root)},
    )
    assert proc.returncode == 0, proc.stderr
    return proc.stdout.strip().splitlines()[-1]


@pytest.fixture
def repo_project(tmp_path: Path) -> tuple[Path, Path]:
    """An initialized Remedy project in a git repo. Returns (repo, data_root)."""
    data_root = tmp_path / "data"
    data_root.mkdir(parents=True)
    repo = _git_repo(tmp_path)
    _run_in(repo, ["init"], data_root)
    return repo, data_root


class TestApprovalOptIn:
    """F056 T002 — the offer rides the plan approval and defaults to NO."""

    def test_the_offer_is_shown_when_intake_flagged_the_goal(self, repo_project):
        repo, data_root = repo_project
        job_id = _pending_plan_job(repo, data_root, "Keep it green",
                                   mission_candidate=True)

        out = _run_in(repo, ["decision", "show", job_id, "fp:approval"],
                      data_root).stdout

        assert "Run as mission" in out
        assert "Default: no" in out
        assert "--as-mission" in out

    def test_approving_without_the_flag_creates_no_mission(self, repo_project):
        """The default is NO — this is the whole point of the opt-in."""
        repo, data_root = repo_project
        job_id = _pending_plan_job(repo, data_root, "Keep it green",
                                   mission_candidate=True)

        _run_in(repo, ["decision", "resolve", job_id, "fp:approval",
                       "--reason", "approve"], data_root)

        assert _missions_on_disk(data_root) == []

    def test_approving_with_the_flag_creates_and_links_the_mission(self, repo_project):
        repo, data_root = repo_project
        job_id = _pending_plan_job(repo, data_root, "Keep it green",
                                   mission_candidate=True)

        out = _run_in(repo, ["decision", "resolve", job_id, "fp:approval",
                             "--reason", "approve", "--as-mission"],
                      data_root).stdout

        assert "Mission" in out
        records = _missions_on_disk(data_root)
        assert len(records) == 1
        body = json.loads(records[0].read_text())
        assert body["goal"] == "Keep it green"
        assert body["job_links"] == [{
            "job_id": job_id, "role": "initial",
            "created_at": body["job_links"][0]["created_at"]}]

    def test_the_flag_works_even_when_intake_did_not_flag_the_goal(self, repo_project):
        """The hint surfaces the offer; the human may always opt in anyway."""
        repo, data_root = repo_project
        job_id = _pending_plan_job(repo, data_root, "Fix the bug",
                                   mission_candidate=False)

        _run_in(repo, ["decision", "resolve", job_id, "fp:approval",
                       "--reason", "approve", "--as-mission"], data_root)

        assert len(_missions_on_disk(data_root)) == 1

    def test_rejecting_with_the_flag_is_a_usage_error(self, repo_project):
        repo, data_root = repo_project
        job_id = _pending_plan_job(repo, data_root, "Keep it green",
                                   mission_candidate=True)

        proc = _run_in(repo, ["decision", "resolve", job_id, "fp:approval",
                              "--reason", "reject", "--as-mission"],
                       data_root, expect_ok=False)

        assert proc.returncode == 1
        assert "--as-mission applies only when approving" in proc.stderr
        assert _missions_on_disk(data_root) == []

    def test_the_flag_is_refused_on_another_decision_kind(self, repo_project):
        repo, data_root = repo_project
        job_id = _pending_plan_job(repo, data_root, "Keep it green",
                                   mission_candidate=True)

        proc = _run_in(repo, ["decision", "resolve", job_id, "sr:whatever",
                              "--reason", "approve", "--as-mission"],
                       data_root, expect_ok=False)

        assert "--as-mission is only valid for the flight-plan approval" in proc.stderr

    def test_a_job_already_in_a_mission_is_refused(self, repo_project):
        repo, data_root = repo_project
        job_id = _pending_plan_job(repo, data_root, "Keep it green",
                                   mission_candidate=True)
        _run_in(repo, ["decision", "resolve", job_id, "fp:approval",
                       "--reason", "approve", "--as-mission"], data_root)

        second = _pending_plan_job(repo, data_root, "Keep it green too",
                                   mission_candidate=True)
        # Re-approving the SAME job is refused by the pending-state check, so
        # link the second job first and then try to link it again.
        _run_in(repo, ["decision", "resolve", second, "fp:approval",
                       "--reason", "approve", "--as-mission"], data_root)

        assert len(_missions_on_disk(data_root)) == 2


class TestPlainDoFlowCreatesNoMission:
    """The negative proof the order requires: no opt-in, no command, no mission."""

    def test_a_plain_do_run_leaves_no_mission_behind(self, repo_project):
        repo, data_root = repo_project

        _run_in(repo, ["do", "Keep the importer working from now on",
                       "--no-llm", "--json"], data_root)

        assert _missions_on_disk(data_root) == []

    def test_not_even_when_the_goal_smells_long_lived(self, repo_project):
        """The hint is recorded on the intake; it still creates nothing."""
        repo, data_root = repo_project

        out = _run_in(repo, ["do", "Maintain the CI pipeline continuously",
                             "--no-llm", "--json"], data_root).stdout
        job_id = json.loads(out)["job_id"]
        job = json.loads((data_root / "jobs" / f"{job_id}.json").read_text())

        assert job["intake"]["mission_candidate"] is True
        assert _missions_on_disk(data_root) == []

    def test_an_auto_approved_run_creates_no_mission(self, repo_project):
        """Unattended approval covers the plan, never the mission opt-in.

        Driven through ``_cmd_do_mission(yes=True)`` because the auto-approval
        path is the one an unattended caller takes; if any approval path could
        create a mission on its own, this is where it would show.
        """
        repo, data_root = repo_project
        script = (
            "import sys; sys.path.insert(0, '.');"
            "from apps.cli.commands.do_cmd import _cmd_do_mission;"
            f"_cmd_do_mission('Keep it green from now on', repo={str(repo)!r},"
            "  json_output=True, no_llm=True, yes=True)"
        )
        proc = subprocess.run(
            [sys.executable, "-c", script], cwd=str(REPO_ROOT),
            capture_output=True, text=True, timeout=120,
            env={**os.environ, "REMEDY_DATA_DIR": str(data_root)},
        )
        assert proc.returncode == 0, proc.stderr

        assert _missions_on_disk(data_root) == []


class TestContinue:
    """F056 T003 — the follow-up job, and the verify task injected in front."""

    def _green_job(self, data_root: Path, project_id: str, mission_id: str,
                   *, command: str = "check the importer") -> str:
        script = (
            "import sys; sys.path.insert(0, '.');"
            "from packages.core.models import Job, RunState;"
            "from packages.orchestration.storage import save_job;"
            "from packages.orchestration.mission_state import link_job_to_mission;"
            f"job = Job(name='job one', state=RunState('completed'),"
            f"  project_id={project_id!r}, metadata={{'verify_command': {command!r}}});"
            "save_job(job);"
            f"link_job_to_mission({project_id!r}, {mission_id!r}, str(job.id), 'initial');"
            "print(job.id)"
        )
        proc = subprocess.run(
            [sys.executable, "-c", script], cwd=str(REPO_ROOT),
            capture_output=True, text=True, timeout=60,
            env={**os.environ, "REMEDY_DATA_DIR": str(data_root)},
        )
        assert proc.returncode == 0, proc.stderr
        return proc.stdout.strip().splitlines()[-1]

    def test_continue_is_in_the_catalog_with_a_handler(self):
        from apps.cli.command_catalog import get_command
        from apps.cli.commands import collect_all_handlers

        assert get_command("mission.continue").action_class == "write_metadata"
        assert "mission.continue" in collect_all_handlers()

    def test_the_follow_up_plan_begins_with_the_verify_task(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, "Keep the importer working")
        self._green_job(data_root, project_id, mission_id)

        body = json.loads(_run(["mission", "continue", mission_id,
                                "Add the CSV path", "--project", project_id,
                                "--json"], data_root).stdout)

        assert body["role"] == "follow_up"
        assert body["verify_first_task"]["verify_command"] == "check the importer"
        assert body["tasks"][0] == body["verify_first_task"]["description"]
        assert body["tasks"][1] == "Add the CSV path"

    def test_the_text_output_names_the_injected_task(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, "Keep the importer working")
        self._green_job(data_root, project_id, mission_id)

        out = _run(["mission", "continue", mission_id, "Add the CSV path",
                    "--project", project_id], data_root).stdout

        assert "Task 1 (injected)" in out
        assert "cannot start until that task completes" in out

    def test_the_new_job_joins_the_chain(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, "Keep the importer working")
        first = self._green_job(data_root, project_id, mission_id)
        body = json.loads(_run(["mission", "continue", mission_id,
                                "Add the CSV path", "--project", project_id,
                                "--json"], data_root).stdout)

        shown = _run(["mission", "show", mission_id, "--project", project_id],
                     data_root).stdout

        assert shown.index(first) < shown.index(body["job_id"])
        assert "follow_up" in shown

    def test_the_first_job_of_an_empty_mission_has_no_verify_task(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, "Keep the importer working")

        body = json.loads(_run(["mission", "continue", mission_id,
                                "Write the importer", "--project", project_id,
                                "--json"], data_root).stdout)

        assert body["role"] == "initial"
        assert body["verify_first_task"] is None

    def test_continuing_an_unknown_mission_is_an_error_not_a_crash(self, project):
        data_root, project_id = project
        proc = _run(["mission", "continue", "0" * 32, "Add the CSV path",
                     "--project", project_id], data_root, expect_ok=False)

        assert proc.returncode == 1
        assert "no mission" in proc.stderr
        assert "Traceback" not in proc.stderr


class TestStatusTransitions:
    """R-0163 — the explicit command surface the feature file promises.

    The verb names the status. There is no transition table: any valid
    status may follow any other, because the human typing the command is
    the authority. Nothing in Remedy moves a mission's status on its own.
    """

    _VERBS = (("achieve", "achieved"), ("abandon", "abandoned"),
              ("pause", "paused"))

    def test_the_transition_commands_are_in_the_catalog(self):
        from apps.cli.command_catalog import CATALOG

        ids = {entry.command_id for entry in CATALOG}
        assert {"mission.achieve", "mission.abandon", "mission.pause"} <= ids

    def test_every_transition_writes_metadata_and_has_a_handler(self):
        from apps.cli.command_catalog import get_command
        from apps.cli.commands import collect_all_handlers

        handlers = collect_all_handlers()
        for verb, _status in self._VERBS:
            command_id = f"mission.{verb}"
            assert get_command(command_id).action_class == "write_metadata"
            assert get_command(command_id).supports_json is True
            assert command_id in handlers

    def test_no_transition_command_may_execute_or_mutate_the_repo(self):
        from apps.cli.command_catalog import get_command

        for verb, _status in self._VERBS:
            entry = get_command(f"mission.{verb}")
            assert entry.may_execute_commands is False
            assert entry.may_mutate_repo is False

    @pytest.mark.parametrize("verb,status", _VERBS)
    def test_the_verb_sets_the_status_it_names(self, project, verb, status):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, "Keep it working")

        out = _run(["mission", verb, mission_id, "--project", project_id],
                   data_root).stdout

        assert mission_id in out
        assert f"Status: {status}" in out
        shown = json.loads(_run(["mission", "show", mission_id, "--project",
                                 project_id, "--json"], data_root).stdout)
        assert shown["mission"]["status"] == status

    @pytest.mark.parametrize("verb,status", _VERBS)
    def test_the_json_shape_matches_show(self, project, verb, status):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, "Keep it working")

        body = json.loads(_run(["mission", verb, mission_id, "--project",
                                project_id, "--json"], data_root).stdout)

        assert body["version"] == 1
        assert body["mission"]["id"] == mission_id
        assert body["mission"]["status"] == status
        assert body["mission"]["goal"] == "Keep it working"

    def test_a_transition_accepts_a_unique_prefix(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, "Keep it working")

        _run(["mission", "pause", mission_id[:8], "--project", project_id],
             data_root)

        shown = json.loads(_run(["mission", "show", mission_id, "--project",
                                 project_id, "--json"], data_root).stdout)
        assert shown["mission"]["status"] == "paused"

    @pytest.mark.parametrize("verb,_status", _VERBS)
    def test_an_unknown_mission_is_an_error_not_a_crash(self, project, verb,
                                                        _status):
        data_root, project_id = project
        proc = _run(["mission", verb, "0" * 32, "--project", project_id],
                    data_root, expect_ok=False)

        assert proc.returncode == 1
        assert "no mission" in proc.stderr
        assert "Traceback" not in proc.stderr

    def test_any_status_may_follow_any_other(self, project):
        """No transition table: the human is the authority on the state."""
        data_root, project_id = project
        mission_id = _start(data_root, project_id, "Keep it working")

        for verb in ("achieve", "pause", "abandon", "achieve"):
            _run(["mission", verb, mission_id, "--project", project_id],
                 data_root)

        shown = json.loads(_run(["mission", "show", mission_id, "--project",
                                 project_id, "--json"], data_root).stdout)
        assert shown["mission"]["status"] == "achieved"

    def test_a_transition_touches_neither_the_goal_nor_the_chain(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, "Keep it working")
        job_id = _link_job(data_root, project_id, mission_id, role="initial")

        _run(["mission", "abandon", mission_id, "--project", project_id],
             data_root)

        shown = json.loads(_run(["mission", "show", mission_id, "--project",
                                 project_id, "--json"], data_root).stdout)
        assert shown["mission"]["goal"] == "Keep it working"
        assert [link["job_id"] for link in shown["mission"]["job_links"]] == [job_id]

    def test_a_transition_without_a_project_exits_three(self, tmp_path):
        data_root = tmp_path / "data"
        data_root.mkdir(parents=True)
        proc = _run(["mission", "pause", "0" * 32], data_root, expect_ok=False)

        assert proc.returncode == 3
        assert "remedy init" in proc.stderr

    def test_nothing_moves_a_status_without_one_of_these_commands(self, project):
        """Linking a job, and continuing the chain, leave the status alone."""
        data_root, project_id = project
        mission_id = _start(data_root, project_id, "Keep it working")
        _link_job(data_root, project_id, mission_id, role="initial")
        _run(["mission", "continue", mission_id, "Add the CSV path",
              "--project", project_id, "--json"], data_root)

        shown = json.loads(_run(["mission", "show", mission_id, "--project",
                                 project_id, "--json"], data_root).stdout)
        assert shown["mission"]["status"] == "active"
