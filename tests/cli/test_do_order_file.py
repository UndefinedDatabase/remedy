"""F295 T001 — `remedy do <order.md>` reads an order file (DECISION F295 D2).

In-process through `apps.cli.grouped.main`, against a temporary git repository
holding one committed file, with the data root under `tmp_path`, the fake
builder and reviewer and `--no-ui` always, exactly as `tests/cli/test_do_flags.py`
drives it. A tripwire fails the test if any model-call factory is reached.
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


def _write_order(repo: Path, text: str, name: str = "order.md") -> Path:
    path = repo / name
    path.write_text(text)
    return path


def _do(capsys, order_arg: str, *extra: str) -> str:
    main(["do", order_arg, "--no-llm", "--no-ui", *FAKE_ROLES, *extra])
    return capsys.readouterr().out


def _do_json(capsys, order_arg: str, *extra: str) -> dict:
    return json.loads(_do(capsys, order_arg, "--json", *extra))


def _exit_code_and_output(capsys, order_arg: str, *extra: str) -> tuple[int, str, str]:
    with pytest.raises(SystemExit) as exc:
        _do(capsys, order_arg, "--json", *extra)
    captured = capsys.readouterr()
    return exc.value.code, captured.out, captured.err


def _step(data: dict, name: str) -> dict:
    return next(s for s in data["steps"] if s["name"] == name)


def _missions_dir_exists(repo: Path) -> bool:
    from packages.orchestration.data_paths import missions_dir

    root = missions_dir()
    return root.exists() and any(root.iterdir())


# ── 1: a valid order file plans and RUNS, the file's own name never named ────


def test_an_order_file_with_a_cost_cap_plans_and_runs_its_order(repo, capsys):
    order_path = _write_order(repo, "---\nmax-cost-usd: 1\n---\nWrite a CONTRIBUTING.md\n")

    data = _do_json(capsys, str(order_path))

    assert data["ok"] is True
    assert _step(data, "run")["status"] == "done"
    plan_text = Path(data["mission_plan_path"]).read_text()
    assert "Write a CONTRIBUTING.md" in plan_text
    assert order_path.name not in plan_text


# ── 2, 3: a missing path is refused before any step ──────────────────────────


def test_a_missing_md_path_exits_2_with_order_file_not_found_and_no_missions_dir(
        repo, capsys):
    missing = repo / "missing.md"

    code, out, err = _exit_code_and_output(capsys, str(missing))

    assert code == 2
    assert err == ""
    body = json.loads(out)
    assert body["ok"] is False
    assert body["error"] == "order_file_not_found"
    assert str(missing) in body["message"]
    assert not _missions_dir_exists(repo)


def test_the_same_refusal_without_json_prints_the_path_on_stderr_and_nothing_on_stdout(
        repo, capsys):
    missing = repo / "missing.md"

    with pytest.raises(SystemExit) as exc:
        main(["do", str(missing), "--no-llm", "--no-ui", *FAKE_ROLES])
    assert exc.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert str(missing) in captured.err


# ── 4: a directory named order.md is unreadable ───────────────────────────────


def test_a_directory_named_order_md_exits_2_with_order_file_unreadable(repo, capsys):
    directory = repo / "order.md"
    directory.mkdir()

    code, out, err = _exit_code_and_output(capsys, str(directory))

    assert code == 2
    body = json.loads(out)
    assert body["error"] == "order_file_unreadable"


# ── 5: an order empty after its header is refused ────────────────────────────


def test_an_order_empty_after_its_header_exits_2_with_order_file_empty(repo, capsys):
    order_path = _write_order(repo, "---\nmax-cost-usd: 1\n---\n   \n")

    code, out, err = _exit_code_and_output(capsys, str(order_path))

    assert code == 2
    body = json.loads(out)
    assert body["error"] == "order_file_empty"


# ── 6: a broken header key is refused ────────────────────────────────────────


def test_a_header_line_budget_3_exits_2_with_order_file_invalid_header(repo, capsys):
    order_path = _write_order(repo, "---\nbudget: 3\n---\nWrite a CONTRIBUTING.md\n")

    code, out, err = _exit_code_and_output(capsys, str(order_path))

    assert code == 2
    body = json.loads(out)
    assert body["error"] == "order_file_invalid_header"


# ── 7, 8: the cost-cap refusal and its escape ────────────────────────────────


def test_an_order_file_without_a_cost_cap_or_flag_exits_2_naming_max_cost_usd(
        repo, capsys):
    order_path = _write_order(repo, "Write a CONTRIBUTING.md\n")

    code, out, err = _exit_code_and_output(capsys, str(order_path))

    assert code == 2
    body = json.loads(out)
    assert body["error"] == "order_file_no_cost_cap"
    assert "--max-cost-usd" in body["message"]
    assert not _missions_dir_exists(repo)


def test_the_same_file_with_max_cost_usd_flag_and_plan_only_is_ok(repo, capsys):
    order_path = _write_order(repo, "Write a CONTRIBUTING.md\n")

    data = _do_json(capsys, str(order_path), "--max-cost-usd", "1", "--plan-only")

    assert data["ok"] is True


# ── 9: a header contract, and a flag that wins over it ───────────────────────


def test_a_header_contract_gives_that_template_and_a_contract_flag_wins_over_it(
        repo, capsys):
    order_path = _write_order(
        repo, "---\nmax-cost-usd: 1\ncontract: website\n---\nWrite a CONTRIBUTING.md\n")

    data = _do_json(capsys, str(order_path), "--plan-only")
    assert data["contract"]["template"] == "website"

    data = _do_json(capsys, str(order_path), "--plan-only", "--contract", "cli-tool")
    assert data["contract"]["template"] == "cli-tool"


# ── 9a-9d: the header's max-cost-usd and project reach the job, flags win (R-1140) ──


def test_a_header_max_cost_usd_becomes_the_run_jobs_recorded_budget(repo, capsys):
    from packages.orchestration.pingpong_job import load_job_plan

    order_path = _write_order(
        repo, "---\nmax-cost-usd: 0.75\n---\nWrite a CONTRIBUTING.md\n")

    data = _do_json(capsys, str(order_path))

    assert _step(data, "run")["status"] == "done"
    [job_id] = data["job_ids"]
    assert load_job_plan(job_id).budgets["max_cost_usd"] == 0.75


def test_the_max_cost_usd_flag_wins_over_the_headers_value(repo, capsys):
    from packages.orchestration.pingpong_job import load_job_plan

    order_path = _write_order(
        repo, "---\nmax-cost-usd: 0.75\n---\nWrite a CONTRIBUTING.md\n")

    data = _do_json(capsys, str(order_path), "--max-cost-usd", "2")

    assert _step(data, "run")["status"] == "done"
    [job_id] = data["job_ids"]
    assert load_job_plan(job_id).budgets["max_cost_usd"] == 2


def test_a_header_project_selects_that_registered_project_for_the_job(
        repo, tmp_path, capsys, monkeypatch):
    """The project `remedy init` registered for ANOTHER repository, named by the
    header, so a walk that ignored the header's `project` key would never find
    it and the target repository must stay unregistered throughout."""
    from packages.orchestration.pingpong_job import load_job_plan
    from packages.orchestration.project_registry import resolve_project

    other = _git_repo(tmp_path / "other")
    monkeypatch.chdir(other)
    main(["init"])
    project = resolve_project(other)
    assert project is not None
    monkeypatch.chdir(repo)
    capsys.readouterr()

    order_path = _write_order(
        repo, f"---\nproject: {project.slug}\nmax-cost-usd: 1\n---\n"
        "Write a CONTRIBUTING.md\n")

    data = _do_json(capsys, str(order_path), "--plan-only")

    [job_id] = data["job_ids"]
    job = load_job_plan(job_id)
    assert job.project_id == str(project.id)
    assert resolve_project(repo) is None


def test_the_project_flag_wins_over_a_header_naming_an_unknown_project(
        repo, tmp_path, capsys, monkeypatch):
    """The header names a project that does not exist; if the header won, the
    init step would fail on it. `--project` wins instead, so the walk selects
    the flag's (real, registered) project and the job plans successfully."""
    from packages.orchestration.pingpong_job import load_job_plan
    from packages.orchestration.project_registry import resolve_project

    other = _git_repo(tmp_path / "other")
    monkeypatch.chdir(other)
    main(["init"])
    project = resolve_project(other)
    assert project is not None
    monkeypatch.chdir(repo)
    capsys.readouterr()

    order_path = _write_order(
        repo, "---\nproject: no-such-project\nmax-cost-usd: 1\n---\n"
        "Write a CONTRIBUTING.md\n")

    data = _do_json(capsys, str(order_path), "--plan-only", "--project", project.slug)

    assert data["ok"] is True
    [job_id] = data["job_ids"]
    job = load_job_plan(job_id)
    assert job.project_id == str(project.id)


# ── 10: a header constraint reaches the plan ─────────────────────────────────


def test_a_header_constraint_reaches_the_mission_plans_goal_section(repo, capsys):
    order_path = _write_order(
        repo,
        "---\nmax-cost-usd: 1\nconstraint: never edit README.md\n---\n"
        "Write a CONTRIBUTING.md\n",
    )

    data = _do_json(capsys, str(order_path), "--plan-only")

    plan_text = Path(data["mission_plan_path"]).read_text()
    assert "Constraints the plan must honour:" in plan_text
    assert "- never edit README.md" in plan_text


# ── 11: order TEXT naming a .md file stays text; the cap rule does not bind ──


def test_order_text_naming_a_md_file_stays_text_and_the_cap_rule_does_not_bind(
        repo, capsys):
    order_text = "fix the heading in README.md"

    data = _do_json(capsys, order_text, "--plan-only")

    assert data["ok"] is True
    plan_text = Path(data["mission_plan_path"]).read_text()
    assert order_text in plan_text
