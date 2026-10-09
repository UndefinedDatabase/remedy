"""F299 T002 — finding a project's own test command and its own environment.

DECISION F299 D1 (2) and (3): the order a command is found in, and where its
environment is found. Every test here builds its project under `tmp_path`;
none drives a job or a provider.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

from packages.orchestration.project_tests import (
    NPM_PLACEHOLDER_MARK,
    ProjectTestCommand,
    ProjectTestConfigError,
    find_node_bin,
    find_project_test_command,
    find_virtualenv,
    project_environment,
    project_lookup_dirs,
    project_python,
    read_configured_command,
)


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=str(repo), capture_output=True,
                          text=True, check=True).stdout


def _make_venv(path: Path) -> None:
    """A folder shaped exactly like a virtual environment: `pyvenv.cfg` + `bin/python`."""
    (path / "bin").mkdir(parents=True)
    (path / "pyvenv.cfg").write_text("home = /usr\n")
    python_bin = path / "bin" / "python"
    python_bin.write_text("#!/bin/sh\n")
    python_bin.chmod(0o755)


def _write_config(cwd: Path, body: str) -> Path:
    conf = cwd / ".remedy"
    conf.mkdir(parents=True, exist_ok=True)
    path = conf / "config.toml"
    path.write_text(body, encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# find_project_test_command — the order
# ---------------------------------------------------------------------------

def test_config_beats_package_json_beats_tests_folder_beats_none(tmp_path: Path):
    cwd = tmp_path
    (cwd / "tests").mkdir()
    (cwd / "package.json").write_text(
        json.dumps({"scripts": {"test": "jest"}}), encoding="utf-8")
    conf = _write_config(cwd, '[tests]\ncommand = ["make", "check"]\n')

    assert find_project_test_command(cwd, "python3") == ProjectTestCommand(
        argv=("make", "check"), source="config")

    conf.unlink()
    assert find_project_test_command(cwd, "python3") == ProjectTestCommand(
        argv=("npm", "test"), source="package_json")

    (cwd / "package.json").unlink()
    assert find_project_test_command(cwd, "python3") == ProjectTestCommand(
        argv=("python3", "-m", "pytest", "-p", "no:cacheprovider", "tests", "-q"),
        source="tests_folder")

    shutil.rmtree(cwd / "tests")
    assert find_project_test_command(cwd, "python3") is None


def test_npm_placeholder_blank_script_and_unparseable_json_read_as_no_script(
        tmp_path: Path):
    (tmp_path / "tests").mkdir()
    pkg = tmp_path / "package.json"

    pkg.write_text(json.dumps({"scripts": {"test": NPM_PLACEHOLDER_MARK}}),
                   encoding="utf-8")
    assert find_project_test_command(tmp_path, "python3").source == "tests_folder"

    pkg.write_text(json.dumps({"scripts": {"test": "   "}}), encoding="utf-8")
    assert find_project_test_command(tmp_path, "python3").source == "tests_folder"

    pkg.write_text("{not valid json", encoding="utf-8")
    assert find_project_test_command(tmp_path, "python3").source == "tests_folder"


def test_the_tests_folder_argv_matches_dod_runners_pytest_argv(tmp_path: Path):
    """D1 (5)'s pin that Remedy's checks on Remedy are unchanged."""
    from packages.orchestration import dod_runners
    from packages.orchestration.dod_schema import DoDCheck

    (tmp_path / "tests").mkdir()
    command = find_project_test_command(tmp_path, dod_runners.PYTEST_PYTHON)

    check = DoDCheck(id="c1", kind="pytest", spec={"selector": "tests"},
                     source="plan_acceptance")
    assert list(command.argv) == dod_runners._pytest_argv(check)


# ---------------------------------------------------------------------------
# read_configured_command
# ---------------------------------------------------------------------------

def test_absent_file_and_no_tests_table_give_none(tmp_path: Path):
    assert read_configured_command(tmp_path) is None

    _write_config(tmp_path, '[runtime]\ncmd = ["x"]\n')
    assert read_configured_command(tmp_path) is None


def test_a_string_command_is_refused(tmp_path: Path):
    _write_config(tmp_path, '[tests]\ncommand = "pytest"\n')
    with pytest.raises(ProjectTestConfigError) as exc:
        read_configured_command(tmp_path)
    assert ".remedy/config.toml" in str(exc.value)


def test_an_empty_list_command_is_refused(tmp_path: Path):
    _write_config(tmp_path, "[tests]\ncommand = []\n")
    with pytest.raises(ProjectTestConfigError) as exc:
        read_configured_command(tmp_path)
    assert ".remedy/config.toml" in str(exc.value)


def test_a_list_holding_a_number_is_refused(tmp_path: Path):
    _write_config(tmp_path, "[tests]\ncommand = [1]\n")
    with pytest.raises(ProjectTestConfigError) as exc:
        read_configured_command(tmp_path)
    assert ".remedy/config.toml" in str(exc.value)


def test_broken_toml_is_refused(tmp_path: Path):
    _write_config(tmp_path, "[tests\n")
    with pytest.raises(ProjectTestConfigError) as exc:
        read_configured_command(tmp_path)
    assert ".remedy/config.toml" in str(exc.value)


# ---------------------------------------------------------------------------
# The environment: a real git worktree of a committed repository
# ---------------------------------------------------------------------------

@pytest.fixture
def checkout(tmp_path: Path) -> Path:
    root = tmp_path / "checkout"
    root.mkdir()
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@e.com")
    _git(root, "config", "user.name", "T")
    _git(root, "config", "commit.gpgsign", "false")
    (root / "README.md").write_text("# repo\n")
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "init")
    return root


@pytest.fixture
def worktree(checkout: Path, tmp_path: Path) -> Path:
    path = tmp_path / "wt"
    _git(checkout, "worktree", "add", str(path), "-b", "wt-branch")
    return path


def test_a_virtualenv_only_in_the_checkout_is_found_from_the_worktree(
        checkout: Path, worktree: Path):
    _make_venv(checkout / ".venv")
    dirs = project_lookup_dirs(worktree)
    assert find_virtualenv(dirs) == checkout / ".venv"


def test_a_virtualenv_in_the_worktree_wins_over_the_checkouts(
        checkout: Path, worktree: Path):
    _make_venv(checkout / ".venv")
    _make_venv(worktree / ".venv")
    dirs = project_lookup_dirs(worktree)
    assert find_virtualenv(dirs) == worktree / ".venv"


def test_venv_dirname_is_found_when_dot_venv_is_absent(worktree: Path):
    _make_venv(worktree / "venv")
    dirs = project_lookup_dirs(worktree)
    assert find_virtualenv(dirs) == worktree / "venv"


def test_a_folder_without_pyvenv_cfg_is_not_a_virtualenv(worktree: Path):
    (worktree / ".venv" / "bin").mkdir(parents=True)
    (worktree / ".venv" / "bin" / "python").write_text("#!/bin/sh\n")
    dirs = project_lookup_dirs(worktree)
    assert find_virtualenv(dirs) is None


def test_node_modules_bin_only_in_the_checkout_is_found_from_the_worktree(
        checkout: Path, worktree: Path):
    node_bin = checkout / "node_modules" / ".bin"
    node_bin.mkdir(parents=True)
    dirs = project_lookup_dirs(worktree)
    assert find_node_bin(dirs) == node_bin


def test_project_environment_orders_venv_then_node_then_the_old_path(
        checkout: Path, worktree: Path):
    venv = checkout / ".venv"
    _make_venv(venv)
    node_bin = checkout / "node_modules" / ".bin"
    node_bin.mkdir(parents=True)
    old_path = os.environ.get("PATH", "")

    env = project_environment(worktree)

    assert env["PATH"] == os.pathsep.join(
        [str(venv / "bin"), str(node_bin), old_path])
    assert env["VIRTUAL_ENV"] == str(venv)


def test_project_environment_is_empty_with_neither(worktree: Path):
    assert project_environment(worktree) == {}


def test_project_python_is_the_virtualenvs_interpreter_else_the_default(
        checkout: Path, worktree: Path):
    assert project_python(worktree, "default-python") == "default-python"
    venv = checkout / ".venv"
    _make_venv(venv)
    assert project_python(worktree, "default-python") == str(venv / "bin" / "python")


def test_lookup_dirs_of_a_folder_outside_any_repository_is_itself_alone(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    folder = tmp_path / "lonely"
    folder.mkdir()
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    assert project_lookup_dirs(folder) == (folder,)
