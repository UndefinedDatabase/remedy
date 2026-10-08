"""F304 T002 — an order that names a project runs in that project's repository (DECISION F304 D2).

The project `b` is registered by `remedy init` in its own repository. The order names it in its
header and is started from repository `a`, which `remedy init` registered as another project,
from a folder that is no repository, and with `--repo` naming either repository. Without
`--repo` the order runs in `b` wherever the client stands; a `--repo` that is not one of `b`'s
repositories, and a project with no registered repository, are refused before any step.

In-process through `apps.cli.grouped.main`, with the data root under `tmp_path`, the fake builder
and reviewer and `--no-ui` always, exactly as `tests/cli/test_do_order_file.py` drives it. A
tripwire fails the test if any model-call factory is reached.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from apps.cli.grouped import main

FAKE_ROLES = ("--builder-provider", "fake", "--reviewer-provider", "fake")


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=str(repo), capture_output=True,
                          text=True, check=True).stdout


def _git_repo(path: Path) -> Path:
    path.mkdir()
    _git(path, "init", "-q")
    _git(path, "config", "user.email", "t@e.com")
    _git(path, "config", "user.name", "T")
    _git(path, "config", "commit.gpgsign", "false")
    (path / "README.md").write_text(f"# {path.name}\n")
    _git(path, "add", "-A")
    _git(path, "commit", "-qm", "init")
    return path.resolve()


def _repo_state(repo: Path) -> tuple[str, str, str]:
    """HEAD, the porcelain status and every branch: what an order that ran there would change."""
    return (_git(repo, "rev-parse", "HEAD"), _git(repo, "status", "--porcelain"),
            _git(repo, "branch", "--list"))


@pytest.fixture(autouse=True)
def no_model_call(monkeypatch):
    """Every factory that could reach a model fails the test when called."""
    def tripwire(*args, **kwargs):
        raise AssertionError("remedy do reached a model-call factory")

    monkeypatch.setattr("packages.orchestration.intake.make_provider_call_fn", tripwire)
    monkeypatch.setattr("packages.orchestration.intake.make_structured_call_fn", tripwire)
    monkeypatch.setattr("packages.orchestration.study.study_call_fn", tripwire)


@pytest.fixture
def projects(tmp_path, monkeypatch, capsys):
    """Repositories `a` and `b`, each registered by `remedy init`; the client stands in `a`."""
    from packages.orchestration.project_registry import resolve_project

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    registered = {}
    for name in ("a", "b"):
        repo = _git_repo(tmp_path / name)
        monkeypatch.chdir(repo)
        main(["init"])
        registered[name] = (repo, resolve_project(repo))
    monkeypatch.chdir(registered["a"][0])
    capsys.readouterr()
    return registered


def _order(folder: Path, project: str) -> Path:
    path = folder / "order.md"
    path.write_text(f"---\nproject: {project}\nmax-cost-usd: 1\n---\nWrite a CONTRIBUTING.md\n")
    return path


def _do_json(capsys, order: Path, *extra: str) -> dict:
    main(["do", str(order), "--no-llm", "--no-ui", "--json", *FAKE_ROLES, *extra])
    return json.loads(capsys.readouterr().out)


def _refused(capsys, order: Path, *extra: str) -> dict:
    with pytest.raises(SystemExit) as exc:
        main(["do", str(order), "--no-llm", "--no-ui", "--json", *FAKE_ROLES, *extra])
    assert exc.value.code == 2
    captured = capsys.readouterr()
    assert captured.err == ""
    return json.loads(captured.out)


def _no_mission_and_no_job() -> None:
    from packages.orchestration.mission_state import project_ids_with_missions
    from packages.orchestration.pingpong_job import list_job_plans

    assert project_ids_with_missions() == []
    assert list_job_plans() == []


def test_an_order_naming_b_started_in_a_runs_in_b_and_leaves_a_unchanged(projects, tmp_path, capsys):
    """A full run with the fake roles: the job, its worktree and its branch are `b`'s."""
    from packages.orchestration.pingpong_job import load_job_plan

    (a, _), (b, project_b) = projects["a"], projects["b"]
    order = _order(tmp_path, project_b.slug)
    before = _repo_state(a)

    data = _do_json(capsys, order)

    assert data["ok"] is True
    [job_id] = data["job_ids"]
    job = load_job_plan(job_id)
    assert (job.project_id, job.repo_path) == (str(project_b.id), str(b))
    assert _repo_state(a) == before
    assert f"remedy/job-{job_id}" in _git(b, "branch", "--list")


def test_an_order_naming_b_started_in_no_repository_runs_in_b(projects, tmp_path, capsys, monkeypatch):
    """`GIT_CEILING_DIRECTORIES` keeps git from climbing out of `plain` into a checkout above it."""
    from packages.orchestration.pingpong_job import load_job_plan

    b, project_b = projects["b"]
    plain = tmp_path / "plain"
    plain.mkdir()
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    monkeypatch.chdir(plain)

    data = _do_json(capsys, _order(plain, project_b.slug), "--plan-only")

    [job_id] = data["job_ids"]
    assert load_job_plan(job_id).repo_path == str(b)


def test_an_order_naming_b_with_repo_b_runs_in_b(projects, tmp_path, capsys):
    from packages.orchestration.pingpong_job import load_job_plan

    b, project_b = projects["b"]

    data = _do_json(capsys, _order(tmp_path, project_b.slug), "--plan-only", "--repo", str(b))

    [job_id] = data["job_ids"]
    assert load_job_plan(job_id).repo_path == str(b)


def test_an_order_naming_b_with_repo_a_is_refused_before_any_step(projects, tmp_path, capsys):
    (a, _), (b, project_b) = projects["a"], projects["b"]
    before = _repo_state(a)

    data = _refused(capsys, _order(tmp_path, project_b.slug), "--repo", str(a))

    assert (data["ok"], data["error"]) == (False, "repo_not_in_project")
    assert str(b) in data["message"]
    assert "steps" not in data
    _no_mission_and_no_job()
    assert _repo_state(a) == before


def test_an_order_naming_a_project_without_a_repository_is_refused_before_any_step(
        projects, tmp_path, capsys):
    from packages.orchestration.project_registry import RemyProject, save_project

    bare = RemyProject(name="bare")
    save_project(bare)

    data = _refused(capsys, _order(tmp_path, bare.slug))

    assert (data["ok"], data["error"]) == (False, "project_has_no_repo")
    assert f"remedy project attach --project {bare.slug} --repo" in data["message"]
    _no_mission_and_no_job()
