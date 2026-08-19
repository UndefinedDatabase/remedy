"""Tests for Managed Builder Execution v1 (Steps 2026-2075).

Unit tests + architecture guards. No network, no provider, no real subprocess for most tests.
"""

from __future__ import annotations

import json
import re
import tempfile
import unittest
from pathlib import Path

from packages.orchestration.managed_builder_execution import (
    _ALLOWED_ENV_KEYS,
    MAX_OUTPUT_BYTES,
    MAX_TIMEOUT_SECONDS,
    SCHEMA_VERSION,
    ApprovalScope,
    CommandTemplate,
    ExecutionApproval,
    ExecutionEvent,
    ExecutionEventKind,
    ManagedExecutionResult,
    ManagedExecutionStatus,
    _build_sanitized_env,
    _resolve_argv,
    _validate_argv_template,
    approve_managed_execution,
    audit_approval_safety,
    audit_execution_result_safety,
    audit_template_safety,
    build_debug_bundle,
    default_command_templates,
    disable_command_template,
    enable_command_template,
    get_command_template,
    get_execution_approval,
    list_command_templates,
    list_execution_approvals,
    list_execution_events,
    managed_execution_integrity,
    managed_execution_mission_signal,
    run_managed_builder,
    save_command_template,
    update_command_template,
    validate_execution_approval,
)


def _create_test_session(td: str, session_id: str, package_id: str = "",
                          adapter_id: str = "", job_id: str = "_global",
                          status: str = "package_ready") -> None:
    """Create a minimal BuilderSessionRecord for tests that need a real session."""
    sessions_dir = Path(td) / "workspaces" / job_id / "main_builder_adapter" / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)
    import json as _json
    _json.dump({
        "session_id": session_id, "adapter_id": adapter_id,
        "package_id": package_id, "job_id": job_id,
        "repair_id": "", "status": status,
        "created_at": "", "updated_at": "",
    }, open(sessions_dir / f"{session_id}.json", "w"))


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
            _create_test_session(td, "ses1")
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
            _create_test_session(td, "ses1")
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
            _create_test_session(td, "ses1")
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
            _create_test_session(td, "ses1")
            t = CommandTemplate(template_id="notfound-test",
                                argv_template=["nonexistent_cmd_abc123"],
                                enabled=True, requires_approval=False)
            save_command_template(t, data_dir=Path(td))
            result = run_managed_builder("ses1", template_id="notfound-test",
                                          data_dir=Path(td))
            assert result.status == ManagedExecutionStatus.FAILED
            assert "command_not_found" in result.blocking_reasons

    def test_spawn_goes_through_the_guard_and_never_through_a_shell(self):
        """Assert the no-shell property by AST, because the text form was vacuous.

        The old assertion searched this function's source for `shell=False` and was
        satisfied by its DOCSTRING (R-0504). Since F085 T002a the spawn lives in
        `exec_guard.run_guarded`, so the property is asserted where it is enforced.
        """
        import ast
        import inspect

        from packages.orchestration import exec_guard
        from packages.orchestration import managed_builder_execution as mbe

        def spawn_calls(func):
            tree = ast.parse(inspect.getsource(func))
            return [n for n in ast.walk(tree)
                    if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                    and n.func.attr in {"run", "Popen", "call", "check_output"}
                    and isinstance(n.func.value, ast.Name)
                    and n.func.value.id == "subprocess"]

        assert spawn_calls(run_managed_builder) == []
        popens = spawn_calls(exec_guard.run_guarded)
        assert len(popens) == 1
        assert "shell" not in {kw.arg for kw in popens[0].keywords}
        # By AST, not by text: this module's own docstring carries the words
        # "NO shell=True", so a substring search fails on prose either way.
        module_tree = ast.parse(inspect.getsource(mbe))
        assert not [n for n in ast.walk(module_tree)
                    if isinstance(n, ast.keyword) and n.arg == "shell"
                    and isinstance(n.value, ast.Constant) and n.value.value is True]

    def test_wall_timeout_is_translated_into_the_timeout_status(self):
        """The guard CLASSIFIES a wall trip; this seam must still REPORT a timeout."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            _create_test_session(td, "ses-to")
            t = CommandTemplate(template_id="to-test", argv_template=["sleep", "5"],
                                enabled=True, requires_approval=False, timeout_seconds=1)
            save_command_template(t, data_dir=Path(td))
            result = run_managed_builder("ses-to", template_id="to-test",
                                          job_id="job-to", data_dir=Path(td))
            assert result.status == ManagedExecutionStatus.TIMEOUT
            assert result.safe_summary == "Timeout after 1s"

    def test_a_signal_death_keeps_the_negative_exit_code_contract(self):
        """subprocess.run reported -SIGNUM; the guard reports a NAME. -9 either way."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            _create_test_session(td, "ses-sig9")
            script = Path(td) / "selfkill.py"
            script.write_text("import os, signal\nos.kill(os.getpid(), signal.SIGKILL)\n")
            t = CommandTemplate(template_id="sig9-test",
                                argv_template=["python3", str(script)],
                                enabled=True, requires_approval=False)
            save_command_template(t, data_dir=Path(td))
            result = run_managed_builder("ses-sig9", template_id="sig9-test",
                                          job_id="job-sig9", data_dir=Path(td))
            assert result.status == ManagedExecutionStatus.FAILED
            assert result.exit_code == -9

    def test_builder_policy_reproduces_the_sanitized_env_and_floors_it(self):
        """The allowlist is an identity on an already-sanitized env, and still a floor."""
        from packages.orchestration.exec_guard import scrub_child_env
        from packages.orchestration.managed_builder_execution import _builder_exec_policy
        env = _build_sanitized_env({})
        policy = _builder_exec_policy(30, 4096, None, env)
        assert scrub_child_env(env, policy.env_allowlist) == env
        assert policy.wall_timeout_seconds == 30.0 and policy.cpu_seconds is None
        smuggled = dict(env, GITHUB_TOKEN="ghp_never")
        floored = _builder_exec_policy(30, 4096, None, smuggled)
        assert "GITHUB_TOKEN" not in scrub_child_env(smuggled, floored.env_allowlist)

    def test_the_builder_policy_denies_the_network_its_row_denies(self):
        """Amendment F085 D1's network column for the `builder` row, in code."""
        from packages.orchestration.exec_guard import (
            DENIED_NETWORK_ENV,
            plan_child_spawn,
        )
        from packages.orchestration.managed_builder_execution import _builder_exec_policy
        env = _build_sanitized_env({})
        policy = _builder_exec_policy(30, 4096, None, env)
        assert policy.deny_network is True
        child_env = plan_child_spawn(policy).env
        assert dict(DENIED_NETWORK_ENV).items() <= child_env.items()
        assert all(child_env[key] == value for key, value in env.items())


