"""Guard: the diff file sidebar draws the model and the two halves agree on one string.

`apps/ui/src/components/diff/DiffFileSidebar.tsx` is the sidebar of F037's viewer
(`docs/roadmap/features/T5_F037.md`, T003). NOTHING IN THIS REPOSITORY CAN RENDER IT: there
is no DOM environment here, and `apps/ui/vitest.config.ts` collects `src/**/*.test.ts` in a
NODE environment, so the frontend runner reaches no markup whatever its availability. The
wiring is therefore gated the way every other component here is gated — by READING it —
exactly as `tests/ui_contracts/test_diff_view_render.py` gates the body of the same viewer.

Every assertion runs over COMMENT-STRIPPED source. All three files carry WHY headers that
NAME the very symbols asserted below — `buildDiffFileSummaries`, `rowKey`, `id` — so an
unstripped guard would be satisfied by the comment describing the code rather than by the
code (finding `R-0584`).

EVERY ASSERTION BELOW IS SCOPED TO A FUNCTION BODY OR TO AN ELEMENT TAG, never to a whole
file. That is finding `R-0725`'s rule, learned in this same feature: a whole-module search
is answered by whichever occurrence survives a break, so it stays green through the very
rename it exists to catch. This guard is written after that finding rather than before it.

It reads all three files AS TEXT and imports nothing from `apps/`.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
UI_SRC = REPO_ROOT / "apps" / "ui" / "src"
SIDEBAR = UI_SRC / "components" / "diff" / "DiffFileSidebar.tsx"
VIEW = UI_SRC / "components" / "diff" / "DiffView.tsx"
SHELL = UI_SRC / "components" / "shell" / "RemedyShell.tsx"

MODEL = "apps/ui/src/api/diffViewModel.ts"
BUILDER = "buildDiffFileSummaries"
VITEST_AUTHORITY = (
    "apps/ui/vitest.config.ts (environment: node, include: src/**/*.test.ts), "
    "DECISION F031 D5 and DECISION F037 D8"
)

# Every field `DiffFileSummary` carries and the sidebar was specified to show. A field the
# model computes and nobody draws is a summary the reader never sees.
SUMMARY_FIELDS = (
    "path",
    "status",
    "added",
    "deleted",
    "hunkCount",
    "oldPath",
    "note",
    "rowKey",
)

# Spellings of a rule the sidebar would be REIMPLEMENTING. Each is a derivation the model
# already made: the hunk count, the per-file stats and the file order the parser fixed.
REIMPLEMENTED_RULE_SPELLINGS = (".hunks.length", ".stats.", "sort(")


def strip_ts_comments(text: str) -> str:
    """Drop `//` and `/* */` comments, the scanner `test_diff_view_render.py` uses.

    None of the three files scanned through this holds a string literal carrying either
    marker, which is what lets so plain a scanner be trustworthy here.
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


def sidebar_code() -> str:
    return strip_ts_comments(SIDEBAR.read_text())


def view_code() -> str:
    return strip_ts_comments(VIEW.read_text())


def shell_code() -> str:
    return strip_ts_comments(SHELL.read_text())


def ts_function_body(code: str, name: str, source: Path) -> str:
    """The body of `export function <name>`, parameter list skipped, brace depth respected.

    The parameter list is stepped over by PAREN depth before the first brace is looked for,
    because every component here destructures its props and so opens a `{` of its own before
    the body ever does. Taking the first brace after the name would return the prop list and
    every assertion built on it would read an empty region.
    """
    match = re.search(rf"export (?:async )?function {name}\b", code)
    assert match, f"{source.name} exports no function named {name}"
    paren = code.index("(", match.end())
    depth = 0
    after_params = -1
    for index in range(paren, len(code)):
        if code[index] == "(":
            depth += 1
        elif code[index] == ")":
            depth -= 1
            if depth == 0:
                after_params = index + 1
                break
    assert after_params != -1, f"the parameter list of {name} never closes in {source.name}"
    start = code.index("{", after_params)
    depth = 0
    for index in range(start, len(code)):
        if code[index] == "{":
            depth += 1
        elif code[index] == "}":
            depth -= 1
            if depth == 0:
                return code[start:index + 1]
    raise AssertionError(f"the body of {name} never closes in {source.name}")


