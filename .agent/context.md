# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 269-276: Merge Gate Closure, Historical Suite Reconciliation, Source Apply Approval Gate.

## Current Problems
- (none — all prior findings resolved)

## Constraints
- No mutation endpoints, no shell=True, no 0.0.0.0
- No fake state, no optimistic LIVE
- React 19 + TypeScript + MUI + CSS Modules
- Redaction: no raw content in UI/API surfaces
- UI remains read-only
- source_apply requires job + intent_id (approved) before mutation
