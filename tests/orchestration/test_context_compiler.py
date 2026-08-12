"""Tests for the context compiler's import-neighbor graph layer (F107 T001).

Every fixture tree is built under pytest's ``tmp_path`` and that tmp_path is
passed as ``root`` — nothing here reads the checkout, so the graph under test
sees only the files the test wrote.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from packages.orchestration.context_compiler import (
    ImportNeighbors,
    build_import_neighbor_graph,
    python_import_neighbors,
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
