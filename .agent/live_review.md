# Live Review — Steps 1135-1154

Reviewer: parallel reviewer
Scope: Canonical Revert + Proof/Provenance/Readiness Integration
Timestamp: 2026-06-12
Last check: 2026-06-12 — Baseline assessment complete, auto-review loop starting

## Verdict
PENDING — Baseline assessment complete. 9 blockers identified. Worker has not started (no new branch).

## Prior Block Status
- Steps 940-974: PASS
- Steps 975-994: PASS
- Steps 995-1009: PASS
- Steps 1010-1029: PASS WITH RISKS
- Steps 1030-1044: PASS WITH RISKS
- Steps 1045-1064: PASS
- Steps 1065-1084: PASS WITH RISKS
- Steps 1085-1109: PASS WITH RISKS
- Steps 1110-1134: PASS WITH RISKS (R-0051/R-0052 carry-forward, Steps 1130-1132 deferred)

## Block-If Condition Tracker

| # | Block-If Condition | Status | Finding | Fix Step |
|---|---|---|---|---|
| 1 | .agent state claims deferred steps completed | NOT YET TESTABLE | — | 1135 |
| 2 | patch.revert routes through legacy patch_revert | OPEN | R-0053 | — |
| 3 | central revert trusts caller-supplied permitted=True | OPEN | R-0054 | — |
| 4 | permission or contract not enforced inside revert service | OPEN | R-0054 | — |
| 5 | revert action absent from canonical RunContract vocabulary | OPEN | R-0055 | — |
| 6 | permission alone or contract alone sufficient | OPEN | R-0054 | — |
| 7 | patch_apply writes duplicate legacy snapshots | OPEN | R-0056 | — |
| 8 | legacy snapshots silently reverted through weaker behavior | OPEN | R-0053 | — |
| 9 | event persistence failure silently ignored | OPEN | R-0057 | — |
| 10 | failed/partial revert marks apply as successfully reverted | NOT FOUND | — | — |
| 11 | Proof Chain verifies apply without verified snapshot proof | OPEN | R-0058 | — |
| 12 | reverted files appear currently applied in File Provenance | OPEN | R-0059 | — |
| 13 | readiness accepts events without verifying manifest/blobs/linkage | OPEN | R-0060 | — |
| 14 | Review Bundle exposes recovery blobs/private paths | NOT YET TESTABLE | — | — |
| 15 | drift protection or restore verification weakened | NOT FOUND | — | — |
| 16 | force revert or destructive Git command introduced | NOT FOUND | — | — |
| 17 | raw source/diff/snapshot/output/secrets/tracebacks leak | NOT FOUND | — | — |
| 18 | final handoff lacks changed files table | NOT YET TESTABLE | — | 1154 |
| 19 | latest review verdict PENDING while merge-ready claimed | NOT YET TESTABLE | — | 1154 |

## Finding Ledger

### Carry-forward from Steps 1110-1134

### R-0051: _emit() still uses except Exception: pass for non-finalization events (LOW)

- **Status**: Open (low priority, carry-forward)
- **Severity**: Low
- **Area**: event-durability
- **Details**: `_emit()` helper in `test_execution_service.py:494` wraps `append_run_event` with `except Exception: pass`. Event loss non-critical but silent.

### R-0052: Legacy patch_revert.py compatibility exception is broad (MEDIUM)

- **Status**: Open (carry-forward)
- **Severity**: Medium
- **Area**: legacy-migration
- **Details**: `patch_apply.py:8c` calls `store_pre_apply_snapshot()` with broad except. Mandatory gate precedes it so apply cannot bypass, but dual snapshot writes are wasteful and confusing.

### New Findings — Steps 1135-1154 Baseline

### R-0053: patch.revert CLI routes through legacy revert_patch_intent() (BLOCKER)

- **Status**: Open
- **Severity**: Blocker
- **Area**: patch-revert
- **Details**: `apps/cli/commands/patch.py:174-176` calls `revert_patch_intent()` from `patch_revert.py`. Does NOT use `revert_repository_apply()` from `repository_snapshot.py`. Legacy path lacks drift detection, restore verification, and does not read DurableApplyRecord. New applies create both new-style and legacy snapshots; revert goes through legacy path only.
- **Evidence**: `patch.py:174`: `from packages.orchestration.patch_revert import format_revert_result, revert_patch_intent`
- **Block-if**: "public `patch.revert` still routes new applies through legacy patch_revert" + "legacy snapshots are silently reverted through weaker behavior"

### R-0054: revert_repository_apply() uses bypass booleans instead of loading real permissions/contract (BLOCKER)

- **Status**: Open
- **Severity**: Blocker
- **Area**: permission / run-contract
- **Details**: `repository_snapshot.py:894-895` takes `permitted: bool = True` and `contract_allows_revert: bool = True` with permissive defaults. The service does NOT load the Job, does NOT check `is_allowed(job, Capability)`, does NOT load/evaluate the persisted RunContract. Any caller can bypass both gates by omitting the arguments.
- **Evidence**: `repository_snapshot.py:894`: `permitted: bool = True`, line 895: `contract_allows_revert: bool = True`
- **Block-if**: "central revert trusts caller-supplied `permitted=True` or `contract_allows_revert=True`" + "permission or persisted RunContract is not enforced inside the central revert service" + "permission alone or contract alone is sufficient"

