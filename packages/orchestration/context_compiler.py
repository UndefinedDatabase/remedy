"""
Context compiler — import-neighbor graphs (F107 T001).

The context compiler stops handing tasks whole files regardless of relevance:
it selects fenced-path files, their direct import neighbors, and only
signatures of distant dependencies (docs/roadmap/features/T2_F107.md). This
module is the GRAPH layer of that compiler: given a repo root and a set of
repo-relative files, it answers "which files does this file import" per file,
in both languages that matter now — Python and TypeScript-ish frontends.

Python neighbors come from ``ast``: real parsing, absolute and relative
imports resolved against the importing file's package, ``from pkg import
name`` disambiguated between name-is-a-module and name-is-a-symbol by looking
at the tree on disk.

The TS/JS scanner is HONESTLY A HEURISTIC: it is a line-level regex over
import/export/require lines, it does not parse. Documented v1 limitations:
  - multi-line import statements are not matched (the specifier line alone
    usually still matches; a statement whose ``from '<spec>'`` clause sits on
    its own continuation line is missed),
  - dynamic ``import()`` expressions and computed/string-built requires are
    invisible,
  - commented-out imports ARE matched — the scanner cannot tell a comment
    from code.
A real TS parser is a later upgrade, not a hidden dependency now (the feature
file's orchestrator brief rejects any diff adding one).

This module is PURE per-file computation: it never follows a neighbor's own
imports, so cyclic imports terminate by construction, and it never calls a
provider, touches the network, or writes evidence. Stdlib only. Determinism:
every output is a sorted, deduplicated tuple of repo-relative POSIX paths —
the same tree always yields the same graph.

Public API::

    ImportNeighbors                    — one file's resolved/external split
    python_import_neighbors(root, rel_path)     -> ImportNeighbors
    typescript_import_neighbors(root, rel_path) -> ImportNeighbors
    build_import_neighbor_graph(root, rel_paths) -> dict[str, ImportNeighbors]
"""

from __future__ import annotations

import ast
import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

# Resolution order is part of the T001 contract: exact file, then these
# suffixes appended, then <spec>/index.<suffix> — first hit wins.
_TS_SUFFIXES = (".ts", ".tsx", ".js", ".jsx")

# Line-level TS/JS import shapes (heuristic, see module docstring):
# import ... from '<spec>' / bare import '<spec>' / export ... from '<spec>'
# / require('<spec>'). [^'\"] between keywords keeps a match from jumping
# across quoted strings on the same line.
_TS_IMPORT_FROM_RE = re.compile(r"""\bimport\s+[^'"]*?\bfrom\s+['"]([^'"]+)['"]""")
_TS_BARE_IMPORT_RE = re.compile(r"""\bimport\s+['"]([^'"]+)['"]""")
_TS_EXPORT_FROM_RE = re.compile(r"""\bexport\s+[^'"]*?\bfrom\s+['"]([^'"]+)['"]""")
_TS_REQUIRE_RE = re.compile(r"""\brequire\(\s*['"]([^'"]+)['"]\s*\)""")
_TS_LINE_PATTERNS = (
    _TS_IMPORT_FROM_RE,
    _TS_BARE_IMPORT_RE,
    _TS_EXPORT_FROM_RE,
    _TS_REQUIRE_RE,
)


# One file's direct import neighbors, split into files found under root and
# specifiers that resolved to nothing there (stdlib, third-party, aliases).
@dataclass(frozen=True)
class ImportNeighbors:
    """Direct import neighbors of a single file.

    ``resolved`` holds repo-relative POSIX paths of neighbor files that exist
    under the scanned root; ``external`` holds the specifiers/modules that
    resolved to no file there. Both are sorted and deduplicated.
    ``parse_failed`` is True when the source could not be read or parsed —
    the caller decides what tier an unparseable file lands in.
    """

    resolved: tuple[str, ...] = ()
    external: tuple[str, ...] = ()
    parse_failed: bool = False


def _sorted_neighbors(
    resolved: set[str], external: set[str], self_path: str
) -> ImportNeighbors:
    """Freeze the collected sets: dedupe, sort, drop the importing file."""
    resolved.discard(self_path)
    return ImportNeighbors(tuple(sorted(resolved)), tuple(sorted(external)))


# --------------------------------------------------------------------------
# Python (ast-based)
# --------------------------------------------------------------------------


def _python_module_file(root: Path, parts: tuple[str, ...]) -> str | None:
    """Map dotted-module parts to a file under root: a/b.py, else a/b/__init__.py."""
    if not parts or any(not part for part in parts):
        return None
    base = PurePosixPath(*parts)
    for candidate in (base.with_suffix(".py"), base / "__init__.py"):
        if (root / candidate).is_file():
            return candidate.as_posix()
    return None


def _python_package_self_file(root: Path, parts: tuple[str, ...]) -> str | None:
    """Map a from-clause package to its own module file: pkg/__init__.py, else pkg.py."""
    if not parts or any(not part for part in parts):
        return None
    base = PurePosixPath(*parts)
    for candidate in (base / "__init__.py", base.with_suffix(".py")):
        if (root / candidate).is_file():
            return candidate.as_posix()
    return None


def _python_from_import_target(
    root: Path, pkg_parts: tuple[str, ...], name: str
) -> str | None:
    """Resolve one ``from <pkg> import <name>``: the name as a module of pkg
    when that file exists, else the pkg module itself."""
    if name != "*":
        hit = _python_module_file(root, pkg_parts + (name,))
        if hit is not None:
            return hit
    return _python_package_self_file(root, pkg_parts)


