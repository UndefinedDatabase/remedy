"""F329 (operator order beweis): Remedy narrows its own test run to the changed parts.

decodeux's order beweis: for a pytest project only the test folder of each source folder the diff
touches runs, plus every test file the diff names; for a Vitest project only the test files that
import a changed file or are named like it; otherwise the full run. The full run stays the default
when the diff touches more than ten source folders. The check says in its evidence which selection
it made (`CheckEvidence.selection`).

The diff is the job's worktree against the job's base commit (`project_test_baseline.
job_base_commit`, else `HEAD`), with the files git does not track yet. Remedy deliberately runs the
full command whenever it cannot be sure the narrowed one covers the change: a changed `conftest.py`,
a changed file that is neither source, test nor prose (configuration, data, a lock file), a command
the project configured itself, a test script that is not Vitest alone, or a selection that comes
out empty.
"""
from __future__ import annotations

import json
import posixpath
import re
import subprocess
from pathlib import Path, PurePosixPath
from typing import Any

#: More source folders than this in the diff, and the full run stays (his word: „mehr als zehn“).
MAX_NARROWED_SOURCE_FOLDERS = 10
#: Changed files that never decide a test run: prose.
_PROSE_SUFFIXES = (".md", ".rst", ".txt")
#: The suffixes of Vitest's source and test files.
_JS_SUFFIXES = (".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".mts", ".cts", ".vue", ".svelte")
#: A Vitest test file: `name.test.ts`, `name.spec.tsx`, ...
_JS_TEST = re.compile(r"^(?P<stem>.+)\.(?:test|spec)\.[cm]?[jt]sx?$")
#: The module a JS/TS file imports or requires, as written.
_JS_IMPORT = re.compile(r"""(?:\bfrom\s*|\bimport\s*\(?\s*|\brequire\s*\(\s*)["'](\.{1,2}/[^"']+)["']""")
#: Folders never searched for Vitest test files.
_SKIPPED_DIRS = {"node_modules", ".git", "dist", "build", "coverage"}


def full_run_sentence(why: str) -> str:
    """The evidence's sentence for a full run, with WHY."""
    return f"full run: {why}"


def _git_lines(cwd: Path, *args: str) -> list[str]:
    done = subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True, timeout=60)
    if done.returncode != 0:
        raise OSError(done.stderr.strip()[:300] or f"git {args[0]} failed")
    return [line for line in done.stdout.splitlines() if line.strip()]


def changed_paths(cwd: Path) -> list[str] | None:
    """The files the job changed under CWD, relative to it, or None when git cannot say."""
    from packages.orchestration.project_test_baseline import job_base_commit

    try:
        base = job_base_commit(cwd) or "HEAD"
        tracked = _git_lines(cwd, "diff", "--name-only", "--relative", base, "--")
        untracked = _git_lines(cwd, "ls-files", "--others", "--exclude-standard")
    except (OSError, subprocess.TimeoutExpired):
        return None
    return sorted(set(tracked) | set(untracked))


def _is_pytest_file(path: PurePosixPath) -> bool:
    return path.suffix == ".py" and (path.name.startswith("test_") or path.stem.endswith("_test"))


def _pytest_selection(cwd: Path, changed: list[str]) -> tuple[list[str], str]:
    """The pytest selectors for CHANGED, or [] with the reason for a full run."""
    folders: set[str] = set()
    selected: set[str] = set()
    for raw in changed:
        path = PurePosixPath(raw)
        if path.suffix in _PROSE_SUFFIXES:
            continue
        if path.name == "conftest.py" or path.suffix != ".py":
            return [], f"the diff changes {raw}, which every test may read"
        if path.parts[0] == "tests":
            if _is_pytest_file(path) and (cwd / path).is_file():
                selected.add(raw)
            continue
        folders.add(str(path.parent))
    if len(folders) > MAX_NARROWED_SOURCE_FOLDERS:
        return [], f"the diff touches {len(folders)} source folders, more than {MAX_NARROWED_SOURCE_FOLDERS}"
    for folder in folders:
        parts = PurePosixPath(folder).parts
        for candidate in (PurePosixPath("tests", *parts), PurePosixPath("tests", *parts[1:])):
            if candidate != PurePosixPath("tests") and (cwd / candidate).is_dir():
                selected.add(str(candidate))
                break
    kept = sorted(s for s in selected if not any(s.startswith(f"{o}/") for o in selected if o != s))
    return kept, "" if kept else "no test folder or test file belongs to the diff"


