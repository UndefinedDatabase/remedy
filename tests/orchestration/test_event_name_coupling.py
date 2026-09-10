"""The EVENT-NAME coupling ratchet — the second measurement finding R-0832 asks for.

WHAT THIS GUARDS. `tests/orchestration/test_cluster_deletion_map.py` built its
edge set from `import` statements parsed with `ast`, and DECISION F274 D2 ruled
the prototype-cluster deletion bounded by those edges. Finding R-0832 records
what that shape cannot see: a consumer coupled to a deleted module by EVENT NAME
holds no import of it, so the map correctly records no edge and the consumer
survives the deletion as dead code. R-0832's fix clause asks for a SECOND
measurement beside the map rather than a wider import walker, because a run-log
event name is a string literal and not an import.

WHAT IT MEASURES. For every `.py` module this branch deleted, the last living
blob is recovered from git and parsed for the event names it EMITTED — a string
literal in first-positional-argument position of a run-log emit call. Each such
name is then looked for in the SURVIVING tree, both as an emitter and as a
reader. A name with a surviving READER and no surviving EMITTER is a DEAD
COUPLING: a consumer kept alive by a producer that no longer exists.

WHY AN ALLOWLIST AND NOT A ZERO. The dead couplings that exist today are real
and their disposal is a ruling DECISION F260 D3 owes, not a repair a test may
make. So this is a RATCHET against a declared set, in the shape this repository
already uses for dead advertisements: the set may SHRINK and never grow, and an
entry that stops being a dead coupling must be removed from the list in the same
commit, or assertion (c) reds. Remedy deliberately does not delete a schema for
an event that historical run logs still carry; what it refuses is an INVISIBLE
coupling.
"""
from __future__ import annotations

import ast
import subprocess
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

BRANCH_BASE = "a5bf894946ab6de053a4232109d6341a63533768"

EMIT_FUNCS = frozenset({"log", "_emit", "emit", "log_event", "write_event",
                        "record_event"})

READER_SUFFIXES = (".py", ".ts", ".tsx")

# The dead couplings that exist today, each with the ruling that owns it.
# THIS LIST ONLY EVER SHRINKS. DECISION F260 D3 disposes of every entry.
KNOWN_DEAD_EVENT_COUPLINGS: tuple[str, ...] = (
    "context_budget_optimized",
)

_COUPLING_CEILING = 1


def _git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(REPO_ROOT), *args],
                          capture_output=True, text=True, check=False).stdout


def deleted_modules() -> list[str]:
    out = _git("log", "--diff-filter=D", "--name-only", "--pretty=format:",
               f"{BRANCH_BASE}..HEAD", "--", "packages", "apps")
    return sorted({p for p in out.split() if p.endswith(".py")})


def _emitted_names(source: str, path: str) -> set[str]:
    try:
        tree = ast.parse(source, filename=path)
    except SyntaxError:
        return set()
    found: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not node.args:
            continue
        fn = node.func
        name = fn.attr if isinstance(fn, ast.Attribute) else (
            fn.id if isinstance(fn, ast.Name) else None)
        if name not in EMIT_FUNCS:
            continue
        first = node.args[0]
        if isinstance(first, ast.Constant) and isinstance(first.value, str):
            found.add(first.value)
    return found


def events_emitted_by_deleted_modules() -> dict[str, set[str]]:
    """Event name -> the deleted modules that emitted it."""
    emitted: dict[str, set[str]] = defaultdict(set)
    for path in deleted_modules():
        rev = _git("rev-list", "-n", "1", "HEAD", "--", path).strip()
        if not rev:
            continue
        blob = _git("show", f"{rev}^:{path}")
        if not blob:
            continue
        for name in _emitted_names(blob, path):
            emitted[name].add(path)
    return dict(emitted)


def dead_event_couplings() -> dict[str, list[str]]:
    """Event name -> surviving readers, for names nothing surviving emits."""
    emitted = events_emitted_by_deleted_modules()
    if not emitted:
        return {}
    survivors = [p for p in _git("ls-files", "packages", "apps").split()
                 if p.endswith(READER_SUFFIXES)]
    still_emitted: set[str] = set()
    readers: dict[str, list[str]] = defaultdict(list)
    for rel in survivors:
        try:
            text = (REPO_ROOT / rel).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for name in emitted:
            if name in text:
                readers[name].append(rel)
        if rel.endswith(".py"):
            still_emitted |= (_emitted_names(text, rel) & set(emitted))
    return {name: sorted(rs) for name, rs in readers.items()
            if name not in still_emitted and rs}


class TestEventNameCouplingRatchet:
    """Finding R-0832: the coupling the import map cannot see."""

    def test_the_instrument_sees_the_deleted_modules_at_all(self) -> None:
        # Anti-blindness floor: a measurement over an empty corpus proves nothing.
        assert len(deleted_modules()) >= 40

    def test_every_dead_coupling_is_declared(self) -> None:
        found = dead_event_couplings()
        undeclared = sorted(set(found) - set(KNOWN_DEAD_EVENT_COUPLINGS))
        assert not undeclared, (
            "an event-name coupling to a deleted module is not declared: "
            f"{ {n: found[n] for n in undeclared} }"
        )

    def test_the_declared_set_only_ever_shrinks(self) -> None:
        assert len(KNOWN_DEAD_EVENT_COUPLINGS) <= _COUPLING_CEILING

    def test_no_declared_entry_is_stale(self) -> None:
        found = dead_event_couplings()
        stale = [n for n in KNOWN_DEAD_EVENT_COUPLINGS if n not in found]
        assert not stale, (
            f"these are no longer dead couplings and must leave the list: {stale}"
        )
