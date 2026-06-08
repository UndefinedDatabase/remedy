"""Tests for remedy do v1 phased flow.

Covers:
- Phase model (DoRunPhase, DoRunResult, DoRunContract)
- Init/plan/context/build/intent/approval/proof phases
- Stop reasons and next safe actions
- Export JSON contract
- Safety (no raw content, no secrets, no traceback)
- Approval gate enforcement
- Context/proof alignment
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from packages.core.models import Job, Task
from packages.orchestration.do_run import (
    DO_PHASES,
    DoRunContract,
    DoRunNextAction,
    DoRunPhase,
    DoRunResult,
    DoRunStopReason,
    export_do_run_json,
    run_do,
    summarize_do_run,
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


def _run_with_tmp(tmp_path, goal="safe docs change", autonomy=3):
    repo = _make_repo(tmp_path)
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    old = os.environ.get("REMEDY_DATA_DIR")
    os.environ["REMEDY_DATA_DIR"] = str(data_dir)
    try:
        return run_do(goal, str(repo), autonomy_level=autonomy)
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
        c = DoRunContract()
        assert c.stop_before_apply is True
        assert c.max_loops == 1
        assert c.autonomy_level == 2


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
        text = json.dumps(data)
        assert ".env.secret" not in text or "excluded" in text.lower() or "protected" in text.lower()

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
# Approval gate enforcement (Step 914)
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


# ---------------------------------------------------------------------------
# Context/proof alignment (Step 921)
# ---------------------------------------------------------------------------


class TestContextProofAlignment:

    def test_context_summary_in_result(self, tmp_path):
        result = _run_with_tmp(tmp_path)
        assert result.context_summary
        # Context summary should mention files or tokens
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
# Next safe action catalog validation (Step 920)
# ---------------------------------------------------------------------------


class TestNextSafeActionCatalog:

    def test_next_action_command_is_real(self, tmp_path):
        """next_safe_action command must reference a real catalog command."""
        from apps.cli.command_catalog import CATALOG
        catalog_groups = set()
        for entry in CATALOG:
            parts = entry.command_id.split(".")
            catalog_groups.add(parts[0])

        result = _run_with_tmp(tmp_path, autonomy=3)
        assert result.next_safe_action is not None
        cmd = result.next_safe_action.command
        # Command should start with "remedy <group>"
        parts = cmd.split()
        assert parts[0] == "remedy"
        assert parts[1] in catalog_groups
