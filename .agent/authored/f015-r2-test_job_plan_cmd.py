"""F015 T002 — `remedy job plan-show` and the `job plan-*` edit commands, and the CLI approval race.

Every command runs through the grouped CLI in process, over a job saved the way
`do_sequence` saves a freshly planned one. The edit commands are thin wrappers over
`plan_editing.edit_plan` (DECISION F015 D1), so these tests prove the wrapping — the
arguments each command hands the backend and the exit code each refusal maps to — and
leave the edits' own rules to `tests/orchestration/test_plan_editing.py`.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.core.models import RunState
from packages.orchestration.data_paths import job_record_path
from packages.orchestration.job_plan import map_task_plan_to_tasks
from packages.orchestration.pingpong_job import JobPlan, load_job_plan, save_job_plan
from packages.orchestration.schemas.models import TaskPlan
from packages.orchestration.task_deliverables import record_llm_task_deliverables


def _task(tid: str, deps: list[str], acceptance: list[str] | None = None) -> dict:
    return {
        "id": tid, "title": f"Build {tid}", "goal": f"goal of {tid}",
        "acceptance": acceptance or [f"{tid} works"], "depends_on": deps,
        "est_tokens_band": "S", "files_hint": [f"src/{tid.lower()}.py"],
    }


_TASKS = [
    _task("T1", []),
    _task("T2", ["T1"], ["parser reads a file", "parser reports errors", "parser is fast"]),
    _task("T3", ["T2"]),
    _task("T4", ["T2", "T1"]),
]


@pytest.fixture
def job_id(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> str:
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    plan = TaskPlan.model_validate({"schema_v": "task_plan_v1", "tasks": _TASKS})
    body = plan.model_dump()
    body["_approval"] = "pending"
    body["_normalization"] = []
    mapped = map_task_plan_to_tasks(plan)
    record_llm_task_deliverables(mapped)
    job = JobPlan(job_title="F015 CLI probe", task_plan=body, tasks=mapped,
                  state=RunState.PLANNED)
    save_job_plan(job)
    return str(job.job_id)


def _run(argv: list[str], capsys) -> tuple[int, str]:
    from apps.cli.grouped import main

    # A success returns and a refusal exits, so both are read as the exit code.
    try:
        code = main(argv)
    except SystemExit as exc:
        code = exc.code
    return code or 0, capsys.readouterr().out


def _json(argv: list[str], capsys) -> tuple[int, dict]:
    code, out = _run([*argv, "--json"], capsys)
    return code, json.loads(out)


def _stored_ids(job_id: str) -> list[str]:
    return [t["id"] for t in load_job_plan(job_id).task_plan["tasks"]]


class TestPlanShow:

    def test_json_names_the_version_the_open_approval_and_indexed_criteria(self, job_id, capsys):
        code, body = _json(["job", "plan-show", job_id], capsys)
        assert code == 0, body
        assert (body["version"], body["approval"], body["editable"]) == (1, "pending", True)
        assert [t["id"] for t in body["tasks"]] == ["T1", "T2", "T3", "T4"]
        assert body["tasks"][1]["acceptance"][2] == "parser is fast"

    def test_text_prints_each_criterion_under_the_index_the_edits_take(self, job_id, capsys):
        code, out = _run(["job", "plan-show", job_id], capsys)
        assert code == 0, out
        assert f"Plan of job {job_id} — version 1, approval pending" in out
        assert "--plan-version 1" in out
        assert "T4 — Build T4 (band S; waits for T2, T1)" in out
        assert "  [2] parser is fast" in out

    def test_an_approved_plan_is_shown_as_not_editable_with_the_reason(self, job_id, capsys):
        job = load_job_plan(job_id)
        job.task_plan["_approval"] = "approved"
        save_job_plan(job)
        code, body = _json(["job", "plan-show", job_id], capsys)
        assert code == 0, body
        assert body["editable"] is False
        assert "the plan is approved" in body["not_editable_because"]


class TestEachEditCommand:

    @pytest.mark.parametrize(("argv", "expected_ids"), [
        (["plan-edit-task", "{job}", "T3", "--title", "Wire T3", "--band", "L",
          "--acceptance", "wired", "--acceptance", "logged", "--files-hint", "src/w.py"],
         ["T1", "T2", "T3", "T4"]),
        (["plan-delete-task", "{job}", "T2"], ["T1", "T3", "T4"]),
        (["plan-reorder", "{job}", "T1,T2,T4,T3"], ["T1", "T2", "T4", "T3"]),
        (["plan-merge-tasks", "{job}", "T2,T3"], ["T1", "T2", "T4"]),
        (["plan-split-task", "{job}", "T2", "--group", "0,2", "--group", "1"],
         ["T1", "T2a", "T2b", "T3", "T4"]),
        (["plan-edit-acceptance", "{job}", "T2", "add", "--text", "docs", "--index", "0"],
         ["T1", "T2", "T3", "T4"]),
    ])
    def test_the_command_hands_the_backend_its_edit_and_reports_version_two(
            self, job_id, capsys, argv, expected_ids):
        argv = ["job", *[job_id if a == "{job}" else a for a in argv], "--plan-version", "1"]
        code, body = _json(argv, capsys)
        assert code == 0, body
        assert body["version"] == 2 and body["tasks"] == expected_ids
        assert _stored_ids(job_id) == expected_ids
        [entry] = load_job_plan(job_id).task_plan["_edits"]
        assert entry["actor"] == "cli"

    def test_edit_task_changes_exactly_the_named_fields(self, job_id, capsys):
        code, _ = _json(["job", "plan-edit-task", job_id, "T3", "--band", "L",
                         "--acceptance", "wired", "--acceptance", "logged",
                         "--plan-version", "1"], capsys)
        assert code == 0
        t3 = load_job_plan(job_id).task_plan["tasks"][2]
        assert (t3["title"], t3["est_tokens_band"], t3["acceptance"]) == (
            "Build T3", "L", ["wired", "logged"])

    def test_edit_acceptance_takes_the_index_plan_show_prints(self, job_id, capsys):
        code, _ = _json(["job", "plan-edit-acceptance", job_id, "T2", "edit", "--index", "2",
                         "--text", "parser is quick", "--plan-version", "1"], capsys)
        assert code == 0
        assert load_job_plan(job_id).task_plan["tasks"][1]["acceptance"][2] == "parser is quick"


class TestRefusalsAndTheirExitCodes:

    @pytest.mark.parametrize(("argv", "exit_code", "error"), [
        (["plan-delete-task", "{job}", "T4"], 2, "missing_plan_version"),
        (["plan-delete-task", "{job}", "T4", "--plan-version", "one"], 2, "invalid_plan_version"),
        (["plan-delete-task", "{job}", "T9", "--plan-version", "1"], 2, "unknown_task"),
        (["plan-split-task", "{job}", "T2", "--group", "0,x", "--plan-version", "1"], 2,
         "invalid_index"),
        (["plan-edit-acceptance", "{job}", "T2", "remove", "--index", "last",
          "--plan-version", "1"], 2, "invalid_index"),
        (["plan-edit-task", "{job}", "T1", "--plan-version", "1"], 2, "invalid_args"),
        (["plan-delete-task", "{job}", "T4", "--plan-version", "2"], 3, "version_conflict"),
        (["plan-edit-acceptance", "{job}", "T1", "remove", "--index", "0",
          "--plan-version", "1"], 1, "invalid_plan"),
    ])
    def test_a_refused_edit_exits_with_its_class_and_changes_nothing(
            self, job_id, capsys, argv, exit_code, error):
        record = job_record_path(job_id)
        before = record.read_bytes()
        code, body = _json(["job", *[job_id if a == "{job}" else a for a in argv]], capsys)
        assert (code, body["error"]) == (exit_code, error), body
        assert record.read_bytes() == before

    def test_a_stale_version_names_the_current_one(self, job_id, capsys):
        _json(["job", "plan-delete-task", job_id, "T4", "--plan-version", "1"], capsys)
        code, body = _json(["job", "plan-delete-task", job_id, "T3", "--plan-version", "1"],
                           capsys)
        assert (code, body["error"], body["current_version"]) == (3, "version_conflict", 2)

    def test_an_approved_plan_refuses_an_edit_with_exit_three(self, job_id, capsys):
        code, _ = _json(["decision", "resolve", job_id, "plan:approval", "--reason", "approve"],
                        capsys)
        assert code == 0
        code, body = _json(["job", "plan-delete-task", job_id, "T4", "--plan-version", "1"],
                           capsys)
        assert (code, body["error"]) == (3, "plan_not_editable")
        assert "the plan is approved" in body["message"]


class TestTheCliApprovalDoor:
    """DECISION F015 D2 at `remedy decision resolve`: an edit landing after the door loaded the
    job is approved with the plan, never written over by the door's older copy."""

    def test_an_edit_landing_mid_approval_is_approved_not_lost(self, job_id, capsys, monkeypatch):
        from packages.orchestration import job_plan
        from packages.orchestration.plan_editing import edit_plan

        real_questions = job_plan.open_clarification_questions

        def questions_after_a_concurrent_edit(clarifications):
            edit_plan(job_id, "plan_delete_task", {"task_id": "T4"}, expected_version=1,
                      actor="tf:other-tab")
            return real_questions(clarifications)

        monkeypatch.setattr(job_plan, "open_clarification_questions",
                            questions_after_a_concurrent_edit)
        code, body = _json(["decision", "resolve", job_id, "plan:approval", "--reason",
                            "approve"], capsys)
        assert code == 0, body
        stored = load_job_plan(job_id)
        assert stored.task_plan["_approval"] == "approved"
        assert _stored_ids(job_id) == ["T1", "T2", "T3"]
        assert stored.task_plan["_version"] == 2
