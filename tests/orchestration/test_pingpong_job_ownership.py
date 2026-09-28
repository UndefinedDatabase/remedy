"""F035 R2 T001's write half — `run_job`'s ownership-ledger save at every job terminal
(DECISION F035 D2). `_write_ownership_ledger_at_run_end` and its `_writes_ownership_ledger`
decorator are pinned directly here rather than only through `ownership.py`'s own suite: the
claim under test is that a REAL `run_job` invocation, through the real decorator, produces the
file on disk, not merely that `build_ownership_ledger` answers the right dict in isolation.

The job fixture mirrors `tests/orchestration/test_task_veto_runner.py`'s own `root`/`repo`
fixtures and its `_pass_provider` (`FakeProvider(pass_on_round=1, fail_on_round=99)`), and reuses
`test_task_edit_runtime.py`'s `_task`/`_save_job` — the same recipe several sibling suites
already share for a minimal approved single-task job.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path

import pytest

from packages.orchestration import ownership as own
from packages.orchestration import pingpong_job as pj
from packages.orchestration import safe_points
from packages.orchestration import task_veto as tv
from packages.orchestration.data_paths import job_evidence_export_dir
from packages.orchestration.ownership_phrases import ownership_sentences
from packages.orchestration.pingpong_job import (
    JOB_BLOCKED,
    JOB_COMPLETED,
    load_job_plan,
    run_job,
)
from packages.orchestration.pingpong_provider import FakeProvider
from tests.orchestration.test_task_edit_runtime import _save_job, _task, _task_id_of


@pytest.fixture
def root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    data = tmp_path / "data"
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data))
    return data


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A plain (non-git) directory: the copy-mode job's target."""
    r = tmp_path / "repo"
    r.mkdir()
    (r / "docs").mkdir()
    (r / "docs" / "README.md").write_text("# Docs\n")
    return r


def _control():
    return safe_points.control_root()


def _pass_provider() -> FakeProvider:
    return FakeProvider(pass_on_round=1, fail_on_round=99)


class TestOwnershipLedgerWrite:
    def test_completed_job_writes_ownership_json_matching_the_returned_job(self, root, repo):
        job_id = _save_job(root, [_task("A", [])], repo_path=str(repo))
        done = run_job(job_id, builder_provider=_pass_provider(),
                       reviewer_provider=_pass_provider(), max_rounds=1, repair_rounds=0)
        assert done.state == JOB_COMPLETED

        path = job_evidence_export_dir(done.job_id) / own.OWNERSHIP_FILENAME
        on_disk = json.loads(path.read_text(encoding="utf-8"))
        assert on_disk == own.build_ownership_ledger(done)

    def test_an_ownershiperror_in_the_write_leaves_the_run_untouched_writes_no_file_and_logs_one_warning(
        self, root, repo, monkeypatch, caplog,
    ):
        job_id_baseline = _save_job(root, [_task("A", [])], repo_path=str(repo))
        baseline = run_job(job_id_baseline, builder_provider=_pass_provider(),
                           reviewer_provider=_pass_provider(), max_rounds=1, repair_rounds=0)

        job_id = _save_job(root, [_task("A", [])], repo_path=str(repo))

        def _raise(job):
            raise own.OwnershipError("boom")

        monkeypatch.setattr(
            "packages.orchestration.ownership.build_ownership_ledger", _raise)

        with caplog.at_level(logging.WARNING, logger="packages.orchestration.pingpong_job"):
            patched = run_job(job_id, builder_provider=_pass_provider(),
                              reviewer_provider=_pass_provider(), max_rounds=1, repair_rounds=0)

        assert patched.state == baseline.state
        path = job_evidence_export_dir(job_id) / own.OWNERSHIP_FILENAME
        assert not path.exists()
        warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warnings) == 1
        assert job_id in warnings[0].getMessage()

    def test_an_unknown_job_id_writes_no_file(self, root):
        job_id = "no-such-job-id"
        done = run_job(job_id, builder_provider=_pass_provider(),
                       reviewer_provider=_pass_provider())
        assert done.state == JOB_BLOCKED

        path = job_evidence_export_dir(job_id) / own.OWNERSHIP_FILENAME
        assert not path.exists()

    def test_run_job_is_wrapped(self):
        assert hasattr(pj.run_job, "__wrapped__")


class TestReportOwnershipSection:
    """F035 R3 T002 (DECISION F035 D3): `format_job_report_text`'s Ownership section, read
    through the same catalog and the same ledger builder the write half above already
    exercises against a real `run_job`."""

    def test_the_section_lists_the_ledger_s_sentences_in_ledger_order(self, root, repo):
        job_id = _save_job(root, [_task("A", [])], repo_path=str(repo))
        job = load_job_plan(job_id, root)
        a_id = _task_id_of(root, job_id, "A")

        veto = tv.veto_task_command(job, task_id=a_id, reason="not needed anymore",
                                    actor="carol", control_root_path=_control())
        assert veto["outcome"] == "vetoed"

        reloaded = load_job_plan(job_id, root)
        ledger = own.build_ownership_ledger(reloaded)
        assert len(ledger["entries"]) >= 2, ledger["entries"]  # the veto, plus plan_approved
        titles = {t.task_id: t.title for t in reloaded.tasks}
        expected = ownership_sentences(ledger, titles=titles)

        text = pj.format_job_report_text(reloaded)
        assert "Ownership:" in text
        start = text.index("Ownership:") + len("Ownership:\n")
        end = text.index("\n\n", start)
        rendered = [line[len("  - "):] for line in text[start:end].splitlines()]
        assert rendered == expected

    def test_a_job_with_no_ledger_entry_prints_no_section(self, root, repo):
        job_id = _save_job(root, [_task("A", [])], repo_path=str(repo), approval="pending")
        job = load_job_plan(job_id, root)

        ledger = own.build_ownership_ledger(job)
        assert ledger["entries"] == []

        text = pj.format_job_report_text(job)
        assert "Ownership:" not in text

    def test_an_unreadable_ledger_prints_the_error_line(self, root, repo, monkeypatch):
        job_id = _save_job(root, [_task("A", [])], repo_path=str(repo))
        job = load_job_plan(job_id, root)

        def _raise(_job):
            raise own.OwnershipError("boom")

        monkeypatch.setattr(
            "packages.orchestration.ownership.build_ownership_ledger", _raise)

        text = pj.format_job_report_text(job)
        assert "Ownership: the ledger could not be read — boom" in text
        assert "Ownership:\n" not in text

    def test_a_vetoed_task_carries_no_per_task_vetoed_by_line(self, root, repo):
        job_id = _save_job(root, [_task("A", [])], repo_path=str(repo))
        job = load_job_plan(job_id, root)
        a_id = _task_id_of(root, job_id, "A")

        veto = tv.veto_task_command(job, task_id=a_id, reason="stop it",
                                    actor="dana", control_root_path=_control())
        assert veto["outcome"] == "vetoed"

        reloaded = load_job_plan(job_id, root)
        text = pj.format_job_report_text(reloaded)
        assert "Vetoed by" not in text
        assert "vetoed task" in text
