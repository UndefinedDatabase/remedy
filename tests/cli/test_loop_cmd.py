"""F045 T003 — `remedy loop list`, `validate` and `run`, through the real table.

Every test dispatches through ``collect_all_handlers()`` with an
``argparse.Namespace`` and never by importing a ``_cmd_*`` function directly:
reaching a command through the REGISTERED table is what proves it is wired, and
an importable-but-unreachable command is exactly the blind spot a green import
check would miss. Precedent: ``tests/cli/test_stats_cost.py``.

Isolation, in every test that runs a command: the working directory is
``tmp_path``, so the ``remedy.toml`` the test wrote is the config the command
finds, AND ``REMEDY_DATA_DIR`` points at ``tmp_path``, so the last-run lookup
reads a job store under it. The second is not optional — the chdir alone would
leave that lookup pointed at the operator's real store.

``apps.cli.commands.loop_cmd`` is imported INSIDE the tests that need its own
constants rather than at module level, so that against a tree where the
module does not exist yet each test fails on its own assertion instead of the
whole file dying at collection.

``loop run`` WRITES, so its tests add one more isolation layer: they register
their own project with ``project_registry.save_project`` under the same
``REMEDY_DATA_DIR``, which is the supported route the CLI tests already use
(``tests/cli/test_stats_cost.py``, ``tests/cli/test_project_current.py``), and
they pass that project's id on the namespace. The command is then invoked with
no ``root``, exactly as an operator invokes it, and every job it writes still
lands under ``tmp_path`` — the operator's real store is never reached.

R-0344 counter-measure: no assertion here matches a string that carries a
filesystem path. ``tmp_path`` is used for the chdir, for the environment
variable and as a ``root`` argument, and never inside an expected value.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pytest

from apps.cli.command_catalog import CATALOG
from apps.cli.commands import collect_all_handlers
from packages.core.models import RunState
from packages.orchestration import storage
from packages.orchestration.loop_run import LOOP_REF_METADATA_KEY, run_loop
from packages.orchestration.loop_spec import INERT_TRIGGER_NOTICE, load_loop_specs

LOOP_COMMANDS = ("loop.list", "loop.validate")

MANUAL_JOB_LOOP = """
[[loop]]
name = "nightly-tidy"

[loop.action]
kind = "job"
goal_template = "tidy {project} on {date}"
"""

SCHEDULE_JOB_LOOP = """
[[loop]]
name = "weekly-sweep"

[loop.trigger]
kind = "schedule"
schedule = "0 3 * * 1"

[loop.action]
kind = "job"
goal_template = "sweep {project}"
"""

TWO_BROKEN_LOOPS = """
[[loop]]
name = "missing-template"

[loop.action]
kind = "job"

[[loop]]
name = "bad-variable"

