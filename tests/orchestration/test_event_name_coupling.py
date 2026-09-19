"""The EVENT-NAME coupling ratchet — the second measurement finding R-0832 asks for.

WHAT THIS GUARDS. `tests/orchestration/test_cluster_deletion_map.py` built its
edge set from `import` statements parsed with `ast`, and DECISION F274 D2 ruled
the prototype-cluster deletion bounded by those edges. THAT FILE NO LONGER
EXISTS: DECISION F275 D15 retired it at round 25, together with the deletion map
and the order ratchet, once `CLUSTER_MODULES` emptied and every assertion in the
three of them quantified over nothing. Finding R-0832 records what its shape
could not see: a consumer coupled to a deleted module by EVENT NAME holds no
import of it, so the map correctly recorded no edge and the consumer survives the
deletion as dead code. R-0832's fix clause asks for a SECOND measurement beside
the map rather than a wider import walker, because a run-log event name is a
string literal and not an import.

WHAT IT MEASURES. For every `.py` module this branch deleted, the last living
blob is recovered from git and parsed for the event names it EMITTED — a string
literal in ANY positional slot of an emit call: a call named in `EMIT_FUNCS`, one
whose snake_case name has an `emit` word (`_emit_continue`, `emit_important_event`),
or one to a helper the module defines that forwards a parameter to such a call
(finding R-0920: first-slot recovery was blind to every helper). Each such
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

# The dead couplings that exist today, each with the ruling that owns it. THIS LIST
# ONLY EVER SHRINKS: DECISION F260 D3 disposes of `context_budget_optimized`. F273
# deleted the readers of `git_status_read` (R-0905) and dropped the level-4 readiness
# signals `run_contract_inspected` and `token_policy_inspected` fed (R-0907), and the
# widened recovery (R-0920) found no further dead name once R-0919 deleted the
# cockpit's `do_continue_stopped` reader.
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


def _call_name(node: ast.Call) -> str:
    fn = node.func
    if isinstance(fn, ast.Attribute):
        return fn.attr
    return fn.id if isinstance(fn, ast.Name) else ""


def _is_emit_call(node: ast.AST, helpers: frozenset[str] = frozenset()) -> bool:
    if not isinstance(node, ast.Call):
        return False
    name = _call_name(node)
    return (name in EMIT_FUNCS or name in helpers
            or "emit" in name.strip("_").split("_"))


def _emit_helpers(tree: ast.AST) -> frozenset[str]:
    """Functions the module defines that forward a parameter to an emit call."""
    helpers: set[str] = set()
    for fdef in ast.walk(tree):
        if not isinstance(fdef, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        params = {a.arg for a in fdef.args.args + fdef.args.kwonlyargs}
        if any(_is_emit_call(n) and any(isinstance(a, ast.Name) and a.id in params
                                        for a in n.args)
               for n in ast.walk(fdef)):
            helpers.add(fdef.name)
    return frozenset(helpers)


def _emitted_names(source: str, path: str) -> set[str]:
    try:
        tree = ast.parse(source, filename=path)
    except SyntaxError:
        return set()
    helpers = _emit_helpers(tree)
    return {a.value for node in ast.walk(tree) if _is_emit_call(node, helpers)
            for a in node.args
            if isinstance(a, ast.Constant) and isinstance(a.value, str)}


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

    def test_the_recovery_finds_a_name_a_helper_emits(self) -> None:
        # Finding R-0920: `do_continue.py` emitted every name through
        # `_emit_continue(data_dir, job_id, event, metadata)`, third slot.
        source = (
            "def _record(data_dir, job_id, event):\n"
            "    persist(data_dir, job_id, event)\n"
            "    log_event(data_dir, job_id, event, {})\n"
            "def run(d, j):\n"
            "    _emit_continue(d, j, 'alpha_stopped', {})\n"
            "    _record(d, j, 'beta_started')\n"
            "    persist(d, j, 'gamma_not_an_event')\n"
        )
        assert _emitted_names(source, "m.py") == {"alpha_stopped", "beta_started"}
        emitted = events_emitted_by_deleted_modules()
        assert emitted.get("do_continue_stopped") == {
            "packages/orchestration/do_continue.py"}

    def test_the_declared_set_only_ever_shrinks(self) -> None:
        assert len(KNOWN_DEAD_EVENT_COUPLINGS) <= _COUPLING_CEILING

    def test_no_declared_entry_is_stale(self) -> None:
        found = dead_event_couplings()
        stale = [n for n in KNOWN_DEAD_EVENT_COUPLINGS if n not in found]
        assert not stale, (
            f"these are no longer dead couplings and must leave the list: {stale}"
        )
