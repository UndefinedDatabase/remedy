"""F304 T004 — the second gate test: a client's real paths, driven through the command line alone.

`docs/roadmap/features/T12_F304.md` closes T004 on one more gate test beside F295's, which
`tests/cli/test_machine_client_contract.py` keeps unchanged: an order file driven to `remedy job
apply <job> --approve --commit-with-history --push --json` against a local bare upstream, reading
the commit, the branch and the push from the answer; an order of two jobs driven to its end as a
program would, from the JSON answers alone; and one order file started twice. Its Goal & Done
also names two more paths, which the hardening stage found missing here (R-1185): an order that
names its project, started by a client that stands in no repository, and a result the client
declines. Every command runs through F295's `_remedy`, in this process with the environment a
child process would have, and with a stdin that fails the test on any read.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

from tests.cli.test_machine_client_contract import _GIT_IDENTITY, _digest_job, _remedy, _scratch_repo

#: An order a fake builder completes in one task step, with the cap an unattended order needs.
ORDER_FILE_TEXT = "---\nmax-cost-usd: 1\n---\nAdd a line saying hello to README.md\n"

#: The builder and reviewer the client names, here the fake ones.
ROLES = ("--builder-provider", "fake", "--reviewer-provider", "fake")

#: How the gate test starts every order: unattended, with its builder and reviewer.
UNATTENDED = ("--no-ui", "--yes", "--no-llm", *ROLES)


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=str(repo), check=True, capture_output=True, text=True,
                          env={**os.environ, **_GIT_IDENTITY}).stdout.strip()


def _client(tmp_path: Path) -> tuple[Path, Path, dict[str, str]]:
    """A scratch repository with one passing test, the order file beside it, and the environment
    the client runs in. The planner's one blocking criterion runs pytest over `tests`, so a
    repository without a test fails it and its push is refused, as a client's would be."""
    repo = _scratch_repo(tmp_path)
    (repo / "tests").mkdir()
    (repo / "tests" / "test_readme.py").write_text(
        "from pathlib import Path\n\n\ndef test_the_readme_exists():\n"
        "    assert Path('README.md').is_file()\n", encoding="utf-8")
    _git(repo, "add", "tests")
    _git(repo, "commit", "-q", "-m", "Add a test")
    order_file = tmp_path / "order.md"
    order_file.write_text(ORDER_FILE_TEXT, encoding="utf-8")
    env = {**os.environ, **_GIT_IDENTITY, "REMEDY_DATA_DIR": str(tmp_path / "data")}
    return repo, order_file, env


def _bare_upstream(repo: Path, tmp_path: Path) -> Path:
    """A bare repository under `tmp_path`, set as the upstream of the repository's branch."""
    upstream = tmp_path / "upstream.git"
    subprocess.run(["git", "init", "-q", "--bare", str(upstream)], check=True)
    _git(repo, "remote", "add", "origin", str(upstream))
    _git(repo, "push", "-q", "-u", "origin", "HEAD")
    return upstream


def test_an_order_file_is_merged_with_its_history_and_pushed_to_the_upstream(tmp_path):
    repo, order_file, env = _client(tmp_path)
    upstream = _bare_upstream(repo, tmp_path)
    branch = _git(repo, "symbolic-ref", "--short", "HEAD")

    code, done = _remedy(["do", str(order_file), *UNATTENDED], repo, env)
    assert code == 0, done
    [job_id] = done["job_ids"]

    code, applied = _remedy(["job", "apply", job_id, "--approve", "--commit-with-history",
                             "--push"], repo, env)
    assert code == 0, applied
    head = _git(repo, "rev-parse", "HEAD")
    assert (applied["ok"], applied["status"]) == (True, "applied")
    assert applied["commit_sha"] == applied["merge_commit"] == head
    assert applied["target_branch"] == branch
    assert (applied["pushed"], applied["push_remote"], applied["push_ref"]) == (
        True, "origin", f"refs/heads/{branch}")
    assert _git(upstream, "rev-parse", f"refs/heads/{branch}") == head

    code, status = _remedy(["status"], repo, env)
    assert _digest_job(status["client"], job_id)["waits_for_apply"] is False


