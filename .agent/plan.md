# Plan — F312 The scope guard knows orders without file names

## Goal
The scope guard tells three kinds of order apart and refuses a plan only for the kind that drew a
fence; an order that names no file gives a plan, not a failure
(`docs/roadmap/features/T2_F312.md`). Accepted PASS_WITH_RISKS on 2026-10-21.

## Current Step
Round 7 (session 1), the closing round: book round 6, register and resolve R-1382, resolve
R-1369, DECISION F312 D5 (no rotation this closure), accept F312 in STATUS with the README sync
and SU-066's `consumed_by`, and open the pull request, left unmerged.

## Next Steps
1. The next session: Phase 1 rule 1 (`.agent/STOP`), then the Open PR Gate merges F312's pull
   request; then Rule A5 proposes the next feature, F311.
2. The next findings paydown, F307, takes R-1375, R-1376 and R-1381 with the rest of the open set.

## Risks
- The integrity check fails on High findings F312 does not own (DECISION F310 D7, Q20).
