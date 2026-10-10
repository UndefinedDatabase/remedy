"""F301 T002 and T003, DECISIONs F301 D1 and D3 — the project's upkeep ledger, the findings a job
leaves open, and the cadence, plan, step, upkeep job and skip built on it."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from packages.core.models import RunState
from packages.orchestration.data_paths import job_dir, run_dir
from packages.orchestration.mission_state import create_mission, link_job_to_mission
from packages.orchestration.mission_upkeep import (
    LINE_JOB_CLOSED,
    LINE_UPKEEP_NOT_NEEDED,
    LINE_UPKEEP_PLANNED,
    LINE_UPKEEP_SKIPPED,
    UPKEEP_EVERY_DEFAULT,
    UPKEEP_EVERY_KEY,
    UPKEEP_METADATA_KEY,
    UpkeepError,
    append_upkeep_line,
    compile_upkeep_step,
    finding_key,
    job_open_findings,
    make_upkeep_job_if_due,
    open_findings,
    plan_upkeep,
    read_upkeep_ledger,
    record_closed_jobs,
    record_upkeep_skip,
    replaced_pairs_from_findings,
    upkeep_cadence,
    upkeep_digest_counts,
    upkeep_every_setting,
    upkeep_has_work,
    upkeep_ledger_path,
    upkeep_preview,
)
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan

REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECT = "a" * 32


@pytest.fixture()
def data_root(tmp_path, monkeypatch):
    """One data root for jobs, runs, missions and projects alike."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    return tmp_path


def _final_review(job_id: str, findings: list[dict]) -> None:
    path = job_dir(job_id) / "final_job_review.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"job_id": job_id, "verdict": "NEEDS_REPAIR", "findings": findings}),
                    encoding="utf-8")


def _run_record(run_id: str, findings: list[dict]) -> None:
    path = run_dir(run_id) / "result.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    rounds = [{"round": 1, "reviewer": {"verdict": "fail", "findings": [{"id": "OLD"}]}},
              {"round": 2, "reviewer": {"verdict": "fail", "findings": findings}}]
    path.write_text(json.dumps({"run_id": run_id, "rounds": rounds}), encoding="utf-8")


def _job(state: str, tasks: list[TaskEntry] | None = None, metadata: dict | None = None) -> JobPlan:
    job = JobPlan(job_title="fixture", state=RunState(state), tasks=list(tasks or []),
                  metadata=dict(metadata or {}))
    save_job_plan(job)
    return job


def _mission_of(*jobs: JobPlan) -> str:
    mission = create_mission(PROJECT, "Keep the importer working")
    for index, job in enumerate(jobs):
        link_job_to_mission(PROJECT, mission.id, str(job.job_id), "initial" if index == 0 else "follow_up")
    return mission.id


REVIEW_FINDING = {"id": "F-TASK-001", "severity": "repairable", "category": "task_verdict",
                  "message": "T001 did not pass review", "task_id": "T001"}
BLOCKED_FINDING = {"id": "R1", "severity": "high", "file": "importer.py", "summary": "the CSV path is unread"}


class TestTheLedgerFile:
    def test_it_lives_under_the_project_beside_its_other_records(self, tmp_path):
        assert upkeep_ledger_path("p1", tmp_path) == tmp_path / "projects" / "p1" / "upkeep_ledger.jsonl"

    def test_lines_are_appended_and_read_back_in_order(self, data_root):
        first = append_upkeep_line(PROJECT, "m1", LINE_UPKEEP_SKIPPED, {"reason": "one"})
        append_upkeep_line(PROJECT, "m1", LINE_UPKEEP_SKIPPED, {"reason": "two"})
        lines = read_upkeep_ledger(PROJECT)
        assert [line["reason"] for line in lines] == ["one", "two"]
        assert first == lines[0]
        assert {k: first[k] for k in ("version", "kind", "mission_id")} == {
            "version": 1, "kind": LINE_UPKEEP_SKIPPED, "mission_id": "m1"}
        assert first["recorded_at"]

    def test_an_unknown_kind_is_refused_and_writes_nothing(self, data_root):
        with pytest.raises(ValueError):
            append_upkeep_line(PROJECT, "m1", "job_opened", {})
        assert not upkeep_ledger_path(PROJECT).exists()

    def test_a_torn_line_and_a_foreign_line_are_skipped(self, data_root):
        append_upkeep_line(PROJECT, "m1", LINE_UPKEEP_SKIPPED, {"reason": "kept"})
        with upkeep_ledger_path(PROJECT).open("a", encoding="utf-8") as fh:
            fh.write('{"kind": "job_closed", "job_id"\n')
            fh.write('{"kind": "something_else"}\n')
            fh.write("[1, 2]\n")
        assert [line["reason"] for line in read_upkeep_ledger(PROJECT)] == ["kept"]

    def test_a_project_without_a_ledger_reads_empty(self, data_root):
        assert read_upkeep_ledger(PROJECT) == []


