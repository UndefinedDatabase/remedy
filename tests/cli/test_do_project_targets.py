"""F299 T004, DECISIONs F299 D1 and D2: `remedy do`'s whole order-to-push walk, driven over
four scratch projects of its own rather than Remedy's own repository, each judged by its own
test command (or told plainly that it names none) instead of by Remedy's `pytest`.
"""

from __future__ import annotations

import venv as venv_mod
from pathlib import Path

import pytest

from packages.orchestration.do_sequence import do_contract_summary_line
from packages.orchestration.project_tests import NO_CHECK_RAN_WORDS
from tests.cli.test_do_commit_flags import _bare_upstream, _pushes, _run
from tests.cli.test_do_sequence_cli import _git, no_model_call  # noqa: F401 — fixture by name

COMMIT_MESSAGE = "Add the contributing guide"


def _new_project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """An UNREGISTERED git repository of its own in a fresh `tmp_path`, as the `repo`
    fixture of `tests/cli/test_do_sequence_cli.py` builds one."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    target = tmp_path / "target"
    target.mkdir()
    _git(target, "init", "-q")
    _git(target, "config", "user.email", "t@e.com")
    _git(target, "config", "user.name", "T")
    _git(target, "config", "commit.gpgsign", "false")
    monkeypatch.chdir(target)
    return target


def _commit(repo: Path, message: str) -> None:
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", message)


def _build_python_venv(repo: Path) -> None:
    """A `.venv` with a module only it holds, and a `.pth` naming the folder that holds the
    outer interpreter's own `pytest` package — the same recipe
    `tests/orchestration/test_dod_runners.py` uses to make the venv's `python -m pytest`
    runnable without a `pip install`."""
    venv_mod.EnvBuilder(with_pip=False, symlinks=True).create(repo / ".venv")
    [site] = list((repo / ".venv" / "lib").glob("python3*/site-packages"))
    (site / "only_in_project_venv.py").write_text("VALUE = 42\n")
    (site / "remedy-pytest.pth").write_text(
        str(Path(pytest.__file__).parent.parent) + "\n")


def _one_criterion(data: dict) -> dict:
    [criterion] = data["contract"]["criteria"]
    return criterion


def test_a_python_project_with_its_own_venv_is_judged_by_its_own_pytest_and_pushed(
        tmp_path, monkeypatch, capsys):
    """T004 (1): the planner's criterion is met by the project's own `.venv`, never Remedy's."""
    from packages.orchestration.dod_gate import load_gate_result

    repo = _new_project(tmp_path, monkeypatch)
    (repo / "pyproject.toml").write_text('[project]\nname = "target"\nversion = "0.1.0"\n')
    (repo / ".gitignore").write_text(".venv/\n")
    (repo / "tests").mkdir()
    (repo / "tests" / "test_dep.py").write_text(
        "import only_in_project_venv\n\n\n"
        "def test_dep():\n    assert only_in_project_venv.VALUE == 42\n")
    _commit(repo, "init")
    _build_python_venv(repo)
    _bare_upstream(repo)

    code, data, err = _run(capsys, "--commit", COMMIT_MESSAGE, "--push")

    assert code == 0, (err, data)
    [job_id] = data["job_ids"]
    criterion = _one_criterion(data)
    assert criterion["status"] == "met"
    assert criterion["check"]["kind"] == "project_tests"
    result = load_gate_result(job_id)
    [check] = result["checks"]
    assert check["command"].startswith(f"{repo / '.venv' / 'bin' / 'python'} -m pytest")
    assert len(_pushes(repo)) == 1
    push = data["push"]
    assert push["open_blocking_criteria"] == []
    assert push["unchecked_blocking_criteria"] == []


def test_a_node_project_run_by_npm_test_is_judged_by_it_and_pushed(tmp_path, monkeypatch, capsys):
    """T004 (2): `npm test` judges a Node project exactly as the project's own pytest does."""
    import json as json_mod

    from packages.orchestration.dod_gate import load_gate_result

    repo = _new_project(tmp_path, monkeypatch)
    (repo / "package.json").write_text(json_mod.dumps(
        {"name": "target", "version": "0.1.0", "private": True,
         "scripts": {"test": "node --test"}}) + "\n")
    (repo / "test").mkdir()
    (repo / "test" / "sum.test.js").write_text(
        "const test = require('node:test');\n"
        "const assert = require('node:assert');\n\n"
        "test('sum', () => { assert.strictEqual(1 + 1, 2); });\n")
    _commit(repo, "init")
    _bare_upstream(repo)

    code, data, err = _run(capsys, "--commit", COMMIT_MESSAGE, "--push")

    assert code == 0, (err, data)
    [job_id] = data["job_ids"]
    criterion = _one_criterion(data)
    assert criterion["status"] == "met"
    result = load_gate_result(job_id)
    [check] = result["checks"]
    assert check["command"] == "npm test"
    assert len(_pushes(repo)) == 1


def test_a_project_with_no_test_command_reads_unchecked_and_pushes_anyway(
        tmp_path, monkeypatch, capsys):
    """T004 (3): DECISION F299 D2 — nothing ran, so the criterion is neither met nor unmet,
    and the push goes through, naming it instead of refusing it."""
    from apps.cli.grouped import main as job_main

    repo = _new_project(tmp_path, monkeypatch)
    (repo / "README.md").write_text("# target\n")
    _commit(repo, "init")
    _bare_upstream(repo)

    code, data, err = _run(capsys, "--commit", COMMIT_MESSAGE, "--push")

    assert code == 0, (err, data)
    [job_id] = data["job_ids"]
    criterion = _one_criterion(data)
    assert criterion["status"] == "unchecked"
    assert data["unmet_blocking_criteria"] == []
    push = data["push"]
    assert push["unchecked_blocking_criteria"] == [criterion["id"]]
    assert len(_pushes(repo)) == 1

    from packages.orchestration.dod_gate import load_gate_result

    result = load_gate_result(job_id)
    assert result["released"] is True
    [check] = result["checks"]
    assert check["check_id"] in result["not_run"]

    from tests.cli.test_do_sequence_cli import _step

    assert NO_CHECK_RAN_WORDS in _step(data, "apply")["detail"]
    assert NO_CHECK_RAN_WORDS in do_contract_summary_line(data["contract"])

    job_main(["job", "show", job_id, "--full"])
    shown = capsys.readouterr()
    assert NO_CHECK_RAN_WORDS in shown.err


def test_a_python_projects_own_failing_test_refuses_the_push(tmp_path, monkeypatch, capsys):
    """T004 (4): F270's rule, unchanged — a criterion that really is unmet refuses the push,
    even though the check that found it is the project's own, not Remedy's."""
    repo = _new_project(tmp_path, monkeypatch)
    (repo / "pyproject.toml").write_text('[project]\nname = "target"\nversion = "0.1.0"\n')
    (repo / ".gitignore").write_text(".venv/\n")
    (repo / "tests").mkdir()
    (repo / "tests" / "test_dep.py").write_text(
        "import only_in_project_venv\n\n\n"
        "def test_dep():\n    assert only_in_project_venv.VALUE == 0\n")
    _commit(repo, "init")
    _build_python_venv(repo)
    _bare_upstream(repo)

    code, data, err = _run(capsys, "--commit", COMMIT_MESSAGE, "--push")

    assert code == 1, (err, data)
    criterion = _one_criterion(data)
    assert criterion["status"] == "unmet"
    assert _pushes(repo) == []
    assert "are unmet, so nothing is pushed" in data["push"]["error"]
