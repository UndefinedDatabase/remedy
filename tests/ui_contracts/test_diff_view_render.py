"""Guard: the rendered diff viewer is wired to rules it must not reimplement.

`apps/ui/src/components/diff/DiffView.tsx` is the DRAWING half of F037's rendering core
(`docs/roadmap/features/T5_F037.md`, T002). NOTHING IN THIS REPOSITORY CAN RENDER IT: there
is no DOM environment here, and `apps/ui/vitest.config.ts` collects `src/**/*.test.ts` in a
NODE environment, so the frontend runner reaches no markup at all whatever its availability.
The component's wiring is therefore gated the way every other component here is gated — by
READING it — exactly as `tests/ui_contracts/test_decision_answer_wiring.py` gates the
decision inbox, and as `tests/ui_contracts/test_diff_surface_css.py` gates the stylesheet
this file reads beside it.

Every assertion runs over COMMENT-STRIPPED source. The component carries a long WHY header
that NAMES the very symbols asserted below — `buildDiffRowModels`, `toggleHunkCollapse`,
`splitLineIntoIntralineSegments` — so an unstripped guard would be satisfied by the comment
describing the code rather than by the code itself (finding `R-0584`).

It reads both files AS TEXT and imports nothing from `apps/`.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DIFF_DIR = REPO_ROOT / "apps" / "ui" / "src" / "components" / "diff"
COMPONENT = DIFF_DIR / "DiffView.tsx"
COMPONENT_CSS = DIFF_DIR / "DiffView.module.css"

MODEL = "apps/ui/src/api/diffViewModel.ts"
MODEL_PATH = REPO_ROOT / "apps" / "ui" / "src" / "api" / "diffViewModel.ts"
ROW_HEIGHT_NAME = "DIFF_VIRTUAL_ROW_HEIGHT_PX"
VITEST_AUTHORITY = (
    "apps/ui/vitest.config.ts (environment: node, include: src/**/*.test.ts), "
    "DECISION F031 D5 and DECISION F037 D8"
)
CSS_AUTHORITY = (
    "docs/roadmap/features/T5_F037.md (Design section, binding CSS; amendments A4 and A5)"
)

# The five rules the component must CALL rather than carry. Each is a decidable rule that
# lives in the model module, where the node-environment vitest config really runs it.
DELEGATED_RULES = (
    "buildDiffRowModels",
    "defaultCollapsedHunkIds",
    "diffRowWindowForViewport",
    "toggleHunkCollapse",
    "splitLineIntoIntralineSegments",
)

# Spellings of a rule REIMPLEMENTED in markup. The collapse threshold's literal is declared
# exactly once, in the model module; a `.length` compared against anything is that rule
# arriving under another name; a sort is the file order the parser already fixed.
#
# The last four are VIRTUALIZATION arriving in the markup. The component receives pixels and
# indices that are already computed, so naming the row height, dividing by it in either
# direction, or slicing the row list from a hard zero would each be the viewport arithmetic
# of `diffRowWindowForViewport` transcribed into the one layer no runner here can execute.
REIMPLEMENTED_RULE_SPELLINGS = (
    "200",
    ".length >",
    "sort(",
    ROW_HEIGHT_NAME,
    "Math.floor(",
    "Math.ceil(",
    ".slice(0,",
)

# F256's wiring, named here rather than inside the assertions so the two halves of it — the
# module the component reaches and the two functions it calls out of the model layer — grep
# to one place. These are DELIBERATELY NOT in DELEGATED_RULES above: that tuple is the set of
# decidable rules the component must not carry, and widening it would change what the
# existing delegation test means.
HIGHLIGHT_MODULE = "apps/ui/src/api/diffHighlight.ts"
HIGHLIGHT_IMPORT_SPECIFIER = '"../../api/diffHighlight"'
HIGHLIGHT_IMPORTER_NAME = "DIFF_HIGHLIGHT_BUNDLE_IMPORTER"
HIGHLIGHT_KIND_CLASS_NAME = "DIFF_HIGHLIGHT_KIND_CLASS"
HIGHLIGHT_WIRED_CALLS = ("loadDiffLanguageBundle", "composeHighlightedRuns")
HIGHLIGHT_PLAIN_KIND = "plain"
HIGHLIGHT_AUTHORITY = "DECISION F256 D1 (lazy bundles) and DECISION F256 D2 (the palette)"


def strip_ts_comments(text: str) -> str:
    """Drop `//` and `/* */` comments, the scanner `test_decision_answer_wiring.py` uses.

    This component holds no string literal carrying either marker, which is what lets so
    plain a scanner be trustworthy here.
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


