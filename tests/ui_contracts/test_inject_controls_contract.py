"""F028 D6/D7 — the injected-task pill agrees with the door it reads, the
browser's send module for the three injection commands names the door's own
ids, and the "Add Task" sheet reaches the door only through that same send
module. Mirrors `test_veto_controls_contract.py`'s own checks for the veto
affordance: `TaskChecklistCard.tsx`, `DetailPopover.tsx`, `injectView.ts` and
`AddTaskSheet.tsx` open no socket of their own, and `taskOriginChip(` is the
one call each of the first two components makes to decide whether the pill
renders.
"""
from __future__ import annotations

from pathlib import Path

from tests.ui_contracts.test_brain_stream_ring import strip_ts_comments

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
UI_SRC = REPO_ROOT / "apps" / "ui" / "src"

TASK_CHECKLIST_CARD = UI_SRC / "components" / "panels" / "TaskChecklistCard.tsx"
DETAIL_POPOVER = UI_SRC / "components" / "detail" / "DetailPopover.tsx"
INJECT_VIEW = UI_SRC / "api" / "injectView.ts"
INJECT_SEND = UI_SRC / "api" / "injectSend.ts"
ADD_TASK_SHEET = UI_SRC / "components" / "panels" / "AddTaskSheet.tsx"
RIGHT_LIVE_PANEL = UI_SRC / "components" / "panels" / "RightLivePanel.tsx"
ASSUMPTION_LOG = REPO_ROOT / "docs" / "ui" / "design_reference" / "assumption_log.md"

NO_FETCH_FILES = (TASK_CHECKLIST_CARD, DETAIL_POPOVER, INJECT_VIEW, ADD_TASK_SHEET)
CHIP_CALL_FILES = (TASK_CHECKLIST_CARD, DETAIL_POPOVER)


def _source(path: Path) -> str:
    return strip_ts_comments(path.read_text(encoding="utf-8"))


def test_none_of_the_three_files_open_a_socket_of_their_own():
    for path in NO_FETCH_FILES:
        assert "fetch(" not in _source(path), f"{path.name} must reach the door only through injectSend.ts"


def test_the_send_modules_three_ids_equal_the_doors_three_constants():
    from packages.orchestration.ui_server import (
        JOB_INJECT_ANSWER_COMMAND_ID,
        JOB_INJECT_COMMAND_ID,
        JOB_INJECT_CONFIRM_COMMAND_ID,
    )

    assert JOB_INJECT_COMMAND_ID == "job.inject"
    assert JOB_INJECT_CONFIRM_COMMAND_ID == "job.inject-confirm"
    assert JOB_INJECT_ANSWER_COMMAND_ID == "job.inject-answer"

    src = _source(INJECT_SEND)
    assert '"job.inject"' in src
    assert '"job.inject-confirm"' in src
    assert '"job.inject-answer"' in src


def test_both_components_decide_the_pill_through_taskoriginchip():
    for path in CHIP_CALL_FILES:
        assert "taskOriginChip(" in _source(path), (
            f"{path.name} must decide whether the pill renders through taskOriginChip(), "
            "never re-derive the rule inline"
        )


def test_the_assumption_log_names_decision_f028_d6_in_exactly_one_row():
    lines = ASSUMPTION_LOG.read_text(encoding="utf-8").splitlines()
    matching = [line for line in lines if "DECISION F028 D6" in line]
    assert len(matching) == 1, f"expected exactly one row naming DECISION F028 D6, found {len(matching)}"


def test_the_assumption_log_names_decision_f028_d7_in_exactly_two_rows():
    lines = ASSUMPTION_LOG.read_text(encoding="utf-8").splitlines()
    matching = [line for line in lines if "DECISION F028 D7" in line]
    assert len(matching) == 2, f"expected exactly two rows naming DECISION F028 D7, found {len(matching)}"


def test_add_task_sheet_reaches_the_door_only_through_the_send_module():
    src = _source(ADD_TASK_SHEET)
    assert "sendInjectDraft(" in src
    assert "sendInjectConfirm(" in src
    assert "sendInjectAnswer(" in src
    assert "injectDraftView(" in src
    assert 'role="dialog"' in src


def test_add_task_sheet_renders_through_a_portal_into_the_document_body():
    """R-1079: `TaskChecklistCard.tsx`'s glass rule sets `backdrop-filter`, which
    makes the card the containing block of every fixed descendant, squeezing
    the sheet into the card instead of covering the viewport. The sheet must
    escape that containing block through a portal straight into `document.body`.
    """
    src = _source(ADD_TASK_SHEET)
    assert "createPortal(" in src
    assert "document.body" in src


def test_right_live_panel_threads_the_server_token_into_the_task_checklist_card():
    src = _source(RIGHT_LIVE_PANEL)
    assert "serverToken={serverToken}" in src
    # The token must land on THIS card, not merely appear somewhere in the file.
    checklist_call = next(line for line in src.splitlines() if "<TaskChecklistCard" in line)
    assert "serverToken={serverToken}" in checklist_call
