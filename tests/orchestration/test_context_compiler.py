"""Tests for the context compiler: import-neighbor graphs (F107 T001),
signature extraction (F107 T002), tiered selection (F107 T003) and the
prompt-segment layer (F107 T004 part 1).

Every fixture tree is built under pytest's ``tmp_path`` and that tmp_path is
passed as ``root`` — nothing here reads the checkout, so the code under test
sees only the files the test wrote.

The signature goldens below were captured MECHANICALLY from the extractors and
must never be edited to make a failing test pass: an intentional change to the
rendering updates them in its own reviewed diff, with the change declared.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from packages.orchestration.config import load_config
from packages.orchestration.context_compiler import (
    COMPILED_CONTEXT_SEGMENT_NAME,
    CONTEXT_SIZE_FILENAME,
    DEFAULT_CONTEXT_TOKEN_BUDGET,
    DEFAULT_INLINE_SIZE_CAP_BYTES,
    DEFAULT_SIGNATURE_LINE_CAP,
    OMISSION_REASON_BINARY,
    OMISSION_REASON_BUDGET,
    OMISSION_REASON_DISTANCE,
    OMISSION_REASON_SIZE,
    OMISSION_REASON_UNPARSEABLE,
    OMITTED_CONTEXT_FILENAME,
    ClassBudgetFit,
    ContextSizeComparison,
    FileSignatures,
    ImportNeighbors,
    OmissionRecord,
    build_import_neighbor_graph,
    compare_context_size,
    compile_task_context,
    export_context_size_comparison_json,
    export_omitted_context_json,
    extract_file_signatures,
    fit_task_context_to_class_cap,
    fits_inline_size_cap,
    python_file_signatures,
    python_import_neighbors,
    register_compiled_context_segment,
    render_compiled_context_text,
    typescript_file_signatures,
    typescript_import_neighbors,
    write_context_size_comparison_json,
    write_omitted_context_json,
)
from packages.orchestration.prompt_budget import TaskClassCapResolution
from packages.orchestration.prompt_segments import (
    PromptSegmentError,
    PromptSegmentRegistry,
    SegmentStabilityRank,
    compose_prompt_segments,
)
from packages.orchestration.token_economy import estimate_text_tokens

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


# --------------------------------------------------------------------------
# Selector — tiers, budget demotion, omissions (F107 T003)
# --------------------------------------------------------------------------


#: Padding that makes `lib_big.py` unmistakably the largest file in the
#: fixture. WHICH tier-2 file the budget demotes is only observable when two
#: of them differ in size, so the sizes are part of the contract, not decor.
_SELECTOR_PADDING = "".join(f'    value_{index} = "padding padding"\n' for index in range(40))

_SELECTOR_LIB_BIG = 'import deep\n\n\ndef big_one():\n    """Big one."""\n' + _SELECTOR_PADDING

#: The candidate listing a caller would have walked — every path in the tree.
_SELECTOR_REPO_PATHS = (
    "app.py",
    "deep.py",
    "lib_big.py",
    "lib_small.py",
    "unrelated.py",
)


def _selector_tree(root: Path) -> None:
    """One fenced file importing TWO tier-2 neighbors of very different size,
    one tier-3 dependency behind the big one, and one file nobody imports."""
    _write_tree(
        root,
        {
            "app.py": "import lib_big\nimport lib_small\n",
            "lib_big.py": _SELECTOR_LIB_BIG,
            "lib_small.py": 'def small_one():\n    """Small one."""\n    return 1\n',
            "deep.py": 'def deep_one():\n    """Deep one."""\n    return 2\n',
            "unrelated.py": "UNRELATED = 1\n",
        },
    )


def _full_tokens(root: Path, rel_path: str) -> int:
    """The estimate a "full" rendering must carry — computed, never copied."""
    return estimate_text_tokens((root / rel_path).read_text(encoding="utf-8"))


def _signature_tokens(root: Path, rel_path: str) -> int:
    """The estimate a "signatures" rendering must carry — computed, never copied."""
    return estimate_text_tokens("\n".join(extract_file_signatures(root, rel_path).lines))


def _tiering(compiled) -> tuple[tuple[str, int, str], ...]:
    """(path, tier, rendering) per included file, which is what the tier table
    actually promises — the token numbers are asserted separately."""
    return tuple((s.rel_path, s.tier, s.rendering) for s in compiled.included)


def test_selector_assigns_tiers_one_two_three_and_omits_the_unimported_file(tmp_path: Path) -> None:
    """The tier table itself: fenced full, neighbors full, distant signatures,
    and the file nobody imports omitted for distance rather than included."""
    _selector_tree(tmp_path)

    compiled = compile_task_context(tmp_path, ["app.py"], _SELECTOR_REPO_PATHS)

    assert _tiering(compiled) == (
        ("app.py", 1, "full"),
        ("lib_big.py", 2, "full"),
        ("lib_small.py", 2, "full"),
        ("deep.py", 3, "signatures"),
    )
    assert compiled.omissions == (OmissionRecord("unrelated.py", 4, "distance", "omitted"),)


def test_tier_two_file_over_the_inline_cap_renders_as_signatures_with_a_size_record(tmp_path: Path) -> None:
    """A small explicit cap keeps the fixture readable: only the big neighbor
    trips it, and the demotion is recorded rather than left silent."""
    _selector_tree(tmp_path)

    compiled = compile_task_context(
        tmp_path, ["app.py"], _SELECTOR_REPO_PATHS, inline_cap_bytes=200
    )

    assert _tiering(compiled) == (
        ("app.py", 1, "full"),
        ("lib_big.py", 2, "signatures"),
        ("lib_small.py", 2, "full"),
        ("deep.py", 3, "signatures"),
    )
    assert OmissionRecord("lib_big.py", 2, "size", "signatures") in compiled.omissions


def test_budget_demotes_the_largest_tier_two_file_first(tmp_path: Path) -> None:
    """Phase A, with the ordering made observable: a budget one token under
    the unconstrained total demotes lib_big.py and leaves lib_small.py full."""
    _selector_tree(tmp_path)
    unconstrained = compile_task_context(tmp_path, ["app.py"], _SELECTOR_REPO_PATHS)

    compiled = compile_task_context(
        tmp_path,
        ["app.py"],
        _SELECTOR_REPO_PATHS,
        token_budget=unconstrained.estimated_tokens - 1,
    )

    assert _tiering(compiled) == (
        ("app.py", 1, "full"),
        ("lib_big.py", 2, "signatures"),
        ("lib_small.py", 2, "full"),
        ("deep.py", 3, "signatures"),
    )
    assert OmissionRecord("lib_big.py", 2, "budget", "signatures") in compiled.omissions
    assert compiled.over_budget is False


def test_budget_omits_tier_three_before_it_omits_tier_two(tmp_path: Path) -> None:
    """Phase B then phase C, asserted by WHICH files survive: one token under
    the all-signatures total drops only the distant file, while a budget equal
    to tier 1 alone drops both neighbors too and tier 1 still stands."""
    _selector_tree(tmp_path)
    all_signatures_total = (
        _full_tokens(tmp_path, "app.py")
        + _signature_tokens(tmp_path, "lib_big.py")
        + _signature_tokens(tmp_path, "lib_small.py")
        + _signature_tokens(tmp_path, "deep.py")
    )

    phase_b = compile_task_context(
        tmp_path, ["app.py"], _SELECTOR_REPO_PATHS, token_budget=all_signatures_total - 1
    )
    phase_c = compile_task_context(
        tmp_path,
        ["app.py"],
        _SELECTOR_REPO_PATHS,
        token_budget=_full_tokens(tmp_path, "app.py"),
    )

    assert _tiering(phase_b) == (
        ("app.py", 1, "full"),
        ("lib_big.py", 2, "signatures"),
        ("lib_small.py", 2, "signatures"),
    )
    assert OmissionRecord("deep.py", 3, "budget", "omitted") in phase_b.omissions
    assert _tiering(phase_c) == (("app.py", 1, "full"),)
    assert OmissionRecord("lib_big.py", 2, "budget", "omitted") in phase_c.omissions
    assert OmissionRecord("lib_small.py", 2, "budget", "omitted") in phase_c.omissions
    assert phase_c.over_budget is False


def test_tier_one_is_never_cut_by_the_budget_and_the_overflow_is_reported(tmp_path: Path) -> None:
    """The declared write scope survives a budget of 1; the overflow is
    reported honestly instead of being hidden by a truncated fenced file."""
    _selector_tree(tmp_path)

    compiled = compile_task_context(
        tmp_path, ["app.py"], _SELECTOR_REPO_PATHS, token_budget=1
    )

    assert _tiering(compiled) == (("app.py", 1, "full"),)
    assert compiled.budget_tokens == 1
    assert compiled.over_budget is True


def test_an_oversized_context_fits_under_its_class_cap_with_the_demotion_recorded(
    monkeypatch, tmp_path: Path
) -> None:
    """The cap comes from the resolver (T001); everything past that is the
    existing compiler unchanged — a cap one token under the unconstrained
    total still forces the same tier-2 demotion phase A already proves, and
    ``fits`` reports the result as fitting."""
    _selector_tree(tmp_path)
    unconstrained = compile_task_context(tmp_path, ["app.py"], _SELECTOR_REPO_PATHS)
    cap = unconstrained.estimated_tokens - 1
    monkeypatch.setattr(
        "packages.orchestration.context_compiler.resolve_task_class_cap",
        lambda task_class: TaskClassCapResolution(
            task_class=task_class,
            cap_tokens=cap,
            source="configured_class",
            estimate_basis="class_default",
        ),
    )

    result = fit_task_context_to_class_cap(
        tmp_path, ["app.py"], _SELECTOR_REPO_PATHS, "format"
    )

    assert result.fits is True
    assert result.cap_tokens == cap
    assert result.cap_source == "configured_class"
    assert result.tier1_tokens == _full_tokens(tmp_path, "app.py")
    assert (
        OmissionRecord("lib_big.py", 2, "budget", "signatures")
        in result.compiled.omissions
    )


def test_an_unfittable_context_reports_cannot_fit_with_the_tier1_arithmetic(
    monkeypatch, tmp_path: Path
) -> None:
    """Tier 1 alone still exceeds a cap of 1: ``fits`` is False and
    ``tier1_tokens`` carries the exact arithmetic a task-split decision
    needs (T003), equal to the compiled context's own total in this case."""
    _selector_tree(tmp_path)
    monkeypatch.setattr(
        "packages.orchestration.context_compiler.resolve_task_class_cap",
        lambda task_class: TaskClassCapResolution(
            task_class=task_class,
            cap_tokens=1,
            source="configured_class",
            estimate_basis="class_default",
        ),
    )

    result = fit_task_context_to_class_cap(
        tmp_path, ["app.py"], _SELECTOR_REPO_PATHS, "format"
    )

    assert result.fits is False
    assert result.cap_tokens == 1
    assert result.tier1_tokens == _full_tokens(tmp_path, "app.py")
    assert result.tier1_tokens == result.compiled.estimated_tokens
    assert result.compiled.over_budget is True


