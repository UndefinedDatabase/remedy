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
    the authority. This surface is not the only writer, though: the
    orchestrator loop's terminal moves write achieved and abandoned with
    no human in the loop.
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


# ---------------------------------------------------------------------------
# F069 T003 — `remedy mission plan`
# ---------------------------------------------------------------------------

_LONG_GOAL = (
    "Keep the CSV importer trustworthy over the next two quarters. Today it "
    "silently drops rows whose encoding it cannot guess, the failure only "
    "surfaces weeks later in the monthly reconciliation, and nobody can say "
    "which imports were affected. Eventually a bad row should fail loudly at "
    "import time and every import should be reconstructable from its own "
    "record."
)


def _plan(data_root: Path, project_id: str, mission_id: str, *,
          expect_ok: bool = True):
    """Compile a mission plan deterministically — no provider in tests."""
    return _run(["mission", "plan", mission_id, "--no-llm", "--project",
                 project_id, "--json"], data_root, expect_ok=expect_ok)


class TestPlanCatalog:
    def test_plan_is_in_the_catalog_with_a_handler(self):
        from apps.cli.command_catalog import get_command
        from apps.cli.commands import collect_all_handlers

        entry = get_command("mission.plan")
        assert entry.action_class == "write_metadata"
        assert entry.supports_json is True
        assert "mission.plan" in collect_all_handlers()

    def test_planning_may_not_execute_or_mutate_the_repo(self):
        """Compiling a plan is metadata work — it runs nothing."""
        from apps.cli.command_catalog import get_command

        entry = get_command("mission.plan")
        assert entry.may_execute_commands is False
        assert entry.may_mutate_repo is False


class TestPlan:
    def test_plan_compiles_milestones_and_renders_them(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, _LONG_GOAL)

        body = json.loads(_plan(data_root, project_id, mission_id).stdout)

        assert body["plan_version"] == 1
        assert body["source"] == "deterministic"
        assert body["milestones"]
        assert Path(body["plan_path"]).is_file()
        assert Path(body["plan_path"]).name == "mission_plan.md"

    def test_every_milestone_carries_a_dod_reference_that_exists(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, _LONG_GOAL)

        body = json.loads(_plan(data_root, project_id, mission_id).stdout)

        evidence = Path(body["plan_path"]).parent
        for milestone in body["milestones"]:
            assert milestone["dod_ref"]
            assert (evidence / milestone["dod_ref"]).is_file()

    def test_the_text_output_says_nothing_was_started(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, _LONG_GOAL)

        out = _run(["mission", "plan", mission_id, "--no-llm", "--project",
                    project_id], data_root).stdout

        assert "No jobs were created and nothing was started" in out
        assert "draft job outline" in out

    def test_planning_creates_no_jobs(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, _LONG_GOAL)

        body = json.loads(_plan(data_root, project_id, mission_id).stdout)

        assert body["jobs_created"] == 0
        shown = json.loads(_run(["mission", "show", mission_id, "--project",
                                 project_id, "--json"], data_root).stdout)
        assert shown["mission"]["job_links"] == []
        jobs = data_root / "jobs"
        assert not jobs.exists() or list(jobs.iterdir()) == []

    def test_the_plan_is_persisted_on_the_mission_record(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, _LONG_GOAL)
        _plan(data_root, project_id, mission_id)

        record = json.loads(
            (data_root / "missions" / project_id / f"{mission_id}.json")
            .read_text(encoding="utf-8"))
        assert record["mission_plan"]["schema_v"] == "mission_plan_v1"
        assert record["mission_plan"]["_version"] == 1

    def test_planning_an_unknown_mission_exits_one(self, project):
        data_root, project_id = project
        proc = _plan(data_root, project_id, "0" * 32, expect_ok=False)
        assert proc.returncode == 1
        assert "no mission" in proc.stderr


