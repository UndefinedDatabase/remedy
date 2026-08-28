"""Guard: the diff surface stylesheet still says what the feature file binds it to say.

`apps/ui/src/components/diff/DiffView.module.css` is a transcription of the binding CSS
block in the Design section of `docs/roadmap/features/T5_F037.md`. Nothing in the frontend
toolchain re-checks that transcription, and a visual review does not reliably catch a
column track that lost a gutter, a changed-line background that was copy-pasted onto both
sides, a ligature setting that drifted out of one rule, or a `var()` naming a design token
that was never defined. This guard prevents each of those from landing silently.

It reads files as text and imports nothing from `apps/`: `apps/ui/vitest.config.ts` collects
`src/**/*.test.ts` in a NODE environment, so the frontend runner reaches no stylesheet and no
markup whatever its availability, which is why the conformance of this stylesheet is pinned
from Python, which is how this repository already pins frontend CSS.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DIFF_CSS = ROOT / "apps" / "ui" / "src" / "components" / "diff" / "DiffView.module.css"
TOKENS_CSS = ROOT / "apps" / "ui" / "src" / "styles" / "tokens.css"

# The binding values, transcribed once here so a drift names the authority in its message.
BINDING_TRACKS = "56px 56px 1fr"
BINDING_ADD_BG = "rgba(56,217,169,.12)"
BINDING_DEL_BG = "rgba(247,103,7,.10)"
LIGATURES_OFF = 'font-feature-settings: "liga" 0'
AUTHORITY = "docs/roadmap/features/T5_F037.md (Design section, binding CSS; amendment A4)"


def _strip_comments(css: str) -> str:
    """Drop `/* ... */` blocks so a token or value named in prose is never read as a rule."""
    return re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)


def _rule_body(css: str, selector: str) -> str:
    """Return the declaration block of exactly `selector`, or fail loudly if it is absent."""
    match = re.search(
        r"(?m)^\s*" + re.escape(selector) + r"\s*\{([^}]*)\}",
        _strip_comments(css),
    )
    assert match, f"No `{selector}` rule in {DIFF_CSS.name}; it is required by {AUTHORITY}"
    return match.group(1)


def _declaration(body: str, prop: str) -> str:
    """Return one declaration's value from a rule body, whitespace-normalised."""
    match = re.search(r"(?<![-\w])" + re.escape(prop) + r"\s*:\s*([^;]+);", body)
    assert match, f"No `{prop}` declaration in rule body: {body.strip()!r}"
    return re.sub(r"\s+", " ", match.group(1)).strip()


def _normalise(body: str) -> str:
    """Collapse runs of whitespace and the spacing around `:` so a declaration is pinned, not its layout."""
    return re.sub(r"\s*:\s*", ": ", re.sub(r"\s+", " ", body)).strip()


def _declaration_offset(body: str, prop: str) -> int:
    """Return the offset at which `prop`'s declaration begins in a rule body, or -1 when it is absent."""
    match = re.search(r"(?<![-\w])" + re.escape(prop) + r"\s*:", body)
    return match.start() if match else -1


def _font_shorthand_after(body: str, offset: int) -> bool:
    """Report whether a `font` SHORTHAND declaration begins after `offset` in this rule body.

    The shorthand resets `font-feature-settings` to its initial value, so a `"liga" 0`
    declaration sitting ABOVE one is dead and the rule composes ligatures anyway.
    """
    return any(match.start() > offset for match in re.finditer(r"(?<![-\w])font\s*:", body))


