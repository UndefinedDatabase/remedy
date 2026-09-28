"""F036 T003's second half — the tour overlay's browser surface, pinned as source.

`TourOverlay.tsx` (DECISION F036 D6) is read as source, exactly as `LessonsOverlay.tsx` and
`AddTaskSheet.tsx` are pinned by their own contract tests (DECISION F031 D5: no DOM harness
exists for these components in this repository's vitest config), because nothing in this
repository can render it. Assertions run against COMMENT-STRIPPED source, or prose above a
definition would satisfy a guard meant for the code (finding R-0584, the reason
`test_main_layout_guard.py`'s neighbours already read this way).
"""
from __future__ import annotations

from pathlib import Path

from tests.ui_contracts.test_brain_stream_ring import strip_ts_comments

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
UI_SRC = REPO_ROOT / "apps" / "ui" / "src"
OVERLAY = UI_SRC / "components" / "tour" / "TourOverlay.tsx"
OVERLAY_CSS = UI_SRC / "components" / "tour" / "TourOverlay.module.css"
SHELL = UI_SRC / "components" / "shell" / "RemedyShell.tsx"
PANEL = UI_SRC / "components" / "panels" / "RightLivePanel.tsx"


def _source(path: Path) -> str:
    return strip_ts_comments(path.read_text(encoding="utf-8"))


def test_the_overlay_is_a_dialog_portaled_to_the_document_body():
    source = _source(OVERLAY)
    assert 'role="dialog"' in source
    assert 'aria-label="Guided tour"' in source
    assert 'data-ui="tour-overlay"' in source
    assert 'data-ui="tour-backdrop"' in source
    assert "createPortal(" in source
    assert "document.body," in source


def test_the_overlay_reads_only_through_the_door_and_drops_a_stale_answer():
    source = _source(OVERLAY)
    assert "fetch(" not in source and "XMLHttpRequest" not in source
    assert "loadTourView(" in source
    assert "let cancelled = false;" in source
    assert "}, [jobId, serverToken]);" in source


def test_escape_closes_the_overlay():
    source = _source(OVERLAY)
    assert 'if (event.key === "Escape") onClose();' in source


def test_the_css_module_names_the_overlay_z_index_and_the_backdrop_tint():
    css = OVERLAY_CSS.read_text(encoding="utf-8")
    assert "var(--remedy-z-overlay)" in css
    assert "var(--remedy-ink-strong)" in css


def test_the_card_carries_data_shown_and_docks_over_the_left_rail_while_shown():
    source = _source(OVERLAY)
    assert "data-shown=" in source

    css = OVERLAY_CSS.read_text(encoding="utf-8")
    assert '.card[data-shown="true"]' in css
    assert "var(--remedy-left-width)" in css


def test_the_shell_mounts_the_overlay_outside_the_main_column():
    source = _source(SHELL)
    assert source.index("</main>") < source.index("<TourOverlay")


def test_the_shell_hands_the_panel_its_open_callback():
    source = _source(SHELL)
    element = [l for l in source.splitlines() if "<RightLivePanel" in l]
    assert len(element) == 1, "expected exactly one RightLivePanel element"
    assert "onOpenTour=" in element[0]


def test_the_shell_opens_the_jobs_whole_diff_and_finds_the_diff_stops_row():
    source = _source(SHELL)
    assert 'setOpenDiffTaskId("")' in source
    assert "tourDiffRowKey(" in source


def test_the_panel_holds_the_tour_button():
    source = _source(PANEL)
    assert ('{onOpenTour && (<button type="button" className={styles.advancedToggle} '
            'onClick={onOpenTour}>Tour</button>)}') in source