class TestTheOpenFindingsOfAJob:
    def test_the_final_review_and_the_blocked_tasks_last_round(self, data_root):
        blocked = TaskEntry(task_id="T002", status="blocked", run_id="run-b")
        passed = TaskEntry(task_id="T003", status="completed", run_id="run-p")
        job = _job("completed", [blocked, passed])
        _final_review(str(job.job_id), [REVIEW_FINDING])
        _run_record("run-b", [BLOCKED_FINDING])
        _run_record("run-p", [{"id": "NOT-READ", "severity": "low", "file": "", "summary": "x"}])

        found = job_open_findings(job)

        job_id = str(job.job_id)
        assert found == [
            {"key": f"{job_id}:T001:F-TASK-001", "source": "final_review", "finding_id": "F-TASK-001",
             "severity": "repairable", "file": "", "summary": "T001 did not pass review", "task_id": "T001"},
            {"key": f"{job_id}:T002:R1", "source": "review", "finding_id": "R1", "severity": "high",
             "file": "importer.py", "summary": "the CSV path is unread", "task_id": "T002"},
        ]

    def test_a_job_level_finding_is_keyed_by_job(self):
        assert finding_key("j1", "", "F-SCOPE-001") == "j1:job:F-SCOPE-001"

    def test_a_job_with_no_review_and_no_blocked_task_leaves_nothing(self, data_root):
        assert job_open_findings(_job("failed", [TaskEntry(status="failed")])) == []

    def test_an_unreadable_final_review_is_no_finding_and_no_crash(self, data_root):
        job = _job("completed")
        path = job_dir(str(job.job_id)) / "final_job_review.json"
        path.write_text("{not json", encoding="utf-8")
        assert job_open_findings(job) == []


class TestReplacedPairs:
    def test_the_hygiene_rules_replaced_file_names_its_original(self):
        findings = [
            {"finding_id": "HYG-replaced-src/importer_v2.py", "file": "src/importer_v2.py",
             "summary": "src/importer_v2.py: added beside src/importer.py, which it replaces"},
            {"finding_id": "HYG-unreferenced-src/x.py", "file": "src/x.py",
             "summary": "src/x.py: an added file that no other file references"},
            {"finding_id": "R1", "file": "src/new_y.py", "summary": "added beside src/y.py, which"},
        ]
        assert replaced_pairs_from_findings(findings) == [
            {"path": "src/importer_v2.py", "original": "src/importer.py"}]

    def test_a_summary_naming_no_original_gives_no_pair(self):
        findings = [{"finding_id": "HYG-replaced-a_v2.py", "file": "a_v2.py", "summary": "a_v2.py: odd"}]
        assert replaced_pairs_from_findings(findings) == []


class TestRecordingClosedJobs:
    def test_each_ended_job_gets_one_line_in_link_order(self, data_root):
        done = _job("completed", [TaskEntry(task_id="T001", status="completed")])
        _final_review(str(done.job_id), [REVIEW_FINDING])
        failed = _job("failed")
        running = _job("running")
        cancelled = _job("cancelled")
        mission_id = _mission_of(done, failed, running, cancelled)

        written = record_closed_jobs(PROJECT, mission_id)

        assert [(line["job_id"], line["job_state"]) for line in written] == [
            (str(done.job_id), "completed"), (str(failed.job_id), "failed"),
            (str(cancelled.job_id), "cancelled")]
        assert written[0]["open_findings"][0]["key"] == f"{done.job_id}:T001:F-TASK-001"
        assert all(line["kind"] == LINE_JOB_CLOSED and line["mission_id"] == mission_id
                   and line["resolved"] == [] and line["replaced"] == [] for line in written)
        assert read_upkeep_ledger(PROJECT) == written

    def test_a_job_is_recorded_once_and_a_running_one_when_it_ends(self, data_root):
        done = _job("completed")
        running = _job("running")
        mission_id = _mission_of(done, running)
        record_closed_jobs(PROJECT, mission_id)

        assert record_closed_jobs(PROJECT, mission_id) == []
        running.state = RunState.COMPLETED
        save_job_plan(running)
        assert [line["job_id"] for line in record_closed_jobs(PROJECT, mission_id)] == [str(running.job_id)]
        assert len(read_upkeep_ledger(PROJECT)) == 2

    def test_a_missing_job_record_is_passed_over(self, data_root):
        done = _job("completed")
        mission_id = _mission_of(done)
        (job_dir(str(done.job_id)) / "job.json").unlink()
        assert record_closed_jobs(PROJECT, mission_id) == []

    def test_a_blocked_replacement_is_recorded_as_a_pair(self, data_root):
        task = TaskEntry(task_id="T001", status="blocked", run_id="run-r")
        job = _job("failed", [task])
        _run_record("run-r", [{"id": "HYG-replaced-src/a_new.py", "severity": "high",
                               "file": "src/a_new.py",
                               "summary": "src/a_new.py: added beside src/a.py, which it replaces"}])
        [line] = record_closed_jobs(PROJECT, _mission_of(job))
        assert line["replaced"] == [{"path": "src/a_new.py", "original": "src/a.py"}]


