"""F277 T001 — the run-ledger event vocabulary is a declaration, not a convention.

`RunEvent.event` is a bare `str`, so until now nothing could answer "which event
names does this repository write?" except a full-text search, and nothing at all
could catch a READER comparing against a name no code path writes.  Two such dead
readers had been scoring a permanently-absent readiness dimension since the day
they were written.

This module reads the CODE rather than the prose.  It walks every module under
``packages`` and ``apps`` and collects two sets:

* WRITTEN — every string literal that reaches an event SINK.  A sink is
  ``RunLogWriter.log``, ``event_persistence.emit_important_event`` or
  ``timeline.append_run_event``, plus — by fixpoint — every function that
  forwards its own parameter into a known sink.  That fixpoint is what makes the
  set honest: the repository wraps all three sinks in per-module ``_emit``
  helpers, and the same collector with the fixpoint removed sees 51 of the 83
  written names and reports 15 phantom dead readers.
* READ — every literal compared against an event lookup (``e.get("event") ==
  <literal>``, ``e["event"] in {...}``).

and asserts ``read ⊆ declared`` and ``written ⊆ declared`` against
``packages.orchestration.event_names``.

Deliberate absences:
  * Remedy deliberately does not resolve event names across module boundaries.
    A name assembled from an import, an f-string or a dict lookup is invisible
    here by construction; the declaration module is the place such a name is
    written down, and the strict-mode flag in ``RunLogWriter.log`` is what
    catches one at runtime.
  * Remedy deliberately does not rename any event name.  F277 declares the
    vocabulary that exists (docs/roadmap/features/T2_F277.md, "Do not touch").
"""

from __future__ import annotations

import ast
import pathlib

import pytest

from packages.orchestration.event_names import (
    EVENT_NAMES,
    READ_ONLY_EVENT_NAMES,
    is_declared_event,
)
from packages.orchestration.run_log import STRICT_EVENT_NAMES_ENV, RunLogWriter

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
SOURCE_ROOTS = ("packages", "apps")

#: (owner file or None for a public name, callee name, positional index, keyword).
#: A private helper — one whose name starts with an underscore — is only itself
#: inside its own file: two modules define ``_emit`` with the event at DIFFERENT
#: positions, so matching a private helper by bare name reads the wrong argument.
SEED_SINKS: frozenset[tuple[pathlib.Path | None, str, int | None, str | None]] = frozenset(
    {
        (None, "log", 0, None),
        (None, "emit_important_event", 2, "event"),
        (None, "append_run_event", 2, "event"),
    }
)


