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
VITEST_AUTHORITY = (
    "apps/ui/vitest.config.ts (environment: node, include: src/**/*.test.ts), "
    "DECISION F031 D5 and DECISION F037 D8"
)
CSS_AUTHORITY = (
    "docs/roadmap/features/T5_F037.md (Design section, binding CSS; amendments A4 and A5)"
)

# The four rules the component must CALL rather than carry. Each is a decidable rule that
# lives in the model module, where the node-environment vitest config really runs it.
DELEGATED_RULES = (
    "buildDiffRowModels",
    "defaultCollapsedHunkIds",
    "toggleHunkCollapse",
    "splitLineIntoIntralineSegments",
)

# Spellings of a rule REIMPLEMENTED in markup. The collapse threshold's literal is declared
# exactly once, in the model module; a `.length` compared against anything is that rule
# arriving under another name; a sort is the file order the parser already fixed.
REIMPLEMENTED_RULE_SPELLINGS = ("200", ".length >", "sort(")


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
                f"and its hidden-line counts are buildDiffRowModels' answer, and the envelope's "
                f"file order is the parser's — each of those transcribed here is a rule "
                f"{VITEST_AUTHORITY} can no longer execute"
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
