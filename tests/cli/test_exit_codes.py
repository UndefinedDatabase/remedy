"""Assert every catalog command's declared exit codes against a static reading
of its handler (DECISION F283 D12 (4)).

The reader below is adapted from the reviewer's prototype
(``.remedy-wt/f283-r20-scratch/reach_proto.py``, pinned at ``98a85b67``): per
catalog command, the exit codes its handler can reach are read statically —
the handler's own body, the same-module functions it calls by bare name (a
fixpoint), the ``apps.cli`` functions it imports and calls by name, and a code
passed into a helper's ``exit_code`` parameter at the call site. A named
module constant resolves through the defining module's globals. A call-site
argument this reading cannot resolve to an integer is an UNRESOLVED SITE: it
must be named in ``UNRESOLVED_SITES`` with the codes a reader verified by
hand, or the test fails naming its location.
"""

from __future__ import annotations

import ast
import importlib
import inspect
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

from apps.cli.command_catalog import CATALOG, CommandEntry
from apps.cli.commands import collect_all_handlers
from apps.cli.exit_codes import EXIT_CODE_FLOOR, exit_codes_for_group

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent

#: Call-site parameter names that PASS a caller's own exit code through rather
#: than choosing one — reading them as a literal would blame the wrong site.
_PASS_THROUGH_PARAMS = frozenset({"exit_code", "status"})


@dataclass(frozen=True)
class _UnresolvedSite:
    """A call-site argument this static reading could not resolve to an int."""

    module: str
    function: str
    lineno: int
    expr: str

    def location(self) -> str:
        path = _REPO_ROOT / (self.module.replace(".", "/") + ".py")
        return f"{path.relative_to(_REPO_ROOT)}:{self.lineno} ({self.function}): {self.expr}"


#: A site an unaided static reading cannot resolve, named with the codes a
#: reader verified by hand and why (D12 (4)). The reviewer's static prototype
#: found exactly one: ``ci run``'s ``sys.exit(ci_exit_code(results))``. An
#: unresolved site absent from this mapping fails the test with its location.
UNRESOLVED_SITES: dict[str, tuple[frozenset[int], str]] = {
    "ci.run": (
        frozenset({0, 1}),
        "sys.exit(ci_exit_code(results)) in apps/cli/commands/ci_cmd.py — "
        "ci_exit_code (packages/orchestration/ci_run.py) returns 0 only when "
        "at least one stage ran and every stage that ran was green, else 1.",
    ),
}


# ---------------------------------------------------------------------------
# The static reader
# ---------------------------------------------------------------------------

_ModuleInfo = tuple[Any, dict[str, ast.AST], dict[str, tuple[str, str]]]
_module_cache: dict[str, _ModuleInfo] = {}
_funcs_by_module_id: dict[int, dict[str, ast.AST]] = {}


def _module_info(modname: str) -> _ModuleInfo:
    """(module object, {func name: FunctionDef}, {imported name: (module, orig name)})."""
    if modname in _module_cache:
        return _module_cache[modname]
    mod = importlib.import_module(modname)
    tree = ast.parse(inspect.getsource(mod))
    funcs: dict[str, ast.AST] = {}
    imports: dict[str, tuple[str, str]] = {}
    # A handler often imports its helper INSIDE the function body (a local
    # import, common in this CLI), so the whole tree is walked here, not just
    # the module's top level.
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("apps.cli"):
            for alias in node.names:
                imports[alias.asname or alias.name] = (node.module, alias.name)
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funcs[node.name] = node
    _funcs_by_module_id[id(mod)] = funcs
    info = (mod, funcs, imports)
    _module_cache[modname] = info
    return info


def _code_of(arg: ast.expr, mod: Any, modname: str, funcname: str,
             locals_: dict[str, list[ast.expr]]) -> set[int | _UnresolvedSite]:
    """The set of ints (or one `_UnresolvedSite`) a call-site argument names."""
    if isinstance(arg, ast.Name) and arg.id in locals_ and arg.id not in _PASS_THROUGH_PARAMS:
        out: set[int | _UnresolvedSite] = set()
        for value in locals_[arg.id]:
            out |= _code_of(value, mod, modname, funcname, locals_)
        return out
    if isinstance(arg, ast.Constant) and isinstance(arg.value, int) and not isinstance(arg.value, bool):
        return {arg.value}
    if isinstance(arg, ast.Constant) and arg.value is None:
        return {0}
    if isinstance(arg, ast.Name):
        if arg.id in _PASS_THROUGH_PARAMS:
            return set()
        value = getattr(mod, arg.id, None)
        if isinstance(value, int):
            return {value}
    if isinstance(arg, ast.IfExp):
        return (_code_of(arg.body, mod, modname, funcname, locals_)
                | _code_of(arg.orelse, mod, modname, funcname, locals_))
    return {_UnresolvedSite(modname, funcname, getattr(arg, "lineno", 0), ast.unparse(arg)[:60])}


