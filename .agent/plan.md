# Plan — Steps 127-134

## Goal
Contract closure, smoke closure, runtime hygiene, UX interaction grounding, autocoder fake-E2E closure.

## Current Step
All steps complete. Final commit.

## Steps
- [x] Step 127: Task progress version 2→1 (stable contract for external smoke)
- [x] Step 128: Smoke has task-progress + node-detail API validation
- [x] Step 129: --no-open prevents browser launch, smoke uses HTTP only
- [x] Step 130: Worker unload errors filter fixed (R-0404), missing tools handled
- [x] Step 131: UX contracts verified — zoom 0 = 1 node, labels controlled, fullGraphMode=false default
- [x] Step 132: Node detail has job_id + status fields, edge meanings verified, no raw leaks
- [x] Step 133: Autocoder calc.py E2E path verified — structured patch → source apply → test → proof
- [x] Step 134: `remedy dev status --json` command added

## Tests
- 62 new tests in test_steps_127_134.py
- 3203 total tests passing
- Frontend builds clean (Vite)
