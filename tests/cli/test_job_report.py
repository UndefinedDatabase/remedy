"""F053 T002 — `remedy job report` renders the run report.

Three modes on ONE command name (the F047 `job resume` pattern): bare and
`--json` keep the pre-existing progress view exactly as it was, `--final`
renders the F053 account of a terminal run, `--interim` renders the same
structure for a run still going, loudly labeled.

The property this file exists to defend: rendering a snapshot must not perturb
the run it is describing.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from apps.cli.command_catalog import CATALOG, get_command
from apps.cli.commands.job import _cmd_job_run_report
from packages.core.models import Job, RunState, Task
from packages.orchestration.run_report import report_path
from packages.orchestration.storage import save_job

pytestmark = pytest.mark.integration

UTC = timezone.utc
T0 = datetime(2026, 7, 31, 12, 0, 0, tzinfo=UTC)


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path: Path, monkeypatch) -> Path:
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


def saved_job(*, state: RunState = RunState.COMPLETED,
              terminal: str = "all_green",
              task_status: RunState = RunState.COMPLETED) -> Job:
    job = Job(
        name="report-job",
        user_prompt="build the thing",
        mission="Build the thing",
        tasks=[Task(description=f"task {i}", inputs={"task_type": "documentation"})
               for i in range(2)],
        state=state,
        metadata={"target_repo": "/tmp/repo", "cycle_terminal_status": terminal},
    )
    for task in job.tasks:
        task.status = task_status
    save_job(job)
    return job


class TestFinalMode:

    def test_it_renders_the_run_report(self, capsys):
        job = saved_job()
        _cmd_job_run_report(str(job.id))
        out = capsys.readouterr().out
        assert "# Run report — report-job" in out
        assert "- Terminal status: all_green" in out
        assert "## Recommended next action" in out

    def test_it_is_not_labeled_as_a_snapshot(self, capsys):
        job = saved_job()
        _cmd_job_run_report(str(job.id))
        assert "INTERIM SNAPSHOT" not in capsys.readouterr().out

    def test_a_short_job_id_prefix_resolves(self, capsys):
        job = saved_job()
        _cmd_job_run_report(str(job.id)[:8])
        assert "# Run report — report-job" in capsys.readouterr().out

    def test_it_reads_disk_sources_not_only_the_job(self, capsys):
        """The mission and both task lines come from the persisted job."""
        job = saved_job()
        _cmd_job_run_report(str(job.id))
        out = capsys.readouterr().out
        assert "- Mission: Build the thing" in out
        assert out.count("- `") >= 2


class TestInterimMode:

    def test_it_renders_the_loud_snapshot_label(self, capsys):
        job = saved_job(state=RunState.RUNNING, terminal="",
                        task_status=RunState.PENDING)
        _cmd_job_run_report(str(job.id), interim=True)
        first = capsys.readouterr().out.splitlines()[0]
        assert first.startswith("> **INTERIM SNAPSHOT — run still in progress")
        assert "rendered at" in first

    def test_it_keeps_the_same_section_structure_as_final(self, capsys):
        job = saved_job(state=RunState.RUNNING, terminal="",
                        task_status=RunState.PENDING)
        _cmd_job_run_report(str(job.id), interim=True)
        interim = capsys.readouterr().out
        _cmd_job_run_report(str(job.id))
        final = capsys.readouterr().out
        assert _headings(interim) == _headings(final)

    def test_interim_never_mutates_job_state(self, capsys):
        """The whole point: looking at a running job must not disturb it."""
        job = saved_job(state=RunState.RUNNING, terminal="",
                        task_status=RunState.PENDING)
        before = _job_file(job).read_bytes()
        _cmd_job_run_report(str(job.id), interim=True)
        capsys.readouterr()
        assert _job_file(job).read_bytes() == before

    def test_interim_writes_no_report_file(self, capsys):
        """Only the terminal hook writes report.md — never a render."""
        job = saved_job(state=RunState.RUNNING, terminal="",
                        task_status=RunState.PENDING)
        _cmd_job_run_report(str(job.id), interim=True)
        capsys.readouterr()
        assert not report_path(str(job.id)).exists()

    def test_final_mode_writes_no_report_file_either(self, capsys):
        job = saved_job()
        _cmd_job_run_report(str(job.id))
        capsys.readouterr()
        assert not report_path(str(job.id)).exists()


class TestJsonMode:

    def test_it_emits_the_structured_sources(self, capsys):
        job = saved_job()
        _cmd_job_run_report(str(job.id), json_output=True)
        payload = json.loads(capsys.readouterr().out)
        assert payload["job_name"] == "report-job"
        assert payload["terminal_status"] == "all_green"
        assert len(payload["tasks"]) == 2
        assert "status_mirror" in payload

    def test_the_json_is_not_the_rendered_markdown(self, capsys):
        job = saved_job()
        _cmd_job_run_report(str(job.id), json_output=True)
        out = capsys.readouterr().out
        assert "# Run report" not in out

    def test_json_and_interim_agree_on_the_sources(self, capsys):
        job = saved_job()
        _cmd_job_run_report(str(job.id), json_output=True)
        payload = json.loads(capsys.readouterr().out)
        _cmd_job_run_report(str(job.id), interim=True)
        text = capsys.readouterr().out
        assert payload["job_name"] in text


class TestUnknownJob:

    def test_it_exits_cleanly_without_a_traceback(self, capsys):
        with pytest.raises(SystemExit) as exc:
            _cmd_job_run_report("ffffffff-ffff-4fff-8fff-ffffffffffff")
        assert exc.value.code == 1
        captured = capsys.readouterr()
        assert "Error: job not found" in captured.err
        assert "Traceback" not in captured.err

    def test_json_mode_reports_the_error_as_json(self, capsys):
        with pytest.raises(SystemExit):
            _cmd_job_run_report("ffffffff-ffff-4fff-8fff-ffffffffffff",
                                json_output=True)
        payload = json.loads(capsys.readouterr().out)
        assert payload["error"] == "job_not_found"


class TestOneCommandThreeModes:
    """The F047 lesson: extend the existing name, never shadow it."""

    def test_the_catalog_registers_job_report_exactly_once(self):
        matches = [e for e in CATALOG if e.command_id == "job.report"]
        assert len(matches) == 1, matches

    def test_the_command_declares_both_new_flags(self):
        names = [a.name for a in get_command("job.report").args]
        assert "--final" in names and "--interim" in names
        assert "--json" in names          # the pre-existing option survives

    def test_the_new_flags_are_flags_not_valued_options(self):
        for arg in get_command("job.report").args:
            if arg.name in ("--final", "--interim"):
                assert arg.is_flag, arg.name
                assert not arg.required, arg.name

    def test_the_bare_progress_view_is_untouched(self, capsys):
        """No existing invocation changes behavior."""
        from apps.cli.commands.job import _cmd_job_report

        job = saved_job()
        _cmd_job_report(str(job.id))
        out = capsys.readouterr().out
        assert "Job Report:" in out           # the pre-F053 view
        assert "# Run report" not in out


def _headings(text: str) -> list[str]:
    return [line for line in text.splitlines() if line.startswith("## ")]


def _job_file(job: Job) -> Path:
    from packages.orchestration.data_paths import jobs_dir

    return jobs_dir() / f"{job.id}.json"
