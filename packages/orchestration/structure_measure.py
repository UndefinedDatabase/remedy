"""The repository's structure measure: every oversized Python function and tracked text file
(F300 T001, DECISION F300 D1).

`remedy integrity structure` prints what this module measures; F300 T002's ratchet test and
F301's upkeep jobs on every project Remedy builds read the same measure the same way. It assumes
nothing about Remedy's own layout — a folder, two line limits and a git repository are all it
needs — and it writes no file: every function here reads a working tree once and returns.
"""

from __future__ import annotations

import ast
import os
import subprocess
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from packages.orchestration.worktrees import GIT_QUERY_TIMEOUT_SEC, WorktreeError, repo_root

#: Function-length default: Remedy's own registration measured by it at the F300 claim
#: (DECISION F300 D1).
DEFAULT_FUNCTION_LIMIT = 100

#: File-length default: Remedy's own registration measured by it at the F300 claim
#: (DECISION F300 D1).
DEFAULT_FILE_LIMIT = 1000


class NotAGitRepository(ValueError):
    """Raised when the folder given to `measure_repository` is not inside a git repository."""


@dataclass(frozen=True)
class FunctionSize:
    """One Python function above its limit: its dotted name, where it starts and how long it is."""

    path: str
    name: str
    line: int
    lines: int


@dataclass(frozen=True)
class FileSize:
    """One tracked text file above its limit: its path and its line count."""

    path: str
    lines: int


@dataclass(frozen=True)
class StructureMeasure:
    """One repository's structure, measured at the limits it was asked for."""

    root: str
    function_limit: int
    file_limit: int
    files_measured: int
    functions_measured: int
    large_functions: tuple[FunctionSize, ...]
    large_files: tuple[FileSize, ...]
    unparsed: tuple[str, ...]


def count_lines(text: str) -> int:
    """`text`'s line count, counting a last line with no trailing newline as one more."""
    return text.count("\n") + (1 if text and not text.endswith("\n") else 0)


class _FunctionVisitor(ast.NodeVisitor):
    """Walks a module's syntax tree in pre-order, naming each function by its enclosing scopes."""

    def __init__(self, path: str) -> None:
        self._path = path
        self._scope: list[str] = []
        self._seen: dict[str, int] = {}
        self.functions: list[FunctionSize] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._scope.append(node.name)
        self.generic_visit(node)
        self._scope.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._record(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._record(node)

    def _record(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        base = ".".join((*self._scope, node.name))
        seen = self._seen.get(base, 0) + 1
        self._seen[base] = seen
        name = base if seen == 1 else f"{base}#{seen}"
        self.functions.append(FunctionSize(
            path=self._path, name=name, line=node.lineno,
            lines=node.end_lineno - node.lineno + 1,
        ))
        self._scope.append(node.name)
        self.generic_visit(node)
        self._scope.pop()


def function_sizes(source: str, path: str) -> list[FunctionSize]:
    """Every function `source`'s syntax tree holds, in pre-order. `SyntaxError`/`ValueError` reach the caller."""
    tree = ast.parse(source)
    visitor = _FunctionVisitor(path)
    visitor.visit(tree)
    return visitor.functions


def tracked_files(folder: Path, paths: Sequence[str] = ()) -> list[str]:
    """Every path git tracks under `folder` (optionally restricted to `paths`), sorted."""
    proc = subprocess.run(
        ["git", "ls-files", "-z", "--full-name", "--", *paths],
        cwd=str(folder), capture_output=True, timeout=GIT_QUERY_TIMEOUT_SEC,
    )
    if proc.returncode != 0:
        raise NotAGitRepository(f"{folder} is not a git repository: {proc.stderr!r}")
    return sorted(os.fsdecode(entry) for entry in proc.stdout.split(b"\0") if entry)


def measure_repository(
    folder: Path,
    *,
    function_limit: int = DEFAULT_FUNCTION_LIMIT,
    file_limit: int = DEFAULT_FILE_LIMIT,
    paths: Sequence[str] = (),
) -> StructureMeasure:
    """Measure every tracked text file and Python function `folder`'s git repository holds."""
    if function_limit < 1 or file_limit < 1:
        raise ValueError(
            f"function_limit and file_limit must each be at least 1, got {function_limit} and {file_limit}"
        )
    try:
        top = repo_root(folder)
    except (WorktreeError, OSError) as exc:
        raise NotAGitRepository(str(exc)) from exc

    files_measured = 0
    functions_measured = 0
    large_functions: list[FunctionSize] = []
    large_files: list[FileSize] = []
    unparsed: list[str] = []

    for rel in tracked_files(folder, paths):
        full = top / rel
        if full.is_symlink() or not full.is_file():
            continue
        try:
            data = full.read_bytes()
        except OSError:
            continue
        if b"\0" in data:
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue

        files_measured += 1
        lines = count_lines(text)
        if lines > file_limit:
            large_files.append(FileSize(path=rel, lines=lines))

        if rel.endswith(".py"):
            try:
                functions = function_sizes(text, rel)
            except (SyntaxError, ValueError):
                unparsed.append(rel)
            else:
                functions_measured += len(functions)
                large_functions.extend(f for f in functions if f.lines > function_limit)

    large_functions.sort(key=lambda f: (-f.lines, f.path, f.name))
    large_files.sort(key=lambda f: (-f.lines, f.path))

    return StructureMeasure(
        root=str(top),
        function_limit=function_limit,
        file_limit=file_limit,
        files_measured=files_measured,
        functions_measured=functions_measured,
        large_functions=tuple(large_functions),
        large_files=tuple(large_files),
        unparsed=tuple(unparsed),
    )


def measure_as_dict(measure: StructureMeasure) -> dict[str, object]:
    """`measure`, shaped exactly as `remedy integrity structure --json` answers it."""
    return {
        "root": measure.root,
        "limits": {"function_lines": measure.function_limit, "file_lines": measure.file_limit},
        "files_measured": measure.files_measured,
        "functions_measured": measure.functions_measured,
        "large_functions": [
            {"path": f.path, "name": f.name, "line": f.line, "lines": f.lines}
            for f in measure.large_functions
        ],
        "large_files": [{"path": f.path, "lines": f.lines} for f in measure.large_files],
        "unparsed": list(measure.unparsed),
    }


def render_measure(measure: StructureMeasure) -> list[str]:
    """`measure`, as the lines `remedy integrity structure` prints without `--json`."""
    lines = [
        f"Measured {measure.files_measured} tracked text files and {measure.functions_measured} "
        f"Python functions in {measure.root}.",
        f"Functions above {measure.function_limit} lines: {len(measure.large_functions)}",
    ]
    lines.extend(f"  {f.lines:>6}  {f.path}:{f.line}  {f.name}" for f in measure.large_functions)
    lines.append(f"Files above {measure.file_limit} lines: {len(measure.large_files)}")
    lines.extend(f"  {f.lines:>6}  {f.path}" for f in measure.large_files)
    if measure.unparsed:
        lines.append(f"Python files whose syntax tree could not be read: {len(measure.unparsed)}")
        lines.extend(f"  {p}" for p in measure.unparsed)
    return lines
