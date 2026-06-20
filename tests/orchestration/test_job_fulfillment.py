"""Job Fulfillment Spine v0 tests.

Unit tests for model, fixture components, and contract.
Integration tests for full fulfillment lifecycle.
CLI tests for job fulfill command.
"""
from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
from uuid import uuid4

_ROOT = Path(__file__).resolve().parent.parent.parent


# ---------------------------------------------------------------------------
# Unit tests: fulfillment model (Step 3310)
# ---------------------------------------------------------------------------


class TestFulfillmentModel:

    def test_status_values(self):
        from packages.orchestration.job_fulfillment import JobFulfillmentStatus
        assert JobFulfillmentStatus.COMPLETED_VERIFIED == "completed_verified"
        assert JobFulfillmentStatus.NOT_STARTED == "not_started"
        assert len(JobFulfillmentStatus) == 13

    def test_record_export_no_secrets(self):
        from packages.orchestration.job_fulfillment import (
            JobFulfillmentRecord,
            export_job_fulfillment_json,
        )
        rec = JobFulfillmentRecord(job_id="test-123", mode="fixture_demo")
        data = export_job_fulfillment_json(rec)
        raw = json.dumps(data)
        assert "sk-" not in raw
        assert "/home/" not in raw
        assert "api_key" not in raw

    def test_contract_check_empty(self):
        from packages.orchestration.job_fulfillment import (
            JobFulfillmentContract,
            JobFulfillmentRecord,
        )
        contract = JobFulfillmentContract()
        record = JobFulfillmentRecord()
        passed, blockers = contract.check(record)
        assert not passed
        assert len(blockers) > 0

    def test_contract_check_all_pass(self):
        from packages.orchestration.job_fulfillment import (
            JobFulfillmentContract,
            JobFulfillmentRecord,
            JobFulfillmentStatus,
        )
        contract = JobFulfillmentContract()
        record = JobFulfillmentRecord(
            task_ids=["t1"],
            apply_ids=["a1"],
            test_passed=True,
            proof_status="verified",
            final_review_status="pass",
            status=JobFulfillmentStatus.COMPLETED_VERIFIED,
        )
        passed, blockers = contract.check(record)
        assert passed
        assert blockers == []

    def test_record_storage(self, tmp_path):
        from packages.orchestration.job_fulfillment import (
            JobFulfillmentRecord,
            list_fulfillment_records,
            load_fulfillment_record,
            save_fulfillment_record,
        )
        rec = JobFulfillmentRecord(job_id="job-abc")
        save_fulfillment_record(rec, tmp_path)
        loaded = load_fulfillment_record(rec.fulfillment_id, "job-abc", tmp_path)
        assert loaded is not None
        assert loaded.job_id == "job-abc"
        records = list_fulfillment_records("job-abc", tmp_path)
        assert len(records) == 1

    def test_summarize(self):
        from packages.orchestration.job_fulfillment import (
            JobFulfillmentRecord,
            summarize_job_fulfillment,
        )
        rec = JobFulfillmentRecord(job_id="job-xyz", mode="fixture_demo")
        text = summarize_job_fulfillment(rec)
        assert "fixture_demo" in text
        assert "job-xyz" in text


# ---------------------------------------------------------------------------
# Unit tests: fixture planner (Step 3311)
# ---------------------------------------------------------------------------


class TestFixturePlanner:

    def test_creates_at_least_two_tasks(self):
        from packages.orchestration.job_fulfillment import fixture_plan_tasks
        tasks = fixture_plan_tasks("job-1")
        assert len(tasks) >= 2

    def test_task_has_required_fields(self):
        from packages.orchestration.job_fulfillment import fixture_plan_tasks
        tasks = fixture_plan_tasks("job-1")
        for t in tasks:
            assert "task_id" in t
            assert "description" in t
            assert "task_type" in t

    def test_deterministic_types(self):
        from packages.orchestration.job_fulfillment import fixture_plan_tasks
        tasks = fixture_plan_tasks("job-1")
        types = {t["task_type"] for t in tasks}
        assert "docs_update" in types
        assert "evidence_summary" in types


# ---------------------------------------------------------------------------
# Unit tests: fixture reviewer (Steps 3312-3313)
# ---------------------------------------------------------------------------


class TestFixtureReviewer:

    def test_pass_mode(self):
        from packages.orchestration.job_fulfillment import fixture_review
        result = fixture_review(1, mode="pass")
        assert result.verdict == "pass"
        assert result.findings == []

    def test_one_finding_then_pass_round1(self):
        from packages.orchestration.job_fulfillment import fixture_review
        result = fixture_review(1, mode="one_finding_then_pass")
        assert result.verdict == "finding"
        assert len(result.findings) == 1
        assert result.findings[0]["code"] == "FIXTURE-001"

    def test_one_finding_then_pass_round2(self):
        from packages.orchestration.job_fulfillment import fixture_review
        result = fixture_review(2, mode="one_finding_then_pass")
        assert result.verdict == "pass"

    def test_finding_to_repair(self):
        from packages.orchestration.job_fulfillment import (
            finding_to_repair_task,
            fixture_review,
        )
        result = fixture_review(1, mode="one_finding_then_pass")
        repair = finding_to_repair_task(result.findings[0], "task-origin", 1)
        assert repair["task_type"] == "repair"
        assert repair["inputs"]["origin_task_id"] == "task-origin"
        assert repair["inputs"]["finding_code"] == "FIXTURE-001"


