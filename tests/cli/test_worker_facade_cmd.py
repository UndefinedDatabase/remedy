"""Tests for worker facade + mission command facade CLI handlers."""

from __future__ import annotations

import argparse
import json
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Alias registry
# ---------------------------------------------------------------------------


class TestWorkerAliasRegistry:
    def test_known_aliases(self):
        from apps.cli.commands.worker_facade_cmd import _WORKER_ALIASES
        assert "claude" in _WORKER_ALIASES
        assert "claude-code" in _WORKER_ALIASES
        assert "fixture" in _WORKER_ALIASES
        assert "generic" in _WORKER_ALIASES

    def test_claude_alias_fields(self):
        from apps.cli.commands.worker_facade_cmd import _WORKER_ALIASES
        c = _WORKER_ALIASES["claude"]
        assert c["adapter_id"] == "claude-code-v0"
        assert c["template_id"] == "claude-code-repair-v0"
        assert c["kind"] == "claude_code"

    def test_resolve_case_insensitive(self):
        from apps.cli.commands.worker_facade_cmd import _resolve_alias
        assert _resolve_alias("Claude") is not None
        assert _resolve_alias("CLAUDE") is not None
        assert _resolve_alias(" claude ") is not None

    def test_resolve_unknown_returns_none(self):
        from apps.cli.commands.worker_facade_cmd import _resolve_alias
        assert _resolve_alias("nonexistent") is None


# ---------------------------------------------------------------------------
# Handler registry
# ---------------------------------------------------------------------------


class TestHandlerRegistry:
    def test_all_handlers_present(self):
        from apps.cli.commands.worker_facade_cmd import COMMAND_HANDLERS
        expected = {"worker.doctor", "worker.add", "worker.disable",
                    "mission.run", "mission.report", "doctor.core",
                    "approval.policy-list", "approval.policy-show",
                    "approval.policy-enable", "approval.policy-disable",
                    "approval.policy-evaluate", "approval.policy-grant"}
        assert set(COMMAND_HANDLERS.keys()) == expected

    def test_all_handlers_callable(self):
        from apps.cli.commands.worker_facade_cmd import COMMAND_HANDLERS
        for key, fn in COMMAND_HANDLERS.items():
            assert callable(fn), f"{key} handler not callable"


# ---------------------------------------------------------------------------
# Catalog + contract integration
# ---------------------------------------------------------------------------


class TestCatalogIntegration:
    def test_mission_group_exists(self):
        from apps.cli.command_catalog import GROUPS
        assert "mission" in GROUPS

    def test_worker_facade_commands_in_catalog(self):
        from apps.cli.command_catalog import CATALOG
        ids = {c.command_id for c in CATALOG}
        for cmd_id in ("worker.doctor", "worker.add", "worker.disable",
                       "mission.run", "mission.report"):
            assert cmd_id in ids, f"{cmd_id} missing from catalog"

    def test_mission_commands_in_catalog(self):
        from apps.cli.command_catalog import CATALOG
        mission_cmds = [c for c in CATALOG if c.group_id == "mission"]
        assert len(mission_cmds) == 2
        ids = {c.command_id for c in mission_cmds}
        assert ids == {"mission.run", "mission.report"}

    def test_all_facade_commands_have_handlers(self):
        from apps.cli.command_catalog import CATALOG
        from apps.cli.commands.worker_facade_cmd import COMMAND_HANDLERS
        facade_cmds = [c for c in CATALOG
                       if c.command_id in COMMAND_HANDLERS]
        assert len(facade_cmds) == 12
        for cmd in facade_cmds:
            assert cmd.command_id in COMMAND_HANDLERS


class TestContractActions:
    def test_facade_actions_exist(self):
        from packages.orchestration.run_contract import ContractAction
        for name in ("WORKER_DOCTOR", "WORKER_ADD", "WORKER_DISABLE",
                     "MISSION_RUN", "MISSION_REPORT"):
            assert hasattr(ContractAction, name)

    def test_facade_actions_in_defaults(self):
        from packages.orchestration.run_contract import (
            _DEFAULT_ALLOWED_ACTIONS,
            ContractAction,
        )
        for name in ("WORKER_DOCTOR", "WORKER_ADD", "WORKER_DISABLE",
                     "MISSION_RUN", "MISSION_REPORT"):
            val = getattr(ContractAction, name)
            assert val in _DEFAULT_ALLOWED_ACTIONS, f"{name} not in defaults"


