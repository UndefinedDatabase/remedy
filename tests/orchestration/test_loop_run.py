"""F045 T002 — unit tests for materializing a loop as an ordinary job.

Every test writes its OWN remedy.toml under ``tmp_path`` and loads it with
``loop_spec.load_loop_specs``, so the real spec path is exercised rather than a
hand-built model. Every call passes an explicit ``save`` callable that appends
to a list, so no test touches the real job store, and an explicit ``date``, so
nothing here depends on the clock.

R-0344 counter-measure: no assertion in this file matches against a string that
carries a filesystem path. Every expected value is computed from the spec or
from the module under test, never from a fixture directory's name.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest

from packages.core.models import Job, RunState
from packages.orchestration.loop_run import (
    LOOP_REF_METADATA_KEY,
    LOOP_UNATTENDED_METADATA_KEY,
    LoopRunError,
    loop_to_job,
    render_goal_template,
)
from packages.orchestration.loop_spec import LoopSpec, load_loop_specs

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
