"""F045 T002 — unit tests for materializing a loop as an ordinary job.

Every test writes its OWN remedy.toml under ``tmp_path`` and loads it with
``loop_spec.load_loop_specs``, so the real spec path is exercised rather than a
hand-built model. Every call passes an explicit ``date``, so nothing here
depends on the clock. MOST calls also pass an explicit ``save`` callable that
appends to a list; the three store tests near the end pass NONE and isolate
through ``root`` instead, because reaching the real store through ``root`` is
the very property they exist to prove.

The LAST test is the T003 end-to-end path — loop, job, cycle loop, report on
disk. It isolates through ``REMEDY_DATA_DIR`` as well as ``root``, because the
report's location comes from ``jobs_dir()`` and no ``root=`` argument reaches
it.

R-0344 counter-measure: no assertion in this file matches against a string that
carries a filesystem path. Every expected value is computed from the spec or
from the module under test, never from a fixture directory's name.

The two ``last_run_for_loop`` tests are the one deliberate exception to the
"spec comes from a real remedy.toml" rule: their subject is the job-store scan
and its ORDERING, so they hand-build jobs with distinct ``created_at`` values —
two jobs materialized inside one test would share a clock reading too closely
for "most recent" to mean anything. Everything touching mission state or the
job store passes an explicit ``root``, so no test reads or writes a real store.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from packages.core.models import Job, RunState
from packages.orchestration import mission_state, storage
from packages.orchestration.builder_models import BuilderOutput, TaskExecutionContext
from packages.orchestration.long_run_executor import (
    TERMINAL_ALL_GREEN,
    VERIFY_PASSED,
    CycleLimits,
    TaskAttempt,
    run_cycles,
)
from packages.orchestration.loop_run import (
    LOOP_REF_METADATA_KEY,
    LOOP_UNATTENDED_METADATA_KEY,
    LoopRunError,
    last_run_for_loop,
    loop_to_job,
    render_goal_template,
    run_loop,
)
from packages.orchestration.loop_spec import (
    INERT_TRIGGER_NOTICE,
    LoopSpec,
    load_loop_specs,
)
from packages.orchestration.run_report import report_path

DEADLINE_ISO = "2026-09-01T00:00:00+00:00"


def _spec(tmp_path: Path, body: str) -> LoopSpec:
    """Write one loop table and load it back through the real spec path."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    path = tmp_path / "remedy.toml"
    path.write_text(body, encoding="utf-8")
    (spec,) = load_loop_specs(path)
    return spec


def _job_loop(tmp_path: Path, *, template: str = "tidy {project} on {date}",
              unattended: bool = False, extra: str = "") -> LoopSpec:
    return _spec(tmp_path, f"""
[[loop]]
name = "nightly-tidy"
unattended = {str(unattended).lower()}

[loop.action]
kind = "job"
goal_template = "{template}"
{extra}
""")


def test_job_action_loop_materializes_a_normal_job(tmp_path: Path) -> None:
    spec = _job_loop(tmp_path, template="tidy {project} on {date}")
    saved: list[Job] = []

    job = loop_to_job(spec, project_id="remedy", date="2026-08-13", save=saved.append)

    assert job.user_prompt == "tidy remedy on 2026-08-13"
    assert job.name == "tidy remedy on 2026-08-13"
    assert job.project_id == "remedy"
    assert job.metadata["project_id"] == "remedy"


def test_loop_ref_metadata_carries_the_loop_name(tmp_path: Path) -> None:
    spec = _job_loop(tmp_path)
    saved: list[Job] = []

    job = loop_to_job(spec, project_id="remedy", date="2026-08-13", save=saved.append)

    assert job.metadata[LOOP_REF_METADATA_KEY] == spec.name
    assert job.metadata[LOOP_REF_METADATA_KEY] == "nightly-tidy"


def test_materialized_job_stops_at_planned_and_is_saved_once(tmp_path: Path) -> None:
    spec = _job_loop(tmp_path)
    saved: list[Job] = []

    job = loop_to_job(spec, project_id="remedy", date="2026-08-13", save=saved.append)

    assert job.state is RunState.PLANNED
    assert len(saved) == 1
    assert saved[0] is job