# ---------------------------------------------------------------------------
# worker doctor
# ---------------------------------------------------------------------------


def _ns(**kwargs) -> argparse.Namespace:
    return argparse.Namespace(**kwargs)


_ADAPTER_PATCH = "packages.orchestration.main_builder_adapter.get_builder_adapter_spec"
_TMPL_PATCH = "packages.orchestration.managed_builder_execution.get_command_template"
_SAVE_ADAPTER = "packages.orchestration.main_builder_adapter.save_builder_adapter_spec"
_ENABLE_TMPL = "packages.orchestration.managed_builder_execution.enable_command_template"
_DISABLE_TMPL = "packages.orchestration.managed_builder_execution.disable_command_template"
_MISSION_LOOP = "packages.orchestration.dogfood_run.run_mission_loop"
_MORNING_REPORT = "packages.orchestration.dogfood_run.build_mission_morning_report"


class TestWorkerDoctor:
    @patch(_TMPL_PATCH)
    @patch(_ADAPTER_PATCH)
    @patch("shutil.which", return_value="/usr/bin/claude")
    def test_doctor_all_ready(self, mock_which, mock_adapter, mock_tmpl, capsys):
        mock_adapter.return_value = {"enabled": True, "mode": "operator_launched",
                                     "adapter_id": "claude-code-v0"}
        mock_tmpl.return_value = {"enabled": True, "template_id": "claude-code-repair-v0"}
        from apps.cli.commands.worker_facade_cmd import _cmd_worker_doctor
        _cmd_worker_doctor(_ns(worker="claude", json=True))
        out = json.loads(capsys.readouterr().out)
        assert out["ready"] is True
        assert out["blockers"] == []

    @patch(_TMPL_PATCH)
    @patch(_ADAPTER_PATCH)
    @patch("shutil.which", return_value=None)
    def test_doctor_binary_missing(self, mock_which, mock_adapter, mock_tmpl, capsys):
        mock_adapter.return_value = {"enabled": True, "mode": "operator_launched",
                                     "adapter_id": "claude-code-v0"}
        mock_tmpl.return_value = {"enabled": True, "template_id": "claude-code-repair-v0"}
        from apps.cli.commands.worker_facade_cmd import _cmd_worker_doctor
        _cmd_worker_doctor(_ns(worker="claude", json=True))
        out = json.loads(capsys.readouterr().out)
        assert out["ready"] is False
        assert any("binary" in b.lower() for b in out["blockers"])

    @patch(_TMPL_PATCH)
    @patch(_ADAPTER_PATCH)
    @patch("shutil.which", return_value="/usr/bin/claude")
    def test_doctor_adapter_disabled(self, mock_which, mock_adapter, mock_tmpl, capsys):
        mock_adapter.return_value = {"enabled": False, "mode": "disabled",
                                     "adapter_id": "claude-code-v0"}
        mock_tmpl.return_value = {"enabled": True, "template_id": "claude-code-repair-v0"}
        from apps.cli.commands.worker_facade_cmd import _cmd_worker_doctor
        _cmd_worker_doctor(_ns(worker="claude", json=True))
        out = json.loads(capsys.readouterr().out)
        assert out["ready"] is False
        assert any("adapter" in b.lower() for b in out["blockers"])
        assert "next_recommended_command" in out

    def test_doctor_unknown_worker(self):
        from apps.cli.commands.worker_facade_cmd import _cmd_worker_doctor
        with pytest.raises(SystemExit):
            _cmd_worker_doctor(_ns(worker="nonexistent", json=True))

    @patch(_TMPL_PATCH)
    @patch(_ADAPTER_PATCH)
    @patch("shutil.which", return_value="/usr/bin/claude")
    def test_doctor_text_output(self, mock_which, mock_adapter, mock_tmpl, capsys):
        mock_adapter.return_value = {"enabled": True, "mode": "operator_launched",
                                     "adapter_id": "claude-code-v0"}
        mock_tmpl.return_value = {"enabled": True, "template_id": "claude-code-repair-v0"}
        from apps.cli.commands.worker_facade_cmd import _cmd_worker_doctor
        _cmd_worker_doctor(_ns(worker="claude", json=False))
        out = capsys.readouterr().out
        assert "Claude Code" in out
        assert "ready: True" in out