def strip_css_comments(css: str) -> str:
    """Drop `/* ... */` blocks so a selector NAMED in prose is never read as a rule."""
    return re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)


def css_rule_selectors(css: str) -> set[str]:
    """Every selector that really opens a declaration block, whitespace-normalised.

    Derived from the sheet rather than listed, so a rule added or lost changes this set on
    its own. A selector mentioned only in a comment is not in it, which is the whole point:
    the deliberate-absence paragraph this sheet carried until F037 R16 described the very
    rules it did not have.
    """
    selectors: set[str] = set()
    for chunk in strip_css_comments(css).split("}"):
        head, brace, _body = chunk.partition("{")
        if not brace:
            continue
        for part in head.split(","):
            selector = " ".join(part.split())
            if selector:
                selectors.add(selector)
    return selectors


def css_class_names(css: str) -> set[str]:
    """Every class name any rule selector in the sheet names."""
    return set(re.findall(r"\.([A-Za-z_][\w-]*)", " ".join(css_rule_selectors(css))))


def component_class_names(code: str) -> list[str]:
    """Every class the component asks the CSS module for, as `styles.<name>`."""
    return re.findall(r"styles\.(\w+)", code)


def ts_const_statement(code: str, name: str) -> str:
    """The whole `const <name> ... ;` statement, from the keyword to its own semicolon.

    SCOPED rather than swept, for the reason finding `R-0725` records: the questions below
    are about ONE declaration each — what the importer imports, and what the kind mapping
    maps — and a whole-file `in` check would be answered by any other line of the component.
    Neither of the two declarations this reads carries a semicolon inside its initialiser,
    which is what makes so plain a terminator trustworthy here; a future initialiser that did
    would cut this short and the vacuity assertion below is what would catch it.
    """
    match = re.search(rf"^const {name}\b", code, re.MULTILINE)
    assert match, (
        f"{COMPONENT.name} declares no module-level `const {name}`, which {HIGHLIGHT_AUTHORITY} "
        f"requires it to carry"
    )
    end = code.find(";", match.end())
    assert end != -1, f"the `const {name}` statement in {COMPONENT.name} never terminates"
    return code[match.start():end + 1]


def highlight_kind_class_entries(code: str) -> list[tuple[str, str]]:
    """Every `<kind>: <value>` pair of the token-kind class mapping, in source order.

    The kinds are read off the component rather than listed here, so a kind added to
    `apps/ui/src/api/diffHighlight.ts` and wired in changes this set on its own.
    """
    statement = ts_const_statement(code, HIGHLIGHT_KIND_CLASS_NAME)
    body = statement[statement.index("{"):]
    return [
        (match.group(1), match.group(2).strip())
        for match in re.finditer(r"(\w+)\s*:\s*([^,\n]+?)\s*,", body)
    ]


def jsx_opening_tag_at(code: str, start: int) -> str:
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
    raise AssertionError(f"the tag opening at offset {start} never closes in {COMPONENT.name}")


def _signature_end(code: str, after_name: int) -> int:
    """The index just past the argument list's closing parenthesis."""
    start = code.index("(", after_name)
    depth = 0
    for index in range(start, len(code)):
        if code[index] == "(":
            depth += 1
        elif code[index] == ")":
            depth -= 1
            if depth == 0:
                return index + 1
    raise AssertionError(f"the argument list opened at {start} never closes")


def ts_function_body(code: str, name: str) -> str:
    """The body of `export function <name>`, brace depth respected.

    The signature's own braces — the destructured prop list and its inline type — are stepped
    over by matching PARENTHESES first, so what comes back is the body and not the arguments.
    """
    match = re.search(rf"export function {name}\b", code)
    assert match, f"no exported function named {name} was found in {COMPONENT.name}"
    open_index = code.index("{", _signature_end(code, match.end()))
    depth = 0
    for index in range(open_index, len(code)):
        if code[index] == "{":
            depth += 1
        elif code[index] == "}":
            depth -= 1
            if depth == 0:
                return code[open_index:index + 1]
    raise AssertionError(f"the body of {name} never closes in {COMPONENT.name}")


