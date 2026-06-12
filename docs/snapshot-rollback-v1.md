# Snapshot / Rollback Proof v1

**Scope:** Steps 1118-1133, 1136-1141  
**Status:** Production

---

## Purpose

Every repository mutation (apply) must have a verified pre-apply snapshot. No apply may proceed without one. Revert requires explicit invocation, verified snapshot integrity, and no post-apply drift.

This document covers the unified Repository Snapshot service that replaces fragmented, best-effort, memory-only snapshot approaches in `source_apply.py` and `patch_apply.py`.

---

## Design Invariants

1. **No raw content in public models.** `SnapshotEntry`, `RepositorySnapshot`, `DurableApplyRecord`, `SnapshotCreateResult`, `SnapshotVerification`, `RepositoryRevertResult` expose no file content, diff text, or secret material.
2. **Snapshot contents are private recovery material.** Blobs stored at `owner-only (0o600)` paths. Never returned to callers, emitted in events, or exposed through CLI.
3. **Apply BLOCKED if snapshot creation or verification fails.** No mutation without verified snapshot.
4. **No symlink following.** Snapshot creation and restore never traverse symlinks.
5. **No absolute paths stored.** All paths in manifests and records are relative.
6. **Bounded size.** 500 KB per file, 10 MiB total per snapshot.
7. **Revert BLOCKED if post-apply drift detected.** If a file changed after apply, revert blocked with `post_apply_drift`.
8. **Restore MUST be verified.** Each restored path checked against `before_sha256`.
9. **No Git reset/checkout/clean.** File restore uses private blobs only.
10. **No automatic revert.** `revert_repository_apply()` must be called explicitly.
11. **Existing snapshots never overwritten.** `FileExistsError` on `snap_dir.mkdir(exist_ok=False)`.

---

## Storage Layout

```
.data/workspaces/<job_id>/
  repository_snapshots/
    <snapshot_id>/
      manifest.json       (0o600 — metadata only, no raw content)
      blob_<sha256_32>.bin (0o600 — private recovery material)
  apply_records/
    <apply_id>.json        (0o600 — before/after proof hashes)
```

Directory permissions: `0o700` (owner-only).

---

## Public API

### Snapshot Creation

```python
from packages.orchestration.repository_snapshot import create_snapshot, verify_snapshot

result: SnapshotCreateResult = create_snapshot(
    job_id,       # str — job UUID string
    intent_id,    # str — intent or apply identifier
    path_set,     # list[str] — relative paths to snapshot
    repo_root,    # Path — repository root
    data_dir,     # Path | None
    apply_id="",  # str — optional apply identifier
)
# result.success must be True before proceeding
# result.snapshot_id is the snapshot to verify

verif: SnapshotVerification = verify_snapshot(snapshot_id, job_id, data_dir)
# verif.verified must be True before any mutation
```

**Apply MUST be blocked** if `result.success is False` or `verif.verified is False`.

### Path Set Derivation

```python
from packages.orchestration.repository_snapshot import build_snapshot_path_set

# From a StructuredPatch (file_ops + unified_diffs):
path_set = build_snapshot_path_set(patch)

# From a plain intent dict:
path_set = build_snapshot_path_set_from_intent({"target_path": "docs/guide.md"})
```

### Durable Apply Record

```python
from packages.orchestration.repository_snapshot import (
    save_durable_apply_record, load_durable_apply_record, DurableApplyRecord,
)

record = DurableApplyRecord(
    apply_id=apply_id,
    job_id=job_id,
    intent_id=intent_id,
    snapshot_id=snapshot_id,
    state="applied",
    target_paths=path_set,
    applied_at=datetime.now(timezone.utc).isoformat(),
    before_proof={...},  # {rel_path: {sha256, bytes, existed}}
    after_proof={...},   # populated after apply completes
    snapshot_verified=True,
)
save_durable_apply_record(record, job_id, data_dir)
```

### Explicit Revert

