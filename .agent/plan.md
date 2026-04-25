# Plan

## Goal
Step 9: Permission Model v1 for Controlled Execution.

## Status
COMPLETE

## What Was Done
1. [x] Create packages/orchestration/permissions.py
       Capability enum (workspace_write, repo_generated_write, repo_overwrite, shell_exec)
       _DEFAULTS (only workspace_write allowed), is_allowed(), set_permission()
2. [x] Add check_and_apply_to_repo() to repo_applicator.py
       Permission-gated apply: checks repo_generated_write, annotates artifact on denial
3. [x] Update CLI: set-permission command (allow|deny + capability validation)
       Use check_and_apply_to_repo in run-next-task-local
4. [x] Create tests/test_permissions.py (28 tests: defaults, set_permission, is_allowed, enum)
5. [x] Update tests/test_repo_applicator.py (8 new tests for check_and_apply_to_repo)
6. [x] Update README.md: Step 9 section, fix Step 8 keyword table
7. [x] Update docs/architecture.md: Permission Model v1, fix Step 8 keyword table
8. [x] Update .agent files; 281 tests passing; commit + push + PR

## Key Decisions
- New branch (feature/step9-permission-model): clearly different purpose from Step 8
- Capability as str, Enum: invalid values raise ValueError at construction
- workspace_write allowed by default; repo_generated_write/repo_overwrite/shell_exec denied
- check_and_apply_to_repo in repo_applicator.py: permission gate + annotation
- repo_overwrite + shell_exec: reserved, defined, no effect yet
- Task completion: always verifier-based, never repo-application-based

## Branch
feature/step9-permission-model
