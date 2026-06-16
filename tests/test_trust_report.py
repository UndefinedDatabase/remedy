"""
Tests for packages/orchestration/trust_report.py and the `remedy brain trust` CLI command.

Coverage:
  - no run logs: renders gracefully with "No run logs available"
  - planned but not run: shows tasks in plan section
  - successful task: shows completed in execution summary
  - permission denied event: shows blocked event in permissions section
  - verification failed event: shows failed checks in verification section
  - patch intent pending medium risk: shows in patch intents section
  - approved intent: shows approved state
  - rejected intent: shows rejected state
  - reserved permissions shown with note
  - no raw exception message rendered
  - no raw artifact content rendered
  - "apply not implemented" shown when intents are approved
  - report includes redaction / trust boundary section
  - report includes all 9 numbered sections
  - CLI command prints report
  - CLI invalid job ID exits 1
  - CLI unknown job ID exits 1
"""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import pytest

from packages.core.models import Artifact, ArtifactKind, Job, RunState, Task
from packages.orchestration.approval_queue import (
    APPROVAL_APPROVED,
    APPROVAL_REJECTED,
    make_intent_id,
    set_approval_state,
)
from packages.orchestration.patch_intent import RISK_HIGH, RISK_LOW, RISK_MEDIUM, RISK_UNKNOWN
from packages.orchestration.permissions import Capability, set_permission
from packages.orchestration.storage import save_job
from packages.orchestration.trust_report import summarize_trust_report

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _ts(offset: int = 0) -> str:
    return f"2026-05-04T10:{offset:02d}:00+00:00"


def _make_job(**kwargs) -> Job:
    defaults: dict = {"name": "Test trust job", "state": RunState.PENDING}
    defaults.update(kwargs)
    return Job(**defaults)


def _make_pending_task(**kwargs) -> Task:
    return Task(description="write the readme", inputs={"task_type": "write_readme"}, **kwargs)


def _completed_task(**kwargs) -> Task:
    t = Task(description="done writing readme", inputs={"task_type": "write_readme"}, **kwargs)
    t.status = RunState.COMPLETED
    return t


def _add_patch_artifact(
    job: Job, *, risk: str = RISK_MEDIUM, intent_count: int = 1
) -> str:
    """Add a fake patch-intent artifact to the job. Returns the first intent_id."""
    explanations = [
        {
            "file": f"docs/file_{i}.md",
            "action": "modify",
            "risk": risk,
            "reason": "task type 'write_readme'",
            "summary": f"Proposed change {i}",
        }
        for i in range(intent_count)
    ]
    artifact = Artifact(
        name="builder_proposal",
        content="",
        kind=ArtifactKind.BUILDER_PROPOSAL,
        task_id=uuid4(),
        metadata={
            "patch_intent_explanations": explanations,
            "patch_intent_risks": [risk] * intent_count,
        },
    )
    job.artifacts.append(artifact)
    return make_intent_id(artifact.id, 0)


def _task_run_succeeded(job_id: str, task_id: str) -> list[dict]:
    return [
        {"event": "task_run_started", "job_id": job_id, "run_id": "r",
         "timestamp": _ts(0), "task_id": task_id,
         "metadata": {"task_type": "write_readme"}},
        {"event": "workspace_materialized", "job_id": job_id, "run_id": "r",
         "timestamp": _ts(1), "task_id": task_id,
         "metadata": {"workspace_file": "/ws/readme.md"}},
        {"event": "verification_passed", "job_id": job_id, "run_id": "r",
         "timestamp": _ts(2), "task_id": task_id, "outcome": "pass",
         "metadata": {"verifier_profile": "markdown_doc"}},
        {"event": "task_run_completed", "job_id": job_id, "run_id": "r",
         "timestamp": _ts(3), "task_id": task_id, "outcome": "pass", "metadata": {}},
    ]


# ---------------------------------------------------------------------------
# Header and structure
# ---------------------------------------------------------------------------


