"""
Context compiler — graphs (T001), signatures (T002), selection (T003),
segments (T004 part 1).

The context compiler stops handing tasks whole files regardless of relevance:
it selects fenced-path files, their direct import neighbors, and only
signatures of distant dependencies (docs/roadmap/features/T2_F107.md). This
module carries four of that compiler's layers. The GRAPH layer answers "which
files does this file import" per file, in both languages that matter now —
Python and TypeScript-ish frontends. The SIGNATURE layer answers "what does
this file declare", rendering a file down to headers and docstring first
lines so a distant dependency costs a few lines instead of its whole body.
The SELECTOR layer answers "what does this task actually get": it assigns
every candidate path a tier, renders each tier, enforces a total token budget
by DEMOTING files rather than truncating any of them mid-content, and records
every demotion and omission with a reason — so "why didn't the model see X"
always has a written answer. The SEGMENT layer answers "how does that
selection enter a prompt": it renders the compiled context into segment text
and registers it into a ``PromptSegmentRegistry`` at rank ``JOB_CONTEXT``, so
the context arrives as a NAMED, RANKED segment the way F105 says prompts are
built, instead of as ad hoc concatenation. Composition stays where it already
lives: that registry owns ordering and the manifest, this feature owns
SELECTION.

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

The graph and signature layers are PURE per-file computation: neither follows
a neighbor's own imports, so cyclic imports terminate by construction. The
selector walks exactly TWO graph hops (fenced files, then their neighbors) and
never more, so it terminates for the same reason. Nothing here calls a
provider or touches the network, and nothing writes evidence EXCEPT the two
writers ``write_omitted_context_json`` and
``write_context_size_comparison_json``, each of which writes its record exactly
where its caller points it. Stdlib only, plus two intra-repo imports — the
repo's named token estimator ``estimate_text_tokens`` and the prompt segment
types of ``prompt_segments``, both reused rather than respelled. That second
import points ONE WAY only: ``prompt_segments`` imports nothing from here.
Determinism: every graph output is a sorted, deduplicated tuple of
repo-relative POSIX paths, every signature output is a source-ordered tuple of
rendered lines, and the same inputs always compile to the same context — which
the segment rendering inherits by walking ``included`` in its existing order.

Scope boundary — deliberate absences (a reader searching here should find this
rather than conclude the wiring was forgotten):
  - No builder prompt is migrated here. This module renders the compiled
    context into segment text and registers it at rank ``JOB_CONTEXT``; WHICH
    role's prompt carries that segment is T004 part 2 and later rounds.
  - The segment manifest is not written into evidence here. Composition and
    ``manifest_as_dicts()`` belong to ``prompt_segments``; wiring the manifest
    and the size comparison into run evidence is a later round.
  - There is no CLI view here. ``remedy job context`` is T004 part 2.

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
    SelectedFile                       — one file the context WILL carry
    OmissionRecord                     — one decision that left something out
    CompiledContext                    — one task's whole selection
    compile_task_context(root, fenced_paths, repo_paths) -> CompiledContext
    export_omitted_context_json(compiled)       -> list[dict]
    write_omitted_context_json(compiled, target_path) -> Path
    COMPILED_CONTEXT_SEGMENT_NAME      — the segment's name, spelled once
    OMITTED_CONTEXT_FILENAME           — the omissions filename, spelled once
    CONTEXT_SIZE_FILENAME              — the size-record filename, spelled once
    render_compiled_context_text(root, compiled) -> str
    register_compiled_context_segment(registry, root, compiled) -> PromptSegment
    ContextSizeComparison              — whole-files baseline vs compiled cost
    compare_context_size(root, repo_paths, compiled) -> ContextSizeComparison
    export_context_size_comparison_json(comparison) -> dict[str, Any]
    write_context_size_comparison_json(comparison, target_path) -> Path
"""

from __future__ import annotations

import ast
import json
import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from packages.orchestration.prompt_budget import resolve_task_class_cap
from packages.orchestration.prompt_segments import (
    PromptSegment,
    PromptSegmentRegistry,
    SegmentStabilityRank,
)
from packages.orchestration.token_economy import estimate_text_tokens

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