def test_both_template_variables_are_substituted(tmp_path: Path) -> None:
    spec = _job_loop(tmp_path, template="sweep {project} at {date} for {project}")
    saved: list[Job] = []

    job = loop_to_job(spec, project_id="acme", date="2026-01-02", save=saved.append)

    assert job.user_prompt == "sweep acme at 2026-01-02 for acme"
    assert "{" not in job.user_prompt


def test_template_without_placeholders_passes_through(tmp_path: Path) -> None:
    spec = _job_loop(tmp_path, template="run the nightly tidy")
    saved: list[Job] = []

    job = loop_to_job(spec, project_id="acme", date="2026-01-02", save=saved.append)

    assert job.user_prompt == "run the nightly tidy"


def test_loop_budgets_map_onto_job_budgets(tmp_path: Path) -> None:
    spec = _job_loop(tmp_path, extra=f"""
[loop.budgets]
max_total_tokens = 50000
max_provider_calls = 12
max_wall_clock_minutes = 30
max_cost_usd = 1.5
deadline = "{DEADLINE_ISO}"
""")
    saved: list[Job] = []

    job = loop_to_job(spec, project_id="remedy", date="2026-08-13", save=saved.append)

    assert job.budgets is not None
    assert job.budgets.max_total_tokens == spec.budgets.max_total_tokens == 50000
    assert job.budgets.max_provider_calls == spec.budgets.max_provider_calls == 12
    assert job.budgets.max_wall_clock_minutes == spec.budgets.max_wall_clock_minutes == 30
    assert job.budgets.max_cost_usd == spec.budgets.max_cost_usd == 1.5
    assert job.budgets.deadline == datetime.fromisoformat(spec.budgets.deadline)
    assert job.budgets.deadline.tzinfo is not None


def test_loop_without_budgets_produces_a_job_without_budgets(tmp_path: Path) -> None:
    spec = _job_loop(tmp_path)
    saved: list[Job] = []

    job = loop_to_job(spec, project_id="remedy", date="2026-08-13", save=saved.append)

    assert spec.budgets is None
    assert job.budgets is None


def test_unattended_is_recorded_and_never_changes_the_state(tmp_path: Path) -> None:
    """The 'a loop never implies --yes' pin: unattended is audit data, not approval."""
    attended = _job_loop(tmp_path / "off", unattended=False)
    unattended = _job_loop(tmp_path / "on", unattended=True)
    saved: list[Job] = []

    attended_job = loop_to_job(attended, project_id="remedy", date="2026-08-13",
                               save=saved.append)
    unattended_job = loop_to_job(unattended, project_id="remedy", date="2026-08-13",
                                 save=saved.append)

    assert attended_job.metadata[LOOP_UNATTENDED_METADATA_KEY] is False
    assert unattended_job.metadata[LOOP_UNATTENDED_METADATA_KEY] is True
    assert unattended_job.state == attended_job.state
    assert unattended_job.state is RunState.PLANNED
    assert attended_job.state is RunState.PLANNED


def test_mission_action_loop_is_refused_by_loop_to_job(tmp_path: Path) -> None:
    spec = _spec(tmp_path, """
[[loop]]
name = "weekly-review"

[loop.action]
kind = "mission"
mission = "review"
""")
    saved: list[Job] = []

    with pytest.raises(LoopRunError) as excinfo:
        loop_to_job(spec, project_id="remedy", date="2026-08-13", save=saved.append)

    assert "mission" in str(excinfo.value)
    assert saved == []


def test_unknown_placeholder_raises_loop_run_error_not_key_error() -> None:
    with pytest.raises(LoopRunError) as excinfo:
        render_goal_template("tidy {repo} on {date}", project="remedy",
                             date="2026-08-13")

    assert "repo" in str(excinfo.value)
    assert not isinstance(excinfo.value, KeyError)


