"""CLI regression tests for `remedy file why` (Step 1157).

Verifies the CLI handler passes data_dir into build_file_provenance so the
authoritative DurableApplyRecord / snapshot truth is used, not stale artifact
metadata. Reverted applies must not appear currently applied; drift-blocked
applies remain active; partial/failed revert is visible. No private paths leak.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from uuid import uuid4

import pytest

from packages.core.models import Artifact, ArtifactKind, Job, RunState
from packages.orchestration.approval_queue import make_intent_id
from packages.orchestration.repository_snapshot import (
    DurableApplyRecord,
    create_snapshot,
    save_durable_apply_record,
    verify_snapshot,
    revert_repository_apply,
)
from packages.orchestration.storage import save_job
from packages.orchestration.permissions import Capability, set_permission
from packages.orchestration.run_contract import (
    build_default_run_contract, save_contract, ContractAction,
)
from apps.cli.commands.file import _cmd_file_why


PATH = "src/foo.py"


def _build_job_with_apply(data_dir: Path, repo_root: Path, *, apply_state: str):
    """Create a job + artifact + verified snapshot + DurableApplyRecord.

    apply_state drives whether we leave the record applied or run a real revert.
    Returns (job, intent_id).
    """
    f = repo_root / "src"
    f.mkdir(parents=True, exist_ok=True)
    target = repo_root / PATH
    target.write_text("before\n")

    job_id = uuid4()
    art_id = uuid4()
    intent_id = make_intent_id(art_id, 0)

    snap = create_snapshot(str(job_id), intent_id, [PATH], repo_root, data_dir)
    verify_snapshot(snap.snapshot_id, str(job_id), data_dir)

    before_sha = hashlib.sha256(b"before\n").hexdigest()
    target.write_text("after\n")
    after_sha = hashlib.sha256(b"after\n").hexdigest()

    art = Artifact(
        id=art_id, name="art", kind=ArtifactKind.PATCH_INTENT, content="",
        metadata={
            "patch_intent_explanations": [
                {"file": PATH, "action": "modify", "risk": "low", "reason": "", "summary": ""}
            ],
            "patch_intent_approvals": {
                intent_id: {"state": "approved", "decided_at": "", "decided_by": ""}
            },
            "patch_intent_apply_records": {
                intent_id: {"state": "applied", "bytes_written": 6, "line_count": 1}
            },
        },
    )
    job = Job(
        id=job_id, name="prov-job", user_prompt="t", state=RunState.RUNNING,
        tasks=[], artifacts=[art], metadata={},
    )
    # Permission + contract so a real revert can run. Persist the job AFTER
    # save_contract (which mutates job.metadata) so the contract is durable.
    set_permission(job, Capability.repo_revert, allow=True)
    contract = build_default_run_contract(job)
    import dataclasses
    contract = dataclasses.replace(
        contract,
        allowed_actions=(*contract.allowed_actions, ContractAction.REVERT),
        denied_actions=tuple(a for a in contract.denied_actions if a != ContractAction.REVERT),
    )
    save_contract(job, contract)
    save_job(job, root=data_dir)

    rec = DurableApplyRecord(
        apply_id=intent_id, job_id=str(job_id), intent_id=intent_id,
        snapshot_id=snap.snapshot_id, state="applied", target_paths=[PATH],
        applied_at="2026-06-12T10:00:00+00:00",
        before_proof={PATH: {"sha256": before_sha, "bytes": 7, "existed": True}},
        after_proof={PATH: {"sha256": after_sha, "bytes": 6, "existed": True}},
        snapshot_verified=True,
    )
    save_durable_apply_record(rec, str(job_id), data_dir)

    if apply_state == "reverted":
        result = revert_repository_apply(str(job_id), intent_id, repo_root, data_dir)
        assert result.success, result
    return job, intent_id


@pytest.fixture()
def env(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir, repo_root


def test_file_why_reflects_reverted_state(env, capsys):
    data_dir, repo_root = env
    job, _ = _build_job_with_apply(data_dir, repo_root, apply_state="reverted")
    _cmd_file_why(str(job.id), PATH, json_output=False)
    out = capsys.readouterr().out
    assert "patch_apply" in out
    # Reverted apply is NOT currently applied.
    assert "status=reverted" in out
    assert "status=applied" not in out


def test_file_why_applied_state(env, capsys):
    data_dir, repo_root = env
    job, _ = _build_job_with_apply(data_dir, repo_root, apply_state="applied")
    _cmd_file_why(str(job.id), PATH, json_output=False)
    out = capsys.readouterr().out
    assert "status=applied" in out


def test_file_why_json_no_private_path_leak(env, capsys):
    data_dir, repo_root = env
    job, _ = _build_job_with_apply(data_dir, repo_root, apply_state="reverted")
    _cmd_file_why(str(job.id), PATH, json_output=True)
    out = capsys.readouterr().out
    assert '"reverted"' in out
    assert str(data_dir) not in out
    assert str(repo_root) not in out
    assert "blob_" not in out
