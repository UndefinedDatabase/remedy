"""F027 D8 — the veto affordance agrees with the door it sends to.

Mirrors `test_task_edit_controls_contract.py`'s own checks for the runtime
edit controls: `TaskVetoForm.tsx`, `vetoView.ts`, `DetailPopover.tsx` and
`ForceBrainGraph.tsx` open no socket of their own, `vetoSend.ts` names the
door's own command id, the popover mounts the form only inside the condition
that names `vetoAction`, keyed by the task id so React remounts it (and drops
its last answer sentence) when the selection changes — the same R-1054 rule
`TaskEditForm`'s own key follows — the shell wires the popover's task-to-task
jump, and the canvas wires the veto's own fade and hover text.
"""
from __future__ import annotations

from pathlib import Path

from tests.ui_contracts.test_brain_stream_ring import strip_ts_comments

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
UI_SRC = REPO_ROOT / "apps" / "ui" / "src"

TASK_VETO_FORM = UI_SRC / "components" / "detail" / "TaskVetoForm.tsx"
VETO_VIEW = UI_SRC / "api" / "vetoView.ts"
VETO_SEND = UI_SRC / "api" / "vetoSend.ts"
POPOVER = UI_SRC / "components" / "detail" / "DetailPopover.tsx"
SHELL = UI_SRC / "components" / "shell" / "RemedyShell.tsx"
FORCE_BRAIN_GRAPH = UI_SRC / "components" / "graph" / "ForceBrainGraph.tsx"
ASSUMPTION_LOG = REPO_ROOT / "docs" / "ui" / "design_reference" / "assumption_log.md"

NO_FETCH_FILES = (TASK_VETO_FORM, VETO_VIEW, POPOVER, FORCE_BRAIN_GRAPH)


def _source(path: Path) -> str:
    return strip_ts_comments(path.read_text(encoding="utf-8"))


def test_none_of_the_four_files_open_a_socket_of_their_own():
    for path in NO_FETCH_FILES:
        assert "fetch(" not in _source(path), f"{path.name} must reach the door only through vetoSend.ts"


def test_the_send_module_names_the_doors_command_id():
    from packages.orchestration.ui_server import JOB_VETO_TASK_COMMAND_ID

    assert JOB_VETO_TASK_COMMAND_ID == "job.veto-task"
    assert '"job.veto-task"' in _source(VETO_SEND)


def test_the_popover_mounts_the_form_keyed_by_the_task_id_inside_the_eligibility_condition():
    src = _source(POPOVER)
    assert "taskVetoAction(dashboard, task.id)" in src, (
        "the popover must compute the eligibility read taskVetoAction(dashboard, task.id) "
        "and gate the mount on its answer, never re-derive the rule inline"
    )
    idx = src.index("<TaskVetoForm")
    assert "key={task.id}" in src[idx:idx + 200]

    # The mount sits inside a condition naming the eligibility answer
    # (`vetoAction`, the binding of the call above) and nothing else that
    # would widen the gate `task`/`serverToken` already narrow it to.
    condition_start = src.rindex("{task && serverToken && vetoAction", 0, idx)
    condition = src[condition_start:idx]
    assert "vetoAction" in condition


def test_the_shell_wires_the_popovers_task_to_task_jump():
    src = _source(SHELL)
    assert "onSelectTask=" in src


def test_the_popover_calls_onselecttask_to_open_the_other_task():
    src = _source(POPOVER)
    assert "onSelectTask(" in src


def test_the_canvas_holds_the_vetos_fade_and_hover_wiring():
    src = _source(FORCE_BRAIN_GRAPH)
    assert "nodeLabel={handleNodeLabel}" in src
    assert ".textContent =" in src
    assert "NODE_STATE_TREATMENTS.vetoed.downstreamAlpha" in src
    assert "const vetoFade = vetoFaded.has(n.id) ? VETO_DOWNSTREAM_ALPHA : 1;" in src
    assert "innerHTML" not in src


def test_the_assumption_log_names_decision_f027_d8_in_exactly_two_rows():
    lines = ASSUMPTION_LOG.read_text(encoding="utf-8").splitlines()
    matching = [line for line in lines if "DECISION F027 D8" in line]
    assert len(matching) == 2, f"expected exactly two rows naming DECISION F027 D8, found {len(matching)}"
