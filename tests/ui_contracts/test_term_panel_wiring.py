"""The '?' panel's wiring in the shell and the right panel (F043 T003, DECISION F043 D3).

The panel's own behaviour is held by `termPanel.test.ts` and `termSearch.test.ts`; this file
pins where the shell mounts it and what opens it, reading the COMMENT-STRIPPED sources as the
other wiring contracts do (R-0584), with the stripper the hook contract owns.
"""
from __future__ import annotations

from pathlib import Path

from .test_brain_stream_hook import strip_ts_comments

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
UI_SRC = REPO_ROOT / "apps" / "ui" / "src"
SHELL = UI_SRC / "components" / "shell" / "RemedyShell.tsx"
PANEL = UI_SRC / "components" / "panels" / "RightLivePanel.tsx"


def _line(code: str, needle: str) -> str:
    start = code.index(needle)
    return code[start:code.index("\n", start)]


def test_the_shell_mounts_the_panel_once_outside_main():
    code = strip_ts_comments(SHELL.read_text())
    assert code.count("<TermPanel ") == 1
    assert code.index("<TermPanel ") > code.index("</main>")
    assert ("{termsOpen && (<TermPanel onClose={() => setTermsOpen(false)} onStartTour={() => "
            "{ setTermsOpen(false); setTourRelaunch((count) => count + 1); }} />)}") in code


def test_the_question_mark_opens_it_through_the_one_rule():
    code = strip_ts_comments(SHELL.read_text())
    assert code.count("isHelpShortcut(") == 1
    assert "if (isHelpShortcut(event.key, target)) {" in code
    assert 'window.addEventListener("keydown", onKey);' in code
    assert 'window.removeEventListener("keydown", onKey);' in code


def test_the_shell_mounts_the_first_run_tour_once_outside_main():
    # DECISION F043 D4: the tour's own mount binds its storage, so the shell keeps its one
    # `window.localStorage` (test_digest_mount.py) and hands the mount only the relaunch count.
    code = strip_ts_comments(SHELL.read_text())
    assert code.count("<FirstRunTourMount ") == 1
    assert code.index("<FirstRunTourMount ") > code.index("</main>")
    assert "<FirstRunTourMount relaunch={tourRelaunch} />" in code
    assert code.count("window.localStorage") == 1


def test_the_right_panel_offers_the_terms_button():
    shell = strip_ts_comments(SHELL.read_text())
    assert "onOpenTerms={() => setTermsOpen(true)}" in _line(shell, "<RightLivePanel")
    panel = strip_ts_comments(PANEL.read_text())
    assert "onOpenTerms?: () => void" in panel
    assert 'data-ui="terms-button" onClick={onOpenTerms} aria-keyshortcuts="?">Terms</button>' in panel