def diff_view_body(code: str) -> str:
    """The component function's own body — never the import block above it."""
    return ts_function_body(code, "DiffView")


def scrolling_section_tag(code: str) -> str:
    """The opening tag of the component's `<section data-ui="diff-view">`.

    That element IS the scrolling panel — it is the one whose `scrollTop` and `clientHeight`
    the handler reads — so the scroll assertions are scoped to its open tag rather than swept
    over the file, where any element's props would answer them (finding `R-0725`).
    """
    for match in re.finditer(r"<section\b", code):
        tag = jsx_opening_tag_at(code, match.start())
        if 'data-ui="diff-view"' in tag:
            return tag
    raise AssertionError(f'no <section data-ui="diff-view"> open tag was found in {COMPONENT.name}')


def inline_styled_div_tags(body: str) -> list[str]:
    """Every `<div ...>` open tag in the component body carrying an inline `style`.

    The spacers are the only such elements: every other div this component draws wears a
    class from the CSS module instead. Scoped to the BODY so a styled element in some future
    helper above the component cannot answer for them.
    """
    tags = [jsx_opening_tag_at(body, match.start()) for match in re.finditer(r"<div\b", body)]
    return [tag for tag in tags if "style=" in tag]


def css_declaration_block(css: str, selector: str) -> str:
    """The declaration block of the rule whose selector is EXACTLY `selector`.

    Exact rather than substring: `.diffLine`, `.diffLine.add` and `.diffLine .ln` are three
    different rules and only the first one carries the line box this guard measures.
    """
    for chunk in strip_css_comments(css).split("}"):
        head, brace, block = chunk.partition("{")
        if not brace:
            continue
        if selector in [" ".join(part.split()) for part in head.split(",")]:
            return block
    raise AssertionError(f"{COMPONENT_CSS.name} carries no rule with the selector {selector!r}")


def stylesheet_line_box_px(css: str) -> float:
    """One `.diffLine`'s rendered height, PARSED out of the sheet's own `font` shorthand.

    Both numbers are read from the file rather than transcribed here, which is the whole
    point: a guard that carried its own copy of `12.5` and `1.6` would agree with itself
    after the stylesheet changed.
    """
    block = css_declaration_block(css, ".diffLine")
    match = re.search(r"font:\s*([\d.]+)px\s*/\s*([\d.]+)", block)
    assert match, (
        f"the `.diffLine` rule in {COMPONENT_CSS.name} carries no `font: <size>px/<height>` "
        f"shorthand, so the row height {ROW_HEIGHT_NAME} fixes cannot be checked against the "
        f"binding CSS at all ({CSS_AUTHORITY})"
    )
    return float(match.group(1)) * float(match.group(2))


def declared_row_height_px(source: str) -> int:
    """The literal `DIFF_VIRTUAL_ROW_HEIGHT_PX` is declared with in the model module."""
    match = re.search(rf"^export const {ROW_HEIGHT_NAME} = (\d+);", source, re.MULTILINE)
    assert match, (
        f"{MODEL} does not declare {ROW_HEIGHT_NAME} as an exported numeric constant; the "
        f"row every index and spacer of the virtualized window is measured in must be "
        f"declared exactly once, by name"
    )
    return int(match.group(1))


def hunk_head_tag(code: str) -> str:
    """The opening tag carrying `aria-expanded` — the hunk head and nothing else.

    Scoped rather than swept: the question is what ELEMENT the collapse control is, and a
    whole-file search for `<button` would be answered by any other control the component
    might one day grow.
    """
    marker = code.index("aria-expanded")
    return jsx_opening_tag_at(code, code.rindex("<", 0, marker))