def _mission_loop(tmp_path: Path, *, template: str = "review {project} for {date}",
                  unattended: bool = False, trigger: str = "") -> LoopSpec:
    return _spec(tmp_path, f"""
[[loop]]
name = "weekly-review"
unattended = {str(unattended).lower()}
{trigger}
[loop.action]
kind = "mission"
mission = "{template}"
""")


def _stored_job(name: str, *, loop_ref: str, created_at: datetime) -> Job:
    """A job built by hand so its ``created_at`` is explicit, not a clock read."""
    return Job(name=name, user_prompt=name, state=RunState.PLANNED,
               created_at=created_at, metadata={LOOP_REF_METADATA_KEY: loop_ref})


def test_run_loop_on_a_job_action_returns_a_planned_job_without_a_mission(
        tmp_path: Path) -> None:
    spec = _job_loop(tmp_path)
    saved: list[Job] = []

    outcome = run_loop(spec, project_id="remedy", date="2026-08-13",
                       save=saved.append, root=tmp_path)

    assert outcome.job.state is RunState.PLANNED
    assert outcome.job.metadata[LOOP_REF_METADATA_KEY] == spec.name
    assert outcome.mission_id is None


def test_run_loop_on_a_mission_action_creates_a_mission_with_the_rendered_goal(
        tmp_path: Path) -> None:
    spec = _mission_loop(tmp_path, template="review {project} for {date}")
    saved: list[Job] = []

    outcome = run_loop(spec, project_id="remedy", date="2026-08-13",
                       save=saved.append, root=tmp_path)

    assert outcome.mission_id is not None
    mission = mission_state.load_mission("remedy", outcome.mission_id, root=tmp_path)
    assert mission.goal == "review remedy for 2026-08-13"
    assert outcome.mission_id == mission.id


def test_mission_path_records_provenance_on_the_job_not_on_the_mission(
        tmp_path: Path) -> None:
    """DECISION F045 D5: loop_ref rides on the JOB; the mission stays reachable."""
    spec = _mission_loop(tmp_path)
    saved: list[Job] = []

    outcome = run_loop(spec, project_id="remedy", date="2026-08-13",
                       save=saved.append, root=tmp_path)

    assert outcome.job.metadata[LOOP_REF_METADATA_KEY] == spec.name
    assert outcome.job.metadata["mission_id"] == outcome.mission_id
    mission = mission_state.load_mission("remedy", outcome.mission_id, root=tmp_path)
    assert hasattr(mission, "loop_ref") is False


def test_mission_job_is_the_missions_initial_link(tmp_path: Path) -> None:
    spec = _mission_loop(tmp_path)
    saved: list[Job] = []

    outcome = run_loop(spec, project_id="remedy", date="2026-08-13",
                       save=saved.append, root=tmp_path)

    mission = mission_state.load_mission("remedy", outcome.mission_id, root=tmp_path)
    (link,) = mission.job_links
    assert link.job_id == str(outcome.job.id)
    assert link.role == mission_state.MISSION_ROLE_INITIAL


def test_unattended_mission_loop_is_recorded_and_still_stops_at_planned(
        tmp_path: Path) -> None:
    """The 'a loop never implies --yes' pin for the mission path."""
    attended = _mission_loop(tmp_path / "off", unattended=False)
    unattended = _mission_loop(tmp_path / "on", unattended=True)
    saved: list[Job] = []

    attended_out = run_loop(attended, project_id="remedy", date="2026-08-13",
                            save=saved.append, root=tmp_path / "off")
    unattended_out = run_loop(unattended, project_id="remedy", date="2026-08-13",
                              save=saved.append, root=tmp_path / "on")

    assert attended_out.job.metadata[LOOP_UNATTENDED_METADATA_KEY] is False
    assert unattended_out.job.metadata[LOOP_UNATTENDED_METADATA_KEY] is True
    assert unattended_out.job.state == attended_out.job.state
    assert unattended_out.job.state is RunState.PLANNED


