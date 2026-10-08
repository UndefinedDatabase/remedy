"""F304 T002 — one command registers a repository for a client and leaves its working copy clean.

`remedy project register --repo <path> --json` registers the repository as a project's, or answers
the project that already holds it, and writes nothing `git status` shows (DECISION F304 D3). An
order that then names the project runs there (DECISION F304 D2).

In-process through `apps.cli.grouped.main`, with the data root under `tmp_path`.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from apps.cli.grouped import main


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


@pytest.fixture
def repo(tmp_path, monkeypatch) -> Path:
    """An unregistered repository; the client stands in `tmp_path`, which is no repository."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    return _git_repo(tmp_path / "b")


def _register(capsys, *args: str) -> dict:
    main(["project", "register", *args, "--json"])
    return json.loads(capsys.readouterr().out)


def test_register_answers_a_new_project_and_leaves_the_working_copy_clean(repo, capsys):
    from packages.orchestration.project_registry import resolve_project

    data = _register(capsys, "--repo", str(repo))

    project = resolve_project(repo)
    assert project is not None
    assert data == {"ok": True, "schema_version": 1, "project_id": str(project.id),
                    "slug": project.slug, "repo_path": str(repo), "created": True}
    assert _git(repo, "status", "--porcelain", "--untracked-files=all") == ""
    assert sorted(path.name for path in repo.iterdir()) == [".git", "README.md"]


def test_register_twice_answers_the_same_project_with_created_false(repo, capsys):
    first = _register(capsys, "--repo", str(repo))
    second = _register(capsys, "--repo", str(repo))

    assert (first["slug"], first["created"]) == ("b", True)
    assert (second["project_id"], second["slug"], second["created"]) == (
        first["project_id"], "b", False)


def test_an_order_naming_the_registered_project_runs_in_its_repository(repo, tmp_path, capsys, monkeypatch):
    from packages.orchestration.pingpong_job import load_job_plan

    for factory in ("intake.make_provider_call_fn", "intake.make_structured_call_fn", "study.study_call_fn"):
        monkeypatch.setattr(f"packages.orchestration.{factory}",
                            lambda *a, **k: pytest.fail("remedy do reached a model-call factory"))
    slug = _register(capsys, "--repo", str(repo))["slug"]
    order = tmp_path / "order.md"
    order.write_text(f"---\nproject: {slug}\nmax-cost-usd: 1\n---\nWrite a CONTRIBUTING.md\n")

    main(["do", str(order), "--no-llm", "--no-ui", "--json", "--plan-only",
          "--builder-provider", "fake", "--reviewer-provider", "fake"])

    [job_id] = json.loads(capsys.readouterr().out)["job_ids"]
    assert load_job_plan(job_id).repo_path == str(repo)


def test_a_path_that_is_no_repository_exits_4_and_registers_nothing(repo, tmp_path, capsys):
    from packages.orchestration.project_registry import list_projects

    plain = tmp_path / "plain"
    plain.mkdir()

    with pytest.raises(SystemExit) as exc:
        main(["project", "register", "--repo", str(plain), "--json"])

    assert exc.value.code == 4
    data = json.loads(capsys.readouterr().out)
    assert (data["ok"], data["error"]) == (False, "not_a_git_repo")
    assert list_projects() == []