def test_a_class_outside_the_shared_vocabulary_is_refused(tmp_path: Path) -> None:
    """No mock here: the real resolver's vocabulary check (T001) refuses the
    class before any file under root is even read."""
    _selector_tree(tmp_path)

    with pytest.raises(ValueError, match="shared vocabulary"):
        fit_task_context_to_class_cap(
            tmp_path, ["app.py"], _SELECTOR_REPO_PATHS, "not_a_real_class"
        )


def test_the_cap_comes_from_the_real_resolver_when_config_sets_one(
    monkeypatch, tmp_path: Path
) -> None:
    """No mock of resolve_task_class_cap here either: a real config
    default_cap reaches the compiler exactly the way T001 designed it to."""
    _selector_tree(tmp_path)
    default_cap = _full_tokens(tmp_path, "app.py")
    config_dir = tmp_path / "_config"
    config_dir.mkdir()
    toml_file = config_dir / "remedy.toml"
    toml_file.write_text(
        f"[remedy.prompt_budget]\ndefault_cap = {default_cap}\n", encoding="utf-8"
    )
    loaded = load_config(
        project_path=toml_file, user_path=Path("/nonexistent/user.toml")
    )
    monkeypatch.setattr("packages.orchestration.config.get_config", lambda: loaded)

    result = fit_task_context_to_class_cap(
        tmp_path, ["app.py"], _SELECTOR_REPO_PATHS, "format"
    )

    assert result.cap_tokens == default_cap
    assert result.cap_source == "configured_default"
    assert result.fits is True