class TestWhatResolvesAFinding:
    def _two_jobs(self, upkeep_state: str) -> tuple[str, str]:
        first = _job("completed")
        _final_review(str(first.job_id), [REVIEW_FINDING])
        key = finding_key(str(first.job_id), "T001", "F-TASK-001")
        upkeep = _job(upkeep_state, metadata={UPKEEP_METADATA_KEY: {"findings": [key]}})
        return _mission_of(first, upkeep), key

    def test_an_upkeep_job_that_completed_resolves_what_it_carried(self, data_root):
        mission_id, key = self._two_jobs("completed")
        lines = record_closed_jobs(PROJECT, mission_id)
        assert lines[1]["resolved"] == [key]
        assert open_findings(read_upkeep_ledger(PROJECT)) == []

    def test_an_upkeep_job_that_failed_resolves_nothing(self, data_root):
        mission_id, key = self._two_jobs("failed")
        lines = record_closed_jobs(PROJECT, mission_id)
        assert lines[1]["resolved"] == []
        assert [f["key"] for f in open_findings(read_upkeep_ledger(PROJECT))] == [key]

    def test_open_findings_are_oldest_first_once_each_and_scoped_to_a_mission(self, data_root):
        mission_id, key = self._two_jobs("failed")
        record_closed_jobs(PROJECT, mission_id)
        lines = read_upkeep_ledger(PROJECT)
        repeated = {**lines[0], "job_id": "other", "mission_id": "m2"}

        found = open_findings([*lines, repeated])

        assert [f["key"] for f in found] == [key]
        assert found[0]["job_id"] == lines[0]["job_id"]
        assert open_findings(lines, mission_id="m2") == []
        assert [f["key"] for f in open_findings(lines, mission_id=mission_id)] == [key]


def test_mission_continue_records_the_ended_jobs_before_the_next_one(tmp_path):
    """The way a user reaches the ledger: `remedy mission continue` on the command line."""
    data_root = tmp_path / "data"
    env = {**os.environ, "REMEDY_DATA_DIR": str(data_root)}
    env.pop("REMEDY_PROJECT", None)
    previous = os.environ.get("REMEDY_DATA_DIR")
    os.environ["REMEDY_DATA_DIR"] = str(data_root)
    try:
        from packages.orchestration.config import reset_config
        from packages.orchestration.project_registry import RemyProject, save_project

        reset_config()
        project = RemyProject(name="Upkeep Test", slug="upkeep-test")
        save_project(project)
        project_id = str(project.id)
        mission = create_mission(project_id, "Keep the importer working")
        first = _job("completed")
        _final_review(str(first.job_id), [REVIEW_FINDING])
        link_job_to_mission(project_id, mission.id, str(first.job_id), "initial")
    finally:
        if previous is None:
            os.environ.pop("REMEDY_DATA_DIR", None)
        else:
            os.environ["REMEDY_DATA_DIR"] = previous
        reset_config()

    def run() -> dict:
        proc = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", "mission", "continue", mission.id, "Add the CSV path",
             "--project", project_id, "--json"],
            cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=120, env=env)
        assert proc.returncode == 0, proc.stderr
        return json.loads(proc.stdout)

    body = run()
    run()

    lines = read_upkeep_ledger(project_id, data_root)
    assert [(line["kind"], line["job_id"]) for line in lines] == [(LINE_JOB_CLOSED, str(first.job_id))]
    assert lines[0]["open_findings"][0]["key"] == f"{first.job_id}:T001:F-TASK-001"
    assert body["role"] == "follow_up"


# ---------------------------------------------------------------------------
# F301 T003, DECISIONs F301 D1 and D3: the cadence, the plan, the upkeep job and the skip
# ---------------------------------------------------------------------------

def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=str(repo), check=True, capture_output=True, timeout=60)