class TestTheStripperIsNotVacuous:
    """Without this, a stripper that silently returned its input would make every assertion
    below satisfiable by the component's own prose header, which names each symbol."""

    def test_the_stripper_removes_both_comment_forms(self):
        sample = 'const a = 1; // note\n/* block */ const b = 2;'
        stripped = strip_ts_comments(sample)
        assert "note" not in stripped, "the // form must go"
        assert "block" not in stripped, "the /* */ form must go"
        assert "const b = 2;" in stripped, "and the code between them must survive"

    def test_the_component_really_loses_text_to_the_stripper(self):
        raw = COMPONENT.read_text()
        assert "//" in raw and "/*" in raw, (
            f"{COMPONENT.name} must keep the WHY header the Code Discoverability Conventions "
            f"of AGENTS.md require; with no comment in the file the stripper below proves nothing"
        )
        assert len(strip_ts_comments(raw)) < len(raw), (
            f"the stripper returned {COMPONENT.name} unchanged, so every assertion in this "
            f"module would be satisfied by prose rather than by code (finding R-0584)"
        )

    def test_the_css_stripper_removes_a_comment_the_sheet_really_carries(self):
        raw = COMPONENT_CSS.read_text()
        assert "/*" in raw, f"{COMPONENT_CSS.name} must keep its binding-CSS header"
        assert len(strip_css_comments(raw)) < len(raw), (
            f"the CSS stripper returned {COMPONENT_CSS.name} unchanged, so a selector named "
            f"only in prose would be read as a rule"
        )


class TestTheComponentDerivesNothing:
    """(a) DECISION F031 D5. Every decidable rule of this feature lives in `diffViewModel.ts`,
    where the node-environment vitest config really executes it. A rule reimplemented in this
    markup is a rule no gate in this repository can run."""

    def test_the_component_calls_every_rule_it_must_not_carry(self):
        code = strip_ts_comments(COMPONENT.read_text())
        for rule in DELEGATED_RULES:
            assert f"{rule}(" in code, (
                f"{COMPONENT.name} must CALL {rule} from {MODEL}: naming it in an import or a "
                f"comment is not using it, and a component that computed this itself would put "
                f"the rule outside what {VITEST_AUTHORITY} reaches"
            )

    def test_the_component_reimplements_no_rule_of_the_model(self):
        code = strip_ts_comments(COMPONENT.read_text())
        for spelling in REIMPLEMENTED_RULE_SPELLINGS:
            assert spelling not in code, (
                f"{COMPONENT.name} contains {spelling!r}. The collapse threshold is declared "
                f"exactly once, as DIFF_HUNK_COLLAPSE_THRESHOLD_LINES in {MODEL}, the row list "
                f"and its hidden-line counts are buildDiffRowModels' answer, the envelope's "
                f"file order is the parser's, and every row index and spacer pixel of the "
                f"virtualized window is diffRowWindowForViewport's — each of those transcribed "
                f"here is a rule {VITEST_AUTHORITY} can no longer execute"
            )


class TestEveryClassTheComponentNamesIsReal:
    """(b) The stylesheet is a transcription of the binding CSS and defines a closed set of
    classes. A `styles.<name>` with no rule behind it is silent: the element renders with the
    browser's defaults and no visual review reliably catches an unstyled diff."""

    def test_the_scan_finds_classes_on_both_sides(self):
        named = component_class_names(strip_ts_comments(COMPONENT.read_text()))
        defined = css_class_names(COMPONENT_CSS.read_text())
        assert named, (
            f"{COMPONENT.name} asks the CSS module for no class at all; a guard that compares "
            f"an empty set checks nothing ({CSS_AUTHORITY})"
        )
        assert defined, (
            f"{COMPONENT_CSS.name} defines no class at all, so this comparison could not fail "
            f"({CSS_AUTHORITY})"
        )

    def test_every_class_the_component_names_has_a_rule_in_the_stylesheet(self):
        named = component_class_names(strip_ts_comments(COMPONENT.read_text()))
        defined = css_class_names(COMPONENT_CSS.read_text())
        missing = sorted({name for name in named if name not in defined})
        assert not missing, (
            f"{COMPONENT.name} names {missing}, which {COMPONENT_CSS.name} does not define. A "
            f"CSS module hands back undefined for such a name, so the element ships unstyled "
            f"and the binding CSS of {CSS_AUTHORITY} never reaches the screen"
        )