def test_a_binary_tier_two_file_is_omitted_entirely(tmp_path: Path) -> None:
    """Bytes that are not valid UTF-8 cannot be inlined at all, so the file is
    dropped with reason "binary" rather than rendered as anything."""
    _write_tree(tmp_path, {"app.py": "import blob\n"})
    (tmp_path / "blob.py").write_bytes(b"\xff\xfe\x00\x01 not utf-8\n")

    compiled = compile_task_context(tmp_path, ["app.py"], ["app.py", "blob.py"])

    assert _tiering(compiled) == (("app.py", 1, "full"),)
    assert compiled.omissions == (OmissionRecord("blob.py", 2, "binary", "omitted"),)


def test_an_unparseable_tier_three_file_is_carried_empty_with_an_unparseable_record(
    tmp_path: Path,
) -> None:
    """The Edge-cases clause "signature-skipped WITH REASON otherwise": the
    file decodes fine, so it is not binary, but nothing parses it — it stays in
    the context with an EMPTY signature rendering and the record says why."""
    _write_tree(
        tmp_path,
        {
            "app.py": "import lib\n",
            "lib.py": "import broken\n",
            "broken.py": "def broken(:\n    return 1\n",
        },
    )

    compiled = compile_task_context(
        tmp_path, ["app.py"], ["app.py", "lib.py", "broken.py"]
    )

    assert ("broken.py", 3, "signatures") in _tiering(compiled)
    assert extract_file_signatures(tmp_path, "broken.py").parse_failed is True
    assert "\n".join(extract_file_signatures(tmp_path, "broken.py").lines) == ""
    assert [r for r in compiled.omissions if r.rel_path == "broken.py"] == [
        OmissionRecord("broken.py", 3, "unparseable", "signatures")
    ]