class TestDiffSurfaceStylesheet:
    def test_stylesheet_exists(self):
        assert DIFF_CSS.is_file(), (
            f"Expected the diff surface stylesheet at {DIFF_CSS.relative_to(ROOT)}; "
            f"it carries the binding CSS of {AUTHORITY}"
        )

    def test_diff_line_is_a_three_column_grid(self):
        body = _rule_body(DIFF_CSS.read_text(), ".diffLine")
        assert _declaration(body, "display") == "grid", (
            "`.diffLine` must lay out as a grid: the two gutters and the code column are "
            "positioned by track, not by flow"
        )
        tracks = _declaration(body, "grid-template-columns")
        assert tracks == BINDING_TRACKS, (
            f"`.diffLine` track list is {tracks!r}, expected {BINDING_TRACKS!r} per {AUTHORITY}. "
            "Two 56px gutters carry the old and new line numbers; dropping one silently "
            "collapses a column of the diff."
        )

    def test_diff_line_font_is_the_binding_mono_size(self):
        body = _rule_body(DIFF_CSS.read_text(), ".diffLine")
        font = _declaration(body, "font").replace(" /", "/").replace("/ ", "/")
        assert "12.5px/1.6" in font, (
            f"`.diffLine` font shorthand is {font!r}; the binding CSS fixes size 12.5px over "
            f"line-height 1.6 ({AUTHORITY})"
        )
        assert "--remedy-font-mono" in font, (
            f"`.diffLine` font shorthand is {font!r}; it must name the canonical mono token "
            "`--remedy-font-mono` (DECISION F037 D4), not a literal family stack"
        )

    def test_added_and_removed_lines_are_two_different_colours(self):
        css = DIFF_CSS.read_text()
        add_bg = _declaration(_rule_body(css, ".diffLine.add"), "background")
        del_bg = _declaration(_rule_body(css, ".diffLine.del"), "background")
        assert add_bg == BINDING_ADD_BG, (
            f"`.diffLine.add` background is {add_bg!r}, expected {BINDING_ADD_BG!r} per {AUTHORITY}"
        )
        assert del_bg == BINDING_DEL_BG, (
            f"`.diffLine.del` background is {del_bg!r}, expected {BINDING_DEL_BG!r} per {AUTHORITY}"
        )
        assert add_bg != del_bg, (
            f"Added and removed lines share one background ({add_bg!r}); a diff whose two "
            "sides render alike is unreadable, which is what this assertion exists to catch"
        )

    def test_ligatures_are_off_in_the_diff_line_rule(self):
        body = _normalise(_rule_body(DIFF_CSS.read_text(), ".diffLine"))
        assert LIGATURES_OFF in body, (
            f"`.diffLine` does not declare `{LIGATURES_OFF}`; a `!=` or a `->` would render as "
            "one composed glyph instead of the characters really in the file "
            "(assets_spec.md section 2, ligatures OFF on diff surfaces). "
            "Note the `font` shorthand resets this property, so the declaration must follow it."
        )

    def test_ligatures_are_off_in_the_hunk_head_rule(self):
        body = _normalise(_rule_body(DIFF_CSS.read_text(), ".hunkHead"))
        assert LIGATURES_OFF in body, (
            f"`.hunkHead` does not declare `{LIGATURES_OFF}`; the hunk header renders `@@ -1,4 +1,6 @@`, "
            "whose characters must not compose either "
            "(assets_spec.md section 2, ligatures OFF on diff surfaces)"
        )

    def test_no_font_shorthand_follows_the_ligature_declaration(self):
        css = DIFF_CSS.read_text()
        for selector in (".diffLine", ".hunkHead"):
            body = _normalise(_rule_body(css, selector))
            offset = _declaration_offset(body, "font-feature-settings")
            assert offset >= 0, (
                f"`{selector}` declares no `font-feature-settings` at all, so there is no ligature "
                f"setting left for this rule to keep off ({AUTHORITY})"
            )
            assert not _font_shorthand_after(body, offset), (
                f"`{selector}` places a `font` shorthand AFTER its `{LIGATURES_OFF}` declaration; the "
                "shorthand resets that property, so ligatures come back to the diff surface and a `!=` "
                "or a `->` renders as one composed glyph instead of the characters really in the file "
                "(assets_spec.md section 2, ligatures OFF on diff surfaces). Declare the shorthand "
                "first and the feature settings after it."
            )

    def test_every_referenced_token_is_defined_in_the_shipped_sheet(self):
        referenced = set(re.findall(r"var\(\s*(--remedy-[\w-]+)", _strip_comments(DIFF_CSS.read_text())))
        assert referenced, "The stylesheet references no `--remedy-*` token at all; that is itself a drift"
        defined = set(re.findall(r"(?m)^\s*(--remedy-[\w-]+)\s*:", TOKENS_CSS.read_text()))
        missing = sorted(referenced - defined)
        assert not missing, (
            f"{DIFF_CSS.name} references design tokens that {TOKENS_CSS.relative_to(ROOT)} does not "
            f"define: {missing}. Such a `var()` resolves to its fallback, or to nothing at all, and no "
            "visual review reliably catches it."
        )
