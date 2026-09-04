"""CLI tests: `remedy queue add|list|rm` (F048 T003a).

The surface, not the store: the store's own behaviour is proven in
tests/orchestration/test_job_queue.py. What matters here is that the catalog carries the
commands, that scoping follows the F148 rules, that the listing is honest about entries
it cannot read, and that `rm` refuses a claimed entry and SAYS WHO holds it.

Every test runs the real grouped CLI in a subprocess against a tmp_path data root, so the
assertions are made on what an operator actually sees.
"""
from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
from datetime import datetime, timedelta, timezone
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


@pytest.fixture
def project(tmp_path: Path) -> tuple[Path, str]:
    """A registered project in an isolated data root. Returns (data_root, project_id)."""
    data_root = tmp_path / "data"
    data_root.mkdir(parents=True)
    proc = subprocess.run(
        [sys.executable, "-c",
         "import sys; sys.path.insert(0, '.');"
         "from packages.orchestration.project_registry import RemyProject, save_project;"
         "p = RemyProject(name='Queue Test', slug='queue-test'); save_project(p); print(p.id)"],
        cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=60,
        env={**os.environ, "REMEDY_DATA_DIR": str(data_root)},
    )
    assert proc.returncode == 0, proc.stderr
    return data_root, proc.stdout.strip().splitlines()[-1]


class TestCatalog:
    def test_the_queue_commands_are_in_the_catalog(self):
        from apps.cli.command_catalog import CATALOG

        ids = {entry.command_id for entry in CATALOG}
        assert {"queue.add", "queue.list", "queue.rm"} <= ids

    def test_list_is_read_only_and_add_writes_metadata(self):
        from apps.cli.command_catalog import get_command

        assert get_command("queue.list").action_class == "read_only"
        assert get_command("queue.add").action_class == "write_metadata"
        assert get_command("queue.rm").action_class == "write_metadata"

    def test_every_queue_command_has_a_handler(self):
        from apps.cli.commands import collect_all_handlers

        handlers = collect_all_handlers()
        assert {"queue.add", "queue.list", "queue.rm"} <= set(handlers)

    def test_no_queue_command_may_execute_or_mutate_the_repo(self):
        from apps.cli.command_catalog import get_commands_for_group

        for entry in get_commands_for_group("queue"):
            assert entry.may_execute_commands is False
            assert entry.may_mutate_repo is False

    def test_list_has_json_flag(self):
        from apps.cli.command_catalog import get_command
        assert get_command("queue.list").supports_json is True


class TestAdd:
    def test_add_prints_the_new_entry_id(self, project):
        data_root, project_id = project
        proc = _run(["queue", "add", "write the README", "--project", project_id], data_root)

        entry_id = proc.stdout.strip()
        assert len(entry_id) == 32
        listing = _run(["queue", "list", "--project", project_id], data_root).stdout
        assert entry_id[:12] in listing
        assert "write the README" in listing

    def test_priority_is_recorded_and_orders_the_listing(self, project):
        data_root, project_id = project
        _run(["queue", "add", "low goal", "--project", project_id], data_root)
        _run(["queue", "add", "high goal", "--prio", "9", "--project", project_id], data_root)

        lines = [ln for ln in _run(["queue", "list", "--project", project_id],
                                   data_root).stdout.splitlines() if ln.strip()]
        assert "high goal" in lines[0]
        assert "low goal" in lines[1]
        assert "prio 9" in lines[0]

    def test_a_non_integer_priority_is_a_usage_error(self, project):
        data_root, project_id = project
        proc = _run(["queue", "add", "goal", "--prio", "soon", "--project", project_id],
                    data_root, expect_ok=False)

        assert proc.returncode == 2
        assert "--prio must be an integer" in proc.stderr

    def test_an_existing_file_is_enqueued_as_a_goal_path(self, project, tmp_path):
        data_root, project_id = project
        goal_file = tmp_path / "goal.md"
        goal_file.write_text("Ship the queue.\n", encoding="utf-8")

        _run(["queue", "add", str(goal_file), "--project", project_id], data_root)

        listing = _run(["queue", "list", "--project", project_id], data_root).stdout
        assert f"@{goal_file}"[:60] in listing

    def test_a_sentence_stays_goal_text_even_with_a_slash(self, project):
        data_root, project_id = project
        _run(["queue", "add", "fix the a/b split", "--project", project_id], data_root)

        listing = _run(["queue", "list", "--project", project_id], data_root).stdout
        assert "fix the a/b split" in listing
        assert "@" not in listing

    def test_add_without_a_project_exits_three(self, tmp_path):
        data_root = tmp_path / "data"
        data_root.mkdir(parents=True)
        proc = _run(["queue", "add", "orphan goal"], data_root, expect_ok=False)

        assert proc.returncode == 3
        assert "no project found" in proc.stderr

    def test_duplicate_goal_text_makes_two_entries(self, project):
        data_root, project_id = project
        first = _run(["queue", "add", "same goal", "--project", project_id], data_root).stdout.strip()
        second = _run(["queue", "add", "same goal", "--project", project_id], data_root).stdout.strip()

        assert first != second
        listing = _run(["queue", "list", "--project", project_id], data_root).stdout
        assert listing.count("same goal") == 2