def test_inert_trigger_yields_the_notice_and_still_produces_a_planned_job(
        tmp_path: Path) -> None:
    spec = _mission_loop(tmp_path, trigger='\n[loop.trigger]\nkind = "schedule"\n'
                                           'schedule = "0 9 * * 1"')
    saved: list[Job] = []

    outcome = run_loop(spec, project_id="remedy", date="2026-08-13",
                       save=saved.append, root=tmp_path)

    assert spec.is_inert is True
    assert outcome.notice == INERT_TRIGGER_NOTICE
    assert outcome.job.state is RunState.PLANNED


def test_manual_trigger_yields_no_notice(tmp_path: Path) -> None:
    spec = _job_loop(tmp_path)
    saved: list[Job] = []

    outcome = run_loop(spec, project_id="remedy", date="2026-08-13",
                       save=saved.append, root=tmp_path)

    assert spec.is_inert is False
    assert outcome.notice is None


def test_last_run_for_loop_returns_the_most_recent_run_or_none(tmp_path: Path) -> None:
    older = _stored_job("older run", loop_ref="nightly-tidy",
                        created_at=datetime(2026, 8, 11, tzinfo=timezone.utc))
    newer = _stored_job("newer run", loop_ref="nightly-tidy",
                        created_at=datetime(2026, 8, 13, tzinfo=timezone.utc))
    storage.save_job(older, tmp_path)
    storage.save_job(newer, tmp_path)

    assert last_run_for_loop("nightly-tidy", root=tmp_path).id == newer.id
    assert last_run_for_loop("never-ran", root=tmp_path) is None


def test_last_run_for_loop_ignores_another_loops_run(tmp_path: Path) -> None:
    mine = _stored_job("mine", loop_ref="nightly-tidy",
                       created_at=datetime(2026, 8, 11, tzinfo=timezone.utc))
    theirs = _stored_job("theirs", loop_ref="weekly-review",
                         created_at=datetime(2026, 8, 13, tzinfo=timezone.utc))
    storage.save_job(mine, tmp_path)
    storage.save_job(theirs, tmp_path)

    found = last_run_for_loop("nightly-tidy", root=tmp_path)
    assert found is not None
    assert found.id == mine.id
    assert found.metadata[LOOP_REF_METADATA_KEY] == "nightly-tidy"


def test_mission_run_persists_the_mission_text_on_the_stored_job(
        tmp_path: Path) -> None:
    """R-0351: the STORED record carries the mission text, not only the object.

    Asserting against ``outcome.job`` would pass either way — reading the
    in-memory object is exactly the defect — so this reads the job back.
    """
    spec = _mission_loop(tmp_path)

    outcome = run_loop(spec, project_id="remedy", date="2026-08-13", root=tmp_path)

    expected_goal = render_goal_template(spec.action.mission, project="remedy",
                                         date="2026-08-13")
    stored = storage.load_job(outcome.job.id, tmp_path)
    assert stored.mission == expected_goal


def test_run_loop_root_isolates_the_job_store_on_the_mission_path(
        tmp_path: Path) -> None:
    """R-0352: run with ``root``, find that same run with the SAME ``root``."""
    spec = _mission_loop(tmp_path)

    outcome = run_loop(spec, project_id="remedy", date="2026-08-13", root=tmp_path)

    found = last_run_for_loop(spec.name, root=tmp_path)
    assert found is not None
    assert found.id == outcome.job.id


def test_run_loop_root_isolates_the_job_store_on_the_job_path(
        tmp_path: Path) -> None:
    """R-0352 for the JOB action kind: both paths honour the caller's root."""
    spec = _job_loop(tmp_path)

    outcome = run_loop(spec, project_id="remedy", date="2026-08-13", root=tmp_path)

    found = last_run_for_loop(spec.name, root=tmp_path)
    assert found is not None
    assert found.id == outcome.job.id


# ---------------------------------------------------------------------------
# T003 — the one end-to-end path: loop -> job -> cycle loop -> report on disk
# ---------------------------------------------------------------------------


