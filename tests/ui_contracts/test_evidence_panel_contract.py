"""F023 T003 — the L3 evidence panel keeps T5_F023.md's binding CSS and its tokens resolve.

`EvidencePanel.tsx` is the side panel semantic zoom opens at L3 for the focused run, with the
tabs diff, prompt trace and chat; `BrainGraphStage.tsx` mounts it at L3 and the run detail's
Open diff and Why open it on their tab (DECISION F023 D5). The feature file writes the panel's
CSS core as binding; its one raw colour became the token `--remedy-shadow-panel`, and the
layers and the slide-in read the reference's tokens, transcribed into the app sheet. The
vitest environment renders no `.tsx` and reads no CSS, so both are pinned from source here.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
GRAPH = ROOT / "apps" / "ui" / "src" / "components" / "graph"
PANEL = GRAPH / "EvidencePanel.tsx"
PANEL_CSS = GRAPH / "EvidencePanel.module.css"
STAGE = GRAPH / "BrainGraphStage.tsx"
POPOVER = GRAPH / "RunDetailPopover.tsx"
APP_TOKENS = ROOT / "apps" / "ui" / "src" / "styles" / "tokens.css"
REF_TOKENS = ROOT / "docs" / "ui" / "design_reference" / "tokens.css"
FEATURE = ROOT / "docs" / "roadmap" / "features" / "T5_F023.md"

# The declarations of the binding core that ship exactly as the feature file writes them,
# with whitespace removed on both sides before they are compared.
BINDING_KEPT = (
    "position:fixed", "right:0", "top:0", "bottom:0", "width:min(560px,44vw)",
    "background:var(--remedy-bg-2)", "border-left:1pxsolidvar(--remedy-line)",
    "display:flex", "flex-direction:column",
)


def _src(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _squash(text: str) -> str:
    return re.sub(r"\s+", "", text)


def _token(sheet: Path, name: str) -> str:
    match = re.search(rf"{re.escape(name)}:\s*([^;]+);", _src(sheet))
    assert match, f"{sheet.name} does not declare {name}"
    return match.group(1).strip()


def test_the_panel_keeps_the_binding_core_and_tokenises_only_its_shadow_layer_and_motion():
    feature = _squash(_src(FEATURE))
    assert "box-shadow:-18px040pxrgba(37,50,79,.08)" in feature
    assert "animation:slideIn.22sease" in feature
    rule = _squash(_src(PANEL_CSS).split(".panel {", 1)[1].split("}", 1)[0])
    for declaration in BINDING_KEPT:
        assert declaration in rule, f".panel lost the binding `{declaration}`"
    assert "box-shadow:var(--remedy-shadow-panel)" in rule
    assert "animation:slideInvar(--remedy-dur-base)var(--remedy-ease-soft)" in rule
    assert "z-index:var(--remedy-z-overlay)" in rule


def test_the_new_tokens_carry_the_values_the_binding_css_and_the_reference_give():
    assert _token(APP_TOKENS, "--remedy-shadow-panel") == "-18px 0 40px rgba(37, 50, 79, 0.08)"
    assert _token(REF_TOKENS, "--remedy-shadow-panel") == _token(APP_TOKENS, "--remedy-shadow-panel")
    assert _token(APP_TOKENS, "--remedy-dur-base") == "220ms"
    for name in ("--remedy-dur-base", "--remedy-z-stage-ui", "--remedy-z-popover", "--remedy-z-overlay"):
        assert _token(APP_TOKENS, name) == _token(REF_TOKENS, name).split("/*")[0].strip(), name


def test_zooms_surfaces_sit_on_layer_tokens_never_a_number():
    for name, layer in (("ZoomBreadcrumbs.module.css", "--remedy-z-stage-ui"),
                        ("RunDetailPopover.module.css", "--remedy-z-popover"),
                        ("EvidencePanel.module.css", "--remedy-z-overlay")):
        css = _src(GRAPH / name)
        assert re.findall(r"z-index:\s*([^;]+);", css) == [f"var({layer})"], name


def test_reduced_motion_drops_the_slide_in():
    css = _squash(_src(PANEL_CSS))
    assert "@media(prefers-reduced-motion:reduce){.panel{animation:none;}}" in css


def test_only_the_open_tab_loads_and_the_panel_is_not_a_dialog():
    src = _src(PANEL)
    assert '{tab === "diff" && <DiffTab jobId={jobId} token={token} taskId={detail.taskId} />}' in src
    assert '{tab === "prompt" && <PromptTracePanel prompts={prompts} selectedPromptId={detail.promptItemId} />}' in src
    assert '{tab === "chat" && <p className={styles.note}>{EVIDENCE_CHAT_NOT_YET}</p>}' in src
    assert "if (!cancelled) setLoaded({ taskId, envelope });" in src
    assert "loaded !== null && loaded.taskId === taskId ? loaded.envelope : null" in src
    assert 'role="dialog"' not in src


def test_the_stage_opens_the_panel_at_l3_and_the_run_detail_at_l2_only():
    src = _src(STAGE)
    assert "{focusedRun && zoom.state.level === 2 && (" in src
    assert "{focusedRun && zoom.state.level === 3 && zoom.state.tab !== null && (" in src
    panel = src[src.index("<EvidencePanel"):]
    panel = panel[:panel.index("/>")]
    for prop in ("tab={zoom.state.tab}", 'onTab={(tab) => zoom.dispatch({ type: "open_evidence", tab })}',
                 'onClose={() => zoom.dispatch({ type: "escape" })}', "token={serverToken}"):
        assert prop in panel, f"<EvidencePanel> lacks {prop}"


def test_the_run_details_diff_and_why_open_the_panel_on_their_tab():
    src = _src(POPOVER)
    assert 'onClick={() => onOpenEvidence("diff")}>Open diff</button>' in src
    assert 'onClick={() => { if (detail.promptItemId !== null) onOpenEvidence("prompt"); }}' in src
