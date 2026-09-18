"""F269 T003 — the check that measures a contract's three hygiene criteria.

DECISION F269 D5.  Every contract template carries three blocking criteria —
no file is added that nothing references, replaced code is never left beside
its replacement, no stub or TODO body survives the job — and each one is
measured by one rule of this module:

* ``unreferenced`` — an added code file that no other file of the tree names
  by its stem (D5 (2));
* ``replaced`` — an added file whose name, less one marker such as ``_v2`` or
  ``.bak``, is a file that still exists beside it (D5 (3));
* ``stubs`` — a ``TODO``/``FIXME``/``XXX`` line, or a Python function whose
  body is only ``pass``, ``...`` or ``raise NotImplementedError``, among the
  lines the job added (D5 (4)).

The rules are pure over a root and the lists of files; the command line
``python3 -m packages.orchestration.contract_hygiene <rule>`` measures those
lists with ``git`` from the current directory — added means untracked and not
ignored, or added in the index, against ``HEAD`` — and exits 0 on no finding,
1 on findings and 2 when it cannot measure, so a tree it cannot read is a red
check, never a met criterion.  It runs as an F061 ``custom_cmd`` check, whose
executable allowlist holds ``python3`` and not ``git``.

Standard library only: the check runs in whatever worktree a job leaves.
"""

from __future__ import annotations

import ast
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

#: The three rule names, in the order the templates list their criteria.
HYGIENE_RULES = ("unreferenced", "replaced", "stubs")

EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_CANNOT_MEASURE = 2

#: The files the rules judge as code (D5 (1)).
CODE_FILE_SUFFIXES = (".py", ".js", ".jsx", ".ts", ".tsx")

#: How much of each file ``unreferenced`` reads when it looks for a reference.
REFERENCE_READ_LIMIT_BYTES = 1024 * 1024

#: Entry-point and packaging files nothing is expected to name (D5 (2)).
UNREFERENCED_EXEMPT_NAMES = frozenset({"__init__.py", "__main__.py", "conftest.py", "setup.py"})
_TEST_DIRECTORY_NAMES = frozenset({"tests", "test"})

_REPLACED_STEM_SUFFIX_RE = re.compile(r"^(?P<base>.+?)(?:_new|_old|_copy|_backup|_bak|_v\d+)$")
_REPLACED_PREFIXES = ("new_", "old_")
_REPLACED_TRAILERS = (".bak", ".orig")

_STUB_MARKER_RE = re.compile(r"\b(?:TODO|FIXME|XXX)\b")
_STUB_EXEMPT_DECORATORS = frozenset({"abstractmethod", "overload"})

_HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(?P<start>\d+)(?:,(?P<count>\d+))? @@")


class HygieneMeasureError(RuntimeError):
    """The tree could not be measured: not a git work tree, or ``git`` failed."""


@dataclass(frozen=True)
class HygieneFinding:
    """One rule violation; ``line`` is 0 when the finding is about the whole file."""

    rule: str
    path: str
    message: str
    line: int = 0

    def render(self) -> str:
        where = f"{self.path}:{self.line}" if self.line else self.path
        return f"{where}: {self.rule}: {self.message}"


@dataclass(frozen=True)
class WorkTreeChanges:
    """What a job did to a tree, relative to ``root``, as posix paths.

    ``added`` are the files the job created; ``changed`` maps each file it
    modified to the line numbers it added there; ``tree`` is every file of the
    tree — tracked or added, not ignored — that exists on disk.
    """

    root: Path
    added: tuple[str, ...] = ()
    changed: dict[str, frozenset[int]] = field(default_factory=dict)
    tree: tuple[str, ...] = ()


def is_code_file(path: str) -> bool:
    return path.endswith(CODE_FILE_SUFFIXES)


def is_unreferenced_exempt(path: str) -> bool:
    """An entry-point file or a test file: nothing is expected to name it (D5 (2))."""
    pure = PurePosixPath(path)
    name = pure.name
    if name in UNREFERENCED_EXEMPT_NAMES:
        return True
    if name.startswith("test_") or name.endswith("_test.py"):
        return True
    if ".test." in name or ".spec." in name:
        return True
    return any(part in _TEST_DIRECTORY_NAMES for part in pure.parts[:-1])


def _read_text(root: Path, rel: str, limit: int | None = None) -> str | None:
    try:
        with open(root / rel, "rb") as handle:
            data = handle.read() if limit is None else handle.read(limit)
    except OSError:
        return None
    return data.decode("utf-8", errors="replace")


