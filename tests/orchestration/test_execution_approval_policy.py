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
    @patch(_PACKAGE_PATCH, return_value={
        "package_id": "pkg-1", "task_type": "repair",
        "token_budget_summary": {"estimated_token_band": "medium", "budget_status": "within_budget"},
    })
    def test_real_provider_allowed_when_explicit(self, mock_pkg, mock_adap, mock_sess, mock_tmpl, tmp_path):
        p = ExecutionApprovalPolicy(
            policy_id="claude-explicit", enabled=True,
            adapter_id="claude-code-v0", adapter_kind="claude_code",
            template_id="claude-code-repair-v0", template_kind="claude_code",
            allowed_task_types=["repair"],
            max_timeout_seconds=300, max_output_bytes=262144,
            max_uses=10, allow_real_provider=True,
            confirmed_real_provider_at="2026-01-01T00:00:00+00:00",
            confirmed_by_operator="test",
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


# ---------------------------------------------------------------------------
# Closure tests: R-0157 redaction strengthening (Steps 2841-2842)
# ---------------------------------------------------------------------------


class TestRedactionStrengthened:
    def test_redact_token_kv(self):
        from packages.orchestration.execution_approval_policy import _safe
        t = _safe('token=mysecret123 visible')
        assert "mysecret123" not in t
        assert "token=***" in t

    def test_redact_quoted_token(self):
        from packages.orchestration.execution_approval_policy import _safe
        t = _safe('token="mysecret123" visible')
        assert "mysecret123" not in t
        assert "token=***" in t

    def test_redact_credential_kv(self):
        from packages.orchestration.execution_approval_policy import _safe
        t = _safe('credential=abc123 visible')
        assert "abc123" not in t

    def test_redact_quoted_api_key(self):
        from packages.orchestration.execution_approval_policy import _safe
        t = _safe('api_key="sk-test-123456" visible')
        assert "sk-test-123456" not in t

    def test_redact_pem_block(self):
        from packages.orchestration.execution_approval_policy import _safe
        t = _safe('data -----BEGIN RSA PRIVATE KEY----- more')
        assert "-----BEGIN" not in t
        assert "[redacted-pem]" in t

    def test_redact_tmp_path(self):
        from packages.orchestration.execution_approval_policy import _safe
        t = _safe('Error at /tmp/private/file.txt')
        assert "/tmp/private" not in t

    def test_redact_mnt_path(self):
        from packages.orchestration.execution_approval_policy import _safe
        t = _safe('Error at /mnt/data/private/file.txt')
        assert "/mnt/data" not in t

    def test_redact_root_path(self):
        from packages.orchestration.execution_approval_policy import _safe
        t = _safe('Error at /root/private/file.txt')
        assert "/root/private" not in t

    def test_save_rejects_token_marker(self, tmp_path):
        p = ExecutionApprovalPolicy(
            policy_id="tkn-test", label="token=abc123",
        )
        assert save_execution_approval_policy(p, tmp_path) is False

    def test_save_rejects_credential_marker(self, tmp_path):
        p = ExecutionApprovalPolicy(
            policy_id="cred-test", notes="credential=secret",
        )
        assert save_execution_approval_policy(p, tmp_path) is False

    def test_save_rejects_pem(self, tmp_path):
        p = ExecutionApprovalPolicy(
            policy_id="pem-test", notes="-----begin certificate-----",
        )
        assert save_execution_approval_policy(p, tmp_path) is False

    def test_save_rejects_tmp_path(self, tmp_path):
        p = ExecutionApprovalPolicy(
            policy_id="tmp-test", notes="/tmp/secret/data",
        )
        assert save_execution_approval_policy(p, tmp_path) is False

    def test_integrity_flags_token_in_data(self, tmp_path):
        pol_dir = tmp_path / "approval_policies"
        pol_dir.mkdir(parents=True)
        import json
        (pol_dir / "bad.json").write_text(
            json.dumps({"policy_id": "bad", "reason": "token=secret123"}),
            encoding="utf-8",
        )
        result = execution_approval_policy_integrity(tmp_path)
        assert not result["healthy"]
        assert any("secret marker" in e for e in result["errors"])


# ---------------------------------------------------------------------------
# Closure tests: R-0158 task type + token estimate (Steps 2844-2845)
# ---------------------------------------------------------------------------


class TestTaskTypeEnforcement:
    @patch(_TEMPLATE_PATCH, return_value=_fixture_template())
    @patch(_SESSION_PATCH, return_value=_fixture_session())
    @patch(_ADAPTER_PATCH, return_value=_fixture_adapter())
    @patch(_PACKAGE_PATCH, return_value={"package_id": "pkg-1"})
    def test_missing_task_type_denied(self, mock_pkg, mock_adap, mock_sess, mock_tmpl, tmp_path):
        """Policy with allowed_task_types denies when package has no task_type."""
        p = ExecutionApprovalPolicy(
            policy_id="fixture-echo-v0", enabled=True,
            adapter_id="fixture-v0", adapter_kind="fixture_builder",
            template_id="fixture-echo-v0", template_kind="fixture_builder",
            allowed_task_types=["repair"],
            max_timeout_seconds=60, max_output_bytes=65536,
            max_uses=100, requires_fixture_only=True,
        )
        save_execution_approval_policy(p, tmp_path)
        d = evaluate_execution_approval_policy("s-1", "fixture-echo-v0", data_dir=tmp_path)
        assert not d.allowed
        assert d.decision_code == "missing_task_type"


class TestTokenEstimateEnforcement:
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
    @patch(_PACKAGE_PATCH, return_value={
        "package_id": "pkg-1", "task_type": "repair",
        "token_budget_summary": {"estimated_token_band": "unknown", "budget_status": "unknown"},
    })
    def test_unknown_token_denied_real_provider(self, mock_pkg, mock_adap, mock_sess, mock_tmpl, tmp_path):
        """Unknown token estimate requires manual approval for real provider."""
        p = ExecutionApprovalPolicy(
            policy_id="claude-1", enabled=True,
            adapter_id="claude-code-v0", adapter_kind="claude_code",
            template_id="claude-code-repair-v0", template_kind="claude_code",
            allowed_task_types=["repair"],
            max_timeout_seconds=300, max_output_bytes=262144,
            max_uses=10, allow_real_provider=True,
            confirmed_real_provider_at="2026-01-01T00:00:00+00:00",
            confirmed_by_operator="test",
        )
        save_execution_approval_policy(p, tmp_path)
        d = evaluate_execution_approval_policy("s-1", "claude-code-repair-v0", data_dir=tmp_path)
        assert not d.allowed
        assert d.decision_code == "token_estimate_unknown"

    @patch(_TEMPLATE_PATCH, return_value=_fixture_template())
    @patch(_SESSION_PATCH, return_value=_fixture_session())
    @patch(_ADAPTER_PATCH, return_value=_fixture_adapter())
    @patch(_PACKAGE_PATCH, return_value={
        "package_id": "pkg-1", "task_type": "repair",
        "token_budget_summary": {"estimated_token_band": "unknown", "budget_status": "unknown"},
    })
    def test_unknown_token_allowed_fixture(self, mock_pkg, mock_adap, mock_sess, mock_tmpl, tmp_path):
        """Fixture policies bypass unknown token estimate check."""
        _enabled_fixture_policy(tmp_path)
        d = evaluate_execution_approval_policy("s-1", "fixture-echo-v0", data_dir=tmp_path)
        assert d.allowed

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
    @patch(_PACKAGE_PATCH, return_value={
        "package_id": "pkg-1", "task_type": "repair",
        "token_budget_summary": {"estimated_token_band": "medium", "budget_status": "over_budget"},
    })
    def test_over_budget_token_denied(self, mock_pkg, mock_adap, mock_sess, mock_tmpl, tmp_path):
        """Over-budget token estimate is denied."""
        p = ExecutionApprovalPolicy(
            policy_id="claude-1", enabled=True,
            adapter_id="claude-code-v0", adapter_kind="claude_code",
            template_id="claude-code-repair-v0", template_kind="claude_code",
            allowed_task_types=["repair"],
            max_timeout_seconds=300, max_output_bytes=262144,
            max_uses=10, allow_real_provider=True,
            confirmed_real_provider_at="2026-01-01T00:00:00+00:00",
            confirmed_by_operator="test",
        )
        save_execution_approval_policy(p, tmp_path)
        d = evaluate_execution_approval_policy("s-1", "claude-code-repair-v0", data_dir=tmp_path)
        assert not d.allowed


# ---------------------------------------------------------------------------
# Closure tests: R-0159 real-provider confirmation (Step 2848)
# ---------------------------------------------------------------------------


class TestRealProviderConfirmation:
    def test_confirmation_fields_roundtrip(self):
        p = ExecutionApprovalPolicy(
            policy_id="rp-1", allow_real_provider=True,
            confirmed_real_provider_at="2026-01-01T00:00:00+00:00",
            confirmed_by_operator="admin",
            real_provider_confirmation_reason="Testing",
        )
        d = p.to_dict()
        p2 = ExecutionApprovalPolicy.from_dict(d)
        assert p2.confirmed_real_provider_at == "2026-01-01T00:00:00+00:00"
        assert p2.confirmed_by_operator == "admin"

    def test_integrity_error_unconfirmed_real_provider(self, tmp_path):
        p = ExecutionApprovalPolicy(
            policy_id="rp-unconf", enabled=True,
            allow_real_provider=True, adapter_id="a",
        )
        save_execution_approval_policy(p, tmp_path)
        result = execution_approval_policy_integrity(tmp_path)
        assert any("confirmation" in e for e in result["errors"])
        assert not result["healthy"]

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
    @patch(_PACKAGE_PATCH, return_value={
        "package_id": "pkg-1", "task_type": "repair",
        "token_budget_summary": {"estimated_token_band": "medium", "budget_status": "within_budget"},
    })
    def test_unconfirmed_real_provider_denied(self, mock_pkg, mock_adap, mock_sess, mock_tmpl, tmp_path):
        """Real provider policy without confirmation metadata is denied."""
        p = ExecutionApprovalPolicy(
            policy_id="rp-noconf", enabled=True,
            adapter_id="claude-code-v0", adapter_kind="claude_code",
            template_id="claude-code-repair-v0", template_kind="claude_code",
            allowed_task_types=["repair"],
            max_timeout_seconds=300, max_output_bytes=262144,
            max_uses=10, allow_real_provider=True,
        )
        save_execution_approval_policy(p, tmp_path)
        d = evaluate_execution_approval_policy("s-1", "claude-code-repair-v0", data_dir=tmp_path)
        assert not d.allowed


# ---------------------------------------------------------------------------
# Closure tests: R-0160 decision codes (Step 2847)
# ---------------------------------------------------------------------------


class TestDecisionCodeCompleteness:
    def test_new_codes_in_all_codes(self):
        assert "missing_task_type" in _ALL_DECISION_CODES
        assert "token_estimate_unknown" in _ALL_DECISION_CODES
        assert "real_provider_unconfirmed" in _ALL_DECISION_CODES

    def test_code_count_at_least_23(self):
        assert len(_ALL_DECISION_CODES) >= 23


# ---------------------------------------------------------------------------
# Closure tests: R-0161 uses decrement order (Step 2849)
# ---------------------------------------------------------------------------


class TestUsesDecrementOrder:
    @patch(_TEMPLATE_PATCH, return_value=_fixture_template())
    @patch(_SESSION_PATCH, return_value=_fixture_session())
    @patch(_ADAPTER_PATCH, return_value=_fixture_adapter())
    @patch(_PACKAGE_PATCH, return_value=_fixture_package())
    def test_uses_not_decremented_when_approval_fails(
        self, mock_pkg, mock_adap, mock_sess, mock_tmpl, tmp_path,
    ):
        """If approve_managed_execution returns None, uses stay unchanged."""
        _enabled_fixture_policy(tmp_path)
        with patch(
            "packages.orchestration.managed_builder_execution.approve_managed_execution",
            return_value=None,
        ):
            result = create_policy_granted_execution_approval(
                "s-1", "fixture-echo-v0", data_dir=tmp_path,
            )
        assert result["granted"] is False
        pol = load_execution_approval_policy("fixture-echo-v0", tmp_path)
        assert pol.uses_consumed == 0


# ---------------------------------------------------------------------------
# Closure tests: R-0163 summary enrichment (Step 2853)
# ---------------------------------------------------------------------------


class TestSummaryEnriched:
    def test_summary_includes_grant_count(self, tmp_path):
        summary = execution_approval_policy_summary(tmp_path)
        assert "grant_count" in summary
        assert "latest_decision_code" in summary
        assert "manual_approval_required" in summary
        assert "next_safe_action" in summary


# ---------------------------------------------------------------------------
# Integration tests: R-0164 real builder package storage (Steps 2880-2886)
# No _load_package mock — exercises real main_builder_adapter paths.
# ---------------------------------------------------------------------------


def _create_real_product_state(tmp_path, *, token_band="small", budget_status="within_budget"):
    """Create real adapter, template, package, session, and policy on disk."""
    from packages.orchestration.main_builder_adapter import (
        BuilderAdapterKind,
        BuilderAdapterMode,
        BuilderAdapterSpec,
        build_builder_request_package,
        create_builder_session,
        save_builder_adapter_spec,
    )
    from packages.orchestration.managed_builder_execution import (
        CommandTemplate,
        save_command_template,
    )

    # Save and enable fixture adapter.
    spec = BuilderAdapterSpec(
        adapter_id="fixture-v0",
        label="Fixture Builder",
        kind=BuilderAdapterKind.FIXTURE_BUILDER,
        enabled=True,
        mode=BuilderAdapterMode.FIXTURE_ONLY,
        requires_operator_approval=False,
        requires_external_sandbox_intake=False,
    )
    save_builder_adapter_spec(spec, data_dir=tmp_path)

    # Save and enable fixture command template.
    tmpl = CommandTemplate(
        template_id="fixture-echo-v0",
        adapter_kind=BuilderAdapterKind.FIXTURE_BUILDER,
        label="Fixture echo",
        argv_template=["echo", "hello"],
        enabled=True,
        requires_approval=True,
        timeout_seconds=30,
        max_output_bytes=1024,
    )
    save_command_template(tmpl, data_dir=tmp_path)

    # Build a real package (persisted to main_builder_adapter/packages).
    pkg = build_builder_request_package(
        "job-integration-test",
        adapter_id="fixture-v0",
        token_hint={
            "estimated_token_band": token_band,
            "budget_status": budget_status,
            "requires_human_approval": False,
        },
        data_dir=tmp_path,
    )

    # Create a real session (persisted to main_builder_adapter/sessions).
    session = create_builder_session(
        pkg.package_id, "fixture-v0",
        job_id="job-integration-test",
        data_dir=tmp_path,
    )

    # Save and enable a fixture policy matching the adapter/template.
    policy = ExecutionApprovalPolicy(
        policy_id="fixture-echo-v0",
        label="Fixture echo policy",
        enabled=True,
        adapter_id="fixture-v0",
        adapter_kind=BuilderAdapterKind.FIXTURE_BUILDER,
        template_id="fixture-echo-v0",
        template_kind=BuilderAdapterKind.FIXTURE_BUILDER,
        requires_fixture_only=True,
        max_uses=10,
        max_timeout_seconds=60,
        max_output_bytes=1024,
    )
    save_execution_approval_policy(policy, data_dir=tmp_path)

    return pkg, session, policy


class TestPolicyEvaluationRealBuilderPackageStorage:
    """Prove package path truth without mocks (R-0164)."""

    def test_evaluate_allowed_real_storage(self, tmp_path):
        """Real package/session/template/policy — evaluate returns allowed."""
        pkg, session, _policy = _create_real_product_state(tmp_path)
        decision = evaluate_execution_approval_policy(
            session.session_id, "fixture-echo-v0", data_dir=tmp_path,
        )
        assert decision.allowed is True
        assert decision.decision_code == PolicyDecisionCode.ALLOWED
        assert decision.matched_package_id == pkg.package_id
        assert decision.matched_session_id == session.session_id

    def test_missing_package_real_storage(self, tmp_path):
        """Session exists but package file missing — returns missing_package."""
        pkg, session, _policy = _create_real_product_state(tmp_path)
        # Delete the real package file.
        pkg_dir = (
            tmp_path / "workspaces" / "job-integration-test"
            / "main_builder_adapter" / "packages"
        )
        for f in pkg_dir.glob("*.json"):
            f.unlink()
        decision = evaluate_execution_approval_policy(
            session.session_id, "fixture-echo-v0", data_dir=tmp_path,
        )
        assert decision.allowed is False
        assert decision.decision_code == PolicyDecisionCode.MISSING_PACKAGE
        assert decision.required_manual_approval is True

    def test_missing_task_type_real_storage(self, tmp_path):
        """Package has empty task_type, policy restricts task types — denied."""
        pkg, session, _policy = _create_real_product_state(tmp_path)
        # Overwrite package file with empty task_type.
        pkg_path = (
            tmp_path / "workspaces" / "job-integration-test"
            / "main_builder_adapter" / "packages" / f"{pkg.package_id}.json"
        )
        import json as json_mod
        data = json_mod.loads(pkg_path.read_text())
        data["task_type"] = ""
        pkg_path.write_text(json_mod.dumps(data))
        # Update policy to restrict task types.
        policy = load_execution_approval_policy("fixture-echo-v0", tmp_path)
        policy.allowed_task_types = ["repair"]
        save_execution_approval_policy(policy, data_dir=tmp_path)
        decision = evaluate_execution_approval_policy(
            session.session_id, "fixture-echo-v0", data_dir=tmp_path,
        )
        assert decision.allowed is False
        assert decision.decision_code == PolicyDecisionCode.MISSING_TASK_TYPE


class TestPolicyGrantRealStorage:
    """Prove grant with real storage binds package/session (R-0166)."""

    def test_grant_real_storage(self, tmp_path):
        """Real storage grant — creates approval, binds IDs, no execution."""
        pkg, session, _policy = _create_real_product_state(tmp_path)
        result = create_policy_granted_execution_approval(
            session.session_id, "fixture-echo-v0", data_dir=tmp_path,
        )
        assert result["granted"] is True
        assert result.get("approval_id") or result.get("approval", {}).get("approval_id")
        # Policy uses incremented.
        pol = load_execution_approval_policy("fixture-echo-v0", tmp_path)
        assert pol.uses_consumed == 1

    def test_grant_denied_missing_package(self, tmp_path):
        """Real session, missing package — grant denied, uses not consumed."""
        _pkg, session, _policy = _create_real_product_state(tmp_path)
        # Delete package files.
        pkg_dir = (
            tmp_path / "workspaces" / "job-integration-test"
            / "main_builder_adapter" / "packages"
        )
        for f in pkg_dir.glob("*.json"):
            f.unlink()
        result = create_policy_granted_execution_approval(
            session.session_id, "fixture-echo-v0", data_dir=tmp_path,
        )
        assert result["granted"] is False
        pol = load_execution_approval_policy("fixture-echo-v0", tmp_path)
        assert pol.uses_consumed == 0


# ---------------------------------------------------------------------------
# Architecture guard: no live_review.md dependency (R-0169 Step 2893)
# ---------------------------------------------------------------------------


class TestNoLiveReviewDependency:
    """Approval policy must not depend on .agent/live_review.md."""

    def test_no_live_review_in_policy_module(self):
        import inspect

        from packages.orchestration import execution_approval_policy as mod
        source = inspect.getsource(mod)
        assert "live_review" not in source
