"""Every top-level child of the data root is in exactly one class (F276 T001).

WHAT THIS GUARDS. ``data_paths.EPHEMERAL_CLASSES`` and ``DURABLE_CLASSES`` are the
registry reclaim (T002) addresses directories through. A child the code creates
that is in neither is a class nobody owns — reclaim would neither touch it nor
report it — so a new one must be classified in the same change that creates it.

WHAT IS MEASURED, NOT LISTED. The set of children is read from the code on every
run, never typed here:
- every public ``*_dir(root=None)`` helper of ``data_paths`` is CALLED with a
  scratch root, and the first path segment below that root is the child;
- an ``ast`` scan of ``packages/``, ``apps/`` and ``scripts/`` finds each
  ``<data root> / "<literal>"`` join, where the data root is a
  ``resolve_data_root()`` call, ``Path(...)`` of one, a conditional or ``or``
  expression containing one, a name bound to such an expression in the same
  function, or a parameter named ``data_root`` / ``data_dir``; a module-level
  string constant on the right counts as its literal;
- a ``".data/<name>"`` string constant in Python, and a ``.data/<name>`` spelling
  in a shell script under ``scripts/``, name a child of the repository-default root.

WHAT THIS DOES NOT CATCH. A parameter called ``root`` or ``base`` is not taken to
be the data root, because most of them are a repository root; a helper that
joins onto such a parameter is caught only through the helper call above.
"""
from __future__ import annotations

import ast
import inspect
import re
from pathlib import Path

from packages.orchestration import data_paths
from packages.orchestration.data_paths import (
    DURABLE_CLASSES,
    EPHEMERAL_CLASSES,
    classify_data_child,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
SCANNED_ROOTS = ("packages", "apps", "scripts")
SKIPPED_DIRS = frozenset({"__pycache__", "node_modules", ".venv", "venv", "dist", "build", ".remedy-wt"})
ROOT_PARAMS = frozenset({"data_root", "data_dir"})
_SH_DATA_CHILD = re.compile(r"\.data/([A-Za-z0-9_]+)")


def _is_root_call(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
    return name == "resolve_data_root"


def _is_root_expr(node: ast.AST, tainted: set[str]) -> bool:
    """True when ``node`` evaluates to the data root itself (not a path below it)."""
    if _is_root_call(node):
        return True
    if isinstance(node, ast.Name):
        return node.id in tainted
    if isinstance(node, ast.Call) and getattr(node.func, "id", "") == "Path" and node.args:
        return _is_root_expr(node.args[0], tainted)
    if isinstance(node, ast.IfExp):
        return _is_root_expr(node.body, tainted) or _is_root_expr(node.orelse, tainted)
    if isinstance(node, ast.BoolOp):
        return any(_is_root_expr(v, tainted) for v in node.values)
    return False


def _module_constants(tree: ast.Module) -> dict[str, str]:
    consts = {}
    for node in tree.body:
        value = node.value if isinstance(node, (ast.Assign, ast.AnnAssign)) else None
        if isinstance(value, ast.Constant) and isinstance(value.value, str):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            consts.update({t.id: value.value for t in targets if isinstance(t, ast.Name)})
    return consts


_FUNCS = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)


def _own_nodes(scope: ast.AST) -> list[ast.AST]:
    """Every node of one scope, not descending into a nested function."""
    out, pending = [], list(ast.iter_child_nodes(scope))
    while pending:
        node = pending.pop()
        out.append(node)
        if not isinstance(node, _FUNCS):
            pending.extend(ast.iter_child_nodes(node))
    return out


def _scopes(tree: ast.Module):
    """(scope nodes, names bound to the data root on entry) per module and function."""
    yield _own_nodes(tree), set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            params = {a.arg for a in (*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs)}
            yield _own_nodes(node), params & ROOT_PARAMS


def data_children_in_python(source: str, rel: str) -> dict[str, set[str]]:
    """``{child name: {"rel:line", ...}}`` for every data-root join in one module."""
    tree = ast.parse(source, filename=rel)
    consts = _module_constants(tree)
    found: dict[str, set[str]] = {}

    def add(name: str, line: int) -> None:
        found.setdefault(name.split("/")[0], set()).add(f"{rel}:{line}")

    for nodes, tainted in _scopes(tree):
        grew = True
        while grew:  # to a fixed point, so `a = resolve_data_root(); b = a` binds b
            before = len(tainted)
            for node in nodes:
                if isinstance(node, ast.Assign) and _is_root_expr(node.value, tainted):
                    tainted |= {t.id for t in node.targets if isinstance(t, ast.Name)}
            grew = len(tainted) != before
        for node in nodes:
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div) and _is_root_expr(node.left, tainted):
                right = node.right
                if isinstance(right, ast.Constant) and isinstance(right.value, str):
                    add(right.value, node.lineno)
                elif isinstance(right, ast.Name) and right.id in consts:
                    add(consts[right.id], node.lineno)
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            dotted = _SH_DATA_CHILD.match(node.value)
            if dotted:
                add(dotted.group(1), node.lineno)
        if (isinstance(node, ast.Call) and getattr(node.func, "id", "") == "data_class_dir"
                and node.args and isinstance(node.args[0], ast.Constant)):
            add(node.args[0].value, node.lineno)
    return found