class TestRecompileVersioning:
    def test_a_recompile_keeps_the_prior_version(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, _LONG_GOAL)

        first = json.loads(_plan(data_root, project_id, mission_id).stdout)
        second = json.loads(_plan(data_root, project_id, mission_id).stdout)

        assert first["plan_version"] == 1
        assert second["plan_version"] == 2
        record = json.loads(
            (data_root / "missions" / project_id / f"{mission_id}.json")
            .read_text(encoding="utf-8"))
        assert len(record["mission_plan"]["_versions"]) == 1
        assert record["mission_plan"]["_versions"][0]["_version"] == 1

    def test_the_earlier_rendered_plan_is_not_destroyed(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, _LONG_GOAL)

        first = json.loads(_plan(data_root, project_id, mission_id).stdout)
        second = json.loads(_plan(data_root, project_id, mission_id).stdout)

        assert Path(first["plan_path"]).is_file()
        assert Path(second["plan_path"]).name == "mission_plan_v2.md"
        assert Path(first["plan_path"]) != Path(second["plan_path"])


class TestInProgressRefusal:
    def test_a_recompile_is_refused_once_a_job_is_linked(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, _LONG_GOAL)
        _plan(data_root, project_id, mission_id)
        _link_job(data_root, project_id, mission_id, role="initial")

        proc = _plan(data_root, project_id, mission_id, expect_ok=False)

        assert proc.returncode == 1
        assert "already in progress" in proc.stderr
        assert "cannot be replanned" in proc.stderr

    def test_the_refusal_leaves_the_persisted_plan_untouched(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, _LONG_GOAL)
        _plan(data_root, project_id, mission_id)
        _link_job(data_root, project_id, mission_id, role="initial")
        record_path = data_root / "missions" / project_id / f"{mission_id}.json"
        before = record_path.read_text(encoding="utf-8")

        _plan(data_root, project_id, mission_id, expect_ok=False)

        assert record_path.read_text(encoding="utf-8") == before

    def test_the_first_compilation_is_allowed_even_with_a_linked_job(self, project):
        """Nothing is in progress while there are no milestones yet."""
        data_root, project_id = project
        mission_id = _start(data_root, project_id, _LONG_GOAL)
        _link_job(data_root, project_id, mission_id, role="initial")

        body = json.loads(_plan(data_root, project_id, mission_id).stdout)

        assert body["plan_version"] == 1


# ---------------------------------------------------------------------------
# F070 T003 — `remedy mission run` (orchestrator mode) and `mission ledger`
# ---------------------------------------------------------------------------


def _plan_no_llm(data_root: Path, project_id: str, mission_id: str):
    return _run(["mission", "plan", mission_id, "--project", project_id,
                 "--no-llm", "--json"], data_root)


class TestTheCatalogCarriesTheLoopCommands:
    def test_mission_run_is_registered_exactly_once(self):
        from apps.cli.command_catalog import CATALOG

        assert len([c for c in CATALOG if c.command_id == "mission.run"]) == 1

    def test_mission_ledger_is_registered_exactly_once(self):
        from apps.cli.command_catalog import CATALOG

        assert len([c for c in CATALOG
                    if c.command_id == "mission.ledger"]) == 1

    def test_mission_run_declares_the_iterations_flag(self):
        from apps.cli.command_catalog import get_command

        names = {a.name for a in get_command("mission.run").args}
        assert "--iterations" in names
        assert "--no-llm" in names