### R-0055: ContractAction.REVERT does not exist in canonical vocabulary (BLOCKER)

- **Status**: Open
- **Severity**: Blocker
- **Area**: run-contract
- **Details**: `run_contract.py:ContractAction` has PLAN, CONTEXT, BUILD_ARTIFACT, CREATE_PATCH_INTENT, CREATE_FIX_TASK, DISCOVER_COMMANDS, WRITE_METADATA, RUN_TEST, APPLY, SOURCE_APPLY, ARBITRARY_SHELL, APPLY_PATCH_WITHOUT_APPROVAL, MODIFY_PERMISSIONS, NETWORK_FETCH, INSTALL_PACKAGES, CLOUD_PROVIDER, PATCH_APPLY — but NO REVERT. Cannot enforce revert through `evaluate_run_action()`.
- **Evidence**: `grep -n "REVERT" run_contract.py` returns empty.
- **Block-if**: "revert action is absent from canonical RunContract vocabulary"

### R-0056: patch_apply.py still writes duplicate legacy snapshots for new applies (BLOCKER)

- **Status**: Open
- **Severity**: Blocker
- **Area**: legacy-migration
- **Details**: `patch_apply.py:206-207` calls `store_pre_apply_snapshot()` from `patch_revert.py` after the mandatory new-style snapshot. Creates two separate snapshot stores for every markdown apply. Wastes disk, confuses state model, enables legacy revert path.
- **Evidence**: `patch_apply.py:206`: `store_pre_apply_snapshot(job, intent_id, target_path, action, repo_root, data_dir=data_dir)`
- **Block-if**: "patch_apply still writes duplicate legacy snapshots for new applies"

### R-0057: Snapshot event persistence failures silently ignored (BLOCKER)

- **Status**: Open
- **Severity**: Blocker
- **Area**: event-durability
- **Details**: `repository_snapshot.py:305-306` — `_emit_snapshot_event()` has `except Exception: pass`. All 10 snapshot event types (create_started, create_completed, verified, revert_started, etc.) can fail silently. Operation truth remains accurate but event history can be incomplete without any signal.
- **Evidence**: `repository_snapshot.py:305`: `except Exception: pass`
- **Block-if**: "event persistence failure is silently ignored"

### R-0058: Proof Chain has no verified snapshot requirement for trusted apply (BLOCKER)

- **Status**: Open
- **Severity**: Blocker
- **Area**: proof
- **Details**: `proof_chain.py` has zero references to `snapshot`, `verified_snapshot`, `snapshot_verified`, `DurableApplyRecord`, or `RepositorySnapshot`. A `source_patch_applied` or `patch_intent_applied` event can satisfy the Proof Chain without any verified snapshot proof.
- **Evidence**: `grep -rn "snapshot" proof_chain.py` returns empty.
- **Block-if**: "Proof Chain can verify an apply without verified snapshot proof"

### R-0059: File Provenance does not track revert state from RepositorySnapshot (BLOCKER)

- **Status**: Open
- **Severity**: Blocker
- **Area**: provenance
- **Details**: `file_provenance.py` reads `patch_intent_apply_records` from artifact metadata (old legacy format). Does not check `DurableApplyRecord` from `repository_snapshot.py`. Reverted files using the new system would still appear as currently applied.
- **Evidence**: `file_provenance.py:120`: `records = artifact.metadata.get("patch_intent_apply_records", {})`
- **Block-if**: "reverted files still appear currently applied in File Provenance"

### R-0060: Readiness has no snapshot/apply_record verification (BLOCKER)

- **Status**: Open
- **Severity**: Blocker
- **Area**: readiness
- **Details**: `readiness.py` has zero references to `RepositorySnapshot`, `DurableApplyRecord`, `snapshot_verified`, manifest, or blob verification. A generic `snapshot_created` event alone could satisfy readiness without verifying manifest integrity, recovery blob presence, or apply linkage.
- **Evidence**: `grep -rn "snapshot" readiness.py` returns empty.
- **Block-if**: "readiness accepts snapshot events without verifying manifest, recovery data, and apply linkage"

## Baseline Check Matrix (Steps 1135-1154)

| Category | Status | Gap Count | Findings |
|---|---|---|---|
| Handoff truth | NOT YET TESTABLE | — | Worker hasn't started |
| Canonical revert | BLOCKER | R-0054, R-0055 | No REVERT action, bypass booleans |
| Public CLI | BLOCKER | R-0053 | Legacy routing |
| Source apply | OK | — | v2 working correctly |
| Legacy behavior | BLOCKER | R-0056 | Duplicate legacy snapshots |
| Event durability | BLOCKER | R-0057 | Silent exception in _emit_snapshot_event |
| State model | OK | — | applied/reverted states correct |
| Proof/Provenance | BLOCKER | R-0058, R-0059 | No snapshot integration |
| Progress/Feature/Review | NOT YET TESTABLE | — | — |
| Readiness | BLOCKER | R-0060 | No snapshot verification |
| CLI runtime | NOT YET TESTABLE | — | — |
| Tests | PENDING | — | After worker commits |

## Test Results
Last full run (Steps 1110-1134): 5227 passed, 0 failed, 8 skipped
Pre-existing failure: test_project_brain.py::test_full_chain_order (on main)
Next run: After worker commits Steps 1135+
