"""R-0755 — the raw-colour rule in `tokens_rules.md` has a gate, and it is this one.

`docs/ui/design_reference/tokens_rules.md` (Forbidden) forbids raw hex/rgb(a)/hsl(a)
colour literals in component CSS and TSX. It used to say a stylelint gate enforced
that; none ever existed. F273 T006 amended the rule to state what is true: the
canvas/SVG paint and MUI-theme files named in `CARVE_OUT` may carry literals, and
every other file's literals are pre-existing debt pinned per file in `RATCHET`.

The ratchet is EXACT on purpose. `<=` would let a pin go stale after a clean-up and
then silently re-admit the colours it no longer counts; equality forces whoever
removes a literal to lower the pin in the same change, so the pins only shrink.
A file absent from both tables must hold zero literals.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SRC = ROOT / "apps" / "ui" / "src"
RULES = ROOT / "docs" / "ui" / "design_reference" / "tokens_rules.md"

#: The token sheet itself: the one place literals are the point.
TOKEN_SHEET = "styles/tokens.css"

#: Files whose literals are sanctioned by tokens_rules.md's carve-out: a 2D canvas
#: context and SVG presentation attributes do not resolve `var()`, and MUI's
#: `createTheme` computes on colour values. Grows only with that document.
CARVE_OUT = frozenset({
    "components/graph/ForceBrainGraph.tsx",
    "components/graph/BrainGraphCanvas.tsx",
    "components/icons/CodeOrbIcon.tsx",
    "components/icons/NetworkLogoIcon.tsx",
    "main.tsx",
})

#: Measured at db9a05cc: raw colour literals per file (var() fallbacks included —
#: a fallback literal is still a second copy of a palette value). Only shrinks.
RATCHET = {
    "RemedyApp.tsx": 1,
    "components/command/CommandBar.module.css": 1,
    "components/detail/DetailPopover.module.css": 15,
    "components/detail/DetailPopover.tsx": 4,
    "components/diff/DiffView.module.css": 14,
    "components/digest/DigestHeroCard.module.css": 1,
    "components/graph/BrainGraphCanvas.module.css": 19,
    "components/graph/BrainGraphStage.module.css": 5,
    "components/graph/ForceBrainGraph.module.css": 2,
    "components/graph/GraphFilterChips.module.css": 4,
    "components/layers/LayerSwitcher.module.css": 5,
    "components/metrics/TopMetricsBar.module.css": 2,
    "components/panels/RightLivePanel.module.css": 14,
    "components/pipeline/Pipeline.module.css": 40,
    "components/prompt/PromptTracePanel.module.css": 17,
    "components/rail/RemedyLogo.module.css": 3,
    "components/rail/SideIconDock.module.css": 10,
    "components/shell/DegradedBanner.module.css": 3,
    "components/shell/RemedyShell.module.css": 6,
    "components/timeline/PhaseTimeline.module.css": 10,
    "styles/globals.css": 6,
}

_LITERAL = re.compile(r"#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?)\(")


def _strip_comments(text: str, suffix: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    if suffix == ".tsx":
        text = re.sub(r"(?m)(^|[^:\"'`])//.*$", r"\1", text)
    return text


def _measure() -> dict[str, int]:
    counts = {}
    for path in sorted(SRC.rglob("*")):
        if path.suffix not in (".css", ".tsx") or path.name.endswith(".test.tsx"):
            continue
        rel = path.relative_to(SRC).as_posix()
        if rel == TOKEN_SHEET or rel in CARVE_OUT:
            continue
        found = len(_LITERAL.findall(_strip_comments(path.read_text(encoding="utf-8"), path.suffix)))
        if found:
            counts[rel] = found
    return counts


def test_raw_colour_literals_match_the_ratchet_exactly():
    measured = _measure()
    new = {f: n for f, n in measured.items() if f not in RATCHET}
    assert not new, (
        f"raw colour literals in files outside the ratchet: {new}. Use a "
        "`var(--remedy-…)` token (tokens_rules.md, Forbidden)"
    )
    drift = {f: (RATCHET[f], measured.get(f, 0)) for f in RATCHET if measured.get(f, 0) != RATCHET[f]}
    assert not drift, (
        f"(pinned, measured) differs: {drift}. A rise is a new literal — use a token; "
        "a fall is a clean-up — lower the pin (drop the entry at zero) in the same change"
    )


def test_the_carve_out_names_real_files_the_rule_names():
    rules = RULES.read_text(encoding="utf-8")
    for rel in sorted(CARVE_OUT):
        assert (SRC / rel).is_file(), f"carve-out names a missing file: {rel}"
        assert Path(rel).name in rules, f"{rel} is carved out here but not in {RULES.name}"
    assert "test_raw_colour_ratchet.py" in rules, f"{RULES.name} must name this gate"


def test_the_literal_pattern_sees_every_colour_form():
    sample = "a{color:#fff;b:#12345678;c:rgb(1,2,3);d:rgba(0,0,0,.1);e:hsl(1,2%,3%);f:hsla(1,2%,3%,.5)}"
    assert len(_LITERAL.findall(sample)) == 6
