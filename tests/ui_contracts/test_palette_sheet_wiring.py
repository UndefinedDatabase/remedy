"""Wiring guard: the command bar is the palette's combobox (DECISIONS F044 D2 to D5).

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
SEND = UI_SRC / "api" / "paletteSend.ts"
CHAT_SHEET = UI_SRC / "components" / "command" / "ChatSheet.tsx"
CHAT_TAB = UI_SRC / "components" / "graph" / "EvidenceChatTab.tsx"


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


def test_the_bar_reaches_the_door_only_through_the_palette_sender():
    bar = code(BAR)
    assert bar.count("sendPaletteCommand(") == 1
    assert "fetch(" not in bar


def test_the_palette_sender_opens_no_socket_of_its_own():
    send = code(SEND)
    assert "fetch(" not in send
    assert "sendChatCard(" in send
    assert "sendRerunSubtree(" in send


def test_the_shell_mounts_its_own_add_task_sheet_outside_main():
    shell = code(SHELL)
    assert shell.count("<AddTaskSheet ") == 1
    assert shell.index("<AddTaskSheet ") > shell.index("</main>")


def test_the_shell_mounts_the_chat_sheet_outside_main():
    shell = code(SHELL)
    assert shell.count("<ChatSheet ") == 1
    assert shell.index("<ChatSheet ") > shell.index("</main>")
    assert "onAskChat=" in shell


def test_the_chat_sheet_routes_to_the_grounded_chat_and_builds_none_of_its_own():
    sheet = code(CHAT_SHEET)
    assert sheet.count("<EvidenceChatTab ") == 1
    assert "initialQuestion={question}" in sheet
    assert 'role="dialog"' in sheet
    for door in ("fetch(", "loadChatTurn(", "sendChatCard("):
        assert door not in sheet


def test_the_chat_tab_asks_the_palettes_question_once():
    tab = code(CHAT_TAB)
    assert "initialQuestion?: string" in tab
    assert tab.count("askedInitial.current = true;") == 1


def test_the_keymap_puts_the_focus_in_the_bar_and_goes_to_the_projects():
    shell = code(SHELL)
    assert shell.count('window.addEventListener("keydown", onKey);') == 1
    assert "setBarFocusRequest((count) => count + 1);" in shell
    assert "focusRequest={barFocusRequest}" in shell
    assert "goHome();" in shell
    bar = code(BAR)
    assert "if (focusRequest > 0) inputRef.current?.focus();" in bar
    assert "ref={inputRef}" in bar
