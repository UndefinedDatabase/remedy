# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 277-282: Final Merge Close, Test Harness Honesty, Baseline Cleanup.

## Current Problems
- (none — all findings R-4001, R-4002, R-4003 resolved)

## Constraints
- No mutation endpoints, no shell=True, no 0.0.0.0
- No fake state, no optimistic LIVE
- React 19 + TypeScript + MUI + CSS Modules
- Redaction: no raw content in UI/API surfaces
- UI remains read-only
- source_apply requires job + intent_id (approved) before mutation
- No unittest.mock in production packages
