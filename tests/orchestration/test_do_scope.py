"""Operator amendment amend1014-do-golden-path-now D6 — a planner may not invent scope for `remedy do`."""
from __future__ import annotations

from packages.orchestration.do_scope import (
    order_has_scope_fence,
    order_scope_files,
    order_scope_violations,
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