# --------------------------------------------------------------------------
# Selector (F107 T003) — tiers, budget demotion, the omissions record
# --------------------------------------------------------------------------


# The whole context one task may cost, in estimated tokens. 24k sits under the
# 32k context floor in packages/orchestration/token_economy.py, leaving room
# for the prompt around the files and for the generation itself.
DEFAULT_CONTEXT_TOKEN_BUDGET = 24000

# The F107 tier table, which IS the selection contract: (1) files in the
# task's declared write scope — full content; (2) their direct import
# neighbors — full up to the per-file size cap, else signatures;
# (3) transitive dependencies — signatures only; (4) everything else — gone.
TIER_FENCED = 1
TIER_NEIGHBOR = 2
TIER_DISTANT = 3
TIER_OMITTED = 4

# Why a file is not carried in full. Every OmissionRecord names exactly one.
OMISSION_REASON_BUDGET = "budget"
OMISSION_REASON_DISTANCE = "distance"
OMISSION_REASON_BINARY = "binary"
OMISSION_REASON_SIZE = "size"
# Its bytes decode but no extractor could parse it: signatures render EMPTY.
OMISSION_REASON_UNPARSEABLE = "unparseable"

# The two renderings a selected file can have, and the two outcomes an
# omission decision can have — "signatures" is both, because a demotion to
# signatures IS the outcome that keeps the file present in reduced form.
_RENDERING_FULL = "full"
_RENDERING_SIGNATURES = "signatures"
_OUTCOME_OMITTED = "omitted"
_OUTCOME_SIGNATURES = "signatures"


# One file the compiled context WILL carry, and in which rendering.
@dataclass(frozen=True)
class SelectedFile:
    """A single included file: its tier, its rendering, its estimated cost.

    ``rendering`` is ``"full"`` (the file's whole text) or ``"signatures"``
    (its rendered signature lines). ``estimated_tokens`` is
    ``estimate_text_tokens`` of whichever of those two texts will be sent, so
    the sum over the included files is the context's estimated cost.
    """

    rel_path: str
    tier: int
    rendering: str
    estimated_tokens: int


# One decision that kept a file, or part of one, out of the context. This is
# the record that answers "why didn't the model see X" after the fact.
@dataclass(frozen=True)
class OmissionRecord:
    """A single exclusion decision, with the tier it was made at.

    ``tier`` is the tier the file HELD when the decision was made — a tier-2
    neighbor demoted by the budget records tier 2, not tier 4. ``reason`` is
    one of the five ``OMISSION_REASON_*`` values; ``outcome`` is ``"omitted"``
    (gone entirely) or ``"signatures"`` (still present, in reduced form), a
    distinction the reason alone cannot carry.
    """

    rel_path: str
    tier: int
    reason: str
    outcome: str


# One task's whole selection: what is carried, what is not, and the budget it
# was measured against.
@dataclass(frozen=True)
class CompiledContext:
    """The compiled context for one task.

    ``included`` and ``omissions`` are both sorted by ``(tier, rel_path)``.
    ``estimated_tokens`` is the sum over ``included``. ``over_budget`` is True
    when every demotion phase is exhausted and the declared write scope alone
    still exceeds ``budget_tokens`` — the compiler reports that overflow
    rather than cutting the files the task must edit. ``line_cap`` is the
    signature line cap this context was compiled at, carried so a rendering
    cannot drift from the estimate the budget was enforced against.
    """

    included: tuple[SelectedFile, ...]
    omissions: tuple[OmissionRecord, ...]
    estimated_tokens: int
    budget_tokens: int
    over_budget: bool
    line_cap: int


def _read_utf8_text(root: Path, rel_path: str) -> str | None:
    """The file's decoded text, or None when it is unreadable or not UTF-8.

    This IS the binary test the selector uses: a file whose bytes do not
    decode cannot be inlined at all, so it is decided by decoding rather than
    by sniffing an extension.
    """
    try:
        return (root / rel_path).read_bytes().decode("utf-8")
    except (OSError, ValueError):
        return None


