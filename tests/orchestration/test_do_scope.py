"""Operator amendment amend1014-do-golden-path-now D6 — a planner may not invent scope for `remedy do`."""
from __future__ import annotations

from packages.orchestration.do_scope import (
    order_has_scope_fence,
    order_scope_files,
    order_scope_violations,
    resolve_order_path,
)

INCIDENT_ORDER = (
    "Add one concise project-description paragraph below the existing heading in README.md. "
    "Change no other files.")

TRACKED = ["README.md", "src/app.py", "tests/test_app.py"]


def test_improve_the_readme_may_not_grow_a_license_ci_or_an_env_file():
    produced = ("Add a LICENSE file\nAdd .github/workflows/ci.yml for CI\n"
                "Add .env.example\nExpand README.md with badges")
    assert order_scope_files("Improve the README", TRACKED) == ["README.md"]
    assert order_scope_violations("Improve the README", produced, TRACKED) == [
        "LICENSE", ".github/workflows/ci.yml", ".env.example"]


def test_a_fence_makes_every_other_file_a_violation_even_a_tracked_one():
    order = "Fix the typo in the intro. Change no other files."
    assert order_has_scope_fence(order)
    assert order_scope_violations(order, "Edit src/app.py", TRACKED) == ["src/app.py"]


def test_a_broad_order_leaves_the_planner_free_to_find_its_files():
    assert order_scope_violations("Refactor the parser", "Split src/app.py", TRACKED) == []


def test_the_incident_order_keeps_only_its_own_file():
    assert order_scope_violations(INCIDENT_ORDER, "Insert a paragraph into README.md",
                                  ["README.md"]) == []
    assert order_scope_violations(INCIDENT_ORDER, "Insert it into README.md and add LICENSE",
                                  ["README.md"]) == ["LICENSE"]


# --- 2026-10-17 audit P0-3: a bare file name is never the same file as a nested one ---------------

BOTH_READMES = ["README.md", "docs/README.md", "src/app.py", "tests/test_app.py"]


def test_root_readme_and_docs_readme_are_two_files():
    order = "Change only README.md"
    assert order_scope_violations(order, "Edit docs/README.md", BOTH_READMES) == ["docs/README.md"]
    assert order_scope_violations(order, "Edit README.md", BOTH_READMES) == []
    assert order_scope_violations("Change only docs/README.md", "Edit README.md", BOTH_READMES) == [
        "README.md"]


def test_a_bare_name_resolves_only_to_one_tracked_file():
    tracked = ["docs/README.md", "src/app.py"]
    assert order_scope_violations("Improve the README", "Edit README.md", tracked) == []
    two = ["docs/README.md", "web/README.md"]
    assert resolve_order_path("README.md", two) is None
    assert resolve_order_path("README.md", ["README.md", *two]) == "README.md"
    assert resolve_order_path("README.md", tracked) == "docs/README.md"


def test_a_name_nothing_proves_is_not_equated_with_a_nested_path():
    assert order_scope_violations("Change only README.md", "Edit docs/README.md", []) == [
        "docs/README.md"]


def test_a_test_the_order_asks_for_is_in_scope_and_a_test_run_is_not_a_license():
    order = "Fix the bug in src/app.py and add a regression test."
    assert order_scope_violations(order, "Add tests/test_app.py", BOTH_READMES) == []
    assert order_scope_violations(order, "Add tests/test_app.py and LICENSE", BOTH_READMES) == [
        "LICENSE"]
    ran = "Fix the bug in src/app.py. Run the tests."
    assert order_scope_violations(ran, "Add tests/test_other.py", BOTH_READMES) == [
        "tests/test_other.py"]