# ---------------------------------------------------------------------------
# worker add
# ---------------------------------------------------------------------------


class TestWorkerAdd:
    @patch(_ENABLE_TMPL)
    @patch(_TMPL_PATCH)
    @patch(_SAVE_ADAPTER)
    @patch(_ADAPTER_PATCH)
    def test_add_enables_both(self, mock_get_adapter, mock_save, mock_get_tmpl,
                              mock_enable_tmpl, capsys):
        mock_get_adapter.return_value = {"enabled": False, "mode": "disabled",
                                         "adapter_id": "claude-code-v0",
                                         "kind": "claude_code"}
        mock_save.return_value = True
        mock_get_tmpl.return_value = {"enabled": False, "template_id": "claude-code-repair-v0"}
        mock_enable_tmpl.return_value = {"enabled": True}

        from apps.cli.commands.worker_facade_cmd import _cmd_worker_add
        _cmd_worker_add(_ns(worker="claude", json=True))
        out = json.loads(capsys.readouterr().out)
        assert out["ready"] is True
        assert out["adapter_enabled"] is True
        assert out["template_enabled"] is True
        assert "quickstart" in out
        assert len(out["quickstart"]) > 0
        assert "advanced" in out

    @patch(_ENABLE_TMPL)
    @patch(_TMPL_PATCH)
    @patch(_SAVE_ADAPTER)
    @patch(_ADAPTER_PATCH)
    def test_add_already_enabled(self, mock_get_adapter, mock_save, mock_get_tmpl,
                                  mock_enable_tmpl, capsys):
        mock_get_adapter.return_value = {"enabled": True, "mode": "operator_launched",
                                         "adapter_id": "claude-code-v0",
                                         "kind": "claude_code"}
        mock_get_tmpl.return_value = {"enabled": True, "template_id": "claude-code-repair-v0"}

        from apps.cli.commands.worker_facade_cmd import _cmd_worker_add
        _cmd_worker_add(_ns(worker="claude", json=True))
        out = json.loads(capsys.readouterr().out)
        assert out["ready"] is True
        mock_save.assert_not_called()
        mock_enable_tmpl.assert_not_called()

    def test_add_unknown_worker(self):
        from apps.cli.commands.worker_facade_cmd import _cmd_worker_add
        with pytest.raises(SystemExit):
            _cmd_worker_add(_ns(worker="nope", json=True))


# ---------------------------------------------------------------------------
# worker disable
# ---------------------------------------------------------------------------


class TestWorkerDisable:
    @patch(_DISABLE_TMPL)
    @patch(_SAVE_ADAPTER)
    @patch(_ADAPTER_PATCH)
    def test_disable_both(self, mock_get_adapter, mock_save, mock_disable_tmpl, capsys):
        mock_get_adapter.return_value = {"enabled": True, "mode": "operator_launched",
                                         "adapter_id": "claude-code-v0",
                                         "kind": "claude_code"}
        mock_save.return_value = True
        mock_disable_tmpl.return_value = {"enabled": False}

        from apps.cli.commands.worker_facade_cmd import _cmd_worker_disable
        _cmd_worker_disable(_ns(worker="claude", json=True))
        out = json.loads(capsys.readouterr().out)
        assert out["adapter_disabled"] is True
        assert out["template_disabled"] is True

    def test_disable_unknown_worker(self):
        from apps.cli.commands.worker_facade_cmd import _cmd_worker_disable
        with pytest.raises(SystemExit):
            _cmd_worker_disable(_ns(worker="nope", json=True))


