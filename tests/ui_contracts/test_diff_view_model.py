"""Guard: the diff view model stays in the layer its own test runner can reach.

`apps/ui/src/api/diffViewModel.ts` is the pure half of F037's rendering core, and
`apps/ui/src/api/diffViewModel.test.ts` proves its BEHAVIOUR under vitest, run here through
`tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`.
This guard proves the structural facts vitest cannot see ABOUT ITSELF, and there is no
overlap between the two: a green vitest run says nothing about any of the classes below.

* Vitest passes just as happily on a module that pulls in React or a `.css` module — it would
  simply stop being loadable in the node environment `apps/ui/vitest.config.ts` pins, and the
  failure would surface later, in a component test that does not exist yet.
* Vitest cannot notice an export nobody tests; an untested function is silently green.
* Vitest cannot notice that a threshold was transcribed rather than imported, because both
  spellings agree right up to the moment one of them is edited.
* Vitest cannot see the MAIN CHUNK. A static import of a syntax highlighter passes every
  behavioural test in the suite while shipping every language to every operator on first
  paint, which is the one thing lazily loaded bundles exist to prevent.
* Vitest cannot notice a mapping entry nobody exercised: a suite that iterates
  `DIFF_SUPPORTED_LANGUAGES` stays green for whatever that mapping happens to hold.
* Vitest cannot forbid its own use of a mocking library, and a call counter that is really a
  patched global hides the zero-call number this feature's Acceptance turns on.

DECISION F037 D8 records why this file is Python: `apps/ui/vitest.config.ts` collects
`src/**/*.test.ts` in a NODE environment, so vitest cannot be the witness for its own
configuration — the three facts above are exactly the ones it is blind to.

A TYPESCRIPT MUTATION RED-PROOF *IS* ORDERABLE IN THIS REPOSITORY, and an earlier wording of
this docstring told every future round that it was not. DECISION F037 D10, landed at F037 R21,
records the route: spawn vitest FROM the primary checkout, so it resolves its own gitignored
`apps/ui/node_modules`, and point `--root` at the disposable worktree that guardrail G5 of
`docs/agents/self_drive_protocol.md` confines every destructive check to, so the tree under
test is the worktree's. That round took six such red-proofs through it. The absent
`node_modules` is a routing problem, never a ceiling. This guard needs no `node_modules` at
all, so it is mutated and red-proved directly.

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
LANGUAGES_NAME = "DIFF_SUPPORTED_LANGUAGES"

# The syntax highlighters a `.ts` module would plausibly reach for. Named rather
# than pattern-matched because the point is a SHORT list a reader can audit; the
# specifier scan below is the general guard and this list is the readable one.
HIGHLIGHTER_PACKAGES = (
    "shiki",
    "prismjs",
    "prism-react-renderer",
    "highlight.js",
    "hljs",
    "refractor",
    "lowlight",
    "codemirror",
    "monaco-editor",
)

# The three spellings of a mocking library, which `apps/ui/src` uses nowhere.
MOCKING_TOKENS = ("vi.stubGlobal", "vi.mock", "vi.fn")


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

    `async function` IS IN SCOPE, and was added at F037 R22 with the module's first async
    export. Until then the pattern read `export function` alone, so `loadDiffLanguageBundle`
    would have been the one export this guard could not see — an untested export slipping
    through the guard whose whole purpose is that it cannot.
    """
    return re.findall(r"^export (?:async function|function|const) (\w+)", source, re.MULTILINE)


def module_specifiers(source: str) -> list[str]:
    """Every module specifier the source names, whether statically or dynamically.

    THE SCOPER for the lazy-bundle guard: it catches `import x from "pkg"`, a bare
    `import "pkg"` and a dynamic `import("pkg")` alike, which is what a bundler reads to
    decide what belongs in the main chunk. Run over COMMENT-STRIPPED source, so the WHY
    header naming a package it forbids cannot satisfy or break it (finding `R-0584`).
    """
    return re.findall(r"""(?:\bfrom|\bimport|\brequire)\s*\(?\s*["']([^"']+)["']""", source)


def supported_languages_block(source: str) -> str:
    """The body of the `DIFF_SUPPORTED_LANGUAGES` object literal, as text.

    THE SCOPER for the language-set guard. It is deliberately narrow: reading the ids out of
    the declaration itself means the guard tracks the mapping rather than a list repeated
    here, so an entry added to the module is an entry this file immediately demands a test
    for.
    """
    match = re.search(
        rf"^export const {LANGUAGES_NAME}[^=]*= Object\.freeze\(\{{(.*?)^\}}\);",
        source,
        re.MULTILINE | re.DOTALL,
    )
    assert match is not None, (
        f"{LANGUAGES_NAME} is not declared as a frozen object literal in {MODULE.name}; the "
        f"supported set of docs/roadmap/features/T5_F037.md must be declared exactly once, by "
        f"name, so this guard and the vitest suite read the same mapping"
    )
    return match.group(1)


