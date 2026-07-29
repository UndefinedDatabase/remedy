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
            staging_used=True,
            staging_promoted=True,
            promotion_files=["CHANGELOG.md"],
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
            staging_used=True,
            staging_promoted=True,
            promotion_files=["CHANGELOG.md"],
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
            staging_used=True,
            staging_promoted=True,
            promotion_files=["CHANGELOG.md"],
        )
        passed, blockers = JobFulfillmentContract().check(rec)
        assert passed
        assert blockers == []


    def test_staging_not_used_blocks(self):
        from packages.orchestration.job_fulfillment import (
            JobFulfillmentContract,
            JobFulfillmentRecord,
        )
        rec = JobFulfillmentRecord(
            task_ids=["t1"], apply_ids=["a1"], test_passed=True,
            proof_status="verified", final_review_status="pass",
            staging_used=False,
        )
        passed, blockers = JobFulfillmentContract().check(rec)
        assert not passed
        assert "staging_not_used" in blockers


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
        assert data["staging_used"] is True
        assert data["staging_promoted"] is True


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

    def test_existing_md_uses_modify_intent(self, tmp_path, monkeypatch):
        """R-0199: Existing MD files use modify intent and succeed (not blocked)."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job
        from packages.orchestration.job_fulfillment import create_demo_repo, run_job_fulfill
        from packages.orchestration.storage import save_job

        repo = create_demo_repo(tmp_path)
        # Pre-create CHANGELOG.md — should trigger modify intent, not create
        (repo / "CHANGELOG.md").write_text("# Existing\n")

        job = Job(name="Existing MD test", metadata={"target_repo": str(repo)})
        save_job(job, root=tmp_path)
        record = run_job_fulfill(str(job.id), repo, data_dir=tmp_path)

        # With modify intent, apply succeeds and fulfillment completes
        assert record.status.value == "completed_verified"
        assert record.staging_promoted


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
        """A bad id is reported on stderr and nothing is printed to stdout."""
        from apps.cli.commands.job import _cmd_job_fulfill

        out, err = io.StringIO(), io.StringIO()
        code = None
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                _cmd_job_fulfill("not-a-uuid", fixture_demo=True, json_output=True)
            except SystemExit as exc:
                code = exc.code
        assert code not in (None, 0)
        assert "invalid job ID" in err.getvalue()
        assert out.getvalue().strip() == ""

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
        path = _ROOT / "docs" / "system" / "first-fulfilled-job-demo-v0.md"
        assert path.exists()

    def test_guide_mentions_fulfill(self):
        path = _ROOT / "docs" / "system" / "first-fulfilled-job-demo-v0.md"
        text = path.read_text()
        assert "job fulfill" in text
        assert "fixture-demo" in text

    def test_guide_mentions_status_report(self):
        path = _ROOT / "docs" / "system" / "first-fulfilled-job-demo-v0.md"
        text = path.read_text()
        assert "job status" in text
        assert "job report" in text

    def test_guide_mentions_propose(self):
        path = _ROOT / "docs" / "system" / "first-fulfilled-job-demo-v0.md"
        text = path.read_text()
        assert "propose list" in text

    def test_guide_no_real_provider_claims(self):
        path = _ROOT / "docs" / "system" / "first-fulfilled-job-demo-v0.md"
        text = path.read_text()
        assert "No real provider" in text

    def test_guide_no_invalid_job_id_syntax(self):
        """R-0196: No --job-id syntax in demo guide."""
        path = _ROOT / "docs" / "system" / "first-fulfilled-job-demo-v0.md"
        text = path.read_text()
        assert "--job-id" not in text

    def test_quickstart_no_invalid_propose_syntax(self):
        """R-0196: No --job-id in propose command in quickstart."""
        path = _ROOT / "docs" / "guides" / "simple-operator-quickstart-v0.md"
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


# ---------------------------------------------------------------------------
# Unit tests: staging workspace (Steps 3524-3527)
# ---------------------------------------------------------------------------


class TestStagingWorkspace:

    def test_filtered_copy_excludes_git(self, tmp_path):
        from packages.orchestration.staging_workspace import create_staging_workspace

        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "README.md").write_text("# Hi")
        (repo / ".git").mkdir()
        (repo / ".git" / "config").write_text("[core]")
        (repo / "__pycache__").mkdir()
        (repo / "__pycache__" / "foo.pyc").write_text("bytecode")

        staging_parent = tmp_path / "staging"
        staging_parent.mkdir()
        ws = create_staging_workspace(repo, staging_parent, "job-123")

        assert (ws.staging_dir / "README.md").exists()
        assert not (ws.staging_dir / ".git").exists()
        assert not (ws.staging_dir / "__pycache__").exists()
        assert ws.files_copied == 1  # only README.md

    def test_filtered_copy_preserves_structure(self, tmp_path):
        from packages.orchestration.staging_workspace import create_staging_workspace

        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "src").mkdir()
        (repo / "src" / "main.py").write_text("x = 1")
        (repo / "docs").mkdir()
        (repo / "docs" / "guide.md").write_text("# Guide")

        staging_parent = tmp_path / "staging"
        staging_parent.mkdir()
        ws = create_staging_workspace(repo, staging_parent, "job-456")

        assert (ws.staging_dir / "src" / "main.py").exists()
        assert (ws.staging_dir / "docs" / "guide.md").exists()

    def test_discard_removes_staging(self, tmp_path):
        from packages.orchestration.staging_workspace import (
            create_staging_workspace,
            discard_staging,
        )

        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "f.txt").write_text("data")

        staging_parent = tmp_path / "staging"
        staging_parent.mkdir()
        ws = create_staging_workspace(repo, staging_parent, "job-789")
        assert ws.staging_dir.exists()

        discard_staging(ws, "test")
        assert not ws.staging_dir.exists()
        assert not ws.active

    def test_find_staged_changes(self, tmp_path):
        from packages.orchestration.staging_workspace import (
            create_staging_workspace,
            find_staged_changes,
        )

        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "existing.md").write_text("old content")

        staging_parent = tmp_path / "staging"
        staging_parent.mkdir()
        ws = create_staging_workspace(repo, staging_parent, "job-abc")

        # Modify a file in staging
        (ws.staging_dir / "existing.md").write_text("new content")
        # Create a new file in staging
        (ws.staging_dir / "new_file.md").write_text("brand new")

        changes = find_staged_changes(ws)
        rel_paths = [r.relative_path for r in changes]
        assert "existing.md" in rel_paths
        assert "new_file.md" in rel_paths


# ---------------------------------------------------------------------------
# Unit tests: promotion gate (Steps 3534-3536)
# ---------------------------------------------------------------------------


class TestPromotionGate:

    def test_promotion_requires_gates_passed(self, tmp_path):
        from packages.orchestration.staging_workspace import (
            StagingApplyRecord,
            StagingWorkspace,
            promote_staged_changes,
        )

        ws = StagingWorkspace(
            staging_dir=tmp_path / "staging",
            target_repo=tmp_path / "target",
            job_id="j1",
        )
        records = [StagingApplyRecord(relative_path="f.md", action="create")]
        result = promote_staged_changes(ws, records, gates_passed=False)
        assert not result.promoted
        assert result.reason == "gates_not_passed"

    def test_promotion_creates_new_files(self, tmp_path):
        from packages.orchestration.staging_workspace import (
            StagingApplyRecord,
            StagingWorkspace,
            promote_staged_changes,
        )

        staging = tmp_path / "staging"
        staging.mkdir()
        (staging / "new.md").write_text("# New File\n")

        target = tmp_path / "target"
        target.mkdir()

        ws = StagingWorkspace(staging_dir=staging, target_repo=target, job_id="j2")
        records = [StagingApplyRecord(relative_path="new.md", action="create")]
        result = promote_staged_changes(ws, records, gates_passed=True)

        assert result.promoted
        assert "new.md" in result.files_promoted
        assert (target / "new.md").exists()

    def test_promotion_skips_existing_target_for_create(self, tmp_path):
        from packages.orchestration.staging_workspace import (
            StagingApplyRecord,
            StagingWorkspace,
            promote_staged_changes,
        )

        staging = tmp_path / "staging"
        staging.mkdir()
        (staging / "exists.md").write_text("staged version")

        target = tmp_path / "target"
        target.mkdir()
        (target / "exists.md").write_text("original")

        ws = StagingWorkspace(staging_dir=staging, target_repo=target, job_id="j3")
        records = [StagingApplyRecord(relative_path="exists.md", action="create")]
        result = promote_staged_changes(ws, records, gates_passed=True)

        assert "exists.md" in result.files_skipped
        # Original content preserved
        assert (target / "exists.md").read_text() == "original"


# ---------------------------------------------------------------------------
# Integration: staging in fulfillment (Steps 3531-3533)
# ---------------------------------------------------------------------------


class TestStagedFulfillment:

    def _setup_job(self, tmp_path):
        from packages.core.models import Job
        from packages.orchestration.job_fulfillment import create_demo_repo
        from packages.orchestration.storage import save_job

        repo = create_demo_repo(tmp_path)
        job = Job(name="Staged test", metadata={"target_repo": str(repo)})
        save_job(job, root=tmp_path)
        return job, repo

    def test_staging_used_in_fulfillment(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.job_fulfillment import run_job_fulfill

        job, repo = self._setup_job(tmp_path)
        record = run_job_fulfill(str(job.id), repo, data_dir=tmp_path)

        assert record.staging_used is True
        assert record.status.value == "completed_verified"

    def test_staging_promoted_on_success(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.job_fulfillment import run_job_fulfill

        job, repo = self._setup_job(tmp_path)
        record = run_job_fulfill(str(job.id), repo, data_dir=tmp_path)

        assert record.staging_promoted is True
        assert len(record.promotion_files) > 0

    def test_target_repo_restored_after_staging(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from uuid import UUID

        from packages.orchestration.job_fulfillment import run_job_fulfill
        from packages.orchestration.storage import load_job

        job, repo = self._setup_job(tmp_path)
        record = run_job_fulfill(str(job.id), repo, data_dir=tmp_path)

        # After fulfillment, target_repo should point to real repo, not staging
        final_job = load_job(UUID(str(job.id)), tmp_path)
        assert final_job.metadata["target_repo"] == str(repo.resolve())
        assert "staging" not in final_job.metadata["target_repo"]

    def test_files_exist_in_real_repo_after_promotion(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.job_fulfillment import run_job_fulfill

        job, repo = self._setup_job(tmp_path)
        record = run_job_fulfill(str(job.id), repo, data_dir=tmp_path)

        # Files should exist in real repo after promotion
        for f in record.changed_files:
            assert (repo / f).exists(), f"File {f} not in target repo after promotion"

    def test_staging_discarded_on_test_failure(self, tmp_path, monkeypatch):
        """Target repo must be untouched when tests fail in staging."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from uuid import UUID

        from packages.core.models import Job
        from packages.orchestration.job_fulfillment import run_job_fulfill
        from packages.orchestration.storage import load_job, save_job

        # Create repo with failing test
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
            "    assert False, \"intentional\"\n"
        )

        job = Job(name="Staging fail test", metadata={"target_repo": str(repo)})
        save_job(job, root=tmp_path)
        record = run_job_fulfill(str(job.id), repo, data_dir=tmp_path)

        # Should not be completed
        assert record.status.value != "completed_verified"
        assert record.staging_used is True
        assert record.staging_promoted is False

        # target_repo restored to real repo
        final_job = load_job(UUID(str(job.id)), tmp_path)
        assert final_job.metadata["target_repo"] == str(repo.resolve())

    def test_export_includes_staging_fields(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.job_fulfillment import (
            export_job_fulfillment_json,
            run_job_fulfill,
        )

        job, repo = self._setup_job(tmp_path)
        record = run_job_fulfill(str(job.id), repo, data_dir=tmp_path)
        data = export_job_fulfillment_json(record)

        assert "staging_used" in data
        assert "staging_promoted" in data
        assert "staged_files" in data
        assert "promotion_files" in data
        assert data["staging_used"] is True
        assert data["staging_promoted"] is True


# ---------------------------------------------------------------------------
# No staging dir leaked (Step 3538)
# ---------------------------------------------------------------------------


class TestStagingCleanup:

    def test_no_staging_dir_after_success(self, tmp_path, monkeypatch):
        """Staging dir must be cleaned up after successful promotion."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        import glob as glob_mod

        from packages.core.models import Job
        from packages.orchestration.job_fulfillment import create_demo_repo, run_job_fulfill
        from packages.orchestration.storage import save_job

        repo = create_demo_repo(tmp_path)
        job = Job(name="Cleanup test", metadata={"target_repo": str(repo)})
        save_job(job, root=tmp_path)
        run_job_fulfill(str(job.id), repo, data_dir=tmp_path)

        # No staging_* dirs should remain in /tmp
        import tempfile
        staging_dirs = glob_mod.glob(
            str(Path(tempfile.gettempdir()) / "remedy_staging_*" / "staging_*")
        )
        # Filter to only dirs for this job (they should be cleaned up)
        for d in staging_dirs:
            if str(job.id)[:16] in d:
                assert False, f"Staging dir not cleaned up: {d}"


# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# v0.3 Regression Tests — Metadata, Filtered Copy, Promotion Safety
# ---------------------------------------------------------------------------


class TestMetadataNeverMutated:
    """target_repo in saved job metadata must never be changed to staging path."""

    def test_target_repo_unchanged_on_success(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job
        from packages.orchestration.job_fulfillment import create_demo_repo, run_job_fulfill
        from packages.orchestration.storage import load_job, save_job

        repo = create_demo_repo(tmp_path)
        job = Job(name="Meta test", metadata={"target_repo": str(repo)})
        save_job(job, root=tmp_path)

        original_target = str(repo.resolve())
        run_job_fulfill(str(job.id), repo, data_dir=tmp_path)

        reloaded = load_job(job.id, tmp_path)
        saved_target = reloaded.metadata.get("target_repo", "")
        assert saved_target == original_target, f"target_repo mutated: {saved_target}"
        assert "staging" not in saved_target.lower()

    def test_target_repo_unchanged_on_test_failure(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job
        from packages.orchestration.job_fulfillment import create_demo_repo, run_job_fulfill
        from packages.orchestration.storage import load_job, save_job

        repo = create_demo_repo(tmp_path)
        # Break the test so it fails
        test_file = repo / "tests" / "test_demo.py"
        test_file.write_text("def test_fail(): assert False\n")
        job = Job(name="Meta fail test", metadata={"target_repo": str(repo)})
        save_job(job, root=tmp_path)

        original_target = str(repo.resolve())
        record = run_job_fulfill(str(job.id), repo, data_dir=tmp_path)

        reloaded = load_job(job.id, tmp_path)
        saved_target = reloaded.metadata.get("target_repo", "")
        assert saved_target == original_target
        assert "staging" not in saved_target.lower()


class TestFilteredCopySafety:
    """Filtered copy must exclude .env variants and symlink escapes."""

    def test_env_variants_excluded(self, tmp_path):
        from packages.orchestration.staging_workspace import create_staging_workspace

        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "README.md").write_text("# Test")
        (repo / ".env").write_text("SECRET=bad")
        (repo / ".env.local").write_text("LOCAL=bad")
        (repo / ".env.production").write_text("PROD=bad")
        (repo / ".env-staging").write_text("STAGING=bad")

        staging_parent = tmp_path / "staging"
        ws = create_staging_workspace(repo, staging_parent, "test123")

        staging_files = [f.name for f in ws.staging_dir.rglob("*") if f.is_file()]
        assert ".env" not in staging_files
        assert ".env.local" not in staging_files
        assert ".env.production" not in staging_files
        assert ".env-staging" not in staging_files
        assert "README.md" in staging_files
        assert len(ws.excluded_env_files) == 4

    def test_symlink_escape_excluded(self, tmp_path):
        from packages.orchestration.staging_workspace import create_staging_workspace

        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "README.md").write_text("# Test")

        external = tmp_path / "external_secret.txt"
        external.write_text("SECRET DATA")
        (repo / "escape_link").symlink_to(external)

        staging_parent = tmp_path / "staging"
        ws = create_staging_workspace(repo, staging_parent, "test123")

        staging_files = [f.name for f in ws.staging_dir.rglob("*") if f.is_file()]
        assert "escape_link" not in staging_files
        assert "README.md" in staging_files
        assert len(ws.excluded_symlinks) >= 1


class TestPromotionSafety:
    """Promotion must enforce MD-only and prefix-based append-only."""

    def test_non_markdown_blocked(self, tmp_path):
        from packages.orchestration.staging_workspace import (
            StagingApplyRecord,
            StagingWorkspace,
            promote_staged_changes,
        )

        target = tmp_path / "target"
        target.mkdir()
        staging = tmp_path / "staging"
        staging.mkdir()
        (staging / "config.py").write_text("import os")

        ws = StagingWorkspace(staging_dir=staging, target_repo=target, job_id="test")
        records = [StagingApplyRecord(
            relative_path="config.py", action="create", scope="staged",
        )]

        result = promote_staged_changes(ws, records, gates_passed=True)
        assert not result.promoted
        assert "config.py" in result.files_blocked
        assert any("non_markdown" in b for b in result.blockers)
        assert not (target / "config.py").exists()

    def test_md_append_only_prefix(self, tmp_path):
        from packages.orchestration.staging_workspace import (
            StagingApplyRecord,
            StagingWorkspace,
            promote_staged_changes,
        )

        target = tmp_path / "target"
        target.mkdir()
        staging = tmp_path / "staging"
        staging.mkdir()

        original = "# Title\n\nExisting content.\n"
        appended = original + "\n## New Section\n\nNew content.\n"

        (target / "doc.md").write_text(original)
        (staging / "doc.md").write_text(appended)

        ws = StagingWorkspace(staging_dir=staging, target_repo=target, job_id="test")
        records = [StagingApplyRecord(
            relative_path="doc.md", action="modify", scope="staged",
        )]

        result = promote_staged_changes(ws, records, gates_passed=True)
        assert result.promoted
        final = (target / "doc.md").read_text()
        assert final == appended

    def test_md_replacement_blocked(self, tmp_path):
        from packages.orchestration.staging_workspace import (
            StagingApplyRecord,
            StagingWorkspace,
            promote_staged_changes,
        )

        target = tmp_path / "target"
        target.mkdir()
        staging = tmp_path / "staging"
        staging.mkdir()

        original = "# Title\n\nExisting content.\n"
        replaced = "# Different Title\n\nReplaced content.\n"

        (target / "doc.md").write_text(original)
        (staging / "doc.md").write_text(replaced)

        ws = StagingWorkspace(staging_dir=staging, target_repo=target, job_id="test")
        records = [StagingApplyRecord(
            relative_path="doc.md", action="modify", scope="staged",
        )]

        result = promote_staged_changes(ws, records, gates_passed=True)
        assert not result.promoted
        assert "doc.md" in result.files_blocked
        assert any("prefix_mismatch" in b for b in result.blockers)
        assert (target / "doc.md").read_text() == original

    def test_path_traversal_blocked(self, tmp_path):
        from packages.orchestration.staging_workspace import (
            StagingApplyRecord,
            StagingWorkspace,
            promote_staged_changes,
        )

        target = tmp_path / "target"
        target.mkdir()
        staging = tmp_path / "staging"
        staging.mkdir()

        ws = StagingWorkspace(staging_dir=staging, target_repo=target, job_id="test")
        records = [StagingApplyRecord(
            relative_path="../../../etc/passwd.md", action="create", scope="staged",
        )]

        result = promote_staged_changes(ws, records, gates_passed=True)
        assert not result.promoted


class TestCodeAppliedTruth:
    """Failing test must leave target files unchanged."""

    def test_failing_test_leaves_target_unchanged(self, tmp_path, monkeypatch):
        import hashlib
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job
        from packages.orchestration.job_fulfillment import create_demo_repo, run_job_fulfill
        from packages.orchestration.storage import save_job

        repo = create_demo_repo(tmp_path)

        # Hash all files before fulfillment
        before_hashes = {}
        for f in repo.rglob("*"):
            if f.is_file():
                before_hashes[str(f.relative_to(repo))] = hashlib.sha256(f.read_bytes()).hexdigest()

        # Break the test
        test_file = repo / "tests" / "test_demo.py"
        test_file.write_text("def test_fail(): assert False\n")
        before_hashes["tests/test_demo.py"] = hashlib.sha256(
            test_file.read_bytes()
        ).hexdigest()

        job = Job(name="Truth test", metadata={"target_repo": str(repo)})
        save_job(job, root=tmp_path)

        record = run_job_fulfill(str(job.id), repo, data_dir=tmp_path)

        # All original files must be unchanged
        for rel, before_hash in before_hashes.items():
            f = repo / rel
            if f.exists():
                after_hash = hashlib.sha256(f.read_bytes()).hexdigest()
                assert after_hash == before_hash, f"File {rel} was modified despite test failure"

        # No new content files should exist (exclude pytest/pycache artifacts)
        after_files = {str(f.relative_to(repo)) for f in repo.rglob("*") if f.is_file()}
        new_files = after_files - set(before_hashes.keys())
        # Filter out test runner artifacts
        new_files = {f for f in new_files if not any(
            part in f for part in ("__pycache__", ".pytest_cache")
        )}
        assert not new_files, f"New files appeared in target despite test failure: {new_files}"


# ---------------------------------------------------------------------------
# v0.4 Regression Tests — Staged Tests, Target Truth, Promotion Contract
# ---------------------------------------------------------------------------


class TestStagedTestExecution:
    """Tests must run against staging dir, not target repo."""

    def test_target_repo_has_no_pytest_cache(self, tmp_path, monkeypatch):
        """After fulfillment, target repo must not contain .pytest_cache."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job
        from packages.orchestration.job_fulfillment import create_demo_repo, run_job_fulfill
        from packages.orchestration.storage import save_job

        repo = create_demo_repo(tmp_path)
        job = Job(name="Cache test", metadata={"target_repo": str(repo)})
        save_job(job, root=tmp_path)

        run_job_fulfill(str(job.id), repo, data_dir=tmp_path)

        # Target should not have .pytest_cache
        pytest_cache = repo / ".pytest_cache"
        assert not pytest_cache.exists(), "Target repo has .pytest_cache after fulfillment"

    def test_target_repo_has_no_pycache(self, tmp_path, monkeypatch):
        """After fulfillment, target repo must not contain test __pycache__."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job
        from packages.orchestration.job_fulfillment import create_demo_repo, run_job_fulfill
        from packages.orchestration.storage import save_job

        repo = create_demo_repo(tmp_path)
        # Remove any pre-existing __pycache__
        import shutil
        for pc in repo.rglob("__pycache__"):
            shutil.rmtree(pc)

        job = Job(name="Pycache test", metadata={"target_repo": str(repo)})
        save_job(job, root=tmp_path)

        run_job_fulfill(str(job.id), repo, data_dir=tmp_path)

        # No new __pycache__ in target
        pycache_dirs = list(repo.rglob("__pycache__"))
        assert not pycache_dirs, f"Target repo has __pycache__ after fulfillment: {pycache_dirs}"


class TestCodeAppliedTruthV04:
    """code_applied must reflect target promotion truth, not staged apply."""

    def test_successful_fulfillment_code_applied_true(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job
        from packages.orchestration.job_fulfillment import (
            create_demo_repo,
            run_job_fulfill,
        )
        from packages.orchestration.storage import save_job

        repo = create_demo_repo(tmp_path)
        job = Job(name="Applied test", metadata={"target_repo": str(repo)})
        save_job(job, root=tmp_path)

        record = run_job_fulfill(str(job.id), repo, data_dir=tmp_path)
        assert record.staging_promoted is True
        assert len(record.promotion_files) > 0

    def test_failing_test_code_applied_false(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job
        from packages.orchestration.job_fulfillment import (
            create_demo_repo,
            run_job_fulfill,
        )
        from packages.orchestration.storage import save_job

        repo = create_demo_repo(tmp_path)
        (repo / "tests" / "test_demo.py").write_text("def test_fail(): assert False\n")
        job = Job(name="Blocked test", metadata={"target_repo": str(repo)})
        save_job(job, root=tmp_path)

        record = run_job_fulfill(str(job.id), repo, data_dir=tmp_path)
        assert record.staging_promoted is False
        assert record.status.value == "blocked"


class TestBlockedFulfillmentStatus:
    """Blocked fulfillment must expose blockers and useful next action."""

    def test_blocked_has_stop_reason(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job
        from packages.orchestration.job_fulfillment import create_demo_repo, run_job_fulfill
        from packages.orchestration.storage import save_job

        repo = create_demo_repo(tmp_path)
        (repo / "tests" / "test_demo.py").write_text("def test_fail(): assert False\n")
        job = Job(name="Stop reason test", metadata={"target_repo": str(repo)})
        save_job(job, root=tmp_path)

        record = run_job_fulfill(str(job.id), repo, data_dir=tmp_path)
        assert record.stop_reason, "Blocked fulfillment must have stop_reason"
        assert "test_not_passed" in record.stop_reason

    def test_blocked_has_next_action(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job
        from packages.orchestration.job_fulfillment import create_demo_repo, run_job_fulfill
        from packages.orchestration.storage import save_job

        repo = create_demo_repo(tmp_path)
        (repo / "tests" / "test_demo.py").write_text("def test_fail(): assert False\n")
        job = Job(name="Next action test", metadata={"target_repo": str(repo)})
        save_job(job, root=tmp_path)

        record = run_job_fulfill(str(job.id), repo, data_dir=tmp_path)
        assert record.next_safe_action, "Blocked fulfillment must have next_safe_action"
        assert "remedy" in record.next_safe_action
        assert "no pending tasks" not in record.next_safe_action


class TestApplyScope:
    """Apply records must distinguish staged vs target scope."""

    def test_staged_apply_has_staged_scope(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job
        from packages.orchestration.job_fulfillment import create_demo_repo, run_job_fulfill
        from packages.orchestration.storage import load_job, save_job

        repo = create_demo_repo(tmp_path)
        job = Job(name="Scope test", metadata={"target_repo": str(repo)})
        save_job(job, root=tmp_path)

        run_job_fulfill(str(job.id), repo, data_dir=tmp_path)

        reloaded = load_job(job.id, tmp_path)
        for art in reloaded.artifacts:
            records = art.metadata.get("patch_intent_apply_records", {})
            for rec in records.values():
                if isinstance(rec, dict) and rec.get("state") == "applied":
                    assert rec.get("scope") == "staged", (
                        f"Apply record scope should be 'staged', got {rec.get('scope')}"
                    )


class TestPromotionContract:
    """Contract must require target promotion for completed_verified."""

    def test_requires_target_promotion(self):
        from packages.orchestration.job_fulfillment import (
            JobFulfillmentContract,
            JobFulfillmentRecord,
        )

        record = JobFulfillmentRecord(
            job_id="test",
            mode="fixture_demo",
            task_ids=["t1"],
            apply_ids=["a1"],
            test_passed=True,
            proof_status="accepted",
            proof_accepted_reason="fixture demo",
            final_review_status="pass",
            staging_used=True,
            staging_promoted=False,  # NOT promoted
            promotion_files=[],
        )
        contract = JobFulfillmentContract()
        passed, blockers = contract.check(record)
        assert not passed
        assert "target_not_promoted" in blockers or "no_promotion_files" in blockers

    def test_promoted_allows_completion(self):
        from packages.orchestration.job_fulfillment import (
            JobFulfillmentContract,
            JobFulfillmentRecord,
        )

        record = JobFulfillmentRecord(
            job_id="test",
            mode="fixture_demo",
            task_ids=["t1"],
            apply_ids=["a1"],
            test_passed=True,
            proof_status="accepted",
            proof_accepted_reason="fixture demo",
            final_review_status="pass",
            staging_used=True,
            staging_promoted=True,
            promotion_files=["CHANGELOG.md"],
        )
        contract = JobFulfillmentContract()
        passed, blockers = contract.check(record)
        assert passed, f"Contract should pass with promotion, got blockers: {blockers}"


class TestExistingMarkdownFulfillment:
    """Existing Markdown files must work via append-only in actual fulfillment."""

    def test_existing_changelog_appended(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job
        from packages.orchestration.job_fulfillment import create_demo_repo, run_job_fulfill
        from packages.orchestration.storage import save_job

        repo = create_demo_repo(tmp_path)
        # Pre-create CHANGELOG.md (fixture normally creates it)
        changelog = repo / "CHANGELOG.md"
        original_content = "# Existing Changelog\n\nPrevious entries.\n"
        changelog.write_text(original_content)

        job = Job(name="Append test", metadata={"target_repo": str(repo)})
        save_job(job, root=tmp_path)

        record = run_job_fulfill(str(job.id), repo, data_dir=tmp_path)
        assert record.status.value == "completed_verified", (
            f"Expected completed_verified, got {record.status.value}: {record.stop_reason}"
        )

        # Original content must be preserved
        final_content = changelog.read_text()
        assert final_content.startswith(original_content), (
            "Original changelog content was not preserved"
        )


class TestReviewBundleFulfillment:
    """Review bundle must include fulfillment/staging/promotion truth."""

    def test_fulfillment_summary_in_bundle(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job
        from packages.orchestration.job_fulfillment import create_demo_repo, run_job_fulfill
        from packages.orchestration.review_bundle import build_review_bundle
        from packages.orchestration.storage import save_job

        repo = create_demo_repo(tmp_path)
        job = Job(name="Bundle test", metadata={"target_repo": str(repo)})
        save_job(job, root=tmp_path)

        run_job_fulfill(str(job.id), repo, data_dir=tmp_path)

        result = build_review_bundle(str(job.id))
        section_names = [s.filename for s in result.sections]
        assert "fulfillment_summary.json" in section_names

        # Check the section was included (not degraded)
        for s in result.sections:
            if s.filename == "fulfillment_summary.json":
                assert s.status == "included", f"Fulfillment section status: {s.status}"


class TestDemoDocsCommands:
    """Demo docs commands must match actual CLI support."""

    def test_job_create_no_json_flag(self):
        """job create does not support --json — docs must not claim it."""
        docs = (_ROOT / "docs" / "system" / "first-fulfilled-job-demo-v0.md").read_text()
        # Should NOT have 'job create' with --json
        create_lines = [l for l in docs.splitlines() if "job create" in l and "remedy" in l]
        for line in create_lines:
            assert "--json" not in line, f"job create should not use --json: {line}"

    def test_fulfill_command_exists(self):
        """job fulfill --fixture-demo must be a valid CLI subcommand."""
        from apps.cli.commands.job import COMMAND_HANDLERS
        assert "job.fulfill" in COMMAND_HANDLERS, "job.fulfill not in CLI COMMAND_HANDLERS"

    def test_status_command_exists(self):
        from apps.cli.commands.job import COMMAND_HANDLERS
        assert "job.status" in COMMAND_HANDLERS

    def test_report_command_exists(self):
        from apps.cli.commands.job import COMMAND_HANDLERS
        assert "job.report" in COMMAND_HANDLERS

    def test_demo_docs_command_shapes(self):
        """All remedy commands in demo docs must be valid shapes."""
        docs = (_ROOT / "docs" / "system" / "first-fulfilled-job-demo-v0.md").read_text()
        cmd_lines = [l.strip() for l in docs.splitlines()
                     if l.strip().startswith("remedy ") or l.strip().startswith("JOB_ID=$(remedy ")]
        assert len(cmd_lines) >= 4, f"Expected >=4 commands, got {len(cmd_lines)}"
        for line in cmd_lines:
            # No --json on job create
            if "job create" in line:
                assert "--json" not in line, f"job create must not use --json: {line}"


# ---------------------------------------------------------------------------
# v0.5 regression tests (Steps 3660-3668)
# ---------------------------------------------------------------------------


class TestBlockedFulfillmentTruthV05:
    """Blocked fulfillment must expose honest stop_reason and changed_files."""

    def _run_blocked(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job
        from packages.orchestration.job_fulfillment import create_demo_repo, run_job_fulfill
        from packages.orchestration.storage import save_job

        repo = create_demo_repo(tmp_path)
        # Create a conftest that makes tests fail
        (repo / "conftest.py").write_text("def pytest_collection_modifyitems(items):\n    raise SystemExit(1)\n")
        job = Job(name="Blocked test", metadata={"target_repo": str(repo)})
        save_job(job, root=tmp_path)
        record = run_job_fulfill(str(job.id), repo, data_dir=tmp_path)
        return job, record

    def test_blocked_has_stop_reason(self, tmp_path, monkeypatch):
        _, record = self._run_blocked(tmp_path, monkeypatch)
        assert record.status.value != "completed_verified"
        assert record.stop_reason != ""

    def test_blocked_has_empty_changed_target_files(self, tmp_path, monkeypatch):
        _, record = self._run_blocked(tmp_path, monkeypatch)
        assert record.changed_target_files == []

    def test_blocked_staging_not_promoted(self, tmp_path, monkeypatch):
        _, record = self._run_blocked(tmp_path, monkeypatch)
        assert record.staging_promoted is False

    def test_blocked_code_applied_false(self, tmp_path, monkeypatch):
        job, _ = self._run_blocked(tmp_path, monkeypatch)
        from apps.cli.commands.job import _extract_job_truth
        truth = _extract_job_truth(job)
        assert truth['code_applied'] is False

    def test_blocked_latest_stop_reason_not_empty(self, tmp_path, monkeypatch):
        job, _ = self._run_blocked(tmp_path, monkeypatch)
        from apps.cli.commands.job import _extract_job_truth
        truth = _extract_job_truth(job)
        assert truth['latest_stop_reason'] != ''

    def test_blocked_has_fulfillment_blockers(self, tmp_path, monkeypatch):
        job, _ = self._run_blocked(tmp_path, monkeypatch)
        from apps.cli.commands.job import _extract_job_truth
        truth = _extract_job_truth(job)
        assert truth['fulfillment_blockers']


class TestSuccessfulFulfillmentTruthV05:
    """Successful fulfillment must show promoted target files."""

    def test_changed_target_files_match_promotion(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job
        from packages.orchestration.job_fulfillment import create_demo_repo, run_job_fulfill
        from packages.orchestration.storage import save_job

        repo = create_demo_repo(tmp_path)
        job = Job(name="Success test", metadata={"target_repo": str(repo)})
        save_job(job, root=tmp_path)
        record = run_job_fulfill(str(job.id), repo, data_dir=tmp_path)

        assert record.status.value == "completed_verified"
        assert record.changed_target_files == record.promotion_files
        assert len(record.changed_target_files) > 0
        # staged_files may be broader than changed_target_files
        for f in record.changed_target_files:
            assert f in record.staged_files


class TestReviewBundleSafeError:
    """Review bundle must not leak raw exception text."""

    def test_error_no_raw_traceback(self):
        from pathlib import Path

        from packages.orchestration.review_bundle import _build_fulfillment_summary
        # Non-existent data_dir triggers error path
        result = _build_fulfillment_summary("nonexistent-job", Path("/tmp/no-such-dir"))
        assert result["status"] in ("no_fulfillment_records", "error")
        if result["status"] == "error":
            assert "error_type" in result
            assert "error" not in result  # no raw str(exc)


# ---------------------------------------------------------------------------
# v0.6 — Review bundle side-effect + public truth (Steps 3696-3714)
# ---------------------------------------------------------------------------


class TestIntegrityReadOnlyV07:
    """_integrity_status() and _build_integrity_summary() must be truly read-only.

    No subprocess. No run_integrity_checks(). No .agent file reads.
    """

    def test_integrity_status_no_run_integrity_checks(self, monkeypatch):
        """run_integrity_checks must not be called at all."""
        import packages.orchestration.integrity_gate as ig

        def bomb(**kwargs):
            raise AssertionError("run_integrity_checks must not be called from readiness")

        monkeypatch.setattr(ig, "run_integrity_checks", bomb)

        from packages.orchestration.overnight_readiness import _integrity_status
        result = _integrity_status()
        assert result == "unknown"

    def test_integrity_status_no_subprocess(self, monkeypatch):
        """No subprocess.run from _integrity_status."""
        import subprocess as sp

        original_run = sp.run

        def bomb(*args, **kwargs):
            raise AssertionError(f"subprocess.run called: {args}")

        monkeypatch.setattr(sp, "run", bomb)

        from packages.orchestration.overnight_readiness import _integrity_status
        result = _integrity_status()
        assert result == "unknown"

    def test_build_integrity_summary_no_run_integrity_checks(self, monkeypatch):
        """Review bundle integrity must not call run_integrity_checks."""
        import packages.orchestration.integrity_gate as ig

        def bomb(**kwargs):
            raise AssertionError("run_integrity_checks must not be called from bundle")

        monkeypatch.setattr(ig, "run_integrity_checks", bomb)

        from packages.orchestration.review_bundle import _build_integrity_summary
        result = _build_integrity_summary()
        assert result.get("status") == "unknown"

    def test_build_integrity_summary_no_subprocess(self, monkeypatch):
        """No subprocess.run from _build_integrity_summary."""
        import subprocess as sp

        def bomb(*args, **kwargs):
            raise AssertionError(f"subprocess.run called: {args}")

        monkeypatch.setattr(sp, "run", bomb)

        from packages.orchestration.review_bundle import _build_integrity_summary
        result = _build_integrity_summary()
        assert result.get("status") == "unknown"

    def test_no_agent_dependency(self, tmp_path, monkeypatch):
        """Read-only integrity works without .agent directory."""
        monkeypatch.chdir(tmp_path)

        from packages.orchestration.integrity_gate import export_readonly_integrity_status
        result = export_readonly_integrity_status()
        assert result["status"] == "unknown"
        assert result["passed"] is None

        from packages.orchestration.overnight_readiness import _integrity_status
        assert _integrity_status() == "unknown"


class TestChangedFilesPublicTruth:
    """Public changed_files must equal changed_target_files, not staged files."""

    def test_export_changed_files_equals_target(self):
        from packages.orchestration.job_fulfillment import (
            JobFulfillmentRecord,
            export_job_fulfillment_json,
        )
        rec = JobFulfillmentRecord(job_id="test-123", mode="fixture_demo")
        rec.changed_files = ["staged_only.md"]
        rec.changed_target_files = ["promoted.md"]
        rec.staged_files = ["staged_only.md"]
        exported = export_job_fulfillment_json(rec)
        assert exported["changed_files"] == ["promoted.md"], \
            "Public changed_files must equal changed_target_files"
        assert exported["changed_target_files"] == ["promoted.md"]
        assert exported["staged_files"] == ["staged_only.md"]

    def test_blocked_export_changed_files_empty(self):
        from packages.orchestration.job_fulfillment import (
            JobFulfillmentRecord,
            export_job_fulfillment_json,
        )
        rec = JobFulfillmentRecord(job_id="test-123", mode="fixture_demo")
        rec.changed_files = ["staged_only.md"]
        rec.changed_target_files = []
        exported = export_job_fulfillment_json(rec)
        assert exported["changed_files"] == [], \
            "Blocked job changed_files must be empty"


class TestChangedFilesSafeScope:
    """changed_files_safe.json must include scope metadata."""

    def test_scope_field_present(self):
        from unittest.mock import MagicMock

        from packages.orchestration.review_bundle import _build_changed_files_safe
        job = MagicMock()
        job.artifacts = []
        result = _build_changed_files_safe(job, [])
        assert result["scope"] == "artifact_intent"
        assert "scope_note" in result


class TestDocsCommandShapesV06:
    """Docs must not contain invalid job create --json."""

    def test_no_job_create_json_in_quickstart(self):
        path = _ROOT / "docs" / "guides" / "simple-operator-quickstart-v0.md"
        if not path.exists():
            return
        content = path.read_text()
        assert "job create" not in content or "--json" not in content.split("job create")[1].split("\n")[0], \
            "simple-operator-quickstart must not use 'job create --json'"

    def test_no_job_create_json_in_any_doc(self):
        docs_dir = _ROOT / "docs"
        if not docs_dir.exists():
            return
        for md in docs_dir.glob("*.md"):
            content = md.read_text()
            for i, line in enumerate(content.splitlines(), 1):
                if "job create" in line and "--json" in line:
                    raise AssertionError(
                        f"{md.name}:{i} contains invalid 'job create --json'"
                    )
