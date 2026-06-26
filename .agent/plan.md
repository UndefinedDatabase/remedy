# Plan — Steps 4961-4974: Job Promote Safety Closure v1

## Goal
Close safety gaps in job promotion: remove workspace fallback, add symlink containment,
add target cleanliness guard, fix persistence failure handling, add redaction.

## Current Step
All implementation and tests complete. Awaiting commit.

## Completed
- Step 4961: Removed `_collect_workspace_files` fallback, require explicit apply manifests
- Step 4962: Added `_validate_source_containment` (symlinks, escapes, parent symlinks)
- Step 4963: Added `_validate_dest_containment` (target symlink escapes)
- Step 4964: Pre-approve target cleanliness guard (`_check_target_cleanliness`)
- Step 4965: Immediate recheck target cleanliness before each apply round
- Step 4966: Redaction via `_redact_json_value`, `_redact_secrets`, `_sanitize_path`
- Step 4967: `_persist_job_promotion` no longer swallows OSError; preflight writability check
- Step 4968: CLI command-path tests (approve, blocked JSON, blocked text)
- Step 4969: Target-clobber regression tests (dirty blocks, clean passes)
- Step 4970: Workspace symlink leakage regression tests (source, parent, dest)
- Step 4971: Missing apply manifest fallback regression tests (none, empty, pending)
- Step 4972: Existing job/evidence safety verified (123 evidence+promote tests pass)
- Step 4973: Architecture guard search clean (no shell=True, no git ops, no fallback)
- Step 4974: Final handoff

## Test Counts
- job_promote: 46 (was 31, +15 new)
- Full suite: 8022 passed (1 pre-existing skip in test_project_brain)
