"""F026 D4 — the edit affordance agrees with the door it sends to.

Mirrors `test_pause_controls_contract.py`'s own checks for the pause/resume
controls: `TaskEditForm.tsx` and `taskSpecView.ts` open no socket of their
own, `taskEditSend.ts` names the door's own command id, and `DetailPopover.tsx`
mounts the form only inside the condition that names `taskEditAction`, keyed
by the task id so React remounts it (and drops its last answer sentence) when
the selection changes — the same R-1054 rule `PauseControl`'s own key follows.
"""
from __future__ import annotations

from pathlib import Path

from tests.ui_contracts.test_brain_stream_ring import strip_ts_comments

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
UI_SRC = REPO_ROOT / "apps" / "ui" / "src"

TASK_EDIT_FORM = UI_SRC / "components" / "detail" / "TaskEditForm.tsx"
TASK_SPEC_VIEW = UI_SRC / "api" / "taskSpecView.ts"
TASK_EDIT_SEND = UI_SRC / "api" / "taskEditSend.ts"
POPOVER = UI_SRC / "components" / "detail" / "DetailPopover.tsx"

NO_FETCH_FILES = (TASK_EDIT_FORM, TASK_SPEC_VIEW)


def _source(path: Path) -> str:
    return strip_ts_comments(path.read_text(encoding="utf-8"))


def test_neither_the_form_nor_the_pure_view_opens_a_socket_of_its_own():
    for path in NO_FETCH_FILES:
        assert "fetch(" not in _source(path), f"{path.name} must reach the door only through taskEditSend.ts"


def test_the_send_module_names_the_doors_command_id():
    from packages.orchestration.ui_server import JOB_EDIT_TASK_COMMAND_ID

    assert JOB_EDIT_TASK_COMMAND_ID == "job.edit-task"
    assert '"job.edit-task"' in _source(TASK_EDIT_SEND)


def test_the_popover_mounts_the_form_keyed_by_the_task_id_inside_the_eligibility_condition():
    src = _source(POPOVER)
    assert "taskEditAction(dashboard, task.id)" in src, (
        "the popover must compute the eligibility read taskEditAction(dashboard, task.id) "
        "and gate the mount on its answer, never re-derive the rule inline"
    )
    idx = src.index("<TaskEditForm")
    assert "key={task.id}" in src[idx:idx + 200]

    # The mount sits inside a condition naming the eligibility answer
    # (`editAction`, the binding of the call above) and nothing else that
    # would widen the gate `task`/`serverToken` already narrow it to.
    condition_start = src.rindex("{task && serverToken && editAction", 0, idx)
    condition = src[condition_start:idx]
    assert "editAction" in condition