def find_unreferenced_files(root: Path, added: list[str] | tuple[str, ...],
                            tree: list[str] | tuple[str, ...]) -> list[HygieneFinding]:
    """Added code files no OTHER file of ``tree`` names by stem (D5 (2)).

    A file's own text never counts: a module that names itself is still a
    module nothing else reaches.
    """
    candidates = [p for p in sorted(set(added)) if is_code_file(p) and not is_unreferenced_exempt(p)]
    if not candidates:
        return []
    texts: dict[str, str] = {}
    for rel in sorted(set(tree) | set(added)):
        text = _read_text(root, rel, REFERENCE_READ_LIMIT_BYTES)
        if text is not None:
            texts[rel] = text
    findings: list[HygieneFinding] = []
    for path in candidates:
        stem = PurePosixPath(path).stem
        pattern = re.compile(r"(?<!\w)" + re.escape(stem) + r"(?!\w)")
        referenced = any(pattern.search(text) for rel, text in texts.items() if rel != path)
        if not referenced:
            findings.append(HygieneFinding(
                "unreferenced", path, "an added file that no other file references"))
    return findings


def replaced_originals(path: str) -> list[str]:
    """The paths ``path`` would replace: its name less one replacement marker (D5 (3))."""
    pure = PurePosixPath(path)
    name = pure.name
    names: list[str] = []
    for trailer in _REPLACED_TRAILERS:
        if name.endswith(trailer) and len(name) > len(trailer):
            names.append(name[:-len(trailer)])
    match = _REPLACED_STEM_SUFFIX_RE.match(pure.stem)
    if match:
        names.append(match.group("base") + pure.suffix)
    for prefix in _REPLACED_PREFIXES:
        if name.startswith(prefix) and len(name) > len(prefix):
            names.append(name[len(prefix):])
    return [str(pure.with_name(n)) for n in names]


def find_replaced_files(root: Path, added: list[str] | tuple[str, ...]) -> list[HygieneFinding]:
    """Added files that sit beside the file they replace (D5 (3))."""
    findings: list[HygieneFinding] = []
    for path in sorted(set(added)):
        for original in replaced_originals(path):
            if original != path and (root / original).is_file():
                findings.append(HygieneFinding(
                    "replaced", path, f"added beside {original}, which it replaces"))
                break
    return findings


def _decorator_name(node: ast.expr) -> str:
    if isinstance(node, ast.Call):
        node = node.func
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Name):
        return node.id
    return ""


def _is_stub_statement(stmt: ast.stmt) -> bool:
    if isinstance(stmt, ast.Pass):
        return True
    if (isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant)
            and stmt.value.value is Ellipsis):
        return True
    if isinstance(stmt, ast.Raise) and stmt.exc is not None:
        exc = stmt.exc.func if isinstance(stmt.exc, ast.Call) else stmt.exc
        return isinstance(exc, ast.Name) and exc.id == "NotImplementedError"
    return False


def _is_stub_function(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if any(_decorator_name(d) in _STUB_EXEMPT_DECORATORS for d in node.decorator_list):
        return False
    body = list(node.body)
    if (body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant)
            and isinstance(body[0].value.value, str)):
        body = body[1:]
    return len(body) == 1 and _is_stub_statement(body[0])


def find_stubs(root: Path, added: list[str] | tuple[str, ...],
               changed: dict[str, frozenset[int]]) -> list[HygieneFinding]:
    """Stub markers and stub bodies among the lines the job added (D5 (4))."""
    findings: list[HygieneFinding] = []
    added_set = set(added)
    for path in sorted(added_set | set(changed)):
        if not is_code_file(path):
            continue
        text = _read_text(root, path)
        if text is None:
            continue
        lines = text.splitlines()
        if path in added_set:
            new_lines = frozenset(range(1, len(lines) + 1))
        else:
            new_lines = changed[path]
        for number in sorted(new_lines):
            if 0 < number <= len(lines) and _STUB_MARKER_RE.search(lines[number - 1]):
                findings.append(HygieneFinding(
                    "stubs", path, "a TODO, FIXME or XXX marker", number))
        if not path.endswith(".py"):
            continue
        try:
            module = ast.parse(text)
        except (SyntaxError, ValueError):
            continue
        for node in ast.walk(module):
            if (isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and node.lineno in new_lines and _is_stub_function(node)):
                findings.append(HygieneFinding(
                    "stubs", path, f"function {node.name} has a stub body", node.lineno))
    return sorted(findings, key=lambda f: (f.path, f.line, f.message))


