"""
Context compiler — import-neighbor graphs (T001) and signatures (T002), F107.

The context compiler stops handing tasks whole files regardless of relevance:
it selects fenced-path files, their direct import neighbors, and only
signatures of distant dependencies (docs/roadmap/features/T2_F107.md). This
module carries two of that compiler's layers. The GRAPH layer answers "which
files does this file import" per file, in both languages that matter now —
Python and TypeScript-ish frontends. The SIGNATURE layer answers "what does
this file declare", rendering a file down to headers and docstring first
lines so a distant dependency costs a few lines instead of its whole body.

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
file's orchestrator brief rejects any diff adding one). The TS SIGNATURE
scanner shares those line-level heuristic limitations: it too reads one line
at a time, so a multi-line export statement contributes only its first line
and a commented-out ``export`` is rendered like real code.

This module is PURE per-file computation: it never follows a neighbor's own
imports, so cyclic imports terminate by construction, and it never calls a
provider, touches the network, or writes evidence. Stdlib only. Determinism:
every graph output is a sorted, deduplicated tuple of repo-relative POSIX
paths and every signature output is a source-ordered tuple of rendered lines —
the same tree always yields the same graph and the same signatures.

Public API::

    ImportNeighbors                    — one file's resolved/external split
    python_import_neighbors(root, rel_path)     -> ImportNeighbors
    typescript_import_neighbors(root, rel_path) -> ImportNeighbors
    build_import_neighbor_graph(root, rel_paths) -> dict[str, ImportNeighbors]
    FileSignatures                     — one file's rendered signature lines
    fits_inline_size_cap(root, rel_path)        -> bool
    python_file_signatures(root, rel_path)      -> FileSignatures
    typescript_file_signatures(root, rel_path)  -> FileSignatures
    extract_file_signatures(root, rel_path)     -> FileSignatures
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

# A TS/JS declaration counts as a signature only when the line's FIRST
# non-space characters are the word `export` — a mid-line `export` is not a
# declaration head, and `exports.x` is not the keyword (no word boundary).
_TS_EXPORT_LINE_RE = re.compile(r"^\s*export\b")

# Tier 2 of the F107 tier table (direct import neighbors) is inlined in full
# only up to this per-file size, then demoted to signatures. 16 KiB is roughly
# 4k tokens of source — one neighbor may not eat a whole context budget.
DEFAULT_INLINE_SIZE_CAP_BYTES = 16384

# A rendered signature list is itself capped, so one generated or vendored
# giant cannot flood the context that signatures exist to shrink.
DEFAULT_SIGNATURE_LINE_CAP = 200

# Python nodes that produce a signature header, at any nesting depth.
_PYTHON_SIGNATURE_NODES = (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)

# Statement-list fields of compound statements, in source order — walked so a
# `def` nested in an `if`/`try`/`match` is still found.
_PYTHON_BODY_FIELDS = ("body", "handlers", "orelse", "finalbody", "cases")

# Three double-quotes, the wrapper a rendered docstring line carries.
_DOCSTRING_FENCE = '"""'

# One nesting level of rendered indentation.
_SIGNATURE_INDENT = "    "


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


# --------------------------------------------------------------------------
# Signatures (F107 T002) — what a file DECLARES, without its bodies
# --------------------------------------------------------------------------


# One file rendered down to declaration headers and docstring first lines,
# which is what tiers 2 and 3 of the F107 tier table send instead of content.
@dataclass(frozen=True)
class FileSignatures:
    """A single file's rendered signature lines, in source order.

    ``lines`` holds the rendered lines; ``truncated`` is True when the line
    cap cut the rendering short, so the caller knows the list is partial;
    ``parse_failed`` is True when the source could not be read or parsed —
    the caller decides what tier an unrenderable file lands in.
    """

    lines: tuple[str, ...] = ()
    truncated: bool = False
    parse_failed: bool = False


def _capped_signatures(lines: list[str], line_cap: int) -> FileSignatures:
    """Freeze the rendered lines, keeping the FIRST ``line_cap`` of them."""
    if len(lines) > line_cap:
        return FileSignatures(tuple(lines[:line_cap]), truncated=True)
    return FileSignatures(tuple(lines))


def fits_inline_size_cap(
    root: Path, rel_path: str, cap_bytes: int = DEFAULT_INLINE_SIZE_CAP_BYTES
) -> bool:
    """The tier-2 demotion switch: may this file be inlined in full?

    True when the path is a file under root whose size in BYTES is at most
    ``cap_bytes`` — a file exactly at the cap fits. A path that is not a file
    is False, because nothing that does not exist can be inlined. This
    function decides nothing else; the selector demotes to signatures.
    """
    target = root / rel_path
    try:
        if not target.is_file():
            return False
        return target.stat().st_size <= cap_bytes
    except OSError:
        return False


# --------------------------------------------------------------------------
# Python signatures (ast-based)
# --------------------------------------------------------------------------


def _docstring_signature_line(node: ast.AST) -> str | None:
    """Render a node's docstring as its first NON-EMPTY line inside triple
    quotes — None when there is no docstring or it is entirely blank."""
    try:
        raw = ast.get_docstring(node, clean=False)
    except TypeError:
        return None
    if raw is None:
        return None
    for line in raw.splitlines():
        stripped = line.strip()
        if stripped:
            return _DOCSTRING_FENCE + stripped + _DOCSTRING_FENCE
    return None


