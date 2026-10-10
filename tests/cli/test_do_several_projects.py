"""F205, DECISION F205 D4 — one order names several projects; `remedy do` plans one job per repository.

The projects `a` and `b` are registered by `remedy init`, each in its own repository, and the order
file's header names both, `a` first. The walk plans one job in each project's repository under one
mission that spans both and lives in `a`; under a commit flag each job is applied and committed in
its own repository, and `--push` pushes each repository once. `--project`, `--repo`, a project
without a repository, an unknown project and a force flag are refused.

In-process through `apps.cli.grouped.main`, with the data root under `tmp_path`, the fake builder
and reviewer and `--no-ui` always, as `tests/cli/test_do_project_repo.py` drives it, whose
fixtures this file uses; a tripwire fails the test if any model-call factory is reached, and each
remote is a bare repository under `tmp_path` whose update hook logs each ref update.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from apps.cli.grouped import main
from tests.cli.test_do_project_repo import (  # noqa: F401 — fixtures used by name
    FAKE_ROLES,
    _git,
    _no_mission_and_no_job,
    _refused,
    _repo_state,
    no_model_call,
    projects,
)


def _order(folder: Path, *slugs: str) -> Path:
    path = folder / "order.md"
    header = "".join(f"project: {slug}\n" for slug in slugs)
    path.write_text(f"---\n{header}max-cost-usd: 1\n---\nWrite a CONTRIBUTING.md\n")
    return path


def _do_json(capsys, order: Path, *extra: str) -> dict:
    main(["do", str(order), "--no-llm", "--no-ui", "--json", *FAKE_ROLES, *extra])
    return json.loads(capsys.readouterr().out)


def _head(repo: Path) -> str:
    return _git(repo, "rev-parse", "HEAD").strip()


def _bare_upstream(repo: Path) -> None:
    """A bare remote beside *repo*, its branch's upstream; its update hook logs each ref update."""
    remote = repo.parent / f"{repo.name}.git"
    subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True,
                   capture_output=True, timeout=60)
    log = repo.parent / f"{repo.name}-pushes.log"
    hook = remote / "hooks" / "update"
    hook.write_text(f'#!/bin/sh\necho "$1 $2 $3" >> {log}\n')
    hook.chmod(0o755)
    _git(repo, "remote", "add", "origin", str(remote))
    _git(repo, "push", "-q", "-u", "origin", _git(repo, "symbolic-ref", "--short", "HEAD").strip())
    log.unlink()


def _pushes(repo: Path) -> list[str]:
    log = repo.parent / f"{repo.name}-pushes.log"
    return log.read_text().splitlines() if log.exists() else []


