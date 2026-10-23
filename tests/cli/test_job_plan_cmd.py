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
from packages.orchestration.pingpong_job import (
    TASK_FAILED,
    TASK_PASSED,
    JobPlan,
    load_job_plan,
    save_job_plan,
)
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


@pytest.fixture
def approved_job_id(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> str:
    """F026 T002: the same four tasks, already APPROVED — the runtime edit's own window."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    plan = TaskPlan.model_validate({"schema_v": "task_plan_v1", "tasks": _TASKS})
    body = plan.model_dump()
    body["_approval"] = "approved"
    body["_normalization"] = []
    mapped = map_task_plan_to_tasks(plan)
    record_llm_task_deliverables(mapped)
    job = JobPlan(job_title="F026 CLI probe", task_plan=body, tasks=mapped,
                  state=RunState.PLANNED)
    save_job_plan(job)
    return str(job.job_id)


def _entry_for(job_id: str, planned_id: str):
    """The ``TaskEntry`` of *job_id* whose plan mapping names *planned_id*."""
    for t in load_job_plan(job_id).tasks:
        if (t.inputs.get("plan") or {}).get("planned_id") == planned_id:
            return t
    raise AssertionError(f"no task for planned id {planned_id!r}")


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

    def test_json_names_each_tasks_own_id_status_and_spec_version(self, job_id, capsys):
        entry = _entry_for(job_id, "T2")
        code, body = _json(["job", "plan-show", job_id], capsys)
        assert code == 0, body
        t2 = body["tasks"][1]
        assert (t2["job_task_id"], t2["status"], t2["spec_version"]) == (
            entry.task_id, "pending", 1)

    def test_text_prints_spec_version_and_status_under_the_goal_line(self, job_id, capsys):
        code, out = _run(["job", "plan-show", job_id], capsys)
        assert code == 0, out
        assert "  spec version 1 · pending" in out

    def test_after_a_runtime_edit_the_spec_version_advances(self, approved_job_id, capsys):
        entry = _entry_for(approved_job_id, "T1")
        _json(["job", "edit-task", approved_job_id, entry.task_id, "--spec-version", "1",
              "--title", "x", "--goal", "y"], capsys)
        code, body = _json(["job", "plan-show", approved_job_id], capsys)
        assert code == 0, body
        t1 = body["tasks"][0]
        assert (t1["job_task_id"], t1["status"], t1["spec_version"]) == (
            entry.task_id, "pending", 2)


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


class TestEditTaskCommand:
    """F026 T002, DECISION F026 D2: `job edit-task`, the runtime edit's own CLI door."""

    def test_accepted_by_the_task_entrys_own_id(self, approved_job_id, capsys):
        entry = _entry_for(approved_job_id, "T1")
        code, body = _json(["job", "edit-task", approved_job_id, entry.task_id,
                            "--spec-version", "1", "--title", "New T1", "--goal", "new goal"],
                           capsys)
        assert code == 0, body
        assert (body["job_id"], body["task_id"], body["planned_id"]) == (
            approved_job_id, entry.task_id, "T1")
        assert (body["state"], body["spec_version"], body["plan_version"]) == (
            "waiting", 2, 2)
        assert body["restored"] == []
        updated = _entry_for(approved_job_id, "T1")
        assert updated.spec_version == 2
        assert updated.title == "New T1: new goal"

    def test_accepted_by_the_task_plans_own_id(self, approved_job_id, capsys):
        code, body = _json(["job", "edit-task", approved_job_id, "T2",
                            "--spec-version", "1", "--title", "New T2", "--goal", "new goal"],
                           capsys)
        assert code == 0, body
        assert body["planned_id"] == "T2"
        assert _entry_for(approved_job_id, "T2").spec_version == 2


class TestEditTaskRefusals:

    def test_missing_spec_version(self, approved_job_id, capsys):
        entry = _entry_for(approved_job_id, "T1")
        code, body = _json(
            ["job", "edit-task", approved_job_id, entry.task_id, "--title", "x"], capsys)
        assert (code, body["error"]) == (2, "missing_spec_version")

    def test_invalid_spec_version(self, approved_job_id, capsys):
        entry = _entry_for(approved_job_id, "T1")
        code, body = _json(
            ["job", "edit-task", approved_job_id, entry.task_id, "--spec-version", "abc",
             "--title", "x"], capsys)
        assert (code, body["error"]) == (2, "invalid_spec_version")

    def test_a_stale_version_names_the_current_one(self, approved_job_id, capsys):
        entry = _entry_for(approved_job_id, "T1")
        _json(["job", "edit-task", approved_job_id, entry.task_id, "--spec-version", "1",
              "--title", "x", "--goal", "y"], capsys)
        code, body = _json(["job", "edit-task", approved_job_id, entry.task_id,
                            "--spec-version", "1", "--title", "z", "--goal", "w"], capsys)
        assert (code, body["error"], body["current_version"]) == (3, "version_conflict", 2)

    def test_a_running_job_refuses_job_not_editable(self, approved_job_id, capsys):
        job = load_job_plan(approved_job_id)
        job.state = RunState.RUNNING
        save_job_plan(job)
        entry = _entry_for(approved_job_id, "T1")
        code, body = _json(
            ["job", "edit-task", approved_job_id, entry.task_id, "--spec-version", "1",
             "--title", "x"], capsys)
        assert (code, body["error"]) == (3, "job_not_editable")

    def test_a_passed_task_refuses_task_not_editable(self, approved_job_id, capsys):
        job = load_job_plan(approved_job_id)
        entry = next(t for t in job.tasks
                    if (t.inputs.get("plan") or {}).get("planned_id") == "T1")
        entry.status = TASK_PASSED
        save_job_plan(job)
        code, body = _json(
            ["job", "edit-task", approved_job_id, entry.task_id, "--spec-version", "1",
             "--title", "x"], capsys)
        assert (code, body["error"]) == (3, "task_not_editable")

    def test_a_task_without_a_planned_id_refuses_not_a_plan_task(self, approved_job_id, capsys):
        job = load_job_plan(approved_job_id)
        entry = next(t for t in job.tasks
                    if (t.inputs.get("plan") or {}).get("planned_id") == "T1")
        entry.inputs = {}
        save_job_plan(job)
        code, body = _json(
            ["job", "edit-task", approved_job_id, entry.task_id, "--spec-version", "1",
             "--title", "x"], capsys)
        assert (code, body["error"]) == (2, "not_a_plan_task")

    def test_an_edit_naming_no_field_refuses_invalid_args(self, approved_job_id, capsys):
        entry = _entry_for(approved_job_id, "T1")
        code, body = _json(
            ["job", "edit-task", approved_job_id, entry.task_id, "--spec-version", "1"], capsys)
        assert (code, body["error"]) == (2, "invalid_args")

    def test_the_failed_states_text_names_the_relaunch_command(self, approved_job_id, capsys):
        job = load_job_plan(approved_job_id)
        entry = next(t for t in job.tasks
                    if (t.inputs.get("plan") or {}).get("planned_id") == "T1")
        entry.status = TASK_FAILED
        entry.error = "boom"
        save_job_plan(job)
        code, out = _run(
            ["job", "edit-task", approved_job_id, entry.task_id, "--spec-version", "1",
             "--title", "x", "--goal", "y"], capsys)
        assert code == 0, out
        assert f"remedy job run {approved_job_id}" in out


class TestPlanShowCalibratedBands:
    """F074 T003: beside a calibrated class's band, the plan view prints the class's measured midpoint."""

    @pytest.fixture
    def calibrated_job_id(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> str:
        import subprocess
        from datetime import datetime, timedelta, timezone

        from packages.orchestration.project_registry import register_project_repo
        from packages.orchestration.token_ledger import CallRecord, record_call

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        repo = tmp_path / "repo"
        repo.mkdir()
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        project = register_project_repo("Plan bands", repo)
        recent = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
        # Twenty measured standard_build tasks and two format tasks, below the floor.
        for task_class, count in (("standard_build", 20), ("format", 2)):
            for k in range(1, count + 1):
                seed = f"jobseed{task_class}{k:02d}"
                path = job_record_path(seed)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps({"tasks": [{"task_id": "T001", "task_class": task_class}]}))
                assert record_call(CallRecord(call_id=f"{seed}:T001", job_id=seed, task_id="T001", role="builder",
                                              ts_utc=recent, tokens_in=k * 1000 - 100, tokens_out=100),
                                   project_id=str(project.id))
        self.repo = repo
        plan = TaskPlan.model_validate({"schema_v": "task_plan_v1", "tasks": _TASKS})
        body = plan.model_dump()
        body["_approval"] = "pending"
        body["_normalization"] = []
        mapped = map_task_plan_to_tasks(plan)
        record_llm_task_deliverables(mapped)
        mapped[3].task_class = "format"
        job = JobPlan(job_title="F074 plan bands", task_plan=body, tasks=mapped, state=RunState.PLANNED,
                      repo_path=str(repo))
        save_job_plan(job)
        return str(job.job_id)

    def test_a_calibrated_class_shows_its_midpoint_and_a_thin_one_its_band_alone(self, calibrated_job_id, capsys):
        code, out = _run(["job", "plan-show", calibrated_job_id], capsys)
        assert code == 0, out
        # Builder totals 1000..20000, one trimmed from each end: the P50 is 10500.
        assert "T1 — Build T1 (band S, standard_build calibrated(20) midpoint 10,500 tokens; waits for nothing)" in out
        assert "T4 — Build T4 (band S; waits for T2, T1)" in out

    def test_a_malformed_calibration_setting_leaves_the_bands_alone(self, calibrated_job_id, capsys):
        (self.repo / "remedy.toml").write_text("[remedy.budget]\ncalibration_sample_floor = 0\n")
        code, out = _run(["job", "plan-show", calibrated_job_id], capsys)
        assert code == 0, out
        assert "T1 — Build T1 (band S; waits for nothing)" in out

    def test_the_json_view_is_unchanged(self, calibrated_job_id, capsys):
        code, body = _json(["job", "plan-show", calibrated_job_id], capsys)
        assert code == 0, body
        assert [t["est_tokens_band"] for t in body["tasks"]] == ["S", "S", "S", "S"]
        assert "calibrated" not in json.dumps(body)


class TestPlanShowTrustRoutingNote:
    """F133 T003 (DECISION F133 D4 (2)): `job plan-show`'s "trust suggests otherwise" note."""

    def _seed_task(self, project, job: str, *, status: str, role: str, model: str, cost: float) -> None:
        from datetime import datetime, timedelta, timezone

        from packages.orchestration.data_paths import job_evidence_dir, resolve_data_root
        from packages.orchestration.token_ledger import CallRecord, record_call

        root = resolve_data_root()
        path = job_record_path(job, root)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"tasks": [
            {"task_id": "T001", "status": status, "repair_rounds_used": 0}]}), encoding="utf-8")
        ev_dir = job_evidence_dir(job, root) / "task_runs" / "T001"
        ev_dir.mkdir(parents=True, exist_ok=True)
        (ev_dir / "provider_evidence.json").write_text(json.dumps({"provider_attempts": [
            {"seq": 1, "round": 1, "role": role, "model": model, "is_parse_retry": False}]}),
            encoding="utf-8")
        recent = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
        assert record_call(CallRecord(
            call_id=f"{job}:T001:1", job_id=job, task_id="T001", role=role, model=None, ts_utc=recent,
            tokens_in=100, tokens_out=10, cost_usd=cost, cost_basis="provider_reported"),
            project_id=str(project.id))

    def _make_job(self, repo: Path, *, builder_model: str, reviewer_model: str = "") -> str:
        from packages.orchestration.execution_config import ExecutionConfig

        plan = TaskPlan.model_validate({"schema_v": "task_plan_v1", "tasks": _TASKS})
        body = plan.model_dump()
        body["_approval"] = "pending"
        body["_normalization"] = []
        mapped = map_task_plan_to_tasks(plan)
        record_llm_task_deliverables(mapped)
        job = JobPlan(job_title="F133 CLI routing-note probe", task_plan=body, tasks=mapped,
                      state=RunState.PLANNED, repo_path=str(repo),
                      execution_config=ExecutionConfig(builder_model=builder_model,
                                                       reviewer_model=reviewer_model))
        save_job_plan(job)
        return str(job.job_id)

    @pytest.fixture
    def trust_project(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
        """A STRONG builder (25 passes) and a WEAK one (15 pass, 5 fail), both above the floor."""
        import subprocess

        from packages.orchestration.project_registry import register_project_repo

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        repo = tmp_path / "repo"
        repo.mkdir()
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        project = register_project_repo("Trust plan show", repo)
        for k in range(1, 26):
            self._seed_task(project, f"jobstrong{k:02d}", status="passed", role="builder",
                            model="claude-strong-v1", cost=0.02)
        for k in range(1, 16):
            self._seed_task(project, f"jobweakpass{k:02d}", status="passed", role="builder",
                            model="claude-weak-v1", cost=0.015)
        for k in range(1, 6):
            self._seed_task(project, f"jobweakfail{k:02d}", status="failed", role="builder",
                            model="claude-weak-v1", cost=0.015)
        self.repo = repo
        return repo

    def test_the_note_is_printed_on_a_contradiction_fixture(self, trust_project, capsys):
        job_id = self._make_job(trust_project, builder_model="claude-weak-v1")
        code, out = _run(["job", "plan-show", job_id], capsys)
        assert code == 0, out
        assert ("Trust suggests otherwise for builder: claude-weak-v1 is configured, with a pass "
                "quota of 75% over 20 settled tasks, while claude-strong-v1 leads with 100% over "
                "25 in the last 90 days. This note is informational: the route is unchanged, and "
                "a change is made through config and an ADR.") in out

    def test_none_printed_when_the_configured_model_already_leads(self, trust_project, capsys):
        job_id = self._make_job(trust_project, builder_model="claude-strong-v1")
        code, out = _run(["job", "plan-show", job_id], capsys)
        assert code == 0, out
        assert "Trust suggests otherwise" not in out

    def test_none_printed_and_no_failure_on_a_malformed_trust_setting(self, trust_project, capsys):
        (trust_project / "remedy.toml").write_text(
            "[remedy.model_routing]\ntrust_sample_floor = -4\n", encoding="utf-8")
        job_id = self._make_job(trust_project, builder_model="claude-weak-v1")
        code, out = _run(["job", "plan-show", job_id], capsys)
        assert code == 0, out
        assert "Trust suggests otherwise" not in out

    def test_the_json_view_is_unchanged(self, trust_project, capsys):
        job_id = self._make_job(trust_project, builder_model="claude-weak-v1")
        code, body = _json(["job", "plan-show", job_id], capsys)
        assert code == 0, body
        assert "trust" not in json.dumps(body).lower()

    def test_the_job_record_and_its_configured_models_are_unchanged_by_plan_show(self, trust_project, capsys):
        """The evidence diff (DECISION F133 D4 (3)): the note reads the job's record and never
        writes it."""
        job_id = self._make_job(trust_project, builder_model="claude-weak-v1")
        record = job_record_path(job_id)
        before_bytes = record.read_bytes()
        before_config = load_job_plan(job_id).execution_config
        code, out = _run(["job", "plan-show", job_id], capsys)
        assert code == 0, out
        assert record.read_bytes() == before_bytes
        after_config = load_job_plan(job_id).execution_config
        assert (after_config.builder_model, after_config.reviewer_model) == (
            before_config.builder_model, before_config.reviewer_model)

    @pytest.fixture
    def trust_project_both_roles(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
        """A STRONG model (25 passes) and a WEAK one (15 pass, 5 fail), both above the floor, for
        BOTH the builder and the reviewer role (R-1434)."""
        import subprocess

        from packages.orchestration.project_registry import register_project_repo

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        repo = tmp_path / "repo"
        repo.mkdir()
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        project = register_project_repo("Trust plan show both roles", repo)
        for role in ("builder", "reviewer"):
            for k in range(1, 26):
                self._seed_task(project, f"job{role}strong{k:02d}", status="passed", role=role,
                                model="claude-strong-v1", cost=0.02)
            for k in range(1, 16):
                self._seed_task(project, f"job{role}weakpass{k:02d}", status="passed", role=role,
                                model="claude-weak-v1", cost=0.015)
            for k in range(1, 6):
                self._seed_task(project, f"job{role}weakfail{k:02d}", status="failed", role=role,
                                model="claude-weak-v1", cost=0.015)
        self.repo = repo
        return repo

    def test_the_reviewer_note_prints_when_only_the_reviewer_contradicts(
            self, trust_project_both_roles, capsys):
        """R-1434: a fixture whose configured reviewer contradicts the reviewer role's clear
        leader prints the reviewer's note, with the builder already leading and silent."""
        job_id = self._make_job(trust_project_both_roles, builder_model="claude-strong-v1",
                                reviewer_model="claude-weak-v1")
        code, out = _run(["job", "plan-show", job_id], capsys)
        assert code == 0, out
        assert "Trust suggests otherwise for builder" not in out
        assert ("Trust suggests otherwise for reviewer: claude-weak-v1 is configured, with a pass "
                "quota of 75% over 20 settled tasks, while claude-strong-v1 leads with 100% over "
                "25 in the last 90 days. This note is informational: the route is unchanged, and "
                "a change is made through config and an ADR.") in out

    def test_both_notes_print_builder_first_when_both_contradict(
            self, trust_project_both_roles, capsys):
        """R-1434: when builder and reviewer both contradict their role's clear leader, both
        notes print, builder before reviewer."""
        job_id = self._make_job(trust_project_both_roles, builder_model="claude-weak-v1",
                                reviewer_model="claude-weak-v1")
        code, out = _run(["job", "plan-show", job_id], capsys)
        assert code == 0, out
        builder_at = out.index("Trust suggests otherwise for builder")
        reviewer_at = out.index("Trust suggests otherwise for reviewer")
        assert builder_at < reviewer_at
