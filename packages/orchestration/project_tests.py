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
  3. ``go test ./...`` for a Go module (``go.mod``) and ``cargo test --offline``
     for a Rust package (``Cargo.toml``), before the tests folder, because a
     Rust crate's ``tests`` folder holds Rust integration tests (exec-1018);
     either is ``unrunnable`` when its dependencies are not vendored, since the
     tool sandbox gives no network to fetch them, and the check then says so;
  4. the pytest argv for the selector ``tests``, under the project's own
     interpreter, when a ``tests`` folder exists;
  5. none of the above: no test command, and the caller refuses the check
     rather than judging it.

R-1236: when the check runs in a job's worktree, the configured command, the
virtual environment and the node tools are read from the repository's own
checkout (``base_lookup_dirs``), never from the worktree, whose files the job
itself writes; and ``changed_source_file`` names the file a found command came
from when the job's copy of it differs from the checkout's, so the caller
refuses to judge a command the job wrote.
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
PROJECT_TEST_SOURCES = ("config", "package_json", "go_module", "cargo_manifest", "tests_folder")

#: The file each source reads its command from; the tests folder's argv is Remedy's own.
PROJECT_TEST_SOURCE_FILES = {"config": CONFIG_RELPATH, "package_json": Path("package.json")}


class ProjectTestConfigError(ValueError):
    """The `[tests]` table of `.remedy/config.toml` cannot be used."""


#: `source` is one of `PROJECT_TEST_SOURCES` — which of D1 (2)'s places found `argv`.
@dataclass(frozen=True)
class ProjectTestCommand:
    """One found test command: its argv, which source found it, and why it cannot run ("" when it can).

    *unrunnable* names a known command that the tool sandbox cannot run as it stands (a Go or Rust
    project whose dependencies are not vendored needs the network): the check refuses it with that
    reason, so the verification reads not run, never failed and never passed.
    """

    argv: tuple[str, ...]
    source: str
    unrunnable: str = ""


#: No source named a command — the caller refuses the check rather than judging it.
NO_TEST_COMMAND_MESSAGE = (
    "the project names no test command: no 'command' in the [tests] table of "
    "its .remedy/config.toml, no 'test' script in its package.json and no "
    "'tests' folder, so no check ran"
)

#: DECISION F299 D2 (4): the one phrase every surface that shows an `unchecked`
#: criterion or check says, so the words never drift between them.
NO_CHECK_RAN_WORDS = "no check ran, because the project names no test command"


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


def base_lookup_dirs(cwd: Path) -> tuple[Path, ...]:
    """Where a check reads a project's interpreter, tools and configured command (R-1236).

    The repository's own checkout when `cwd` is a job's worktree, the last of
    `project_lookup_dirs`, and never the worktree, whose files the job itself
    writes; `cwd` alone when it is no job's worktree.
    """
    return project_lookup_dirs(cwd)[-1:]


def changed_source_file(cwd: Path, command: ProjectTestCommand) -> str:
    """The file *command* came from, when the job's worktree holds it different from the checkout.

    Empty for the tests folder's argv, which Remedy builds itself, and when `cwd`
    is no job's worktree. A file present on one side only counts as changed
    (R-1236), except a file the checkout keeps out of git (operator amendment
    amend1027-green-builds: an untracked `.remedy/config.toml`), which the worktree
    never holds and the job therefore never wrote.
    """
    relpath = PROJECT_TEST_SOURCE_FILES.get(command.source)
    [base] = base_lookup_dirs(cwd)
    if relpath is None or base == cwd:
        return ""
    mine, theirs = cwd / relpath, base / relpath
    if not mine.exists() and theirs.is_file() and not _tracked(cwd, relpath):
        return ""
    if (mine.read_bytes() if mine.is_file() else None) != (theirs.read_bytes() if theirs.is_file() else None):
        return str(relpath)
    return ""


