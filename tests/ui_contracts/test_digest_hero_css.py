"""Guard: the completion-digest hero card's stylesheet still says what the feature file binds.

`apps/ui/src/components/digest/DigestHeroCard.module.css` is a transcription of the
binding CSS block in the Design section of `docs/roadmap/features/T5_F040.md`. Nothing in
the frontend toolchain re-checks that transcription: `apps/ui/vitest.config.ts` collects
`src/**/*.test.ts` in a NODE environment, so the frontend runner reaches no stylesheet and
no markup, and this repository therefore pins frontend CSS from Python (DECISION F040 D7,
and the same split `tests/ui_contracts/test_diff_surface_css.py` uses for F037).

What a visual review does not reliably catch, and what this guard exists to catch: a card
that lost its `max-width` and now spans the viewport, a radius or a shadow retuned by hand
away from the value the feature file binds, a `var()` naming a design token that
`tokens.css` never defined (which resolves to nothing at all), a second raw colour
smuggled in beside the one DECISION F040 D9 allows, or an animation added to a surface
whose reduced-motion obligation is currently met by carrying no motion whatever.

The assertions below pin VALUES and never selector NAMES. A CSS module has no global
`.digest`, so the transcription chooses its own local class names; a guard that asserted
`.digest` would redden on a faithful rename while a card that had quietly dropped its
`max-width` stayed green. Each binding rule is instead located by the declarations it
carries.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
HERO_CSS = ROOT / "apps" / "ui" / "src" / "components" / "digest" / "DigestHeroCard.module.css"
TOKENS_CSS = ROOT / "apps" / "ui" / "src" / "styles" / "tokens.css"

AUTHORITY = "docs/roadmap/features/T5_F040.md (Design section, 'Hero card, binding CSS core')"

# The three binding rules, transcribed once here so a drift names the authority in its
# message. Keys are the binding block's own selectors; they are used in FAILURE TEXT only,
# never to find a rule in the module.
BINDING_CARD = (
    "max-width:720px",
    "margin:32px auto",
    "padding:28px",
    "border-radius:var(--remedy-radius-lg)",
    "background:var(--remedy-card)",
    "backdrop-filter:blur(14px)",
    "box-shadow:var(--remedy-shadow-soft)",
)
BINDING_HEADLINE = (
    "font:700 22px/1.2 var(--remedy-font-ui)",
    "color:var(--remedy-ink)",
)
BINDING_CTA = (
    "display:inline-flex",
    "padding:10px 18px",
    "border-radius:var(--remedy-radius-pill)",
    "background:var(--remedy-blue)",
    "color:#fff",
    "font-weight:600",
)

# DECISION F040 D9: this ONE literal is transcribed as the feature file writes it, because
# no foreground token exists to replace it and the nearest shipped sibling
# (`RightLivePanel.module.css`) writes the same `background: var(--remedy-blue); color:
# #fff;` pair. The trade is that it must be the sheet's ONLY raw colour, which is a
# stricter property than a quiet token swap would have bought, and which the test below
# is what makes true.
ALLOWED_LITERAL = "#fff"


def _strip_comments(css: str) -> str:
    """Drop `/* ... */` blocks so a value or token named in prose is never read as a rule."""
    return re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)


def _canonical(text: str) -> str:
    """Collapse whitespace and the spacing around `:`, `/` and `,` so a VALUE is pinned, not its layout."""
    collapsed = re.sub(r"\s+", " ", text)
    return re.sub(r"\s*([:/,])\s*", r"\1", collapsed).strip()


def _rules(css: str) -> list[tuple[str, list[str]]]:
    """Return every `selector { ... }` rule as (selector, canonical declarations)."""
    found = []
    for match in re.finditer(r"([^{}]+)\{([^{}]*)\}", _strip_comments(css)):
        selector = _canonical(match.group(1))
        declarations = [
            _canonical(part) for part in match.group(2).split(";") if part.strip()
        ]
        found.append((selector, declarations))
    return found


def _rule_carrying(css: str, required: tuple[str, ...], binding_selector: str) -> tuple[str, list[str]]:
    """Return the single rule that carries EVERY declaration of a binding rule, or fail loudly.

    Located by declarations rather than by name: the module's selector form is the
    transcription's to choose (only the values are bound), so this must survive a rename
    and must not survive a dropped declaration.
    """
    rules = _rules(css)
    assert rules, (
        f"{HERO_CSS.name} parses to no CSS rule at all; the transcription of {AUTHORITY} "
        "cannot be checked against a sheet the reader cannot see"
    )
    matches = [rule for rule in rules if all(item in rule[1] for item in required)]
    if not matches:
        best = max(
            rules,
            key=lambda rule: sum(1 for item in required if item in rule[1]),
        )
        missing = [item for item in required if item not in best[1]]
        raise AssertionError(
            f"No rule in {HERO_CSS.name} carries every declaration the binding "
            f"`{binding_selector}` rule of {AUTHORITY} fixes. The closest rule is "
            f"`{best[0]}`, which is missing {missing}. The values are transcribed, not "
            "designed: changing one here contradicts the feature file rather than "
            "restyling the card."
        )
    assert len(matches) == 1, (
        f"{len(matches)} rules in {HERO_CSS.name} carry the binding `{binding_selector}` "
        f"declarations ({[rule[0] for rule in matches]}); the transcription must land in "
        "exactly one rule, or a reader cannot tell which one the card actually uses"
    )
    return matches[0]


class TestDigestHeroStylesheet:
    def test_the_reader_reaches_the_stylesheet(self):
        """POSITIVE CONTROL: every absence asserted below is a real absence, not a blind read."""
        assert HERO_CSS.is_file(), (
            f"Expected the hero card stylesheet at {HERO_CSS.relative_to(ROOT)}; it carries "
            f"the binding CSS of {AUTHORITY}"
        )
        raw = HERO_CSS.read_text()
        assert raw.strip(), f"{HERO_CSS.name} is empty"
        assert "T5_F040.md" in raw, (
            f"{HERO_CSS.name} does not name its authority in a comment; a reader changing a "
            f"value there must be able to see what they are contradicting ({AUTHORITY})"
        )
        rules = _rules(raw)
        assert len(rules) >= 3, (
            f"{HERO_CSS.name} parses to {len(rules)} rule(s); the binding block fixes three "
            "(the card, the headline and the CTA), so the reader is either looking at the "
            "wrong file or the parse is broken — in which case no absence below means anything"
        )

    def test_the_card_rule_carries_every_binding_value(self):
        selector, declarations = _rule_carrying(
            HERO_CSS.read_text(), BINDING_CARD, ".digest"
        )
        assert "max-width:720px" in declarations, (
            f"`{selector}` lost its `max-width: 720px`; the digest hero is a centred card, "
            f"not a full-bleed region ({AUTHORITY})"
        )

    def test_the_headline_rule_carries_every_binding_value(self):
        selector, declarations = _rule_carrying(
            HERO_CSS.read_text(), BINDING_HEADLINE, ".digest h2"
        )
        assert "font:700 22px/1.2 var(--remedy-font-ui)" in declarations, (
            f"`{selector}` no longer sets the bound headline shorthand; weight, size, "
            f"line-height and the UI family are one declaration in {AUTHORITY}"
        )

    def test_the_cta_rule_carries_every_binding_value(self):
        selector, declarations = _rule_carrying(
            HERO_CSS.read_text(), BINDING_CTA, ".digest .cta"
        )
        assert "background:var(--remedy-blue)" in declarations, (
            f"`{selector}` no longer fills with `var(--remedy-blue)`; the digest's single "
            f"primary action is the one blue thing on the card ({AUTHORITY})"
        )

    def test_every_referenced_token_is_defined_in_the_shipped_sheet(self):
        referenced = set(
            re.findall(r"var\(\s*(--remedy-[\w-]+)", _strip_comments(HERO_CSS.read_text()))
        )
        assert referenced, (
            f"{HERO_CSS.name} references no `--remedy-*` token at all; the binding block "
            f"names seven, so that is itself a drift from {AUTHORITY}"
        )
        defined = set(re.findall(r"(?m)^\s*(--remedy-[\w-]+)\s*:", TOKENS_CSS.read_text()))
        missing = sorted(referenced - defined)
        assert not missing, (
            f"{HERO_CSS.name} references design tokens that {TOKENS_CSS.relative_to(ROOT)} "
            f"does not define: {missing}. Such a `var()` resolves to its fallback, or to "
            f"nothing at all, and no visual review reliably catches it. Tokens found in the "
            f"sheet: {sorted(referenced)}"
        )

    def test_the_cta_white_is_the_only_raw_colour_in_the_sheet(self):
        """DECISION F040 D9's trade, asserted rather than asserted-about.

        One literal is transcribed verbatim because no token exists for it. That is only
        defensible while it stays the ONLY one, so this is the assertion that makes D9's
        "stricter than a quiet swap" claim true.
        """
        css = _strip_comments(HERO_CSS.read_text())
        hexes = re.findall(r"#[0-9a-fA-F]{3,8}\b", css)
        allowed = [value for value in hexes if value.lower() == ALLOWED_LITERAL]
        others = [value for value in hexes if value.lower() != ALLOWED_LITERAL]
        assert not others, (
            f"{HERO_CSS.name} contains raw hex colours beyond the one DECISION F040 D9 "
            f"allows: {others}. Every colour other than the CTA's `{ALLOWED_LITERAL}` must "
            f"be a `var(--remedy-…)` naming a token {TOKENS_CSS.name} defines "
            "(`docs/ui/design_reference/tokens_rules.md`, Forbidden)."
        )
        functional = re.findall(r"\brgba?\(", css)
        assert not functional, (
            f"{HERO_CSS.name} contains {len(functional)} `rgb(`/`rgba(` literal(s); a colour "
            f"here is either the CTA's `{ALLOWED_LITERAL}` or a design token, never a "
            "functional literal"
        )
        assert len(allowed) == 1, (
            f"`{ALLOWED_LITERAL}` occurs {len(allowed)} time(s) in {HERO_CSS.name}; DECISION "
            "F040 D9 permits exactly one, the CTA's foreground, and permits it only because "
            "no `--remedy-*` foreground token exists to carry it"
        )
        carriers = [
            (selector, declarations)
            for selector, declarations in _rules(HERO_CSS.read_text())
            if any(ALLOWED_LITERAL in declaration for declaration in declarations)
        ]
        assert len(carriers) == 1, (
            f"Expected exactly one rule in {HERO_CSS.name} to carry `{ALLOWED_LITERAL}`, "
            f"found {[selector for selector, _ in carriers]}"
        )
        selector, declarations = carriers[0]
        assert f"color:{ALLOWED_LITERAL}" in declarations, (
            f"`{ALLOWED_LITERAL}` in `{selector}` is not the `color` declaration D9 permits; "
            f"its declarations are {declarations}"
        )
        assert "background:var(--remedy-blue)" in declarations, (
            f"`{ALLOWED_LITERAL}` sits in `{selector}`, which is not the CTA rule: DECISION "
            "F040 D9 permits the literal only as the foreground of the "
            "`background: var(--remedy-blue)` action, exactly as the shipped sibling "
            "`apps/ui/src/components/panels/RightLivePanel.module.css` writes it"
        )

    def test_the_sheet_declares_no_motion_and_no_breakpoint(self):
        """`ux_spec.md` §16 is met by carrying no motion at all, and §15 by hard-coding no frame."""
        css = _strip_comments(HERO_CSS.read_text())
        for prop in ("animation", "transition", "transform"):
            found = re.findall(r"(?<![-\w])" + prop + r"[-\w]*\s*:", css)
            assert not found, (
                f"{HERO_CSS.name} declares `{prop}` ({found}). The binding block of "
                f"{AUTHORITY} declares no motion, and `docs/ui/design_reference/ux_spec.md` "
                "§16 is satisfied here by carrying none — `prefers-reduced-motion` is "
                "global-killed in `globals.css` and the Provider, so motion added here has "
                "no reduced-motion answer of its own."
            )
        media = re.findall(r"@media", css)
        assert not media, (
            f"{HERO_CSS.name} declares {len(media)} `@media` block(s). This card is centred "
            "with `max-width` and `margin: auto` and belongs to neither side region, so it "
            "hard-codes no frame and `ux_spec.md` §15 asks nothing of it; a breakpoint "
            "written before the card renders is a guess, not a measurement."
        )
