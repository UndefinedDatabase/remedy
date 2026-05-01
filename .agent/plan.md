# Plan

## Goal
Step 13.4: Final Context Count Fix

## Status
COMPLETE — committed, pushed

## Steps
1. [x] .agent/context.md: fix "455 tests" → "456 tests"
2. [x] test_task_registry.py: expand "# known ↔ has repo_route" comment to
       full v1 invariant + revisit note
3. [x] 456 tests pass; committed; pushed

## Branch
feature/step13-task-registry

## PR
#13 (open)

## Step-14 invariant
is_known_task_type ≡ repo_route is not None (v1).
Must revisit if non-repo known types are added.
