# Plan — Steps 135-140

## Goal
Do-direct contract fix, autocoder fake-E2E closure, smoke gates, honest dev status, next-action surface, commit-readiness preview.

## Current Step
All steps complete. Final commit.

## Steps
- [x] Step 135: `remedy do "<goal>"` direct contract — `"do": "run"` added to `_DEFAULT_COMMAND`
- [x] Step 136: Autocoder fake-E2E — calc.py starts wrong (`a - b`), fixed via structured patch modify
- [x] Step 137: Both smoke gates pass (built-in + external safe-smoke)
- [x] Step 138: `remedy dev status --json` reports honest `latest_smoke` object (not flat bool)
- [x] Step 139: `build_next_action()` surface with `/api/jobs/<id>/next-action` endpoint
- [x] Step 140: `remedy repo commit-readiness <job_id> --json` — read-only, no git writes

## Tests
- 41 new tests in test_steps_135_140.py
- 3244 total tests passing
- Frontend builds clean (Vite)