class TestEventLedger(unittest.TestCase):
    """Test event recording and listing."""

    def test_events_recorded_on_run(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            _create_test_session(td, "ses-ev")
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
            _create_test_session(td, "ses-db")
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
            _create_test_session(td, "ses-sig")
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
        result = {"execution_id": "exe1", "status": "completed",
                  "output_ref": "mbe/output/exe1.raw"}
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
            _create_test_session(td, "ses1")
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
            _create_test_session(td, "ses1")
            t = CommandTemplate(template_id="tmpl1", argv_template=["echo", "hi"],
                                enabled=True)
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
            "expires_at": "2099-12-31T23:59:59+00:00",
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
            _create_test_session(td, "ses-db2")
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
            _create_test_session(td, "ses-sc")
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
            _create_test_session(td, "ses1")
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
            _create_test_session(td, "ses1")
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
            _create_test_session(td, "ses1")
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
            _create_test_session(td, "ses1")
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


class TestR0106DefaultExpiry(unittest.TestCase):
    """R-0106: Approval must have default expiry; missing expiry = invalid."""

    def test_default_approval_has_future_expires_at(self):
        """approve_managed_execution() auto-sets expires_at ~30min in future."""
        import tempfile
        from datetime import datetime, timezone
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="r106-t", argv_template=["echo", "hi"],
                                enabled=True)
            save_command_template(t, data_dir=Path(td))
            approval = approve_managed_execution("ses-r106", "r106-t",
                                                   data_dir=Path(td))
            assert approval is not None
            d = approval.to_dict()
            assert d["expires_at"], "expires_at must not be empty"
            exp_dt = datetime.fromisoformat(d["expires_at"])
            assert exp_dt > datetime.now(timezone.utc), "expires_at must be in the future"

    def test_missing_expires_at_is_invalid(self):
        """validate_execution_approval flags missing expires_at as expired."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="r106-t", argv_template=["echo", "hi"],
                                enabled=True)
            save_command_template(t, data_dir=Path(td))
            # Approve then manually strip expires_at.
            approve_managed_execution("ses-r106b", "r106-t", data_dir=Path(td))
            p = Path(td) / "managed_builder_execution" / "approvals" / "ses-r106b.json"
            import json
            data = json.loads(p.read_text())
            data["expires_at"] = ""
            p.write_text(json.dumps(data))
            codes = validate_execution_approval("ses-r106b", "r106-t",
                                                  data_dir=Path(td))
            assert "approval_expired" in codes

    def test_expired_approval_blocks_execution(self):
        """Runner blocks execution when approval has expired."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            _create_test_session(td, "ses-r106c")
            t = CommandTemplate(template_id="r106-t", argv_template=["echo", "hi"],
                                enabled=True)
            save_command_template(t, data_dir=Path(td))
            approve_managed_execution("ses-r106c", "r106-t",
                                       expires_at="2020-01-01T00:00:00+00:00",
                                       data_dir=Path(td))
            result = run_managed_builder("ses-r106c", template_id="r106-t",
                                           data_dir=Path(td))
            assert result.status == ManagedExecutionStatus.BLOCKED

    def test_integrity_flags_missing_expiry(self):
        """audit_approval_safety flags missing expires_at."""
        violations = audit_approval_safety({
            "approval_id": "a-r106", "approval_scope": "single_run",
            "max_runs": 1, "used_count": 0,
        })
        codes = [v["code"] for v in violations]
        assert "missing_expires_at" in codes


