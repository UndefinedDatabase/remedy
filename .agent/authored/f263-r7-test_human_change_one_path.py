"""F263 Acceptance — the explicit command and the in-run path are provably one implementation.

`human_change.absorb` detects a change, certifies it, and only then calls the re-base it is
given; `human_change.absorb_job` is the one function that hands it a job's re-base. This guard
reads every tracked module under `packages/` and `apps/` and holds both facts: `absorb` is called from
`absorb_job` alone, and `absorb_job` is called from exactly the three entrances DECISIONS F263
D4 to D6 name — `remedy absorb`, a run's safe point, and the apply. A fourth spelling of
absorption, or an entrance that stops going through the one path, turns this red.
"""
from __future__ import annotations

import ast
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HUMAN_CHANGE = "packages/orchestration/human_change.py"

#: (module path, enclosing function) of every call to `absorb_job`.
ENTRANCES = {
    ("apps/cli/commands/absorb_cmd.py", "_cmd_absorb"),
    ("packages/orchestration/pingpong_job.py", "_absorb_at_safe_point"),
    ("packages/orchestration/job_apply.py", "apply_job"),
}


def _calls(name: str) -> set[tuple[str, str]]:
    """(module path, innermost enclosing function) of every call whose callee is `name`."""
    found: set[tuple[str, str]] = set()
    # Tracked sources only: an installed dependency under `apps/ui/node_modules` may ship Python
    # this repository does not own.
    listed = subprocess.run(["git", "-C", str(ROOT), "ls-files", "--", "packages/*.py", "apps/*.py"],
                            capture_output=True, text=True, check=True).stdout.split()
    assert listed, "git ls-files named no Python source; the guard would pass on nothing"
    for rel in sorted(listed):
        tree = ast.parse((ROOT / rel).read_text(encoding="utf-8"), filename=rel)

        def visit(node: ast.AST, owner: str, rel: str = rel) -> None:
            for child in ast.iter_child_nodes(node):
                inner = owner
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    inner = child.name
                if isinstance(child, ast.Call):
                    func = child.func
                    callee = func.attr if isinstance(func, ast.Attribute) else (
                        func.id if isinstance(func, ast.Name) else "")
                    if callee == name:
                        found.add((rel, owner))
                visit(child, inner, rel)

        visit(tree, "<module>")
    return found


def test_absorb_is_called_from_absorb_job_alone():
    assert _calls("absorb") == {(HUMAN_CHANGE, "absorb_job")}


def test_absorb_job_is_called_from_the_three_entrances_and_nowhere_else():
    assert _calls("absorb_job") == ENTRANCES