def data_children_in_shell(text: str, rel: str) -> dict[str, set[str]]:
    found: dict[str, set[str]] = {}
    for lineno, line in enumerate(text.splitlines(), 1):
        for name in _SH_DATA_CHILD.findall(line):
            found.setdefault(name, set()).add(f"{rel}:{lineno}")
    return found


def scan_tree(root: Path) -> dict[str, set[str]]:
    """Every data-root child named anywhere under ``root``'s scanned trees."""
    found: dict[str, set[str]] = {}
    for top in SCANNED_ROOTS:
        for path in sorted((root / top).rglob("*")):
            if SKIPPED_DIRS.intersection(path.relative_to(root).parts) or not path.is_file():
                continue
            rel = path.relative_to(root).as_posix()
            if path.suffix == ".py":
                part = data_children_in_python(path.read_text(encoding="utf-8"), rel)
            elif path.suffix == ".sh":
                part = data_children_in_shell(path.read_text(encoding="utf-8", errors="replace"), rel)
            else:
                continue
            for name, sites in part.items():
                found.setdefault(name, set()).update(sites)
    return found


def data_children_of_helpers(scratch: Path) -> dict[str, set[str]]:
    """Call every public ``*_dir(root=None)`` helper of data_paths with a scratch root."""
    found: dict[str, set[str]] = {}
    for name, fn in inspect.getmembers(data_paths, inspect.isfunction):
        if name.startswith("_") or not name.endswith("_dir") or fn.__module__ != data_paths.__name__:
            continue
        params = list(inspect.signature(fn).parameters)
        if params != ["root"]:
            continue
        child = fn(scratch).relative_to(scratch).parts[0]
        found.setdefault(child, set()).add(f"data_paths.{name}()")
    return found


def _names(classes) -> list[str]:
    return [c.name for c in classes]


def test_the_two_classes_are_disjoint_and_each_name_is_unique():
    ephemeral, durable = _names(EPHEMERAL_CLASSES), _names(DURABLE_CLASSES)
    assert len(set(ephemeral)) == len(ephemeral)
    assert len(set(durable)) == len(durable)
    assert not set(ephemeral) & set(durable)


def test_every_class_names_an_owner_and_a_reclaim_rule():
    for entry in (*EPHEMERAL_CLASSES, *DURABLE_CLASSES):
        assert entry.owner.strip() and entry.reclaim_rule.strip(), entry.name


def test_every_child_the_code_creates_is_in_exactly_one_class(tmp_path):
    """A new unclassified child — a helper or a literal join — reds here, naming its site."""
    found = scan_tree(REPO_ROOT)
    for name, sites in data_children_of_helpers(tmp_path).items():
        found.setdefault(name, set()).update(sites)
    ephemeral, durable = set(_names(EPHEMERAL_CLASSES)), set(_names(DURABLE_CLASSES))
    unclassified = {n: s for n, s in found.items() if (n in ephemeral) == (n in durable)}
    assert not unclassified, (
        "These data-root children are created by the code but are in neither "
        "data_paths.EPHEMERAL_CLASSES nor DURABLE_CLASSES (or in both):\n"
        + "\n".join(f"{n}: {', '.join(sorted(s))}" for n, s in sorted(unclassified.items())))


def test_every_class_is_created_somewhere_in_the_code(tmp_path):
    """The registry is a measurement too: a class no code creates is stale."""
    found = set(scan_tree(REPO_ROOT)) | set(data_children_of_helpers(tmp_path))
    stale = sorted((set(_names(EPHEMERAL_CLASSES)) | set(_names(DURABLE_CLASSES))) - found)
    assert not stale, f"registered classes no production code creates: {stale}"


def test_classify_data_child_reads_the_registry():
    assert classify_data_child("job_workspaces") == "ephemeral"
    assert classify_data_child("jobs") == "durable"
    assert classify_data_child("review_staging.Ab12Cd") == "ephemeral"
    assert classify_data_child("review_stagingX") is None
    assert classify_data_child("task_jobs") is None


def test_data_class_dir_refuses_an_unregistered_name(tmp_path):
    assert data_paths.data_class_dir("runs", tmp_path) == tmp_path / "runs"
    try:
        data_paths.data_class_dir("task_jobs", tmp_path)
    except KeyError:
        return
    raise AssertionError("an unregistered class name resolved to a directory")


def test_the_scanner_finds_every_spelling_it_claims(tmp_path):
    """The scanner's own standing red proof, over a planted tree."""
    files = {
        "packages/p/a.py": (
            "from pathlib import Path\n"
            "from packages.orchestration.data_paths import resolve_data_root\n"
            "SUB = 'by_constant'\n"
            "def f(data_dir, root):\n"
            "    r = resolve_data_root()\n"
            "    ui = Path(resolve_data_root()) / 'direct_path'\n"
            "    d = data_dir or resolve_data_root()\n"
            "    return (r / 'bound_name', ui / 'not_a_child', d / 'bool_op',\n"
            "            data_dir / 'param', root / 'repo_child', r / SUB,\n"
            "            resolve_data_root() / 'nested' / 'deeper', Path('.data/dotted'))\n"),
        "scripts/s.sh": 'mktemp -d "$ROOT/.data/from_shell.XXXX"\n',
    }
    for rel, text in files.items():
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    assert sorted(scan_tree(tmp_path)) == [
        "bool_op", "bound_name", "by_constant", "direct_path", "dotted",
        "from_shell", "nested", "param"]
