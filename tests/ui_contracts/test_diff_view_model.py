"""Guard: the diff view model stays in the layer its own test runner can reach.

`apps/ui/src/api/diffViewModel.ts` is the pure half of F037's rendering core, and
`apps/ui/src/api/diffViewModel.test.ts` proves its BEHAVIOUR under vitest, run here through
`tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`.
This guard proves the structural facts vitest cannot see ABOUT ITSELF, and there is no
overlap between the two: a green vitest run says nothing about any of the three below.

* Vitest passes just as happily on a module that pulls in React or a `.css` module — it would
  simply stop being loadable in the node environment `apps/ui/vitest.config.ts` pins, and the
  failure would surface later, in a component test that does not exist yet.
* Vitest cannot notice an export nobody tests; an untested function is silently green.
* Vitest cannot notice that a threshold was transcribed rather than imported, because both
  spellings agree right up to the moment one of them is edited.

DECISION F037 D8 records why this file is Python: `apps/ui/vitest.config.ts` collects
`src/**/*.test.ts` in a NODE environment, and the same decision records that a mutation
red-proof of TypeScript is not orderable in this repository — `apps/ui/node_modules` is
gitignored, so it is absent from the disposable worktree guardrail G5 of
`docs/agents/self_drive_protocol.md` confines every destructive check to. This guard needs no
`node_modules`, so it is mutated and red-proved normally.

It reads both files AS TEXT and imports nothing from `apps/`.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
UI_API = REPO_ROOT / "apps" / "ui" / "src" / "api"
MODULE = UI_API / "diffViewModel.ts"
MODULE_TESTS = UI_API / "diffViewModel.test.ts"

VITEST_CONFIG_AUTHORITY = (
    "apps/ui/vitest.config.ts (environment: node, include: src/**/*.test.ts) and DECISION F037 D8"
)
THRESHOLD_NAME = "DIFF_HUNK_COLLAPSE_THRESHOLD_LINES"


def strip_ts_comments(text: str) -> str:
    """Drop `//` and `/* */` comments, the scanner `test_decision_answer_wiring.py` uses.

    Every assertion below runs over stripped source. These two files carry long WHY headers
    that NAME the very symbols being asserted — an unstripped guard would be satisfied by the
    comment describing the code rather than by the code itself (finding `R-0584`).
    """
    out: list[str] = []
    i, n = 0, len(text)
    while i < n:
        pair = text[i:i + 2]
        if pair == "//":
            newline = text.find("\n", i)
            i = n if newline == -1 else newline
        elif pair == "/*":
            end = text.find("*/", i + 2)
            i = n if end == -1 else end + 2
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def exported_names(source: str) -> list[str]:
    """Every name the module exports as a value, derived from the module rather than listed.

    Deriving it is the point: a later `export function` grows this set on its own, so an export
    added without a test cannot ship. Types are deliberately out of scope — `export interface`
    and `export type` carry no runtime behaviour for a test to pin.
    """
    return re.findall(r"^export (?:function|const) (\w+)", source, re.MULTILINE)


def threshold_literal(source: str) -> str:
    """The numeric literal `DIFF_HUNK_COLLAPSE_THRESHOLD_LINES` is declared with, as text."""
    match = re.search(rf"^export const {THRESHOLD_NAME} = (\d[\d_]*);", source, re.MULTILINE)
    assert match is not None, (
        f"{THRESHOLD_NAME} is not declared as an exported numeric constant in {MODULE.name}; "
        f"the collapse rule of docs/roadmap/features/T5_F037.md must be declared exactly once, "
        f"by name, so every other site can reference it"
    )
    return match.group(1)


def test_view_model_imports_nothing_and_carries_no_markup() -> None:
    """(a) The module stays inside what the node-environment vitest config can load.

    Invisible to vitest itself, which would pass on a module it could never load in a browser
    and would only fail once something rendered it.
    """
    source = strip_ts_comments(MODULE.read_text())
    offenders = re.findall(r"\bimport\b", source)
    assert offenders == [], (
        f"{MODULE.name} must contain no import statement at all — it is pure data in, pure data "
        f"out, which is what keeps it inside what {VITEST_CONFIG_AUTHORITY} reaches; found "
        f"{len(offenders)} import token(s)"
    )
    for marker in ("</", "/>"):
        assert marker not in source, (
            f"{MODULE.name} must carry no JSX construct ({marker!r} found): it is a .ts module, "
            f"and markup belongs in apps/ui/src/components/ where {VITEST_CONFIG_AUTHORITY} "
            f"reaches none of it"
        )


def test_every_exported_name_is_named_by_the_vitest_suite() -> None:
    """(b) No export ships untested. Vitest cannot see an export nobody imported."""
    module_source = strip_ts_comments(MODULE.read_text())
    test_source = strip_ts_comments(MODULE_TESTS.read_text())
    names = exported_names(module_source)
    assert len(names) >= 2, (
        f"the export scan over {MODULE.name} found {len(names)} name(s); a guard that checks an "
        f"empty set checks nothing, so this file is either mis-scanned or no longer the module "
        f"DECISION F037 D8 describes"
    )
    untested = [name for name in names if name not in test_source]
    assert untested == [], (
        f"{MODULE.name} exports {untested} which {MODULE_TESTS.name} never names, so vitest "
        f"never runs them; every rule of the F037 rendering core is pinned in the layer "
        f"{VITEST_CONFIG_AUTHORITY} reaches"
    )


def test_collapse_threshold_literal_occurs_exactly_once() -> None:
    """(c) The threshold is declared, never transcribed.

    Counted over the RAW text of both files, comments included: a number repeated in prose
    drifts from the rule exactly as readily as one repeated in code.

    ANCHORED TO WHOLE NUMBERS, the repair of finding `R-0728`. A bare `.count(literal)` is a
    substring count, so an unrelated constant whose digits merely CONTAIN the threshold's —
    `2000` beside a threshold of `200` — inflated the count and turned this guard red for a
    change that neither transcribed nor drifted from the collapse rule. The fence below
    forbids a word character or a `.` on either side, which drops `2000`, `1200` and `200.5`
    while still catching the bare `200` this guard exists to catch.
    """
    module_text = MODULE.read_text()
    tests_text = MODULE_TESTS.read_text()
    literal = threshold_literal(strip_ts_comments(module_text))
    whole_number = re.compile(rf"(?<![\w.]){re.escape(literal)}(?![\w.])")
    occurrences = len(whole_number.findall(module_text)) + len(whole_number.findall(tests_text))
    assert occurrences == 1, (
        f"the literal {literal!r} occurs {occurrences} time(s) across {MODULE.name} and "
        f"{MODULE_TESTS.name}; {THRESHOLD_NAME} is declared once and referenced BY NAME "
        f"everywhere else, which is what stops the collapse rule of "
        f"docs/roadmap/features/T5_F037.md from drifting away from its own tests"
    )
