"""F053 T002 — the run report, now the `report` section of `remedy job show <id> --full`.

The former `remedy job report` command had three modes on one name: bare and `--json`
printed the progress view, `--final` rendered the F053 account of a terminal run, and
`--interim` rendered the same structure for a run still going, loudly labeled. DECISION
F261 D10 folds all three into the `report` section: its data is the progress payload
followed by `run_report`, whose mode is `final` for a job that reached a reported terminal
and `interim` for every other job, which therefore always carries the snapshot banner.

The property this file exists to defend: rendering a snapshot must not perturb the run it
is describing.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

import pytest

from apps.cli.grouped import main
from packages.core.models import RunState
from packages.orchestration import long_run_executor
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, require_job_plan, save_job_plan
from packages.orchestration.run_report import build_report_sources, report_path

pytestmark = pytest.mark.integration

UTC = timezone.utc
T0 = datetime(2026, 7, 31, 12, 0, 0, tzinfo=UTC)

#: Every key of the former `job report --json` payload, in its order.
PROGRESS_KEYS = [
    "job_id", "name", "state", "task_count", "done_count", "pending_count", "event_count",
    "artifact_count", "patch_intent_ids", "approval_required", "latest_stop_reason",
    "code_applied", "fulfillment_status", "staging_used", "staging_promoted",
    "fulfillment_blockers", "next_safe_action", "open_decisions", "open_decision_count", "tasks",
]


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path: Path, monkeypatch) -> Path:
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


def saved_job(*, state: RunState = RunState.COMPLETED,
              terminal: str = "all_green",
              task_status: RunState = RunState.COMPLETED) -> JobPlan:
    job = JobPlan(
        job_title="report-job",
        user_prompt="build the thing",
        mission="Build the thing",
        tasks=[TaskEntry(title=f"task {i}", inputs={"task_type": "documentation"})
               for i in range(2)],
        state=state,
        metadata={"target_repo": "/tmp/repo", "cycle_terminal_status": terminal},
    )
    for task in job.tasks:
        task.status = task_status
    save_job_plan(job)
    return job


def running_job(terminal: str = "") -> JobPlan:
    return saved_job(state=RunState.RUNNING, terminal=terminal, task_status=RunState.PENDING)


def show_report(capsys, job_id: str) -> tuple[dict, str]:
    """`job show <id> --full`: the report section's envelope, and its text on stderr up to the next heading."""
    main(["job", "show", job_id, "--full"])
    shown = capsys.readouterr()
    text = shown.err.split("--- Report ---\n", 1)[1].split("\n--- ", 1)[0]
    return json.loads(shown.out)["sections"]["report"], text


def run_report(capsys, job_id: str) -> dict:
    section, _text = show_report(capsys, job_id)
    assert section["ok"] is True
    return section["data"]["run_report"]


class TestFinalMode:

    def test_it_renders_the_run_report(self, capsys):
        job = saved_job()
        report = run_report(capsys, str(job.job_id))
        assert report["mode"] == "final"
        assert "# Run report — report-job" in report["markdown"]
        assert "- Terminal status: all_green" in report["markdown"]
        assert "## Recommended next action" in report["markdown"]

    def test_it_is_not_labeled_as_a_snapshot(self, capsys):
        job = saved_job()
        section, text = show_report(capsys, str(job.job_id))
        assert "INTERIM SNAPSHOT" not in section["data"]["run_report"]["markdown"]
        assert "INTERIM SNAPSHOT" not in text

    def test_a_short_job_id_prefix_resolves(self, capsys):
        job = saved_job()
        assert "# Run report — report-job" in run_report(capsys, str(job.job_id)[:8])["markdown"]

    def test_it_reads_disk_sources_not_only_the_job(self, capsys):
        """The mission and both task lines come from the persisted job."""
        job = saved_job()
        markdown = run_report(capsys, str(job.job_id))["markdown"]
        assert "- Mission: Build the thing" in markdown
        assert markdown.count("- `") >= 2


