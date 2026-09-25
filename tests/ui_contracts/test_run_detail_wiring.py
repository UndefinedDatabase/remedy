"""F023 T002 — the L2 run detail is mounted, fed and wired as DECISION F023 D4 rules.

`RunDetailPopover.tsx` shows the words `runDetailModel.ts` computes for the focused run
and reads the task's per-round facts through the rounds door; `BrainGraphStage.tsx`
mounts it for the focused run at L2 and L3; `RemedyShell.tsx` hands the stage the token
and the diff panel's opener; `ForceBrainGraph.tsx` stops a run click from opening the
task's popover as well. The vitest environment renders no `.tsx`, so the wiring is pinned
from source here; the words are goldened by `runDetailModel.test.ts`.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
GRAPH = ROOT / "apps" / "ui" / "src" / "components" / "graph"
POPOVER = GRAPH / "RunDetailPopover.tsx"
POPOVER_CSS = GRAPH / "RunDetailPopover.module.css"
STAGE = GRAPH / "BrainGraphStage.tsx"
CANVAS = GRAPH / "ForceBrainGraph.tsx"
SHELL = ROOT / "apps" / "ui" / "src" / "components" / "shell" / "RemedyShell.tsx"


def _src(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_the_stage_mounts_the_detail_for_the_focused_run_from_the_model():
    src = _src(STAGE)
    assert ("const focusedRun = zoom.state.level >= 2 ? model.nodes.find((n) => n.id === zoom.state.focusId)"
            " ?? null : null;") in src
    mount = src[src.index("<RunDetailPopover"):]
    mount = mount[:mount.index("/>")]
    for prop in ("node={focusedRun}", "rows={rows}", "promptItems={dashboard.promptTrace?.items ?? []}",
                 "jobId={dashboard.jobId}", "token={serverToken}", "onOpenDiff={onOpenDiff}",
                 "onOpenPrompt={onSelectNode}", 'onClose={() => zoom.dispatch({ type: "escape" })}'):
        assert prop in mount, f"<RunDetailPopover> lacks {prop}"


def test_the_shell_hands_the_stage_the_token_and_the_diff_opener():
    element = [line for line in _src(SHELL).splitlines() if "<BrainGraphStage" in line]
    assert len(element) == 1
    assert "serverToken={serverToken}" in element[0]
    assert "onOpenDiff={setOpenDiffTaskId}" in element[0]


def test_the_detail_reads_its_facts_through_the_door_and_never_shows_another_tasks():
    src = _src(POPOVER)
    assert "loadTaskRunRounds({ jobId, taskId, token })" in src
    assert "if (!cancelled) setLoaded(rounds);" in src
    assert "const rounds = loaded !== null && loaded.taskId === taskId ? loaded : null;" in src
    assert "runDetailOf({ node, rows, rounds, promptItems })" in src


def test_rerun_is_disabled_with_its_reason_visible_and_the_detail_is_not_a_dialog():
    src = _src(POPOVER)
    rerun = src[src.rindex("<button", 0, src.index("Rerun\n")):src.index("Rerun\n")]
    assert "disabled" in rerun and "title={RERUN_NOT_YET}" in rerun and "aria-describedby={reasonId}" in rerun
    assert "<p id={reasonId} className={styles.reason}>{RERUN_NOT_YET}</p>" in src
    # A dialog would make Escape skip the zoom (useSemanticZoom.ts), and Escape is how L2 closes.
    assert 'role="dialog"' not in src
    assert ".action:disabled { opacity: 0.45;" in _src(POPOVER_CSS)


def test_a_run_click_does_not_also_open_the_tasks_popover():
    src = _src(CANVAS)
    body = src[src.index("const handleNodeClick = useCallback("):src.index("}, [onSelectNode, onZoomEvent]);")]
    assert body.index('onZoomEvent({ type: "click", nodeId: n.id });') < body.index("if (isZoomRunKind(n.kind)) return;")
    assert body.index("if (isZoomRunKind(n.kind)) return;") < body.index("onSelectNode(id)")
