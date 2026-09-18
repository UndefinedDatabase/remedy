"""F268 T001 — `remedy do "<order>"` end to end, one test per step boundary.

In-process through `apps.cli.grouped.main`, against a temporary git repository
holding one committed file, with the data root under `tmp_path`, the fake
builder and reviewer, `--no-ui`, and `--no-llm`. A tripwire fails the test if
any model-call factory is reached: no step of this walk may call a model.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import pytest

from apps.cli.grouped import main

ORDER = "Write a CONTRIBUTING.md"


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=str(repo), capture_output=True,
                          text=True, check=True).stdout


@pytest.fixture
def repo(tmp_path, monkeypatch) -> Path:
    """An UNREGISTERED git repository with one committed file, as the working directory."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    target = tmp_path / "target"
    target.mkdir()
    _git(target, "init", "-q")
    _git(target, "config", "user.email", "t@e.com")
    _git(target, "config", "user.name", "T")
    _git(target, "config", "commit.gpgsign", "false")
    (target / "README.md").write_text("# target\n")
    _git(target, "add", "-A")
    _git(target, "commit", "-qm", "init")
    monkeypatch.chdir(target)
    return target.resolve()


@pytest.fixture(autouse=True)
def no_model_call(monkeypatch):
    """Every factory that could reach a model fails the test when called."""
    def tripwire(*args, **kwargs):
        raise AssertionError("remedy do reached a model-call factory under --no-llm")

    monkeypatch.setattr("packages.orchestration.intake.make_provider_call_fn", tripwire)
    monkeypatch.setattr("packages.orchestration.intake.make_structured_call_fn", tripwire)
    monkeypatch.setattr("packages.orchestration.study.study_call_fn", tripwire)


def _do(capsys, *extra: str, order: str = ORDER) -> str:
    main(["do", order, "--no-llm", "--no-ui",
          "--builder-provider", "fake", "--reviewer-provider", "fake", *extra])
    return capsys.readouterr().out


def _do_json(capsys, order: str = ORDER) -> dict:
    return json.loads(_do(capsys, "--json", order=order))


def _step(data: dict, name: str) -> dict:
    return next(s for s in data["steps"] if s["name"] == name)


def test_init_to_study_registers_studies_once_and_records_it(repo, capsys):
    from packages.orchestration.project_registry import resolve_project

    assert resolve_project(repo) is None
    head = _git(repo, "rev-parse", "HEAD").strip()

    first = _do_json(capsys)

    project = resolve_project(repo)
    assert project is not None
    assert _step(first, "init")["detail"].startswith(f"registered {repo} as project ")
    assert _step(first, "study")["status"] == "done"
    studied_at = project.metadata["studied_at"]
    assert studied_at
    assert project.metadata["studied_head"] == head

    second = _do_json(capsys, order="Write a CHANGELOG.md")

    assert _step(second, "study")["status"] == "skipped"
    assert "already studied" in _step(second, "study")["detail"]
    assert resolve_project(repo).metadata["studied_at"] == studied_at


def test_study_to_plan_creates_the_mission_carrying_the_order(repo, capsys):
    from packages.orchestration.mission_state import load_mission
    from packages.orchestration.project_registry import resolve_project

    data = _do_json(capsys)

    mission = load_mission(str(resolve_project(repo).id), data["mission_id"])
    assert mission.id == data["mission_id"]
    assert mission.goal == ORDER
    assert mission.order.text == ORDER
    assert mission.mission_plan is not None
    assert data["mission_id"] in _step(data, "plan")["detail"]


def test_plan_to_shape_yields_one_job_linked_to_the_mission_targeting_the_repo(repo, capsys):
    from packages.orchestration.mission_state import load_mission
    from packages.orchestration.pingpong_job import list_job_plans, load_job_plan
    from packages.orchestration.project_registry import resolve_project

    data = _do_json(capsys)

    [job_id] = data["job_ids"]
    assert [str(j.job_id) for j in list_job_plans()] == [job_id]
    mission = load_mission(str(resolve_project(repo).id), data["mission_id"])
    assert [(link.job_id, link.role) for link in mission.job_links] == [(job_id, "initial")]
    assert load_job_plan(job_id).repo_path == str(repo)


def test_shape_to_run_completes_on_the_named_fake_providers(repo, capsys):
    from packages.orchestration.pingpong_job import JOB_COMPLETED, load_job_plan

    data = _do_json(capsys)

    job = load_job_plan(data["job_ids"][0])
    assert job.state == JOB_COMPLETED
    assert job.tasks and {str(t.status) for t in job.tasks} == {"applied_to_job_workspace"}
    assert _step(data, "run")["status"] == "done"
    # R-0933: the flag reached the run — recorded as the CLI's choice, not a default.
    config = job.execution_config
    assert (config.builder, config.builder_source) == ("fake", "cli")
    assert (config.reviewer, config.reviewer_source) == ("fake", "cli")


def test_run_to_stop_leaves_the_target_untouched_and_stops_before_apply(repo, capsys):
    before = _git(repo, "status", "--porcelain", "--untracked-files=all")
    head = _git(repo, "rev-parse", "HEAD")

    data = _do_json(capsys)

    assert _git(repo, "status", "--porcelain", "--untracked-files=all") == before
    assert _git(repo, "rev-parse", "HEAD") == head
    assert data["stopped_before_apply"] is True
    assert data["contract"] is None
    assert [s["name"] for s in data["steps"]] == [
        "init", "study", "plan", "shape", "run", "ui", "apply"]
    assert _step(data, "apply")["status"] == "stopped"


def test_job_apply_accepts_the_job_do_ran(repo, capsys):
    """R-0897: every run `remedy do` starts belongs to a job `job apply` accepts."""
    from packages.orchestration.job_apply import apply_job

    data = _do_json(capsys)

    result = apply_job(data["job_ids"][0], str(repo), approve=True)
    assert result.status == "applied", result.blocked_reason
    assert result.files_applied


def test_next_lines_carry_real_ids_and_paths_never_placeholders(repo, capsys):
    """R-0811: `do` attaches the working directory's repo without a flag, and every
    `Next:` line names the real job and path."""
    out = _do(capsys)

    for placeholder in ("<job_id>", "<path>", "<mission>"):
        assert placeholder not in out
    assert not re.search(r"<[a-z_]+>", out)
    [job_id] = re.findall(r"one job ([0-9a-f]{16}) linked", out)
    next_lines = [line for line in out.splitlines() if line.startswith("Next: ")]
    assert next_lines
    assert all(job_id in line for line in next_lines)
    assert f"Next: remedy job apply {job_id} --repo {repo} --approve" in next_lines
