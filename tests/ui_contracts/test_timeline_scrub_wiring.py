"""F024 T003 — the scrubber is wired: the shell, the bar, the stage and the pill share one position.

T5_F024.md's DONE asks that scrubbing any position renders exactly the reducer state of
that prefix and that scrubbed mode is unmistakably labeled. The pure halves are pinned by
vitest (DECISIONS F024 D1 to D3); what no vitest run can see, because this repository has
no DOM environment, is the WIRING of DECISION F024 D4: that the shell builds one scrubber
over the one ledger and hands it to the bar, the stage and the pill; that the stage draws
the scrubbed model and says SCRUBBED; that the bar is a keyboard-operable slider driven by
pointer and sub-glyph clicks; and that LIVE's timers live in the hook alone. Every
assertion reads COMMENT-STRIPPED source (finding R-0584).
"""
from __future__ import annotations

import re
from pathlib import Path

from tests.ui_contracts.test_brain_stream_ring import strip_ts_comments

UI_SRC = Path(__file__).resolve().parent.parent.parent / "apps" / "ui" / "src" / "components"
SHELL = UI_SRC / "shell" / "RemedyShell.tsx"
STAGE = UI_SRC / "graph" / "BrainGraphStage.tsx"
BAR = UI_SRC / "timeline" / "PhaseTimeline.tsx"
HOOK = UI_SRC / "timeline" / "useTimelineScrub.ts"
PILL = UI_SRC / "panels" / "LiveStatusPill.tsx"
PANEL = UI_SRC / "panels" / "RightLivePanel.tsx"


def _source(path: Path) -> str:
    return strip_ts_comments(path.read_text(encoding="utf-8"))


def _line(src: str, tag: str) -> str:
    lines = [line for line in src.splitlines() if tag in line]
    assert len(lines) == 1, f"expected exactly one {tag} line"
    return lines[0]


def test_the_shell_builds_one_scrubber_and_hands_it_to_the_bar_the_stage_and_the_pill():
    shell = _source(SHELL)
    assert shell.count("useTimelineScrub(") == 1
    assert "const scrub = useTimelineScrub(dashboard.jobId, dashboard.tasks, ledgerRows);" in shell
    assert "<PhaseTimeline scrub={scrub} />" in shell
    assert "scrub={scrub}" in _line(shell, "<BrainGraphStage")
    assert 'replay={scrub.state.mode === "scrubbed"}' in _line(shell, "<RightLivePanel")


def test_the_stage_draws_the_scrubbed_model_and_says_so():
    stage = _source(STAGE)
    assert "const model = scrub.scrubbedModel ?? liveModel;" in stage
    assert "const liveModel = useMemo(() => rebuildBrainModel(dashboard.jobId, seeds, rows)" in stage
    banner = stage[stage.index('{scrub.state.mode === "scrubbed" && ('):]
    banner = banner[:banner.index(")}")]
    for part in ('role="status"', 'data-ui="scrub-banner"', ">SCRUBBED<", "{scrub.view.readout}",
                 "onClick={scrub.goLive}"):
        assert part in banner, f"the SCRUBBED banner lacks {part}"


def test_the_bar_is_a_slider_the_keyboard_the_pointer_and_the_glyphs_all_move():
    bar = _source(BAR)
    handle = bar[bar.index('role="slider"'):]
    handle = handle[:handle.index("/>")]
    for part in ("tabIndex={0}", "aria-valuemin={-1}", "aria-valuenow={state.position}",
                 "aria-valuetext={view.readout}", "scrub.onKey(event.key, event.shiftKey)",
                 "fractionOfSeq(whole, state.position)"):
        assert part in handle, f"the scrubber handle lacks {part}"
    assert "setPointerCapture(event.pointerId)" in bar and "hasPointerCapture(event.pointerId)" in bar
    assert "scrub.scrubTo(seqAtFraction(whole, (event.clientX - rect.left) / rect.width))" in bar
    assert "onClick={() => scrub.scrubTo(g.seq)}" in bar
    assert "onClick={scrub.goLive}" in bar and "aria-pressed={live}" in bar


def test_live_s_timers_live_in_the_hook_alone():
    hook = _source(HOOK)
    assert "catchUpPlan(state.position, state.head, reducedMotion)" in hook
    assert "scrubOverflowed(state)" in hook and "fed.reset(rows)" in hook
    assert "window.setTimeout(" in hook and "window.clearTimeout(" in hook
    assert "setInterval" not in hook
    for path in (SHELL, STAGE, BAR, PILL, PANEL):
        src = _source(path)
        assert "setTimeout" not in src and "setInterval" not in src, f"{path.name} keeps a timer"


def test_the_pill_says_replay_first_and_the_panel_passes_it_on():
    pill = _source(PILL)
    assert 'data-state="replay"' in pill and ">REPLAY<" in pill
    assert pill.index("if (replay)") < pill.index('streamStatus === "delayed"')
    assert "replay={replay}" in _line(_source(PANEL), "<LiveStatusPill")
    assert re.search(r"replay\?: boolean", _source(PANEL))
