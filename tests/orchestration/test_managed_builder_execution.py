"""Tests for Managed Builder Execution v1 (Steps 2026-2075).

Unit tests + architecture guards. No network, no provider, no real subprocess for most tests.
"""

from __future__ import annotations

import json
import os
import re
import textwrap
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from packages.orchestration.managed_builder_execution import (
    SCHEMA_VERSION,
    ApprovalScope,
    CommandTemplate,
    ExecutionApproval,
    ExecutionEvent,
    ExecutionEventKind,
    ManagedExecutionResult,
    ManagedExecutionStatus,
    default_command_templates,
    save_command_template,
    list_command_templates,
    get_command_template,
    approve_managed_execution,
    get_execution_approval,
    list_execution_approvals,
    validate_execution_approval,
    run_managed_builder,
    list_execution_events,
    get_execution_result,
    list_execution_results,
    build_debug_bundle,
    managed_execution_mission_signal,
    audit_template_safety,
    audit_execution_result_safety,
    audit_approval_safety,
    managed_execution_integrity,
    _validate_argv_template,
    _resolve_argv,
    _build_sanitized_env,
    _SHELL_METACHARS,
    _FORBIDDEN_PROGRAMS,
    _ALLOWED_ENV_KEYS,
    _FORBIDDEN_ENV_KEYS,
    _ALLOWED_PLACEHOLDER_KEYS,
    MAX_TIMEOUT_SECONDS,
    MAX_OUTPUT_BYTES,
)


class TestModels(unittest.TestCase):
    """Test model serialization and safety."""

    def test_command_template_roundtrip(self):
        t = CommandTemplate(template_id="test-v0", adapter_kind="generic",
                            argv_template=["echo", "hello"],
                            timeout_seconds=120, enabled=False)
        d = t.to_dict()
        assert d["template_id"] == "test-v0"
        assert d["enabled"] is False
        assert d["timeout_seconds"] == 120
        t2 = CommandTemplate.from_dict(d)
        assert t2.template_id == "test-v0"
        assert t2.enabled is False

    def test_template_clamps_timeout(self):
        t = CommandTemplate(timeout_seconds=9999)
        d = t.to_dict()
        assert d["timeout_seconds"] == MAX_TIMEOUT_SECONDS

    def test_template_clamps_output(self):
        t = CommandTemplate(max_output_bytes=999999)
        d = t.to_dict()
        assert d["max_output_bytes"] == MAX_OUTPUT_BYTES

    def test_result_roundtrip(self):
        r = ManagedExecutionResult(execution_id="exe1", session_id="ses1",
                                    status=ManagedExecutionStatus.COMPLETED,
                                    exit_code=0, duration_ms=123)
        d = r.to_dict()
        assert d["execution_id"] == "exe1"
        assert d["status"] == "completed"
        r2 = ManagedExecutionResult.from_dict(d)
        assert r2.execution_id == "exe1"
        assert r2.exit_code == 0

    def test_result_scrubs_output_ref(self):
        r = ManagedExecutionResult(output_ref="/home/user/secret/path.raw")
        d = r.to_dict()
        assert "/home/" not in d["output_ref"]

    def test_result_scrubs_safe_summary(self):
        r = ManagedExecutionResult(safe_summary="key=sk-ant-secret123456789")
        d = r.to_dict()
        assert "sk-ant-secret" not in d["safe_summary"]

    def test_event_scrubs(self):
        ev = ExecutionEvent(safe_summary="token=sk-abcdefghijklmnop")
        d = ev.to_dict()
        assert "sk-abcdef" not in d["safe_summary"]

    def test_approval_to_dict(self):
        a = ExecutionApproval(approval_id="ap1", session_id="ses1",
                               template_id="tmpl1", operator_id="ops")
        d = a.to_dict()
        assert d["approval_id"] == "ap1"
        assert d["schema_version"] == SCHEMA_VERSION


