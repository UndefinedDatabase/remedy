# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 261-268: False PASS Cleanup, Real Dashboard Truth, Runtime Test Closure.

## Current Problems
- UI fetches 5 scattered endpoints, not /dashboard as primary
- Empty jobs get demo_mode=true and synthetic_count=4 (should be false/0)
- No Vitest test script or real frontend behavior tests
- source_apply.py allows job=None bypass
- TestRunRecord lacks output_truncated/original_output_bytes metadata
- command_discovery CLI tests may timeout in external verification
- live_review says PASS but issues remain
- Broad `except Exception` in _build_guide_json and _build_context_budget_json

## Constraints
- No mutation endpoints, no shell=True, no 0.0.0.0
- No fake state, no optimistic LIVE
- React 19 + TypeScript + MUI + CSS Modules
- Redaction: no raw content in UI/API surfaces
- UI remains read-only