class TestR0107SessionBinding(unittest.TestCase):
    """R-0107: validate_execution_approval validates against real session."""

    def test_missing_session_returns_session_not_found(self):
        """Missing session yields session_not_found code (R-0111)."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="r107-t", argv_template=["echo", "hi"],
                                enabled=True)
            save_command_template(t, data_dir=Path(td))
            approve_managed_execution("ses-r107-ghost", "r107-t",
                                       data_dir=Path(td))
            codes = validate_execution_approval("ses-r107-ghost", "r107-t",
                                                  data_dir=Path(td))
            assert "session_not_found" in codes

    def _create_session(self, td, session_id, package_id="", adapter_id="",
                         job_id="_global", status=None):
        """Helper to create a real builder session for binding tests."""
        from packages.orchestration.main_builder_adapter import (
            BuilderSessionRecord,
            BuilderSessionStatus,
        )
        if status is None:
            status = BuilderSessionStatus.PACKAGE_READY
        s = BuilderSessionRecord(
            session_id=session_id, adapter_id=adapter_id,
            package_id=package_id, job_id=job_id, status=status)
        sessions_dir = Path(td) / "workspaces" / job_id / "main_builder_adapter" / "sessions"
        sessions_dir.mkdir(parents=True, exist_ok=True)
        (sessions_dir / f"{session_id}.json").write_text(json.dumps(s.to_dict()))

    def test_package_mismatch_via_binding(self):
        """Approval with package_id mismatch against real session package_id."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            self._create_session(td, "ses-r107-pkg", package_id="pkg-real")
            t = CommandTemplate(template_id="r107-t", argv_template=["echo", "hi"],
                                enabled=True)
            save_command_template(t, data_dir=Path(td))
            approve_managed_execution("ses-r107-pkg", "r107-t",
                                       package_id="pkg-WRONG",
                                       data_dir=Path(td))
            codes = validate_execution_approval("ses-r107-pkg", "r107-t",
                                                  data_dir=Path(td))
            assert "approval_package_mismatch" in codes

    def test_valid_session_passes_binding(self):
        """Session with matching fields passes binding validation."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            self._create_session(td, "ses-r107-ok", package_id="pkg1")
            t = CommandTemplate(template_id="r107-t", argv_template=["echo", "hi"],
                                enabled=True)
            save_command_template(t, data_dir=Path(td))
            approve_managed_execution("ses-r107-ok", "r107-t",
                                       package_id="pkg1",
                                       data_dir=Path(td))
            codes = validate_execution_approval("ses-r107-ok", "r107-t",
                                                  data_dir=Path(td))
            # Should not have binding-related codes.
            assert "approval_package_mismatch" not in codes


class TestR0108UsedCountTiming(unittest.TestCase):
    """R-0108: used_count increments before execution, not after success."""

    def test_failed_run_consumes_approval(self):
        """A run that fails (exit_code != 0) still increments used_count."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            _create_test_session(td, "ses-r108")
            t = CommandTemplate(template_id="r108-t", argv_template=["false"],
                                enabled=True)
            save_command_template(t, data_dir=Path(td))
            approve_managed_execution("ses-r108", "r108-t",
                                       max_runs=5,
                                       approval_scope=ApprovalScope.SESSION_LIFETIME,
                                       data_dir=Path(td))
            result = run_managed_builder("ses-r108", template_id="r108-t",
                                           data_dir=Path(td))
            # Even with non-zero exit, used_count must increment.
            approval = get_execution_approval("ses-r108", data_dir=Path(td))
            assert approval is not None
            assert int(approval.get("used_count", 0)) >= 1

    def test_single_run_blocks_after_failed_run(self):
        """Single-run approval is exhausted even if first run fails."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            _create_test_session(td, "ses-r108b")
            t = CommandTemplate(template_id="r108-t2", argv_template=["false"],
                                enabled=True)
            save_command_template(t, data_dir=Path(td))
            approve_managed_execution("ses-r108b", "r108-t2",
                                       max_runs=1,
                                       approval_scope=ApprovalScope.SINGLE_RUN,
                                       data_dir=Path(td))
            # First run fails but consumes.
            run_managed_builder("ses-r108b", template_id="r108-t2",
                                  data_dir=Path(td))
            # Second run must be blocked.
            r2 = run_managed_builder("ses-r108b", template_id="r108-t2",
                                       data_dir=Path(td))
            assert r2.status == ManagedExecutionStatus.BLOCKED

    def test_argv_failure_does_not_consume(self):
        """If argv resolution fails before subprocess start, used_count stays 0."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            _create_test_session(td, "ses-r108c")
            # Template with allowed placeholder but no value provided at runtime.
            t = CommandTemplate(template_id="r108-t3",
                                argv_template=["echo", "{repo_path}"],
                                allowed_placeholders=["repo_path"],
                                enabled=True)
            save_command_template(t, data_dir=Path(td))
            approve_managed_execution("ses-r108c", "r108-t3",
                                       max_runs=5,
                                       approval_scope=ApprovalScope.SESSION_LIFETIME,
                                       data_dir=Path(td))
            result = run_managed_builder("ses-r108c", template_id="r108-t3",
                                           data_dir=Path(td))
            assert result.status == ManagedExecutionStatus.BLOCKED
            assert any("argv_resolution_failed" in r for r in result.blocking_reasons)
            approval = get_execution_approval("ses-r108c", data_dir=Path(td))
            # Argv failed before subprocess start — used_count stays 0.
            assert int(approval.get("used_count", 0)) == 0


