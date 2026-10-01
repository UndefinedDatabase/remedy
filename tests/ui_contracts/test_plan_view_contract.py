"""F292 T001 — the plan view reads exactly what the dashboard's `plan` section serves.

`normalizePlan` and `normalizePlanTask` in `apps/ui/src/api/remedyApi.ts` decode the section
`_build_plan_section` writes (DECISION F292 D1 (1)). A decoder that read a key the server never
writes would show a plan as empty, and one that missed a key the server added would drop a fact
the plan view owes, so each key the TypeScript reads is compared with the Python that writes it.
The view is read as source too (DECISION F292 D2): its rules live in a pure module, it reaches no
door, it is a dialog that Escape closes, and the shell mounts it outside the main column. Its
edits (T002, DECISION F292 D3) name the door's own six commands, the planner's own size bands and
editable fields, and an accepted one reads the dashboard again at once.
"""
from __future__ import annotations

import re
from pathlib import Path
from types import SimpleNamespace

from packages.core.models import RunState
from tests.ui_contracts.test_brain_stream_ring import strip_ts_comments

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
UI_SRC = REPO_ROOT / "apps" / "ui" / "src"
REMEDY_API = UI_SRC / "api" / "remedyApi.ts"
PLAN_VIEW_TS = UI_SRC / "api" / "planView.ts"
VIEW = UI_SRC / "components" / "plan" / "PlanView.tsx"
SHELL = UI_SRC / "components" / "shell" / "RemedyShell.tsx"
PANEL = UI_SRC / "components" / "panels" / "RightLivePanel.tsx"


def _source(path: Path) -> str:
    return strip_ts_comments(path.read_text(encoding="utf-8"))


def _function_body(name: str) -> str:
    source = _source(REMEDY_API)
    start = source.index(f"function {name}(")
    return source[start:source.index("\n}\n", start)]


def _served_section() -> dict:
    from packages.orchestration.ui_server import _build_plan_section

    task = {"id": "T1", "title": "t", "goal": "g", "depends_on": [], "est_tokens_band": "S",
            "files_hint": [], "acceptance": ["a"]}
    job = SimpleNamespace(task_plan={"tasks": [task], "_approval": "pending"}, tasks=[],
                          state=RunState.PLANNED)
    section = _build_plan_section(job)
    assert section["available"] is True
    return section


def test_the_section_keys_the_decoder_reads_are_the_servers():
    read = set(re.findall(r"\br\.([a-z_]+)", _function_body("normalizePlan")))
    assert read == set(_served_section())


def test_the_task_keys_the_decoder_reads_are_the_servers():
    read = set(re.findall(r"\br\.([a-z_]+)", _function_body("normalizePlanTask")))
    assert read == set(_served_section()["tasks"][0])


def test_the_dashboard_and_the_failure_path_both_carry_the_plan():
    source = _source(REMEDY_API)
    assert "plan: normalizePlan(dashboard.plan)," in source
    assert "plan: normalizePlan(undefined)," in source


def test_the_pure_module_opens_no_socket_reads_no_clock_and_keeps_no_storage():
    source = _source(PLAN_VIEW_TS)
    for forbidden in ("fetch(", "XMLHttpRequest", "Date.now", "new Date", "localStorage", "react"):
        assert forbidden not in source, forbidden


def test_the_view_reaches_no_door_and_shows_only_the_rules_sentences():
    source = _source(VIEW)
    for forbidden in ("fetch(", "XMLHttpRequest", "remedyApi", "localStorage"):
        assert forbidden not in source, forbidden
    for pure in (UI_SRC / "api" / "planEditView.ts", UI_SRC / "components" / "plan" / "PlanTaskEditForm.tsx",
                 UI_SRC / "components" / "plan" / "PlanCriteria.tsx",
                 UI_SRC / "components" / "plan" / "PlanMergeForm.tsx",
                 UI_SRC / "components" / "plan" / "PlanSplitForm.tsx"):
        for forbidden in ("fetch(", "XMLHttpRequest", "Date.now", "new Date", "localStorage"):
            assert forbidden not in _source(pure), (pure.name, forbidden)
    for rule in ("planHeadline(plan)", "planWindowText(plan)", "planDependencyText(task)",
                 "planEntryText(task)"):
        assert rule in source, rule


def test_the_view_is_a_dialog_that_escape_closes():
    source = _source(VIEW)
    assert 'role="dialog"' in source and 'aria-label="Plan"' in source
    assert 'data-ui="plan-view"' in source
    assert 'if (event.key === "Escape") onClose();' in source


def test_the_shell_mounts_the_view_outside_the_main_column_over_the_dashboards_plan():
    source = _source(SHELL)
    assert source.index("</main>") < source.index("<PlanView")
    assert ("<PlanView plan={dashboard.plan} target={{ jobId: dashboard.jobId, serverToken }}\n"
            "          onReload={onReload} onClose={() => setPlanOpen(false)} />") in source
    assert "onOpenPlan={() => setPlanOpen(true)}" in source


def test_an_accepted_edit_reads_the_dashboard_again_at_once():
    app = _source(UI_SRC / "RemedyApp.tsx")
    assert "const requestReload = useCallback(() => setReloadRequest((count) => count + 1), []);" in app
    assert "}, [face, jobId, token, reloadRequest]);" in app
    assert "onReload={requestReload}" in app
    view = _source(VIEW)
    assert "const outcome = await sendPlanEdit(target, edit, plan.version);" in view
    assert "if (outcome.version !== null) {\n      setOpen(null);\n      onReload?.();" in view


def test_the_edit_commands_are_the_doors():
    from packages.orchestration.ui_server import PLAN_EDIT_COMMAND_IDS

    source = _source(UI_SRC / "api" / "planEditSend.ts")
    block = source[source.index("export const PLAN_EDIT_COMMANDS = ["):]
    listed = re.findall(r'^  "([a-z.-]+)",$', block[:block.index("] as const;")], re.MULTILINE)
    assert listed == list(PLAN_EDIT_COMMAND_IDS)


def test_the_sizes_and_the_edited_fields_are_the_planners():
    from typing import get_args

    from packages.orchestration.plan_editing import EDITABLE_TASK_FIELDS
    from packages.orchestration.schemas.models import TokenBand

    view = _source(UI_SRC / "api" / "planEditView.ts")
    [bands] = re.findall(r"export const PLAN_TOKEN_BANDS = \[([^\]]*)\] as const;", view)
    assert re.findall(r'"([A-Z]+)"', bands) == list(get_args(TokenBand))
    send = _source(UI_SRC / "api" / "planEditSend.ts")
    body = send[send.index("export interface PlanTaskFields {"):]
    fields = re.findall(r"^  ([a-z_]+)\?: string;$", body[:body.index("}")], re.MULTILINE)
    assert fields == ["title", "goal", "est_tokens_band"]
    assert set(fields) <= set(EDITABLE_TASK_FIELDS)


def test_the_criterion_operations_are_the_backends():
    from packages.orchestration.plan_editing import ACCEPTANCE_OPS

    send = _source(UI_SRC / "api" / "planEditSend.ts")
    [ops] = re.findall(r"export type PlanAcceptanceOp = ([^;]*);", send)
    assert re.findall(r'"([a-z]+)"', ops) == list(ACCEPTANCE_OPS)


def test_the_right_panel_offers_the_plan_button():
    source = _source(PANEL)
    assert 'data-ui="plan-button" onClick={onOpenPlan}>Plan</button>' in source
