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


# exec-1018b (R-1358): adversarial wordings of the order's P1 4, English and German.
M = "mentioned"


@pytest.mark.parametrize(("order", "roles"), [
    ("Fix add() in src/calc.js without touching src/format.js.", {"src/calc.js": R, "src/format.js": P}),
    ("Repariere add() in src/calc.js, ohne src/format.js anzufassen.", {"src/calc.js": R, "src/format.js": P}),
    ("Fix add() in src/calc.js. src/format.js is off limits.", {"src/calc.js": R, "src/format.js": P}),
    ("Repariere add() in src/calc.js. Finger weg von src/format.js.", {"src/calc.js": R, "src/format.js": P}),
    ("Read docs/FORMAT.md first, then fix the empty-name bug in src/format.js.",
     {"docs/FORMAT.md": C, "src/format.js": R}),
    ("Lies zuerst docs/FORMAT.md und behebe dann den Fehler in src/format.js.",
     {"docs/FORMAT.md": C, "src/format.js": R}),
    ("Fix add() in src/calc.js; adjusting src/format.js is fine if it helps.", {"src/calc.js": R, "src/format.js": O}),
    # A guard no pattern knows, told by its negation: never an instruction to change the file.
    ("Fix add() in src/calc.js. Under no circumstances modify config/prod.json.",
     {"src/calc.js": R, "config/prod.json": M}),
    # An unknown verb without a negation keeps its file required: no part of the order is dropped.
    ("Lass src/price.js kaufmännisch runden.", {"src/price.js": R}),
    ("Add a GET /health endpoint in src/api/routes.py, register it in src/api/app.py.",
     {"src/api/routes.py": R, "src/api/app.py": R}),
], ids=["without-touching", "ohne-anzufassen", "off-limits", "finger-weg", "read-first", "lies-zuerst",
        "fine-if", "negated-unknown-guard", "unknown-verb-de", "register"])
def test_an_adversarial_wording_reads_each_files_role(order, roles):
    assert order_file_roles(order) == roles


@pytest.mark.parametrize(("order", "intent"), [
    ("Führe nur die Tests aus und sag mir das Ergebnis, ohne etwas zu ändern.", "verify_only"),
    ("Schlag vor, wie wir src/auth.ts von md5 auf argon2 umstellen; noch nichts umsetzen.", "plan_only"),
    ("Document the add() function in docs/API.md. Do not change any code.", "change"),
    ("Dokumentiere die Funktion add() in docs/API.md. Am Code nichts ändern.", "change"),
    ("Explain what src/cache.ts does. No changes please.", "no_work"),
    # A fence on the apply is no "change nothing": the lab's own sentence.
    ("Ergänze README.md um einen Abschnitt. Übernimm keine Änderungen automatisch.", "change"),
], ids=["verify-only-de", "plan-only-de", "docs-only-en", "docs-only-de", "no-changes", "apply-fence-de"])
def test_an_adversarial_wording_reads_the_orders_intent(order, intent):
    assert order_intent(order) == intent