class TestR0109ActionClass(unittest.TestCase):
    """R-0109: execution.run action_class must be controlled_builder_execution."""

    def test_catalog_execution_run_action_class(self):
        from apps.cli.command_catalog import CATALOG
        execution_run = None
        for cmd in CATALOG:
            if cmd.group_id == "execution" and cmd.subcommand == "run":
                execution_run = cmd
                break
        assert execution_run is not None, "execution.run not found in catalog"
        assert execution_run.action_class == "controlled_builder_execution", \
            f"Expected controlled_builder_execution, got {execution_run.action_class}"

    def test_not_test_execution(self):
        from apps.cli.command_catalog import CATALOG
        for cmd in CATALOG:
            if cmd.group_id == "execution" and cmd.subcommand == "run":
                assert cmd.action_class != "test_execution", \
                    "execution.run must NOT use test_execution action_class"


class TestR0110EventSequenceIntegrity(unittest.TestCase):
    """R-0110: Debug/integrity must verify event sequence and output refs."""

    def test_completed_missing_output_ref_flagged(self):
        violations = audit_execution_result_safety(
            {"execution_id": "r110-e1", "status": "completed"})
        codes = [v["code"] for v in violations]
        assert "completed_missing_output_ref" in codes

    def test_completed_with_output_ref_clean(self):
        violations = audit_execution_result_safety(
            {"execution_id": "r110-e2", "status": "completed",
             "output_ref": "mbe/output/r110-e2.raw"})
        assert len(violations) == 0

    def test_completed_missing_started_event_flagged(self):
        events = [{"execution_id": "r110-e3", "kind": "approval_validated"}]
        violations = audit_execution_result_safety(
            {"execution_id": "r110-e3", "status": "completed",
             "output_ref": "mbe/output/r110-e3.raw"},
            events=events)
        codes = [v["code"] for v in violations]
        assert "completed_missing_started_event" in codes

    def test_completed_with_full_events_clean(self):
        events = [
            {"execution_id": "r110-e4", "kind": ExecutionEventKind.STARTED},
            {"execution_id": "r110-e4", "kind": ExecutionEventKind.OUTPUT_REF_CREATED},
            {"execution_id": "r110-e4", "kind": ExecutionEventKind.COMPLETED},
        ]
        violations = audit_execution_result_safety(
            {"execution_id": "r110-e4", "status": "completed",
             "output_ref": "mbe/output/r110-e4.raw"},
            events=events)
        assert len(violations) == 0

    def test_result_claiming_repair_done_flagged(self):
        violations = audit_execution_result_safety(
            {"execution_id": "r110-e5", "status": "completed",
             "output_ref": "mbe/output/r110-e5.raw",
             "safe_summary": "repair_done successfully"})
        codes = [v["code"] for v in violations]
        assert "result_claims_repair_or_mission_done" in codes

    def test_debug_bundle_has_binding_summary(self):
        """Debug bundle includes binding_summary and event_sequence."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            _create_test_session(td, "ses-r110")
            t = CommandTemplate(template_id="r110-t", argv_template=["echo", "hi"],
                                enabled=True, requires_approval=False)
            save_command_template(t, data_dir=Path(td))
            result = run_managed_builder("ses-r110", template_id="r110-t",
                                          job_id="job-r110", data_dir=Path(td))
            bundle = build_debug_bundle(result.execution_id, data_dir=Path(td))
            assert bundle is not None
            assert "binding_summary" in bundle
            assert "event_sequence" in bundle
            assert "output_ref_present" in bundle

    def test_debug_bundle_no_absolute_paths(self):
        """Debug bundle output_ref must not leak absolute paths."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            _create_test_session(td, "ses-r110b")
            t = CommandTemplate(template_id="r110-t2", argv_template=["echo", "hi"],
                                enabled=True, requires_approval=False)
            save_command_template(t, data_dir=Path(td))
            result = run_managed_builder("ses-r110b", template_id="r110-t2",
                                          data_dir=Path(td))
            bundle = build_debug_bundle(result.execution_id, data_dir=Path(td))
            assert bundle is not None
            # output_ref must be scrubbed (no absolute paths).
            output_ref = bundle.get("output_ref", "")
            assert not output_ref.startswith("/home/"), "output_ref leaks absolute path"


