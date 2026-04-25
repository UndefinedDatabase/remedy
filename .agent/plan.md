# Plan

## Goal
Step 8.6: Repo Applicator Routing and Boundary Hotfix.

## Status
COMPLETE

## What Was Done
1. [x] Fix _REPO_PATH_RULES order: docs/remedy/ keywords before plain doc/documentation
       Fixes spec_document / planning_document / requirement_document routing to docs/remedy/
2. [x] Fix _write_to_repo: resolve repo_root internally before is_relative_to comparison
       Fixes false boundary violation when caller passes a symlinked path
3. [x] Add stale-path guard to apply_task_output_to_repo (return [] for invalid root)
       Enables direct behavioral tests without CLI/Ollama dependency
4. [x] 3 regression routing tests; symlink boundary test; stale tests replaced with behavioral
5. [x] Update .agent files; 253 tests passing; commit + push

## Key Decisions
- Continue on feature/step8-repo-attachment (PR Continuity Rule — in-scope hotfix)
- Routing: docs/remedy/ entries before plain docs/ entries in _REPO_PATH_RULES
- Boundary: repo_root.resolve() inside _write_to_repo; self-contained, caller-agnostic
- Stale guard: added to apply_task_output_to_repo itself; CLI check retained as depth

## Branch
feature/step8-repo-attachment
