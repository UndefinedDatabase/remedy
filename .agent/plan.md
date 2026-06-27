# Plan — Steps 5037-5052: Pingpong Context Pack + Target Snapshot Symlink Closure v6

## Goal
Make pingpong context building, repo token estimation, and target snapshots
symlink-safe before the first single Remedy prompt dogfood.

## Current Step
All implementation and tests complete. Ready for commit.

## Completed
- Step 5037: `_is_safe_repo_path()` helper — symlink, parent walk, escape, regular file, readable, absolute path checks
- Step 5038: `build_repo_context()` file tree — `followlinks=False`, symlink dir prune, file symlink skip + safety note
- Step 5039: Mentioned file reads — validated via `_is_safe_repo_path()` before read, placeholder on unsafe
- Step 5040: README read — validated via `_is_safe_repo_path()` before read, safety note on unsafe
- Step 5041: `_snapshot_target()` — `followlinks=False`, symlink dir prune, file symlink skip, `_is_safe_repo_path()` check
- Step 5042: `_estimate_full_repo_tokens()` — `followlinks=False`, symlink dir prune, file symlink skip, `_is_safe_repo_path()` check
- Step 5043: README symlink context leak tests (4 tests)
- Step 5044: Mentioned file symlink context leak tests (4 tests)
- Step 5045: Context file tree symlink behavior tests (4 tests)
- Step 5046: `_snapshot_target()` symlink safety tests (5 tests)
- Step 5047: Token estimate symlink safety tests (4 tests)
- Step 5048: run_pingpong prompt no-leak integration tests (3 tests)
- Step 5049: Staging/safe-diff/workspace-apply/promote symlink safety preserved — 165 pingpong, 74 promote, 187 runner tests pass
- Step 5050: Job/evidence/runner safety preserved — 423 orchestration, 8097 full suite
- Step 5051: Architecture guard clean — no followlinks=True, no shutil.copy2 in pingpong, no git subprocess, no os.symlink, no shell=True
- Step 5052: Handoff — awaiting 5-minute quiet window

## Test Counts
- pingpong_cli: 165 (was 135, +30 new)
- job_task_runner: 187 (unchanged)
- job_promote: 74 (unchanged)
- job_evidence: 53 (unchanged)
- job_fulfillment: 109 (unchanged, ×2)
- fast lane: 571
- runtime: 4/4 suites
- Full suite: 8097 passed, 8 skipped, 0 failed
