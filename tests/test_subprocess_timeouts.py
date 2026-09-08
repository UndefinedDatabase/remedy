"""No production subprocess call may run without a timeout.

A hung child process hangs the unattended loop forever. The deadline budget is
checked BETWEEN steps, so it cannot see a step that never returns: a stale
``index.lock``, a git hook that prompts, or a network filesystem that stops
answering all block inside one ``subprocess.run`` call, and nothing in this
repository interrupts it.

This guard is a text-free AST pass over ``packages/`` and ``apps/``. It collects
every ``subprocess.run``, ``subprocess.check_output``, ``subprocess.check_call``
and ``subprocess.call`` whose keywords carry neither ``timeout=`` nor a
``**kwargs`` splat — a splat may supply the timeout at the call site, so it is
accepted here rather than guessed at — and requires the list to be empty.

Registered by operator amendment amend0908-brainstorm-intake, Part 5, which
measured eight offending sites: six in ``packages/orchestration/worktrees.py``,
one in ``job_evidence.py`` and one in ``gauntlet_runner.py``.

Remedy deliberately does NOT check ``tests/`` or ``scripts/`` here: a test that
hangs is caught by the pytest runner's own timeout, and this guard exists to
protect the unattended runtime.
"""

from __future__ import annotations

import ast
from pathlib import Path

#: The subprocess entry points that start a child process and wait for it.
#: ``subprocess.Popen`` is absent on purpose: it does not wait, so it has no
#: timeout to carry — its ``wait``/``communicate`` call is where a deadline
#: belongs, and no production site uses it today.
BLOCKING_SUBPROCESS_CALLS = frozenset(
    {"run", "check_output", "check_call", "call"}
)

#: Production trees this guard covers.
PRODUCTION_DIRS = ("packages", "apps")


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _production_python_files() -> list[Path]:
    root = _repo_root()
    files: list[Path] = []
    for directory in PRODUCTION_DIRS:
        files.extend(sorted((root / directory).rglob("*.py")))
    return files


def _call_is_untimed(node: ast.Call) -> bool:
    """True when `node` is a blocking subprocess call with no timeout."""
    func = node.func
    if not isinstance(func, ast.Attribute):
        return False
    if func.attr not in BLOCKING_SUBPROCESS_CALLS:
        return False
    if not (isinstance(func.value, ast.Name) and func.value.id == "subprocess"):
        return False
    keywords = {kw.arg for kw in node.keywords}
    # `None` is the arg name of a `**kwargs` splat: the timeout may come
    # through it, so such a call is not an offender by inspection alone.
    return "timeout" not in keywords and None not in keywords


def find_untimed_subprocess_calls() -> list[str]:
    """Every offending call as `path:line`, repo-relative and sorted."""
    root = _repo_root()
    offenders: list[str] = []
    for path in _production_python_files():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and _call_is_untimed(node):
                relative = path.relative_to(root)
                offenders.append(f"{relative}:{node.lineno}")
    return sorted(offenders)


def test_no_production_subprocess_call_is_missing_a_timeout():
    offenders = find_untimed_subprocess_calls()
    assert offenders == [], (
        f"{len(offenders)} production subprocess call(s) carry no timeout=; "
        "a hung child hangs the unattended loop forever:\n  "
        + "\n  ".join(offenders)
    )
