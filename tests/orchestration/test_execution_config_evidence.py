"""Tests for execution_config_evidence — config snapshot recording."""
from __future__ import annotations

from datetime import datetime, timezone

from packages.orchestration.execution_config_evidence import (
    build_execution_config_evidence,
)

_ROLE_CONFIGS = {
    "builder": {"provider": "claude", "model": "opus", "effort": "high"},
    "reviewer": {"provider": "ollama", "model": "qwen3", "effort": "medium"},
    "repair": {"provider": "fake", "model": "test", "effort": "low"},
}


def _build(**overrides):
    defaults = {
        "job_id": "job-001",
        "step_range": "5000-5050",
        "role_configs": _ROLE_CONFIGS,
    }
    defaults.update(overrides)
    return build_execution_config_evidence(**defaults)


def test_schema_version():
    ev = _build()
    assert ev["schema_version"] == 1


def test_source_root_recorded():
    ev = _build(source_root="/home/user/project")
    assert ev["source_root"] == "/home/user/project"


def test_job_id_and_step_range():
    ev = _build(job_id="job-xyz", step_range="100-200")
    assert ev["job_id"] == "job-xyz"
    assert ev["step_range"] == "100-200"


def test_per_role_config_recorded():
    ev = _build()
    assert ev["builder_provider"] == "claude"
    assert ev["builder_model"] == "opus"
    assert ev["builder_effort"] == "high"
    assert ev["reviewer_provider"] == "ollama"
    assert ev["reviewer_model"] == "qwen3"
    assert ev["reviewer_effort"] == "medium"
    assert ev["repair_provider"] == "fake"
    assert ev["repair_model"] == "test"
    assert ev["repair_effort"] == "low"


def test_actual_fields_null_when_unavailable():
    ev = _build()
    for role in ("builder", "reviewer", "repair"):
        assert ev[f"{role}_actual_provider"] is None
        assert ev[f"{role}_actual_model"] is None


def test_actual_config_available_false():
    ev = _build()
    assert ev["actual_config_available"] is False


def test_warnings_empty_by_default():
    ev = _build()
    assert ev["warnings"] == []


def test_mismatch_findings_empty_by_default():
    ev = _build()
    assert ev["mismatch_findings"] == []


def test_resolved_at_is_utc_timestamp():
    ev = _build()
    ts = ev["resolved_at"]
    parsed = datetime.fromisoformat(ts)
    assert parsed.tzinfo is not None
    assert parsed.tzinfo == timezone.utc


def test_cli_args_recorded():
    cli = {"provider": "claude", "model": "opus"}
    ev = _build(cli_args=cli)
    assert ev["provider_cli_args"] == {"provider": "claude", "model": "opus"}
    # CLI args are configured, not proof of an actual invocation.
    assert ev["configured_invocation_args"] == {"provider": "claude", "model": "opus"}


def test_configured_args_do_not_populate_actual():
    cli = {"provider": "claude", "model": "opus"}
    ev = _build(cli_args=cli)
    assert ev["actual_invocation_args"] is None
    assert ev["actual_invocation_observed"] is False


def test_actual_invocation_observed_false_by_default():
    ev = _build()
    assert ev["actual_invocation_observed"] is False
    assert ev["actual_invocation_args"] is None


def test_actual_invocation_args_when_observed():
    observed = {"provider": "claude", "model": "opus", "tokens": 1234}
    ev = _build(observed_invocation_args=observed)
    assert ev["actual_invocation_args"] == observed
    assert ev["actual_invocation_observed"] is True


def test_configured_and_actual_separation_maintained():
    cli = {"provider": "claude", "model": "opus"}
    observed = {"provider": "claude", "model": "opus-actual"}
    ev = _build(cli_args=cli, observed_invocation_args=observed)
    assert ev["configured_invocation_args"] == cli
    assert ev["actual_invocation_args"] == observed
    assert ev["configured_invocation_args"] != ev["actual_invocation_args"]


def test_no_cross_contamination_between_configured_and_actual():
    cli = {"provider": "claude"}
    observed = {"provider": "ollama"}
    ev = _build(cli_args=cli, observed_invocation_args=observed)
    # mutating the returned actual dict must not leak into configured
    ev["actual_invocation_args"]["provider"] = "mutated"
    assert ev["configured_invocation_args"]["provider"] == "claude"


def test_configured_vs_actual_model_separation():
    ev = _build()
    for role in ("builder", "reviewer", "repair"):
        # configured model present, actual model null until observed
        assert ev[f"{role}_model"] is not None
        assert ev[f"{role}_actual_model"] is None


def test_actual_invocation_args_field_always_present():
    ev = _build()
    assert "actual_invocation_args" in ev
    assert "configured_invocation_args" in ev
    assert "actual_invocation_observed" in ev
