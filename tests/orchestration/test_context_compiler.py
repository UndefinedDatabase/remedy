"""Tests for the context compiler: import-neighbor graphs (F107 T001) and
signature extraction (F107 T002).

Every fixture tree is built under pytest's ``tmp_path`` and that tmp_path is
passed as ``root`` — nothing here reads the checkout, so the code under test
sees only the files the test wrote.

The signature goldens below were captured MECHANICALLY from the extractors and
must never be edited to make a failing test pass: an intentional change to the
rendering updates them in its own reviewed diff, with the change declared.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from packages.orchestration.context_compiler import (
    DEFAULT_INLINE_SIZE_CAP_BYTES,
    DEFAULT_SIGNATURE_LINE_CAP,
    FileSignatures,
    ImportNeighbors,
    build_import_neighbor_graph,
    extract_file_signatures,
    fits_inline_size_cap,
    python_file_signatures,
    python_import_neighbors,
    typescript_file_signatures,
    typescript_import_neighbors,
)

pytestmark = pytest.mark.unit


# Fixture trees are written file-by-file so each test states exactly the tree
# its assertion depends on — this is where a reader looks for the setup.
def _write_tree(root: Path, files: dict[str, str]) -> None:
    """Write every {repo-relative path: content} pair under root."""
    for rel_path, content in files.items():
        target = root / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


# --------------------------------------------------------------------------
# Python — absolute imports
# --------------------------------------------------------------------------


def test_python_absolute_import_resolves_module_and_package(tmp_path: Path) -> None:
    """`import pkg.mod` finds pkg/mod.py; `import pkg` falls back to pkg/__init__.py."""
    _write_tree(
        tmp_path,
        {
            "pkg/__init__.py": "",
            "pkg/mod.py": "",
            "caller.py": "import pkg.mod\n",
            "pkg_caller.py": "import pkg\n",
        },
    )

    assert python_import_neighbors(tmp_path, "caller.py").resolved == ("pkg/mod.py",)
    assert python_import_neighbors(tmp_path, "pkg_caller.py").resolved == ("pkg/__init__.py",)


def test_python_from_import_splits_module_from_symbol(tmp_path: Path) -> None:
    """`from pkg import mod` hits the module; `from pkg import VALUE` hits the package."""
    _write_tree(
        tmp_path,
        {
            "pkg/__init__.py": "VALUE = 1\n",
            "pkg/mod.py": "",
            "uses_module.py": "from pkg import mod\n",
            "uses_symbol.py": "from pkg import VALUE\n",
        },
    )

    assert python_import_neighbors(tmp_path, "uses_module.py").resolved == ("pkg/mod.py",)
    assert python_import_neighbors(tmp_path, "uses_symbol.py").resolved == ("pkg/__init__.py",)


# --------------------------------------------------------------------------
# Python — relative imports
# --------------------------------------------------------------------------


def test_python_relative_imports_resolve_against_the_importing_package(tmp_path: Path) -> None:
    """One dot resolves inside pkg, two dots climb to the root."""
    _write_tree(
        tmp_path,
        {
            "a.py": "z = 1\n",
            "pkg/__init__.py": "",
            "pkg/mod.py": "VALUE = 1\n",
            "pkg/rel_pkg.py": "from . import mod\n",
            "pkg/rel_mod.py": "from .mod import VALUE\n",
            "pkg/rel_parent.py": "from ..a import z\n",
        },
    )

    assert python_import_neighbors(tmp_path, "pkg/rel_pkg.py").resolved == ("pkg/mod.py",)
    assert python_import_neighbors(tmp_path, "pkg/rel_mod.py").resolved == ("pkg/mod.py",)
    assert python_import_neighbors(tmp_path, "pkg/rel_parent.py").resolved == ("a.py",)


def test_python_relative_import_above_root_lands_in_external_with_its_dots(tmp_path: Path) -> None:
    """A specifier that climbs out of the scanned root keeps its leading dots."""
    _write_tree(tmp_path, {"pkg/__init__.py": "", "pkg/rel.py": "from ... import x\n"})

    neighbors = python_import_neighbors(tmp_path, "pkg/rel.py")

    assert neighbors.resolved == ()
    assert neighbors.external == ("...x",)


# --------------------------------------------------------------------------
# Python — termination, rendering, hygiene
# --------------------------------------------------------------------------


def test_python_two_file_cycle_terminates_and_lists_each_other(tmp_path: Path) -> None:
    """Both calls return, and each file names the other — the termination proof."""
    _write_tree(tmp_path, {"c1.py": "import c2\n", "c2.py": "import c1\n"})

    assert python_import_neighbors(tmp_path, "c1.py").resolved == ("c2.py",)
    assert python_import_neighbors(tmp_path, "c2.py").resolved == ("c1.py",)


def test_python_unresolvable_specifiers_keep_the_source_spelling(tmp_path: Path) -> None:
    """External rendering is a contract choice: 'os' and 'typing.Iterable', pinned."""
    _write_tree(tmp_path, {"ext.py": "import os\nfrom typing import Iterable\n"})

    neighbors = python_import_neighbors(tmp_path, "ext.py")

    assert neighbors.resolved == ()
    assert neighbors.external == ("os", "typing.Iterable")


def test_python_unparseable_source_reports_parse_failed(tmp_path: Path) -> None:
    """A SyntaxError and a missing file both yield parse_failed with empty tuples."""
    _write_tree(tmp_path, {"broken.py": "def (\n"})

    broken = python_import_neighbors(tmp_path, "broken.py")
    missing = python_import_neighbors(tmp_path, "nope.py")

    assert broken.parse_failed is True
    assert broken.resolved == ()
    assert broken.external == ()
    assert missing.parse_failed is True


def test_python_file_importing_its_own_module_name_does_not_list_itself(tmp_path: Path) -> None:
    """The importing file is discarded from its own neighbor set."""
    _write_tree(tmp_path, {"self_ref.py": "import self_ref\n"})

    assert python_import_neighbors(tmp_path, "self_ref.py").resolved == ()


def test_python_duplicate_imports_collapse_and_resolved_comes_back_sorted(tmp_path: Path) -> None:
    """Imported reverse-alphabetically and twice; returned once each, sorted."""
    _write_tree(
        tmp_path,
        {
            "alpha.py": "",
            "zed.py": "",
            "dupes.py": "import zed\nimport alpha\nimport zed\n",
        },
    )

    assert python_import_neighbors(tmp_path, "dupes.py").resolved == ("alpha.py", "zed.py")


# --------------------------------------------------------------------------
# TypeScript / JavaScript
# --------------------------------------------------------------------------


def test_typescript_relative_specifiers_resolve_across_import_shapes(tmp_path: Path) -> None:
    """import-from, default-import of a directory, export-from, require and bare import."""
    _write_tree(
        tmp_path,
        {
            "x.ts": "",
            "dir/index.ts": "",
            "y.tsx": "",
            "comp.jsx": "",
            "side.js": "",
            "named.ts": "import {x} from './x';\n",
            "default_dir.ts": "import d from './dir';\n",
            "reexport.ts": "export {q} from './y';\n",
            "required.js": "const c = require('./comp');\n",
            "bare.ts": "import './side';\n",
        },
    )

    assert typescript_import_neighbors(tmp_path, "named.ts").resolved == ("x.ts",)
    assert typescript_import_neighbors(tmp_path, "default_dir.ts").resolved == ("dir/index.ts",)
    assert typescript_import_neighbors(tmp_path, "reexport.ts").resolved == ("y.tsx",)
    assert typescript_import_neighbors(tmp_path, "required.js").resolved == ("comp.jsx",)
    assert typescript_import_neighbors(tmp_path, "bare.ts").resolved == ("side.js",)


def test_typescript_non_relative_and_escaping_specifiers_go_external_verbatim(tmp_path: Path) -> None:
    """A package name and a specifier climbing above the root are both kept as written."""
    _write_tree(
        tmp_path,
        {
            "pkg_import.ts": "import React from 'react';\n",
            "escaping.ts": "import {e} from '../../escape';\n",
        },
    )

    package_neighbors = typescript_import_neighbors(tmp_path, "pkg_import.ts")
    escaping_neighbors = typescript_import_neighbors(tmp_path, "escaping.ts")

    assert package_neighbors.resolved == ()
    assert package_neighbors.external == ("react",)
    assert escaping_neighbors.resolved == ()
    assert escaping_neighbors.external == ("../../escape",)


def test_typescript_suffix_candidate_beats_index_file_candidate(tmp_path: Path) -> None:
    """Extension priority: with BOTH x.ts and x/index.ts present, './x' is x.ts."""
    _write_tree(
        tmp_path,
        {
            "x.ts": "",
            "x/index.ts": "",
            "importer.ts": "import {v} from './x';\n",
        },
    )

    assert typescript_import_neighbors(tmp_path, "importer.ts").resolved == ("x.ts",)


def test_typescript_missing_file_reports_parse_failed(tmp_path: Path) -> None:
    """An unreadable path yields parse_failed rather than an empty success."""
    assert typescript_import_neighbors(tmp_path, "nope.ts").parse_failed is True


# --------------------------------------------------------------------------
# Graph
# --------------------------------------------------------------------------


def _mixed_tree(tmp_path: Path) -> None:
    """A .py + .ts + .md tree — one file per suffix branch of the dispatcher."""
    _write_tree(
        tmp_path,
        {
            "helper.py": "",
            "app.py": "import helper\n",
            "sib.ts": "",
            "main.ts": "import {s} from './sib';\n",
            "notes.md": "# not code\n",
        },
    )


def test_graph_keys_are_deduplicated_inputs_in_sorted_order(tmp_path: Path) -> None:
    """Duplicated, unsorted input paths come back once each, sorted."""
    _mixed_tree(tmp_path)

    graph = build_import_neighbor_graph(tmp_path, ["notes.md", "main.ts", "app.py", "app.py"])

    assert list(graph) == ["app.py", "main.ts", "notes.md"]
    assert graph["app.py"].resolved == ("helper.py",)
    assert graph["main.ts"].resolved == ("sib.ts",)


def test_graph_is_deterministic_over_the_same_tree(tmp_path: Path) -> None:
    """Two builds over one tree are equal — the determinism claim, asserted."""
    _mixed_tree(tmp_path)
    paths = ["main.ts", "app.py", "notes.md"]

    assert build_import_neighbor_graph(tmp_path, paths) == build_import_neighbor_graph(tmp_path, paths)


def test_graph_unknown_suffix_is_reported_as_parse_failed(tmp_path: Path) -> None:
    """A .md file has no scanner, so the dispatcher marks it parse_failed."""
    _mixed_tree(tmp_path)

    graph = build_import_neighbor_graph(tmp_path, ["notes.md"])

    assert graph["notes.md"] == ImportNeighbors((), (), parse_failed=True)


# --------------------------------------------------------------------------
# Signatures — Python goldens (F107 T002)
# --------------------------------------------------------------------------


#: One fixture exercising, in a single file: a module docstring, a DECORATED
#: top-level def with annotated args and a return annotation, an async def, a
#: class with a base and a docstring, a method nested in that class, a
#: signature written across THREE source lines, a module-level assignment and
#: an import. What it pins is as much what is absent as what is present.
_PY_GOLDEN_SOURCE = '''"""Fixture module docstring."""

import os

MODULE_LEVEL_VALUE = 1


@some_decorator
def render_report(rows: list[str], limit: int = 10) -> str:
    """Render the report."""
    return ""


async def fetch_rows(url: str) -> list[str]:
    """Fetch the rows."""
    return []


class ReportBuilder(BaseBuilder):
    """Build one report."""

    def add_row(self, row: str) -> None:
        """Add a single row."""
        return None


def spread_across_three_lines(
    first: int,
    second: int,
) -> bool:
    return True
'''

#: The rendering of _PY_GOLDEN_SOURCE, captured from the extractor. It pins:
#: the decorator, the import and the assignment are all absent; the three-line
#: signature collapsed to one line; the nested method indented four spaces and
#: every docstring line four spaces deeper than its own header.
_PY_GOLDEN_LINES = (
    '"""Fixture module docstring."""',
    "def render_report(rows: list[str], limit: int=10) -> str:",
    '    """Render the report."""',
    "async def fetch_rows(url: str) -> list[str]:",
    '    """Fetch the rows."""',
    "class ReportBuilder(BaseBuilder):",
    '    """Build one report."""',
    "    def add_row(self, row: str) -> None:",
    '        """Add a single row."""',
    "def spread_across_three_lines(first: int, second: int) -> bool:",
)


def test_python_signature_golden_renders_headers_and_docstrings_only(tmp_path: Path) -> None:
    """The whole-file golden: exact tuple equality, nothing rewritten by hand."""
    _write_tree(tmp_path, {"golden.py": _PY_GOLDEN_SOURCE})

    signatures = python_file_signatures(tmp_path, "golden.py")

    assert signatures.lines == _PY_GOLDEN_LINES
    assert signatures.truncated is False
    assert signatures.parse_failed is False


def test_python_class_without_bases_renders_without_empty_parentheses(tmp_path: Path) -> None:
    """`class Bare:` — never `class Bare():`."""
    _write_tree(tmp_path, {"bare.py": "class Bare:\n    pass\n"})

    assert python_file_signatures(tmp_path, "bare.py").lines == ("class Bare:",)


def test_python_def_without_return_annotation_renders_without_arrow(tmp_path: Path) -> None:
    """No return annotation means no ` -> ` fragment at all."""
    _write_tree(tmp_path, {"plain.py": "def plain(value):\n    return value\n"})

    assert python_file_signatures(tmp_path, "plain.py").lines == ("def plain(value):",)


def test_python_docstring_with_blank_first_line_uses_its_first_non_empty_line(tmp_path: Path) -> None:
    """A docstring opening on a blank line contributes its first NON-EMPTY line."""
    source = 'def wrapped():\n    """\n    Summary sits on line two.\n    """\n'
    _write_tree(tmp_path, {"blank_first.py": source})

    assert python_file_signatures(tmp_path, "blank_first.py").lines == (
        "def wrapped():",
        '    """Summary sits on line two."""',
    )


def test_python_file_without_any_docstring_renders_headers_only(tmp_path: Path) -> None:
    """No module, class or function docstring anywhere: headers and nothing else."""
    source = "class Quiet:\n    def act(self):\n        return 1\n\n\ndef free():\n    return 2\n"
    _write_tree(tmp_path, {"quiet.py": source})

    assert python_file_signatures(tmp_path, "quiet.py").lines == (
        "class Quiet:",
        "    def act(self):",
        "def free():",
    )


def test_python_signatures_report_parse_failed_for_broken_and_missing_sources(tmp_path: Path) -> None:
    """A SyntaxError and a missing path both yield parse_failed with empty lines."""
    _write_tree(tmp_path, {"broken.py": "def (\n"})

    broken = python_file_signatures(tmp_path, "broken.py")
    missing = python_file_signatures(tmp_path, "nope.py")

    assert broken.parse_failed is True
    assert broken.lines == ()
    assert missing.parse_failed is True
    assert missing.lines == ()


def test_python_signatures_honor_the_line_cap_and_keep_the_first_lines(tmp_path: Path) -> None:
    """Over the cap: exactly `line_cap` lines, the FIRST ones, truncated=True."""
    source = "".join(f"def fn_{index}():\n    pass\n\n\n" for index in range(5))
    _write_tree(tmp_path, {"many.py": source})

    capped = python_file_signatures(tmp_path, "many.py", line_cap=3)
    generous = python_file_signatures(tmp_path, "many.py", line_cap=50)

    assert capped.lines == ("def fn_0():", "def fn_1():", "def fn_2():")
    assert capped.truncated is True
    assert len(generous.lines) == 5
    assert generous.truncated is False


# --------------------------------------------------------------------------
# Signatures — TypeScript / JavaScript goldens (F107 T002)
# --------------------------------------------------------------------------


#: One fixture exercising every export shape the T002 contract names, plus the
#: two shapes that must NOT be rendered: a non-exported declaration and a line
#: where the word `export` only appears mid-line.
_TS_GOLDEN_SOURCE = """import {dep} from "./dep";