class TestInterimMode:

    def test_it_renders_the_loud_snapshot_label(self, capsys):
        job = running_job()
        report = run_report(capsys, str(job.job_id))
        assert report["mode"] == "interim"
        first = report["markdown"].splitlines()[0]
        assert first.startswith("> **INTERIM SNAPSHOT — run still in progress")
        assert "rendered at" in first

    def test_it_keeps_the_same_section_structure_as_final(self, capsys):
        """A running job's interim report and a terminal job's final report share every heading."""
        interim = run_report(capsys, str(running_job().job_id))
        final = run_report(capsys, str(saved_job().job_id))
        assert (interim["mode"], final["mode"]) == ("interim", "final")
        assert _headings(interim["markdown"]) == _headings(final["markdown"])

    def test_interim_never_mutates_job_state(self, capsys):
        """The whole point: looking at a running job must not disturb it."""
        job = running_job()
        before = _job_file(job).read_bytes()
        assert run_report(capsys, str(job.job_id))["mode"] == "interim"
        assert _job_file(job).read_bytes() == before

    def test_interim_writes_no_report_file(self, capsys):
        """Only the terminal hook writes report.md — never a render."""
        job = running_job()
        assert run_report(capsys, str(job.job_id))["mode"] == "interim"
        assert not report_path(str(job.job_id)).exists()

    def test_final_mode_writes_no_report_file_either(self, capsys):
        job = saved_job()
        assert run_report(capsys, str(job.job_id))["mode"] == "final"
        assert not report_path(str(job.job_id)).exists()


class TestANonTerminalRunGetsTheInterimReport:
    """R-0161: a moving run must never read as a final account, so its section is interim."""

    def test_a_running_job_s_section_is_interim_with_the_banner(self, capsys):
        job = running_job()
        section, text = show_report(capsys, str(job.job_id))
        assert section["ok"] is True
        report = section["data"]["run_report"]
        assert report["mode"] == "interim"
        assert report["markdown"].startswith("> **INTERIM SNAPSHOT — run still in progress")
        assert "- State: running" in report["markdown"]
        assert "\n\n> **INTERIM SNAPSHOT — run still in progress" in text

    def test_a_pending_job_with_no_metadata_gets_the_interim_report(self, capsys):
        """Nothing on the path raises for a job that never ran and carries no metadata."""
        job = JobPlan(job_title="bare-job", state=RunState.PENDING)
        save_job_plan(job)
        section, _text = show_report(capsys, str(job.job_id))
        assert section["ok"] is True
        report = section["data"]["run_report"]
        assert report["mode"] == "interim"
        assert report["sources"]["terminal_status"] == ""
        assert "Tasks: not recorded." in report["markdown"]

    @pytest.mark.parametrize("terminal", [
        "all_green", "stopped_by_operator", "budget_exhausted",
        "deadline_reached", "blocked",
    ])
    def test_every_reported_terminal_gives_the_final_report(self, terminal, capsys):
        job = saved_job(terminal=terminal)
        report = run_report(capsys, str(job.job_id))
        assert report["mode"] == "final"
        assert "# Run report — report-job" in report["markdown"]
        assert f"- Terminal status: {terminal}" in report["markdown"]
        assert "INTERIM SNAPSHOT" not in report["markdown"]

    def test_max_cycles_reached_gives_the_interim_report_like_any_non_terminal(self, capsys):
        """It is not in REPORTED_TERMINALS; the job still has work."""
        job = running_job(terminal="max_cycles_reached")
        report = run_report(capsys, str(job.job_id))
        assert report["mode"] == "interim"
        assert report["markdown"].startswith("> **INTERIM SNAPSHOT — run still in progress")
        assert "- Terminal status: max_cycles_reached" in report["markdown"]

    def test_the_guard_reads_the_executor_s_own_set(self):
        """No second list of terminals to drift out of sync."""
        from packages.orchestration.long_run_executor import REPORTED_TERMINALS

        assert "all_green" in REPORTED_TERMINALS
        assert "max_cycles_reached" not in REPORTED_TERMINALS

    def test_the_section_decides_the_mode_by_the_executor_s_set(self, capsys, monkeypatch):
        """Change the executor's set and the section's mode follows it."""
        monkeypatch.setattr(long_run_executor, "REPORTED_TERMINALS", frozenset({"max_cycles_reached"}))
        assert run_report(capsys, str(running_job(terminal="max_cycles_reached").job_id))["mode"] == "final"
        assert run_report(capsys, str(saved_job(terminal="all_green").job_id))["mode"] == "interim"


