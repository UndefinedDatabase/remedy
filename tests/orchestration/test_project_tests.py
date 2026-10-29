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
    changed_source_file,
    find_node_bin,
    find_project_test_command,
    find_virtualenv,
    project_environment,
    project_lookup_dirs,
    project_python,
    project_sandbox_read_paths,
    project_sandbox_scratch_dirs,
    project_test_env,
    project_tool_environment,
    read_configured_command,
    read_test_settings,
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



@pytest.mark.parametrize(("files", "argv", "source", "runnable"), [
    ({"go.mod": "module x\n\ngo 1.22\n"}, ("go", "test", "./..."), "go_module", True),
    ({"go.mod": "module x\n\ngo 1.22\n\nrequire github.com/a/b v1.0.0\n"}, ("go", "test", "./..."),
     "go_module", False),                                  # needs the network the sandbox does not give
    ({"go.mod": "module x\nrequire github.com/a/b v1.0.0\n", "vendor/modules.txt": "# github.com/a/b\n"},
     ("go", "test", "-mod=vendor", "./..."), "go_module", True),
    # A Rust crate's tests folder holds Rust integration tests: cargo, never pytest.
    ({"Cargo.toml": "[package]\nname = 'x'\nversion = '0.1.0'\n", "tests/it.rs": "#[test] fn t() {}\n"},
     ("cargo", "test", "--offline"), "cargo_manifest", True),
    ({"Cargo.toml": "[package]\nname = 'x'\nversion = '0.1.0'\n[dependencies]\nserde = '1'\n"},
     ("cargo", "test", "--offline"), "cargo_manifest", False),
    ({"Cargo.toml": "[package\n"}, ("cargo", "test", "--offline"), "cargo_manifest", False),
])
def test_go_and_rust_projects_get_their_standard_test_command_or_say_why_not(tmp_path: Path, files, argv,
                                                                              source, runnable):
    """exec-1018: the language-standard test command, honestly unrunnable when the sandbox cannot run it."""
    for rel, text in files.items():
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text(text)

    command = find_project_test_command(tmp_path, "python3")

    assert command is not None and (command.argv, command.source) == (argv, source)
    assert (command.unrunnable == "") is runnable

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


def test_a_virtualenv_and_node_bin_only_in_the_worktree_are_never_the_checks_own(
        checkout: Path, worktree: Path):
    """R-1236: the job writes its worktree, so a planted interpreter or tool there is not used."""
    _make_venv(worktree / ".venv")
    (worktree / "node_modules" / ".bin").mkdir(parents=True)
    assert project_python(worktree, "default-python") == "default-python"
    assert project_environment(worktree) == {}

    _make_venv(checkout / ".venv")
    assert project_python(worktree, "default-python") == str(checkout / ".venv" / "bin" / "python")
    assert project_environment(worktree)["VIRTUAL_ENV"] == str(checkout / ".venv")


def test_in_a_worktree_the_configured_command_is_read_from_the_checkout(
        checkout: Path, worktree: Path):
    """R-1236: the worktree's `.remedy/config.toml` never names the command; the checkout's does."""
    _write_config(checkout, '[tests]\ncommand = ["make", "check"]\n')
    _write_config(worktree, '[tests]\ncommand = ["python", "-c", "pass"]\n')
    assert find_project_test_command(worktree, "python3") == ProjectTestCommand(
        argv=("make", "check"), source="config")


def test_a_source_file_the_job_changed_is_named_and_an_unchanged_one_is_not(
        checkout: Path, worktree: Path):
    """R-1236: the config, or the package.json a command came from, differing from the checkout's."""
    config = ProjectTestCommand(argv=("make", "check"), source="config")
    npm = ProjectTestCommand(argv=("npm", "test"), source="package_json")
    folder = ProjectTestCommand(argv=("python3", "-m", "pytest"), source="tests_folder")
    assert changed_source_file(worktree, config) == ""

    _write_config(worktree, '[tests]\ncommand = ["python", "-c", "pass"]\n')
    assert changed_source_file(worktree, config) == ".remedy/config.toml"
    _write_config(checkout, '[tests]\ncommand = ["python", "-c", "pass"]\n')
    assert changed_source_file(worktree, config) == ""

    (worktree / "package.json").write_text('{"scripts": {"test": "true"}}', encoding="utf-8")
    assert changed_source_file(worktree, npm) == "package.json"
    assert changed_source_file(worktree, folder) == ""
    assert changed_source_file(checkout, npm) == ""