# ---------------------------------------------------------------------------
# Unit tests: completion contract (Step 3314)
# ---------------------------------------------------------------------------


class TestCompletionContract:

    def test_missing_apply_blocks(self):
        from packages.orchestration.job_fulfillment import (
            JobFulfillmentContract,
            JobFulfillmentRecord,
        )
        rec = JobFulfillmentRecord(
            task_ids=["t1"],
            test_passed=True,
            proof_status="verified",
            final_review_status="pass",
        )
        passed, blockers = JobFulfillmentContract().check(rec)
        assert not passed
        assert "no_apply" in blockers

    def test_missing_test_blocks(self):
        from packages.orchestration.job_fulfillment import (
            JobFulfillmentContract,
            JobFulfillmentRecord,
        )
        rec = JobFulfillmentRecord(
            task_ids=["t1"],
            apply_ids=["a1"],
            test_passed=False,
            proof_status="verified",
            final_review_status="pass",
        )
        passed, blockers = JobFulfillmentContract().check(rec)
        assert not passed
        assert "test_not_passed" in blockers

    def test_missing_proof_blocks(self):
        from packages.orchestration.job_fulfillment import (
            JobFulfillmentContract,
            JobFulfillmentRecord,
        )
        rec = JobFulfillmentRecord(
            task_ids=["t1"],
            apply_ids=["a1"],
            test_passed=True,
            proof_status="unknown",
            final_review_status="pass",
        )
        passed, blockers = JobFulfillmentContract().check(rec)
        assert not passed
        assert "proof_not_verified" in blockers


# ---------------------------------------------------------------------------
# Integration test: fixture pass (Step 3315)
# ---------------------------------------------------------------------------


