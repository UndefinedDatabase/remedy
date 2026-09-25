"""F025 D4 — the pause/resume controls agree with the door and the CLI they send to.

`apps/ui/src/api/pauseSend.ts` mirrors the door's two command ids, and
`apps/ui/src/api/pauseView.ts` mirrors the two sources DECISION F025 D2 lets own a pause —
the CLI's own `--source` default and the door's `COMMAND_EFFECT_SOURCE` — so the operator is
told "paused by you" exactly when the record agrees. `PauseControl.tsx`, `RightLivePanel.tsx`,
`DetailPopover.tsx`, `BrainGraphStage.tsx` and `AgentNowCard.tsx` are read as source too,
because no DOM harness exists: none of the five may open a socket of its own, and the wiring
between them is what no vitest run can see.
"""
from __future__ import annotations

import re
from pathlib import Path

from tests.ui_contracts.test_brain_stream_ring import strip_ts_comments

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
UI_SRC = REPO_ROOT / "apps" / "ui" / "src"

PAUSE_SEND = UI_SRC / "api" / "pauseSend.ts"
PAUSE_VIEW = UI_SRC / "api" / "pauseView.ts"
CONTROL = UI_SRC / "components" / "panels" / "PauseControl.tsx"
PANEL = UI_SRC / "components" / "panels" / "RightLivePanel.tsx"
NOWCARD = UI_SRC / "components" / "panels" / "AgentNowCard.tsx"
POPOVER = UI_SRC / "components" / "detail" / "DetailPopover.tsx"
STAGE = UI_SRC / "components" / "graph" / "BrainGraphStage.tsx"

NO_FETCH_FILES = (CONTROL, PANEL, POPOVER, STAGE, NOWCARD)


def _source(path: Path) -> str:
    return strip_ts_comments(path.read_text(encoding="utf-8"))


def test_the_pause_owner_sources_are_the_clis_default_and_the_doors_source():
    from apps.cli.command_catalog import CATALOG
    from packages.orchestration.ui_server import COMMAND_EFFECT_SOURCE

    pause_entry = next(c for c in CATALOG if c.command_id == "job.pause")
    source_arg = next(a for a in pause_entry.args if a.name == "--source")
    expected = {source_arg.default, COMMAND_EFFECT_SOURCE}

    [body] = re.findall(r"PAUSE_OWNER_SOURCES: readonly string\[\] = \[([^\]]*)\];", _source(PAUSE_VIEW))
    assert set(re.findall(r'"([^"]+)"', body)) == expected


def test_the_two_command_ids_are_the_doors():
    from packages.orchestration.ui_server import JOB_PAUSE_COMMAND_ID, JOB_UNPAUSE_COMMAND_ID

    src = _source(PAUSE_SEND)
    [pause_id] = re.findall(r'export const JOB_PAUSE_COMMAND_ID = "([^"]+)";', src)
    [unpause_id] = re.findall(r'export const JOB_UNPAUSE_COMMAND_ID = "([^"]+)";', src)
    assert pause_id == JOB_PAUSE_COMMAND_ID
    assert unpause_id == JOB_UNPAUSE_COMMAND_ID


def test_none_of_the_five_components_opens_a_socket_of_its_own():
    for path in NO_FETCH_FILES:
        assert "fetch(" not in _source(path), f"{path.name} must reach the door only through pauseSend.ts"


def test_the_panels_control_follows_the_nowcards_line():
    lines = _source(PANEL).splitlines()
    idx = next(i for i, line in enumerate(lines)
               if "<AgentNowCard dashboard={dashboard} recent={recent} />" in line)
    assert "<PauseControl" in lines[idx + 1], (
        "the job's pause control must mount directly after the NowCard"
    )


def test_the_popovers_control_is_passed_the_tasks_id():
    src = _source(POPOVER)
    assert "scope={task.id}" in src, "the popover must pass the SELECTED TASK's id, not the node id"
    assert "taskPauseAction(dashboard, task.id, task.state)" in src


def test_the_stage_renders_the_pause_banner_under_its_own_data_ui():
    src = _source(STAGE)
    assert "const banner = pauseBanner(dashboard);" in src
    block = src[src.index("{banner && ("):]
    block = block[:block.index(")}") + 2]
    assert 'data-ui="pause-banner"' in block