class TestTheSources:

    def test_it_emits_the_structured_sources(self, capsys):
        job = saved_job()
        sources = run_report(capsys, str(job.job_id))["sources"]
        assert sources["job_name"] == "report-job"
        assert sources["terminal_status"] == "all_green"
        assert len(sources["tasks"]) == 2
        assert "status_mirror" in sources

    def test_the_sources_are_not_the_rendered_markdown(self, capsys):
        job = saved_job()
        sources = run_report(capsys, str(job.job_id))["sources"]
        assert "# Run report" not in json.dumps(sources)

    def test_the_sources_and_the_markdown_agree(self, capsys):
        job = saved_job()
        report = run_report(capsys, str(job.job_id))
        assert report["sources"]["job_name"] in report["markdown"]

    def test_the_sources_equal_the_normalized_report_sources(self, capsys):
        """The former `--json` document: every source, with sorted keys and `str` for the rest."""
        job = saved_job()
        sources = run_report(capsys, str(job.job_id))["sources"]
        expected = json.loads(json.dumps(asdict(build_report_sources(require_job_plan(job.job_id))),
                                         sort_keys=True, default=str))
        assert sources == expected
        assert list(sources) == sorted(sources)


class TestUnknownJob:

    def test_it_exits_cleanly_without_a_traceback(self, capsys):
        with pytest.raises(SystemExit) as exc:
            main(["job", "show", "ffffffff-ffff-4fff-8fff-ffffffffffff", "--full"])
        assert exc.value.code == 1
        captured = capsys.readouterr()
        assert "Error: Job not found: ffffffff-ffff-4fff-8fff-ffffffffffff" in captured.err
        assert "Traceback" not in captured.err
        assert captured.out == ""


class TestTheProgressView:
    """The former bare and `--json` view comes first, in the data and in the text."""

    def test_the_data_is_the_progress_payload_then_the_run_report(self, capsys):
        job = saved_job()
        section, _text = show_report(capsys, str(job.job_id))
        data = section["data"]
        assert list(data) == [*PROGRESS_KEYS, "run_report"]
        assert list(data["run_report"]) == ["mode", "sources", "markdown"]
        assert data["job_id"] == str(job.job_id)
        assert (data["task_count"], data["done_count"], data["pending_count"]) == (2, 2, 0)
        assert [task["description"] for task in data["tasks"]] == ["task 0", "task 1"]
        assert "fulfillment" not in data

    def test_the_text_is_the_progress_view_a_blank_line_and_the_markdown(self, capsys):
        job = saved_job()
        section, text = show_report(capsys, str(job.job_id))
        markdown = section["data"]["run_report"]["markdown"]
        assert text.endswith("\n\n" + markdown)
        progress = text[:-len("\n" + markdown)].splitlines()
        assert progress[0] == f"Job Report: {job.job_id}"   # the pre-F053 view
        assert "  Tasks:     2/2 done, 0 pending" in progress
        assert "# Run report" not in "\n".join(progress)


def _headings(text: str) -> list[str]:
    return [line for line in text.splitlines() if line.startswith("## ")]


def _job_file(job: JobPlan) -> Path:
    from packages.orchestration.data_paths import jobs_dir

    return jobs_dir() / job.job_id / "job.json"
