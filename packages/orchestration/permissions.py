"""
Permission Model v1 for Remedy.

Capabilities represent distinct execution actions that Remedy may perform.
Each capability has a conservative default (deny unless otherwise specified).
Job-level permission overrides are stored in job.metadata["permissions"] as
a mapping of capability name → "allow" | "deny".

Defined capabilities:
  workspace_write      — write files into the Remedy-owned workspace directory.
                         Allowed by default for local task execution.
  repo_generated_write — write generated documentation/markdown into a user-
                         attached target repository. Denied by default (opt-in).
  repo_overwrite       — overwrite existing files in the attached repo. Denied
                         by default. Reserved for a future step; currently has
                         no effect even if granted.
  shell_exec           — execute arbitrary shell commands. Denied by default.
                         Reserved for a future step; currently unused.

Usage:
  from packages.orchestration.permissions import Capability, is_allowed, set_permission

  # Check
  if is_allowed(job, Capability.repo_generated_write):
      ...

  # Configure
  set_permission(job, Capability.repo_generated_write, allow=True)
  save_job(job)
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
    repo_overwrite = "repo_overwrite"
    shell_exec = "shell_exec"


# Conservative defaults: only workspace_write is allowed without an explicit grant.
_DEFAULTS: dict[str, bool] = {
    "workspace_write": True,
    "repo_generated_write": False,
    "repo_overwrite": False,
    "shell_exec": False,
}


def is_allowed(job: "Job", capability: Capability) -> bool:
    """Return True if the capability is allowed for this job.

    Reads the job-level override from job.metadata["permissions"][capability.value].
    If no override is set, falls back to _DEFAULTS (conservative deny by default).
    """
    overrides: dict[str, str] = job.metadata.get("permissions", {})
    if capability.value in overrides:
        return overrides[capability.value] == "allow"
    return _DEFAULTS.get(capability.value, False)


def set_permission(job: "Job", capability: Capability, *, allow: bool) -> None:
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