def test_a_tier_two_file_over_the_cap_and_unparseable_carries_both_records(
    tmp_path: Path,
) -> None:
    """Two independent facts about one file, so two records: the size cap
    demoted it, and the demotion bought nothing because it does not parse."""
    _write_tree(
        tmp_path,
        {
            "app.py": "import bigbroken\n",
            "bigbroken.py": "def bigbroken(:\n" + "# padding for the size cap\n" * 20,
        },
    )

    compiled = compile_task_context(
        tmp_path, ["app.py"], ["app.py", "bigbroken.py"], inline_cap_bytes=200
    )

    assert ("bigbroken.py", 2, "signatures") in _tiering(compiled)
    assert sorted(
        (r.tier, r.reason, r.outcome)
        for r in compiled.omissions
        if r.rel_path == "bigbroken.py"
    ) == [(2, "size", "signatures"), (2, "unparseable", "signatures")]
    assert compiled.omissions == tuple(
        r for r in compiled.omissions if r.rel_path == "bigbroken.py"
    )


def test_an_unparseable_tier_one_file_is_included_whole_with_no_record(
    tmp_path: Path,
) -> None:
    """Tier 1 is "better safe": the declared write scope is carried in FULL
    whether or not an extractor can read it, so there is nothing to record."""
    _write_tree(tmp_path, {"broken.py": "def broken(:\n    return 1\n"})

    compiled = compile_task_context(tmp_path, ["broken.py"], ["broken.py"])

    assert _tiering(compiled) == (("broken.py", 1, "full"),)
    assert compiled.omissions == ()


def test_a_budget_demoted_tier_two_file_that_cannot_be_parsed_carries_both_records(
    tmp_path: Path,
) -> None:
    """Phase A's own blind spot: the budget demoted the file AND nothing can
    parse it, so the budget record alone would blame the budget for a blank the
    budget did not cause — an infinite budget renders it just as empty."""
    _write_tree(
        tmp_path,
        {
            "app.py": "import broken\n" + "PADDING = 'padding line'\n" * 40,
            "broken.py": "def broken(:\n    return 1\n",
        },
    )
    unconstrained = compile_task_context(tmp_path, ["app.py"], ["app.py", "broken.py"])

    compiled = compile_task_context(
        tmp_path,
        ["app.py"],
        ["app.py", "broken.py"],
        token_budget=unconstrained.estimated_tokens - 1,
    )

    assert ("broken.py", 2, "signatures") in _tiering(compiled)
    assert sorted(
        (r.reason, r.outcome) for r in compiled.omissions if r.rel_path == "broken.py"
    ) == [("budget", "signatures"), ("unparseable", "signatures")]


def test_a_fenced_path_with_no_file_under_root_is_not_a_candidate_at_all(tmp_path: Path) -> None:
    """It is neither included nor omitted: nothing that does not exist can be."""
    _write_tree(tmp_path, {"app.py": "VALUE = 1\n"})

    compiled = compile_task_context(tmp_path, ["app.py", "ghost.py"], ["app.py"])

    assert _tiering(compiled) == (("app.py", 1, "full"),)
    assert compiled.omissions == ()


def test_compilation_is_deterministic_across_input_orderings(tmp_path: Path) -> None:
    """Same inputs, both iterables reversed: the compiled contexts are equal."""
    _selector_tree(tmp_path)
    fenced = ("app.py", "unrelated.py")

    first = compile_task_context(tmp_path, fenced, _SELECTOR_REPO_PATHS)
    second = compile_task_context(
        tmp_path, tuple(reversed(fenced)), tuple(reversed(_SELECTOR_REPO_PATHS))
    )

    assert first == second


def test_estimated_tokens_come_from_the_estimator_over_the_rendered_text(tmp_path: Path) -> None:
    """Each estimate is asserted against a direct `estimate_text_tokens` call
    on the text that rendering sends, and the total is their sum."""
    _selector_tree(tmp_path)

    compiled = compile_task_context(tmp_path, ["app.py"], _SELECTOR_REPO_PATHS)

    expected = {
        "app.py": _full_tokens(tmp_path, "app.py"),
        "lib_big.py": _full_tokens(tmp_path, "lib_big.py"),
        "lib_small.py": _full_tokens(tmp_path, "lib_small.py"),
        "deep.py": _signature_tokens(tmp_path, "deep.py"),
    }
    assert {s.rel_path: s.estimated_tokens for s in compiled.included} == expected
    assert compiled.estimated_tokens == sum(expected.values())
    assert compiled.budget_tokens == DEFAULT_CONTEXT_TOKEN_BUDGET


def test_export_omitted_context_json_carries_exactly_four_keys_in_record_order(tmp_path: Path) -> None:
    """The exported shape is the debugging view's contract: path, tier, reason
    and outcome, one dict per record, in `compiled.omissions` order."""
    _selector_tree(tmp_path)
    compiled = compile_task_context(
        tmp_path, ["app.py"], _SELECTOR_REPO_PATHS, inline_cap_bytes=200
    )

    exported = export_omitted_context_json(compiled)

    assert [entry["path"] for entry in exported] == [r.rel_path for r in compiled.omissions]
    assert len(exported) == 2
    for entry, record in zip(exported, compiled.omissions):
        assert set(entry) == {"path", "tier", "reason", "outcome"}
        assert entry["tier"] == record.tier
        assert entry["reason"] == record.reason
        assert entry["outcome"] == record.outcome


