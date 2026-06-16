"""Architecture guards for snapshot/revert system.

Step 1152: Enforce invariants that must never be violated:
- No shell=True in snapshot/revert code paths
- revert_repository_apply() has no caller-supplied permission bypass params
- No raw blob content in public result types
- DurableApplyRecord.state is the authority for revert state
- snapshot_verified comes from DurableApplyRecord, not raw blob
"""

from __future__ import annotations

import inspect

# ---------------------------------------------------------------------------
# Guard: No shell=True in snapshot/revert code paths
# ---------------------------------------------------------------------------


class TestNoShellTrue:

    def test_repository_snapshot_no_shell_true(self):
        from packages.orchestration import repository_snapshot
        src = inspect.getsource(repository_snapshot)
        assert "shell=True" not in src

    def test_source_apply_no_shell_true(self):
        from packages.orchestration import source_apply
        src = inspect.getsource(source_apply)
        assert "shell=True" not in src

    def test_patch_apply_no_shell_true(self):
        from packages.orchestration import patch_apply
        src = inspect.getsource(patch_apply)
        assert "shell=True" not in src

    def test_snapshot_cmds_no_shell_true(self):
        from apps.cli.commands import snapshot_cmds
        src = inspect.getsource(snapshot_cmds)
        assert "shell=True" not in src

    def test_patch_cmd_no_shell_true(self):
        from apps.cli.commands import patch
        src = inspect.getsource(patch)
        assert "shell=True" not in src


# ---------------------------------------------------------------------------
# Guard: No caller-supplied permission bypass in revert_repository_apply
# ---------------------------------------------------------------------------


class TestRevertNoBypasParams:

    def test_revert_no_permitted_param(self):
        """revert_repository_apply() must not accept 'permitted' bypass param."""
        from packages.orchestration.repository_snapshot import revert_repository_apply
        sig = inspect.signature(revert_repository_apply)
        assert "permitted" not in sig.parameters

    def test_revert_no_contract_allows_param(self):
        """revert_repository_apply() must not accept 'contract_allows_revert' bypass param."""
        from packages.orchestration.repository_snapshot import revert_repository_apply
        sig = inspect.signature(revert_repository_apply)
        assert "contract_allows_revert" not in sig.parameters

    def test_revert_source_loads_job_from_storage(self):
        """revert_repository_apply() must reference load_job (loads from storage)."""
        from packages.orchestration import repository_snapshot
        src = inspect.getsource(repository_snapshot.revert_repository_apply)
        assert "_load_job" in src or "load_job" in src

    def test_revert_source_checks_capability(self):
        """revert_repository_apply() must check is_allowed / repo_revert capability."""
        from packages.orchestration import repository_snapshot
        src = inspect.getsource(repository_snapshot.revert_repository_apply)
        assert "repo_revert" in src or "_is_allowed" in src


# ---------------------------------------------------------------------------
# Guard: No raw content in public result types
# ---------------------------------------------------------------------------


class TestNoRawContentInResults:

    def test_repository_revert_result_has_no_content_field(self):
        """RepositoryRevertResult must not expose raw file content."""
        from packages.orchestration.repository_snapshot import RepositoryRevertResult
        fields = {f.name for f in RepositoryRevertResult.__dataclass_fields__.values()}
        for forbidden in ("content", "diff", "blob", "raw", "source", "stdout", "stderr"):
            assert forbidden not in fields, f"Forbidden field '{forbidden}' in RepositoryRevertResult"

    def test_snapshot_create_result_has_no_content_field(self):
        """SnapshotCreateResult must not expose raw file content."""
        from packages.orchestration.repository_snapshot import SnapshotCreateResult
        fields = {f.name for f in SnapshotCreateResult.__dataclass_fields__.values()}
        for forbidden in ("content", "diff", "blob", "raw", "source"):
            assert forbidden not in fields, f"Forbidden field '{forbidden}' in SnapshotCreateResult"

    def test_snapshot_verification_has_no_content_field(self):
        """SnapshotVerification must not expose raw file content."""
        from packages.orchestration.repository_snapshot import SnapshotVerification
        fields = {f.name for f in SnapshotVerification.__dataclass_fields__.values()}
        for forbidden in ("content", "diff", "blob", "raw", "source"):
            assert forbidden not in fields, f"Forbidden field '{forbidden}' in SnapshotVerification"

    def test_durable_apply_record_has_no_content_field(self):
        """DurableApplyRecord must not store raw file content."""
        from packages.orchestration.repository_snapshot import DurableApplyRecord
        fields = {f.name for f in DurableApplyRecord.__dataclass_fields__.values()}
        for forbidden in ("content", "diff", "raw_source", "stdout", "stderr"):
            assert forbidden not in fields, f"Forbidden field '{forbidden}' in DurableApplyRecord"