# ---------------------------------------------------------------------------
# mission run facade
# ---------------------------------------------------------------------------


class TestMissionRun:
    @patch(_MISSION_LOOP)
    def test_run_calls_loop(self, mock_loop, capsys):
        result = MagicMock()
        result.run_id = "r-1"
        result.steps_attempted = 3
        result.final_status = "satisfied"
        result.stop_reason = "mission_satisfied"
        result.next_safe_action = None
        result.blocking_reasons = []
        result.to_dict.return_value = {
            "run_id": "r-1", "steps_attempted": 3,
            "final_status": "satisfied", "stop_reason": "mission_satisfied",
        }
        mock_loop.return_value = result

        from apps.cli.commands.worker_facade_cmd import _cmd_mission_run
        _cmd_mission_run(_ns(run_id="r-1", job_id="j-1", max_steps=5,
                             max_seconds=60, json=True))
        out = json.loads(capsys.readouterr().out)
        assert out["run_id"] == "r-1"
        assert out["stop_reason"] == "mission_satisfied"
        mock_loop.assert_called_once_with(
            "r-1", job_id="j-1", max_steps=5, max_seconds=60)

    def test_run_no_run_id(self):
        from apps.cli.commands.worker_facade_cmd import _cmd_mission_run
        with pytest.raises(SystemExit):
            _cmd_mission_run(_ns(run_id="", job_id="", max_steps=10,
                                 max_seconds=300, json=True))


# ---------------------------------------------------------------------------
# mission report facade
# ---------------------------------------------------------------------------


class TestMissionReport:
    @patch(_MORNING_REPORT)
    def test_report_calls_builder(self, mock_report, capsys):
        rpt = MagicMock()
        rpt.run_id = "r-1"
        rpt.mission_status = "in_progress"
        rpt.final_status = "running"
        rpt.stopped_because = None
        rpt.steps_completed = 5
        rpt.next_safe_action = "step"
        rpt.operator_summary = "All systems go."
        rpt.to_dict.return_value = {
            "run_id": "r-1", "mission_status": "in_progress",
            "steps_completed": 5, "operator_summary": "All systems go.",
        }
        mock_report.return_value = rpt

        from apps.cli.commands.worker_facade_cmd import _cmd_mission_report
        _cmd_mission_report(_ns(run_id="r-1", job_id="j-1", json=True))
        out = json.loads(capsys.readouterr().out)
        assert out["run_id"] == "r-1"
        assert out["operator_summary"] == "All systems go."
        mock_report.assert_called_once_with("r-1", job_id="j-1")

    def test_report_no_run_id(self):
        from apps.cli.commands.worker_facade_cmd import _cmd_mission_report
        with pytest.raises(SystemExit):
            _cmd_mission_report(_ns(run_id="", job_id="", json=True))


# ---------------------------------------------------------------------------
# collect_all_handlers includes facade
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# doctor core
# ---------------------------------------------------------------------------


class TestDoctorCore:
    def test_core_all_ready(self, capsys):
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core
        _cmd_doctor_core(_ns(json=True))
        out = json.loads(capsys.readouterr().out)
        assert out["ready"] is True
        assert out["blockers"] == []
        check_names = {c["check"] for c in out["checks"]}
        assert "worker_facade" in check_names
        assert "command_catalog" in check_names
        assert "run_contract" in check_names
        assert "mission_facade" in check_names
        assert "fast_test_lane" in check_names

    def test_core_error_messages_safe(self, capsys):
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core
        _cmd_doctor_core(_ns(json=True))
        out = json.loads(capsys.readouterr().out)
        raw = json.dumps(out)
        assert "/home/" not in raw, "Doctor core must not leak absolute home paths"
        assert "/root/" not in raw, "Doctor core must not leak root paths"
        for check in out["checks"]:
            detail = str(check.get("detail", ""))
            assert len(detail) <= 200, f"Detail too long: {detail[:50]}..."

    def test_core_text_output(self, capsys):
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core
        _cmd_doctor_core(_ns(json=False))
        out = capsys.readouterr().out
        assert "Core Product Spine" in out
        assert "READY" in out


