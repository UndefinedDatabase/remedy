"""Contract tests for the COST metric's render.

DECISION F022 D5 rules that the metric is a FIELD LOOKUP over `CostMetricView`
and that its threshold is never carried by colour alone. This repository has no
DOM environment and the vitest config collects `src/**/*.test.ts` only, so the
component is gated the way every other component here is gated — by reading its
source. Every assertion runs against COMMENT-STRIPPED source, because a guard
that counted a token inside a comment would be satisfied by the prose about the
code rather than by the code (finding R-0584).
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
UI_SRC = REPO_ROOT / "apps" / "ui" / "src"
BAR = UI_SRC / "components" / "metrics" / "TopMetricsBar.tsx"
GLYPHS = UI_SRC / "components" / "icons" / "RemedyGlyphs.tsx"
SHEET = UI_SRC / "components" / "metrics" / "TopMetricsBar.module.css"

#: The two banded levels. `normal` is deliberately absent: it is the state that
#: needs no extra signal, so the never-colour-alone rule has nothing to say
#: about it.
BANDED_LEVELS = ("warn", "exceeded")

#: Every icon the bar mapped before the cost metric existed, so a regression
#: that dropped one while adding the eighth would be seen here.
EXISTING_ICON_ENTRIES = (
    ("open", "ClipboardGlyph"),
    ("planned", "CalendarGlyph"),
    ("done", "TaskDoneGlyph"),
    ("progress", "ChartGlyph"),
    ("tests", "FlaskGlyph"),
    ("proof", "ShieldCheckGlyph"),
    ("tokens", "TokenGlyph"),
)


def strip_ts_comments(text: str) -> str:
    """Drop // and /* */ comments. These files contain no string literal holding
    either marker, which is what lets so plain a scanner be trustworthy here."""
    out: list[str] = []
    i, n = 0, len(text)
    while i < n:
        pair = text[i:i + 2]
        if pair == "//":
            nl = text.find("\n", i)
            i = n if nl == -1 else nl
        elif pair == "/*":
            end = text.find("*/", i + 2)
            i = n if end == -1 else end + 2
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def blank_quoted_literals(text: str) -> str:
    """Empty every single- and double-quoted literal, keeping its quotes, so an
    import specifier's path separator is not read as arithmetic. TEMPLATE
    literals are left intact on purpose: this component's templates carry
    expressions, and blanking them would HIDE a division rather than exclude
    one."""
    out: list[str] = []
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch in "\"'":
            j = i + 1
            while j < n and text[j] != ch:
                j += 2 if text[j] == "\\" else 1
            out.append(ch + ch)
            i = j + 1
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def code_of(path: Path) -> str:
    """The comment-stripped source, which is what every assertion below reads."""
    return strip_ts_comments(path.read_text())


def arithmetic_of(text: str) -> str:
    """The source with comments, quoted literals and JSX tag punctuation gone,
    leaving only operators the component actually evaluates."""
    return blank_quoted_literals(strip_ts_comments(text)).replace("</", "").replace("/>", "")


def css_rules_naming(marks: tuple[str, ...]) -> list[tuple[str, str]]:
    """Every (selector, body) pair in the stylesheet whose selector names one of
    `marks`. Selectors are compared case-insensitively so `.costWarn` is found
    by `cost`."""
    blocks = re.findall(r"([^{}]*)\{([^{}]*)\}", SHEET.read_text())
    return [
        (selector.strip(), body)
        for selector, body in blocks
        if any(mark.lower() in selector.lower() for mark in marks)
    ]


class TestCommentStripping:
    def test_stripper_removes_a_comment_the_component_really_carries(self):
        raw = BAR.read_text()
        assert "// The cost view has already decided its own text" in raw, (
            "the cost arm must keep its WHY comment"
        )
        assert "The cost view has already decided its own text" not in strip_ts_comments(raw), (
            "stripper must remove it"
        )

    def test_stripper_leaves_the_code_around_the_comment(self):
        code = strip_ts_comments(BAR.read_text())
        assert "export function TopMetricsBar(" in code, (
            "a stripper that ate the code as well would make every assertion below vacuous"
        )


class TestTheCoinGlyphIsWired:
    def test_the_glyph_is_defined_under_its_own_name(self):
        code = code_of(GLYPHS)
        assert "export function CoinGlyph(" in code, (
            "assets_spec.md line 179 names the budget/cost mark, so the glyph is "
            "conformance to the asset authority rather than a new asset"
        )
        assert 'viewBox="0 0 16 16"' in code.split("export function CoinGlyph(")[1], (
            "the coin is drawn in the 16 DOM box the same spec line states"
        )

    def test_the_bar_imports_it_and_maps_it_to_cost(self):
        code = code_of(BAR)
        imports = code.split("const iconByKey")[0]
        assert "CoinGlyph" in imports, "the glyph must be imported, not redeclared"
        assert "cost: CoinGlyph," in code, "the cost key must resolve to the coin"


class TestTheMarkerIsTheBasisNotTheThreshold:
    def test_the_marker_is_named_once_and_rendered_off_estimated(self):
        code = code_of(BAR)
        assert 'const ESTIMATE_MARK = "~";' in code, (
            "the marker is a named constant so its every use is greppable"
        )
        assert (
            "{m.cost?.estimated && <span className={styles.estimateMark}>{ESTIMATE_MARK}</span>}"
            in code
        ), "the marker renders when and only when the view says the figure is an estimate"

    def test_no_expression_joins_the_marker_to_a_level(self):
        code = code_of(BAR)
        marker_lines = [
            line for line in code.splitlines()
            if "~" in line or "ESTIMATE_MARK" in line
        ]
        assert marker_lines, "the marker was not found at all, so this guard would be vacuous"
        for line in marker_lines:
            for level in BANDED_LEVELS:
                assert level not in line, (
                    f"a marker driven from {level!r} would claim the figure had become an "
                    f"estimate, which is a false statement about provenance: {line.strip()!r}"
                )
            assert ".level" not in line, (
                f"the marker must not read the threshold band at all: {line.strip()!r}"
            )


class TestNoFakeDenominatorAtTheRenderLayer:
    def test_the_track_is_guarded_on_a_real_fill(self):
        code = code_of(BAR)
        assert "m.cost && m.cost.fill !== null && (" in code, (
            "a limitless job has no denominator, so the track must not render at all "
            "rather than render an invented one"
        )

    def test_the_source_supplies_no_default_for_the_fill(self):
        code = code_of(BAR)
        for default in ("?? 0", "|| 0", "fill ??", "fill ||", "fill ?", "fill:"):
            assert default not in code, (
                f"{default!r} would turn an absent fill into a rendered zero"
            )


class TestTheThresholdIsNeverColourAlone:
    def test_each_banded_level_reaches_the_accessible_name(self):
        code = code_of(BAR)
        table = code.split("const costLevelPhrase")[1].split("}")[0]
        for level in BANDED_LEVELS:
            phrase = re.search(rf"^\s*{level}: \"([^\"]+)\",", table, re.M)
            assert phrase is not None, f"{level} carries no phrase in words"
            assert phrase.group(1).strip(), f"{level}'s phrase is empty"
        assert "costLevelPhrase[m.cost.level" in code, (
            "the phrase table must be read from the view's own level"
        )
        assert "aria-label={`${m.label}: ${ariaValue}${costPhrase}`}" in code, (
            "the phrase must reach the accessible name, or it is decoration"
        )

    def test_each_banded_level_has_a_non_colour_signal_in_the_sheet(self):
        for level in BANDED_LEVELS:
            selector = f".cost{level.capitalize()} > span"
            rules = css_rules_naming((selector,))
            assert rules, f"{selector} has no rule at all"
            body = "".join(body for _, body in rules)
            assert "repeating-linear-gradient" in body, (
                f"{selector} signals its state by colour alone, which ux_spec.md §14 forbids"
            )


class TestTheComponentDoesNoArithmeticButTheClamp:
    def test_the_component_divides_nothing(self):
        assert "/" not in arithmetic_of(BAR.read_text()), (
            "every ratio the cost metric shows is already decided in costMetric.ts "
            "(DECISION F022 D5 clause 1)"
        )

    def test_the_division_scan_can_actually_see_a_division(self):
        salted = arithmetic_of("const fakeRatio = spent / limit;\n" + BAR.read_text())
        assert "/" in salted, "the scan must be able to fail, or its green means nothing"

    def test_the_cost_branch_carries_only_the_clamps_numbers(self):
        code = blank_quoted_literals(code_of(BAR))
        literals: set[str] = set()
        for line in code.splitlines():
            if "cost" not in line.lower():
                continue
            literals.update(re.findall(r"(?<![A-Za-z_$.\d])\d+(?:\.\d+)?", line))
        assert literals, "no cost line was found, so this guard would be vacuous"
        assert literals == {"0", "100"}, (
            f"the clamp's 0 and 100 are the only numbers the cost branch may name: "
            f"{sorted(literals)}"
        )


class TestTheOtherSevenMetricsAreUntouched:
    def test_every_existing_icon_entry_is_still_named(self):
        code = code_of(BAR)
        for key, glyph in EXISTING_ICON_ENTRIES:
            assert f"{key}: {glyph}," in code, f"the {key} metric lost its icon"

    def test_the_token_tooltip_keeps_its_own_testid(self):
        code = code_of(BAR)
        assert 'data-testid="token-tooltip"' in code, "the token tooltip's testid is a contract"
        assert 'data-testid="cost-tooltip"' in code, "the cost rows get a testid of their own"

    def test_the_tokens_caption_still_renders_off_is_tokens(self):
        code = code_of(BAR)
        assert (
            "{isTokens && main !== EM_DASH && <div className={styles.estimated}>estimated</div>}"
            in code
        ), "the tokens metric's own estimated caption is unrelated to the cost marker"

    def test_the_progress_track_still_renders_off_its_own_key(self):
        code = code_of(BAR)
        assert '{m.key === "progress" && (' in code, "the progress track keeps its own guard"
        assert "className={styles.progressTrack}" in code, "and its own class"


class TestTheStylesheetUsesNamedTokens:
    def test_the_cost_rules_name_the_threshold_tokens(self):
        body = "".join(body for _, body in css_rules_naming(("cost",)))
        assert body, "no cost rule was found, so this guard would be vacuous"
        for token in ("--remedy-blue-100", "--remedy-orange-400", "--remedy-red-500"):
            assert token in body, f"{token} is the primitive both sheets already carry"

    def test_the_new_rules_carry_no_literal_hex(self):
        for selector, body in css_rules_naming(("cost", "estimateMark")):
            assert not re.search(r"#[0-9a-fA-F]{3,8}", body), (
                f"{selector} names a literal hex instead of a token"
            )