def _signature_render_text(root: Path, rel_path: str, line_cap: int) -> str:
    """Exactly the text a "signatures" rendering sends: the extractor's lines
    joined by newlines. Estimates are taken from this, never from the file."""
    return "\n".join(extract_file_signatures(root, rel_path, line_cap).lines)


def _import_neighbor_files(root: Path, rel_paths: Iterable[str]) -> set[str]:
    """Every file the given files import, unioned — one graph hop outward.

    Only ``resolved`` entries appear: an external specifier resolves to no
    file under root, so there is nothing to select.
    """
    graph = build_import_neighbor_graph(root, rel_paths)
    return {
        neighbor
        for neighbors in graph.values()
        for neighbor in neighbors.resolved
    }


def _largest_tokens_first(
    chosen: dict[str, SelectedFile], tier: int, rendering: str | None
) -> str | None:
    """The budget's victim rule in ONE place: within a tier (and optionally
    one rendering), the largest ``estimated_tokens`` is picked, ties broken by
    ``rel_path`` ascending. None when the tier holds no such file left."""
    candidates = [
        selected
        for selected in chosen.values()
        if selected.tier == tier
        and (rendering is None or selected.rendering == rendering)
    ]
    if not candidates:
        return None
    return min(candidates, key=lambda s: (-s.estimated_tokens, s.rel_path)).rel_path


