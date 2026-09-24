"""F020 T001 — the token guard for the brain graph's glyph and state modules.

`apps/ui/src/components/graph/renderers/nodeStates.ts` names design tokens and
never colour values, and `glyphPaths.ts` names no colour at all (T5_F020.md,
Design; `docs/ui/design_reference/tokens_rules.md`, Forbidden). The raw-colour
ratchet in `test_raw_colour_ratchet.py` reads `.css` and `.tsx` files only, so
the `.ts` modules of `renderers/` are guarded here, every one of them. Every value below is parsed from the
files, never copied into this test, except the state colours T5_F020.md fixes,
which are the binding spec this guard exists to hold the tokens to.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
RENDERERS = ROOT / "apps" / "ui" / "src" / "components" / "graph" / "renderers"
NODE_STATES = RENDERERS / "nodeStates.ts"
GLYPH_PATHS = RENDERERS / "glyphPaths.ts"
APP_TOKENS = ROOT / "apps" / "ui" / "src" / "styles" / "tokens.css"
REFERENCE_TOKENS = ROOT / "docs" / "ui" / "design_reference" / "tokens.css"
ASSETS_SPEC = ROOT / "docs" / "ui" / "design_reference" / "assets_spec.md"
CANVAS = ROOT / "apps" / "ui" / "src" / "components" / "graph" / "ForceBrainGraph.tsx"

#: T5_F020.md, "How it fits (binding visual spec, restated)": the colour each
#: of these node states is drawn in.
BINDING_STATE_COLOURS = {
    "open": "#a78bfa",
    "planned": "#ffffff",
    "in_progress": "#4c83ff",
    "pass": "#34c27e",
    "fail": "#ef6363",
}

#: The raw-colour ratchet's own literal pattern.
_LITERAL = re.compile(r"#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?)\(")
_TOKEN = re.compile(r"--remedy-[a-z0-9-]+")


def _declared(css_text: str, name: str) -> str | None:
    match = re.search(rf"^\s*{re.escape(name)}\s*:\s*([^;]+);", css_text, flags=re.M)
    return match.group(1).strip() if match else None


def _fill_token(state: str) -> str:
    match = re.search(
        rf'^  {state}: \{{\n    name: "[^"]*",\n    fillToken: "(--remedy-[a-z0-9-]+)",',
        NODE_STATES.read_text(encoding="utf-8"),
        flags=re.M,
    )
    assert match, f"nodeStates.ts declares no fill token for {state}"
    return match.group(1)


def _header(ts_text: str) -> str:
    lines = []
    for line in ts_text.splitlines():
        if not line.startswith("//"):
            break
        lines.append(line[2:].strip())
    return " ".join(" ".join(lines).split())


def test_every_token_the_state_module_names_resolves_in_the_app_sheet():
    tokens = sorted(set(_TOKEN.findall(NODE_STATES.read_text(encoding="utf-8"))))
    assert tokens, "nodeStates.ts names no token"
    app = APP_TOKENS.read_text(encoding="utf-8")
    missing = [t for t in tokens if _declared(app, t) is None]
    assert not missing, f"tokens nodeStates.ts names that tokens.css never declares: {missing}"


def test_every_token_the_state_module_names_carries_the_reference_value():
    tokens = sorted(set(_TOKEN.findall(NODE_STATES.read_text(encoding="utf-8"))))
    app = APP_TOKENS.read_text(encoding="utf-8")
    reference = REFERENCE_TOKENS.read_text(encoding="utf-8")
    drift = {
        t: (_declared(app, t), _declared(reference, t))
        for t in tokens
        if _declared(app, t) != _declared(reference, t)
    }
    assert not drift, f"(app, reference) values differ: {drift}"


def test_each_binding_state_colour_is_the_value_of_the_token_that_paints_it():
    app = APP_TOKENS.read_text(encoding="utf-8")
    measured = {state: _declared(app, _fill_token(state)) for state in BINDING_STATE_COLOURS}
    assert measured == BINDING_STATE_COLOURS


def test_the_pulse_constant_is_the_pulse_tokens_millisecond_value():
    token = _declared(APP_TOKENS.read_text(encoding="utf-8"), "--remedy-dur-pulse")
    assert token is not None and re.fullmatch(r"\d+ms", token), token
    constant = re.search(r"NODE_PULSE_MS\s*=\s*(\d+)", NODE_STATES.read_text(encoding="utf-8"))
    assert constant, "NODE_PULSE_MS is not declared in nodeStates.ts"
    assert int(constant.group(1)) == int(token[:-2])


def test_no_renderer_module_holds_a_raw_colour_literal():
    modules = sorted(p for p in RENDERERS.glob("*.ts") if not p.name.endswith(".test.ts"))
    assert NODE_STATES in modules and GLYPH_PATHS in modules
    for path in modules:
        found = _LITERAL.findall(path.read_text(encoding="utf-8"))
        assert not found, f"{path.name} holds raw colour literals {found}; name a token instead"


def test_both_module_headers_quote_the_precedence_rule_verbatim():
    spec = " ".join(ASSETS_SPEC.read_text(encoding="utf-8").split())
    match = re.search(r"This is the codified form of .*?feature-file prose\.", spec)
    assert match, "assets_spec.md §4 no longer states its precedence rule"
    for path in (NODE_STATES, GLYPH_PATHS):
        assert match.group(0) in _header(path.read_text(encoding="utf-8")), (
            f"{path.name}'s header does not quote assets_spec.md §4's precedence rule verbatim"
        )


def test_the_canvas_paints_every_non_core_kind_through_the_glyph_painter():
    src = CANVAS.read_text(encoding="utf-8")
    table = re.search(r"const NODE_PAINTERS: Record<NodeKind, NodePainter> = \{\n(.*?)\n\};", src, flags=re.S)
    assert table, "ForceBrainGraph.tsx no longer declares NODE_PAINTERS"
    entries = dict(re.findall(r"^  (\w+): (\w+),$", table.group(1), flags=re.M))
    assert entries.pop("job_core") == "paintCoreNode"
    assert set(entries.values()) == {"paintGlyphNode"}, entries
    assert "paintBrainNode(ctx, node, { palette, zoom: globalScale" in src
    assert "useMemo(() => readDocumentPalette(), [])" in src


def test_the_canvas_holds_no_state_colour_of_its_own():
    src = CANVAS.read_text(encoding="utf-8").lower()
    for name in ("STATE_FILL", "STATE_RING"):
        assert name.lower() not in src, f"ForceBrainGraph.tsx still declares {name}"
    app = APP_TOKENS.read_text(encoding="utf-8")
    for state in BINDING_STATE_COLOURS:
        value = _declared(app, _fill_token(state))
        if value != "#ffffff":
            assert value.lower() not in src, f"ForceBrainGraph.tsx paints {state}'s colour {value} itself"
