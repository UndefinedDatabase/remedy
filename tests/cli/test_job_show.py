"""F261 T002 — `remedy job show <id>`, the one read command of a job.

Round 8 (finding R-0896): next-step hints told the operator to run
``remedy job show <id> --json`` and the command exited 2 on the flag. `job show`
now declares ``--json``; its output was always JSON, so the flag changes nothing.

Round 8 (finding R-0806): a blocked run's reviewer findings were readable only by
opening evidence JSON. `job show` now prints, for every blocked task, the findings
of its run's last round, ten by default and all of them with ``--full``. The
findings tests write every job and run record by hand under a temporary data root;
one end-to-end test blocks a task through the real fake-provider runner on a
temporary git repository, as the acceptance line asks.

Round 8 (DECISION amend0905-vocab D4): `job show --full` carries the job's read
views as `sections`, in D4's order, each in an ok/error envelope; the former
`job permissions` command is the first of them.
"""
from __future__ import annotations

import json
import subprocess

import pytest

import apps.cli.commands.job as job_commands
from apps.cli.grouped import build_parser, main
from packages.core.models import RunState
from packages.orchestration import data_paths
from packages.orchestration.pingpong_job import (
    TASK_APPLIED,
    TASK_BLOCKED,
    TASK_SKIPPED,
    JobPlan,
    TaskEntry,
    _export_job,
    parse_job_file,
    require_job_plan,
    run_job,
    save_job_plan,
)
from packages.orchestration.pingpong_loop import load_run
from packages.orchestration.pingpong_provider import FakeProvider


@pytest.fixture
def data_root(tmp_path, monkeypatch):
    root = tmp_path / "data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


def _show(capsys, *argv: str):
    main(["job", "show", *argv])
    return capsys.readouterr()


class TestJsonFlag:
    def test_job_show_json_parses_with_no_unknown_argument(self) -> None:
        args, unknown = build_parser().parse_known_args(["job", "show", "abc", "--json"])

        assert args._command_id == "job.show"
        assert unknown == []

    def test_the_json_flag_changes_nothing_in_the_output(self, data_root, capsys) -> None:
        job = JobPlan(job_title="show me", state=RunState.PENDING)
        save_job_plan(job)

        bare = _show(capsys, str(job.job_id))
        flagged = _show(capsys, str(job.job_id), "--json")

        assert json.loads(bare.out)["job_id"] == job.job_id
        assert flagged.out == bare.out
        assert flagged.err == bare.err


def _write_run(data_root, run_id: str, rounds: list[dict]) -> None:
    """A run record in the shape `export_pingpong_json` writes, built by hand."""
    run_dir = data_paths.run_dir(run_id, data_root)
    run_dir.mkdir(parents=True)
    (run_dir / "result.json").write_text(json.dumps({
        "run_id": run_id,
        "final_status": "repair_exhausted",
        "total_rounds": len(rounds),
        "rounds": rounds,
    }))


def _round(number: int, findings: list[dict]) -> dict:
    return {
        "round": number,
        "kind": "initial" if number == 1 else "repair",
        "reviewer": {"verdict": "fail", "finding_count": len(findings), "findings": findings},
    }


def _finding(number: int) -> dict:
    return {
        "id": f"R-{number:04d}",
        "severity": "high",
        "file": f"src/module_{number}.py",
        "summary": f"Finding number {number} is real",
    }


def _blocked_job(data_root, *, last_round_findings: int) -> JobPlan:
    """T001 applied (its run HAS findings), T002 blocked after two rounds, T003 skipped."""
    _write_run(data_root, "run-applied", [_round(1, [_finding(90)])])
    _write_run(data_root, "run-blocked", [
        _round(1, [_finding(80)]),
        _round(2, [_finding(number) for number in range(1, last_round_findings + 1)]),
    ])
    job = JobPlan(job_title="blocked job", state=RunState.BLOCKED, tasks=[
        TaskEntry(task_id="T001", title="applied", status=TASK_APPLIED, run_id="run-applied"),
        TaskEntry(task_id="T002", title="blocked", status=TASK_BLOCKED, run_id="run-blocked"),
        TaskEntry(task_id="T003", title="skipped", status=TASK_SKIPPED),
    ])
    save_job_plan(job)
    return job