def test_write_omitted_context_json_creates_its_parent_and_round_trips(tmp_path: Path) -> None:
    """One of the two writing functions: it creates the directory, returns the path it
    wrote, and what lands on disk reads back equal to the exported list."""
    _selector_tree(tmp_path)
    compiled = compile_task_context(
        tmp_path, ["app.py"], _SELECTOR_REPO_PATHS, inline_cap_bytes=200
    )
    target = tmp_path / "evidence" / "nested" / "omitted_context.json"

    written = write_omitted_context_json(compiled, target)

    assert written == target
    assert target.is_file()
    written_text = target.read_text(encoding="utf-8")
    assert json.loads(written_text) == export_omitted_context_json(compiled)
    assert written_text.endswith("\n")


def test_selector_defaults_and_reason_vocabulary_are_the_documented_values() -> None:
    """A silent change to the budget or to any reason word is a red test."""
    assert DEFAULT_CONTEXT_TOKEN_BUDGET == 24000
    assert OMISSION_REASON_BUDGET == "budget"
    assert OMISSION_REASON_DISTANCE == "distance"
    assert OMISSION_REASON_BINARY == "binary"
    assert OMISSION_REASON_SIZE == "size"
    assert OMISSION_REASON_UNPARSEABLE == "unparseable"


def test_every_candidate_path_is_accounted_for_exactly_once(tmp_path: Path) -> None:
    """The feature's own Acceptance wording, on a tree where nothing is
    demoted — so no path can carry both an included entry and a record, and a
    path that silently vanished would show up as a shorter list."""
    _selector_tree(tmp_path)

    compiled = compile_task_context(tmp_path, ["app.py"], _SELECTOR_REPO_PATHS)

    accounted = sorted(
        [s.rel_path for s in compiled.included] + [r.rel_path for r in compiled.omissions]
    )
    assert accounted == sorted(_SELECTOR_REPO_PATHS)


# --------------------------------------------------------------------------
# Segments — rendering, registration, size comparison (F107 T004 part 1)
# --------------------------------------------------------------------------


def _selector_compiled(root: Path, **kwargs):
    """The fixture tree compiled the way every segment test below needs it."""
    _selector_tree(root)
    return compile_task_context(root, ["app.py"], _SELECTOR_REPO_PATHS, **kwargs)


def test_render_compiled_context_text_builds_one_block_per_included_file(tmp_path: Path) -> None:
    """The expected text is BUILT here from the fixture's own file texts and
    from the extractor's own lines — never pasted — so the assertion measures
    the rendering rather than a snapshot someone could have refreshed."""
    compiled = _selector_compiled(tmp_path)
    app_text = (tmp_path / "app.py").read_text(encoding="utf-8").rstrip("\n")
    big_text = (tmp_path / "lib_big.py").read_text(encoding="utf-8").rstrip("\n")
    small_text = (tmp_path / "lib_small.py").read_text(encoding="utf-8").rstrip("\n")
    deep_lines = "\n".join(extract_file_signatures(tmp_path, "deep.py").lines)

    rendered = render_compiled_context_text(tmp_path, compiled)

    assert rendered == "\n\n".join(
        (
            "# app.py — tier 1 (full)\n" + app_text,
            "# lib_big.py — tier 2 (full)\n" + big_text,
            "# lib_small.py — tier 2 (full)\n" + small_text,
            "# deep.py — tier 3 (signatures)\n" + deep_lines,
        )
    )
    # The blocks follow `compiled.included`, and every header reads exactly
    # "# <path> — tier <n> (<rendering>)" — asserted by position, because a
    # file body may itself contain blank lines.
    headers = [
        "# app.py — tier 1 (full)",
        "# lib_big.py — tier 2 (full)",
        "# lib_small.py — tier 2 (full)",
        "# deep.py — tier 3 (signatures)",
    ]
    assert [s.rel_path for s in compiled.included] == [
        "app.py",
        "lib_big.py",
        "lib_small.py",
        "deep.py",
    ]
    rendered_lines = rendered.split("\n")
    for header in headers:
        assert rendered_lines.count(header) == 1
    positions = [rendered_lines.index(header) for header in headers]
    assert positions == sorted(positions)


def test_an_omitted_file_contributes_neither_its_path_nor_its_content(tmp_path: Path) -> None:
    """The separation the debugging view rests on: what was left out lives in
    the omissions record, and nothing of it leaks into the segment text."""
    compiled = _selector_compiled(tmp_path)

    rendered = render_compiled_context_text(tmp_path, compiled)

    assert "unrelated.py" not in rendered
    assert "UNRELATED = 1" not in rendered
    assert "import lib_big" in rendered


def test_register_compiled_context_segment_names_and_ranks_the_segment(tmp_path: Path) -> None:
    """JOB_CONTEXT is pinned here: a silent move to another rank is red."""
    compiled = _selector_compiled(tmp_path)
    registry = PromptSegmentRegistry()

    segment = register_compiled_context_segment(registry, tmp_path, compiled)

    assert segment.name == COMPILED_CONTEXT_SEGMENT_NAME
    assert segment.rank == SegmentStabilityRank.JOB_CONTEXT
    assert segment.text == render_compiled_context_text(tmp_path, compiled)
    assert registry.registered_segments() == (segment,)