class TestDoctorCoreSafeErr:
    def test_private_paths_redacted(self, monkeypatch, capsys):
        import importlib
        orig = importlib.import_module

        def _boom(name, *a, **kw):
            if name == "apps.cli.commands.worker_facade_cmd":
                return orig(name, *a, **kw)
            if name == "packages.orchestration.run_contract":
                raise ImportError(
                    "No module at /home/alice/secret-project/packages/orchestration/run_contract"
                )
            return orig(name, *a, **kw)

        monkeypatch.setattr(importlib, "import_module", _boom)
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core
        _cmd_doctor_core(_ns(json=True))
        out = json.loads(capsys.readouterr().out)
        raw = json.dumps(out)
        assert "/home/" not in raw
        assert "alice" not in raw

    def test_secrets_redacted(self, monkeypatch, capsys):
        import importlib
        orig = importlib.import_module

        def _boom(name, *a, **kw):
            if name == "apps.cli.commands.worker_facade_cmd":
                return orig(name, *a, **kw)
            if name == "packages.orchestration.config":
                raise ImportError("Failed: api_key=sk-live-abc123def token=tok_xyz")
            return orig(name, *a, **kw)

        monkeypatch.setattr(importlib, "import_module", _boom)
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core
        _cmd_doctor_core(_ns(json=True))
        out = json.loads(capsys.readouterr().out)
        raw = json.dumps(out)
        assert "sk-live" not in raw
        assert "tok_xyz" not in raw
        assert "api_key=***" in raw

    def test_mnt_tmp_users_redacted(self, monkeypatch, capsys):
        import importlib
        orig = importlib.import_module

        def _boom(name, *a, **kw):
            if name == "apps.cli.commands.worker_facade_cmd":
                return orig(name, *a, **kw)
            if name == "packages.orchestration.review_bundle":
                raise ImportError(
                    "Error at /mnt/data/x and /tmp/build/y and /Users/bob/.config/z"
                )
            return orig(name, *a, **kw)

        monkeypatch.setattr(importlib, "import_module", _boom)
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core
        _cmd_doctor_core(_ns(json=True))
        out = json.loads(capsys.readouterr().out)
        raw = json.dumps(out)
        assert "/mnt/" not in raw
        assert "/tmp/" not in raw
        assert "/Users/" not in raw


class TestCollectHandlers:
    def test_facade_in_collected(self):
        from apps.cli.commands import collect_all_handlers
        handlers = collect_all_handlers()
        for key in ("worker.doctor", "worker.add", "worker.disable",
                    "mission.run", "mission.report", "doctor.core",
                    "approval.policy-list", "approval.policy-show",
                    "approval.policy-enable", "approval.policy-disable",
                    "approval.policy-evaluate", "approval.policy-grant"):
            assert key in handlers, f"{key} missing from collect_all_handlers"


# ---------------------------------------------------------------------------
# Approval CLI handlers (Steps 2781-2785)
# ---------------------------------------------------------------------------

_POLICY_LIST = "packages.orchestration.execution_approval_policy.list_execution_approval_policies"
_POLICY_LOAD = "packages.orchestration.execution_approval_policy.load_execution_approval_policy"
_POLICY_SAVE = "packages.orchestration.execution_approval_policy.save_execution_approval_policy"
_POLICY_EVAL = "packages.orchestration.execution_approval_policy.evaluate_execution_approval_policy"
_POLICY_GRANT = "packages.orchestration.execution_approval_policy.create_policy_granted_execution_approval"


class TestApprovalPolicyList:
    @patch(_POLICY_LIST)
    def test_list_json(self, mock_list, capsys):
        mock_list.return_value = [
            {"policy_id": "test-1", "enabled": True, "label": "Test"},
        ]
        from apps.cli.commands.worker_facade_cmd import _cmd_approval_policy_list
        _cmd_approval_policy_list(_ns(json=True))
        out = json.loads(capsys.readouterr().out)
        assert out["count"] == 1
        assert out["policies"][0]["policy_id"] == "test-1"

    @patch(_POLICY_LIST)
    def test_list_text(self, mock_list, capsys):
        mock_list.return_value = [
            {"policy_id": "fixture-echo-v0", "enabled": False, "label": "Fixture"},
        ]
        from apps.cli.commands.worker_facade_cmd import _cmd_approval_policy_list
        _cmd_approval_policy_list(_ns(json=False))
        out = capsys.readouterr().out
        assert "fixture-echo-v0" in out
        assert "disabled" in out