class TestBlockedTaskFindings:
    def test_only_the_last_round_of_the_blocked_task_appears(self, data_root, capsys) -> None:
        job = _blocked_job(data_root, last_round_findings=2)

        shown = _show(capsys, str(job.job_id))

        assert json.loads(shown.out)["blocked_task_findings"] == [{
            "task_id": "T002",
            "run_id": "run-blocked",
            "round": 2,
            "findings": [_finding(1), _finding(2)],
            "findings_total": 2,
            "findings_omitted": 0,
        }]
        assert "--- Blocked task findings ---" in shown.err
        assert "  T002 [high] src/module_1.py: Finding number 1 is real (R-0001)" in shown.err
        assert "R-0080" not in shown.out + shown.err

    def test_a_task_that_is_not_blocked_is_absent_even_with_findings(self, data_root, capsys) -> None:
        job = _blocked_job(data_root, last_round_findings=1)

        shown = _show(capsys, str(job.job_id))

        assert [e["task_id"] for e in json.loads(shown.out)["blocked_task_findings"]] == ["T002"]
        assert "R-0090" not in shown.out + shown.err

    def test_the_default_shows_ten_findings_and_names_the_overflow(self, data_root, capsys) -> None:
        job = _blocked_job(data_root, last_round_findings=12)

        shown = _show(capsys, str(job.job_id))

        (entry,) = json.loads(shown.out)["blocked_task_findings"]
        assert entry["findings"] == [_finding(number) for number in range(1, 11)]
        assert entry["findings_total"] == 12
        assert entry["findings_omitted"] == 2
        assert f"  T002 \u2026 2 more (job show {job.job_id} --full)" in shown.err
        assert "(R-0011)" not in shown.err

    def test_full_shows_every_finding(self, data_root, capsys) -> None:
        job = _blocked_job(data_root, last_round_findings=12)

        shown = _show(capsys, str(job.job_id), "--full")

        (entry,) = json.loads(shown.out)["blocked_task_findings"]
        assert entry["findings"] == [_finding(number) for number in range(1, 13)]
        assert entry["findings_total"] == 12
        assert entry["findings_omitted"] == 0
        assert "(R-0012)" in shown.err
        assert "more (job show" not in shown.err

    def test_a_blocked_task_without_a_readable_run_reports_no_findings(self, data_root, capsys) -> None:
        corrupt = data_paths.run_dir("run-corrupt", data_root)
        corrupt.mkdir(parents=True)
        (corrupt / "result.json").write_text("{not json")
        job = JobPlan(job_title="no readable runs", state=RunState.BLOCKED, tasks=[
            TaskEntry(task_id="T001", title="never ran", status=TASK_BLOCKED),
            TaskEntry(task_id="T002", title="run gone", status=TASK_BLOCKED, run_id="run-missing"),
            TaskEntry(task_id="T003", title="run broken", status=TASK_BLOCKED, run_id="run-corrupt"),
        ])
        save_job_plan(job)

        shown = _show(capsys, str(job.job_id))

        assert json.loads(shown.out)["blocked_task_findings"] == [
            {"task_id": task_id, "run_id": run_id, "round": None, "findings": [],
             "findings_total": 0, "findings_omitted": 0}
            for task_id, run_id in (("T001", ""), ("T002", "run-missing"), ("T003", "run-corrupt"))
        ]
        assert "--- Blocked task findings ---" not in shown.err


def _git(repo, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=str(repo), capture_output=True,
                          text=True, check=True).stdout


_BLOCKING_JOB = """\
# Job: Blocked by its reviewer

## Task 1
Update docs/README.md.

Acceptance:
- done

## Task 2
A second task the block skips.

Acceptance:
- done
"""