def test_lookup_dirs_of_a_folder_outside_any_repository_is_itself_alone(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    folder = tmp_path / "lonely"
    folder.mkdir()
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    assert project_lookup_dirs(folder) == (folder,)


def _config(repo: Path, text: str) -> None:
    (repo / ".remedy").mkdir(exist_ok=True)
    (repo / ".remedy" / "config.toml").write_text(text)


class TestTheTestSettings:
    """amend1027: the [tests] table's env and read_only_paths, and where a check reads them."""

    def test_unset_keys_read_empty(self, tmp_path):
        assert read_test_settings(tmp_path).env == () and read_test_settings(tmp_path).read_only_paths == ()

    def test_env_and_read_only_paths_are_read(self, tmp_path):
        kit = tmp_path / "kit"
        kit.mkdir()
        repo = tmp_path / "repo"
        repo.mkdir()
        _config(repo, f'[tests]\nenv = {{ KIT = "{kit}" }}\nread_only_paths = ["{kit}"]\n')
        settings = read_test_settings(repo)
        assert settings.env == (("KIT", str(kit)),)
        assert settings.read_only_paths == (str(kit.resolve()),)
        assert project_sandbox_read_paths(repo) == (str(kit.resolve()),)
        assert project_tool_environment(repo, "/usr/bin") == {"PATH": "/usr/bin", "KIT": str(kit)}

    @pytest.mark.parametrize("line", [
        'env = { "A-B" = "x" }', 'env = { A = 1 }', 'env = "A=1"', 'env = { LD_PRELOAD = "x" }', 'read_only_paths = ["relative"]',
        'read_only_paths = ["/"]', 'read_only_paths = ["/no/such/folder/amend1027"]',
        'read_only_paths = "/tmp"'])
    def test_a_wrong_shape_is_refused(self, tmp_path, line):
        _config(tmp_path, f"[tests]\n{line}\n")
        with pytest.raises(ProjectTestConfigError):
            read_test_settings(tmp_path)

    def test_the_home_is_never_a_read_only_path(self, tmp_path):
        _config(tmp_path, f'[tests]\nread_only_paths = ["{os.path.expanduser("~")}"]\n')
        with pytest.raises(ProjectTestConfigError):
            read_test_settings(tmp_path)

    def test_a_node_project_shares_its_packages_and_cache_folders(self, tmp_path):
        (tmp_path / "node_modules" / ".bin").mkdir(parents=True)
        assert project_sandbox_read_paths(tmp_path) == (str((tmp_path / "node_modules").resolve()),)
        scratch = project_sandbox_scratch_dirs(tmp_path)
        assert [Path(d).name for d in scratch] == [".vite-temp", ".vite", ".cache"]
        assert all(Path(d).is_dir() for d in scratch)
        env = project_tool_environment(tmp_path, "/usr/bin")
        assert env["PATH"].split(os.pathsep) == [str(tmp_path / "node_modules" / ".bin"), "/usr/bin"]


class TestTheWorkspacePlaceholderAndPath:
    """amend1027: `{workspace}` names the job's copy; a table's PATH goes in front, never in place."""

    def test_the_placeholder_names_the_workspace_and_path_goes_in_front(self, tmp_path):
        _config(tmp_path, '[tests]\nenv = { ROOT = "{workspace}/sub", PATH = "/opt/tool/bin" }\n')
        env = project_test_env(tmp_path, Path("/w/job-1"), "/usr/bin")
        assert env == {"ROOT": "/w/job-1/sub", "PATH": "/opt/tool/bin:/usr/bin"}
        assert project_tool_environment(tmp_path, "/usr/bin")["PATH"] == "/opt/tool/bin:/usr/bin"

    def test_an_untracked_config_only_the_checkout_holds_is_no_change_of_the_job(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        _git(repo, "init", "-q")
        _git(repo, "config", "user.email", "t@e.com")
        _git(repo, "config", "user.name", "T")
        (repo / "README.md").write_text("x\n")
        _git(repo, "add", "-A")
        _git(repo, "commit", "-qm", "init")
        (repo / ".git" / "info" / "exclude").write_text(".remedy/\n.remedy-wt/\n")
        _config(repo, '[tests]\ncommand = ["make", "check"]\n')
        wt = repo / ".remedy-wt" / "job-1"
        _git(repo, "worktree", "add", "-q", "--detach", str(wt))
        command = ProjectTestCommand(argv=("make", "check"), source="config")
        assert changed_source_file(wt, command) == ""
        _config(wt, '[tests]\ncommand = ["true"]\n')                  # the job writes its own
        assert changed_source_file(wt, command) == ".remedy/config.toml"


# ---------------------------------------------------------------------------
# F322 — a Python project's tests import the job's worktree, never the checkout
# ---------------------------------------------------------------------------

def test_a_python_worktrees_source_comes_first_on_pythonpath(checkout: Path, worktree: Path):
    # Jobs of 2026-10-28: the editable install made the worktree's pytest import the checkout.
    _make_venv(checkout / ".venv")
    (worktree / "pyproject.toml").write_text("[project]\nname = 'demo'\n")
    (worktree / "src").mkdir()
    want = os.pathsep.join([str(worktree / "src"), str(worktree)])
    assert project_environment(worktree)["PYTHONPATH"] == want
    assert project_tool_environment(worktree, "/usr/bin")["PYTHONPATH"] == want


def test_the_checkout_itself_and_a_non_python_worktree_get_no_pythonpath(checkout: Path, worktree: Path):
    _make_venv(checkout / ".venv")
    (checkout / "pyproject.toml").write_text("[project]\nname = 'demo'\n")
    assert "PYTHONPATH" not in project_environment(checkout)
    assert "PYTHONPATH" not in project_environment(worktree)     # the worktree has no pyproject.toml