def compile_task_context(
    root: Path,
    fenced_paths: Iterable[str],
    repo_paths: Iterable[str],
    *,
    token_budget: int = DEFAULT_CONTEXT_TOKEN_BUDGET,
    inline_cap_bytes: int = DEFAULT_INLINE_SIZE_CAP_BYTES,
    line_cap: int = DEFAULT_SIGNATURE_LINE_CAP,
) -> CompiledContext:
    """Select and render one task's context under a total token budget.

    ``fenced_paths`` is the task's declared write scope (files_hint + fence
    allow scope, already resolved by the caller); ``repo_paths`` is the
    candidate listing the caller walked — this function never walks a tree
    itself. Both are order-insensitive and deduplicated on input.

    Tiers, in order: tier 1 is every fenced path that exists under root,
    always carried in FULL and never demoted or dropped for size or budget; a
    fenced path with no file under root is not a candidate at all and is
    dropped silently. Tier 2 is the direct import neighbors of tier 1, full
    when ``fits_inline_size_cap`` allows and signatures otherwise. Tier 3 is
    one hop further out, signatures always — that is tier 3's normal
    rendering, not a demotion, so it carries no record. Tier 4 is every
    remaining candidate, omitted for distance. A tier-1, tier-2 or tier-3 file
    whose bytes are not valid UTF-8 is omitted outright — the one case that
    removes a fenced file, because a binary blob cannot be inlined. A
    non-tier-1 file that decodes but that no extractor can parse is still
    carried, yet its signature rendering is EMPTY, so it also records an
    ``unparseable`` omission — that record is what explains the blank. Tier 1
    is exempt: an unparseable fenced file is carried whole and records nothing.

    Over budget, three phases run in order, each repeating while the total
    still exceeds ``token_budget``: (A) demote the largest full tier-2 file to
    signatures, (B) omit the largest tier-3 file, (C) omit the largest tier-2
    file. Nothing is ever truncated mid-content. When all three are exhausted
    and tier 1 alone still exceeds the budget, the overflow is reported as
    ``over_budget=True`` instead of cutting the declared write scope.
    """
    omissions: list[OmissionRecord] = []
    chosen: dict[str, SelectedFile] = {}

    fenced = {rel_path for rel_path in set(fenced_paths) if (root / rel_path).is_file()}
    neighbors = _import_neighbor_files(root, fenced) - fenced
    distant = _import_neighbor_files(root, neighbors) - fenced - neighbors
    remaining = set(repo_paths) - fenced - neighbors - distant

    for rel_path in sorted(fenced):
        text = _read_utf8_text(root, rel_path)
        if text is None:
            omissions.append(
                OmissionRecord(
                    rel_path, TIER_FENCED, OMISSION_REASON_BINARY, _OUTCOME_OMITTED
                )
            )
            continue
        chosen[rel_path] = SelectedFile(
            rel_path, TIER_FENCED, _RENDERING_FULL, estimate_text_tokens(text)
        )

    for rel_path in sorted(neighbors):
        text = _read_utf8_text(root, rel_path)
        if text is None:
            omissions.append(
                OmissionRecord(
                    rel_path, TIER_NEIGHBOR, OMISSION_REASON_BINARY, _OUTCOME_OMITTED
                )
            )
            continue
        if fits_inline_size_cap(root, rel_path, inline_cap_bytes):
            chosen[rel_path] = SelectedFile(
                rel_path, TIER_NEIGHBOR, _RENDERING_FULL, estimate_text_tokens(text)
            )
            continue
        signatures = extract_file_signatures(root, rel_path, line_cap)
        chosen[rel_path] = SelectedFile(
            rel_path,
            TIER_NEIGHBOR,
            _RENDERING_SIGNATURES,
            estimate_text_tokens("\n".join(signatures.lines)),
        )
        omissions.append(
            OmissionRecord(
                rel_path, TIER_NEIGHBOR, OMISSION_REASON_SIZE, _OUTCOME_SIGNATURES
            )
        )
        if signatures.parse_failed:
            omissions.append(
                OmissionRecord(
                    rel_path,
                    TIER_NEIGHBOR,
                    OMISSION_REASON_UNPARSEABLE,
                    _OUTCOME_SIGNATURES,
                )
            )

    for rel_path in sorted(distant):
        if _read_utf8_text(root, rel_path) is None:
            omissions.append(
                OmissionRecord(
                    rel_path, TIER_DISTANT, OMISSION_REASON_BINARY, _OUTCOME_OMITTED
                )
            )
            continue
        signatures = extract_file_signatures(root, rel_path, line_cap)
        chosen[rel_path] = SelectedFile(
            rel_path,
            TIER_DISTANT,
            _RENDERING_SIGNATURES,
            estimate_text_tokens("\n".join(signatures.lines)),
        )
        if signatures.parse_failed:
            omissions.append(
                OmissionRecord(
                    rel_path,
                    TIER_DISTANT,
                    OMISSION_REASON_UNPARSEABLE,
                    _OUTCOME_SIGNATURES,
                )
            )

    for rel_path in sorted(remaining):
        omissions.append(
            OmissionRecord(
                rel_path, TIER_OMITTED, OMISSION_REASON_DISTANCE, _OUTCOME_OMITTED
            )
        )

    # Phase A — a full neighbor becomes signatures before anything is dropped.
    while sum(s.estimated_tokens for s in chosen.values()) > token_budget:
        victim = _largest_tokens_first(chosen, TIER_NEIGHBOR, _RENDERING_FULL)
        if victim is None:
            break
        signatures = extract_file_signatures(root, victim, line_cap)
        chosen[victim] = SelectedFile(
            victim,
            TIER_NEIGHBOR,
            _RENDERING_SIGNATURES,
            estimate_text_tokens("\n".join(signatures.lines)),
        )
        omissions.append(
            OmissionRecord(
                victim, TIER_NEIGHBOR, OMISSION_REASON_BUDGET, _OUTCOME_SIGNATURES
            )
        )
        if signatures.parse_failed:
            omissions.append(
                OmissionRecord(
                    victim,
                    TIER_NEIGHBOR,
                    OMISSION_REASON_UNPARSEABLE,
                    _OUTCOME_SIGNATURES,
                )
            )

    # Phase B — then the distant files go, being the least relevant.
    while sum(s.estimated_tokens for s in chosen.values()) > token_budget:
        victim = _largest_tokens_first(chosen, TIER_DISTANT, None)
        if victim is None:
            break
        del chosen[victim]
        omissions.append(
            OmissionRecord(
                victim, TIER_DISTANT, OMISSION_REASON_BUDGET, _OUTCOME_OMITTED
            )
        )

    # Phase C — only then do neighbors leave entirely. Tier 1 never does.
    while sum(s.estimated_tokens for s in chosen.values()) > token_budget:
        victim = _largest_tokens_first(chosen, TIER_NEIGHBOR, None)
        if victim is None:
            break
        del chosen[victim]
        omissions.append(
            OmissionRecord(
                victim, TIER_NEIGHBOR, OMISSION_REASON_BUDGET, _OUTCOME_OMITTED
            )
        )

    included = tuple(
        sorted(chosen.values(), key=lambda s: (s.tier, s.rel_path))
    )
    total_tokens = sum(selected.estimated_tokens for selected in included)
    return CompiledContext(
        included=included,
        omissions=tuple(sorted(omissions, key=lambda o: (o.tier, o.rel_path))),
        estimated_tokens=total_tokens,
        budget_tokens=token_budget,
        over_budget=total_tokens > token_budget,
        line_cap=line_cap,
    )