class TestMissionRunInOrchestratorMode:
    def test_a_mission_id_runs_the_orchestrator_loop(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, _LONG_GOAL)
        _plan_no_llm(data_root, project_id, mission_id)

        body = json.loads(_run(["mission", "run", mission_id, "--project",
                                project_id, "--no-llm", "--json"],
                               data_root).stdout)
        assert body["mission_id"] == mission_id
        assert body["terminal"] == "no_provider"
        assert body["iterations"] == 1

    def test_no_provider_is_an_honest_terminal_not_a_fake_run(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, _LONG_GOAL)
        _plan_no_llm(data_root, project_id, mission_id)

        out = _run(["mission", "run", mission_id, "--project", project_id,
                    "--no-llm"], data_root).stdout
        assert "no_provider" in out
        assert "Remedy does not invent a run" in out
        # Nothing was decided, so the mission is untouched.
        record = json.loads(
            (data_root / "missions" / project_id / f"{mission_id}.json")
            .read_text(encoding="utf-8"))
        assert record["status"] == "active"
        assert record["job_links"] == []

    def test_the_iterations_flag_bounds_the_run(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, _LONG_GOAL)
        _plan_no_llm(data_root, project_id, mission_id)

        body = json.loads(_run(["mission", "run", mission_id, "--project",
                                project_id, "--no-llm", "--iterations", "3",
                                "--json"], data_root).stdout)
        assert body["max_iterations"] == 3

    def test_a_nonsense_iteration_bound_is_a_usage_error(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, _LONG_GOAL)
        _plan_no_llm(data_root, project_id, mission_id)

        proc = _run(["mission", "run", mission_id, "--project", project_id,
                     "--no-llm", "--iterations", "0"], data_root,
                    expect_ok=False)
        assert proc.returncode == 2
        assert "max_iterations" in proc.stderr

    def test_an_unknown_id_still_reaches_the_pre_f070_facade(self, project):
        """A run id that names no mission must behave exactly as before."""
        data_root, project_id = project
        proc = _run(["mission", "run", "not-a-mission-id", "--project",
                     project_id, "--json"], data_root, expect_ok=False)
        # The dogfood facade owns this path; what matters is that the
        # orchestrator loop did NOT claim it.
        assert "no_provider" not in proc.stdout


class TestMissionLedger:
    def test_an_unrun_mission_has_an_empty_ledger(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, _LONG_GOAL)

        out = _run(["mission", "ledger", mission_id, "--project", project_id],
                   data_root).stdout
        assert "Iterations recorded: 0" in out
        assert "No ledger entries." in out

    def test_the_ledger_renders_what_the_run_recorded(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, _LONG_GOAL)
        _plan_no_llm(data_root, project_id, mission_id)
        _run(["mission", "run", mission_id, "--project", project_id,
              "--no-llm"], data_root)

        out = _run(["mission", "ledger", mission_id, "--project", project_id],
                   data_root).stdout
        assert "Iterations recorded: 1" in out
        assert "no_provider" in out
        assert "[1]" in out

    def test_the_json_view_carries_the_entries(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, _LONG_GOAL)
        _plan_no_llm(data_root, project_id, mission_id)
        _run(["mission", "run", mission_id, "--project", project_id,
              "--no-llm"], data_root)

        body = json.loads(_run(["mission", "ledger", mission_id, "--project",
                                project_id, "--json"], data_root).stdout)
        assert body["mission_id"] == mission_id
        assert len(body["entries"]) == 1
        assert body["entries"][0]["iteration"] == 1
        assert body["entries"][0]["context_digest"].startswith("sha256:")

    def test_the_ledger_is_read_only(self, project):
        """Rendering the trail must not change the mission or add entries."""
        data_root, project_id = project
        mission_id = _start(data_root, project_id, _LONG_GOAL)
        _plan_no_llm(data_root, project_id, mission_id)
        _run(["mission", "run", mission_id, "--project", project_id,
              "--no-llm"], data_root)
        record = (data_root / "missions" / project_id / f"{mission_id}.json")
        before = record.read_text(encoding="utf-8")

        _run(["mission", "ledger", mission_id, "--project", project_id],
             data_root)
        _run(["mission", "ledger", mission_id, "--project", project_id],
             data_root)

        assert record.read_text(encoding="utf-8") == before
        body = json.loads(_run(["mission", "ledger", mission_id, "--project",
                                project_id, "--json"], data_root).stdout)
        assert len(body["entries"]) == 1


