"""
Permission Model v1 for Remedy.

Capabilities represent distinct execution actions that Remedy may perform.
Each capability has a conservative default (deny unless otherwise specified).
Job-level permission overrides are stored in job.metadata["permissions"] as
a mapping of capability name → "allow" | "deny".

Defined capabilities:
  workspace_write      — write files into the Remedy-owned workspace directory.
                         Allowed by default for local task execution.
                         ACTIVE: enforced in the CLI before workspace materialization.
  repo_generated_write — write generated documentation/markdown into a user-
                         attached target repository. Denied by default (opt-in).
                         ACTIVE: enforced by check_and_apply_to_repo().
  repo_test_run        — execute a discovered test command inside the attached
                         target repository. Denied by default (opt-in).
                         ACTIVE: enforced by _cmd_run_tests_local() in the CLI.
                         Command is selected by command_discovery.py (not Python-only).
                         No shell=True. High-risk candidates are refused.
  repo_overwrite       — overwrite existing files in the attached repo. Denied
                         by default. RESERVED: configurable but not yet enforced
                         at runtime. Setting it has no effect in this version.
  shell_exec           — execute arbitrary shell commands. Denied by default.
                         RESERVED: configurable but not yet enforced at runtime.
                         Setting it has no effect in this version.
  repo_revert          — revert an applied repository mutation using a verified
                         pre-apply snapshot. Denied by default (opt-in).
                         ACTIVE: enforced by revert_repository_apply() in
                         repository_snapshot.py (Step 1138).

Usage:
  from packages.orchestration.permissions import (
      Capability, is_allowed, is_reserved, set_permission, effective_permissions
  )

  # Check
  if is_allowed(job, Capability.repo_generated_write):
      ...

  # Inspect reserved status
  if is_reserved(Capability.repo_overwrite):
      ...

  # Configure
  set_permission(job, Capability.repo_generated_write, allow=True)
  save_job(job)

  # Display all effective permissions
  for row in effective_permissions(job):
      print(row["capability"], row["effective"], row["status"])
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from packages.core.models import Job


class Capability(str, Enum):
    """Named execution capabilities controlled by the permission model."""

    workspace_write = "workspace_write"
    repo_generated_write = "repo_generated_write"
    repo_test_run = "repo_test_run"
    repo_overwrite = "repo_overwrite"
    shell_exec = "shell_exec"
    repo_revert = "repo_revert"


# Conservative defaults: only workspace_write is allowed without an explicit grant.
_DEFAULTS: dict[str, bool] = {
    "workspace_write": True,
    "repo_generated_write": False,
    "repo_test_run": False,
    "repo_overwrite": False,
    "shell_exec": False,
    "repo_revert": False,
}

# Capabilities that are configurable today but not yet enforced at runtime.
# Setting a reserved capability is persisted and visible in show-permissions,
# but no execution callsite consults it — granting it has no operational effect.
#
# Rules for this set:
#   - Add a capability here when it is defined but has no enforcement callsite yet.
#   - Remove a capability here only when an enforcement callsite is added.
#   - Never treat a reserved capability as granted just because it is set in metadata;
#     always verify is_reserved() is False before relying on is_allowed() at a new site.
_RESERVED: frozenset[str] = frozenset({"repo_overwrite", "shell_exec"})


def is_allowed(job: Job, capability: Capability) -> bool:
    """Return True if the capability is allowed for this job.

    Reads the job-level override from job.metadata["permissions"][capability.value].
    If no override is set, falls back to _DEFAULTS (conservative deny by default).
    """
    overrides: dict[str, str] = job.metadata.get("permissions", {})
    if capability.value in overrides:
        return overrides[capability.value] == "allow"
    return _DEFAULTS.get(capability.value, False)


def set_permission(job: Job, capability: Capability, *, allow: bool) -> None:
    """Set a capability permission on a job.

    Mutates job.metadata["permissions"] in place.  The caller is responsible
    for persisting the job afterwards.

    Args:
        job:        The job to update.
        capability: The capability to configure.
        allow:      True to grant, False to explicitly deny.
    """
    if "permissions" not in job.metadata:
        job.metadata["permissions"] = {}
    job.metadata["permissions"][capability.value] = "allow" if allow else "deny"


def is_reserved(capability: Capability) -> bool:
    """Return True if the capability is defined but not yet enforced at runtime.

    Reserved capabilities can be configured (set_permission persists the setting),
    but no code path checks them during execution.  The setting has no effect in
    the current version.
    """
    return capability.value in _RESERVED


def effective_permissions(job: Job) -> list[dict]:
    """Return the effective permission state for all capabilities.

    Each entry in the returned list is a dict with:
      capability: str   — capability name
      effective:  str   — "allow" or "deny" (incorporating defaults and overrides)
      status:     str   — "active" (enforced at runtime) or "reserved" (not yet enforced)

    Suitable for display in CLI commands such as show-permissions.
    """
    return [
        {
            "capability": cap.value,
            "effective": "allow" if is_allowed(job, cap) else "deny",
            "status": "reserved" if is_reserved(cap) else "active",
        }
        for cap in Capability
    ]