def test_an_order_of_two_jobs_is_driven_to_its_end_from_the_answers_alone(tmp_path):
    repo, order_file, env = _client(tmp_path)

    code, done = _remedy(["do", str(order_file), *UNATTENDED, "--force-mission"], repo, env)
    assert code == 0, done
    first, second = done["job_ids"]
    assert done["waiting_job_ids"] == [second]

    # The first job ran. Each later job runs on what the one before it committed, so the client
    # applies and commits the first, runs the second with its own builder and reviewer, and
    # applies and commits that one too.
    code, applied_first = _remedy(["job", "apply", first, "--approve", "--commit-auto"], repo, env)
    assert (code, applied_first["status"]) == (0, "applied"), applied_first
    code, ran = _remedy(["job", "run", second, *ROLES], repo, env)
    assert (code, ran["status"]) == (0, "completed"), ran
    code, applied_second = _remedy(["job", "apply", second, "--approve", "--commit-auto"], repo, env)
    assert (code, applied_second["status"]) == (0, "applied"), applied_second

    assert _git(repo, "rev-parse", "HEAD") == applied_second["commit_sha"]
    assert _git(repo, "rev-parse", "HEAD~1") == applied_first["commit_sha"]
    code, status = _remedy(["status"], repo, env)
    digest = status["client"]
    assert [_digest_job(digest, job_id)["state"] for job_id in (first, second)] == [
        "completed", "completed"]
    assert digest["awaiting_apply"] == []


def test_one_order_file_started_twice_is_refused_naming_the_mission_that_runs_it(tmp_path):
    repo, order_file, env = _client(tmp_path)

    code, first = _remedy(["do", str(order_file), *UNATTENDED, "--plan-only"], repo, env)
    assert code == 0, first
    code, again = _remedy(["do", str(order_file), *UNATTENDED, "--plan-only"], repo, env)
    assert (code, again["ok"], again["error"]) == (2, False, "order_already_running"), again
    assert again["mission_id"] == first["mission_id"]
    code, status = _remedy(["status"], repo, env)
    assert [mission["mission_id"] for project in status["client"]["projects"]
            for mission in project["missions"]] == [first["mission_id"]]

    code, other = _remedy(["do", str(order_file), *UNATTENDED, "--plan-only", "--new-mission"],
                          repo, env)
    assert code == 0, other
    assert other["mission_id"] != first["mission_id"]


def _project_order(tmp_path: Path) -> tuple[Path, Path, Path, dict[str, str], dict]:
    """The client's repository registered as a project from a folder that is no repository, and
    the order file naming that project; the client stands in that folder from here on."""
    repo, order_file, env = _client(tmp_path)
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    code, registered = _remedy(["project", "register", "--repo", str(repo)], elsewhere, env)
    assert code == 0, registered
    order_file.write_text(ORDER_FILE_TEXT.replace(
        "---\n", f"---\nproject: {registered['slug']}\n", 1), encoding="utf-8")
    return repo, elsewhere, order_file, env, registered


def test_an_order_naming_its_project_runs_in_that_projects_repository_wherever_the_client_stands(
        tmp_path):
    repo, elsewhere, order_file, env, registered = _project_order(tmp_path)

    code, done = _remedy(["do", str(order_file), *UNATTENDED], elsewhere, env)
    assert code == 0, done
    [job_id] = done["job_ids"]

    # The answer names the project's repository as the place to apply, and the job records it.
    assert f"remedy job apply {job_id} --repo {registered['repo_path']} --approve" in done["next"]
    code, shown = _remedy(["job", "show", job_id], elsewhere, env)
    assert (code, shown["repo_path"], shown["project_id"]) == (
        0, registered["repo_path"], registered["project_id"])
    code, applied = _remedy(["job", "apply", job_id, "--repo", registered["repo_path"],
                             "--approve"], elsewhere, env)
    assert (code, applied["status"]) == (0, "applied"), applied
    assert (repo / "docs" / "README.md").is_file()
    assert list(elsewhere.iterdir()) == []


def test_a_client_declines_a_completed_result_and_it_waits_for_nothing(tmp_path):
    repo, elsewhere, order_file, env, registered = _project_order(tmp_path)
    code, done = _remedy(["do", str(order_file), *UNATTENDED], elsewhere, env)
    assert code == 0, done
    [job_id] = done["job_ids"]
    code, status = _remedy(["status"], elsewhere, env)
    assert status["client"]["awaiting_apply"] == [job_id]

    code, declined = _remedy(["job", "decline", job_id, "--reason", "not wanted"], elsewhere, env)

    assert (code, declined["ok"], declined["reason"]) == (0, True, "not wanted"), declined
    code, status = _remedy(["status"], elsewhere, env)
    job = _digest_job(status["client"], job_id)
    assert (job["state"], job["waits_for_apply"]) == ("completed", False)
    assert status["client"]["awaiting_apply"] == []
    code, ownership = _remedy(["job", "ownership", job_id], elsewhere, env)
    assert [(entry["action"], entry["text"]) for entry in ownership["entries"]] == [
        ("result_declined", "not wanted")]
    # Nothing was applied: the repository is as the client left it.
    assert not (repo / "docs" / "README.md").exists()