@pytest.fixture()
def repository(tmp_path) -> Path:
    """A committed repository with one long function, a long code file, a longer data file, and a
    file that sits beside the one it replaces."""
    repo = tmp_path / "repo"
    (repo / "src").mkdir(parents=True)
    body = "".join(f"    x = {n}\n" for n in range(119))
    filler = "".join(f"VALUE_{n} = {n}\n" for n in range(1000))
    (repo / "src" / "big.py").write_text(f"def very_long():\n{body}\n\n{filler}", encoding="utf-8")
    (repo / "notes.txt").write_text("line\n" * 1500, encoding="utf-8")
    (repo / "src" / "importer.py").write_text("OLD = 1\n", encoding="utf-8")
    (repo / "src" / "importer_v2.py").write_text("NEW = 2\n", encoding="utf-8")
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "fixture@example.com")
    _git(repo, "config", "user.name", "Fixture")
    _git(repo, "config", "commit.gpgsign", "false")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "fixture")
    return repo


@pytest.fixture()
def registered(data_root, repository) -> str:
    """A project registered with the repository above; answers its id."""
    from packages.orchestration.config import reset_config
    from packages.orchestration.project_registry import RemyProject, save_project

    reset_config()
    project = RemyProject(name="Upkeep Fixture", slug="upkeep-fixture", canonical_repo_path=str(repository))
    save_project(project)
    return str(project.id)


def _chain(project_id: str, states: list[str], *, findings: int = 0) -> tuple[str, list[JobPlan]]:
    mission = create_mission(project_id, "Keep the importer working")
    jobs = []
    for index, state in enumerate(states):
        job = _job(state)
        if index == 0 and findings:
            _final_review(str(job.job_id), [
                {"id": f"F-TASK-{n:03d}", "severity": "repairable", "category": "task_verdict",
                 "message": f"finding number {n}", "task_id": "T001"} for n in range(1, findings + 1)])
        link_job_to_mission(project_id, mission.id, str(job.job_id), "initial" if index == 0 else "follow_up")
        jobs.append(job)
    return mission.id, jobs


EVERY_TWO = {"mission.upkeep_every": 2}


class TestTheSetting:
    def test_it_is_registered_with_its_default_and_its_variable(self):
        from packages.orchestration.config import get_key_spec

        spec = get_key_spec(UPKEEP_EVERY_KEY)
        assert (spec.default, spec.value_type, spec.env_var) == (5, int, "REMEDY_MISSION_UPKEEP_EVERY")

    def test_unset_reads_five_and_a_number_reads_itself(self):
        assert upkeep_every_setting({}) == UPKEEP_EVERY_DEFAULT == 5
        assert upkeep_every_setting({UPKEEP_EVERY_KEY: 3}) == 3

    @pytest.mark.parametrize("value", [0, -1, True, "5", 2.5])
    def test_anything_but_a_whole_number_of_at_least_one_is_refused(self, value):
        with pytest.raises(UpkeepError):
            upkeep_every_setting({UPKEEP_EVERY_KEY: value})

    def test_the_variable_reaches_the_setting(self, monkeypatch):
        from packages.orchestration.config import reset_config

        monkeypatch.setenv("REMEDY_MISSION_UPKEEP_EVERY", "7")
        reset_config()
        try:
            assert upkeep_every_setting() == 7
        finally:
            monkeypatch.delenv("REMEDY_MISSION_UPKEEP_EVERY")
            reset_config()


class TestTheCadence:
    def test_only_completed_jobs_count(self, data_root):
        mission_id, _ = _chain(PROJECT, ["completed", "failed", "completed", "running", "completed"])
        cadence = upkeep_cadence(PROJECT, mission_id, config={})
        assert (cadence.every, cadence.completed, cadence.due, cadence.jobs_left) == (5, 3, False, 2)
        assert upkeep_cadence(PROJECT, mission_id, config={UPKEEP_EVERY_KEY: 3}).due

    def test_a_skip_or_a_not_needed_line_ends_the_slot_at_the_job_it_names(self, data_root):
        mission_id, jobs = _chain(PROJECT, ["completed", "completed", "completed"])
        append_upkeep_line(PROJECT, mission_id, LINE_UPKEEP_SKIPPED, {"after_job_id": str(jobs[1].job_id)})
        assert upkeep_cadence(PROJECT, mission_id, config={}).completed == 1
        append_upkeep_line(PROJECT, mission_id, LINE_UPKEEP_NOT_NEEDED, {"after_job_id": str(jobs[2].job_id)})
        assert upkeep_cadence(PROJECT, mission_id, config={}).completed == 0

    def test_an_upkeep_job_ends_the_slot_and_is_not_counted(self, data_root):
        mission_id, jobs = _chain(PROJECT, ["completed", "completed", "completed", "completed"])
        append_upkeep_line(PROJECT, mission_id, LINE_UPKEEP_PLANNED, {"job_id": str(jobs[1].job_id)})
        assert upkeep_cadence(PROJECT, mission_id, config={}).completed == 2

    def test_another_missions_lines_do_not_count(self, data_root):
        mission_id, jobs = _chain(PROJECT, ["completed", "completed"])
        append_upkeep_line(PROJECT, "another", LINE_UPKEEP_SKIPPED, {"after_job_id": str(jobs[1].job_id)})
        assert upkeep_cadence(PROJECT, mission_id, config={}).completed == 2