class TestArgvValidation(unittest.TestCase):
    """Test argv template validation."""

    def test_empty_argv(self):
        ok, reason = _validate_argv_template([])
        assert not ok
        assert "empty" in reason

    def test_shell_metachar(self):
        ok, reason = _validate_argv_template(["echo", "hello; rm -rf /"])
        assert not ok
        assert "metacharacter" in reason

    def test_forbidden_program(self):
        ok, reason = _validate_argv_template(["rm", "-rf", "/"])
        assert not ok
        assert "forbidden" in reason

    def test_valid_argv(self):
        ok, reason = _validate_argv_template(["python", "-c", "print('hello')"])
        assert ok

    def test_pipe_rejected(self):
        ok, reason = _validate_argv_template(["echo", "hello", "|", "cat"])
        assert not ok


class TestArgvResolve(unittest.TestCase):
    """Test placeholder resolution."""

    def test_resolve_simple(self):
        tmpl = {"argv_template": ["echo", "{goal_summary}"],
                "allowed_placeholders": ["goal_summary"]}
        ok, argv, reason = _resolve_argv(tmpl, {"goal_summary": "fix bug"})
        assert ok
        assert argv == ["echo", "fix bug"]

    def test_reject_missing_value(self):
        tmpl = {"argv_template": ["{goal_summary}"],
                "allowed_placeholders": ["goal_summary"]}
        ok, argv, reason = _resolve_argv(tmpl, {})
        assert not ok
        assert "no value" in reason

    def test_reject_metachar_in_value(self):
        tmpl = {"argv_template": ["{goal_summary}"],
                "allowed_placeholders": ["goal_summary"]}
        ok, argv, reason = _resolve_argv(tmpl, {"goal_summary": "hello; rm -rf /"})
        assert not ok
        assert "metacharacter" in reason

    def test_reject_disallowed_placeholder(self):
        tmpl = {"argv_template": ["{goal_summary}"],
                "allowed_placeholders": []}
        ok, argv, reason = _resolve_argv(tmpl, {"goal_summary": "test"})
        assert not ok
        assert "not in allowed" in reason


class TestSanitizedEnv(unittest.TestCase):
    """Test environment sanitization."""

    def test_only_allowed_keys(self):
        tmpl = {"sanitized_env_keys": ["PATH", "HOME"]}
        env = _build_sanitized_env(tmpl)
        for key in env:
            assert key in _ALLOWED_ENV_KEYS

    def test_no_forbidden_keys(self):
        tmpl = {"sanitized_env_keys": ["PATH", "ANTHROPIC_API_KEY"]}
        env = _build_sanitized_env(tmpl)
        assert "ANTHROPIC_API_KEY" not in env

    def test_empty_config(self):
        tmpl = {"sanitized_env_keys": []}
        env = _build_sanitized_env(tmpl)
        assert len(env) == 0


class TestTemplateRegistry(unittest.TestCase):
    """Test template storage and defaults."""

    def test_defaults_all_disabled(self):
        templates = default_command_templates()
        for t in templates:
            assert not t.enabled
            assert t.requires_approval

    def test_save_and_load(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="test-save", argv_template=["echo", "hi"],
                                enabled=False)
            ok = save_command_template(t, data_dir=Path(td))
            assert ok
            loaded = list_command_templates(data_dir=Path(td))
            assert any(x.get("template_id") == "test-save" for x in loaded)

    def test_save_rejects_shell_metachars(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="bad", argv_template=["echo", "hello | rm"])
            ok = save_command_template(t, data_dir=Path(td))
            assert not ok

    def test_save_rejects_forbidden_program(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="bad", argv_template=["rm", "-rf", "/"])
            ok = save_command_template(t, data_dir=Path(td))
            assert not ok

    def test_save_rejects_unknown_placeholder(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="bad", argv_template=["echo"],
                                allowed_placeholders=["unknown_key"])
            ok = save_command_template(t, data_dir=Path(td))
            assert not ok