class TestR0111SessionRequired(unittest.TestCase):
    """R-0111: run_managed_builder blocks ghost sessions."""

    def test_runner_blocks_ghost_session(self):
        """run_managed_builder blocks when no BuilderSession exists."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="r111-t", argv_template=["echo", "hi"],
                                enabled=True, requires_approval=False)
            save_command_template(t, data_dir=Path(td))
            result = run_managed_builder("ghost-session", template_id="r111-t",
                                          data_dir=Path(td))
            assert result.status == ManagedExecutionStatus.BLOCKED
            assert "session_not_found" in result.blocking_reasons

    def test_runner_passes_with_real_session(self):
        """run_managed_builder succeeds when a real BuilderSession exists."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            _create_test_session(td, "real-ses")
            t = CommandTemplate(template_id="r111-t", argv_template=["echo", "hi"],
                                enabled=True, requires_approval=False)
            save_command_template(t, data_dir=Path(td))
            result = run_managed_builder("real-ses", template_id="r111-t",
                                          data_dir=Path(td))
            assert result.status == ManagedExecutionStatus.COMPLETED

    def test_validate_returns_session_not_found(self):
        """validate_execution_approval returns session_not_found for ghost."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            t = CommandTemplate(template_id="r111-t", argv_template=["echo", "hi"],
                                enabled=True)
            save_command_template(t, data_dir=Path(td))
            approve_managed_execution("ghost-v", "r111-t", data_dir=Path(td))
            codes = validate_execution_approval("ghost-v", "r111-t",
                                                  data_dir=Path(td))
            assert "session_not_found" in codes


class TestR0112AdapterSpecDict(unittest.TestCase):
    """R-0112: AdapterSpec dict handling — no crash."""

    def test_real_session_with_adapter_spec_no_crash(self):
        """Validation with real session + adapter spec doesn't crash on dict."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            _create_test_session(td, "ses-r112", adapter_id="adp-r112")
            # Create adapter spec as dict (same format get_builder_adapter_spec returns).
            adapters_dir = Path(td) / "main_builder_adapter" / "adapters"
            adapters_dir.mkdir(parents=True, exist_ok=True)
            import json
            json.dump({"adapter_id": "adp-r112", "kind": "claude_code",
                        "enabled": True, "mode": "safe", "command_template_id": ""},
                       open(adapters_dir / "adp-r112.json", "w"))
            t = CommandTemplate(template_id="r112-t", argv_template=["echo", "hi"],
                                enabled=True, adapter_kind="claude_code")
            save_command_template(t, data_dir=Path(td))
            approve_managed_execution("ses-r112", "r112-t",
                                       adapter_id="adp-r112",
                                       data_dir=Path(td))
            # Must not crash.
            codes = validate_execution_approval("ses-r112", "r112-t",
                                                  data_dir=Path(td))
            assert "template_adapter_kind_mismatch" not in codes

    def test_template_kind_mismatch_detected(self):
        """Template kind != adapter spec kind → template_adapter_kind_mismatch."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            _create_test_session(td, "ses-r112b", adapter_id="adp-r112b")
            adapters_dir = Path(td) / "main_builder_adapter" / "adapters"
            adapters_dir.mkdir(parents=True, exist_ok=True)
            import json
            json.dump({"adapter_id": "adp-r112b", "kind": "pi_dev",
                        "enabled": True, "mode": "safe", "command_template_id": ""},
                       open(adapters_dir / "adp-r112b.json", "w"))
            t = CommandTemplate(template_id="r112-t2", argv_template=["echo", "hi"],
                                enabled=True, adapter_kind="claude_code")
            save_command_template(t, data_dir=Path(td))
            approve_managed_execution("ses-r112b", "r112-t2",
                                       adapter_id="adp-r112b",
                                       data_dir=Path(td))
            codes = validate_execution_approval("ses-r112b", "r112-t2",
                                                  data_dir=Path(td))
            assert "template_adapter_kind_mismatch" in codes

    def test_disabled_adapter_detected(self):
        """Disabled adapter → adapter_disabled code."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            _create_test_session(td, "ses-r112c", adapter_id="adp-r112c")
            adapters_dir = Path(td) / "main_builder_adapter" / "adapters"
            adapters_dir.mkdir(parents=True, exist_ok=True)
            import json
            json.dump({"adapter_id": "adp-r112c", "kind": "claude_code",
                        "enabled": False, "mode": "safe", "command_template_id": ""},
                       open(adapters_dir / "adp-r112c.json", "w"))
            t = CommandTemplate(template_id="r112-t3", argv_template=["echo", "hi"],
                                enabled=True, adapter_kind="claude_code")
            save_command_template(t, data_dir=Path(td))
            approve_managed_execution("ses-r112c", "r112-t3",
                                       adapter_id="adp-r112c",
                                       data_dir=Path(td))
            codes = validate_execution_approval("ses-r112c", "r112-t3",
                                                  data_dir=Path(td))
            assert "adapter_disabled" in codes


