"""Two guards over the permission matrix (DECISION F141 D6 (3) and (4)).

THE NO-BYPASS GUARD reads every tracked Python module under `packages/` and `apps/` with
Python's own syntax tree, never text, so a comment or a string that merely mentions a banned
word never matches: a call of `require_permission` or `require_permissions` that passes a
keyword outside `config`, `root` and `now` would widen a cell or a check per caller, and a
function parameter whose name holds `bypass`, `permission_override`, `force_permission`,
`skip_permission`, `allow_all` or `unsafe_permission` is the shape of a parameter built to let a
caller skip the matrix. A bare `override` is left out on purpose: `apply_patch_intent`'s
`target_repo_override` redirects a write and widens nothing.

THE SEAM GUARD holds that the six modules DECISION F141 D6 (4) names each import from the
matrix or from its apply seam, and that every action of `PERMISSION_ACTIONS` is asked by name
somewhere outside `permission_matrix.py` itself — so an action added to the constant and never
wired to a seam is caught here, not in production.
"""
from __future__ import annotations

import ast
import subprocess
from pathlib import Path

import pytest

from packages.orchestration.permission_matrix import PERMISSION_ACTIONS

REPO_ROOT = Path(__file__).resolve().parents[2]

#: `require_permission(s)` may vary a call only by these; everything else widens per-caller.
ALLOWED_CALL_KEYWORDS = frozenset({"config", "root", "now"})

#: Substrings that mark a parameter built to let a caller skip the matrix.
BANNED_PARAMETER_SUBSTRINGS = (
    "bypass", "permission_override", "force_permission", "skip_permission", "allow_all",
    "unsafe_permission",
)

#: The six modules DECISION F141 D6 (4) names: each must route through the matrix.
SEAM_MODULES = (
    "packages/orchestration/builder_context.py",
    "packages/orchestration/apply_permissions.py",
    "packages/orchestration/job_apply.py",
    "packages/orchestration/do_apply.py",
    "apps/cli/cost_preview_confirm.py",
    "packages/orchestration/exec_guard.py",
)

#: What a seam module must import at least one name from.
PERMISSION_SOURCE_MODULES = (
    "packages.orchestration.permission_matrix",
    "packages.orchestration.apply_permissions",
)


def _call_name(node: ast.Call) -> str | None:
    """The plain or attribute name a call expresses, by name or attribute."""
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def _parameter_names(fn: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
    """Every parameter name a function declares: positional, keyword-only, *args, **kwargs."""
    args = fn.args
    names = [a.arg for a in (*args.posonlyargs, *args.args, *args.kwonlyargs)]
    if args.vararg:
        names.append(args.vararg.arg)
    if args.kwarg:
        names.append(args.kwarg.arg)
    return names


def find_bypass_violations(source: str) -> list[str]:
    """Every disallowed `require_permission(s)` call keyword, and every bypass-shaped parameter."""
    tree = ast.parse(source)
    violations: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _call_name(node) in ("require_permission", "require_permissions"):
            for kw in node.keywords:
                if kw.arg is not None and kw.arg not in ALLOWED_CALL_KEYWORDS:
                    violations.append(f"call keyword {kw.arg!r}")
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for name in _parameter_names(node):
                if any(word in name for word in BANNED_PARAMETER_SUBSTRINGS):
                    violations.append(f"parameter {name!r}")
    return violations


def _tracked_py_files() -> list[str]:
    """Every file `git ls-files` tracks under `packages/` or `apps/`, ending `.py`."""
    out = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "ls-files"], capture_output=True, text=True, check=True,
    ).stdout
    return [
        path for path in out.split()
        if path.endswith(".py") and (path.startswith("packages/") or path.startswith("apps/"))
    ]


@pytest.mark.parametrize("path", _tracked_py_files())
def test_no_tracked_file_has_a_bypass_shaped_call_or_parameter(path):
    source = (REPO_ROOT / path).read_text(encoding="utf-8")
    assert find_bypass_violations(source) == [], path


def test_the_checker_catches_each_bypass_shape_and_spares_a_look_alike():
    assert len(find_bypass_violations('require_permission("read", r, force=True)')) == 1
    assert len(find_bypass_violations('require_permissions(("read",), r, override=True)')) == 1
    assert len(find_bypass_violations("def f(x, bypass_matrix=False): pass")) == 1
    assert find_bypass_violations("def f(target_repo_override=None): pass") == []


def _imports_a_permission_name(source: str) -> bool:
    tree = ast.parse(source)
    return any(
        isinstance(node, ast.ImportFrom) and node.module in PERMISSION_SOURCE_MODULES and node.names
        for node in ast.walk(tree)
    )


@pytest.mark.parametrize("path", SEAM_MODULES)
def test_every_seam_module_imports_from_the_matrix_or_its_apply_seam(path):
    source = (REPO_ROOT / path).read_text(encoding="utf-8")
    assert _imports_a_permission_name(source), path


def _string_constants(source: str) -> set[str]:
    tree = ast.parse(source)
    return {
        node.value for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    }


def test_every_action_is_asked_by_name_in_a_seam_module():
    named: set[str] = set()
    for path in SEAM_MODULES:
        named |= _string_constants((REPO_ROOT / path).read_text(encoding="utf-8"))
    for action in PERMISSION_ACTIONS:
        assert action in named, action