class TestThePlanAndItsStep:
    def test_it_carries_the_oldest_findings_the_largest_code_and_the_replaced_file(self, registered):
        mission_id, _ = _chain(registered, ["completed", "completed"], findings=7)
        record_closed_jobs(registered, mission_id)
        lines = read_upkeep_ledger(registered)

        plan = plan_upkeep(registered, mission_id, upkeep_cadence(registered, mission_id, config=EVERY_TWO), lines)

        assert [key.rsplit(":", 1)[1] for key in plan["findings"]] == [
            "F-TASK-001", "F-TASK-002", "F-TASK-003", "F-TASK-004", "F-TASK-005"]
        assert plan["structure"]["largest_function"] == {
            "path": "src/big.py", "name": "very_long", "line": 1, "lines": 120}
        assert plan["structure"]["largest_file"] == {"path": "src/big.py", "lines": 1122}
        assert plan["structure"]["limits"] == {"function_lines": 100, "file_lines": 1000}
        assert plan["replaced"] == [{"path": "src/importer_v2.py", "original": "src/importer.py"}]
        assert upkeep_has_work(plan)

        step = compile_upkeep_step(plan)
        assert step.splitlines()[0] == ("Upkeep after 2 completed jobs of this mission, planned by "
                                        "Remedy's fixed rules (DECISION F301 D1).")
        for needle in ("finding F-TASK-001", "finding F-TASK-005", "very_long in src/big.py (line 1), 120 lines",
                       "the file src/big.py, 1122 lines", "- src/importer.py, replaced by src/importer_v2.py"):
            assert needle in step
        assert "F-TASK-006" not in step and "notes.txt" not in step
        order = [step.index(n) for n in ("finding F-TASK-001", "very_long", "the file src/big.py", "- src/importer.py")]
        assert order == sorted(order)

    def test_a_project_without_a_repository_carries_findings_alone(self, data_root):
        mission_id, _ = _chain(PROJECT, ["completed"], findings=1)
        record_closed_jobs(PROJECT, mission_id)
        plan = plan_upkeep(PROJECT, mission_id, upkeep_cadence(PROJECT, mission_id, config={}),
                           read_upkeep_ledger(PROJECT))
        assert plan["structure"] == {"unmeasured": "the project names no repository"}
        assert plan["replaced"] == [] and len(plan["findings"]) == 1

    def test_only_the_missions_own_findings_ride(self, data_root):
        other_id, _ = _chain(PROJECT, ["completed"], findings=2)
        mission_id, jobs = _chain(PROJECT, ["completed"], findings=1)
        record_closed_jobs(PROJECT, other_id)
        record_closed_jobs(PROJECT, mission_id)
        plan = plan_upkeep(PROJECT, mission_id, upkeep_cadence(PROJECT, mission_id, config={}),
                           read_upkeep_ledger(PROJECT))
        assert [f["job_id"] for f in plan["carried"]] == [str(jobs[0].job_id)]

    def test_a_replaced_pair_a_job_left_is_carried_while_both_files_exist(self, registered, repository):
        mission_id, jobs = _chain(registered, ["completed"])
        append_upkeep_line(registered, mission_id, LINE_JOB_CLOSED, {
            "job_id": str(jobs[0].job_id), "open_findings": [], "resolved": [],
            "replaced": [{"path": "src/importer_v2.py", "original": "src/importer.py"},
                         {"path": "src/extra_new.py", "original": "src/extra.py"},
                         {"path": "src/gone_new.py", "original": "src/gone.py"}]})
        (repository / "src" / "importer_v2.py").unlink()
        _git(repository, "commit", "-qam", "drop the replacement")
        for name in ("extra.py", "extra_new.py"):  # untracked, so only the job's line can name them
            (repository / "src" / name).write_text("X = 1\n", encoding="utf-8")
        plan = plan_upkeep(registered, mission_id, upkeep_cadence(registered, mission_id, config={}),
                           read_upkeep_ledger(registered))
        assert plan["replaced"] == [{"path": "src/extra_new.py", "original": "src/extra.py"}]