class TestR0113AutoBinding(unittest.TestCase):
    """R-0113: approve_managed_execution auto-binds from real session."""

    def test_auto_binds_package_id(self):
        """Approval omitting package_id auto-binds from real session."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            _create_test_session(td, "ses-r113", package_id="auto-pkg")
            t = CommandTemplate(template_id="r113-t", argv_template=["echo", "hi"],
                                enabled=True)
            save_command_template(t, data_dir=Path(td))
            approval = approve_managed_execution("ses-r113", "r113-t",
                                                   data_dir=Path(td))
            assert approval is not None
            assert approval.package_id == "auto-pkg"

    def test_auto_binds_adapter_id(self):
        """Approval omitting adapter_id auto-binds from real session."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            _create_test_session(td, "ses-r113b", adapter_id="auto-adp")
            t = CommandTemplate(template_id="r113-t", argv_template=["echo", "hi"],
                                enabled=True)
            save_command_template(t, data_dir=Path(td))
            approval = approve_managed_execution("ses-r113b", "r113-t",
                                                   data_dir=Path(td))
            assert approval is not None
            assert approval.adapter_id == "auto-adp"

    def test_explicit_binding_not_overridden(self):
        """Caller-provided binding fields are not overridden."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            _create_test_session(td, "ses-r113c", package_id="session-pkg",
                                  adapter_id="session-adp")
            t = CommandTemplate(template_id="r113-t", argv_template=["echo", "hi"],
                                enabled=True)
            save_command_template(t, data_dir=Path(td))
            approval = approve_managed_execution("ses-r113c", "r113-t",
                                                   package_id="explicit-pkg",
                                                   adapter_id="explicit-adp",
                                                   data_dir=Path(td))
            assert approval is not None
            assert approval.package_id == "explicit-pkg"
            assert approval.adapter_id == "explicit-adp"


class TestR0114ControlledExecution(unittest.TestCase):
    """R-0114: execution.run must not use generic may_execute_commands."""

    def test_execution_run_may_execute_false(self):
        from apps.cli.command_catalog import CATALOG
        for cmd in CATALOG:
            if cmd.command_id == "execution.run":
                assert cmd.may_execute_commands is False, \
                    "execution.run must not have may_execute_commands=True"
                assert cmd.action_class == "controlled_builder_execution"
                return
        self.fail("execution.run not found in CATALOG")

    def test_no_generic_execution_permission(self):
        """execution.run is controlled, not generic command execution."""
        from apps.cli.command_catalog import CATALOG
        for cmd in CATALOG:
            if cmd.command_id == "execution.run":
                assert cmd.action_class != "test_execution"
                assert cmd.action_class != "dev_helper"
                assert cmd.may_execute_commands is False


class TestR0115OutputRefEvent(unittest.TestCase):
    """R-0115: Output-ref-created event for dogfood replay."""

    def test_successful_run_emits_output_ref_event(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            _create_test_session(td, "ses-r115")
            t = CommandTemplate(template_id="r115-t", argv_template=["echo", "hi"],
                                enabled=True, requires_approval=False)
            save_command_template(t, data_dir=Path(td))
            result = run_managed_builder("ses-r115", template_id="r115-t",
                                          job_id="job-r115", data_dir=Path(td))
            assert result.status == ManagedExecutionStatus.COMPLETED
            events = list_execution_events(session_id="ses-r115", job_id="job-r115",
                                            data_dir=Path(td))
            kinds = [e.get("kind") for e in events]
            assert ExecutionEventKind.OUTPUT_REF_CREATED in kinds

    def test_completed_missing_output_ref_event_flagged(self):
        """Integrity flags completed run missing output_ref_created event."""
        events = [
            {"execution_id": "r115-e1", "kind": ExecutionEventKind.STARTED},
            {"execution_id": "r115-e1", "kind": ExecutionEventKind.COMPLETED},
        ]
        violations = audit_execution_result_safety(
            {"execution_id": "r115-e1", "status": "completed",
             "output_ref": "mbe/output/r115-e1.raw"},
            events=events)
        codes = [v["code"] for v in violations]
        assert "completed_missing_output_ref_event" in codes

    def test_completed_with_all_events_clean(self):
        """Completed run with all required events has no violations."""
        events = [
            {"execution_id": "r115-e2", "kind": ExecutionEventKind.STARTED},
            {"execution_id": "r115-e2", "kind": ExecutionEventKind.OUTPUT_REF_CREATED},
            {"execution_id": "r115-e2", "kind": ExecutionEventKind.COMPLETED},
        ]
        violations = audit_execution_result_safety(
            {"execution_id": "r115-e2", "status": "completed",
             "output_ref": "mbe/output/r115-e2.raw"},
            events=events)
        assert len(violations) == 0

    def test_debug_bundle_output_ref_event_present(self):
        """Debug bundle includes output_ref_event_present field."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            _create_test_session(td, "ses-r115b")
            t = CommandTemplate(template_id="r115-t2", argv_template=["echo", "hi"],
                                enabled=True, requires_approval=False)
            save_command_template(t, data_dir=Path(td))
            result = run_managed_builder("ses-r115b", template_id="r115-t2",
                                          data_dir=Path(td))
            bundle = build_debug_bundle(result.execution_id, data_dir=Path(td))
            assert bundle is not None
            assert "output_ref_event_present" in bundle
            assert bundle["output_ref_event_present"] is True

    def test_output_ref_created_in_all_event_kinds(self):
        """OUTPUT_REF_CREATED is in _ALL_EVENT_KINDS."""
        from packages.orchestration.managed_builder_execution import _ALL_EVENT_KINDS
        assert ExecutionEventKind.OUTPUT_REF_CREATED in _ALL_EVENT_KINDS

    def test_no_raw_output_in_event(self):
        """Output-ref event must not contain raw subprocess output."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            _create_test_session(td, "ses-r115c")
            t = CommandTemplate(template_id="r115-t3", argv_template=["echo", "secret_test_value"],
                                enabled=True, requires_approval=False)
            save_command_template(t, data_dir=Path(td))
            result = run_managed_builder("ses-r115c", template_id="r115-t3",
                                          job_id="job-r115c", data_dir=Path(td))
            events = list_execution_events(session_id="ses-r115c", job_id="job-r115c",
                                            data_dir=Path(td))
            ref_events = [e for e in events
                          if e.get("kind") == ExecutionEventKind.OUTPUT_REF_CREATED]
            assert len(ref_events) >= 1
            for e in ref_events:
                summary = e.get("safe_summary", "")
                assert "secret_test_value" not in summary


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


# ---------------------------------------------------------------------------
# Phase 2: Template enable/disable/update (Step 2506)
# ---------------------------------------------------------------------------


class TestTemplateEnableDisable(unittest.TestCase):

    def test_enable_default_claude_template(self):
        with tempfile.TemporaryDirectory() as td:
            ddir = Path(td)
            for t in default_command_templates():
                save_command_template(t, ddir)
            tmpl = enable_command_template("claude-code-repair-v0", ddir)
            assert tmpl is not None
            assert tmpl.enabled is True
            reloaded = get_command_template("claude-code-repair-v0", ddir)
            assert reloaded["enabled"] is True

    def test_disable_template(self):
        with tempfile.TemporaryDirectory() as td:
            ddir = Path(td)
            for t in default_command_templates():
                save_command_template(t, ddir)
            enable_command_template("claude-code-repair-v0", ddir)
            tmpl = disable_command_template("claude-code-repair-v0", ddir)
            assert tmpl is not None
            assert tmpl.enabled is False

    def test_enable_nonexistent_returns_none(self):
        with tempfile.TemporaryDirectory() as td:
            assert enable_command_template("nope", Path(td)) is None

    def test_update_timeout(self):
        with tempfile.TemporaryDirectory() as td:
            ddir = Path(td)
            for t in default_command_templates():
                save_command_template(t, ddir)
            tmpl = update_command_template("claude-code-repair-v0", timeout_seconds=120, data_dir=ddir)
            assert tmpl is not None
            assert tmpl.timeout_seconds == 120
            reloaded = get_command_template("claude-code-repair-v0", ddir)
            assert reloaded["timeout_seconds"] == 120

    def test_update_max_output_bytes(self):
        with tempfile.TemporaryDirectory() as td:
            ddir = Path(td)
            for t in default_command_templates():
                save_command_template(t, ddir)
            tmpl = update_command_template("claude-code-repair-v0", max_output_bytes=100000, data_dir=ddir)
            assert tmpl is not None
            assert tmpl.max_output_bytes == 100000

    def test_update_label(self):
        with tempfile.TemporaryDirectory() as td:
            ddir = Path(td)
            for t in default_command_templates():
                save_command_template(t, ddir)
            tmpl = update_command_template("claude-code-repair-v0", label="Custom label", data_dir=ddir)
            assert tmpl is not None
            assert tmpl.label == "Custom label"

    def test_update_nonexistent_returns_none(self):
        with tempfile.TemporaryDirectory() as td:
            assert update_command_template("nope", timeout_seconds=60, data_dir=Path(td)) is None


# ---------------------------------------------------------------------------
# Phase 3: Package-bound placeholder resolution (Step 2506)
# ---------------------------------------------------------------------------


class TestPackageBoundPlaceholders(unittest.TestCase):

    def _setup_session_with_package(self, ddir):
        """Create adapter, package, session for placeholder tests."""
        from packages.orchestration.main_builder_adapter import (
            BuilderAdapterKind,
            BuilderAdapterMode,
            BuilderAdapterSpec,
            build_builder_request_package,
            create_builder_session,
            save_builder_adapter_spec,
        )
        spec = BuilderAdapterSpec(
            adapter_id="fixture-v0",
            kind=BuilderAdapterKind.FIXTURE_BUILDER,
            enabled=True,
            mode=BuilderAdapterMode.FIXTURE_ONLY,
            requires_operator_approval=False,
        )
        save_builder_adapter_spec(spec, ddir)
        pkg = build_builder_request_package(
            "job-ph", adapter_id="fixture-v0",
            context_pack={"goal_summary": "Fix the auth bug"},
            data_dir=ddir,
        )
        session = create_builder_session(
            pkg.package_id, "fixture-v0", job_id="job-ph", data_dir=ddir,
        )
        return pkg, session

    def test_goal_summary_resolved_from_package(self):
        with tempfile.TemporaryDirectory() as td:
            ddir = Path(td)
            pkg, session = self._setup_session_with_package(ddir)
            tmpl = CommandTemplate(
                template_id="test-ph-tmpl",
                adapter_kind="fixture_builder",
                argv_template=["echo", "{goal_summary}"],
                allowed_placeholders=["goal_summary"],
                requires_approval=False,
                enabled=True,
            )
            save_command_template(tmpl, ddir)
            result = run_managed_builder(
                session.session_id, template_id="test-ph-tmpl", data_dir=ddir,
            )
            assert result.status == ManagedExecutionStatus.COMPLETED
            assert "Fix the auth bug" in result.safe_summary

    def test_missing_package_blocks_placeholder(self):
        with tempfile.TemporaryDirectory() as td:
            ddir = Path(td)
            from packages.orchestration.main_builder_adapter import (
                BuilderAdapterKind,
                BuilderAdapterMode,
                BuilderAdapterSpec,
                create_builder_session,
                save_builder_adapter_spec,
            )
            spec = BuilderAdapterSpec(
                adapter_id="fixture-v0",
                kind=BuilderAdapterKind.FIXTURE_BUILDER,
                enabled=True,
                mode=BuilderAdapterMode.FIXTURE_ONLY,
                requires_operator_approval=False,
            )
            save_builder_adapter_spec(spec, ddir)
            session = create_builder_session(
                "fake-pkg", "fixture-v0", job_id="job-nopkg", data_dir=ddir,
            )
            tmpl = CommandTemplate(
                template_id="test-nopkg-tmpl",
                adapter_kind="fixture_builder",
                argv_template=["echo", "{goal_summary}"],
                allowed_placeholders=["goal_summary"],
                requires_approval=False,
                enabled=True,
            )
            save_command_template(tmpl, ddir)
            result = run_managed_builder(
                session.session_id, template_id="test-nopkg-tmpl", data_dir=ddir,
            )
            assert result.status == ManagedExecutionStatus.BLOCKED
            assert "goal_summary" in str(result.blocking_reasons)


# ---------------------------------------------------------------------------
# Phase 6: Fixture end-to-end path (Step 2506)
# ---------------------------------------------------------------------------


class TestFixtureEndToEnd(unittest.TestCase):

    def test_full_flow_fixture(self):
        """E2E: adapter → package → session → template → approve → run → output ref → intake."""
        with tempfile.TemporaryDirectory() as td:
            ddir = Path(td)
            from packages.orchestration.main_builder_adapter import (
                BuilderAdapterKind,
                BuilderAdapterMode,
                BuilderAdapterSpec,
                BuilderSessionStatus,
                build_builder_request_package,
                create_builder_session,
                load_builder_session,
                record_builder_session_intake_complete,
                record_builder_session_output,
                save_builder_adapter_spec,
            )
            # 1. Enable fixture adapter.
            spec = BuilderAdapterSpec(
                adapter_id="fixture-v0",
                kind=BuilderAdapterKind.FIXTURE_BUILDER,
                enabled=True,
                mode=BuilderAdapterMode.FIXTURE_ONLY,
                requires_operator_approval=False,
            )
            save_builder_adapter_spec(spec, ddir)

            # 2. Create request package.
            pkg = build_builder_request_package(
                "job-e2e", adapter_id="fixture-v0",
                context_pack={"goal_summary": "E2E test goal"},
                data_dir=ddir,
            )
            assert pkg.package_id

            # 3. Create session.
            session = create_builder_session(
                pkg.package_id, "fixture-v0", job_id="job-e2e", data_dir=ddir,
            )
            assert session.session_id

            # 4. Enable safe fixture command template.
            tmpl = CommandTemplate(
                template_id="e2e-fixture-tmpl",
                adapter_kind="fixture_builder",
                argv_template=["echo", "fixture-output"],
                allowed_placeholders=[],
                requires_approval=False,
                enabled=True,
            )
            save_command_template(tmpl, ddir)

            # 5-6. Run execution (no approval needed for fixture).
            result = run_managed_builder(
                session.session_id, template_id="e2e-fixture-tmpl",
                job_id="job-e2e", data_dir=ddir,
            )
            assert result.status == ManagedExecutionStatus.COMPLETED
            assert result.output_ref

            # 7. Record output ref.
            updated = record_builder_session_output(
                session.session_id, candidate_artifact_ref=result.output_ref,
                data_dir=ddir,
            )
            assert updated is not None
            assert updated.status == BuilderSessionStatus.CANDIDATE_RECEIVED

            # 8. Intake.
            intake = record_builder_session_intake_complete(
                session.session_id, sandbox_submission_id="e2e-sandbox",
                data_dir=ddir,
            )
            assert intake is not None
            assert intake.status == BuilderSessionStatus.COMPLETED_INTAKE_ONLY

            # 9. Verify session.
            final = load_builder_session(session.session_id, data_dir=ddir)
            assert final is not None
            assert final.candidate_artifact_ref

            # 10. Debug bundle.
            bundle = build_debug_bundle(result.execution_id, data_dir=ddir)
            assert bundle is not None
            assert bundle["status"] == "completed"
            assert bundle["output_ref_present"] is True


if __name__ == "__main__":
    unittest.main()
