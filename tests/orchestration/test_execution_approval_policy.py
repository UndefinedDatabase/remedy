"""Tests for execution approval policy — model, storage, evaluation, grant."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

from packages.orchestration.execution_approval_policy import (
    _ALL_DECISION_CODES,
    ExecutionApprovalPolicy,
    ExecutionApprovalPolicyDecision,
    PolicyDecisionCode,
    create_policy_granted_execution_approval,
    default_policies,
    evaluate_execution_approval_policy,
    execution_approval_policy_integrity,
    execution_approval_policy_summary,
    list_execution_approval_policies,
    load_execution_approval_policy,
    save_execution_approval_policy,
)

# ---------------------------------------------------------------------------
# Model / export tests (Step 2766)
# ---------------------------------------------------------------------------


class TestPolicyModel:
    def test_default_fields(self):
        p = ExecutionApprovalPolicy()
        assert p.enabled is False
        assert p.allow_real_provider is False
        assert p.requires_fixture_only is False
        assert p.max_uses == 0
        assert p.uses_consumed == 0

    def test_roundtrip(self):
        p = ExecutionApprovalPolicy(
            policy_id="test-1", label="Test", enabled=True,
            adapter_id="a-1", template_id="t-1",
            max_timeout_seconds=120, max_output_bytes=1024,
            max_uses=5, uses_consumed=2,
        )
        d = p.to_dict()
        p2 = ExecutionApprovalPolicy.from_dict(d)
        assert p2.policy_id == "test-1"
        assert p2.enabled is True
        assert p2.max_uses == 5
        assert p2.uses_consumed == 2

    def test_caps_clamped(self):
        p = ExecutionApprovalPolicy(
            max_timeout_seconds=9999, max_output_bytes=999_999_999,
            max_estimated_tokens=999_999_999,
        )
        d = p.to_dict()
        assert d["max_timeout_seconds"] <= 600
        assert d["max_output_bytes"] <= 256 * 1024
        assert d["max_estimated_tokens"] <= 500_000

    def test_safe_export_no_secrets(self):
        p = ExecutionApprovalPolicy(
            policy_id="x", label="Test",
            reason="api_key=sk-live-test123 is set",
            notes="password=hunter2 exposed",
        )
        d = p.to_dict()
        assert "sk-live" not in d["reason"]
        assert "hunter2" not in d["notes"]
        assert "api_key=***" in d["reason"]
        assert "password=***" in d["notes"]

    def test_safe_export_no_paths(self):
        p = ExecutionApprovalPolicy(
            reason="Error at /home/alice/project/src",
            notes="Built from /Users/bob/.config/remedy",
        )
        d = p.to_dict()
        assert "/home/alice" not in d["reason"]
        assert "/Users/bob" not in d["notes"]

    def test_uses_non_negative(self):
        p = ExecutionApprovalPolicy.from_dict({"uses_consumed": -5, "max_uses": -3})
        assert p.uses_consumed == 0
        assert p.max_uses == 0


class TestDecisionModel:
    def test_default_denied(self):
        d = ExecutionApprovalPolicyDecision()
        assert d.allowed is False
        assert d.required_manual_approval is True

    def test_to_dict_safe(self):
        d = ExecutionApprovalPolicyDecision(
            reason="Failed at /home/user/path: api_key=sk-test",
        )
        out = d.to_dict()
        assert "/home/" not in out["reason"]
        assert "sk-test" not in out["reason"]

    def test_all_decision_codes_present(self):
        assert len(_ALL_DECISION_CODES) >= 20
        assert PolicyDecisionCode.ALLOWED in _ALL_DECISION_CODES
        assert PolicyDecisionCode.POLICY_DISABLED in _ALL_DECISION_CODES
        assert PolicyDecisionCode.REAL_PROVIDER_NOT_ALLOWED in _ALL_DECISION_CODES


# ---------------------------------------------------------------------------
# Storage tests (Step 2767)
# ---------------------------------------------------------------------------


class TestPolicyStorage:
    def test_save_load_roundtrip(self, tmp_path):
        p = ExecutionApprovalPolicy(
            policy_id="test-save", label="Save test", enabled=True,
            adapter_id="a-1", template_id="t-1",
        )
        assert save_execution_approval_policy(p, tmp_path)
        loaded = load_execution_approval_policy("test-save", tmp_path)
        assert loaded is not None
        assert loaded.policy_id == "test-save"
        assert loaded.enabled is True

    def test_save_rejects_empty_id(self, tmp_path):
        p = ExecutionApprovalPolicy(label="No ID")
        assert save_execution_approval_policy(p, tmp_path) is False

    def test_save_rejects_secrets(self, tmp_path):
        p = ExecutionApprovalPolicy(
            policy_id="secret-test", label="sk-live-abc123",
        )
        assert save_execution_approval_policy(p, tmp_path) is False

    def test_save_rejects_private_paths(self, tmp_path):
        p = ExecutionApprovalPolicy(
            policy_id="path-test", notes="/home/alice/secret",
        )
        assert save_execution_approval_policy(p, tmp_path) is False

    def test_list_returns_defaults_when_empty(self, tmp_path):
        policies = list_execution_approval_policies(tmp_path)
        assert len(policies) >= 3
        ids = {p["policy_id"] for p in policies}
        assert "fixture-echo-v0" in ids
        assert "claude-code-repair-v0" in ids

    def test_list_returns_stored(self, tmp_path):
        p = ExecutionApprovalPolicy(
            policy_id="stored-1", label="Stored", adapter_id="a",
        )
        save_execution_approval_policy(p, tmp_path)
        policies = list_execution_approval_policies(tmp_path)
        ids = {pi["policy_id"] for pi in policies}
        assert "stored-1" in ids

    def test_load_missing_returns_none(self, tmp_path):
        assert load_execution_approval_policy("nonexistent", tmp_path) is None

    def test_corrupt_file_returns_none(self, tmp_path):
        pol_dir = tmp_path / "approval_policies"
        pol_dir.mkdir(parents=True)
        (pol_dir / "bad.json").write_text("not json{{{", encoding="utf-8")
        assert load_execution_approval_policy("bad", tmp_path) is None


# ---------------------------------------------------------------------------
# Integrity tests (Step 2768)
# ---------------------------------------------------------------------------


class TestPolicyIntegrity:
    def test_healthy_defaults(self, tmp_path):
        result = execution_approval_policy_integrity(tmp_path)
        assert result["healthy"] is True
        assert result["policy_count"] >= 3

    def test_real_provider_enabled_warning(self, tmp_path):
        p = ExecutionApprovalPolicy(
            policy_id="rp-warn", enabled=True,
            allow_real_provider=True, adapter_id="a",
        )
        save_execution_approval_policy(p, tmp_path)
        result = execution_approval_policy_integrity(tmp_path)
        assert any("real provider" in w for w in result["warnings"])

    def test_fixture_real_conflict_error(self, tmp_path):
        p = ExecutionApprovalPolicy(
            policy_id="conflict", enabled=True,
            requires_fixture_only=True, allow_real_provider=True,
            adapter_id="a",
        )
        save_execution_approval_policy(p, tmp_path)
        result = execution_approval_policy_integrity(tmp_path)
        assert any("conflict" in e for e in result["errors"])
        assert result["healthy"] is False

    def test_uses_exceeded_error(self, tmp_path):
        p = ExecutionApprovalPolicy(
            policy_id="overused", max_uses=5, uses_consumed=10,
            adapter_id="a",
        )
        save_execution_approval_policy(p, tmp_path)
        result = execution_approval_policy_integrity(tmp_path)
        assert any("uses_consumed" in e for e in result["errors"])

    def test_expired_enabled_warning(self, tmp_path):
        past = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
        p = ExecutionApprovalPolicy(
            policy_id="expired", enabled=True,
            expires_at=past, adapter_id="a",
        )
        save_execution_approval_policy(p, tmp_path)
        result = execution_approval_policy_integrity(tmp_path)
        assert any("expired" in w for w in result["warnings"])


# ---------------------------------------------------------------------------
# Evaluation denied tests (Step 2769)
# ---------------------------------------------------------------------------


_ADAPTER_PATCH = "packages.orchestration.execution_approval_policy._load_adapter"
_SESSION_PATCH = "packages.orchestration.execution_approval_policy._load_session"
_PACKAGE_PATCH = "packages.orchestration.execution_approval_policy._load_package"
_TEMPLATE_PATCH = "packages.orchestration.execution_approval_policy._load_template"


def _fixture_adapter():
    return {"adapter_id": "fixture-v0", "kind": "fixture_builder", "enabled": True}


def _fixture_template():
    return {
        "template_id": "fixture-echo-v0", "adapter_kind": "fixture_builder",
        "enabled": True, "timeout_seconds": 60, "max_output_bytes": 65536,
    }


def _fixture_session():
    return {
        "session_id": "s-1", "adapter_id": "fixture-v0",
        "package_id": "pkg-1", "status": "active",
    }


def _fixture_package():
    return {"package_id": "pkg-1", "task_type": "repair"}


def _enabled_fixture_policy(tmp_path):
    p = ExecutionApprovalPolicy(
        policy_id="fixture-echo-v0", label="Fixture test",
        enabled=True, adapter_id="fixture-v0", adapter_kind="fixture_builder",
        template_id="fixture-echo-v0", template_kind="fixture_builder",
        allowed_task_types=["repair", "test"],
        max_timeout_seconds=60, max_output_bytes=65536,
        max_uses=100, requires_fixture_only=True,
    )
    save_execution_approval_policy(p, tmp_path)
    return p


class TestEvaluationDenied:
    @patch(_TEMPLATE_PATCH, return_value=None)
    def test_missing_template(self, mock_tmpl, tmp_path):
        d = evaluate_execution_approval_policy("s-1", "bad", data_dir=tmp_path)
        assert d.decision_code == PolicyDecisionCode.MISSING_TEMPLATE
        assert not d.allowed

    @patch(_TEMPLATE_PATCH, return_value={"enabled": False, "template_id": "t-1"})
    def test_disabled_template(self, mock_tmpl, tmp_path):
        d = evaluate_execution_approval_policy("s-1", "t-1", data_dir=tmp_path)
        assert d.decision_code == PolicyDecisionCode.UNSAFE_TEMPLATE
        assert not d.allowed

    @patch(_TEMPLATE_PATCH, return_value=_fixture_template())
    @patch(_SESSION_PATCH, return_value=None)
    def test_missing_session(self, mock_sess, mock_tmpl, tmp_path):
        d = evaluate_execution_approval_policy("bad", "fixture-echo-v0", data_dir=tmp_path)
        assert d.decision_code == PolicyDecisionCode.MISSING_SESSION
        assert not d.allowed

    @patch(_TEMPLATE_PATCH, return_value=_fixture_template())
    @patch(_SESSION_PATCH, return_value={"session_id": "s-1", "adapter_id": "", "package_id": ""})
    def test_missing_adapter_in_session(self, mock_sess, mock_tmpl, tmp_path):
        d = evaluate_execution_approval_policy("s-1", "fixture-echo-v0", data_dir=tmp_path)
        assert d.decision_code == PolicyDecisionCode.MISSING_ADAPTER

    @patch(_TEMPLATE_PATCH, return_value=_fixture_template())
    @patch(_SESSION_PATCH, return_value=_fixture_session())
    @patch(_ADAPTER_PATCH, return_value=None)
    def test_adapter_not_found(self, mock_adap, mock_sess, mock_tmpl, tmp_path):
        d = evaluate_execution_approval_policy("s-1", "fixture-echo-v0", data_dir=tmp_path)
        assert d.decision_code == PolicyDecisionCode.MISSING_ADAPTER

    @patch(_TEMPLATE_PATCH, return_value=_fixture_template())
    @patch(_SESSION_PATCH, return_value=_fixture_session())
    @patch(_ADAPTER_PATCH, return_value=_fixture_adapter())
    def test_no_enabled_policies(self, mock_adap, mock_sess, mock_tmpl, tmp_path):
        d = evaluate_execution_approval_policy("s-1", "fixture-echo-v0", data_dir=tmp_path)
        assert d.decision_code == PolicyDecisionCode.NO_MATCHING_POLICY

    @patch(_TEMPLATE_PATCH, return_value=_fixture_template())
    @patch(_SESSION_PATCH, return_value=_fixture_session())
    @patch(_ADAPTER_PATCH, return_value=_fixture_adapter())
    @patch(_PACKAGE_PATCH, return_value=_fixture_package())
    def test_adapter_mismatch(self, mock_pkg, mock_adap, mock_sess, mock_tmpl, tmp_path):
        p = ExecutionApprovalPolicy(
            policy_id="wrong-adapter", enabled=True,
            adapter_id="wrong-adapter-id", adapter_kind="fixture_builder",
            template_id="fixture-echo-v0",
            requires_fixture_only=True,
        )
        save_execution_approval_policy(p, tmp_path)
        d = evaluate_execution_approval_policy("s-1", "fixture-echo-v0", data_dir=tmp_path)
        assert not d.allowed

    @patch(_TEMPLATE_PATCH, return_value=_fixture_template())
    @patch(_SESSION_PATCH, return_value=_fixture_session())
    @patch(_ADAPTER_PATCH, return_value=_fixture_adapter())
    @patch(_PACKAGE_PATCH, return_value=_fixture_package())
    def test_template_mismatch(self, mock_pkg, mock_adap, mock_sess, mock_tmpl, tmp_path):
        p = ExecutionApprovalPolicy(
            policy_id="wrong-tmpl", enabled=True,
            adapter_id="fixture-v0", adapter_kind="fixture_builder",
            template_id="wrong-template-id",
            requires_fixture_only=True,
        )
        save_execution_approval_policy(p, tmp_path)
        d = evaluate_execution_approval_policy("s-1", "fixture-echo-v0", data_dir=tmp_path)
        assert not d.allowed

    @patch(_TEMPLATE_PATCH, return_value=_fixture_template())
    @patch(_SESSION_PATCH, return_value=_fixture_session())
    @patch(_ADAPTER_PATCH, return_value=_fixture_adapter())
    @patch(_PACKAGE_PATCH, return_value={"package_id": "pkg-1", "task_type": "deploy"})
    def test_task_type_not_allowed(self, mock_pkg, mock_adap, mock_sess, mock_tmpl, tmp_path):
        _enabled_fixture_policy(tmp_path)
        d = evaluate_execution_approval_policy("s-1", "fixture-echo-v0", data_dir=tmp_path)
        assert not d.allowed

    @patch(_TEMPLATE_PATCH)
    @patch(_SESSION_PATCH, return_value=_fixture_session())
    @patch(_ADAPTER_PATCH, return_value=_fixture_adapter())
    @patch(_PACKAGE_PATCH, return_value=_fixture_package())
    def test_timeout_exceeds_policy(self, mock_pkg, mock_adap, mock_sess, mock_tmpl, tmp_path):
        mock_tmpl.return_value = {
            **_fixture_template(), "timeout_seconds": 300,
        }
        _enabled_fixture_policy(tmp_path)
        d = evaluate_execution_approval_policy("s-1", "fixture-echo-v0", data_dir=tmp_path)
        assert not d.allowed

    @patch(_TEMPLATE_PATCH)
    @patch(_SESSION_PATCH, return_value=_fixture_session())
    @patch(_ADAPTER_PATCH, return_value=_fixture_adapter())
    @patch(_PACKAGE_PATCH, return_value=_fixture_package())
    def test_output_cap_exceeds_policy(self, mock_pkg, mock_adap, mock_sess, mock_tmpl, tmp_path):
        mock_tmpl.return_value = {
            **_fixture_template(), "max_output_bytes": 999999,
        }
        _enabled_fixture_policy(tmp_path)
        d = evaluate_execution_approval_policy("s-1", "fixture-echo-v0", data_dir=tmp_path)
        assert not d.allowed

    @patch(_TEMPLATE_PATCH, return_value=_fixture_template())
    @patch(_SESSION_PATCH, return_value=_fixture_session())
    @patch(_ADAPTER_PATCH, return_value=_fixture_adapter())
    @patch(_PACKAGE_PATCH, return_value=_fixture_package())
    def test_policy_expired(self, mock_pkg, mock_adap, mock_sess, mock_tmpl, tmp_path):
        past = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
        p = ExecutionApprovalPolicy(
            policy_id="expired-pol", enabled=True,
            adapter_id="fixture-v0", adapter_kind="fixture_builder",
            template_id="fixture-echo-v0",
            expires_at=past, requires_fixture_only=True,
        )
        save_execution_approval_policy(p, tmp_path)
        d = evaluate_execution_approval_policy("s-1", "fixture-echo-v0", data_dir=tmp_path)
        assert not d.allowed

    @patch(_TEMPLATE_PATCH, return_value=_fixture_template())
    @patch(_SESSION_PATCH, return_value=_fixture_session())
    @patch(_ADAPTER_PATCH, return_value=_fixture_adapter())
    @patch(_PACKAGE_PATCH, return_value=_fixture_package())
    def test_policy_uses_exhausted(self, mock_pkg, mock_adap, mock_sess, mock_tmpl, tmp_path):
        p = ExecutionApprovalPolicy(
            policy_id="exhausted", enabled=True,
            adapter_id="fixture-v0", adapter_kind="fixture_builder",
            template_id="fixture-echo-v0",
            max_uses=5, uses_consumed=5,
            requires_fixture_only=True,
        )
        save_execution_approval_policy(p, tmp_path)
        d = evaluate_execution_approval_policy("s-1", "fixture-echo-v0", data_dir=tmp_path)
        assert not d.allowed

    @patch(_TEMPLATE_PATCH, return_value=_fixture_template())
    @patch(_SESSION_PATCH, return_value={
        "session_id": "s-1", "adapter_id": "claude-code-v0", "package_id": "pkg-1",
    })
    @patch(_ADAPTER_PATCH, return_value={
        "adapter_id": "claude-code-v0", "kind": "claude_code", "enabled": True,
    })
    @patch(_PACKAGE_PATCH, return_value=_fixture_package())
    def test_real_provider_not_allowed(self, mock_pkg, mock_adap, mock_sess, mock_tmpl, tmp_path):
        p = ExecutionApprovalPolicy(
            policy_id="no-real", enabled=True,
            adapter_id="claude-code-v0", adapter_kind="claude_code",
            template_id="fixture-echo-v0",
            allow_real_provider=False,
        )
        save_execution_approval_policy(p, tmp_path)
        d = evaluate_execution_approval_policy("s-1", "fixture-echo-v0", data_dir=tmp_path)
        assert not d.allowed

    @patch(_TEMPLATE_PATCH, return_value=_fixture_template())
    @patch(_SESSION_PATCH, return_value={
        "session_id": "s-1", "adapter_id": "claude-code-v0", "package_id": "pkg-1",
    })
    @patch(_ADAPTER_PATCH, return_value={
        "adapter_id": "claude-code-v0", "kind": "claude_code", "enabled": True,
    })
    @patch(_PACKAGE_PATCH, return_value=_fixture_package())
    def test_fixture_required_but_real_adapter(self, mock_pkg, mock_adap, mock_sess, mock_tmpl, tmp_path):
        p = ExecutionApprovalPolicy(
            policy_id="fixture-only", enabled=True,
            adapter_id="claude-code-v0", adapter_kind="claude_code",
            template_id="fixture-echo-v0",
            requires_fixture_only=True,
        )
        save_execution_approval_policy(p, tmp_path)
        d = evaluate_execution_approval_policy("s-1", "fixture-echo-v0", data_dir=tmp_path)
        assert not d.allowed


# ---------------------------------------------------------------------------
# Evaluation allowed tests (Step 2770)
# ---------------------------------------------------------------------------


class TestEvaluationAllowed:
    @patch(_TEMPLATE_PATCH, return_value=_fixture_template())
    @patch(_SESSION_PATCH, return_value=_fixture_session())
    @patch(_ADAPTER_PATCH, return_value=_fixture_adapter())
    @patch(_PACKAGE_PATCH, return_value=_fixture_package())
    def test_fixture_policy_allowed(self, mock_pkg, mock_adap, mock_sess, mock_tmpl, tmp_path):
        _enabled_fixture_policy(tmp_path)
        d = evaluate_execution_approval_policy("s-1", "fixture-echo-v0", data_dir=tmp_path)
        assert d.allowed
        assert d.decision_code == PolicyDecisionCode.ALLOWED
        assert d.policy_id == "fixture-echo-v0"
        assert not d.required_manual_approval

    @patch(_TEMPLATE_PATCH, return_value={
        "template_id": "claude-code-repair-v0", "adapter_kind": "claude_code",
        "enabled": True, "timeout_seconds": 300, "max_output_bytes": 262144,
    })
    @patch(_SESSION_PATCH, return_value={
        "session_id": "s-1", "adapter_id": "claude-code-v0", "package_id": "pkg-1",
    })
    @patch(_ADAPTER_PATCH, return_value={
        "adapter_id": "claude-code-v0", "kind": "claude_code", "enabled": True,
    })
    @patch(_PACKAGE_PATCH, return_value=_fixture_package())
    def test_real_provider_allowed_when_explicit(self, mock_pkg, mock_adap, mock_sess, mock_tmpl, tmp_path):
        p = ExecutionApprovalPolicy(
            policy_id="claude-explicit", enabled=True,
            adapter_id="claude-code-v0", adapter_kind="claude_code",
            template_id="claude-code-repair-v0", template_kind="claude_code",
            allowed_task_types=["repair"],
            max_timeout_seconds=300, max_output_bytes=262144,
            max_uses=10, allow_real_provider=True,
        )
        save_execution_approval_policy(p, tmp_path)
        d = evaluate_execution_approval_policy("s-1", "claude-code-repair-v0", data_dir=tmp_path)
        assert d.allowed
        assert d.policy_id == "claude-explicit"

    @patch(_TEMPLATE_PATCH, return_value={
        **_fixture_template(), "timeout_seconds": 30, "max_output_bytes": 4096,
    })
    @patch(_SESSION_PATCH, return_value=_fixture_session())
    @patch(_ADAPTER_PATCH, return_value=_fixture_adapter())
    @patch(_PACKAGE_PATCH, return_value=_fixture_package())
    def test_limits_applied_tighter_wins(self, mock_pkg, mock_adap, mock_sess, mock_tmpl, tmp_path):
        p = ExecutionApprovalPolicy(
            policy_id="tight-limits", enabled=True,
            adapter_id="fixture-v0", adapter_kind="fixture_builder",
            template_id="fixture-echo-v0", template_kind="fixture_builder",
            max_timeout_seconds=60, max_output_bytes=65536,
            requires_fixture_only=True,
        )
        save_execution_approval_policy(p, tmp_path)
        d = evaluate_execution_approval_policy("s-1", "fixture-echo-v0", data_dir=tmp_path)
        assert d.allowed
        assert d.limits_applied["max_timeout_seconds"] == 30
        assert d.limits_applied["max_output_bytes"] == 4096


# ---------------------------------------------------------------------------
# Grant denied tests (Step 2771)
# ---------------------------------------------------------------------------


class TestGrantDenied:
    @patch(_TEMPLATE_PATCH, return_value=None)
    def test_denied_no_approval_created(self, mock_tmpl, tmp_path):
        result = create_policy_granted_execution_approval(
            "s-1", "bad", data_dir=tmp_path,
        )
        assert result["granted"] is False
        assert result["approval_id"] == ""

    @patch(_TEMPLATE_PATCH, return_value=_fixture_template())
    @patch(_SESSION_PATCH, return_value=_fixture_session())
    @patch(_ADAPTER_PATCH, return_value=_fixture_adapter())
    @patch(_PACKAGE_PATCH, return_value=_fixture_package())
    def test_no_enabled_policy_no_grant(self, mock_pkg, mock_adap, mock_sess, mock_tmpl, tmp_path):
        result = create_policy_granted_execution_approval(
            "s-1", "fixture-echo-v0", data_dir=tmp_path,
        )
        assert result["granted"] is False


# ---------------------------------------------------------------------------
# Grant allowed tests (Step 2772)
# ---------------------------------------------------------------------------


class TestGrantAllowed:
    @patch(_TEMPLATE_PATCH, return_value=_fixture_template())
    @patch(_SESSION_PATCH, return_value=_fixture_session())
    @patch(_ADAPTER_PATCH, return_value=_fixture_adapter())
    @patch(_PACKAGE_PATCH, return_value=_fixture_package())
    @patch("packages.orchestration.managed_builder_execution.approve_managed_execution")
    def test_fixture_grant_creates_approval(
        self, mock_approve, mock_pkg, mock_adap, mock_sess, mock_tmpl, tmp_path,
    ):
        mock_approval = MagicMock()
        mock_approval.approval_id = "appr-123"
        mock_approve.return_value = mock_approval
        _enabled_fixture_policy(tmp_path)

        result = create_policy_granted_execution_approval(
            "s-1", "fixture-echo-v0", data_dir=tmp_path,
        )
        assert result["granted"] is True
        assert result["approval_id"] == "appr-123"
        mock_approve.assert_called_once()

    @patch(_TEMPLATE_PATCH, return_value=_fixture_template())
    @patch(_SESSION_PATCH, return_value=_fixture_session())
    @patch(_ADAPTER_PATCH, return_value=_fixture_adapter())
    @patch(_PACKAGE_PATCH, return_value=_fixture_package())
    @patch("packages.orchestration.managed_builder_execution.approve_managed_execution")
    def test_grant_binds_policy_id_in_operator(
        self, mock_approve, mock_pkg, mock_adap, mock_sess, mock_tmpl, tmp_path,
    ):
        mock_approval = MagicMock()
        mock_approval.approval_id = "appr-456"
        mock_approve.return_value = mock_approval
        _enabled_fixture_policy(tmp_path)

        create_policy_granted_execution_approval(
            "s-1", "fixture-echo-v0", data_dir=tmp_path,
        )
        call_kwargs = mock_approve.call_args
        assert "policy:" in call_kwargs.kwargs.get("operator_id", "")


# ---------------------------------------------------------------------------
# Caps inherited tests (Step 2773)
# ---------------------------------------------------------------------------


class TestCapsInherited:
    @patch(_TEMPLATE_PATCH, return_value={
        **_fixture_template(), "timeout_seconds": 30, "max_output_bytes": 8192,
    })
    @patch(_SESSION_PATCH, return_value=_fixture_session())
    @patch(_ADAPTER_PATCH, return_value=_fixture_adapter())
    @patch(_PACKAGE_PATCH, return_value=_fixture_package())
    @patch("packages.orchestration.managed_builder_execution.approve_managed_execution")
    def test_approval_uses_tighter_caps(
        self, mock_approve, mock_pkg, mock_adap, mock_sess, mock_tmpl, tmp_path,
    ):
        mock_approval = MagicMock()
        mock_approval.approval_id = "appr-caps"
        mock_approve.return_value = mock_approval
        p = ExecutionApprovalPolicy(
            policy_id="tight", enabled=True,
            adapter_id="fixture-v0", adapter_kind="fixture_builder",
            template_id="fixture-echo-v0", template_kind="fixture_builder",
            max_timeout_seconds=60, max_output_bytes=65536,
            requires_fixture_only=True,
        )
        save_execution_approval_policy(p, tmp_path)

        create_policy_granted_execution_approval(
            "s-1", "fixture-echo-v0", data_dir=tmp_path,
        )
        call_kwargs = mock_approve.call_args.kwargs
        assert call_kwargs["max_runtime_seconds"] == 30
        assert call_kwargs["max_output_bytes"] == 8192


# ---------------------------------------------------------------------------
# Uses decrement tests (Step 2774)
# ---------------------------------------------------------------------------


class TestUsesDecrement:
    @patch(_TEMPLATE_PATCH, return_value=_fixture_template())
    @patch(_SESSION_PATCH, return_value=_fixture_session())
    @patch(_ADAPTER_PATCH, return_value=_fixture_adapter())
    @patch(_PACKAGE_PATCH, return_value=_fixture_package())
    @patch("packages.orchestration.managed_builder_execution.approve_managed_execution")
    def test_grant_decrements_uses(
        self, mock_approve, mock_pkg, mock_adap, mock_sess, mock_tmpl, tmp_path,
    ):
        mock_approval = MagicMock()
        mock_approval.approval_id = "appr-use"
        mock_approve.return_value = mock_approval

        _enabled_fixture_policy(tmp_path)
        create_policy_granted_execution_approval(
            "s-1", "fixture-echo-v0", data_dir=tmp_path,
        )
        reloaded = load_execution_approval_policy("fixture-echo-v0", tmp_path)
        assert reloaded is not None
        assert reloaded.uses_consumed == 1

    @patch(_TEMPLATE_PATCH, return_value=_fixture_template())
    @patch(_SESSION_PATCH, return_value=_fixture_session())
    @patch(_ADAPTER_PATCH, return_value=_fixture_adapter())
    @patch(_PACKAGE_PATCH, return_value=_fixture_package())
    @patch("packages.orchestration.managed_builder_execution.approve_managed_execution")
    def test_exhausted_after_max(
        self, mock_approve, mock_pkg, mock_adap, mock_sess, mock_tmpl, tmp_path,
    ):
        mock_approval = MagicMock()
        mock_approval.approval_id = "appr-last"
        mock_approve.return_value = mock_approval

        p = ExecutionApprovalPolicy(
            policy_id="one-shot", enabled=True,
            adapter_id="fixture-v0", adapter_kind="fixture_builder",
            template_id="fixture-echo-v0", template_kind="fixture_builder",
            max_uses=1, requires_fixture_only=True,
        )
        save_execution_approval_policy(p, tmp_path)
        r1 = create_policy_granted_execution_approval(
            "s-1", "fixture-echo-v0", data_dir=tmp_path,
        )
        assert r1["granted"] is True

        r2 = create_policy_granted_execution_approval(
            "s-1", "fixture-echo-v0", data_dir=tmp_path,
        )
        assert r2["granted"] is False


# ---------------------------------------------------------------------------
# Summary tests (Step 2751)
# ---------------------------------------------------------------------------


class TestPolicySummary:
    def test_summary_defaults(self, tmp_path):
        s = execution_approval_policy_summary(tmp_path)
        assert s["configured_policy_count"] >= 3
        assert s["enabled_policy_count"] == 0
        assert s["integrity_healthy"] is True

    def test_summary_with_enabled(self, tmp_path):
        _enabled_fixture_policy(tmp_path)
        s = execution_approval_policy_summary(tmp_path)
        assert s["enabled_policy_count"] >= 1
        assert "fixture-echo-v0" in s["enabled_policy_ids"]


# ---------------------------------------------------------------------------
# Default policies tests
# ---------------------------------------------------------------------------


class TestDefaultPolicies:
    def test_all_disabled(self):
        for p in default_policies():
            assert not p.enabled, f"{p.policy_id} should be disabled by default"

    def test_fixture_is_fixture_only(self):
        for p in default_policies():
            if "fixture" in p.policy_id:
                assert p.requires_fixture_only
                assert not p.allow_real_provider

    def test_real_provider_not_allowed_by_default(self):
        for p in default_policies():
            assert not p.allow_real_provider, \
                f"{p.policy_id} should not allow real provider by default"