def jsx_opening_tag_at(code: str, start: int, source: Path) -> str:
    """The whole opening tag beginning at `start`, brace depth respected.

    A JSX attribute value carries arbitrary expressions — an arrow function's `=>` holds a
    `>` of its own — so the tag ends at the first `>` OUTSIDE every `{...}`. Scanning to the
    first `>` instead would cut the tag in the middle of an `onClick`.
    """
    depth = 0
    for index in range(start, len(code)):
        char = code[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
        elif char == ">" and depth == 0:
            return code[start:index + 1]
    raise AssertionError(f"the tag opening at offset {start} never closes in {source.name}")


def sidebar_entry_tag(code: str) -> str:
    """The opening tag of the sidebar's per-file control: the one naming `rowKey`.

    Scoped rather than swept, and scoped BY the model's key on purpose. The question this
    guard asks is what the reader clicks and what that click carries, and a whole-file search
    for `<button` would be answered by any other control the sidebar might one day grow.
    """
    body = ts_function_body(code, "DiffFileSidebar", SIDEBAR)
    tags: list[str] = []
    index = body.find("<button")
    while index != -1:
        tags.append(jsx_opening_tag_at(body, index, SIDEBAR))
        index = body.find("<button", index + 1)
    assert tags, (
        f"{SIDEBAR.name} renders no <button inside DiffFileSidebar, so its file list is not "
        f"a set of controls and a reader has nothing to click"
    )
    keyed = [tag for tag in tags if "rowKey" in tag]
    assert len(keyed) == 1, (
        f"{SIDEBAR.name} has {len(keyed)} <button tags naming rowKey out of {len(tags)} in "
        f"DiffFileSidebar; the entry must navigate by the model's own key, because any other "
        f"string is a second identity for a file the model already addressed"
    )
    return keyed[0]


def file_row_tag(code: str) -> str:
    """The opening tag of `DiffView`'s FILE row, found by the path it draws.

    Anchored on `row.file.path` rather than on the `id` this guard is about to assert, so a
    deleted `id` fails the assertion with the reason rather than losing the scanner.
    """
    body = ts_function_body(code, "DiffView", VIEW)
    marker = body.index("row.file.path")
    return jsx_opening_tag_at(body, body.rindex("<div", 0, marker), VIEW)


class TestTheStripperIsNotVacuous:
    """Without this, every assertion below is satisfiable by the three files' own WHY
    headers, each of which names the symbols asserted here verbatim."""

    def test_the_stripper_removes_both_comment_forms(self):
        sample = 'const a = 1; // note\n/* block */ const b = 2;'
        stripped = strip_ts_comments(sample)
        assert "note" not in stripped, "the // form must go"
        assert "block" not in stripped, "the /* */ form must go"
        assert "const b = 2;" in stripped, "and the code between them must survive"

    def test_every_scanned_file_really_loses_text_to_the_stripper(self):
        for source in (SIDEBAR, VIEW, SHELL):
            raw = source.read_text()
            assert "//" in raw or "/*" in raw, (
                f"{source.name} must keep the WHY comments the Code Discoverability "
                f"Conventions of AGENTS.md require; with no comment in the file the stripper "
                f"proves nothing"
            )
            assert len(strip_ts_comments(raw)) < len(raw), (
                f"the stripper returned {source.name} unchanged, so every assertion in this "
                f"module that reads it would be satisfied by prose rather than by code "
                f"(finding R-0584)"
            )

    def test_the_function_scoper_returns_less_than_each_whole_module(self):
        """The scoping rule finding `R-0725` cost this feature two rounds to learn.

        A `ts_function_body` that silently handed back the file would turn every assertion
        below into the whole-file search it was written to avoid, and all of them would
        still pass.
        """
        for code, name, source in (
            (sidebar_code(), "DiffFileSidebar", SIDEBAR),
            (view_code(), "DiffView", VIEW),
            (shell_code(), "RemedyShell", SHELL),
        ):
            body = ts_function_body(code, name, source)
            assert len(body) < len(code), (
                f"ts_function_body returned {len(body)} characters for {name} out of "
                f"{len(code)} in {source.name}, so it is not scoping at all and every "
                f"assertion built on it is a whole-file search wearing a function's name "
                f"(finding R-0725)"
            )
            assert "import " not in body, (
                f"the body ts_function_body returns for {name} reaches the import block of "
                f"{source.name}, so a symbol merely IMPORTED there could satisfy an "
                f"assertion about what the function does with it"
            )

    def test_both_tag_scanners_find_their_subject(self):
        entry = sidebar_entry_tag(sidebar_code())
        assert entry.startswith("<button"), (
            f"the entry scanner returned {entry[:40]!r} from {SIDEBAR.name}, which is not an "
            f"opening button tag, so the assertions scoped to it read the wrong region"
        )
        row = file_row_tag(view_code())
        assert row.startswith("<div"), (
            f"the file-row scanner returned {row[:40]!r} from {VIEW.name}, which is not the "
            f"row element, so the anchor assertion below reads the wrong region"
        )


class TestTheSidebarDerivesNothing:
    """(b) DECISION F031 D5. Every decidable rule of this feature lives in `diffViewModel.ts`,
    where the node-environment vitest config really executes it. A rule reimplemented in this
    markup is a rule no gate in this repository can run."""

    def test_the_sidebar_calls_the_model_builder(self):
        body = ts_function_body(sidebar_code(), "DiffFileSidebar", SIDEBAR)
        assert f"{BUILDER}(" in body, (
            f"{SIDEBAR.name} must CALL {BUILDER} from {MODEL} inside DiffFileSidebar: naming "
            f"it in an import or a comment is not using it, and a sidebar that walked the "
            f"envelope itself would put the file order, the counts and the row keys outside "
            f"what {VITEST_AUTHORITY} reaches"
        )

    def test_the_sidebar_reimplements_no_rule_of_the_model(self):
        body = ts_function_body(sidebar_code(), "DiffFileSidebar", SIDEBAR)
        for spelling in REIMPLEMENTED_RULE_SPELLINGS:
            assert spelling not in body, (
                f"DiffFileSidebar in {SIDEBAR.name} contains {spelling!r}. The hunk count is "
                f"{BUILDER}'s answer, the per-file stats are the parser's and the file order "
                f"is fixed upstream — each of those transcribed here is the model's own "
                f"derivation arriving under another name, outside what {VITEST_AUTHORITY} "
                f"can execute"
            )


class TestEverySummaryFieldIsReallyDrawn:
    """(c) `DiffFileSummary` carries eight fields and the sidebar was specified to show all of
    them. A field the model computes and the markup never reads is a summary the reader never
    sees, and nothing else in this repository would notice."""

    def test_the_sidebar_reads_every_field_of_the_summary(self):
        body = ts_function_body(sidebar_code(), "DiffFileSidebar", SIDEBAR)
        missing = [
            field for field in SUMMARY_FIELDS
            if not re.search(rf"\.{field}\b", body)
        ]
        assert not missing, (
            f"DiffFileSidebar in {SIDEBAR.name} reads none of {missing} off its summaries, so "
            f"{BUILDER} in {MODEL} computes a value this sidebar drops on the floor"
        )


class TestTheEntryIsARealControl:
    """(d) The reason the hunk head in `DiffView.tsx` is a button: a div carries no keyboard
    affordance at all, and the explicit type stops it submitting a form it may one day sit
    in."""

    def test_the_entry_is_a_button_with_an_explicit_type(self):
        tag = sidebar_entry_tag(sidebar_code())
        assert 'type="button"' in tag, (
            f"the file entry in {SIDEBAR.name} is {tag[:60]!r}, which declares no explicit "
            f"button type; inside a form it would submit it, and the reader's way into a "
            f"file would reload the page instead"
        )


class TestTheTwoHalvesAgreeOnOneString:
    """(e) The sidebar moves the reader to a row by a DOM id, and `DiffView.tsx` puts that id
    on the row. Both strings are `buildDiffFileSummaries`' own — `rowKey` on one side and the
    row's `key` on the other — which is the whole reason neither half recomputes it."""

    def test_the_sidebar_navigates_by_the_models_key(self):
        tag = sidebar_entry_tag(sidebar_code())
        assert "rowKey" in tag, (
            f"the file entry in {SIDEBAR.name} is {tag[:60]!r} and carries no rowKey, so it "
            f"addresses a row by something the model did not mint — a path or an index is "
            f"data about a file rather than its address"
        )

    def test_the_file_row_carries_a_dom_anchor_holding_the_same_string(self):
        tag = file_row_tag(view_code())
        assert "id=" in tag, (
            f"the file row in {VIEW.name} is {tag[:60]!r} and carries no id. A React key is "
            f"reconciliation and never reaches the DOM, so with no id the sidebar's entry "
            f"has nothing at all to move the reader to and every click is inert"
        )
        assert "id={row.key}" in tag, (
            f"the file row in {VIEW.name} is {tag[:60]!r}, whose id is not row.key. The two "
            f"halves agree only because {BUILDER} in {MODEL} puts that same string in each "
            f"summary's rowKey; any other id is a second naming scheme for the same row"
        )


class TestTheShellRendersBothHalves:
    """(f) A sidebar nobody mounts is invisible, and a sidebar mounted without the body it
    points into offers rows to jump to that are not on the screen."""

    def test_the_shell_renders_the_sidebar_beside_the_view(self):
        body = ts_function_body(shell_code(), "RemedyShell", SHELL)
        for tag in ("<DiffFileSidebar", "<DiffView"):
            assert tag in body, (
                f"RemedyShell in {SHELL.name} renders no {tag}; importing a component is not "
                f"mounting it, and half of the viewer would be unreachable from the shell "
                f"while every other gate in this repository stayed green"
            )