class TestJobFulfillFixturePass:

    def _setup_job(self, tmp_path):
        from packages.core.models import Job
        from packages.orchestration.job_fulfillment import create_demo_repo
        from packages.orchestration.storage import save_job

        repo = create_demo_repo(tmp_path)
        job = Job(name="Test fulfillment", metadata={"target_repo": str(repo)})
        save_job(job, root=tmp_path)
        return job, repo

    def test_fixture_pass_completes(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.job_fulfillment import run_job_fulfill

        job, repo = self._setup_job(tmp_path)
        record = run_job_fulfill(str(job.id), repo, data_dir=tmp_path)

        assert record.status.value == "completed_verified"
        assert len(record.task_ids) >= 2
        assert record.review_round_count >= 1
        assert len(record.apply_ids) > 0
        assert record.test_passed
        assert record.proof_status in ("verified", "accepted", "incomplete")
        assert record.final_review_status == "pass"
        assert len(record.next_suggestion_ids) >= 2

    def test_repo_file_changed(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.job_fulfillment import run_job_fulfill

        job, repo = self._setup_job(tmp_path)
        record = run_job_fulfill(str(job.id), repo, data_dir=tmp_path)

        assert len(record.changed_files) > 0
        for f in record.changed_files:
            assert (repo / f).exists()


# ---------------------------------------------------------------------------
# Integration test: one-finding repair loop (Step 3316)
# ---------------------------------------------------------------------------


class TestOneFindingRepairLoop:

    def test_repair_loop(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job
        from packages.orchestration.job_fulfillment import (
            create_demo_repo,
            run_job_fulfill,
        )
        from packages.orchestration.storage import save_job

        repo = create_demo_repo(tmp_path)
        job = Job(name="Repair loop test", metadata={"target_repo": str(repo)})
        save_job(job, root=tmp_path)

        record = run_job_fulfill(
            str(job.id), repo, data_dir=tmp_path,
            review_mode="one_finding_then_pass",
        )

        assert record.status.value == "completed_verified"
        assert len(record.repair_task_ids) > 0
        assert record.review_round_count >= 2


# ---------------------------------------------------------------------------
# Integration test: no provider execution (Step 3318)
# ---------------------------------------------------------------------------


class TestNoProviderExecution:

    def test_no_provider_import_in_fulfillment(self):
        src = _ROOT / "packages" / "orchestration" / "job_fulfillment.py"
        text = src.read_text()
        for pattern in ["import anthropic", "import openai", "from anthropic", "from openai"]:
            assert pattern not in text, f"Fulfillment must not import: {pattern}"

    def test_no_subprocess_in_fulfillment(self):
        src = _ROOT / "packages" / "orchestration" / "job_fulfillment.py"
        text = src.read_text()
        assert "subprocess.run" not in text
        assert "subprocess.Popen" not in text
        assert "shell=True" not in text


# ---------------------------------------------------------------------------
# Integration test: job report after fulfilled (Step 3320)
# ---------------------------------------------------------------------------


class TestJobReportAfterFulfilled:

    def test_report_shows_completed(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job
        from packages.orchestration.job_fulfillment import (
            create_demo_repo,
            run_job_fulfill,
        )
        from packages.orchestration.storage import save_job

        repo = create_demo_repo(tmp_path)
        job = Job(name="Report test", metadata={"target_repo": str(repo)})
        save_job(job, root=tmp_path)
        run_job_fulfill(str(job.id), repo, data_dir=tmp_path)

        from apps.cli.commands.job import _cmd_job_report

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            _cmd_job_report(str(job.id), json_output=True)
        data = json.loads(buf.getvalue())
        assert data["state"] == "completed"
        assert data["code_applied"] is True


# ---------------------------------------------------------------------------
# Integration test: job status after fulfilled (Step 3321)
# ---------------------------------------------------------------------------


class TestJobStatusAfterFulfilled:

    def test_status_shows_completed(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job
        from packages.orchestration.job_fulfillment import (
            create_demo_repo,
            run_job_fulfill,
        )
        from packages.orchestration.storage import save_job

        repo = create_demo_repo(tmp_path)
        job = Job(name="Status test", metadata={"target_repo": str(repo)})
        save_job(job, root=tmp_path)
        run_job_fulfill(str(job.id), repo, data_dir=tmp_path)

        from apps.cli.commands.job import _cmd_job_status

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            _cmd_job_status(str(job.id), json_output=True)
        data = json.loads(buf.getvalue())
        assert data["state"] == "completed"
        # Secondary fixture artifacts may have pending intents; only check state.


# ---------------------------------------------------------------------------
# CLI tests (Steps 3323-3325)
# ---------------------------------------------------------------------------


class TestJobFulfillCLI:

    def test_invalid_job_id(self):
        from apps.cli.commands.job import _cmd_job_fulfill

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            try:
                _cmd_job_fulfill("not-a-uuid", fixture_demo=True, json_output=True)
            except SystemExit:
                pass
        output = buf.getvalue()
        assert "invalid_job_id" in output

    def test_missing_job(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from apps.cli.commands.job import _cmd_job_fulfill

        fake_id = str(uuid4())
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            try:
                _cmd_job_fulfill(fake_id, fixture_demo=True, json_output=True)
            except SystemExit:
                pass
        output = buf.getvalue()
        assert "job_not_found" in output

    def test_missing_fixture_flag(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job
        from packages.orchestration.storage import save_job

        job = Job(name="No flag test")
        save_job(job, root=tmp_path)

        from apps.cli.commands.job import _cmd_job_fulfill

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            try:
                _cmd_job_fulfill(str(job.id), fixture_demo=False, json_output=True)
            except SystemExit:
                pass
        output = buf.getvalue()
        assert "fixture_demo_required" in output


# ---------------------------------------------------------------------------
# Docs tests (Step 3327)
# ---------------------------------------------------------------------------


class TestFulfilledDemoGuide:

    def test_guide_exists(self):
        path = _ROOT / "docs" / "first-fulfilled-job-demo-v0.md"
        assert path.exists()

    def test_guide_mentions_fulfill(self):
        path = _ROOT / "docs" / "first-fulfilled-job-demo-v0.md"
        text = path.read_text()
        assert "job fulfill" in text
        assert "fixture-demo" in text

    def test_guide_mentions_status_report(self):
        path = _ROOT / "docs" / "first-fulfilled-job-demo-v0.md"
        text = path.read_text()
        assert "job status" in text
        assert "job report" in text

    def test_guide_mentions_propose(self):
        path = _ROOT / "docs" / "first-fulfilled-job-demo-v0.md"
        text = path.read_text()
        assert "propose list" in text

    def test_guide_no_real_provider_claims(self):
        path = _ROOT / "docs" / "first-fulfilled-job-demo-v0.md"
        text = path.read_text()
        assert "No real provider" in text


# ---------------------------------------------------------------------------
# Command catalog tests (Step 3329)
# ---------------------------------------------------------------------------


class TestFulfillCatalog:

    def test_job_fulfill_in_catalog(self):
        from apps.cli.command_catalog import get_command
        cmd = get_command("job.fulfill")
        assert cmd is not None
        assert cmd.action_class == "write_metadata"
        assert cmd.supports_json

    def test_job_fulfill_has_handler(self):
        from apps.cli.commands import collect_all_handlers
        handlers = collect_all_handlers()
        assert "job.fulfill" in handlers


# ---------------------------------------------------------------------------
# Development artifact boundary (Step 3331)
# ---------------------------------------------------------------------------


class TestFulfillmentNoDevelopmentDependency:

    def test_no_live_review_dependency(self):
        src = _ROOT / "packages" / "orchestration" / "job_fulfillment.py"
        text = src.read_text()
        assert "live_review" not in text
        assert ".agent/" not in text