[loop.action]
kind = "job"
goal_template = "do {nonsense}"
"""


@pytest.fixture
def project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Config and job store both under tmp_path; the real ones are never touched."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    return tmp_path


def _write_config(root: Path, body: str) -> None:
    (root / "remedy.toml").write_text(body, encoding="utf-8")


@pytest.fixture
def registered_project(project: Path, monkeypatch: pytest.MonkeyPatch) -> str:
    """A registered project id inside the isolated data root, so `select_project` resolves.

    The supported route the CLI tests already use: build a ``RemyProject`` and
    ``save_project`` it under ``REMEDY_DATA_DIR``. No registry internal is
    touched. ``REMEDY_PROJECT`` is cleared so only the explicit id decides.
    """
    from packages.orchestration.project_registry import RemyProject, save_project

    monkeypatch.delenv("REMEDY_PROJECT", raising=False)
    record = RemyProject(name="Loop Run Test", slug="loop-run-test")
    save_project(record)
    return str(record.id)


def _dispatch(command_id: str) -> None:
    """Run the command the way the CLI does: registered handler, argparse namespace."""
    collect_all_handlers()[command_id](argparse.Namespace())


def _dispatch_with(command_id: str, **attributes: object) -> None:
    """The same dispatch, with the attributes argparse would have parsed onto the namespace."""
    collect_all_handlers()[command_id](argparse.Namespace(**attributes))


def _stored_jobs() -> list:
    """Every job actually PERSISTED, read back through the store the command wrote to."""
    jobs, _degraded, _skipped = storage.list_jobs_safe()
    return jobs


def _row(text: str, name: str) -> str:
    """The listed row whose first cell is *name*."""
    for line in text.splitlines():
        cells = line.split()
        if cells and cells[0] == name:
            return line
    raise AssertionError(f"no listed row for {name!r} in:\n{text}")


def test_a_manual_loop_lists_its_name_trigger_action_and_never(project, capsys):
    _write_config(project, MANUAL_JOB_LOOP)

    _dispatch_with("loop.list", json=False)

    row = _row(capsys.readouterr().out, "nightly-tidy")
    assert "manual" in row
    assert "job" in row
    assert "never" in row
    assert "inert" not in row


def test_a_schedule_trigger_loop_is_listed_and_marked_inert(project, capsys):
    from apps.cli.commands.loop_cmd import INERT_TRIGGER_LEGEND

    _write_config(project, SCHEDULE_JOB_LOOP)

    _dispatch_with("loop.list", json=False)

    out = capsys.readouterr().out
    row = _row(out, "weekly-sweep")
    assert "schedule" in row
    assert "inert" in row
    assert INERT_TRIGGER_LEGEND in out
    # The actual pin: a listing has run nothing, so the RUN notice — whose text
    # claims a loop "ran on demand" — must never appear anywhere in a listing.
    assert INERT_TRIGGER_NOTICE not in out


def test_after_one_real_firing_the_row_shows_that_run(project, capsys):
    _write_config(project, MANUAL_JOB_LOOP)
    (spec,) = load_loop_specs()
    outcome = run_loop(spec, project_id="remedy", date="2026-08-13", root=project)
    stored = storage.load_job(outcome.job.id, project)

    _dispatch_with("loop.list", json=False)

    row = _row(capsys.readouterr().out, "nightly-tidy")
    assert "never" not in row
    assert stored.created_at.isoformat() in row
    assert stored.state.value in row


def test_json_output_carries_last_run_created_at_and_state(project, capsys):
    _write_config(project, MANUAL_JOB_LOOP)
    (spec,) = load_loop_specs()
    outcome = run_loop(spec, project_id="remedy", date="2026-08-13", root=project)
    stored = storage.load_job(outcome.job.id, project)

    _dispatch_with("loop.list", json=True)

    data = json.loads(capsys.readouterr().out)
    row = next(item for item in data["loops"] if item["name"] == "nightly-tidy")
    assert row["last_run_created_at"] == stored.created_at.isoformat()
    assert row["last_run_state"] == stored.state.value


def test_json_output_last_run_is_null_when_never_ran(project, capsys):
    _write_config(project, MANUAL_JOB_LOOP)

    _dispatch_with("loop.list", json=True)

    data = json.loads(capsys.readouterr().out)
    row = next(item for item in data["loops"] if item["name"] == "nightly-tidy")
    assert row["last_run_created_at"] is None
    assert row["last_run_state"] is None


def test_validate_reports_every_error_and_exits_non_zero(project, capsys):
    from apps.cli.commands import loop_cmd

    _write_config(project, TWO_BROKEN_LOOPS)

    with pytest.raises(SystemExit) as exc:
        _dispatch("loop.validate")

    assert exc.value.code == loop_cmd.EXIT_ERROR
    assert exc.value.code != 0
    err = capsys.readouterr().err
    reported = [line for line in err.splitlines() if line.startswith("loop '")]
    assert len(reported) == 2, err
    assert any("missing-template" in line for line in reported)
    assert any("bad-variable" in line for line in reported)


def test_validate_on_a_valid_config_exits_zero(project, capsys):
    _write_config(project, MANUAL_JOB_LOOP)

    _dispatch("loop.validate")          # no SystemExit

    assert "no errors" in capsys.readouterr().out


def test_both_commands_are_registered_and_in_the_catalog():
    handlers = collect_all_handlers()
    catalog_ids = {entry.command_id for entry in CATALOG}

    for command_id in LOOP_COMMANDS:
        assert command_id in handlers
        assert command_id in catalog_ids


def test_run_with_yes_materializes_a_planned_job_carrying_the_loop_ref(
        project, registered_project, capsys):
    _write_config(project, MANUAL_JOB_LOOP)

    _dispatch_with("loop.run", name="nightly-tidy", project=registered_project, yes=True)

    out = capsys.readouterr().out
    (stored,) = _stored_jobs()          # read back through the STORE, not the text
    assert stored.metadata[LOOP_REF_METADATA_KEY] == "nightly-tidy"
    assert stored.state == RunState.PLANNED
    assert str(stored.id) in out


def test_run_prints_the_next_command_naming_the_job_it_just_created(
        project, registered_project, capsys):
    _write_config(project, MANUAL_JOB_LOOP)

    _dispatch_with("loop.run", name="nightly-tidy", project=registered_project, yes=True)

    out = capsys.readouterr().out
    (stored,) = _stored_jobs()
    assert f"remedy job run {stored.id}" in out


def test_an_unknown_loop_name_is_refused_and_names_the_loops_that_exist(
        project, registered_project, capsys):
    from apps.cli.commands import loop_cmd

    _write_config(project, MANUAL_JOB_LOOP)

    with pytest.raises(SystemExit) as exc:
        _dispatch_with("loop.run", name="midday-tidy", project=registered_project, yes=True)

    assert exc.value.code == loop_cmd.EXIT_ERROR
    assert exc.value.code != 0
    err = capsys.readouterr().err
    assert "midday-tidy" in err          # what was asked for
    assert "nightly-tidy" in err         # what actually exists
    assert _stored_jobs() == []


def test_without_yes_a_non_tty_stdin_is_refused_rather_than_prompted(
        project, registered_project, monkeypatch, capsys):
    from apps.cli.commands import loop_cmd

    _write_config(project, MANUAL_JOB_LOOP)
    monkeypatch.setattr(loop_cmd, "_stdin_is_a_tty", lambda: False)

    with pytest.raises(SystemExit) as exc:
        _dispatch_with("loop.run", name="nightly-tidy", project=registered_project, yes=False)

    assert exc.value.code == loop_cmd.EXIT_USAGE
    assert exc.value.code != 0
    assert "--yes" in capsys.readouterr().err
    assert _stored_jobs() == []


def test_a_tty_stdin_answering_yes_materializes(
        project, registered_project, monkeypatch, capsys):
    from apps.cli.commands import loop_cmd

    _write_config(project, MANUAL_JOB_LOOP)
    monkeypatch.setattr(loop_cmd, "_stdin_is_a_tty", lambda: True)
    monkeypatch.setattr("builtins.input", lambda prompt="": "y")

    _dispatch_with("loop.run", name="nightly-tidy", project=registered_project, yes=False)

    (stored,) = _stored_jobs()
    assert stored.state == RunState.PLANNED
    assert str(stored.id) in capsys.readouterr().out


def test_a_tty_stdin_declining_creates_nothing_and_does_not_raise(
        project, registered_project, monkeypatch, capsys):
    from apps.cli.commands import loop_cmd

    _write_config(project, MANUAL_JOB_LOOP)
    monkeypatch.setattr(loop_cmd, "_stdin_is_a_tty", lambda: True)
    monkeypatch.setattr("builtins.input", lambda prompt="": "n")

    # No pytest.raises: declining is a normal, successful return.
    _dispatch_with("loop.run", name="nightly-tidy", project=registered_project, yes=False)

    assert _stored_jobs() == []
    assert "Cancelled" in capsys.readouterr().out


def test_running_an_inert_loop_prints_the_run_notice_and_still_stops_at_planned(
        project, registered_project, capsys):
    _write_config(project, SCHEDULE_JOB_LOOP)

    _dispatch_with("loop.run", name="weekly-sweep", project=registered_project, yes=True)

    out = capsys.readouterr().out
    # Correct HERE and wrong in a listing (R-0355): a run really did happen.
    assert INERT_TRIGGER_NOTICE in out
    # The "a loop never implies --yes" pin: an inert trigger changes nothing
    # about where the job stops.
    (stored,) = _stored_jobs()
    assert stored.state == RunState.PLANNED


def test_loop_run_is_registered_and_in_the_catalog():
    handlers = collect_all_handlers()
    catalog_ids = {entry.command_id for entry in CATALOG}

    assert "loop.run" in handlers
    assert "loop.run" in catalog_ids