@dataclass(frozen=True)
class ClassBudgetFit:
    """Whether ``task_class``'s compiled context fits its resolved cap (F112 T002).

    ``fits`` is False exactly for the ``cannot_fit`` outcome
    (docs/roadmap/features/T3_F112.md Design): tier-1 content alone still
    exceeds ``cap_tokens`` after the existing demotion cascade has demoted or
    dropped every tier-2 and tier-3 candidate, which is also why
    ``tier1_tokens`` equals ``compiled.estimated_tokens`` in that case.
    """

    compiled: CompiledContext
    task_class: str
    cap_tokens: int
    cap_source: str
    fits: bool
    tier1_tokens: int


def fit_task_context_to_class_cap(
    root: Path,
    fenced_paths: Iterable[str],
    repo_paths: Iterable[str],
    task_class: str,
    *,
    inline_cap_bytes: int = DEFAULT_INLINE_SIZE_CAP_BYTES,
    line_cap: int = DEFAULT_SIGNATURE_LINE_CAP,
) -> ClassBudgetFit:
    """Compile ``task_class``'s context under its resolved per-class cap.

    Resolves the cap via
    :func:`packages.orchestration.prompt_budget.resolve_task_class_cap`
    (F112 T001), then runs ``compile_task_context`` unchanged at that
    budget — no new selection or demotion logic, only the class-specific
    number the existing cascade enforces
    (docs/roadmap/features/T3_F112.md Design). ``fits`` is False exactly
    when tier-1 content alone still exceeds the cap after every tier-2 and
    tier-3 candidate has been demoted or dropped, carrying the arithmetic
    (``tier1_tokens``, ``cap_tokens``, ``task_class``) the ``cannot_fit``
    task-split decision needs (T003).
    """
    resolution = resolve_task_class_cap(task_class)
    compiled = compile_task_context(
        root,
        fenced_paths,
        repo_paths,
        token_budget=resolution.cap_tokens,
        inline_cap_bytes=inline_cap_bytes,
        line_cap=line_cap,
    )
    tier1_tokens = sum(
        selected.estimated_tokens
        for selected in compiled.included
        if selected.tier == TIER_FENCED
    )
    return ClassBudgetFit(
        compiled=compiled,
        task_class=task_class,
        cap_tokens=resolution.cap_tokens,
        cap_source=resolution.source,
        fits=not compiled.over_budget,
        tier1_tokens=tier1_tokens,
    )


def export_omitted_context_json(compiled: CompiledContext) -> list[dict]:
    """The omissions record as JSON-ready dicts, in ``compiled.omissions``
    order, one per record, with exactly the keys path/tier/reason/outcome.
    PURE: touches no disk, and carries no absolute path — ``rel_path`` is
    already repo-relative."""
    return [
        {
            "path": record.rel_path,
            "tier": record.tier,
            "reason": record.reason,
            "outcome": record.outcome,
        }
        for record in compiled.omissions
    ]