class TestApprovalGate(unittest.TestCase):
    """Test operator approval."""

    def test_approve_requires_enabled_template(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            # Default templates are disabled
            result = approve_managed_execution("ses1", "claude-code-repair-v0",
                                                data_dir=Path(td))
            assert result is None

    def test_approve_with_enabled_template(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="test-tmpl", argv_template=["echo", "hi"],
                                enabled=True, requires_approval=True)
            save_command_template(t, data_dir=Path(td))
            result = approve_managed_execution("ses1", "test-tmpl", data_dir=Path(td))
            assert result is not None
            assert result.session_id == "ses1"
            assert result.template_id == "test-tmpl"

    def test_load_approval(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="test-tmpl", argv_template=["echo", "hi"],
                                enabled=True)
            save_command_template(t, data_dir=Path(td))
            approve_managed_execution("ses1", "test-tmpl", data_dir=Path(td))
            loaded = get_execution_approval("ses1", data_dir=Path(td))
            assert loaded is not None
            assert loaded["session_id"] == "ses1"


class TestManagedRunner(unittest.TestCase):
    """Test the managed runner."""

    def test_blocks_missing_template(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            result = run_managed_builder("ses1", template_id="nonexistent",
                                          data_dir=Path(td))
            assert result.status == ManagedExecutionStatus.BLOCKED
            assert "template_not_found" in result.blocking_reasons

    def test_blocks_disabled_template(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            # Default templates are disabled
            result = run_managed_builder("ses1", template_id="claude-code-repair-v0",
                                          data_dir=Path(td))
            assert result.status == ManagedExecutionStatus.BLOCKED
            assert "template_disabled" in result.blocking_reasons

    def test_blocks_unapproved(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="tmpl1", argv_template=["echo", "hi"],
                                enabled=True, requires_approval=True)
            save_command_template(t, data_dir=Path(td))
            result = run_managed_builder("ses1", template_id="tmpl1",
                                          data_dir=Path(td))
            assert result.status == ManagedExecutionStatus.APPROVAL_REQUIRED

    def test_runs_approved_echo(self):
        """Test actual subprocess execution with echo."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="echo-test", argv_template=["echo", "hello-managed"],
                                enabled=True, requires_approval=False)
            save_command_template(t, data_dir=Path(td))
            result = run_managed_builder("ses1", template_id="echo-test",
                                          job_id="job1", data_dir=Path(td))
            assert result.status == ManagedExecutionStatus.COMPLETED
            assert result.exit_code == 0
            assert result.duration_ms >= 0
            assert result.output_ref  # has output ref

    def test_captures_nonzero_exit(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="fail-test", argv_template=["false"],
                                enabled=True, requires_approval=False)
            save_command_template(t, data_dir=Path(td))
            result = run_managed_builder("ses1", template_id="fail-test",
                                          job_id="job1", data_dir=Path(td))
            assert result.status == ManagedExecutionStatus.FAILED
            assert result.exit_code != 0

    def test_command_not_found(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="notfound-test",
                                argv_template=["nonexistent_cmd_abc123"],
                                enabled=True, requires_approval=False)
            save_command_template(t, data_dir=Path(td))
            result = run_managed_builder("ses1", template_id="notfound-test",
                                          data_dir=Path(td))
            assert result.status == ManagedExecutionStatus.FAILED
            assert "command_not_found" in result.blocking_reasons

    def test_shell_false_always(self):
        """Verify shell=False in subprocess call by checking the source."""
        import inspect
        src = inspect.getsource(run_managed_builder)
        # Must contain shell=False
        assert "shell=False" in src
        # Must NOT contain shell=True
        assert "shell=True" not in src


class TestEventLedger(unittest.TestCase):
    """Test event recording and listing."""

    def test_events_recorded_on_run(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="ev-test", argv_template=["echo", "hi"],
                                enabled=True, requires_approval=False)
            save_command_template(t, data_dir=Path(td))
            result = run_managed_builder("ses-ev", template_id="ev-test",
                                          job_id="job-ev", data_dir=Path(td))
            events = list_execution_events(session_id="ses-ev", job_id="job-ev",
                                            data_dir=Path(td))
            assert len(events) >= 2  # started + completed at minimum
            kinds = [e.get("kind") for e in events]
            assert ExecutionEventKind.STARTED in kinds
            assert ExecutionEventKind.COMPLETED in kinds


class TestDebugBundle(unittest.TestCase):
    """Test debug bundle generation."""

    def test_bundle_from_execution(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="bundle-test", argv_template=["echo", "debug"],
                                enabled=True, requires_approval=False)
            save_command_template(t, data_dir=Path(td))
            result = run_managed_builder("ses-db", template_id="bundle-test",
                                          job_id="job-db", data_dir=Path(td))
            bundle = build_debug_bundle(result.execution_id, data_dir=Path(td))
            assert bundle is not None
            assert bundle["execution_id"] == result.execution_id
            assert bundle["status"] == "completed"
            assert len(bundle["event_timeline"]) >= 2

    def test_bundle_nonexistent(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            bundle = build_debug_bundle("nonexistent", data_dir=Path(td))
            assert bundle is None


class TestMissionSignal(unittest.TestCase):
    """Test mission signal integration."""

    def test_empty_signal(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            sig = managed_execution_mission_signal("job1", data_dir=Path(td))
            assert sig["total_executions"] == 0
            assert sig["execution_satisfies_mission"] is False

    def test_never_satisfies_mission(self):
        """execution_satisfies_mission is ALWAYS False."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="sig-test", argv_template=["echo", "done"],
                                enabled=True, requires_approval=False)
            save_command_template(t, data_dir=Path(td))
            run_managed_builder("ses-sig", template_id="sig-test",
                                 job_id="job-sig", data_dir=Path(td))
            sig = managed_execution_mission_signal("job-sig", data_dir=Path(td))
            assert sig["completed_count"] == 1
            assert sig["execution_satisfies_mission"] is False


class TestIntegrity(unittest.TestCase):
    """Test integrity checks."""

    def test_defaults_pass(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            result = managed_execution_integrity(data_dir=Path(td))
            assert result["passed"]
            assert result["violation_count"] == 0

    def test_shell_metachar_flagged(self):
        tmpl = {"template_id": "bad", "argv_template": ["echo", "hello; rm"],
                "sanitized_env_keys": []}
        violations = audit_template_safety(tmpl)
        codes = [v["code"] for v in violations]
        assert "shell_metachar_in_template" in codes

    def test_forbidden_program_flagged(self):
        tmpl = {"template_id": "bad", "argv_template": ["rm", "-rf"],
                "sanitized_env_keys": []}
        violations = audit_template_safety(tmpl)
        codes = [v["code"] for v in violations]
        assert "forbidden_program_in_template" in codes

    def test_forbidden_env_flagged(self):
        tmpl = {"template_id": "bad", "argv_template": ["echo"],
                "sanitized_env_keys": ["ANTHROPIC_API_KEY"]}
        violations = audit_template_safety(tmpl)
        codes = [v["code"] for v in violations]
        assert "forbidden_env_key_in_template" in codes

    def test_secret_in_template_flagged(self):
        tmpl = {"template_id": "bad", "argv_template": ["echo"],
                "sanitized_env_keys": [], "notes": "sk-ant-secret123456789"}
        violations = audit_template_safety(tmpl)
        codes = [v["code"] for v in violations]
        assert "secret_or_raw_in_template" in codes

    def test_unknown_status_flagged(self):
        result = {"execution_id": "exe1", "status": "teleported"}
        violations = audit_execution_result_safety(result)
        codes = [v["code"] for v in violations]
        assert "unknown_execution_status" in codes

    def test_known_status_clean(self):
        result = {"execution_id": "exe1", "status": "completed"}
        violations = audit_execution_result_safety(result)
        assert len(violations) == 0

    def test_abs_path_in_result_flagged(self):
        result = {"execution_id": "exe1", "status": "completed",
                  "output_ref": "/home/user/output.raw"}
        violations = audit_execution_result_safety(result)
        codes = [v["code"] for v in violations]
        assert "absolute_path_in_result" in codes


class TestApprovalHardening(unittest.TestCase):
    """v1.1: Approval model hardening tests."""

    def test_approval_has_new_fields(self):
        a = ExecutionApproval(
            approval_id="ap1", session_id="ses1", template_id="tmpl1",
            package_id="pkg1", adapter_id="adp1", adapter_kind="generic",
            expires_at="2099-12-31T23:59:59+00:00", max_runs=5,
            used_count=0, approval_scope=ApprovalScope.SESSION_LIFETIME,
        )
        d = a.to_dict()
        assert d["package_id"] == "pkg1"
        assert d["adapter_id"] == "adp1"
        assert d["adapter_kind"] == "generic"
        assert d["max_runs"] == 5
        assert d["used_count"] == 0
        assert d["approval_scope"] == "session_lifetime"

    def test_approval_roundtrip(self):
        a = ExecutionApproval(
            approval_id="ap2", session_id="ses2", template_id="tmpl2",
            max_runs=3, approval_scope=ApprovalScope.TIME_BOUNDED,
            expires_at="2099-01-01T00:00:00+00:00",
        )
        d = a.to_dict()
        a2 = ExecutionApproval.from_dict(d)
        assert a2.approval_id == "ap2"
        assert a2.max_runs == 3
        assert a2.approval_scope == "time_bounded"

    def test_approval_clamps_runtime(self):
        a = ExecutionApproval(max_runtime_seconds=99999)
        d = a.to_dict()
        assert d["max_runtime_seconds"] == MAX_TIMEOUT_SECONDS

    def test_approval_clamps_output(self):
        a = ExecutionApproval(max_output_bytes=999999)
        d = a.to_dict()
        assert d["max_output_bytes"] == MAX_OUTPUT_BYTES

    def test_invalid_scope_defaults_to_single_run(self):
        a = ExecutionApproval(approval_scope="teleport")
        d = a.to_dict()
        assert d["approval_scope"] == "single_run"

    def test_approve_single_run_forces_max_runs_1(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="tmpl1", argv_template=["echo", "hi"],
                                enabled=True)
            save_command_template(t, data_dir=Path(td))
            result = approve_managed_execution(
                "ses1", "tmpl1", max_runs=99,
                approval_scope=ApprovalScope.SINGLE_RUN,
                data_dir=Path(td),
            )
            assert result is not None
            assert result.max_runs == 1

    def test_approve_with_binding(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="tmpl1", argv_template=["echo", "hi"],
                                enabled=True, adapter_kind="generic")
            save_command_template(t, data_dir=Path(td))
            result = approve_managed_execution(
                "ses1", "tmpl1",
                package_id="pkg1", adapter_id="adp1",
                data_dir=Path(td),
            )
            assert result is not None
            assert result.package_id == "pkg1"
            assert result.adapter_id == "adp1"
            assert result.adapter_kind == "generic"  # derived from template


class TestApprovalValidation(unittest.TestCase):
    """v1.1: validate_execution_approval() tests."""

    def test_approval_not_found(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            codes = validate_execution_approval("ses1", "tmpl1", data_dir=Path(td))
            assert "approval_not_found" in codes

    def test_valid_approval(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="tmpl1", argv_template=["echo", "hi"],
                                enabled=True)
            save_command_template(t, data_dir=Path(td))
            approve_managed_execution("ses1", "tmpl1", data_dir=Path(td))
            codes = validate_execution_approval("ses1", "tmpl1", data_dir=Path(td))
            assert len(codes) == 0

    def test_template_mismatch(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="tmpl1", argv_template=["echo", "hi"],
                                enabled=True)
            save_command_template(t, data_dir=Path(td))
            approve_managed_execution("ses1", "tmpl1", data_dir=Path(td))
            codes = validate_execution_approval("ses1", "wrong-tmpl", data_dir=Path(td))
            assert "template_mismatch" in codes

    def test_expired_approval(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="tmpl1", argv_template=["echo", "hi"],
                                enabled=True)
            save_command_template(t, data_dir=Path(td))
            approve_managed_execution(
                "ses1", "tmpl1", expires_at="2020-01-01T00:00:00+00:00",
                data_dir=Path(td),
            )
            codes = validate_execution_approval("ses1", "tmpl1", data_dir=Path(td))
            assert "approval_expired" in codes

    def test_exhausted_approval(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="tmpl1", argv_template=["echo", "hi"],
                                enabled=True, requires_approval=False)
            save_command_template(t, data_dir=Path(td))
            # Approve with max_runs=1, then run to exhaust.
            approve_managed_execution("ses1", "tmpl1", max_runs=1,
                                       approval_scope=ApprovalScope.SINGLE_RUN,
                                       data_dir=Path(td))
            # Run to exhaust the approval.
            run_managed_builder("ses1", template_id="tmpl1", data_dir=Path(td))
            codes = validate_execution_approval("ses1", "tmpl1", data_dir=Path(td))
            assert "approval_exhausted" in codes or "scope_violation" in codes

    def test_adapter_kind_mismatch(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="tmpl1", argv_template=["echo", "hi"],
                                enabled=True, adapter_kind="claude_code")
            save_command_template(t, data_dir=Path(td))
            approve_managed_execution(
                "ses1", "tmpl1", adapter_kind="wrong_kind",
                data_dir=Path(td),
            )
            codes = validate_execution_approval("ses1", "tmpl1", data_dir=Path(td))
            assert "adapter_kind_mismatch" in codes

    def test_package_mismatch(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="tmpl1", argv_template=["echo", "hi"],
                                enabled=True)
            save_command_template(t, data_dir=Path(td))
            approve_managed_execution(
                "ses1", "tmpl1", package_id="pkg1",
                data_dir=Path(td),
            )
            codes = validate_execution_approval(
                "ses1", "tmpl1", package_id="wrong-pkg",
                data_dir=Path(td),
            )
            assert "package_mismatch" in codes

    def test_adapter_mismatch(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="tmpl1", argv_template=["echo", "hi"],
                                enabled=True)
            save_command_template(t, data_dir=Path(td))
            approve_managed_execution(
                "ses1", "tmpl1", adapter_id="adp1",
                data_dir=Path(td),
            )
            codes = validate_execution_approval(
                "ses1", "tmpl1", adapter_id="wrong-adp",
                data_dir=Path(td),
            )
            assert "adapter_mismatch" in codes


class TestApprovalIntegrity(unittest.TestCase):
    """v1.1: Approval integrity audit tests."""

    def test_unknown_scope(self):
        violations = audit_approval_safety({"approval_id": "a1", "approval_scope": "teleport"})
        codes = [v["code"] for v in violations]
        assert "unknown_approval_scope" in codes

    def test_used_exceeds_max(self):
        violations = audit_approval_safety({
            "approval_id": "a1", "max_runs": 3, "used_count": 5,
        })
        codes = [v["code"] for v in violations]
        assert "used_count_exceeds_max_runs" in codes

    def test_expired_flagged(self):
        violations = audit_approval_safety({
            "approval_id": "a1", "expires_at": "2020-01-01T00:00:00+00:00",
        })
        codes = [v["code"] for v in violations]
        assert "approval_currently_expired" in codes

    def test_adapter_kind_mismatch_with_template(self):
        templates = [{"template_id": "t1", "adapter_kind": "claude_code"}]
        violations = audit_approval_safety(
            {"approval_id": "a1", "template_id": "t1", "adapter_kind": "generic"},
            templates=templates,
        )
        codes = [v["code"] for v in violations]
        assert "adapter_kind_mismatch_with_template" in codes

    def test_runtime_exceeds_system_max(self):
        violations = audit_approval_safety({
            "approval_id": "a1", "max_runtime_seconds": 99999,
        })
        codes = [v["code"] for v in violations]
        assert "approval_runtime_exceeds_system_max" in codes

    def test_single_run_max_runs_mismatch(self):
        violations = audit_approval_safety({
            "approval_id": "a1", "approval_scope": "single_run", "max_runs": 5,
        })
        codes = [v["code"] for v in violations]
        assert "single_run_scope_max_runs_mismatch" in codes

    def test_clean_approval_passes(self):
        violations = audit_approval_safety({
            "approval_id": "a1", "approval_scope": "single_run", "max_runs": 1,
            "used_count": 0,
        })
        assert len(violations) == 0

    def test_integrity_includes_approvals(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            result = managed_execution_integrity(data_dir=Path(td))
            assert "approval_count" in result
            assert result["version"] == 2


class TestDebugBundleHardening(unittest.TestCase):
    """v1.1: Debug bundle includes approval validation."""

    def test_bundle_has_approval_validation(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="db-test", argv_template=["echo", "hi"],
                                enabled=True, requires_approval=False)
            save_command_template(t, data_dir=Path(td))
            result = run_managed_builder("ses-db2", template_id="db-test",
                                          job_id="job-db2", data_dir=Path(td))
            bundle = build_debug_bundle(result.execution_id, data_dir=Path(td))
            assert bundle is not None
            assert "approval_validation" in bundle
            assert "repair_suggestion" in bundle

    def test_bundle_approval_scope_visible(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="sc-test", argv_template=["echo", "hi"],
                                enabled=True)
            save_command_template(t, data_dir=Path(td))
            approve_managed_execution("ses-sc", "sc-test",
                                       approval_scope=ApprovalScope.SESSION_LIFETIME,
                                       max_runs=10, data_dir=Path(td))
            result = run_managed_builder("ses-sc", template_id="sc-test",
                                          job_id="job-sc", data_dir=Path(td))
            bundle = build_debug_bundle(result.execution_id, data_dir=Path(td))
            assert bundle is not None
            assert bundle["approval"]["scope"] == "session_lifetime"
            assert bundle["approval"]["max_runs"] == 10


class TestRunnerApprovalEnforcement(unittest.TestCase):
    """v1.1: Runner enforces approval validation."""

    def test_runner_blocks_expired_approval(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="tmpl1", argv_template=["echo", "hi"],
                                enabled=True)
            save_command_template(t, data_dir=Path(td))
            approve_managed_execution("ses1", "tmpl1",
                                       expires_at="2020-01-01T00:00:00+00:00",
                                       data_dir=Path(td))
            result = run_managed_builder("ses1", template_id="tmpl1",
                                          data_dir=Path(td))
            assert result.status == ManagedExecutionStatus.BLOCKED
            assert any("approval_expired" in r for r in result.blocking_reasons)

    def test_runner_blocks_exhausted_approval(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="tmpl1", argv_template=["echo", "hi"],
                                enabled=True)
            save_command_template(t, data_dir=Path(td))
            approve_managed_execution("ses1", "tmpl1",
                                       max_runs=1, approval_scope=ApprovalScope.SINGLE_RUN,
                                       data_dir=Path(td))
            # First run succeeds.
            r1 = run_managed_builder("ses1", template_id="tmpl1",
                                      data_dir=Path(td))
            assert r1.status == ManagedExecutionStatus.COMPLETED
            # Second run blocked.
            r2 = run_managed_builder("ses1", template_id="tmpl1",
                                      data_dir=Path(td))
            assert r2.status == ManagedExecutionStatus.BLOCKED

    def test_runner_emits_approval_consumed_event(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="tmpl1", argv_template=["echo", "hi"],
                                enabled=True)
            save_command_template(t, data_dir=Path(td))
            approve_managed_execution("ses1", "tmpl1",
                                       max_runs=5, approval_scope=ApprovalScope.SESSION_LIFETIME,
                                       data_dir=Path(td))
            result = run_managed_builder("ses1", template_id="tmpl1",
                                          job_id="j1", data_dir=Path(td))
            events = list_execution_events(session_id="ses1", job_id="j1",
                                            data_dir=Path(td))
            kinds = [e.get("kind") for e in events]
            assert ExecutionEventKind.APPROVAL_VALIDATED in kinds
            assert ExecutionEventKind.APPROVAL_CONSUMED in kinds

    def test_runner_increments_used_count(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="tmpl1", argv_template=["echo", "hi"],
                                enabled=True)
            save_command_template(t, data_dir=Path(td))
            approve_managed_execution("ses1", "tmpl1",
                                       max_runs=5, approval_scope=ApprovalScope.SESSION_LIFETIME,
                                       data_dir=Path(td))
            run_managed_builder("ses1", template_id="tmpl1", data_dir=Path(td))
            approval = get_execution_approval("ses1", data_dir=Path(td))
            assert approval is not None
            assert int(approval.get("used_count", 0)) == 1

    def test_list_approvals(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="tmpl1", argv_template=["echo", "hi"],
                                enabled=True)
            save_command_template(t, data_dir=Path(td))
            approve_managed_execution("ses1", "tmpl1", data_dir=Path(td))
            approve_managed_execution("ses2", "tmpl1", data_dir=Path(td))
            approvals = list_execution_approvals(data_dir=Path(td))
            assert len(approvals) >= 2

    def test_new_event_kinds_exist(self):
        """All v1.1 event kinds are in _ALL_EVENT_KINDS."""
        from packages.orchestration.managed_builder_execution import _ALL_EVENT_KINDS
        for kind in [
            ExecutionEventKind.APPROVAL_EXPIRED,
            ExecutionEventKind.APPROVAL_EXHAUSTED,
            ExecutionEventKind.APPROVAL_VALIDATED,
            ExecutionEventKind.BINDING_MISMATCH,
            ExecutionEventKind.APPROVAL_CONSUMED,
            ExecutionEventKind.RUNTIME_CAP_APPLIED,
            ExecutionEventKind.OUTPUT_CAP_APPLIED,
        ]:
            assert kind in _ALL_EVENT_KINDS, f"{kind} not in _ALL_EVENT_KINDS"


class TestArchitectureGuards(unittest.TestCase):
    """Verify the module does not import forbidden libraries or use shell=True."""

    def test_no_forbidden_imports(self):
        """managed_builder_execution.py must only use stdlib + provider_trust."""
        src_path = Path(__file__).resolve().parent.parent.parent / "packages" / "orchestration" / "managed_builder_execution.py"
        src = src_path.read_text()
        # Allowed: stdlib (hashlib, json, os, re, subprocess, time, dataclasses, datetime,
        #          pathlib, typing, uuid) + provider_trust
        forbidden_patterns = [
            r"import anthropic", r"import openai", r"import requests",
            r"import httpx", r"import aiohttp", r"import urllib\.request",
            r"import selenium", r"import playwright",
            r"from packages\.orchestration\.storage ",
            r"import boto3", r"import google\.",
        ]
        for pat in forbidden_patterns:
            assert not re.search(pat, src), f"Forbidden import: {pat}"

    def test_no_shell_true(self):
        """No shell=True in executable code (docstrings/comments describing the rule are ok)."""
        src_path = Path(__file__).resolve().parent.parent.parent / "packages" / "orchestration" / "managed_builder_execution.py"
        src = src_path.read_text()
        # Check only non-comment, non-docstring lines for shell=True as a kwarg
        for line in src.splitlines():
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith('"""') or stripped.startswith("'"):
                continue
            if stripped.startswith("-"):  # docstring continuation
                continue
            assert "shell=True" not in stripped, f"shell=True found in code: {stripped}"

    def test_no_auto_apply_or_approve(self):
        """No auto-apply/approve/PR/git patterns."""
        src_path = Path(__file__).resolve().parent.parent.parent / "packages" / "orchestration" / "managed_builder_execution.py"
        src = src_path.read_text().lower()
        for forbidden in ["auto_apply", "auto_approve", "git push", "git commit",
                          "gh pr create", "auto_merge"]:
            assert forbidden not in src, f"Forbidden pattern: {forbidden}"

    def test_execution_satisfies_mission_hardcoded_false(self):
        """execution_satisfies_mission must be hardcoded to False."""
        src_path = Path(__file__).resolve().parent.parent.parent / "packages" / "orchestration" / "managed_builder_execution.py"
        src = src_path.read_text()
        assert '"execution_satisfies_mission": False' in src


if __name__ == "__main__":
    unittest.main()
