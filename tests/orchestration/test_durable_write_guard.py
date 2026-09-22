"""F278 T002 — no private atomic-write helper outside `packages/common/`.

`packages.common.secure_fs.durable_write` is the one path-based durable write. A module that
defines its own `_atomic_write` (or `atomic_write_text`, `_atomic_private_write`, ...) is a
second copy of it, and every copy measured before F278 got at least one of the fsyncs, the
temporary-file placement or the failure cleanup wrong. This guard reads every function
definition under `packages/`, `apps/` and `scripts/` by AST.

`STILL_TO_MIGRATE` is a RATCHET: it names the copies T002 has not yet deleted, and it only
ever shrinks. The commit that deletes a copy removes its entry here in the same commit, so a
copy that comes back, or a new one, turns this test red.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCANNED_ROOTS = ("packages", "apps", "scripts")
ALLOWED_ROOT = "packages/common/"
HELPER_NAME = re.compile(r"_?atomic_(private_)?write")

#: (module path, function name) — the copies not yet migrated. Only ever shrinks.
STILL_TO_MIGRATE = frozenset({
    ("packages/orchestration/real_test_execution.py", "_atomic_write"),
    ("packages/orchestration/self_dogfood_execution.py", "_atomic_write"),
    ("packages/orchestration/token_economy.py", "_atomic_write"),
    ("packages/runtimes/dev_server.py", "_atomic_write"),
    ("packages/runtimes/dev_server.py", "atomic_write_bytes"),
    ("packages/runtimes/dev_server.py", "atomic_write_text"),
})


def _private_helper_definitions(root: Path) -> set[tuple[str, str]]:
    found: set[tuple[str, str]] = set()
    for top in SCANNED_ROOTS:
        for path in sorted((root / top).rglob("*.py")):
            rel = path.relative_to(root).as_posix()
            if rel.startswith(ALLOWED_ROOT):
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=rel)
            for node in ast.walk(tree):
                if (isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                        and HELPER_NAME.match(node.name)):
                    found.add((rel, node.name))
    return found


def test_no_private_atomic_write_helper_outside_packages_common() -> None:
    found = _private_helper_definitions(REPO)
    new = sorted(found - STILL_TO_MIGRATE)
    assert not new, (
        f"private atomic-write helper(s) defined outside {ALLOWED_ROOT}: {new} — import "
        f"packages.common.secure_fs.durable_write instead")


def test_the_ratchet_names_only_copies_that_still_exist() -> None:
    gone = sorted(STILL_TO_MIGRATE - _private_helper_definitions(REPO))
    assert not gone, (
        f"{gone} no longer exist(s); remove the entry from STILL_TO_MIGRATE in the commit "
        f"that deleted it, so the ratchet cannot let it back in")


def test_the_guard_sees_a_helper_planted_in_a_scanned_tree(tmp_path: Path) -> None:
    module = tmp_path / "packages" / "orchestration" / "planted.py"
    module.parent.mkdir(parents=True)
    module.write_text("def _atomic_private_write(path, data):\n    pass\n", encoding="utf-8")
    allowed = tmp_path / "packages" / "common" / "fine.py"
    allowed.parent.mkdir(parents=True)
    allowed.write_text("def atomic_write_text(path, data):\n    pass\n", encoding="utf-8")

    assert _private_helper_definitions(tmp_path) == {
        ("packages/orchestration/planted.py", "_atomic_private_write")}
