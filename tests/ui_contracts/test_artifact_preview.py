"""F041 T003's results panel, pinned as source (DECISION F041 D5).

None of `ArtifactsPanel.tsx`, `ArtifactLightbox.tsx` or `AppPreviewCard.tsx` can be rendered by
this repository's vitest config (no DOM harness exists for it — DECISION F031 D5, the reason
`TourOverlay.tsx` and `StoryPanel.tsx` are pinned this same way, `test_tour_overlay_contract.py`
and `test_story_panel_contract.py`). Assertions run against COMMENT-STRIPPED source, or prose
above a definition would satisfy a guard meant for the code (finding R-0584).
"""
from __future__ import annotations

import re
from pathlib import Path

from tests.ui_contracts.test_brain_stream_ring import strip_ts_comments

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
UI_SRC = REPO_ROOT / "apps" / "ui" / "src"
ARTIFACTS_DIR = UI_SRC / "components" / "artifacts"
PANEL = ARTIFACTS_DIR / "ArtifactsPanel.tsx"
PANEL_CSS = ARTIFACTS_DIR / "ArtifactsPanel.module.css"
LIGHTBOX = ARTIFACTS_DIR / "ArtifactLightbox.tsx"
LIGHTBOX_CSS = ARTIFACTS_DIR / "ArtifactLightbox.module.css"
CARD = ARTIFACTS_DIR / "AppPreviewCard.tsx"
PURE = UI_SRC / "api" / "artifactPreview.ts"
PREVIEW_SEND = UI_SRC / "api" / "previewSend.ts"
SHELL = UI_SRC / "components" / "shell" / "RemedyShell.tsx"
RIGHT_PANEL = UI_SRC / "components" / "panels" / "RightLivePanel.tsx"

#: `artifactPreview.ts`'s own purity words (S1): none of these may occur in that file.
PURITY_WORDS = ("window.", "document.", "fetch(", "Date", "Math.random", "React")

_RAW_COLOUR = re.compile(r"#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?)\(")


def _source(path: Path) -> str:
    return strip_ts_comments(path.read_text(encoding="utf-8"))


def test_dangerously_set_inner_html_occurs_exactly_once_in_apps_ui_src():
    total = 0
    found_at: Path | None = None
    found_source = ""
    for path in sorted(UI_SRC.rglob("*")):
        if path.suffix not in (".ts", ".tsx"):
            continue
        source = _source(path)
        count = source.count("dangerouslySetInnerHTML")
        if count:
            total += count
            found_at = path
            found_source = source
    assert total == 1, f"expected exactly one dangerouslySetInnerHTML site under apps/ui/src, found {total}"
    assert found_at == PANEL, f"the one dangerouslySetInnerHTML site must be ArtifactsPanel.tsx, found {found_at}"
    block = found_source[found_source.index("dangerouslySetInnerHTML"):]
    block = block[:block.index("}}") + 2]
    assert "readmeCockpitHtml(" in block, "the dangerouslySetInnerHTML site must read readmeCockpitHtml("


def test_no_component_of_the_directory_opens_a_socket_of_its_own():
    for path in (PANEL, LIGHTBOX, CARD):
        assert "fetch(" not in _source(path), (
            f"{path.name} must reach a door only through remedyApi.ts or previewSend.ts"
        )


def test_the_panel_is_a_region_portaled_to_the_document_body():
    source = _source(PANEL)
    assert "createPortal(" in source
    assert "document.body" in source
    assert 'role="region"' in source
    assert 'data-ui="artifacts-panel"' in source


def test_the_lightbox_is_a_dialog_portaled_to_the_document_body():
    source = _source(LIGHTBOX)
    assert "createPortal(" in source
    assert 'role="dialog"' in source
    assert 'aria-modal="true"' in source
    assert 'data-ui="artifact-lightbox"' in source


def test_the_card_owns_exactly_one_timer_reads_visibility_and_sends_through_the_door():
    source = _source(CARD)
    assert source.count("window.setTimeout(") == 1
    assert "window.clearTimeout(" in source
    assert "usePageVisible()" in source
    assert "sendPreviewCommand(" in source
    assert "[jobId, serverToken, visible, tick]" in source


def test_preview_sends_two_ids_are_the_doors():
    from packages.orchestration.ui_server import (
        JOB_PREVIEW_START_COMMAND_ID,
        JOB_PREVIEW_STOP_COMMAND_ID,
    )

    source = _source(PREVIEW_SEND)
    [start_id] = re.findall(r'export const JOB_PREVIEW_START_COMMAND_ID = "([^"]+)";', source)
    [stop_id] = re.findall(r'export const JOB_PREVIEW_STOP_COMMAND_ID = "([^"]+)";', source)
    assert start_id == JOB_PREVIEW_START_COMMAND_ID
    assert stop_id == JOB_PREVIEW_STOP_COMMAND_ID


def test_both_css_modules_name_the_overlay_layer_with_no_raw_colour():
    for css_path in (PANEL_CSS, LIGHTBOX_CSS):
        css = css_path.read_text(encoding="utf-8")
        assert "var(--remedy-z-overlay)" in css
        assert not _RAW_COLOUR.search(css), f"{css_path.name} carries a raw colour literal"


def test_no_purity_word_of_s1_occurs_in_artifact_preview_ts():
    source = _source(PURE)
    for word in PURITY_WORDS:
        assert word not in source, f"artifactPreview.ts reaches for {word}"


def test_the_shell_mounts_the_panel_outside_main_and_wires_the_toggle():
    source = _source(SHELL)
    assert source.index("</main>") < source.index("<ArtifactsPanel")
    assert "onOpenResults={() => setResultsOpen(true)}" in source
    element = [line for line in source.splitlines() if "<ArtifactsPanel" in line]
    assert len(element) == 1, "expected exactly one ArtifactsPanel element"


def test_the_right_panel_holds_the_results_button():
    source = _source(RIGHT_PANEL)
    assert ('{onOpenResults && (<button type="button" className={styles.advancedToggle} '
            'onClick={onOpenResults}>Results</button>)}') in source


def test_the_shells_tour_anchor_handler_opens_results_for_a_preview_anchor():
    """DECISION F041 D6: the tour's "See it running" stop opens the Results panel."""
    source = _source(SHELL)
    start = source.index("function handleTourShowAnchor(")
    end = source.index("\n  }", start)
    body = source[start:end]
    assert 'anchor.kind === "preview"' in body
    assert "setResultsOpen(true)" in body
