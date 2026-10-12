"""F206 T002, DECISION F206 D2 — the repository catalog orders a multi-project walk's jobs.

The projects `a` and `b` of `tests/cli/test_do_several_projects.py` are reused here with an
order naming `a` then `b`. When the repository catalog holds an edge between them, the jobs plan
in the catalog's order instead of the header's, the init step's detail cites the edge, and each
job's order text cites it too; the mission still lives in `a`, the project the header names
first. A catalog without an edge between the two leaves the header's own order untouched. A
catalog that cannot be used — a cycle, an unknown key — fails the init step before anything is
planned.

In-process through `apps.cli.grouped.main`, exactly as `tests/cli/test_do_several_projects.py`
drives it, importing its fixtures.
"""
from __future__ import annotations

from packages.orchestration.repo_catalog import repo_catalog_path
from tests.cli.test_do_project_repo import (  # noqa: F401 — fixtures used by name
    _no_mission_and_no_job,
    _refused,
    no_model_call,
    projects,
)
from tests.cli.test_do_several_projects import _do_json, _order


def _write_catalog(text: str) -> None:
    path = repo_catalog_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _init_detail(data: dict) -> str:
    return next(step["detail"] for step in data["steps"] if step["name"] == "init")


def test_a_catalog_naming_the_dependency_by_slug_reorders_the_jobs_and_cites_the_edge(
        projects, tmp_path, capsys):
    from packages.orchestration.mission_state import load_mission
    from packages.orchestration.pingpong_job import load_job_plan

    (a, project_a), (b, project_b) = projects["a"], projects["b"]
    _write_catalog(
        f'[[repo]]\npid = "{project_a.slug}"\ndepends_on = ["{project_b.slug}"]\n'
        f'[[repo]]\npid = "{project_b.slug}"\n')

    data = _do_json(capsys, _order(tmp_path, project_a.slug, project_b.slug), "--plan-only")

    jobs = [load_job_plan(job_id) for job_id in data["job_ids"]]
    assert [(job.project_id, job.repo_path) for job in jobs] == [
        (str(project_b.id), str(b)), (str(project_a.id), str(a))]
    # The mission still lives in `a`, the project the header names first (DECISION F206 D2).
    assert load_mission(str(project_a.id), data["mission_id"]).id == data["mission_id"]
    sentence = f"{project_a.slug} depends on {project_b.slug}"
    assert _init_detail(data).endswith(f"; ordered by the repository catalog: {sentence}")
    for job in jobs:
        assert f"The repository catalog orders them: {sentence}." in job.mission


def test_a_catalog_naming_the_dependency_by_id_reorders_the_jobs_the_same_way(
        projects, tmp_path, capsys):
    from packages.orchestration.pingpong_job import load_job_plan

    (a, project_a), (b, project_b) = projects["a"], projects["b"]
    _write_catalog(
        f'[[repo]]\npid = "{project_a.slug}"\ndepends_on = ["{project_b.id}"]\n'
        f'[[repo]]\npid = "{project_b.id}"\n')

    data = _do_json(capsys, _order(tmp_path, project_a.slug, project_b.slug), "--plan-only")

    jobs = [load_job_plan(job_id) for job_id in data["job_ids"]]
    assert [(job.project_id, job.repo_path) for job in jobs] == [
        (str(project_b.id), str(b)), (str(project_a.id), str(a))]
    sentence = f"{project_a.slug} depends on {project_b.id}"
    assert _init_detail(data).endswith(f"; ordered by the repository catalog: {sentence}")
    for job in jobs:
        assert f"The repository catalog orders them: {sentence}." in job.mission


def test_a_catalog_without_an_edge_between_them_keeps_the_headers_own_order(
        projects, tmp_path, capsys):
    from packages.orchestration.pingpong_job import load_job_plan

    (a, project_a), (b, project_b) = projects["a"], projects["b"]
    _write_catalog(f'[[repo]]\npid = "{project_a.slug}"\n[[repo]]\npid = "{project_b.slug}"\n')

    data = _do_json(capsys, _order(tmp_path, project_a.slug, project_b.slug), "--plan-only")

    jobs = [load_job_plan(job_id) for job_id in data["job_ids"]]
    assert [(job.project_id, job.repo_path) for job in jobs] == [
        (str(project_a.id), str(a)), (str(project_b.id), str(b))]
    assert "ordered by the repository catalog" not in _init_detail(data)
    for job in jobs:
        assert "The repository catalog orders them" not in job.mission


def test_a_cycle_in_the_catalog_fails_the_init_step_before_anything_is_planned(
        projects, tmp_path, capsys):
    (a, project_a), (_, project_b) = projects["a"], projects["b"]
    _write_catalog(
        f'[[repo]]\npid = "{project_a.slug}"\ndepends_on = ["{project_b.slug}"]\n'
        f'[[repo]]\npid = "{project_b.slug}"\ndepends_on = ["{project_a.slug}"]\n')

    data = _refused(capsys, _order(tmp_path, project_a.slug, project_b.slug), "--plan-only", code=1)

    assert data["failed_step"] == "init"
    assert data["message"].startswith("init failed: the repository catalog cannot be used: ")
    assert "the repository catalog has a dependency cycle" in data["message"]
    _no_mission_and_no_job()


def test_an_unknown_key_in_the_catalog_fails_the_init_step_before_anything_is_planned(
        projects, tmp_path, capsys):
    (a, project_a), (_, project_b) = projects["a"], projects["b"]
    _write_catalog(
        f'[[repo]]\npid = "{project_a.slug}"\nbogus = 1\n'
        f'[[repo]]\npid = "{project_b.slug}"\n')

    data = _refused(capsys, _order(tmp_path, project_a.slug, project_b.slug), "--plan-only", code=1)

    assert data["failed_step"] == "init"
    assert data["message"].startswith("init failed: the repository catalog cannot be used: ")
    assert "'bogus'" in data["message"]
    _no_mission_and_no_job()
