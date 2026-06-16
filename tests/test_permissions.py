"""
Tests for packages/orchestration/permissions.py.

All tests are deterministic — no live Ollama, no filesystem access.
"""

from __future__ import annotations

import pytest

from packages.core.models import Job, RunState
from packages.orchestration.permissions import (
    Capability,
    effective_permissions,
    is_allowed,
    is_reserved,
    set_permission,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_job(**metadata_overrides) -> Job:
    """Build a minimal Job for permission tests."""
    job = Job(name="test", state=RunState.PENDING)
    job.metadata.update(metadata_overrides)
    return job


# ---------------------------------------------------------------------------
# Default permissions
# ---------------------------------------------------------------------------


class TestDefaultPermissions:
    def test_workspace_write_allowed_by_default(self):
        job = _make_job()
        assert is_allowed(job, Capability.workspace_write) is True

    def test_repo_generated_write_denied_by_default(self):
        job = _make_job()
        assert is_allowed(job, Capability.repo_generated_write) is False

    def test_repo_overwrite_denied_by_default(self):
        job = _make_job()
        assert is_allowed(job, Capability.repo_overwrite) is False

    def test_shell_exec_denied_by_default(self):
        job = _make_job()
        assert is_allowed(job, Capability.shell_exec) is False

    def test_defaults_apply_when_permissions_key_absent(self):
        """job.metadata has no 'permissions' key — all fall back to defaults."""
        job = _make_job()
        assert "permissions" not in job.metadata
        assert is_allowed(job, Capability.workspace_write) is True
        assert is_allowed(job, Capability.repo_generated_write) is False

    def test_defaults_apply_when_permissions_dict_is_empty(self):
        """Empty permissions dict also falls back to defaults."""
        job = _make_job(permissions={})
        assert is_allowed(job, Capability.workspace_write) is True
        assert is_allowed(job, Capability.repo_generated_write) is False


# ---------------------------------------------------------------------------
# set_permission
# ---------------------------------------------------------------------------


class TestSetPermission:
    def test_allow_sets_allow_in_metadata(self):
        job = _make_job()
        set_permission(job, Capability.repo_generated_write, allow=True)
        assert job.metadata["permissions"]["repo_generated_write"] == "allow"

    def test_deny_sets_deny_in_metadata(self):
        job = _make_job()
        set_permission(job, Capability.repo_generated_write, allow=False)
        assert job.metadata["permissions"]["repo_generated_write"] == "deny"

    def test_set_permission_creates_permissions_key_if_absent(self):
        job = _make_job()
        assert "permissions" not in job.metadata
        set_permission(job, Capability.repo_generated_write, allow=True)
        assert "permissions" in job.metadata

    def test_set_permission_preserves_other_capabilities(self):
        job = _make_job()
        set_permission(job, Capability.workspace_write, allow=False)
        set_permission(job, Capability.repo_generated_write, allow=True)
        assert job.metadata["permissions"]["workspace_write"] == "deny"
        assert job.metadata["permissions"]["repo_generated_write"] == "allow"

    def test_deny_then_allow_overrides(self):
        job = _make_job()
        set_permission(job, Capability.repo_generated_write, allow=False)
        set_permission(job, Capability.repo_generated_write, allow=True)
        assert job.metadata["permissions"]["repo_generated_write"] == "allow"

    def test_allow_then_deny_overrides(self):
        job = _make_job()
        set_permission(job, Capability.workspace_write, allow=True)
        set_permission(job, Capability.workspace_write, allow=False)
        assert job.metadata["permissions"]["workspace_write"] == "deny"


# ---------------------------------------------------------------------------
# is_allowed — override behaviour
# ---------------------------------------------------------------------------


class TestIsAllowed:
    def test_explicit_allow_overrides_default_deny(self):
        """repo_generated_write is denied by default; explicit allow grants it."""
        job = _make_job()
        set_permission(job, Capability.repo_generated_write, allow=True)
        assert is_allowed(job, Capability.repo_generated_write) is True

    def test_explicit_deny_overrides_default_allow(self):
        """workspace_write is allowed by default; explicit deny revokes it."""
        job = _make_job()
        set_permission(job, Capability.workspace_write, allow=False)
        assert is_allowed(job, Capability.workspace_write) is False

    def test_allow_stored_in_pre_populated_metadata(self):
        """Metadata supplied at job construction is respected."""
        job = _make_job(permissions={"repo_generated_write": "allow"})
        assert is_allowed(job, Capability.repo_generated_write) is True

    def test_deny_stored_in_pre_populated_metadata(self):
        job = _make_job(permissions={"workspace_write": "deny"})
        assert is_allowed(job, Capability.workspace_write) is False

    def test_unrecognised_metadata_value_is_not_allow(self):
        """Only the string 'allow' grants permission — anything else is treated as deny."""
        job = _make_job(permissions={"repo_generated_write": "yes"})
        assert is_allowed(job, Capability.repo_generated_write) is False


# ---------------------------------------------------------------------------
# is_reserved
# ---------------------------------------------------------------------------


class TestIsReserved:
    def test_repo_overwrite_is_reserved(self):
        assert is_reserved(Capability.repo_overwrite) is True

    def test_shell_exec_is_reserved(self):
        assert is_reserved(Capability.shell_exec) is True

    def test_workspace_write_is_not_reserved(self):
        assert is_reserved(Capability.workspace_write) is False

    def test_repo_generated_write_is_not_reserved(self):
        assert is_reserved(Capability.repo_generated_write) is False

    def test_repo_revert_is_not_reserved(self):
        """repo_revert is actively enforced at runtime (Step 1138)."""
        assert is_reserved(Capability.repo_revert) is False


# ---------------------------------------------------------------------------
# repo_revert (Step 1138)
# ---------------------------------------------------------------------------


class TestRepoRevert:
    def test_repo_revert_denied_by_default(self):
        job = _make_job()
        assert is_allowed(job, Capability.repo_revert) is False

    def test_repo_revert_can_be_granted(self):
        job = _make_job()
        set_permission(job, Capability.repo_revert, allow=True)
        assert is_allowed(job, Capability.repo_revert) is True

    def test_repo_revert_can_be_denied_explicitly(self):
        job = _make_job(permissions={"repo_revert": "allow"})
        set_permission(job, Capability.repo_revert, allow=False)
        assert is_allowed(job, Capability.repo_revert) is False

    def test_repo_revert_is_active_not_reserved(self):
        rows = effective_permissions(_make_job())
        row = next(r for r in rows if r["capability"] == "repo_revert")
        assert row["status"] == "active"
        assert row["effective"] == "deny"


# ---------------------------------------------------------------------------
# effective_permissions
# ---------------------------------------------------------------------------


class TestEffectivePermissions:
    def test_returns_all_capabilities(self):
        job = _make_job()
        rows = effective_permissions(job)
        names = {r["capability"] for r in rows}
        assert names == {
            "workspace_write",
            "repo_generated_write",
            "repo_test_run",
            "repo_overwrite",
            "shell_exec",
            "repo_revert",
        }

    def test_default_effective_state(self):
        job = _make_job()
        by_cap = {r["capability"]: r for r in effective_permissions(job)}
        assert by_cap["workspace_write"]["effective"] == "allow"
        assert by_cap["repo_generated_write"]["effective"] == "deny"
        assert by_cap["repo_overwrite"]["effective"] == "deny"
        assert by_cap["shell_exec"]["effective"] == "deny"
        assert by_cap["repo_revert"]["effective"] == "deny"

    def test_reserved_capabilities_have_reserved_status(self):
        job = _make_job()
        by_cap = {r["capability"]: r for r in effective_permissions(job)}
        assert by_cap["repo_overwrite"]["status"] == "reserved"
        assert by_cap["shell_exec"]["status"] == "reserved"

    def test_active_capabilities_have_active_status(self):
        job = _make_job()
        by_cap = {r["capability"]: r for r in effective_permissions(job)}
        assert by_cap["workspace_write"]["status"] == "active"
        assert by_cap["repo_generated_write"]["status"] == "active"
        assert by_cap["repo_revert"]["status"] == "active"

    def test_explicit_allow_reflected_in_effective(self):
        job = _make_job()
        set_permission(job, Capability.repo_generated_write, allow=True)
        by_cap = {r["capability"]: r for r in effective_permissions(job)}
        assert by_cap["repo_generated_write"]["effective"] == "allow"

    def test_explicit_deny_reflected_in_effective(self):
        job = _make_job()
        set_permission(job, Capability.workspace_write, allow=False)
        by_cap = {r["capability"]: r for r in effective_permissions(job)}
        assert by_cap["workspace_write"]["effective"] == "deny"


# ---------------------------------------------------------------------------
# Capability enum validation
# ---------------------------------------------------------------------------


class TestCapabilityEnum:
    def test_capability_values_are_strings(self):
        for cap in Capability:
            assert isinstance(cap.value, str)

    def test_invalid_capability_raises_value_error(self):
        with pytest.raises(ValueError):
            Capability("nonexistent_capability")

    def test_all_capabilities_exist(self):
        values = {c.value for c in Capability}
        assert values == {
            "workspace_write",
            "repo_generated_write",
            "repo_test_run",
            "repo_overwrite",
            "shell_exec",
            "repo_revert",
        }
