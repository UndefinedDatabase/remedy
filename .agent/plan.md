# Plan

## Goal
Step 5.6: CLI Hotfix and Final Pre-Step-6 Hardening.

## Status
COMPLETE. All 3 commits on feature/step5-task-execution (PR #6).

## What Was Done
1. Fix CLI: OllamaBuilder() moved inside try/except — bad env vars now show "Error: configuration"
2. annotate_planning_result: raise RuntimeError on changed=True but no artifact
3. BuilderOutput: proposed_changes requires min_length=1; 4 new tests added

## Key Decisions
- OllamaBuilder() construction raises ValueError on bad env vars from __init__,
  not from .build() — constructor must be inside try block to be caught
- annotate_planning_result now symmetric with annotate_task_result
- proposed_changes min_length=1: an empty list is not a valid execution result

## Branch
feature/step5-task-execution (PR #6) — in-scope per PR Continuity Rule