class TestTrustReportHeader:
    def test_header_present(self):
        job = _make_job()
        out = summarize_trust_report(job, [])
        assert "Remedy Trust Report" in out

    def test_short_job_id_shown(self):
        job = _make_job()
        out = summarize_trust_report(job, [])
        assert str(job.id)[:8] in out

    def test_job_name_shown(self):
        job = _make_job(name="My special job")
        out = summarize_trust_report(job, [])
        assert "My special job" in out

    def test_job_state_shown(self):
        job = _make_job(state=RunState.COMPLETED)
        out = summarize_trust_report(job, [])
        assert "completed" in out

    def test_all_nine_sections_present(self):
        job = _make_job()
        out = summarize_trust_report(job, [])
        for n in range(1, 10):
            assert f"{n}." in out, f"Section {n} not found in output"

    def test_redaction_section_present(self):
        job = _make_job()
        out = summarize_trust_report(job, [])
        assert "Redaction" in out or "trust boundary" in out


# ---------------------------------------------------------------------------
# Section 1: User request
# ---------------------------------------------------------------------------


class TestUserRequestSection:
    def test_user_prompt_shown_when_set(self):
        job = _make_job()
        job.user_prompt = "Write a comprehensive README for this project"
        out = summarize_trust_report(job, [])
        assert "Write a comprehensive README" in out

    def test_no_prompt_shows_fallback(self):
        job = _make_job(name="Unnamed job")
        out = summarize_trust_report(job, [])
        assert "no prompt" in out.lower() or "Unnamed job" in out

    def test_long_prompt_truncated(self):
        job = _make_job()
        job.user_prompt = "x" * 600
        out = summarize_trust_report(job, [])
        # Truncated — should not exceed 410 chars of the prompt in output
        assert "x" * 401 not in out


# ---------------------------------------------------------------------------
# Section 2: Plan
# ---------------------------------------------------------------------------


class TestPlanSection:
    def test_no_tasks_says_unplanned(self):
        job = _make_job()
        out = summarize_trust_report(job, [])
        assert "No tasks" in out or "unplanned" in out.lower()

    def test_task_count_shown(self):
        job = _make_job()
        job.tasks.append(_make_pending_task())
        job.tasks.append(_completed_task())
        out = summarize_trust_report(job, [])
        assert "2 total" in out

    def test_task_type_shown(self):
        job = _make_job()
        job.tasks.append(_make_pending_task())
        out = summarize_trust_report(job, [])
        assert "write_readme" in out

    def test_task_statuses_shown(self):
        job = _make_job()
        job.tasks.append(_make_pending_task())
        job.tasks.append(_completed_task())
        out = summarize_trust_report(job, [])
        assert "pending" in out
        assert "completed" in out


# ---------------------------------------------------------------------------
# Section 3: Execution summary
# ---------------------------------------------------------------------------


