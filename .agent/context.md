# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 297-304: Post-rearchitecture polish, source apply cleanup, project memory integration.

## Completed
- Test re-architecture (25 step files → 19 domain suites, 97 class renames)
- Rollback consolidation (R-6007/R-6008 resolved)
- Memory planning integration (approved memory → planner prompt)
- Memory execution integration (approved memory → TaskExecutionContext)
- Memory event/visibility (project_memory_recalled events, dashboard)
- Memory safety coverage (14 regression tests)

## Current Problems
- R-7001: Duplicate imports in 15/24 domain test files (cosmetic)

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
- Test files use domain directories — no step-numbered files or class names
- Memory: approved-only, bounded, redacted, no raw leaks

## Recommended Next Block
Steps 305-312 — Event-Ledger Replay And Checkpoint Resume