def test_the_registered_segment_composes_into_a_one_row_manifest(tmp_path: Path) -> None:
    """Composition stays the registry's job: the compiled context arrives as
    one auditable manifest row whose digest is recomputed here, not trusted."""
    compiled = _selector_compiled(tmp_path)
    registry = PromptSegmentRegistry()
    segment = register_compiled_context_segment(registry, tmp_path, compiled)

    composed = compose_prompt_segments(registry.registered_segments())

    assert len(composed.manifest) == 1
    entry = composed.manifest[0]
    assert entry.name == COMPILED_CONTEXT_SEGMENT_NAME
    assert entry.rank == int(SegmentStabilityRank.JOB_CONTEXT)
    assert entry.sha256 == hashlib.sha256(segment.text.encode("utf-8")).hexdigest()
    assert composed.text == segment.text


def test_registering_the_compiled_context_twice_raises_the_registry_error(tmp_path: Path) -> None:
    """The duplicate rule is INHERITED from the registry, not re-implemented
    here and not prevented in advance."""
    compiled = _selector_compiled(tmp_path)
    registry = PromptSegmentRegistry()
    register_compiled_context_segment(registry, tmp_path, compiled)

    with pytest.raises(PromptSegmentError):
        register_compiled_context_segment(registry, tmp_path, compiled)


def test_rendering_the_same_tree_twice_produces_the_same_text(tmp_path: Path) -> None:
    """The rendering inherits the selector's determinism instead of adding an
    ordering of its own, so the same tree always gives the same bytes."""
    _selector_tree(tmp_path)
    first = compile_task_context(tmp_path, ["app.py"], _SELECTOR_REPO_PATHS)
    second = compile_task_context(tmp_path, ["app.py"], _SELECTOR_REPO_PATHS)

    assert render_compiled_context_text(tmp_path, first) == render_compiled_context_text(
        tmp_path, second
    )


def test_the_omissions_filename_constant_is_what_the_writer_writes(tmp_path: Path) -> None:
    """One spelling of the omissions filename, used by the writer and by every
    caller that will later look for it — the constant IS the contract."""
    compiled = _selector_compiled(tmp_path, inline_cap_bytes=200)
    target = tmp_path / "task_runs" / "t1" / OMITTED_CONTEXT_FILENAME

    written = write_omitted_context_json(compiled, target)

    assert OMITTED_CONTEXT_FILENAME == "omitted_context.json"
    assert written == target
    assert json.loads(target.read_text(encoding="utf-8")) == export_omitted_context_json(
        compiled
    )


def test_compare_context_size_reports_the_saving_against_whole_files(tmp_path: Path) -> None:
    """The feature's Done condition, measured: the baseline is summed here over
    the five fixture files, and the saving must actually be positive."""
    compiled = _selector_compiled(tmp_path)
    expected_whole = sum(_full_tokens(tmp_path, path) for path in _SELECTOR_REPO_PATHS)

    comparison = compare_context_size(tmp_path, _SELECTOR_REPO_PATHS, compiled)

    assert comparison.whole_file_tokens == expected_whole
    assert comparison.compiled_tokens == compiled.estimated_tokens
    assert comparison.saved_tokens == expected_whole - compiled.estimated_tokens
    assert comparison.saved_ratio == comparison.saved_tokens / expected_whole
    assert comparison.saved_tokens > 0


def test_compare_context_size_reports_no_ratio_for_a_zero_baseline(tmp_path: Path) -> None:
    """A zero baseline has no ratio: 0.0 exactly, never a fabricated number and
    never a ZeroDivisionError. The saving itself is reported as it falls."""
    compiled = _selector_compiled(tmp_path)

    comparison = compare_context_size(tmp_path, (), compiled)

    assert comparison.whole_file_tokens == 0
    assert comparison.saved_ratio == 0.0
    assert comparison.saved_tokens == -compiled.estimated_tokens


def test_compare_context_size_charges_nothing_for_missing_or_binary_paths(tmp_path: Path) -> None:
    """A path with no file and a file whose bytes are not UTF-8 each contribute
    0 instead of raising: what could not be inlined either way costs nothing
    either way, so the junk run equals the clean one exactly."""
    compiled = _selector_compiled(tmp_path)
    (tmp_path / "blob.bin").write_bytes(b"\xff\xfe\x00\x01 not utf-8\n")

    clean = compare_context_size(tmp_path, _SELECTOR_REPO_PATHS, compiled)
    with_junk = compare_context_size(
        tmp_path, _SELECTOR_REPO_PATHS + ("ghost.py", "blob.bin"), compiled
    )

    assert with_junk == clean
    assert with_junk.whole_file_tokens == clean.whole_file_tokens