class TestTheUpkeepJob:
    def test_nothing_happens_before_it_is_due(self, registered):
        mission_id, _ = _chain(registered, ["completed"], findings=1)
        outcome = make_upkeep_job_if_due(registered, mission_id, config=EVERY_TWO)
        assert (outcome.job, outcome.plan, outcome.line, outcome.cadence.completed) == (None, None, None, 1)
        assert [line["kind"] for line in read_upkeep_ledger(registered)] == [LINE_JOB_CLOSED]

    def test_when_due_it_is_an_ordinary_follow_up_job_known_by_its_metadata(self, registered):
        from packages.orchestration.mission_state import load_mission
        from packages.orchestration.pingpong_job import load_job_plan

        mission_id, jobs = _chain(registered, ["completed", "completed"], findings=1)
        outcome = make_upkeep_job_if_due(registered, mission_id, config=EVERY_TWO)

        job = load_job_plan(str(outcome.job.job_id))
        assert job.metadata["mission_role"] == "follow_up"
        assert job.metadata[UPKEEP_METADATA_KEY]["findings"] == outcome.plan["findings"]
        assert job.metadata[UPKEEP_METADATA_KEY]["after_job_id"] == str(jobs[1].job_id)
        assert job.tasks[-1].title == compile_upkeep_step(outcome.plan)
        assert load_mission(registered, mission_id).job_ids()[-1] == str(job.job_id)
        assert outcome.line["kind"] == LINE_UPKEEP_PLANNED and outcome.line["job_id"] == str(job.job_id)
        assert upkeep_cadence(registered, mission_id, config=EVERY_TWO).completed == 0

    def test_findings_alone_are_work_enough_for_a_job(self, data_root):
        mission_id, _ = _chain(PROJECT, ["completed", "completed"], findings=1)
        outcome = make_upkeep_job_if_due(PROJECT, mission_id, config=EVERY_TWO)
        assert outcome.plan["structure"] == {"unmeasured": "the project names no repository"}
        assert outcome.job is not None and outcome.line["kind"] == LINE_UPKEEP_PLANNED

    def test_when_due_with_nothing_to_carry_no_job_is_made_and_that_is_recorded(self, data_root):
        mission_id, jobs = _chain(PROJECT, ["completed", "completed"])
        outcome = make_upkeep_job_if_due(PROJECT, mission_id, config=EVERY_TWO)
        assert outcome.job is None and outcome.line["kind"] == LINE_UPKEEP_NOT_NEEDED
        assert outcome.line["after_job_id"] == str(jobs[1].job_id)
        assert upkeep_cadence(PROJECT, mission_id, config=EVERY_TWO).completed == 0

    def test_a_completed_upkeep_job_resolves_what_it_carried_and_the_rest_comes_next(self, registered):
        from packages.orchestration.pingpong_job import load_job_plan

        mission_id, _ = _chain(registered, ["completed", "completed"], findings=7)
        outcome = make_upkeep_job_if_due(registered, mission_id, config=EVERY_TWO)
        job = load_job_plan(str(outcome.job.job_id))
        job.state = RunState.COMPLETED
        save_job_plan(job)
        record_closed_jobs(registered, mission_id)

        left = open_findings(read_upkeep_ledger(registered), mission_id=mission_id)
        assert [f["finding_id"] for f in left] == ["F-TASK-006", "F-TASK-007"]


class TestTheSkip:
    def test_a_skip_needs_a_reason(self, data_root):
        mission_id, _ = _chain(PROJECT, ["completed", "completed"])
        for reason in ("", "   ", None):
            with pytest.raises(UpkeepError, match="reason"):
                record_upkeep_skip(PROJECT, mission_id, reason, config=EVERY_TWO)
        assert [line["kind"] for line in read_upkeep_ledger(PROJECT)] == []

    def test_a_skip_needs_an_upkeep_job_that_is_due(self, data_root):
        mission_id, _ = _chain(PROJECT, ["completed"])
        with pytest.raises(UpkeepError, match="1 more completed job of this mission"):
            record_upkeep_skip(PROJECT, mission_id, "a release is due", config=EVERY_TWO)
        assert LINE_UPKEEP_SKIPPED not in [line["kind"] for line in read_upkeep_ledger(PROJECT)]

    def test_a_recorded_skip_carries_its_reason_and_ends_the_slot(self, data_root):
        mission_id, jobs = _chain(PROJECT, ["completed", "completed"])
        line = record_upkeep_skip(PROJECT, mission_id, "  a release is due  ", config=EVERY_TWO)
        assert (line["kind"], line["reason"], line["after_jobs"], line["after_job_id"]) == (
            LINE_UPKEEP_SKIPPED, "a release is due", 2, str(jobs[1].job_id))
        assert upkeep_cadence(PROJECT, mission_id, config=EVERY_TWO).completed == 0