class _CountingProvider:
    """A builder that always returns verifiable output and counts its calls."""

    def __init__(self) -> None:
        self.calls = 0

    def __call__(self, context: TaskExecutionContext) -> BuilderOutput:
        self.calls += 1
        return BuilderOutput(
            summary=f"did {context.task_description}",
            proposed_changes=[f"write docs for {context.task_description}"],
        )


class _SteppingClock:
    """A clock that advances by a fixed step per read, so nothing here sleeps."""

    def __init__(self) -> None:
        self.now = datetime(2026, 8, 13, 12, 0, 0, tzinfo=timezone.utc)

    def __call__(self) -> datetime:
        current = self.now
        self.now = self.now + timedelta(seconds=1)
        return current


def _completing_step(job: Job, provider_call) -> TaskAttempt:
    """Complete the first PENDING task, through the counted provider seam."""
    task = next((t for t in job.tasks if t.status == RunState.PENDING), None)
    if task is None:
        return TaskAttempt()
    provider_call(
        TaskExecutionContext(
            job_id=job.id,
            job_prompt=job.user_prompt,
            task_id=task.id,
            task_type=task.inputs.get("task_type", "unknown"),
            task_description=task.description,
        )
    )
    task.status = RunState.COMPLETED
    if all(t.status == RunState.COMPLETED for t in job.tasks):
        job.state = RunState.COMPLETED
    return TaskAttempt(task_id=task.id, executed=True, verified=True)


def _passing_verify(job: Job, cycle_index: int, verify_command) -> str:
    return VERIFY_PASSED


@pytest.fixture
def isolated_data_root(tmp_path: Path, monkeypatch) -> Path:
    """The one data root the end-to-end run may touch.

    ``report_path`` resolves through ``jobs_dir()``, which honours no ``root=``
    argument — only ``REMEDY_DATA_DIR``. So the report half of the path can be
    isolated ONLY through the environment, and the same directory is handed to
    ``run_loop`` as ``root`` so the job store and the evidence area are one
    place (the R-0351/R-0352 counter-measure).
    """
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


def test_a_fixture_loop_runs_end_to_end_and_its_report_names_the_loop(
        tmp_path: Path, isolated_data_root: Path) -> None:
    """The F045 acceptance path in one test: a loop materializes a job, that
    job runs through the STANDARD cycle loop with a fake provider, and the
    report written at the terminal state names the loop it came from.

    The fixture supplies NO task: ``run_loop`` runs ``job_runner.plan_job``, so
    the job it hands back is already planned. Nothing asserted here is
    fixture-decided — the loop ref comes from ``loop_to_job``, the tasks from
    the planner, the ``- Loop:`` line from ``run_report``, and the last
    assertion reads the job back off disk rather than out of ``outcome.job``
    (R-0344/R-0351).
    """
    spec = _job_loop(tmp_path / "config")

    outcome = run_loop(spec, project_id="remedy", date="2026-08-13",
                       root=isolated_data_root)
    job = outcome.job
    assert job.metadata[LOOP_REF_METADATA_KEY] == spec.name

    provider = _CountingProvider()

    result = run_cycles(
        job, CycleLimits(max_cycles=5), provider,
        task_step=_completing_step, verify=_passing_verify,
        clock=_SteppingClock(),
    )

    # OBSERVED at the R14 gate, not ordered in advance: the planner gives the
    # job ``job_runner._PLANNING_TASK_SPECS`` — three tasks — and this step
    # completes one per cycle, so three cycles and three provider calls end the
    # run all green.
    assert result.terminal_status == TERMINAL_ALL_GREEN
    assert len(job.tasks) == 3
    assert result.cycles_run == 3
    assert provider.calls == 3
    assert job.state is RunState.COMPLETED

    written = report_path(str(job.id))
    assert written.is_file()
    expected_line = f"- Loop: {spec.name}"
    text = written.read_text(encoding="utf-8")
    assert [line for line in text.splitlines() if line == expected_line] == [expected_line]

    stored = storage.load_job(job.id, isolated_data_root)
    assert stored.metadata[LOOP_REF_METADATA_KEY] == spec.name