class TestTheHunkHeadIsAControl:
    """(c) The hunk head opens and closes its hunk, which is the collapse the Design section
    of `docs/roadmap/features/T5_F037.md` requires. A `div` carries no keyboard affordance at
    all, so the whole collapse would be mouse-only."""

    def test_the_collapse_control_is_a_button_rather_than_a_div(self):
        tag = hunk_head_tag(strip_ts_comments(COMPONENT.read_text()))
        assert tag.startswith("<button"), (
            f"the element carrying aria-expanded in {COMPONENT.name} opens as {tag[:24]!r}; the "
            f"hunk head must be a button, or the hunk collapse of {CSS_AUTHORITY} is unreachable "
            f"by keyboard"
        )

    def test_the_control_declares_its_type_and_its_state(self):
        tag = hunk_head_tag(strip_ts_comments(COMPONENT.read_text()))
        assert 'type="button"' in tag, (
            f"the hunk head in {COMPONENT.name} needs an explicit type, or it submits the form "
            f"it may one day sit in — the rule every control in this package follows"
        )
        assert "aria-expanded" in tag, (
            f"the hunk head in {COMPONENT.name} must say whether its hunk is open; a control "
            f"whose state is visible only as a row count announces nothing"
        )

    def test_the_declared_state_is_the_negation_of_the_collapse_flag(self):
        """The POLARITY, which the presence assertion above does not pin.

        Measured at `774cf732`: inverting this expression left the whole module green at 12
        passed, so `aria-expanded` bound to the flag itself rather than to its negation would
        ship unnoticed — and a screen reader would then announce every OPEN hunk as closed,
        which is worse than announcing nothing at all.
        """
        tag = hunk_head_tag(strip_ts_comments(COMPONENT.read_text()))
        assert "aria-expanded={!row.collapsed}" in tag, (
            f"the hunk head in {COMPONENT.name} must bind aria-expanded to the NEGATION of "
            f"row.collapsed; `expanded` and `collapsed` are opposites, and binding one to the "
            f"other inverts every announcement the control makes"
        )
        assert "aria-expanded={row.collapsed}" not in tag, (
            f"the hunk head in {COMPONENT.name} binds aria-expanded to row.collapsed itself, "
            f"so an open hunk announces itself as collapsed and a collapsed one as open"
        )


class TestTheIntralineMarkExists:
    """(d) Amendment A5 of `docs/roadmap/features/T5_F037.md` and DECISION F037 D9. Acceptance
    requires intraline markers to highlight word-level changes, and F037 R9 through R15 each
    deferred the treatment. This is that requirement expressed where it can fail: the cut, the
    marked element's class, and the two rules that give it a colour."""

    def test_the_component_cuts_the_line_and_marks_the_covered_run(self):
        code = strip_ts_comments(COMPONENT.read_text())
        assert "splitLineIntoIntralineSegments(" in code, (
            f"{COMPONENT.name} must cut a line through {MODEL}; rendering the content plainly "
            f"loses the word-level emphasis Goal & Done of {CSS_AUTHORITY} requires"
        )
        assert "styles.intraline" in code, (
            f"{COMPONENT.name} names no intraline class, so a marked segment would render "
            f"exactly like an unmarked one (amendment A5, DECISION F037 D9)"
        )

    def test_both_intraline_rules_are_real_rules_in_the_stylesheet(self):
        selectors = css_rule_selectors(COMPONENT_CSS.read_text())
        for selector in (".diffLine.add .intraline", ".diffLine.del .intraline"):
            assert selector in selectors, (
                f"{COMPONENT_CSS.name} carries no `{selector}` rule. Amendment A5 gives the mark "
                f"this sheet's OWN added and removed hues at a higher alpha, one rule per side; "
                f"with one of them gone that side's emphasis is invisible ({CSS_AUTHORITY})"
            )


