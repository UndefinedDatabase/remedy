"""Every `REMEDY_*` name production code spells is a registered variable (T2_F279 T001).

DECISION F279 D2: the environment registry is the key registry of
`packages/orchestration/config.py` — one `ConfigKeySpec` per variable, carrying its type, its
default and its description — and not a second module beside it. These guards read the
production tree as SOURCE: a variable that is read, written, forwarded or named in a constant
must be registered, because a name nobody registered is a name nobody can validate, document
or report as a typo. The scan is over whole string literals, which also catches the names a
module keeps in a constant and reads through it (`PORT_ENV = "REMEDY_RUNTIME_PORT"`).
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

from packages.orchestration.config import all_key_specs

REPO_ROOT = Path(__file__).resolve().parents[2]
SCANNED_ROOTS = ("packages", "apps", "scripts")
VARIABLE_NAME = re.compile(r"REMEDY_[A-Z0-9_]+")
ENV_READERS = frozenset({"get", "pop", "setdefault", "getenv"})


def production_modules() -> list[Path]:
    modules: list[Path] = []
    for root in SCANNED_ROOTS:
        modules.extend(path for path in sorted((REPO_ROOT / root).rglob("*.py"))
                       if "node_modules" not in path.parts)
    return modules


def spelled_names(tree: ast.AST) -> set[str]:
    """Every whole string literal in `tree` that is a `REMEDY_*` variable name."""
    return {node.value for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
            and VARIABLE_NAME.fullmatch(node.value)}


def literal_env_reads(tree: ast.AST) -> set[str]:
    """The `REMEDY_*` literals passed straight to `os.environ[...]`, `.get`, `.pop`,
    `.setdefault` or `os.getenv` — T001's own wording of what the guard must hold."""
    names: set[str] = set()
    for node in ast.walk(tree):
        key = None
        if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Attribute) \
                and node.value.attr == "environ":
            key = node.slice
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.args \
                and node.func.attr in ENV_READERS:
            key = node.args[0]
        if isinstance(key, ast.Constant) and isinstance(key.value, str) \
                and VARIABLE_NAME.fullmatch(key.value):
            names.add(key.value)
    return names


def registered_names() -> set[str]:
    return {spec.env_var for spec in all_key_specs()}


def scan(collect) -> dict[str, list[str]]:
    """name -> the modules that spell it, for every name `collect` finds and nobody registered."""
    registered = registered_names()
    unregistered: dict[str, list[str]] = {}
    for path in production_modules():
        for name in collect(ast.parse(path.read_text(encoding="utf-8"))):
            if name not in registered:
                unregistered.setdefault(name, []).append(str(path.relative_to(REPO_ROOT)))
    return unregistered


def test_the_scan_sees_the_production_tree():
    """A guard over an empty file list passes for every tree, so the list is measured first."""
    modules = production_modules()
    assert len(modules) > 100
    assert REPO_ROOT / "packages" / "orchestration" / "config.py" in modules


def test_every_literal_env_read_names_a_registered_variable():
    assert scan(literal_env_reads) == {}


def test_every_remedy_name_production_code_spells_is_registered():
    assert scan(spelled_names) == {}


def test_every_registered_variable_is_a_remedy_name_and_registered_once():
    names = [spec.env_var for spec in all_key_specs()]
    assert [name for name in names if not VARIABLE_NAME.fullmatch(name)] == []
    assert len(names) == len(set(names))
    keys = [spec.key for spec in all_key_specs()]
    assert len(keys) == len(set(keys))