class TestABlockedFakeRunShowsItsFindingText:
    def test_the_persisted_finding_summary_appears_in_job_show(
            self, tmp_path, data_root, capsys, monkeypatch) -> None:
        # The temporary git repository of tests/orchestration/test_job_worktree_integration.py,
        # driven by the never-passing fake reviewer of tests/orchestration/test_job_task_runner.py.
        # The process runs outside every checkout, so no worktree or branch can land in one.
        monkeypatch.chdir(tmp_path)
        repo = tmp_path / "repo"
        repo.mkdir()
        _git(repo, "init", "-q")
        _git(repo, "config", "user.email", "t@e.com")
        _git(repo, "config", "user.name", "T")
        _git(repo, "config", "commit.gpgsign", "false")
        (repo / "README.md").write_text("# Demo\n")
        _git(repo, "add", "-A")
        _git(repo, "commit", "-qm", "init")
        job = parse_job_file(_BLOCKING_JOB, str(repo))

        result = run_job(
            job.job_id,
            builder_provider=FakeProvider(pass_on_round=99),
            reviewer_provider=FakeProvider(pass_on_round=99),
            max_rounds=1, repair_rounds=0,
        )

        (blocked,) = [task for task in result.tasks if task.status == TASK_BLOCKED]
        persisted = load_run(blocked.run_id)["rounds"][-1]["reviewer"]["findings"]
        assert persisted, "the blocking round left no reviewer finding on disk"
        capsys.readouterr()

        shown = _show(capsys, str(job.job_id))

        (entry,) = json.loads(shown.out)["blocked_task_findings"]
        assert entry["task_id"] == blocked.task_id
        assert [finding["summary"] for finding in entry["findings"]] == [
            finding["summary"] for finding in persisted
        ]
        for finding in persisted:
            assert finding["summary"] in shown.err


class TestTheDefaultOutputOnlyGainsTheFindingsKey:
    def test_a_job_without_a_blocked_task_prints_the_old_json_plus_an_empty_list(
            self, data_root, capsys) -> None:
        job = JobPlan(job_title="nothing blocked", state=RunState.PENDING,
                      tasks=[TaskEntry(task_id="T001", title="pending")])
        save_job_plan(job)

        shown = _show(capsys, str(job.job_id))

        data = json.loads(shown.out)
        old = json.loads(json.dumps(_export_job(require_job_plan(job.job_id))))
        assert list(data) == [*old, "blocked_task_findings"]
        assert {key: data[key] for key in old} == old
        assert data["blocked_task_findings"] == []
        assert shown.err == ""


def _plain_job() -> JobPlan:
    job = JobPlan(job_title="sections", state=RunState.PENDING)
    save_job_plan(job)
    return job


class TestSections:
    def test_the_default_output_has_no_sections_key(self, data_root, capsys) -> None:
        job = _plain_job()

        assert "sections" not in json.loads(_show(capsys, str(job.job_id)).out)

    def test_full_prints_the_registered_sections_in_the_d4_order(self, data_root, capsys) -> None:
        job = _plain_job()

        shown = _show(capsys, str(job.job_id), "--full")

        registered = [name for name, _builder in job_commands._SHOW_SECTIONS]
        assert registered == ["permissions", "assumptions"]
        assert list(json.loads(shown.out)["sections"]) == registered
        assert registered == [name for name in job_commands._SHOW_SECTION_ORDER if name in registered]
        assert job_commands._SHOW_SECTION_ORDER == (
            "permissions", "fences", "assumptions", "digest", "summary", "status", "report", "dod",
        )

    def test_a_raising_section_becomes_section_failed_and_the_command_exits_zero(
            self, data_root, capsys, monkeypatch) -> None:
        def explode(job):
            raise RuntimeError("the section broke")

        monkeypatch.setattr(job_commands, "_SHOW_SECTIONS", (("permissions", explode),))
        job = _plain_job()

        # `main` returning rather than raising SystemExit is the exit code 0.
        shown = _show(capsys, str(job.job_id), "--full")

        assert json.loads(shown.out)["sections"] == {
            "permissions": {
                "ok": False,
                "error": {"code": "section_failed", "message": "RuntimeError: the section broke"},
            },
        }
        assert "--- Permissions ---" in shown.err
        assert "  Error: section_failed: RuntimeError: the section broke" in shown.err