# ---------------------------------------------------------------------------
# Guard: ContractAction.REVERT and Capability.repo_revert are denied by default
# ---------------------------------------------------------------------------


class TestDefaultDenyInvariants:

    def test_revert_action_in_default_denied(self):
        """ContractAction.REVERT must be denied by default in run contract."""
        from packages.orchestration.run_contract import _DEFAULT_DENIED_ACTIONS, ContractAction
        assert ContractAction.REVERT in _DEFAULT_DENIED_ACTIONS

    def test_revert_action_requires_approval(self):
        """ContractAction.REVERT must require approval."""
        from packages.orchestration.run_contract import _DEFAULT_REQUIRES_APPROVAL, ContractAction
        assert ContractAction.REVERT in _DEFAULT_REQUIRES_APPROVAL

    def test_repo_revert_denied_by_default(self):
        """Capability.repo_revert must be denied by default."""
        from packages.core.models import Job, RunState
        from packages.orchestration.permissions import Capability, is_allowed
        job = Job(name="test", state=RunState.PENDING)
        assert is_allowed(job, Capability.repo_revert) is False

    def test_repo_revert_not_reserved(self):
        """Capability.repo_revert must be actively enforced (not reserved/skipped)."""
        from packages.orchestration.permissions import Capability, is_reserved
        assert is_reserved(Capability.repo_revert) is False


# ---------------------------------------------------------------------------
# Guard: No git reset/checkout/clean in snapshot code
# ---------------------------------------------------------------------------


class TestNoGitDestructiveOps:

    def test_no_git_reset_in_snapshot(self):
        from packages.orchestration import repository_snapshot
        src = inspect.getsource(repository_snapshot)
        assert "git reset" not in src
        assert "git checkout" not in src
        assert "git clean" not in src

    def test_no_git_reset_in_source_apply(self):
        from packages.orchestration import source_apply
        src = inspect.getsource(source_apply)
        assert "git reset" not in src
        assert "git checkout" not in src


# ---------------------------------------------------------------------------
# Guard: snapshot_verified flows from artifact metadata (not raw blob)
# ---------------------------------------------------------------------------


class TestSnapshotVerifiedFlowGuard:

    def test_proof_chain_reads_snapshot_verified_from_proof_info(self):
        """_classify_proof_status accepts snapshot_verified parameter (Step 1145)."""
        from packages.orchestration.proof_chain import _classify_proof_status
        sig = inspect.signature(_classify_proof_status)
        assert "snapshot_verified" in sig.parameters

    def test_derive_missing_links_checks_snapshot_verified(self):
        """_derive_missing_links accepts snapshot_verified parameter (Step 1145)."""
        from packages.orchestration.proof_chain import _derive_missing_links
        sig = inspect.signature(_derive_missing_links)
        assert "snapshot_verified" in sig.parameters

    def test_file_provenance_accepts_data_dir_for_authoritative_state(self):
        """build_file_provenance accepts data_dir for DurableApplyRecord lookup (Step 1146)."""
        from packages.orchestration.file_provenance import build_file_provenance
        sig = inspect.signature(build_file_provenance)
        assert "data_dir" in sig.parameters
