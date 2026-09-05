"""Tests for remedy do v1 phased flow + truth closure.

Covers:
- Phase model (DoRunPhase, DoRunResult, DoRunContract)
- Init/plan/context/build/intent/approval/proof phases
- Stop reasons and next safe actions
- Export JSON contract
- Safety (no raw content, no secrets, no traceback)
- Approval gate enforcement
- Context/proof alignment
- Step 926-927: Full next_safe_action catalog validation
- Step 928: Context failure stops run
- Step 929: Catalog metadata truth
- Step 930: Contract consolidation
- Step 931: max_loops enforcement
- Step 932: Autonomy level truth
- Step 933: Approval gate regression
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from unittest.mock import patch

from packages.core.models import Job
from packages.orchestration.do_run import (
    DO_PHASES,
    DoRunNextAction,
    DoRunPhase,
    DoRunStopReason,
    export_do_run_json,
    run_do,
    summarize_do_run,
    validate_next_safe_action_command,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "pyproject.toml").write_text("[project]\nname = 'test'")
    (repo / "README.md").write_text("# Test project")
    src = repo / "src"
    src.mkdir()
    (src / "example.py").write_text("def hello(): return 'world'")
    (repo / ".env.secret").write_text("API_KEY=secret123")
    return repo


def _run_with_tmp(tmp_path, goal="safe docs change", autonomy=3, max_loops=1):
    repo = _make_repo(tmp_path)
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    old = os.environ.get("REMEDY_DATA_DIR")
    os.environ["REMEDY_DATA_DIR"] = str(data_dir)
    try:
        return run_do(goal, str(repo), autonomy_level=autonomy, max_loops=max_loops)
    finally:
        if old:
            os.environ["REMEDY_DATA_DIR"] = old
        else:
            os.environ.pop("REMEDY_DATA_DIR", None)


# ---------------------------------------------------------------------------
# Phase model tests (Step 906)
# ---------------------------------------------------------------------------


class TestPhaseModel:

    def test_phases_defined(self):
        assert "init" in DO_PHASES
        assert "stop" in DO_PHASES
        assert "approval_required" in DO_PHASES

    def test_phase_dataclass(self):
        p = DoRunPhase(phase="init", status="completed", safe_summary="ok")
        assert p.phase == "init"
        assert p.status == "completed"

    def test_stop_reason(self):
        sr = DoRunStopReason(reason="approval_required", detail="needs approval")
        assert sr.reason == "approval_required"

    def test_next_action(self):
        na = DoRunNextAction(label="Approve", command="remedy patch approve x y", reason="needed")
        assert "remedy" in na.command

    def test_contract_defaults(self):
        from packages.orchestration.run_contract import build_default_run_contract
        job = Job(name="test")
        c = build_default_run_contract(job)
        assert c.stop_before_apply is True
        assert c.max_loops == 10
        assert c.autonomy_level == 1
        assert c.source == "default_v1"
        assert "plan" in c.allowed_actions
        assert "apply" in c.denied_actions


# ---------------------------------------------------------------------------
# Full flow tests (Steps 909-915)
# ---------------------------------------------------------------------------


class TestDoRunFlow:

    def test_full_flow_autonomy_3(self, tmp_path):
        result = _run_with_tmp(tmp_path, autonomy=3)
        assert result.job_id
        assert result.task_id
        assert result.autonomy_level == 3
        phase_names = [p.phase for p in result.phases]
        assert "init" in phase_names
        assert "plan" in phase_names
        assert "context" in phase_names
        assert "build" in phase_names
        assert "stop" in phase_names

    def test_stop_reason_approval_required(self, tmp_path):
        result = _run_with_tmp(tmp_path, autonomy=3)
        assert result.stop_reason.reason == "approval_required"

    def test_next_safe_action_exists(self, tmp_path):
        result = _run_with_tmp(tmp_path, autonomy=3)
        assert result.next_safe_action is not None
        assert "remedy" in result.next_safe_action.command

    def test_patch_intent_created(self, tmp_path):
        result = _run_with_tmp(tmp_path, autonomy=3)
        assert result.patch_intent_id

    def test_patch_intent_created_has_created_at(self, tmp_path):
        from uuid import UUID

        from packages.orchestration.approval_queue import list_patch_intents
        from packages.orchestration.storage import load_job

        result = _run_with_tmp(tmp_path, autonomy=3)
        job = load_job(UUID(result.job_id), root=tmp_path / "data")
        intents = list_patch_intents(job)
        assert intents[0]["created_at"]

    def test_artifact_created(self, tmp_path):
        result = _run_with_tmp(tmp_path, autonomy=3)
        assert len(result.artifact_ids) >= 1

    def test_context_summary_present(self, tmp_path):
        result = _run_with_tmp(tmp_path, autonomy=3)
        assert result.context_summary
        assert "files" in result.context_summary or "tokens" in result.context_summary

    def test_proof_status_present(self, tmp_path):
        result = _run_with_tmp(tmp_path, autonomy=3)
        assert result.proof_status in ("incomplete", "unavailable", "no_changes", "verified", "unverified")

    def test_low_autonomy_skips_build(self, tmp_path):
        result = _run_with_tmp(tmp_path, autonomy=1)
        phase_names = [p.phase for p in result.phases]
        assert "build" in phase_names
        build_phase = [p for p in result.phases if p.phase == "build"][0]
        assert build_phase.status == "skipped"

    def test_generated_at(self, tmp_path):
        result = _run_with_tmp(tmp_path)
        assert result.generated_at

    def test_repo_path_safe_is_basename(self, tmp_path):
        result = _run_with_tmp(tmp_path)
        assert result.repo_path_safe == "repo"
        assert "/" not in result.repo_path_safe


# ---------------------------------------------------------------------------
# Result contract / JSON export (Step 907)
# ---------------------------------------------------------------------------


class TestDoRunExport:

    def test_json_top_level_keys(self, tmp_path):
        result = _run_with_tmp(tmp_path)
        data = export_do_run_json(result)
        expected = {
            "version", "job_id", "task_id", "artifact_ids",
            "patch_intent_id", "proof_status", "phases",
            "stop_reason", "next_safe_action", "autonomy_level",
            "requested_autonomy_level", "autonomy_capped", "cap_reason",
            "repo_path_safe", "context_summary", "generated_at",
        }
        assert expected.issubset(set(data.keys()))

    def test_json_phases_structure(self, tmp_path):
        result = _run_with_tmp(tmp_path)
        data = export_do_run_json(result)
        for p in data["phases"]:
            assert "phase" in p
            assert "status" in p
            assert "safe_summary" in p

    def test_json_stop_reason_structure(self, tmp_path):
        result = _run_with_tmp(tmp_path)
        data = export_do_run_json(result)
        assert "reason" in data["stop_reason"]
        assert "detail" in data["stop_reason"]

    def test_json_next_safe_action_structure(self, tmp_path):
        result = _run_with_tmp(tmp_path, autonomy=3)
        data = export_do_run_json(result)
        nsa = data["next_safe_action"]
        assert nsa is not None
        assert "label" in nsa
        assert "command" in nsa
        assert "reason" in nsa

    def test_json_roundtrip(self, tmp_path):
        result = _run_with_tmp(tmp_path)
        data = export_do_run_json(result)
        text = json.dumps(data, sort_keys=True)
        data2 = json.loads(text)
        assert data2["version"] == 1
        assert data2["job_id"] == result.job_id

    def test_json_has_run_contract(self, tmp_path):
        """Step 930: JSON export includes run_contract section."""
        result = _run_with_tmp(tmp_path)
        data = export_do_run_json(result, contract=result._contract)
        assert "run_contract" in data
        rc = data["run_contract"]
        assert rc["stop_before_apply"] is True
        assert rc["max_loops"] == 1
        assert "allowed_actions" in rc
        assert "denied_actions" in rc
        assert rc["source"] in ("default_v1", "do_v1_caller_override")

    def test_json_autonomy_truth_fields(self, tmp_path):
        """Step 932: JSON has requested vs effective autonomy."""
        result = _run_with_tmp(tmp_path, autonomy=7)
        data = export_do_run_json(result)
        assert data["autonomy_level"] == 3
        assert data["requested_autonomy_level"] == 7
        assert data["autonomy_capped"] is True
        assert "cap" in data["cap_reason"].lower() or "v1" in data["cap_reason"].lower()


# ---------------------------------------------------------------------------
# Safety / redaction tests (Step 920)
# ---------------------------------------------------------------------------


class TestDoRunSafety:

    def test_no_raw_file_content(self, tmp_path):
        result = _run_with_tmp(tmp_path)
        data = export_do_run_json(result)
        text = json.dumps(data)
        assert "def hello" not in text
        assert "secret123" not in text
        assert "API_KEY" not in text

    def test_no_absolute_paths(self, tmp_path):
        result = _run_with_tmp(tmp_path)
        data = export_do_run_json(result)
        assert not data["repo_path_safe"].startswith("/")

    def test_no_traceback_in_output(self, tmp_path):
        result = _run_with_tmp(tmp_path)
        text = summarize_do_run(result)
        assert "Traceback" not in text

    def test_output_bounded(self, tmp_path):
        result = _run_with_tmp(tmp_path)
        text = summarize_do_run(result)
        assert len(text) < 5000

    def test_env_not_in_context(self, tmp_path):
        result = _run_with_tmp(tmp_path)
        data = export_do_run_json(result)
        # .env.secret may appear in run_contract.denied_paths (policy, not leaked content)
        # Check it doesn't appear in phases or context_summary
        for phase in data["phases"]:
            assert ".env.secret" not in phase["safe_summary"]
        assert ".env.secret" not in (data.get("context_summary") or "")

    def test_invalid_repo_safe(self, tmp_path):
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        old = os.environ.get("REMEDY_DATA_DIR")
        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            result = run_do("test", "/nonexistent/path", autonomy_level=3)
        finally:
            if old:
                os.environ["REMEDY_DATA_DIR"] = old
            else:
                os.environ.pop("REMEDY_DATA_DIR", None)
        assert result.repo_path_safe == ""
        assert result.job_id


# ---------------------------------------------------------------------------
# Approval gate enforcement (Step 914 + Step 933 regression)
# ---------------------------------------------------------------------------


class TestApprovalGate:

    def test_stop_before_apply_default(self, tmp_path):
        result = _run_with_tmp(tmp_path, autonomy=3)
        phase_names = [p.phase for p in result.phases]
        assert "apply" not in phase_names
        assert "approval_required" in phase_names

    def test_no_source_apply_without_approval(self, tmp_path):
        result = _run_with_tmp(tmp_path, autonomy=3)
        phase_statuses = {p.phase: p.status for p in result.phases}
        assert phase_statuses.get("approval_required") == "stopped"

    def test_no_apply_import_in_do_run(self):
        """Step 933: source_apply not imported in do_run."""
        import inspect

        from packages.orchestration import do_run
        src = inspect.getsource(do_run)
        assert "from packages.orchestration.source_apply import" not in src
        assert "source_apply(" not in src

    def test_no_apply_phase_before_approval(self, tmp_path):
        """Step 933: apply never appears before approval_required."""
        result = _run_with_tmp(tmp_path, autonomy=3)
        phase_names = [p.phase for p in result.phases]
        assert "apply" not in phase_names

    def test_patch_intent_not_approved(self, tmp_path):
        """Step 933: patch_intent_approvals is empty (not pre-approved)."""
        from packages.orchestration.storage import load_job
        repo = _make_repo(tmp_path)
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        old = os.environ.get("REMEDY_DATA_DIR")
        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            result = run_do("test", str(repo), autonomy_level=3)
            job = load_job(result.job_id)
        finally:
            if old:
                os.environ["REMEDY_DATA_DIR"] = old
            else:
                os.environ.pop("REMEDY_DATA_DIR", None)
        for art in job.artifacts:
            approvals = art.metadata.get("patch_intent_approvals", {})
            assert not approvals, "Patch intent should not be pre-approved"

    def test_proof_not_verified_before_apply(self, tmp_path):
        """Step 933: proof_status is not 'verified' before apply."""
        result = _run_with_tmp(tmp_path, autonomy=3)
        assert result.proof_status != "verified"

    def test_next_action_is_approval(self, tmp_path):
        """Step 933: next_safe_action points to approval."""
        result = _run_with_tmp(tmp_path, autonomy=3)
        assert result.next_safe_action is not None
        assert "approve" in result.next_safe_action.command


# ---------------------------------------------------------------------------
# Context/proof alignment (Step 921)
# ---------------------------------------------------------------------------


class TestContextProofAlignment:

    def test_context_summary_in_result(self, tmp_path):
        result = _run_with_tmp(tmp_path)
        assert result.context_summary
        assert "file" in result.context_summary.lower() or "token" in result.context_summary.lower()

    def test_proof_incomplete_before_apply(self, tmp_path):
        result = _run_with_tmp(tmp_path)
        assert result.proof_status in ("incomplete", "no_changes", "unavailable")


# ---------------------------------------------------------------------------
# Summary text (Step 920)
# ---------------------------------------------------------------------------


class TestDoRunSummary:

    def test_summary_has_phases(self, tmp_path):
        result = _run_with_tmp(tmp_path)
        text = summarize_do_run(result)
        assert "Phases:" in text
        assert "init" in text

    def test_summary_has_stop_reason(self, tmp_path):
        result = _run_with_tmp(tmp_path)
        text = summarize_do_run(result)
        assert "Stop:" in text

    def test_summary_has_next_action(self, tmp_path):
        result = _run_with_tmp(tmp_path, autonomy=3)
        text = summarize_do_run(result)
        assert "Next:" in text
        assert "remedy" in text


# ---------------------------------------------------------------------------
# Step 926-927: Full next_safe_action catalog validation
# ---------------------------------------------------------------------------


class TestNextSafeActionValidation:

    def test_validate_real_command(self):
        """remedy patch approve -> patch.approve exists."""
        assert validate_next_safe_action_command("remedy patch approve job123 intent456") is True

    def test_validate_context_inspect(self):
        """remedy context inspect -> context.inspect exists."""
        assert validate_next_safe_action_command("remedy context inspect job123 --json") is True

    def test_validate_job_show(self):
        """remedy job show -> job.show exists."""
        assert validate_next_safe_action_command("remedy job show job123 --json") is True

    def test_validate_do_run(self):
        """remedy do run -> do.run exists."""
        assert validate_next_safe_action_command('remedy do run "goal" --json') is True

    def test_reject_fake_subcommand(self):
        """remedy patch does-not-exist -> fails."""
        assert validate_next_safe_action_command("remedy patch does-not-exist job123") is False

    def test_reject_group_only(self):
        """remedy patch -> fails (no subcommand)."""
        assert validate_next_safe_action_command("remedy patch") is False

    def test_reject_empty(self):
        assert validate_next_safe_action_command("") is False

    def test_reject_non_remedy(self):
        assert validate_next_safe_action_command("curl http://example.com") is False

    def test_all_emitted_actions_valid(self, tmp_path):
        """Every next_safe_action emitted by run_do validates against catalog."""
        # Normal flow
        result = _run_with_tmp(tmp_path, autonomy=3)
        assert result.next_safe_action is not None
        assert validate_next_safe_action_command(result.next_safe_action.command), \
            f"Invalid command: {result.next_safe_action.command}"

    def test_low_autonomy_action_valid(self, tmp_path):
        """Low autonomy next_safe_action also validates."""
        result = _run_with_tmp(tmp_path, autonomy=1)
        assert result.next_safe_action is not None
        assert validate_next_safe_action_command(result.next_safe_action.command), \
            f"Invalid command: {result.next_safe_action.command}"


# ---------------------------------------------------------------------------
# Step 928: Context failure stops run
# ---------------------------------------------------------------------------


class TestContextFailureStops:

    def test_context_error_stops_run(self, tmp_path):
        """Monkeypatched context inspector raises -> no build, no patch intent."""
        repo = _make_repo(tmp_path)
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        old = os.environ.get("REMEDY_DATA_DIR")
        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            with patch(
                "packages.orchestration.do_run._run_context_phase"
            ) as mock_ctx:
                mock_ctx.return_value = DoRunPhase(
                    phase="context", status="failed",
                    safe_summary="Context inspection failed: RuntimeError",
                )
                result = run_do("test goal", str(repo), autonomy_level=3)
        finally:
            if old:
                os.environ["REMEDY_DATA_DIR"] = old
            else:
                os.environ.pop("REMEDY_DATA_DIR", None)

        assert result.stop_reason.reason == "context_error"
        assert not result.artifact_ids
        assert not result.patch_intent_id
        phase_names = [p.phase for p in result.phases]
        assert "build" not in phase_names
        assert "patch_intent" not in phase_names

    def test_context_error_no_traceback(self, tmp_path):
        """Context failure does not expose traceback."""
        repo = _make_repo(tmp_path)
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        old = os.environ.get("REMEDY_DATA_DIR")
        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            with patch(
                "packages.orchestration.do_run._run_context_phase"
            ) as mock_ctx:
                mock_ctx.return_value = DoRunPhase(
                    phase="context", status="failed",
                    safe_summary="Context inspection failed: ValueError",
                )
                result = run_do("test goal", str(repo), autonomy_level=3)
        finally:
            if old:
                os.environ["REMEDY_DATA_DIR"] = old
            else:
                os.environ.pop("REMEDY_DATA_DIR", None)

        text = summarize_do_run(result)
        assert "Traceback" not in text

    def test_context_error_next_action_valid(self, tmp_path):
        """Context failure next_safe_action points to context inspect."""
        repo = _make_repo(tmp_path)
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        old = os.environ.get("REMEDY_DATA_DIR")
        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            with patch(
                "packages.orchestration.do_run._run_context_phase"
            ) as mock_ctx:
                mock_ctx.return_value = DoRunPhase(
                    phase="context", status="failed",
                    safe_summary="Context inspection failed: RuntimeError",
                )
                result = run_do("test goal", str(repo), autonomy_level=3)
        finally:
            if old:
                os.environ["REMEDY_DATA_DIR"] = old
            else:
                os.environ.pop("REMEDY_DATA_DIR", None)

        assert result.next_safe_action is not None
        assert "context inspect" in result.next_safe_action.command
        assert validate_next_safe_action_command(result.next_safe_action.command)


# ---------------------------------------------------------------------------
# Step 929: Command catalog metadata truth
# ---------------------------------------------------------------------------


class TestCatalogMetadataTruth:

    def test_do_run_no_repo_mutation(self):
        """do.run should not claim may_mutate_repo in v1."""
        from apps.cli.command_catalog import CATALOG
        entry = next(e for e in CATALOG if e.command_id == "do.run")
        assert entry.may_mutate_repo is False, \
            "v1 never mutates repo — fixture only, stops before apply"

    def test_do_run_no_command_execution(self):
        """do.run should not claim may_execute_commands in v1."""
        from apps.cli.command_catalog import CATALOG
        entry = next(e for e in CATALOG if e.command_id == "do.run")
        assert entry.may_execute_commands is False, \
            "v1 runs no external commands"

    def test_do_run_action_class_not_apply_write(self):
        """do.run action_class should reflect data-only writes."""
        from apps.cli.command_catalog import CATALOG
        entry = next(e for e in CATALOG if e.command_id == "do.run")
        assert entry.action_class != "apply_write", \
            "v1 writes metadata only, not repo files"


# ---------------------------------------------------------------------------
# Step 930: Contract consolidation
# ---------------------------------------------------------------------------


class TestContractConsolidation:

    def test_contract_has_source(self):
        from packages.orchestration.run_contract import build_default_run_contract
        c = build_default_run_contract(Job(name="test"))
        assert c.source == "default_v1"

    def test_contract_has_allowed_actions(self):
        from packages.orchestration.run_contract import build_default_run_contract
        c = build_default_run_contract(Job(name="test"))
        assert len(c.allowed_actions) > 0
        assert "plan" in c.allowed_actions

    def test_contract_has_denied_actions(self):
        from packages.orchestration.run_contract import build_default_run_contract
        c = build_default_run_contract(Job(name="test"))
        assert len(c.denied_actions) > 0
        assert "apply" in c.denied_actions

    def test_contract_in_result(self, tmp_path):
        result = _run_with_tmp(tmp_path)
        assert result._contract is not None
        assert result._contract.source in ("default_v1", "do_v1_caller_override")


# ---------------------------------------------------------------------------
# Step 931: max_loops enforcement
# ---------------------------------------------------------------------------


class TestMaxLoopsEnforcement:

    def test_max_loops_zero_stops(self, tmp_path):
        """max_loops=0 -> invalid_input, safe stop."""
        result = _run_with_tmp(tmp_path, max_loops=0)
        assert result.stop_reason.reason == "invalid_input"
        assert "max_loops" in result.stop_reason.detail
        assert not result.job_id  # never created a job

    def test_max_loops_negative_stops(self, tmp_path):
        """max_loops=-1 -> invalid_input."""
        result = _run_with_tmp(tmp_path, max_loops=-1)
        assert result.stop_reason.reason == "invalid_input"

    def test_max_loops_one_works(self, tmp_path):
        """max_loops=1 -> normal flow."""
        result = _run_with_tmp(tmp_path, max_loops=1)
        assert result.job_id
        assert result.stop_reason.reason != "invalid_input"

    def test_max_loops_three_single_pass(self, tmp_path):
        """max_loops=3 -> still single pass in v1, contract shows 1."""
        result = _run_with_tmp(tmp_path, max_loops=3)
        assert result.job_id
        assert result._contract is not None
        assert result._contract.max_loops == 1  # v1 caps to 1


# ---------------------------------------------------------------------------
# Step 932: Autonomy level truth
# ---------------------------------------------------------------------------


class TestAutonomyTruth:

    def test_autonomy_7_capped_to_3(self, tmp_path):
        result = _run_with_tmp(tmp_path, autonomy=7)
        assert result.autonomy_level == 3
        assert result.requested_autonomy_level == 7
        assert result.autonomy_capped is True
        assert result.cap_reason

    def test_autonomy_3_not_capped(self, tmp_path):
        result = _run_with_tmp(tmp_path, autonomy=3)
        assert result.autonomy_level == 3
        assert result.requested_autonomy_level == 3
        assert result.autonomy_capped is False
        assert result.cap_reason == ""

    def test_autonomy_1_not_capped(self, tmp_path):
        result = _run_with_tmp(tmp_path, autonomy=1)
        assert result.autonomy_level == 1
        assert result.autonomy_capped is False
