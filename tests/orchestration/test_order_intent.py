"""exec-1018 (R-1348, R-1349, R-1350): what an order asks Remedy to do, and of each file it names.

Pure readings of the order's words, English and German, no model call. The lab orders of 2026-10-17
are read verbatim, so a new pattern that changed what they ask for goes red here first.
"""
from __future__ import annotations

import pytest

from packages.orchestration.order_intent import (
    FILE_ROLE_CONTEXT,
    FILE_ROLE_OPTIONAL,
    FILE_ROLE_PROTECTED,
    FILE_ROLE_REQUIRED,
    independent_parts,
    order_file_roles,
    order_intent,
)
from tests.orchestration.scale_matrix import LAB_ADD_ORDER, LAB_NORMALIZE_ORDER, LAB_README_ORDER

R, O, C, P = FILE_ROLE_REQUIRED, FILE_ROLE_OPTIONAL, FILE_ROLE_CONTEXT, FILE_ROLE_PROTECTED


@pytest.mark.parametrize(("order", "intent"), [
    ("Fix the typo in README.md.", "change"),
    ("Fix the typo in README.md. Change nothing else.", "change"),                  # a fence, not intent
    ("Fix the typo in README.md and change nothing elsewhere.", "change"),
    ("Korrigiere README.md. Verändere sonst nichts.", "change"),
    (LAB_README_ORDER, "change"), (LAB_NORMALIZE_ORDER, "change"), (LAB_ADD_ORDER, "change"),
    ("Only plan how to restructure README.md; do not change anything.", "plan_only"),
    ("Only plan, do not change anything: how would we split src/api/server.js?", "plan_only"),
    ("Erstelle nur einen Plan für src/app.py, ändere nichts.", "plan_only"),
    ("Only run the project tests and report the result; do not change any file.", "verify_only"),
    ("Führe nur die Projekttests aus und ändere nichts.", "verify_only"),
    ("Just run the tests.", "verify_only"),
    ("Do not change anything.", "no_work"),
], ids=["plain", "fence-else", "fence-elsewhere", "fence-sonst-de", "lab-readme", "lab-normalize", "lab-add",
        "plan-only", "plan-only-question", "plan-only-de", "verify-only", "verify-only-de", "just-run",
        "no-work"])
def test_the_order_s_intent(order, intent):
    assert order_intent(order) == intent


@pytest.mark.parametrize(("order", "roles"), [
    ("Fix the empty-name bug in src/format.js; the expected format is described in docs/FORMAT.md.",
     {"src/format.js": R, "docs/FORMAT.md": C}),
    ("Fix add() in src/calc.js. See src/format.js for how errors are reported.",
     {"src/calc.js": R, "src/format.js": C}),
    ("Behebe den Fehler in src/calc.js. Die Datei src/format.js nicht ändern.",
     {"src/calc.js": R, "src/format.js": P}),
    ("Fix add() in src/calc.js but do not touch src/format.js.", {"src/calc.js": R, "src/format.js": P}),
    ("Fix add() in src/calc.js and leave src/format.js unchanged.", {"src/calc.js": R, "src/format.js": P}),
    ("Fix add() in src/calc.js; you may also adjust src/format.js if needed.",
     {"src/calc.js": R, "src/format.js": O}),
    # A guard on PART of a file the order asks to change keeps the file required.
    ("Fix the bug in src/calc.js but do not change the API of src/calc.js.", {"src/calc.js": R}),
    ("Rename normalizeName to normalizePersonName in src/format.js and src/index.js.",
     {"src/format.js": R, "src/index.js": R}),
    (LAB_NORMALIZE_ORDER, {"src/format.js": R, "test/format.test.js": R}),
    (LAB_ADD_ORDER, {"src/calc.js": R, "test/calc.test.js": R}),
], ids=["described-in", "see", "protected-de", "do-not-touch", "leave-unchanged", "may-adjust", "api-guard",
        "rename-two", "lab-normalize", "lab-add"])
def test_each_named_file_s_role(order, roles):
    assert order_file_roles(order) == roles


@pytest.mark.parametrize(("order", "required", "parts"), [
    ("1. Fix the typo in README.md. 2. Add a --verbose flag to src/api/server.js. 3. Make src/format.js "
     "handle negative numbers.", ["README.md", "src/api/server.js", "src/format.js"],
     [["README.md"], ["src/api/server.js"], ["src/format.js"]]),
    # A rename and its callers in one sentence: one change.
    ("Rename the function fmt to formatValue in src/format.js and update its callers in src/calc.js and "
     "src/api/routes.js.", ["src/format.js", "src/calc.js", "src/api/routes.js"],
     [["src/format.js", "src/calc.js", "src/api/routes.js"]]),
    # Two sentences sharing an identifier are one change too, however they are laid out.
    ("Add a helper clamp(x) to src/math.js. Use clamp( in src/price.js.", ["src/math.js", "src/price.js"],
     [["src/math.js", "src/price.js"]]),
    ("Add a helper to src/math.js.\n- Then use it in src/price.js.", ["src/math.js", "src/price.js"],
     [["src/math.js", "src/price.js"]]),                                          # "it" refers back
    ("Füge in src/math.js eine Funktion hinzu. Verwende sie in src/price.js.", ["src/math.js", "src/price.js"],
     [["src/math.js", "src/price.js"]]),                                          # "sie" refers back
], ids=["three-independent", "rename-and-callers", "shared-identifier", "back-reference-it", "back-reference-sie-de"])
def test_independent_parts_are_told_apart_from_one_change_by_references_not_layout(order, required, parts):
    assert independent_parts(order, required) == parts