def _render_python_signature_header(node: ast.AST) -> str:
    """Reconstruct one declaration header FROM THE AST, never from the source,
    so a signature spread over several source lines collapses to one line."""
    if isinstance(node, ast.ClassDef):
        # Bases only, per the T002 contract: no empty parentheses when there
        # are none, and class keywords (metaclass=…) are deliberately absent.
        bases = ", ".join(ast.unparse(base) for base in node.bases)
        return f"class {node.name}({bases}):" if bases else f"class {node.name}:"
    prefix = "async def " if isinstance(node, ast.AsyncFunctionDef) else "def "
    header = f"{prefix}{node.name}({ast.unparse(node.args)})"
    if node.returns is not None:
        header += f" -> {ast.unparse(node.returns)}"
    return header + ":"


def _python_child_statements(node: ast.AST) -> list[ast.AST]:
    """Statement lists nested inside one compound statement, in source order."""
    nested: list[ast.AST] = []
    for field in _PYTHON_BODY_FIELDS:
        nested.extend(getattr(node, field, None) or [])
    return nested


def _collect_python_signature_lines(
    nodes: Iterable[ast.AST], depth: int, out: list[str]
) -> None:
    """Append rendered lines for every declaration in ``nodes``, recursing so
    declarations at ANY nesting depth appear, indented one level per depth."""
    for node in nodes:
        if isinstance(node, _PYTHON_SIGNATURE_NODES):
            indent = _SIGNATURE_INDENT * depth
            out.append(indent + _render_python_signature_header(node))
            docstring_line = _docstring_signature_line(node)
            if docstring_line is not None:
                out.append(indent + _SIGNATURE_INDENT + docstring_line)
            _collect_python_signature_lines(node.body, depth + 1, out)
        else:
            nested = _python_child_statements(node)
            if nested:
                # Not a declaration, so the depth does not grow.
                _collect_python_signature_lines(nested, depth, out)


def python_file_signatures(
    root: Path, rel_path: str, line_cap: int = DEFAULT_SIGNATURE_LINE_CAP
) -> FileSignatures:
    """Signature lines of one Python file under root, via ``ast``.

    Renders, in source order: the module docstring's first non-empty line;
    every class/def/async def header at any nesting depth, indented four
    spaces per level; and directly after each header that node's docstring
    first non-empty line, four spaces deeper again. Decorators, bodies,
    imports and assignments never appear. Unreadable source or a SyntaxError
    yields ``parse_failed=True`` with empty lines; more than ``line_cap``
    rendered lines keeps the first ``line_cap`` and sets ``truncated=True``.
    """
    try:
        source = (root / rel_path).read_text(encoding="utf-8")
        tree = ast.parse(source)
    except (OSError, SyntaxError, ValueError):
        return FileSignatures(parse_failed=True)

    lines: list[str] = []
    module_docstring_line = _docstring_signature_line(tree)
    if module_docstring_line is not None:
        lines.append(module_docstring_line)
    _collect_python_signature_lines(tree.body, 0, lines)
    return _capped_signatures(lines, line_cap)


# --------------------------------------------------------------------------
# TypeScript / JavaScript signatures (line-level heuristic)
# --------------------------------------------------------------------------


def _render_typescript_signature_line(line: str) -> str:
    """Deliberately minimal so the rendering stays predictable: strip both
    ends, then drop a TRAILING ``{`` and the whitespace before it. Nothing
    else is rewritten — no mid-line cutting, no semicolon removal."""
    stripped = line.strip()
    if stripped.endswith("{"):
        stripped = stripped[:-1].rstrip()
    return stripped


def typescript_file_signatures(
    root: Path, rel_path: str, line_cap: int = DEFAULT_SIGNATURE_LINE_CAP
) -> FileSignatures:
    """Signature lines of one TS/JS file, via the line-level export scanner.

    One entry per source line whose first non-space characters are the word
    ``export``, in source order — so non-exported declarations and a line
    where ``export`` appears mid-line contribute nothing. An unreadable file
    yields ``parse_failed=True``. Same ``line_cap`` and ``truncated``
    semantics as the Python extractor. Its heuristic limitations are the
    line-level ones the module docstring already documents.
    """
    try:
        source = (root / rel_path).read_text(encoding="utf-8")
    except (OSError, ValueError):
        return FileSignatures(parse_failed=True)

    lines = [
        _render_typescript_signature_line(line)
        for line in source.splitlines()
        if _TS_EXPORT_LINE_RE.match(line)
    ]
    return _capped_signatures(lines, line_cap)


def extract_file_signatures(
    root: Path, rel_path: str, line_cap: int = DEFAULT_SIGNATURE_LINE_CAP
) -> FileSignatures:
    """Signature lines for one file, dispatching on suffix.

    Same dispatch as ``build_import_neighbor_graph``: .py → the ast
    extractor, .ts/.tsx/.js/.jsx → the export scanner, anything else →
    ``parse_failed=True`` with empty lines, because no extractor claims it.
    Determinism: the same file always renders to the same tuple.
    """
    suffix = PurePosixPath(rel_path).suffix
    if suffix == ".py":
        return python_file_signatures(root, rel_path, line_cap)
    if suffix in _TS_SUFFIXES:
        return typescript_file_signatures(root, rel_path, line_cap)
    return FileSignatures(parse_failed=True)
