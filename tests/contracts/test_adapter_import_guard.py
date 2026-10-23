"""F151 T003: the import guard that keeps orchestration and the contracts layer away from a
concrete adapter (DECISION F151 D5 (4)).

Orchestration binds to the contract (`packages/contracts/adapter_contract.py`) only; a concrete
adapter under `packages/providers/adapters/` is reached through the registry linkage
(`packages/providers/adapters/adapter_registry.py`) that only the wiring layer
(`apps/cli/commands/worker.py`) and each adapter's own tests import. This guard parses every
Python file under `packages/orchestration/` and `packages/contracts/` with `ast` and fails on
any import — top-level or inside a function — of `packages.providers.adapters` or a module
beneath it.
"""
from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

#: The two trees this guard keeps away from a concrete adapter (DECISION F151 D5 (4)).
GUARDED_TREES = ("packages/orchestration", "packages/contracts")

#: Any import of this dotted name or a module beneath it is forbidden in a guarded tree.
FORBIDDEN_PREFIX = "packages.providers.adapters"


def _is_forbidden(dotted: str) -> bool:
    return dotted == FORBIDDEN_PREFIX or dotted.startswith(FORBIDDEN_PREFIX + ".")


def import_guard_violations(source: str) -> list[int]:
    """The line number of every import of `FORBIDDEN_PREFIX` (or a module beneath it) in `source`.

    Reads both `import a.b` and `from a.b import c` — top-level or inside a function body, since
    `ast.walk` does not stop at a `FunctionDef`.
    """
    tree = ast.parse(source)
    lines: list[int] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _is_forbidden(alias.name):
                    lines.append(node.lineno)
        elif isinstance(node, ast.ImportFrom):
            if node.module and _is_forbidden(node.module):
                lines.append(node.lineno)
    return lines


def walk_guarded_trees(root: Path) -> list[str]:
    """`path:line` for every import guard violation under either tree in `GUARDED_TREES`."""
    violations: list[str] = []
    for tree_rel in GUARDED_TREES:
        for path in sorted((root / tree_rel).rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            rel = path.relative_to(root).as_posix()
            source = path.read_text(encoding="utf-8")
            for lineno in import_guard_violations(source):
                violations.append(f"{rel}:{lineno}")
    return violations


def test_neither_guarded_tree_imports_a_concrete_adapter():
    assert walk_guarded_trees(REPO_ROOT) == []


def test_the_checker_reports_a_function_body_import_of_the_reference_adapter():
    violation_fixture = (
        "def wire_it():\n"
        "    from packages.providers.adapters.claude_cli_reference import ClaudeCliReferenceAdapter\n"
        "    return ClaudeCliReferenceAdapter\n"
    )
    assert len(import_guard_violations(violation_fixture)) == 1


def test_the_checker_reports_no_violation_for_the_contract_module():
    clean_fixture = "from packages.contracts.adapter_contract import WorkerAdapter\n"
    assert import_guard_violations(clean_fixture) == []