def supported_language_ids(source: str) -> list[str]:
    """The language ids the mapping maps ONTO, in declaration order and with repeats kept."""
    return re.findall(r'^\s*\w+:\s*"([^"]+)",\s*$', supported_languages_block(source), re.MULTILINE)


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


def test_the_bundle_importer_is_a_parameter_and_no_highlighter_is_imported() -> None:
    """(d) "Lazy" is a property of the MAIN CHUNK, and vitest cannot see the main chunk.

    A green vitest run says nothing here: a static `import "shiki"` at the head of this module
    would pass every behavioural test in `diffViewModel.test.ts` while shipping every language
    to every operator on first paint, which is the one thing lazy bundles exist to prevent.
    The bundle importer is a FUNCTION ARGUMENT for exactly this reason, so the module names no
    package at all and a bundler has nothing to pull in.
    """
    raw = MODULE.read_text()
    source = strip_ts_comments(raw)
    assert len(source) < len(raw), (
        f"the comment scoper returned the whole of {MODULE.name} ({len(source)} of {len(raw)} "
        f"characters), so it stripped nothing and every assertion over it would be reading the "
        f"WHY headers rather than the code"
    )

    control = 'import shiki from "shiki";\nconst mod = await import("prismjs");\n'
    assert module_specifiers(control) == ["shiki", "prismjs"], (
        f"the specifier scan missed a planted import, so its silence over {MODULE.name} proves "
        f"nothing; it found {module_specifiers(control)}"
    )

    specifiers = module_specifiers(source)
    assert specifiers == [], (
        f"{MODULE.name} names the module specifier(s) {specifiers}; it must name none at all — "
        f"the syntax bundle arrives through the `DiffLanguageBundleImporter` argument of "
        f"`loadDiffLanguageBundle`, and any specifier here is a chunk the bundler ships whether "
        f"or not a diff ever needs it"
    )
    named = [package for package in HIGHLIGHTER_PACKAGES if package in source]
    assert named == [], (
        f"{MODULE.name} names the syntax-highlighting package(s) {named} in executable code; "
        f"this module chooses no highlighter, exactly as it chooses no colour and no class"
    )


def test_every_supported_language_id_is_named_by_the_vitest_suite() -> None:
    """(e) No entry of the supported set ships untested.

    Vitest cannot notice a mapping entry nobody exercised — the suite iterates the mapping, so
    it stays green for whatever the mapping happens to hold. This reads the ids out of the
    declaration and demands each one appear in the suite BY NAME, which is what makes an added
    language a test the author has to write rather than a silent pass.
    """
    module_source = strip_ts_comments(MODULE.read_text())
    declarations = re.findall(rf"^export const {LANGUAGES_NAME}\b", module_source, re.MULTILINE)
    assert len(declarations) == 1, (
        f"{LANGUAGES_NAME} is declared {len(declarations)} time(s) in {MODULE.name}; the "
        f"supported set is declared exactly once so no second spelling can drift from it"
    )

    block = supported_languages_block(module_source)
    assert 0 < len(block) < len(module_source), (
        f"the {LANGUAGES_NAME} scoper returned {len(block)} of {len(module_source)} characters; "
        f"a scoper that returns nothing, or the whole module, is not scoping anything"
    )

    ids = supported_language_ids(module_source)
    assert len(ids) >= 2, (
        f"the language-id scan over {LANGUAGES_NAME} found {len(ids)} id(s); a guard that "
        f"checks an empty set checks nothing, so the mapping is either mis-scanned or no longer "
        f"the frozen object literal this file describes"
    )

    test_source = strip_ts_comments(MODULE_TESTS.read_text())
    unnamed = sorted({language for language in ids if f'"{language}"' not in test_source})
    assert unnamed == [], (
        f"{LANGUAGES_NAME} maps onto {unnamed}, which {MODULE_TESTS.name} never names, so no "
        f"test would notice if those bundles were never loadable; every id of the supported set "
        f"is named by the suite that {VITEST_CONFIG_AUTHORITY} runs"
    )


def test_the_vitest_suite_counts_calls_without_a_mocking_library() -> None:
    """(f) The suite proves "no bundle fetch" with its own counter, not with a framework.

    Nothing under `apps/ui/src` patches a global or replaces a module, and this round starts
    nothing: an importer that is a plain function argument is already injectable, so a mocking
    library here would buy nothing and hide the one number this feature's Acceptance turns on.
    Counted over the RAW text, comments included — a comment reaching for one of these
    spellings is drift toward exactly the arrangement this guard exists to prevent.
    """
    control = "const spy = vi.fn();\n"
    assert [token for token in MOCKING_TOKENS if token in control] == ["vi.fn"], (
        "the mocking-token scan missed a planted `vi.fn()`, so its silence over "
        f"{MODULE_TESTS.name} proves nothing"
    )

    text = MODULE_TESTS.read_text()
    offenders = sorted({token for token in MOCKING_TOKENS if token in text})
    assert offenders == [], (
        f"{MODULE_TESTS.name} names {offenders}; the bundle importer is a function ARGUMENT "
        f"with a hand-written counter beside it, which is what keeps the zero-call Acceptance "
        f"property readable at the point of use rather than at the point of configuration"
    )
