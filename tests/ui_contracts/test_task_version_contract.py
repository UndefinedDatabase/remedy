"""F026 R3 T003 first half, DECISION F026 D3 clause 3 — the popover's Versions
list mounts where the spec says, and neither it nor the pure view it reads
touches a network of its own. No DOM harness exists, so this is read as
source, exactly as `test_pause_controls_contract.py` reads the pause wiring.
"""
from __future__ import annotations

import re
from pathlib import Path

from tests.ui_contracts.test_brain_stream_ring import strip_ts_comments

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
UI_SRC = REPO_ROOT / "apps" / "ui" / "src"

POPOVER = UI_SRC / "components" / "detail" / "DetailPopover.tsx"
VERSION_LIST = UI_SRC / "components" / "detail" / "TaskVersionList.tsx"
TASK_SPEC_VIEW = UI_SRC / "api" / "taskSpecView.ts"

NO_FETCH_FILES = (VERSION_LIST, TASK_SPEC_VIEW)

# A JSX tag's closing `>` is matched non-greedily, with `=>` (an arrow function
# inside an attribute, e.g. `onClick={() => ...}`) consumed as one unit first
# so its own `>` is never mistaken for the tag's end.
_TAG_RE = r"<{name}\b(?:=>|[^>])*?>"


def _source(path: Path) -> str:
    return strip_ts_comments(path.read_text(encoding="utf-8"))


def test_the_popover_mounts_task_version_list_with_the_tasks_key_after_prompt_trace_panel():
    src = _source(POPOVER)
    prompt_idx = src.index("<PromptTracePanel")
    version_idx = src.index("<TaskVersionList")
    assert prompt_idx < version_idx, "TaskVersionList must mount after PromptTracePanel"

    match = re.search(_TAG_RE.format(name="TaskVersionList"), src[version_idx:])
    assert match, "no closed <TaskVersionList ... /> tag found"
    mount = match.group()
    assert 'key={task?.id ?? ""}' in mount, mount


def test_task_version_list_and_task_spec_view_touch_no_network():
    for path in NO_FETCH_FILES:
        assert "fetch(" not in _source(path), f"{path.name} must stay a pure view"


def test_every_button_in_task_version_list_is_type_button_with_aria_expanded():
    src = _source(VERSION_LIST)
    buttons = re.findall(_TAG_RE.format(name="button"), src)
    assert buttons, "no <button> found in TaskVersionList.tsx"
    for button in buttons:
        assert 'type="button"' in button, button
        assert "aria-expanded" in button, button
