"""F272 T001 — ``JobPlan.run_refs``: the ordered ids of the runs one job produced.

DECISION F260 D1 says a Job has MANY runs. F260 closed with a record that could
name only the one run of each task, so nothing on disk carried the job-level run
list. These tests pin the field itself, its persistence through the job record,
its defaulted read for a record written without the key, and — the one that
matters — its population on a job driven end to end through the real grouped CLI
with the deterministic fake providers.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from apps.cli.grouped import main as grouped_main
from packages.orchestration.pingpong_job import (
    JobPlan,
    _export_job,
    _import_job,
    load_job_plan,
)

RUN_ID_RE = re.compile(r"^[0-9a-f]{16}$")


class TestJobPlanRunRefsField:
    """The field and its default_factory."""

    def test_run_refs_defaults_empty_and_is_not_shared(self):
        first = JobPlan()
        second = JobPlan()
        assert first.run_refs == []
        assert second.run_refs == []
        # A mutable default must come from a factory, so two plans never share
        # one list object.
        assert first.run_refs is not second.run_refs
        first.run_refs.append("aaaaaaaaaaaaaaaa")
        assert second.run_refs == []


class TestJobPlanRunRefsPersistence:
    """Round-trip through ``_export_job`` / ``_import_job``."""

    def test_run_refs_roundtrip_keeps_order(self):
        plan = JobPlan(run_refs=["1111111111111111", "2222222222222222"])
        exported = _export_job(plan)
        assert exported["run_refs"] == ["1111111111111111", "2222222222222222"]
        imported = _import_job(exported)
        assert imported.run_refs == ["1111111111111111", "2222222222222222"]

    def test_record_without_run_refs_key_imports_empty(self):
        # A job record written before this field existed carries no key at all;
        # it loads as the empty default rather than raising.
        imported = _import_job({"job_id": "test123"})
        assert imported.run_refs == []


class TestJobRunRefsEndToEnd:
    """The real grouped CLI, the fake providers, two tasks, one job record."""

    @pytest.fixture
    def isolate_data(self, tmp_path: Path, monkeypatch) -> Path:
        """Persist jobs/runs under tmp_path, never the repo's real .data dir."""
        data_dir = tmp_path / "remedy_data"
        data_dir.mkdir()
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
        return data_dir

    @pytest.fixture
    def demo_repo(self, tmp_path: Path) -> Path:
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "README.md").write_text("# Demo\n")
        return repo

    @pytest.fixture
    def job_file(self, tmp_path: Path) -> Path:
        jf = tmp_path / "job.md"
        jf.write_text(
            "# Job: Run refs E2E\n"
            "\n"
            "## Task 1\n"
            "Add a documentation file.\n"
            "\n"
            "Acceptance:\n"
            "- file exists\n"
            "\n"
            "## Task 2\n"
            "Add a second documentation file.\n"
            "\n"
            "Acceptance:\n"
            "- file exists\n"
        )
        return jf

    def test_run_refs_names_every_task_run_in_order(
        self, capsys, isolate_data, demo_repo, job_file, tmp_path
    ):
        grouped_main([
            "do", "job-flow",
            "--job-file", str(job_file),
            "--repo", str(demo_repo),
            "--builder", "fake",
            "--reviewer", "fake",
            "--out", str(tmp_path / "evidence"),
            "--json",
        ])
        data = json.loads(capsys.readouterr().out)
        job_id = data["job_id"]
        assert job_id

        job = load_job_plan(job_id)
        assert job is not None
        assert len(job.tasks) == 2
        assert job.run_refs == [t.run_id for t in job.tasks]
        assert len(job.run_refs) == 2
        assert len(set(job.run_refs)) == 2
        for run_id in job.run_refs:
            assert RUN_ID_RE.match(run_id), run_id