class TestAHaltedJob:
    """R-1234: a job halted blocked or stopped counts as ended once a later job of its mission is
    linked; before that it may still be taken up again, and a paused job is never ended by one."""

    @pytest.mark.parametrize("state", ["blocked", "stopped"])
    def test_it_is_recorded_once_the_mission_moves_on(self, data_root, state):
        mission = create_mission(PROJECT, "Keep the importer working")
        halted = _job(state, [TaskEntry(task_id="T001", status="blocked", run_id="run-h")])
        _run_record("run-h", [BLOCKED_FINDING])
        link_job_to_mission(PROJECT, mission.id, str(halted.job_id), "initial")
        assert record_closed_jobs(PROJECT, mission.id) == []

        later = _job("planned")
        link_job_to_mission(PROJECT, mission.id, str(later.job_id), "follow_up")
        [line] = record_closed_jobs(PROJECT, mission.id)

        assert (line["job_id"], line["job_state"]) == (str(halted.job_id), state)
        assert [f["finding_id"] for f in line["open_findings"]] == ["R1"]

    def test_a_paused_job_is_not_ended_by_a_later_one(self, data_root):
        mission = create_mission(PROJECT, "Keep the importer working")
        for index, state in enumerate(("paused", "planned")):
            link_job_to_mission(PROJECT, mission.id, str(_job(state).job_id), "initial" if index == 0 else "follow_up")
        assert record_closed_jobs(PROJECT, mission.id) == []


class TestAReplacementThroughARun:
    """F301 T004, DECISION F301 D1 (10): the round hygiene rule fails a round that leaves a file beside
    the one it replaces; the halted job's line records the pair, and an upkeep plan carries it while
    both files are in the repository."""

    def test_the_chain_from_the_round_to_the_upkeep_plan(self, data_root, tmp_path):
        from packages.orchestration.config import reset_config
        from packages.orchestration.pingpong_job import parse_job_file, run_job
        from packages.orchestration.pingpong_provider import FakeProvider
        from packages.orchestration.project_registry import RemyProject, save_project

        repo = tmp_path / "importer-repo"
        (repo / "src").mkdir(parents=True)
        (repo / "README.md").write_text("# Importer\n", encoding="utf-8")
        (repo / "src" / "importer.py").write_text("OLD = 1\n", encoding="utf-8")
        for args in (("init", "-q"), ("config", "user.email", "f@example.com"), ("config", "user.name", "F"),
                     ("config", "commit.gpgsign", "false"), ("add", "-A"), ("commit", "-qm", "base")):
            _git(repo, *args)
        reset_config()
        project = RemyProject(name="Importer", slug="importer", canonical_repo_path=str(repo))
        save_project(project)
        project_id = str(project.id)
        mission = create_mission(project_id, "Replace the importer")
        job = parse_job_file("# Job: Replace\n\n## Task 1\nReplace the importer.\n\nAcceptance:\n- done\n",
                             str(repo))
        save_job_plan(job)
        link_job_to_mission(project_id, mission.id, str(job.job_id), "initial")
        provider = FakeProvider(builder_files=["src/importer_v2.py"], pass_on_round=1, fail_on_round=99)

        ended = run_job(job.job_id, builder_provider=provider, reviewer_provider=provider, repair_rounds=0)

        assert str(getattr(ended.state, "value", ended.state)) == "blocked"
        assert ended.tasks[0].reviewer_verdict == "needs_repair"
        later = _job("planned")
        link_job_to_mission(project_id, mission.id, str(later.job_id), "follow_up")
        [line] = record_closed_jobs(project_id, mission.id)
        pair = {"path": "src/importer_v2.py", "original": "src/importer.py"}
        assert line["replaced"] == [pair]
        assert "HYG-replaced-src/importer_v2.py" in [f["finding_id"] for f in line["open_findings"]]

        cadence = upkeep_cadence(project_id, mission.id, config={})
        assert plan_upkeep(project_id, mission.id, cadence, read_upkeep_ledger(project_id))["replaced"] == []
        (repo / "src" / "importer_v2.py").write_text("NEW = 2\n", encoding="utf-8")
        assert plan_upkeep(project_id, mission.id, cadence, read_upkeep_ledger(project_id))["replaced"] == [pair]