class TestExecutionSummarySection:
    def test_no_logs_says_unavailable(self):
        job = _make_job()
        out = summarize_trust_report(job, [])
        assert "No run logs" in out or "no task_run_started" in out.lower()

    def test_run_invocations_counted(self):
        job = _make_job()
        task_id = str(uuid4())
        events = _task_run_succeeded(str(job.id), task_id)
        out = summarize_trust_report(job, events)
        assert "Run invocations" in out
        assert "1" in out

    def test_completed_count_shown(self):
        job = _make_job()
        task_id = str(uuid4())
        events = _task_run_succeeded(str(job.id), task_id)
        out = summarize_trust_report(job, events)
        assert "Completed" in out

    def test_failed_count_shown_when_present(self):
        job = _make_job()
        task_id = str(uuid4())
        events = [
            {"event": "task_run_started", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "task_id": task_id, "metadata": {"task_type": "write_readme"}},
            {"event": "task_run_failed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(1), "task_id": task_id, "outcome": "builder_error", "metadata": {}},
        ]
        out = summarize_trust_report(job, events)
        assert "Failed" in out or "failed" in out

    def test_noop_count_shown_when_present(self):
        job = _make_job()
        events = [
            {"event": "task_run_noop", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "outcome": "no_pending_tasks", "metadata": {}},
        ]
        out = summarize_trust_report(job, events)
        assert "No-op" in out or "noop" in out.lower()

    def test_interrupted_flagged(self):
        job = _make_job()
        task_id = str(uuid4())
        events = [
            {"event": "task_run_started", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "task_id": task_id, "metadata": {"task_type": "write_readme"}},
            # No terminal event → interrupted
        ]
        out = summarize_trust_report(job, events)
        assert "Interrupted" in out or "interrupted" in out

    def test_planning_failed_with_error_category_shown(self):
        """planning_failed event with error_category → safe category label shown."""
        job = _make_job()
        events = [
            {"event": "planning_failed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "outcome": "error",
             "message": "SECRET_EXCEPTION_TEXT",
             "metadata": {"error_category": "RuntimeError"}},
        ]
        out = summarize_trust_report(job, events)
        assert "Planning failed" in out
        assert "RuntimeError" in out

    def test_planning_failed_raw_message_never_rendered(self):
        """planning_failed event without error_category → 'unknown error', message suppressed."""
        job = _make_job()
        events = [
            {"event": "planning_failed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "outcome": "error",
             "message": "SECRET_MUST_NOT_APPEAR connection refused password=abc",
             "metadata": {}},
        ]
        out = summarize_trust_report(job, events)
        assert "Planning failed" in out
        assert "unknown error" in out
        assert "SECRET_MUST_NOT_APPEAR" not in out
        assert "connection refused" not in out

    def test_planning_failed_no_longer_shows_vague_no_started_message(self):
        """planning_failed-only run log should not fall through to the vague fallback."""
        job = _make_job()
        events = [
            {"event": "planning_failed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "outcome": "error",
             "message": "irrelevant",
             "metadata": {"error_category": "ImportError"}},
        ]
        out = summarize_trust_report(job, events)
        assert "no task_run_started" not in out.lower()
        assert "Planning failed" in out


# ---------------------------------------------------------------------------
# Section 4: Artifacts
# ---------------------------------------------------------------------------


class TestArtifactsSection:
    def test_no_artifacts_says_so(self):
        job = _make_job()
        out = summarize_trust_report(job, [])
        assert "No artifacts" in out

    def test_planning_artifact_shown(self):
        job = _make_job()
        a = Artifact(name="planning_output", content="tasks...", kind=ArtifactKind.PLANNING)
        job.artifacts.append(a)
        out = summarize_trust_report(job, [])
        assert "planning" in out.lower()
        assert "planning_output" in out

    def test_builder_proposal_artifact_shown(self):
        job = _make_job()
        a = Artifact(name="my_proposal", content="stuff", kind=ArtifactKind.BUILDER_PROPOSAL)
        job.artifacts.append(a)
        out = summarize_trust_report(job, [])
        assert "builder_proposal" in out or "builder proposal" in out

    def test_raw_artifact_content_not_shown(self):
        job = _make_job()
        a = Artifact(
            name="proposal",
            content="SECRET_CONTENT_MUST_NOT_APPEAR",
            kind=ArtifactKind.BUILDER_PROPOSAL,
        )
        job.artifacts.append(a)
        out = summarize_trust_report(job, [])
        assert "SECRET_CONTENT_MUST_NOT_APPEAR" not in out


# ---------------------------------------------------------------------------
# Section 5: Verification
# ---------------------------------------------------------------------------


class TestVerificationSection:
    def test_no_verification_events_says_so(self):
        job = _make_job()
        out = summarize_trust_report(job, [])
        assert "No verification" in out

    def test_verification_passed_shown(self):
        job = _make_job()
        task_id = str(uuid4())
        events = _task_run_succeeded(str(job.id), task_id)
        out = summarize_trust_report(job, events)
        assert "passed" in out
        assert task_id[:8] in out

    def test_verifier_profile_shown(self):
        job = _make_job()
        task_id = str(uuid4())
        events = _task_run_succeeded(str(job.id), task_id)
        out = summarize_trust_report(job, events)
        assert "markdown_doc" in out

    def test_verification_failed_shown_with_checks(self):
        job = _make_job()
        task_id = str(uuid4())
        events = [
            {"event": "task_run_started", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "task_id": task_id, "metadata": {"task_type": "write_readme"}},
            {"event": "verification_failed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(1), "task_id": task_id, "outcome": "fail",
             "metadata": {"failure_count": 2, "failed_checks": ["check_a", "check_b"]}},
            {"event": "task_run_failed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(2), "task_id": task_id, "outcome": "fail", "metadata": {}},
        ]
        out = summarize_trust_report(job, events)
        assert "failed" in out
        assert "check_a" in out
        assert "check_b" in out
        assert "2" in out


# ---------------------------------------------------------------------------
# Section 6: Permissions and safety
# ---------------------------------------------------------------------------


class TestPermissionsSafetySection:
    def test_all_capabilities_shown(self):
        job = _make_job()
        out = summarize_trust_report(job, [])
        assert "workspace_write" in out
        assert "repo_generated_write" in out
        assert "repo_overwrite" in out
        assert "shell_exec" in out

    def test_reserved_capabilities_noted(self):
        job = _make_job()
        out = summarize_trust_report(job, [])
        assert "reserved" in out

    def test_workspace_write_allow_by_default(self):
        job = _make_job()
        out = summarize_trust_report(job, [])
        # workspace_write defaults to allow
        section = out.split("6. Permissions")[1].split("7.")[0]
        assert "workspace_write" in section
        assert "allow" in section

    def test_workspace_write_denied_shown(self):
        job = _make_job()
        set_permission(job, Capability.workspace_write, allow=False)
        out = summarize_trust_report(job, [])
        section = out.split("6. Permissions")[1].split("7.")[0]
        assert "workspace_write" in section
        assert "deny" in section

    def test_permission_denied_run_event_shown(self):
        job = _make_job()
        task_id = str(uuid4())
        events = [
            {"event": "task_run_started", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "task_id": task_id, "metadata": {"task_type": "write_readme"}},
            {"event": "task_run_failed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(1), "task_id": task_id,
             "outcome": "permission_denied",
             "metadata": {"capability": "workspace_write"}},
        ]
        out = summarize_trust_report(job, events)
        assert "permission_denied" in out
        assert "workspace_write" in out

    def test_no_blocked_events_section_when_clean(self):
        job = _make_job()
        task_id = str(uuid4())
        events = _task_run_succeeded(str(job.id), task_id)
        out = summarize_trust_report(job, events)
        assert "Blocked run events" not in out


# ---------------------------------------------------------------------------
# Section 7: Patch intents and decisions
# ---------------------------------------------------------------------------


class TestPatchIntentsSection:
    def test_no_intents_says_so(self):
        job = _make_job()
        out = summarize_trust_report(job, [])
        assert "No patch intents" in out

    def test_pending_intent_shown(self):
        job = _make_job()
        intent_id = _add_patch_artifact(job, risk=RISK_MEDIUM)
        out = summarize_trust_report(job, [])
        assert intent_id in out
        assert "pending" in out
        assert "medium" in out

    def test_approved_intent_shown(self):
        job = _make_job()
        intent_id = _add_patch_artifact(job, risk=RISK_LOW)
        set_approval_state(job, intent_id, APPROVAL_APPROVED)
        out = summarize_trust_report(job, [])
        assert "approved" in out

    def test_rejected_intent_shown(self):
        job = _make_job()
        intent_id = _add_patch_artifact(job, risk=RISK_MEDIUM)
        set_approval_state(job, intent_id, APPROVAL_REJECTED)
        out = summarize_trust_report(job, [])
        assert "rejected" in out

    def test_apply_command_shown_when_approved_and_no_pending(self):
        job = _make_job(state=RunState.COMPLETED)
        intent_id = _add_patch_artifact(job, risk=RISK_LOW)
        set_approval_state(job, intent_id, APPROVAL_APPROVED)
        out = summarize_trust_report(job, [])
        assert "patch apply" in out or "approved" in out

    def test_approve_command_shown_when_pending(self):
        """Pending intents show approval instructions."""
        job = _make_job()
        _add_patch_artifact(job, risk=RISK_MEDIUM)
        out = summarize_trust_report(job, [])
        assert "patch approve" in out or "approved" in out or "pending" in out

    def test_target_path_shown(self):
        job = _make_job()
        _add_patch_artifact(job, risk=RISK_MEDIUM)
        out = summarize_trust_report(job, [])
        assert "docs/file_0.md" in out

    def test_unknown_risk_shown_as_unknown(self):
        job = _make_job()
        _add_patch_artifact(job, risk=RISK_UNKNOWN)
        out = summarize_trust_report(job, [])
        assert "unknown" in out

    def test_intent_counts_summary(self):
        job = _make_job()
        intent_id0 = _add_patch_artifact(job, risk=RISK_LOW, intent_count=1)
        intent_id1 = _add_patch_artifact(job, risk=RISK_MEDIUM, intent_count=1)
        set_approval_state(job, intent_id0, APPROVAL_APPROVED)
        out = summarize_trust_report(job, [])
        assert "1 pending" in out
        assert "1 approved" in out

    def test_approval_reason_never_rendered(self):
        """Free-text approval reason is stored in metadata but must not appear in report."""
        job = _make_job()
        intent_id = _add_patch_artifact(job, risk=RISK_LOW)
        set_approval_state(
            job, intent_id, APPROVAL_APPROVED,
            reason="SECRET_APPROVAL_REASON_DO_NOT_RENDER"
        )
        out = summarize_trust_report(job, [])
        assert "approved" in out          # state still visible
        assert "SECRET_APPROVAL_REASON_DO_NOT_RENDER" not in out


# ---------------------------------------------------------------------------
# Section 9: Redaction / trust boundary
# ---------------------------------------------------------------------------


class TestRedactionSection:
    def test_raw_exception_text_not_shown(self):
        job = _make_job()
        events = [
            {"event": "planning_failed", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "outcome": "error",
             "message": "secret-token MUST_NOT_APPEAR",
             "metadata": {"error_category": "RuntimeError"}},
        ]
        out = summarize_trust_report(job, events)
        assert "MUST_NOT_APPEAR" not in out
        assert "secret-token" not in out

    def test_raw_artifact_content_not_shown(self):
        job = _make_job()
        a = Artifact(
            name="builder_proposal",
            content="PRIVATE_DIFF_CONTENT_MUST_NOT_APPEAR",
            kind=ArtifactKind.BUILDER_PROPOSAL,
        )
        job.artifacts.append(a)
        out = summarize_trust_report(job, [])
        assert "PRIVATE_DIFF_CONTENT_MUST_NOT_APPEAR" not in out

    def test_redaction_statement_present(self):
        job = _make_job()
        out = summarize_trust_report(job, [])
        section = out.split("9. Redaction")[1].split("10.")[0]
        assert "not included" in section or "raw" in section.lower()

    def test_trust_boundary_source_mentioned(self):
        """Report must mention it is generated from Job JSON + run logs."""
        job = _make_job()
        out = summarize_trust_report(job, [])
        section = out.split("9. Redaction")[1].split("10.")[0]
        assert "Job" in section or "run log" in section.lower()

    def test_unknown_events_do_not_crash(self):
        job = _make_job()
        events = [{"event": "totally_unknown_event_zyx", "job_id": str(job.id),
                   "run_id": "r", "timestamp": _ts(0), "metadata": {}}]
        out = summarize_trust_report(job, events)
        assert "Remedy Trust Report" in out


# ---------------------------------------------------------------------------
# Section 10: Next safe action
# ---------------------------------------------------------------------------


class TestNextSafeAction:
    def test_no_tasks_suggests_plan(self):
        """Empty task list → suggest job plan before anything else."""
        job = _make_job()
        out = summarize_trust_report(job, [])
        assert "job plan" in out

    def test_no_tasks_pending_state_suggests_plan(self):
        """Pending state with no tasks → job plan."""
        job = _make_job(state=RunState.PENDING)
        out = summarize_trust_report(job, [])
        assert "job plan" in out

    def test_no_tasks_does_not_say_inspect_generated_files(self):
        """Before planning, 'Inspect generated files' would be misleading."""
        job = _make_job()
        out = summarize_trust_report(job, [])
        section10 = out.split("10. Next safe action")[1]
        assert "Inspect generated files" not in section10

    def test_pending_suggests_run(self):
        job = _make_job()
        job.tasks.append(_make_pending_task())
        out = summarize_trust_report(job, [])
        assert "job run-next" in out

    def test_workspace_denied_suggests_set_permission(self):
        job = _make_job()
        job.tasks.append(_make_pending_task())
        set_permission(job, Capability.workspace_write, allow=False)
        out = summarize_trust_report(job, [])
        assert "job permit" in out

    def test_interrupted_suggests_timeline(self):
        job = _make_job()
        job.tasks.append(_make_pending_task())
        task_id = str(uuid4())
        events = [
            {"event": "task_run_started", "job_id": str(job.id), "run_id": "r",
             "timestamp": _ts(0), "task_id": task_id, "metadata": {"task_type": "write_readme"}},
        ]
        out = summarize_trust_report(job, events)
        assert "timeline" in out

    def test_all_approved_no_pending_mentions_apply_command(self):
        job = _make_job(state=RunState.COMPLETED)
        job.tasks.append(_completed_task())
        intent_id = _add_patch_artifact(job, risk=RISK_LOW)
        set_approval_state(job, intent_id, APPROVAL_APPROVED)
        out = summarize_trust_report(job, [])
        assert "patch apply" in out

    def test_high_risk_pending_suggests_list_patch_intents(self):
        job = _make_job()
        job.tasks.append(_make_pending_task())
        _add_patch_artifact(job, risk=RISK_HIGH)
        out = summarize_trust_report(job, [])
        assert "patch list" in out

    def test_no_pending_no_intents_suggests_inspect_or_create(self):
        job = _make_job(state=RunState.COMPLETED)
        job.tasks.append(_completed_task())
        out = summarize_trust_report(job, [])
        assert "job create" in out or "Inspect" in out


# ---------------------------------------------------------------------------
# data_dir integration
# ---------------------------------------------------------------------------


class TestDataDir:
    def test_run_log_dir_shown_when_data_dir_provided(self):
        job = _make_job()
        out = summarize_trust_report(job, [], data_dir=Path("/tmp/remedy_test"))
        assert "run log" in out.lower() or "runs" in out

    def test_run_log_dir_absent_when_no_data_dir(self):
        job = _make_job()
        out = summarize_trust_report(job, [], data_dir=None)
        assert "run log dir" not in out.lower()


# ---------------------------------------------------------------------------
# CLI integration
# ---------------------------------------------------------------------------


class TestCmdTrustReport:
    def _save(self, tmp_path, monkeypatch, **kwargs) -> Job:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job(**kwargs)
        save_job(job)
        return job

    def test_prints_report_for_valid_job(self, tmp_path, monkeypatch, capsys):
        job = self._save(tmp_path, monkeypatch)

        from apps.cli.commands.brain import _cmd_trust_report

        _cmd_trust_report(str(job.id))
        out = capsys.readouterr().out
        assert "Remedy Trust Report" in out
        assert str(job.id)[:8] in out

    def test_report_includes_permissions(self, tmp_path, monkeypatch, capsys):
        job = self._save(tmp_path, monkeypatch)

        from apps.cli.commands.brain import _cmd_trust_report

        _cmd_trust_report(str(job.id))
        out = capsys.readouterr().out
        assert "workspace_write" in out

    def test_invalid_job_id_exits_1(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))

        from apps.cli.commands.brain import _cmd_trust_report

        with pytest.raises(SystemExit) as exc_info:
            _cmd_trust_report("not-a-uuid")
        assert exc_info.value.code == 1

    def test_unknown_job_id_exits_1(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))

        from apps.cli.commands.brain import _cmd_trust_report

        with pytest.raises(SystemExit) as exc_info:
            _cmd_trust_report(str(uuid4()))
        assert exc_info.value.code == 1

    def test_no_run_logs_exits_0(self, tmp_path, monkeypatch, capsys):
        """trust-report should exit cleanly (0) even when no run logs exist."""
        job = self._save(tmp_path, monkeypatch)

        from apps.cli.commands.brain import _cmd_trust_report

        _cmd_trust_report(str(job.id))  # Must not raise SystemExit
        out = capsys.readouterr().out
        assert "Remedy Trust Report" in out