```python
from packages.orchestration.repository_snapshot import revert_repository_apply

result: RepositoryRevertResult = revert_repository_apply(
    job_id,
    apply_id,
    repo_root,
    data_dir,
)
# result.success True only on full verified revert
# result.block_reason set if blocked
# result.safe_summary is caller-safe
# No caller-supplied permission booleans (Step 1137).
# Service loads Job from storage and enforces Capability.repo_revert
# and ContractAction.REVERT internally.
```

---

## Revert Gate Order

1. Load apply record — `block_reason: no_apply_record`
2. Load snapshot — `block_reason: no_snapshot`
3a. Load Job from storage — `block_reason: permission_denied` (job not found)
3b. `is_allowed(job, Capability.repo_revert)` — `block_reason: permission_denied`
3c. `evaluate_run_action(contract, ContractAction.REVERT)` — `block_reason: contract_denied`
4. Re-verify snapshot integrity — `block_reason: verify_failed`
5. Post-apply drift check — `block_reason: post_apply_drift`
6. File restore from private blobs
7. Verify restored state (hash check per path)
8. Update snapshot + apply record state

No caller-supplied `permitted=` or `contract_allows_revert=` booleans (Step 1137).
Both `Capability.repo_revert` and `ContractAction.REVERT` are denied by default.

---

## Event Types (Step 1128)

All events: safe metadata only, no raw content.

| Event | When |
|-------|------|
| `snapshot_create_completed` | create_snapshot success |
| `snapshot_create_failed` | create_snapshot failure |
| `snapshot_verified` | verify_snapshot success |
| `snapshot_verify_failed` | verify_snapshot failure |
| `apply_record_saved` | save_durable_apply_record success |
| `revert_started` | revert_repository_apply entry |
| `revert_blocked` | any gate blocks revert |
| `revert_completed` | successful full revert |
| `revert_failed` | partial or failed revert |
| `snapshot_create_started` | (reserved) |

---

## CLI Commands

```bash
# Inspect snapshot metadata (no recovery content)
remedy snapshot inspect <job_id> <snapshot_id> [--json]

# List durable apply records
remedy snapshot list-applies <job_id> [--json]
```

---

## Integration Points

| Module | Change |
|--------|--------|
| `source_apply.py` | Mandatory snapshot before any mutation. Transactional rollback uses durable blobs. `FileSnapshot.content` removed. `ApplyResult.snapshot_id` + `.snapshot_verified` added. `revert_apply()` returns `RepositoryRevertResult` (Step 1140). |
| `patch_apply.py` | Mandatory snapshot replaces `store_pre_apply_snapshot()`. `DurableApplyRecord` saved after apply. `snapshot_id` + `snapshot_verified` in artifact apply record. Legacy snapshot call removed (Step 1141). |
| `apps/cli/commands/patch.py` | `patch.revert` routes through `revert_repository_apply()` (Step 1139). `apply_id` canonical; `intent_id` resolves via apply records. `--apply-id` opt added to catalog. |
| `run_contract.py` | `ContractAction.REVERT = "revert"` — default denied, requires explicit contract grant + approval (Step 1136). |
| `permissions.py` | `Capability.repo_revert` — default deny, actively enforced by `revert_repository_apply()` (Step 1138). |
| `repository_snapshot.py` | `revert_repository_apply()` loads Job from storage, enforces `repo_revert` capability and `REVERT` contract action internally. No caller-supplied permission booleans (Step 1137). |
| `command_catalog.py` | `snapshot` group. `snapshot.inspect` + `snapshot.list-applies` commands. `patch.revert` gains `--apply-id` opt. |

---

## Limitations (v1)

- Snapshot covers only paths listed in `path_set`. Directories not snapshotted.
- No cross-apply dependency tracking.
- No automatic snapshot expiry or cleanup.
- Post-apply drift check requires `after_proof` to be populated in `DurableApplyRecord`; unchecked paths are not drift-detected.
- `source_apply.py` `revert_apply()` signature changed — old `(snapshots, repo_path)` replaced by `(apply_id, repo_path, *, job_id, data_dir=None)`. Callers must update.