# --------------------------------------------------------------------------
# The rendered cap (F107 R-0273) — the rendering matches the compiled cap
# --------------------------------------------------------------------------


#: A cap far below what the fixture's tier-3 file declares, so a rendering at
#: the module default is unmistakably longer than a rendering at this cap.
_CAPPED_LINE_CAP = 2

#: Six top-level functions, each with a docstring: twelve signature lines
#: against a cap of two, so the cap cannot pass unnoticed.
_CAPPED_DEEP = "".join(
    f'def deep_{index}():\n    """Deep {index}."""\n    return {index}\n\n\n' for index in range(6)
)

_CAPPED_REPO_PATHS = ("app.py", "deep.py", "lib.py")


def _capped_tree(root: Path) -> None:
    """One fenced file, one tier-2 neighbor, and a tier-3 file behind it that
    declares far more than the cap the tests below compile at."""
    _write_tree(
        root,
        {
            "app.py": "import lib\n",
            "lib.py": 'import deep\n\n\ndef lib_one():\n    """Lib one."""\n    return 1\n',
            "deep.py": _CAPPED_DEEP,
        },
    )


def _rendered_bodies(rendered: str, compiled) -> dict[str, str]:
    """Split the rendered text back into {rel_path: body} by walking the header
    lines in `compiled.included` order — never by splitting on blank lines,
    because a file body may contain them. The body runs from the line after its
    header to the line before the blank separator that precedes the next one."""
    lines = rendered.split("\n")
    starts: list[int] = []
    cursor = 0
    for selected in compiled.included:
        header = f"# {selected.rel_path} — tier {selected.tier} ({selected.rendering})"
        cursor = lines.index(header, cursor)
        starts.append(cursor)
        cursor += 1
    bodies: dict[str, str] = {}
    for position, selected in enumerate(compiled.included):
        start = starts[position] + 1
        end = starts[position + 1] - 1 if position + 1 < len(starts) else len(lines)
        bodies[selected.rel_path] = "\n".join(lines[start:end])
    return bodies


def test_the_compiled_context_carries_the_line_cap_it_was_compiled_at(tmp_path: Path) -> None:
    """The cap travels ON the context: compiling without the argument records
    the module default, and an explicit cap records exactly that value."""
    _selector_tree(tmp_path)

    defaulted = compile_task_context(tmp_path, ["app.py"], _SELECTOR_REPO_PATHS)
    capped = compile_task_context(
        tmp_path, ["app.py"], _SELECTOR_REPO_PATHS, line_cap=_CAPPED_LINE_CAP
    )

    assert defaulted.line_cap == DEFAULT_SIGNATURE_LINE_CAP
    assert capped.line_cap == _CAPPED_LINE_CAP


def test_signature_blocks_render_at_the_cap_the_context_was_compiled_at(tmp_path: Path) -> None:
    """R-0273, both halves of the invariant: every signatures body in the
    rendered text is the CAPPED rendering, not the module-default one, and its
    estimate is the very number the budget was enforced against — so
    `estimated_tokens` and the text that would be sent describe the same bytes.
    Every expected value is computed here from the extractor and the estimator."""
    _capped_tree(tmp_path)

    compiled = compile_task_context(
        tmp_path, ["app.py"], _CAPPED_REPO_PATHS, line_cap=_CAPPED_LINE_CAP
    )
    rendered = render_compiled_context_text(tmp_path, compiled)
    bodies = _rendered_bodies(rendered, compiled)

    signature_files = [s for s in compiled.included if s.rendering == "signatures"]
    # A fixture that produced no signatures file would make the loop vacuous.
    assert signature_files
    for selected in signature_files:
        expected_body = "\n".join(
            extract_file_signatures(tmp_path, selected.rel_path, _CAPPED_LINE_CAP).lines
        )
        assert bodies[selected.rel_path] == expected_body
        assert estimate_text_tokens(expected_body) == selected.estimated_tokens
    # The cap is doing real work here: the default rendering is much longer.
    uncapped_lines = extract_file_signatures(tmp_path, "deep.py").lines
    assert len(uncapped_lines) > _CAPPED_LINE_CAP


def test_two_contexts_compiled_at_the_same_custom_cap_stay_equal(tmp_path: Path) -> None:
    """The new field does not cost determinism: same tree, same cap, equal
    contexts and byte-equal renderings."""
    _capped_tree(tmp_path)

    first = compile_task_context(
        tmp_path, ["app.py"], _CAPPED_REPO_PATHS, line_cap=_CAPPED_LINE_CAP
    )
    second = compile_task_context(
        tmp_path, ["app.py"], _CAPPED_REPO_PATHS, line_cap=_CAPPED_LINE_CAP
    )

    assert first == second
    assert first.line_cap == _CAPPED_LINE_CAP
    assert render_compiled_context_text(tmp_path, first) == render_compiled_context_text(
        tmp_path, second
    )


# --------------------------------------------------------------------------
# The size record (F107 T004 part 2b-i) — the comparison as an exported and
# written artifact, beside the omissions record it is the sibling of
# --------------------------------------------------------------------------


