# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 283-288: Full Repo Baseline Reconciliation, Stale Historical Tests, Final Merge Honesty.

## Current Problems
- (none — R-5001 and R-5002 resolved, full baseline green)

## Constraints
- No mutation endpoints, no shell=True, no 0.0.0.0
- No fake state, no optimistic LIVE
- React 19 + TypeScript + MUI + CSS Modules
- Redaction: no raw content in UI/API surfaces
- UI remains read-only
- source_apply requires job + intent_id (approved) before mutation
- No unittest.mock in production packages
- Dashboard is version 3
- Graph architecture is Canvas/Force (not React Flow)

## Recommended Next Block
Project Memory integration into Planning/Execution pipeline.
