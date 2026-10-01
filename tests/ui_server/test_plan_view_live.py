"""F292 T003, DECISION F292 D8 — the plan view and the hunk decisions, end to end through the
cockpit and the real write door.

A job is saved with a plan of two tasks waiting for approval and an evidence folder holding a
three-hunk diff of the job's own. The REAL UI server is started for it in this process, serving a
cockpit built into this module's own temporary folder (never the shared ``apps/ui/dist``, which a
parallel worker's build could empty out, DECISION F039 D9), and headless Chrome is driven over
``--remote-debugging-pipe`` with the story test's ``ChromePipe``. Every write goes through the
server's own command door, and every result is read back from the job's record on disk.

What it proves, as a person meets it: the palette lists the six plan edits and the hunk approval
as entries it can open, none disabled; "Edit a planned task" opens the plan view; an edit made
there lands as the plan's next version, and the view reads the dashboard again and shows it; "Approve
or reject the hunks of a change" opens the job's diff with its hunk decisions; and a decision
recorded there is exactly the record ``record_hunk_decision_from_view`` writes for the same
decision, the one ``remedy patch approve-hunks`` writes too.
"""
from __future__ import annotations

import copy
import difflib
import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest

from packages.core.models import RunState
from packages.orchestration.job_plan import map_task_plan_to_tasks
from packages.orchestration.pingpong_job import JobPlan, load_job_plan, save_job_plan
from packages.orchestration.plan_editing import plan_version
from packages.orchestration.schemas.models import TaskPlan
from packages.orchestration.task_deliverables import record_llm_task_deliverables
from tests.ui_server.test_story_export_file_live import (
    CHROME_BIN,
    CHROME_STARTUP_TIMEOUT,
    IDLE_DRAIN_SECONDS,
    VITE_BIN,
    ChromePipe,
    _dispatch_key,
    _poll,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
NEW_TITLE = "Build the strict config loader"
REASON = "caching hides a stale value"
PLAN_COMMANDS = ["job.plan-edit-task", "job.plan-delete-task", "job.plan-reorder", "job.plan-merge-tasks",
                 "job.plan-split-task", "job.plan-edit-acceptance"]


@pytest.fixture(scope="module")
def cockpit_dist(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Once per module: the cockpit built into ITS OWN temporary folder."""
    if not VITE_BIN.is_file():
        pytest.skip(f"{VITE_BIN} is not built; run `cd apps/ui && npm install`")
    import subprocess

    out_dir = tmp_path_factory.mktemp("cockpit-build") / "dist"
    proc = subprocess.run(
        [str(VITE_BIN), "build", "--outDir", str(out_dir), "--emptyOutDir"],
        cwd=str(REPO_ROOT / "apps" / "ui"), capture_output=True, text=True, timeout=300,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert (out_dir / "index.html").is_file()
    return out_dir


def _diff() -> str:
    original = "".join(f"value_{n} = load({n})\n" for n in range(1, 41))
    edited = (original.replace("value_3 = load(3)\n", "value_3 = load(3, strict=True)\n")
              .replace("value_20 = load(20)\n", "value_20 = load_cached(20)\n")
              .replace("value_37 = load(37)\n", "value_37 = None\n"))
    return "".join(difflib.unified_diff(original.splitlines(True), edited.splitlines(True),
                                        fromfile="a/src/config.py", tofile="b/src/config.py"))


def _save_job(tmp_path: Path) -> JobPlan:
    """A planned job whose plan waits for approval, with a three-hunk diff of its own."""
    from packages.orchestration.data_paths import job_evidence_index_dir
    from packages.orchestration.diff_view_source import DIFF_JOB_ARTIFACT_NAME

    tasks = [
        {"id": "T1", "title": "Build the config loader", "goal": "load every key", "depends_on": [],
         "acceptance": ["reads a file", "reports a missing file"], "est_tokens_band": "S", "files_hint": []},
        {"id": "T2", "title": "Build the field validator", "goal": "reject unknown keys", "depends_on": ["T1"],
         "acceptance": ["rejects an unknown key"], "est_tokens_band": "M", "files_hint": []},
    ]
    plan = TaskPlan.model_validate({"schema_v": "task_plan_v1", "tasks": tasks})
    body = plan.model_dump()
    body["_approval"] = "pending"
    body["_normalization"] = []
    mapped = map_task_plan_to_tasks(plan)
    record_llm_task_deliverables(mapped)
    job = JobPlan(job_title="F292 live e2e", task_plan=body, tasks=mapped, state=RunState.PLANNED)
    save_job_plan(job)
    evidence = tmp_path / "evidence"
    evidence.mkdir()
    (evidence / DIFF_JOB_ARTIFACT_NAME).write_text(_diff(), encoding="utf-8")
    index = job_evidence_index_dir()
    index.mkdir(parents=True, exist_ok=True)
    (index / f"{job.job_id}.json").write_text(
        json.dumps({"job_id": str(job.job_id), "evidence_dir_local": str(evidence)}), encoding="utf-8")
    return job


def _start_server(job_id: str, tmp_path: Path) -> dict[str, Any]:
    """The REAL UI server for ``job_id`` in a daemon thread; its published info."""
    import secrets

    from packages.orchestration.ui_server import start_ui_server
    from tests.ui_server.server_start import wait_for_server_info

    info_file = str(tmp_path / "server_info.json")

    def run() -> None:
        try:
            start_ui_server(job_id, host="127.0.0.1", port=0, token=secrets.token_hex(16),
                            open_browser=False, info_file=info_file)
        except (SystemExit, KeyboardInterrupt):
            pass

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    return wait_for_server_info(info_file, thread)


def _set_value(selector: str, value: str) -> str:
    """An expression typing ``value`` into the field ``selector`` names, as React reads typing."""
    return (
        f"(() => {{ const el = document.querySelector({json.dumps(selector)}); if (!el) return false;"
        " const proto = el instanceof HTMLTextAreaElement ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;"
        f" Object.getOwnPropertyDescriptor(proto, 'value').set.call(el, {json.dumps(value)});"
        " el.dispatchEvent(new Event('input', { bubbles: true })); return true; })()"
    )


def _click(expression: str) -> str:
    """An expression clicking the element ``expression`` answers, true when there was one."""
    return f"(() => {{ const el = {expression}; if (el) el.click(); return !!el; }})()"


BAR = '[data-ui="command-bar"] input'
ROWS_EXPR = (
    "Array.from(document.querySelectorAll('[data-ui=\"palette-sheet\"] [data-palette-row]'))"
    ".map((r) => [r.getAttribute('data-palette-row'), r.getAttribute('aria-disabled')])"
)
PLAN_HEADLINE = "(document.querySelector('[data-ui=\"plan-headline\"]') || {}).textContent || null"
PLAN_MESSAGE = "(document.querySelector('[data-ui=\"plan-edit-message\"]') || {}).textContent || null"
HUNK_ROWS = "document.querySelectorAll('[data-ui=\"hunk-decisions\"] li').length"
HUNK_MESSAGE = "(document.querySelector('[data-ui=\"hunk-decision-message\"]') || {}).textContent || null"


def _button(scope: str, text: str) -> str:
    return (f"Array.from(document.querySelectorAll({json.dumps(scope + ' button')}))"
            f".find((b) => b.textContent === {json.dumps(text)})")


def _ask_palette(pipe: ChromePipe, query: str) -> list[list[Any]]:
    """Type ``query`` into the bar and answer the palette's rows once its command rows show."""
    assert _poll(pipe, f"(() => {{ const el = document.querySelector({json.dumps(BAR)}); el.focus(); return true; }})()",
                 lambda v: v is True)
    assert _poll(pipe, _set_value(BAR, query), lambda v: v is True)
    return _poll(pipe, ROWS_EXPR, lambda v: isinstance(v, list) and any(r[0].startswith("command:") for r in v))


def test_the_plan_view_and_the_hunk_decisions_work_through_the_cockpit_and_the_door(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, cockpit_dist: Path,
) -> None:
    if CHROME_BIN is None:
        pytest.skip("neither google-chrome nor chromium is on the path")
    from packages.orchestration import ui_server
    from packages.orchestration.diff_view_source import build_diff_view
    from packages.orchestration.hunk_decision_record import (
        HUNK_DECISIONS_METADATA_KEY,
        record_hunk_decision_from_view,
    )

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setattr(ui_server, "_get_frontend_dist", lambda: cockpit_dist)
    monkeypatch.setattr(ui_server, "_frontend_is_stale", lambda: False)
    job = _save_job(tmp_path)
    job_id = str(job.job_id)
    info = _start_server(job_id, tmp_path)

    pipe = ChromePipe(CHROME_BIN, tmp_path / "profile", log_path=tmp_path / "chrome.log")
    events: list[dict[str, Any]] = []
    try:
        target = pipe.send("Target.createTarget", {"url": "about:blank"}, timeout=CHROME_STARTUP_TIMEOUT)
        attach = pipe.send("Target.attachToTarget", {"targetId": target["targetId"], "flatten": True})
        pipe.session_id = attach["sessionId"]
        pipe.send("Page.enable")
        pipe.send("Runtime.enable")
        pipe.send("Log.enable")
        pipe.send("Page.addScriptToEvaluateOnNewDocument", {
            "source": "window.localStorage.setItem('remedy:first-run-tour', 'seen');"})
        pipe.send("Page.navigate", {"url": info["url"]})
        assert _poll(pipe, "document.querySelector('[data-ui=\"remedy-visual-v2\"]') !== null",
                     lambda v: v is True, timeout=30.0)

        # THE PALETTE lists the six plan edits as entries it can open, none disabled.
        rows = dict(_ask_palette(pipe, "planned"))
        for command in ["job.plan-edit-task", "job.plan-delete-task", "job.plan-split-task", "job.plan-edit-acceptance"]:
            assert rows.get(f"command:{command}", "missing") is None, (command, rows)
        rows = dict(_ask_palette(pipe, "plan"))
        for command in PLAN_COMMANDS:
            assert rows.get(f"command:{command}", "missing") is None, (command, rows)

        # "Edit a planned task" opens the plan view at the stored plan's version.
        _ask_palette(pipe, "Edit a planned task")
        assert _poll(pipe, _click("document.querySelector('[data-palette-row=\"command:job.plan-edit-task\"]')"),
                     lambda v: v is True)
        assert _poll(pipe, PLAN_HEADLINE, lambda v: v == "Version 1 · waiting for approval") is not None

        # AN EDIT lands at the door as the next version, and the view reads it back.
        assert _poll(pipe, _click(_button('[data-ui="plan-view"] [data-plan-task="T1"]', "Edit")), lambda v: v is True)
        assert _poll(pipe, _set_value('[data-ui="plan-task-form"] input', NEW_TITLE), lambda v: v is True)
        assert _poll(pipe, _click(_button('[data-ui="plan-task-form"]', "Save")), lambda v: v is True)
        assert _poll(pipe, PLAN_MESSAGE, lambda v: v == "Saved as version 2.", timeout=20.0) == "Saved as version 2."
        assert _poll(pipe, PLAN_HEADLINE, lambda v: v == "Version 2 · waiting for approval", timeout=20.0)
        stored = load_job_plan(job_id).task_plan
        assert plan_version(stored) == 2
        assert [t["title"] for t in stored["tasks"]] == [NEW_TITLE, "Build the field validator"]
        _dispatch_key(pipe, key="Escape", code="Escape", virtual_key_code=27)
        assert _poll(pipe, PLAN_HEADLINE, lambda v: v is None) is None

        # "Approve or reject the hunks of a change" opens the job's diff with its hunk decisions.
        _ask_palette(pipe, "Approve or reject the hunks")
        assert _poll(pipe, _click("document.querySelector('[data-palette-row=\"command:patch.approve-hunks\"]')"),
                     lambda v: v is True)
        assert _poll(pipe, HUNK_ROWS, lambda v: v == 3, timeout=20.0) == 3

        # A DECISION recorded there is the recorder's own record for the same decision.
        rows_scope = '[data-ui="hunk-decisions"] li'
        assert _poll(pipe, _click(f"Array.from(document.querySelectorAll({json.dumps(rows_scope)})[0]"
                                  ".querySelectorAll('button')).find((b) => b.textContent === 'Approve')"), lambda v: v is True)
        assert _poll(pipe, _click(f"Array.from(document.querySelectorAll({json.dumps(rows_scope)})[1]"
                                  ".querySelectorAll('button')).find((b) => b.textContent === 'Reject')"), lambda v: v is True)
        assert _poll(pipe, _set_value('[data-ui="hunk-decisions"] li input', REASON), lambda v: v is True)
        assert _poll(pipe, _click(_button('[data-ui="hunk-decisions"]', "Record decisions")), lambda v: v is True)
        assert _poll(pipe, HUNK_MESSAGE, lambda v: v == "Recorded: 1 approved, 1 rejected, 1 pending.",
                     timeout=20.0) is not None
        pipe.drain(IDLE_DRAIN_SECONDS)
    finally:
        events = list(pipe.events)
        pipe.close()

    recorded = load_job_plan(job_id).metadata[HUNK_DECISIONS_METADATA_KEY]["job:workspace.diff"]
    view = build_diff_view(ui_server._resolve_evidence_dir(job_id))
    ids = [hunk["id"] for file in view["files"] for hunk in file["hunks"]]
    expected_job = copy.deepcopy(load_job_plan(job_id))
    expected_job.metadata.pop(HUNK_DECISIONS_METADATA_KEY)
    expected = record_hunk_decision_from_view(
        expected_job, task_id="job", attempt=view["source"], attempt_view=view, approved=[ids[0]],
        rejected=[{"id": ids[1], "reason": REASON}], now=datetime.now(timezone.utc))
    assert recorded["hunks"] == expected.exported["hunks"]
    assert [row["state"] for row in recorded["hunks"]] == ["approved", "rejected", "pending"]

    exceptions = [e for e in events if e.get("method") == "Runtime.exceptionThrown"]
    assert exceptions == []
    log_errors = [
        e for e in events
        if e.get("method") == "Log.entryAdded"
        and e["params"]["entry"].get("level") == "error"
        and e["params"]["entry"].get("source") != "network"
    ]
    assert log_errors == []
