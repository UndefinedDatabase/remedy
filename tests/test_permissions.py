"""
Tests for packages/orchestration/permissions.py.

All tests are deterministic — no live Ollama, no filesystem access.
"""

from __future__ import annotations

import pytest

from packages.core.models import Job, RunState
from packages.orchestration.permissions import Capability, is_allowed, set_permission


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
# Capability enum validation
# ---------------------------------------------------------------------------


class TestCapabilityEnum:
    def test_capability_values_are_strings(self):
        for cap in Capability:
            assert isinstance(cap.value, str)

    def test_invalid_capability_raises_value_error(self):
        with pytest.raises(ValueError):
            Capability("nonexistent_capability")

    def test_all_four_capabilities_exist(self):
        values = {c.value for c in Capability}
        assert values == {
            "workspace_write",
            "repo_generated_write",
            "repo_overwrite",
            "shell_exec",
        }