def write_omitted_context_json(compiled: CompiledContext, target_path: Path) -> Path:
    """Write the omissions record to ``target_path`` and return that path.

    ONE OF THE TWO writing functions in this module — the other is
    ``write_context_size_comparison_json`` — and NEITHER of them picks its own
    location. It creates the parent directory, writes
    ``export_omitted_context_json(compiled)`` as JSON with ``indent=2`` and a
    trailing newline, and writes nowhere but where the caller pointed.
    """
    target = Path(target_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(export_omitted_context_json(compiled), indent=2)
    target.write_text(payload + "\n", encoding="utf-8")
    return target


# --------------------------------------------------------------------------
# Segments (F107 T004 part 1) — the compiled context as a ranked prompt segment
# --------------------------------------------------------------------------


#: The name the compiled context registers under. One spelling, so the segment,
#: its manifest row and every test that looks for it agree by construction.
COMPILED_CONTEXT_SEGMENT_NAME = "compiled_context"

#: The omissions record's filename, named ONCE so the writer, the future CLI
#: view and every test spell it the same way. It is a BARE FILENAME and never a
#: path: where the file sits is the caller's decision, and
#: ``write_omitted_context_json`` already takes the full target path.
OMITTED_CONTEXT_FILENAME = "omitted_context.json"

#: The size comparison's filename, named ONCE so the writer, the evidence
#: wiring and every test spell it the same way. Like its omissions sibling it is
#: a BARE FILENAME and never a path: where the file sits is the caller's
#: decision, and ``write_context_size_comparison_json`` already takes the full
#: target path.
CONTEXT_SIZE_FILENAME = "context_size.json"


def render_compiled_context_text(root: Path, compiled: CompiledContext) -> str:
    """The compiled context as prompt-segment text: one block per included file.

    Blocks follow ``compiled.included`` order — already sorted by
    ``(tier, rel_path)``, so this rendering INHERITS the selector's determinism
    instead of inventing an order of its own — and are joined by a blank line.
    Each block is a header line ``# <rel_path> — tier <n> (<rendering>)``
    followed by the body: the file's full decoded text when ``rendering`` is
    ``"full"``, and the signature lines joined by newlines when it is
    ``"signatures"``. Trailing newlines are stripped from each body so that
    blank line stays the ONLY separator between blocks and the text does not
    depend on whether a file happens to end in a newline.

    An OMITTED file contributes NOTHING here — not its content and not its
    path. The omissions record is where those live, and keeping the two apart
    is exactly the separation the debugging view depends on. An empty
    ``included`` renders to the empty string.

    PURE READ: it opens the included files and nothing else, never walks a tree
    and never writes. Signature bodies are rendered at ``compiled.line_cap``,
    the cap the context was compiled at, so the rendered text and
    ``estimated_tokens`` describe the same bytes.
    """
    blocks: list[str] = []
    for selected in compiled.included:
        path = selected.rel_path
        if selected.rendering == _RENDERING_SIGNATURES:
            body = _signature_render_text(root, path, compiled.line_cap)
        else:
            text = _read_utf8_text(root, path)
            body = text if text is not None else ""
        header = f"# {path} — tier {selected.tier} ({selected.rendering})"
        blocks.append(header + "\n" + body.rstrip("\n"))
    return "\n\n".join(blocks)


def register_compiled_context_segment(
    registry: PromptSegmentRegistry, root: Path, compiled: CompiledContext
) -> PromptSegment:
    """Register the compiled context into ``registry`` at rank ``JOB_CONTEXT``.

    ``JOB_CONTEXT`` is the rank because the compiled context IS the job/task
    context of a prompt: it composes after the stable system and conventions
    prefixes a provider cache wants byte-identical, and before the volatile
    task and steering tails. The choice is pinned by a test, so a silent move
    to another rank is red rather than invisible.

    This function adds NO discipline of its own. A second call against the same
    registry raises the registry's own ``PromptSegmentError`` — the duplicate
    rule lives in ``prompt_segments`` and is inherited here, never
    re-implemented and never prevented in advance.
    """
    return registry.register(
        COMPILED_CONTEXT_SEGMENT_NAME,
        SegmentStabilityRank.JOB_CONTEXT,
        render_compiled_context_text(root, compiled),
    )


# What whole-file context would have cost against what the compiled context
# costs — the measurement the feature's Done condition rests on.
@dataclass(frozen=True)
class ContextSizeComparison:
    """The compiled context's saving against a whole-files baseline.

    ``saved_tokens`` MAY BE NEGATIVE and is reported as it falls: a selection
    that grew the context has to show that, and clamping it to zero would hide
    the one number the comparison exists to expose. ``saved_ratio`` is exactly
    ``0.0`` when ``whole_file_tokens`` is 0, because a zero baseline has no
    ratio and inventing one would be a fabricated number.
    """

    whole_file_tokens: int
    compiled_tokens: int
    saved_tokens: int
    saved_ratio: float


def compare_context_size(
    root: Path, repo_paths: Iterable[str], compiled: CompiledContext
) -> ContextSizeComparison:
    """Measure the compiled context against sending ``repo_paths`` whole.

    ``whole_file_tokens`` sums ``estimate_text_tokens`` over the full text of
    every path in ``repo_paths`` that both exists under root and decodes as
    UTF-8. A missing path and a path whose bytes are not UTF-8 each contribute
    0 and never raise: the baseline is "what whole files would have cost", and
    a file that could not be inlined either way costs nothing either way.
    ``compiled_tokens`` is ``compiled.estimated_tokens`` READ, never recomputed,
    so the two sides of the comparison cannot drift apart.

    PURE: it reads files and writes nothing.
    """
    whole_file_tokens = 0
    for rel_path in repo_paths:
        text = _read_utf8_text(root, rel_path)
        if text is not None:
            whole_file_tokens += estimate_text_tokens(text)
    compiled_tokens = compiled.estimated_tokens
    saved_tokens = whole_file_tokens - compiled_tokens
    return ContextSizeComparison(
        whole_file_tokens=whole_file_tokens,
        compiled_tokens=compiled_tokens,
        saved_tokens=saved_tokens,
        saved_ratio=saved_tokens / whole_file_tokens if whole_file_tokens else 0.0,
    )


def export_context_size_comparison_json(comparison: ContextSizeComparison) -> dict[str, Any]:
    """The size comparison as one JSON-ready dict of exactly four fields.

    Carries ``whole_file_tokens``, ``compiled_tokens``, ``saved_tokens`` and
    ``saved_ratio`` as plain JSON types, READ off the dataclass and never
    rounded, clamped or recomputed. A NEGATIVE ``saved_tokens`` therefore
    reaches the record unchanged — a selection that grew the context has to show
    that — and ``saved_ratio`` is exactly ``0.0`` only where the zero baseline
    already put it, never a ratio this function invented. An export that
    quietly disagreed with ``ContextSizeComparison`` would turn the written
    record into a second, wrong source of truth.

    PURE: touches no disk, and carries no absolute path.
    """
    return {
        "whole_file_tokens": comparison.whole_file_tokens,
        "compiled_tokens": comparison.compiled_tokens,
        "saved_tokens": comparison.saved_tokens,
        "saved_ratio": comparison.saved_ratio,
    }


def write_context_size_comparison_json(
    comparison: ContextSizeComparison, target_path: Path
) -> Path:
    """Write the size comparison to ``target_path`` and return that path.

    The SECOND of this module's two writing functions — the other is
    ``write_omitted_context_json`` — and like it, it picks no location of its
    own. It creates the parent directory, writes
    ``export_context_size_comparison_json(comparison)`` as JSON with
    ``indent=2`` and a trailing newline, and writes nowhere but where the caller
    pointed.
    """
    target = Path(target_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(export_context_size_comparison_json(comparison), indent=2)
    target.write_text(payload + "\n", encoding="utf-8")
    return target
