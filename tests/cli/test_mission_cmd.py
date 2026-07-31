"""CLI tests: `remedy mission start|list|show` (F056 T001).

The surface, not the store: the store's own behaviour is proven in
tests/orchestration/test_mission_state.py. What matters here is that the
catalog carries the commands, that scoping follows the F148 rules, that the
listing is honest about records it cannot read, and that `show` renders a
chain whose jobs are gone without crashing.

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
