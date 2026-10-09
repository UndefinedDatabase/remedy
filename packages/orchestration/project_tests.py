"""F299 T002 — how a check finds a project's own test command and environment.

A mission's acceptance checks on a repository that is not Remedy's own must run
that project's own test command, in that project's own environment, never in
Remedy's (DECISION F299 D1). This module is the one place that answers both
questions; the check kind ``project_tests`` in ``dod_runners`` is its only
caller.

DECISION F299 D1 (2)'s order, tried at run time so a job that adds a project's
first tests is judged by them:
  1. the ``command`` list in the ``[tests]`` table of the project's own
     ``.remedy/config.toml``, the file that already holds its ``[runtime]``
     table;
  2. a ``test`` script in the project's ``package.json`` that is not the
     placeholder ``npm init`` writes;
  3. the pytest argv for the selector ``tests``, under the project's own
     interpreter, when a ``tests`` folder exists;
  4. none of the above: no test command, and the caller refuses the check
     rather than judging it.
"""
from __future__ import annotations

import json
import os
import subprocess
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from packages.runtimes.runtime_config import CONFIG_RELPATH

try:                                   # Python >= 3.11
    import tomllib
except ModuleNotFoundError:            # Python 3.10 with the tomli backport
    import tomli as tomllib  # type: ignore[no-redef]


#: DECISION F299 D1 (2) source 1: the `[tests]` table's own key names.
PROJECT_TESTS_TABLE = "tests"
PROJECT_TESTS_KEY = "command"

#: A `test` script holding this is the one `npm init` writes and names no test.
NPM_PLACEHOLDER_MARK = "Error: no test specified"

#: Virtual environment folder names, tried in this order (DECISION F299 D1 (3)).
VENV_DIRNAMES = (".venv", "venv")

#: Where a found command came from, in DECISION F299 D1 (2)'s order.
PROJECT_TEST_SOURCES = ("config", "package_json", "tests_folder")


class ProjectTestConfigError(ValueError):
    """The `[tests]` table of `.remedy/config.toml` cannot be used."""


#: `source` is one of `PROJECT_TEST_SOURCES` — which of D1 (2)'s three places found `argv`.
@dataclass(frozen=True)
class ProjectTestCommand:
    """One found test command: its argv, and which source found it."""

    argv: tuple[str, ...]
    source: str


#: No source named a command — the caller refuses the check rather than judging it.
NO_TEST_COMMAND_MESSAGE = (
    "the project names no test command: no 'command' in the [tests] table of "
    "its .remedy/config.toml, no 'test' script in its package.json and no "
    "'tests' folder, so no check ran"
)


def project_lookup_dirs(cwd: Path) -> tuple[Path, ...]:
    """Where a project's environment and configuration might live.

    `cwd` first, then the SAME relative place in the repository's own
    checkout when `cwd` is a job's worktree (DECISION F299 D1 (3)): one `git
    rev-parse --show-toplevel --git-common-dir` names both the top of `cwd`'s
    work tree and its common git folder, resolved against `cwd` when relative
    as `worktrees.ensure_ignored` resolves it. When that folder's name is
    `.git`, its parent is the repository's own checkout, and the checkout's
    copy of `cwd`'s own position inside its work tree is added when it
    differs from `cwd` itself. A missing git, a timeout or a non-zero exit —
    `cwd` is not inside a git repository at all — leaves `cwd` as the only
    lookup directory, and no other git call is made.
    """
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "--show-toplevel", "--git-common-dir"],
            cwd=str(cwd), capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return (cwd,)
    if proc.returncode != 0:
        return (cwd,)

    lines = proc.stdout.splitlines()
    if len(lines) < 2:
        return (cwd,)
    top = Path(lines[0])
    common_raw = Path(lines[1])
    common = common_raw if common_raw.is_absolute() else (cwd / common_raw)
    common = common.resolve()
    if common.name != ".git":
        return (cwd,)

    checkout = common.parent
    resolved_cwd = cwd.resolve()
    candidate = checkout / resolved_cwd.relative_to(top.resolve())
    if candidate == resolved_cwd:
        return (cwd,)
    return (cwd, candidate)


def find_virtualenv(dirs: Sequence[Path]) -> Path | None:
    """The first `d / name` holding both `pyvenv.cfg` and `bin/python`.

    Tried over `dirs` in order and `VENV_DIRNAMES` in order, so a virtual
    environment found in the first directory wins outright over any later
    directory's, and `.venv` wins over `venv` within the same directory.
    """
    for d in dirs:
        for name in VENV_DIRNAMES:
            candidate = d / name
            if (candidate / "pyvenv.cfg").is_file() and (candidate / "bin" / "python").is_file():
                return candidate
    return None


