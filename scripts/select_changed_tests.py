#!/usr/bin/env python3
"""The test files that own what a change touched — the selection of the change-aware fast lane.

Reads the changed paths (``--base REF``: committed since the merge base with REF, plus staged,
unstaged and untracked files; or the paths given as arguments) and prints one test file per line:

- a changed test file itself;
- for a changed module under ``packages/`` or ``apps/``: every test file that imports it
  (``import a.b``, ``from a.b import x``, ``from a import b``, at any depth of the file), found by
  a static AST index of ``tests/`` — no test is imported or run to build it;
- for a changed module under ``apps/cli/``: also the tests of the dispatch boundary
  (``apps.cli.grouped``, ``apps.cli.commands.do_cmd``), because a handler is mostly reached
  through dispatch or a CLI subprocess, which no import names;
- for a changed file under ``docs/``: every test file under ``tests/docs/``, the documentation
  checks, which read the tree rather than name one page;
- for any changed file: every test file whose text names its repository path as a whole path
  (not as the tail of a longer one), or names its file name in quotes when no other tracked file
  has that name (``SCRIPTS / "remedy_test_fast.sh"``), which is how the guards over scripts,
  docs and workflow files find what they read. A shared name such as ``README.md`` is matched
  by its whole path only.

Remedy deliberately does NOT pretend a selection exists for a change to the test machinery
itself: ``tests/conftest.py``, ``tests/load_governor.py``, ``pyproject.toml``, ``constraints.txt``
and the pytest runner scripts change every test, so such a change exits 3 naming the path, and
the caller runs the full lane. It deliberately follows no import chain past the test files'
own imports either: measured on 2026-10-17, one hop of production importers from a module such
as ``pi_provider`` or ``order_scope`` already reaches the ``pingpong_job`` hub and selects 424 to
469 of the 775 test files, about 60 percent of the suite's CPU, so the neighbours of a change ARE
the full suite, which stays the gate at merge and release.

Exit codes: 0 a selection was printed (possibly empty); 2 bad arguments or git failed; 3 the
change touches the test machinery, so only the full suite answers.

Usage: python3 scripts/select_changed_tests.py --base origin/main
       python3 scripts/select_changed_tests.py packages/orchestration/pi_provider.py
"""
from __future__ import annotations

import argparse
import ast
import collections
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
#: Paths whose change reaches every test, so no owner selection can answer for them.
TEST_MACHINERY_PATHS = frozenset({
    "tests/conftest.py", "tests/load_governor.py", "pyproject.toml", "constraints.txt",
    "scripts/remedy_pytest.sh", "scripts/remedy_pytest_runner.py",
})
#: The modules a CLI handler is reached through when no test imports the handler itself.
CLI_DISPATCH_MODULES = ("apps.cli.grouped", "apps.cli.commands.do_cmd")
GIT_TIMEOUT_SEC = 30


def changed_paths_since(base: str) -> list[str]:
    """Committed since the merge base with ``base``, plus staged, unstaged and untracked paths."""
    def git(*args: str) -> list[str]:
        out = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True,
                             timeout=GIT_TIMEOUT_SEC, check=True).stdout
        return [line for line in out.splitlines() if line]
    merge_base = git("merge-base", base, "HEAD")[0]
    return sorted(set(git("diff", "--name-only", merge_base))
                  | set(git("ls-files", "--others", "--exclude-standard")))


def tracked_name_counts() -> collections.Counter:
    """How many tracked files carry each file name; empty when git cannot answer."""
    try:
        out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, text=True,
                             timeout=GIT_TIMEOUT_SEC, check=True).stdout
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError):
        return collections.Counter()
    return collections.Counter(Path(rel).name for rel in out.split("\0") if rel)


def module_name_of(path: str) -> str | None:
    """``packages/a/b.py`` -> ``packages.a.b``; a package's ``__init__.py`` names the package."""
    p = Path(path)
    if p.suffix != ".py" or p.parts[0] not in ("packages", "apps"):
        return None
    parts = list(p.with_suffix("").parts)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def imported_modules(source: str) -> set[str]:
    """Every dotted name a file imports, ``from a import b`` counted as both ``a`` and ``a.b``."""
    names: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
            names.add(node.module)
            names.update(f"{node.module}.{alias.name}" for alias in node.names)
    return names


def index_tests(files: list[Path]) -> dict[str, tuple[set[str], str]]:
    """Repository-relative path -> (the dotted names it imports, its text).

    An unparsable file imports nothing but keeps its text. A file that vanishes between the
    listing and the read is left out: a running test may write a scratch test file into
    ``tests/`` and remove it again (measured 2026-10-17, ``test_resource_safety``'s
    ``test_slow_*`` files).
    """
    index: dict[str, tuple[set[str], str]] = {}
    for path in files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except FileNotFoundError:
            continue
        try:
            names = imported_modules(text)
        except SyntaxError:
            names = set()
        index[path.relative_to(ROOT).as_posix()] = (names, text)
    return index


def select_test_files(changed: list[str]) -> list[str]:
    """The owning test files of ``changed``, sorted; see the module docstring for the rules."""
    index = index_tests(sorted((ROOT / "tests").rglob("test_*.py")))
    test_imports = {rel: names for rel, (names, _text) in index.items()}
    test_text = {rel: text for rel, (_names, text) in index.items()}
    owners = {name for name in map(module_name_of, changed) if name}
    if any(name.startswith("apps.cli.") for name in owners):
        owners.update(CLI_DISPATCH_MODULES)
    selected = {rel for rel in changed if rel in test_imports and (ROOT / rel).is_file()}
    selected.update(rel for rel, names in test_imports.items() if names & owners)
    if any(rel.startswith("docs/") for rel in changed):
        selected.update(rel for rel in test_imports if rel.startswith("tests/docs/"))
    names = tracked_name_counts()
    for rel in changed:
        reference = rf"(?<![\w./-]){re.escape(rel)}(?![\w/-])"
        name = Path(rel).name
        if names[name] == 1 and name != rel:
            reference += rf"|[\"']{re.escape(name)}[\"']"
        pattern = re.compile(reference)
        selected.update(t for t, text in test_text.items() if pattern.search(text))
    return sorted(selected)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*", help="changed repository-relative paths")
    parser.add_argument("--base", help="select for everything changed since the merge base with this ref")
    args = parser.parse_args(argv)
    if bool(args.paths) == bool(args.base):
        parser.error("give changed paths or --base, not both")
    try:
        changed = changed_paths_since(args.base) if args.base else list(args.paths)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, IndexError) as exc:
        print(f"select_changed_tests: git could not list the change: {exc}", file=sys.stderr)
        return 2
    machinery = sorted(TEST_MACHINERY_PATHS.intersection(changed))
    if machinery:
        print(f"select_changed_tests: {', '.join(machinery)} changed; only the full suite answers",
              file=sys.stderr)
        return 3
    for rel in select_test_files(changed):
        print(rel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
