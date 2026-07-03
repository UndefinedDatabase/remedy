"""Execution config evidence — records how Remedy was configured when it ran."""
from __future__ import annotations

from datetime import datetime, timezone

_ROLES = ("builder", "reviewer", "repair")


def build_execution_config_evidence(
    job_id: str,
    step_range: str,
    role_configs: dict,
    cli_args: dict | None = None,
    source_root: str = "",
    config_source: str = "defaults",
    observed_invocation_args: dict | None = None,
) -> dict:
    """Return a structured evidence dict capturing the resolved configuration.

    ``cli_args`` are treated as *configured* invocation args (planned, not
    proof of an actual call). ``observed_invocation_args`` are the args the
    provider actually exposed from its output; only these populate
    ``actual_invocation_args``. When no provider-observed args are supplied,
    ``actual_invocation_args`` is ``None`` and ``actual_invocation_observed``
    is ``False`` so a final verifier cannot treat configured args as proof.
    """
    resolved_at = datetime.now(timezone.utc).isoformat()
    cli = cli_args or {}

    result: dict = {
        "schema_version": 1,
        "source_root": source_root,
        "job_id": job_id,
        "step_range": step_range,
        "resolved_at": resolved_at,
        "config_source": config_source,
        "environment_source": "cli",
    }

    for role in _ROLES:
        rc = role_configs.get(role, {})
        result[f"{role}_provider"] = rc.get("provider", None)
        result[f"{role}_model"] = rc.get("model", None)
        result[f"{role}_effort"] = rc.get("effort", None)
        result[f"{role}_actual_provider"] = None
        result[f"{role}_actual_model"] = None

    result["fallback_models"] = []
    result["provider_cli_args"] = dict(cli)
    result["configured_invocation_args"] = dict(cli)
    if observed_invocation_args is not None:
        result["actual_invocation_args"] = dict(observed_invocation_args)
        result["actual_invocation_observed"] = True
    else:
        result["actual_invocation_args"] = None
        result["actual_invocation_observed"] = False
    result["per_role_invocation_args"] = dict(cli.get("per_role", {})) if isinstance(cli.get("per_role"), dict) else {}
    result["warnings"] = []
    result["mismatch_findings"] = []
    result["unknown_fields"] = []
    result["actual_config_available"] = False
    result["evidence_status"] = "recorded"

    return result