#: A comparison written out by hand, so every assertion below can name the four
#: figures LITERALLY instead of recomputing them with the code's own
#: expression. 900 - 250 = 650 and 650 / 900 is not a round number, which is
#: exactly why it is here: a silently rounded ratio would show.
_SIZE_FIXTURE = ContextSizeComparison(
    whole_file_tokens=900,
    compiled_tokens=250,
    saved_tokens=650,
    saved_ratio=650 / 900,
)


def test_export_context_size_comparison_json_carries_the_four_real_figures() -> None:
    """The exported record IS the four fields, spelled out: no extra key, no
    missing key, and each value the one the comparison carries."""
    exported = export_context_size_comparison_json(_SIZE_FIXTURE)

    assert exported == {
        "whole_file_tokens": 900,
        "compiled_tokens": 250,
        "saved_tokens": 650,
        "saved_ratio": 650 / 900,
    }
    assert list(exported) == [
        "whole_file_tokens",
        "compiled_tokens",
        "saved_tokens",
        "saved_ratio",
    ]
    assert isinstance(exported["saved_tokens"], int)
    assert isinstance(exported["saved_ratio"], float)


def test_a_negative_saving_survives_the_export_unclamped() -> None:
    """A selection that GREW the context has to show that. Clamping the number
    to zero would hide the one figure the comparison exists to expose."""
    grew = ContextSizeComparison(
        whole_file_tokens=40,
        compiled_tokens=100,
        saved_tokens=-60,
        saved_ratio=-1.5,
    )

    exported = export_context_size_comparison_json(grew)

    assert exported["saved_tokens"] == -60
    assert exported["saved_ratio"] == -1.5
    assert exported["whole_file_tokens"] == 40
    assert exported["compiled_tokens"] == 100


def test_a_zero_baseline_exports_a_ratio_of_exactly_zero(tmp_path: Path) -> None:
    """A zero baseline has no ratio. The export must carry the 0.0 the dataclass
    documents and never a ratio of its own invention."""
    compiled = _selector_compiled(tmp_path)

    exported = export_context_size_comparison_json(compare_context_size(tmp_path, (), compiled))

    assert exported["whole_file_tokens"] == 0
    assert exported["saved_ratio"] == 0.0
    assert exported["compiled_tokens"] == compiled.estimated_tokens
    assert exported["saved_tokens"] == -compiled.estimated_tokens
    assert exported["saved_tokens"] < 0


def test_write_context_size_comparison_json_creates_its_parent_and_round_trips(
    tmp_path: Path,
) -> None:
    """The second writing function: it creates the directory nobody made for it,
    and what lands on disk reads back as the same four figures."""
    target = tmp_path / "evidence" / "nested" / "context_size.json"
    assert not target.parent.exists()

    written = write_context_size_comparison_json(_SIZE_FIXTURE, target)

    assert written == target
    assert target.is_file()
    written_text = target.read_text(encoding="utf-8")
    assert json.loads(written_text) == {
        "whole_file_tokens": 900,
        "compiled_tokens": 250,
        "saved_tokens": 650,
        "saved_ratio": 650 / 900,
    }
    assert written_text.endswith("\n")
    assert written_text.startswith('{\n  "whole_file_tokens": 900,\n')


def test_the_size_record_filename_constant_is_what_the_writer_writes(tmp_path: Path) -> None:
    """One spelling of the size record's filename, used by the writer and by
    every caller that will later look for it — the constant IS the contract."""
    target = tmp_path / "task_runs" / "t1" / CONTEXT_SIZE_FILENAME

    written = write_context_size_comparison_json(_SIZE_FIXTURE, target)

    assert CONTEXT_SIZE_FILENAME == "context_size.json"
    assert written == target
    assert written.name == "context_size.json"
    assert json.loads(target.read_text(encoding="utf-8")) == export_context_size_comparison_json(
        _SIZE_FIXTURE
    )


def test_the_written_size_record_reports_the_fixture_repo_saving(tmp_path: Path) -> None:
    """The record over a REAL compiled context, not a hand-built dataclass: the
    five-file fixture tree, whose whole-file baseline is summed here rather than
    read back from the comparison."""
    compiled = _selector_compiled(tmp_path)
    expected_whole = sum(_full_tokens(tmp_path, path) for path in _SELECTOR_REPO_PATHS)
    comparison = compare_context_size(tmp_path, _SELECTOR_REPO_PATHS, compiled)
    target = tmp_path / "runs" / CONTEXT_SIZE_FILENAME

    write_context_size_comparison_json(comparison, target)

    record = json.loads(target.read_text(encoding="utf-8"))
    assert record["whole_file_tokens"] == expected_whole
    assert record["compiled_tokens"] == compiled.estimated_tokens
    assert record["saved_tokens"] == expected_whole - compiled.estimated_tokens
    assert record["saved_tokens"] > 0
    assert 0.0 < record["saved_ratio"] < 1.0
