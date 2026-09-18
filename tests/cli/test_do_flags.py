"""F268 — `remedy do`'s flags as DECISION F268 D16 rules them.

`--project` selects the project the init step uses; the budget flags are resolved
before the first step and reach the job; `--builder-model` and `--reviewer-model`
reach the job and every `remedy job run` Next line; `--planner-model` reaches every
structured planner call (D16 (4) to (7)).

In-process through `apps.cli.grouped.main`, against a temporary git repository
holding one committed file, with the data root under `tmp_path`, the fake builder
and reviewer and `--no-ui` always. A tripwire fails the test if any model-call
factory is reached, except where a test replaces one with a recorder.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from apps.cli.grouped import main

ORDER = "Write a CONTRIBUTING.md"
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


@pytest.fixture
def repo(tmp_path, monkeypatch) -> Path:
    """An UNREGISTERED git repository with one committed file, as the working directory."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    target = _git_repo(tmp_path / "target")
    monkeypatch.chdir(target)
    return target


@pytest.fixture(autouse=True)
def no_model_call(monkeypatch):
    """Every factory that could reach a model fails the test when called."""
    def tripwire(*args, **kwargs):
        raise AssertionError("remedy do reached a model-call factory")

    monkeypatch.setattr("packages.orchestration.intake.make_provider_call_fn", tripwire)
    monkeypatch.setattr("packages.orchestration.intake.make_structured_call_fn", tripwire)
    monkeypatch.setattr("packages.orchestration.study.study_call_fn", tripwire)


def _do(capsys, *extra: str, order: str = ORDER, llm: bool = False) -> str:
    main(["do", order, *(() if llm else ("--no-llm",)), "--no-ui", *FAKE_ROLES, *extra])
    return capsys.readouterr().out


def _do_json(capsys, *extra: str, llm: bool = False) -> dict:
    return json.loads(_do(capsys, "--json", *extra, llm=llm))


def _step(data: dict, name: str) -> dict:
    return next(s for s in data["steps"] if s["name"] == name)


def _exit_code_and_output(capsys, *extra: str) -> tuple[int, str, str]:
    with pytest.raises(SystemExit) as exc:
        _do(capsys, "--json", *extra)
    captured = capsys.readouterr()
    return exc.value.code, captured.out, captured.err


# ── --project (DECISION F268 D16 (4)) ────────────────────────────────────────


def test_project_of_a_project_init_registered_walks_and_the_job_is_that_projects(
        repo, tmp_path, capsys, monkeypatch):
    """The project `remedy init` registered for ANOTHER repository, so a walk that
    ignored `--project` would register the target and plan the job under it."""
    from packages.orchestration.pingpong_job import load_job_plan
    from packages.orchestration.project_registry import resolve_project

    other = _git_repo(tmp_path / "other")
    monkeypatch.chdir(other)
    main(["init"])
    project = resolve_project(other)
    assert project is not None
    monkeypatch.chdir(repo)
    capsys.readouterr()

    data = _do_json(capsys, "--project", project.slug)

    init = _step(data, "init")
    assert (init["status"], init["detail"]) == (
        "done", f"project {project.slug} ({project.id}) selected by --project")
    assert _step(data, "run")["status"] == "done"
    [job_id] = data["job_ids"]
    job = load_job_plan(job_id)
    assert job.project_id == str(project.id)
    assert job.repo_path == str(repo)
    assert resolve_project(repo) is None


def test_an_unknown_project_exits_1_with_the_init_step_failed_and_no_mission(repo, capsys):
    from packages.orchestration.mission_state import project_ids_with_missions
    from packages.orchestration.pingpong_job import list_job_plans
    from packages.orchestration.project_registry import resolve_project

    code, out, err = _exit_code_and_output(capsys, "--project", "no-such-project")

    assert code == 1
    data = json.loads(out)
    assert [(s["name"], s["status"]) for s in data["steps"]] == [("init", "failed")]
    assert "no-such-project" in _step(data, "init")["detail"]
    assert data["mission_id"] is None
    assert project_ids_with_missions() == []
    assert list_job_plans() == []
    assert resolve_project(repo) is None
    assert "Error: init failed: " in err


# ── the budget flags (DECISION F268 D16 (5)) ─────────────────────────────────


def test_max_total_tokens_is_the_jobs_recorded_budget(repo, capsys):
    from packages.orchestration.pingpong_job import load_job_plan

    data = _do_json(capsys, "--max-total-tokens", "100000")

    [job_id] = data["job_ids"]
    assert _step(data, "run")["status"] == "done"
    assert load_job_plan(job_id).budgets["max_total_tokens"] == 100000


def test_an_invalid_budget_value_exits_2_and_leaves_the_repository_unregistered(repo, capsys):
    from packages.orchestration.pingpong_job import list_job_plans
    from packages.orchestration.project_registry import resolve_project

    code, out, err = _exit_code_and_output(capsys, "--max-total-tokens", "many")

    assert code == 2
    assert out == ""
    assert "Nothing was run." in err
    assert resolve_project(repo) is None
    assert list_job_plans() == []


# ── the model flags (DECISION F268 D16 (6), (7)) ─────────────────────────────


def test_builder_and_reviewer_models_are_the_jobs_cli_models_and_on_the_next_line(
        repo, capsys):
    from packages.orchestration.pingpong_job import load_job_plan

    data = _do_json(capsys, "--builder-model", "m1", "--reviewer-model", "m2")

    [job_id] = data["job_ids"]
    config = load_job_plan(job_id).execution_config
    assert (config.builder_model, config.builder_model_source) == ("m1", "cli")
    assert (config.reviewer_model, config.reviewer_model_source) == ("m2", "cli")

    planned = _do_json(capsys, "--builder-model", "m1", "--reviewer-model", "m2",
                       "--plan-only")

    [planned_job] = planned["job_ids"]
    assert planned["next"] == [
        f"remedy job run {planned_job} --builder-provider fake --reviewer-provider fake "
        f"--builder-model m1 --reviewer-model m2"]


def test_planner_model_reaches_every_structured_planner_call(repo, capsys, monkeypatch):
    """Without `--no-llm`: every structured call the plan and shape steps build is
    recorded, and none is served, so each step plans deterministically."""
    calls: list[tuple[str, object]] = []

    def recorder(model_cls, **kwargs):
        calls.append((model_cls.__name__, kwargs.get("model")))
        return None

    monkeypatch.setattr("packages.orchestration.intake.make_structured_call_fn", recorder)
    monkeypatch.setattr("packages.orchestration.study.study_call_fn", lambda *a, **kw: None)

    data = _do_json(capsys, "--planner-model", "p1", "--plan-only", llm=True)

    assert data["job_ids"]
    assert calls
    # The plan step's mission plan call and the shape step's intake call, at least.
    assert {"MissionPlanDraft", "JobIntake"} <= {name for name, _model in calls}, calls
    assert [model for _name, model in calls] == ["p1"] * len(calls), calls