def _python_external_specifier(level: int, module: str | None, name: str) -> str:
    """Render an unresolved from-import the way the source spelled it (dots kept)."""
    spec = "." * level + (module or "")
    if name == "*":
        return spec or "."
    if module:
        return spec + "." + name
    return spec + name


def python_import_neighbors(root: Path, rel_path: str) -> ImportNeighbors:
    """Direct import neighbors of one Python file under root, via ``ast``.

    Absolute imports resolve ``a.b`` to a/b.py or a/b/__init__.py; from-imports
    prefer the imported name as a module of the package, falling back to the
    package module itself; relative imports resolve against the importing
    file's package. Specifiers resolving to no file under root land in
    ``external``. A SyntaxError yields ``parse_failed=True`` and empty tuples.
    """
    try:
        source = (root / rel_path).read_text(encoding="utf-8")
        tree = ast.parse(source)
    except (OSError, SyntaxError, ValueError):
        return ImportNeighbors(parse_failed=True)

    self_path = PurePosixPath(rel_path).as_posix()
    package_parts = PurePosixPath(rel_path).parent.parts
    resolved: set[str] = set()
    external: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                hit = _python_module_file(root, tuple(alias.name.split(".")))
                if hit is None:
                    external.add(alias.name)
                else:
                    resolved.add(hit)
        elif isinstance(node, ast.ImportFrom):
            level = node.level or 0
            if level - 1 > len(package_parts):
                # The relative import climbs out of the scanned root: nothing
                # to resolve against, so every name is external.
                for alias in node.names:
                    external.add(
                        _python_external_specifier(level, node.module, alias.name)
                    )
                continue
            if level:
                base_parts = package_parts[: len(package_parts) - (level - 1)]
            else:
                base_parts = ()
            module_parts = tuple(node.module.split(".")) if node.module else ()
            pkg_parts = base_parts + module_parts
            for alias in node.names:
                hit = _python_from_import_target(root, pkg_parts, alias.name)
                if hit is None:
                    external.add(
                        _python_external_specifier(level, node.module, alias.name)
                    )
                else:
                    resolved.add(hit)

    return _sorted_neighbors(resolved, external, self_path)


# --------------------------------------------------------------------------
# TypeScript / JavaScript (line-level heuristic)
# --------------------------------------------------------------------------


def _ts_normalize_relative(importer_dir: str, spec: str) -> str | None:
    """Join a ./ or ../ specifier onto the importer's directory and normalize;
    None when the path climbs out of the scanned root."""
    joined = f"{importer_dir}/{spec}" if importer_dir else spec
    normalized: list[str] = []
    for part in PurePosixPath(joined).parts:
        if part == ".":
            continue
        if part == "..":
            if not normalized:
                return None
            normalized.pop()
        else:
            normalized.append(part)
    if not normalized:
        return None
    return "/".join(normalized)


def _ts_resolve_relative(root: Path, importer_dir: str, spec: str) -> str | None:
    """Contract resolution order: exact path, +.ts/.tsx/.js/.jsx, then
    <spec>/index.(ts|tsx|js|jsx) — first hit wins."""
    base = _ts_normalize_relative(importer_dir, spec)
    if base is None:
        return None
    candidates = [base]
    candidates += [base + suffix for suffix in _TS_SUFFIXES]
    candidates += [f"{base}/index{suffix}" for suffix in _TS_SUFFIXES]
    for candidate in candidates:
        if (root / candidate).is_file():
            return candidate
    return None


def typescript_import_neighbors(root: Path, rel_path: str) -> ImportNeighbors:
    """Direct import neighbors of one TS/JS file, via the line-level scanner.

    Only relative specifiers (./ or ../) are resolved to files; non-relative
    specifiers go to ``external`` verbatim. An unreadable file yields
    ``parse_failed=True``. Heuristic limitations are in the module docstring.
    """
    try:
        source = (root / rel_path).read_text(encoding="utf-8")
    except (OSError, ValueError):
        return ImportNeighbors(parse_failed=True)

    self_path = PurePosixPath(rel_path).as_posix()
    importer_dir = PurePosixPath(rel_path).parent.as_posix()
    if importer_dir == ".":
        importer_dir = ""

    specifiers: set[str] = set()
    for line in source.splitlines():
        for pattern in _TS_LINE_PATTERNS:
            for match in pattern.finditer(line):
                specifiers.add(match.group(1))

    resolved: set[str] = set()
    external: set[str] = set()
    for spec in specifiers:
        if spec.startswith(("./", "../")):
            hit = _ts_resolve_relative(root, importer_dir, spec)
            if hit is None:
                external.add(spec)
            else:
                resolved.add(hit)
        else:
            external.add(spec)

    return _sorted_neighbors(resolved, external, self_path)


# --------------------------------------------------------------------------
# Graph
# --------------------------------------------------------------------------


def build_import_neighbor_graph(
    root: Path, rel_paths: Iterable[str]
) -> dict[str, ImportNeighbors]:
    """Per-file import neighbors for every given repo-relative path.

    Dispatches on suffix (.py → Python, .ts/.tsx/.js/.jsx → TS/JS scanner,
    anything else → ``parse_failed=True`` with empty tuples). Purely per-file:
    no neighbor's imports are followed, so cyclic imports terminate by
    construction. Keys are the deduplicated input paths in sorted order.
    """
    graph: dict[str, ImportNeighbors] = {}
    for rel_path in sorted(set(rel_paths)):
        suffix = PurePosixPath(rel_path).suffix
        if suffix == ".py":
            graph[rel_path] = python_import_neighbors(root, rel_path)
        elif suffix in _TS_SUFFIXES:
            graph[rel_path] = typescript_import_neighbors(root, rel_path)
        else:
            graph[rel_path] = ImportNeighbors(parse_failed=True)
    return graph
