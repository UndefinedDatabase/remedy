"""Operator amendment amend1014-do-golden-path-now D6 — a planner may not invent scope for `remedy do`.

A prompt that says "do not invent files" is a request, not a guard. This is the guard: the files
an order puts in scope are read from the order itself, and the files a planner's output names
are compared with them. A plan that names a file outside the scope is not kept; the caller falls
back to the deterministic one-milestone plan, which names only the order's own deliverables.

The scope of an order is the files it names, plus the tracked files whose name it uses as a word
("Improve the README" puts `README.md` in scope). An order that names a file or uses such a name,
or that carries a fence like "Change no other files", is bounded; an order that does neither
(`Refactor the parser`) leaves the planner free to discover its files, and nothing here refuses.

Deliberately not checked: content that is no file ("add badges"), because text search cannot tell
a section of the README from an invention, and the deterministic floor already keeps the plan to
the deliverables the order names.
"""

from __future__ import annotations

import re
from pathlib import PurePosixPath
from typing import Any

from packages.orchestration.order_scope import is_test_path, requests_test_files
from packages.orchestration.task_deliverables import explicit_order_paths

#: Words that fence an order to the files it names. A fence turns every other file into scope creep.
_SCOPE_FENCE_RE = re.compile(
    r"\b(?:no other files?|nothing else|(?:do not|don't|never) (?:change|modify|edit|touch) "
    r"(?:any )?(?:other|more)|only (?:change|modify|edit|touch)|change only)\b",
    re.IGNORECASE,
)

#: A tracked file's stem is used as a word only when it is at least this long (`a`, `io` match anything).
_MIN_STEM_CHARS = 3


def order_has_scope_fence(order: str) -> bool:
    """True when the order says in words that no other file may change."""
    return _SCOPE_FENCE_RE.search(order) is not None


def order_scope_files(order: str, tracked_files: list[str]) -> list[str]:
    """The files the order puts in scope: the ones it names, then the tracked ones it names as words."""
    named = explicit_order_paths(order)
    lowered = order.lower()
    # An order that spells a file name out ("README.md") has settled which README it means.
    spelled = {PurePosixPath(path).name for path in named}
    for path in tracked_files:
        stem = PurePosixPath(path).stem.lower().lstrip(".")
        if (path not in named and PurePosixPath(path).name not in spelled and len(stem) >= _MIN_STEM_CHARS
                and re.search(rf"(?<![\w-]){re.escape(stem)}(?![\w-])", lowered)):
            named.append(path)
    return named


def resolve_order_path(path: str, tracked_files: list[str]) -> str | None:
    """The tracked file *path* names, or None when the repository does not prove one.

    A path that is tracked as written is that file (root `README.md` wins over `docs/README.md`);
    a bare name resolves only when exactly one tracked file bears it. A name two nested files
    share, or one nothing tracks, is not resolved: it is never guessed.
    """
    if path in tracked_files:
        return path
    if "/" in path:
        return None
    same_name = [tracked for tracked in tracked_files if PurePosixPath(tracked).name == path]
    return same_name[0] if len(same_name) == 1 else None


def _same_file(produced: str, scoped: str, tracked_files: list[str]) -> bool:
    """The same file: equal paths, or two names the repository resolves to one tracked file.

    Basenames are never equated on their own: root `README.md` and `docs/README.md` are two files.
    """
    if produced == scoped:
        return True
    resolved = resolve_order_path(produced, tracked_files)
    return resolved is not None and resolved == (resolve_order_path(scoped, tracked_files) or scoped)


def mission_plan_text(plan: Any) -> str:
    """Every sentence of a mission plan that can name a file: milestone goals and job outlines."""
    parts: list[str] = []
    for milestone in plan.milestones:
        parts += [milestone.goal, milestone.rationale]
        for outline in milestone.jobs_draft:
            parts += [outline.title, outline.goal]
    return "\n".join(str(part) for part in parts)


def order_scope_violations(order: str, produced_text: str, tracked_files: list[str]) -> list[str]:
    """The files *produced_text* names that the order did not put in scope, in order of appearance.

    [] when the order is unbounded (it names nothing and carries no fence), so a planner that
    must discover the files of a broad order is never refused for finding them.
    """
    scope = order_scope_files(order, tracked_files)
    if not scope and not order_has_scope_fence(order):
        return []
    tests_requested = requests_test_files(order)
    return [path for path in explicit_order_paths(produced_text)
            if not (tests_requested and is_test_path(path))
            and not any(_same_file(path, scoped, tracked_files) for scoped in scope)]