def _tracked(cwd: Path, relpath: Path) -> bool:
    """Whether git tracks RELPATH in CWD's work tree (a missing git or any failure reads tracked)."""
    try:
        done = subprocess.run(["git", "ls-files", "--error-unmatch", "--", str(relpath)], cwd=str(cwd),
                              capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return True
    return done.returncode == 0


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
    virtual environment was found. Both are read where `base_lookup_dirs`
    says, never in a job's worktree (R-1236).
    """
    dirs = base_lookup_dirs(cwd)
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


#: Operator amendment amend1027-green-builds: the two further keys of the `[tests]` table. `env`
#: names variables the project's tests read (universe-chat's `UNIVERSE_TEST_KIT`), `read_only_paths`
#: the folders outside the project they read (a sibling repository), both read from the
#: repository's own checkout, never from a job's worktree (R-1236).
PROJECT_TESTS_ENV_KEY = "env"
PROJECT_TESTS_READ_ONLY_KEY = "read_only_paths"


@dataclass(frozen=True)
class ProjectTestSettings:
    """The `[tests]` table's `env` and `read_only_paths`, checked; both empty when unset."""

    env: tuple[tuple[str, str], ...] = ()
    read_only_paths: tuple[str, ...] = ()


def read_test_settings(cwd: Path) -> ProjectTestSettings:
    """`env` and `read_only_paths` of the `[tests]` table where `base_lookup_dirs` says.

    Raises :class:`ProjectTestConfigError` when either key has the wrong shape: `env` a table of
    strings with names of letters, digits and underscores, none of them a key the exec guard
    forbids (`FORBIDDEN_ENV_KEYS`) or a loader's (`LD_*`, `DYLD_*`), `read_only_paths` a list of absolute paths of existing
    folders that are neither the root, the home nor one of its ancestors.
    """
    from packages.orchestration.exec_guard import FORBIDDEN_ENV_KEYS

    table = _tests_table(base_lookup_dirs(cwd)[0])
    env = table.get(PROJECT_TESTS_ENV_KEY, {})
    if not isinstance(env, dict) or not all(
            isinstance(k, str) and k.replace("_", "a").isalnum() and isinstance(v, str)
            and k not in FORBIDDEN_ENV_KEYS and not k.startswith(("LD_", "DYLD_"))
            for k, v in env.items()):
        raise ProjectTestConfigError(
            f"{CONFIG_RELPATH}: [{PROJECT_TESTS_TABLE}].{PROJECT_TESTS_ENV_KEY} must be a table "
            f"of strings, got {env!r}")
    paths = table.get(PROJECT_TESTS_READ_ONLY_KEY, [])
    home = Path(os.path.expanduser("~")).resolve()
    if not isinstance(paths, list) or not all(
            isinstance(p, str) and os.path.isabs(p) and Path(p).is_dir()
            and Path(p).resolve() not in (Path("/"), home, *home.parents) for p in paths):
        raise ProjectTestConfigError(
            f"{CONFIG_RELPATH}: [{PROJECT_TESTS_TABLE}].{PROJECT_TESTS_READ_ONLY_KEY} must list "
            f"absolute paths of existing folders, never the root, the home or above, got {paths!r}")
    return ProjectTestSettings(env=tuple(sorted(env.items())),
                               read_only_paths=tuple(str(Path(p).resolve()) for p in paths))


#: The placeholder an `env` value may hold for the job's workspace (the worktree a check runs in).
WORKSPACE_PLACEHOLDER = "{workspace}"


def project_test_env(cwd: Path, workspace: Path, path: str | None = None) -> dict[str, str]:
    """The `[tests]` table's `env` with `WORKSPACE_PLACEHOLDER` replaced by WORKSPACE, so a value
    names the job's own copy of the project, never the checkout; raises like `read_test_settings`.

    A `PATH` in the table is put IN FRONT of PATH, the one the command would otherwise get, never in
    its place, so the builder and a check keep their own tools.
    """
    env = {key: value.replace(WORKSPACE_PLACEHOLDER, str(workspace))
           for key, value in read_test_settings(cwd).env}
    if "PATH" in env and path:
        env["PATH"] = os.pathsep.join([env["PATH"], path])
    return env


def project_sandbox_read_paths(cwd: Path) -> tuple[str, ...]:
    """The folders a project's test command reads inside the tool sandbox, read-only.

    The checkout's `node_modules`, whose `.bin` tools link into it and which a job's worktree
    below the checkout resolves its packages from, and the `[tests]` table's `read_only_paths`.
    """
    node_bin = find_node_bin(base_lookup_dirs(cwd))
    extra = (str(node_bin.parent.resolve()),) if node_bin is not None else ()
    return (*extra, *read_test_settings(cwd).read_only_paths)


#: The cache folders of a project's `node_modules` that its test tools write (Vite bundles its
#: config into `.vite-temp`, Vitest caches under `.vite`); inside the sandbox each is a scratch folder.
NODE_SCRATCH_DIRNAMES = (".vite-temp", ".vite", ".cache")


def project_sandbox_scratch_dirs(cwd: Path) -> tuple[str, ...]:
    """The checkout's `node_modules` cache folders, created when missing so they can be mounted over."""
    node_bin = find_node_bin(base_lookup_dirs(cwd))
    if node_bin is None:
        return ()
    found = []
    for name in NODE_SCRATCH_DIRNAMES:
        folder = node_bin.parent / name
        try:
            folder.mkdir(exist_ok=True)
        except OSError:
            continue
        found.append(str(folder.resolve()))
    return tuple(found)


def project_tool_environment(cwd: Path, path: str) -> dict[str, str]:
    """The environment a builder runs the project's tools under (amend1027 A2).

    `PATH` is the project's virtual environment's `bin` and its `node_modules/.bin`, each when
    found where `base_lookup_dirs` says, then *path*; `VIRTUAL_ENV` when a virtual environment
    was found; and the `[tests]` table's `env` (`project_test_env` of *cwd*), whose `PATH` goes in
    front. A table that cannot be read adds no variable.
    """
    dirs = base_lookup_dirs(cwd)
    venv, node_bin = find_virtualenv(dirs), find_node_bin(dirs)
    front = [str(d) for d in (venv / "bin" if venv else None, node_bin) if d is not None]
    env = {"PATH": os.pathsep.join([*front, path] if path else front)}
    if venv is not None:
        env["VIRTUAL_ENV"] = str(venv)
    try:
        env.update(project_test_env(cwd, cwd, env["PATH"]))
    except ProjectTestConfigError:
        pass
    return env


def project_python(cwd: Path, default: str) -> str:
    """The virtual environment's `bin/python` where `base_lookup_dirs` says, else `default`."""
    venv = find_virtualenv(base_lookup_dirs(cwd))
    return str(venv / "bin" / "python") if venv is not None else default


def read_configured_command(cwd: Path) -> tuple[str, ...] | None:
    """The `command` the `[tests]` table of `.remedy/config.toml` names.

    `None` when the file is absent, has no `[tests]` table, or the table has
    no `command`. Raises :class:`ProjectTestConfigError` when the file is not
    readable TOML, when `tests` is not a table, or when `command` is not a
    non-empty list of non-empty strings.
    """
    command = _tests_table(cwd).get(PROJECT_TESTS_KEY)
    if command is None:
        return None
    if (not isinstance(command, list) or not command
            or not all(isinstance(item, str) and item for item in command)):
        raise ProjectTestConfigError(
            f"{CONFIG_RELPATH}: [{PROJECT_TESTS_TABLE}].{PROJECT_TESTS_KEY} must be "
            f"a non-empty list of non-empty strings, got {command!r}")
    return tuple(command)


def _tests_table(cwd: Path) -> dict:
    """The `[tests]` table of *cwd*'s `.remedy/config.toml`; {} when the file or the table is absent.

    Raises :class:`ProjectTestConfigError` when the file is not readable TOML or `tests` is no table.
    """
    path = cwd / CONFIG_RELPATH
    if not path.is_file():
        return {}
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ProjectTestConfigError(
            f"{CONFIG_RELPATH} is not readable TOML: {exc}") from exc
    table = data.get(PROJECT_TESTS_TABLE, {})
    if not isinstance(table, dict):
        raise ProjectTestConfigError(
            f"{CONFIG_RELPATH}: [{PROJECT_TESTS_TABLE}] must be a table, "
            f"got {type(table).__name__}")
    return table


def find_project_test_command(cwd: Path, python: str) -> ProjectTestCommand | None:
    """The project's own test command, DECISION F299 D1 (2)'s order.

    The configured command, source `config`; else `("npm", "test")`, source
    `package_json`, when `cwd / "package.json"` parses as a JSON object whose
    `scripts` object has a non-blank `test` string that is not the npm
    placeholder (a file that does not parse counts as having no such
    script); else, when `cwd / "tests"` is a folder, the pytest argv for the
    selector `tests` under the project's own interpreter, source
    `tests_folder`; else `None`. A :class:`ProjectTestConfigError` from the
    first source propagates. The configured command is read where
    `base_lookup_dirs` says, never from a job's worktree (R-1236).
    """
    configured = read_configured_command(base_lookup_dirs(cwd)[0])
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

    if (cwd / "go.mod").is_file():
        return _go_test_command(cwd)
    if (cwd / "Cargo.toml").is_file():
        return _cargo_test_command(cwd)

    if (cwd / "tests").is_dir():
        return ProjectTestCommand(
            argv=(python, "-m", "pytest", "-p", "no:cacheprovider", "tests", "-q"),
            source="tests_folder")

    return None


#: Why a Go or Rust check cannot run in the sandbox as it stands.
NEEDS_NETWORK_WORDS = ("its dependencies are not vendored, and the tool sandbox gives no network to "
                       "fetch them")


def _go_test_command(cwd: Path) -> ProjectTestCommand:
    """`go test ./...` for the module at *cwd*; vendored dependencies run with `-mod=vendor`."""
    try:
        text = (cwd / "go.mod").read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        text = ""
    requires = any(line.strip().startswith("require") for line in text.splitlines())
    if (cwd / "vendor" / "modules.txt").is_file():
        return ProjectTestCommand(argv=("go", "test", "-mod=vendor", "./..."), source="go_module")
    return ProjectTestCommand(argv=("go", "test", "./..."), source="go_module",
                              unrunnable=f"go.mod requires modules: {NEEDS_NETWORK_WORDS}" if requires else "")


def _cargo_test_command(cwd: Path) -> ProjectTestCommand:
    """`cargo test --offline` for the package at *cwd*, unrunnable when it depends on crates not vendored."""
    argv = ("cargo", "test", "--offline")
    try:
        manifest = tomllib.loads((cwd / "Cargo.toml").read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        return ProjectTestCommand(argv=argv, source="cargo_manifest",
                                  unrunnable=f"Cargo.toml cannot be read ({exc})")
    depends = any(manifest.get(table) for table in ("dependencies", "dev-dependencies", "build-dependencies"))
    vendored = (cwd / "vendor").is_dir() and (cwd / ".cargo" / "config.toml").is_file()
    return ProjectTestCommand(argv=argv, source="cargo_manifest",
                              unrunnable=f"Cargo.toml depends on crates: {NEEDS_NETWORK_WORDS}"
                              if depends and not vendored else "")
