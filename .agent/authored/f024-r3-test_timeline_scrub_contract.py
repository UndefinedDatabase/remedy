"""F024 T003, pure half — the scrubber's timing is a motion token and its three modules stay pure.

`scrubState.ts` (the machine, the keyboard, LIVE's catch-up), `timelineIndex.ts` (the
phase reading of every prefix from one fold) and `timelineView.ts` (the bar's view
model) are the headless half of T5_F024.md T003 (DECISION F024 D3). The catch-up's frame
length is `--remedy-dur-fast` of the design reference's motion system, and the bar's
labels are the dashboard's phase titles; the vitest environment reads neither CSS nor
Python, so this guard holds both bindings, and the purity every module here promises.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
TIMELINE = ROOT / "apps" / "ui" / "src" / "components" / "timeline"
STATE = TIMELINE / "scrubState.ts"
INDEX = TIMELINE / "timelineIndex.ts"
VIEW = TIMELINE / "timelineView.ts"
TOKENS = ROOT / "docs" / "ui" / "design_reference" / "tokens.css"
UI_SERVER = ROOT / "packages" / "orchestration" / "ui_server.py"


def _code(path: Path) -> str:
    # Comments are stripped first, so a WHY comment naming a word cannot satisfy or
    # trip a guard about the code (finding R-0584).
    return re.sub(r"//[^\n]*|/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)


def _imports(path: Path) -> list[str]:
    return sorted(set(re.findall(r'^import [^;]*from "([^"]+)";$', _code(path), re.MULTILINE)))


def test_the_catch_up_frame_is_the_fast_motion_token():
    token = re.search(r"--remedy-dur-fast:\s*(\d+)ms;", TOKENS.read_text(encoding="utf-8"))
    assert token, "the design reference no longer defines --remedy-dur-fast"
    step = re.search(r"^export const CATCH_UP_STEP_MS = (\d+);$", _code(STATE), re.MULTILINE)
    assert step and step.group(1) == token.group(1)


def test_the_keyboard_names_the_slider_keys():
    src = _code(STATE)
    for key in ('"ArrowLeft"', '"ArrowRight"', '"Home"', '"End"'):
        assert key in src, f"scrubKeyEvent no longer handles {key}"


def test_the_bar_s_labels_are_the_dashboard_s_phase_titles():
    labels = re.findall(r'^  ([a-z]+): "([A-Za-z]+)",$', _code(VIEW), re.MULTILINE)
    server = UI_SERVER.read_text(encoding="utf-8")
    block = server[server.index("    phases = [\n"):]
    block = block[:block.index("\n    ]\n")]
    titles = re.findall(r'\{"id": "([a-z]+)", "title": "([A-Za-z]+)"', block)
    assert labels == titles


def test_the_three_modules_are_pure():
    assert _imports(STATE) == []
    assert _imports(INDEX) == ["../graph/brainOntology", "../graph/brainReducer", "./phaseMapping"]
    assert _imports(VIEW) == ["./phaseMapping"]
    for path in (STATE, INDEX, VIEW):
        src = _code(path)
        for word in ("window.", "document.", "Date.now", "new Date(", "Math.random", "useState", "useEffect",
                     "setTimeout", "fetch("):
            assert word not in src, f"{path.name} reaches for {word}"