class TestTheTruncationNoticeExists:
    """(e) DECISION F037 D5, D6 and D7 are three ceilings — the parsed body, the file count and
    the artifact bytes — and `truncated` is the single flag all three feed. A viewer that shows
    part of a diff in silence is the failure those ceilings exist to avoid."""

    def test_the_component_reads_the_envelopes_truncation_flag(self):
        code = strip_ts_comments(COMPONENT.read_text())
        assert "envelope.truncated" in code, (
            f"{COMPONENT.name} never reads envelope.truncated, so a diff cut short by DECISION "
            f"F037 D5, D6 or D7 would render as a complete one and the operator would judge a "
            f"change against a prefix of it"
        )


class TestTheComponentReallyVirtualizes:
    """(f) "virtual scrolling >2k lines" of the Design section of
    `docs/roadmap/features/T5_F037.md`, expressed where it can fail.

    `TestTheComponentDerivesNothing` above says the component must not do the arithmetic; this
    class says it must do the DRAWING — ask the model for a window, slice by that window's own
    two indices, measure the panel on scroll, and stand the undrawn rows up as spacers. A
    component that merely IMPORTED `diffRowWindowForViewport` and rendered the whole row list
    would satisfy the delegation check alone and still put ten thousand rows in the DOM.

    EVERY ASSERTION IS SCOPED to a function body or a JSX open tag, never to the whole file:
    finding `R-0725` is the defect a whole-file `in` check produces.
    """

    def test_every_new_scanner_returns_strictly_less_than_its_whole_file(self):
        """The vacuity guard the scoped assertions below stand on.

        A scoper that silently handed back its input would turn each of them into the
        whole-file search this class exists to avoid, and all of them would still pass.
        """
        code = strip_ts_comments(COMPONENT.read_text())
        css = COMPONENT_CSS.read_text()
        scoped = (
            ("DiffView body", diff_view_body(code), code),
            ("diff-view section tag", scrolling_section_tag(code), code),
            (".diffLine declaration block", css_declaration_block(css, ".diffLine"), css),
        )
        for label, region, whole in scoped:
            assert region, f"the scanner for the {label} found nothing at all"
            assert len(region) < len(whole), (
                f"the scanner for the {label} returned {len(region)} characters out of "
                f"{len(whole)}, so it is not scoping and every assertion built on it is a "
                f"whole-file search (finding R-0725)"
            )
        spacers = inline_styled_div_tags(diff_view_body(code))
        assert spacers, (
            f"no inline-styled div was found in the body of {COMPONENT.name}, so the two "
            f"spacer assertions below would be checking an empty list"
        )
        for tag in spacers:
            assert len(tag) < len(code), (
                f"an inline-styled div tag scanner returned {len(tag)} characters out of "
                f"{len(code)}, so it is not scoping (finding R-0725)"
            )

    def test_the_component_asks_the_model_for_a_window(self):
        body = diff_view_body(strip_ts_comments(COMPONENT.read_text()))
        assert "diffRowWindowForViewport(" in body, (
            f"{COMPONENT.name} never CALLS diffRowWindowForViewport in its own body, so the "
            f"windowing rule of {MODEL} has no caller and every row of a ten-thousand-row "
            f"diff reaches the DOM. Scoped to the body because the import list names it too "
            f"(finding R-0725)"
        )

    def test_the_drawn_rows_are_sliced_by_the_windows_own_two_indices(self):
        body = diff_view_body(strip_ts_comments(COMPONENT.read_text()))
        assert re.search(r"\.slice\(\s*(\w+)\.startIndex\s*,\s*\1\.endIndex\s*\)", body), (
            f"{COMPONENT.name} does not slice its row list with `<window>.startIndex` and "
            f"`<window>.endIndex` of the SAME window value. Those two are the half-open pair "
            f"diffRowWindowForViewport answers with, and a component that draws the whole "
            f"list beside them has computed a window it then ignores"
        )

    def test_the_scrolling_panel_measures_itself_on_scroll(self):
        tag = scrolling_section_tag(strip_ts_comments(COMPONENT.read_text()))
        assert "onScroll" in tag, (
            f"the scrolling panel of {COMPONENT.name} carries no onScroll handler, so the "
            f"viewport is measured once at zero and the window never moves — the operator "
            f"would scroll a document whose drawn rows never change"
        )
        for measurement in ("currentTarget.scrollTop", "currentTarget.clientHeight"):
            assert measurement in tag, (
                f"the onScroll handler on the panel of {COMPONENT.name} never reads "
                f"{measurement}. Both numbers are needed: an offset without the height it "
                f"was measured against names no range of rows, and the height is what "
                f"resolves the unmeasured-viewport fallback in {MODEL}"
            )

    def test_both_spacer_heights_reach_an_inline_style(self):
        body = diff_view_body(strip_ts_comments(COMPONENT.read_text()))
        tags = inline_styled_div_tags(body)
        for field in ("rowsBeforePx", "rowsAfterPx"):
            carrying = [tag for tag in tags if field in tag]
            assert len(carrying) == 1, (
                f"{COMPONENT.name} has {len(carrying)} inline-styled div(s) naming {field}; "
                f"exactly one spacer must be sized from it, or the scrollbar stops describing "
                f"the whole document and a ten-thousand-row diff scrolls as if it were the "
                f"length of its window"
            )
            assert "style=" in carrying[0], (
                f"the {field} spacer in {COMPONENT.name} does not carry an inline style"
            )
            assert "className" not in carrying[0], (
                f"the {field} spacer in {COMPONENT.name} asks the CSS module for a class. The "
                f"stylesheet is a transcription of the binding CSS and defines a closed set of "
                f"classes; a spacer is presentation that set does not cover ({CSS_AUTHORITY})"
            )

    def test_the_row_height_agrees_with_the_stylesheets_own_line_box(self):
        """The one guard that stops the model and the stylesheet drifting apart in silence.

        Both numbers are PARSED — the `font: <size>px/<height>` shorthand out of the sheet's
        `.diffLine` rule, and the constant's literal out of the model module. Nothing here is
        transcribed, so editing either file alone turns this red instead of leaving a viewer
        whose spacers are sized in a row height the rows do not have.
        """
        measured = stylesheet_line_box_px(COMPONENT_CSS.read_text())
        declared = declared_row_height_px(MODEL_PATH.read_text())
        assert measured == declared, (
            f"{COMPONENT_CSS.name} renders one .diffLine at {measured}px, while {MODEL} "
            f"declares {ROW_HEIGHT_NAME} = {declared}. Every row index and both spacer heights "
            f"of the virtualized window are computed from the constant, so a disagreement "
            f"scrolls the viewer to the wrong rows and mis-sizes the document ({CSS_AUTHORITY})"
        )