class TestApprovalPolicyShow:
    @patch(_POLICY_LOAD)
    def test_show_json(self, mock_load, capsys):
        from packages.orchestration.execution_approval_policy import ExecutionApprovalPolicy
        mock_load.return_value = ExecutionApprovalPolicy(
            policy_id="test-1", label="Test", enabled=True,
            adapter_id="a-1", template_id="t-1",
        )
        from apps.cli.commands.worker_facade_cmd import _cmd_approval_policy_show
        _cmd_approval_policy_show(_ns(policy_id="test-1", json=True))
        out = json.loads(capsys.readouterr().out)
        assert out["policy_id"] == "test-1"
        assert out["enabled"] is True

    @patch(_POLICY_LOAD)
    def test_show_not_found(self, mock_load):
        mock_load.return_value = None
        from apps.cli.commands.worker_facade_cmd import _cmd_approval_policy_show
        with pytest.raises(SystemExit):
            _cmd_approval_policy_show(_ns(policy_id="nonexistent", json=True))

    def test_show_no_id(self):
        from apps.cli.commands.worker_facade_cmd import _cmd_approval_policy_show
        with pytest.raises(SystemExit):
            _cmd_approval_policy_show(_ns(policy_id="", json=True))


class TestApprovalPolicyEnable:
    @patch(_POLICY_SAVE, return_value=True)
    @patch(_POLICY_LOAD)
    def test_enable_fixture_json(self, mock_load, mock_save, capsys):
        from packages.orchestration.execution_approval_policy import ExecutionApprovalPolicy
        mock_load.return_value = ExecutionApprovalPolicy(
            policy_id="fixture-echo-v0", label="Fixture",
            requires_fixture_only=True,
        )
        from apps.cli.commands.worker_facade_cmd import _cmd_approval_policy_enable
        _cmd_approval_policy_enable(_ns(
            policy_id="fixture-echo-v0", json=True, confirm_real_provider=False,
        ))
        out = json.loads(capsys.readouterr().out)
        assert out["enabled"] is True

    @patch(_POLICY_LOAD)
    def test_enable_real_without_confirm_exits(self, mock_load):
        from packages.orchestration.execution_approval_policy import ExecutionApprovalPolicy
        mock_load.return_value = ExecutionApprovalPolicy(
            policy_id="real-1", label="Real",
            requires_fixture_only=False, allow_real_provider=False,
        )
        from apps.cli.commands.worker_facade_cmd import _cmd_approval_policy_enable
        with pytest.raises(SystemExit):
            _cmd_approval_policy_enable(_ns(
                policy_id="real-1", json=True, confirm_real_provider=False,
            ))


class TestApprovalPolicyEnableConfirmRealProvider:
    @patch(_POLICY_SAVE, return_value=True)
    @patch(_POLICY_LOAD)
    def test_enable_real_with_confirm_sets_fields(self, mock_load, mock_save, capsys):
        from packages.orchestration.execution_approval_policy import ExecutionApprovalPolicy
        mock_load.return_value = ExecutionApprovalPolicy(
            policy_id="real-1", label="Real",
            requires_fixture_only=False, allow_real_provider=False,
        )
        from apps.cli.commands.worker_facade_cmd import _cmd_approval_policy_enable
        _cmd_approval_policy_enable(_ns(
            policy_id="real-1", json=True, confirm_real_provider=True,
        ))
        saved_pol = mock_save.call_args[0][0]
        assert saved_pol.allow_real_provider is True
        assert saved_pol.confirmed_by_operator == "cli_operator"
        assert saved_pol.confirmed_real_provider_at is not None
        assert saved_pol.real_provider_confirmation_reason is not None
        out = json.loads(capsys.readouterr().out)
        assert out["enabled"] is True
        assert out["allow_real_provider"] is True


