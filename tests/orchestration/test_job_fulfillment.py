"""Job Fulfillment Spine v0 tests — Truth Closure v0.1.

Unit tests for model, fixture components, and contract.
Integration tests for full fulfillment lifecycle.
CLI tests for job fulfill command.
Failure path tests.
Strengthened truth assertions.
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

    def test_record_export_has_contract_id(self):
        from packages.orchestration.job_fulfillment import (
            JobFulfillmentRecord,
            export_job_fulfillment_json,
        )
        rec = JobFulfillmentRecord(job_id="test-123", contract_id="rc-abc")
        data = export_job_fulfillment_json(rec)
        assert data["contract_id"] == "rc-abc"

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
        rec = JobFulfillmentRecord(job_id="job-xyz", mode="fixture_demo", contract_id="rc-1")
        text = summarize_job_fulfillment(rec)
        assert "fixture_demo" in text
        assert "job-xyz" in text
        assert "rc-1" in text


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
# Unit tests: fixture worker output format (Steps 3362-3363)
# ---------------------------------------------------------------------------


class TestFixtureWorkerOutput:

    def test_artifact_content_has_proposed_changes(self):
        from packages.orchestration.job_fulfillment import fixture_worker_output
        wo = fixture_worker_output({"task_id": "t1", "task_type": "docs_update",
                                     "inputs": {"target_file": "CHANGELOG.md"}})
        assert "Proposed Changes:" in wo["content"]
        assert "Summary:" in wo["content"]

    def test_content_has_meaningful_lines(self):
        from packages.orchestration.job_fulfillment import fixture_worker_output
        wo = fixture_worker_output({"task_id": "t1", "task_type": "docs_update",
                                     "inputs": {"target_file": "CHANGELOG.md"}})
        assert "Changelog" in wo["content"]
        assert "Initial project setup" in wo["content"]

    def test_verification_content_has_evidence(self):
        from packages.orchestration.job_fulfillment import fixture_worker_output
        wo = fixture_worker_output({"task_id": "t2", "task_type": "evidence_summary",
                                     "inputs": {"target_file": "docs/VERIFICATION.md"}})
        assert "Verification" in wo["content"]
        assert "Proposed Changes:" in wo["content"]


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
# Unit tests: completion contract (Steps 3314, 3370, 3373-3374)
# ---------------------------------------------------------------------------


class TestCompletionContract:

    def test_missing_apply_blocks(self):
        from packages.orchestration.job_fulfillment import (
            JobFulfillmentContract,
            JobFulfillmentRecord,
        )
        rec = JobFulfillmentRecord(
            task_ids=["t1"], test_passed=True,
            proof_status="verified", final_review_status="pass",
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
            task_ids=["t1"], apply_ids=["a1"], test_passed=False,
            proof_status="verified", final_review_status="pass",
        )
        passed, blockers = JobFulfillmentContract().check(rec)
        assert not passed
        assert "test_not_passed" in blockers

    def test_incomplete_proof_blocks(self):
        from packages.orchestration.job_fulfillment import (
            JobFulfillmentContract,
            JobFulfillmentRecord,
        )
        rec = JobFulfillmentRecord(
            task_ids=["t1"], apply_ids=["a1"], test_passed=True,
            proof_status="incomplete", final_review_status="pass",
        )
        passed, blockers = JobFulfillmentContract().check(rec)
        assert not passed
        assert any("proof" in b for b in blockers)

    def test_accepted_proof_without_reason_blocks(self):
        from packages.orchestration.job_fulfillment import (
            JobFulfillmentContract,
            JobFulfillmentRecord,
        )
        rec = JobFulfillmentRecord(
            task_ids=["t1"], apply_ids=["a1"], test_passed=True,
            proof_status="accepted", proof_accepted_reason="",
            final_review_status="pass",
        )
        passed, blockers = JobFulfillmentContract().check(rec)
        assert not passed
        assert any("proof" in b for b in blockers)

    def test_accepted_proof_with_reason_passes(self):
        from packages.orchestration.job_fulfillment import (
            JobFulfillmentContract,
            JobFulfillmentRecord,
        )
        rec = JobFulfillmentRecord(
            task_ids=["t1"], apply_ids=["a1"], test_passed=True,
            proof_status="accepted",
            proof_accepted_reason="Fixture demo: explicit acceptance",
            final_review_status="pass",
        )
        passed, blockers = JobFulfillmentContract().check(rec)
        assert passed

    def test_mode_mismatch_blocks(self):
        from packages.orchestration.job_fulfillment import (
            JobFulfillmentContract,
            JobFulfillmentRecord,
        )
        rec = JobFulfillmentRecord(
            mode="unknown_mode",
            task_ids=["t1"], apply_ids=["a1"], test_passed=True,
            proof_status="verified", final_review_status="pass",
        )
        passed, blockers = JobFulfillmentContract().check(rec)
        assert not passed
        assert any("mode_mismatch" in b for b in blockers)

    def test_all_gates_pass(self):
        from packages.orchestration.job_fulfillment import (
            JobFulfillmentContract,
            JobFulfillmentRecord,
        )
        rec = JobFulfillmentRecord(
            task_ids=["t1"], apply_ids=["a1"], test_passed=True,
            proof_status="verified", final_review_status="pass",
        )
        passed, blockers = JobFulfillmentContract().check(rec)
        assert passed
        assert blockers == []


# ---------------------------------------------------------------------------
# Integration test: fixture pass with truth (Steps 3315, 3386)
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
        assert len(record.apply_ids) >= 2  # both outputs applied
        assert record.test_passed is True
        assert record.proof_status in ("verified", "accepted")
        if record.proof_status == "accepted":
            assert record.proof_accepted_reason != ""
        assert record.final_review_status == "pass"
        assert len(record.next_suggestion_ids) >= 2
        assert record.contract_id != ""
        assert record.contract_blockers == []

    def test_repo_file_changed(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.job_fulfillment import run_job_fulfill

        job, repo = self._setup_job(tmp_path)
        record = run_job_fulfill(str(job.id), repo, data_dir=tmp_path)

        assert len(record.changed_files) >= 2
        for f in record.changed_files:
            assert (repo / f).exists()

    def test_applied_content_is_meaningful(self, tmp_path, monkeypatch):
        """R-0190: Applied files must not contain placeholder text."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.job_fulfillment import run_job_fulfill

        job, repo = self._setup_job(tmp_path)
        run_job_fulfill(str(job.id), repo, data_dir=tmp_path)

        cl = (repo / "CHANGELOG.md").read_text()
        assert "(no proposed changes found in artifact)" not in cl
        assert "Changelog" in cl

        vf = (repo / "docs" / "VERIFICATION.md").read_text()
        assert "(no proposed changes found in artifact)" not in vf
        assert "Verification" in vf

    def test_real_test_execution(self, tmp_path, monkeypatch):
        """R-0192: Tests must actually pass, not be accepted as blocked."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.job_fulfillment import run_job_fulfill

        job, repo = self._setup_job(tmp_path)
        record = run_job_fulfill(str(job.id), repo, data_dir=tmp_path)

        assert record.test_passed is True
        assert len(record.test_run_ids) > 0
        assert record.test_run_ids[0] != ""


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
# Integration test: no provider execution (Step 3318, 3388-3391)
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

    def test_no_live_review_dependency(self):
        src = _ROOT / "packages" / "orchestration" / "job_fulfillment.py"
        text = src.read_text()
        assert "live_review" not in text
        assert ".agent/" not in text

    def test_no_direct_repo_write_in_engine(self):
        """R-0189: run_job_fulfill must not write directly to repo_root."""
        src = _ROOT / "packages" / "orchestration" / "job_fulfillment.py"
        text = src.read_text()
        # Find run_job_fulfill function body
        start = text.index("def run_job_fulfill(")
        engine_body = text[start:]
        # Should not contain direct file writes (write_text, open(..., 'w'))
        assert ".write_text(" not in engine_body
        assert "open(" not in engine_body


# ---------------------------------------------------------------------------
# Integration test: job report after fulfilled (Step 3320, 3375, 3392)
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
        assert data["approval_required"] is False
        assert data["fulfillment_status"] == "completed_verified"


# ---------------------------------------------------------------------------
# Integration test: job status after fulfilled (Step 3321, 3375-3377, 3393)
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
        assert data["approval_required"] is False
        assert data["code_applied"] is True
        assert data["fulfillment_status"] == "completed_verified"


# ---------------------------------------------------------------------------
# Failure path tests (Steps 3384-3385)
# ---------------------------------------------------------------------------


class TestFailurePaths:

    def test_failing_test_blocks_completion(self, tmp_path, monkeypatch):
        """R-0199: Failing tests must block completed_verified."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job
        from packages.orchestration.job_fulfillment import run_job_fulfill
        from packages.orchestration.storage import save_job

        # Create demo repo with failing test
        repo = tmp_path / "fail_repo"
        repo.mkdir()
        (repo / "README.md").write_text("# Test\n")
        (repo / "pyproject.toml").write_text(
            "[tool.pytest.ini_options]\ntestpaths = [\"tests\"]\n"
        )
        tests_dir = repo / "tests"
        tests_dir.mkdir()
        (tests_dir / "__init__.py").write_text("")
        (tests_dir / "test_fail.py").write_text(
            "def test_always_fails():\n"
            "    assert False, \"intentional failure\"\n"
        )

        job = Job(name="Fail test", metadata={"target_repo": str(repo)})
        save_job(job, root=tmp_path)
        record = run_job_fulfill(str(job.id), repo, data_dir=tmp_path)

        assert record.status.value != "completed_verified"
        assert record.test_passed is False
        assert "test_not_passed" in record.stop_reason

    def test_apply_blocked_stops_completion(self, tmp_path, monkeypatch):
        """R-0199: Apply blocked must stop fulfillment."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job
        from packages.orchestration.job_fulfillment import create_demo_repo, run_job_fulfill
        from packages.orchestration.storage import save_job

        repo = create_demo_repo(tmp_path)
        # Pre-create CHANGELOG.md so apply sees target_exists for create action
        (repo / "CHANGELOG.md").write_text("# Existing\n")

        job = Job(name="Apply blocked test", metadata={"target_repo": str(repo)})
        save_job(job, root=tmp_path)
        record = run_job_fulfill(str(job.id), repo, data_dir=tmp_path)

        assert record.status.value != "completed_verified"
        assert "apply_blocked" in record.stop_reason


# ---------------------------------------------------------------------------
# Proposed task lifecycle test (Step 3379)
# ---------------------------------------------------------------------------


class TestProposedTaskLifecycle:

    def test_proposed_tasks_accessible(self, tmp_path, monkeypatch):
        """R-0196: Proposed tasks can be listed and acted on after fulfillment."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job
        from packages.orchestration.job_fulfillment import create_demo_repo, run_job_fulfill
        from packages.orchestration.proposed_tasks import (
            approve_proposed_task,
            defer_proposed_task,
            load_proposed_tasks,
            reject_proposed_task,
        )
        from packages.orchestration.storage import save_job

        repo = create_demo_repo(tmp_path)
        job = Job(name="Propose test", metadata={"target_repo": str(repo)})
        save_job(job, root=tmp_path)
        record = run_job_fulfill(str(job.id), repo, data_dir=tmp_path)

        assert record.status.value == "completed_verified"
        assert len(record.next_suggestion_ids) >= 3

        # Load and verify
        tasks = load_proposed_tasks(str(job.id), root=tmp_path)
        assert len(tasks) >= 3

        # Approve/reject/defer
        ids = [t.id for t in tasks]
        approve_proposed_task(str(job.id), ids[0], root=tmp_path)
        reject_proposed_task(str(job.id), ids[1], reason="not needed", root=tmp_path)
        defer_proposed_task(str(job.id), ids[2], reason="later", root=tmp_path)

        updated = load_proposed_tasks(str(job.id), root=tmp_path)
        statuses = {t.id: t.status.value for t in updated}
        assert statuses[ids[0]] == "approved_for_build"
        assert statuses[ids[1]] == "rejected"
        assert statuses[ids[2]] == "deferred"


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
# Docs tests (Step 3327, 3378, 3381, 3396-3398)
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

    def test_guide_no_invalid_job_id_syntax(self):
        """R-0196: No --job-id syntax in demo guide."""
        path = _ROOT / "docs" / "first-fulfilled-job-demo-v0.md"
        text = path.read_text()
        assert "--job-id" not in text

    def test_quickstart_no_invalid_propose_syntax(self):
        """R-0196: No --job-id in propose command in quickstart."""
        path = _ROOT / "docs" / "simple-operator-quickstart-v0.md"
        text = path.read_text()
        assert "propose list --job-id" not in text


# ---------------------------------------------------------------------------
# Command catalog tests (Step 3329, 3382)
# ---------------------------------------------------------------------------


class TestFulfillCatalog:

    def test_job_fulfill_in_catalog(self):
        from apps.cli.command_catalog import get_command
        cmd = get_command("job.fulfill")
        assert cmd is not None
        assert cmd.action_class == "apply_write"
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