export function renderWidget(id: string): void {
export default renderWidget;
export const WIDGET_NAME = "remedy";
export class WidgetView extends BaseView {
export interface WidgetShape {
export type WidgetId = string;
export async function loadWidget(): Promise<void> {
export * from "./widget_extras";
export {alpha, beta} from "./widget_pair";
  export const nestedWidgetFlag = 1;
function hiddenHelper() {
const localOnly = 1; // export const shadow = 2;
"""

#: The rendering of _TS_GOLDEN_SOURCE, captured from the extractor. It pins:
#: a trailing `{` is removed with the whitespace before it, a trailing
#: semicolon is KEPT, leading indentation is stripped, and neither the
#: non-exported line nor the mid-line `export` appears at all.
_TS_GOLDEN_LINES = (
    "export function renderWidget(id: string): void",
    "export default renderWidget;",
    'export const WIDGET_NAME = "remedy";',
    "export class WidgetView extends BaseView",
    "export interface WidgetShape",
    "export type WidgetId = string;",
    "export async function loadWidget(): Promise<void>",
    'export * from "./widget_extras";',
    'export {alpha, beta} from "./widget_pair";',
    "export const nestedWidgetFlag = 1;",
)


def test_typescript_signature_golden_renders_exported_lines_only(tmp_path: Path) -> None:
    """The whole-file golden: exact tuple equality across every export shape."""
    _write_tree(tmp_path, {"golden.ts": _TS_GOLDEN_SOURCE})

    signatures = typescript_file_signatures(tmp_path, "golden.ts")

    assert signatures.lines == _TS_GOLDEN_LINES
    assert signatures.truncated is False
    assert signatures.parse_failed is False


def test_typescript_signatures_report_parse_failed_for_a_missing_path(tmp_path: Path) -> None:
    """An unreadable path yields parse_failed rather than an empty success."""
    missing = typescript_file_signatures(tmp_path, "nope.ts")

    assert missing.parse_failed is True
    assert missing.lines == ()


def test_typescript_signatures_honor_the_line_cap_and_keep_the_first_lines(tmp_path: Path) -> None:
    """Same cap semantics as the Python extractor, asserted on its own fixture."""
    source = "".join(f"export const value_{index} = {index};\n" for index in range(5))
    _write_tree(tmp_path, {"many.ts": source})

    capped = typescript_file_signatures(tmp_path, "many.ts", line_cap=2)
    generous = typescript_file_signatures(tmp_path, "many.ts", line_cap=50)

    assert capped.lines == ("export const value_0 = 0;", "export const value_1 = 1;")
    assert capped.truncated is True
    assert len(generous.lines) == 5
    assert generous.truncated is False


# --------------------------------------------------------------------------
# Signatures — the inline size cap and the suffix dispatcher (F107 T002)
# --------------------------------------------------------------------------


def test_fits_inline_size_cap_is_inclusive_at_the_cap_and_false_when_absent(tmp_path: Path) -> None:
    """Five bytes on disk: fits under 6 and at 5, does not fit at 4."""
    _write_tree(tmp_path, {"sized.py": "abcde"})

    assert (tmp_path / "sized.py").stat().st_size == 5
    assert fits_inline_size_cap(tmp_path, "sized.py", cap_bytes=6) is True
    assert fits_inline_size_cap(tmp_path, "sized.py", cap_bytes=5) is True
    assert fits_inline_size_cap(tmp_path, "sized.py", cap_bytes=4) is False
    assert fits_inline_size_cap(tmp_path, "missing.py", cap_bytes=4096) is False


def test_signature_defaults_are_the_documented_values() -> None:
    """A silent change to either default is a red test, by design."""
    assert DEFAULT_INLINE_SIZE_CAP_BYTES == 16384
    assert DEFAULT_SIGNATURE_LINE_CAP == 200


def test_extract_file_signatures_dispatches_on_suffix(tmp_path: Path) -> None:
    """.py to the ast extractor, .ts/.jsx to the export scanner, .md to nothing."""
    _write_tree(
        tmp_path,
        {
            "golden.py": _PY_GOLDEN_SOURCE,
            "golden.ts": _TS_GOLDEN_SOURCE,
            "golden.jsx": _TS_GOLDEN_SOURCE,
            "notes.md": "# not code\n",
        },
    )

    assert extract_file_signatures(tmp_path, "golden.py") == python_file_signatures(
        tmp_path, "golden.py"
    )
    assert extract_file_signatures(tmp_path, "golden.ts") == typescript_file_signatures(
        tmp_path, "golden.ts"
    )
    assert extract_file_signatures(tmp_path, "golden.jsx") == typescript_file_signatures(
        tmp_path, "golden.jsx"
    )
    assert extract_file_signatures(tmp_path, "notes.md") == FileSignatures(parse_failed=True)
