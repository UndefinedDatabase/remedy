"""T2_F271 design (c), scoped narrow by F281 (T2_F281.md Acceptance: the
section only). A catalog command is DEAD when none of its handler's
underlying names, its dotted command_id, its spaced ``<group> <subcommand>``
form, or an adjacent ``("<group>", "<subcommand>")`` list/tuple literal
appears anywhere under a search root's ``tests/`` or ``scripts/`` directory.

The fourth signal exists because a CLI test invoked as an argv list —
``subprocess.run([*_CLI, "job", "run-next", short_id])`` — holds the group and
the subcommand as two separate string tokens that neither the spaced nor the
dotted text scan ever matches (the blind spot F275 round 33's command-deletion
sweep hit). Text scans alone would misreport a subprocess-tested command as
dead; the AST pass over list/tuple literals is what makes this check answer
the real question rather than a shape it resembles.

This module never imports ``apps.cli.command_catalog``: the caller passes the
catalog's own ``(command_id, group_id, subcommand)`` triples and its handler
table, so a CLI-layer import cycle can never form here.

Public API::

    dead_command_ids(catalog, handlers, root=None) -> list[str]
"""

from __future__ import annotations

import ast
import re
from collections.abc import Callable, Iterable
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SEARCH_DIRS = ("tests", "scripts")


def _handler_names(fn: Callable[..., object]) -> frozenset[str]:
    """Every identifier the handler's own code references, by name.

    Most catalog handlers are a ``lambda`` closing over the real
    implementation function (``lambda args: _cmd_list_jobs(...)``), so the
    lambda's own ``__name__`` is always the literal string ``"<lambda>"`` and
    never the name a test actually imports; ``co_names`` reaches through to
    the real callee.
    """
    names = set(fn.__code__.co_names)
    if fn.__name__ != "<lambda>":
        names.add(fn.__name__)
    return frozenset(n for n in names if not n.startswith("__"))


def _iter_search_files(root: Path) -> Iterable[Path]:
    for rel in _SEARCH_DIRS:
        d = root / rel
        if d.is_dir():
            yield from (p for p in d.rglob("*") if p.is_file())


def _adjacent_string_pairs(tree: ast.AST) -> set[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.List, ast.Tuple)):
            elts = node.elts
            for i in range(len(elts) - 1):
                a, b = elts[i], elts[i + 1]
                if (isinstance(a, ast.Constant) and isinstance(a.value, str)
                        and isinstance(b, ast.Constant) and isinstance(b.value, str)):
                    pairs.add((a.value, b.value))
    return pairs


def dead_command_ids(
    catalog: Iterable[tuple[str, str, str]],
    handlers: dict[str, Callable[..., object]],
    *,
    root: Path | None = None,
) -> list[str]:
    """The sorted command_ids of every catalog command referenced nowhere.

    ``catalog`` is an iterable of ``(command_id, group_id, subcommand)``
    triples, taken from the caller's own ``CATALOG`` entries.
    """
    root = root if root is not None else _REPO_ROOT
    texts: list[str] = []
    pairs: set[tuple[str, str]] = set()
    for path in _iter_search_files(root):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        texts.append(text)
        if path.suffix == ".py":
            try:
                pairs |= _adjacent_string_pairs(ast.parse(text))
            except SyntaxError:
                continue

    dead: list[str] = []
    for command_id, group_id, subcommand in catalog:
        if (group_id, subcommand) in pairs:
            continue
        spaced = f"{group_id} {subcommand}"
        if any(spaced in t or command_id in t for t in texts):
            continue
        patterns = [re.compile(r"\b" + re.escape(n) + r"\b") for n in _handler_names(handlers[command_id])]
        if any(p.search(t) for t in texts for p in patterns):
            continue
        dead.append(command_id)
    return sorted(dead)