def _string_literals(node: ast.AST) -> list[str]:
    """The string literals an expression can denote, without name resolution."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return [node.value]
    if isinstance(node, ast.IfExp):
        return _string_literals(node.body) + _string_literals(node.orelse)
    if isinstance(node, (ast.Tuple, ast.List, ast.Set)):
        out: list[str] = []
        for element in node.elts:
            out.extend(_string_literals(element))
        return out
    return []


def _scope_bindings(scope: ast.AST) -> dict[str, tuple[str, ...]]:
    """``NAME = <string literal>`` assignments made DIRECTLY in one scope.

    Scoped rather than flat on purpose: a flat map lets a sentinel like
    ``state = "unknown"`` in one function resolve an ``{"event": name}`` in
    another, which puts a string that is not an event name into the vocabulary.
    """
    bindings: dict[str, list[str]] = {}
    nested = {
        child
        for node in ast.walk(scope)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        and node is not scope
        for child in ast.walk(node)
    }
    for node in ast.walk(scope):
        if node in nested or not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        if node.value is None:
            continue
        literals = _string_literals(node.value)
        if not literals:
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        for target in targets:
            if isinstance(target, ast.Name):
                bindings.setdefault(target.id, []).extend(literals)
    return {name: tuple(values) for name, values in bindings.items()}


def _callee_name(call: ast.Call) -> str | None:
    if isinstance(call.func, ast.Attribute):
        return call.func.attr
    if isinstance(call.func, ast.Name):
        return call.func.id
    return None


def _event_arguments(call: ast.Call, sinks: set, owner: pathlib.Path) -> list[ast.AST]:
    """EVERY expression this call passes as an event name, over all sinks it matches.

    Returning only the first match reads the wrong argument whenever one callee
    name is registered at two positions.
    """
    name = _callee_name(call)
    if name is None:
        return []
    found: list[ast.AST] = []
    for sink_owner, sink_name, index, keyword in sinks:
        if sink_name != name:
            continue
        if sink_owner is not None and sink_owner != owner:
            continue
        if keyword is not None:
            for passed in call.keywords:
                if passed.arg == keyword and passed.value not in found:
                    found.append(passed.value)
        if index is not None and len(call.args) > index and call.args[index] not in found:
            found.append(call.args[index])
    return found


def _parsed_sources() -> dict[pathlib.Path, ast.Module]:
    trees: dict[pathlib.Path, ast.Module] = {}
    for root in SOURCE_ROOTS:
        for path in sorted((REPO_ROOT / root).rglob("*.py")):
            try:
                trees[path.relative_to(REPO_ROOT)] = ast.parse(
                    path.read_text(encoding="utf-8")
                )
            except SyntaxError:  # pragma: no cover - a broken source is another test's job
                continue
    return trees


def _discover_sinks(trees: dict[pathlib.Path, ast.Module]) -> set:
    """Seed sinks plus every function that forwards its own parameter into one."""
    sinks = set(SEED_SINKS)
    for _ in range(10):
        grew = False
        for path, tree in trees.items():
            for node in ast.walk(tree):
                if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                positional = [a.arg for a in node.args.args]
                parameters = positional + [a.arg for a in node.args.kwonlyargs]
                for call in ast.walk(node):
                    if not isinstance(call, ast.Call):
                        continue
                    for argument in _event_arguments(call, sinks, path):
                        if not isinstance(argument, ast.Name):
                            continue
                        if argument.id not in parameters:
                            continue
                        index = (
                            positional.index(argument.id)
                            if argument.id in positional
                            else None
                        )
                        owner = path if node.name.startswith("_") else None
                        entry = (owner, node.name, index, argument.id)
                        if entry not in sinks:
                            sinks.add(entry)
                            grew = True
        if not grew:
            break
    return sinks


def _is_event_lookup(node: ast.AST) -> bool:
    """True for ``<expr>.get("event"...)`` and ``<expr>["event"]``."""
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "get"
        and node.args
    ):
        first = node.args[0]
        return isinstance(first, ast.Constant) and first.value == "event"
    if isinstance(node, ast.Subscript):
        index = node.slice
        return isinstance(index, ast.Constant) and index.value == "event"
    return False


def collect_event_names() -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    """Walk the tree once and return ``(written, read)``, each name -> its sites."""
    trees = _parsed_sources()
    sinks = _discover_sinks(trees)
    written: dict[str, set[str]] = {}
    read: dict[str, set[str]] = {}

    for path, tree in trees.items():

        def visit(node: ast.AST, chain: tuple[dict[str, tuple[str, ...]], ...]) -> None:
            """Walk one node, resolving names against the enclosing scope chain."""
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                chain = (_scope_bindings(node),) + chain

            def resolve(expression: ast.AST) -> list[str]:
                literals = _string_literals(expression)
                if literals:
                    return literals
                if isinstance(expression, ast.Name):
                    for bindings in chain:
                        if expression.id in bindings:
                            return list(bindings[expression.id])
                return []

            if isinstance(node, ast.Call):
                for argument in _event_arguments(node, sinks, path):
                    for name in resolve(argument):
                        written.setdefault(name, set()).add(str(path))
                for keyword in node.keywords:
                    if keyword.arg == "event":
                        for name in resolve(keyword.value):
                            written.setdefault(name, set()).add(str(path))
            if isinstance(node, ast.Dict):
                for key, value in zip(node.keys, node.values):
                    if isinstance(key, ast.Constant) and key.value == "event":
                        for name in resolve(value):
                            written.setdefault(name, set()).add(str(path))
            if isinstance(node, ast.Compare) and len(node.comparators) == 1:
                left, operator = node.left, node.ops[0]
                if _is_event_lookup(left) and isinstance(
                    operator, (ast.Eq, ast.NotEq, ast.In, ast.NotIn)
                ):
                    for name in resolve(node.comparators[0]):
                        read.setdefault(name, set()).add(str(path))

            for child in ast.iter_child_nodes(node):
                visit(child, chain)

        visit(tree, (_scope_bindings(tree),))
    return written, read


@pytest.fixture(scope="module")
def collected() -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    return collect_event_names()


class TestTheEventVocabularyIsDeclared:
    def test_every_written_event_name_is_declared(self, collected) -> None:
        written, _ = collected
        undeclared = sorted(set(written) - set(EVENT_NAMES))
        assert not undeclared, (
            "these event names are WRITTEN but not declared in "
            "packages/orchestration/event_names.py: "
            + ", ".join(
                f"{name} ({', '.join(sorted(written[name]))})" for name in undeclared
            )
        )

    def test_every_read_event_name_is_declared(self, collected) -> None:
        _, read = collected
        declared = set(EVENT_NAMES) | set(READ_ONLY_EVENT_NAMES)
        undeclared = sorted(set(read) - declared)
        assert not undeclared, (
            "these event names are READ but not declared: "
            + ", ".join(
                f"{name} ({', '.join(sorted(read[name]))})" for name in undeclared
            )
        )

    def test_no_declared_name_is_unused(self, collected) -> None:
        written, read = collected
        unused = sorted(set(EVENT_NAMES) - set(written) - set(read))
        assert not unused, (
            "these names are declared in EVENT_NAMES but neither written nor read; "
            "the declaration must describe the code, not outlive it: "
            + ", ".join(unused)
        )

    def test_a_read_only_name_that_gains_a_writer_leaves_the_quarantine(
        self, collected
    ) -> None:
        """The ratchet: READ_ONLY_EVENT_NAMES may only ever shrink."""
        written, _ = collected
        resurrected = sorted(set(READ_ONLY_EVENT_NAMES) & set(written))
        assert not resurrected, (
            "these names are quarantined in READ_ONLY_EVENT_NAMES as having no "
            "writer, but a writer now exists — move them into EVENT_NAMES: "
            + ", ".join(resurrected)
        )

    def test_every_quarantined_name_really_has_a_reader(self, collected) -> None:
        _, read = collected
        orphans = sorted(set(READ_ONLY_EVENT_NAMES) - set(read))
        assert not orphans, (
            "these names are quarantined as read-but-never-written, but nothing "
            "reads them any more — delete the entry: " + ", ".join(orphans)
        )


class TestTheDeclarationModuleApi:
    def test_is_declared_event_accepts_a_written_name(self) -> None:
        assert is_declared_event("task_run_started")

    def test_is_declared_event_rejects_an_undeclared_name(self) -> None:
        assert not is_declared_event("no_such_event_name_exists")

    def test_the_two_sets_are_disjoint(self) -> None:
        assert not (set(EVENT_NAMES) & set(READ_ONLY_EVENT_NAMES))


class TestStrictModeRejectsAnUndeclaredName:
    """The declaration only bites when something can fail on it."""

    def test_the_writer_accepts_an_undeclared_name_by_default(
        self, tmp_path, monkeypatch
    ) -> None:
        monkeypatch.delenv(STRICT_EVENT_NAMES_ENV, raising=False)
        writer = RunLogWriter("job-default", data_root=tmp_path)
        writer.log("no_such_event_name_exists")
        assert writer.path.read_text(encoding="utf-8").count("\n") == 1

    def test_the_writer_rejects_an_undeclared_name_under_the_flag(
        self, tmp_path, monkeypatch
    ) -> None:
        monkeypatch.setenv(STRICT_EVENT_NAMES_ENV, "1")
        writer = RunLogWriter("job-strict", data_root=tmp_path)
        with pytest.raises(ValueError, match="undeclared run-ledger event name"):
            writer.log("no_such_event_name_exists")
        assert not writer.path.exists()

    def test_the_writer_accepts_a_declared_name_under_the_flag(
        self, tmp_path, monkeypatch
    ) -> None:
        monkeypatch.setenv(STRICT_EVENT_NAMES_ENV, "1")
        writer = RunLogWriter("job-strict-ok", data_root=tmp_path)
        writer.log("task_run_started")
        assert writer.path.read_text(encoding="utf-8").count("\n") == 1

    def test_a_quarantined_name_is_accepted_under_the_flag(
        self, tmp_path, monkeypatch
    ) -> None:
        """Giving a quarantined name its writer must not have to fight the flag."""
        monkeypatch.setenv(STRICT_EVENT_NAMES_ENV, "1")
        writer = RunLogWriter("job-strict-quarantined", data_root=tmp_path)
        writer.log(sorted(READ_ONLY_EVENT_NAMES)[0])
        assert writer.path.read_text(encoding="utf-8").count("\n") == 1