class TestList:
    def test_an_empty_queue_says_so(self, project):
        data_root, project_id = project
        proc = _run(["queue", "list", "--project", project_id], data_root)

        assert "No queue entries found." in proc.stdout

    def test_a_claimed_entry_shows_its_owner(self, project):
        data_root, project_id = project
        _run(["queue", "add", "claimed goal", "--project", project_id], data_root)
        _claim_one(data_root, project_id, "host-x#99")

        listing = _run(["queue", "list", "--project", project_id], data_root).stdout
        assert "claimed" in listing
        assert "host-x#99" in listing

    def test_entries_are_scoped_to_their_project(self, project, tmp_path):
        data_root, project_id = project
        other_id = _make_second_project(data_root, tmp_path)
        _run(["queue", "add", "mine", "--project", project_id], data_root)
        _run(["queue", "add", "theirs", "--project", other_id], data_root)

        mine = _run(["queue", "list", "--project", project_id], data_root).stdout
        assert "mine" in mine
        assert "theirs" not in mine

    def test_all_projects_widens_the_listing_and_labels_it(self, project, tmp_path):
        data_root, project_id = project
        other_id = _make_second_project(data_root, tmp_path)
        _run(["queue", "add", "mine", "--project", project_id], data_root)
        _run(["queue", "add", "theirs", "--project", other_id], data_root)

        listing = _run(["queue", "list", "--all-projects"], data_root).stdout
        assert "mine" in listing
        assert "theirs" in listing
        assert f"(project: {project_id[:8]})" in listing

    def test_a_corrupt_entry_is_counted_not_hidden(self, project):
        data_root, project_id = project
        _run(["queue", "add", "good goal", "--project", project_id], data_root)
        broken = _run(["queue", "add", "doomed goal", "--project", project_id], data_root).stdout.strip()
        (data_root / "queue" / project_id / f"{broken}.json").write_text("{ nope", encoding="utf-8")

        proc = _run(["queue", "list", "--project", project_id], data_root)
        assert "good goal" in proc.stdout
        assert "doomed goal" not in proc.stdout
        assert "1 unreadable queue file(s) skipped" in proc.stderr

    def test_json_has_created_at_and_goal(self, project):
        data_root, project_id = project
        _run(["queue", "add", "json goal", "--project", project_id], data_root)

        proc = _run(["queue", "list", "--project", project_id, "--json"], data_root)
        data = json.loads(proc.stdout)
        assert data["version"] == 1
        assert data["entries"][0]["created_at"]
        assert data["entries"][0]["goal"] == "json goal"

    def test_sort_created_at_overrides_the_priority_default(self, project):
        data_root, project_id = project
        _run(["queue", "add", "first goal", "--project", project_id], data_root)
        _run(["queue", "add", "second goal", "--prio", "9", "--project", project_id], data_root)

        lines = [ln for ln in _run(
            ["queue", "list", "--project", project_id, "--sort", "created_at"], data_root,
        ).stdout.splitlines() if ln.strip()]
        assert "first goal" in lines[0]
        assert "second goal" in lines[1]

    def test_unknown_sort_field_exits_nonzero_naming_valid_fields(self, project):
        data_root, project_id = project
        _run(["queue", "add", "a goal", "--project", project_id], data_root)

        proc = _run(["queue", "list", "--project", project_id, "--sort", "bogus"], data_root,
                    expect_ok=False)
        assert proc.returncode == 1
        assert "created_at" in proc.stderr


