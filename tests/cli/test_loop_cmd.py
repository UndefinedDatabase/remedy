"""F045 T003 — `remedy loop list` and `remedy loop validate`, through the real table.

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

R-0344 counter-measure: no assertion here matches a string that carries a
filesystem path. ``tmp_path`` is used for the chdir, for the environment
variable and as a ``root`` argument, and never inside an expected value.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pytest

from apps.cli.command_catalog import CATALOG
from apps.cli.commands import collect_all_handlers
from packages.orchestration import storage
from packages.orchestration.loop_run import run_loop
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


def _dispatch(command_id: str) -> None:
    """Run the command the way the CLI does: registered handler, argparse namespace."""
    collect_all_handlers()[command_id](argparse.Namespace())


def _row(text: str, name: str) -> str:
    """The listed row whose first cell is *name*."""
    for line in text.splitlines():
        cells = line.split()
        if cells and cells[0] == name:
            return line
    raise AssertionError(f"no listed row for {name!r} in:\n{text}")


def test_a_manual_loop_lists_its_name_trigger_action_and_never(project, capsys):
    _write_config(project, MANUAL_JOB_LOOP)

    _dispatch("loop.list")

    row = _row(capsys.readouterr().out, "nightly-tidy")
    assert "manual" in row
    assert "job" in row
    assert "never" in row
    assert "inert" not in row


def test_a_schedule_trigger_loop_is_listed_and_marked_inert(project, capsys):
    from apps.cli.commands.loop_cmd import INERT_TRIGGER_LEGEND

    _write_config(project, SCHEDULE_JOB_LOOP)

    _dispatch("loop.list")

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

    _dispatch("loop.list")

    row = _row(capsys.readouterr().out, "nightly-tidy")
    assert "never" not in row
    assert stored.created_at.isoformat() in row
    assert stored.state.value in row


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