def _js_test_files(cwd: Path) -> list[PurePosixPath]:
    found = []
    for path in cwd.rglob("*"):
        rel = path.relative_to(cwd)
        if not _SKIPPED_DIRS.intersection(rel.parts) and _JS_TEST.match(path.name) and path.is_file():
            found.append(PurePosixPath(rel.as_posix()))
    return sorted(found)


def _without_suffix(path: PurePosixPath) -> str:
    return str(path.with_suffix("")).removesuffix("/index")


def _imports(cwd: Path, test: PurePosixPath) -> set[str]:
    """The project-relative modules (without suffix) TEST imports by a relative path."""
    try:
        text = (cwd / test).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return set()
    out = set()
    for spec in _JS_IMPORT.findall(text):
        target = posixpath.normpath(posixpath.join(str(test.parent), spec))
        module = PurePosixPath(target)
        out.add(_without_suffix(module) if module.suffix in _JS_SUFFIXES else target.removesuffix("/index"))
    return out


def _vitest_selection(cwd: Path, changed: list[str]) -> tuple[list[str], str]:
    """The Vitest test files for CHANGED, or [] with the reason for a full run."""
    sources: list[PurePosixPath] = []
    selected: set[str] = set()
    for raw in changed:
        path = PurePosixPath(raw)
        if path.suffix in _PROSE_SUFFIXES:
            continue
        if path.suffix not in _JS_SUFFIXES:
            return [], f"the diff changes {raw}, which every test may read"
        if _JS_TEST.match(path.name):
            if (cwd / path).is_file():
                selected.add(raw)
        else:
            sources.append(path)
    folders = {str(path.parent) for path in sources}
    if len(folders) > MAX_NARROWED_SOURCE_FOLDERS:
        return [], f"the diff touches {len(folders)} source folders, more than {MAX_NARROWED_SOURCE_FOLDERS}"
    if sources:
        stems = {path.name.split(".")[0] for path in sources}
        modules = {_without_suffix(path) for path in sources}
        for test in _js_test_files(cwd):
            match = _JS_TEST.match(test.name)
            if (match and match.group("stem") in stems) or modules & _imports(cwd, test):
                selected.add(str(test))
    kept = sorted(selected)
    return kept, "" if kept else "no test file imports or is named like a changed file"


def _vitest_script(cwd: Path) -> bool:
    """True when the project's `test` script is Vitest alone, so files appended reach Vitest."""
    try:
        script = json.loads((cwd / "package.json").read_text(encoding="utf-8"))["scripts"]["test"]
    except (OSError, ValueError, KeyError, TypeError):
        return False
    return isinstance(script, str) and re.fullmatch(r"vitest(?: run)?(?: --run)?", script.strip()) is not None


def narrowed_test_argv(command: Any, cwd: Path, diff_cwd: Path | None = None) -> tuple[list[str], str]:
    """COMMAND's argv narrowed to the changed parts of DIFF_CWD (CWD by default), and the sentence
    the evidence keeps; the full argv with the sentence why when nothing narrows it."""
    argv = list(command.argv)
    if command.source == "tests_folder":
        kind, pick = "pytest", _pytest_selection
    elif command.source == "package_json" and _vitest_script(cwd):
        kind, pick = "vitest", _vitest_selection
    else:
        return argv, full_run_sentence(f"Remedy narrows only pytest and Vitest, not {command.source}")
    changed = changed_paths(diff_cwd or cwd)
    if changed is None:
        return argv, full_run_sentence("git could not name the changed files")
    if not changed:
        return argv, full_run_sentence("the diff changes no file")
    chosen, why = pick(diff_cwd or cwd, changed)
    if not chosen:
        return argv, full_run_sentence(why)
    if kind == "pytest":
        at = argv.index("tests")
        narrowed = argv[:at] + chosen + argv[at + 1:]
    else:
        narrowed = argv + ["--", *chosen]
    return narrowed, f"{kind} narrowed to {len(chosen)} of the diff's parts: {', '.join(chosen)}"
