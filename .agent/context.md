# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 289-296: Test suite re-architecture, source apply transactionality, dashboard truth, frontend fixes, truncation metadata.

## Current Problems
- (none — full baseline green, all guardrails pass)

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
- Test files use domain directories (tests/orchestration/, tests/ui_server/, etc.) — no step-numbered files

## Recommended Next Block
Project Memory integration into Planning/Execution pipeline.