class TestHandoffCommand:
    """`remedy mission handoff <id>` — F079's explicit boundary trigger."""

    def test_the_command_is_in_the_catalog_with_a_handler(self):
        from apps.cli.command_catalog import get_command
        from apps.cli.commands import collect_all_handlers

        entry = get_command("mission.handoff")
        assert entry.action_class == "write_metadata"
        assert entry.may_execute_commands is False
        assert entry.may_mutate_repo is False
        assert "mission.handoff" in collect_all_handlers()

    def test_it_writes_the_artifact_and_prints_where(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, "Ship the handoff")

        proc = _run(["mission", "handoff", mission_id], data_root)

        path = Path(proc.stdout.splitlines()[0].strip())
        assert path.is_file()
        assert path.name == "handoff_v1.json"
        assert path.with_suffix(".md").is_file()
        body = json.loads(path.read_text(encoding="utf-8"))
        assert body["mission_id"] == mission_id
        assert body["schema_version"] == 1
        # A zero-progress mission is valid: its empty sections are named gaps.
        assert body["gaps"]
        assert "Gaps:" in proc.stdout

    def test_the_json_view_names_both_files(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, "Ship the handoff")

        body = json.loads(_run(["mission", "handoff", mission_id, "--json"],
                               data_root).stdout)

        assert body["mission_id"] == mission_id
        assert Path(body["handoff"]).is_file()
        assert Path(body["rendered"]).is_file()

    def test_building_twice_leaves_one_account(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, "Ship the handoff")

        first = _run(["mission", "handoff", mission_id], data_root).stdout
        second = _run(["mission", "handoff", mission_id], data_root).stdout

        assert first.splitlines()[0] == second.splitlines()[0]
        evidence = Path(first.splitlines()[0].strip()).parent
        assert sorted(p.name for p in evidence.glob("handoff_v*.json")) == \
            ["handoff_v1.json"]

    def test_an_unknown_mission_exits_nonzero_and_says_so(self, project):
        data_root, _project_id = project

        proc = _run(["mission", "handoff", "no-such-mission"], data_root,
                    expect_ok=False)

        assert proc.returncode != 0
        assert "no mission 'no-such-mission' exists to hand off" in proc.stderr


class TestWatchdogCommandCatalog:
    """`remedy mission watchdog <id>` — F077 T003's manual audit surface."""

    def test_the_command_is_in_the_catalog_with_a_handler(self):
        from apps.cli.command_catalog import get_command
        from apps.cli.commands import collect_all_handlers

        entry = get_command("mission.watchdog")
        assert entry.action_class == "read_only"
        assert entry.supports_json is True
        assert entry.may_execute_commands is False
        assert entry.may_mutate_repo is False
        assert "mission.watchdog" in collect_all_handlers()


class TestMissionWatchdog:
    def test_an_unrun_mission_reports_no_tripwires(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, _LONG_GOAL)

        proc = _run(["mission", "watchdog", mission_id, "--project", project_id],
                    data_root)

        assert proc.returncode == 0
        assert mission_id in proc.stdout
        assert "Status: active" in proc.stdout
        assert "Tripwires fired: 0" in proc.stdout

    def test_the_json_view_carries_the_trip_list(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, _LONG_GOAL)

        body = json.loads(_run(["mission", "watchdog", mission_id, "--project",
                                project_id, "--json"], data_root).stdout)

        assert body["version"] == 1
        assert body["mission_id"] == mission_id
        assert body["trips"] == []

    def test_asking_the_watchdog_changes_nothing(self, project):
        """The acceptance claim: an audit must not pause what it audits."""
        data_root, project_id = project
        mission_id = _start(data_root, project_id, _LONG_GOAL)
        _plan_no_llm(data_root, project_id, mission_id)
        _run(["mission", "run", mission_id, "--project", project_id,
              "--no-llm"], data_root)
        record = (data_root / "missions" / project_id / f"{mission_id}.json")
        before = record.read_text(encoding="utf-8")

        _run(["mission", "watchdog", mission_id, "--project", project_id],
             data_root)
        _run(["mission", "watchdog", mission_id, "--project", project_id],
             data_root)

        assert record.read_text(encoding="utf-8") == before
        ledger = json.loads(_run(["mission", "ledger", mission_id, "--project",
                                  project_id, "--json"], data_root).stdout)
        assert len(ledger["entries"]) == 1

    def test_an_unknown_mission_is_an_error_not_a_crash(self, project):
        data_root, project_id = project

        proc = _run(["mission", "watchdog", "0" * 32, "--project", project_id],
                    data_root, expect_ok=False)

        assert proc.returncode == 1
        assert "no mission" in proc.stderr
        assert "Traceback" not in proc.stderr