class TestRm:
    def test_rm_removes_an_unclaimed_entry(self, project):
        data_root, project_id = project
        entry_id = _run(["queue", "add", "regrettable goal", "--project", project_id],
                        data_root).stdout.strip()

        proc = _run(["queue", "rm", entry_id, "--project", project_id], data_root)
        assert f"Removed {entry_id}" in proc.stdout

        listing = _run(["queue", "list", "--project", project_id], data_root).stdout
        assert "No queue entries found." in listing

    def test_a_unique_prefix_is_enough(self, project):
        data_root, project_id = project
        entry_id = _run(["queue", "add", "prefixed goal", "--project", project_id],
                        data_root).stdout.strip()

        proc = _run(["queue", "rm", entry_id[:12], "--project", project_id], data_root)
        assert f"Removed {entry_id}" in proc.stdout

    def test_rm_refuses_a_claimed_entry_and_names_the_owner(self, project):
        data_root, project_id = project
        entry_id = _run(["queue", "add", "busy goal", "--project", project_id],
                        data_root).stdout.strip()
        _claim_one(data_root, project_id, "host-y#4242")

        proc = _run(["queue", "rm", entry_id, "--project", project_id],
                    data_root, expect_ok=False)

        assert proc.returncode == 1
        assert "host-y#4242" in proc.stderr
        assert "claimed" in proc.stderr
        # And it is still there — a refusal that deleted anything would be worse than none.
        assert entry_id[:12] in _run(["queue", "list", "--project", project_id], data_root).stdout

    def test_rm_of_an_unknown_entry_is_an_error(self, project):
        data_root, project_id = project
        _run(["queue", "add", "something else", "--project", project_id], data_root)

        proc = _run(["queue", "rm", "deadbeef", "--project", project_id],
                    data_root, expect_ok=False)

        assert proc.returncode == 1
        assert "not found" in proc.stderr

    def test_rm_against_an_empty_queue_says_there_is_no_queue(self, project):
        data_root, project_id = project
        proc = _run(["queue", "rm", "deadbeef", "--project", project_id],
                    data_root, expect_ok=False)

        assert proc.returncode == 1
        assert "no queue for project" in proc.stderr


class TestReclaim:
    def test_reclaim_refuses_a_live_owner_and_explains_both_gates(self, project):
        data_root, project_id = project
        entry_id = _run(["queue", "add", "held goal", "--project", project_id],
                        data_root).stdout.strip()
        _claim_one(data_root, project_id, f"{socket.gethostname()}#{os.getpid()}")

        proc = _run(["queue", "reclaim", entry_id, "--project", project_id],
                    data_root, expect_ok=False)

        assert proc.returncode == 1
        assert str(os.getpid()) in proc.stderr
        assert "verifiably gone" in proc.stderr
        assert "never takes a claim away on a timer alone" in proc.stderr
        listing = _run(["queue", "list", "--project", project_id], data_root).stdout
        assert "claimed" in listing

    def test_reclaim_returns_a_dead_owners_stale_claim_to_the_queue(self, project):
        data_root, project_id = project
        entry_id = _run(["queue", "add", "abandoned goal", "--project", project_id],
                        data_root).stdout.strip()
        _claim_one(data_root, project_id, f"{socket.gethostname()}#{_dead_pid()}")
        _backdate_claim(data_root, project_id, entry_id, minutes=600)

        proc = _run(["queue", "reclaim", entry_id, "--project", project_id], data_root)

        assert f"Reclaimed {entry_id}" in proc.stdout
        listing = _run(["queue", "list", "--project", project_id], data_root).stdout
        assert "queued" in listing
        assert "claimed" not in listing

    def test_reclaim_is_in_the_catalog_with_a_handler(self):
        from apps.cli.command_catalog import get_command
        from apps.cli.commands import collect_all_handlers

        assert get_command("queue.reclaim").action_class == "write_metadata"
        assert "queue.reclaim" in collect_all_handlers()


# ---------------------------------------------------------------------------
# Helpers that drive the store directly, in their own process
# ---------------------------------------------------------------------------


def _dead_pid() -> int:
    """A pid that has certainly exited: started, then reaped."""
    proc = subprocess.Popen([sys.executable, "-c", "pass"])
    proc.communicate(timeout=60)
    return proc.pid


def _backdate_claim(data_root: Path, project_id: str, entry_id: str, *, minutes: int) -> None:
    """Age a claim on disk, so the TTL gate can be exercised without waiting an hour."""
    path = data_root / "queue" / project_id / f"{entry_id}.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    stamp = datetime.now(timezone.utc) - timedelta(minutes=minutes)
    payload["claimed_at"] = stamp.isoformat()
    path.write_text(json.dumps(payload), encoding="utf-8")


def _claim_one(data_root: Path, project_id: str, consumer: str) -> None:
    proc = subprocess.run(
        [sys.executable, "-c",
         "import sys; sys.path.insert(0, '.');"
         "from packages.orchestration.job_queue import claim_next;"
         f"e = claim_next({project_id!r}, {consumer!r});"
         "print(e.id if e else 'NONE')"],
        cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=60,
        env={**os.environ, "REMEDY_DATA_DIR": str(data_root)},
    )
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip() != "NONE", "nothing was claimable"


def _make_second_project(data_root: Path, tmp_path: Path) -> str:
    proc = subprocess.run(
        [sys.executable, "-c",
         "import sys; sys.path.insert(0, '.');"
         "from packages.orchestration.project_registry import RemyProject, save_project;"
         "p = RemyProject(name='Other', slug='other'); save_project(p); print(p.id)"],
        cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=60,
        env={**os.environ, "REMEDY_DATA_DIR": str(data_root)},
    )
    assert proc.returncode == 0, proc.stderr
    return proc.stdout.strip().splitlines()[-1]