def find_node_bin(dirs: Sequence[Path]) -> Path | None:
    """The first `d / "node_modules" / ".bin"` that is a folder."""
    for d in dirs:
        candidate = d / "node_modules" / ".bin"
        if candidate.is_dir():
            return candidate
    return None


def project_environment(cwd: Path) -> dict[str, str]:
    """The environment a project's own test command runs under.

    `{}` when neither a virtual environment nor a `node_modules/.bin` is
    found, so a caller merging this in adds nothing. Otherwise `PATH` is the
    virtual environment's `bin`, then the node folder — each only when
    found — then the parent's own `PATH`, and `VIRTUAL_ENV` is set when a
    virtual environment was found.
    """
    dirs = project_lookup_dirs(cwd)
    venv = find_virtualenv(dirs)
    node_bin = find_node_bin(dirs)
    if venv is None and node_bin is None:
        return {}

    path_parts: list[str] = []
    if venv is not None:
        path_parts.append(str(venv / "bin"))
    if node_bin is not None:
        path_parts.append(str(node_bin))
    path_parts.append(os.environ.get("PATH", ""))

    env = {"PATH": os.pathsep.join(path_parts)}
    if venv is not None:
        env["VIRTUAL_ENV"] = str(venv)
    return env


def project_python(cwd: Path, default: str) -> str:
    """The found virtual environment's `bin/python`, else `default`."""
    venv = find_virtualenv(project_lookup_dirs(cwd))
    return str(venv / "bin" / "python") if venv is not None else default


def read_configured_command(cwd: Path) -> tuple[str, ...] | None:
    """The `command` the `[tests]` table of `.remedy/config.toml` names.

    `None` when the file is absent, has no `[tests]` table, or the table has
    no `command`. Raises :class:`ProjectTestConfigError` when the file is not
    readable TOML, when `tests` is not a table, or when `command` is not a
    non-empty list of non-empty strings.
    """
    path = cwd / CONFIG_RELPATH
    if not path.is_file():
        return None
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ProjectTestConfigError(
            f"{CONFIG_RELPATH} is not readable TOML: {exc}") from exc

    table = data.get(PROJECT_TESTS_TABLE)
    if table is None:
        return None
    if not isinstance(table, dict):
        raise ProjectTestConfigError(
            f"{CONFIG_RELPATH}: [{PROJECT_TESTS_TABLE}] must be a table, "
            f"got {type(table).__name__}")

    command = table.get(PROJECT_TESTS_KEY)
    if command is None:
        return None
    if (not isinstance(command, list) or not command
            or not all(isinstance(item, str) and item for item in command)):
        raise ProjectTestConfigError(
            f"{CONFIG_RELPATH}: [{PROJECT_TESTS_TABLE}].{PROJECT_TESTS_KEY} must be "
            f"a non-empty list of non-empty strings, got {command!r}")
    return tuple(command)


def find_project_test_command(cwd: Path, python: str) -> ProjectTestCommand | None:
    """The project's own test command, DECISION F299 D1 (2)'s order.

    The configured command, source `config`; else `("npm", "test")`, source
    `package_json`, when `cwd / "package.json"` parses as a JSON object whose
    `scripts` object has a non-blank `test` string that is not the npm
    placeholder (a file that does not parse counts as having no such
    script); else, when `cwd / "tests"` is a folder, the pytest argv for the
    selector `tests` under the project's own interpreter, source
    `tests_folder`; else `None`. A :class:`ProjectTestConfigError` from the
    first source propagates.
    """
    configured = read_configured_command(cwd)
    if configured is not None:
        return ProjectTestCommand(argv=configured, source="config")

    package_json = cwd / "package.json"
    if package_json.is_file():
        try:
            data = json.loads(package_json.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            data = None
        if isinstance(data, dict):
            scripts = data.get("scripts")
            if isinstance(scripts, dict):
                test_script = scripts.get("test")
                if (isinstance(test_script, str) and test_script.strip()
                        and NPM_PLACEHOLDER_MARK not in test_script):
                    return ProjectTestCommand(argv=("npm", "test"), source="package_json")

    if (cwd / "tests").is_dir():
        return ProjectTestCommand(
            argv=(python, "-m", "pytest", "-p", "no:cacheprovider", "tests", "-q"),
            source="tests_folder")

    return None
