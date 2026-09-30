"""Wiring guard: the command bar is the palette's combobox (DECISION F044 D2).

The palette's jump REPLACES the shell's `handleJump`, a substring match over task labels, so
by AGENTS.md's "replacing is deleting" the shell no longer carries it and hands the bar the
palette's own jump targets instead. The bar binds its browser storage edge itself, as the
first-run tour's mount does, because the shell keeps its one `window.localStorage` binding for
the digest (`tests/ui_contracts/test_digest_mount.py`). Behaviour is proved in a real browser by
the round's render harness; this guard pins only the wiring a render cannot see, and it reads
COMMENT-STRIPPED source, so a name a comment mentions never satisfies it (finding R-0584).
"""
from __future__ import annotations

from pathlib import Path

UI_SRC = Path(__file__).resolve().parent.parent.parent / "apps" / "ui" / "src"
SHELL = UI_SRC / "components" / "shell" / "RemedyShell.tsx"
BAR = UI_SRC / "components" / "command" / "CommandBar.tsx"
SHEET = UI_SRC / "components" / "command" / "PaletteSheet.tsx"


def strip_ts_comments(text: str) -> str:
    """Drop // and /* */ comments, keeping the newlines that end line comments."""
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


def code(path: Path) -> str:
    return strip_ts_comments(path.read_text(encoding="utf-8"))


def test_the_shell_no_longer_carries_its_own_jump():
    shell = code(SHELL)
    assert "handleJump" not in shell
    assert "jumpTargetsOf(dashboard)" in shell
    assert "onJump={onSelectNode}" in shell


def test_the_bar_binds_its_own_storage_edge_once():
    bar = code(BAR)
    assert bar.count("window.localStorage") == 1
    assert "useMemo(() => window.localStorage, [])" in bar


def test_the_bar_is_a_combobox_over_the_sheet():
    bar = code(BAR)
    assert 'role="combobox"' in bar
    assert "aria-activedescendant=" in bar
    assert bar.count("<PaletteSheet") == 1


def test_the_sheet_is_portalled_into_the_body():
    sheet = code(SHEET)
    assert "createPortal(" in sheet
    assert "document.body" in sheet
    assert 'role="listbox"' in sheet
    assert 'role="option"' in sheet