class TestTheHighlightIsWiredAndLazy:
    """(g) F256's wiring, expressed where it can fail. `apps/ui/src/api/diffHighlight.ts` shipped
    the token model and `composeHighlightedRuns` shipped the composition, but a model with no
    caller highlights nothing — the defect class finding `R-0220` records. This class asserts the
    three halves of the wiring the component owns: that it CALLS the two functions, that it
    reaches the highlight module through a DYNAMIC import so the tokenizer is a chunk rather
    than main-chunk weight (DECISION F256 D1), and that every class DECISION F256 D2's mapping
    names has a rule behind it.

    Every assertion reads the COMMENT-STRIPPED source: the component's WHY header names
    `loadDiffLanguageBundle`, `composeHighlightedRuns` and the import specifier in prose, so an
    unstripped guard would be satisfied by the description rather than by the code (finding
    `R-0584`).
    """

    def test_the_two_new_scanners_return_strictly_less_than_the_whole_file(self):
        """The vacuity guard the scoped assertions below stand on.

        A `ts_const_statement` that silently handed back its input would turn the importer
        assertion into the whole-file search finding `R-0725` describes, and an empty entry list
        would make the mapping assertions pass over nothing at all.
        """
        code = strip_ts_comments(COMPONENT.read_text())
        for name in (HIGHLIGHT_IMPORTER_NAME, HIGHLIGHT_KIND_CLASS_NAME):
            statement = ts_const_statement(code, name)
            assert statement, f"the scanner for `const {name}` found nothing at all"
            assert len(statement) < len(code), (
                f"the scanner for `const {name}` returned {len(statement)} characters out of "
                f"{len(code)}, so it is not scoping and every assertion built on it is a "
                f"whole-file search (finding R-0725)"
            )
        entries = highlight_kind_class_entries(code)
        assert entries, (
            f"no `<kind>: <class>` entry was read out of `{HIGHLIGHT_KIND_CLASS_NAME}` in "
            f"{COMPONENT.name}, so the mapping assertions below would be checking an empty list"
        )

    def test_the_component_calls_the_loader_and_the_composition(self):
        code = strip_ts_comments(COMPONENT.read_text())
        for name in HIGHLIGHT_WIRED_CALLS:
            assert f"{name}(" in code, (
                f"{COMPONENT.name} never CALLS {name}. The highlight model and its composition "
                f"are shipped and pinned by their own vitest suite, but a model with no caller "
                f"colours nothing on screen: naming it in an import or a comment is not using it "
                f"({HIGHLIGHT_AUTHORITY})"
            )

    def test_the_highlight_module_is_reached_through_a_dynamic_import(self):
        statement = ts_const_statement(strip_ts_comments(COMPONENT.read_text()), HIGHLIGHT_IMPORTER_NAME)
        assert f"import({HIGHLIGHT_IMPORT_SPECIFIER})" in statement, (
            f"`const {HIGHLIGHT_IMPORTER_NAME}` in {COMPONENT.name} does not reach "
            f"{HIGHLIGHT_MODULE} through a dynamic `import(...)` call. A static import of the "
            f"same module puts every grammar in the main chunk for every operator who never "
            f"opens a diff, which is the whole of what DECISION F256 D1 promised the lazy "
            f"bundles would avoid, and the laziness would then exist only in the name of "
            f"`loadDiffLanguageBundle`"
        )

    def test_every_class_the_kind_mapping_names_has_a_rule_in_the_stylesheet(self):
        code = strip_ts_comments(COMPONENT.read_text())
        defined = css_class_names(COMPONENT_CSS.read_text())
        named = component_class_names(
            ts_const_statement(code, HIGHLIGHT_KIND_CLASS_NAME)
        )
        assert named, (
            f"`{HIGHLIGHT_KIND_CLASS_NAME}` in {COMPONENT.name} asks the CSS module for no class "
            f"at all, so DECISION F256 D2's palette reaches no run on screen"
        )
        missing = sorted({name for name in named if name not in defined})
        assert not missing, (
            f"`{HIGHLIGHT_KIND_CLASS_NAME}` in {COMPONENT.name} names {missing}, which "
            f"{COMPONENT_CSS.name} does not define. A CSS module hands back undefined for such a "
            f"name, so that token kind ships in the row's own colour and no visual review "
            f"reliably catches one uncoloured kind among five ({HIGHLIGHT_AUTHORITY})"
        )

    def test_the_plain_kind_maps_to_the_empty_string(self):
        """Why `plain` may demand no rule, said where it can fail.

        The mapping is total over a closed kind set, so `plain` must be IN it; and it must be
        in it as the empty string, because an unhighlighted run wears no extra class and the
        stylesheet deliberately carries no `.tokPlain`. A `plain` bound to a class name would
        make every ordinary character of every diff line ask for a rule that is not there — and
        would break the promise that an unknown language renders exactly as it did before F256.
        """
        code = strip_ts_comments(COMPONENT.read_text())
        entries = highlight_kind_class_entries(code)
        values = [value for kind, value in entries if kind == HIGHLIGHT_PLAIN_KIND]
        assert len(values) == 1, (
            f"`{HIGHLIGHT_KIND_CLASS_NAME}` in {COMPONENT.name} carries {len(values)} entries for "
            f"the `{HIGHLIGHT_PLAIN_KIND}` kind; exactly one is required, because the mapping is "
            f"total over the closed token set of {HIGHLIGHT_MODULE}"
        )
        assert values[0] == '""', (
            f"`{HIGHLIGHT_KIND_CLASS_NAME}` maps `{HIGHLIGHT_PLAIN_KIND}` to {values[0]!r} rather "
            f"than to the empty string. `{HIGHLIGHT_PLAIN_KIND}` is the kind that must wear no "
            f"class at all — the stylesheet defines no rule for it on purpose, exactly as `ctx` "
            f"wears none in DIFF_LINE_KIND_CLASS — and a class name here would put an undefined "
            f"CSS-module lookup on every ordinary run of every diff line ({HIGHLIGHT_AUTHORITY})"
        )
