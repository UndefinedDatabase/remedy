"""A structural guard for F200 DECISION D4's client-mode scope.

The amended acceptance names the client-mode boundary exactly: "Client mode
covers `job.stop`, `job.pause`, `job.unpause` and `job.run`; the other
commands the cockpit's door carries run direct in both modes, as the
commands it does not carry do." Nothing but a parse of every module under
`apps/` and `packages/` can keep that boundary exact as the codebase grows —
a new command that starts forwarding through the client bridge
(`apps/cli/serve_client.py`'s `forward_effect`/`supervisor_answers`) must
fail THIS test before it can ship, not be caught later by someone reading a
diff.

The parse is by `ast`, not by import: importing every module under `apps/`
and `packages/` to see what it calls would execute code this test has no
business running, and a literal that is never reached at import time would
be invisible to it anyway. This is the same approach
`tests/ui_contracts/test_humanize_catalog.py` uses to derive a vocabulary
from source (`safe_points.py`'s `_emit_budget_tick` docstring names it): a
value counts only when it is an `ast.Constant`.
"""
from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

#: DECISION F200 D4's exact set.
EXPECTED_COMMANDS = frozenset({"job.stop", "job.pause", "job.unpause", "job.run"})

#: The modules that handle those four commands, read from their own
#: `COMMAND_HANDLERS` tables rather than guessed: `job.stop` ->
#: `job_stop_cmd.py`, `job.pause`/`job.unpause` -> `job_pause_cmd.py`,
#: `job.run` -> `do_cmd.py`. `apps/cli/serve_client.py` only DEFINES
#: `forward_effect` and `supervisor_answers`; it calls neither itself.
EXPECTED_MODULES = frozenset({
    "apps/cli/commands/job_stop_cmd.py",
    "apps/cli/commands/job_pause_cmd.py",
    "apps/cli/commands/do_cmd.py",
})

_BRIDGE_NAMES = frozenset({"forward_effect", "supervisor_answers"})


def _call_name(node: ast.Call) -> str | None:
    fn = node.func
    if isinstance(fn, ast.Name):
        return fn.id
    if isinstance(fn, ast.Attribute):
        return fn.attr
    return None


def _command_argument(node: ast.Call) -> ast.expr | None:
    """`forward_effect`'s COMMAND argument: the second positional argument,
    or the keyword `command` when a caller names it instead."""
    if len(node.args) >= 2:
        return node.args[1]
    for kw in node.keywords:
        if kw.arg == "command":
            return kw.value
    return None


def _iter_python_files():
    for top in ("apps", "packages"):
        yield from sorted((REPO_ROOT / top).rglob("*.py"))


def _bridge_calls() -> list[tuple[str, int, str, ast.Call]]:
    """Every `forward_effect`/`supervisor_answers` call site under `apps/`
    and `packages/`: (relative path, line number, call name, call node)."""
    calls: list[tuple[str, int, str, ast.Call]] = []
    for path in _iter_python_files():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        rel = path.relative_to(REPO_ROOT).as_posix()
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = _call_name(node)
                if name in _BRIDGE_NAMES:
                    calls.append((rel, node.lineno, name, node))
    return calls


def test_every_forward_effect_command_is_one_of_the_four_door_literals():
    """(a) Every `forward_effect` call's command argument is a string
    literal, and the whole set of those literals is exactly the four DECISION
    F200 D4 names — no more, no fewer."""
    calls = [c for c in _bridge_calls() if c[2] == "forward_effect"]
    assert calls, "no forward_effect call sites found under apps/ or packages/ — scan is broken"

    literals: set[str] = set()
    for rel, lineno, _name, node in calls:
        arg = _command_argument(node)
        assert isinstance(arg, ast.Constant) and isinstance(arg.value, str), (
            f"{rel}:{lineno} calls forward_effect with a non-literal command argument "
            f"({ast.dump(arg) if arg is not None else 'missing'}) — a command id must be "
            f"readable by this guard without running the program")
        literals.add(arg.value)

    assert literals == EXPECTED_COMMANDS


def test_only_the_four_command_modules_reach_the_client_bridge():
    """(b) The modules that call `forward_effect` or `supervisor_answers` are
    exactly the modules that handle the four DECISION F200 D4 commands. A new
    command that starts forwarding fails here until the feature file and this
    test change together."""
    modules = {rel for rel, _lineno, _name, _node in _bridge_calls()}
    assert modules == EXPECTED_MODULES