def run_hygiene_rule(rule: str, changes: WorkTreeChanges) -> list[HygieneFinding]:
    """Apply one of :data:`HYGIENE_RULES` to measured changes."""
    if rule == "unreferenced":
        return find_unreferenced_files(changes.root, changes.added, changes.tree)
    if rule == "replaced":
        return find_replaced_files(changes.root, changes.added)
    if rule == "stubs":
        return find_stubs(changes.root, changes.added, changes.changed)
    raise ValueError(f"unknown hygiene rule {rule!r}; the rules are {', '.join(HYGIENE_RULES)}")


# ── measuring a git work tree ──────────────────────────────────────────────


def _git(cwd: Path, *args: str) -> str:
    # Optional locks off: measuring must never write the index of a live worktree.
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
    try:
        done = subprocess.run(["git", "-c", "core.quotePath=false", *args], cwd=str(cwd),
                              capture_output=True, text=True, env=env, check=False)
    except OSError as exc:
        raise HygieneMeasureError(f"git could not run: {exc}") from exc
    if done.returncode != 0:
        raise HygieneMeasureError(
            f"git {' '.join(args)} exited {done.returncode}: {done.stderr.strip()}")
    return done.stdout


def _nul_list(output: str) -> list[str]:
    return [item for item in output.split("\0") if item]


def _added_lines_by_file(diff: str) -> dict[str, frozenset[int]]:
    changed: dict[str, set[int]] = {}
    current: str | None = None
    for line in diff.splitlines():
        if line.startswith("+++ "):
            target = line[4:]
            current = target[2:] if target.startswith("b/") else None
            if current is not None:
                changed.setdefault(current, set())
            continue
        match = _HUNK_RE.match(line)
        if match and current is not None:
            start = int(match.group("start"))
            count = int(match.group("count")) if match.group("count") is not None else 1
            changed[current].update(range(start, start + count))
    return {path: frozenset(lines) for path, lines in changed.items()}


def measure_work_tree(cwd: Path | str) -> WorkTreeChanges:
    """What the uncommitted work in the git work tree at ``cwd`` changed against ``HEAD``."""
    cwd = Path(cwd)
    if _git(cwd, "rev-parse", "--is-inside-work-tree").strip() != "true":
        raise HygieneMeasureError(f"{cwd} is not inside a git work tree")
    root = Path(_git(cwd, "rev-parse", "--show-toplevel").strip())
    untracked = _nul_list(_git(root, "ls-files", "-z", "--others", "--exclude-standard"))
    staged_new = _nul_list(_git(root, "diff", "--cached", "--name-only", "-z", "--no-renames",
                                "--diff-filter=A", "HEAD"))
    tracked = _nul_list(_git(root, "ls-files", "-z"))
    modified = _added_lines_by_file(_git(root, "diff", "-U0", "--no-color", "--no-ext-diff",
                                         "--no-renames", "--diff-filter=M", "HEAD"))
    added = tuple(sorted(p for p in set(untracked) | set(staged_new) if (root / p).is_file()))
    tree = tuple(sorted(p for p in set(tracked) | set(added) if (root / p).is_file()))
    changed = {p: lines for p, lines in modified.items() if p not in added}
    return WorkTreeChanges(root=root, added=added, changed=changed, tree=tree)


def main(argv: list[str] | None = None) -> int:
    """``contract_hygiene <rule>``: print one line per finding; exit 0, 1 or 2."""
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1 or args[0] not in HYGIENE_RULES:
        print(f"usage: python3 -m packages.orchestration.contract_hygiene "
              f"{{{','.join(HYGIENE_RULES)}}}", file=sys.stderr)
        return EXIT_CANNOT_MEASURE
    try:
        changes = measure_work_tree(Path.cwd())
    except HygieneMeasureError as exc:
        print(f"contract hygiene {args[0]}: cannot measure: {exc}", file=sys.stderr)
        return EXIT_CANNOT_MEASURE
    findings = run_hygiene_rule(args[0], changes)
    for finding in findings:
        print(finding.render())
    return EXIT_FINDINGS if findings else EXIT_CLEAN


if __name__ == "__main__":
    sys.exit(main())
