# Plan — Steps 4396-4445: Promotion Integrity Closure v1

## Goal
Fix 6 promotion-integrity gaps found by review. All validation before
any target write. Universal persistence. Hash verification. Completeness
check. Skipped tracking. No partial apply.

## Current Step
Complete. All implementation, tests, verification done.

## Completed
- Artifact hash verification: SHA-256 of artifact bytes checked against manifest staged_hash
- Staged-file/artifact completeness: all staged_files must appear in manifest
- Skipped artifact tracking: persist_artifacts records skipped files with reasons
- Manifest format: {"artifacts": [...], "skipped": [...]} with old flat-list backward compat
- load_artifacts returns 3-tuple (entries, skipped, staged_dir)
- Universal persistence: every return path (_block, dry_run, promoted) calls _persist_promotion
- No partial apply: all validation (hash, blocked, baseline, unsupported) before any target write
- New PromotionResult fields: artifact_hash_mismatches, missing_artifacts, skipped_artifacts
- _block() helper centralizes blocked status + persistence
- 44 promotion tests (11 new): hash mismatch, missing artifact, skipped unsafe, no partial apply,
  dry-run persisted, no-approve persisted, blocked persisted, JSON integrity fields,
  skipped tracking, load_artifacts skipped, old manifest compat
- Full suite: 7381 passed, 0 failed (1 pre-existing deselected)
- Lint: clean
- Architecture guard: clean (subprocess.run in _run_post_test only, intentional)
- Dogfood smoke: 6/6 scenarios pass