class TestApprovalPolicyDisable:
    @patch(_POLICY_SAVE, return_value=True)
    @patch(_POLICY_LOAD)
    def test_disable_json(self, mock_load, mock_save, capsys):
        from packages.orchestration.execution_approval_policy import ExecutionApprovalPolicy
        mock_load.return_value = ExecutionApprovalPolicy(
            policy_id="test-1", label="Test", enabled=True,
        )
        from apps.cli.commands.worker_facade_cmd import _cmd_approval_policy_disable
        _cmd_approval_policy_disable(_ns(policy_id="test-1", json=True))
        out = json.loads(capsys.readouterr().out)
        assert out["disabled"] is True

    @patch(_POLICY_LOAD)
    def test_disable_not_found(self, mock_load):
        mock_load.return_value = None
        from apps.cli.commands.worker_facade_cmd import _cmd_approval_policy_disable
        with pytest.raises(SystemExit):
            _cmd_approval_policy_disable(_ns(policy_id="nonexistent", json=True))


class TestApprovalPolicyEvaluate:
    @patch(_POLICY_EVAL)
    def test_evaluate_json(self, mock_eval, capsys):
        from packages.orchestration.execution_approval_policy import (
            ExecutionApprovalPolicyDecision,
            PolicyDecisionCode,
        )
        mock_eval.return_value = ExecutionApprovalPolicyDecision(
            allowed=False,
            decision_code=PolicyDecisionCode.NO_MATCHING_POLICY,
            reason="No enabled policies",
        )
        from apps.cli.commands.worker_facade_cmd import _cmd_approval_policy_evaluate
        _cmd_approval_policy_evaluate(_ns(
            session_id="ses-001", template_id="tmpl-001", json=True,
        ))
        out = json.loads(capsys.readouterr().out)
        assert out["allowed"] is False
        assert out["decision_code"] == "no_matching_policy"

    def test_evaluate_no_session(self):
        from apps.cli.commands.worker_facade_cmd import _cmd_approval_policy_evaluate
        with pytest.raises(SystemExit):
            _cmd_approval_policy_evaluate(_ns(
                session_id="", template_id="tmpl-001", json=True,
            ))

    def test_evaluate_no_template(self):
        from apps.cli.commands.worker_facade_cmd import _cmd_approval_policy_evaluate
        with pytest.raises(SystemExit):
            _cmd_approval_policy_evaluate(_ns(
                session_id="ses-001", template_id="", json=True,
            ))


class TestApprovalPolicyGrant:
    @patch(_POLICY_GRANT)
    def test_grant_allowed_json(self, mock_grant, capsys):
        mock_grant.return_value = {
            "granted": True,
            "approval_id": "apr-001",
            "decision": {"decision_code": "allowed"},
        }
        from apps.cli.commands.worker_facade_cmd import _cmd_approval_policy_grant
        _cmd_approval_policy_grant(_ns(
            session_id="ses-001", template_id="tmpl-001", json=True,
        ))
        out = json.loads(capsys.readouterr().out)
        assert out["granted"] is True
        assert out["approval_id"] == "apr-001"

    @patch(_POLICY_GRANT)
    def test_grant_denied_text(self, mock_grant, capsys):
        mock_grant.return_value = {
            "granted": False,
            "decision": {"decision_code": "no_matching_policy", "reason": "none"},
        }
        from apps.cli.commands.worker_facade_cmd import _cmd_approval_policy_grant
        _cmd_approval_policy_grant(_ns(
            session_id="ses-001", template_id="tmpl-001", json=False,
        ))
        out = capsys.readouterr().out
        assert "Denied" in out

    def test_grant_no_session(self):
        from apps.cli.commands.worker_facade_cmd import _cmd_approval_policy_grant
        with pytest.raises(SystemExit):
            _cmd_approval_policy_grant(_ns(
                session_id="", template_id="tmpl-001", json=True,
            ))