def _direct(fn: ast.AST, mod: Any, modname: str) -> tuple[set[int | _UnresolvedSite], set[str]]:
    """Codes reached directly in `fn`'s own body, and the bare-name calls it makes."""
    codes: set[int | _UnresolvedSite] = set()
    calls: set[str] = set()
    locals_: dict[str, list[ast.expr]] = {}
    for node in ast.walk(fn):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            locals_.setdefault(node.targets[0].id, []).append(node.value)
    for node in ast.walk(fn):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Attribute) and func.attr == "exit" and getattr(func.value, "id", None) == "sys":
            arg = node.args[0] if node.args else ast.Constant(0)
            codes |= _code_of(arg, mod, modname, fn.name, locals_)
        elif isinstance(func, ast.Name) and func.id == "SystemExit":
            arg = node.args[0] if node.args else ast.Constant(0)
            codes |= _code_of(arg, mod, modname, fn.name, locals_)
        elif isinstance(func, ast.Name) and func.id == "fail":
            arg: ast.expr = ast.Constant(1)
            for kw in node.keywords:
                if kw.arg == "exit_code":
                    arg = kw.value
            codes |= _code_of(arg, mod, modname, fn.name, locals_)
        elif isinstance(func, ast.Name):
            calls.add(func.id)
            # A call site that passes a literal into a SAME-MODULE helper's
            # `exit_code` (or `status`) parameter names the code for the
            # CALLING function directly — the helper's own body only ever
            # sees that parameter as a pass-through, so reach()-ing the
            # helper generically would find nothing (e.g. `runtime_cmd.py`'s
            # `_runtime_refusal(error_class, message, exit_code, ...)`).
            target = _funcs_by_module_id.get(id(mod), {}).get(func.id)
            if target is not None:
                target_params = [a.arg for a in target.args.args] + [a.arg for a in target.args.kwonlyargs]
                positional_params = [a.arg for a in target.args.args]
                for pname in _PASS_THROUGH_PARAMS & set(target_params):
                    value = None
                    for kw in node.keywords:
                        if kw.arg == pname:
                            value = kw.value
                    if value is None and pname in positional_params:
                        idx = positional_params.index(pname)
                        if idx < len(node.args):
                            value = node.args[idx]
                    if value is not None:
                        codes |= _code_of(value, mod, modname, fn.name, locals_)
    for node in ast.walk(fn):
        if isinstance(node, ast.Raise) and isinstance(node.exc, ast.Name) and node.exc.id == "SystemExit":
            codes.add(0)
    return codes, calls


_reach_memo: dict[tuple[str, str], set[int | _UnresolvedSite]] = {}


def _reach(modname: str, funcname: str, stack: tuple = ()) -> set[int | _UnresolvedSite]:
    """Every exit code `modname.funcname` can reach: itself, and (fixpoint)
    every same-module function it calls by bare name or `apps.cli` function it
    imports and calls by name."""
    key = (modname, funcname)
    if key in _reach_memo:
        return _reach_memo[key]
    if key in stack:                      # a call cycle reaches nothing new
        return set()
    mod, funcs, imports = _module_info(modname)
    if funcname not in funcs:
        if funcname in imports:
            other_module, other_name = imports[funcname]
            return _reach(other_module, other_name, stack + (key,))
        return set()
    codes, calls = _direct(funcs[funcname], mod, modname)
    for called in calls:
        if called == "fail":
            continue
        codes |= _reach(modname, called, stack + (key,))
    _reach_memo[key] = codes
    return codes


def _codes_for_handler(entry: CommandEntry, handlers: dict) -> set[int | _UnresolvedSite]:
    handler = handlers.get(entry.command_id)
    assert handler is not None, f"{entry.command_id}: no registered handler"
    handler = inspect.unwrap(handler)
    if handler.__name__ == "<lambda>":
        codes: set[int | _UnresolvedSite] = set()
        for name in handler.__code__.co_names:
            codes |= _reach(handler.__module__, name)
        return codes
    return _reach(handler.__module__, handler.__name__)


def _above_floor(codes: set[int]) -> set[int]:
    return {c for c in codes if c not in EXIT_CODE_FLOOR}


def _resolved_ints(entry: CommandEntry, raw: set[int | _UnresolvedSite]) -> set[int]:
    """`raw`'s integers, with any unresolved site folded in from
    `UNRESOLVED_SITES` — or the test fails naming the site's location."""
    ints = {c for c in raw if isinstance(c, int)}
    unresolved = [c for c in raw if isinstance(c, _UnresolvedSite)]
    if unresolved:
        verified = UNRESOLVED_SITES.get(entry.command_id)
        if verified is None:
            locations = "; ".join(site.location() for site in unresolved)
            pytest.fail(
                f"{entry.command_id}: unresolved exit-code site with no entry in "
                f"UNRESOLVED_SITES: {locations}"
            )
        codes, _reason = verified
        ints |= set(codes)
    return ints


_HANDLERS = collect_all_handlers()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("entry", CATALOG, ids=lambda e: e.command_id)
def test_declared_codes_are_the_floor_plus_named_codes(entry: CommandEntry) -> None:
    """Every entry's `exit_codes` contains the floor and only codes its
    group's table names (D12 (1), (2), (4))."""
    declared = set(entry.exit_codes)
    assert set(EXIT_CODE_FLOOR) <= declared, (
        f"{entry.command_id}: {sorted(declared)} is missing the floor {EXIT_CODE_FLOOR}"
    )
    table_codes = {m.code for m in exit_codes_for_group(entry.group_id)}
    unnamed = declared - table_codes
    assert not unnamed, (
        f"{entry.command_id}: declares {sorted(unnamed)}, which its group "
        f"({entry.group_id}) table does not name"
    )


@pytest.mark.parametrize("entry", CATALOG, ids=lambda e: e.command_id)
def test_declared_codes_equal_the_codes_the_handler_reaches(entry: CommandEntry) -> None:
    """Per command, the codes above the floor its handler reaches by D12 (4)'s
    static reading EQUAL the codes above the floor it declares."""
    raw = _codes_for_handler(entry, _HANDLERS)
    reached_above_floor = _above_floor(_resolved_ints(entry, raw))
    declared_above_floor = _above_floor(set(entry.exit_codes))
    assert reached_above_floor == declared_above_floor, (
        f"{entry.command_id}: handler reaches {sorted(reached_above_floor)} above the "
        f"floor, catalog declares {sorted(declared_above_floor)}"
    )