class TestThePreview:
    """F301 T005, DECISION F301 D5: what a person and a client see, computed without writing."""

    def test_it_writes_nothing_and_counts_the_ended_jobs_not_yet_recorded(self, data_root):
        mission_id, _ = _chain(PROJECT, ["completed", "completed"], findings=2)

        preview = upkeep_preview(PROJECT, mission_id, config=EVERY_TWO)

        assert (preview["every"], preview["completed"], preview["jobs_left"], preview["due"]) == (2, 2, 0, True)
        assert preview["open_findings"] == 2 and len(preview["carries"]["findings"]) == 2
        assert not upkeep_ledger_path(PROJECT).exists()

    def test_without_the_measure_it_carries_no_plan(self, data_root):
        mission_id, _ = _chain(PROJECT, ["completed"], findings=1)
        preview = upkeep_preview(PROJECT, mission_id, config={}, measure=False)
        assert "carries" not in preview and (preview["jobs_left"], preview["open_findings"]) == (4, 1)

    def test_it_carries_the_structure_and_the_replaced_file(self, registered):
        mission_id, _ = _chain(registered, ["completed"])
        carries = upkeep_preview(registered, mission_id, config={})["carries"]
        assert carries["structure"]["largest_file"]["path"] == "src/big.py"
        assert carries["replaced"] == [{"path": "src/importer_v2.py", "original": "src/importer.py"}]

    def test_a_bad_setting_is_refused(self, data_root):
        mission_id, _ = _chain(PROJECT, ["completed"])
        with pytest.raises(UpkeepError):
            upkeep_preview(PROJECT, mission_id, config={UPKEEP_EVERY_KEY: 0})


class TestTheDigestCounts:
    def test_they_are_the_setting_the_jobs_left_and_the_open_findings(self, data_root):
        from packages.orchestration.config import reset_config

        reset_config()
        mission_id, _ = _chain(PROJECT, ["completed", "completed"], findings=3)
        assert upkeep_digest_counts(PROJECT, mission_id) == {"every": 5, "jobs_left": 3, "open_findings": 3}

    def test_they_never_read_the_repository(self, registered, monkeypatch):
        from packages.orchestration import structure_measure

        def tripwire(*args, **kwargs):
            raise AssertionError("the digest's counts read the project's repository")

        monkeypatch.setattr(structure_measure, "measure_repository", tripwire)
        monkeypatch.setattr(structure_measure, "tracked_files", tripwire)
        mission_id, _ = _chain(registered, ["completed"])
        assert upkeep_digest_counts(registered, mission_id)["jobs_left"] == 4

    def test_they_read_none_and_never_raise_when_unreadable(self, data_root, monkeypatch):
        from packages.orchestration.config import reset_config

        nothing = {"every": None, "jobs_left": None, "open_findings": None}
        assert upkeep_digest_counts(PROJECT, "0" * 32) == nothing
        mission_id, _ = _chain(PROJECT, ["completed"])
        monkeypatch.setenv("REMEDY_MISSION_UPKEEP_EVERY", "0")
        reset_config()
        try:
            assert upkeep_digest_counts(PROJECT, mission_id) == nothing
        finally:
            monkeypatch.delenv("REMEDY_MISSION_UPKEEP_EVERY")
            reset_config()


class TestTheUpkeepOfAMissionOverSeveralProjects:
    """DECISION F205 D7: the cadence counts the jobs of every repository; the upkeep job works, is
    measured and carries findings where the mission's next job works."""

    OTHER = "b" * 32

    def _mission(self, tmp_path):
        """Five completed jobs, three in the first project and two in the second, the second last;
        a finding open in one job of each project."""
        repos = {PROJECT: tmp_path / "first-repo", self.OTHER: tmp_path / "second-repo"}
        mission = create_mission(PROJECT, "Keep both repositories working",
                                 project_ids=(PROJECT, self.OTHER))
        jobs = []
        for index, project in enumerate((PROJECT, PROJECT, PROJECT, self.OTHER, self.OTHER)):
            job = JobPlan(job_title=f"job {index}", state=RunState.COMPLETED, project_id=project,
                          repo_path=str(repos[project]))
            save_job_plan(job)
            link_job_to_mission(PROJECT, mission.id, str(job.job_id),
                                "initial" if index == 0 else "follow_up")
            jobs.append(job)
        for job in (jobs[0], jobs[3]):
            _final_review(str(job.job_id), [{"id": "F-TASK-001", "severity": "repairable",
                                             "message": f"left by {job.job_title}", "task_id": "T001"}])
        return mission, jobs, repos

    def test_the_cadence_counts_the_completed_jobs_of_every_repository(self, data_root, tmp_path):
        mission, _jobs, _repos = self._mission(tmp_path)

        cadence = upkeep_cadence(PROJECT, mission.id)

        assert (cadence.completed, cadence.due) == (5, True)

    def test_the_upkeep_job_works_and_carries_where_the_chain_ends(self, data_root, tmp_path):
        mission, jobs, repos = self._mission(tmp_path)

        outcome = make_upkeep_job_if_due(PROJECT, mission.id)

        assert (outcome.job.project_id, outcome.job.repo_path) == (self.OTHER, str(repos[self.OTHER]))
        assert outcome.plan["repository"] == str(repos[self.OTHER])
        assert outcome.plan["findings"] == [finding_key(str(jobs[3].job_id), "T001", "F-TASK-001")]
        assert str(jobs[0].job_id) not in compile_upkeep_step(outcome.plan)