def _commit_a_passing_suite(repo: Path) -> None:
    """R-0977: a passing suite, so each job's gate meets the planner's criteria and the push goes."""
    (repo / "tests").mkdir()
    (repo / "tests" / "test_ok.py").write_text("def test_ok():\n    assert True\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "suite")


def test_the_plan_is_one_job_per_project_in_its_own_repository_under_one_mission(
        projects, tmp_path, capsys):
    from packages.orchestration.mission_state import load_mission
    from packages.orchestration.pingpong_job import load_job_plan

    (a, project_a), (b, project_b) = projects["a"], projects["b"]
    before = (_repo_state(a), _repo_state(b))

    data = _do_json(capsys, _order(tmp_path, project_a.slug, project_b.slug), "--plan-only")

    assert (data["shape"], data["shape_source"]) == ("one job per repository", "the order's projects")
    jobs = [load_job_plan(job_id) for job_id in data["job_ids"]]
    assert [(job.project_id, job.repo_path) for job in jobs] == [
        (str(project_a.id), str(a)), (str(project_b.id), str(b))]
    assert f"belongs to project {project_b.slug};" in jobs[1].mission
    mission = load_mission(str(project_a.id), data["mission_id"])
    assert mission.project_ids == (str(project_a.id), str(project_b.id))
    assert [link.project_id for link in mission.job_links] == [str(project_a.id), str(project_b.id)]
    assert (_repo_state(a), _repo_state(b)) == before


def test_under_a_commit_flag_each_job_lands_in_its_own_repository_and_each_is_pushed_once(
        projects, tmp_path, capsys):
    (a, project_a), (b, project_b) = projects["a"], projects["b"]
    heads = {}
    for repo in (a, b):
        _commit_a_passing_suite(repo)
        _bare_upstream(repo)
        heads[repo] = _head(repo)

    data = _do_json(capsys, _order(tmp_path, project_a.slug, project_b.slug),
                    "--commit", "Add the contributing guide", "--push")

    assert data["ok"] is True, data["steps"]
    assert [(entry["job_id"], entry["repo"]) for entry in data["landed"]] == [
        (data["job_ids"][0], str(a)), (data["job_ids"][1], str(b))]
    for entry in data["landed"]:
        repo = Path(entry["repo"])
        assert entry["sha"] == _head(repo)
        assert _git(repo, "rev-list", f"{heads[repo]}..{entry['sha']}").split() == [entry["sha"]]
        trailers = _git(repo, "log", "-1", "--format=%(trailers:only,unfold)").splitlines()
        assert f"Remedy-Job: {entry['job_id']}" in trailers
        [pushed] = _pushes(repo)
        assert pushed.endswith(entry["sha"])
    assert data["push"]["pushed"] is True
    assert [(push["repo"], push["sha"], push["pushed"]) for push in data["push"]["repositories"]] == [
        (entry["repo"], entry["sha"], True) for entry in data["landed"]]
    # Each job's calls are read from its own project's ledger, so the walk counts both.
    from packages.orchestration.token_ledger import query_cost

    rows = [query_cost(project_id=str(project.id), job_id=job_id, by="role").rows
            for job_id, project in zip(data["job_ids"], (project_a, project_b))]
    assert all(rows), "a job's calls are missing from its own project's ledger"
    assert sum(role["calls"] for role in data["cost"]["roles"]) == sum(
        row.calls for job_rows in rows for row in job_rows)


def test_a_repository_without_an_upstream_refuses_the_push_of_every_repository(
        projects, tmp_path, capsys):
    """The upstream of every repository is asked before any is pushed, so `a` is not pushed alone."""
    (a, project_a), (b, project_b) = projects["a"], projects["b"]
    for repo in (a, b):
        _commit_a_passing_suite(repo)
    _bare_upstream(a)

    with pytest.raises(SystemExit) as exc:
        main(["do", str(_order(tmp_path, project_a.slug, project_b.slug)), "--no-llm", "--no-ui",
              "--json", *FAKE_ROLES, "--commit", "Add the contributing guide", "--push"])
    data = json.loads(capsys.readouterr().out)

    assert exc.value.code == 1 and data["failed_step"] == "apply"
    assert "was refused after the commits landed, so nothing was pushed" in data["message"]
    assert [entry["repo"] for entry in data["landed"]] == [str(a), str(b)]
    assert _pushes(a) == [] and data["push"]["repositories"] == []


def test_the_init_step_adds_the_ignore_entries_in_every_repository(projects, tmp_path, capsys):
    (_, project_a), (b, project_b) = projects["a"], projects["b"]
    exclude = b / ".git" / "info" / "exclude"
    exclude.write_text("")

    _do_json(capsys, _order(tmp_path, project_a.slug, project_b.slug), "--plan-only")

    assert ".remedy-wt/" in exclude.read_text().split()


def test_a_project_whose_repository_is_not_a_git_repository_fails_the_init_step(
        projects, tmp_path, capsys, monkeypatch):
    from packages.orchestration.project_registry import RemyProject, save_project

    plain = tmp_path / "plain"
    plain.mkdir()
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    folder = RemyProject(name="plain", canonical_repo_path=str(plain))
    save_project(folder)

    data = _refused(capsys, _order(tmp_path, projects["a"][1].slug, folder.slug), code=1)

    assert data["failed_step"] == "init"
    assert f"{plain} is not a git repository; nothing was planned" in data["message"]
    _no_mission_and_no_job()


def test_one_project_named_twice_fails_the_init_step(projects, tmp_path, capsys):
    """Its slug and its id are two header values for one project."""
    project_a = projects["a"][1]

    data = _refused(capsys, _order(tmp_path, project_a.slug, str(project_a.id)), code=1)

    assert (data["failed_step"], data["message"]) == (
        "init", f"init failed: the order names project {project_a.slug} twice; nothing was planned")
    _no_mission_and_no_job()


def test_project_beside_a_header_naming_several_is_refused_before_any_step(projects, tmp_path, capsys):
    (_, project_a), (_, project_b) = projects["a"], projects["b"]

    data = _refused(capsys, _order(tmp_path, project_a.slug, project_b.slug),
                    "--project", project_b.slug, code=2)

    assert (data["ok"], data["error"]) == (False, "invalid_argument")
    _no_mission_and_no_job()


def test_repo_beside_several_projects_is_refused_before_any_step(projects, tmp_path, capsys):
    (a, project_a), (_, project_b) = projects["a"], projects["b"]

    data = _refused(capsys, _order(tmp_path, project_a.slug, project_b.slug),
                    "--repo", str(a), code=2)

    assert (data["ok"], data["error"]) == (False, "repo_not_in_project")
    _no_mission_and_no_job()


def test_a_named_project_without_a_repository_is_refused_before_any_step(projects, tmp_path, capsys):
    from packages.orchestration.project_registry import RemyProject, save_project

    bare = RemyProject(name="bare")
    save_project(bare)

    data = _refused(capsys, _order(tmp_path, projects["a"][1].slug, bare.slug), code=3)

    assert (data["ok"], data["error"]) == (False, "project_has_no_repo")
    assert bare.slug in data["message"]
    _no_mission_and_no_job()


def test_an_unknown_project_fails_the_init_step_and_plans_nothing(projects, tmp_path, capsys):
    data = _refused(capsys, _order(tmp_path, projects["a"][1].slug, "nowhere"), code=1)

    assert (data["error"], data["failed_step"]) == ("step_failed", "init")
    assert "'nowhere'" in data["message"]
    _no_mission_and_no_job()


@pytest.mark.parametrize("flag", ["--force-job", "--force-mission"])
def test_a_force_flag_fails_the_shape_step(projects, tmp_path, capsys, flag):
    from packages.orchestration.pingpong_job import list_job_plans

    order = _order(tmp_path, projects["a"][1].slug, projects["b"][1].slug)

    data = _refused(capsys, order, flag, "--plan-only", code=1)

    assert (data["error"], data["failed_step"]) == ("step_failed", "shape")
    assert "one job per repository" in data["message"]
    assert list_job_plans() == []
